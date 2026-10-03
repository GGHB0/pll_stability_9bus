---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-10-03 (15h23) — Escala de P e Q corrigida + potências médias (#315) (V10)

- Oscar (#315): médias de potência na falta comparadas com a rampa. Ao
  validar, achado: o `.slx` (SID 4055) usava ganho 1/√3 em P e Q, então P
  saía ×√3/2 (pré-falta 0,87 pu) e Q ×1,5. `.slx` corrigido, rodadas antigas
  reescaladas na leitura (`src/pipeline/pq.py`, ver [[export-workflow]]).
- Figuras 5.4, 5.8, 5.15, 5.19 e 5.20 regeneradas e trocadas
  (`troca_imagem.py`, rId29/33/40/44/45). Texto: 0,14 → 0,09 pu (Fig. 5.8),
  0,34 → 0,41 pu (Barra 6, texto e Tabela 5.2), coluna de P da Tabela 5.2
  −0,01/−0,01/0,02/0,41, ondulação de Q 4,8 → 3,0 virou 3,2 → 2,0 pu.
  Bloco 585 ganhou P = 0,70 pu (1,01 pré-falta) e Q = 0,22 pu; "Feito." no
  #315 (40 → 41). Percentuais de sentido do fluxo (§5.4) não mudam.
- 1ª entrega abortou: o Bruno salvou o V10 às 14h56 (só estilos renomeados,
  texto e comentários iguais); reaplicado sobre ele. Há um V11 (Victor,
  14h49) com o mesmo texto: o Victor confirmou que o canônico segue o V10.
  Entregue `cf77f1ac…`, backup `_20261003_152345`.

## 2026-10-03 (14h16) — Figura 4.2 com letras maiores (V10)

- Oscar (#190, 1ª parte): "gostaria que as letras tivessem um tamanho maior".
  O `vsi_lcl_pwm_circuit.svg` tinha `viewBox` 900×780 e fontes de 8-15 px:
  4-7,5 pt na página. Sem título interno (repetia a legenda), `viewBox`
  recortado para `40 45 840 730` e fontes de 14-18 px (7,6-9,8 pt).
  Subscritos que caíam sobre seta ou borda foram reposicionados, e a nota
  do Submódulo perdeu o "—". Os dois `θ̂_PLL` viraram `θ_PLL` (chapéu
  combinante sai deslocado, armadilha 2 da skill `svg-diagrams`).
- Troca do `media/image10.png` (rId23), cy 4992624 → 5006340. Finalize
  82 págs → audit 0 → entregue (`428d3a77…`); o `θ` foi numa 2ª entrega já
  pelo `troca_imagem.py` (`90879eba…`, backup `_20261003_141940`).
- **#190 segue aberto, sem "Feito."**: a 2ª parte pede uma caixa de regime
  permanente (entradas Pmppt, Qmppt, Vpcc; saídas as referências dq), ainda
  não feita.
- Virou ferramenta: `tcc-docx-editor/scripts/troca_imagem.py`.

## 2026-10-03 (14h03) — "Referência" no início do §5.1 (V10)

- Oscar (#221): "a referência de que?" no bloco 511. Virou "mostra as
  componentes de eixo direto e de quadratura da tensão com a sintonia nominal,
  que serve de base de comparação para a sintonia inadequada"; "valores
  contínuos" → "constantes". #221 reancorado em "base de comparação", "Feito.".
- `C:\Temp\tcc_ref51\gen_ref51.py` → audit 0 → entregue (`58e4be8f…`); o Word
  regravou o canônico ao fechar, staging refeito antes da entrega.

## 2026-10-03 (12h23) — Comentários do Oscar após a Figura 5.8: 3 tabelas e 2 figuras (V10)

- 13 abertos entre os blocos 543 e 599. Pedido do Victor: números em
  sequência no texto viram tabela ("nosso relatório carece de tabelas").
- **Novas:** Tabela 5.1 (trifásicas nominais: retenção, pico, retorno, 120 Hz),
  Figura 5.9 (`bus7_3phase_corrente_dq.png`, #266), Tabela 5.2 (rampa do ONS ×
  `iq_ref` simulado, #268/#344), Figura 5.10 (`espectro_vd_falta.png`, gerada por
  `scripts/gen_espectro_vd.py`, #275), Tabela 5.3 (assimétricas, #276/#277).
  Figuras antigas 5.9-5.19 → 5.11-5.21 (24 remissões). Primeiras tabelas
  Word do TCC (estilo IBGE, sem bordas verticais, `tblHeader`, `keepNext`).
- Métricas pela receita de [[tcc-revisao-fragmento-cap5-metricas]]; rampa
  `i_q = (0,85 − V)/0,35` aplicada ao `|V|` médio do inversor. Fecha bem em
  corrente (Barra 6: rampa 0,76, `iq_ref` médio 0,72, final 0,78).
- "Feito." em 266-269, 272, 273, 275-277, 344, 345; resposta escrita no #347.
  **#300 ficou sem resposta**: Q medido ≠ V·i_q na mesma base (fator ≈ 1,5),
  a conferir antes de citar Q médio. Ver [[tcc-pendencias]].
- `C:\Temp\tcc_oscar58\gen_oscar58.py` → finalize 82 págs → audit 0 →
  entregue (`cfb354f3…`); backup `_20261003_122344`. O MD5 do OneDrive mudou
  entre a conferência e a cópia porque o Word regravou o arquivo ao fechar;
  backup conferido: texto e comentários idênticos ao staging.

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
