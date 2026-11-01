"""Guia de estudos: o construtor completo e as caixas de fala (texto em falas/)."""
from falas import PALCO_FALAS, PONTOS, SLIDE_SPEECHES
from gw_blocos import _Blocos
from gw_texto import _Texto
from gw_util import *  # noqa: F401,F403

# Tópicos curtos dos slides sem caixa "O que falar" no roteiro de estudo (1-4, 17-21)
EXTRA_FALAS_TOPICOS = {n: PONTOS[n] for n in (1, 2, 3, 4, 16, 17, 18, 19, 20)}
# Falas do palco no formato da caixa: (rótulo, texto, cor)
PALCO_SPEECHES = {
    cap: [(f"[{quem}] ", texto, C_BRUNO if quem == "Bruno" else C_VICTOR) for quem, texto in falas]
    for cap, falas in PALCO_FALAS.items()
}


class WordRoteiroBuilder(_Texto, _Blocos):
    """Intercepta todos os comandos do gen_roteiro_estudo_defesa.py e constrói o Word (.docx)
    enriquecido com as falas completas de 30 minutos e o mapa do TCC."""

    def add_slide_speech_box(self, slide_num: int):
        """Adiciona os tópicos resumidos (se não estiverem no FALAS de 5-15) e a fala completa cronometrada."""
        if slide_num in EXTRA_FALAS_TOPICOS:
            topicos = [f"<b>{quem}:</b> {txt}" for quem, txt in EXTRA_FALAS_TOPICOS[slide_num]]
            self.box("fala", *topicos)

        speech_raw = SLIDE_SPEECHES.get(slide_num, "")
        if not speech_raw or slide_num in (21, 22):
            return
        paras = [p.strip() for p in speech_raw.split("\n\n") if p.strip()]
        formatted_lines = []
        tot_w = len(speech_raw.split())
        curr_spk = "Bruno"
        for p_txt in paras:
            if p_txt.startswith("[Bruno]"):
                curr_spk = "Bruno"
                body = p_txt[len("[Bruno]"):].strip()
            elif p_txt.startswith("[Victor]"):
                curr_spk = "Victor"
                body = p_txt[len("[Victor]"):].strip()
            else:
                body = p_txt
            w_c = len(body.split())
            spk_color = C_BRUNO if curr_spk == "Bruno" else C_VICTOR
            formatted_lines.append((f"[{curr_spk}] ({w_c} pal. ~ {format_mmss(w_c/130)}): ", body, spk_color))

        rot_Kind = "script" if slide_num <= 20 else "palco_s"
        label = (
            f"ORDEM DE FALAS PRONTA DO SLIDE {slide_num:02d} ({tot_w} palavras ~ {format_mmss(tot_w/130)})"
            if slide_num <= 20
            else f"FALA DE RESERVA DO SLIDE OCULTO {slide_num:02d} ({tot_w} palavras ~ {format_mmss(tot_w/130)})"
        )
        self.box(rot_Kind, *formatted_lines, titulo=label)

    def add_palco_speech_box(self, cap_num: int):
        """Adiciona o roteiro de fala passo a passo para o Capítulo `cap_num` do Modo Apresentação."""
        items = PALCO_SPEECHES.get(cap_num, [])
        if not items:
            return
        tot_w = sum(len(body.split()) for _, body, _ in items)
        self.box(
            "palco_s",
            *items,
            titulo=f"ORDEM DE FALAS NO PALCO · CAPÍTULO {cap_num}/8 ({tot_w} palavras ~ {format_mmss(tot_w/130)})",
        )
