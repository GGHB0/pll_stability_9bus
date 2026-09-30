---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

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
