# -*- coding: utf-8 -*-
"""
Gera um documento Word (.docx) enxuto e focado EXCLUSIVAMENTE em:
  1. Cronograma e Controle de Tempo (Meta de 30m00s, com contagem de palavras,
     tempo de fala + cliques e relógio acumulado item a item).
  2. Pontos principais a serem comentados em cada slide (1-21) e em cada capítulo
     do Modo Apresentação do painel HTML (Capítulos 1-8, sincronizados com a
     versão final de output/pll_metrics.html, incluindo os 5 passos do Cap. 4 e
     os 5 passos do Cap. 7).
  3. Falas completas cronometradas ([Bruno] e [Victor]) com rubricas de clique
     (Seta ->) e ganchos de transição.
  4. Resumo rápido dos slides de Apêndice (22-23) e Reserva Oculta (24-29).

Saídas:
  - output/Roteiro_Falas_e_Tempo_Defesa_TCC.docx
  - OneDrive: .../Template Modelo TCC/Roteiro_Falas_e_Tempo_Defesa_TCC.docx
"""
import re
import shutil
from pathlib import Path

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT_LOCAL = ROOT / "output" / "Roteiro_Falas_e_Tempo_Defesa_TCC.docx"
ONEDRIVE_DIR = Path(r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC")
OUT_ONEDRIVE = ONEDRIVE_DIR / "Roteiro_Falas_e_Tempo_Defesa_TCC.docx"

# Paleta de cores
C_NAVY = RGBColor(0x1B, 0x36, 0x5D)
C_BLUE = RGBColor(0x25, 0x63, 0xEB)
C_BRUNO = RGBColor(0x1E, 0x3A, 0x8A)
C_VICTOR = RGBColor(0x06, 0x5F, 0x46)
C_ORANGE = RGBColor(0xC2, 0x41, 0x0C)
C_INK = RGBColor(0x1E, 0x29, 0x3B)
C_MUTED = RGBColor(0x64, 0x74, 0x8B)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEX_NAVY = "1B365D"
HEX_PANEL = "0F766E"
HEX_SUB = "F1F5F9"
HEX_MSG_BG = "E8EFF7"
HEX_MSG_BD = "1B365D"
HEX_PTS_BG = "FFFBEB"
HEX_PTS_BD = "B45309"
HEX_FALA_BG = "F8FAFC"
HEX_FALA_BD = "2563EB"
HEX_PALCO_BG = "F0FDF4"
HEX_PALCO_BD = "15803D"
HEX_BORDER = "CBD5E1"
HEX_ZEBRA = "F8FAFC"


def set_cell_bg(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side, cfg in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        if cfg is None:
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:val"), "none")
            tcBorders.append(node)
        else:
            val, sz, color = cfg
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:val"), val)
            node.set(qn("w:sz"), str(sz))
            node.set(qn("w:space"), "0")
            node.set(qn("w:color"), color.lstrip("#"))
            tcBorders.append(node)
    tcPr.append(tcBorders)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def repeat_header_row(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def count_words(text: str) -> int:
    clean = re.sub(r"\[(Bruno|Victor)\]", " ", text)
    clean = re.sub(r"\([^)]*\)", " ", clean)
    return len(re.findall(r"\S+", clean))


def fmt_mmss(seconds: int) -> str:
    m, s = divmod(int(round(seconds)), 60)
    return f"{m:02d}:{s:02d}"


def fmt_dur(seconds: int) -> str:
    m, s = divmod(int(round(seconds)), 60)
    if m > 0 and s > 0:
        return f"{m}m {s:02d}s"
    if m > 0:
        return f"{m}m 00s"
    return f"{s}s"


# ==============================================================================
# DADOS ESTRUTURADOS DE TODOS OS SLIDES (1-21) E CAPÍTULOS DO HTML (1-8)
# ==============================================================================

SLIDES_ROTEIRO = [
    # -------------------------------------------------------------------------
    # PARTE I: SLIDES 1 A 18
    # -------------------------------------------------------------------------
    {
        "tipo": "SLIDE",
        "num": 1,
        "titulo": "Capa — Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos",
        "bloco": "Abertura",
        "tcc": "Capa",
        "quem": "Bruno",
        "dur_s": 40,
        "msg": "Quem somos, o título do trabalho (foco no SRF-PLL sob contingências) e os cinco blocos do percurso.",
        "pontos": [
            ("Bruno", "Cumprimentar a banca, apresentar a si e ao parceiro Victor Hugo, e anunciar o título do TCC delimitando o foco no SRF-PLL sob contingências."),
            ("Bruno", "Apresentar o percurso em 5 blocos: contexto global, fundamentação e modelagem, metodologia de simulação, resultados no painel interativo e conclusões."),
            ("Bruno", "Agradecer aos orientadores Prof. Dr. Oscar Cuaresma Zevallos e Prof. Dr. André Guilherme Peixoto Alves, e aos membros da banca, abrindo com o contexto que motivou o estudo."),
        ],
        "falas": [
            ("Bruno", "Bom dia a todos. Eu sou o Bruno Henrique de Oliveira e, junto com o Victor Hugo de Avelar Rezende, apresento o nosso Trabalho de Conclusão de Curso: Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos.\n\nVamos percorrer cinco blocos hoje: o contexto global, a fundamentação e a modelagem, a metodologia de simulação, os resultados no painel interativo e as conclusões. Agradecemos desde já ao nosso orientador, professor Oscar, ao coorientador, professor André, e aos membros da banca. Vamos começar pelo contexto que motivou este estudo."),
        ],
        "atencao": "Ponte direta para o Slide 2: 'Vamos começar pelo contexto que motivou este estudo.'",
    },
    {
        "tipo": "SLIDE",
        "num": 2,
        "titulo": "Expansão das renováveis",
        "bloco": "Motivação",
        "tcc": "Cap. 2 (IEA 2026, ONS 2025)",
        "quem": "Bruno",
        "dur_s": 60,
        "msg": "Solar e eólica saltaram de 5% para 17% da geração mundial em uma década; no Brasil a capacidade já passa da carga média.",
        "pontos": [
            ("Bruno", "Cartão superior direito (IEA, 2026): velocidade da transição energética — geração solar mundial cresceu cerca de 600 TWh em 2025 (~70% do avanço global) e o mundo adicionou 800 GW renováveis."),
            ("Bruno", "Gráfico de barras e cartão ONS: fatia mundial de solar + eólica triplicou de 5% para 17% em uma década (~30% na UE e 35% no Brasil com MMGD). No SIN, 96,8 GW instalados já superam a carga média nacional de 85,8 GWmed."),
            ("Bruno", "Pergunta do rodapé: A geração nova chega por inversores e a geração síncrona, que impõe tensão e frequência pela inércia mecânica, perde espaço na matriz."),
        ],
        "falas": [
            ("Bruno", "A motivação do nosso trabalho parte da velocidade da transição energética. Segundo a Agência Internacional de Energia, em 2025, a geração solar mundial cresceu cerca de 600 terawatts-hora. Isso responde sozinha por 70% de todo o avanço da geração elétrica global, num ano em que o mundo adicionou 800 gigawatts renováveis.\n\nNo gráfico à esquerda, vemos que em uma década a fatia mundial de solar e eólica triplicou, de 5% para 17%, chegando a cerca de 30% na União Europeia e 35% no Brasil, se considerarmos a micro e minigeração distribuída. Os dados do ONS mostram que a capacidade eólica e solar no SIN atingiu 96,8 gigawatts em 2025, superando a própria carga média nacional de 85,8 gigawatts médios. E qual a consequência disso para a rede? Como diz o rodapé, a geração nova chega por inversores, e a geração síncrona, que impõe tensão e frequência pela inércia, perde espaço na matriz."),
        ],
        "atencao": "Cuidado: 96,8 GW é capacidade instalada e 85,8 GWmed é carga média (mostra escala, não atendimento exclusivo). MMGD = micro e minigeração distribuída.",
    },
    {
        "tipo": "SLIDE",
        "num": 3,
        "titulo": "Eventos no mundo real",
        "bloco": "Motivação",
        "tcc": "Cap. 2, §2.4 (RAP-ONS, ENTSO-E, CEN)",
        "quem": "Bruno",
        "dur_s": 85,
        "msg": "Os grandes blecautes recentes passaram pela geração conectada por inversores.",
        "pontos": [
            ("Bruno", "Cartão 1 — SIN, Brasil (15/08/2023): abertura acidental da LT 500 kV Quixadá–Fortaleza II levou a afundamento de tensão no Nordeste, desligamentos em cascata e perda de 23.368 MW (34,5% da carga nacional)."),
            ("Bruno", "Diagnóstico do RAP-ONS (2023): descartou falta de inércia (~265 GW·s) e falta de curto; colapso de tensão com suporte dinâmico de reativos de eólicas e solares muito aquém do previsto nos modelos."),
            ("Bruno", "Cartões 2 e 3 (Península Ibérica e Chile, 2025): oscilação de 0,63 Hz guiada por conversores (> 2,5 GW desconectados por sobretensão) e abertura de 500 kV no Chile (11.066 MW perdidos com 73% de renováveis)."),
            ("Bruno", "Rodapé sintetizador: nos três eventos, o elo crítico sistêmico foi o controle e o sincronismo dos inversores durante o distúrbio."),
        ],
        "falas": [
            ("Bruno", "Quando essa geração baseada em inversores enfrenta perturbações reais, falhas de controle ganham escala sistêmica. No blecaute brasileiro de 15 de agosto de 2023, a abertura acidental da linha de 500 quilovolts entre Quixadá e Fortaleza II provocou um afundamento de tensão no Nordeste, desligamentos em cascata e a perda de 23.368 megawatts, ou 34,5% da carga nacional.\n\nO diagnóstico do relatório do ONS é o grande motivador do nosso estudo: o operador descartou falta de inércia, já que o SIN tinha cerca de 265 gigawatts-segundo, e descartou falta de potência de curto-circuito. Concluiu-se que o colapso foi de tensão, porque o suporte dinâmico de reativos das usinas eólicas e solares ficou muito aquém do previsto nos modelos.\n\nTivemos padrões semelhantes em 2025. Na Península Ibérica, uma oscilação guiada por conversores levou à perda de mais de 2,5 gigawatts por sobretensão. No Chile, uma abertura em 500 quilovolts num sistema com 73% de renováveis isolou o norte do país, provocando colapso de tensão e a perda de mais de 11 mil megawatts. Como resume o rodapé, nos três eventos o elo crítico sistêmico foi o controle e o sincronismo dos inversores durante o distúrbio."),
        ],
        "atencao": "Citar 23.368 MW (34,5%, §2.4.3 do TCC e RAP-ONS). Se perguntarem sobre o Chile ou Ibéria: o elo comum é a resposta de tensão e sincronismo no transitório.",
    },
    {
        "tipo": "SLIDE",
        "num": 4,
        "titulo": "Problema e objetivos",
        "bloco": "Motivação",
        "tcc": "Cap. 1",
        "quem": "Bruno",
        "dur_s": 75,
        "msg": "O SRF-PLL depende de uma tensão limpa, justamente o que a falta na rede destrói.",
        "pontos": [
            ("Bruno", "Cadeia causal (bloco 1): o inversor precisa do ângulo da tensão no PCC estimado pelo SRF-PLL, mas a falta na rede degrada exatamente essa tensão com afundamento e assimetria."),
            ("Bruno", "Cadeia causal (blocos 2 e 3): o afundamento reduz a componente de eixo direto vd (enfraquecendo o laço); o desequilíbrio introduz oscilação de 120 Hz no eixo em quadratura vq (sinal de erro do PLL), gerando desvio angular ou perda de sincronismo."),
            ("Bruno", "Cadeia causal (bloco 4): erro angular contamina as malhas de corrente, perde o desacoplamento P-Q, compromete o suporte exigido pelo Submódulo 2.10 do ONS e pode levar à inversão de fluxo ativo."),
            ("Bruno", "Caixas inferiores: Objetivo Geral (analisar dinâmica, sensibilidade à sintonia e robustez do SRF-PLL de 100 MW no IEEE 9 barras) e Específicos (modelar no Simulink, comparar sintonias sob faltas simétricas/assimétricas, verificar ONS)."),
            ("Bruno", "Transição: Passar a palavra ao Victor para iniciar o bloco de modelagem no Slide 5."),
        ],
        "falas": [
            ("Bruno", "Isso nos traz ao problema central do trabalho, ilustrado nesta cadeia causal. No primeiro bloco, o inversor precisa do ângulo da tensão no ponto de conexão estimado pelo SRF-PLL, mas a falta na rede degrada exatamente essa tensão com afundamento e assimetria.\n\nNos blocos seguintes, o afundamento reduz a componente de eixo direto, enfraquecendo o laço, e o desequilíbrio introduz uma oscilação de 120 hertz no eixo em quadratura, que é o sinal de erro do PLL. O resultado é desvio angular ou perda de sincronismo. Sem o ângulo correto, o desacoplamento entre potência ativa e reativa se perde, comprometendo o suporte de reativos exigido pelo Submódulo 2.10 do ONS e podendo levar até à inversão do fluxo ativo.\n\nDaí o nosso objetivo geral: analisar a dinâmica, a sensibilidade à sintonia e a robustez do SRF-PLL de um inversor de 100 megawatts frente a contingências no sistema IEEE 9 barras. E nos objetivos específicos: modelar o sistema no Simulink, comparar sintonias sob faltas simétricas e assimétricas, e verificar a conformidade com o ONS.\n\nPasso agora a palavra ao Victor, que vai iniciar o bloco de modelagem."),
        ],
        "atencao": "Não mencionar sobrecorrentes (o TCC conclui que são contidas pela malha rápida de corrente). Fazer ponte para a Modelagem no Slide 5.",
    },
    {
        "tipo": "SLIDE",
        "num": 5,
        "titulo": "Fonte renovável",
        "bloco": "Modelagem",
        "tcc": "Fig. 3.2, §3.2, §4.1, §4.3.1",
        "quem": "Victor",
        "dur_s": 45,
        "msg": "A usina fotovoltaica ou eólica se conecta à rede por um inversor seguidor de rede.",
        "pontos": [
            ("Victor", "Início da modelagem e fonte primária renovável: escolha de barramento CC ideal, ignorando a dinâmica do elo CC e o rastreamento de máxima potência (MPPTs)."),
            ("Victor", "Inversor e filtro LCL: inversor faz a conversão trifásica e recebe os comandos do controle; filtro de acoplamento LCL conecta a usina ao ponto de acoplamento comum no sistema IEEE 9 barras."),
            ("Victor", "Controle digital do SRF-PLL: sinal medido no PCC vai para o controle digital para fazer a realimentação e o rastreamento do ângulo da rede."),
        ],
        "falas": [
            ("Victor", "Iniciando a parte de modelagem no slide 5, nós nos deparamos com o modelo do nosso sistema. Começando pela fonte primária, que vai ser uma fonte renovável: nós escolhemos utilizar um barramento CC ideal, ignorando a dinâmica do elo CC e o rastreamento de máxima potência, os MPPTs.\n\nSeguindo para a direita, temos o inversor, que faz a conversão trifásica e é quem vai receber os comandos do controle. Logo após, temos o filtro de acoplamento LCL, conectando a usina ao ponto de acoplamento comum na rede elétrica, o sistema IEEE de 9 barras. O sinal medido ali vai para o controle digital do SRF-PLL para fazer a realimentação e o rastreamento do ângulo da rede."),
        ],
        "atencao": "Gancho direto para a transformada de Park: 'Para poder fazer o rastreamento dessa rede, é utilizada a transformada de Park.'",
    },
    {
        "tipo": "SLIDE",
        "num": 6,
        "titulo": "Transformada de Park",
        "bloco": "Modelagem",
        "tcc": "Eqs. (3.4)-(3.7), §3.1.2, §3.4",
        "quem": "Victor",
        "dur_s": 60,
        "msg": "Girando com a rede, a transformada de Park torna constantes as grandezas trifásicas.",
        "pontos": [
            ("Victor", "Conceito básico da transformada de Park: transformar as tensões trifásicas em duas grandezas lineares e constantes, dividindo em vd e vq."),
            ("Victor", "Matriz de transformação e equações resultantes: objetivo do PLL é referenciar exatamente o ângulo da rede, obtendo cosseno de zero para vd e seno de zero para vq."),
            ("Victor", "O grande porquê de Park: sinais senoidais no controlador PI propagam erro sem zerar em regime; convertendo para sinais constantes, a ação integral zera o sinal facilmente na detecção de fase."),
        ],
        "falas": [
            ("Victor", "Para poder fazer o rastreamento dessa rede, é utilizada a transformada de Park. O conceito básico dela é transformar as tensões trifásicas em duas grandezas lineares e constantes, dividindo em vd e vq.\n\nComo vocês podem ver, aqui segue a matriz de transformação e, logo abaixo, observamos as equações resultantes dessa multiplicação. O objetivo do PLL é fazer com que o seu ângulo esteja exatamente em referência ao ângulo da rede. Assim, para vd teremos o cosseno de zero, e para vq o seno de zero.\n\nE por que a gente utiliza essa transformada de Park? Porque quando aplicamos sinais senoidais num controlador PI, o erro se propaga e a gente nunca consegue trazer esse erro a zero. Porém, quando convertemos para sinais constantes, a ação integral consegue zerar esse sinal facilmente. Então, esse é o grande porquê de utilizar a transformada de Park na nossa detecção de fase."),
        ],
        "atencao": "Destaque conceitual: a ação integral sobre grandezas contínuas zera o erro perfeitamente.",
    },
    {
        "tipo": "SLIDE",
        "num": 7,
        "titulo": "Estrutura do SRF-PLL",
        "bloco": "Modelagem",
        "tcc": "Fig. 4.3, §3.4, Eqs. (3.10)-(3.19)",
        "quem": "Victor",
        "dur_s": 60,
        "msg": "O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede.",
        "pontos": [
            ("Victor", "Modelagem da malha fechada e detector de fase: transformada de Park envia vq para o PI convergir para zero (zerando o erro) e consequentemente vd convergir para a amplitude total da tensão."),
            ("Victor", "Set point de frequência e VCO: integra o sinal de velocidade angular para obter o ângulo do PLL, que faz a realimentação para a transformada de Park fechando o laço."),
            ("Victor", "Dimensionamento dos ganhos: equações características de segunda ordem no cartão direito dimensionam os ganhos Kp e Ki do PLL."),
        ],
        "falas": [
            ("Victor", "Passando para o slide 7, a gente consegue verificar a modelagem da nossa malha de controle fechada. Como já explicamos, a transformada de Park vai ser o nosso detector de fase. O objetivo dela é enviar a componente vq para o controlador PI, e nós queremos utilizar o PI para fazer esse vq convergir para zero, zerando o erro. Consequentemente, o vd vai convergir para a amplitude total da tensão.\n\nTendo em vista que referenciamos um set point com a frequência natural da rede, no VCO nós integramos esse sinal de velocidade angular e obtemos o ângulo do PLL. Esse ângulo faz a realimentação de volta para a transformada de Park, fechando o laço. Como a gente pode ver do lado direito, utilizamos as fórmulas da equação característica de segunda ordem para poder dimensionar os ganhos Kp e Ki do nosso PLL."),
        ],
        "atencao": "Estrutura clássica de 2ª ordem: Park (detector) -> PI -> VCO (integrador) -> realimentação em ângulo.",
    },
    {
        "tipo": "SLIDE",
        "num": 8,
        "titulo": "Sistema IEEE 9 barras",
        "bloco": "Modelagem",
        "tcc": "Fig. 4.1, §4.3.1",
        "quem": "Victor",
        "dur_s": 40,
        "msg": "A UFV assume a Barra 2 e enxerga o resto da rede como um equivalente de Thévenin.",
        "pontos": [
            ("Victor", "Sistema IEEE 9 barras modificado: máquina síncrona original da Barra 2 substituída pela usina fotovoltaica de 100 MW; G1 e G3 permanecem como fontes síncronas mantendo a inércia da rede."),
            ("Victor", "Topologia da rede: permite variar a distância elétrica das faltas mantendo o nível de curto-circuito constante."),
            ("Victor", "Equivalente de Thévenin: redução de toda a rede a um equivalente visto da Barra 2 para os estudos iniciais de controle."),
        ],
        "falas": [
            ("Victor", "Podendo passar para o próximo slide, aqui a gente encontra o sistema IEEE de 9 barras modificado. A máquina síncrona original da Barra 2 foi substituída pela nossa usina fotovoltaica de 100 megawatts, enquanto os geradores G1 e G3 permanecem como fontes síncronas mantendo a inércia da rede.\n\nEssa topologia nos permite variar a distância elétrica das faltas mantendo o nível de curto-circuito constante. E para os nossos estudos iniciais de controle, reduzimos toda a rede a um equivalente de Thévenin visto da Barra 2."),
        ],
        "atencao": "Transição suave para o Slide 9 (bancada do PLL com equivalente de Thévenin).",
    },
    {
        "tipo": "SLIDE",
        "num": 9,
        "titulo": "Bancada do PLL",
        "bloco": "Modelagem",
        "tcc": "Exceção de método (PSIM)",
        "quem": "Bruno → Victor",
        "dur_s": 35,
        "msg": "Antes do inversor, o SRF-PLL foi testado isolado entre duas fontes ideais.",
        "pontos": [
            ("Bruno", "Apontar o diagrama da bancada no PSIM (Cartão 1 — Sem conversor): geração representada como fonte trifásica ideal à esquerda e rede como equivalente de Thévenin + barramento infinito à direita; sem chaveamento PWM e sem filtro LCL."),
            ("Victor", "Cartões 2 e 3 + Rodapé: serviu para validar o travamento (v_q → 0 e θ_PLL seguindo θ_rede) e dimensionar os ganhos K_pPLL e K_iPLL de forma isolada — se o PLL falhasse ali, o problema seria do laço, não do conversor."),
        ],
        "falas": [
            ("Bruno", "Antes de conectar o inversor completo, montamos no PSIM esta bancada isolada: à esquerda uma fonte trifásica ideal representando a geração e, à direita, a rede com a impedância de Thévenin e o barramento infinito, sem chaves semicondutoras e sem filtro LCL."),
            ("Victor", "O objetivo metodológico dessa etapa, destacado no rodapé, é isolar o subsistema de sincronismo: validamos ali o erro vq indo a zero, o travamento do ângulo e o dimensionamento dos ganhos do controlador PI que detalhamos no próximo slide."),
        ],
        "atencao": "Exceção de método aprovada: não citar nenhum número neste slide.",
    },
    {
        "tipo": "SLIDE",
        "num": 10,
        "titulo": "Sintonia do PLL",
        "bloco": "Modelagem",
        "tcc": "§3.4, Eqs. (3.10)-(3.20)",
        "quem": "Victor → Bruno → Victor",
        "dur_s": 75,
        "msg": "Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação.",
        "pontos": [
            ("Victor", "Etapa 1 (Tensão em pu): a tensão medida é dividida pelo pico nominal de fase de 20 kV (16.329,93 V), fazendo V_m = 1 pu e o ganho do detector K_pd = 1 em condição nominal."),
            ("Bruno", "Etapas 2, 3 e 4 (Linearizar, Forma canônica e Fixar ξ): perto do travamento, v_q ≈ V_m(θ_ref − θ_PLL); casando com s² + 2ξω_n·s + ω_n² = 0, saem K_iPLL = ω_n² e K_pPLL = 2ξω_n. Fixa-se ξ = 0,707 (compromisso clássico de Ogata, sobre-elevação ~5%), restando um único grau de liberdade: o tempo de acomodação t_s."),
            ("Victor", "Etapa 5 (Régua do t_s) e Caixa de cálculo: t_s muito curto deixa passar ruído e desequilíbrio; muito longo não acompanha a rede. Pelo critério de 1% (t_s = 4,6/(ξω_n)), adota-se t_s = 20 ms (pouco mais de 1 período da rede, conforme Alves, Dias e Rolim, 2020 e Teodorescu et al., 2011), resultando em K_pPLL = 9,2/t_s = 460, ω_n = 325,3 rad/s (51,8 Hz) e K_iPLL = 105.820."),
        ],
        "falas": [
            ("Victor", "Este slide mostra como chegamos aos ganhos nominais do PLL em cinco etapas. Na etapa 1, a tensão na entrada do PLL é normalizada em por unidade pelo valor de pico nominal de fase, 16.329,93 volts, de modo que em regime nominal a amplitude vale 1 pu e o ganho do detector de fase é unitário."),
            ("Bruno", "Nas etapas 2 a 4, linearizando o detector para pequenos desvios em torno do travamento, igualamos a equação característica à forma canônica de segunda ordem, obtendo Ki igual a ômega n ao quadrado e Kp igual a 2 ksi ômega n. Fixamos então o amortecimento em 0,707, valor clássico de Ogata que limita a sobre-elevação a cerca de 5%, restando um único grau de liberdade: o tempo de acomodação ts."),
            ("Victor", "Na régua à direita vemos o compromisso de projeto: um ts curto demais amplia a banda e deixa passar ruído e desequilíbrio; longo demais atrasa o rastreamento da rede. Adotando o critério de 1%, em que ts é 4,6 sobre ksi ômega n, escolhemos ts igual a 20 milissegundos, pouco mais de um período da fundamental, conforme Alves, Dias e Rolim e Teodorescu, Liserre e Rodriguez. Na caixa inferior, isso fornece Kp igual a 460, frequência natural de 325,3 radianos por segundo, ou 51,8 hertz, e Ki igual a 105.820."),
        ],
        "atencao": "Não citar '16,7 ms' neste slide (a régua traz apenas '1 período' e '20 ms'). Usar sempre Ki = 105.820.",
    },
    {
        "tipo": "SLIDE",
        "num": 11,
        "titulo": "Duas sintonias do PLL",
        "bloco": "Modelagem",
        "tcc": "§3.4 (eq. 3.20), §4.3",
        "quem": "Bruno → Victor",
        "dur_s": 55,
        "msg": "A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos amortecido.",
        "pontos": [
            ("Bruno", "Tabela comparativa (esquerda) e Rodapé: para investigar a sensibilidade paramétrica, a sintonia inadequada multiplica K_pPLL e K_iPLL por 0,2 (caindo para 92 e 21.164). Com isso, ω_n cai de 325,3 para 145,5 rad/s e ξ cai de 0,707 para 0,316 — uma malha mais lenta e menos amortecida que, no caso-limite, não recupera o sincronismo."),
            ("Victor", "Cartão da direita (2ω_0 = 2,32·ω_n): sob falta assimétrica, a sequência negativa oscila a 120 Hz (754 rad/s) em v_q, o que representa apenas 2,32 vezes a frequência natural nominal (325,3 rad/s) — perto demais da banda do PI para ser atenuada de forma significativa."),
        ],
        "falas": [
            ("Bruno", "Para testar a sensibilidade do sincronismo à escolha de projeto, comparamos na tabela duas parametrizações: a sintonia nominal em azul e a sintonia inadequada em laranja, obtida reduzindo ambos os ganhos em 80%, para Kp igual a 92 e Ki igual a 21.164. Como Ki cai cinco vezes, a frequência natural cai pela raiz de 5, para 145,5 radianos por segundo, e o amortecimento cai na mesma proporção, para 0,316, tornando o laço mais lento e subamortecido."),
            ("Victor", "No cartão à direita destacamos o segundo problema que motiva nossos testes: sob faltas assimétricas, a oscilação de 120 hertz corresponde a 754 radianos por segundo, o que representa apenas 2,32 vezes a frequência natural da sintonia nominal. Como um filtro de segunda ordem só atenua bem frequências muito acima de ômega n, o controlador PI não rejeita essa componente, e é o compromisso entre filtrar os 120 hertz e não perder o sincronismo que vamos investigar."),
        ],
        "atencao": "Sempre dizer 'sintonia inadequada' (nunca dizer BAD_PLL ou PLL ruim).",
    },
    {
        "tipo": "SLIDE",
        "num": 12,
        "titulo": "Referência de corrente",
        "bloco": "Modelagem",
        "tcc": "§3.1.3-3.1.4, Eqs. (3.8)-(3.9)",
        "quem": "Victor → Bruno",
        "dur_s": 45,
        "msg": "Na primeira versão do inversor, a referência de corrente saía direto da potência desejada.",
        "pontos": [
            ("Victor", "Diagrama superior (1ª versão no PSIM): aplica-se P_ref = 1 pu (100 MW, degrau em t = 35 ms) e Q_ref = 0; ambas são divididas pela tensão de eixo direto v_d entregue pelo SRF-PLL para gerar i_d,ref e i_q,ref."),
            ("Bruno", "Cartão inferior esquerdo (Eq. 3.9 invertida: i_d,ref = 2P/(3v_d) e i_q,ref = −2Q/(3v_d)) e Rodapé: em pu o fator 3/2 desaparece, mas essa divisão simples só desacopla P e Q porque assume v_q = 0 — e quem alinha o eixo d com a tensão para zerar v_q é o SRF-PLL."),
        ],
        "falas": [
            ("Victor", "Passamos agora à construção do inversor em etapas. Na primeira versão montada no PSIM, mostrada no diagrama, as referências de potência eram fixas: um degrau de 1 por unidade de potência ativa, os 100 megawatts, aplicado aos 35 milissegundos, e potência reativa nula, divididos diretamente pela tensão vd estimada pelo SRF-PLL."),
            ("Bruno", "No cartão inferior esquerdo temos a Equação 3.9 do TCC invertida: id de referência igual a 2P sobre 3 vd e iq de referência igual a menos 2Q sobre 3 vd. Como destaca o rodapé, essa relação direta só é válida quando vq é igual a zero, ou seja, quem garante o alinhamento do eixo d e o desacoplamento entre potência ativa e reativa é o próprio SRF-PLL."),
        ],
        "atencao": "'t = 35 ms' é o único número de etapa de modelagem (PSIM) aprovado neste slide.",
    },
    {
        "tipo": "SLIDE",
        "num": 13,
        "titulo": "Filtro LCL",
        "bloco": "Modelagem",
        "tcc": "§4.3.2 e §4.3.2.1",
        "quem": "Bruno → Victor",
        "dur_s": 60,
        "msg": "Quatro passos fixam o filtro, com a ressonância entre a rede e o chaveamento.",
        "pontos": [
            ("Bruno", "Esquema elétrico por fase à esquerda e Passos 1 e 2 à direita: entre o VSI chaveando a 5 kHz e o PCC na Barra 2 entra o filtro LCL. No Passo 1, L_1 é dimensionado pelo limite de ondulação (ripple) da corrente; no Passo 2, L_2 é proporcional a L_1, totalizando L_est = L_1 + L_2 = 30,71 mH."),
            ("Victor", "Passos 3 e 4, Régua de frequência e Rodapé: no Passo 3, o capacitor C posiciona a frequência de ressonância em ω_res = 9.068,99 rad/s (na régua, longe dos 60 Hz da rede e dos 5 kHz do chaveamento); no Passo 4, as resistências de amortecimento passivo valem 5% da reatância em 60 Hz (R_d1 = 0,5734 Ω, R_d2 = 0,0054 Ω e R_d3 = 3,1228 Ω). Na caixa direita do rodapé: barramento CC fixado em valor constante para manter a margem de modulação."),
        ],
        "falas": [
            ("Bruno", "Antes de fechar a malha de corrente, dimensionamos o filtro LCL que conecta o inversor à Barra 2, seguindo quatro passos. No circuito à esquerda, o inversor chaveia a 5 quilohertz. Nos passos 1 e 2 à direita, o indutor L1 é fixado pelo limite de ondulação da corrente na saída das chaves e L2 é tomado proporcional a L1, resultando na indutância equivalente Lest de 30,71 milihenrys."),
            ("Victor", "No passo 3, o capacitor posiciona a frequência de ressonância em 9.068,99 radianos por segundo: como mostra a régua, numa faixa intermediária segura entre os 60 hertz da rede e os 5 quilohertz do chaveamento. No passo 4, inserimos resistências de amortecimento passivo iguais a 5% da reatância de cada ramo em 60 hertz: 0,5734, 0,0054 e 3,1228 ohms, suprimindo o pico de ressonância, enquanto o barramento CC é mantido constante para garantir a margem de modulação."),
        ],
        "atencao": "Citar apenas os números que estão na tela (L_est = 30,71 mH, ω_res = 9.068,99 rad/s, R_d1/R_d2/R_d3, 60 Hz e 5 kHz). Os valores individuais de L_1, L_2, C e V_cc ficam apenas para perguntas no Apêndice (Slide 22).",
    },
    {
        "tipo": "SLIDE",
        "num": 14,
        "titulo": "Controle de corrente",
        "bloco": "Modelagem",
        "tcc": "Fig. 3.1, §3.5 (Eqs. 3.21-3.23), §4.3.2",
        "quem": "Bruno → Victor",
        "dur_s": 55,
        "msg": "Um PI com notch em cada eixo faz a corrente do inversor seguir a referência.",
        "pontos": [
            ("Bruno", "Figura 3.1 à esquerda e Cartão 1 (PWM): malhas idênticas nos eixos d e q; o erro de corrente passa pelo PI, pelo filtro notch N(s) sintonizado na ressonância do LCL e gera os índices de modulação m_d e m_q para o PWM de 5 kHz."),
            ("Victor", "Cartões 2 e 3 (Filtro LCL e PI de corrente) + Rodapé: em baixa frequência o filtro LCL equivale à indutância L_est = 30,71 mH (com ω_res = 9.068,99 rad/s e ξ = 0,707). Pela mesma forma canônica do PLL, fixa-se ξ = 0,707 e ω_n = 4√2·f_g para acomodar em 1 ciclo da rede, resultando em K_p = 8·f_g·L_est e K_i = 32·f_g²·L_est. Rodapé: o PI do PLL entrega o ângulo; o PI de corrente faz i_d e i_q seguirem a referência."),
        ],
        "falas": [
            ("Bruno", "Na Figura 3.1 temos a malha interna de controle de corrente nos eixos d e q. Em cada eixo, o erro entre a corrente de referência e a corrente medida passa por um controlador PI, atravessa um filtro notch sintonizado exatamente na frequência de ressonância do LCL e gera o índice de modulação para o chaveamento PWM a 5 quilohertz."),
            ("Victor", "Nos cartões à direita, como em baixa frequência o filtro LCL se comporta como a indutância equivalente Lest de 30,71 milihenrys, sintonizamos o PI de corrente pela mesma forma canônica de segunda ordem: com amortecimento de 0,707 e frequência natural de 4 raiz de 2 vezes a frequência da rede, a corrente acomoda em um ciclo, resultando em Kp igual a 8 fg Lest e Ki igual a 32 fg ao quadrado Lest. Como resume o rodapé, são dois PIs independentes: o do PLL entrega o ângulo e o de corrente faz id e iq seguirem as referências."),
        ],
        "atencao": "Nunca confundir os dois PIs: os ganhos do PI de corrente ficaram fixos em todos os cenários; só a sintonia do SRF-PLL varia.",
    },
    {
        "tipo": "SLIDE",
        "num": 15,
        "titulo": "Submódulo 2.10 do ONS",
        "bloco": "Modelagem",
        "tcc": "Fig. 2.2, §2.5.2, §4.3.2, §5.2",
        "quem": "Bruno",
        "dur_s": 65,
        "msg": "No modelo final, a tensão medida define o reativo e o ativo fica com o que sobra.",
        "pontos": [
            ("Bruno", "Substituição das referências fixas pela lógica de suporte de subtensão do Submódulo 2.10 do ONS: no gráfico à esquerda, é a tensão que define o reativo. Na faixa normal (0,85 a 1,1 pu), corrente reativa de referência zero e potência ativa nominal."),
            ("Bruno", "Quando a tensão afunda abaixo de 0,85 durante uma falta, o código de rede exige a injeção de corrente reativa proporcional a esse afundamento, seguindo a rampa da equação até o limite de saturação (em 0,5 pu ou menos, injeta 100% da corrente máxima, ou seja, 1 pu de corrente reativa)."),
            ("Bruno", "No gráfico à direita, regra de prioridade sobre o limite de corrente: a corrente máxima forma esse raio, e a corrente reativa tem prioridade total para sustentar a tensão. A corrente ativa fica apenas com o que sobra dentro desse círculo."),
        ],
        "falas": [
            ("Bruno", "No modelo final do nosso inversor, nós substituímos aquelas referências fixas por essa lógica de suporte de subtensão do Submódulo 2.10 do ONS. Como vocês podem ver no gráfico à esquerda, é a tensão que define o reativo. Quando a tensão medida permanece numa faixa normal, entre 0,85 e 1,1 por unidade, a corrente reativa de referência é zero e o inversor injeta potência ativa nominal.\n\nQuando essa tensão afunda abaixo de 0,85 durante uma falta, o código de rede exige a injeção de corrente reativa proporcional a esse afundamento, seguindo essa rampa da equação. Isso vai até o limite de saturação: quando a tensão chega a 0,5 p.u. ou menos, o inversor injeta 100% da corrente máxima, ou seja, 1 p.u. de corrente reativa.\n\nNo gráfico à direita, vemos a nossa regra de prioridade sobre o limite de corrente. A corrente máxima forma esse raio, e a corrente reativa tem prioridade total para sustentar a tensão. A corrente ativa fica apenas com o que sobra dentro desse círculo."),
        ],
        "atencao": "Slide novo enxuto: foco na rampa (0,85 a 0,5 pu) e na prioridade de reativo no círculo de corrente máxima.",
    },
    {
        "tipo": "SLIDE",
        "num": 16,
        "titulo": "Sistema completo",
        "bloco": "Modelagem",
        "tcc": "Fig. 4.2, §4.3.2",
        "quem": "Bruno",
        "dur_s": 40,
        "msg": "Juntando as partes, este é o inversor usado em todas as simulações.",
        "pontos": [
            ("Bruno", "Integração do modelo completo utilizado em todas as simulações, como mostra a Figura 4.2 do TCC."),
            ("Bruno", "Na parte superior, a etapa de potência com inversor, filtro LCL e ponto de acoplamento da Barra 2; na parte inferior, o controle digital onde tudo se conecta (SRF-PLL entrega o ângulo, Submódulo 2.10 define referências de corrente pela tensão e malhas geram modulação)."),
            ("Bruno", "Com o modelo fechado, passagem para o método de teste para ver como as contingências vão testar esse SRF-PLL."),
        ],
        "falas": [
            ("Bruno", "Juntando então todas essas partes, chegamos ao nosso modelo completo, que foi utilizado em todas as simulações, como mostra a Figura 4.2 do TCC.\n\nNa parte superior, temos a etapa de potência, com o inversor, o filtro LCL e o ponto de acoplamento da Barra 2. Na parte inferior, o controle digital, onde tudo se conecta: o SRF-PLL entrega o ângulo, o Submódulo 2.10 define as referências de corrente a partir da tensão, e as malhas de controle geram a modulação.\n\nCom o modelo fechado, passamos agora para o nosso método de teste, para ver como as contingências vão testar esse nosso SRF-PLL."),
        ],
        "atencao": "Slide de fechamento da Modelagem: transição direta para o Método de Teste (Slide 17).",
    },
    {
        "tipo": "SLIDE",
        "num": 17,
        "titulo": "Protocolo de contingência",
        "bloco": "Método",
        "tcc": "§4.3.4, Tab. 4.1, §5.2",
        "quem": "Bruno → Victor",
        "dur_s": 60,
        "msg": "Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da falta.",
        "pontos": [
            ("Bruno", "Linha do tempo no topo: 0 a 0,1 s = Inicialização (partida do modelo e travamento inicial do PLL, fora das métricas); 0,1 a 0,3 s = Pré-falta (regime permanente, base para as métricas em %); 0,3 a 0,4 s = Falta (100 ms = 6 ciclos de 60 Hz); 0,4 a 0,6 s = Pós-falta (janela de 200 ms para observar a recuperação)."),
            ("Victor", "Matriz de cenários e caixas inferiores: colunas azuis analisadas no texto da mais próxima à mais distante da UFV (Barra 7, Linha 7-8, Linha 8-9 e Barra 6) e colunas cinzas (Barras 4, 5, 8 e 9) simuladas e consultáveis no painel. Faltas trifásicas nos 4 pontos e faltas assimétricas (monofásica e bifásica, que injetam sequência negativa) nas Barras 7 e 6, comparando sintonia nominal (N) e inadequada (I). Rodapé: a janela de 200 ms pós-falta delimita o alcance das conclusões sobre recuperação."),
        ],
        "falas": [
            ("Bruno", "Entrando na metodologia, todas as simulações seguem rigorosamente a mesma linha do tempo no topo do slide: de 0 a 0,1 segundo ocorre a inicialização do modelo, que fica fora das métricas; de 0,1 a 0,3 segundo o sistema opera em regime permanente pré-falta; em t igual a 0,3 segundo aplicamos a falta por 100 milissegundos, ou seja, 6 ciclos de 60 hertz; e de 0,4 a 0,6 segundo observamos os 200 milissegundos de recomposição pós-falta."),
            ("Victor", "Na matriz abaixo estão as combinações de local e tipo de curto-circuito. Nas colunas em azul estão os quatro pontos analisados em detalhe no texto, ordenados do mais próximo ao mais distante da usina: Barra 7, Linha 7-8, Linha 8-9 e Barra 6; e em cinza as demais barras, também simuladas e disponíveis no painel. Aplicamos faltas trifásicas nos quatro locais e faltas monofásicas e bifásicas nas Barras 7 e 6, confrontando a sintonia nominal N e a inadequada I."),
        ],
        "atencao": "Não citar número total de cenários (o slide não traz contagem). Dizer que 'não retorna' significa 'não retorna dentro da janela de 200 ms pós-falta'.",
    },
    {
        "tipo": "SLIDE",
        "num": 18,
        "titulo": "Fluxo de análise",
        "bloco": "Método",
        "tcc": "§4.3.3; métricas em §5.1-5.3",
        "quem": "Bruno → Victor → Bruno",
        "dur_s": 60,
        "msg": "Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel interativo.",
        "pontos": [
            ("Bruno", "Quatro cartões superiores (1. Simulink → 2. Arquivos CSV → 3. Python → 4. Painel interativo): cada cenário exporta tensões, correntes, P, Q e variáveis internas do SRF-PLL; o script em Python processa os dados de forma padronizada até gerar o painel interativo."),
            ("Victor", "Tabela das 5 métricas: (1) Retenção de V_d (% do valor pré-falta durante a falta, ex.: 9,2% na Barra 7 nominal); (2) Pico do erro de fase |Δθ| na falta após descartar o 1º ciclo; (3) Tempo de retorno definitivo à faixa de ±2° contado da eliminação em 0,4 s; (4) Componente de 120 Hz extraída pela FFT de V_d na janela de 6 ciclos da falta (resolução de 10 Hz); e (5) Potências P e Q médias na falta."),
            ("Bruno", "Rodapé ('Dos dados aos resultados'): fazer a ponte direta para o Slide 19 e a abertura do painel ao vivo."),
        ],
        "falas": [
            ("Bruno", "Para garantir que todos os cenários fossem avaliados pelo mesmo critério, automatizamos o fluxo de análise em quatro etapas: cada rodada no Simulink exporta arquivos CSV com as variáveis da rede, do inversor e do SRF-PLL, que são processados em Python para extrair os indicadores e montar o painel interativo."),
            ("Victor", "Na tabela estão as cinco métricas calculadas automaticamente: a retenção de vd em porcentagem do valor pré-falta; o pico do erro de fase durante a falta, medido após o primeiro ciclo para descartar o salto instantâneo da aplicação do curto; o tempo de retorno definitivo à faixa de mais ou menos 2 graus após a eliminação da falta; a amplitude da componente de 120 hertz no espectro de Fourier de vd durante os 6 ciclos da falta; e as potências ativa e reativa médias."),
            ("Bruno", "Como indica o rodapé, é com essas cinco métricas que lemos os resultados: passamos agora ao próximo slide para abrir o painel interativo ao vivo."),
        ],
        "atencao": "Saber explicar por que a FFT na janela de 0,1 s (6 ciclos) é exata em 120 Hz: Δf = 1/0,1 s = 10 Hz, então 60 e 120 Hz caem exatamente em bins inteiros sem vazamento espectral.",
    },
    # -------------------------------------------------------------------------
    # PARTE II: SLIDE 19 (PORTA PARA O PAINEL)
    # -------------------------------------------------------------------------
    {
        "tipo": "SLIDE",
        "num": 19,
        "titulo": "Demonstração ao vivo",
        "bloco": "Porta para o painel",
        "tcc": "Cap. 5 (no painel HTML)",
        "quem": "Victor",
        "dur_s": 20,
        "msg": "Os resultados seguem no painel interativo, em modo apresentação.",
        "pontos": [
            ("Victor", "Anunciar a transição para o navegador (Alt+Tab para `pll_metrics.html`, já aberto offline antes da defesa) e clicar no botão 'Modo apresentação' no canto superior direito para percorrer os 8 capítulos de resultados em tela cheia."),
        ],
        "falas": [
            ("Victor", "A partir deste ponto, apresentamos todos os resultados do Capítulo 5 diretamente no nosso painel interativo em modo apresentação. (Pressiona Alt+Tab para o navegador e clica em 'Modo apresentação')."),
        ],
        "atencao": "Ação prática: Alt+Tab -> clicar em 'Modo apresentação'. Usar Seta -> ou PageDown para avançar cada passo dos capítulos 1 a 8.",
    },
]

PALCO_ROTEIRO = [
    # -------------------------------------------------------------------------
    # PARTE III: PAINEL INTERATIVO HTML — CAPÍTULOS 1 A 8 (VERSÃO FINAL)
    # -------------------------------------------------------------------------
    {
        "tipo": "PAINEL",
        "num": 1,
        "titulo": "Faltas destacadas (Mapa Unifilar e Régua de Severidade)",
        "bloco": "Painel HTML · Cap. 1/8 · 6 passos",
        "tcc": "Antes dos resultados (Fig. 4.1 e Tab. 4.1)",
        "quem": "Victor → Bruno",
        "dur_s": 60,
        "reserva": "Slide 17 (Matriz do Protocolo)",
        "msg": "Quatro pontos de falta, do mais próximo ao mais distante da usina fotovoltaica; a pergunta é como a distância elétrica muda a resposta do SRF-PLL.",
        "pontos": [
            ("Victor", "Passo 1 (Visão geral): apresentar o unifilar limpo do IEEE 9 barras e explicar que a análise foca em 4 pontos que vão do afundamento mais profundo ao mais raso (duas barras e duas linhas)."),
            ("Victor", "Passo 2 (Seta → Barra 7) e Passo 3 (Seta → Linha 7-8): Barra 7 fica logo após o transformador T2 (extremo mais severo, recebe 3φ, 2φ, 1φ nas duas sintonias); Linha 7-8 sai da B7 em circuito simples (toda a linha fica sob falta, 3φ nas duas sintonias)."),
            ("Bruno", "Passo 4 (Seta → Linha 8-9), Passo 5 (Seta → Barra 6) e Passo 6 (Seta → Resumo): Linha 8-9 tem circuito duplo (um caminho segue conduzindo, 3φ nominal); Barra 6 fica a três linhas de distância no ramo inferior (extremo mais brando, 3φ, 2φ, 1φ nas duas sintonias). No Passo 6, a régua inferior resume a ordem B7 → L7-8 → L8-9 → B6."),
        ],
        "falas": [
            ("Victor", "No primeiro capítulo do modo apresentação vemos onde as faltas são aplicadas no sistema IEEE 9 barras. No passo 1 temos a visão geral dos quatro pontos destacados. (Seta →) No passo 2, o ponto mais crítico é a Barra 7, logo depois do transformador T2: como só existe o transformador entre o inversor e o defeito, o afundamento ali é o mais profundo. (Seta →) No passo 3 temos a Linha 7-8, de circuito simples, ainda eletricamente muito próxima da usina."),
            ("Bruno", "(Seta →) Avançando ao passo 4, a Linha 8-9 possui dois circuitos em paralelo: a falta ocorre em apenas um deles e o outro continua conduzindo. (Seta →) No passo 5 chegamos à Barra 6, no ramo inferior, separada da usina por três linhas de transmissão, sendo o caso mais brando e o contraponto da Barra 7. (Seta →) E o passo 6 fecha o resumo na régua inferior: da mais severa à mais branda, Barra 7, Linha 7-8, Linha 8-9 e Barra 6. (Seta → para o Cap. 2)"),
        ],
        "atencao": "Conceito físico: 'distância' aqui é impedância elétrica (divisor de tensão entre o inversor e a falta), não quilômetros.",
    },
    {
        "tipo": "PAINEL",
        "num": 2,
        "titulo": "Energização do inversor",
        "bloco": "Painel HTML · Cap. 2/8 · 2 passos",
        "tcc": "§5.1 · Figura 5.3",
        "quem": "Victor → Bruno",
        "dur_s": 50,
        "reserva": "Slide Oculto 24",
        "msg": "Na partida, o SRF-PLL trava na rede: o erro de fase entra na faixa de 2° em 40 ms com a sintonia nominal e em 79 ms com a inadequada, quase o dobro.",
        "pontos": [
            ("Victor", "Passo 1 (Nominal em azul, foco 0 a 60 ms): sem falta na rede, o erro de fase entra na faixa verde de ±2° em 40 ms (e v_d entra em ±5% em 34 ms)."),
            ("Bruno", "Passo 2 (Seta → Entra a inadequada em laranja + Fasor à direita): com ganhos reduzidos em 80%, o erro oscila mais e leva 79 ms para entrar em ±2° (quase o dobro; v_d leva 42 ms). Ao clicar em '▶ play' no fasor, os dois vetores convergem para o topo antes de 0,1 s: em regime permanente as duas sintonias funcionam igual — a inadequada é lenta, não quebrada."),
        ],
        "falas": [
            ("Victor", "No Capítulo 2 avaliamos a energização do inversor sem falta, correspondente à Figura 5.3 do TCC. No passo 1, com a sintonia nominal em azul, o erro de fase converge rapidamente e entra de vez na faixa de mais ou menos 2 graus em 40 milissegundos."),
            ("Bruno", "(Seta →) No passo 2 ligamos a sintonia inadequada em laranja: por ter menor amortecimento e menor banda, ela oscila mais e leva 79 milissegundos para entrar na faixa de 2 graus, quase o dobro do tempo, enquanto embaixo a tensão vd acomoda em 42 milissegundos contra 34 da nominal. Olhando o fasor à direita, vemos que ambas travam no topo muito antes de a falta começar em 0,3 segundo: ou seja, a sintonia inadequada é lenta, mas em regime permanente ela opera normalmente. A diferença crítica só aparece nas contingências. (Seta → para o Cap. 3)"),
        ],
        "atencao": "Deixar claro que às vésperas da falta (t = 0,3 s) as duas sintonias estão perfeitamente travadas no mesmo ponto de operação.",
    },
    {
        "tipo": "PAINEL",
        "num": 3,
        "titulo": "Falta trifásica: quanto mais perto, mais severa",
        "bloco": "Painel HTML · Cap. 3/8 · 3 passos",
        "tcc": "§5.2 · Tabela 5.1 · Figura 5.7",
        "quem": "Bruno",
        "dur_s": 75,
        "reserva": "Slide Oculto 25",
        "msg": "A mesma falta trifásica em quatro pontos: quanto mais perto da usina, menos tensão sobra e maior o erro, mas com a sintonia nominal o erro sempre volta à faixa de 2° em até 112 ms.",
        "pontos": [
            ("Bruno", "Passo 1 (Retenção da tensão vd no mini-mapa): aplicação da mesma falta trifásica franca nos 4 pontos sob sintonia nominal. A retenção da tensão vd segue a distância elétrica, caindo para 9,2% na Barra 7 e alcançando 58,4% na Barra 6."),
            ("Bruno", "Passo 2 (Seta → Pico do erro de fase): acompanha a severidade da falta, atingindo 37,3 graus na Barra 7 contra apenas 7,3 graus na Barra 6."),
            ("Bruno", "Passo 3 (Seta → Janela pós-falta e setas no topo): na sintonia nominal, o SRF-PLL recupera o sincronismo em todos os casos, retornando a 2 graus em no máximo 112 ms na Linha 8-9 (delay um pouco maior pela dinâmica da linha dupla). Sem sequência negativa, distúrbio puramente transitório."),
        ],
        "falas": [
            ("Bruno", "Entrando no nosso Capítulo 3 aqui do painel, a gente aplica a mesma falta trifásica franca nos quatro pontos da rede, mantendo a nossa sintonia nominal.\n\nNo passo 1, vocês podem ver no mini-mapa à direita como a retenção da tensão vd segue exatamente a nossa distância elétrica. Ela cai ali para 9,2% quando a gente trata da Barra 7, mas quando a gente trata de um curto lá na Barra 6, a tensão consegue sobreviver ali com quase 60% do valor, cravando 58,4%.\n\n(Seta →) Já aqui no nosso segundo passo, nós vemos que o pico do erro de fase também acompanha essa severidade, né? Ele atinge um pico bem alto ali na Barra 7, de 37,3 graus, contra apenas 7,3 graus na Barra 6.\n\n(Seta →) Bom, abrindo essa janela de pós-falta, as setas no topo confirmam que a sintonia nominal do nosso SRF-PLL recupera o sincronismo em todos os casos. Ele retorna à nossa faixa de 2 graus em, no máximo, 112 milissegundos, que acontece na nossa Linha 8-9 — por ser um circuito duplo, quando uma das linhas sai e a outra fica sozinha após a falta, ele tem esse delay um pouco maior. Então, vocês podem ver que sem a sequência negativa, o distúrbio é puramente transitório, sem problema algum."),
        ],
        "atencao": "Ponto de atenção da Linha 8-9 (112 ms): circuito duplo em que uma das linhas sai na falta e a outra permanece sozinha na recuperação, justificando o tempo de acomodação.",
    },
    {
        "tipo": "PAINEL",
        "num": 4,
        "titulo": "Faltas assimétricas: de onde vem o 120 Hz (NOVO: 5 Passos Didáticos)",
        "bloco": "Painel HTML · Cap. 4/8 · 5 passos",
        "tcc": "§5.3 · Tabela 5.3 · Figura 5.10",
        "quem": "Bruno",
        "dur_s": 80,
        "reserva": "Slide Oculto 26",
        "msg": "Nas faltas assimétricas, a sequência negativa gira ao contrário da rede e aparece no referencial dq do PLL como uma oscilação de 120 Hz (0,29 a 0,72 pu), mais de 250 vezes maior que nas trifásicas.",
        "pontos": [
            ("Bruno", "Passo 1 (Tensões trifásicas na Barra 6): na falta trifásica as três fases caem por igual, enquanto na falta bifásica elas ficam desequilibradas."),
            ("Bruno", "Passo 2 (Seta → Animação do Teorema de Fortescue à direita): soma da sequência positiva (gira com a rede) com a negativa (sentido oposto). Visto do referencial do PLL, a positiva fica parada no eixo e a negativa gira ao contrário em velocidade dupla: 120 hertz."),
            ("Bruno", "Passo 3 (Seta → Componentes vd e vq): na trifásica temos praticamente uma falta contínua; a bifásica oscila bastante nesses 120 hertz."),
            ("Bruno", "Passo 4 (Seta → Entrada do controlador PI em vq): 120 hertz próximo da frequência natural do laço; o PI acaba não conseguindo filtrar e lê essa oscilação como erro de fase, dando um salto bem alto."),
            ("Bruno", "Passo 5 (Seta → Espectro de Fourier de vd na falta): na trifásica o 120 hertz é quase irrisório; nas assimétricas chega a 0,72 pu na Barra 7, mais de 250 vezes maior do que na trifásica."),
        ],
        "falas": [
            ("Bruno", "(Seta → para abrir o Cap. 4) No Capítulo 4, quando nós falamos de faltas assimétricas, a gente mostra outra face do nosso controlador. No passo 1, comparando as tensões trifásicas na Barra 6, a gente pode ver que na falta trifásica as três fases caem por igual, enquanto na falta bifásica elas ficam desequilibradas.\n\n(Seta →) A animação à direita no passo 2 mostra exatamente isso e explica como esse desequilíbrio funciona através do Teorema de Fortescue. Ele nada mais é do que a soma da sequência positiva, que está girando ali junto com a nossa rede, com a sequência negativa, que gira no sentido oposto. E como o referencial do nosso PLL gira junto com a positiva, na vista dele, a positiva fica exatamente embaixo e parada no eixo, enquanto a negativa gira ao contrário numa velocidade dupla, ou seja, em 120 hertz.\n\n(Seta →) No passo 3, a gente pode ver os efeitos diretos disso nas nossas componentes vd e vq. Enquanto na trifásica temos praticamente uma falta contínua, a bifásica oscila bastante nesses 120 hertz.\n\n(Seta →) E como vq é exatamente a entrada do nosso controlador PI, e esses 120 hertz estão bem próximos da frequência natural desse laço, no passo 4 vemos que o PI acaba não conseguindo filtrar essas componentes, e ele lê essa oscilação como um erro de fase, que dá um salto bem alto.\n\n(Seta →) Aqui no passo 5, a gente demonstra exatamente isso dentro do espectro de Fourier do vd durante a falta. Na trifásica, a gente não consegue nem enxergar um valor para 120 hertz, porque ele é quase irrisório. Já nas assimétricas, no curto mais severo que seria na Barra 7, ele chega a 0,72 p.u. — o que é um valor mais de 250 vezes maior do que na trifásica."),
        ],
        "atencao": "Capítulo 4 em 5 passos didáticos: 1 (v_abc) -> 2 (Fortescue) -> 3 (v_d e v_q) -> 4 (v_q e erro) -> 5 (espectro FFT > 250×).",
    },
    {
        "tipo": "PAINEL",
        "num": 5,
        "titulo": "Compromisso da sintonia: ganho menor filtra melhor o 120 Hz",
        "bloco": "Painel HTML · Cap. 5/8 · 3 passos",
        "tcc": "§5.3 · Tabela 5.3 · Figura 5.14",
        "quem": "Bruno → Victor",
        "dur_s": 55,
        "reserva": "Slide Oculto 27",
        "msg": "Na bifásica da Barra 6, o ganho menor filtra melhor o 120 Hz (pico cai de 96,0° para 34,5° e retorno de 48 para 30 ms), mas retarda a recuperação onde a falta é severa.",
        "pontos": [
            ("Bruno", "Passo 1 (Nominal em azul na B6 bifásica) e Passo 2 (Seta → Inadequada em laranja): no Passo 1, com banda nominal, o 120 Hz leva o erro a 96,0°. No Passo 2, embora o 120 Hz em v_d seja quase idêntico (0,39 vs. 0,37 pu), a menor banda da sintonia inadequada atenua a oscilação e reduz o pico do erro para 34,5° e o retorno de 48 para 30 ms."),
            ("Victor", "Passo 3 (Seta → Visão completa e pergunta-ponte): explicar por que funcionou na Barra 6 (a tensão residual positiva v_d = 0,72 pu ainda sustenta o laço) e apontar o preço pago na Barra 7 (onde o tempo de retorno quase dobra: 46 → 95 ms na monofásica e 51 → 96 ms na bifásica). Fechar com a pergunta na tela: 'E numa falta mais severa?'"),
        ],
        "falas": [
            ("Bruno", "Diante dessa oscilação de 120 hertz, uma solução frequentemente sugerida é reduzir os ganhos do PI para estreitar a banda passante, o que testamos no Capítulo 5, correspondente à Figura 5.14 do TCC. No passo 1 temos a falta bifásica na Barra 6 com a sintonia nominal, onde o erro atinge 96,0 graus. (Seta →) No passo 2, ao aplicar a sintonia inadequada em laranja, a oscilação de 120 hertz em vd continua quase a mesma, cerca de 0,38 pu, mas como a banda caiu o PI filtra melhor: o pico do erro cai para 34,5 graus e o retorno cai de 48 para 30 milissegundos."),
            ("Victor", "(Seta →) No passo 3 entendemos a armadilha desse compromisso: na Barra 6, a falta é distante e sobram 0,72 pu de tensão positiva para manter o PLL travado, então a filtragem vence. Porém, nas faltas da Barra 7, essa mesma lentidão já faz o tempo de retorno quase dobrar, subindo de 46 para 95 milissegundos na monofásica e de 51 para 96 milissegundos na bifásica. Fica então a pergunta na tela: o que acontece com esse ganho menor numa falta ainda mais severa? (Seta → para o Cap. 6)"),
        ],
        "atencao": "O Passo 3 deste capítulo é o clímax que prepara a perda de sincronismo do Capítulo 6.",
    },
    {
        "tipo": "PAINEL",
        "num": 6,
        "titulo": "Barra 7 trifásica: a sintonia decide o sincronismo",
        "bloco": "Painel HTML · Cap. 6/8 · 3 passos",
        "tcc": "§5.4 · Figuras 5.18 e 5.19",
        "quem": "Victor → Bruno",
        "dur_s": 70,
        "reserva": "Slide Oculto 28",
        "msg": "Na Barra 7 trifásica, a sintonia decide o sincronismo: com a nominal o erro volta em 98 ms; com a inadequada sofre escorregamento de ciclo (±180°) e a usina absorve potência ativa em 66,8% do pós-falta.",
        "pontos": [
            ("Victor", "Passo 1 (Nominal em azul na B7 trifásica) e Passo 2 (Seta → Inadequada em laranja): no Passo 1, mesmo com retenção de 9,2% de v_d, a sintonia nominal recupera a faixa de 2° em 98 ms. No Passo 2, com a sintonia inadequada (retenção similar de 8,2%), o amortecimento efetivo colapsa na falta e o PLL entra em escorregamento de ciclo, varrendo ±180° sem parar até 0,6 s."),
            ("Bruno", "Passo 3 (Seta → Potência ativa P e destaque '66,8%' sob o fasor): o mesmo ganho que filtrava o 120 Hz na Barra 6 perde o sincronismo aqui. Como o referencial gira sem parar em relação à rede (visível no vetor laranja dando voltas no fasor), P = (3/2)·V·i_d·cos(Δθ) inverte de sinal e a usina absorve potência ativa da rede em 66,8% do tempo pós-falta (média de −0,40 pu)."),
        ],
        "falas": [
            ("Victor", "O Capítulo 6 responde a essa pergunta com o resultado central do trabalho, nas Figuras 5.18 e 5.19 do TCC: a falta trifásica na Barra 7. No passo 1, com a sintonia nominal em azul, mesmo sob um afundamento severo que retém apenas 9,2% da tensão, o PLL recupera o sincronismo em 98 milissegundos após a eliminação da falta. (Seta →) No passo 2, para a mesma falta com a sintonia inadequada em laranja, a tensão retém quase o mesmo, 8,2%, mas o laço lento e subamortecido não consegue retravar: o erro varre continuamente a faixa de mais a menos 180 graus em escorregamento de ciclo até o fim da simulação."),
            ("Bruno", "(Seta →) E no passo 3 vemos a consequência física no gráfico inferior da potência ativa e no fasor à direita: o mesmo ganho menor que parecia vantajoso na Barra 6 é o que provoca o colapso de sincronismo na Barra 7. A malha de corrente não falhou, mas como o referencial estimado pelo PLL gira continuamente em relação à rede, o cosseno do erro angular troca de sinal e o inversor passa a se comportar como uma carga oscilante, absorvendo potência ativa da rede em 66,8% do tempo pós-falta, com média de menos 0,40 por unidade. (Seta → para o Cap. 7)"),
        ],
        "atencao": "Se quiser, clicar em '▶ play' sob o fasor no Passo 3 para mostrar o vetor azul travado no topo e o laranja girando sem parar.",
    },
    {
        "tipo": "PAINEL",
        "num": 7,
        "titulo": "Código de rede: permanência e corrente reativa (NOVO: 5 Passos)",
        "bloco": "Painel HTML · Cap. 7/8 · 5 passos",
        "tcc": "§5.5 · Figuras 2.1 e 2.2 · Tabela 5.2",
        "quem": "Bruno → Victor",
        "dur_s": 70,
        "reserva": "Slide Oculto 29",
        "msg": "O inversor cumpre a letra do Submódulo 2.10 nas trifásicas, mas permanecer conectado não basta sem rastreamento angular.",
        "pontos": [
            ("Bruno", "Passo 1 (Curva LVRT da Fig. 2.1 à esquerda e Rampa de i_q da Fig. 2.2 à direita): apresentar os dois requisitos simultâneos do Submódulo 2.10: permanecer conectado na região de suportabilidade e injetar corrente reativa conforme o afundamento."),
            ("Bruno", "Passo 2 (Seta → Barra 7 e Linha 7-8 + destaque '0,09 pu' na rampa): na B7 (0,10 pu) e L7-8 (0,11 pu) a tensão cai abaixo de 0,2 pu, onde a desconexão seria permitida, mas o inversor permanece conectado com i_q saturado em 1,00 pu; contudo, como Q ≈ V·i_q e a tensão caiu abaixo de 10%, a corrente máxima entrega apenas 0,09 pu de potência reativa."),
            ("Victor", "Passo 3 (Seta → Linha 8-9 e Barra 6 na rampa), Passo 4 (Seta → Acendem as assimétricas e a perda de sincronismo) e Passo 5 (Seta → Cartão de fecho): no Passo 3, mais longe da falta a injeção segue a rampa (0,72 pu contra 0,76 pu na Barra 6) e entrega muito mais reativo porque há tensão. No Passo 4, nas assimétricas e na perda de sincronismo o inversor também permanece conectado, mas injeta potência com 120 Hz ou drena energia da rede. No Passo 5, o cartão de fecho crava a tese: perguntar apenas 'O inversor permaneceu conectado?' é insuficiente."),
        ],
        "falas": [
            ("Bruno", "No Capítulo 7 confrontamos os resultados com os requisitos do Submódulo 2.10 do ONS. No passo 1 vemos os dois painéis: à esquerda a curva de suportabilidade de tensão da Figura 2.1 e à direita a rampa de injeção de corrente reativa da Figura 2.2. (Seta →) No passo 2 entram os casos mais próximos, Barra 7 e Linha 7-8: a tensão cai abaixo de 0,2 por unidade, onde a desconexão já seria permitida pela norma, e mesmo assim o inversor permanece conectado e satura a corrente reativa iq em 1 por unidade. Porém, aparece aqui um dilema físico fundamental: como a potência reativa é o produto da tensão pela corrente e a tensão caiu abaixo de 10%, mesmo injetando 100% de corrente o inversor entrega apenas 0,09 por unidade de potência reativa à rede."),
            ("Victor", "(Seta →) No passo 3 entram a Linha 8-9 e a Barra 6: mais longe do defeito, a corrente reativa acompanha a rampa, com 0,72 contra 0,76 por unidade na Barra 6, e como há mais tensão o suporte de reativo entregue é muito mais efetivo. (Seta →) No passo 4 acendemos todos os demais cenários: tanto nas faltas assimétricas quanto na perda de sincronismo o inversor também permanece conectado o tempo todo, cumprindo a exigência de permanência, mas entrega potência contaminada por 120 hertz ou drena potência ativa da rede. (Seta →) Isso leva ao cartão de fecho no passo 5: perguntar apenas se o inversor permaneceu conectado é insuficiente para caracterizar conformidade; é indispensável auditar a qualidade do rastreamento angular durante toda a contingência e na recuperação. (Seta → para o Cap. 8)"),
        ],
        "atencao": "Atenção à atualização do HTML final: o Capítulo 7 agora tem 5 passos (o destaque de '0,09 pu' já aparece junto com a B7 e L7-8 no Passo 2, e o cartão de fecho é o Passo 5).",
    },
    {
        "tipo": "PAINEL",
        "num": 8,
        "titulo": "Todos os casos do TCC (Tabelas 5.1, 5.2 e 5.3)",
        "bloco": "Painel HTML · Cap. 8/8 · Tabela Síntese",
        "tcc": "Tabelas 5.1 a 5.3 completas",
        "quem": "Victor",
        "dur_s": 25,
        "reserva": "Slide 23 (Apêndice)",
        "msg": "Não é para ler linha por linha: consolida todos os indicadores das Tabelas 5.1 a 5.3 e serve de ponto de apoio interativo para as perguntas da banca.",
        "pontos": [
            ("Victor", "Mostrar rapidamente que a tabela reúne todos os cenários do Capítulo 5 nas duas sintonias (clicar em qualquer linha abre os gráficos completos do caso nas abas) e retornar ao PowerPoint (apertar `Esc` e `Alt+Tab` para o Slide 20)."),
        ],
        "falas": [
            ("Victor", "Por fim, o Capítulo 8 consolida em uma única tabela interativa todos os indicadores das Tabelas 5.1, 5.2 e 5.3 do TCC, onde qualquer linha pode ser clicada durante a arguição para abrir as curvas completas do cenário. Saímos agora da tela cheia e voltamos ao PowerPoint para os dois slides finais de conclusão. (Pressiona Esc e Alt+Tab para o Slide 20)."),
        ],
        "atencao": "Ação prática: apertar Esc (sai da tela cheia) e Alt+Tab de volta para o PowerPoint no Slide 20.",
    },
]

SLIDES_CONCLUSAO = [
    # -------------------------------------------------------------------------
    # PARTE IV: SLIDES 20 E 21 (CONCLUSÃO E ENCERRAMENTO)
    # -------------------------------------------------------------------------
    {
        "tipo": "SLIDE",
        "num": 20,
        "titulo": "Síntese dos resultados (Conclusão)",
        "bloco": "Conclusão",
        "tcc": "Cap. 6",
        "quem": "Bruno → Victor → Bruno → Victor",
        "dur_s": 70,
        "msg": "O sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico.",
        "pontos": [
            ("Bruno", "Cartão 1 ('1. Faltas simétricas'): com a sintonia nominal, o SRF-PLL preserva o sincronismo e reconverge em todos os pontos; a severidade do afundamento depende diretamente da distância elétrica até a usina."),
            ("Victor", "Cartão 2 ('2. Faltas assimétricas'): a fragilidade do SRF-PLL é estrutural — a componente de sequência negativa introduz oscilação de 120 Hz que o controlador PI não rejeita, contaminando as potências injetadas P e Q."),
            ("Bruno", "Cartão 3 ('3. Sensibilidade de ganhos'): reduzir os ganhos atenua a falta moderada, mas retarda o restabelecimento e leva ao escorregamento de ciclo na Barra 7, fazendo o inversor drenar potência ativa da rede."),
            ("Victor", "Caixa de rodapé ('Qual é a conclusão central da defesa?'): permanecer conectado é insuficiente para garantir a estabilidade; a conformidade regulatória deve auditar o erro angular dinâmico durante a falta e em toda a recomposição da rede."),
        ],
        "falas": [
            ("Bruno", "De volta aos slides para sintetizar nossas conclusões nos três pontos principais de apoio. Primeiro, nas faltas simétricas: com a sintonia nominal, o SRF-PLL preserva a estabilidade e reconverge em todos os pontos da rede, sendo a severidade do afundamento ditada diretamente pela distância elétrica até a usina."),
            ("Victor", "Segundo, nas faltas assimétricas: demonstramos que a fragilidade do SRF-PLL clássico é estrutural, pois a componente de sequência negativa introduz uma oscilação de 120 hertz que o controlador PI não consegue rejeitar, contaminando diretamente as potências ativa e reativa injetadas."),
            ("Bruno", "Terceiro, na sensibilidade de ganhos: reduzir os ganhos do PI atenua a oscilação durante faltas distantes, mas retarda o restabelecimento pós-falta e leva à perda de sincronismo por escorregamento de ciclo na falta severa da Barra 7, fazendo o inversor drenar potência ativa da rede."),
            ("Victor", "Por tudo isso, nossa conclusão central no rodapé é que o sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico: permanecer conectado não basta; a verificação de conformidade precisa auditar o erro angular dinâmico durante a falta e em toda a recomposição da rede."),
        ],
        "atencao": "Slide 20 atualizado: foco 100% nos 3 pontos conceituais dos cartões (sem números isolados no topo).",
    },
    {
        "tipo": "SLIDE",
        "num": 21,
        "titulo": "Trabalhos futuros e encerramento",
        "bloco": "Conclusão",
        "tcc": "Cap. 7",
        "quem": "Victor → Bruno → Victor",
        "dur_s": 60,
        "msg": "Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho.",
        "pontos": [
            ("Victor", "Caixa inferior ('Limites do estudo', dizer com naturalidade e transparência): resultados obtidos no sistema IEEE 9 barras com nível fixo de curto-circuito, duas sintonias contrastantes e janela de simulação de 200 ms pós-falta — o estudo descreve um mecanismo físico-dinâmico rigoroso, não um envelope universal de projeto."),
            ("Bruno", "Cartões 1 e 2 ('Trabalhos futuros'): (1) implementar novas estruturas de sincronismo como DDSRF-PLL e DSOGI-PLL, que desacoplam as componentes de sequência positiva e negativa antes do laço PI para rejeitar o 120 Hz sem reduzir a banda passante; (2) varrer a relação de curto-circuito (SCR / impedância de Thévenin) para mapear a fronteira crítica de perda de sincronismo e investigar múltiplos inversores interagindo em redes fracas."),
            ("Victor", "Cartão azul à direita ('Obrigado!'): agradecer novamente aos orientadores Prof. Oscar e Prof. André, aos membros da banca e à UERJ, colocando-se à disposição para a arguição com o painel interativo aberto."),
        ],
        "falas": [
            ("Victor", "Para encerrar, registramos com transparência os limites metodológicos deste trabalho: analisamos o sistema IEEE 9 barras com nível de curto-circuito fixo, duas sintonias contrastantes e janela de observação de 200 milissegundos pós-falta; portanto, nossos resultados caracterizam um mecanismo físico-dinâmico e não um envelope universal de projeto."),
            ("Bruno", "A partir desses limites, dois eixos dão continuidade direta à pesquisa: o primeiro é implementar estruturas avançadas de sincronismo, como o DDSRF-PLL e o DSOGI-PLL, capazes de separar as componentes de sequência antes do filtro PI para rejeitar a oscilação de 120 hertz preservando a largura de banda e a rapidez de recomposição; o segundo é varrer a relação de curto-circuito da rede para mapear a fronteira crítica de perda de sincronismo e investigar a interação entre múltiplos inversores em redes fracas."),
            ("Victor", "Agradecemos mais uma vez aos nossos orientadores, professor Oscar e professor André, aos membros da banca pela leitura cuidadosa e à UERJ. Muito obrigado, e estamos à disposição para as perguntas da banca."),
        ],
        "atencao": "Não propor salto de fase nem RoCoF como trabalhos futuros (foram descartados). Deixar o painel interativo pronto para abrir no botão da tela durante as perguntas.",
    },
]

APENDICE_E_RESERVA = [
    (22, "Apêndice 1", "Defesa Técnica 1: Rede, Filtro LCL e Controle", "Cap. 3 e 4",
     "Acionar se a banca perguntar valores construtivos internos: V_cc = 136,36 kV (1,5 × 90,91 kV para evitar sobremodulação PWM), R_th = 10,04 mΩ, L_th = 1,16 mH, passos Ts = 5 μs (elétrico) e Tsc = 200 μs (controle), L_1 = 30,42 mH, L_2 = 0,289 mH, C_f = 42,47 μF e ganhos da malha de corrente (Kp,i = 14,74 e Ki,i = 3.537,8, aplicados ÷4 no Simulink).",
     "[Bruno] Neste slide de apêndice reunimos todas as especificações elétricas da rede IEEE 9 barras, do equivalente de Thévenin, dos elementos individuais do filtro LCL e da sintonia analítica das malhas de corrente e do SRF-PLL."),
    (23, "Apêndice 2", "Defesa Técnica 2: Tabelas 5.1, 5.2 e 5.3 Completas", "Cap. 5",
     "Acionar se a banca quiser ver todas as métricas numéricas em formato estático de slide (equivale ao Capítulo 8 do painel HTML).",
     "[Victor] Este slide consolida integralmente as Tabelas 5.1, 5.2 e 5.3 do Capítulo 5, permitindo comparar lado a lado as faltas trifásicas com suporte LVRT do ONS e as faltas assimétricas nas duas sintonias."),
    (24, "Reserva Cap. 2", "Na energização, o PLL inadequado leva cerca do dobro do tempo para travar", "Fig. 5.3",
     "Reserva estática do Capítulo 2 do painel HTML (34/40 ms nominal vs. 42/79 ms inadequada).",
     "[Victor] (Reserva do Cap. 2) Na energização sem falta, a sintonia nominal acomoda vd em 34 ms e o erro em 2° em 40 ms; a inadequada leva 42 ms e 79 ms, mas ambas operam travadas antes da falta."),
    (25, "Reserva Cap. 3", "Quanto mais perto da usina, mais severa a falta trifásica, mas o PLL nominal reconverge", "Fig. 5.7, Tab. 5.1",
     "Reserva estática do Capítulo 3 do painel HTML (retenção de 9,2% a 58,4%, pico de 37,3° a 7,3°, retorno de 76 a 112 ms).",
     "[Bruno] (Reserva do Cap. 3) Nas faltas trifásicas com sintonia nominal, a retenção de vd vai de 9,2% na Barra 7 a 58,4% na Barra 6, mas sem sequência negativa o PLL reconverge em todos os casos em até 112 ms."),
    (26, "Reserva Cap. 4", "Faltas assimétricas expõem a fragilidade estrutural do SRF-PLL", "Figs. 5.10 e 5.18",
     "Reserva estática do Capítulo 4 do painel HTML (120 Hz entre 0,29 e 0,72 pu, > 250× maior que nas trifásicas).",
     "[Victor] (Reserva do Cap. 4) Nas faltas assimétricas, a sequência negativa gera oscilação de 120 Hz em dq entre 0,29 e 0,72 pu, mais de 250 vezes maior que nas trifásicas, contaminando o ângulo pois 754 rad/s é apenas 2,32 vezes ωn."),
    (27, "Reserva Cap. 5", "Ganhos menores: compromisso entre filtragem na falta e lentidão na recuperação", "Fig. 5.14, Tab. 5.3",
     "Reserva estática do Capítulo 5 do painel HTML (B6 bifásica cai de 96,0° para 34,5°, mas retorno na B7 dobra de ~50 para ~96 ms).",
     "[Bruno] (Reserva do Cap. 5) Reduzir os ganhos atenua o pico do erro na Barra 6 bifásica de 96,0° para 34,5°, mas na Barra 7 quase dobra o tempo de retorno pós-falta, preparando a perda de sincronismo."),
    (28, "Reserva Cap. 6", "Dinâmica pós-falta: sob sintonia inadequada, o inversor absorve P em 66,8% do tempo", "Figs. 5.20 e 5.21",
     "Reserva estática do Capítulo 6 do painel HTML (escorregamento de ciclo na B7 trifásica, absorção ativa em 66,8% do pós-falta, média −0,40 pu).",
     "[Bruno] (Reserva do Cap. 6) Sob falta trifásica na Barra 7 com sintonia inadequada, o escorregamento de ciclo faz o inversor absorver potência ativa em 66,8% do pós-falta, com média de −0,40 pu."),
    (29, "Reserva Cap. 7", "Cumprir o Submódulo 2.10 do ONS exige mais do que permanecer conectado", "Fig. 2.2, Tab. 5.2",
     "Reserva estática do Capítulo 7 do painel HTML (Iq = 1,00 pu na B7 entrega só Q = 0,09 pu porque V = 0,10 pu).",
     "[Victor] (Reserva do Cap. 7) Nas trifásicas o inversor cumpre a rampa do Submódulo 2.10, mas na Barra 7 a corrente máxima entrega apenas 0,09 pu de reativo devido à tensão de 0,10 pu, provando que permanecer conectado não basta."),
]


# ==============================================================================
# CONSTRUÇÃO DO DOCUMENTO WORD
# ==============================================================================

def add_styled_box(doc, title: str, bg_hex: str, border_hex: str, title_color: RGBColor, items: list):
    """Cria uma caixa com borda esquerda grossa e conteúdo estruturado."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    set_cell_bg(cell, bg_hex)
    set_cell_margins(cell, top=90, bottom=90, left=160, right=140)
    set_cell_borders(
        cell,
        left=("single", 24, border_hex),
        top=("single", 4, HEX_BORDER),
        bottom=("single", 4, HEX_BORDER),
        right=("single", 4, HEX_BORDER),
    )
    prevent_row_split(tbl.rows[0])

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(title)
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(9.5)
    r0.font.color.rgb = title_color

    for item in items:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if isinstance(item, str):
            r = p.add_run(item)
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.font.color.rgb = C_INK
        elif isinstance(item, tuple) and len(item) == 2:
            speaker, text = item
            r_sp = p.add_run(f"• {speaker}: ")
            r_sp.bold = True
            r_sp.font.name = "Calibri"
            r_sp.font.size = Pt(10)
            r_sp.font.color.rgb = C_BRUNO if "Bruno" in speaker else (C_VICTOR if "Victor" in speaker else C_NAVY)
            r_tx = p.add_run(text)
            r_tx.font.name = "Calibri"
            r_tx.font.size = Pt(10)
            r_tx.font.color.rgb = C_INK
        elif isinstance(item, tuple) and len(item) == 3:
            speaker, text, w_info = item
            paras = [p_it.strip() for p_it in text.split("\n\n") if p_it.strip()]
            for p_idx, p_txt in enumerate(paras):
                p_elem = p if p_idx == 0 else cell.add_paragraph()
                if p_idx > 0:
                    p_elem.paragraph_format.space_before = Pt(2)
                    p_elem.paragraph_format.space_after = Pt(3)
                    p_elem.paragraph_format.line_spacing = 1.15
                if p_idx == 0:
                    r_sp = p_elem.add_run(f"[{speaker}] ")
                    r_sp.bold = True
                    r_sp.font.name = "Calibri"
                    r_sp.font.size = Pt(10.5)
                    r_sp.font.color.rgb = C_BRUNO if "Bruno" in speaker else C_VICTOR
                r_tx = p_elem.add_run(f"“{p_txt}”" if len(paras) == 1 else p_txt)
                r_tx.font.name = "Calibri"
                r_tx.font.size = Pt(10.5)
                r_tx.font.color.rgb = C_INK
                if p_idx == len(paras) - 1:
                    r_w = p_elem.add_run(f"   {w_info}")
                    r_w.font.name = "Calibri"
                    r_w.font.size = Pt(8.5)
                    r_w.font.color.rgb = C_MUTED

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(3)


def add_item_section(doc, item: dict, clock_start: int, clock_end: int):
    """Renderiza um Slide ou Capítulo do Painel com cabeçalho, pontos principais e falas."""
    is_palco = item["tipo"] == "PAINEL"
    badge_bg = HEX_PANEL if is_palco else HEX_NAVY
    badge_label = f"PAINEL CAP. {item['num']}" if is_palco else f"SLIDE {item['num']:02d}"

    total_words = sum(count_words(t) for _, t in item["falas"])
    read_s = int(round(total_words / 130.0 * 60))

    # 1. Faixa de cabeçalho
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c0, c1 = tbl.rows[0].cells
    c0.width = Cm(3.2)
    c1.width = Cm(13.8)
    set_cell_bg(c0, badge_bg)
    set_cell_bg(c1, HEX_SUB)
    set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
    set_cell_margins(c1, top=80, bottom=80, left=140, right=120)
    set_cell_borders(c0)
    set_cell_borders(c1, top=("single", 4, HEX_BORDER), bottom=("single", 4, HEX_BORDER), right=("single", 4, HEX_BORDER))
    c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    prevent_row_split(tbl.rows[0])

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    r_b = p0.add_run(badge_label)
    r_b.bold = True
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(11)
    r_b.font.color.rgb = C_WHITE

    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    r_t = p1.add_run(item["titulo"])
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = C_NAVY

    p2 = c1.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    meta_str = (
        f"{item['bloco']}   |   Oradores: {item['quem']}   |   "
        f"{total_words} palavras (~{fmt_dur(read_s)} leitura / Alvo: {fmt_dur(item['dur_s'])})   |   "
        f"Relógio: {fmt_mmss(clock_start)} → {fmt_mmss(clock_end)}"
    )
    if is_palco and item.get("reserva"):
        meta_str += f"   |   Reserva: {item['reserva']}"
    r_m = p2.add_run(meta_str)
    r_m.font.name = "Calibri"
    r_m.font.size = Pt(8.5)
    r_m.font.color.rgb = C_MUTED

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(2)

    # 2. Caixa combinada: Mensagem Central + Pontos Principais a Comentar
    pts_items = [("Mensagem-chave", item["msg"])] + item["pontos"]
    add_styled_box(
        doc,
        "PONTOS PRINCIPAIS A COMENTAR (O QUE EXPLICAR E APONTAR NA TELA)",
        HEX_PTS_BG,
        HEX_PTS_BD,
        C_ORANGE,
        pts_items,
    )

    # 3. Caixa de Falas Cronometradas
    fala_items = []
    for speaker, text in item["falas"]:
        w = count_words(text)
        s = int(round(w / 130.0 * 60))
        fala_items.append((speaker, text, f"({w} pal. · ~{s}s)"))

    add_styled_box(
        doc,
        "FALA SUGERIDA CRONOMETRADA (ENSAIO PASSO A PASSO)",
        HEX_PALCO_BG if is_palco else HEX_FALA_BG,
        HEX_PALCO_BD if is_palco else HEX_FALA_BD,
        C_VICTOR if is_palco else C_BLUE,
        fala_items,
    )

    # 4. Linha rápida de atenção/ponte
    if item.get("atencao"):
        pa = doc.add_paragraph()
        pa.paragraph_format.space_before = Pt(0)
        pa.paragraph_format.space_after = Pt(8)
        ra1 = pa.add_run("⚡ Atenção / Transição: ")
        ra1.bold = True
        ra1.font.name = "Calibri"
        ra1.font.size = Pt(9)
        ra1.font.color.rgb = C_ORANGE
        ra2 = pa.add_run(item["atencao"])
        ra2.font.name = "Calibri"
        ra2.font.size = Pt(9)
        ra2.font.color.rgb = C_MUTED


def add_part_banner(doc, title: str, subtitle: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.color.rgb = C_NAVY

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.keep_with_next = True
    r2 = p2.add_run(subtitle)
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_MUTED


def build_document():
    doc = docx.Document()

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
        "Sincronizado com o Deck Final (29 slides: 1–21 Corpo + 22–29 Apêndice/Reserva), "
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

    # ==========================================================================
    # ROTEIRO DETALHADO ITEM A ITEM
    # ==========================================================================
    idx_global = 0

    add_part_banner(
        doc,
        "PARTE I · PowerPoint: Abertura, Motivação, Modelagem e Método (Slides 1 a 18)",
        "Relógio: 00:00 → 17:15 (17 min 15 s) · Bloco 1 (Slides 1 a 4) conduzido integralmente pelo Bruno; slides 5 a 18 alternados entre Victor e Bruno.",
    )
    for it in SLIDES_ROTEIRO[:18]:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    add_part_banner(
        doc,
        "PARTE II · A Passagem para o Painel Interativo (Slide 19)",
        "Relógio: 17:15 → 17:35 (20 s) · Transição via Alt+Tab para o navegador no Modo Apresentação.",
    )
    for it in SLIDES_ROTEIRO[18:]:
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
        "PARTE IV · Retorno ao PowerPoint: Conclusão e Encerramento (Slides 20 e 21)",
        "Relógio: 25:35 → 27:45 (2 min 10 s + margem até 30:00) · Fechamento nos 3 pontos principais de apoio à conclusão.",
    )
    for it in SLIDES_CONCLUSAO:
        c_start, c_end = item_clocks[idx_global]
        idx_global += 1
        add_item_section(doc, it, c_start, c_end)

    # ==========================================================================
    # PARTE V: APÊNDICE E SLIDES OCULTOS DE RESERVA (22 A 29)
    # ==========================================================================
    add_part_banner(
        doc,
        "PARTE V · Apêndice (Slides 22–23) e Reserva Oculta do Painel (Slides 24–29)",
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

    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    saved_path = OUT_LOCAL
    try:
        doc.save(str(OUT_LOCAL))
        print(f"[OK] Roteiro de Falas e Tempo salvo em: {OUT_LOCAL} ({OUT_LOCAL.stat().st_size:,} bytes)")
    except PermissionError:
        alt_path = OUT_LOCAL.with_name("Roteiro_Falas_e_Tempo_Defesa_TCC_atualizado.docx")
        doc.save(str(alt_path))
        saved_path = alt_path
        print(f"[OK] Salvo em: {alt_path} ({alt_path.stat().st_size:,} bytes)")

    try:
        shutil.copy2(str(saved_path), str(OUT_ONEDRIVE))
        print(f"[OK] Cópia salva no OneDrive: {OUT_ONEDRIVE}")
    except Exception as e:
        alt_one = OUT_ONEDRIVE.with_name("Roteiro_Falas_e_Tempo_Defesa_TCC_atualizado.docx")
        try:
            shutil.copy2(str(saved_path), str(alt_one))
            print(f"[OK] Cópia atualizada salva no OneDrive (com sufixo): {alt_one}")
        except Exception as e2:
            print(f"[AVISO] Não foi possível copiar para o OneDrive ({e} / {e2})")


if __name__ == "__main__":
    build_document()

