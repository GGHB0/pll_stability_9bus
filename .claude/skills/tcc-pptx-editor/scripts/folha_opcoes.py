"""Folha de comparação de variantes de um slide (prévia com opções).

Uso: folha_opcoes.py <saida.png> <rotulo=png> [<rotulo=png> ...] [--recorte y0,y1]

Empilha os PNGs do render.ps1 (um por variante) com o rótulo em cima.
--recorte guarda só a faixa vertical y0-y1 (px) de cada PNG, para comparar
de perto a parte que muda (ex.: 90,600 = título e figura em 1600x900).
"""
import argparse

from PIL import Image, ImageDraw, ImageFont


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("saida")
    ap.add_argument("variantes", nargs="+", help="rotulo=caminho.png")
    ap.add_argument("--recorte", help="y0,y1 em px")
    a = ap.parse_args()
    ims = []
    for v in a.variantes:
        rot, png = v.split("=", 1)
        im = Image.open(png).convert("RGB")
        if a.recorte:
            y0, y1 = (int(x) for x in a.recorte.split(","))
            im = im.crop((0, y0, im.width, y1))
        ims.append((rot, im))
    w = max(i.width for _, i in ims)
    out = Image.new("RGB", (w, sum(i.height + 50 for _, i in ims)), "white")
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype("arialbd.ttf", 34)
    y = 0
    for rot, im in ims:
        d.text((20, y + 6), rot, fill="black", font=f)
        out.paste(im, (0, y + 50))
        y += im.height + 50
    out.save(a.saida)
    print(a.saida, out.size)


if __name__ == "__main__":
    main()
