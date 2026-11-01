"""Roteiro de estudo (PDF): caixas, faixas de slide/capítulo e figuras."""
from pdf_base import *  # noqa: F401,F403
from pdf_base import _style  # noqa: F401


def box(kind, *paras, titulo=None):
    """Caixa colorida de uma célula só: o reportlab não parte tabela de uma linha,
    então a caixa nunca fica com o título numa página e o texto na outra."""
    bg, bar, rot = KIND[kind]
    estilo = S_MSG if kind == "msg" else S_BOX
    conteudo = [Paragraph(f"<font color='{bar}'>{titulo or rot}</font>", S_BOXT)]
    for p_ in paras:
        conteudo += [Spacer(1, 3), Paragraph(p_, estilo)]
    t = Table([[conteudo]], colWidths=[W * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor(bar)),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    n.story.append(t)
    n.gap(8)


def sub(text):
    n.story.append(Paragraph(text, S_SUB))


def bul(*items):
    for it in items:
        n.story.append(Paragraph(it, S_BUL, bulletText="•"))
    n.gap(3)


def eq(tex, tag=None, onde=None):
    n.eq_tex(tex, tag, fontsize=12.5)
    if onde:
        n.story.append(Paragraph(onde, S_ONDE))
    else:
        n.gap(7)


def tab(header, rows, widths):
    n.table(header, rows, widths)
    if len(rows) <= 6:  # tabela curta não se parte entre páginas
        bloco = [n.story.pop()]
        anterior = n.story[-1] if n.story else None
        if isinstance(anterior, Paragraph) and getattr(anterior.style, "keepWithNext", 0):
            bloco.insert(0, n.story.pop())  # título vai junto com a tabela
        n.story.append(KeepTogether(bloco))
    n.gap(8)


def nums(rows):
    tab(["Número", "O que é"], rows, [3.9, 10.8])


def figura(caminho, legenda, largura=W):
    with Image.open(caminho) as im:
        h = largura * cm * im.height / im.width
    img = RLImage(str(caminho), width=largura * cm, height=h)
    img.hAlign = "CENTER"
    n.story.append(KeepTogether([img, Spacer(1, 3), Paragraph(legenda, n.s_tag)]))
    n.gap(6)


S_INST = _style("inst", fontName="TNR-Bold", fontSize=11, leading=13.5, textColor=ACCENT,
                spaceAfter=0)


def instante(quando, titulo, primeiro):
    """Selo do instante, título do passo e o primeiro parágrafo, sempre na mesma página."""
    t = Table([[Paragraph(quando, S_BAND_L), Paragraph(titulo, S_INST)]],
              colWidths=[3.1 * cm, (W - 3.1) * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), ACCENT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LINEBELOW", (1, 0), (1, 0), 0.6, ACCENT),
    ]))
    n.story.append(KeepTogether([Spacer(1, 8), t, Spacer(1, 5),
                                 Paragraph(primeiro, n.s_body)]))


def ponte(text):
    # prende a ponte ao bloco anterior (caixa + espaçador): sem linha solta na página seguinte
    ultimos = [n.story.pop(), n.story.pop()][::-1]
    n.story.append(KeepTogether(ultimos + [Paragraph(f"&#8594; <b>Próximo:</b> {text}",
                                                     S_PONTE)]))


PARTE = []  # título e abertura de parte, impressos na página do próximo slide


def parte(titulo, *paras):
    PARTE.extend([Paragraph(titulo, n.s_h)] + [Paragraph(x, n.s_body) for x in paras])


def faixa(rotulo, num, titulo, meta, imagem=None, alt=6.0, legenda=None):
    """Faixa de título e miniatura juntas; página nova só se não couberem com folga
    (sobra de um slide curto não vira página quase vazia)."""
    n.story.append(CondPageBreak((alt + 4.5) * cm))
    n.story.extend(PARTE)
    PARTE.clear()
    band = Table([[[Paragraph(rotulo, S_BAND_L), Paragraph(str(num), S_BAND_N)],
                   [Paragraph(titulo, S_BAND_T), Paragraph(meta, S_BAND_M)]]],
                 colWidths=[2.1 * cm, (W - 2.1) * cm])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), ACCENT),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#F4F7F9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    bloco = [band]
    if imagem:
        with Image.open(imagem) as im:
            asp = im.height / im.width
        w = W * cm
        h = w * asp
        if h > alt * cm:
            h = alt * cm
            w = h / asp
        img = RLImage(str(imagem), width=w, height=h)
        img.hAlign = "CENTER"
        bloco += [Table([[img]], colWidths=[W * cm], style=TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))]
        if legenda:
            bloco.append(Paragraph(legenda, n.s_tag))
    n.story.append(KeepTogether(bloco))
    n.gap(10)


def slide(num, titulo, bloco, quem, tcc):
    faixa("SLIDE", num, titulo, f"{bloco} &#160;·&#160; Fala: {quem} &#160;·&#160; No TCC: {tcc}",
          jpg(SLIDES_PNG / f"s{num:02d}.png"))


def cap(num, titulo, ref, png, legenda):
    faixa("PAINEL", num, titulo, ref, jpg(PALCO_PNG / png), alt=7.8, legenda=legenda)


def imagem_palco(png, legenda, alt=8.6):
    n.image(jpg(PALCO_PNG / png), width_cm=W, max_height_cm=alt, caption=legenda)
