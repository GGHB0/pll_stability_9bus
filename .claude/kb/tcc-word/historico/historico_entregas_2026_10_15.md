---
name: tcc-historico-entregas-2026-10-15
description: Entregas de 2026-10-15 no TCC: referências de delimitação de escopo (Oscar) e Figura 3.2 só em blocos (André)
aliases: [tcc-historico-entregas-2026-10-15]
---

# TCC Word — Histórico de Entregas (2026-10-15)

Continuação de [[tcc-historico-entregas]].

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
