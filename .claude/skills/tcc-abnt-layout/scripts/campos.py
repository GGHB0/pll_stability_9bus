"""campos.py — trio [legenda][imagem][Fonte] no padrao ABNT deste TCC (D3, D7).

Extraido da passagem ABNT de 2026-09-13 (gen_abnt.py). Ilustracao nova no
canonico entra por aqui; legenda em texto corrido fica fora das listas
automaticas e o trio quebra entre folhas. Uso num gen_*.py:

    import sys
    sys.path.insert(0, r'C:/projetos/pll_stability_9bus/.claude/skills/tcc-abnt-layout/scripts')
    from campos import legenda, imagem, fonte
    trio = (legenda('Figura', 5, 16, 'Erro de fase do PLL sob falta bifasica')
            + imagem(paragrafo_com_o_drawing)
            + fonte('Os autores (2026).'))

Tabela Word (D11): tabela_completa(cap, n, titulo, larguras, cab, linhas).
PNG que ainda nao esta no pacote: figura_nova(doc, rels, modelo_p, png, ...).

`ident` e o identificador do SEQ, em ASCII: Figura ou Tabela (D9: nao ha
mais Grafico nem Quadro). `n` e so o cache do campo: o
word_finalize.ps1 renumera tudo e reconstroi as listas.

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
ROTULO = {'Figura': 'Figura', 'Tabela': 'Tabela'}


def run(t, rpr=SZ10):
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{html.escape(t, quote=False)}</w:t></w:r>'


def legenda(ident, cap, n, titulo, tag='<w:p>'):
    """Acima da ilustracao: 'Figura 5.16 – titulo', 10 pt, simples, a esquerda, keepNext."""
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


# ── Tabela Word (D11): estilo IBGE ─────────────────────────────────────────
# Sem bordas laterais nem internas; filete acima e abaixo do cabecalho e abaixo
# da ultima linha. Cabecalho repete na quebra (tblHeader), linha nao parte
# (cantSplit), keepNext em TODAS as linhas, inclusive a ultima, para o Fonte:
# nao descolar. 10 pt, primeira coluna a esquerda, demais centralizadas.
# Entregue assim nas Tabelas 5.1-5.3 (2026-10-03).
LARGURA_UTIL = 9072  # dxa, A4 com margens 3/2 cm
_FILETE = '<w:{0} w:val="single" w:sz="8" w:space="0" w:color="000000"/>'


def _cel(texto, larg, jc, bordas):
    b = ''.join(_FILETE.format(x) for x in bordas)
    tcpr = f'<w:tcW w:w="{larg}" w:type="dxa"/>' + (f'<w:tcBorders>{b}</w:tcBorders>' if b else '') + '<w:vAlign w:val="center"/>'
    return (f'<w:tc><w:tcPr>{tcpr}</w:tcPr><w:p><w:pPr><w:keepNext/>'
            '<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
            f'<w:ind w:firstLine="0"/><w:jc w:val="{jc}"/><w:rPr>{SZ10}</w:rPr></w:pPr>{run(texto)}</w:p></w:tc>')


def tabela(larguras, cab, linhas):
    """<w:tbl> IBGE. larguras em dxa (soma = LARGURA_UTIL); cab e cada linha: listas de str.

    Primeira coluna estreita quebra o rotulo ('Bifasica na Barra 7'): conferir no PDF.
    """
    if sum(larguras) != LARGURA_UTIL:
        raise ValueError(f'larguras somam {sum(larguras)}, esperado {LARGURA_UTIL}')
    if any(len(x) != len(larguras) for x in [cab, *linhas]):
        raise ValueError('linha com numero de celulas diferente de larguras')
    grid = ''.join(f'<w:gridCol w:w="{x}"/>' for x in larguras)
    xml = (f'<w:tbl><w:tblPr><w:tblW w:w="{LARGURA_UTIL}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>'
           '<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/>'
           '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders><w:tblLayout w:type="fixed"/>'
           '<w:tblCellMar><w:left w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
           f'</w:tblPr><w:tblGrid>{grid}</w:tblGrid>')
    xml += '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' + ''.join(
        _cel(t, l, 'center', ('top', 'bottom')) for t, l in zip(cab, larguras)) + '</w:tr>'
    for i, lin in enumerate(linhas):
        bordas = ('bottom',) if i == len(linhas) - 1 else ()
        xml += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(
            _cel(t, l, 'left' if j == 0 else 'center', bordas)
            for j, (t, l) in enumerate(zip(lin, larguras))) + '</w:tr>'
    return xml + '</w:tbl>'


def tabela_completa(cap, n, titulo, larguras, cab, linhas, texto_fonte='Os autores (2026).'):
    """Trio [legenda Tabela][tabela][Fonte]. A remissao no texto vem ANTES (texto antes da ilustracao)."""
    return legenda('Tabela', cap, n, titulo) + tabela(larguras, cab, linhas) + fonte(texto_fonte)


# ── Figura com midia nova ──────────────────────────────────────────────────
EMU_IN = 914400
REL_IMG = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'


def figura_nova(doc, rels, modelo_p, png, larg_in, k, cap, n, titulo,
                texto_fonte='Os autores (2026).', prefixo='nova'):
    """Trio [legenda Figura][imagem][Fonte] com um PNG que ainda nao esta no pacote.

    modelo_p: XML de um paragrafo de imagem ja existente (inline), clonado.
    k: 1, 2, ... distinto por figura na mesma rodada: docPr/cNvPr = max do doc + k,
    sobre o doc ORIGINAL (gerar todas antes de inserir). rels: passar sempre o
    devolvido pela chamada anterior (rId = max + 1).
    Altura sai da razao do PNG. Devolve (xml, rels_novo, (caminho_no_zip, bytes)):
    o gen grava os bytes em word/media/ ao montar o zip.
    """
    import re
    import struct
    b = open(png, 'rb').read()
    w, h = struct.unpack('>II', b[16:24])
    cx = int(round(larg_in * EMU_IN))
    cy = int(round(cx * h / w))
    rid = 'rId%d' % (max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1)  # rels ja traz as anteriores
    doc_id = max(int(x) for x in re.findall(r'<wp:docPr id="(\d+)"', doc)) + k
    cnv_id = max(int(x) for x in re.findall(r'<pic:cNvPr id="(\d+)"', doc)) + k
    alvo = f'media/{prefixo}_{k}.png'
    rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="{REL_IMG}" Target="{alvo}"/></Relationships>')
    img = re.sub(r'<w:p\b[^>]*>', '<w:p>', modelo_p, count=1)
    img = re.sub(r' wp14:anchorId="[^"]*" wp14:editId="[^"]*"', '', img)
    img, n_ext = re.subn(r'cx="\d+" cy="\d+"', f'cx="{cx}" cy="{cy}"', img)
    img, n_emb = re.subn(r'r:embed="rId\d+"', f'r:embed="{rid}"', img)
    if (n_ext, n_emb) != (2, 1):
        raise ValueError(f'modelo inesperado: {n_ext} extents, {n_emb} r:embed (esperado 2 e 1)')
    nome = png.replace('\\', '/').rsplit('/', 1)[-1]
    img = re.sub(r'<wp:docPr id="\d+" name="[^"]*"', f'<wp:docPr id="{doc_id}" name="Picture {doc_id}"', img)
    img = re.sub(r'<pic:cNvPr id="\d+" name="[^"]*"', f'<pic:cNvPr id="{cnv_id}" name="{nome}"', img)
    xml = legenda('Figura', cap, n, titulo) + imagem(img) + fonte(texto_fonte)
    return xml, rels, ('word/' + alvo, b)


def lista(ident, tag='<w:p>'):
    """Campo TOC de uma lista pre-textual (so para recriar lista; as tres ja existem)."""
    instr = f' TOC {BS}h {BS}z {BS}c "{ident}" '
    return (tag + '<w:pPr><w:pStyle w:val="ndicedeilustraes"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9062"/>'
            '</w:tabs></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Atualizar lista</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
