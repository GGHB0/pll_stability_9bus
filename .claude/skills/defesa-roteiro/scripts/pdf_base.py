"""Roteiro de estudo (PDF): imagens, nota e estilos locais."""
from pathlib import Path


from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.platypus import (CondPageBreak, Image as RLImage, KeepTogether, Paragraph, Spacer, Table,
                                TableStyle)
from caminhos import CACHE, OUTPUT, PALCO_PNG, RAP_PDF, ROOT, SLIDES_PNG  # noqa: F401
from pdfnote import ACCENT, MUTED, Note, _style, render_preview  # noqa: E402,F401

CACHE.mkdir(parents=True, exist_ok=True)
W = 14.7  # largura útil em cm


def jpg(src: Path, largura=1300) -> Path:
    """Cópia JPEG reduzida da imagem (cache por nome e data)."""
    dst = CACHE / (src.parent.name + "_" + src.stem + ".jpg")
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        with Image.open(src) as im:
            im = im.convert("RGB")
            if im.width > largura:
                im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=86, optimize=True)
    return dst


def rap_fig(nome, pagina, clip) -> Path:
    """Recorte de uma figura do RAP-ONS 00012/2023 (página 1-based, clip em pt)."""
    dst = CACHE / f"rap_{nome}.jpg"
    if not dst.exists():
        import pymupdf
        with pymupdf.open(RAP_PDF) as d:
            pix = d[pagina - 1].get_pixmap(dpi=220, clip=pymupdf.Rect(*clip))
            png = CACHE / f"rap_{nome}.png"
            pix.save(png)
        with Image.open(png) as im:
            im.convert("RGB").save(dst, "JPEG", quality=88, optimize=True)
        png.unlink()
    return dst


n = Note(
    title="Roteiro de estudo da defesa",
    subtitle="Slide a slide e capítulo a capítulo, na ordem em que a apresentação acontece "
             "(PPTX, painel HTML e de volta ao PPTX), com os fundamentos de cada tema",
    out=OUTPUT / "roteiro_estudo_defesa.pdf",
    meta_left="Victor e Bruno<br/>Comportamento do SRF-PLL de inversores frente a contingências",
    meta_right="Material de estudo<br/>25 de outubro de 2026",
    running_head="Roteiro de estudo da defesa",
)

# ------------------------------------------------------------------ estilos locais
S_BOXT = _style("boxt", fontName="TNR-Bold", fontSize=8.6, leading=11, spaceAfter=0)
S_BOX = _style("box", fontSize=10.3, leading=14.4, spaceAfter=0, alignment=TA_JUSTIFY)
S_MSG = _style("msg", fontName="TNR-Bold", fontSize=12.2, leading=16.2, spaceAfter=0,
               textColor=ACCENT)
S_SUB = _style("sub", fontName="TNR-Bold", fontSize=11.3, leading=14.5, textColor=ACCENT,
               spaceBefore=8, spaceAfter=4, keepWithNext=1)
S_BUL = _style("bul", leftIndent=15, bulletIndent=4, spaceAfter=3.5, alignment=TA_JUSTIFY)
S_ONDE = _style("onde", fontSize=9.4, leading=12.8, textColor=MUTED, leftIndent=12,
                spaceAfter=7, alignment=TA_JUSTIFY)
S_PONTE = _style("ponte", fontName="TNR-Italic", fontSize=10.3, leading=14,
                 textColor=MUTED, spaceBefore=4)
S_BAND_L = _style("bandl", fontName="TNR-Bold", fontSize=8.5, leading=10,
                  textColor=colors.white, spaceAfter=0, alignment=1)
S_BAND_N = _style("bandn", fontName="TNR-Bold", fontSize=22, leading=24,
                  textColor=colors.white, spaceAfter=0, alignment=1)
S_BAND_T = _style("bandt", fontName="TNR-Bold", fontSize=15, leading=18, textColor=ACCENT,
                  spaceAfter=1)
S_BAND_M = _style("bandm", fontSize=9.2, leading=12, textColor=MUTED, spaceAfter=0)

KIND = {  # fundo, barra, rótulo
    "msg": ("#E7EFF6", "#1A4A6E", "MENSAGEM"),
    "banca": ("#EDF4FB", "#2F6FA8", "PERGUNTA DO RODAPÉ DO SLIDE"),
    "prova": ("#F3EEF8", "#6B4C9A", "PERGUNTA PROVÁVEL DA BANCA"),
    "cuidado": ("#FDF3E1", "#C27C0E", "CUIDADO"),
    "alem": ("#EAF4EC", "#3D8A57", "ALÉM DO TCC · para entender e responder, não para a fala"),
    "passo": ("#F4F7F9", "#5A6B78", "PASSOS DO CAPÍTULO"),
    "fala": ("#FBF6EC", "#8A6D3B", "O QUE FALAR · tópicos para dizer com as suas palavras"),
    "base": ("#EEF2F7", "#34495E", "RELEMBRANDO CONTROLE · em uma frase"),
}
