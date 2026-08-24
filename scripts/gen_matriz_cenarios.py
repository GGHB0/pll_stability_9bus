# -*- coding: utf-8 -*-
"""Gera assets/diagrams/matriz_cenarios.svg a partir de output/results/.

A matriz e lida do disco, nao escrita a mao: cada pasta de cenario vira uma
marca na celula (local x tipo de falta), separada por condicao de sintonia.
Reexecutar apos qualquer re-simulacao.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RESULTS = RAIZ / "output" / "results"
SAIDA = RAIZ / "assets" / "diagrams" / "matriz_cenarios.svg"

TIPOS = ["1phase", "2phase", "3phase"]
ROTULO_TIPO = {"1phase": "Monofásica (1φ)", "2phase": "Bifásica (2φ)", "3phase": "Trifásica (3φ)"}
ROTULO_LOCAL = {
    "bus4": "Barra 4", "bus5": "Barra 5", "bus6": "Barra 6", "bus7": "Barra 7",
    "bus8": "Barra 8", "bus9": "Barra 9", "line7_8": "Linha 7-8", "line8_9": "Linha 8-9",
}
ORDEM = ["bus4", "bus5", "bus6", "bus7", "bus8", "bus9", "line7_8", "line8_9"]

NAVY, LARANJA, CINZA = "#0B132B", "#F97316", "#94a3b8"

X0, LARG_LOCAL, LARG_COL = 50, 180, 160
XS = [X0 + LARG_LOCAL + i * LARG_COL for i in range(4)]   # bordas das colunas
Y_CAB, H_CAB, H_LIN, H_REG = 62, 40, 38, 50
LARG_TAB = LARG_LOCAL + 3 * LARG_COL
LINHA = '  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#cbd5e1" stroke-width="1"/>'
TEXTO = '  <text x="%d" y="%d"%s font-size="%d"%s fill="%s">%s</text>'


def levantar():
    """Devolve {local: {tipo: (tem_nominal, tem_inadequada)}} e o par do regime."""
    m = {}
    for local in ORDEM:
        pasta = RESULTS / local
        sub = {p.name for p in pasta.iterdir() if p.is_dir()} if pasta.is_dir() else set()
        m[local] = {t: (t in sub, t + "_bad_pll" in sub) for t in TIPOS}
    regime = ((RESULTS / "regime").is_dir(), (RESULTS / "regime_bad_pll").is_dir())
    return m, regime


def texto(x, y, txt, tam=15, cor=NAVY, centro=False, italico=False, negrito=False):
    est = ' font-style="italic"' if italico else ""
    if negrito:
        est += ' font-weight="700"'
    return TEXTO % (x, y, ' text-anchor="middle"' if centro else "", tam, est, cor, txt)


def chip(x, y, letra, cor):
    return ('  <rect x="%d" y="%d" width="30" height="22" rx="5" fill="%s"/>' % (x, y, cor),
            texto(x + 15, y + 16, letra, 14, "#ffffff", centro=True, negrito=True))


def celula(cx, cy, nominal, inadequada):
    """Chips centrados em cx; cy e o topo do chip."""
    if not nominal and not inadequada:
        return (texto(cx, cy + 16, "–", 16, CINZA, centro=True),)
    if nominal and inadequada:
        return chip(cx - 34, cy, "N", NAVY) + chip(cx + 4, cy, "I", LARANJA)
    return chip(cx - 15, cy, "N" if nominal else "I", NAVY if nominal else LARANJA)


def montar():
    m, regime = levantar()
    n_nom = sum(v[0] for lin in m.values() for v in lin.values()) + int(regime[0])
    n_ina = sum(v[1] for lin in m.values() for v in lin.values()) + int(regime[1])
    y_regime = Y_CAB + H_CAB + len(ORDEM) * H_LIN
    y_fim = y_regime + H_REG

    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 560"'
         ' font-family="ui-sans-serif, system-ui, -apple-system, sans-serif">',
         '  <rect width="760" height="560" fill="#ffffff"/>',
         texto(380, 32, "Cenários simulados: local da falta, tipo e sintonia do PLL",
               19, centro=True, negrito=True)]

    # cabecalho
    s.append('  <rect x="%d" y="%d" width="%d" height="%d" fill="#f1f5f9"/>'
             % (X0, Y_CAB, LARG_TAB, H_CAB))
    s.append(texto(X0 + 14, Y_CAB + 26, "Local da falta", 16, negrito=True))
    for i, t in enumerate(TIPOS):
        s.append(texto(XS[i] + LARG_COL // 2, Y_CAB + 26, ROTULO_TIPO[t], 16,
                       centro=True, negrito=True))

    # linhas de dados
    for j, local in enumerate(ORDEM):
        y = Y_CAB + H_CAB + j * H_LIN
        if j % 2:
            s.append('  <rect x="%d" y="%d" width="%d" height="%d" fill="#f8fafc"/>'
                     % (X0, y, LARG_TAB, H_LIN))
        s.append(texto(X0 + 14, y + 25, ROTULO_LOCAL[local]))
        for i, t in enumerate(TIPOS):
            s.extend(celula(XS[i] + LARG_COL // 2, y + 8, *m[local][t]))

    # regime permanente: celula unica, sem divisao por tipo de falta
    s.append('  <rect x="%d" y="%d" width="%d" height="%d" fill="#eef2f7"/>'
             % (X0, y_regime, LARG_TAB, H_REG))
    s.append(texto(X0 + 14, y_regime + 22, "Regime permanente"))
    s.append(texto(X0 + 14, y_regime + 40, "sem falta aplicada", 13, "#6b7280", italico=True))
    s.extend(celula(XS[0] + (3 * LARG_COL) // 2, y_regime + 14, *regime))

    # grade: as verticais internas param no regime, que e celula unica
    for i, x in enumerate([X0, XS[0], XS[1], XS[2], XS[3]]):
        s.append(LINHA % (x, Y_CAB, x, y_fim if i in (0, 1, 4) else y_regime))
    for y in [Y_CAB] + [Y_CAB + H_CAB + j * H_LIN for j in range(len(ORDEM) + 1)] + [y_fim]:
        s.append(LINHA % (X0, y, X0 + LARG_TAB, y))

    # legenda
    y_leg = y_fim + 32
    s.extend(chip(196, y_leg, "N", NAVY))
    s.append(texto(234, y_leg + 16, "sintonia nominal"))
    s.extend(chip(400, y_leg, "I", LARANJA))
    s.append(texto(438, y_leg + 16, "sintonia inadequada"))
    s.append(texto(380, y_leg + 50,
                   "%d cenários exportados: %d com sintonia nominal e %d com sintonia inadequada."
                   % (n_nom + n_ina, n_nom, n_ina), 14, "#6b7280", centro=True))
    s.append('</svg>')

    SAIDA.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("%s | %d nominais + %d inadequadas = %d" % (SAIDA.name, n_nom, n_ina, n_nom + n_ina))


if __name__ == "__main__":
    montar()
