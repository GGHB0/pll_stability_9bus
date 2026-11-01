---
name: tcc-historico-entregas-2026-10-12
description: "Entregas de 2026-10-12 no VF - Copia — comentários do Oscar de 11/10, P e Q reaplicados, 180° = oposição de fase, ANEXOS removido, salto de fase"
aliases: [tcc-historico-entregas-2026-10-12]
---

# TCC Word — Entregas de 2026-10-12

Continuação de [[tcc-historico-entregas]] (fragmentado em 2026-10-15 por
limite de linhas). Ordem: mais recente primeiro.

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

## Relacionados

- [[tcc-historico-entregas]] — histórico principal, entregas mais recentes
- [[tcc-pendencias]] — comentários do Oscar de 11/10 ainda abertos
