"""Guia de estudos: cronograma de 30 min e mapa sequencial do TCC."""
from falas import SLIDE_SPEECHES
from gw_builder import PALCO_SPEECHES, WordRoteiroBuilder
from gw_util import *  # noqa: F401,F403


def inject_30min_schedule_and_tcc_map(wb: WordRoteiroBuilder):
    """Insere o Cronograma de 30 Minutos (PPTX 1-18 -> Palco 1-8 -> PPTX 19-20) e o Mapa Sequencial do TCC."""
    wb.h("Cronograma de 30 Minutos e Ordem Exata de Falas ([Bruno] e [Victor])")
    wb.p(
        "Abaixo está a distribuição exata do tempo de fala na apresentação real (a 130 palavras por minuto), "
        "percorrendo os <b>Slides 1 a 19 no PowerPoint</b>, a <b>passagem no Slide 20</b>, os <b>8 Capítulos do "
        "Modo Apresentação no Painel HTML</b> (avançados com a seta &#8594; ou PageDown) e o <b>fechamento nos "
        "Slides 21 e 22</b>:"
    )

    schedule_rows = []
    cum_w = 0
    b_total = 0
    v_total = 0

    # 1. Slides 1 a 18
    slide_titles = {
        1: "Capa e abertura",
        2: "Expansão das renováveis (IEA / ONS)",
        3: "Eventos no mundo real (Brasil, Ibéria, Chile)",
        4: "Problema e objetivos",
        5: "Fonte renovável (Fig. 3.2)",
        6: "Transformada de Park (Eq. 3.5)",
        7: "Estrutura do SRF-PLL (Fig. 4.3)",
        8: "Sistema IEEE 9 barras e Thévenin (Fig. 4.1)",
        9: "Sintonia nominal do PLL (ts = 20 ms)",
        10: "Duas sintonias do PLL (nominal × inadequada)",
        11: "Referência de corrente (1ª versão PSIM)",
        12: "Filtro LCL (equivalente por fase)",
        13: "Controle de corrente (Fig. 3.1)",
        14: "Submódulo 2.10 do ONS (rampa e círculo)",
        15: "Sistema completo (Fig. 4.2)",
        16: "Protocolo de contingência e matriz (Tab. 4.1)",
        17: "Fluxo de análise e 5 métricas",
        18: "Porta para o painel (Alt+Tab -> Modo apresentação)",
    }

    for s_num in range(1, 19):
        txt = SLIDE_SPEECHES[s_num]
        w = len(txt.split())
        cum_w += w
        spks = []
        for p_part in txt.split("\n\n"):
            p_part = p_part.strip()
            if p_part.startswith("[Bruno]"):
                spks.append("Bruno")
                b_total += len(p_part[7:].split())
            elif p_part.startswith("[Victor]"):
                spks.append("Victor")
                v_total += len(p_part[8:].split())
        schedule_rows.append([
            f"Slide {s_num:02d}",
            slide_titles[s_num],
            " &#8594; ".join(spks),
            str(w),
            format_mmss(w / 130),
            format_mmss(cum_w / 130),
        ])

    # 2. Palco HTML 1 a 8
    palco_titles = {
        1: "Faltas destacadas (6 passos no mapa)",
        2: "Energização do inversor (§5.1, Fig. 5.3, 2 passos)",
        3: "Localização: quanto mais perto, mais severa (§5.2, 3 passos)",
        4: "Sequência negativa: espectro 120 Hz (§5.3, Fig. 5.10, 2 passos)",
        5: "Compromisso da sintonia: B6 bifásica (§5.3, Fig. 5.14, 3 passos)",
        6: "Perda de sincronismo: B7 trifásica e P absorvida (§5.4, 3 passos)",
        7: "Código de rede: Submódulo 2.10 e fecho (§5.5, 6 passos)",
        8: "Todos os casos: Tabelas 5.1 a 5.3 (apoio e saída Esc)",
    }

    for c_num in range(1, 9):
        items = PALCO_SPEECHES[c_num]
        w = sum(len(body.split()) for _, body, _ in items)
        cum_w += w
        spks = []
        for pref, body, _ in items:
            if "Bruno" in pref:
                spks.append("Bruno")
                b_total += len(body.split())
            else:
                spks.append("Victor")
                v_total += len(body.split())
        schedule_rows.append([
            f"Painel {c_num}/8",
            palco_titles[c_num],
            " &#8594; ".join(spks),
            str(w),
            format_mmss(w / 130),
            format_mmss(cum_w / 130),
        ])

    # 3. Slides 19 e 20
    for s_num, t_str in [(19, "Síntese dos resultados (Cap. 6)"), (20, "Trabalhos futuros e encerramento (Cap. 7)")]:
        txt = SLIDE_SPEECHES[s_num]
        w = len(txt.split())
        cum_w += w
        spks = []
        for p_part in txt.split("\n\n"):
            p_part = p_part.strip()
            if p_part.startswith("[Bruno]"):
                spks.append("Bruno")
                b_total += len(p_part[7:].split())
            elif p_part.startswith("[Victor]"):
                spks.append("Victor")
                v_total += len(p_part[8:].split())
        schedule_rows.append([
            f"Slide {s_num:02d}",
            t_str,
            " &#8594; ".join(spks),
            str(w),
            format_mmss(w / 130),
            format_mmss(cum_w / 130),
        ])

    wb.table(
        ["Etapa", "Conteúdo em Cena", "Ordem de Fala", "Pal.", "Tempo", "Relógio"],
        schedule_rows,
        [2.0, 6.2, 2.9, 1.1, 1.2, 1.3],
    )
    wb.note(
        f"Total cronometrado do percurso completo (Slides 1–18 + Palco 1–8 + Slides 19–20): "
        f"<b>{cum_w} palavras = {format_mmss(cum_w / 130)} min</b> a 130 palavras/minuto "
        f"(<b>Bruno:</b> {b_total} palavras / {round(100*b_total/cum_w)}%; "
        f"<b>Victor:</b> {v_total} palavras / {round(100*v_total/cum_w)}%)."
    )

    wb.h("Sequência do TCC (Capítulos 1 a 7) × Slides e Capítulos do Palco")
    wb.p(
        "Para estudar acompanhando a ordem exata dos capítulos do documento final entregue "
        "(<b>TCC_Victor_Bruno_VFinal.docx</b>), consulte a tabela de correspondência abaixo:"
    )
    wb.table(
        ["Capítulo / Seção do TCC", "Pontos Importantes, Equações e Figuras no TCC", "Onde Entra na Defesa"],
        [
            ["Cap. 1 — Introdução", "Contextualização, apagão de 15/08/2023, vulnerabilidade do SRF-PLL sob faltas, objetivo geral (inversor de 100 MW no IEEE 9 barras) e objetivos específicos.", "Slides 1, 2, 3 e 4"],
            ["Cap. 2 — §2.1 a §2.3\nTransição e Estabilidade", "IEA (2026): +600 TWh solares, 5%&#8594;17% no mundo; ONS (2025): 96,8 GW (> 85,8 GWmed, 35% no SIN). Classificação clássica IEEE/CIGRE 2004 (Gu e Green, 2023) vs. estendida IEEE PES TR77 (estabilidade guiada por conversores).", "Slides 2, 4, 5, 20 e 22"],
            ["Cap. 2 — §2.4\nGrandes Blecautes", "§2.4.1 Ibéria 2025 (ENTSO-E: 0,63 Hz, fator de potência fixo, >2,5 GW por sobretensão); §2.4.2 Chile 2025 (CEN: 11.066 MW, 73% solar+eólica, 2 ilhas em 1,5 s); §2.4.3 Brasil 2023 (RAP-ONS 00012/2023: 23.368 MW, 265 GW·s, suporte de reativo aquém dos modelos).", "Slide 3"],
            ["Cap. 2 — §2.5\nRequisitos Normativos", "Curva LVRT (Fig. 2.1) e rampa de injeção reativa do Submódulo 2.10 do ONS (Fig. 2.2): banda morta 0,85–1,10 pu, rampa (0,85−V)/0,35 saturando em 1 pu para V &#8804; 0,50 pu.", "Slides 14, 15, Painel 7 e Reserva"],
            ["Cap. 3 — §3.1 a §3.3\nPark, Potência dq e VSI", "Transformadas de Clarke e Park (Eqs. 3.1–3.7), potência instantânea e controle desacoplado (Eqs. 3.8–3.9), VSI conectado à rede (Fig. 3.2) e malha de corrente (Fig. 3.1).", "Slides 5, 6, 11 e 12"],
            ["Cap. 3 — §3.4 e §3.5\nSRF-PLL e Sintonia Canônica", "Estrutura PD/PI/VCO (Fig. 3.3 / 4.3, Eqs. 3.10–3.18), sintonia por 2ª ordem com &#958; = 0,707 e ts(1%) = 20 ms (Eqs. 3.19–3.20: Kp=460, Ki=105.820, &#969;n=325,3 rad/s) e sintonia da corrente (§3.5, Eqs. 3.21–3.23).", "Slides 7, 9, 10 e 12"],
            ["Cap. 4 — §4.1 a §4.3\nMetodologia e IEEE 9 Barras", "Abordagem Python/PSIM/Simulink (§4.2), IEEE 9 barras com UFV na Barra 2 e Thévenin (§4.3.1, Fig. 4.1), filtro LCL e controle completo (§4.3.2, Fig. 4.2, Eq. 4.2), matriz de cenários e protocolo de 6 ciclos (§4.3.3–4.3.4, Tab. 4.1).", "Slides 8, 12–18 e Painel 1"],
            ["Cap. 5 — §5.1 a §5.5\nResultados e Discussão", "§5.1 Energização (Fig. 5.3: 40 vs 79 ms); §5.2 Trifásicas (Fig. 5.7, Tab. 5.1: 9,2% a 58,4%); §5.3 Assimétricas (Figs. 5.10 e 5.14, Tab. 5.3: 120 Hz até 0,72 pu, >250×; B6 96°&#8594;34,5°; B7 retorno dobra); §5.4 Perda de sincronismo (Figs. 5.18–5.21: escorregamento de ciclo na B7 e L7-8, 66,8% absorvendo P); §5.5 Código de rede (Tab. 5.2: Q=0,09 pu na B7).", "Slide 18 &#8594; Painel 1 a 8 (e Reserva 23–28)"],
            ["Cap. 6 e Cap. 7\nConclusões e Trabalhos Futuros", "Cap. 6: síntese qualitativa, insuficiência do critério estático de permanecer conectado, ressalvas metodológicas (sobrecorrentes limitadas pelo controle e SCR fixo). Cap. 7: Eixo 1 (DDSRF-PLL e DSOGI-PLL) e Eixo 2 (varredura de SCR e múltiplos inversores).", "Slides 19 e 20"],
        ],
        [3.4, 8.5, 2.8],
    )
