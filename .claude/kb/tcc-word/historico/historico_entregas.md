---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-10-25 — Sigla de transitórios eletromagnéticos fora do TCC (pedido do Oscar)

5 trocas no VFinal, todas em texto bruto: Resumo ("simulação computacional
de transitórios eletromagnéticos"), Abstract (espelho, sem comentário: o
VFinal não tem comentários e ficou assim), objetivo específico 2, dois
trechos da Conclusão ("simulações computacionais"). A sigla não estava na
lista de siglas. fb061b4a… → a69b1839c7f0faf1d6ff5801a6d2ff43, backup
`_backups\VF\..._20261025_162820`. `diff_texto.py`: 5 trechos, 813 → 813
parágrafos, comentários 0 → 0. O PDF ao lado do VFinal não foi regerado.

## 2026-10-15 (01h43) — Referências de delimitação de escopo (pedido do Oscar)

Oscar pediu duas referências para o leitor saber que a literatura de
estabilidade com IBR vai além do recorte (estabilidade por impedância etc.).
Parágrafo novo no fim do §2.3 (pág. 23) citando ALI et al. (2025) e
IEEE (2026), e as duas entradas na lista de REFERÊNCIAS (pág. 80): ALI antes
de ALVES, IEEE Std 2800.2-2026 depois do IEEE Std 1547-2018. Base em
[[stability-classification-extended]]. Pedido veio por fora do docx: sem
"Feito.". `C:\Temp\gen_scope_refs.py` → 82 págs → diff: 3 trechos,
33 comentários, 9 "Feito.". MD5 af879170…; backup `_014334`. O Word regravou
o canônico ao sair e o sync mudou o MD5 de novo sem texto novo: staging
refeito duas vezes. Audit acusa uma imagem de 6,44 in (> 6,30 in) que **já
estava** no canônico antes desta entrega (provável Figura 3.2 de 01h18).

## 2026-10-15 (01h18) — Figura 3.2 só em diagrama de blocos (prof. André)

André: a Figura 3.2 misturava diagrama de blocos com unifilar (nó de PCC,
rede como fonte senoidal); propôs trocar pela 4.2 ou redesenhar só em
blocos. Seguido o redesenho (sem renumeração): `vsi_grid_blocos.svg`, rede
como bloco, sem PCC, medições i_abc (filtro) e u_abc (rede) ao controle;
a versão antiga ficou em `vsi_grid_schematic.svg`. `troca_imagem.py` (rId16)
+ frase "A Figura 3.2 ilustra…" no fim do §3.2 (faltava remissão). Comentário
veio por fora do docx: sem "Feito.". Diff: 1 trecho, 33 comentários,
9 "Feito.". MD5 ad9adbbc…; backup `_011854`.

## Entregas de 2026-10-12

Ver [[tcc-historico-entregas-2026-10-12]]: comentários do Oscar de 11/10,
P e Q de 03/10 reaplicados, 180° = oposição de fase, ANEXOS removido e
primeiro ciclo = salto de fase.

## 2026-10-14 (00h58) — Monofásica na Barra 7 com sintonia inadequada (#150, #164)

Rodada do Bruno de 13/10 ([[cenarios-simulados]]): Tabela 5.3 ganhou
"Inadequada 0,64 | 0,55 | 70,6 | 95"; §579 (pico 89,7° → 70,6°), §580
(abaixo de 90° na falta, −88° ~30 ms após a eliminação) e §588 (retorno
dobra nas duas assimétricas da Barra 7: 46 → 95 ms na mono). Figuras 5.7,
5.14 e 5.18 trocadas: legenda "1º ciclo (comutação…)" virou "salto de
fase", alinhada ao #130. "Feito." nos dois; diff: 3 trechos, 33
comentários, 9 "Feito.". MD5 7560ba58…; backup `_005804`.

## 2026-10-13 (23h54) — Restauração da entrega de 12/10 (VF - Copia)

O Bruno salvou às 00h59 de 13/10 uma cópia aberta às 17h56 de 12/10: texto
idêntico ao backup `_175643`, perdendo as 6 entregas de 18h23 a 21h02
(#130 Bollen, Tabela 5.2, médias de P e Q, ANEXOS, notas [Claude]; "Feito."
7 → 2). Achado pelo `diff_texto` contra cada backup do dia. De novo, só 4
resoluções (2 do Oscar, 2 notas [Claude] já apagadas). Entregue o
`final.docx` das 21h02, com as 2 resoluções do Oscar refeitas pelo
`word_finalize.ps1 -Resolve` (novo). Diff contra 21h02: 0 trechos, 31
comentários, 7 "Feito."; backup `_235421` guarda a versão do Bruno.

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
