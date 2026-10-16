"""Mapa dos slides: layout, formas (nome, tipo, posição em polegadas), texto e notas.

    python.exe dump_slides.py <deck.pptx> [--slides 3-7,10] [--notas] [--sem-texto] [--xml N]

--slides     intervalo (numeração do PowerPoint, base 1); padrão: todos
--notas      inclui as notas do apresentador inteiras (padrão: 1ª linha)
--sem-texto  só o esqueleto (nome, tipo, caixa), útil para achar a forma-alvo
--xml N      despeja o XML cru do slide N (para cirurgia que o python-pptx não cobre)

Saída longa: redirecionar para arquivo (> C:\\Temp\\defesa_<tema>\\dump.txt).
O nome da forma ("Moldura da figura", "Justificativa de ouro") é o que os
gen_*.py usam para localizar o alvo; idx entre colchetes desempata nomes repetidos.
"""
import argparse

from lxml import etree

from pptx_util import abrir, faixa, formas, notas, pol, texto_forma, tipo, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("--slides")
ap.add_argument("--notas", action="store_true")
ap.add_argument("--sem-texto", action="store_true")
ap.add_argument("--xml", type=int)
a = ap.parse_args()

prs = abrir(a.pptx)
slides = list(prs.slides)

if a.xml:
    print(etree.tostring(slides[a.xml - 1]._element, pretty_print=True, encoding="unicode"))
    raise SystemExit

print(f"{len(slides)} slides, {pol(prs.slide_width):.2f} x {pol(prs.slide_height):.2f} in")
for n in faixa(a.slides, len(slides)):
    s = slides[n - 1]
    oculto = " OCULTO" if s._element.get("show") == "0" else ""
    print(f"\n=== {n} [{s.slide_layout.name}]{oculto}")
    for i, (sh, prof) in enumerate(formas(s)):
        cx = f"@({pol(sh.left):.2f},{pol(sh.top):.2f}) {pol(sh.width):.2f}x{pol(sh.height):.2f}"
        extra = ""
        if tipo(sh) == "imagem":
            extra = f" img={sh.image.filename or '?'} {sh.image.size[0]}x{sh.image.size[1]}px"
        txt = "" if a.sem_texto else " " + texto_forma(sh)[:240]
        print(f"{'  ' * (prof + 1)}[{i}] {tipo(sh):6} \"{sh.name}\" {cx}{extra}{txt}")
    nt = notas(s)
    if nt:
        print("  NOTAS:", nt if a.notas else nt.splitlines()[0][:200])
