"""ppr.py — edicao segura do <w:pPr> de um paragrafo OOXML, por string.

Extraido da passagem ABNT de 2026-09-13 (gen_abnt.py). Uso num gen_*.py:

    import sys
    sys.path.insert(0, r'C:/projetos/pll_stability_9bus/.claude/skills/tcc-abnt-layout/scripts')
    from ppr import ppr_edit
    novo = ppr_edit(keepNext='<w:keepNext/>',
                    spacing=dict(before=None, after='240'),
                    ind='<w:ind w:firstLine="708"/>')(paragrafo_xml)

Valor None remove o filho (ou, dentro de `spacing`, o atributo).

Duas armadilhas que ele resolve:

1. <w:pPr> tem ORDEM de schema (CT_PPr). Filho inserido fora de ordem pode
   fazer o Word acusar conteudo ilegivel. `poe` insere na posicao certa.
2. A regex plana de paragrafo (a mesma do dump_blocks.py) casa um <w:p .../>
   auto-fechado junto com o paragrafo seguinte num span so. Editar o pPr desse
   span sem tratar isso abre uma tag sem fechar. `partes` preserva os vazios
   da frente como prefixo e edita o paragrafo real.

Nunca faz ET.parse no documento inteiro (ver kb/tcc-word/armadilhas_xml.md).
"""
import re

ORDEM = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl', 'numPr',
         'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
         'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd',
         'snapToGrid', 'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc',
         'textDirection', 'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr',
         'sectPr', 'pPrChange']
TOK = re.compile(r'<w:(\w+)\b[^>]*?/>|<w:(\w+)\b[^>]*>', re.S)
SELF = re.compile(r'(?:<w:p\b[^>]*/>)*')


def partes(p):
    """-> (tag_de_abertura_com_prefixo, [(nome, xml_do_filho)], resto_do_paragrafo)."""
    pre = SELF.match(p).group(0)
    if pre == p:
        ult = re.findall(r'<w:p\b[^>]*/>', p)[-1]
        return p[:len(p) - len(ult)] + '<w:p' + ult[4:-2] + '>', [], ''
    p = p[len(pre):]
    abre = re.match(r'<w:p\b[^>]*>', p)
    tag = pre + abre.group(0)
    resto = p[abre.end():-len('</w:p>')]
    if not resto.startswith('<w:pPr>'):
        return tag, [], resto
    fim = resto.index('</w:pPr>')
    inner, fs, pos = resto[len('<w:pPr>'):fim], [], 0
    while pos < len(inner):
        m = TOK.match(inner, pos)
        if not m:
            raise ValueError(f'pPr inesperado: {inner[pos:pos + 80]!r}')
        if m.group(1):
            fs.append((m.group(1), m.group(0)))
            pos = m.end()
        else:
            fecha = f'</w:{m.group(2)}>'
            f_ = inner.index(fecha, m.end()) + len(fecha)
            fs.append((m.group(2), inner[pos:f_]))
            pos = f_
    return tag, fs, resto[fim + len('</w:pPr>'):]


def monta(tag, fs, resto):
    ppr = ''.join(v for _, v in fs)
    return tag + (f'<w:pPr>{ppr}</w:pPr>' if ppr else '') + resto + '</w:p>'


def poe(fs, nome, xml):
    """Troca, insere na ordem do schema, ou remove (xml=None) o filho `nome`."""
    fs = [f for f in fs if f[0] != nome]
    if xml is None:
        return fs
    k = ORDEM.index(nome)
    for j, (n, _) in enumerate(fs):
        if n in ORDEM and ORDEM.index(n) > k:
            return fs[:j] + [(nome, xml)] + fs[j:]
    return fs + [(nome, xml)]


def atr(xml):
    return dict(re.findall(r'(w:\w+)="([^"]*)"', xml))


def spc(fs, **kv):
    """Mexe atributo a atributo no <w:spacing>, preservando os demais."""
    cur = next((atr(v) for n, v in fs if n == 'spacing'), {})
    for k, v in kv.items():
        if v is None:
            cur.pop('w:' + k, None)
        else:
            cur['w:' + k] = v
    xml = ('<w:spacing ' + ' '.join(f'{k}="{v}"' for k, v in cur.items()) + '/>') if cur else None
    return poe(fs, 'spacing', xml)


def ppr_edit(**ops):
    """Funcao paragrafo -> paragrafo. `spacing=dict(...)`, demais: xml ou None."""
    def f(p):
        tag, fs, resto = partes(p)
        for nome, val in ops.items():
            fs = spc(fs, **val) if nome == 'spacing' else poe(fs, nome, val)
        return monta(tag, fs, resto)
    return f
