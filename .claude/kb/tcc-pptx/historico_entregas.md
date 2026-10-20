---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

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

## 2026-10-18 (noite, 4): slide 5 novo, a fonte antes de Park, 27 → 28 (entregue)

- Pedido do Victor: apresentar a fonte renovável antes do IEEE 9 barras.
  Slide novo (cópia do layout do 6) entre a motivação e Park: Fig. 3.2
  redesenhada (`vsi_grid_blocos_defesa.svg`), 3 cartões e gancho "Como o
  inversor segue a rede?". Primeiro passo com PRÉVIA na skill (v1.2.0).
  Staging `C:\Temp\defesa_fonte\`.
- MD5 antes 2d916e20cfbbe4e70c8e60b3f1904c67, depois
  f2c78deb98e0a2a84df2bdffd6610a9e; backup
  `Defesa_TCC_SRF-PLL_backup_20261018_193851.pptx`. slide-validator: sem
  bloqueador, demais slides idênticos com deslocamento de 1; V_CC → V_dc
  como na Fig. 3.2; check_pptx 0 falhas; tempo 23,3 min.

## 2026-10-18 (noite, 3): blocos funcionais demarcados no slide 6 (entregue)

- Pedido do Victor: marcar na figura o detector de fase, o PI e o VCO.
  Áreas tracejadas com os nomes dos cartões, recorte da Fig. 3.3 do TCC
  (§3.4; VCO = ω0 + somador + 1/s). Moldura e cartão de equações 2,80 in;
  cartões e caixa do pé descidos. Staging `C:\Temp\defesa_s6b\`.
- MD5 antes 08b059738bcac85515b68e20cca33788, depois
  2d916e20cfbbe4e70c8e60b3f1904c67; backup
  `Defesa_TCC_SRF-PLL_backup_20261018_185235.pptx`. `diff_slides.py`: só a
  imagem do slide 6; check_pptx 0 falhas; slide-validator sem bloqueador.

## 2026-10-18 (noite, 2): slide 6 com a Fig. 4.3 redesenhada (entregue)

- Pedido do Victor: diagrama e equações maiores no projetor. Três variantes
  em staging (`C:\Temp\defesa_s6\`), aprovada a C: diagrama compacto
  (`assets/diagrams/pll_control_loop_defesa.svg`, 7,55 x 1,87 in, notação v,
  sem título interno), cartão novo "Sintonia do PI" com as equações da
  figura em Cambria Math 20 pt, cartões PD/PI/VCO em linha embaixo; legenda
  "Figura 4.3 do TCC: diagrama conceitual do SRF-PLL" (saiu "Clarke").
- MD5 antes 7f164f87e23f4e100235577ae4cc5fda, depois
  08b059738bcac85515b68e20cca33788; backup
  `Defesa_TCC_SRF-PLL_backup_20261018_184248.pptx`. `diff_slides.py`: só o
  slide 6; check_pptx 0 falhas (aviso: fonte Cambria Math); slide-validator
  sem bloqueador.

## 2026-10-18 (noite): figuras dedicadas nos slides 13, 15 e 16 (entregue)

- Pedido do Victor: gráficos do Cap. 5 ilegíveis no projetor → versão
  redesenhada dos mesmos dados no tamanho da caixa (skill, caso
  `figura_dedicada.md`; PNG/SVG em `assets/charts/defesa/`). Staging
  `C:\Temp\defesa_figs\`, MD5 antes c5e1a2dd42fd8c3cecf4417fd27ba20d (o
  b6f8 regravado pelo PowerPoint ao reabrir: só core.xml/viewProps),
  depois 7f164f87e23f4e100235577ae4cc5fda; backup
  `Defesa_TCC_SRF-PLL_backup_20261018_174517.pptx`.
- Slide 13: Fig. 5.3. Slide 15: Fig. 5.7 (moldura 5,82 in; tabela e nota
  5,83 in em x = 7,12). Slide 16: Figs. 5.10 e 5.18. Legendas "Figura X.Y
  do TCC" mantidas.
- `diff_slides.py`: só o hash das 4 imagens; check_pptx 0 falhas; 23,2 min;
  slide-validator sem bloqueador (opcionais em [[defesa-pendencias]]).

## 2026-10-18 (fim de tarde): layout dos slides 5 e 6 (entregue)

- Os três opcionais do slide-validator, aprovados pelo Victor. Staging
  `C:\Temp\defesa_ajustes\`, MD5 antes c4435c1044edee968c2626da45d8820c,
  depois b6f8295f94bd4e8017b37b1a28f1b118; backup
  `Defesa_TCC_SRF-PLL_backup_20261018_172913.pptx`.
- Slide 5: moldura da equação 11,85 x 2,30 in, imagem 9,09 x 1,80 in;
  cartões lado a lado (5,80 x 1,20 in, top 4,65). Slide 6: moldura 7,30 x
  3,65 in, figura 6,18 x 3,18 in, cartões 4,40 x 1,15 in em x = 8,55;
  subscritos por run com `baseline="-25000"`.
- `diff_slides.py`: 0 slides com diferença (só posição e estilo de run);
  check_pptx 0/0; 23,2 min; slide-validator sem bloqueador.

## 2026-10-18 (tarde): slide 5 dividido em dq + Fig. 4.3, 26 → 27 slides (entregue)

- Pedido do Victor: slide 5 só com a transformada dq, com a matriz na tela
  e gancho para o PLL; a Fig. 4.3 não pode sumir. Staging MD5
  `90d55095ce259bc043bcc49e563be05f`; script
  `C:\Temp\defesa_slide5\gen_slide5.py` (grupos divide, dq, pll, notas).
  Entregue MD5 `c4435c1044edee968c2626da45d8820c`; backup
  `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261018_161852.pptx`; PDF
  `C:\Temp\defesa_slide5inal.pdf`.
- Slide 5: título "Girando com a rede, a transformada de Park torna
  constantes as grandezas trifásicas"; imagem da equação (3.5) desenhada em
  SVG (`assets/diagrams/park_abc_dq_equacao.svg`, Cambria Math, θ em laranja) no lugar da Fig. 4.3; 2
  cartões; faixa "E o ângulo θ?". Slide 6 (cópia do antigo 5 por
  `duplica_slide`): Fig. 4.3, cartões PD/PI/VCO, faixa "Por que o
  travamento importa?". Notas dos dois = marcador.
- diff: slides 1-4 e 7-27 = antigos 1-4 e 6-26. check 0 falha;
  slide-validator sem bloqueio (equação conferida com a 3.5); 23,2 min.
- A 1ª tentativa do `entrega.ps1` abortou ("PowerPoint não fechou em
  30 s"); o processo sumiu logo depois e a 2ª passou.

## 2026-10-18: bloco MODELAGEM reestruturado, 25 → 26 slides (entregue)

- Alternativa 1 aprovada pelo Victor: ordem do trabalho real (dq →
  9 barras/Thévenin → bancada do PLL entre duas fontes ideais → ganhos →
  inversor em etapas). Staging MD5 `3ee5d96bbd991ea529e6f6f5a4f51884`;
  script `C:\Temp\defesa_modelagem\gen_modelagem.py`. Entregue MD5
  `90d55095ce259bc043bcc49e563be05f`; backup
  `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261018_133056.pptx`; PDF de
  reserva `C:\Temp\defesa_modelagem\final.pdf`.
- Slide 5 (era 6): sai a Fig. 3.1, entram 3 cartões; pergunta "Por que dq
  e não abc?". Slide 6 (era 8): "Ferramentas" → "Redução". Slide 7 novo,
  figura `assets/diagrams/pll_bancada_duas_fontes.svg`. Slide 8 (era 7):
  título "Na bancada..."; sai "(16,7 ms)", que não está no TCC
  (slide-validator). Slide 9 (era 5): título e cartões em etapas.
- diff: slides 1-4 e 10-26 idênticos aos antigos 1-4 e 9-25. check 0
  falha; slide-validator sem bloqueio após o 16,7 ms; 24,9 min (notas de
  5-9 ainda antigas).

## 2026-10-17: deck igual ao TCC final, sem valor fora dele (entregue)

- Regra do Victor: todo número e afirmação do deck é o do TCC entregue
  (VFinal, 15/10); o que não está no TCC sai. Staging MD5
  `cc5e0460a8b0effb45180236061f10ca`; spec `C:\Temp\defesa_qa\spec.md`,
  script `gen_tcc_exato.py`. Entregue MD5 `7975d03f419fc2900c712aa48ac26ab0`;
  backup `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261017_123432.pptx`.
- Slides 3 (23.368 MW; Ibéria: 2,5 GW por sobretensão, 0,63 Hz antes do
  colapso), 4 (objetivos do TCC), 5 (saem Vcc 136,36 kV, L1, L2, Cf e o
  argumento do MPPT; fica a margem de modulação da §4.3.2), 8 (sai 18/230 kV),
  9 e 10 (saem "29 cenários", partida até 0,1 s, janela da retenção e
  0,091/0,989), 12 ("98 ms após a eliminação"), 14 (título sem cycle
  slipping), 17 (sai grid-forming e DSOGI; cartões do Cap. 7), 21 (P da
  Tabela 5.2: −0,01/−0,01/0,02/0,41), 22 (sai a coluna Vd mín/máx).
- diff_slides: só os 11 slides previstos. check 0 falha; 24,8 min.

## Antes de 2026-10-17

Entregas de 2026-10-16 em [[defesa-historico-entregas-10-16]].
