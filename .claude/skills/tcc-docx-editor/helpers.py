"""
Funções auxiliares para gerar parágrafos OOXML com tracked changes (w:ins).
Usar em scripts de edição do TCC DOCX.

IDs de referência: ver .claude/kb/tcc-word/docx_structure.md
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

DATE = "2026-06-14T00:00:00Z"
AUTHOR = "Claude"


def ins_attr(ins_id: int) -> str:
    return f'<w:ins w:id="{ins_id}" w:author="{AUTHOR}" w:date="{DATE}"/>'


def h2(text: str, bm_id: int, i1: int, i2: int) -> str:
    """Título de seção (Ttulo2). paraId prefix=1."""
    return (
        f'    <w:p w14:paraId="1{bm_id:07X}" w14:textId="77777777"'
        f' w:rsidR="00DB34AF" w:rsidRDefault="00DB34AF" w:rsidP="7211126C">\n'
        f'      <w:pPr><w:pStyle w:val="Ttulo2"/><w:autoSpaceDE w:val="0"/>'
        f'<w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/>'
        f'<w:spacing w:before="299" w:after="299"/><w:jc w:val="both"/>'
        f'<w:rPr>{ins_attr(i1)}<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="36"/><w:szCs w:val="36"/><w:lang w:val="pt-BR"/></w:rPr></w:pPr>\n'
        f'      <w:bookmarkStart w:id="{bm_id}" w:name="_Toc3_{bm_id}"/>\n'
        f'      <w:ins w:id="{i2}" w:author="{AUTHOR}" w:date="{DATE}">'
        f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="36"/><w:szCs w:val="36"/><w:lang w:val="pt-BR"/></w:rPr>'
        f'<w:t>{text}</w:t></w:r></w:ins>\n'
        f'      <w:bookmarkEnd w:id="{bm_id}"/>\n'
        f'    </w:p>\n'
    )


def h3(text: str, bm_id: int, i1: int, i2: int) -> str:
    """Subtítulo de seção (Ttulo3). paraId prefix=2."""
    return (
        f'    <w:p w14:paraId="2{bm_id:07X}" w14:textId="77777777"'
        f' w:rsidR="00DB34AF" w:rsidRDefault="00DB34AF" w:rsidP="7211126C">\n'
        f'      <w:pPr><w:pStyle w:val="Ttulo3"/><w:autoSpaceDE w:val="0"/>'
        f'<w:autoSpaceDN w:val="0"/><w:adjustRightInd w:val="0"/>'
        f'<w:spacing w:before="281" w:after="281"/><w:jc w:val="both"/>'
        f'<w:rPr>{ins_attr(i1)}<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="pt-BR"/></w:rPr></w:pPr>\n'
        f'      <w:bookmarkStart w:id="{bm_id}" w:name="_Toc3_{bm_id}"/>\n'
        f'      <w:ins w:id="{i2}" w:author="{AUTHOR}" w:date="{DATE}">'
        f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="pt-BR"/></w:rPr>'
        f'<w:t>{text}</w:t></w:r></w:ins>\n'
        f'      <w:bookmarkEnd w:id="{bm_id}"/>\n'
        f'    </w:p>\n'
    )


def body(text: str, pid: int, i1: int, i2: int) -> str:
    """Parágrafo de corpo, justificado. paraId prefix=3."""
    return (
        f'    <w:p w14:paraId="3{pid:07X}" w14:textId="77777777"'
        f' w:rsidR="00DB34AF" w:rsidRDefault="00DB34AF" w:rsidP="7211126C">\n'
        f'      <w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/>'
        f'<w:adjustRightInd w:val="0"/><w:spacing w:before="240" w:after="240"/>'
        f'<w:jc w:val="both"/>'
        f'<w:rPr>{ins_attr(i1)}<w:szCs w:val="24"/></w:rPr></w:pPr>\n'
        f'      <w:ins w:id="{i2}" w:author="{AUTHOR}" w:date="{DATE}">'
        f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:szCs w:val="24"/><w:lang w:val="pt-BR"/></w:rPr>'
        f'<w:t xml:space="preserve">{text}</w:t></w:r></w:ins>\n'
        f'    </w:p>\n'
    )


def placeholder(text: str, pid: int, i1: int, i2: int) -> str:
    """Placeholder italic centralizado (figuras/tabelas). paraId prefix=4."""
    return (
        f'    <w:p w14:paraId="4{pid:07X}" w14:textId="77777777"'
        f' w:rsidR="00DB34AF" w:rsidRDefault="00DB34AF" w:rsidP="7211126C">\n'
        f'      <w:pPr><w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/>'
        f'<w:adjustRightInd w:val="0"/><w:spacing w:before="240" w:after="240"/>'
        f'<w:jc w:val="center"/>'
        f'<w:rPr>{ins_attr(i1)}<w:i/><w:szCs w:val="24"/></w:rPr></w:pPr>\n'
        f'      <w:ins w:id="{i2}" w:author="{AUTHOR}" w:date="{DATE}">'
        f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:i/><w:szCs w:val="24"/><w:lang w:val="pt-BR"/></w:rPr>'
        f'<w:t>{text}</w:t></w:r></w:ins>\n'
        f'    </w:p>\n'
    )


class Counter:
    """Contador de IDs sequenciais para w:ins e paraId internos."""
    def __init__(self, start: int = 1):
        self._v = start

    def next(self) -> int:
        v = self._v
        self._v += 1
        return v

    @property
    def current(self) -> int:
        return self._v
