"""Guia de estudos: cabeçalho, títulos, parágrafos, listas e caixas."""
from gw_util import *  # noqa: F401,F403
from gw_util import _mathtext_image  # noqa: F401


class _Texto:
    def __init__(self, doc: Document):
        self.doc = doc
        self.s_body = "body"
        self.s_h = "h"
        self.s_tag = "tag"
        self.story = []  # dummy list para compatibilidade com KeepTogether/pop se necessário

    def add_header_banner(self, title: str, subtitle: str, meta_left: str, meta_right: str):
        p_kicker = self.doc.add_paragraph()
        p_kicker.paragraph_format.space_before = Pt(0)
        p_kicker.paragraph_format.space_after = Pt(2)
        rk = p_kicker.add_run("UERJ • FACULDADE DE ENGENHARIA • ENGENHARIA ELÉTRICA • DEFESA DE TCC (2026)")
        rk.bold = True
        rk.font.name = "Arial"
        rk.font.size = Pt(8.5)
        rk.font.color.rgb = C_ACCENT

        p_t = self.doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(3)
        rt = p_t.add_run(title)
        rt.bold = True
        rt.font.name = "Arial"
        rt.font.size = Pt(18)
        rt.font.color.rgb = C_ACCENT

        p_sub = self.doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(8)
        rs = p_sub.add_run(subtitle)
        rs.font.name = "Arial"
        rs.font.size = Pt(10.5)
        rs.font.color.rgb = C_MUTED

        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        set_cell_bg(c0, "F4F7F9")
        set_cell_bg(c1, "F4F7F9")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        c0.width = Cm(11.5)
        c1.width = Cm(5.5)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        add_rich_runs(p0, meta_left, base_size=9.0, base_color=C_MUTED)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(0)
        add_rich_runs(p1, meta_right, base_size=9.0, base_color=C_MUTED)
        self.gap(6)

    def h(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "10")
        bottom.set(qn("w:space"), "3")
        bottom.set(qn("w:color"), "1A4A6E")
        pBdr.append(bottom)
        pPr.append(pBdr)
        add_rich_runs(p, text, base_size=13.5, base_color=C_ACCENT, base_bold=True)

    def sub(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        add_rich_runs(p, text, base_size=11.0, base_color=C_ACCENT, base_bold=True)

    def p(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        add_rich_runs(p, text, base_size=10.0, base_color=C_INK)

    def bul(self, *items, numbered=False):
        for idx, it in enumerate(items, 1):
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.4)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            prefix = f"{idx}. " if numbered else "• "
            rp = p.add_run(prefix)
            rp.bold = True
            rp.font.name = "Arial"
            rp.font.size = Pt(10.0)
            rp.font.color.rgb = C_ACCENT
            add_rich_runs(p, it, base_size=10.0, base_color=C_INK)

    def note(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.12
        add_rich_runs(p, f"<i>Nota:</i> {text}", base_size=9.2, base_color=C_MUTED)

    def gap(self, pt_val=4):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(max(1, pt_val // 2))

    def pagebreak(self):
        self.doc.add_page_break()

    def box(self, kind: str, *paras, titulo: str = None):
        bg_hex, bar_hex, title_rgb, default_rot = KIND_STYLE.get(kind, KIND_STYLE["msg"])
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Cm(17.0)
        set_cell_bg(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=160, right=140)

        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        left_b = OxmlElement("w:left")
        left_b.set(qn("w:val"), "single")
        left_b.set(qn("w:sz"), "24")
        left_b.set(qn("w:color"), bar_hex)
        tcBorders.append(left_b)
        for b_name in ["top", "bottom", "right"]:
            b = OxmlElement(f"w:{b_name}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), "4")
            b.set(qn("w:color"), "DCE4EC")
            tcBorders.append(b)
        tcPr.append(tcBorders)

        p0 = cell.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(3)
        add_rich_runs(p0, titulo or default_rot, base_size=8.8, base_color=title_rgb, base_bold=True)

        is_msg = (kind == "msg")
        for para_text in paras:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if isinstance(para_text, tuple):
                prefix, body, p_rgb = para_text
                rp = p.add_run(prefix)
                rp.bold = True
                rp.font.name = "Arial"
                rp.font.size = Pt(9.8)
                rp.font.color.rgb = p_rgb
                add_rich_runs(p, body, base_size=9.8, base_color=C_INK)
            else:
                add_rich_runs(
                    p,
                    para_text,
                    base_size=11.0 if is_msg else 9.8,
                    base_color=C_ACCENT if is_msg else C_INK,
                    base_bold=is_msg,
                )
        self.gap(4)
