---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

## 2026-10-21 (madrugada): layout do 20 e frase de abertura em 20-22 (entregue)

- 20 (demo): só layout, texto intacto (diff sem diferença de texto): grade de
  2 colunas 5,82, moldura da figura, caixas chapadas, Arial → Calibri do tema,
  corpo 11 → 12 pt, legenda 11 pt. 20, 21 e 22 ganharam título curto + frase
  de abertura. Staging `C:\Temp\defesa_s20\gen_s20.py` e `defesa_s22\gen_s22.py`.
- 1ª entrega (20-21): 7377235a… → 869545bf…, backup `_20261021_005432`.
  2ª (22): o canônico virou c581ac8c… só por regravação do PowerPoint (diff
  vazio); entregue → 151946bf8daca45e2b2586816a7c99a8, backup `_20261021_005913`.
- Ficam na tela, para a passada de texto: travessão nos cartões do 20,
  "BAD_PLL" no 20, "EMT" na legenda do 20 e nos limites do 22.

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
  resultados" (opção B de 2). Sai o último "EMT" do deck. Ajuste do
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
  ao original (com "1. Simulação EMT", a decidir na análise conjunta); as
  trocas de "EMT" dos slides 3, 4 e 8 ficam. Montado a partir do deck
  anterior + só o grupo `g_emt` de `gen_pipeline.py`.
- O canônico tinha sido regravado depois da entrega anterior (PowerPoint ao
  reabrir e OneDrive: 324c27d6… → 2054f41f… → a2a384ea…, conteúdo igual).
  MD5 a2a384ea… → 74cc0096b7dacaa2c17e990b344ad524; backup `_20261020_000011`.
  diff: só o slide 14 (e ordem de formas no 13); check 0 falha.

## 2026-10-19 (noite, revertida em 2026-10-20): slide 14, fluxo de trabalho e métricas; "EMT" fora do deck (entregue)

- Slide 14: título curto "Fluxo de trabalho" + frase de abertura; 4 cartões =
  plataformas da §4.2 na ordem da §4.4 (Python, PSIM, MATLAB/Simulink, painel
  em Python); tabela de métricas com as definições do Cap. 5 (retenção, pico a
  partir do 1º ciclo, retorno a 2° da eliminação, 120 Hz, P e Q médias);
  pergunta do painel à direita (§4.3.3). Saem "EMT", "duas taxas", "sinais
  da rede" e o cartão "mesmo código". Notas reescritas (220 palavras).
- "EMT" fora do deck a pedido do Victor (o TCC ainda usa): slide 4 na tela
  ("Identificar o que compromete o rastreamento de fase"), notas 3 e 4
  ("simulação computacional"), notas 8 sem a frase das ferramentas.
- MD5 87539413… → 324c27d6af1d452eec564a7023ff6151; backup
  `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261019_235430.pptx`. A 1ª
  entrega abortou (PowerPoint não fechou em 90 s); a 2ª passou.
- diff_slides: só 3, 4, 8 e 14. slide-validator sem bloqueador; check 0
  falha; 26,0 min. Staging `C:\Temp\defesa_pipeline\gen_pipeline.py`.

## 2026-10-19: slide 13, protocolo com matriz de cenários (entregue)

- Título curto "Protocolo de contingência" + frase; linha do tempo com
  0,1 s de inicialização (exceção aprovada, só no MÉTODO); matriz 3 × 8
  no lugar dos cartões (Tabela 4.1 + "I" na monofásica B7); sai a pré-falta
  40/79 ms e "12 ciclos"; entra "Faltas assimétricas" (§4.3.4). Staging
  `C:\Temp\defesa_metodo\` (`gen_metodo.py`): MD5 73188b08… (só regravado)
  → 87539413354045f46e3958a516e71d15, backup `_20261019_233408`. diff: só o
  slide 13; slide-validator sem bloqueio; check 0 falha; 25,7 min.

## 2026-10-19: slide 10, etapa "Tensão em pu" e fontes nas notas (entregue)

- Pedido do Victor: deixar frisado que os ganhos são calculados em pu (a
  tensão é dividida por 16.329,93 V de pico na entrada do PLL, antes de
  Park). Opção B de 2: 4 etapas (1. Tensão em pu, 2. Linearizar, 3. Forma
  canônica, 4. Fixar ξ), régua vira etapa 5. Notas citam Ogata, Alves/Dias/
  Rolim 2020 e Teodorescu/Liserre/Rodriguez 2011, como a §3.4; saiu a
  definição de ts que não está no TCC (slide-validator). Staging
  `C:\Temp\defesa_s10pu\`: MD5 a20d3094… (só regravado pelo PowerPoint,
  conteúdo igual à entrega anterior) → 88e8f55bd32bc280ad4b979f0eeeb928,
  backup `_20261019_225558`. diff: só o slide 10; check 0 falha; 25,4 min.

## 2026-10-19: slide 10 em dois, sintonia do PLL e duas sintonias, 28 → 29 (entregue)

- Pedido do Victor: dizer como se chegou aos ganhos, não só jogá-los.
  Direção B de 3, layout B de 2: 10 "Sintonia do PLL" (passos 1-3 da §3.4,
  régua do ts `pll_ts_regua_defesa.svg`, conta até os ganhos); 11 novo
  "Duas sintonias do PLL" (tabela, 2ω0 = 2,32·ωn, "Por que reduzir os
  ganhos?"). Notas novas, com a escolha do ts explicada pelo TCC (saíram
  16,7 ms e "mesma rede, mesmo inversor, mesma falta", fora do TCC).
  Staging `C:\Temp\defesa_s10\`: MD5 f59e7627… → 6a22988e6be3d7d1e40cf5f3f3a7ee50,
  backup `_20261019_223544`. Slides 12-29 = antigos 11-28 (conferido por
  script); check_pptx 0 falhas; slide-validator sem bloqueio (2 ajustes de
  redação literais ao TCC aplicados); 24,8 min.

## 2026-10-19: slide 9, título curto e bancada espelhada (entregue)

- Opção B de 3 ("Bancada do PLL"). Pedido do Victor: geração à esquerda e
  rede à direita, impedâncias junto (`pll_bancada_duas_fontes.svg`, linha
  de cima espelhada, mesmo PNG 1644x1356). Staging `C:\Temp\defesa_titulo9\`:
  MD5 fd61897d… → f59e76279ebd1d783e3cd4ccf9db8052, backup `_20261019_220257`.
  diff: só o slide 9; check_pptx 0 falhas; slide-validator sem bloqueio.

## 2026-10-19: título curto e frase de abertura nos slides 6, 7 e 8 (entregue)

- Revisão slide a slide pedida pelo Victor, padrão do slide 5 por
  `Edicao.frase_abertura` (novo). Slides 6 ("Transformada de Park", var. A)
  e 7 ("Estrutura do SRF-PLL", var. D) em `C:\Temp\defesa_titulo6\`: MD5
  0c7c30ea… → 2388670c95e82fc71c0b8e46abafc25e, backup `_20261019_213908`.
  Slide 8 ("Sistema IEEE 9 barras", var. C) em `C:\Temp\defesa_titulo8\`:
  → fd61897d96d28d9133952e81c4cc92f2, backup `_20261019_214732`.
- diff: só os títulos; check_pptx 0 falhas; slide-validator sem bloqueio.
  `entrega.ps1` abortou 2× (PowerPoint do finalize ainda saindo): espera
  passou de 30 para 90 s, e a entrega do 8 passou de primeira.

## 2026-10-19: título curto e frase de abertura no slide 5 (entregue)

- Pedido do Victor: título menor. "Fonte renovável" + frase em 20 pt
  com barra azul (opção C de 4 variantes, `folha_opcoes.py` novo).
  Staging `C:\Temp\defesa_titulo5\`. MD5 f2c78deb… → 0c7c30ea9529f85012aa5ad8452b810c;
  backup `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261019_212538.pptx`.
  diff: só o título do slide 5; check_pptx 0 falhas; slide-validator sem bloqueio.

## Antes de 2026-10-19

Entregas de 2026-10-17 e 2026-10-18 em [[defesa-historico-entregas-10-17-18]];
de 2026-10-16 em [[defesa-historico-entregas-10-16]].
