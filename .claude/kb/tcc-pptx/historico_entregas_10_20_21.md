---
name: defesa-historico-entregas-10-20-21
description: "Histórico de entregas ao deck da defesa em 2026-10-20 e 2026-10-21 (slide 12 dividido, slide 14 e fluxo de análise, ONS e sistema completo, frase de abertura em 20-22)"
aliases: [defesa-historico-entregas-10-20-21]
---

# Deck da defesa — histórico de entregas de 2026-10-20 e 2026-10-21

> Continuação de [[defesa-historico-entregas]], mais recente primeiro.

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

