---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

## 2026-10-29: pandas/Plotly e agente de IA no slide 17 (entregue)

- Pedido do Victor: linha cinza menor nos cartões 3 e 4 do "Fluxo de
  análise" e fala do Bruno (pandas/Plotly; painel em HTML/CSS/JS com agente
  de IA num modelo de harness). Staging `C:\Temp\defesa_s17\gen_s17.py`.
  MD5 b59af1ae… → 308fc43a07db5f4e66d3ded993b5efe2; backup `_20261029_001644`.
  diff: só o 17; check_pptx 0 falhas; fala 25,3 min.

## 2026-10-29: cartão do slide 10 vira ts 20 → 100 ms (entregue)

- Pedido do Victor: o cartão 2ω0 = 2,32·ωn de "Duas sintonias" confundia
  (ωn nominal ao lado da coluna inadequada; o mesmo dado já está no 25).
  Agora "ts: 20 → 100 ms" + "Pelo critério de 1%, ts = 4,6 / (ξωn): o laço
  fica 5 vezes mais lento e leva tanto quanto a própria falta (0,1 s) para
  acomodar"; fala do Victor idem. Exceção registrada em pendências.
  Staging `C:\Temp\defesa_s11\`. MD5 0ca54315… → b59af1ae339189bebef69b86e088b136;
  backup `_20261029_000710`. diff: só o 10; check_pptx 0 falhas; fala 24,8 min.

## 2026-10-28 (noite): bancada do PLL dentro do slide 8 (entregue)

- Pedido do professor: sem slide só para a fonte ideal. O slide 9 "Bancada
  do PLL" saiu (deck 29 → 28); o 8 ganhou a frase "O PLL foi modelado no
  PSIM; a rede, com as máquinas síncronas, vem pronta no Simulink", cartões
  Substituição / PSIM / Simulink e rodapé "Por que dois softwares?" (§4.1 do
  TCC); notas dos dois slides fundidas. Staging `C:\Temp\defesa_ieee9_psim\v2\`.
  MD5 ad173d7c… → 0ca54315d09358fb41466636f37c0e2b; backup `_20261028_235135`.
- diff: só o 8 e o deslocamento do 9 em diante; check_pptx 0 falhas; fala 24,8 min.

## 2026-10-28 (noite): V_dc → V_cc na figura do slide 5 (entregue)

- Pedido do usuário: padronizar corrente contínua como "cc". Só o subscrito
  em `assets/diagrams/vsi_grid_blocos_defesa.svg`; PNG reexportado (3420×1035)
  e trocado na moldura por `troca_imagem.py`. Staging `C:\Temp\defesa_cc\`.
  MD5 938f4ce7… → ad173d7c6c2c2d371cc95844b5523066; backup `_20261028_234806`.
- diff: só a imagem do slide 5; check_pptx 0 falhas. A Fig. 3.2 do TCC
  (`vsi_grid_blocos.svg`) segue com V_dc.

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

## Antes de 2026-10-22

Entregas de 2026-10-20 e 2026-10-21 em [[defesa-historico-entregas-10-20-21]];
de 2026-10-19 em [[defesa-historico-entregas-10-19]]; de 2026-10-17
e 2026-10-18 em [[defesa-historico-entregas-10-17-18]]; de 2026-10-16 em
[[defesa-historico-entregas-10-16]].
