# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-10-21 — Curva de suportabilidade no capítulo "Código de rede"

Arquivos: `src/pipeline/indicadores.py`, `src/pipeline/loader.py`,
`src/report/renderer.py`, `src/report/roteiro.py`

O capítulo do ONS ganhou, ao lado da rampa de corrente reativa, a curva de
suportabilidade a subtensões (Figura 2.1) com a tensão da fase mais
afundada no inversor de cada caso. Etiqueta "dentro/fora da região" nos
chips e cartões; anel vermelho na rampa para os casos fora; faixas por
regime na rampa. "+ Mostrar os outros curtos" acende os demais cenários sem
destaque, e o mouse sobre "Fora/Dentro da região · N casos" lista e filtra
os casos no gráfico. Nova receita `suportabilidade_ons` (60 Hz por fase,
janela de 1 ciclo); a série entra em `tccInd.lvrt` (~0,2 MB no HTML).

## 2026-10-21 — Capítulo "Faltas destacadas"

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`

Primeiro capítulo da aba Análise TCC e do modo apresentação: antes dos
resultados, o unifilar mostra onde as faltas foram aplicadas (Barra 7, Linha
7-8, Linha 8-9 em circuito duplo, Barra 6). Seis passos: visão geral, um
por ponto e resumo. Cada passo traz um cartão com texto, as faltas e
sintonias simuladas e "Abrir no painel →", além de uma régua do
afundamento mais profundo ao mais raso. A seta → percorre os passos antes de
trocar de capítulo. Clicar na barra, na linha ou no pino da régua pula para
o ponto. Saiu de três prévias standalone aprovadas pelo usuário.

## 2026-10-20 — Modo apresentação em palco branco

Arquivo: `src/report/renderer.py`

O palco escuro não agradou. Entre três prévias claras (branco puro, cinza
com cartões, faixa azul-marinho no topo), o usuário escolheu o branco puro:
fundo branco, título escuro, destaque azul, curvas com as cores do tema
claro. O palco fica claro mesmo com o site em dark mode.

## 2026-10-20 — Modo apresentação, rampa do ONS e rótulo do mouse

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`

- Botão "Modo apresentação" no cabeçalho: o site vira um palco escuro em
  tela cheia, um capítulo do Cap. 5 por tela, com os sinais empilhados
  (erro de fase + v_d ou + P), legenda, chips e mini-cartões, sem rolagem.
  Seta ou PageDown avança, Esc sai.
- Capítulo do ONS: as barras deram lugar à rampa do Submódulo 2.10 com o
  ponto de operação de cada trifásica.
- Cores distintas (amarelo → índigo) nos capítulos só com casos nominais.
- Rótulo do mouse legível em todas as abas: fundo sólido, borda azul, fonte
  maior e 3 casas decimais.

Detalhes em `.claude/kb/dashboard/layout/roteiro-casos-tcc.md`.

## 2026-10-20 — Aba "Análise TCC" no lugar da faixa de roteiro

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`

O usuário pediu o roteiro numa aba própria, com mais liberdade para comparar
os gráficos num painel direcionado. A faixa de 9 passos (entrada abaixo)
saiu e a nova aba é a primeira, aberta por padrão:

- 7 capítulos do Cap. 5 (energização, localização, perda de sincronismo,
  sequência negativa, compromisso da sintonia, código de rede, todos os
  casos), cada um com legenda e referência às tabelas e figuras do TCC.
- Cenários sobrepostos no mesmo eixo (azul = nominal, laranja =
  inadequada), seletor de sinal (erro de fase, v_d, P, Q), chips para ligar
  e desligar curvas e "+ comparar com…" para qualquer cenário.
- Mini-cartões por cenário com os indicadores do TCC; o clique abre o
  cenário nas abas.
- Seta ou PageDown troca de capítulo (passador de slides).
- As curvas reaproveitam as figuras já embutidas: o HTML não cresce.

Detalhes em `.claude/kb/dashboard/layout/roteiro-casos-tcc.md`.

## 2026-10-20 — Casos do TCC em destaque e modo roteiro da demonstração

Arquivos: `src/report/roteiro.py` (novo), `src/report/renderer.py`

O painel tem 34 cenários e o TCC discute 17; na defesa, a banca precisa ver
quais são os do TCC, e a demonstração não pode depender de achar cenário no
`<select>` durante a fala. Mudanças:

- Seletor agrupado por seção do Cap. 5 (§5.1 a §5.4) e "Outros cenários
  (fora do TCC)".
- Mapa unifilar: pontos de falta do TCC em azul, os demais esmaecidos (ainda
  clicáveis), com legenda. É a convenção do slide 13 do deck.
- Comparativo: etiqueta `§5.x`, linhas fora do TCC esmaecidas e botão "Só
  casos do TCC", que ordena pelas Tabelas 5.1-5.3.
- Modo roteiro: botão "Roteiro", 9 passos com legenda (cenário, aba, zoom e
  painel), avançados por seta ou PageDown (passador de slides).
- Fixes: `goToChart` voltou a rolar até o painel (quebrado desde 2026-07-24),
  `regime_bad_pll` passou a acender o mapa, e o toggle PLL acha a monofásica
  inadequada da Barra 6 (`1phase_ground`).

Detalhes em `.claude/kb/dashboard/layout/roteiro-casos-tcc.md`.

## 2026-10-20 — Indicadores do Cap. 5 do TCC no painel

Arquivos: `src/pipeline/indicadores.py` (novo), `src/pipeline/loader.py`,
`src/pipeline/chart.py`, `src/pipeline/spectrum.py`, `src/report/renderer.py`,
`src/config/settings.py`, `src/config/__init__.py`, `src/__init__.py`,
`scripts/medir_tabelas_cap5.py`, `scripts/gen_erro_fase.py`

A defesa passa do slide 14 para o HTML ao vivo, e o painel não batia com o TCC.
O erro de fase era `θ̂ − θ_rede` com faixa ±1,15° (pico de 53,1° contra
37,3° na Barra 7 trifásica, e `bus6/2phase` aparecia como "não acomoda", contra
48 ms no TCC), e faltavam os indicadores das Tabelas 5.1-5.3. Mudanças:

- As receitas do Cap. 5 viraram o módulo `indicadores.py`, usado pelo
  dashboard e pelos scripts do TCC. `tabelas_cap5.csv` regenerado com
  diferença zero.
- O erro de fase passa a ser `atan2(v_q, v_d)` da rede, com faixa de 2°, 1º
  ciclo sombreado e linha quebrada nos saltos de ±180°. `TOL_RAD` foi removido.
- Cards novos: "Sincronismo do SRF-PLL", "Tensão e suporte de reativo" e
  "Energização do inversor" (regime), além do item "Sincronismo" na narrativa.
- A tabela comparativa ganhou 9 colunas das Tabelas 5.1-5.3, geradas de
  `_CMP_COLS`.
- A aba Espectro ganhou um destaque com o 120 Hz pela receita do TCC; a tabela
  de harmônicas, que é outro instrumento, continua igual.
- O cabeçalho passou de "UERJ 2025" para "UERJ 2026".

Detalhes em `.claude/kb/dashboard/cards/indicadores-tcc.md`.

## 2026-10-16 — Plotly embutido no HTML (abre sem internet)

Arquivos: `src/report/renderer.py`, `assets/vendor/plotly-2.35.0.min.js` (novo)

O painel vai ser aberto ao vivo na defesa do TCC, e a sala pode não ter
internet: com o `<script src>` do CDN, os gráficos ficavam em branco. O
`_plotly_js_html` embute o plotly.js 2.35.0 (mesma versão do CDN, 4,5 MB) a
partir de `assets/vendor/`; sem o arquivo, volta ao CDN. O HTML passa de
~68 MB para ~73 MB e também renderiza aberto como `file://`.

## 2026-10-03 — Fix: escala de P e Q do UFV

Arquivos: `src/pipeline/pq.py` (novo), `src/pipeline/loader.py`

O subsistema do `.slx` que calcula P e Q (SID 4055) usava ganho 1/√3 nos
dois: P saía ×√3/2 (0,87 pu pré-falta com i_d = 1) e Q ×1,5. O `.slx` foi
corrigido, mas as rodadas existentes não foram re-simuladas: o `SimData`
passa o CSV por `corrige_pq`, que reescala quando o `fault_info.json` não
traz `pq_ganho_p` (P ×2/√3, Q ×2/3). Os gráficos e métricas de potência do
dashboard mudam de valor, não de forma. Detalhe em
`.claude/kb/simulation/export_workflow.md`.

## Entradas anteriores

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
