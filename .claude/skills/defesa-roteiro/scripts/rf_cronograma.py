"""Roteiro de falas: título, resumo de tempo e mapa de tempo item a item."""
from falas import PALCO_ROTEIRO, SLIDES_CONCLUSAO, SLIDES_ROTEIRO
from rf_caixa import add_part_banner, add_styled_box
from rf_util import *  # noqa: F401,F403


def cabecalho_e_cronograma(doc):
    """Escreve o início do documento e devolve o relógio (início, fim) de cada item."""
    # Margens A4 compactas e confortáveis para leitura
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(1.6)
        sec.bottom_margin = Cm(1.6)
        sec.left_margin = Cm(2.0)
        sec.right_margin = Cm(2.0)

    # Cabeçalho do documento
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("Roteiro Prático de Falas, Pontos-Chave e Controle de Tempo (30 min)")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(17)
    r_t.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_s = p_sub.add_run(
        "Defesa de TCC (UERJ 2026) · Bruno Henrique de Oliveira & Victor Hugo de Avelar Rezende\n"
        "Sincronizado com o Deck Final (28 slides: 1–20 Corpo + 21–28 Apêndice/Reserva), "
        "o Guia em PDF e o Painel Interativo Final (output/pll_metrics.html)"
    )
    r_s.font.name = "Calibri"
    r_s.font.size = Pt(9.5)
    r_s.font.color.rgb = C_MUTED

    # Calcular estatísticas globais e relógio item a item
    all_items = SLIDES_ROTEIRO + PALCO_ROTEIRO + SLIDES_CONCLUSAO
    words_bruno = 0
    words_victor = 0
    for it in all_items:
        for spk, txt in it["falas"]:
            w = count_words(txt)
            if "Bruno" in spk:
                words_bruno += w
            else:
                words_victor += w
    total_words = words_bruno + words_victor
    total_dur_s = sum(it["dur_s"] for it in all_items)

    # Resumo executivo de tempo
    add_styled_box(
        doc,
        "RESUMO DE CALIBRAÇÃO DO TEMPO TOTAL (META: 30 MINUTOS)",
        HEX_MSG_BG,
        HEX_MSG_BD,
        C_NAVY,
        [
            ("Tempo total planejado (fala + cliques no painel)", f"{fmt_mmss(total_dur_s)} min ({total_dur_s // 60} min exatos), deixando margem de segurança para transições."),
            ("Volume total de fala no corpo da defesa", f"{total_words} palavras (~{total_words / 130:.1f} min de fala pura a 130 palavras/min + ~{30 - total_words / 130:.1f} min para cliques e animações no Modo Apresentação)."),
            ("Divisão equilibrada entre a dupla", f"Bruno: {words_bruno} palavras ({words_bruno * 100 / total_words:.1f}%)   |   Victor: {words_victor} palavras ({words_victor * 100 / total_words:.1f}%)."),
            ("Convenções obrigatórias para a banca", "Usar sempre 'sintonia inadequada' (nunca BAD_PLL), 'escorregamento de ciclo' (nunca cycle slipping), 'simulação computacional' (sem a sigla de transitórios eletromagnéticos) e 'recuperar o sincronismo' (nunca reaquisitar)."),
        ],
    )

    # Tabela Cronograma Geral Item a Item
    add_part_banner(
        doc,
        "1. Mapa de Tempo Item a Item (Relógio Acumulado de 00:00 a 30:00)",
        "Use a coluna 'Relógio Acumulado' durante o ensaio para conferir se o ritmo está adiantado ou atrasado em cada bloco.",
    )

    headers = ["Item", "Título do Slide / Capítulo", "Bloco", "Oradores", "Palavras", "Tempo Alvo", "Relógio"]
    widths = [Cm(2.1), Cm(5.5), Cm(2.4), Cm(2.5), Cm(1.4), Cm(1.4), Cm(1.7)]
    t_sched = doc.add_table(rows=1, cols=len(headers))
    t_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sched.autofit = False
    repeat_header_row(t_sched.rows[0])
    prevent_row_split(t_sched.rows[0])

    for i, h in enumerate(headers):
        cell = t_sched.rows[0].cells[i]
        cell.width = widths[i]
        set_cell_bg(cell, HEX_NAVY)
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        set_cell_borders(cell, top=("single", 4, HEX_NAVY), bottom=("single", 4, HEX_NAVY))
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = C_WHITE

    clock = 0
    item_clocks = []
    for idx, it in enumerate(all_items):
        start_c = clock
        end_c = clock + it["dur_s"]
        clock = end_c
        item_clocks.append((start_c, end_c))

        w_it = sum(count_words(t) for _, t in it["falas"])
        label = f"Palco Cap. {it['num']}" if it["tipo"] == "PAINEL" else f"Slide {it['num']:02d}"
        row_vals = [
            label,
            it["titulo"].split(" (")[0],
            it["bloco"].split(" · ")[0],
            it["quem"],
            str(w_it),
            fmt_dur(it["dur_s"]),
            f"{fmt_mmss(start_c)}–{fmt_mmss(end_c)}",
        ]
        row = t_sched.add_row()
        prevent_row_split(row)
        bg = HEX_PALCO_BG if it["tipo"] == "PAINEL" else (HEX_ZEBRA if idx % 2 == 1 else "FFFFFF")
        for ci, val in enumerate(row_vals):
            cell = row.cells[ci]
            cell.width = widths[ci]
            set_cell_bg(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            set_cell_borders(cell, bottom=("single", 4, HEX_BORDER))
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.bold = ci in (0, 6)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_VICTOR if (it["tipo"] == "PAINEL" and ci == 0) else C_INK

    doc.add_page_break()

    return item_clocks
