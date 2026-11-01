"""Roteiro de falas (.docx): paleta e utilitários de célula."""
import re

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# Paleta de cores
C_NAVY = RGBColor(0x1B, 0x36, 0x5D)
C_BLUE = RGBColor(0x25, 0x63, 0xEB)
C_BRUNO = RGBColor(0x1E, 0x3A, 0x8A)
C_VICTOR = RGBColor(0x06, 0x5F, 0x46)
C_ORANGE = RGBColor(0xC2, 0x41, 0x0C)
C_INK = RGBColor(0x1E, 0x29, 0x3B)
C_MUTED = RGBColor(0x64, 0x74, 0x8B)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEX_NAVY = "1B365D"
HEX_PANEL = "0F766E"
HEX_SUB = "F1F5F9"
HEX_MSG_BG = "E8EFF7"
HEX_MSG_BD = "1B365D"
HEX_PTS_BG = "FFFBEB"
HEX_PTS_BD = "B45309"
HEX_FALA_BG = "F8FAFC"
HEX_FALA_BD = "2563EB"
HEX_PALCO_BG = "F0FDF4"
HEX_PALCO_BD = "15803D"
HEX_BORDER = "CBD5E1"
HEX_ZEBRA = "F8FAFC"


def set_cell_bg(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side, cfg in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        if cfg is None:
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:val"), "none")
            tcBorders.append(node)
        else:
            val, sz, color = cfg
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:val"), val)
            node.set(qn("w:sz"), str(sz))
            node.set(qn("w:space"), "0")
            node.set(qn("w:color"), color.lstrip("#"))
            tcBorders.append(node)
    tcPr.append(tcBorders)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def repeat_header_row(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def count_words(text: str) -> int:
    clean = re.sub(r"\[(Bruno|Victor)\]", " ", text)
    clean = re.sub(r"\([^)]*\)", " ", clean)
    return len(re.findall(r"\S+", clean))


def fmt_mmss(seconds: int) -> str:
    m, s = divmod(int(round(seconds)), 60)
    return f"{m:02d}:{s:02d}"


def fmt_dur(seconds: int) -> str:
    m, s = divmod(int(round(seconds)), 60)
    if m > 0 and s > 0:
        return f"{m}m {s:02d}s"
    if m > 0:
        return f"{m}m 00s"
    return f"{s}s"
