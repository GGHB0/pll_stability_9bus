---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-09-26 — Sintonia inadequada no Resumo e no Abstract (V10)

- **Canônico passou a ser `TCC_Victor_Bruno_V10.docx`**, com os comentários
  do Oscar (e respostas do Bruno). O `_2` saiu da pasta; `config.py` foi atualizado.
- **Pedido**: incluir o caso da sintonia inadequada no Resumo, atendendo ao
  comentário 1 do Oscar. A primeira versão trazia o desfecho (perda de
  sincronismo) e foi recusada, porque o Resumo apresenta e não conclui.
- **Aplicado** (bloco 116, antes de "O trabalho conclui avaliando"):
  "Analisa-se também um cenário de sintonia inadequada, com os ganhos do
  controlador PI do PLL reduzidos em relação ao projeto nominal, comparando
  sua resposta dinâmica à do caso nominal."
- **Abstract** (bloco 123, espelho, atendendo ao comentário 2): "An
  inadequate-tuning scenario is also analyzed, …". A tradução não foi
  aprovada no chat: leva um comentário `[Claude]` no Word para o Victor dar
  o ok lá. Comentários do Oscar intactos (92 → 93).
- **Pipeline**: `gen_resumo_sintonia.py` → `word_finalize.ps1 -Comments`
  (parâmetro novo; 75 págs, 0 campo com erro) → `audit_docx.py` 0 falhas →
  MD5 conferido → backup `V10_backup_20260926_195650` → entregue e reaberto
  no Word. Os padrões que ficaram estão em `padroes_revisao.md` da skill.

## 2026-09-13 (noite, 2) — Subscrito nos símbolos do texto corrido

- **Pedido**: símbolos como "vq" estavam com o índice na mesma linha. A
  varredura mostrou que o documento **não tinha nenhum** `w:vertAlign`: todo
  símbolo em texto corrido estava achatado (as equações OMML já estavam certas).
- **Aplicado** (aprovado): **59** subscritos, do Cap. 1 às REFERÊNCIAS
  (exclusive): v<sub>d</sub>, v<sub>q</sub> (8), i<sub>d</sub>/i<sub>q</sub> (8),
  i<sub>d,ref</sub>/i<sub>q,ref</sub>, m<sub>d</sub>/m<sub>q</sub>,
  K<sub>p,PLL</sub>/K<sub>i,PLL</sub> (10), K<sub>p</sub>/K<sub>i</sub> (8),
  ω<sub>n</sub> (4), 2ω<sub>0</sub>, ω<sub>nom</sub>, ω<sub>res</sub>,
  f<sub>g</sub> (3, incl. f<sub>g</sub>²), L<sub>est</sub> (4),
  R<sub>d1..d3</sub>, Z<sub>th</sub>, t<sub>s</sub> (2). "Vq = 0" virou v minúsculo;
  sobras de LaTeX `v_q` e `t_s` perderam o underscore.
- **Não feito**: itálico nas letras-base (ABNT/praxe) foi oferecido e ficou
  sem resposta. Fica só o subscrito; o próprio texto já tem "eixo *d*" em itálico.
- **Pipeline**: `gen_subscritos.py` (docx-scripter; split de run clonando o
  rPr, `vertAlign` antes de `w:lang`) → `word_finalize.ps1` (74 págs, 0 erro) →
  `audit_docx.py` **0 falhas / 0 avisos** → 59 subscritos conferidos no final →
  backup `..._backup_20260913_232317.docx` → entrega, MD5 `545001db…`
  (pré-check `5aa09ba3…` conferido).

## 2026-09-13 (noite) — Lista de siglas revisada contra o texto

- **Pedido**: deixar na lista só as siglas usadas no trabalho; o Victor
  sentia falta do SRF-PLL. Ele **já estava** na lista, mas desalinhado (ver
  abaixo), provável motivo de passar despercebido.
- **Conteúdo** (aprovado; CSV vetado): 31 → **36**. Saíram 9 sem nenhuma
  ocorrência (AVR, IAE, ISE, ITAE, LG, LLG, MPPT, PSS, SPWM); entraram 14
  usadas no corpo (BESS, CIGRE, COI, DSO, ENTSO-E, FFR, GFM, IEA, SCR, SEN,
  SEP, SOTF, TSO, UFV). Lista completa em `siglas_inventory.md`.
- **Formatação**: o render mostrou CIGRE/DDSRF-PLL/ENTSO-E/SRF-PLL com o
  significado numa coluna mais à direita (dois tabs padrão) e a 2ª linha do
  BESS na margem. Virou tab único em 3 cm + recuo deslocado + `jc=left`;
  `after` 120 → 60 para as 36 linhas caberem na folha 13.
- **Pipeline**: `gen_siglas_revisao.py` (docx-scripter; paraIds
  `1FB00300`–`1FB0030D`, +5 parágrafos, fora da região byte-idêntico) →
  `gen_siglas_tabs.py` (pPr via `ppr.py`) → `word_finalize.ps1` (74 páginas,
  0 campo com erro, salvou) → `audit_docx.py` **0 falhas** → `pagecheck.py`
  1 grupo (ANEXOS vazio, pré-existente) → backup
  `..._backup_20260913_205128.docx` → entrega, MD5 `5aa09ba3…` (pré-check
  `17de36b4…` conferido).
- **Achado não corrigido**: 3 paraIds duplicados pré-existentes fora da lista
  (`00A662AF`, `1C32F253`, `69872514`); o Word salva sem reclamar.

## 2026-09-13 — Passagem ABNT completa (skill tcc-abnt-layout)

- **Pedido**: "Coloque tudo nas normas da ABNT, tudo bonitinho", com skill e
  KB antes. Decisões D1-D8 em `tcc-abnt-layout/decisoes.md`; estado antes e
  depois em `abnt_layout.md`.
- **Paginação**: even/odd desligado, seção 2 declara rodapé vazio, capa com
  `start="0"`, contagem contínua. Sem número no pré-texto nem no rodapé;
  Introdução na folha 16 imprime 15.
- **Ilustrações**: 24 legendas em campo `SEQ` (5 Figuras, 18 Gráficos,
  1 Quadro), três listas automáticas, `keepNext` em legenda e imagem, 23
  remissões reescritas. Figura 3.2 autoral no lugar das duas imagens do
  SRF-PLL (uma copiada de outro trabalho, sem citação).
- **Corpo e pré-texto**: 160 parágrafos com recuo de 1,25 cm; 23 equações
  em `(3.1)`; ~140 vazios de enchimento fora; dedicatória criada;
  REFERÊNCIAS no sumário; `74 f.` e 2026 no resumo.
- **Três bugs do próprio pipeline**, todos pegos antes da entrega: heredoc
  reduzindo barra dupla (gerador escrito com Write), `<w:p/>` auto-fechado
  engolido pela regex plana (tag aberta, XML não parseou; `scripts/ppr.py`),
  e falso "evenAndOddHeaders desligado" no `check_abnt.py` (corrigido).
- **Pipeline**: `C:/Temp/abnt_work/gen_abnt.py` → `word_finalize.ps1`
  (agora atualiza também as listas; 74 páginas, 0 campo com erro, salvou)
  → `audit_docx.py` **0 falhas** → `check_abnt.py` **0 falhas** →
  `pagecheck.py` 1 grupo (ANEXOS vazio) → backup
  `..._backup_20260913_171105.docx` → entrega, MD5 `17de36b4…`.
- **Aberto**: ANEXOS vazio, dedicatória/epígrafe, `74 f.` a confirmar com o
  Oscar, subseções do Cap. 1 fora do sumário, título dentro de algumas
  imagens (`pendencias.md` 20-24).

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
- [[tcc-historico-entregas-2026-09-12]] — histórico detalhado de setembro
