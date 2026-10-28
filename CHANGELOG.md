# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-10-28 — Sequência negativa: o porquê do 120 Hz antes do espectro

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`,
`src/report/js/tcc.js`, `src/report/js/palco.js`, `src/report/js/seq.js` (novo)

O capítulo 4 do palco abria no espectro, que mostra o 120 Hz sem dizer de
onde ele vem. Agora são cinco passos na Barra 6 (trifásica × bifásica):
v_abc desequilibrado; animação da positiva e da negativa vistas da rede e
do PLL (painel `seq`, ilustrativo, sem número); v_d e v_q do inversor
oscilando a 120 Hz; v_q como entrada do PI e o pico do erro (7,3° ×
96,0°); por fim, o espectro com a matriz da Tabela 5.3. Os passos ganharam
`sinais`, `xrange` e `cartoes`; v_abc é embutido só para os dois casos da
Barra 6 (`ABC_CASOS`). `verifica_palco.py` sem falhas.

## 2026-10-28 — Código de rede: reativo no passo dos curtos fora da região e área V·iq

Arquivos: `src/report/roteiro.py`, `src/report/js/ons.js`

O passo do 0,09 pu de reativo (antes o 4º) entrou no 2º, o da Barra 7 e
da Linha 7-8 abaixo de 0,2 pu: o capítulo passa de seis para cinco
passos. Para comparar o reativo entre os pontos de falta sem número que
não está no TCC, o painel da rampa ganhou, por caso em cena, o retângulo
da origem ao ponto (V médio, i_q,ref médio), cuja área é V·i_q = Q. As
áreas batem com o Q médio medido (0,09/0,11/0,48/0,43 pu). O passo 3
ganhou a frase da área. `verifica_palco.py` sem falhas.

## 2026-10-25 — Sem a aba Análise TCC; ONS e ganhos nas abas por cenário

Arquivos: `src/report/renderer.py`, `src/report/js/navegacao.js`,
`src/report/js/eventos.js`, `src/report/js/palco.js`,
`src/report/js/ons.js`, `src/pipeline/chart.py`,
`src/config/settings.py`, `src/config/__init__.py`

Revisão do painel contra o deck da defesa. A aba "Análise TCC" saiu: o
palco ("Modo apresentação") já mostra os mesmos capítulos, e a página
passa a abrir no Resumo. O "+ comparar com…", que só a aba tinha, saiu
junto. O envelope de trip da IEEE 1547 no |V| Bus 2 deu lugar à curva de
suportabilidade do ONS (Figura 2.1), que é a usada no TCC e no deck. O
Resumo ganhou o card "Suportabilidade ONS" (dentro/fora, mesma conta do
capítulo Código de rede; B7 e L7-8 fora, B6 e L8-9 dentro). Kp, Ki, ωn e
ξ do modo ativo aparecem ao lado do toggle PLL (460 / 105.820 / 325,3 /
0,707 e 92 / 21.164 / 145,5 / 0,316, como no slide 11). `verifica_palco.py`
sem falhas, sem erro de JS. Fica para depois, com prévia: a rampa i_q × V
por cenário.

## 2026-10-25 — Gráficos: vírgula decimal e leitura no projetor

Arquivos: `src/report/js/tcc.js`, `src/report/renderer.py`,
`src/pipeline/chart.py`, `src/pipeline/spectrum.py`

Revisão dos gráficos do palco. Os eixos saíam com ponto decimal (0.25,
1.5) enquanto cartões e texto usam vírgula: `separators=",."` no palco, na
aba Análise TCC e nas abas Inversor e Sistema. O cursor do fasor virou
linha cinza tracejada (a preta cortava "Potência ativa P"). O rótulo de
cada painel subiu 12 px, com margem de cima 44 px nos gráficos de dois
painéis, para não colar no número do topo do eixo; o vão entre os
painéis tem ao menos 48 px e os tempos da Energização se afastam pela
altura do painel (colavam em 1280×720). No palco, curvas de
3 px e fonte proporcional à altura do gráfico (14 a 18). A faixa da falta
fica só dentro de cada painel. As setas de retorno à faixa de 2°
(Localização, Compromisso, Perda de sincronismo) foram para uma faixa
própria acima do eixo do erro, fora das curvas, escolhida por prévia.
Recusados nas prévias: espectro em hastes ou com pontos e rótulo direto
nas curvas. `verifica_palco.py` sem falhas.

## 2026-10-25 — Palco: Código de rede em seis passos, com fecho

Arquivos: `src/report/roteiro.py`, `src/report/js/ons.js`,
`src/report/js/palco.js`, `src/report/js/navegacao.js`,
`src/report/renderer.py`

A tela mostrava tudo de uma vez (parágrafo, dois gráficos e quatro
cartões), sem os dois argumentos mais fortes do deck. Agora são seis
passos: a regra sozinha (região e rampa, sem casos); Barra 7 e Linha 7-8
abaixo de 0,2 pu e conectadas com i<sub>q</sub> = 1 pu; os quatro casos,
com a Barra 6 a 0,72 contra 0,76 pu da rampa; o dilema, com a Barra 7
realçada e "0,09 pu" de reativo com seta ao ponto (texto da Fig. 5.8);
os outros curtos acesos, com assimétricas e perda de sincronismo (§5.5);
e o fecho, com o gráfico velado e um cartão com a frase da Conclusão
("essa pergunta é insuficiente"), escolhido entre três prévias. Campos
novos no passo do kind "ons": `realce`, `outros`, `fecho`; no capítulo,
`cartoes_pres=False` (sem cartões no palco) e `destaque.key` (ponto
apontado na rampa). A aba Análise TCC não mudou. `verifica_palco.py`
sem falhas.

## 2026-10-25 — Palco: foco também na Energização, Localização e Sequência negativa

Arquivos: `src/report/roteiro.py`, `src/report/js/navegacao.js`,
`src/report/js/palco.js`, `src/report/js/mapa.js`, `src/report/renderer.py`

A mesma dinâmica de passos com foco foi para os outros capítulos com
gráfico. Energização: foco na partida (0 a 60 ms, depois 0 a 100 ms).
Localização: foco na falta nos passos 1 e 2 e um passo 3 novo, "o erro
sempre volta à faixa de 2°: em até 112 ms", com foco no pós-falta.
Sequência negativa: dois passos novos, a trifásica sozinha e depois as
assimétricas com o "> 250×", foco em 100 a 140 Hz. Em todos os
capítulos, o último passo fica sem foco, com o gráfico inteiro. O texto
"passo N de M · seta → avança" virou uma barra em segmentos que enche até
o passo atual, com "k de n" embaixo, no palco e no mapa (`_passoInd` em
`navegacao.js`, CSS `.passo-*` no `renderer.py`; escolhida entre três
prévias). Revisão dos textos contra o deck e o TCC: "escorregamento de
ciclo", "sintonia nominal" na 1ª menção, retenção de v<sub>d</sub> na ordem
nominal/inadequada, i<sub>q,ref</sub> explícito no Código de rede e cartão
"Pico do erro de fase", como no slide 19. `verifica_palco.py` sem falhas.

## 2026-10-25 — Palco: passos com foco no Compromisso e na Perda de sincronismo

Arquivos: `src/report/roteiro.py`, `src/report/js/tcc.js`,
`src/report/js/navegacao.js`, `src/report/js/fasor.js`

As duas telas apareciam inteiras de uma vez, e a do Compromisso já
anunciava a perda de sincronismo no cabeçalho. Agora cada uma tem 3 passos
(nominal sozinha, entra a inadequada, frase-ponte ou fecho). Campo novo
`foco` no passo esmaece o gráfico fora da janela que importa; campo
`destaque` no passo faz o 66,8% aparecer só no fecho da Perda de
sincronismo. O texto corrido da aba Análise TCC não mudou.

## 2026-10-24 — Palco: Perda de sincronismo depois do Compromisso

Arquivos: `src/report/roteiro.py`

O palco mostrava a perda de sincronismo da sintonia inadequada (§5.4) antes
do capítulo em que ela filtra melhor o 120 Hz (§5.3), e o capítulo favorável
soava como defesa de algo já derrubado. A ordem passou a seguir o TCC:
Sequência negativa → Compromisso → Perda de sincronismo. O título do
Compromisso virou "Ganho menor filtra melhor o 120 Hz" e a última frase
virou ponte ("Mas, na trifásica da Barra 7, a mesma sintonia perde o
sincronismo").

## Entradas anteriores

- [2026-10-24](docs/changelog/2026-10-24.md) — palco com passos, fasor,
  mini-mapa e números de destaque; marcação da acomodação na Energização;
  JS em arquivos, `verifica_palco.py`, telas menores, matriz da sequência
  negativa.
- [2026-10-21](docs/changelog/2026-10-21.md) — capítulo "Faltas destacadas"
  (unifilar com os quatro pontos) e curva de suportabilidade no "Código de rede".
- [2026-10-20](docs/changelog/2026-10-20.md) — indicadores do Cap. 5 no painel,
  casos do TCC em destaque, aba "Análise TCC", modo apresentação (palco branco),
  rampa do ONS e rótulo do mouse.
- [2026-10-03 a 2026-10-16](docs/changelog/2026-10-03_16.md) — Plotly embutido
  no HTML (abre sem internet); fix da escala de P e Q do UFV.
- [2026-08-17 a 2026-08-18](docs/changelog/2026-08-17_18.md) — fix do filtro
  do toggle PLL na carga inicial, título do eixo X do espectro, aba "Sistema
  9-Bus" renomeada para "Barras de Geração".
- [2026-08-11](docs/changelog/2026-08-11.md) — tabela de critérios na legenda
  da tabela de harmônicas; FFT mede a frequência real por segmento (abc).
- [2026-08-09](docs/changelog/2026-08-09.md) — medição de harmônicas pelo
  IEEE 519 §4.1 (3 bins RMS, janela retangular) e relaxamento ×1,5 na falta;
  remoção dos cards de erro de
  ângulo (grupo "Desempenho do PLL": IAE/ISE/tₛ/pico/Erro R.P.), sem base
  bibliográfica que os sustentasse como métrica de desempenho.
- [2026-08-05](docs/changelog/2026-08-05.md) — linha de 0 Hz (fundamental em
  DC) na tabela dq, tabela de harmônicas separada em abc e dq.
- [2026-08-03](docs/changelog/2026-08-03.md) — card e item de diagnóstico
  "Topologia" (line7_8 vs. line8_9, circuito único vs. duplo).
- [2026-08-02](docs/changelog/2026-08-02.md) — teto fixo em 1 pu no eixo Y
  do espectro FFT, legenda explicada da tabela de harmônicas.
- [2026-07-28 a 2026-07-30](docs/changelog/2026-07-28_30.md) — faixa de
  frequência ONS §5.2.1 no painel "Frequência PLL" (depois removido),
  destaque normativo (IEEE 519/1547) na tabela de harmônicas, remoção do
  painel "Frequência PLL".
- [2026-07-25](docs/changelog/2026-07-25.md) — eixo Y com nome+unidade,
  título branco fix, remoção do overlay "Comparar PLL", cards de tensão
  mínimo → média (V médio / V residual médio).
- [2026-07-18 a 2026-07-24](docs/changelog/2026-07-18_24.md) — terminologia
  "sintonia inadequada", remoção dos ícones emoji dos botões/abas, remoção
  das métricas ΔP/ΔQ UFV, cards/diagnóstico movidos para a aba Resumo.
- [2026-07-15](docs/changelog/2026-07-15.md) — espectro FFT multi-modo
  (a/b/c/d/q) + tabela de harmônicas, abas de gráficos + aba Resumo + cards
  clicáveis.
- [2026-07-14](docs/changelog/2026-07-14.md) — regime sem tₛ, cards de
  severidade renomeados para "V residual", Vmin das Barras 1 e 3.
- [2026-07-12](docs/changelog/2026-07-12.md) — export de correntes/tensões
  abc, T_SETTLE fora de todos os cálculos, espectro de Fourier segmentado.
- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
