"""Conferencias de paginacao sobre o PDF. Usadas pelo pagecheck.py.

Cada funcao imprime o seu bloco e registra em FALHAS. Read-only.
"""
import os
import re

CAP = re.compile(r'^(Figura|Quadro|Tabela|Gr[áa]fico)\s*\d+[.\d]*\s*[–\-—]', re.I)
FONTE = re.compile(r'^Fonte:', re.I)

# Titulo de secao: indicativo numerico (ou "Capitulo N") seguido de palavra
# comecando em MAIUSCULA. A exigencia da maiuscula e o que separa
# "2.4.1. Blecaute da Peninsula" de "3 (V3 2 vb - V3 2 vc) EQUACAO 3.3",
# uma equacao que casava com o padrao antigo.
SECAO = re.compile(r'^\s*(?:\d+(?:\.\d+){0,3}\.?|Cap[íi]tulo\s+\d+\s*[–\-—])'
                   r'\s+[A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇ]')

PRETEXTUAL = re.compile(r'^(LISTA DE [A-ZÇÃÕÉ ]+|SUM[ÁA]RIO)\s*$')

FALHAS = []


def limpa(s):
    return re.sub(r'\s+', ' ', s).strip()


def paginas_vazias(folhas):
    print("\n-- paginas em branco ou quase --")
    achou = 0
    for f in folhas:
        # descontar o numero da pagina, que sozinho nao e conteudo
        corpo = re.sub(r'^\d+\s*|\s*\d+$', '', limpa(f['txt'])).strip()
        # dedicatoria e epigrafe: pouco texto de proposito, na metade de baixo
        if f['blocos'] and min(b[1] for b in f['blocos']) > f['h'] * 0.5:
            continue
        if len(corpo) < 60 and not f['rects']:
            print(f"    folha {f['n']:>3}: {corpo[:60]!r}")
            achou += 1
    FALHAS.append(f"{achou} folha(s) em branco ou quase") if achou \
        else print("  OK    nenhuma")


def legenda_separada(folhas):
    """Legenda no pe de uma folha com a imagem na seguinte, e 'Fonte:' orfa."""
    print("\n-- legenda separada da imagem / fonte orfa --")
    achou = 0
    for i, f in enumerate(folhas):
        seg = folhas[i + 1] if i + 1 < len(folhas) else None
        for b in [b for b in f['blocos'] if CAP.match(limpa(b[4]))]:
            if not [r for r in f['rects'] if r.y0 > b[1]] and seg and seg['rects']:
                print(f"    folha {f['n']:>3} -> {seg['n']:<3} legenda sem imagem "
                      f"abaixo: {limpa(b[4])[:60]}")
                achou += 1
        if i and f['blocos'] and FONTE.match(limpa(f['blocos'][0][4])) \
                and folhas[i - 1]['rects'] and not f['rects']:
            print(f"    folha {folhas[i-1]['n']:>3} -> {f['n']:<3} 'Fonte:' orfa no topo")
            achou += 1
    FALHAS.append(f"{achou} quebra(s) entre legenda, imagem e fonte") if achou \
        else print("  OK    nenhuma")


def titulo_no_pe(folhas, margem=0.82):
    print("\n-- titulo no pe da pagina --")
    achou = 0
    for f in folhas:
        if not f['blocos']:
            continue
        ultimo = f['blocos'][-1]
        t = limpa(ultimo[4])
        if SECAO.match(t) and len(t) < 90 and ultimo[1] > f['h'] * margem:
            print(f"    folha {f['n']:>3} y={ultimo[1]:.0f}/{f['h']:.0f}: {t[:62]}")
            achou += 1
    FALHAS.append(f"{achou} titulo(s) isolado(s) no pe da pagina") if achou \
        else print("  OK    nenhum")


def imagens_sem_legenda(folhas, fig_dir=None, corpo=1):
    print(f"\n-- imagens sem legenda (a partir da folha {corpo}) --")
    achou = 0
    for i, f in enumerate(folhas):
        if not f['rects'] or f['n'] < corpo:
            continue
        vizinhanca = list(f['blocos']) + (folhas[i - 1]['blocos'][-3:] if i else [])
        caps = [b for b in vizinhanca if CAP.match(limpa(b[4]))]
        if len(caps) >= len(f['rects']):
            continue
        falta = len(f['rects']) - len(caps)
        print(f"    folha {f['n']:>3}: {falta} imagem(ns) sem legenda")
        achou += falta
        if fig_dir:
            os.makedirs(fig_dir, exist_ok=True)
            for j, r in enumerate(f['rects']):
                destino = os.path.join(fig_dir, f"folha{f['n']}_{j}.png")
                f['pagina'].get_pixmap(dpi=120, clip=r).save(destino)
                print(f"        -> {destino}")
    FALHAS.append(f"{achou} imagem(ns) sem legenda") if achou \
        else print("  OK    nenhuma")


def listas_pretextuais(folhas):
    print("\n-- listas pre-textuais --")
    achou = 0
    for f in folhas:
        for b in f['blocos']:
            t = limpa(b[4])
            if not PRETEXTUAL.match(t):
                continue
            resto = [limpa(o[4]) for o in f['blocos'] if o[1] > b[1]]
            resto = [r for r in resto if r and not r.isdigit()]
            if not resto:
                print(f"    folha {f['n']:>3}: '{t}' sem nenhuma entrada")
                achou += 1
            elif b[1] > f['h'] * 0.70:
                print(f"    folha {f['n']:>3}: '{t}' comeca no pe da folha "
                      f"(y={b[1]:.0f}/{f['h']:.0f}) — cada elemento pre-textual "
                      f"abre folha nova")
                achou += 1
    FALHAS.append(f"{achou} problema(s) em lista pre-textual") if achou \
        else print("  OK    nenhum")
