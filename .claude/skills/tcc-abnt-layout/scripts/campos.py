"""campos.py — trio [legenda][imagem][Fonte] no padrao ABNT deste TCC (D3, D7).

Extraido da passagem ABNT de 2026-09-13 (gen_abnt.py). Ilustracao nova no
canonico entra por aqui; legenda em texto corrido fica fora das listas
automaticas e o trio quebra entre folhas. Uso num gen_*.py:

    import sys
    sys.path.insert(0, r'C:/projetos/pll_stability_9bus/.claude/skills/tcc-abnt-layout/scripts')
    from campos import legenda, imagem, fonte
    trio = (legenda('Grafico', 5, 16, 'Erro de fase do PLL sob falta bifasica')
            + imagem(paragrafo_com_o_drawing)
            + fonte('Os autores (2026).'))

`ident` e o identificador do SEQ, em ASCII (Figura, Grafico, Quadro); o
rotulo impresso sai acentuado. `n` e so o cache do campo: o
word_finalize.ps1 renumera tudo e reconstroi as tres listas.

Comparado com as legendas entregues em 2026-09-13: mesma estrutura. O Word,
ao salvar, tira `jc=left` e `szCs` (redundantes) e poe `noProof` no numero;
diff so nisso e normalizacao, nao regressao.

Escrito pela ferramenta Write: o heredoc do Bash reduz barra dupla a simples
e estraga a instrucao do campo.
"""
import html

from ppr import ppr_edit

BS = '\\'
SZ10 = '<w:sz w:val="20"/><w:szCs w:val="20"/>'
ROTULO = {'Figura': 'Figura', 'Grafico': 'Gráfico', 'Quadro': 'Quadro'}


def run(t, rpr=SZ10):
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{html.escape(t, quote=False)}</w:t></w:r>'


def legenda(ident, cap, n, titulo, tag='<w:p>'):
    """Acima da ilustracao: 'Gráfico 5.16 – titulo', 10 pt, simples, a esquerda, keepNext."""
    if ident not in ROTULO:
        raise ValueError(f'ident deve ser um de {sorted(ROTULO)}: {ident!r}')
    r = lambda inner: f'<w:r><w:rPr>{SZ10}</w:rPr>{inner}</w:r>'
    instr = f' SEQ {ident} {BS}* ARABIC {BS}s 1 '
    return (tag + '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/>'
            f'<w:jc w:val="left"/><w:rPr>{SZ10}</w:rPr></w:pPr>'
            + run(f'{ROTULO[ident]} {cap}.') + r('<w:fldChar w:fldCharType="begin"/>')
            + r(f'<w:instrText xml:space="preserve">{instr}</w:instrText>')
            + r('<w:fldChar w:fldCharType="separate"/>') + run(str(n)) + r('<w:fldChar w:fldCharType="end"/>')
            + run(f' – {titulo}') + '</w:p>')


# paragrafo que ja contem o <w:drawing>: segura o Fonte:, centralizado, sem recuo nem espaco
imagem = ppr_edit(keepNext='<w:keepNext/>', spacing=dict(before='0', after='0'),
                  ind=None, jc='<w:jc w:val="center"/>')


def fonte(texto, tag='<w:p>'):
    """Abaixo da ilustracao, 10 pt, simples, a esquerda. Aceita o texto com ou sem 'Fonte: '."""
    if not texto.startswith('Fonte:'):
        texto = 'Fonte: ' + texto
    return (tag + '<w:pPr><w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/>'
            f'<w:jc w:val="left"/><w:rPr>{SZ10}</w:rPr></w:pPr>' + run(texto) + '</w:p>')


def lista(ident, tag='<w:p>'):
    """Campo TOC de uma lista pre-textual (so para recriar lista; as tres ja existem)."""
    instr = f' TOC {BS}h {BS}z {BS}c "{ident}" '
    return (tag + '<w:pPr><w:pStyle w:val="ndicedeilustraes"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9062"/>'
            '</w:tabs></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Atualizar lista</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
