---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-10-13 (23h54) — Restauração da entrega de 12/10 (VF - Copia)

O Bruno salvou às 00h59 de 13/10 uma cópia aberta às 17h56 de 12/10: texto
idêntico ao backup `_175643`, perdendo as 6 entregas de 18h23 a 21h02
(#130 Bollen, Tabela 5.2, médias de P e Q, ANEXOS, notas [Claude]; "Feito."
7 → 2). Achado pelo `diff_texto` contra cada backup do dia. De novo, só 4
resoluções (2 do Oscar, 2 notas [Claude] já apagadas). Entregue o
`final.docx` das 21h02, com as 2 resoluções do Oscar refeitas pelo
`word_finalize.ps1 -Resolve` (novo). Diff contra 21h02: 0 trechos, 31
comentários, 7 "Feito."; backup `_235421` guarda a versão do Bruno.

## 2026-10-12 (21h02) — Primeiro ciclo = salto de fase (#130, VF - Copia)

§542: "transitório de comutação" (termo sem uso na bibliografia para falta)
virou "salto de fase que o curto-circuito impõe à tensão, ao qual o SRF-PLL
só responde com atraso (BOLLEN, 2000)". Bollen já estava nas referências.
Base em [[pll-phase-jump-fault-inception]]. "Feito." no comentário. Um
parágrafo alterado, 81 págs, 31 comentários, audit limpo. MD5 d688df33…;
backup `_210221`.

## 2026-10-12 (20h23) — ANEXOS removido (#218, VF - Copia)

Título ANEXOS vazio (último parágrafo, sem remissão no texto; material
autoral seria APÊNDICE) apagado junto com o comentário do Oscar e a resposta
do Bruno, ancorados só nele: `-Delete`, corte do parágrafo no XML (o
`sectPr` é do `body`), sumário reconstruído. 82 → 81 págs, 30 comentários;
saíram só a linha do sumário e o título. `pagecheck` perdeu o grupo do
ANEXOS; restam 2 anteriores (legendas das Tabelas 5.1-5.3, título "3.
Objetivos" no pé da folha 18). MD5 03641fa8…; backup `_202324`.

## 2026-10-12 (20h08) — Notas [Claude] aprovadas apagadas (VF - Copia)

Victor aprovou as notas da frase nova do §573 (atende o comentário do Oscar
sobre a sintonia inadequada parecer melhor), da remissão "perda de
sincronismo descrita acima" e do "recuperando o travamento angular". Apagadas
com `-Delete`; nenhuma nota [Claude] sobra no documento. Texto visível
idêntico. 82 págs, 32 comentários, audit limpo. MD5 3c72df2f…; backup
`_backups\VF\…_backup_20261012_200815.docx`.

## 2026-10-12 (19h32) — "5.45 ??" respondido (#175, VF - Copia)

Remissão à Figura 5.5 no §592 estava certa; as legendas já dizem "com
sintonia nominal". Só comentários: "Feito." no "5.45 ??" e nota [Claude] das
legendas apagada (`word_finalize.ps1 -Delete`, opção nova). Texto visível
idêntico ao anterior. 82 págs, 35 comentários, audit limpo. MD5 91bac371…;
backup `_backups\VF\…_backup_20261012_193225.docx`.

## 2026-10-12 (18h40) — 180° = oposição de fase (#148 e #183, VF - Copia)

- Oscar: 180° = −1 + j0, o inversor absorveria P (#148, célula da Tabela 5.3);
  ligação com a §5.4 (#183, Bruno confirmou). Dados (bifásica Barra 7): P < 0
  em 50,9 % (nominal) e 47,5 % (inadequada) da falta, 1-3 % depois.
- Frase no §580 (após "…alinhamento com o vetor de tensão da rede.") e no
  §596 (após "…dentro do referencial estimado."): na bifásica, a oposição se
  repete só durante a falta; na §5.4, a cada volta após a eliminação. Reativo
  fora de propósito (já no §604). "Feito." nos dois. `C:\Temp\tcc_180\gen_180.py`
  → 82 págs, 35 comentários, audit 0 → MD5 1263623e…, backup `_20261012_184054`.

## 2026-10-12 (18h23) — Q acima de V·Iq e média na falta nas figuras (#168, VF - Copia)

- Oscar: V·Iq = 0,77 × 0,22 ≈ 0,17 pu, mas o texto dá Q = 0,22 pu. Nos dados
  (bifásica Barra 6, inadequada, janela 0,317-0,4 s): a média do produto não é
  o produto das médias. vd e iq oscilam juntos em 120 Hz (≈ +0,04 pu) e vq ≈
  0,025 com id ≈ 0,94 (≈ +0,04 pu). Na trifásica da Barra 6 a conta fecha
  (0,58 × 0,66 ≈ 0,39; Q = 0,40). Os dq gravados não reconstroem Q exato
  (0,24 × 0,22): explicação de ordem de grandeza.
- Bloco 585 reescrito com "média" uma vez só, pré-falta "1 pu" (pedido do
  Victor) e a frase da diferença. Figuras 5.8, 5.15 e 5.19 com tracejada da
  média na falta sem o 1º ciclo (`gen_fault_waveforms.py`, rótulos afastados
  quando P e Q quase coincidem); rId33/40/44. 5.4 e 5.20 não têm falta.
  "Feito." no #168. `C:\Temp\tcc_media1012\gen_media1012.py` → 82 págs →
  audit 0 → entregue `ffc6ee37…`, backup `_backups/VF/…_20261012_182329`.

## 2026-10-12 (17h56) — Correção de P e Q de 03/10 reaplicada (VF - Copia)

- O VF (03/10 18h47) saiu de um arquivo anterior à entrega das 15h23 abaixo:
  texto **e figuras** de antes da correção (imagens idênticas às do backup
  `V10_backup_20261003_152345`). Só isso divergia do V10.
- Reaplicado do V10: blocos 551 (0,09 pu), 555 (0,41 pu, mantendo "de
  tensão"/"de corrente reativa" do Bruno), 585 (P 0,70 / Q 0,22 pu), 589
  (3,2 → 2,0 pu), Tabela 5.2 inteira, e as Figuras 5.4, 5.8, 5.15, 5.19 e
  5.20 (`troca_imagem.py --rid` rId29/33/40/44/45 com o PNG do V10). Depois:
  0 imagem divergente do V10. `C:\Temp\tcc_pq1012\gen_pq1012.py` → 82 págs
  → audit 0 → entregue `c34c4fce…`, backup `_backups/VF/…_20261012_175643`.
- O Word estava aberto (reaberto pela entrega anterior): fechado por COM,
  `Saved=True`, MD5 sem mudança.

## 2026-10-12 (17h37) — Comentários do Oscar de 11/10, parte de texto (VF - Copia)

- Canônico novo (Victor confirmou): `TCC_Victor_Bruno_VF - Copia.docx`, o VF
  com 22 comentários do Oscar (11/10, Cap. 5 + ANEXOS), respostas e edições
  diretas do Bruno (12/10). Pendências em [[tcc-pendencias]].
- Texto: "energização" → "transitório de inicialização" (Figs. 5.1-5.4 e
  §5.1); "com sintonia nominal" nas legendas 5.5, 5.6, 5.8; fórmula da rampa
  com o "−" que o Bruno apagou; vírgula no 559; "−0,02" no 573 + frase de
  ressalva (#152); Figura 5.14 → 5.16 no 592; 596 e 600 reescritos (o Bruno
  tirou "escorregamento de ciclo" do 596); 625 "recuperando o travamento
  após a eliminação". "Feito." em #152 e "Fiquei confuso…"; 4 comentários
  [Claude]. `C:\Temp\tcc_oscar1012\gen_oscar1012.py` (troca mínima por
  prefixo/sufixo comum, preserva âncoras) → finalize 82 págs → audit 0 →
  entregue `cbaf969d…`, backup `_backups/VF/…_20261012_173752`.

## Entregas de 2026-10-03

Ver [[tcc-historico-entregas-2026-10-03]]: comentários do Oscar após a
Figura 5.8 (3 tabelas e 2 figuras), "Referência" no §5.1, Figura 4.2 com
letras maiores e escala de P e Q corrigida com potências médias.

## Entregas de 2026-10-02

Ver [[tcc-historico-entregas-2026-10-02]]: Figura 3.1 do controle de corrente
dq, fontes "Adaptado de" nas figuras conceituais, Figura 4.1 redesenhada com
a potência da UFV, Cap. 5 restaurado após save por cima.

## Entregas de 2026-10-01

Ver [[tcc-historico-entregas-2026-10-01]]: gráficos e texto do Cap. 5 da
safra de 01/10, texto antes das figuras, "reaquisitar" fora, citações de
alto risco e referências pedidas pelo Oscar.

## Entregas de 2026-09-27 a 2026-09-29

Ver [[tcc-historico-entregas-2026-09-fim]]: citação de "redes fracas" para Wu
e Wang, Xiong na Motivação (comentário 16) e 38 comentários novos do Oscar
mesclados no Cap. 5.

## Entregas de 2026-09-26

Ver [[tcc-historico-entregas-2026-09-26]]: comentários do Oscar no V10
(notação do PLL, Resumo/Abstract, figuras ONS), comentário 16 com o Xiong
(duas tentativas revertidas) e siglas definidas uma vez só.

## Entregas de 2026-09-13

Ver [[tcc-historico-entregas-2026-09-13]]: passagem ABNT completa, lista de
siglas revisada contra o texto, subscrito nos símbolos do texto corrido.

## Entregas de 2026-09-12

Ver `historico_entregas_2026_09_12.md`: referências em amarelo fechadas,
revisão de português do documento inteiro, Cap. 7 e Cap. 6 redigidos.

## Entregas de setembro/2026 até o dia 09

Ver `historico_entregas_2026_09_inicio.md` — troca de terminologia
PAC → PCC (2026-09-09), mesclagem dos Cap. 4 e 5 do fragmento no
canônico e enxugamento analítico do Cap. 5 (ambas de 2026-09-02).

## Entregas de agosto/2026

Ver `historico_entregas_2026_08.md` — nova §3.5 (controlador de corrente) +
referências cruzadas Cap.3↔Cap.4, passe de estilo Fase 2, e os ganhos do PLL
(§3.4) / CIGRE (§2.3) / dois cenários (§4.3.3) / duas etapas (§4.3.2).

## Entregas de julho/2026 (2026-07-22 e anteriores)

Ver `historico_entregas_2026_07.md` — inclui a remoção retroativa de
travessão, a remoção de linguagem de código/merge de 4.3.2.1–4.3.3.2, e o
incidente de corrupção que motivou a troca para `TCC_Victor_Bruno_V9_novo_indice_2.docx`.

## Entregas anteriores (V8)

Ver `historico_entregas_v8.md` (fragmentado em 2026-07-22 por limite de linhas).

## Relacionados

- [[tcc-historico-entregas-2026-08]] — histórico detalhado de agosto
- [[tcc-historico-entregas-2026-09-26]] — entregas de 2026-09-26 (V10)
