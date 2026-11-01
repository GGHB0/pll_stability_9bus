"""Troca a imagem de uma forma por um PNG novo, mantendo a moldura.

    python.exe troca_imagem.py <entrada.pptx> <slide> <forma> <novo.png> <saida.pptx> [--esticar]

<forma>   nome exato ("Image 0") ou índice [i] do dump_slides.py
Padrão:   o PNG novo cabe dentro da caixa antiga pela proporção dele, centrado
          (nunca deforma; a moldura ao redor continua certa).
--esticar ocupa a caixa inteira (só quando o PNG foi gerado na mesma proporção).

Troca a parte da imagem no pacote (a:blip r:embed) sem recriar a forma, então
nome, ordem de empilhamento e animações ficam. Se a mesma mídia for usada em
outro slide, só este slide muda (a relação nova é deste slide).
"""
import argparse

from PIL import Image

from pptx_util import abrir, formas, tipo, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("entrada")
ap.add_argument("slide", type=int)
ap.add_argument("forma")
ap.add_argument("png")
ap.add_argument("saida")
ap.add_argument("--esticar", action="store_true")
a = ap.parse_args()

prs = abrir(a.entrada)
slide = prs.slides[a.slide - 1]
lista = [sh for sh, _ in formas(slide)]
if a.forma.isdigit():
    alvo = lista[int(a.forma)]
else:
    cand = [sh for sh in lista if sh.name == a.forma]
    if len(cand) != 1:
        raise SystemExit(f"'{a.forma}' casou {len(cand)} formas no slide {a.slide}; usar o índice")
    alvo = cand[0]
if tipo(alvo) != "imagem":
    raise SystemExit(f"forma '{alvo.name}' não é imagem ({tipo(alvo)})")

x, y, w, h = alvo.left, alvo.top, alvo.width, alvo.height
_, rid = slide.part.get_or_add_image_part(a.png)
alvo._element.blipFill.blip.rEmbed = rid
alvo.crop_left = alvo.crop_right = alvo.crop_top = alvo.crop_bottom = 0

if not a.esticar:
    pw, ph = Image.open(a.png).size
    if pw / ph > w / h:
        nw, nh = w, int(w * ph / pw)
    else:
        nw, nh = int(h * pw / ph), h
    alvo.left, alvo.top = x + (w - nw) // 2, y + (h - nh) // 2
    alvo.width, alvo.height = nw, nh

prs.save(a.saida)
print(f"slide {a.slide} '{alvo.name}': {a.png} -> caixa "
      f"{alvo.width / 914400:.2f}x{alvo.height / 914400:.2f} in; gravado {a.saida}")
