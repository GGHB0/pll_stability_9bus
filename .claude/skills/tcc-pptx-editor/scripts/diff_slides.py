"""Diferença de conteúdo entre dois decks: texto, tabelas, notas e imagens, slide a slide.

    python.exe diff_slides.py <antes.pptx> <depois.pptx> [--sem-notas]

Conferência pós-entrega (backup x canônico): só pode aparecer o que o plano
previa. Compara pelo número do slide; inserção/remoção de slide aparece como
diferença em todos os seguintes, então o cabeçalho avisa quando a contagem muda.
Imagens comparadas pelo SHA1 da mídia, não pelo nome do arquivo no pacote.
"""
import argparse
import difflib
import hashlib

from pptx_util import abrir, formas, notas, texto_forma, tipo, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("antes")
ap.add_argument("depois")
ap.add_argument("--sem-notas", action="store_true")
a = ap.parse_args()


def linhas(slide):
    out = []
    for sh, _ in formas(slide):
        if tipo(sh) == "imagem":
            out.append(f'[img "{sh.name}" {hashlib.sha1(sh.image.blob).hexdigest()[:10]}]')
        t = texto_forma(sh)
        if t.strip():
            out.append(f'"{sh.name}": {t}')
    if not a.sem_notas and notas(slide):
        out += ["NOTAS: " + ln for ln in notas(slide).splitlines() if ln.strip()]
    return out


A, B = list(abrir(a.antes).slides), list(abrir(a.depois).slides)
if len(A) != len(B):
    print(f"AVISO: {len(A)} -> {len(B)} slides; diferenças abaixo se deslocam")
mudou = 0
for n in range(1, max(len(A), len(B)) + 1):
    la = linhas(A[n - 1]) if n <= len(A) else []
    lb = linhas(B[n - 1]) if n <= len(B) else []
    d = [x for x in difflib.unified_diff(la, lb, lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    if d:
        mudou += 1
        print(f"\n=== slide {n}")
        print("\n".join(d))
print(f"\n{mudou} slide(s) com diferença")
