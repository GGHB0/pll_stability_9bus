"""Roteiro de falas: um slide ou capítulo (cabeçalho, pontos, falas)."""
from rf_caixa import add_styled_box
from rf_util import *  # noqa: F401,F403


def add_item_section(doc, item: dict, clock_start: int, clock_end: int):
    """Renderiza um Slide ou Capítulo do Painel com cabeçalho, pontos principais e falas."""
    is_palco = item["tipo"] == "PAINEL"
    badge_bg = HEX_PANEL if is_palco else HEX_NAVY
    badge_label = f"PAINEL CAP. {item['num']}" if is_palco else f"SLIDE {item['num']:02d}"

    total_words = sum(count_words(t) for _, t in item["falas"])
    read_s = int(round(total_words / 130.0 * 60))

    # 1. Faixa de cabeçalho
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c0, c1 = tbl.rows[0].cells
    c0.width = Cm(3.2)
    c1.width = Cm(13.8)
    set_cell_bg(c0, badge_bg)
    set_cell_bg(c1, HEX_SUB)
    set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
    set_cell_margins(c1, top=80, bottom=80, left=140, right=120)
    set_cell_borders(c0)
    set_cell_borders(c1, top=("single", 4, HEX_BORDER), bottom=("single", 4, HEX_BORDER), right=("single", 4, HEX_BORDER))
    c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    prevent_row_split(tbl.rows[0])

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    r_b = p0.add_run(badge_label)
    r_b.bold = True
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(11)
    r_b.font.color.rgb = C_WHITE

    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    r_t = p1.add_run(item["titulo"])
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = C_NAVY

    p2 = c1.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    meta_str = (
        f"{item['bloco']}   |   Oradores: {item['quem']}   |   "
        f"{total_words} palavras (~{fmt_dur(read_s)} leitura / Alvo: {fmt_dur(item['dur_s'])})   |   "
        f"Relógio: {fmt_mmss(clock_start)} → {fmt_mmss(clock_end)}"
    )
    if is_palco and item.get("reserva"):
        meta_str += f"   |   Reserva: {item['reserva']}"
    r_m = p2.add_run(meta_str)
    r_m.font.name = "Calibri"
    r_m.font.size = Pt(8.5)
    r_m.font.color.rgb = C_MUTED

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(2)

    # 2. Caixa combinada: Mensagem Central + Pontos Principais a Comentar
    pts_items = [("Mensagem-chave", item["msg"])] + item["pontos"]
    add_styled_box(
        doc,
        "PONTOS PRINCIPAIS A COMENTAR (O QUE EXPLICAR E APONTAR NA TELA)",
        HEX_PTS_BG,
        HEX_PTS_BD,
        C_ORANGE,
        pts_items,
    )

    # 3. Caixa de Falas Cronometradas
    fala_items = []
    for speaker, text in item["falas"]:
        w = count_words(text)
        s = int(round(w / 130.0 * 60))
        fala_items.append((speaker, text, f"({w} pal. · ~{s}s)"))

    add_styled_box(
        doc,
        "FALA SUGERIDA CRONOMETRADA (ENSAIO PASSO A PASSO)",
        HEX_PALCO_BG if is_palco else HEX_FALA_BG,
        HEX_PALCO_BD if is_palco else HEX_FALA_BD,
        C_VICTOR if is_palco else C_BLUE,
        fala_items,
    )

    # 4. Linha rápida de atenção/ponte
    if item.get("atencao"):
        pa = doc.add_paragraph()
        pa.paragraph_format.space_before = Pt(0)
        pa.paragraph_format.space_after = Pt(8)
        ra1 = pa.add_run("⚡ Atenção / Transição: ")
        ra1.bold = True
        ra1.font.name = "Calibri"
        ra1.font.size = Pt(9)
        ra1.font.color.rgb = C_ORANGE
        ra2 = pa.add_run(item["atencao"])
        ra2.font.name = "Calibri"
        ra2.font.size = Pt(9)
        ra2.font.color.rgb = C_MUTED
