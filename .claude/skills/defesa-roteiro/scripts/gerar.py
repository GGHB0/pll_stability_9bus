"""Ponto de entrada único dos materiais da defesa.

    .venv\\Scripts\\python.exe .claude\\skills\\defesa-roteiro\\scripts\\gerar.py <alvo>...

Alvos: roteiro (falas e tempo, .docx), guia (guia de estudos, .docx), pdf (roteiro de
estudo), audios (edge-tts, precisa de internet), docs (roteiro + guia + pdf).
--sem-onedrive: gera só em output/, sem copiar os .docx para o template no OneDrive.
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import caminhos  # noqa: E402,F401  (ajusta o sys.path para falas/ e pdfnote)

ALVOS = {"roteiro": "roteiro_falas", "guia": "guia", "pdf": "pdf", "audios": "audios"}
GRUPOS = {"docs": ["roteiro", "guia", "pdf"]}


def main(args):
    alvos = [a for arg in args if arg != "--sem-onedrive" for a in GRUPOS.get(arg, [arg])]
    if not alvos or any(a not in ALVOS for a in alvos):
        sys.exit(__doc__)
    for alvo in alvos:
        print(f"── {alvo}")
        mod = importlib.import_module(ALVOS[alvo])
        if alvo == "audios":
            import asyncio
            asyncio.run(mod.main())
        else:
            mod.main()


if __name__ == "__main__":
    main(sys.argv[1:])
