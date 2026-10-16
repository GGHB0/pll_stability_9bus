"""Acha texto nos slides (caixas, tabelas) e, com --notas, no roteiro de fala.

    python.exe find_text.py <deck.pptx> <padrão> [--regex] [--notas] [-i]

Saída: slide, forma (nome [idx]) e contexto. Contagem total no fim: é o
"count esperado" que a spec de um gen_*.py precisa informar.
"""
import argparse
import re

from pptx_util import abrir, formas, notas, texto_forma, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("padrao")
ap.add_argument("--regex", action="store_true")
ap.add_argument("--notas", action="store_true")
ap.add_argument("-i", action="store_true", help="ignora maiúsculas")
a = ap.parse_args()

flags = re.I if a.i else 0
pat = re.compile(a.padrao if a.regex else re.escape(a.padrao), flags)
total = 0


def mostra(onde, texto):
    global total
    for m in pat.finditer(texto):
        total += 1
        ini, fim = max(0, m.start() - 60), min(len(texto), m.end() + 60)
        print(f"{onde}: ...{texto[ini:fim]}...")


for n, s in enumerate(abrir(a.pptx).slides, 1):
    for i, (sh, _) in enumerate(formas(s)):
        mostra(f'slide {n} "{sh.name}" [{i}]', texto_forma(sh))
    if a.notas:
        mostra(f"slide {n} NOTAS", notas(s))
print(f"\ntotal: {total}")
