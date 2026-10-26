# -*- coding: utf-8 -*-
"""
Gera o documento Word completo de estudos e roteiro de fala para a Defesa de TCC (30 minutos):
- Segue a ordem exata dos 30 slides de Defesa_TCC_SRF-PLL.pptx
- Conecta cada slide à sequência de capítulos, seções, figuras, tabelas e equações do TCC
- Apresenta o cronograma exato para 30 minutos (130 palavras/min) e a divisão de falas [Bruno] e [Victor]
- Inclui as falas completas dos Slides 5, 6, 7 e 9 e o roteiro de demonstração ao vivo do painel HTML
- Inclui o Guia de Arguição da Banca (9 perguntas críticas + tabelas mestras do TCC)
"""
import shutil
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
PPTX_STAGED = Path(r"C:\Temp\defesa_s2_cards\final.pptx")
PPTX_CANON = Path(r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\Defesa_TCC_SRF-PLL.pptx")
OUT_LOCAL = ROOT / "output" / "Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx"
OUT_ONEDRIVE = Path(r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx")

# Paleta de cores alinhada ao deck da defesa
C_NAVY = RGBColor(0x0F, 0x17, 0x2A)      # #0F172A - Títulos principais
C_BLUE = RGBColor(0x1E, 0x3A, 0x8A)      # #1E3A8A - Subtítulos e destaques Bruno
C_TEAL = RGBColor(0x0F, 0x76, 0x6E)      # #0F766E - Destaques Victor
C_AMBER = RGBColor(0xB4, 0x53, 0x09)     # #B45309 - Alertas e pontos de atenção
C_MUTED = RGBColor(0x47, 0x55, 0x69)     # #475569 - Texto secundário
C_TEXT = RGBColor(0x1E, 0x29, 0x3B)      # #1E293B - Corpo do texto
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_cell_bg(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for b_name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        b = OxmlElement(f"w:{b_name}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), sz)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), color)
        borders.append(b)
    tblPr.append(borders)


def add_callout_box(doc, title: str, lines: list, bg_hex="F8FAFC", border_hex="1E3A8A", title_color=C_BLUE):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_bg(cell, bg_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "24")
    left_b.set(qn("w:color"), border_hex)
    tcBorders.append(left_b)
    for b_name in ["top", "bottom", "right"]:
        b = OxmlElement(f"w:{b_name}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), "E2E8F0")
        tcBorders.append(b)
    tcPr.append(tcBorders)

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(4)
    r_title = p0.add_run(title)
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = title_color

    for item in lines:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if isinstance(item, tuple):
            prefix, body, p_color = item
            rp = p.add_run(prefix)
            rp.bold = True
            rp.font.name = "Arial"
            rp.font.size = Pt(10)
            rp.font.color.rgb = p_color
            rb = p.add_run(body)
            rb.font.name = "Arial"
            rb.font.size = Pt(10)
            rb.font.color.rgb = C_TEXT
        else:
            rb = p.add_run(item)
            rb.font.name = "Arial"
            rb.font.size = Pt(10)
            rb.font.color.rgb = C_TEXT

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)


def add_heading_1(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "1E3A8A")
    pBdr.append(bottom)
    pPr.append(pBdr)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.color.rgb = C_NAVY
    return p


def add_heading_2(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.color.rgb = C_BLUE
    return p


def add_para(doc, text: str, bold_prefix: str = "", space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rp = p.add_run(bold_prefix)
        rp.bold = True
        rp.font.name = "Arial"
        rp.font.size = Pt(10)
        rp.font.color.rgb = C_NAVY
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = C_TEXT
    return p


def add_styled_table(doc, headers: list, rows: list, col_widths_cm: list = None, header_bg="0F172A"):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="CBD5E1", sz="4")

    # Header
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        set_cell_bg(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = C_WHITE

    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            set_cell_bg(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
            row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.color.rgb = C_TEXT
            if c_idx == 0:
                r.bold = True

    if col_widths_cm:
        for row in tbl.rows:
            for i, w in enumerate(col_widths_cm):
                row.cells[i].width = Cm(w)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)
    return tbl


# ==============================================================================
# FALAS COMPLETAS PARA OS SLIDES 5, 6, 7 E 9 (QUE ESTAVAM COM PLACEHOLDER)
# ==============================================================================
NEW_NOTES = {
    5: (
        "[Victor] Entrando na modelagem, a Figura 3.2 do TCC mostra como a usina se conecta à rede. "
        "A fonte primária é um barramento contínuo ideal, sem dinâmica do elo CC nem rastreamento de "
        "máxima potência, pois o foco está no sincronismo e na resposta à rede CA.\n\n"
        "[Bruno] O inversor converte essa energia contínua em corrente alternada trifásica, passa pelo "
        "filtro e entrega os 100 MW no ponto de conexão. Como opera como seguidor de rede, precisa "
        "medir a tensão local para que o SRF-PLL estime o ângulo e oriente a injeção de corrente."
    ),
    6: (
        "[Victor] Para controlar grandezas senoidais sem erro em regime, usamos a transformada de Park, "
        "na Equação 3.5 do TCC. Ela projeta as fases a, b e c nos eixos ortogonais d e q, que giram "
        "na mesma velocidade angular da rede.\n\n"
        "[Bruno] Com o referencial girando junto com o vetor da rede, as senoides de 60 Hz viram "
        "grandezas contínuas em regime permanente, onde os controladores PI operam com erro nulo. "
        "Mas a matriz depende do ângulo teta: quem precisa estimar esse ângulo em tempo real é o PLL."
    ),
    7: (
        "[Victor] A Figura 4.3 do TCC mostra a estrutura do SRF-PLL em três partes. A primeira é o "
        "detector de fase, a própria transformada de Park aplicada à tensão medida. Com o eixo d "
        "alinhado à tensão da rede, toda a amplitude fica em vd e vq vale zero.\n\n"
        "[Bruno] A segunda parte é o controlador PI, que recebe vq como erro e fornece a correção de "
        "velocidade delta ômega. Somada à frequência nominal, ela entra no oscilador controlado por "
        "tensão, um integrador que devolve o ângulo teta para a transformada de Park e para as malhas de corrente."
    ),
    9: (
        "[Bruno] Antes de montar o inversor completo, construímos esta bancada inicial no PSIM, "
        "conectando duas fontes trifásicas ideais pela impedância da rede. Sem chaves nem filtro LCL, "
        "isolamos exclusivamente o laço do SRF-PLL.\n\n"
        "[Victor] Essa etapa separa o sincronismo do resto do conversor: medindo a tensão no ponto de "
        "conexão, verificamos o zeramento de vq, o travamento do ângulo estimado e validamos os ganhos "
        "do PI detalhados no próximo slide."
    ),
    10: (
        "[Victor] Aqui está o projeto dos ganhos do PLL. Antes da transformada de Park, a tensão medida "
        "é dividida pela amplitude nominal de fase, 16.329,93 V de pico, entrando em pu com amplitude "
        "unitária. Assim, no detector de fase linearizado, vq é igual ao próprio erro angular e o ganho "
        "do detector vale 1.\n\n"
        "[Bruno] Com isso, a malha fechada assume a forma canônica de segunda ordem: o ganho integral é "
        "ômega n ao quadrado e o proporcional é 2 xi ômega n. Fixamos o amortecimento xi em 0,707, valor "
        "clássico de resposta ótima em Ogata, com sobre-elevação de cerca de 5%. Resta escolher apenas o "
        "tempo de acomodação.\n\n"
        "[Victor] Pelo critério de 1%, ts vale 4,6 sobre xi ômega n. Com ts curto demais, a banda alarga "
        "e o laço fica sensível a ruído e desequilíbrio; com ts longo demais, não acompanha variações da "
        "rede. Adotamos 20 ms, pouco mais de um ciclo, seguindo Alves, Dias e Rolim, de 2020, e "
        "Teodorescu, Liserre e Rodriguez, de 2011. Daí saem Kp igual a 460, frequência natural de "
        "325,3 rad/s, ou 51,8 Hz, e Ki igual a 105.820."
    ),
    23: "[Bruno] Material de apoio para a arguição: parâmetros da rede, do filtro LCL e das malhas de controle.",
    24: "[Victor] Material de apoio para a arguição: tabelas completas 5.1, 5.2 e 5.3 do Capítulo 5 do TCC.",
    30: (
        "[Bruno] Voltamos ao Submódulo 2.10 do ONS, que exige permanência conectada e injeção de corrente "
        "reativa conforme a queda de tensão: corrente máxima abaixo de 0,5 pu, rampa até 0,85 pu, banda "
        "morta entre 0,85 e 1,10 pu e absorção de reativo acima disso.\n\n"
        "[Victor] Com sintonia nominal sob faltas simétricas, o inversor cumpre a curva: na Barra 7, com "
        "0,10 pu de tensão média, a referência reativa satura em 1,0 pu e a ativa zera; na Linha 8-9, com "
        "0,48 pu, fica em 0,99 pu; na Barra 6, com 0,58 pu, entrega 0,72 pu frente aos 0,76 previstos pela rampa.\n\n"
        "[Bruno] Um ponto físico essencial: na Barra 7, mesmo com corrente reativa saturada em 1,0 pu, a "
        "potência reativa entregue é de apenas 0,09 pu, pois a potência é o produto da tensão pela corrente "
        "e a tensão caiu abaixo de 10%.\n\n"
        "[Victor] Já nas assimétricas e na perda de sincronismo, o inversor permanece conectado, mas "
        "entrega potência contaminada em 120 Hz ou drena energia da rede. Por isso, permanecer conectado "
        "não basta: é preciso auditar a qualidade dinâmica do rastreamento angular."
    ),
}


# ==============================================================================
# METADADOS RICOS DE CADA UM DOS 30 SLIDES (CONEXÃO TCC + PONTOS DE ESTUDO)
# ==============================================================================
SLIDE_STUDY_META = {
    1: {
        "bloco": "BLOCO 1 — MOTIVAÇÃO E OBJETIVOS",
        "titulo": "Capa: Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos",
        "tcc_ref": "Capa, Folha de Rosto e Resumo do TCC",
        "visual": "Título do trabalho, identificação UERJ / Engenharia Elétrica (Sistemas de Potência), autores (Bruno e Victor) e orientadores (Prof. Oscar Zevallos e Prof. André Alves).",
        "pontos_tcc": [
            "Postura inicial: saudação calma, apresentação da dupla e agradecimento aos orientadores e à banca.",
            "Deixar claro desde o início que a apresentação está organizada em 5 blocos lógicos: (1) Motivação e Contexto, (2) Fundamentação e Modelagem, (3) Metodologia de Contingência, (4) Resultados com Demonstração Interativa e (5) Conclusões.",
        ],
    },
    2: {
        "bloco": "BLOCO 1 — MOTIVAÇÃO E OBJETIVOS",
        "titulo": "Expansão das renováveis: Solar e eólica saltaram de 5% para 17% da geração mundial em uma década",
        "tcc_ref": "Cap. 1 (Introdução) e Cap. 2 — Seção 2.1 (Redes elétricas em transição: IEA 2026) + Dados ONS (2025)",
        "visual": "Gráfico de barras horizontais (Mundo 5% -> 17%; União Europeia -> ~30%; Brasil Solar+Eólica+MMGD -> 35%). Dois cartões à direita: 600 TWh (crescimento solar mundial em 2025, ~70% da expansão global) e 96,8 GW (capacidade eólica, solar e MMGD no SIN em 2025, +279% desde 2020, superando a carga média de 85,8 GWmed). Faixa inferior: perda de espaço da geração síncrona.",
        "pontos_tcc": [
            "No TCC (Seção 2.1), os dados globais vêm do relatório IEA Global Energy Review 2026: demanda global cresceu 3% (+800 TWh), adições renováveis bateram 800 GW (23º recorde anual) e solar PV cresceu 600 TWh (~70% do avanço líquido).",
            "Os dados brasileiros do ONS (2025) contextualizam a motivação nacional: 96,8 GW instalados de eólica, solar centralizada e MMGD (salto de 25,5 GW em 2020 para 96,8 GW em 2025, +279%), representando 35% da matriz do SIN e superando a carga média de 85,8 GWmed.",
            "Conceito físico chave (Seção 2.2 - Gu e Green, 2023): geradores síncronos acoplam-se eletromecanicamente à rede via inércia física (equação de oscilação). Inversores (IBR) são desacoplados pela eletrônica de potência; sua resposta depende inteiramente dos algoritmos de controle e sincronismo.",
        ],
    },
    3: {
        "bloco": "BLOCO 1 — MOTIVAÇÃO E OBJETIVOS",
        "titulo": "Eventos no mundo real: Os grandes blecautes recentes passaram pela geração conectada por inversores",
        "tcc_ref": "Cap. 1 (Introdução) e Cap. 2 — Seção 2.4 (Principais blecautes: 2.4.1 Ibéria 2025, 2.4.2 Chile 2025 e 2.4.3 Brasil 2023)",
        "visual": "Três cartões verticais comparando os grandes apagões: (1) SIN, Brasil (15/08/2023 — 23.368 MW, 34,5% da carga, abertura 500 kV Quixadá-Fortaleza II); (2) Península Ibérica (28/04/2025 — > 2,5 GW desconectados, oscilação de 0,63 Hz); (3) Chile (25/02/2025 — 11.066 MW, 73% solar e eólica, ilhamento em 1,5 s). Faixa inferior: o que une os três eventos.",
        "pontos_tcc": [
            "Brasil 15/08/2023 (RAP-ONS 00012/2023 — Seção 2.4.3): A causa raiz NÃO foi falta de inércia (o SIN tinha ~265 GW.s, bem acima do piso crítico de 150 GW.s) nem baixa potência de curto-circuito. Foi colapso de tensão porque o suporte dinâmico de reativos das usinas eólicas/UFVs em campo ficou muito aquém dos modelos matemáticos.",
            "Península Ibérica 28/04/2025 (ENTSO-E — Seção 2.4.1): Oscilação forçada de 0,63 Hz classificada como instabilidade guiada por conversor (converter-driven stability). Inversores operando em fator de potência fixo sem controle dinâmico de tensão causaram sobretensões e desligamento em cascata (> 2,5 GW).",
            "Chile 25/02/2025 (CEN — Seção 2.4.2): Abertura da LT 500 kV Nueva Maitencillo - Nueva Pan de Azúcar com 73% de penetração solar/eólica no norte. Ilhamento em 1,5 s e colapso por falta de suporte dinâmico de tensão dos inversores GFL.",
        ],
    },
    4: {
        "bloco": "BLOCO 1 — MOTIVAÇÃO E OBJETIVOS",
        "titulo": "Problema e objetivos: O SRF-PLL depende de uma tensão limpa, justamente o que a falta na rede destrói",
        "tcc_ref": "Cap. 1 (Objetivos Geral e Específicos) e Cap. 2 — Seção 2.3 (Classificação Estendida IEEE TR77 / CIGRE)",
        "visual": "À esquerda: diagrama da cadeia causal (1. Falta na Rede -> 2. Distúrbio no Referencial dq -> 3. Falha do SRF-PLL -> 4. Colapso do Controle Vetorial). À direita: cartões do Objetivo Geral (inversor de 100 MW no IEEE 9 barras) e Objetivos Específicos. Faixa inferior: pergunta central do trabalho.",
        "pontos_tcc": [
            "Enquadramento teórico (Seção 2.3 — Strauss-Mincu et al., 2026 / IEEE TR77): O fenômeno estudado é a Estabilidade Dominada por Conversores de Baixa Frequência (Low-Frequency Converter-Driven Stability, ~10 Hz), governada pela malha externa de sincronismo (SRF-PLL).",
            "Cadeia causal física: Falta na rede -> afundamento de amplitude + salto de fase + sequência negativa -> no referencial dq surgem queda do ganho do detector de fase e oscilação de 120 Hz (2*omega_0) -> erro em teta_PLL ou cycle slipping -> perda do desacoplamento entre id (ativo) e iq (reativo).",
            "Atenção para arguição: se perguntarem sobre 'sobrecorrentes' ou 'impedância da rede' citadas nos objetivos da Introdução, o Cap. 6 explica que as sobrecorrentes não se materializam (pois a malha de corrente satura a referência em 1,0 pu) e a impedância foi avaliada variando a distância elétrica da falta.",
        ],
    },
    5: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Fonte renovável: A usina fotovoltaica ou eólica se conecta à rede por um inversor seguidor de rede",
        "tcc_ref": "Cap. 2 — Seção 2.2 (GFL vs. GFM) e Cap. 3 — Seção 3.2 (Figura 3.2: VSI conectado à rede)",
        "visual": "Figura 3.2 do TCC (diagrama em blocos do VSI conectado à rede elétrica via filtro no PCC) e três cartões abaixo: Fonte primária (barramento CC ideal), Conversão (VSI CC -> CA trifásica) e Seguidor de rede (100 MW injetados no ângulo estimado pelo SRF-PLL).",
        "pontos_tcc": [
            "Delimitação de escopo (Seções 3.2 e 4.1): O lado CC é modelado como fonte de tensão contínua ideal (sem dinâmica do capacitor do elo CC e sem MPPT). Isso isola a dinâmica do lado CA e do sincronismo.",
            "Conceito de Seguidor de Rede (Grid-Following — GFL): O conversor comporta-se como uma fonte de corrente controlada, sincronizada ao vetor de tensão medido no Ponto de Acoplamento Comum (PCC). Ele não impõe frequência nem tensão de forma autônoma.",
        ],
    },
    6: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Transformada de Park: Girando com a rede, a transformada de Park torna constantes as grandezas trifásicas",
        "tcc_ref": "Cap. 3 — Seção 3.1 (Transformadas de Clarke e Park — Equações 3.1 a 3.5)",
        "visual": "Equação (3.5) do TCC (matriz da transformada de Park abc -> dq0 em função de teta) à esquerda; dois cartões à direita: 'Senoides viram constantes' e 'PI sem erro em regime'. Faixa inferior: dependência do ângulo teta real.",
        "pontos_tcc": [
            "Por que não usar controladores PI direto em abc? Porque controladores PI têm ganho infinito apenas em frequência zero (CC). Aplicados a senoides de 60 Hz, produzem erro de amplitude e atraso de fase em regime permanente.",
            "Ao projetar as fases abc num referencial síncrono dq que gira a omega_0 = 376,99 rad/s (Equação 3.5), componentes fundamentais de sequência positiva tornam-se sinais contínuos (CC), permitindo erro nulo com controladores PI.",
            "Ponto vulnerável: a matriz de Park usa cos(teta) e sin(teta). Se o ângulo estimado teta_PLL divergir do ângulo real da rede teta_rede, a projeção inteira gira em falso.",
        ],
    },
    7: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Estrutura do SRF-PLL: O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede",
        "tcc_ref": "Cap. 3 — Seção 3.4 (Equações 3.10 a 3.18) e Cap. 4 — Seção 4.3.2.3 (Figura 4.3)",
        "visual": "Figura 4.3 do TCC (diagrama de blocos do SRF-PLL: Transformada de Park / Detector de Fase -> Filtro de Laço PI -> VCO integrador com pré-alimentação omega_0 = 2*pi*60) e equação característica de 2ª ordem embaixo; 3 cartões à direita (Detector de fase, Controlador PI, VCO).",
        "pontos_tcc": [
            "Princípio de funcionamento (Seção 3.4): Aplicando Park à tensão da rede, obtemos vd = Vm*cos(teta_rede - teta_PLL) e vq = Vm*sin(teta_rede - teta_PLL).",
            "Quando o erro angular delta_teta = teta_rede - teta_PLL é pequeno, sin(delta_teta) ~ delta_teta e cos(delta_teta) ~ 1. Logo, vd ~ Vm (toda a amplitude da tensão fica no eixo d) e vq ~ Vm * delta_teta.",
            "O controlador PI força vq -> 0, garantindo teta_PLL = teta_rede. A equação característica em malha fechada (Equação 3.17) é s^2 + Kp_PLL*U*s + Ki_PLL*U = 0, onde U é a amplitude da tensão em pu.",
        ],
    },
    8: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Sistema IEEE 9 barras: A UFV assume a Barra 2 e enxerga o resto da rede como um equivalente de Thévenin",
        "tcc_ref": "Cap. 4 — Seções 4.2 (Plataformas de simulação) e 4.3.1 (Modelo da rede e equivalente de Thévenin — Figura 4.1)",
        "visual": "Figura 4.1 do TCC (diagrama unifilar do sistema IEEE 9 barras modificado, com a UFV de 100 MW conectada na Barra 2 no lugar de G2); dois cartões à direita (Substituição e Redução de Thévenin).",
        "pontos_tcc": [
            "Topologia do sistema (Seção 4.3.1): Rede clássica de Anderson e Fouad (2003) em 230 kV, 60 Hz, base S_base = 100 MVA. Possui 3 geradores, 3 transformadores elevadores, 6 linhas de transmissão e 3 cargas.",
            "Modificação: O gerador síncrono G2 na Barra 2 (originalmente 192 MVA) foi substituído pela UFV de 100 MW (1,0 pu). Os geradores síncronos G1 (Barra 1, barra swing) e G3 (Barra 3) permanecem no sistema mantendo a inércia remanescente.",
            "Equivalente de Thévenin: Calculado a partir do elemento diagonal Z_22 da matriz de impedância nodal Z_barra na Barra 2, permitindo representar a rede vista pelo inversor no PSIM com fidelidade à rede completa do Simulink.",
        ],
    },
    9: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Bancada do PLL: Antes do inversor, o SRF-PLL foi testado isolado entre duas fontes ideais",
        "tcc_ref": "Cap. 4 — Seção 4.2 (Validação em etapas: Python -> PSIM -> Simulink)",
        "visual": "Esquemático da bancada inicial no PSIM (duas fontes trifásicas ideais conectadas por impedância, com o bloco SRF-PLL medindo a tensão no PCC) e três cartões à direita: Sem conversor, Travamento e Ganhos.",
        "pontos_tcc": [
            "Exceção didática aprovada para a defesa: esta figura vem do arquivo PSIM do projeto e ilustra a Seção 4.2 do TCC (metodologia multi-plataforma).",
            "Por que testar entre duas fontes ideais antes de colocar o VSI e o filtro LCL? Para isolar a malha de sincronismo (PD + PI + VCO) de qualquer harmônico de chaveamento ou interação com a malha de corrente.",
        ],
    },
    10: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Sintonia do PLL: Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação",
        "tcc_ref": "Cap. 3 — Seção 3.4 (Equações 3.18 a 3.20) e Cap. 4 — Seção 4.3.2.3",
        "visual": "Fluxo em 5 passos: (1) Tensão em pu (v_abc / 16.329,93 V de pico -> Vm = 1 pu); (2) Linearizar (vq ~ Vm*(teta_ref - teta_PLL), Kpd = 1); (3) Forma canônica (Ki = omega_n^2, Kp = 2*xi*omega_n); (4) Fixar xi = 0,707 (sobre-elevação ~5%); (5) Escolher ts = 20 ms pelo critério de 1% (ts = 4,6 / (xi*omega_n)), chegando a Kp_PLL = 460, omega_n = 325,3 rad/s (51,8 Hz) e Ki_PLL = 105.820.",
        "pontos_tcc": [
            "Normalização da tensão na entrada do PLL: Tensão nominal de linha na Barra 2 = 20 kV eficazes -> tensão de fase de pico = 20.000 * sqrt(2)/sqrt(3) = 16.329,93 V. Dividindo v_abc por 16.329,93 V antes da matriz de Park, U = 1 pu em condição nominal!",
            "Equações de projeto (Equações 3.18–3.20): Comparando s^2 + Kp*s + Ki = 0 com s^2 + 2*xi*omega_n*s + omega_n^2 = 0 (Ogata, 2009), com xi = 1/sqrt(2) = 0,707 e ts(1%) = 4,6/(xi*omega_n) = 20 ms (Alves, Dias e Rolim, 2020; Teodorescu et al., 2011): Kp_PLL = 9,2 / 0,020 = 460; omega_n = 4,6 / (0,707 * 0,020) = 325,3 rad/s (51,8 Hz); Ki_PLL = 325,3^2 = 105.820.",
            "Observação física crucial: durante um afundamento de tensão (U < 1 pu), o ganho efetivo do detector de fase cai proporcionalmente a U, reduzindo o amortecimento efetivo do laço!",
        ],
    },
    11: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Duas sintonias do PLL: A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos amortecido",
        "tcc_ref": "Cap. 3 — Seção 3.4 e Cap. 4 — Seção 4.3.2.3",
        "visual": "Tabela comparando Sintonia Nominal (Kp = 460, Ki = 105.820, omega_n = 325,3 rad/s, xi = 0,707) vs. Sintonia Inadequada x0,2 (Kp = 92, Ki = 21.164, omega_n = 145,5 rad/s, xi = 0,316). Cartão à direita: 2*omega_0 = 2,32 * omega_n (oscilação de 754 rad/s em vq sob falta assimétrica).",
        "pontos_tcc": [
            "Por que multiplicar Kp e Ki por 0,20 (redução de 80%) reduz tanto omega_n quanto xi? Porque Ki = omega_n^2, então reduzir Ki para 20% reduz omega_n por sqrt(0,2) = 0,447 (de 325,3 para 145,5 rad/s, ou 23,2 Hz). Como Kp = 2*xi*omega_n também caiu para 20%, o amortecimento xi cai por sqrt(0,2): 0,707 * 0,447 = 0,316!",
            "Relação 2*omega_0 = 2,32 * omega_n (Seção 3.4): Sob falta assimétrica, a sequência negativa gira a -omega_0, aparecendo no referencial positivo (+omega_0) a 2*omega_0 = 120 Hz = 754 rad/s. Para a sintonia nominal, 754 / 325,3 = 2,32. Como está muito próximo da frequência natural do filtro, o PI não rejeita os 120 Hz.",
        ],
    },
    12: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Referência de corrente: Na primeira versão do inversor, a referência de corrente saía direto da potência desejada",
        "tcc_ref": "Cap. 3 — Seção 3.1.3 (Controle P/Q desacoplado — Equações 3.6 a 3.9)",
        "visual": "Esquemático da geração de referência no PSIM (degrau de potência ativa P = 1 pu em 35 ms e Q = 0 divididos por vd para gerar id,ref e iq,ref) e caixa da Equação (3.9) do TCC: id,ref = 2P/(3*vd) e iq,ref = -2Q/(3*vd).",
        "pontos_tcc": [
            "Equações de potência instantânea em dq (Seção 3.1.3): P = (3/2)*(vd*id + vq*iq) e Q = (3/2)*(vq*id - vd*iq).",
            "Quando o SRF-PLL está perfeitamente travado, vq = 0! Então as equações simplificam para P = (3/2)*vd*id e Q = -(3/2)*vd*iq (em pu, o fator 3/2 é absorvido na base). Assim, id controla exclusivamente a potência ativa P, e iq controla exclusivamente a potência reativa Q.",
            "Se o PLL perde o alinhamento (vq != 0), id e iq deixam de ser desacoplados: injetar id passa a gerar reativo indesejado e vice-versa!",
        ],
    },
    13: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Controle de corrente: Um PI com notch em cada eixo faz a corrente do inversor seguir a referência",
        "tcc_ref": "Cap. 3 — Seções 3.3 e 3.5 (Figura 3.1 e Equações 3.21 a 3.23) e Cap. 4 — Seções 4.3.2.1 e 4.3.2.2",
        "visual": "Figura 3.1 do TCC (malha de controle de corrente em dq com PI + Filtro Notch + PWM -> filtro LCL); três cartões embaixo: 1. PWM (VSI 2 níveis a 5 kHz), 2. Filtro LCL (Lest = 30,71 mH, omega_res = 9.068,99 rad/s, xi = 0,707) e 3. PI de corrente (xi = 0,707, omega_n = 4*sqrt(2)*fg, Kp = 8*fg*Lest, Ki = 32*fg^2*Lest).",
        "pontos_tcc": [
            "Sintonia da malha de corrente (Seção 3.5 e 4.3.2.2 — metodologia de Alves, 2022): A planta simplificada em baixas frequências é o indutor equivalente Lest = L1 + L2 = 30,71 mH, G(s) = 1/(s*Lest). Aplicando a forma canônica de 2ª ordem com xi = 0,707 e acomodação em 1 ciclo da rede (16,67 ms -> omega_n = 4*sqrt(2)*fg = 339,4 rad/s), obtém-se Kp = 8*fg*Lest = 14,74 e Ki = 32*fg^2*Lest = 35.383,87 (escalados no bloco por pu/modulação para 0,2831 e 6,47).",
            "Filtro LCL e Notch (Seção 4.3.2.1): Ressonância em omega_res = 9.068,99 rad/s (~1.443 Hz), posicionada entre os 60 Hz da rede e os 5 kHz do PWM. Além do amortecimento passivo por resistores em série com os capacitores, há um filtro rejeita-faixa (notch) sintonizado em omega_res na saída do PI.",
            "Distinção fundamental para a banca: os ganhos do PI de corrente ficam FIXOS em todas as 29 simulações; apenas os ganhos do PI do SRF-PLL variam entre nominal e inadequada.",
        ],
    },
    14: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Referência pelo ONS: No modelo final, as referências fixas deram lugar ao bloco do Submódulo 2.10",
        "tcc_ref": "Cap. 2 — Seção 2.5.2 (Submódulo 2.10 do ONS) e Cap. 4 — Seção 4.3.2 (Figura 4.2)",
        "visual": "Recorte do controle digital da Figura 4.2 do TCC mostrando o bloco 'Controle do ONS - Submódulo 2.10' recebendo V_PCC e entregando id,ref e iq,ref para a malha de corrente, enquanto o SRF-PLL fornece teta_PLL para as transformadas de tensão e corrente.",
        "pontos_tcc": [
            "Evolução do modelo: Na bancada preliminar (Slide 12), P e Q eram fixos (1 pu e 0). No modelo sistêmico final (Figura 4.2), um gerador real no SIN não pode operar com referência cega durante afundamentos: ele precisa obedecer aos Procedimentos de Rede do ONS (Submódulo 2.10).",
            "Arquitetura de papéis: O bloco do ONS responde 'QUANTO' injetar de corrente ativa e reativa em função do módulo da tensão no PCC; já o SRF-PLL responde 'EM QUE DIREÇÃO' (ângulo teta_PLL) injetar essas correntes.",
        ],
    },
    15: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Dentro do Submódulo 2.10: A tensão medida define o reativo, e o ativo fica com o que sobra",
        "tcc_ref": "Cap. 2 — Seções 2.5.1 e 2.5.2 (Figuras 2.1 e 2.2 — LVRT e injeção de corrente reativa do ONS)",
        "visual": "Figura 2.2 do TCC (curva de injeção/absorção de corrente reativa por faixa de tensão do ONS) ligada ao diagrama interno do bloco Submódulo 2.10 no Simulink (cálculo da rampa, saturação e prioridade reativa).",
        "pontos_tcc": [
            "Regra das faixas de tensão (Seção 2.5.2 — ONS, 2022): Entre 0,85 pu e 1,10 pu (banda morta normal), a injeção adicional de reativo é zero e o inversor entrega 1,0 pu de corrente ativa.",
            "Para subtensões (V < 0,85 pu): entra a rampa de suporte reativo Iq_ref = (0,85 - V) / 0,35, que vai de 0% em 0,85 pu até 100% da corrente nominal (1,0 pu) quando V <= 0,50 pu. Para sobretensões (V > 1,10 pu), o inversor absorve reativo.",
            "Prioridade de corrente reativa com limitação de corrente total: A capacidade térmica dos IGBTs limita a corrente aparente total a I_max = 1,0 pu. Logo, Id_ref = sqrt(I_max^2 - Iq_ref^2). Quando V <= 0,50 pu, Iq_ref = 1,0 pu e Id_ref vai a ZERO.",
        ],
    },
    16: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Lógica em blocos: No código, a faixa de tensão escolhe o caminho e a prioridade divide a corrente",
        "tcc_ref": "Cap. 2 — Seção 2.5.2 e Cap. 4 — Seção 4.3.2",
        "visual": "Fluxograma em blocos da rotina implementada no Simulink: leitura de V_PCC -> decisão de faixa (V < 0,85 pu, normal, ou V > 1,10 pu) -> limitação de iq_ref a I_max -> cálculo do ativo remanescente id_ref -> saída para a malha de corrente.",
        "pontos_tcc": [
            "Este slide fecha a explicação didática do código dentro do bloco ONS antes de mostrar a planta completa no Slide 17.",
            "Destaque importante para a recomposição pós-falta: assim que a falta é eliminada em 0,4 s e a tensão retorna para dentro da faixa normal (acima de 0,85 pu), o bloco zera iq_ref e devolve id_ref para 1,0 pu automaticamente.",
        ],
    },
    17: {
        "bloco": "BLOCO 2 — FUNDAMENTAÇÃO TEÓRICA E MODELAGEM",
        "titulo": "Sistema completo: Juntando as partes, este é o inversor usado em todas as simulações",
        "tcc_ref": "Cap. 4 — Seção 4.3.2 (Figura 4.2 completa: Inversor, filtro LCL, PCC e controle digital)",
        "visual": "Figura 4.2 integral do TCC no centro, sintetizando os 3 subsistemas: (1) Sincronismo (SRF-PLL), (2) Referência normativa (Submódulo 2.10 ONS) e (3) Controle de Corrente + PWM + Filtro LCL conectado à Barra 2.",
        "pontos_tcc": [
            "Fechamento do Bloco 2 (Modelagem): Aqui a banca enxerga como todos os elementos explicados nos Slides 5 a 16 se encaixam na Figura 4.2 do TCC.",
            "Transição limpa para o Bloco 3 (Método): Com o inversor modelado e validado na Barra 2, o próximo passo é definir o protocolo de faltas na rede IEEE 9 barras.",
        ],
    },
    18: {
        "bloco": "BLOCO 3 — METODOLOGIA E FLUXO DE ANÁLISE",
        "titulo": "Protocolo de contingência: Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da falta",
        "tcc_ref": "Cap. 4 — Seções 4.3.3 (Tabela 4.1 — Matriz de cenários) e 4.3.4 (Protocolos de contingência)",
        "visual": "No topo: linha do tempo da simulação (0 a 0,1 s Inicialização; 0,1 a 0,3 s Pré-falta; 0,3 a 0,4 s Falta de 100 ms / 6 ciclos; 0,4 a 0,6 s Pós-falta de 200 ms). Embaixo: Tabela 4.1 de cenários (Barras 7, Linha 7-8, Linha 8-9, Barra 6 analisadas em detalhe; Barras 4, 5, 8 e 9 consultáveis no painel; N = Nominal, I = Inadequada).",
        "pontos_tcc": [
            "Duração da falta (Seção 4.3.4): 100 ms (6 ciclos de 60 Hz), tempo típico de atuação da proteção primária em linhas de transmissão de 230 kV.",
            "Janela de observação pós-falta: 200 ms após a abertura do defeito. Nota técnica para a banca: nas rodadas com sintonia inadequada, o instante absoluto de aplicação foi 0,6 a 0,7 s (pois o PLL lento demora 79 ms na partida), mas todos os gráficos são alinhados pela janela relativa ao início da falta.",
            "Contagem exata de cenários (Seção 4.3.3): 29 simulações no total (28 com falta + 1 de regime permanente com as duas sintonias), sendo 21 com sintonia nominal e 8 com sintonia inadequada.",
        ],
    },
    19: {
        "bloco": "BLOCO 3 — METODOLOGIA E FLUXO DE ANÁLISE",
        "titulo": "Fluxo de análise: Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel interativo",
        "tcc_ref": "Cap. 4 — Seção 4.3.3 (Monitoramento e tratamento de dados) e Cap. 5 (Métricas das Tabelas 5.1, 5.2 e 5.3)",
        "visual": "Fluxo em 4 etapas (1. Simulink -> 2. Arquivos CSV -> 3. Python -> 4. Painel interativo) e tabela inferior definindo as 5 métricas padronizadas: Retenção de Vd (%), Pico do erro de fase (após o 1º ciclo da falta), Retorno à faixa de +/-2 graus (desde a eliminação), Componente de 120 Hz (FFT de Vd na falta) e P e Q médios.",
        "pontos_tcc": [
            "Rigor no processamento (Seção 4.3.3): O Simulink exporta sinais da planta (passo de 1 microssegundo) e do controle; o pipeline em Python alinha as séries temporais e extrai automaticamente os indicadores numéricos das Tabelas 5.1 a 5.3.",
            "Por que o pico do erro de fase exclui o 1º ciclo da falta (primeiros 16,67 ms)? Para separar o pico puramente geométrico do salto instantâneo de fase na aplicação do curto-circuito da resposta dinâmica do laço do PLL.",
        ],
    },
    20: {
        "bloco": "BLOCO 4 — RESULTADOS E DEMONSTRAÇÃO AO VIVO",
        "titulo": "Demonstração ao vivo: No painel interativo, três casos resumem o comportamento dos 28 cenários",
        "tcc_ref": "Cap. 5 Completo — Seções 5.1 a 5.5 (Figuras 5.1 a 5.21 e Tabelas 5.1 a 5.3) via Dashboard output/pll_metrics.html",
        "visual": "Botão de abertura do painel interativo (pll_metrics.html) e três cartões de roteiro: (1) Falta Trifásica na Barra 7 — Sintonia Nominal (9,2% retido, reconverge em 98 ms); (2) Mesma Falta — Sintonia Inadequada (8,2% retido, cycle slipping +/-180 graus e absorção ativa em 66,8% do tempo); (3) Falta Bifásica na Barra 7 — Análise Espectral FFT (pico de 120 Hz de 0,72 pu em Vd).",
        "pontos_tcc": [
            "ESTE É O SLIDE PIVÔ DOS RESULTADOS! Ao abrir o painel HTML (output/pll_metrics.html), a aba 'Análise TCC' traz 7 sub-abas numeradas (1 Energização, 2 Localização, 3 Perda de sincronismo, 4 Sequência negativa, 5 Compromisso da sintonia, 6 Código de rede, 7 Todos os casos) que correspondem exatamente aos Slides 25 a 30 e 24.",
            "Estratégia de tempo para fechar em 30 minutos: Você pode conduzir toda a apresentação do Capítulo 5 diretamente dentro do painel HTML (guiando-se pelas sub-abas 1 a 6 cujos textos de fala estão detalhados nos Slides 25 a 30 abaixo) e, ao terminar a sub-aba 6, voltar para o PowerPoint diretamente no Slide 21 (Síntese dos Resultados)!",
            "Atenção na demonstração ao vivo: nos cartões superiores do Simulador Interativo, o cartão mostra |V| na Barra 2 (8,3%), enquanto a Tabela 5.1 do TCC mostra a retenção de Vd (9,2%). Cite verbalmente 9,2% como no TCC.",
        ],
    },
    21: {
        "bloco": "BLOCO 5 — CONCLUSÕES E TRABALHOS FUTUROS",
        "titulo": "Síntese dos resultados: O sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico",
        "tcc_ref": "Cap. 5 — Seção 5.6 (Resumo do capítulo) e Cap. 6 (Conclusões)",
        "visual": "Três cartões síntese: (1) '9,2% Vres — Faltas simétricas' (reconvergência em 98 ms na B7 com sintonia nominal; severidade ditada pela distância elétrica); (2) '250x mais 120 Hz — Faltas assimétricas' (fragilidade estrutural à sequência negativa, contaminando P e Q); (3) '66,8% do tempo — Sensibilidade de ganhos' (cycle slipping na B7 com sintonia inadequada, drenando potência ativa da rede). Faixa inferior: conclusão central da defesa.",
        "pontos_tcc": [
            "Síntese dos três pilares do Cap. 6: (1) Em faltas equilibradas, o SRF-PLL bem sintonizado é robusto mesmo sob afundamento severo (9,2% de Vd); (2) Em faltas desequilibradas, a limitação é estrutural da topologia SRF-PLL clássica frente aos 120 Hz; (3) Reduzir ganhos suaviza a falta moderada mas causa perda de sincronismo (cycle slipping) na falta severa.",
            "Tese regulatória central (Seção 5.5 e Cap. 6): Os códigos de rede atuais (como o Submódulo 2.10 do ONS) avaliam a suportabilidade (LVRT) pela permanência física conectada e pela referência de corrente reativa. Porém, se o PLL perde o sincronismo, o inversor permanece conectado mas injeta corrente com fase errada e absorve potência ativa da rede!",
        ],
    },
    22: {
        "bloco": "BLOCO 5 — CONCLUSÕES E TRABALHOS FUTUROS",
        "titulo": "Trabalhos futuros e encerramento: Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho",
        "tcc_ref": "Cap. 6 (Limites de validade) e Cap. 7 (Trabalhos Futuros)",
        "visual": "À esquerda: 2 eixos de trabalhos futuros — (1) Novas estruturas de sincronismo (DDSRF-PLL e DSOGI) e (2) Varrer relação de curto-circuito (SCR) e múltiplos inversores — mais caixa de Limites do estudo. À direita: cartão de encerramento ('Obrigado!', agradecimentos aos orientadores e à banca, botão para abrir o painel interativo na arguição).",
        "pontos_tcc": [
            "Transparência metodológica (Cap. 6): O trabalho utilizou nível de curto-circuito fixo no IEEE 9 barras, duas sintonias contrastantes e janela pós-falta de 200 ms. Ele demonstra um mecanismo físico-dinâmico rigoroso, não um envelope universal.",
            "Eixo 1 do Cap. 7 (Rodriguez et al., 2007; Teodorescu et al., 2011): Substituir o SRF-PLL clássico pelo DDSRF-PLL (Decoupled Double Synchronous Reference Frame) ou pelo DSOGI-PLL, que desacoplam a sequência negativa antes do detector de fase, eliminando a oscilação de 120 Hz sem precisar reduzir a banda passante do PI.",
            "Eixo 2 do Cap. 7 (Wu e Wang, 2020; Strauss-Mincu et al., 2026): Realizar varredura paramétrica da relação de curto-circuito (SCR) para mapear a fronteira exata do cycle slipping em redes fracas e estudar interação entre múltiplos inversores.",
        ],
    },
    23: {
        "bloco": "ANEXO DE ARGUIÇÃO E DEFESA TÉCNICA (SLIDES DE APOIO)",
        "titulo": "Defesa Técnica 1: Rede, Filtro LCL e Controle",
        "tcc_ref": "Cap. 3 (Seções 3.4 e 3.5) e Cap. 4 (Seções 4.3.1 e 4.3.2) — Parâmetros completos da simulação",
        "visual": "Três blocos técnicos densos: (1) Rede IEEE 9 Barras e Conversor UFV (Sbase=100 MVA, 20 kV/230 kV, Vcc=40 kV); (2) Filtro LCL e Amortecimento Passivo (L1=30,42 mH, L2=0,289 mH, Lest=30,71 mH, Cf=39,89 uF, Rd=19,6 ohms, omega_res=9.068,99 rad/s); (3) Controle em dq e Sintonia do SRF-PLL (Kp,i=14,74, Ki,i=35.383,87; Kp_PLL=460 vs 92).",
        "pontos_tcc": [
            "Quando usar este slide: Exclusivamente durante a arguição se um membro da banca perguntar pelos parâmetros construtivos do filtro LCL (L1, L2, Cf, Rd), tensão do barramento CC (Vcc = 40 kV) ou ganhos exatos da malha interna de corrente.",
        ],
    },
    24: {
        "bloco": "ANEXO DE ARGUIÇÃO E DEFESA TÉCNICA (SLIDES DE APOIO)",
        "titulo": "Defesa Técnica 2: Tabelas 5.1, 5.2 e 5.3 do TCC",
        "tcc_ref": "Cap. 5 — Tabelas 5.1, 5.2 e 5.3 completas (também na aba 'Análise TCC > 7 Todos os casos' do painel)",
        "visual": "Duas tabelas mestras contendo todos os números das Tabelas 5.1, 5.2 (Faltas Trifásicas e Suporte LVRT ONS) e Tabela 5.3 (Faltas Assimétricas Nominal vs. Inadequada nas Barras 6 e 7), com notas de leitura física.",
        "pontos_tcc": [
            "Quando usar este slide: Consulta rápida de qualquer número das Tabelas 5.1, 5.2 e 5.3 caso a banca peça comparação numérica direta entre Barra 6, Linha 8-9, Linha 7-8 e Barra 7.",
        ],
    },
    25: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABA 1 / SLIDE 25 ESMAECIDO)",
        "titulo": "Energização: Na energização, o PLL inadequado leva cerca do dobro do tempo para travar o ângulo",
        "tcc_ref": "Cap. 5 — Seção 5.1 (Validação da operação em regime permanente — Figuras 5.1 a 5.4, destaque Figura 5.3)",
        "visual": "Figura 5.3 do TCC (erro de fase na energização para sintonia nominal e inadequada) e dois cartões: Sintonia nominal (Vd acomoda em 34 ms; erro de fase em +/-2 graus em 40 ms) vs. Sintonia inadequada (Vd acomoda em 42 ms; erro de fase em +/-2 graus em 79 ms).",
        "pontos_tcc": [
            "Equivalente no painel HTML: Aba 'Análise TCC > 1 Energização'.",
            "Mensagem central da Seção 5.1: Antes de aplicar qualquer falta, precisamos provar que o modelo parte e atinge o regime permanente corretamente nas duas sintonias. A sintonia inadequada demora quase o dobro do tempo para travar na partida (79 ms contra 40 ms), mas ambas chegam ao mesmo regime permanente (Vd = 1,0 pu, erro = 0 grau) antes da falta em 0,3 s.",
        ],
    },
    26: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABA 2 / SLIDE 26 ESMAECIDO)",
        "titulo": "Faltas trifásicas: Quanto mais perto da usina, mais severa a falta trifásica, mas o PLL nominal reconverge",
        "tcc_ref": "Cap. 5 — Seção 5.2 (Faltas simétricas: severidade e localização — Figuras 5.5 a 5.9 e Tabela 5.1, destaque Figura 5.7)",
        "visual": "Figura 5.7 do TCC (erro de fase nas faltas trifásicas para os 4 locais) e Tabela 5.1 ao lado: Barra 7 (Vd 9,2%, pico 37,3 graus, retorno 98 ms), Linha 7-8 (Vd 11,3%, pico 32,5 graus, retorno 98 ms), Linha 8-9 (Vd 47,1%, pico 29,8 graus, retorno 112 ms) e Barra 6 (Vd 58,4%, pico 7,3 graus, retorno 76 ms).",
        "pontos_tcc": [
            "Equivalente no painel HTML: Aba 'Análise TCC > 2 Localização'.",
            "Mensagem central da Seção 5.2: Mantendo a sintonia nominal fixa e variando a distância elétrica da falta trifásica, o afundamento é tanto mais severo quanto mais perto da Barra 2 (9,2% na Barra 7 contra 58,4% na Barra 6). Contudo, como a falta é simétrica (sem sequência negativa, componente de 120 Hz <= 0,0011 pu), o erro de fase ocorre apenas nos transitórios de entrada e saída da falta, e o PLL nominal reconverge em todos os casos (76 a 112 ms).",
        ],
    },
    27: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABAS 3 E 4 / SLIDE 27 ESMAECIDO)",
        "titulo": "Faltas assimétricas e perda de sincronismo: Fragilidade estrutural do SRF-PLL",
        "tcc_ref": "Cap. 5 — Seções 5.3 (Figura 5.10: Espectro FFT de vd) e 5.4 (Figura 5.18: Erro de fase na trifásica da Barra 7)",
        "visual": "Lado a lado: Figura 5.10 do TCC (espectro FFT de vd durante a falta mostrando picos de 0,29 a 0,72 pu em 120 Hz nas assimétricas contra ~0 nas trifásicas) e Figura 5.18 do TCC (erro de fase na trifásica da Barra 7: nominal recupera em 98 ms; inadequada sofre cycle slipping). Cartões: 250x mais 120 Hz e 98 ms.",
        "pontos_tcc": [
            "Equivalente no painel HTML: Abas 'Análise TCC > 4 Sequência negativa' e '3 Perda de sincronismo'.",
            "Mensagem central da Seção 5.3: Nas faltas monofásicas e bifásicas, a sequência negativa gera uma oscilação de 120 Hz em vd e vq de 0,29 a 0,72 pu (mais de 250 vezes maior que o 0,0011 pu das trifásicas). Como 120 Hz (754 rad/s) é apenas 2,32 vezes omega_n, o PI não consegue filtrá-la.",
            "Mensagem central da Seção 5.4 (Figura 5.18): O escorregamento de ciclo (cycle slipping) ocorre quando se combinam falta severa (Barra 7 ou Linha 7-8) e sintonia inadequada: após a eliminação da falta, o erro angular gira continuamente entre -180 e +180 graus e não retorna na janela de 200 ms.",
        ],
    },
    28: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABA 5 / SLIDE 28 ESMAECIDO)",
        "titulo": "Efeito da sintonia nas assimétricas: A aparente atenuação do erro na falta esconde lentidão crítica no restabelecimento",
        "tcc_ref": "Cap. 5 — Seção 5.3 (Figura 5.14 e Tabela 5.3 — Comparação Nominal vs. Inadequada nas faltas assimétricas)",
        "visual": "Figura 5.14 do TCC (erro de fase nas faltas assimétricas, nominal vs. inadequada) e extrato da Tabela 5.3: Bifásica B6 (pico cai de 96,0 para 34,5 graus; retorno 48 -> 30 ms), Monofásica B6 (12,0 -> 12,8 graus; 39 -> 31 ms), Monofásica B7 (pico cai de 89,7 para 70,6 graus, mas retorno dobra de 46 para 95 ms) e Bifásica B7 (pico ~180 graus nas duas; retorno dobra de 51 para 96 ms).",
        "pontos_tcc": [
            "Equivalente no painel HTML: Aba 'Análise TCC > 5 Compromisso da sintonia'.",
            "Mensagem central da Seção 5.3 (Tabela 5.3): Reduzir os ganhos do PLL estreita a banda passante (de 51,8 Hz para 23,2 Hz), o que filtra parcialmente o pico de 120 Hz durante faltas moderadas (como na Barra 6, onde o pico bifásico cai de 96,0 para 34,5 graus). Porém, na Barra 7 (perto da usina), essa lentidão cobra seu preço na recomposição pós-falta: o tempo de retorno à faixa de 2 graus quase dobra (46 -> 95 ms na monofásica e 51 -> 96 ms na bifásica).",
        ],
    },
    29: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABA 3 / SLIDE 29 ESMAECIDO)",
        "titulo": "Dinâmica pós-falta: Sob sintonia inadequada, o inversor absorve potência ativa em 66,8% do tempo",
        "tcc_ref": "Cap. 5 — Seção 5.4 (Figuras 5.20 e 5.21 — Fluxo de potência e correntes dq sob perda de sincronismo na Barra 7)",
        "visual": "Figura 5.20 do TCC (potência ativa pós-falta na Barra 7 com sintonia inadequada, mostrando absorção de potência da rede em 66,8% do tempo, média de -0,40 pu) e Figura 5.21 do TCC (correntes id e iq descoladas das referências devido à rotação contínua do referencial estimado).",
        "pontos_tcc": [
            "Equivalente no painel HTML: Aba 'Análise TCC > 3 Perda de sincronismo'.",
            "Consequência sistêmica mais grave do TCC (Seção 5.4): Por que o inversor passa a absorver potência ativa (atuando como carga em 66,8% do tempo pós-falta, com P médio de -0,40 pu)? Porque a malha interna de corrente continua tentando injetar id_ref = 1,0 pu no eixo d estimado pelo PLL; mas como teta_PLL está girando continuamente em relação à tensão real da rede, quando o erro angular passa de 90 graus, cos(delta_teta) fica negativo e a corrente ativa comandada vira potência ativa absorvida da rede!",
        ],
    },
    30: {
        "bloco": "ROTEIRO TÉCNICO DO CAP. 5 (PAINEL ABA 6 / SLIDE 30 ESMAECIDO)",
        "titulo": "Conformidade normativa: Cumprir o Submódulo 2.10 do ONS exige mais do que permanecer conectado",
        "tcc_ref": "Cap. 5 — Seção 5.5 (Conformidade com o código de rede — Figura 2.2 e Tabela 5.2)",
        "visual": "Figura 2.2 do TCC (rampa LVRT do ONS) e Tabela 5.2: Barra 7 (Vméd 0,10 pu, Iq previsto 1,00, Iq sim 1,00, Qméd 0,09 pu), Linha 7-8 (Vméd 0,11 pu, Iq 1,00/1,00), Linha 8-9 (Vméd 0,48 pu, Iq 1,00/0,99) e Barra 6 (Vméd 0,58 pu, Iq previsto 0,76, Iq sim 0,72).",
        "pontos_tcc": [
            "Equivalente no painel HTML: Aba 'Análise TCC > 6 Código de rede'.",
            "Dois achados fundamentais da Seção 5.5: (1) Com sintonia nominal sob faltas trifásicas, o controle cumpre fielmente a curva do Submódulo 2.10 do ONS (saturando Iq = 1,0 pu quando V <= 0,50 pu e seguindo a rampa em 0,58 pu na Barra 6). (2) Na Barra 7, mesmo injetando 1,00 pu de corrente reativa, a potência reativa entregue à rede é de apenas 0,09 pu, pois Q = V * Iq e a tensão afundou para 0,10 pu.",
            "Fechamento da tese: Sob falta assimétrica ou sintonia inadequada, o inversor permanece conectado (cumprindo formalmente a curva tensão x tempo do LVRT), mas entrega potência contaminada por 120 Hz ou drena potência ativa no pós-falta. Daí a recomendação de auditar a qualidade do sincronismo angular.",
        ],
    },
}


def update_pptx_missing_notes():
    """Preenche as 4 notas 'Fala a escrever' (Slides 5, 6, 7 e 9) no PPTX para não deixar lacunas."""
    prs = Presentation(str(PPTX_STAGED))
    for slide_num, note_text in NEW_NOTES.items():
        slide = prs.slides[slide_num - 1]
        if slide.has_notes_slide:
            slide.notes_slide.notes_text_frame.text = note_text
    prs.save(str(PPTX_STAGED))
    try:
        shutil.copy2(str(PPTX_STAGED), str(PPTX_CANON))
        print(f"[OK] Notas dos slides 5, 6, 7 e 9 atualizadas também em: {PPTX_CANON}")
    except PermissionError:
        print("[AVISO] Defesa_TCC_SRF-PLL.pptx está aberto no PowerPoint; C:\\Temp\\defesa_s2_cards\\final.pptx atualizado.")


def extract_slides_data():
    prs = Presentation(str(PPTX_STAGED))
    slides_data = []
    for idx, s in enumerate(prs.slides, 1):
        notes = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
        if idx in NEW_NOTES:
            notes = NEW_NOTES[idx]
        words = len(notes.split())
        slides_data.append({
            "num": idx,
            "notes": notes,
            "words": words,
            "minutes": words / 130.0,
        })
    return slides_data


def format_mmss(minutes_float: float) -> str:
    total_sec = int(round(minutes_float * 60))
    m = total_sec // 60
    s = total_sec % 60
    return f"{m:02d}:{s:02d}"


def build_word_study_guide():
    update_pptx_missing_notes()
    slides_data = extract_slides_data()

    doc = Document()

    # Configuração de página A4 com margens confortáveis para leitura e impressão
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    # ==========================================================================
    # CAPA / CABEÇALHO DO GUIA DE ESTUDOS
    # ==========================================================================
    p_kicker = doc.add_paragraph()
    p_kicker.paragraph_format.space_before = Pt(0)
    p_kicker.paragraph_format.space_after = Pt(2)
    rk = p_kicker.add_run("UNIVERSIDADE DO ESTADO DO RIO DE JANEIRO (UERJ) • FACULDADE DE ENGENHARIA • ENGENHARIA ELÉTRICA")
    rk.bold = True
    rk.font.name = "Arial"
    rk.font.size = Pt(8.5)
    rk.font.color.rgb = C_BLUE

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    rt = p_title.add_run("GUIA FINAL DE ESTUDOS E ROTEIRO DE FALA DA DEFESA (30 MINUTOS)")
    rt.bold = True
    rt.font.name = "Arial"
    rt.font.size = Pt(18)
    rt.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    rs = p_sub.add_run(
        "Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos\n"
        "Autores: Bruno Henrique de Oliveira e Victor Hugo de Avelar Rezende | "
        "Orientadores: Prof. Dr. Oscar Cuaresma Zevallos e Prof. Dr. André G. Peixoto Alves"
    )
    rs.font.name = "Arial"
    rs.font.size = Pt(10)
    rs.font.color.rgb = C_MUTED

    add_callout_box(
        doc,
        "COMO USAR ESTE DOCUMENTO NO ESTUDO E NO DIA DA APRESENTAÇÃO",
        [
            ("1. Alinhamento 100% Canônico: ", "Este guia segue a ordem exata dos 30 slides do arquivo final Defesa_TCC_SRF-PLL.pptx e cruza cada slide com os Capítulos 1 a 7 do documento final entregue (TCC_Victor_Bruno_VFinal.docx).", C_BLUE),
            ("2. Calibrado para 30 Minutos (130 palavras/min): ", "As falas estão divididas equilibradamente entre [Bruno] e [Victor] (~15 minutos para cada orador). Os Slides 5, 6, 7 e 9, que estavam sem texto nas notas antigas, agora possuem roteiro completo redigido e integrado.", C_TEAL),
            ("3. Estratégia do Painel Interativo (Slide 20 vs. Slides 25 a 30): ", "Na apresentação ao vivo, ao chegar no Slide 20 vocês abrem o painel interativo (output/pll_metrics.html) e percorrem as sub-abas 1 a 6 da aba 'Análise TCC' (que equivalem exatamente aos Slides 25 a 30 esmaecidos no final do deck). O roteiro verbal completo tanto para a demonstração enxuta quanto para a explicação detalhada das 6 abas está incluído neste documento.", C_AMBER),
            ("4. Blindagem para a Arguição da Banca: ", "A Seção 4 no final deste documento reúne as 9 perguntas mais prováveis da banca e as tabelas completas de parâmetros e métricas para consulta imediata na mesa.", C_NAVY),
        ],
        bg_hex="F1F5F9",
        border_hex="0F172A",
        title_color=C_NAVY,
    )

    # ==========================================================================
    # SEÇÃO 1: ARQUITETURA DOS 30 MINUTOS E CRONOGRAMA DE ORADORES
    # ==========================================================================
    add_heading_1(doc, "1. Arquitetura da Apresentação de 30 Minutos e Cronograma Geral")

    add_para(
        doc,
        "A defesa oficial tem duração máxima de 30 minutos. Considerando a cadência natural de defesa técnica "
        "(130 palavras por minuto, já incluindo pausas para apontar gráficos e equações na tela), uma apresentação "
        "de 28 a 30 minutos comporta entre 3.600 e 3.900 palavras faladas. A tabela abaixo mostra a distribuição "
        "exata dos 5 blocos da apresentação:",
    )

    # Cálculo das palavras por bloco
    # Bloco 1: S1..S4
    # Bloco 2: S5..S17
    # Bloco 3: S18..S19
    # Bloco 4: S20 + S25..S30 (roteiro completo das abas do painel / slides de resultado)
    # Bloco 5: S21..S22
    b1_w = sum(slides_data[i - 1]["words"] for i in range(1, 5))
    b2_w = sum(slides_data[i - 1]["words"] for i in range(5, 18))
    b3_w = sum(slides_data[i - 1]["words"] for i in range(18, 20))
    b4_w = slides_data[19]["words"] + sum(slides_data[i - 1]["words"] for i in range(25, 31))
    b5_w = sum(slides_data[i - 1]["words"] for i in range(21, 23))
    total_w = b1_w + b2_w + b3_w + b4_w + b5_w

    add_styled_table(
        doc,
        ["Bloco da Defesa", "Slides no Deck", "Capítulos do TCC", "Palavras", "Tempo do Bloco", "Tempo Acumulado"],
        [
            ["Bloco 1 — Motivação, Apagões e Objetivos", "Slides 1 a 4", "Cap. 1 e Cap. 2 (2.1–2.4)", str(b1_w), format_mmss(b1_w / 130), format_mmss(b1_w / 130)],
            ["Bloco 2 — Fundamentação e Modelagem", "Slides 5 a 17", "Cap. 2 (2.5), Cap. 3 e Cap. 4", str(b2_w), format_mmss(b2_w / 130), format_mmss((b1_w + b2_w) / 130)],
            ["Bloco 3 — Protocolo de Faltas e Pipeline", "Slides 18 e 19", "Cap. 4 (4.3.3 e 4.3.4)", str(b3_w), format_mmss(b3_w / 130), format_mmss((b1_w + b2_w + b3_w) / 130)],
            ["Bloco 4 — Resultados (Painel Ao Vivo / Cap. 5)", "Slide 20 (+ Abas S25–S30)", "Cap. 5 (5.1 a 5.5)", str(b4_w), format_mmss(b4_w / 130), format_mmss((b1_w + b2_w + b3_w + b4_w) / 130)],
            ["Bloco 5 — Conclusões e Trabalhos Futuros", "Slides 21 e 22", "Cap. 5 (5.6), Cap. 6 e Cap. 7", str(b5_w), format_mmss(b5_w / 130), format_mmss(total_w / 130)],
            ["Reserva Técnica — Arguição da Banca", "Slides 23 e 24", "Tabelas 4.1, 5.1–5.3 e LCL", "Consulta", "Sob demanda", "Fechamento em ~29:20"],
        ],
        col_widths_cm=[4.8, 2.8, 3.4, 1.8, 2.1, 2.1],
    )

    add_heading_2(doc, "1.1. Ordem Cronológica de Entrada nas Falas (Percurso de 30 Minutos)")
    add_para(
        doc,
        "Abaixo está a sequência exata de passagem de bastão entre [Bruno] e [Victor] do início ao fim da defesa. "
        "Note que, ao chegar no Slide 20 (aos ~20 minutos de apresentação), vocês abrem o painel interativo "
        "e apresentam os resultados do Capítulo 5 (guiados pelo roteiro das abas 1 a 6 / Slides 25 a 30) antes de "
        "fechar nos Slides 21 e 22:",
    )

    # Ordem real de apresentação (S1..S20 -> Abas 1..6 [S25..S30] -> S21..S22)
    presentation_order = list(range(1, 21)) + list(range(25, 31)) + [21, 22]
    cron_rows = []
    cum_min = 0.0
    for s_num in presentation_order:
        sd = slides_data[s_num - 1]
        meta = SLIDE_STUDY_META[s_num]
        cum_min += sd["minutes"]
        # Identificar oradores na ordem em que aparecem na nota
        speakers = []
        for line in sd["notes"].splitlines():
            line_s = line.strip()
            if line_s.startswith("[Bruno]"):
                speakers.append("Bruno")
            elif line_s.startswith("[Victor]"):
                speakers.append("Victor")
        spk_str = " -> ".join(speakers) if speakers else "Ambos"
        label_slide = f"Slide {s_num:02d}" if s_num <= 22 else f"Painel Aba / S{s_num:02d}"
        short_title = meta["titulo"].split(":")[0]
        cron_rows.append([
            label_slide,
            short_title,
            meta["tcc_ref"].split("—")[0].strip(),
            spk_str,
            str(sd["words"]),
            format_mmss(sd["minutes"]),
            format_mmss(cum_min),
        ])

    add_styled_table(
        doc,
        ["Etapa / Slide", "Tema do Slide", "Ref. TCC", "Ordem de Fala", "Pal.", "Duração", "Relógio"],
        cron_rows,
        col_widths_cm=[2.4, 4.4, 2.8, 3.0, 1.2, 1.6, 1.6],
    )

    # ==========================================================================
    # SEÇÃO 2: MAPA SEQUENCIAL DO TCC × APRESENTAÇÃO (PONTOS IMPORTANTES)
    # ==========================================================================
    add_heading_1(doc, "2. Sequência do TCC (Capítulos 1 a 7) e Pontos Importantes para Estudo")
    add_para(
        doc,
        "Para que o estudo siga ao mesmo tempo a lógica do texto escrito (TCC_Victor_Bruno_VFinal.docx) e a "
        "sequência dos slides, a tabela abaixo resume cada capítulo e seção do TCC, seus conceitos-chave que a "
        "banca avalia e em quais slides eles são apresentados:",
    )

    tcc_map_rows = [
        [
            "Cap. 1 — Introdução",
            "Contextualização da transição energética; motivação pelo apagão de 15/08/2023 no SIN; problema da perda de referência limpa no PCC durante faltas; objetivo geral (inversor de 100 MW no IEEE 9 barras) e 5 objetivos específicos.",
            "Slides 1, 2, 3 e 4",
        ],
        [
            "Cap. 2 — Seção 2.1\nRedes em transição",
            "Dados IEA (2026): demanda global +3% (+800 TWh), solar PV +600 TWh (~70% da expansão global), renováveis variáveis saltam de 5% para 17% no mundo e ~30% na UE. No Brasil (ONS, 2025): 96,8 GW de eólica, solar e MMGD (+279% desde 2020), alcançando 35% da geração e superando a carga média (85,8 GWmed).",
            "Slide 2",
        ],
        [
            "Cap. 2 — Seções 2.2 e 2.3\nClassificação da Estabilidade",
            "Clássica IEEE/CIGRE 2004 (Gu e Green, 2023): ângulo do rotor, frequência e tensão; diferença física entre máquina síncrona (inércia) e inversor GFL/GFM. Estendida IEEE TR77 / CIGRE (Strauss-Mincu et al., 2026; Hatziargyriou et al., 2021): inclusão de 'Estabilidade Dominada por Conversores' (baixa frequência ~10 Hz ligada ao PLL vs. alta frequência ligada ao LCL/chaveamento).",
            "Slides 2, 4, 5 e 23",
        ],
        [
            "Cap. 2 — Seção 2.4\nGrandes Blecautes Recentes",
            "2.4.1 Península Ibérica (28/04/2025): oscilação 0,63 Hz, conversores sem suporte dinâmico de tensão, >2,5 GW perdidos. 2.4.2 Chile (25/02/2025): 11.066 MW perdidos (73% solar+eólica), ilhamento em 1,5 s e colapso de tensão. 2.4.3 Brasil (15/08/2023, RAP-ONS 00012/2023): 23.368 MW (34,5% da carga); ONS descartou falta de inércia (~265 GW.s) e apontou falha no suporte dinâmico de reativos dos inversores.",
            "Slide 3",
        ],
        [
            "Cap. 2 — Seção 2.5\nRequisitos Normativos (ONS)",
            "Curvas LVRT/FRT (Figura 2.1) e injeção obrigatória de corrente reativa do Submódulo 2.10 do ONS (Figura 2.2): banda morta entre 0,85 e 1,10 pu; rampa reativa abaixo de 0,85 pu atingindo 100% de Iq em V <= 0,50 pu; prioridade reativa sobre corrente ativa. Natureza das faltas simétricas e assimétricas (Bollen, 2000 — Figura 2.3).",
            "Slides 14, 15, 16, 24 e 30",
        ],
        [
            "Cap. 3 — Seções 3.1 a 3.3\nPark, Controle P/Q e VSI",
            "Transformadas de Clarke (Eq. 3.1–3.2) e Park (Eq. 3.3–3.5): conversão de senoides abc de 60 Hz em níveis contínuos dq. Controle P/Q desacoplado (Eq. 3.6–3.9): quando vq = 0, P depende só de id e Q depende só de iq. Estrutura do VSI conectado à rede (Figura 3.2) e malha de corrente em cascata (Figura 3.1).",
            "Slides 5, 6, 12 e 13",
        ],
        [
            "Cap. 3 — Seções 3.4 e 3.5\nTeoria e Sintonia do SRF-PLL e PI de Corrente",
            "Estrutura PD + PI + VCO do SRF-PLL (Figura 3.3 / 4.3, Eq. 3.10–3.17). Projeto analítico por forma canônica de 2ª ordem (Eq. 3.18–3.20): xi = 0,707 e ts(1%) = 20 ms -> Kp_PLL = 460, Ki_PLL = 105.820, omega_n = 325,3 rad/s (51,8 Hz). Oscilação de 120 Hz (754 rad/s = 2,32*omega_n). Sintonia canônica da malha de corrente (Seção 3.5, Eq. 3.21–3.23): Kp = 8*fg*Lest e Ki = 32*fg^2*Lest.",
            "Slides 7, 10, 11, 13 e 23",
        ],
        [
            "Cap. 4 — Seções 4.1 a 4.3\nMetodologia, IEEE 9 Barras e Protocolo",
            "Abordagem multi-plataforma (Python analítico, PSIM em nível de circuito e Simulink sistêmico). Substituição de G2 (192 MVA) na Barra 2 pela UFV de 100 MW no IEEE 9 barras (Figura 4.1) e equivalente de Thévenin via Z_barra. Filtro LCL (Lest = 30,71 mH, omega_res = 9.068,99 rad/s — Figura 4.2). Sintonia inadequada (x0,2: Kp=92, Ki=21.164, omega_n=145,5 rad/s, xi=0,316). Matriz de 29 cenários (Tabela 4.1) e falta de 100 ms (6 ciclos).",
            "Slides 8, 9, 10, 11, 14–19 e 23",
        ],
        [
            "Cap. 5 — Seções 5.1 a 5.5\nResultados e Discussão",
            "5.1 Regime permanente/energização (Fig. 5.1–5.4: travamento em 40 ms vs 79 ms). 5.2 Faltas trifásicas (Fig. 5.5–5.9, Tab. 5.1 e 5.2: Vd cai a 9,2% na B7, mas PLL nominal recupera em 98 ms). 5.3 Faltas assimétricas (Fig. 5.10–5.15, Tab. 5.3: 120 Hz chega a 0,72 pu, 250x maior; sintonia lenta reduz pico na B6 mas dobra tempo de retorno na B7 de 46->95 ms e 51->96 ms). 5.4 Perda de sincronismo na B7 trifásica com sintonia inadequada (Fig. 5.16–5.21: cycle slipping e absorção de potência ativa em 66,8% do tempo pós-falta, P_med = -0,40 pu). 5.5 Conformidade com o Submódulo 2.10 ONS (Q = 0,09 pu na B7 devido a V = 0,10 pu).",
            "Slide 20 (Painel Ao Vivo) e Slides 24 a 30",
        ],
        [
            "Cap. 6 e Cap. 7\nConclusões e Trabalhos Futuros",
            "Cap. 6: Síntese qualitativa do mecanismo físico-dinâmico, insuficiência do critério LVRT puramente estático (permanecer conectado sem auditar o erro angular) e transparência sobre limites metodológicos (sobrecorrentes limitadas pelo controle e SCR fixo). Cap. 7: Eixo 1 (DDSRF-PLL e DSOGI-PLL para rejeitar 120 Hz) e Eixo 2 (varredura de SCR e múltiplos inversores).",
            "Slides 21 e 22",
        ],
    ]

    add_styled_table(
        doc,
        ["Capítulo / Seção do TCC", "Pontos Essenciais e Números Canônicos para Dominar", "Slides"],
        tcc_map_rows,
        col_widths_cm=[3.8, 10.6, 2.6],
    )

    # ==========================================================================
    # SEÇÃO 3: ROTEIRO DETALHADO SLIDE A SLIDE (SLIDES 1 A 30)
    # ==========================================================================
    add_heading_1(doc, "3. Guia de Estudo e Roteiro de Fala Slide a Slide (Slides 1 a 30)")
    add_para(
        doc,
        "Abaixo estão todos os 30 slides na ordem exata do arquivo PowerPoint. Para cada slide você tem: "
        "(1) o cabeçalho com tempo e seção do TCC; (2) o que está visível na tela; (3) os pontos teóricos "
        "importantes do TCC para estudo; e (4) a fala exata de [Bruno] e [Victor].",
    )

    cum_clock = 0.0
    for s_num in range(1, 31):
        sd = slides_data[s_num - 1]
        meta = SLIDE_STUDY_META[s_num]
        if s_num <= 22:
            cum_clock += sd["minutes"]
            clock_label = f"Tempo do slide: {format_mmss(sd['minutes'])} ({sd['words']} palavras) | Relógio no fluxo base: {format_mmss(cum_clock)}"
        elif s_num in (23, 24):
            clock_label = f"Slide de Reserva Técnica para Arguição ({sd['words']} palavras de nota auxiliar)"
        else:
            cum_clock += sd["minutes"]
            clock_label = f"Tempo da aba/slide: {format_mmss(sd['minutes'])} ({sd['words']} palavras) | Usado durante a Demo do Painel (Slide 20) ou Backup"

        add_heading_2(doc, f"SLIDE {s_num:02d} — {meta['titulo']}")

        # Metadados rápidos do slide
        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_before = Pt(0)
        p_meta.paragraph_format.space_after = Pt(4)
        rm1 = p_meta.add_run(f"[{meta['bloco']}]  •  ")
        rm1.bold = True
        rm1.font.name = "Arial"
        rm1.font.size = Pt(9)
        rm1.font.color.rgb = C_AMBER

        rm2 = p_meta.add_run(f"Conexão TCC: {meta['tcc_ref']}  •  {clock_label}")
        rm2.bold = True
        rm2.font.name = "Arial"
        rm2.font.size = Pt(9)
        rm2.font.color.rgb = C_MUTED

        # Caixa 1: O que está na tela + Pontos importantes do TCC
        study_lines = [
            ("Na tela do slide: ", meta["visual"], C_NAVY),
        ]
        for pt_idx, pt_text in enumerate(meta["pontos_tcc"], 1):
            study_lines.append((f"Ponto-chave do TCC ({pt_idx}): ", pt_text, C_BLUE))

        add_callout_box(
            doc,
            f"O QUE SABER E APONTAR NO SLIDE {s_num:02d} (CONEXÃO COM O TCC)",
            study_lines,
            bg_hex="F8FAFC",
            border_hex="475569",
            title_color=C_NAVY,
        )

        # Caixa 2: Roteiro de Fala ([Bruno] e [Victor])
        speech_lines = []
        paragraphs = [p.strip() for p in sd["notes"].split("\n\n") if p.strip()]
        for para in paragraphs:
            if para.startswith("[Bruno]"):
                body = para[len("[Bruno]"):].strip()
                w_cnt = len(body.split())
                speech_lines.append((f"[Bruno] ({w_cnt} pal. ~ {format_mmss(w_cnt/130)}): ", body, C_BLUE))
            elif para.startswith("[Victor]"):
                body = para[len("[Victor]"):].strip()
                w_cnt = len(body.split())
                speech_lines.append((f"[Victor] ({w_cnt} pal. ~ {format_mmss(w_cnt/130)}): ", body, C_TEAL))
            else:
                speech_lines.append(("", para, C_TEXT))

        add_callout_box(
            doc,
            f"ROTEIRO DE FALA DO SLIDE {s_num:02d}",
            speech_lines,
            bg_hex="EFF6FF" if s_num <= 22 else "F0FDFA",
            border_hex="1E3A8A" if s_num <= 22 else "0F766E",
            title_color=C_BLUE if s_num <= 22 else C_TEAL,
        )

    # ==========================================================================
    # SEÇÃO 4: GUIA DE BOLSO PARA A ARGUIÇÃO DA BANCA (Q&A + TABELAS MESTRAS)
    # ==========================================================================
    add_heading_1(doc, "4. Guia Blindado para a Arguição da Banca (Perguntas Prováveis e Respostas)")
    add_para(
        doc,
        "Esta seção consolida os 9 pontos em que um examinador atento pode cruzar detalhes do texto do TCC "
        "entregue com os slides da apresentação. Não antecipe esses pontos espontaneamente durante os 30 minutos; "
        "use estas respostas prontas e diretas caso a banca pergunte:",
    )

    qa_items = [
        (
            "Pergunta 1: Quantos cenários foram simulados no total? Por que o Slide 20 cita 28 cenários de falta e a Tabela 4.1 tem 27 marcas?",
            "Foram simulados 29 cenários no total: 28 cenários com falta na rede e 1 cenário de regime permanente (sem falta, testado com as duas sintonias na Seção 5.1). "
            "Entre os 29 cenários, são 21 com a sintonia nominal (as 8 localidades com falta trifásica, as 6 barras com falta monofásica, as 6 barras com falta bifásica e 1 em regime permanente) "
            "e 8 com a sintonia inadequada (as 3 faltas na Barra 6, as 3 faltas na Barra 7, a falta trifásica na Linha 7-8 e 1 em regime permanente). "
            "Na Tabela 4.1 do TCC, faltaram apenas as marcas visuais da Linha 7-8 inadequada e da linha de regime permanente, mas ambos os casos estão descritos e analisados no texto do Capítulo 5 (Seções 5.1 e 5.4)."
        ),
        (
            "Pergunta 2: Por que os objetivos específicos da Introdução falam em 'sobrecorrentes transitórias' e em 'influência da impedância da rede', se isso não aparece como varredura no Cap. 5?",
            "Nós tratamos essas duas ressalvas explicitamente na conclusão do trabalho (Capítulo 6, parágrafo de limites de validade). "
            "Primeiro: as sobrecorrentes severas no conversor não se materializam porque a malha interna de corrente e a lógica do Submódulo 2.10 limitam a referência total de corrente a 1,0 pu antes que a sobrecorrente ocorra. "
            "Segundo: a influência da impedância equivalente da rede foi avaliada de forma indireta variando a distância elétrica da falta (da Barra 7, colada à usina, até a Barra 6, distante), mantendo o nível de curto-circuito do sistema fixo. A varredura paramétrica de SCR fica proposta no Capítulo 7."
        ),
        (
            "Pergunta 3: Quais são os valores individuais de Vcc, L1, L2, Cf e Rd do filtro LCL que não estão tabelados no corpo do Cap. 4?",
            "No texto do Capítulo 4 optamos por apresentar a indutância total equivalente Lest = 30,71 mH e a frequência de ressonância omega_res = 9.068,99 rad/s (1.443,4 Hz), que são os parâmetros que entram diretamente nas equações de sintonia. "
            "No modelo Simulink (e no Slide 23 de Defesa Técnica), os valores individuais são: tensão do barramento CC Vcc = 40 kV; indutor do lado do inversor L1 = 30,42 mH; indutor do lado da rede L2 = 0,289 mH; banco de capacitores em delta Cf = 39,89 microfarads (equivalente em estrela C_Y = 119,68 microfarads); e resistores de amortecimento passivo Rd = 19,6 ohms em série nos ramos capacitivos."
        ),
        (
            "Pergunta 4: A malha interna de corrente (omega_n = 339,4 rad/s) e o SRF-PLL nominal (omega_n = 325,3 rad/s) têm praticamente a mesma largura de banda. Isso não viola a separação clássica de escalas de tempo em cascata?",
            "Sim, as duas frequências naturais são próximas (54,0 Hz na malha de corrente e 51,8 Hz no PLL nominal), pois cada uma foi projetada pela respectiva referência clássica (Alves, 2022 para acomodação da corrente em 1 ciclo da rede; Alves, Dias e Rolim, 2020 e Teodorescu et al., 2011 para acomodação do PLL em 20 ms). "
            "No nosso trabalho, os ganhos da malha de corrente foram mantidos estritamente fixos em todos os cenários para isolar o efeito da variação dos ganhos do PLL. O acoplamento dinâmico em pequenos sinais entre as duas malhas de mesma banda é uma frente analítica complementar para trabalhos futuros."
        ),
        (
            "Pergunta 5: Na demonstração do painel interativo, o cartão no topo mostra 8,3% de tensão retida na Barra 7, mas o Slide 20 e a Tabela 5.1 dizem 9,2%. Qual é a diferença?",
            "São duas grandezas elétricas diferentes medidas em pontos ligeiramente distintos. "
            "O valor oficial do TCC (Tabela 5.1 e slides) é 9,2%, que corresponde à componente de eixo direto Vd no referencial do inversor em percentual do valor pré-falta. "
            "Já o cartão superior do simulador interativo exibe o módulo da tensão trifásica |V_abc| diretamente no barramento de 20 kV da Barra 2 (8,3%). Na sub-aba 'Análise TCC' do próprio painel, todas as tabelas usam os exatos 9,2% da Tabela 5.1."
        ),
        (
            "Pergunta 6: Na Introdução do TCC o apagão de 15/08/2023 aparece com 22.547 MW (31%), e na Seção 2.4.3 e no Slide 3 aparece com 23.368 MW (34,5%). Qual é o certo?",
            "O número consolidado oficial é 23.368 MW (34,5% da demanda nacional do instante), extraído diretamente do Relatório de Análise de Perturbação oficial do ONS (RAP-ONS 00012/2023), que é a fonte primária detalhada na Seção 2.4.3. O valor de 22.547 MW na introdução reflete boletins preliminares emitidos logo após o evento."
        ),
        (
            "Pergunta 7: Onde exatamente ocorre o escorregamento de ciclo (cycle slipping)? Ocorre nas faltas assimétricas ou nas trifásicas?",
            "A perda irreversível de sincronismo por escorregamento de ciclo (cycle slipping) ocorre com a sintonia inadequada nas faltas TRIFÁSICAS severas: na Barra 7 e na Linha 7-8 (Seção 5.4, Figura 5.18). Nesses casos, após a eliminação da falta em 0,4 s, o erro de fase gira continuamente de -180 a +180 graus e não retorna à faixa de 2 graus até o fim da janela. "
            "Nas faltas ASSIMÉTRICAS (Seção 5.3), a fragilidade é outra: é a oscilação estacionária de 120 Hz que o filtro PI não rejeita. Na bifásica da Barra 7 o erro chega a tocar 180 graus durante a falta nas duas sintonias, mas ambas reconvergem após a abertura do defeito (em 51 ms na nominal e 96 ms na inadequada)."
        ),
        (
            "Pergunta 8: Na Tabela 5.2 (Slide 30), durante a falta trifásica na Barra 7 o inversor injeta 1,00 pu de corrente reativa, mas a potência reativa entregue é de apenas 0,09 pu. Por quê?",
            "Porque a potência reativa entregue à rede é o produto da tensão terminal pela corrente reativa (Q = V * Iq). Como na falta franca na Barra 7 a tensão média no ponto de conexão cai para 0,10 pu (menos de 10% da tensão nominal), mesmo com o inversor saturando sua capacidade máxima de corrente reativa em 1,00 pu conforme exige o Submódulo 2.10 do ONS, a potência reativa resultante fica limitada fisicamente a cerca de 0,09 pu."
        ),
        (
            "Pergunta 9: Vocês consideraram usar inversores formadores de rede (grid-forming / GFM) para resolver o problema?",
            "Os conversores formadores de rede (GFM) são discutidos conceitualmente na revisão do Capítulo 2 (Seções 2.2 e 2.4), mas estão fora do escopo de simulação deste TCC. Nosso trabalho foca na imensa frota de usinas eólicas e fotovoltaicas já instaladas no SIN, que operam como seguidoras de rede (grid-following) sincronizadas por PLL. Por isso, o Capítulo 7 propõe evoluir primeiro a estrutura do algoritmo de sincronismo (para DDSRF-PLL e DSOGI-PLL) mantendo a arquitetura seguidora de rede."
        ),
    ]

    for q_title, q_ans in qa_items:
        add_callout_box(
            doc,
            q_title,
            [("Resposta fundamentada no TCC: ", q_ans, C_TEAL)],
            bg_hex="F8FAFC",
            border_hex="0F766E",
            title_color=C_NAVY,
        )

    add_heading_2(doc, "4.1. Tabelas Mestras do Capítulo 5 para Consulta Rápida (Tabelas 5.1, 5.2 e 5.3)")
    add_para(doc, "Tabela 5.1 e Tabela 5.2 combinadas — Faltas Trifásicas (Sintonia Nominal) e Suporte Reativo Submódulo 2.10 ONS:")

    add_styled_table(
        doc,
        ["Local da Falta", "Retenção Vd (%)", "Pico |Δθ| (°)", "Retorno ±2° (ms)", "120 Hz em Vd (pu)", "Vméd PCC (pu)", "Iq Rampa ONS (pu)", "Iq Simulado (pu)", "Pméd / Qméd (pu)"],
        [
            ["Barra 7 (próxima)", "9,2%", "37,3°", "98 ms", "0,0002", "0,10", "1,00", "1,00", "-0,01 / 0,09"],
            ["Linha 7-8", "11,3%", "32,5°", "98 ms", "0,0004", "0,11", "1,00", "1,00", "-0,01 / 0,10"],
            ["Linha 8-9", "47,1%", "29,8°", "112 ms", "0,0003", "0,48", "1,00", "0,99", "0,02 / 0,43"],
            ["Barra 6 (distante)", "58,4%", "7,3°", "76 ms", "0,0011", "0,58", "0,76", "0,72", "0,39 / 0,40"],
        ],
        col_widths_cm=[2.6, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8],
    )

    add_para(doc, "Tabela 5.3 — Faltas Assimétricas nas Barras 6 e 7 (Comparação Sintonia Nominal vs. Sintonia Inadequada):")

    add_styled_table(
        doc,
        ["Cenário de Falta Assimétrica", "Sintonia do PLL", "Vd médio na falta (pu)", "Componente 120 Hz (pu)", "Pico |Δθ| na falta (°)", "Tempo de Retorno a ±2° (ms)"],
        [
            ["Bifásica — Barra 7", "Nominal (Kp=460)", "0,57", "0,72", "180,0°", "51 ms"],
            ["Bifásica — Barra 7", "Inadequada (Kp=92)", "0,56", "0,64", "179,9°", "96 ms (quase dobra)"],
            ["Monofásica — Barra 7", "Nominal (Kp=460)", "0,64", "0,59", "89,7°", "46 ms"],
            ["Monofásica — Barra 7", "Inadequada (Kp=92)", "0,64", "0,51", "70,6°", "95 ms (mais que dobra)"],
            ["Bifásica — Barra 6", "Nominal (Kp=460)", "0,72", "0,44", "96,0°", "48 ms"],
            ["Bifásica — Barra 6", "Inadequada (Kp=92)", "0,76", "0,35", "34,5° (filtra pico)", "30 ms"],
            ["Monofásica — Barra 6", "Nominal (Kp=460)", "0,82", "0,29", "12,0°", "39 ms"],
            ["Monofásica — Barra 6", "Inadequada (Kp=92)", "0,82", "0,26", "12,8°", "31 ms"],
        ],
        col_widths_cm=[3.6, 3.0, 2.5, 2.5, 2.7, 2.7],
    )

    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_LOCAL))
    print(f"[OK] Guia de estudos salvo em: {OUT_LOCAL}")

    try:
        shutil.copy2(str(OUT_LOCAL), str(OUT_ONEDRIVE))
        print(f"[OK] Cópia salva na pasta OneDrive do TCC: {OUT_ONEDRIVE}")
    except Exception as e:
        print(f"[AVISO] Não foi possível copiar para OneDrive ({e}).")


if __name__ == "__main__":
    build_word_study_guide()
