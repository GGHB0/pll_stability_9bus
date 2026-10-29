"""Roteiro de falas e controle de tempo da defesa (.docx).

Cronograma de 30 min, pontos a comentar e falas cronometradas de cada slide (1-20)
e capítulo do palco (1-8), mais apêndice e reserva (21-28). Texto em falas/.
Saída: output/Roteiro_Falas_e_Tempo_Defesa_TCC.docx + cópia no OneDrive.
"""
import docx

from caminhos import OUTPUT, entregar, salvar
from falas import APENDICE_E_RESERVA, PALCO_ROTEIRO, SLIDES_CONCLUSAO, SLIDES_ROTEIRO
from rf_caixa import add_part_banner, add_styled_box
from rf_cronograma import cabecalho_e_cronograma
from rf_item import add_item_section
from rf_util import *  # noqa: F401,F403

NOME = "Roteiro_Falas_e_Tempo_Defesa_TCC.docx"


def main():
    doc = docx.Document()
    item_clocks = cabecalho_e_cronograma(doc)

    # ==========================================================================
    # ROTEIRO DETALHADO ITEM A ITEM
    # ==========================================================================
    idx_global = 0

    add_part_banner(
        doc,
        "PARTE I · PowerPoint: Abertura, Motivação, Modelagem e Método (Slides 1 a 17)",
        "Relógio: 00:00 → 17:15 (17 min 15 s) · Bloco 1 (Slides 1 a 4) conduzido integralmente pelo Bruno; slides 5 a 17 alternados entre Victor e Bruno.",
    )
    for it in SLIDES_ROTEIRO[:17]:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    add_part_banner(
        doc,
        "PARTE II · A Passagem para o Painel Interativo (Slide 18)",
        "Relógio: 17:15 → 17:35 (20 s) · Transição via Alt+Tab para o navegador no Modo Apresentação.",
    )
    for it in SLIDES_ROTEIRO[17:]:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    add_part_banner(
        doc,
        "PARTE III · Painel Interativo HTML: Modo Apresentação (Capítulos 1 a 8)",
        "Relógio: 17:35 → 25:35 (8 min 00 s) · Avançar cada passo com Seta → ou PageDown conforme indicado nas falas.",
    )
    for it in PALCO_ROTEIRO:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    add_part_banner(
        doc,
        "PARTE IV · Retorno ao PowerPoint: Conclusão e Encerramento (Slides 19 e 20)",
        "Relógio: 25:35 → 27:45 (2 min 10 s + margem até 30:00) · Fechamento nos 3 pontos principais de apoio à conclusão.",
    )
    for it in SLIDES_CONCLUSAO:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    # ==========================================================================
    # PARTE V: APÊNDICE E SLIDES OCULTOS DE RESERVA (21 A 28)
    # ==========================================================================
    add_part_banner(
        doc,
        "PARTE V · Apêndice (Slides 21–22) e Reserva Oculta do Painel (Slides 23–28)",
        "Fora do tempo de 30 min · Acionar apenas na arguição ou se o navegador não puder ser exibido.",
    )

    for s_num, tipo_lbl, tit, ref, quando_usar, fala_curta in APENDICE_E_RESERVA:
        add_styled_box(
            doc,
            f"SLIDE {s_num:02d} ({tipo_lbl}) — {tit} [{ref}]",
            HEX_FALA_BG,
            HEX_NAVY,
            C_NAVY,
            [
                ("Quando usar / Ponto principal", quando_usar),
                ("Fala curta de apoio", fala_curta),
            ],
        )

    entregar(salvar(doc, OUTPUT / NOME), NOME)


if __name__ == "__main__":
    main()
