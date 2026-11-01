"""Guia de estudos (.docx): paleta, caixas e utilitários de formatação."""
import html
import io
import re
from pathlib import Path
from PIL import Image as PILImage
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from caminhos import ROOT  # noqa: F401  (também põe pdfnote no path)
from pdfnote import _mathtext_image  # noqa: F401

# Paleta de cores do documento Word
C_INK = RGBColor(0x14, 0x23, 0x2E)
C_ACCENT = RGBColor(0x1A, 0x4A, 0x6E)
C_BRUNO = RGBColor(0x1E, 0x3A, 0x8A)
C_VICTOR = RGBColor(0x0F, 0x76, 0x6E)
C_MUTED = RGBColor(0x5A, 0x6B, 0x78)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# Estilo das caixas do roteiro do Victor
KIND_STYLE = {
    "msg":     ("#E7EFF6", "1A4A6E", RGBColor(0x1A, 0x4A, 0x6E), "MENSAGEM"),
    "banca":   ("#EDF4FB", "2F6FA8", RGBColor(0x2F, 0x6F, 0xA8), "PERGUNTA DO RODAPÉ DO SLIDE"),
    "prova":   ("#F3EEF8", "6B4C9A", RGBColor(0x6B, 0x4C, 0x9A), "PERGUNTA PROVÁVEL DA BANCA"),
    "cuidado": ("#FDF3E1", "C27C0E", RGBColor(0xC2, 0x7C, 0x0E), "CUIDADO"),
    "alem":    ("#EAF4EC", "3D8A57", RGBColor(0x3D, 0x8A, 0x57), "ALÉM DO TCC · para entender e responder, não para a fala"),
    "passo":   ("#F4F7F9", "5A6B78", RGBColor(0x5A, 0x6B, 0x78), "PASSOS DO CAPÍTULO"),
    "fala":    ("#FBF6EC", "8A6D3B", RGBColor(0x8A, 0x6D, 0x3B), "O QUE FALAR · tópicos para dizer com as suas palavras"),
    "script":  ("#EFF6FF", "1E3A8A", RGBColor(0x1E, 0x3A, 0x8A), "ROTEIRO DE FALA COMPLETO (30 MINUTOS) · [Bruno] e [Victor]"),
    "palco_s": ("#F0FDFA", "0F766E", RGBColor(0x0F, 0x76, 0x6E), "ROTEIRO DE FALA PASSO A PASSO NO PALCO · [Bruno] e [Victor]"),
}


def set_cell_bg(cell, hex_color: str):
    hex_clean = hex_color.lstrip("#")
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_clean)
    tcPr.append(shd)


def set_cell_margins(cell, top=90, bottom=90, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="C7D2DA", sz="4"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for b_name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        b = OxmlElement(f"w:{b_name}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), sz)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), color)
        borders.append(b)
    tblPr.append(borders)


def add_rich_runs(p, html_text: str, base_font="Arial", base_size=10.0, base_color=C_INK, base_bold=False, base_italic=False):
    """Converte tags simples (<b>, <i>, <sub>, <super>, <font color='...'>, <br/>) e entidades HTML em runs do Word."""
    txt = html_text.replace("<br/>", "\n").replace("<br>", "\n")
    # Tokenizar por tags conhecidas
    token_re = re.compile(r"(</?(?:b|i|sub|super|sup|font)[^>]*>)", re.IGNORECASE)
    tokens = token_re.split(txt)

    bold_stack = [base_bold]
    italic_stack = [base_italic]
    sub_state = False
    sup_state = False
    color_stack = [base_color]

    for tok in tokens:
        if not tok:
            continue
        low = tok.lower()
        if low == "<b>":
            bold_stack.append(True)
        elif low == "</b>":
            if len(bold_stack) > 1:
                bold_stack.pop()
        elif low == "<i>":
            italic_stack.append(True)
        elif low == "</i>":
            if len(italic_stack) > 1:
                italic_stack.pop()
        elif low == "<sub>":
            sub_state = True
        elif low == "</sub>":
            sub_state = False
        elif low in ("<super>", "<sup>"):
            sup_state = True
        elif low in ("</super>", "</sup>"):
            sup_state = False
        elif low.startswith("<font"):
            m = re.search(r"color=['\"]?#?([0-9a-fA-F]{6})['\"]?", tok)
            if m:
                hx = m.group(1)
                color_stack.append(RGBColor(int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)))
            else:
                color_stack.append(color_stack[-1])
        elif low == "</font>":
            if len(color_stack) > 1:
                color_stack.pop()
        else:
            clean = html.unescape(re.sub(r"<[^>]+>", "", tok))
            if not clean:
                continue
            r = p.add_run(clean)
            r.font.name = base_font
            r.font.size = Pt(base_size)
            r.bold = bold_stack[-1]
            r.italic = italic_stack[-1]
            r.font.subscript = sub_state
            r.font.superscript = sup_state
            r.font.color.rgb = color_stack[-1]


def format_mmss(minutes_float: float) -> str:
    total_sec = int(round(minutes_float * 60))
    return f"{total_sec // 60:02d}:{total_sec % 60:02d}"
