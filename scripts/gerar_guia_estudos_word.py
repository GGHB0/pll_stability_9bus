# -*- coding: utf-8 -*-
"""
Gera o Guia Final de Estudos e Roteiro de Fala da Defesa em Word (.docx):
  - output/Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx
  - OneDrive/.../Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx

Totalmente integrado e adaptado ao roteiro feito pelo Victor (gen_roteiro_estudo_defesa.py)
e à versão mais recente do painel HTML (output/pll_metrics.html — Modo Apresentação em 8 capítulos):
  1. Segue o percurso real da defesa:
     - PARTE I: PowerPoint, Slides 1 a 19 (Abertura, Motivação, Modelagem e Método)
     - PARTE II: PowerPoint, Slide 20 (Porta para o painel -> Alt+Tab -> Modo apresentação)
     - PARTE III: Painel HTML, Modo Apresentação (Capítulos 1 a 8 do palco, passo a passo)
     - PARTE IV: PowerPoint, Slides 21 e 22 (Síntese dos resultados, Trabalhos futuros e Encerramento)
     - PARTE V: Conteúdo adicional (Apêndice Slides 23-24, Slides ocultos de reserva 25-30,
       Perguntas da Banca do defesa_qa.pdf e Folha de Números)
  2. Inclui TODAS as miniaturas dos slides, os prints dos 8 capítulos do palco (1920x1080),
     as figuras recortadas do RAP-ONS 00012/2023 e todas as equações renderizadas via matplotlib STIX.
  3. Inclui todas as caixas do roteiro do Victor (Mensagem, O que falar, Passos do capítulo,
     Fundamentos, Números, Pergunta do rodapé, Pergunta provável da banca, Cuidado, Além do TCC, Próximo).
  4. Adiciona em cada slide (1-22) e em cada capítulo do palco (1-8) o ROTEIRO DE FALA COMPLETO
     CRONOMETRADO ([Bruno] e [Victor]) calibrado para 30 minutos (130 ppm), além do Mapa Sequencial
     do TCC (Capítulos 1 a 7).
"""
import html
import io
import re
import shutil
from pathlib import Path
from PIL import Image as PILImage
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "notas"))
from pdfnote import _mathtext_image  # noqa: E402

PPTX_STAGED = Path(r"C:\Temp\defesa_final_revisao\final.pptx")
PPTX_CANON = Path(r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\Defesa_TCC_SRF-PLL.pptx")
OUT_LOCAL = ROOT / "output" / "Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx"
OUT_ONEDRIVE = Path(r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx")

# Paleta de cores do documento Word
C_INK = RGBColor(0x14, 0x23, 0x2E)
C_ACCENT = RGBColor(0x1A, 0x4A, 0x6E)
C_BRUNO = RGBColor(0x1E, 0x3A, 0x8A)
C_VICTOR = RGBColor(0x0F, 0x76, 0x6E)
C_MUTED = RGBColor(0x5A, 0x6B, 0x78)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# Estilo das caixas do roteiro do Victor
KIND_STYLE = {
    "msg":     ("#E7EFF6", "1A4A6E", RGBColor(0x1A, 0x4A, 0x6E), "MENSAGEM"),
    "banca":   ("#EDF4FB", "2F6FA8", RGBColor(0x2F, 0x6F, 0xA8), "PERGUNTA DO RODAPÉ DO SLIDE"),
    "prova":   ("#F3EEF8", "6B4C9A", RGBColor(0x6B, 0x4C, 0x9A), "PERGUNTA PROVÁVEL DA BANCA"),
    "cuidado": ("#FDF3E1", "C27C0E", RGBColor(0xC2, 0x7C, 0x0E), "CUIDADO"),
    "alem":    ("#EAF4EC", "3D8A57", RGBColor(0x3D, 0x8A, 0x57), "ALÉM DO TCC · para entender e responder, não para a fala"),
    "passo":   ("#F4F7F9", "5A6B78", RGBColor(0x5A, 0x6B, 0x78), "PASSOS DO CAPÍTULO"),
    "fala":    ("#FBF6EC", "8A6D3B", RGBColor(0x8A, 0x6D, 0x3B), "O QUE FALAR · tópicos para dizer com as suas palavras"),
    "script":  ("#EFF6FF", "1E3A8A", RGBColor(0x1E, 0x3A, 0x8A), "ROTEIRO DE FALA COMPLETO (30 MINUTOS) · [Bruno] e [Victor]"),
    "palco_s": ("#F0FDFA", "0F766E", RGBColor(0x0F, 0x76, 0x6E), "ROTEIRO DE FALA PASSO A PASSO NO PALCO · [Bruno] e [Victor]"),
}


# ==============================================================================
# FALAS COMPLETAS REVISADAS E CALIBRADAS PARA 30 MINUTOS (SLIDES + PALCO 1 A 8)
# Seguindo todas as convenções do roteiro do Victor (sem sigla proibida, sem BAD_PLL,
# "escorregamento de ciclo", "retenção de Vd", sem puxar "sobrecorrentes" no slide 4)
# ==============================================================================
SLIDE_SPEECHES = {
    1: (
        "[Bruno] Bom dia a todos. Eu sou o Bruno, e este é o Victor. Hoje apresentamos o nosso "
        "trabalho de conclusão de curso, sobre o comportamento do SRF-PLL de inversores frente a "
        "contingências em sistemas elétricos.\n\n"
        "[Victor] Vamos percorrer cinco blocos: o contexto global, a fundamentação e a modelagem, "
        "a metodologia de simulação, os resultados no painel interativo e, por fim, as conclusões. "
        "Ao longo da apresentação, vocês vão ver destacadas as justificativas para as principais "
        "escolhas do trabalho.\n\n"
        "[Bruno] Agradecemos ao professor Oscar, nosso orientador, ao professor André, coorientador, "
        "e à banca por estarem aqui. Vamos começar pelo contexto que motivou este estudo."
    ),
    2: (
        "[Bruno] Começamos pelo cenário global da transição energética. Em 2025, a geração "
        "fotovoltaica cresceu cerca de 600 TWh, o maior aumento anual já registrado para qualquer "
        "fonte, respondendo sozinha por aproximadamente 70% de todo o incremento da geração "
        "elétrica mundial. As adições de capacidade renovável somaram 800 GW, o vigésimo terceiro "
        "recorde anual consecutivo.\n\n"
        "[Victor] No gráfico, a participação conjunta de solar e eólica saltou de cerca de 5% há "
        "uma década para 17% em 2025 no mundo, aproximando-se de 30% na União Europeia e alcançando "
        "35% no Brasil com a MMGD. Em capacidade instalada, são 96,8 GW segundo o ONS, um salto de "
        "279% desde 2020 que já supera a própria carga média nacional de 85,8 GW médios. Toda essa "
        "potência chega por inversores e transfere a sustentação da rede das massas girantes para "
        "os algoritmos de controle."
    ),
    3: (
        "[Victor] E essa vulnerabilidade já se provou em eventos reais de grande porte. No Brasil, "
        "em 15 de agosto de 2023, a abertura acidental de uma linha de 500 kV pela proteção "
        "provocou um afundamento de tensão no Nordeste, desligamentos em cascata e a perda de "
        "23.368 MW, 34,5% da demanda nacional.\n\n"
        "[Bruno] O diagnóstico do relatório do ONS é o grande motivador do nosso estudo: o operador "
        "descartou falta de inércia, já que o SIN tinha cerca de 265 GW·s, e descartou potência de "
        "curto-circuito. Foi um colapso de tensão, agravado porque o suporte dinâmico de reativos "
        "das usinas eólicas e fotovoltaicas em campo ficou muito aquém dos modelos matemáticos.\n\n"
        "[Victor] O mesmo padrão repetiu-se em 2025. Na Península Ibérica, em abril, o apagão foi "
        "precedido por uma oscilação de 0,63 Hz classificada pela ENTSO-E como instabilidade guiada "
        "por conversores: usinas operavam em fator de potência fixo, sem suporte dinâmico de tensão, "
        "e mais de 2,5 GW desconectaram-se por sobretensão.\n\n"
        "[Bruno] E no Chile, em fevereiro de 2025, um apagão de 11.066 MW atingiu um sistema com "
        "73% de geração solar e eólica. Após a separação em duas ilhas em 1,5 segundo, a ilha norte "
        "colapsou por instabilidade de tensão devido à ausência de controle dinâmico de reativos nas "
        "renováveis. Nos três casos, o elo crítico foi a resposta dinâmica do controle dos conversores."
    ),
    4: (
        "[Bruno] Isso nos traz ao problema central do trabalho: o SRF-PLL precisa de uma tensão "
        "limpa e equilibrada no ponto de conexão para orientar o controle do inversor, mas uma "
        "falta na rede destrói justamente essa referência, causando afundamento de amplitude, "
        "salto de fase e assimetria.\n\n"
        "[Victor] No referencial síncrono dq, esse afundamento reduz o ganho do laço e a assimetria "
        "introduz uma oscilação de 120 Hz no eixo q. O PLL responde com erro angular elevado ou "
        "perde o sincronismo.\n\n"
        "[Bruno] Sem o ângulo correto, o desacoplamento entre potências ativa e reativa se perde: "
        "as correntes d e q saem orientadas no lugar errado, comprometendo o suporte de reativos "
        "exigido pelo Submódulo 2.10 do ONS.\n\n"
        "[Victor] Daí o nosso objetivo geral: analisar a dinâmica, a sensibilidade à sintonia e a "
        "robustez do SRF-PLL de um inversor de 100 MW sob contingências no sistema IEEE 9 barras, "
        "comparando a sintonia nominal e a inadequada sob faltas simétricas e assimétricas."
    ),
    5: (
        "[Victor] Começamos pela usina, na Figura 3.2 do TCC. À esquerda, a fonte primária é um "
        "barramento contínuo ideal, sem dinâmica do elo CC e sem rastreamento de máxima potência: "
        "assim, tudo o que se observa na falta vem do lado CA e do sincronismo.\n\n"
        "[Bruno] Seguindo da esquerda para a direita, o inversor converte a tensão contínua em "
        "corrente alternada trifásica, passa pelo filtro LCL e entrega os 100 MW na Barra 2. Como "
        "ele é seguidor de rede, mede a tensão no ponto de acoplamento comum e o SRF-PLL, destacado "
        "em laranja, estima o ângulo que orienta as malhas de corrente."
    ),
    6: (
        "[Victor] Para controlar grandezas senoidais sem erro em regime permanente, usamos a "
        "transformada de Park, na Equação 3.5 do TCC. Um controlador PI comum não zera o erro de "
        "uma senoide, por isso a transformada projeta as três fases em dois eixos ortogonais, d e q, "
        "que giram junto com a rede.\n\n"
        "[Bruno] Como mostram os desenhos à direita, girando na mesma velocidade da rede, as "
        "senoides de 60 Hz viram grandezas constantes em d e q, onde o PI opera com erro nulo. "
        "Mas toda essa transformação depende do ângulo teta: quem estima esse ângulo em tempo real é o PLL."
    ),
    7: (
        "[Victor] A Figura 4.3 do TCC mostra a estrutura do SRF-PLL nos três blocos tracejados. O "
        "primeiro é o detector de fase, a própria transformada de Park aplicada à tensão medida: "
        "com o eixo d alinhado à tensão da rede, toda a amplitude fica em vd e vq vale zero. "
        "Logo, vq mede o próprio erro de ângulo.\n\n"
        "[Bruno] O segundo bloco é o controlador PI, que recebe vq e devolve a correção de "
        "frequência delta ômega; somada aos 60 Hz nominais, ela entra no VCO, um integrador que "
        "devolve o ângulo teta para a transformada de Park e para as malhas de corrente. No cartão "
        "à direita, o laço fechado é de segunda ordem, com Kp igual a 2 xi ômega n e Ki igual a "
        "ômega n ao quadrado."
    ),
    8: (
        "[Victor] O sistema de teste é o IEEE de 9 barras modificado. A máquina síncrona da Barra 2, "
        "que no caso original tinha 192 MVA, foi substituída pela usina fotovoltaica de 100 MW, e a "
        "Barra 2 passa a ser o ponto de conexão do inversor. Os geradores G1 e G3 permanecem como "
        "fontes síncronas, mantendo a inércia remanescente no sistema.\n\n"
        "[Bruno] O sistema base tem três geradores, três transformadores, seis linhas de transmissão "
        "e três cargas, em 230 kV. Os 100 MW da usina correspondem a 1 pu na base de 100 MVA. As "
        "faltas são aplicadas em pontos que variam a distância elétrica até a usina, com o nível de "
        "curto-circuito mantido fixo, uma limitação que retomamos no final.\n\n"
        "[Victor] Usamos duas ferramentas complementares: no PSIM, a rede é reduzida a um equivalente "
        "de Thévenin na Barra 2, obtido da matriz de impedância nodal; no Simulink, roda o sistema completo."
    ),
    9: (
        "[Bruno] Antes de montar o inversor completo, construímos esta bancada inicial no PSIM: "
        "duas fontes trifásicas ideais ligadas pela impedância da rede. Sem chaves e sem filtro LCL, "
        "testamos isolado apenas o laço PD, PI e VCO do PLL.\n\n"
        "[Victor] Essa etapa separa o sincronismo do resto do conversor: verificamos vq indo a zero "
        "e o ângulo estimado travando na rede. Foi nesta bancada que validamos os ganhos do PI "
        "detalhados no próximo slide."
    ),
    10: (
        "[Victor] Na etapa 1 do projeto dos ganhos, a tensão medida entra em pu, dividida pelo pico "
        "nominal de fase de 16.329,93 V. Assim, na condição nominal a amplitude vale 1 pu, o ganho "
        "do detector de fase vale 1 e vq é o próprio erro de ângulo.\n\n"
        "[Bruno] Nas etapas 2 a 4, com o detector linearizado, a malha fechada assume a forma "
        "canônica de segunda ordem: Ki é ômega n ao quadrado e Kp é 2 xi ômega n. Fixamos o "
        "amortecimento xi em 0,707, valor clássico de Ogata com cerca de 5% de sobre-elevação. "
        "Resta um único grau de liberdade: o tempo de acomodação ts.\n\n"
        "[Victor] Na régua à direita, pelo critério de 1%, ts vale 4,6 sobre xi ômega n. Com ts "
        "curto demais, a banda alarga e deixa passar ruído e desequilíbrio; longo demais, não "
        "acompanha variações da rede. Adotamos 20 ms, pouco mais de um ciclo, seguindo Alves, Dias "
        "e Rolim, de 2020, e Teodorescu, Liserre e Rodriguez, de 2011. Daí saem Kp igual a 460, "
        "ômega n igual a 325,3 rad/s, ou 51,8 Hz, e Ki igual a 105.820."
    ),
    11: (
        "[Bruno] Essa é a sintonia nominal. Na coluna laranja, para a sintonia inadequada, reduzimos "
        "os dois ganhos em 80%, multiplicando por 0,2: Kp cai para 92 e Ki para 21.164. A frequência "
        "natural cai para 145,5 rad/s e o amortecimento para 0,316: uma malha mais lenta e menos "
        "amortecida. No caso-limite, o PLL deixa de recuperar o sincronismo depois que a falta é eliminada.\n\n"
        "[Victor] No cartão à direita está a ponte para os resultados: sob falta assimétrica, a "
        "sequência negativa produz em vq uma oscilação de 120 Hz, ou 754 rad/s, que fica a apenas "
        "2,32 vezes a frequência natural do laço. O PI não a atenua de forma significativa, e ela "
        "passa ao ângulo estimado. É esse mecanismo que investigamos nos resultados."
    ),
    12: (
        "[Victor] Com o sincronismo resolvido, passamos ao inversor. Na primeira versão, montada no "
        "PSIM, pedimos a potência nominal da usina, 1 pu ou 100 MW, num degrau aplicado aos 35 ms, "
        "e reativo zero. Cada potência é dividida pela tensão de eixo direto vd que vem do próprio "
        "SRF-PLL, gerando as referências de corrente id e iq.\n\n"
        "[Bruno] No cartão embaixo à esquerda, essa divisão é a Equação 3.9 do TCC invertida. Ela só "
        "vale com vq igual a zero, quando o eixo d está alinhado com a tensão, e quem garante isso é "
        "o SRF-PLL."
    ),
    13: (
        "[Bruno] Aberta, a malha de corrente é a Figura 3.1 do TCC: em cada eixo, o erro entre a "
        "referência e a corrente medida passa pelo PI e por um filtro notch na ressonância do LCL, "
        "gerando o índice de modulação que o PWM a 5 kHz aplica no inversor de dois níveis.\n\n"
        "[Victor] O filtro LCL ressoa em 9.068,99 rad/s, entre a fundamental e o chaveamento, com "
        "amortecimento de 0,707 e indutância total Lest de 30,71 mH. O PI de corrente segue a mesma "
        "forma canônica do PLL: amortecimento de 0,707 e frequência natural de 4 raiz de 2 vezes a "
        "fundamental, acomodando a corrente em um ciclo da rede. Daí saem Kp igual a 8 fg Lest e Ki "
        "igual a 32 fg ao quadrado Lest. São dois PIs distintos: o do PLL sincroniza, e o de corrente "
        "faz id e iq seguirem a referência."
    ),
    14: (
        "[Bruno] Com a malha de corrente ajustada, trocamos a referência fixa pela lógica do ONS. "
        "O esqueleto é o mesmo do slide 12, mas agora as referências id e iq saem do bloco laranja "
        "do Submódulo 2.10, que lê a tensão no ponto de conexão e recebe a corrente nominal e a "
        "corrente máxima do conversor, como na Figura 4.2 do TCC.\n\n"
        "[Victor] Repare que o SRF-PLL aparece duas vezes no diagrama: ele sai da mesma transformação "
        "que mede a tensão e orienta as correntes na malha. O bloco do ONS decide quanto injetar; "
        "o PLL decide em que direção."
    ),
    15: (
        "[Victor] Por dentro, o bloco faz três coisas. Primeiro, olha a faixa da tensão medida: "
        "abaixo de 0,85 pu, pede corrente reativa pela rampa da Figura 2.2, nula em 0,85 e igual à "
        "nominal em 0,5 pu. Segundo, limita essa corrente ao máximo do conversor.\n\n"
        "[Bruno] Terceiro, aplica a prioridade mostrada no círculo à direita: o eixo d fica só com a "
        "parcela de corrente que o suporte de reativo deixa livre, e por isso a potência ativa cai "
        "durante a falta. Abaixo de 0,5 pu quase nada sobra para o ativo, garantindo o suporte de "
        "tensão sem ultrapassar o limite do equipamento."
    ),
    16: (
        "[Bruno] No código, a mesma lógica vira esta sequência em blocos: dois testes de tensão "
        "escolhem o caminho, e na faixa normal o reativo fica em zero e o eixo d na corrente nominal.\n\n"
        "[Victor] Nos dois caminhos de defeito, primeiro limita-se a corrente reativa e depois "
        "aplica-se a prioridade. Quando a falta é eliminada, a tensão volta à faixa normal, o "
        "reativo adicional zera e a potência ativa retorna ao patamar pré-falta."
    ),
    17: (
        "[Victor] Juntando todas as partes, este é o sistema completo da Figura 4.2 do TCC: em cima, "
        "o inversor de dois níveis, o filtro LCL e o ponto de acoplamento na Barra 2; embaixo, o "
        "controle digital, onde o SRF-PLL entrega o ângulo, o Submódulo 2.10 define as referências e "
        "os PIs de corrente comandam o PWM.\n\n"
        "[Bruno] É esse sistema completo que as contingências no IEEE 9 barras vão testar a partir de agora."
    ),
    18: (
        "[Bruno] Todas as simulações seguem a mesma linha do tempo. Nos primeiros 0,1 s o modelo "
        "inicializa e o PLL trava; esse trecho fica fora das métricas. A falta é aplicada em 0,3 s e "
        "eliminada em 0,4 s, seis ciclos a 60 Hz, e o sistema é observado até 0,6 s, 200 ms após a "
        "eliminação. Essa janela delimita o alcance das nossas conclusões sobre a recuperação.\n\n"
        "[Victor] A matriz mostra onde cada falta foi aplicada. A análise se concentra nas quatro "
        "primeiras colunas em azul: Barra 7, Linha 7-8, Linha 8-9 e Barra 6, da mais próxima à mais "
        "distante da usina. As faltas monofásicas e bifásicas introduzem sequência negativa e impõem "
        "maior esforço ao sincronismo. A sintonia inadequada foi avaliada nas Barras 7 e 6 e na "
        "Linha 7-8, enquanto as demais barras em cinza ficam disponíveis para consulta no painel."
    ),
    19: (
        "[Bruno] Antes de abrir os resultados, veja como eles foram extraídos. Ao fim de cada "
        "simulação, o Simulink exporta os sinais em duas taxas de amostragem; um código em Python "
        "alinha as duas num eixo de tempo comum e calcula os mesmos indicadores para todos os "
        "cenários, sem nenhuma leitura manual no gráfico.\n\n"
        "[Victor] Na tabela estão as cinco métricas: a retenção da tensão de eixo direto em "
        "percentual do pré-falta, que na Barra 7 nominal é de 9,2%; o pico do erro de fase após o "
        "primeiro ciclo; o tempo de retorno à faixa de 2 graus desde a eliminação; a componente de "
        "120 Hz extraída pela transformada de Fourier de vd na janela de 6 ciclos da falta; e as "
        "potências médias.\n\n"
        "[Bruno] Tudo isso alimenta o nosso painel interativo, que vamos abrir agora para percorrer "
        "os resultados."
    ),
    20: (
        "[Victor] A partir deste slide, apresentamos todos os resultados do Capítulo 5 diretamente "
        "no painel interativo em tela cheia, no Modo Apresentação. (Aperta Alt+Tab para o navegador "
        "e clica no botão Modo apresentação no cabeçalho)."
    ),
    21: (
        "[Bruno] De volta aos slides para concluir. No primeiro cartão, sob faltas simétricas, com a "
        "sintonia nominal o SRF-PLL preserva o sincronismo e reconverge em todos os pontos, mesmo "
        "com retenção de vd de apenas 9,2% na Barra 7, sendo a severidade ditada pela distância "
        "elétrica até a usina.\n\n"
        "[Victor] No segundo cartão, sob faltas assimétricas, a sequência negativa expõe uma "
        "fragilidade estrutural do algoritmo: a componente de 120 Hz é mais de 250 vezes maior que "
        "nas trifásicas, o PI não a rejeita e essa oscilação contamina as potências ativa e reativa.\n\n"
        "[Bruno] No terceiro cartão, reduzir os ganhos do PI filtra melhor a falta moderada, mas "
        "retarda a recuperação e, na falta severa da Barra 7, leva à perda de sincronismo por "
        "escorregamento de ciclo, fazendo a usina absorver potência ativa da rede em 66,8% do tempo pós-falta.\n\n"
        "[Victor] Por isso, o sincronismo do SRF-PLL é uma decisão de estabilidade do sistema "
        "elétrico: permanecer conectado não basta; a verificação de conformidade precisa auditar a "
        "qualidade do rastreamento angular durante a falta e em toda a recomposição."
    ),
    22: (
        "[Victor] Como limites deste trabalho, utilizamos o sistema IEEE 9 barras com nível de "
        "curto-circuito fixo, duas sintonias contrastantes e janela de 200 ms pós-falta: ou seja, "
        "o trabalho identifica e explica um mecanismo físico-dinâmico, e não um envelope universal "
        "de projeto.\n\n"
        "[Bruno] A partir desses limites, dois eixos dão continuidade ao estudo no Capítulo 7: "
        "primeiro, avaliar novas estruturas de sincronismo como o DDSRF-PLL e o DSOGI-PLL, que "
        "separam as componentes de sequência positiva e negativa antes do laço PI para eliminar o "
        "120 Hz sem reduzir a banda; segundo, varrer a relação de curto-circuito para mapear a "
        "fronteira de perda de sincronismo e investigar múltiplos inversores em redes fracas.\n\n"
        "[Victor] Encerramos agradecendo novamente ao professor Oscar, ao professor André, aos "
        "membros da banca e à UERJ. Ficamos à disposição para as perguntas, com o painel aberto."
    ),
    23: "[Bruno] Slide de apêndice para a arguição: reúne os parâmetros da rede, do equivalente de Thévenin, do filtro LCL e das malhas de controle.",
    24: "[Victor] Slide de apêndice para a arguição: reúne as Tabelas 5.1, 5.2 e 5.3 completas do Capítulo 5.",
    25: (
        "[Victor] (Reserva do Capítulo 2 do painel) Na energização, com a sintonia nominal, vd "
        "acomoda em 34 ms e o erro de fase entra na faixa de 2 graus em 40 ms. Com a sintonia "
        "inadequada, são 42 ms e 79 ms, quase o dobro do tempo.\n\n"
        "[Bruno] Em regime permanente, porém, as duas chegam ao mesmo ponto de operação antes da "
        "falta em 0,3 s: a sintonia inadequada é lenta, não quebrada, e a diferença aparece nas contingências."
    ),
    26: (
        "[Bruno] (Reserva do Capítulo 3 do painel) Nas faltas trifásicas com sintonia nominal, "
        "quanto mais perto da usina, mais severo o afundamento: a retenção de vd vai de 58,4% na "
        "Barra 6 a 9,2% na Barra 7, e o pico do erro sobe de 7,3 para 37,3 graus.\n\n"
        "[Victor] Como a falta é equilibrada, sem sequência negativa, a componente de 120 Hz fica "
        "abaixo de 0,0011 pu, o erro é apenas transitório e o PLL nominal retorna à faixa de 2 graus "
        "em todos os pontos, entre 76 e 112 ms."
    ),
    27: (
        "[Victor] (Reserva do Capítulo 4 do painel) Nas faltas assimétricas, a sequência negativa "
        "aparece em dq como uma oscilação de 120 Hz entre 0,29 e 0,72 pu, mais de 250 vezes maior "
        "que nas trifásicas.\n\n"
        "[Bruno] Como 754 rad/s é apenas 2,32 vezes a frequência natural do laço, o PI não filtra "
        "essa componente. Já no gráfico da direita, na trifásica da Barra 7, a nominal recupera em "
        "98 ms enquanto a inadequada perde o sincronismo por escorregamento de ciclo."
    ),
    28: (
        "[Bruno] (Reserva do Capítulo 5 do painel) Na bifásica da Barra 6, onde a tensão residual "
        "sustenta o laço, a menor banda da sintonia inadequada filtra o 120 Hz: o pico do erro cai "
        "de 96,0 para 34,5 graus e o retorno cai de 48 para 30 ms.\n\n"
        "[Victor] Porém, na Barra 7, onde o afundamento é severo, essa lentidão cobra o preço na "
        "recuperação: o tempo de retorno quase dobra, passando de 46 para 95 ms na monofásica e de "
        "51 para 96 ms na bifásica."
    ),
    29: (
        "[Bruno] (Reserva do Capítulo 6 do painel) No pós-falta da Barra 7 trifásica com sintonia "
        "inadequada, o inversor passa 66,8% do tempo absorvendo potência ativa da rede, com média de "
        "menos 0,40 pu, comportando-se como uma carga oscilante.\n\n"
        "[Victor] A malha de corrente não falhou, mas como o referencial estimado pelo PLL gira "
        "continuamente em escorregamento de ciclo, a corrente comandada no eixo d troca de sinal em "
        "relação à tensão da rede."
    ),
    30: (
        "[Bruno] (Reserva do Capítulo 7 do painel) Pelo Submódulo 2.10 do ONS, nas faltas trifásicas "
        "com sintonia nominal o inversor cumpre a rampa: satura iq em 1,0 pu na Barra 7 e na Linha "
        "7-8 e entrega 0,72 pu frente a 0,76 pu na Barra 6.\n\n"
        "[Victor] Mas na Barra 7, com a tensão em 0,10 pu, a corrente máxima de 1,0 pu entrega "
        "apenas 0,09 pu de potência reativa. E nas assimétricas ou sob perda de sincronismo, o "
        "inversor segue conectado mas entrega potência com 120 Hz ou drena energia: ficar conectado "
        "não basta."
    ),
}

# Tópicos curtos "O que falar" para os slides que não estavam no dicionário FALAS original (1-4 e 18-22)
EXTRA_FALAS_TOPICOS = {
    1: [
        ("Bruno", "Saudação à banca, apresentação da dupla e título do trabalho (foco no SRF-PLL sob contingências)."),
        ("Victor", "Apresentação dos 5 blocos do percurso: Motivação, Modelagem, Método, Resultados no painel e Conclusão."),
        ("Bruno", "Agradecimento aos orientadores Prof. Oscar e Prof. André e gancho para a motivação."),
    ],
    2: [
        ("Bruno", "Dados globais IEA (2026): cartão de 600 TWh solares (~70% do avanço global) e 800 GW renováveis adicionados."),
        ("Victor", "Gráfico horizontal (5% -> 17% no mundo, ~30% UE, 35% Brasil com MMGD) e cartão ONS (96,8 GW > 85,8 GWmed). Fechar com o rodapé: troca de inércia física por algoritmo de controle."),
    ],
    3: [
        ("Victor", "Cartão 1 (Brasil 15/08/2023): abertura em 500 kV sem curto, afundamento no Nordeste, cascata e 23.368 MW perdidos (34,5%)."),
        ("Bruno", "Diagnóstico do RAP-ONS: descartou falta de inércia (265 GW·s) e curto-circuito; o fator determinante foi o suporte dinâmico de reativos das renováveis muito aquém dos modelos."),
        ("Victor", "Cartão 2 (Península Ibérica 28/04/2025): oscilação de 0,63 Hz guiada por conversor, usinas em fator de potência fixo, > 2,5 GW desligados por sobretensão."),
        ("Bruno", "Cartão 3 (Chile 25/02/2025): 11.066 MW perdidos com 73% solar e eólica, separação em 1,5 s e colapso de tensão na ilha norte. Rodapé: o elo comum é a falha do controle e sincronismo no transitório."),
    ],
    4: [
        ("Bruno", "Diagrama passo 1: o SRF-PLL precisa de tensão limpa, mas a falta traz afundamento, salto de fase e assimetria."),
        ("Victor", "Diagrama passos 2 e 3: em dq, o afundamento reduz o ganho do laço e a sequência negativa vira 120 Hz em vq, gerando erro angular ou perda de sincronismo."),
        ("Bruno", "Diagrama passo 4: com erro em teta, perde-se o desacoplamento entre P e Q e o suporte do Submódulo 2.10 falha."),
        ("Victor", "Cartões da direita: ler o objetivo geral (100 MW no IEEE 9 barras) e os específicos, fechando na pergunta central do rodapé."),
    ],
    18: [
        ("Bruno", "Linha do tempo no topo: 0 a 0,1 s inicialização (fora das métricas), falta de 0,3 a 0,4 s (100 ms = 6 ciclos) e pós-falta até 0,6 s (200 ms de observação)."),
        ("Victor", "Matriz embaixo: colunas azuis analisadas da mais perto à mais longe (B7, L7-8, L8-9, B6); colunas cinzas consultáveis no painel; N = nominal e I = inadequada."),
    ],
    19: [
        ("Bruno", "Quatro blocos superiores: Simulink exporta CSV em duas taxas -> Python alinha no tempo e calcula as métricas automaticamente -> Painel interativo."),
        ("Victor", "Tabela das 5 métricas: retenção de Vd (9,2% na B7 nominal), pico do erro após o 1º ciclo, retorno a ±2° desde a eliminação, 120 Hz no espectro de Vd e P/Q médios."),
        ("Bruno", "Ponte do rodapé: passar para o slide 20 e abrir o painel ao vivo."),
    ],
    20: [
        ("Victor", "Anunciar que os resultados serão mostrados no painel interativo em tela cheia: apertar Alt+Tab para o navegador e clicar em 'Modo apresentação'."),
    ],
    21: [
        ("Bruno", "Cartão 1 (9,2% Vres): nas trifásicas com sintonia nominal, o PLL reconverge em todos os pontos (98 ms na B7); severidade segue a distância elétrica."),
        ("Victor", "Cartão 2 (250× mais 120 Hz): nas assimétricas, a fragilidade é estrutural; o PI não filtra os 120 Hz da sequência negativa, contaminando P e Q."),
        ("Bruno", "Cartão 3 (66,8% do tempo): reduzir os ganhos filtra na B6, mas atrasa a recuperação e causa escorregamento de ciclo na B7, drenando potência ativa em 66,8% do pós-falta."),
        ("Victor", "Rodapé: o sincronismo é decisão de estabilidade; permanecer conectado é insuficiente, é preciso auditar o rastreamento angular."),
    ],
    22: [
        ("Victor", "Caixa de limites (sem defensividade): IEEE 9 barras com nível de curto fixo, duas sintonias e janela de 200 ms pós-falta -> explica um mecanismo físico-dinâmico."),
        ("Bruno", "Dois eixos futuros: (1) DDSRF-PLL e DSOGI-PLL para separar as sequências antes do PI e eliminar o 120 Hz sem perder banda; (2) varrer SCR e múltiplos inversores."),
        ("Victor", "Agradecimento final aos orientadores, à banca e à UERJ, mantendo o painel aberto para perguntas."),
    ],
}

# Roteiro de fala passo a passo para cada um dos 8 capítulos do Modo Apresentação (Palco HTML)
PALCO_SPEECHES = {
    1: [
        ("[Victor] (Passos 1 a 3 — Visão geral, Barra 7 e Linha 7-8): ",
         "No primeiro capítulo do modo apresentação, vemos onde as faltas são aplicadas no IEEE 9 barras. "
         "(Seta →) O ponto mais crítico é a Barra 7, logo depois do transformador T2: como só há o transformador "
         "entre o inversor e o curto, quase toda a tensão cai ali. (Seta →) Em seguida vem a Linha 7-8, de circuito "
         "simples, ainda muito próxima da usina.", C_VICTOR),
        ("[Bruno] (Passos 4 a 6 — Linha 8-9, Barra 6 e Resumo): ",
         "(Seta →) Mais adiante está a Linha 8-9, que tem dois circuitos em paralelo: a falta ocorre em um e o "
         "outro segue conduzindo. (Seta →) E no ramo inferior fica a Barra 6, separada por três linhas de "
         "transmissão, que é o caso mais brando e o contraponto da Barra 7. (Seta →) Essa régua resume a primeira "
         "pergunta dos resultados: como a distância elétrica muda a resposta do SRF-PLL? (Seta → para o Cap. 2)", C_BRUNO),
    ],
    2: [
        ("[Victor] (Passo 1 — Partida com a sintonia nominal): ",
         "No Capítulo 2 verificamos a energização do inversor sem falta, que é a Figura 5.3 do TCC. No passo 1, "
         "com a sintonia nominal em azul, o erro de fase entra de vez na faixa de mais ou menos 2 graus em 40 ms.", C_VICTOR),
        ("[Bruno] (Passo 2 — Entra a sintonia inadequada e o fasor): ",
         "(Seta →) No passo 2, ao ligar a sintonia inadequada em laranja, o travamento leva 79 ms, quase o dobro, "
         "e no gráfico inferior a tensão vd entra na faixa de 5% em 42 ms contra 34 ms da nominal. No fasor à "
         "direita, dando o play desde t igual a zero, vemos os dois vetores girando até travarem no topo. Ou seja, "
         "em regime permanente as duas chegam ao mesmo ponto de operação antes da falta em 0,3 s: a sintonia "
         "inadequada é lenta, não quebrada. (Seta → para o Cap. 3)", C_BRUNO),
    ],
    3: [
        ("[Bruno] (Passo 1 — Foco na falta e mini-mapa de retenção de vd): ",
         "No Capítulo 3 aplicamos a mesma falta trifásica nos quatro pontos com a sintonia nominal, correspondente "
         "à Tabela 5.1 e à Figura 5.7 do TCC. No passo 1, o mini-mapa à direita mostra a retenção de vd durante a "
         "falta: 9,2% na Barra 7, 11,3% na Linha 7-8, 47,1% na Linha 8-9 e 58,4% na Barra 6.", C_BRUNO),
        ("[Victor] (Passos 2 e 3 — Pico do erro no fasor e setas de retorno no pós-falta): ",
         "(Seta →) No passo 2, o pico do erro de fase acompanha a proximidade da falta: chega a 37,3 graus na "
         "Barra 7 contra apenas 7,3 graus na Barra 6. (Seta →) E no passo 3, abrindo a janela toda após a "
         "eliminação em 0,4 s, as setas no topo mostram que o erro volta à faixa de 2 graus em todos os pontos, "
         "em 98 ms na Barra 7 e na Linha 7-8, 112 ms na Linha 8-9 e 76 ms na Barra 6. Sem sequência negativa, o "
         "laço tipo 2 do PLL sempre recupera o sincronismo. (Seta → para o Cap. 4)", C_VICTOR),
    ],
    4: [
        ("[Victor] (Passo 1 — Espectro da trifásica na Barra 7): ",
         "No Capítulo 4 passamos às faltas assimétricas, olhando o espectro da tensão vd durante a falta, que é a "
         "Figura 5.10 do TCC. No passo 1, na falta trifásica da Barra 7 em grafite, a componente em 120 Hz é "
         "praticamente zero: 0,0002 pu.", C_VICTOR),
        ("[Bruno] (Passo 2 — Entram as assimétricas, destaque > 250× e matriz): ",
         "(Seta →) No passo 2, ao ligar as faltas monofásicas e bifásicas nas Barras 6 e 7, aparece o pico em "
         "120 Hz de 0,29 pu na monofásica da Barra 6 até 0,72 pu na bifásica da Barra 7: mais de 250 vezes o maior "
         "valor das trifásicas. Essa oscilação vem da sequência negativa girando a menos ômega, que o referencial "
         "dq enxerga a 2 ômega, 754 rad/s, apenas 2,32 vezes a frequência natural do PLL. Quase dois terços "
         "passam pelo PI e contaminam o ângulo: na bifásica da Barra 7 o erro chega a 180 graus nas duas sintonias. "
         "(Seta → para o Cap. 5)", C_BRUNO),
    ],
    5: [
        ("[Bruno] (Passos 1 e 2 — Bifásica na Barra 6, nominal vs. inadequada): ",
         "No Capítulo 5 avaliamos o efeito de reduzir os ganhos do PLL sob falta assimétrica, na Figura 5.14 do "
         "TCC. No passo 1, na falta bifásica da Barra 6 com sintonia nominal, o 120 Hz passa para o ângulo e o "
         "pico do erro chega a 96,0 graus. (Seta →) No passo 2, com a sintonia inadequada em laranja, a perturbação "
         "em vd é quase a mesma, mas como a banda caiu de 107 para 38 Hz, ela filtra melhor o 120 Hz: o pico do "
         "erro cai para 34,5 graus e o retorno cai de 48 para 30 ms.", C_BRUNO),
        ("[Victor] (Passo 3 — A frase-ponte e a lentidão na Barra 7): ",
         "(Seta →) No passo 3, vemos por que isso parece vantajoso na Barra 6: ali a tensão positiva que sobra, "
         "0,72 pu, ainda sustenta o laço. Porém, na Barra 7, onde a tensão cai mais, o mesmo ganho menor faz o "
         "tempo de retorno quase dobrar: vai de 46 para 95 ms na monofásica e de 51 para 96 ms na bifásica. "
         "E o que acontece numa falta ainda mais severa? (Seta → para o Cap. 6)", C_VICTOR),
    ],
    6: [
        ("[Victor] (Passos 1 e 2 — Barra 7 trifásica: nominal recupera, inadequada sofre escorregamento de ciclo): ",
         "O Capítulo 6 responde com a falta trifásica na Barra 7, as Figuras 5.18 e 5.19 do TCC. No passo 1, com "
         "a sintonia nominal, mesmo retendo apenas 9,2% de vd, o erro volta à faixa de 2 graus em 98 ms. "
         "(Seta →) No passo 2, com a sintonia inadequada, a retenção de tensão é quase idêntica, 8,2%, mas o "
         "amortecimento efetivo cai a quase zero durante o afundamento e o PLL entra em escorregamento de ciclo, "
         "varrendo toda a faixa de mais a menos 180 graus sem recuperar até o fim da janela.", C_VICTOR),
        ("[Bruno] (Passo 3 — Fecho com potência ativa absorvida em 66,8% do tempo): ",
         "(Seta →) E no passo 3 vemos o impacto na potência ativa e no fasor à direita: o mesmo ganho menor que "
         "filtrava o 120 Hz na Barra 6 é o que perde o sincronismo aqui. A malha de corrente não falhou, mas como "
         "o vetor laranja gira sem parar em relação à rede, o cosseno do erro angular troca de sinal e a usina "
         "absorve potência ativa da rede em 66,8% do tempo após a eliminação, com média de menos 0,40 pu. "
         "(Seta → para o Cap. 7)", C_BRUNO),
    ],
    7: [
        ("[Bruno] (Passos 1 a 3 — Curva de suportabilidade e rampa de corrente reativa do ONS): ",
         "No Capítulo 7 confrontamos os resultados com o Submódulo 2.10 do ONS: à esquerda a curva de "
         "suportabilidade da Figura 2.1 e à direita a rampa de corrente reativa da Figura 2.2. (Seta →) No passo 2, "
         "na Barra 7 e na Linha 7-8 a tensão cai abaixo de 0,2 pu, onde a desconexão seria permitida, mas o "
         "inversor permanece conectado e satura iq em 1,0 pu. (Seta →) No passo 3, nos pontos mais distantes a "
         "injeção segue a rampa, entregando 0,72 pu na Barra 6 contra 0,76 pu previstos.", C_BRUNO),
        ("[Victor] (Passos 4 a 6 — O dilema dos 0,09 pu, outros curtos e o cartão de fecho): ",
         "(Seta →) O passo 4 mostra o dilema físico na Barra 7: com a tensão retida abaixo de 10%, em 0,10 pu, "
         "mesmo a corrente máxima de 1,0 pu entrega apenas 0,09 pu de potência reativa à rede. (Seta →) No passo 5, "
         "acendendo os demais curtos, vemos que nas faltas assimétricas e na perda de sincronismo o inversor "
         "também permanece conectado, mas entrega potência oscilando em 120 Hz ou drena energia da rede. "
         "(Seta →) Daí o cartão de fecho no passo 6: perguntar apenas se o inversor permaneceu conectado é "
         "insuficiente; é preciso acompanhar a qualidade do rastreamento angular durante toda a contingência e na "
         "recuperação. (Seta → para o Cap. 8)", C_VICTOR),
    ],
    8: [
        ("[Victor] (Tabela síntese de todos os casos e retorno ao PowerPoint): ",
         "O Capítulo 8 reúne em uma tela todos os indicadores das Tabelas 5.1, 5.2 e 5.3 do TCC, onde qualquer "
         "linha pode ser clicada na arguição para abrir o cenário completo. Agora saímos da tela cheia e voltamos "
         "ao PowerPoint para os dois slides finais. (Aperta Esc e Alt+Tab para o Slide 21).", C_VICTOR),
    ],
}


# ==============================================================================
# UTILITÁRIOS DE FORMATAÇÃO WORD (PYTHON-DOCX)
# ==============================================================================
def set_cell_bg(cell, hex_color: str):
    hex_clean = hex_color.lstrip("#")
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_clean)
    tcPr.append(shd)


def set_cell_margins(cell, top=90, bottom=90, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="C7D2DA", sz="4"):
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


def add_rich_runs(p, html_text: str, base_font="Arial", base_size=10.0, base_color=C_INK, base_bold=False, base_italic=False):
    """Converte tags simples (<b>, <i>, <sub>, <super>, <font color='...'>, <br/>) e entidades HTML em runs do Word."""
    txt = html_text.replace("<br/>", "\n").replace("<br>", "\n")
    # Tokenizar por tags conhecidas
    token_re = re.compile(r"(</?(?:b|i|sub|super|sup|font)[^>]*>)", re.IGNORECASE)
    tokens = token_re.split(txt)

    bold_stack = [base_bold]
    italic_stack = [base_italic]
    sub_state = False
    sup_state = False
    color_stack = [base_color]

    for tok in tokens:
        if not tok:
            continue
        low = tok.lower()
        if low == "<b>":
            bold_stack.append(True)
        elif low == "</b>":
            if len(bold_stack) > 1:
                bold_stack.pop()
        elif low == "<i>":
            italic_stack.append(True)
        elif low == "</i>":
            if len(italic_stack) > 1:
                italic_stack.pop()
        elif low == "<sub>":
            sub_state = True
        elif low == "</sub>":
            sub_state = False
        elif low in ("<super>", "<sup>"):
            sup_state = True
        elif low in ("</super>", "</sup>"):
            sup_state = False
        elif low.startswith("<font"):
            m = re.search(r"color=['\"]?#?([0-9a-fA-F]{6})['\"]?", tok)
            if m:
                hx = m.group(1)
                color_stack.append(RGBColor(int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)))
            else:
                color_stack.append(color_stack[-1])
        elif low == "</font>":
            if len(color_stack) > 1:
                color_stack.pop()
        else:
            clean = html.unescape(re.sub(r"<[^>]+>", "", tok))
            if not clean:
                continue
            r = p.add_run(clean)
            r.font.name = base_font
            r.font.size = Pt(base_size)
            r.bold = bold_stack[-1]
            r.italic = italic_stack[-1]
            r.font.subscript = sub_state
            r.font.superscript = sup_state
            r.font.color.rgb = color_stack[-1]


def format_mmss(minutes_float: float) -> str:
    total_sec = int(round(minutes_float * 60))
    return f"{total_sec // 60:02d}:{total_sec % 60:02d}"


class WordRoteiroBuilder:
    """Intercepta todos os comandos do gen_roteiro_estudo_defesa.py e constrói o Word (.docx)
    enriquecido com as falas completas de 30 minutos e o mapa do TCC."""

    def __init__(self, doc: Document):
        self.doc = doc
        self.s_body = "body"
        self.s_h = "h"
        self.s_tag = "tag"
        self.story = []  # dummy list para compatibilidade com KeepTogether/pop se necessário

    def add_header_banner(self, title: str, subtitle: str, meta_left: str, meta_right: str):
        p_kicker = self.doc.add_paragraph()
        p_kicker.paragraph_format.space_before = Pt(0)
        p_kicker.paragraph_format.space_after = Pt(2)
        rk = p_kicker.add_run("UERJ • FACULDADE DE ENGENHARIA • ENGENHARIA ELÉTRICA • DEFESA DE TCC (2026)")
        rk.bold = True
        rk.font.name = "Arial"
        rk.font.size = Pt(8.5)
        rk.font.color.rgb = C_ACCENT

        p_t = self.doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(3)
        rt = p_t.add_run(title)
        rt.bold = True
        rt.font.name = "Arial"
        rt.font.size = Pt(18)
        rt.font.color.rgb = C_ACCENT

        p_sub = self.doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(8)
        rs = p_sub.add_run(subtitle)
        rs.font.name = "Arial"
        rs.font.size = Pt(10.5)
        rs.font.color.rgb = C_MUTED

        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        set_cell_bg(c0, "F4F7F9")
        set_cell_bg(c1, "F4F7F9")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        c0.width = Cm(11.5)
        c1.width = Cm(5.5)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        add_rich_runs(p0, meta_left, base_size=9.0, base_color=C_MUTED)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(0)
        add_rich_runs(p1, meta_right, base_size=9.0, base_color=C_MUTED)
        self.gap(6)

    def h(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "10")
        bottom.set(qn("w:space"), "3")
        bottom.set(qn("w:color"), "1A4A6E")
        pBdr.append(bottom)
        pPr.append(pBdr)
        add_rich_runs(p, text, base_size=13.5, base_color=C_ACCENT, base_bold=True)

    def sub(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        add_rich_runs(p, text, base_size=11.0, base_color=C_ACCENT, base_bold=True)

    def p(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        add_rich_runs(p, text, base_size=10.0, base_color=C_INK)

    def bul(self, *items, numbered=False):
        for idx, it in enumerate(items, 1):
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.4)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            prefix = f"{idx}. " if numbered else "• "
            rp = p.add_run(prefix)
            rp.bold = True
            rp.font.name = "Arial"
            rp.font.size = Pt(10.0)
            rp.font.color.rgb = C_ACCENT
            add_rich_runs(p, it, base_size=10.0, base_color=C_INK)

    def note(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.12
        add_rich_runs(p, f"<i>Nota:</i> {text}", base_size=9.2, base_color=C_MUTED)

    def gap(self, pt_val=4):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(max(1, pt_val // 2))

    def pagebreak(self):
        self.doc.add_page_break()

    def box(self, kind: str, *paras, titulo: str = None):
        bg_hex, bar_hex, title_rgb, default_rot = KIND_STYLE.get(kind, KIND_STYLE["msg"])
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Cm(17.0)
        set_cell_bg(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=160, right=140)

        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        left_b = OxmlElement("w:left")
        left_b.set(qn("w:val"), "single")
        left_b.set(qn("w:sz"), "24")
        left_b.set(qn("w:color"), bar_hex)
        tcBorders.append(left_b)
        for b_name in ["top", "bottom", "right"]:
            b = OxmlElement(f"w:{b_name}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), "4")
            b.set(qn("w:color"), "DCE4EC")
            tcBorders.append(b)
        tcPr.append(tcBorders)

        p0 = cell.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(3)
        add_rich_runs(p0, titulo or default_rot, base_size=8.8, base_color=title_rgb, base_bold=True)

        is_msg = (kind == "msg")
        for para_text in paras:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if isinstance(para_text, tuple):
                prefix, body, p_rgb = para_text
                rp = p.add_run(prefix)
                rp.bold = True
                rp.font.name = "Arial"
                rp.font.size = Pt(9.8)
                rp.font.color.rgb = p_rgb
                add_rich_runs(p, body, base_size=9.8, base_color=C_INK)
            else:
                add_rich_runs(
                    p,
                    para_text,
                    base_size=11.0 if is_msg else 9.8,
                    base_color=C_ACCENT if is_msg else C_INK,
                    base_bold=is_msg,
                )
        self.gap(4)

    def eq(self, tex: str, tag: str = None, onde: str = None):
        buf, w_pt, h_pt = _mathtext_image(tex, fontsize=13.5, dpi=300)
        tbl = self.doc.add_table(rows=1, cols=2 if tag else 1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0 = tbl.cell(0, 0)
        set_cell_bg(c0, "F4F7F9")
        set_cell_margins(c0, top=80, bottom=80, left=140, right=100)
        c0.width = Cm(14.8 if tag else 17.0)

        tcPr = c0._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        left_b = OxmlElement("w:left")
        left_b.set(qn("w:val"), "single")
        left_b.set(qn("w:sz"), "18")
        left_b.set(qn("w:color"), "1A4A6E")
        tcBorders.append(left_b)
        tcPr.append(tcBorders)

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r_img = p0.add_run()
        # Limitar largura máxima a 13.5 cm mantendo proporção
        w_cm = min(13.5, w_pt * 2.54 / 72.0)
        r_img.add_picture(buf, width=Cm(w_cm))

        if tag:
            c1 = tbl.cell(0, 1)
            set_cell_bg(c1, "F4F7F9")
            set_cell_margins(c1, top=80, bottom=80, left=40, right=100)
            c1.width = Cm(2.2)
            c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p1 = c1.paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p1.paragraph_format.space_after = Pt(0)
            rt = p1.add_run(f"({tag})")
            rt.font.name = "Arial"
            rt.font.size = Pt(9.5)
            rt.font.color.rgb = C_MUTED

        if onde:
            p_onde = self.doc.add_paragraph()
            p_onde.paragraph_format.left_indent = Cm(0.4)
            p_onde.paragraph_format.space_before = Pt(2)
            p_onde.paragraph_format.space_after = Pt(5)
            p_onde.paragraph_format.line_spacing = 1.12
            add_rich_runs(p_onde, onde, base_size=9.0, base_color=C_MUTED)
        else:
            self.gap(4)

    def table(self, headers: list, rows: list, widths_cm: list = None):
        tbl = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="C7D2DA", sz="4")

        # Escalar larguras de 14.7 cm (PDF) para 17.0 cm (Word)
        scaled_w = None
        if widths_cm:
            tot = sum(widths_cm)
            scaled_w = [w * 17.0 / tot for w in widths_cm]

        hdr_cells = tbl.rows[0].cells
        for i, h_text in enumerate(headers):
            set_cell_bg(hdr_cells[i], "1A4A6E")
            set_cell_margins(hdr_cells[i], top=75, bottom=75, left=100, right=100)
            hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = hdr_cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            add_rich_runs(p, h_text, base_size=9.2, base_color=C_WHITE, base_bold=True)

        for r_idx, row_data in enumerate(rows):
            row_cells = tbl.rows[r_idx + 1].cells
            bg = "F4F7F9" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                set_cell_bg(row_cells[c_idx], bg)
                set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
                row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = row_cells[c_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.12
                add_rich_runs(p, str(val), base_size=9.2, base_color=C_INK, base_bold=(c_idx == 0 and len(str(val)) < 35))

        if scaled_w:
            for row in tbl.rows:
                for i, w in enumerate(scaled_w):
                    row.cells[i].width = Cm(w)

        self.gap(5)

    def figura(self, img_path: Path, legenda: str = None, largura_cm: float = 15.2):
        if img_path and Path(img_path).exists():
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            r = p_img.add_run()
            r.add_picture(str(img_path), width=Cm(min(16.5, largura_cm)))
        if legenda:
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(6)
            add_rich_runs(p_cap, legenda, base_size=8.8, base_color=C_MUTED, base_italic=True)

    def instante(self, quando: str, titulo: str, primeiro: str):
        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        c0.width = Cm(3.4)
        c1.width = Cm(13.6)
        set_cell_bg(c0, "1A4A6E")
        set_cell_bg(c1, "E7EFF6")
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=120, right=100)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        add_rich_runs(p0, quando, base_size=8.8, base_color=C_WHITE, base_bold=True)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        add_rich_runs(p1, titulo, base_size=10.2, base_color=C_ACCENT, base_bold=True)
        self.p(primeiro)

    def ponte(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        add_rich_runs(p, f"&#8594; <b>Próximo:</b> <i>{text}</i>", base_size=9.8, base_color=C_MUTED)

    def faixa(self, rotulo: str, num: int, titulo: str, meta: str, imagem: Path = None, legenda: str = None):
        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = tbl.rows[0].cells
        c0.width = Cm(2.3)
        c1.width = Cm(14.7)
        set_cell_bg(c0, "1A4A6E" if rotulo == "SLIDE" else "0F766E")
        set_cell_bg(c1, "F4F7F9")
        set_cell_margins(c0, top=80, bottom=80, left=60, right=60)
        set_cell_margins(c1, top=80, bottom=80, left=140, right=100)
        c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r_rot = p0.add_run(f"{rotulo}\n")
        r_rot.bold = True
        r_rot.font.name = "Arial"
        r_rot.font.size = Pt(8.5)
        r_rot.font.color.rgb = C_WHITE
        r_num = p0.add_run(f"{num:02d}" if isinstance(num, int) else str(num))
        r_num.bold = True
        r_num.font.name = "Arial"
        r_num.font.size = Pt(18)
        r_num.font.color.rgb = C_WHITE

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(2)
        add_rich_runs(p1, titulo, base_size=13.5, base_color=C_ACCENT, base_bold=True)
        p2 = c1.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        add_rich_runs(p2, meta, base_size=9.0, base_color=C_MUTED)

        if imagem and Path(imagem).exists():
            self.figura(imagem, legenda=legenda, largura_cm=15.0)
        else:
            self.gap(4)

    def add_slide_speech_box(self, slide_num: int):
        """Adiciona os tópicos resumidos (se não estiverem no FALAS de 5-17) e a fala completa cronometrada."""
        if slide_num in EXTRA_FALAS_TOPICOS:
            topicos = [f"<b>{quem}:</b> {txt}" for quem, txt in EXTRA_FALAS_TOPICOS[slide_num]]
            self.box("fala", *topicos)

        speech_raw = SLIDE_SPEECHES.get(slide_num, "")
        if not speech_raw or slide_num in (23, 24):
            return
        paras = [p.strip() for p in speech_raw.split("\n\n") if p.strip()]
        formatted_lines = []
        tot_w = len(speech_raw.split())
        for p_txt in paras:
            if p_txt.startswith("[Bruno]"):
                body = p_txt[len("[Bruno]"):].strip()
                w_c = len(body.split())
                formatted_lines.append((f"[Bruno] ({w_c} pal. ~ {format_mmss(w_c/130)}): ", body, C_BRUNO))
            elif p_txt.startswith("[Victor]"):
                body = p_txt[len("[Victor]"):].strip()
                w_c = len(body.split())
                formatted_lines.append((f"[Victor] ({w_c} pal. ~ {format_mmss(w_c/130)}): ", body, C_VICTOR))
            else:
                formatted_lines.append(p_txt)

        rot_Kind = "script" if slide_num <= 22 else "palco_s"
        label = (
            f"ORDEM DE FALAS PRONTA DO SLIDE {slide_num:02d} ({tot_w} palavras ~ {format_mmss(tot_w/130)})"
            if slide_num <= 22
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


def sync_pptx_notes():
    """As notas do apresentador já são sincronizadas via gen_revisao_final.py + pptx_finalize.ps1 + entrega.ps1."""
    return


def inject_30min_schedule_and_tcc_map(wb: WordRoteiroBuilder):
    """Insere o Cronograma de 30 Minutos (PPTX 1-20 -> Palco 1-8 -> PPTX 21-22) e o Mapa Sequencial do TCC."""
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

    # 1. Slides 1 a 20
    slide_titles = {
        1: "Capa e abertura",
        2: "Expansão das renováveis (IEA / ONS)",
        3: "Eventos no mundo real (Brasil, Ibéria, Chile)",
        4: "Problema e objetivos",
        5: "Fonte renovável (Fig. 3.2)",
        6: "Transformada de Park (Eq. 3.5)",
        7: "Estrutura do SRF-PLL (Fig. 4.3)",
        8: "Sistema IEEE 9 barras e Thévenin (Fig. 4.1)",
        9: "Bancada do PLL entre fontes ideais (PSIM)",
        10: "Sintonia nominal do PLL (ts = 20 ms)",
        11: "Duas sintonias do PLL (nominal × inadequada)",
        12: "Referência de corrente (1ª versão PSIM)",
        13: "Controle de corrente e filtro LCL (Fig. 3.1)",
        14: "Referência pelo ONS (Submódulo 2.10)",
        15: "Dentro do Submódulo 2.10 (rampa e círculo)",
        16: "Lógica em blocos do Submódulo 2.10",
        17: "Sistema completo (Fig. 4.2)",
        18: "Protocolo de contingência e matriz (Tab. 4.1)",
        19: "Fluxo de análise e 5 métricas",
        20: "Porta para o painel (Alt+Tab -> Modo apresentação)",
    }

    for s_num in range(1, 21):
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

    # 3. Slides 21 e 22
    for s_num, t_str in [(21, "Síntese dos resultados (Cap. 6)"), (22, "Trabalhos futuros e encerramento (Cap. 7)")]:
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
        f"Total cronometrado do percurso completo (Slides 1–20 + Palco 1–8 + Slides 21–22): "
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
            ["Cap. 2 — §2.1 a §2.3\nTransição e Estabilidade", "IEA (2026): +600 TWh solares, 5%&#8594;17% no mundo; ONS (2025): 96,8 GW (> 85,8 GWmed, 35% no SIN). Classificação clássica IEEE/CIGRE 2004 (Gu e Green, 2023) vs. estendida IEEE PES TR77 (estabilidade guiada por conversores).", "Slides 2, 4, 5, 21 e 23"],
            ["Cap. 2 — §2.4\nGrandes Blecautes", "§2.4.1 Ibéria 2025 (ENTSO-E: 0,63 Hz, fator de potência fixo, >2,5 GW por sobretensão); §2.4.2 Chile 2025 (CEN: 11.066 MW, 73% solar+eólica, 2 ilhas em 1,5 s); §2.4.3 Brasil 2023 (RAP-ONS 00012/2023: 23.368 MW, 265 GW·s, suporte de reativo aquém dos modelos).", "Slide 3"],
            ["Cap. 2 — §2.5\nRequisitos Normativos", "Curva LVRT (Fig. 2.1) e rampa de injeção reativa do Submódulo 2.10 do ONS (Fig. 2.2): banda morta 0,85–1,10 pu, rampa (0,85−V)/0,35 saturando em 1 pu para V &#8804; 0,50 pu.", "Slides 14–16, Painel 7 e Slide 30"],
            ["Cap. 3 — §3.1 a §3.3\nPark, Potência dq e VSI", "Transformadas de Clarke e Park (Eqs. 3.1–3.7), potência instantânea e controle desacoplado (Eqs. 3.8–3.9), VSI conectado à rede (Fig. 3.2) e malha de corrente (Fig. 3.1).", "Slides 5, 6, 12 e 13"],
            ["Cap. 3 — §3.4 e §3.5\nSRF-PLL e Sintonia Canônica", "Estrutura PD/PI/VCO (Fig. 3.3 / 4.3, Eqs. 3.10–3.18), sintonia por 2ª ordem com &#958; = 0,707 e ts(1%) = 20 ms (Eqs. 3.19–3.20: Kp=460, Ki=105.820, &#969;n=325,3 rad/s) e sintonia da corrente (§3.5, Eqs. 3.21–3.23).", "Slides 7, 10, 11 e 13"],
            ["Cap. 4 — §4.1 a §4.3\nMetodologia e IEEE 9 Barras", "Abordagem Python/PSIM/Simulink (§4.2), IEEE 9 barras com UFV na Barra 2 e Thévenin (§4.3.1, Fig. 4.1), filtro LCL e controle completo (§4.3.2, Fig. 4.2, Eq. 4.2), matriz de cenários e protocolo de 6 ciclos (§4.3.3–4.3.4, Tab. 4.1).", "Slides 8, 9, 13–19 e Painel 1"],
            ["Cap. 5 — §5.1 a §5.5\nResultados e Discussão", "§5.1 Energização (Fig. 5.3: 40 vs 79 ms); §5.2 Trifásicas (Fig. 5.7, Tab. 5.1: 9,2% a 58,4%); §5.3 Assimétricas (Figs. 5.10 e 5.14, Tab. 5.3: 120 Hz até 0,72 pu, >250×; B6 96°&#8594;34,5°; B7 retorno dobra); §5.4 Perda de sincronismo (Figs. 5.18–5.21: escorregamento de ciclo na B7 e L7-8, 66,8% absorvendo P); §5.5 Código de rede (Tab. 5.2: Q=0,09 pu na B7).", "Slide 20 &#8594; Painel 1 a 8 (e Reserva 24–30)"],
            ["Cap. 6 e Cap. 7\nConclusões e Trabalhos Futuros", "Cap. 6: síntese qualitativa, insuficiência do critério estático de permanecer conectado, ressalvas metodológicas (sobrecorrentes limitadas pelo controle e SCR fixo). Cap. 7: Eixo 1 (DDSRF-PLL e DSOGI-PLL) e Eixo 2 (varredura de SCR e múltiplos inversores).", "Slides 21 e 22"],
        ],
        [3.4, 8.5, 2.8],
    )


def inject_defesa_qa_and_hidden_slides(wb: WordRoteiroBuilder, slides_jpg_fn):
    """Adiciona no final da Parte V os slides ocultos 25-30 com fala de reserva e as 9 perguntas do defesa_qa.pdf."""
    wb.h("Detalhamento dos Slides Ocultos de Reserva (Slides 25 a 30)")
    wb.p(
        "Caso o navegador falhe no dia da apresentação, estes 6 slides no final do PowerPoint "
        "substituem diretamente os Capítulos 2 a 7 do Modo Apresentação:"
    )
    hidden_meta = [
        (25, "Energização (Reserva do Painel 2)", "§5.1 · Figura 5.3 · 34/40 ms vs. 42/79 ms"),
        (26, "Faltas trifásicas (Reserva do Painel 3)", "§5.2 · Figura 5.7 e Tabela 5.1 · 9,2% a 58,4%"),
        (27, "Sequência negativa e perda de sincronismo (Reserva dos Painéis 4 e 6)", "§5.3 e §5.4 · Figuras 5.10 e 5.18 · > 250× e 98 ms"),
        (28, "Compromisso da sintonia nas assimétricas (Reserva do Painel 5)", "§5.3 · Figura 5.14 e Tabela 5.3 · 96,0° &#8594; 34,5° na B6; retorno dobra na B7"),
        (29, "Dinâmica pós-falta e absorção de potência (Reserva do Painel 6)", "§5.4 · Figuras 5.20 e 5.21 · 66,8% do tempo absorvendo P (média −0,40 pu)"),
        (30, "Conformidade com o Submódulo 2.10 do ONS (Reserva do Painel 7)", "§5.5 · Figura 2.2 e Tabela 5.2 · Q = 0,09 pu na Barra 7"),
    ]
    for s_num, tit, ref in hidden_meta:
        wb.faixa("RESERVA", s_num, tit, ref, imagem=slides_jpg_fn(s_num))
        wb.add_slide_speech_box(s_num)

    wb.h("Respostas Rápidas para Cruzamentos entre Deck e TCC (defesa_qa.pdf)")
    wb.p(
        "Estes 9 pontos cobrem divergências ou detalhes internos do TCC entregue (VFinal, 15/10/2026) "
        "que a banca pode perguntar na arguição:"
    )
    qa_list = [
        ("1. Quantos cenários foram simulados (28 na Tabela 4.1 vs. 29 no Cap. 5)?",
         "Foram simulados <b>29 cenários: 21 com a sintonia nominal e 8 com a sintonia inadequada</b> "
         "(28 com falta e 1 em regime permanente). Na Tabela 4.1 faltam a marca da Linha 7-8 inadequada "
         "e a linha de regime permanente, mas ambas estão descritas e analisadas no Capítulo 5 (§5.1 e §5.4)."),
        ("2. Por que os objetivos da Introdução citam sobrecorrentes e impedância da rede?",
         "O Capítulo 6 registra as duas ressalvas: as sobrecorrentes não se manifestam porque o controle "
         "limita a referência de corrente antes disso; e a impedância da rede foi observada variando a "
         "distância elétrica da falta (da Barra 7 à Barra 6) com nível de curto fixo."),
        ("3. Quais são os valores de Vcc, L1, L2, Cf e Rd que não estão no texto do Cap. 4?",
         "Estão no modelo Simulink e no Slide 23 (Apêndice): V<sub>cc</sub> = 136,36 kV (1,5 &#215; 90,91 kV "
         "do cálculo para evitar sobremodulação do PWM na escala de 100 MW), L<sub>1</sub> = 30,42 mH, "
         "L<sub>2</sub> = 0,289 mH (L<sub>est</sub> = 30,71 mH), C<sub>f</sub> = 42,47 &#956;F e resistores "
         "de amortecimento passivo R<sub>d</sub> em série."),
        ("4. A malha de corrente (339,4 rad/s) e o PLL nominal (325,3 rad/s) têm quase a mesma banda?",
         "Sim: cada malha seguiu a sua referência clássica (Alves, 2022 para acomodar a corrente em 1 ciclo; "
         "Alves, Dias e Rolim, 2020 e Teodorescu et al., 2011 para acomodar o PLL em 20 ms). Os ganhos de "
         "corrente ficaram fixos em todas as simulações para isolar o efeito do PLL; a interação entre bandas "
         "próximas fica fora do escopo."),
        ("5. O cartão nas abas por cenário mostra 8,3% na Barra 7, mas o TCC e o palco dizem 9,2%.",
         "São métricas diferentes: <b>9,2%</b> é a retenção de v<sub>d</sub> em percentual do valor pré-falta "
         "(Tabela 5.1 e cartões do Modo Apresentação). Já 8,3% no cartão superior da aba por cenário é o "
         "módulo da tensão |V| na Barra 2."),
        ("6. O blecaute de 15/08/2023 desligou 22.547 MW (Introdução) ou 23.368 MW (§2.4.3 e Slide 3)?",
         "O valor consolidado oficial é <b>23.368 MW (34,5% da demanda do momento)</b>, do Relatório de "
         "Análise de Perturbação do ONS (RAP-ONS 00012/2023) detalhado na §2.4.3."),
        ("7. Onde ocorre o escorregamento de ciclo (cycle slipping)?",
         "Ocorre com a <b>sintonia inadequada nas faltas trifásicas severas: Barra 7 e Linha 7-8</b> (§5.4, "
         "Fig. 5.18), onde o erro gira continuamente após a eliminação e não retorna até 0,6 s. Nas faltas "
         "assimétricas (§5.3), a fragilidade é a oscilação estacionária de 120 Hz."),
        ("8. Por que a potência reativa na Barra 7 é de apenas 0,09 pu com corrente reativa saturada em 1,0 pu?",
         "Porque Q &#8776; V&#183;i<sub>q</sub>: como a tensão média durante a falta na Barra 7 cai para "
         "0,10 pu (menos de 10%), mesmo injetando 1,0 pu de corrente reativa a potência entregue fica em 0,09 pu."),
        ("9. E o modo formador de rede (grid-forming / GFM)?",
         "Está fora do escopo de simulação. O Capítulo 7 propõe dar continuidade mantendo inversores seguidores "
         "de rede: evoluir a estrutura de sincronismo (DDSRF-PLL e DSOGI-PLL) e varrer as condições de rede (SCR)."),
    ]
    for q_t, q_a in qa_list:
        wb.box("prova", q_a, titulo=q_t)


def build_word_document():
    sync_pptx_notes()

    doc = Document()
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(1.6)
        section.bottom_margin = Cm(1.6)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    wb = WordRoteiroBuilder(doc)

    # Cabeçalho principal
    wb.add_header_banner(
        title="Roteiro e Guia Completo de Estudo da Defesa (30 Minutos)",
        subtitle="Slide a slide e capítulo a capítulo, na ordem em que a apresentação acontece "
                 "(PPTX 1–20, Painel HTML Modo Apresentação 1–8 e volta ao PPTX 21–22), com os "
                 "fundamentos de cada tema, a sequência do TCC e as falas completas cronometradas",
        meta_left="<b>Victor Hugo de Avelar Rezende e Bruno Henrique de Oliveira</b><br/>"
                  "Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos",
        meta_right="<b>Guia Final Unificado (Word + Palco)</b><br/>26 de outubro de 2026",
    )

    # Vamos executar o conteúdo de gen_roteiro_estudo_defesa.py redirecionando as chamadas para `wb`!
    roteiro_py = (ROOT / "scripts" / "notas" / "gen_roteiro_estudo_defesa.py").read_text(encoding="utf-8")

    # Cortamos o cabeçalho de imports/definições até "# =============================================================================\n# ABERTURA"
    marker = "# =============================================================================\n# ABERTURA"
    if marker not in roteiro_py:
        marker = "# ABERTURA"
    body_code = roteiro_py[roteiro_py.index(marker):]
    # Remover as 4 linhas finais de `out = n.build() ...`
    body_code = body_code[:body_code.index("out = n.build()")]

    SLIDES_PNG = Path(r"C:\Temp\defesa_roteiro\png")
    PALCO_PNG = ROOT / "output" / "verifica_palco" / "1920x1080"
    CACHE = SLIDES_PNG.parent / "jpg"
    CACHE.mkdir(parents=True, exist_ok=True)

    def jpg(src: Path, largura=1300) -> Path:
        dst = CACHE / (src.parent.name + "_" + src.stem + ".jpg")
        if not dst.exists() or (src.exists() and dst.stat().st_mtime < src.stat().st_mtime):
            with PILImage.open(src) as im:
                im = im.convert("RGB")
                if im.width > largura:
                    im = im.resize((largura, round(im.height * largura / im.width)), PILImage.LANCZOS)
                im.save(dst, "JPEG", quality=86, optimize=True)
        return dst

    def rap_fig(nome, pagina, clip) -> Path:
        dst = CACHE / f"rap_{nome}.jpg"
        return dst

    current_context = {"type": None, "num": None, "injected_schedule": False}

    class NoteProxy:
        def h(self, text):
            wb.h(text)
            if text == "Folha de números":
                # Antes da Folha de números final, injetamos os slides ocultos 25-30 e o Q&A completo!
                pass

        def p(self, text):
            wb.p(text)

        def table(self, header, rows, widths):
            wb.table(header, rows, widths)

        def note(self, text):
            wb.note(text)
            # Logo após a nota das "Convenções que valem para tudo", injetamos o Cronograma de 30 min e o Mapa do TCC!
            if "Sem RoCoF" in text and not current_context["injected_schedule"]:
                current_context["injected_schedule"] = True
                inject_30min_schedule_and_tcc_map(wb)

        def gap(self, h=6):
            wb.gap(h)

        def pagebreak(self):
            wb.pagebreak()

    n_proxy = NoteProxy()
    FALAS_DICT = {}

    def box_hook(kind, *paras, titulo=None):
        wb.box(kind, *paras, titulo=titulo)
        # Se acabamos de colocar a MENSAGEM de um slide que NÃO tem `fala(num)` (ex.: slides 1-4, 18-22),
        # injetamos a caixa de fala completa logo abaixo da MENSAGEM!
        if kind == "msg":
            if current_context["type"] == "slide":
                s_num = current_context["num"]
                if s_num not in range(5, 18):
                    wb.add_slide_speech_box(s_num)
            elif current_context["type"] == "cap":
                c_num = current_context["num"]
                # Nos capítulos 1 e 8 (que não têm box("passo")), injetamos a fala do palco logo após a MENSAGEM
                if c_num in (1, 8):
                    wb.add_palco_speech_box(c_num)
        elif kind == "passo" and current_context["type"] == "cap":
            # Nos capítulos 2 a 7 (que têm box("passo")), injetamos a fala passo a passo logo após os PASSOS!
            wb.add_palco_speech_box(current_context["num"])

    def fala_hook(num):
        wb.box("fala", *[f"<b>{quem}:</b> {texto}" for quem, texto in FALAS_DICT[num]])
        # E logo abaixo dos tópicos do Victor nos slides 5 a 17, colocamos o texto completo cronometrado!
        wb.add_slide_speech_box(num)

    def slide_hook(num, titulo, bloco, quem, tcc):
        current_context["type"] = "slide"
        current_context["num"] = num
        wb.faixa(
            "SLIDE",
            num,
            titulo,
            f"{bloco} &#160;·&#160; Fala: {quem} &#160;·&#160; No TCC: {tcc}",
            imagem=jpg(SLIDES_PNG / f"s{num:02d}.png"),
        )

    def cap_hook(num, titulo, ref, png, legenda):
        current_context["type"] = "cap"
        current_context["num"] = num
        wb.faixa(
            "PAINEL",
            num,
            titulo,
            ref,
            imagem=jpg(PALCO_PNG / png),
            legenda=legenda,
        )

    def imagem_palco_hook(png, legenda, alt=8.6):
        wb.figura(jpg(PALCO_PNG / png), legenda=legenda, largura_cm=15.0)

    def parte_hook(titulo, *paras):
        wb.h(titulo)
        for x in paras:
            wb.p(x)

    def tab_hook(header, rows, widths):
        wb.table(header, rows, widths)
        # Se acabamos de colocar a tabela "Outros materiais" na Parte V, injetamos os Slides Ocultos 25-30 e o Q&A!
        if header == ["Material", "Para quê"]:
            inject_defesa_qa_and_hidden_slides(wb, lambda s_n: jpg(SLIDES_PNG / f"s{s_n:02d}.png"))

    def nums_hook(rows):
        wb.table(["Número", "O que é"], rows, [3.9, 10.8])

    def figura_hook(caminho, legenda, largura=14.7):
        wb.figura(caminho, legenda=legenda, largura_cm=largura * 16.5 / 14.7)

    exec_env = {
        "n": n_proxy,
        "W": 14.7,
        "S_BUL": "bul",
        "Paragraph": lambda txt, style, bulletText=None: txt,
        "box": box_hook,
        "sub": wb.sub,
        "bul": wb.bul,
        "eq": wb.eq,
        "tab": tab_hook,
        "nums": nums_hook,
        "figura": figura_hook,
        "instante": wb.instante,
        "ponte": wb.ponte,
        "parte": parte_hook,
        "slide": slide_hook,
        "cap": cap_hook,
        "imagem_palco": imagem_palco_hook,
        "rap_fig": rap_fig,
        "FALAS": FALAS_DICT,
        "fala": fala_hook,
    }

    # Pequeno ajuste para o loop `for i, f in enumerate([...], 1): n.story.append(Paragraph(f, S_BUL, bulletText=f"{i}."))`
    body_code = body_code.replace(
        'n.story.append(Paragraph(f, S_BUL, bulletText=f"{i}."))',
        'wb_bul_num(i, f)'
    )
    exec_env["wb_bul_num"] = lambda i, f: wb.bul(f, numbered=False) if i == 0 else wb.p(f"<b>{i}.</b> {f}")

    # Garantir que FALAS seja populado no exec_env quando atribuído no script
    body_code = body_code.replace("FALAS = {", "FALAS.update({").replace("}\n\n\ndef fala(num):", "})\n\n\ndef _unused_fala(num):")

    exec(body_code, exec_env)

    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_LOCAL))
    print(f"[OK] Guia de Estudos Word atualizado salvo em: {OUT_LOCAL} ({OUT_LOCAL.stat().st_size:,} bytes)")

    try:
        shutil.copy2(str(OUT_LOCAL), str(OUT_ONEDRIVE))
        print(f"[OK] Cópia atualizada no OneDrive: {OUT_ONEDRIVE}")
    except Exception as e:
        print(f"[AVISO] Não foi possível sobrescrever no OneDrive ({e}).")


if __name__ == "__main__":
    build_word_document()
