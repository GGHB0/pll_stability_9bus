"""renumera_figuras.py — renumera remissoes "Figura(s) C.N" / "Tabela(s) C.N" no texto.

Usado quando uma ilustracao nova entra no meio do capitulo: toda remissao a
N >= a_partir vira N + delta. As LEGENDAS nao precisam disso (o numero delas e
campo SEQ; o word_finalize.ps1 recalcula); este script so mexe no texto
corrido, que o Word nao atualiza.

Cobre os dois formatos vistos no V10:
  - tudo num <w:t>: "Figura 5.12", "Figuras 5.12 e 5.13", "Figuras 5.12 a 5.14";
  - rotulo e numero em runs separados, com ou sem <w:proofErr/> entre eles
    ("Figura " | "5.12"), que o Word cria ao salvar.

Rodar ANTES de inserir texto novo que ja cita a numeracao nova, senao a
remissao nova tambem anda. Comentarios ([Claude] ou do Oscar) que citam numero
ficam em comments.xml: conferir a parte com --comments.

Extraido de gen_erro_fase_docx.py (2026-10-01) e gen_oscar58.py (2026-10-03).

Uso num gen_*.py:
    sys.path.insert(0, r'C:/projetos/pll_stability_9bus/.claude/skills/tcc-docx-editor/scripts')
    from renumera_figuras import renumera
    doc, trocas = renumera(doc, cap=5, a_partir=9, delta=2)          # Figura
    doc, trocas = renumera(doc, cap=5, a_partir=2, delta=1, rotulo='Tabela')

Linha de comando (so lista, nao grava):
    python.exe renumera_figuras.py <document.xml> <cap> <a_partir> <delta> [Figura|Tabela]
"""
import re
import sys


def renumera(xml, cap, a_partir, delta, rotulo='Figura'):
    """Devolve (xml_novo, [(antes, depois), ...]). Passo unico: nao ha dupla renumeracao."""
    c = re.escape(str(cap))
    rot = re.escape(rotulo)

    def novo(n):
        n = int(n)
        return n + delta if n >= a_partir else n

    def ren(m):
        return f'{m.group(1)}{cap}.{novo(m.group(2))}'

    # rotulo e numero em runs separados
    partida = re.compile(
        rf'({rot}s? </w:t></w:r>(?:<w:proofErr[^>]*/>)?<w:r(?: [^>]*)?>'
        rf'(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:t(?: [^>]*)?>){c}\.(\d+)', re.S)
    trocas = [(f'{rotulo} {cap}.{m.group(2)} (partida)', f'{cap}.{novo(m.group(2))}')
              for m in partida.finditer(xml) if novo(m.group(2)) != int(m.group(2))]
    xml = partida.sub(ren, xml)

    padrao = re.compile(rf'{rot}s? {c}\.\d+(?:(?: e | a |, ){c}\.\d+)*')

    def fix_t(m):
        t = m.group(2)
        if rotulo not in t:
            return m.group(0)

        def grupo(g):
            return re.sub(rf'(^|[^\d.]){c}\.(\d+)\b', lambda x: f'{x.group(1)}{cap}.{novo(x.group(2))}', g.group(0))
        t2 = padrao.sub(grupo, t)
        for a, b in zip(padrao.findall(t), padrao.findall(t2)):
            if a != b:
                trocas.append((a, b))
        return m.group(1) + t2 + m.group(3)

    antes = len(padrao.findall(xml))
    xml = re.sub(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', fix_t, xml)
    assert len(padrao.findall(xml)) == antes, 'contagem de remissoes mudou'
    return xml, trocas


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    xml = open(sys.argv[1], encoding='utf-8').read()
    rot = sys.argv[5] if len(sys.argv) > 5 else 'Figura'
    _, trocas = renumera(xml, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), rot)
    for a, b in trocas:
        print(f'  {a} -> {b}')
    print(f'{len(trocas)} remissoes mudariam')
