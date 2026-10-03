---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-10-02 (23h36) — Figura 4.1 redesenhada + potência da UFV no §4.3.1 (V10)

- Oscar (#181): "O inversor está injetando 163 MW?? ... tirar o G2". A figura
  também trazia MVA nominal como MW (G1 "247", G3 "128"). Rótulos agora com o
  imposto no modelo: UFV 100 MW, G3 85 MW, G1 slack ([[ieee9bus-topology]]).
- PNG do TCC sai de cópia do `ieee9bus_unifilar.svg` sem as duas linhas de
  título e com `viewBox="0 95 920 580"` (2760×1740); o SVG do repo mantém o
  título porque serve o dashboard. Troca do `media/image9.png` (rId22) e
  extent `cy` 4257923 → 3631758.
- §467 dizia "máquina síncrona de 100 MVA ... inversor de mesma potência":
  virou "da Barra 2, de 192 MVA e 163 MW despachados no caso original, foi
  substituída por um inversor fotovoltaico de 100 MW (1 pu na base de 100 MVA
  do sistema)", com comentário [Claude] pedindo o ok do Victor.
- `C:\Temp\tcc_fig41\gen_fig41.py` → finalize 80 págs, +1 comentário,
  "Feito." no #181 → audit 0 → entregue (`0014ee96…`); backup `_20261002_233617`.

## 2026-10-02 (21h55) — Fontes "Adaptado de" nas figuras conceituais + "Feito." no #182 (V10)

- Oscar (#182, Fonte da Figura 4.1): "Poderiam colocar adaptado de [ref.]".
  Victor estendeu a todas as figuras apoiadas em obra (D10 revisada em
  `tcc-abnt-layout/decisoes.md`). Troca por paraId: 2.3 Bollen (2000); 3.1
  Yazdani e Iravani (2010); 3.2 Yazdani e Iravani + Teodorescu et al.; 3.3 e
  4.3 Teodorescu, Liserre e Rodriguez (2011); 4.1 Anderson e Fouad (2003) e
  MathWorks (2025); 4.2 Alves (2022). Tabela 4.1 e Cap. 5 seguem "Os autores".
- `C:\Temp\tcc_fontes\gen_fontes.py` → finalize 80 págs → audit 0 →
  entregue (`78366896…`); backup `_20261002_215525`.

## 2026-10-02 (19h55) — Parágrafo que apresenta a Figura 2.3 + "Feito." no #83 (V10)

- Oscar (#83): figura do afundamento sem conexão com o texto. Parágrafo novo
  `1FB00315` entre o da assimetria (`4352E7EF`) e a legenda: V_res e Δt
  (BOLLEN, 2000), limiar 0,9 pu, ligação com a curva da Figura 2.1 e com o
  ganho da malha do PLL ([[pll-gain-voltage-dependence]]). A frase final
  sobre faltas assimétricas foi cortada pelo Victor ("foi excesso").
- `C:\Temp\tcc_fig23\gen_fig23.py` → finalize 80 págs → audit 0 →
  entregue (`1335dfd7…`); backup `_20261002_195516`.

## 2026-10-02 (18h54) — Figura 3.1 só com o controlador (V10)

- Victor: "só deixa o que realmente está no nosso controlador". Saíram v_g,d,
  v_g,q, os dois ωL e os somadores do lado CA: duas malhas independentes, PI +
  N(s) → Vcc/2 → 1/(Ls+R) (os dois últimos são modelos médios, aceitos assim).
  SVG 720×345; `image6.png` trocada no DOCX, 16 cm × cy 2760345.
- Bloco 379: "…pela ação integral do PI, conforme a Figura 3.1." → "…do PI. A
  Figura 3.1 mostra a malha de corrente implementada."
- `C:\Temp\tcc_fig31\gen_fig31.py` partiu do arquivo com a edição das 18h de
  outra sessão (preservada). Audit 0; backup `_20261002_185440`.

## 2026-10-02 (18h) — "maioria das variáveis" no 2.2 + "Feito." no #27 (V10)

- Oscar (#27, "maioria" na definição IEEE/CIGRE do bloco 280): brecha para
  a banca perguntar quais variáveis. Victor preferiu tirar o "maioria"
  (paráfrase, não citação literal) a explicá-lo. Texto: "mantendo as
  variáveis operacionais, como as tensões nas barras e a frequência,
  limitadas de modo a preservar...". Comentários 27/28 reancorados no trecho.
- `C:\Temp\tcc_c22\gen_c22.py` (3 replaces) → finalize 79 págs → audit 0
  falhas → entregue (`f3ddccaa…`). Staging refeito 2x: Word aberto salvou ao fechar.

## 2026-10-02 (17h43) — Fonte da Figura 3.1 autoral + "Feito." no #95 (V10)

- Victor: "o exemplo é do Yazdani, mas é referente à nossa implementação".
  Fonte → "Os autores (2026)." (D10 em `tcc-abnt-layout/decisoes.md`), parágrafo
  `1FB0D104` reconstruído por paraId (Word tinha posto `proofErr`).
  `C:\Temp\tcc_fonte\gen_fonte.py`; "Feito." no #95 via `-Replies`.
- Figura reconferida contra o `.slx` (PWM Control: Sum +−, Kp/4 e Ki/4·∫ com
  integrador saturado em ±2, notch, `m_dq`; PLL usa só v_q da rede). Audit 0
  falhas; pagecheck com as 2 falhas antigas. Backup `_20261002_174256`.

## 2026-10-02 (16h39) — Figura 3.1 do controle de corrente dq no §3.1.4 (V10)

- Comentário #95 do Oscar (figura como a 8.10 de Yazdani, adaptada ao modelo).
  Figura nova `assets/diagrams/current_control_dq_blocos.png` (PI + notch por
  eixo, sem desacoplamento ωL/feedforward, conferido no `.slx` e no PSIM),
  trio por `campos.py`, 16 cm, fonte "Adaptado de Yazdani e Iravani (2010)".
- Frase do bloco 379 que prometia desacoplamento/feedforward trocada: formulação
  clássica citada, modelo sem esses termos, remissão "conforme a Figura 3.1". As
  antigas 3.1/3.2 viraram 3.2/3.3 (sem remissão no texto). `C:\Temp\gen_ccdq.py`
  (mídia `pll_ccdq.png`, `rId200`, docPr `900000100`, paraIds `1FB0D102-104`).
- Finalize (79 folhas) → audit 0 falhas → backup `V10_backup_20261002_163927`.
  Comentário #95 não marcado como feito.

## 2026-10-02 (00h23) — Seções 3.1.1-3.1.3 e parágrafo da GD (3.2) (V10)

- Redação do Victor; síntese da 3.1.2 corrigida: (3.5) é abc→dq e (3.6)/(3.7) são vd/vq, não há inversa. Comentários 81, 85-88, 95, 96 reancorados no texto novo; sigla GD saiu do texto.
- `gen_cap3_transformadas.py` + `gen_cap3_gd.py` (C:\Temp) → backup `_002315`. 00h27: "Feito." em 81, 83, 95 e nos dois "depois de vq = 0" (`replies_cap3.json`), não nos que pediam P e Q logo após cada definição (backup `_002747`). 16h36: GD fora da lista de siglas (`gen_sigla_gd.py`, backup `_163604`).

## 2026-10-02 (00h17) — Cap. 5 restaurado após save por cima (V10)

- O save das 00h08-00h10 (Word aberto com versão anterior) desfez a entrega
  das 23h59: sumiram as Figuras 5.8, 5.10, 5.11, 5.13, 5.16 e 5.18, as
  chamadas voltaram para baixo das legendas e 5.17/5.19 ficaram com a legenda
  em dobro. Sintoma relatado pelo Victor: "do 5.12 foi para o 5.14".
- Base = entrega das 23h59 + os 7 parágrafos editados pelo Victor nos Caps.
  1-2 (por paraId, ids de comentário remapeados) + remoção dos 7 comentários
  que ele apagou ali (25-27, 36-39). `C:\Temp\gen_restaura.py`.
- Finalize (78 págs, 19 figuras no Cap. 5) → audit 0 falhas → backup
  `V10_backup_20261002_001733` (save em Word inglês, só ids de estilo).

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
