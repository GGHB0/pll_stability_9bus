"""Guia de estudos: equação, tabela, figura, instante e faixa de slide."""
from gw_util import *  # noqa: F401,F403
from gw_util import _mathtext_image  # noqa: F401


class _Blocos:
    def eq(self, tex: str, tag: str = None, onde: str = None):
        buf, w_pt, h_pt = _mathtext_image(tex, fontsize=13.5, dpi=300)
        tbl = self.doc.add_table(rows=1, cols=2 if tag else 1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0 = tbl.cell(0, 0)
        set_cell_bg(c0, "F4F7F9")
        set_cell_margins(c0, top=80, bottom=80, left=140, right=100)
        c0.width = Cm(14.8 if tag else 17.0)

        tcPr = c0._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        left_b = OxmlElement("w:left")
        left_b.set(qn("w:val"), "single")
        left_b.set(qn("w:sz"), "18")
        left_b.set(qn("w:color"), "1A4A6E")
        tcBorders.append(left_b)
        tcPr.append(tcBorders)

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r_img = p0.add_run()
        # Limitar largura máxima a 13.5 cm mantendo proporção
        w_cm = min(13.5, w_pt * 2.54 / 72.0)
        r_img.add_picture(buf, width=Cm(w_cm))

        if tag:
            c1 = tbl.cell(0, 1)
            set_cell_bg(c1, "F4F7F9")
            set_cell_margins(c1, top=80, bottom=80, left=40, right=100)
            c1.width = Cm(2.2)
            c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p1 = c1.paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p1.paragraph_format.space_after = Pt(0)
            rt = p1.add_run(f"({tag})")
            rt.font.name = "Arial"
            rt.font.size = Pt(9.5)
            rt.font.color.rgb = C_MUTED

        if onde:
            p_onde = self.doc.add_paragraph()
            p_onde.paragraph_format.left_indent = Cm(0.4)
            p_onde.paragraph_format.space_before = Pt(2)
            p_onde.paragraph_format.space_after = Pt(5)
            p_onde.paragraph_format.line_spacing = 1.12
            add_rich_runs(p_onde, onde, base_size=9.0, base_color=C_MUTED)
        else:
            self.gap(4)

    def table(self, headers: list, rows: list, widths_cm: list = None):
        tbl = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="C7D2DA", sz="4")

        # Escalar larguras de 14.7 cm (PDF) para 17.0 cm (Word)
        scaled_w = None
        if widths_cm:
            tot = sum(widths_cm)
            scaled_w = [w * 17.0 / tot for w in widths_cm]

        hdr_cells = tbl.rows[0].cells
        for i, h_text in enumerate(headers):
            set_cell_bg(hdr_cells[i], "1A4A6E")
            set_cell_margins(hdr_cells[i], top=75, bottom=75, left=100, right=100)
            hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = hdr_cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            add_rich_runs(p, h_text, base_size=9.2, base_color=C_WHITE, base_bold=True)

        for r_idx, row_data in enumerate(rows):
            row_cells = tbl.rows[r_idx + 1].cells
            bg = "F4F7F9" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                set_cell_bg(row_cells[c_idx], bg)
                set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
                row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = row_cells[c_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.12
                add_rich_runs(p, str(val), base_size=9.2, base_color=C_INK, base_bold=(c_idx == 0 and len(str(val)) < 35))

        if scaled_w:
            for row in tbl.rows:
                for i, w in enumerate(scaled_w):
                    row.cells[i].width = Cm(w)

        self.gap(5)

    def figura(self, img_path: Path, legenda: str = None, largura_cm: float = 15.2):
        if img_path and Path(img_path).exists():
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            r = p_img.add_run()
            r.add_picture(str(img_path), width=Cm(min(16.5, largura_cm)))
        if legenda:
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(6)
            add_rich_runs(p_cap, legenda, base_size=8.8, base_color=C_MUTED, base_italic=True)

    def instante(self, quando: str, titulo: str, primeiro: str):
        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        c0.width = Cm(3.4)
        c1.width = Cm(13.6)
        set_cell_bg(c0, "1A4A6E")
        set_cell_bg(c1, "E7EFF6")
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=120, right=100)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        add_rich_runs(p0, quando, base_size=8.8, base_color=C_WHITE, base_bold=True)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        add_rich_runs(p1, titulo, base_size=10.2, base_color=C_ACCENT, base_bold=True)
        self.p(primeiro)

    def ponte(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        add_rich_runs(p, f"&#8594; <b>Próximo:</b> <i>{text}</i>", base_size=9.8, base_color=C_MUTED)

    def faixa(self, rotulo: str, num: int, titulo: str, meta: str, imagem: Path = None, legenda: str = None):
        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        c0.width = Cm(2.3)
        c1.width = Cm(14.7)
        set_cell_bg(c0, "1A4A6E" if rotulo == "SLIDE" else "0F766E")
        set_cell_bg(c1, "F4F7F9")
        set_cell_margins(c0, top=80, bottom=80, left=60, right=60)
        set_cell_margins(c1, top=80, bottom=80, left=140, right=100)
        c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r_rot = p0.add_run(f"{rotulo}\n")
        r_rot.bold = True
        r_rot.font.name = "Arial"
        r_rot.font.size = Pt(8.5)
        r_rot.font.color.rgb = C_WHITE
        r_num = p0.add_run(f"{num:02d}" if isinstance(num, int) else str(num))
        r_num.bold = True
        r_num.font.name = "Arial"
        r_num.font.size = Pt(18)
        r_num.font.color.rgb = C_WHITE

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(2)
        add_rich_runs(p1, titulo, base_size=13.5, base_color=C_ACCENT, base_bold=True)
        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        add_rich_runs(p2, meta, base_size=9.0, base_color=C_MUTED)

        if imagem and Path(imagem).exists():
            self.figura(imagem, legenda=legenda, largura_cm=15.0)
        else:
            self.gap(4)
