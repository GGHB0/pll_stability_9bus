"""Perguntas e respostas para a defesa: pontos em que a banca pode cruzar deck e TCC."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdfnote import Note, render_preview  # noqa: E402

n = Note(
    title="Defesa do TCC: perguntas e respostas",
    subtitle="Perguntas prováveis da banca, com a resposta apoiada no TCC entregue",
    out=ROOT / "output" / "defesa_qa.pdf",
    meta_left="Victor e Bruno<br/>SRF-PLL na rede IEEE 9 barras",
    meta_right="Preparação da defesa<br/>17 de outubro de 2026",
    running_head="Defesa do TCC: perguntas e respostas",
)

n.h("Como usar")
n.p("Em 17/10/2026 o deck foi alinhado ao TCC entregue (VFinal, 15/10/2026): todo número "
    "e afirmação dos slides e das notas de fala é o do TCC, e o que não estava no TCC saiu. "
    "Nada aqui é para ser dito por iniciativa própria. São respostas prontas para o caso de "
    "a banca perguntar, e cada uma se apoia no texto do TCC.")
n.table(["Pergunta provável", "Resposta curta"], [
    ["1. Quantos cenários foram simulados?", "29: 21 nominais e 8 inadequados"],
    ["2. Por que o objetivo cita sobrecorrentes?", "Elas não se manifestam (Cap. 6)"],
    ["3. Qual o valor de V<sub>cc</sub>, L<sub>1</sub>, L<sub>2</sub>, C<sub>f</sub>?",
     "Estão no modelo; o TCC traz L<sub>est</sub>"],
    ["4. Malha de corrente e PLL com a mesma banda?", "Sim; interação fora do escopo"],
    ["5. O cartão do painel não mostra 9,2%", "É outra métrica, |V| na Barra 2"],
    ["6. 22.547 ou 23.368 MW?", "23.368 MW, do RAP do ONS"],
    ["7. Onde ocorre o cycle slipping?", "Trifásicas severas, sintonia inadequada"],
    ["8. Reativo de 0,09 ou 0,14 pu?", "0,09 pu (versão final)"],
    ["9. E o modo grid-forming?", "Fora da premissa do trabalho"],
], [7.6, 7.1])

n.h("1. Quantos cenários foram simulados?")
n.p("<b>Por que pode surgir.</b> A Tabela 4.1 do TCC entregue diz &#8220;28 cenários "
    "exportados: 21 com sintonia nominal e 7 com sintonia inadequada&#8221;, mas a Tabela 5.3 "
    "já traz a monofásica na Barra 7 com sintonia inadequada (70,6° e 95 ms). O deck não "
    "cita a contagem.")
n.p("<b>Resposta.</b> São 29: 21 com a sintonia nominal e 8 com a inadequada. A monofásica "
    "na Barra 7 com sintonia inadequada foi simulada depois de montada a matriz da Tabela 4.1, "
    "para completar a comparação da Tabela 5.3.")
n.table(["Monofásica na Barra 7", "Pico do erro de fase", "Retorno à faixa de 2°"], [
    ["Sintonia nominal", "89,7°", "46 ms"],
    ["Sintonia inadequada", "70,6°", "95 ms"],
], [6.0, 4.35, 4.35])
n.note("Se pedirem a leitura: o pico cai, mas a recuperação dobra, de 46 para 95 ms. "
       "Não dizer que &#8220;segue a mesma tendência&#8221;.")

n.h("2. Por que o objetivo cita sobrecorrentes?")
n.p("<b>Por que pode surgir.</b> O slide 4 traz o objetivo &#8220;avaliar oscilações de "
    "potência e sobrecorrentes&#8221;, e os resultados não mostram sobrecorrente.")
n.p("<b>Resposta.</b> O próprio Cap. 6 registra essa ressalva: as sobrecorrentes antecipadas "
    "entre os impactos não chegam a se manifestar, porque a arquitetura de controle por "
    "corrente limita a referência antes disso. A referência de corrente reativa satura em "
    "1,0 pu nas faltas mais severas (Tabela 5.2).")

n.h("3. Valores do conversor que não estão no texto")
n.p("<b>Por que pode surgir.</b> O deck traz só o que o TCC traz: L<sub>est</sub> = 30,71 mH, "
    "ω<sub>res</sub> = 9.068,99 rad/s, ξ = 0,707, as resistências de amortecimento e o barramento "
    "CC constante. A banca pode pedir os valores individuais.")
n.p("<b>Resposta.</b> Os valores do modelo de simulação são estes. L<sub>1</sub> + L<sub>2</sub> "
    "dá o L<sub>est</sub> do TCC.")
n.table(["Grandeza", "Valor no modelo", "Observação"], [
    ["V<sub>cc</sub>", "136,36 kV", "90,91 kV do projeto analítico × 1,5"],
    ["L<sub>1</sub>", "30,42 mH", "lado do inversor"],
    ["L<sub>2</sub>", "0,289 mH", "lado da rede"],
    ["C<sub>f</sub>", "42,47 µF", "capacitor do filtro LCL"],
], [3.4, 4.0, 7.3])
n.p("Sobre o barramento CC, a justificativa do TCC (Seção 4.3.2) é que ele foi fixado em valor "
    "constante para manter a margem de modulação necessária e concentrar a análise nos efeitos "
    "de sincronismo e acoplamento com a rede. O fator 1,5 sobre o valor do projeto analítico "
    "não vem do projeto teórico: foi um ajuste manual para estabilizar a simulação. Se a "
    "banca perguntar pelo número, responder com franqueza que é um ajuste de simulação.")

n.h("4. Malha de corrente e PLL com bandas parecidas")
n.p("<b>Por que pode surgir.</b> A malha de corrente tem ω<sub>n</sub> = 4√2·f<sub>g</sub> ≈ "
    "339,4 rad/s e o PLL nominal, 325,3 rad/s. As notas do slide 6 repetem a frase do TCC "
    "(Seção 4.3.2.2): a malha de corrente é &#8220;suficientemente rápida para não se tornar "
    "o gargalo do sistema&#8221;.")
n.p("<b>Resposta.</b> A observação procede: as duas frequências naturais são quase iguais. "
    "Cada malha seguiu a sintonia publicada da sua referência: a de corrente, Alves (2022); a do "
    "PLL, Alves, Dias e Rolim (2020). O trabalho isola a dinâmica do PLL sob falta e não analisa "
    "a interação entre as malhas. Ela cabe na segunda frente de trabalhos futuros (Cap. 7): "
    "varredura da relação de curto-circuito e modelagem por impedância em pequenos sinais.")
n.note("Se a banca disser que o PLL deveria ser bem mais lento que a malha de corrente, "
       "reconhecer. É um critério comum de projeto, mas não está no TCC: tratar como raciocínio "
       "oral, sem citar fonte.")

n.h("5. O cartão do painel não mostra 9,2%")
n.p("<b>Por que pode surgir.</b> Na demonstração (slide 12), as notas citam a retenção do TCC "
    "(9,2% e 8,2%), mas o cartão do painel mostra outra grandeza.")
n.p("<b>Resposta.</b> São métricas diferentes. O cartão &#8220;V residual médio B2&#8221; é a "
    "média do módulo |V| na Barra 2 durante a falta, em pu. O TCC usa a retenção da componente "
    "de eixo direto da tensão durante a falta, em percentual do valor pré-falta.")
n.table(["Trifásica na Barra 7", "Painel (|V| médio, B2)", "TCC (retenção de V<sub>d</sub>)"], [
    ["Sintonia nominal", "0,099 pu", "9,2%"],
    ["Sintonia inadequada", "0,094 pu", "8,2%"],
], [5.0, 4.85, 4.85])
n.note("Na demonstração, não ler o cartão em voz alta. Só responder se perguntarem.")

n.h("6. Número do blecaute de 2023")
n.p("<b>Por que pode surgir.</b> A introdução do TCC traz 22.547 MW (31%), e a Seção 2.4.3 traz "
    "23.368 MW (34,5%). O deck (slide 3) usa o da Seção 2.4.3.")
n.p("<b>Resposta.</b> O número de referência é <b>23.368 MW, 34,5% da demanda do momento</b>, do "
    "Relatório de Análise de Perturbação do ONS (RAP-ONS 00012/2023), descrito na seção dedicada "
    "ao evento. A origem do 22.547 MW (31%) da introdução está a confirmar.")

n.h("7. Onde ocorre o cycle slipping?")
n.p("<b>Por que pode surgir.</b> O título do slide 14 fala em fragilidade estrutural nas "
    "assimétricas, e o gráfico ao lado (Figura 5.18) é de uma falta trifásica.")
n.p("<b>Resposta.</b> No TCC, o escorregamento de ciclo aparece com a sintonia inadequada nas "
    "trifásicas severas: Barra 7 e Linha 7-8. O erro de fase gira continuamente depois da "
    "eliminação e não volta à faixa de 2° até o fim da janela. Nas assimétricas, a fragilidade "
    "é a oscilação de 120 Hz, que a malha PI não rejeita. Na bifásica da Barra 7, o erro chega "
    "a 180° durante a falta com as duas sintonias, mas volta depois da eliminação.")
n.table(["Trifásica na Barra 7", "Retorno à faixa de 2°"], [
    ["Sintonia nominal", "98 ms após a eliminação"],
    ["Sintonia inadequada", "não retorna dentro da janela (até 0,6 s)"],
], [6.0, 8.7])
n.note("O tempo de retorno é contado a partir da eliminação, em 0,4 s. No eixo dos gráficos, "
       "que começa na aplicação da falta, os 98 ms aparecem em torno de 198 ms.")

n.h("8. Reativo na Barra 7: 0,09 ou 0,14 pu?")
n.p("<b>Por que pode surgir.</b> Só se a banca tiver uma versão do TCC anterior à final.")
n.p("<b>Resposta.</b> Vale <b>0,09 pu</b>, que está na versão final (Figura 5.8). O 0,14 pu "
    "vinha de um erro de escala no cálculo de P e Q, corrigido antes da entrega final, e "
    "0,14 ÷ 1,5 ≈ 0,09.")

n.h("9. E o modo grid-forming?")
n.p("<b>Resposta.</b> Está fora do escopo. O Cap. 7 propõe as duas frentes de continuidade "
    "mantendo a premissa de inversores operando como seguidores de rede: trocar a estrutura do "
    "algoritmo de sincronismo (DDSRF-PLL e integradores generalizados de segunda ordem duplos) "
    "e ampliar as condições de rede.")

n.h("Correções possíveis no TCC")
n.p("Só fazem sentido se ainda for possível trocar o arquivo entregue à banca:")
n.p("• <b>Tabela 4.1:</b> regenerar a matriz de cenários (29: 21 + 8) e trocar a figura.<br/>"
    "• <b>Introdução:</b> trocar 22.547 MW (31%) por 23.368 MW (34,5%), citando o RAP do ONS.")

n.refs([
    "ALVES, André Gustavo Pereira. Metodologia para Auto-Ajuste de Controladores de Corrente "
    "em Conversores Fonte de Tensão Conectados a Redes Sujeitas a Distúrbios Harmônicos. "
    "Tese (Doutorado em Engenharia Elétrica), COPPE/UFRJ, Rio de Janeiro, 2022.",
    "ALVES, André G. P.; DIAS, Robson F. S.; ROLIM, Luís G. B. A Smooth Synchronization "
    "Methodology for the Reconnection of Autonomous Microgrids. Journal of Control, "
    "Automation and Electrical Systems, v. 31, p. 665-674, 2020. DOI 10.1007/s40313-020-00576-x.",
    "OPERADOR NACIONAL DO SISTEMA ELÉTRICO (ONS). RAP-ONS 00012/2023: Análise da "
    "Perturbação do dia 15/08/2023 às 08h30min. Relatório de Análise de Perturbação. "
    "Rio de Janeiro: ONS, 2023.",
])

out = n.build()
print(out)
if "--preview" in sys.argv:
    render_preview(out, Path(sys.argv[sys.argv.index("--preview") + 1]))
