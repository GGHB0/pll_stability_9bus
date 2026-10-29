"""Fonte única das falas da defesa.

Os slides 1-21 e os capítulos do palco valem para os três materiais (roteiro de
falas, guia de estudos e áudios). O texto corrido, os tópicos e as falas do palco
saem daqui; nenhum gerador guarda fala própria.
"""
from .slides_01_09 import SLIDES_01_09
from .slides_10_18 import SLIDES_10_18
from .slide_19 import SLIDE_19
from .conclusao import APENDICE_E_RESERVA, SLIDES_CONCLUSAO
from .palco import PALCO_ROTEIRO
from .reserva import RESERVA_SPEECHES
from .topicos import FALAS

SLIDES_ROTEIRO = SLIDES_01_09 + SLIDES_10_18 + SLIDE_19


def _corrida(item):
    """Falas de um item em texto corrido: "[Bruno] ...\n\n[Victor] ..."."""
    return "\n\n".join(f"[{quem}] {texto}" for quem, texto in item["falas"])


_SLIDES = SLIDES_ROTEIRO + SLIDES_CONCLUSAO
SLIDE_SPEECHES = {it["num"]: _corrida(it) for it in _SLIDES}
SLIDE_SPEECHES.update(RESERVA_SPEECHES)
PONTOS = {it["num"]: it["pontos"] for it in _SLIDES}
PALCO_FALAS = {it["num"]: it["falas"] for it in PALCO_ROTEIRO}
