"""check_abnt.py <document.xml> [--recuo N] [--settings F]

Conferencia estatica de formatacao ABNT sobre o document.xml extraido.
Read-only: nao abre o Word e nao precisa do PDF.

Pega: numeracao de paginas (secoes, pgNumType, header/footer even-odd),
keepNext ausente em legenda/imagem, legenda e 'Fonte:' fora do padrao,
recuo de paragrafo inconsistente, estilo de titulo, rotulo de equacao,
residuo de template.

NAO pega (so o PDF mostra): pagina em branco, legenda numa folha e imagem
na seguinte, titulo no pe da pagina. Para isso, pagecheck.py.

Legenda, imagem e recuo sao conferidos so no corpo (titulo do Cap. 1 ate
REFERENCIAS): o pre-texto tem brasao sem legenda e resumo sem recuo.

--recuo N     recuo de primeira linha esperado, em twips (default 708 = 1,25 cm)
--settings F  settings.xml (so e achado sozinho quando o XML se chama document.xml)

Sai com codigo 1 se houver falha. As conferencias vivem em checks_xml.py.
"""
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import checks_xml as c


def arg(nome):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    caminho = sys.argv[1]
    alvo = int(arg('--recuo') or 708)
    settings = (re.sub(r'document\.xml$', 'settings.xml', caminho)
                if caminho.endswith('document.xml') else arg('--settings'))

    x = open(caminho, encoding='utf-8').read()
    body = x[x.index('<w:body>'):] if '<w:body>' in x else x
    paras = c.paragrafos(body)
    cp = c.corpo(paras)
    print(f"== {caminho} ({len(paras)} paragrafos, {len(cp)} no corpo) ==")

    c.paginacao(x)
    c.evenodd(settings)
    c.keepnext(cp)
    c.legendas(cp)
    c.recuo(cp, alvo)
    c.titulos(paras)
    c.equacoes(x)
    c.placeholders(x)

    print(f"\n== {len(c.FALHAS)} falha(s), {len(c.AVISOS)} aviso(s) ==")
    return 1 if c.FALHAS else 0


if __name__ == '__main__':
    sys.exit(main())
