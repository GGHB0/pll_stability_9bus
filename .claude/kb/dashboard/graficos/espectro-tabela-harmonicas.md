---
name: espectro-tabela-harmonicas
description: Tabela de harmônicas do dashboard — duas tabelas por domínio (abc/dq), destaque normativo por célula, isenção do segmento de falta e a legenda em duas camadas
metadata:
  type: project
---

# Tabela de harmônicas do espectro (renderer.py)

Parte da aba de espectro descrita em
[espectro-fourier.md](espectro-fourier.md) (FFT, segmentos, seletor de fase e
layout dos gráficos). Aqui fica só a **tabela** abaixo dos gráficos: como é
montada, como cada célula é comparada a limite normativo e como a legenda
explica isso ao leitor.

Origem de cada limite em `kb/standards/harmonic_significance_criteria.md`;
por que abc e dq usam critérios diferentes em
`kb/standards/harmonic_norm_application.md`; condições de medição e pendências
em `kb/standards/harmonic_measurement_conditions.md`.

## Construção e destaque

- **Duas tabelas por domínio, não uma combinada** (2026-08-05,
  `HTMLRenderer._harm_subtable_html`, chamada 2× por bloco em
  `_spec_table_html`): uma tabela **abc** e uma tabela **dq**, para cada um
  dos dois blocos (Corrente UFV / Tensão UFV) — 4 tabelas no total,
  injetadas em `#spec-harm-area` no `switchScenario`. Motivo: abc e dq não
  compartilham semântica por linha (em abc, linha k = k-ésima harmônica,
  checável por ordem; em dq, linha k = bin de colisão de duas ordens abc de
  sequências opostas, só k=2/120 Hz com critério real) — a tabela única
  anterior forçava as duas coisas na mesma linha (mesma frequência k·60 Hz)
  e confundia o leitor.
  - **Tabela abc**: linhas h=1ª…12ª (60–720 Hz), colunas segmento × fase
    (a/b/c). Coluna de linha única "abc: h".
  - **Tabela dq**: linhas **só nos bins fisicamente significativos**
    (`_DQ_TABLE_ROWS`, filtra `_DQ_BIN_ORDERS` descartando as entradas
    "—") — **0 Hz** (fund. (DC), adicionado 2026-08-05, ver "Componente
    DC" acima), 120 Hz (fund. seq. neg.), 180/360/540/720 Hz (colisões
    2ª/4ª, 5ª/7ª, 8ª/10ª, 11ª/13ª). As linhas sem colisão nem fundamental
    (60/240/300/420/480/600/660 Hz) não aparecem — só mostrariam
    ruído de fundo sem nenhum destaque. Colunas segmento × eixo (d/q).
    Coluna de linha única "dq: ordens". Leitura de célula usa `amps[k]`
    (não `amps[k-1]`) desde que o índice 0 passou a ser o DC.
  - Célula sem dado = "—" (ex.: bloco sem os dois kinds i/v). Valores
    `%.3g` pu. CSS: `.harm-table`, separador vertical `.harm-first` entre
    segmentos — reaproveitado das duas tabelas, sem mudança.
- **Destaque normativo** (2026-07-29, `HTMLRenderer._harm_cell_tier`,
  substitui o esquema puramente estético anterior): linha h=1ª recebe
  `.harm-fund` na tabela abc; na tabela dq, a linha 0 Hz (fund. (DC),
  2026-08-05) recebe a mesma classe `.harm-fund` com tooltip próprio —
  reforça que é a fundamental/ponto de operação, não ruído nem harmônico,
  sem ser comparada a nenhum limite; colunas
  abc comparadas por ordem `k` aos limites de `settings.py`
  (`CURR_ODD_LIMIT_PU`=4%, `CURR_ODD_LIMIT_11_16_PU`=2% (11≤h<17, interino —
  ver `harmonic_significance_criteria.md`), `CURR_EVEN_LIMITS_PU`=
  {2:1%,4:2%,6:3%,8:4%}, `VOLT_INDIVIDUAL_LIMIT_PU`=3% — IEEE
  519-2014/1547-2018) → `.harm-viol` com `title=` citando o limite; tabela
  dq, só a linha 120 Hz (k=2) comparada a `DQ_UNBALANCE_WARN_PU`/`_HIGH_PU`
  (2%/3%, TeseAGP) → `.harm-warn`/`.harm-unb`. `_HARM_LO_PU=0.02` continua
  como fallback de "apagado" (`.harm-lo`) quando nenhum critério normativo
  se aplica. Ver `kb/standards/harmonic_significance_criteria.md` para a
  origem de cada limite, e `kb/standards/harmonic_norm_application.md` para
  por que abc/dq usam critérios diferentes e a notação normalizada das
  variáveis de corrente (Isc/IL/I_rated — TDD não é usado).
- **Segmento "Durante a falta" com limite abc RELAXADO ×1,5**, não isento
  (2026-08-09; `SPEC_SEG_LIMIT_FACTOR = {"Durante a falta": 1.5}` substitui
  o antigo `SPEC_SEG_NO_NORM`): a nota 118 do IEEE 1547.2-2023 admite exceder
  os limites em 50% em "startups or unusual conditions", por serem valores de
  projeto para regime acima de 1 h. Ímpar vira 6%, a 2ª vira 1,5%; o tooltip
  cita limite base, fator e a nota. `_harm_cell_tier` lê o fator com
  `SPEC_SEG_LIMIT_FACTOR.get(seg_name, 1.0)`, então segmento fora do dicionário
  usa 1,0. **Efeito**: o segmento de falta passou a acusar violações, onde
  antes nenhuma célula era destacada. O critério de desequilíbrio dq (linha
  120 Hz) não é relaxado em segmento nenhum — é ali que a sequência negativa é
  mais severa.
- **Legenda em duas camadas** (`.harm-legend`, ajustada 2026-08-05 para a
  separação abc/dq e para a linha DC): linha compacta sempre visível com os
  swatches (`.harm-leg-sw` + `.harm-leg-viol`/`-warn`/`-unb`/`-lo`) e um
  `<details class='harm-help'>` "Como ler esta tabela" com um bloco por
  critério — conformidade a/b/c, desequilíbrio + linha DC + linhas
  informativas em dq, e o `*` de "Durante a falta". Fecha com as referências
  em forma curta (`.harm-refs`). Tokens de tema `--danger`/`--warn` no CSS
  (`_css()`).
- **Regra editorial da legenda**: a tela carrega só **a regra aplicada**
  (qual limite, de qual norma). A *genealogia* do número — razão Isc/IL,
  nota "c" da Tab.2 do IEEE 519-2014, por que `IL` foi descartado — fica no
  KB (`kb/standards/harmonic_norm_application.md`), não no HTML. Ver a seção
  "O que vai na tela vs. o que fica no KB" lá.
