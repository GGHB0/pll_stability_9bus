---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

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

## 2026-10-01 (23h30) — "Reaquisitar" fora do texto (V10)

- 14 trocas por "recuperar/retomada do sincronismo" (Cap. 4 a 7), segmento a
  segmento nos `<w:t>` (`C:\Temp\figs\gen_reaquisita.py`). Três já tinham
  virado "requisitar" no Word, que também está errado. Comentário `[Claude]`
  em cada trecho; "Feito." no do Oscar ("Acho que essa palavra não existe").
- O Victor reverteu a decisão de 2026-09-12 de manter a palavra; regra em
  `revisao_pt.md` da skill. 1ª entrega abortou por MD5 (save sincronizado,
  texto idêntico) → backup `V10_backup_20261001_233613`.

## 2026-10-01 (23h59) — Texto antes das figuras nos Caps. 4 e 5 (V10)

- 19 parágrafos "A Figura X…" movidos (`w:p` inteiro, âncoras do Oscar
  junto) para antes da legenda: Figuras 4.1-4.3, Tabela 4.1 e todo o Cap. 5;
  pares 5.1/5.2, 5.5/5.6 e 5.10/5.11 com o texto acima do par. Regra nova no
  item 6 de `padroes_revisao.md` da skill tcc-docx-editor.
- Remissões com número antigo corrigidas: 5.5→5.6, 5.6→5.8, 5.12→5.15,
  5.4→5.5, 5.13→5.17, 5.15→5.19 e o par 5.12/5.13→5.16/5.17.
- Figuras 5.10/5.11 reescritas: mesmas escalas de tempo e de amplitude;
  v_d de −0,02 a 1,35 pu (nominal) contra 0,30 a 1,32 pu (inadequada).
- Números do Cap. 5 reconferidos com `medir_cap5.py`, todos batem (falta de
  0,3 a 0,4 s nos 28 cenários). Duas ressalvas viraram texto: 120 Hz ≤
  0,002 pu e "duas ordens de grandeza" só com sintonia nominal (a trifásica
  da Barra 6 inadequada dá 0,006 pu); §5.5, prolongamento da recuperação
  só "nas contingências mais severas".
- 4 comentários `[Claude]` e resposta ao Oscar no "tensão em regime
  permanente está em 1 p.u." (as duas sintonias partem de 1,00 pu).
- **Pipeline**: `C:\Temp\figs\gen_figuras_antes.py` (refeito sobre o save do
  Victor das 23h52) → finalize (78 págs) → audit 0 falhas → backup
  `V10_backup_20261001_235907`.

## 2026-10-01 (23h) — Gráficos de erro de fase no Cap. 5 (V10)

- 4 figuras novas (legenda SEQ + imagem + Fonte via `campos.py` + parágrafo
  de chamada): 5.3 energização, 5.7 trifásicas nominais, 5.12 assimétricas,
  5.16 perda de sincronismo. Cap. 5 passou a 19 figuras, documento a 77
  págs. Mapa em [[tcc-revisao-fragmento-cap5-figuras]].
- Citações em texto fixo renumeradas num passo único pelo mapa antigo→novo.
  **Armadilha:** o Word partiu "A Figura " | `proofErr` | "5.9 mostra" em
  runs separados; o regex por `<w:t>` não pegou e a chamada ficou errada até
  a conferência legenda × chamada. Tratar o caso partido antes do passo geral.
- "Feito." nos 4 pedidos de gráfico angular do Oscar; 4 comentários
  `[Claude]`. Rótulo do painel vazio do gerador virou "fora da comparação".
- 1ª entrega abortou por MD5 (OneDrive sincronizou o save do Word ao fechar;
  texto idêntico). Refeito sobre a versão nova → backup
  `V10_backup_20261001_230942`.

## 2026-10-01 (22h30) — Texto do Cap. 5 para a safra de 01/10 (V10)

- 26 trocas por paraId, segmento a segmento dentro de `<w:t>`, preservando
  as âncoras do Oscar (`C:\Temp\figs\gen_texto_cap5.py`; métricas de
  `medir_cap5.py`, receita de [[tcc-revisao-fragmento-cap5-metricas]]).
- Muda a tese da §5.3: a sintonia inadequada recupera **mais rápido** nas
  assimétricas da Barra 6 (30/31 ms × 48/39 ms; ondulação de Q 4,8→3,0 pu) e
  mais devagar na bifásica da Barra 7 (51→96 ms) e na trifásica da Barra 6
  (76→106 ms); o compromisso passa a depender da severidade. Saiu o "ponto
  de operação degradado" (regime inadequado converge a 1,00 pu, 79 ms), saiu
  o par monofásico da Barra 7 (reprovado), a Linha 7-8 entrou na perda de
  sincronismo (§5.4) e a janela pós-falta passou a 200 ms (Cap. 4 bloco 487
  e §5.4).
- 15 comentários `[Claude]`, um por trecho; "Feito." nos do Oscar sobre
  grandeza/ordem de grandeza, tensão degradada, ponto de operação, escala de
  tempo e 0,823 pu. O "Não entendi." ficou sem resposta (dois comentários
  com o mesmo início). Cap. 6 não foi tocado.
- Finalize (74 págs) → audit 0 falhas → backup `V10_backup_20261001_223143`.

## 2026-10-01 (22h) — Gráficos da safra de 01/10 no V10

- Troca só da mídia (`word/media/imageN.png`) de 12 ilustrações pelos PNGs
  regenerados: Tabela 4.1 (`image11`), Figuras 5.1-5.3 (`image12`-`14`) e
  5.8-5.15 (`image19`-`26`). Proporções idênticas, `cy` inalterado. As
  Figuras 5.4-5.7 já eram iguais a `assets/`. Mapa em
  [[tcc-revisao-fragmento-cap5-figuras]].
- **Texto não mexido**: comentário `[Claude]` na abertura do Cap. 5 avisa da
  troca e dos números antigos (563→79 ms; 34,9°/78 ms→34,5°/30 ms; Linha 7-8
  trifásica também perde sincronismo). Revisão dos números fica pendente,
  com tabela em [[cenarios-simulados]]. Gráficos `erro_fase_*` não inseridos.
- **Pipeline**: `C:\Temp\figs\gen_troca_figuras.py` → finalize com
  `-Comments` (74 págs) → audit 0 falhas → backup `V10_backup_20261001_222015`.

## Entregas de 2026-10-01 (dia)

Ver [[tcc-historico-entregas-2026-10-01]]: citações de alto risco corrigidas e
referências pedidas pelo Oscar.

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
