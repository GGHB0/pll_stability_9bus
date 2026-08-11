# -*- coding: utf-8 -*-
"""Notas tecnicas em PDF do projeto pll_stability_9bus.

Uso minimo:

    from pdfnote import Note, XI, WN, SQ
    n = Note("Titulo", "Subtitulo", out="output/nota.pdf")
    n.h("1. Seccao"); n.p("texto"); n.eq(f"K = 2{XI}{WN}", "1")
    n.refs(["SOBRENOME, Nome. Titulo. Editora, ano."])
    n.build()

Regras aprendidas (nao mexer sem motivo):
- Fonte Times New Roman via TTF: as fontes embutidas do reportlab nao tem grego.
- Nunca usar o atributo `rise` em <sub>/<super>: desalinha o avanco horizontal.
- Nao usar U+2713 (check): ausente no Times New Roman. Grego, seta, raiz e
  aproximadamente estao todos presentes.
- `eq_tex()` (mathtext do matplotlib, fontes STIX) e o modo recomendado para
  qualquer formula com fracao, raiz de expressao, soma/integral ou mais de um
  nivel de sub/sobrescrito. `eq()` (Paragraph com entidades HTML) fica so
  para simbolo isolado ou substituicao trivial de uma variavel.
"""
import io
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image as RLImage, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

# simbolos prontos (todos conferidos no cmap do Times New Roman)
W, XI, SQ, AP, AR, DL, TAU = "ω", "ξ", "√", "≈", "→", "δ", "τ"
WN, W0 = "ω<sub>n</sub>", "ω<sub>0</sub>"
MINUS = "&#8722;"

INK = colors.HexColor("#14232E")
ACCENT = colors.HexColor("#1A4A6E")
RULE = colors.HexColor("#C7D2DA")
BOXBG = colors.HexColor("#F4F7F9")
MUTED = colors.HexColor("#5A6B78")

_FONTS = r"C:\Windows\Fonts"
_registered = False


def _register_fonts():
    global _registered
    if _registered:
        return
    for alias, ttf in [("TNR", "times.ttf"), ("TNR-Bold", "timesbd.ttf"),
                       ("TNR-Italic", "timesi.ttf"), ("TNR-BoldItalic", "timesbi.ttf")]:
        pdfmetrics.registerFont(TTFont(alias, f"{_FONTS}\\{ttf}"))
    pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-Bold",
                                  italic="TNR-Italic", boldItalic="TNR-BoldItalic")
    _registered = True


def _mathtext_image(expr, fontsize=15, color="#14232E", dpi=300):
    """Renderiza `expr` (sintaxe LaTeX/mathtext, sem os `$`) num PNG com fundo
    transparente, recortado ao bounding box do glifo. Usa o backend Agg do
    matplotlib (sem display) e fontes STIX, desenhadas para casar
    metricamente com Times New Roman. Retorna (buffer_png, largura_pt,
    altura_pt) prontos para um reportlab Image."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image as PILImage

    fig = plt.figure(figsize=(0.1, 0.1))
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${expr}$", fontsize=fontsize, color=color,
              math_fontfamily="stix")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, transparent=True, bbox_inches="tight",
                pad_inches=0.06)
    plt.close(fig)
    buf.seek(0)
    with PILImage.open(buf) as im:
        px_w, px_h = im.size
    buf.seek(0)
    return buf, px_w * 72.0 / dpi, px_h * 72.0 / dpi


def _plain(text):
    """Texto puro para o canvas do rodape: canvas nao interpreta entidades nem tags."""
    import html
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", text)).replace("\xa0", " ")


def _style(name, **kw):
    base = dict(name=name, fontName="TNR", fontSize=10.5, leading=14.6,
                textColor=INK, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(**base)


class Note:
    """Monta uma nota tecnica de uma coluna, A4, com cabecalho e rodape."""

    def __init__(self, title, subtitle, out, meta_left=None, meta_right=None,
                 running_head=None, author="Victor Rezende", subject="TCC UERJ"):
        _register_fonts()
        self.out = Path(out)
        self.title = title
        self.running_head = _plain(running_head or title)
        self.author, self.subject = author, subject
        self.story = []
        self._init_styles()
        self._header(title, subtitle, meta_left, meta_right)

    def _init_styles(self):
        self.s_title = _style("t", fontName="TNR-Bold", fontSize=21, leading=25,
                              textColor=ACCENT, spaceAfter=2)
        self.s_sub = _style("sb", fontSize=12.5, leading=16, textColor=MUTED, spaceAfter=14)
        self.s_meta = _style("m", fontSize=9, leading=13, textColor=MUTED, spaceAfter=0)
        self.s_metaR = _style("mr", fontSize=9, leading=13, textColor=MUTED,
                              spaceAfter=0, alignment=TA_RIGHT)
        self.s_h = _style("h", fontName="TNR-Bold", fontSize=13, leading=16,
                          textColor=ACCENT, spaceBefore=12, spaceAfter=5)
        self.s_body = _style("b", alignment=TA_JUSTIFY)
        self.s_eq = _style("eq", fontName="TNR-Italic", fontSize=11, leading=17,
                           alignment=TA_CENTER, spaceAfter=0)
        self.s_tag = _style("tg", fontSize=9.5, alignment=TA_CENTER,
                            textColor=MUTED, spaceAfter=0)
        self.s_cell = _style("c", fontSize=9.5, leading=13, spaceAfter=0)
        self.s_head = _style("ch", fontName="TNR-Bold", fontSize=9.5, leading=13,
                             spaceAfter=0, textColor=colors.white)
        self.s_note = _style("n", fontSize=9.5, leading=14, textColor=MUTED,
                             alignment=TA_JUSTIFY, leftIndent=10)
        self.s_ref = _style("r", fontSize=9, leading=13, alignment=TA_JUSTIFY,
                            leftIndent=16, firstLineIndent=-16, spaceAfter=6)

    # ---------------------------------------------------------------- blocos
    def _header(self, title, subtitle, meta_left, meta_right):
        self.story.append(Paragraph(title, self.s_title))
        if subtitle:
            self.story.append(Paragraph(subtitle, self.s_sub))
        if meta_left or meta_right:
            t = Table([[Paragraph(meta_left or "", self.s_meta),
                        Paragraph(meta_right or "", self.s_metaR)]],
                      colWidths=[10.7 * cm, 4.0 * cm])
            t.setStyle(TableStyle([
                ("LINEABOVE", (0, 0), (-1, 0), 1.2, ACCENT),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("RIGHTPADDING", (-1, 0), (-1, -1), 0),
            ]))
            self.story.append(t)
            self.story.append(Spacer(1, 12))

    def h(self, text):
        self.story.append(Paragraph(text, self.s_h))

    def p(self, text):
        self.story.append(Paragraph(text, self.s_body))

    def note(self, text):
        self.story.append(Paragraph(text, self.s_note))

    def gap(self, pts=8):
        self.story.append(Spacer(1, pts))

    def pagebreak(self):
        """Quebra de pagina explicita: evita cabecalho de secao ou tabela
        orfaos no pe da pagina, sem depender de espacador com valor magico."""
        self.story.append(PageBreak())

    def _eq_box(self, inner, tag):
        if tag:
            data, widths = [[inner, Paragraph(f"({tag})", self.s_tag)]], [13.1 * cm, 1.6 * cm]
        else:
            data, widths = [[inner]], [14.7 * cm]
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), BOXBG),
            ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (0, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        self.story.append(t)

    def eq(self, text, tag=None):
        """Bloco de equacao em texto simples (Paragraph + entidades HTML):
        fundo claro, barra de destaque, numero opcional. Serve para simbolo
        isolado ou substituicao trivial de uma variavel. Para fracao, raiz de
        expressao, soma/integral ou sub/sobrescrito aninhado, usar eq_tex()."""
        self._eq_box(Paragraph(text, self.s_eq), tag)

    def eq_tex(self, expr, tag=None, fontsize=15):
        """Bloco de equacao com tipografia real via mathtext do matplotlib
        (fontes STIX, casam com Times): fracao com barra, raiz com vinculo,
        sub/sobrescrito aninhado, somatorio/integral. `expr` em sintaxe
        LaTeX/mathtext, SEM os `$` delimitadores — ex.:
        r"K_p = 2\\xi\\omega_n", r"\\sqrt{L_1 L_2 C}",
        r"\\frac{A}{\\pi\\,\\Delta f\\,T}". Cai para o modo texto (eq()) se a
        renderizacao falhar (parse invalido, glifo ausente)."""
        try:
            buf, w_pt, h_pt = _mathtext_image(expr, fontsize=fontsize)
            # ao contrario de Paragraph, uma Image nao quebra linha sozinha:
            # expressao comprida precisa ser reduzida pra caber na coluna.
            max_w = (12.3 if tag else 13.9) * cm
            if w_pt > max_w:
                scale = max_w / w_pt
                w_pt, h_pt = w_pt * scale, h_pt * scale
            img = RLImage(buf, width=w_pt, height=h_pt)
            img.hAlign = "CENTER"
            inner = img
        except Exception as exc:
            print(f"AVISO: eq_tex('{expr}') falhou ({exc!r}) - usando texto plano")
            inner = Paragraph(expr, self.s_eq)
        self._eq_box(inner, tag)

    def image(self, path, width_cm=None, caption=None, max_height_cm=9.0):
        """Insere um PNG/JPG centralizado na coluna util (14.7 cm) — grafico,
        captura de tela, diagrama exportado. Sem width_cm, ajusta a imagem a
        essa largura limitada a max_height_cm de altura (o que for mais
        restritivo). caption opcional aparece abaixo, centrado, como legenda
        (estilo s_tag, ja usado nos numeros de equacao)."""
        from PIL import Image as PILImage
        path = Path(path)
        with PILImage.open(path) as im:
            px_w, px_h = im.size
        aspect = px_h / px_w
        w = (width_cm or 14.7) * cm
        h = w * aspect
        max_h = max_height_cm * cm
        if h > max_h:
            h = max_h
            w = h / aspect
        img = RLImage(str(path), width=w, height=h)
        img.hAlign = "CENTER"
        self.story.append(img)
        if caption:
            self.story.append(Spacer(1, 5))
            self.story.append(Paragraph(caption, self.s_tag))
        self.gap(10)

    def table(self, header, rows, widths):
        """widths em cm; a soma util da coluna de texto e 14.7 cm."""
        data = [[Paragraph(h, self.s_head) for h in header]]
        data += [[Paragraph(c, self.s_cell) for c in r] for r in rows]
        t = Table(data, colWidths=[x * cm for x in widths], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BOXBG]),
            ("GRID", (0, 0), (-1, -1), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ]))
        self.story.append(t)

    def refs(self, entries, heading="Refer&#234;ncias"):
        self.h(heading)
        for e in entries:
            self.story.append(Paragraph(e, self.s_ref))

    # ---------------------------------------------------------------- saida
    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("TNR", 8.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(2.4 * cm, 1.35 * cm, self.running_head)
        canvas.drawRightString(A4[0] - 2.4 * cm, 1.35 * cm, str(doc.page))
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(2.4 * cm, 1.75 * cm, A4[0] - 2.4 * cm, 1.75 * cm)
        canvas.restoreState()

    def build(self):
        self.out.parent.mkdir(parents=True, exist_ok=True)
        doc = BaseDocTemplate(str(self.out), pagesize=A4,
                              leftMargin=2.4 * cm, rightMargin=2.4 * cm,
                              topMargin=2.2 * cm, bottomMargin=2.1 * cm,
                              title=_plain(self.title), author=self.author,
                              subject=self.subject)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
        doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=self._decorate)])
        doc.build(self.story)
        print(f"OK -> {self.out} ({self.out.stat().st_size} bytes)")
        return self.out


def render_preview(pdf_path, out_dir, scale=2):
    """Renderiza cada pagina em PNG para conferencia visual."""
    import pypdfium2 as pdfium
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    stem = Path(pdf_path).stem
    paths = []
    for i in range(len(pdf)):
        png = out_dir / f"{stem}_p{i + 1}.png"
        pdf[i].render(scale=scale).to_pil().save(png)
        paths.append(png)
    print(f"paginas: {len(pdf)}")
    return paths
