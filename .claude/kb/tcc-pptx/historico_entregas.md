---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

## 2026-10-28: ONS enxugado em 2 slides (15-16) e Conclusão (20) focada nos 3 pontos (entregue)

- Pedido do usuário: (1) condensar a sequência ONS + Sistema completo em 2 slides
  enxutos (saíram "Referência pelo ONS" e "Lógica em blocos", deck 31 → 29);
  (2) no slide de Conclusão (antigo 22, atual 20, "Síntese dos resultados"),
  remover os 3 valores soltos no topo dos cartões (`9,2% Vd`, `250× mais 120 Hz`,
  `66,8% do tempo`) e focar nos 3 pontos principais de apoio à conclusão já
  escritos no slide (`1. Faltas simétricas`, `2. Faltas assimétricas`,
  `3. Sensibilidade de ganhos`), redimensionados com divisória e destaques em negrito.
- Slide 15 ("Submódulo 2.10 do ONS"): manteve `ons_logica_defesa.svg` (gráfico
  aprovado) e dividiu o rodapé em 2 caixas lado a lado ("Por que priorizar o
  reativo?" e "Quem orienta as correntes?").
- Slide 16 ("Sistema completo"): manteve a Fig. 4.2 do TCC e atualizou o
  cartão 2 ("2. Referência pelo Submódulo 2.10: Antes fixas (P = 1 pu, Q = 0),
  i_d,ref e i_q,ref seguem a tensão V_PCC"). Roteiros PDF/Word sincronizados.
- e1306f85… → d5ae8c30… (backup `_20261028_005224`) → 7d7d9daca13d2baeecd6041af304f3e1
  (backup `_20261028_012205`). check_pptx 0 falhas, 0 avisos no 20; tempo 25,1 min.
  Staging `C:\Temp\defesa_ons_2slides\` e `C:\Temp\defesa_s20_conclusao\`.

## 2026-10-28: slide 21 (demo) só com a tela e o botão (entregue)

- Pedido do Victor: o slide da demo vira só a entrada para o painel, sem
  informação. Saíram os 3 cartões de resultados, a faixa "Suporte à
  Arguição" e a legenda; frase de abertura neutra "Os resultados seguem no
  painel interativo, em modo apresentação"; captura (6,19 × 3,80 in)
  centrada com o botão logo abaixo, na largura da moldura. Notas intactas.
- 5ae82aec… → e1306f85c2df6b0ffc5ee680dfda66eb, backup `_20261028_002251`.
  Diff: só o slide 21. check 0 falha. Staging `C:\Temp\defesa_demo21\`
  (`gen_demo21.py`).

## 2026-10-27 (noite): v_d e v_q com o ângulo do PLL no slide 6 (entregue)

- Imagem `assets/diagrams/park_vdq_pll.png` (STIX, θ_PLL em laranja, como a
  matriz) sob a Eq. (3.5); legenda "..., com o ângulo do PLL"; fala do Bruno
  com v_d/v_q. "K_pd = 1" do slide 10 mantido: está na Eq. (3.10) do TCC.
- 5b204ca9… → 51ddb76fbf68fa77f7582c1201cbcfef, backup `_20261027_221024`.
  Diff: só o slide 6. check 0 falha; 26,2 min. Staging
  `C:\Temp\defesa_kpd\` (`gen_park.py`, `gen_eq_png.py`).

## 2026-10-27: slide novo "Filtro LCL" (13), deck 30 → 31 (entregue)

- Exceção de método aprovada pelo Victor: equações de projeto do LCL
  (ripple, ressonância, Rd = 5%) fora do TCC; na tela só números do TCC.
  Cópia do 13 com `assets/diagrams/lcl_filtro_defesa.svg` (circuito por
  fase com Vcc, régua 60 Hz / ωres / 5 kHz), 4 cartões e 2 caixas de rodapé.
- Junto: 3 cópias empilhadas de Kp/Ki e da barra no "Controle de corrente"
  (agora 14) viraram 1; a fala dele deixa ωres e Lest para o 13.
- 43840708… → de0dc1b4477cca637437d1195c61bf52, backup `_20261027_003108`
  (1ª entrega abortou: PowerPoint do `-Pdf` ainda saindo). Diff: só o
  previsto. check_pptx 0 falhas; tempo 24,7 → 25,9 min. Staging
  `C:\Temp\defesa_lcl\gen_lcl.py`.

## 2026-10-26: revisão final de auditoria sobre a base de 25/10 (entregue)

- Base restaurada do backup _20261025_162639 (MD5 21891b35…, com diagramas dq no 6 e Cambria Math em 7, 10-14, 23-24).
- Correções aplicadas (C:\Temp\defesa_final_revisao\gen_revisao_final.py): figura da cadeia causal no 4 sem sobreposição e com subscritos reais; rodapé do 19 para o Modo Apresentação; slide 20 com print 16:10 do Modo Apresentação (8 capítulos), frase de abertura, legenda e 3 cartões sem BAD_PLL/68 MB/travessões; slide 21 (9,2% Vd, escorregamento de ciclo, remoção de barra duplicada); limpeza de termos proibidos, travessões e botões de navegação em 22-30; notas sincronizadas nos 30 slides (24,7 min, 48% Bruno / 52% Victor).
- check_pptx --tcc 0 falhas; MD5 901949dd… → e931c642978da38d41586a4ebb6aa93b, backup _20261026_170904.

## 2026-10-25: sigla de transitórios eletromagnéticos fora do deck (entregue)

- Pedido do Oscar. 7 trocas: legenda do 20 e notas do 20, limites do 22 e
  notas do 22, subtítulo e "Passo de integração" do 23, notas do 28.
- 21891b35… → 67a4ceefd33f3c4a486240436d19eede, backup `_20261025_162639`.
  Diff: só as 7 trocas. Staging `C:\Temp\defesa_semsigla\gen_sem_sigla.py`.

## 2026-10-24 (noite): referencial dq ao lado da equação, slide 6 (entregue)

- Moldura, cartões e rodapé intactos. Equação 9,09 → 5,45 in à esquerda,
  divisória `CBD5E1` em x = 7,10, e dois desenhos à direita (variante "E",
  escolhida entre A, B, C, D, E): vetor v em dq girante + senoides → constantes.
- a018e6d77e7e4161267d4dfd22d2370f → 21891b35dc5a0cfa7f6e0ac426ef38f5,
  backup `_20261024_204055`. Diff: só as 2 imagens novas no 6. Staging
  `C:\Temp\defesa_dq\` (`gen_svgs.py`, `gen_dq.py BC_largo`).

## 2026-10-24: padronização das equações, slides 7, 10-14, 23-24 (entregue)

- Só runs de texto, nenhuma caixa mexida. Destaque (7, 12, 13, 14): Cambria
  Math com letras em itálico e números/rótulos retos, centralizado (o 7 era à
  esquerda). Texto: K<sub>pPLL</sub>/K<sub>iPLL</sub> do TCC (10, tabela do 11, 23) e
  subscrito/sobrescrito onde faltava (12-14, 23-24). Regra em `design.md`.
- 95f02b8b2752954bba02f9cd33e7c27d → a018e6d77e7e4161267d4dfd22d2370f,
  backup `_20261024_150810`. Diff: só 10, 13, 23 ("²" → sobrescrito).
  Staging `C:\Temp\defesa_equacoes\gen_equacoes.py`.
- Ficam: a sigla de transitórios eletromagnéticos/"params.m" no 23, cabeçalhos "Vd/Vméd/Pméd" no 24, espaço
  levemente apertado antes do "+" na equação característica do 7.

## 2026-10-21 (madrugada): layout do 20 e frase de abertura em 20-22 (entregue)

- 20 (demo): só layout, texto intacto (diff sem diferença de texto): grade de
  2 colunas 5,82, moldura da figura, caixas chapadas, Arial → Calibri do tema,
  corpo 11 → 12 pt, legenda 11 pt. 20, 21 e 22 ganharam título curto + frase
  de abertura. Staging `C:\Temp\defesa_s20\gen_s20.py` e `defesa_s22\gen_s22.py`.
- 1ª entrega (20-21): 7377235a… → 869545bf…, backup `_20261021_005432`.
  2ª (22): o canônico virou c581ac8c… só por regravação do PowerPoint (diff
  vazio); entregue → 151946bf8daca45e2b2586816a7c99a8, backup `_20261021_005913`.
- Ficam na tela, para a passada de texto: travessão nos cartões do 20,
  "BAD_PLL" no 20, a sigla de transitórios eletromagnéticos na legenda do 20 e nos limites do 22.

## 2026-10-21: lógica do ONS e sistema completo, slides 14-17 (entregue)

- 14 "Referência pelo ONS" (`referencia_corrente_ons.svg`), 15 "Dentro do
  Submódulo 2.10" (`ons_logica_defesa.svg`, gráfico aprovado "não tirar";
  1ª versão em caixas recusada), 16 "Lógica em blocos"
  (`ons_fluxo_defesa.svg`), 17 "Sistema completo" (Fig. 4.2 do TCC).
  Notas do 13 enxugadas. 26 → 30 slides. Staging `C:\Temp\defesa_ons\gen_ons.py`.
- Canônico mudou duas vezes no caminho: c8e650c4… (regravação do PowerPoint
  ao reabrir a entrega anterior) e ab12935c… (outra sessão, 00:05: demo
  antes da energização). Re-staging sobre ab12935c…, mesmo script. MD5 →
  b46729b611a54fcdf760d4c00e70eca4, backup `_20261021_003827`. A 1ª
  tentativa do entrega.ps1 abortou ("PowerPoint não fechou", sem processo);
  a 2ª passou.
- check_pptx 0 falhas (13-17); slide-validator: "antes fixas (P = 1 pu,
  Q = 0)" mantido por ser a exceção aprovada do 12; vírgula do cartão do 14
  virou "e"; falas do 15/16 sem repetição. Fala: 29,9 min (limite 30), com
  os slides 5, 6, 7 e 9 ainda sem fala e o 10 com 384 palavras.

## 2026-10-20: slide 12 dividido, 12a e 12b (entregue)

- 12 = "Referência de corrente" (novo, cópia do 11): diagrama da 1ª versão
  no PSIM (`assets/diagrams/referencia_corrente_psim.svg`, "t = 35 ms"
  aprovado), Eq. 3.9 invertida, "Por que o PLL importa aqui?". 13 =
  "Controle de corrente" (o 12 antigo): Fig. 3.1 do TCC no lugar da 4.2,
  cartões PWM/LCL/PI com Kp e Ki em Cambria Math, "Por que dois PIs?".
  Slides 13+ desceram 1 (26 slides). Staging `C:\Temp\defesa_inversor\`.
- 1ª entrega abortou: o canônico mudou no meio (outra sessão, slides 2-4,
  MD5 1e172cac… → d00bc679…). Re-staging sobre a versão nova, mesmo
  script: MD5 d00bc679… → aaac0979c795e7889e5b4407e6395af7, backup
  `_20261020_235714`. diff: 2-4 intactos, 12+ só o deslocamento previsto.
- check_pptx 0 falhas; slide-validator sem bloqueio (2 falas reescritas
  para a redação do TCC: "o quarto da figura" saiu; erro de sincronismo
  "compromete o desacoplamento das potências"). Fala: 27,9 min.

## 2026-10-20: slide 14, fluxo de análise (entregue)

- "Fluxo de análise" + frase de abertura; cartões Simulink, Arquivos CSV,
  Python, Painel interativo (§4.3.3); tabela 2 × 5 das métricas (opção T de
  2, a faixa de texto solta foi recusada como feia); rodapé "Dos dados aos
  resultados" (opção B de 2). Sai a última ocorrência da sigla de transitórios eletromagnéticos do deck. Ajuste do
  slide-validator: "Após o 1º ciclo da falta" (o 1º ciclo fica fora).
- Staging `C:\Temp\defesa_fluxo\` (`gen_fluxo.py`): MD5 74cc0096… →
  a2b58bdf67e259a7e9ba0c649a8d4deb, backup `_20261020_001615`. diff: só o
  slide 14; check 0 falha; 25,6 min.
- **Sobrescrita**: às 00:17:37 um PowerPoint ainda aberto na versão antiga
  regravou o canônico (slide 14 antigo, notas editadas à mão). Reentregue
  sobre essa versão: só a tela nova, **notas do Victor mantidas** (ainda
  citam "duas taxas" e "nenhuma métrica lida à mão", fora do TCC). MD5
  1a121959… → 28fe61546aa9637f17d96d9f6768c9e7, backup `_20261020_001847`.
  Lição: depois da entrega, conferir o canônico de novo antes de encerrar.

## 2026-10-20: slide 14 revertido ao original (entregue)

- O Victor corrigiu a leitura: o fluxo do slide 14 é o da simulação
  consolidada no Simulink, não as ferramentas da modelagem. Slide 14 volta
  ao original (com "1. Simulação" e a sigla, a decidir na análise conjunta); as
  trocas da sigla nos slides 3, 4 e 8 ficam. Montado a partir do deck
  anterior + só o grupo `g_emt` de `gen_pipeline.py`.
- O canônico tinha sido regravado depois da entrega anterior (PowerPoint ao
  reabrir e OneDrive: 324c27d6… → 2054f41f… → a2a384ea…, conteúdo igual).
  MD5 a2a384ea… → 74cc0096b7dacaa2c17e990b344ad524; backup `_20261020_000011`.
  diff: só o slide 14 (e ordem de formas no 13); check 0 falha.

## Antes de 2026-10-20

Entregas de 2026-10-19 em [[defesa-historico-entregas-10-19]]; de 2026-10-17
e 2026-10-18 em [[defesa-historico-entregas-10-17-18]]; de 2026-10-16 em
[[defesa-historico-entregas-10-16]].
