"""Roteiro de estudo da defesa (PDF): slide a slide e capítulo a capítulo do palco.

Roda os arquivos de conteudo/ em ordem; os tópicos "O que falar" vêm de falas/.
Saída: output/roteiro_estudo_defesa.pdf.   Uso: pdf.py [--preview <pasta>]

Imagens: miniaturas dos slides em SLIDES_PNG (render.ps1 da tcc-pptx-editor sobre
uma cópia do deck) e telas do palco de scripts/verifica_palco.py, convertidas para
JPEG reduzido em CACHE antes de entrar no PDF.
"""
import sys
from pathlib import Path

import pdf_base
import pdf_blocos
from caminhos import conteudo_texto, entregar
from falas import FALAS


def fala(num):
    pdf_blocos.box("fala", *[f"<b>{quem}:</b> {texto}" for quem, texto in FALAS[num]])


def main():
    env = {**vars(pdf_base), **vars(pdf_blocos), "FALAS": FALAS, "fala": fala}
    exec(conteudo_texto(), env)
    out = pdf_base.n.build()
    print(out)
    entregar(Path(out), Path(out).name)
    if "--preview" in sys.argv:
        print(pdf_base.render_preview(out, sys.argv[sys.argv.index("--preview") + 1]))


if __name__ == "__main__":
    main()
