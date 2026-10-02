---
name: tcc-historico-entregas-2026-09-fim
description: Entregas de 2026-09-27 a 2026-09-29 no V10 (Wu e Wang em redes fracas, Xiong na Motivação, 38 comentários do Oscar no Cap.5), fragmentado do arquivo principal
aliases: [tcc-historico-entregas-2026-09-fim]
---

# TCC Word — Entregas de 2026-09-27 a 2026-09-29

> Fragmentado de [[tcc-historico-entregas]] em 2026-10-01 por limite de
> 200 linhas. Ordem: mais recente primeiro.

## 2026-09-29 — 38 comentários novos do Oscar mesclados no Cap.5 (V10)

- Victor recebeu do Oscar uma cópia comentada (`TCC_Victor_Bruno_V10 (1).docx`,
  baixada em 2026-09-29) com comentários novos datados de 25 e 28/09, além de
  edições de texto soltas (Figura→Gráfico, "EMT"→"transitórios
  eletromagnéticos", "IBR"→"Recurso Baseado em Inversor") feitas por
  cima. Pedido explícito: só os comentários do Cap. 5, sem as edições de
  texto.
- Diff por texto de comentário identificou 42 comentários novos (ausentes no
  canônico); 4 eram do Cap. 1/2 (datados de 23/09) e ficaram de fora por
  pedido — checagem por data confirmou que também já tinham sido mesclados
  antes (o canônico não tem nenhum comentário do Oscar após
  2026-09-24T17:02Z, então qualquer coisa datada de 23/09 já estava
  capturada, só com pequena variação textual, ex.: uma vírgula). Os 38
  restantes (todos ancorados no Cap. 5, ids 133-190 no arquivo baixado) foram
  inseridos.
- **Método**: sem tracked changes nem `d.Comments.Add` (que atribuiria a
  conta do Office como autor). Correspondência de bloco por índice
  (deslocamento constante entre os dois arquivos, +2 depois do heading da
  §5.3 que veio partido em 3 blocos por um bug do Word) + `difflib` para
  mapear os offsets do texto do âncora do arquivo baixado (com "Gráfico") de
  volta para o texto do canônico (com "Figura"), preservando a redação atual.
  Inserção cirúrgica de `commentRangeStart/End` + `commentReference` direto no
  XML, reaproveitando `paraId`/`durableId`/data do comentário original do
  Oscar (autoria preservada). Dois comentários (141, 182) ancoram imagem, não
  texto; dois blocos (503, 526) tinham `<w:lastRenderedPageBreak/>` partindo o
  parágrafo em duas runs, sem afetar a lógica de corte.
- **Pipeline**: script Python próprio (não um `gen_*.py` de replace simples,
  dado o volume) grava os 5 XMLs (`document.xml` + 4 partes de comentário) →
  `word_finalize.ps1` (74 págs, 141 comentários, 0 erro) → `audit_docx.py` 0
  falhas → MD5 do OneDrive conferido antes → backup
  `_backup_20260929_234138` → entregue.

## 2026-09-27 (2) — Comentário 16 do Oscar resolvido: Xiong na Motivação (V10)

- Motivação, último parágrafo: frase nova depois da frase ancorada ("…por que
  os equipamentos falharam."): "Estudos posteriores sobre o evento destacam
  que a área afetada tinha alta penetração de inversores e que, nesses
  equipamentos, a perda de sincronismo passa a ser governada pela dinâmica de
  controle do PLL, e não pelo ângulo físico das máquinas síncronas (XIONG et
  al., 2025)." A seguinte passou de "É imperativo investigar" a "Torna-se,
  assim, imperativo investigar". O trecho ancorado ficou intacto.
- Fidelidade: o Xiong (p. 1) liga o apagão de 2023 a uma área com alta
  penetração de GFL e mostra que a perda de sincronismo do GFL é a divergência
  do ângulo do PLL. A causa que o artigo aponta (falha das proteções PSB/OST)
  ficou de fora de propósito. Aprovado pelo Victor depois de três tentativas
  rejeitadas (09-26 ×2 e a primeira de 09-27).
- "Feito." respondido na thread do comentário 16 (`replies_xiong.json`).
- **Pipeline**: `gen_xiong_motivacao.py` (1 replace; XIONG 1→2) → finalize
  (74 págs, 0 erro) → audit 0 falhas → MD5 `2fa47e24…` conferido → backup
  `_backup_20260927_224244` → entregue (`66a817de…`) e reaberto.

## 2026-09-27 — Citação de "redes fracas" trocada para Wu e Wang (V10)

- Motivação, 4º parágrafo: "…especialmente em redes fracas (XIONG et al.,
  2025)" virou "(WU; WANG, 2020)". O Xiong não trata de rede fraca (nenhuma
  ocorrência de "weak"/SCR no PDF); o Wu e Wang (2020) trata (p. 1 e p. 3).
- Origem rastreada nas versões antigas: a frase entrou na versão de
  29/10/2025 (último a salvar: Bruno) como "[9]", uma entrada duplicada do
  Xiong anotada "(Citação utilizada para a estabilidade em redes fracas)".
  Seguiu assim até o V8; o V9 reescreveu o início do parágrafo e manteve o
  final. Não veio do Claude. Revisão geral das citações: [[tcc-pendencias]]
  item 26.
- Não é comentário do Oscar: sem "Feito." O comentário 16 continua aberto.
- **Pipeline**: `gen_wuwang_redes_fracas.py` (1 replace; XIONG 2→1, WU;WANG
  3→4) → finalize (74 págs, 0 erro) → audit 0 falhas → MD5 `3ec671a0…`
  conferido → backup `_backup_20260927_212300` → entregue (`2fa47e24…`) e
  reaberto.


## Relacionados

- [[tcc-historico-entregas]] — entregas mais recentes
- [[tcc-historico-entregas-2026-09-26]] — entregas anteriores
