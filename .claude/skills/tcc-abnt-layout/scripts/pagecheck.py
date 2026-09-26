"""pagecheck.py <arquivo.pdf> [--dump N] [--corpo N] [--fig-dir DIR]

Conferencia de PAGINACAO sobre o PDF exportado pelo Word. Read-only.

Pega o que nao existe no XML: pagina em branco, legenda numa folha e
imagem na seguinte, 'Fonte:' orfa, titulo no pe da pagina, lista
pre-textual vazia ou dividindo folha.

Gerar o PDF antes, com o word_finalize.ps1 da skill tcc-docx-editor:
  word_finalize.ps1 -In C:\\Temp\\tcc_edit.docx -Out C:\\Temp\\c.docx -Pdf C:\\Temp\\c.pdf

--dump N    imprime todos os blocos da folha N (para investigar um achado)
--corpo N   primeira folha textual (default: detectada pelo titulo do Cap. 1);
            imagem antes dela e brasao institucional, nao ilustracao
--fig-dir   salva PNG de cada imagem sem legenda, para identifica-las

Depende de pymupdf (`python -m pip install pymupdf`).

"Folha" aqui e sempre a posicao FISICA no PDF, nao o numero impresso —
depois de um pgNumType w:start os dois divergem.

Sai com codigo 1 se houver falha. As conferencias vivem em checks_pdf.py.
"""
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import pymupdf
except ImportError:
    sys.exit("pymupdf nao instalado: python -m pip install pymupdf")

import checks_pdf as c


def ler(doc, topo=70, base=765):
    """Uma entrada por folha: texto, blocos de texto ordenados, imagens.

    `blocos` exclui a faixa de cabecalho e a de rodape (o numero da pagina
    mora la). Sem esse corte, o numero impresso vira o 'primeiro bloco' da
    folha e mascara uma linha 'Fonte:' orfa logo abaixo dele.
    """
    folhas = []
    for p in doc:
        blocos = sorted([b for b in p.get_text("blocks")
                         if b[6] == 0 and b[4].strip() and topo < b[1] < base],
                        key=lambda b: b[1])
        rects = [r for im in p.get_images(full=True) for r in p.get_image_rects(im[0])]
        folhas.append(dict(n=p.number + 1, pagina=p, blocos=blocos, rects=rects,
                           h=p.rect.height, txt=p.get_text("text")))
    return folhas


def inicio_do_corpo(folhas):
    """Primeira folha textual. Imagem antes dela e brasao/institucional."""
    alvo = re.compile(r'(Cap[íi]tulo\s+1\s*[–\-—]|^\s*1\s+INTRODU)')
    for f in folhas:
        if f['blocos'] and alvo.search(c.limpa(f['blocos'][0][4])):
            return f['n']
    return 1


def dump(folhas, n):
    f = folhas[n - 1]
    print(f"\n== folha {n} (altura {f['h']:.0f}) ==")
    for b in f['blocos']:
        print(f"  txt y={b[1]:6.0f}-{b[3]:<6.0f} {c.limpa(b[4])[:96]}")
    for r in f['rects']:
        print(f"  IMG y={r.y0:6.0f}-{r.y1:<6.0f} ({r.width:.0f}x{r.height:.0f} pt)")


def arg(nome, default=None):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else default


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    doc = pymupdf.open(sys.argv[1])
    folhas = ler(doc)
    print(f"== {sys.argv[1]} ({doc.page_count} folhas) ==")

    if '--dump' in sys.argv:
        dump(folhas, int(arg('--dump')))
        return 0

    corpo = int(arg('--corpo') or inicio_do_corpo(folhas))

    c.paginas_vazias(folhas)
    c.legenda_separada(folhas)
    c.titulo_no_pe(folhas)
    c.imagens_sem_legenda(folhas, arg('--fig-dir'), corpo)
    c.listas_pretextuais(folhas)

    print(f"\n== {len(c.FALHAS)} grupo(s) de falha ==")
    for f in c.FALHAS:
        print(f"   - {f}")
    return 1 if c.FALHAS else 0


if __name__ == '__main__':
    sys.exit(main())
