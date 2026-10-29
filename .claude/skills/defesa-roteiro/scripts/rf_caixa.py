"""Roteiro de falas: caixa com borda e faixa de parte."""
from rf_util import *  # noqa: F401,F403


def add_styled_box(doc, title: str, bg_hex: str, border_hex: str, title_color: RGBColor, items: list):
    """Cria uma caixa com borda esquerda grossa e conteúdo estruturado."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    set_cell_bg(cell, bg_hex)
    set_cell_margins(cell, top=90, bottom=90, left=160, right=140)
    set_cell_borders(
        cell,
        left=("single", 24, border_hex),
        top=("single", 4, HEX_BORDER),
        bottom=("single", 4, HEX_BORDER),
        right=("single", 4, HEX_BORDER),
    )
    prevent_row_split(tbl.rows[0])

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(title)
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(9.5)
    r0.font.color.rgb = title_color

    for item in items:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if isinstance(item, str):
            r = p.add_run(item)
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.font.color.rgb = C_INK
        elif isinstance(item, tuple) and len(item) == 2:
            speaker, text = item
            r_sp = p.add_run(f"• {speaker}: ")
            r_sp.bold = True
            r_sp.font.name = "Calibri"
            r_sp.font.size = Pt(10)
            r_sp.font.color.rgb = C_BRUNO if "Bruno" in speaker else (C_VICTOR if "Victor" in speaker else C_NAVY)
            r_tx = p.add_run(text)
            r_tx.font.name = "Calibri"
            r_tx.font.size = Pt(10)
            r_tx.font.color.rgb = C_INK
        elif isinstance(item, tuple) and len(item) == 3:
            speaker, text, w_info = item
            paras = [p_it.strip() for p_it in text.split("\n\n") if p_it.strip()]
            for p_idx, p_txt in enumerate(paras):
                p_elem = p if p_idx == 0 else cell.add_paragraph()
                if p_idx > 0:
                    p_elem.paragraph_format.space_before = Pt(2)
                    p_elem.paragraph_format.space_after = Pt(3)
                    p_elem.paragraph_format.line_spacing = 1.15
                if p_idx == 0:
                    r_sp = p_elem.add_run(f"[{speaker}] ")
                    r_sp.bold = True
                    r_sp.font.name = "Calibri"
                    r_sp.font.size = Pt(10.5)
                    r_sp.font.color.rgb = C_BRUNO if "Bruno" in speaker else C_VICTOR
                r_tx = p_elem.add_run(f"“{p_txt}”" if len(paras) == 1 else p_txt)
                r_tx.font.name = "Calibri"
                r_tx.font.size = Pt(10.5)
                r_tx.font.color.rgb = C_INK
                if p_idx == len(paras) - 1:
                    r_w = p_elem.add_run(f"   {w_info}")
                    r_w.font.name = "Calibri"
                    r_w.font.size = Pt(8.5)
                    r_w.font.color.rgb = C_MUTED

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(3)


def add_part_banner(doc, title: str, subtitle: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.color.rgb = C_NAVY

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.keep_with_next = True
    r2 = p2.add_run(subtitle)
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_MUTED
