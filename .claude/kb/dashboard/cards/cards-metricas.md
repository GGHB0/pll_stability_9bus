---
name: cards-metricas
description: Cards de métricas em 3 grupos com semáforo good/warn/bad e diagnóstico narrativo (story) com veredito por cenário
---

# Cards de Métricas e Diagnóstico Narrativo (renderer.py)

Gerados **em Python** por cenário (`_cards_html`, `_story_html`) e embutidos
prontos no JS (`SCENARIOS[key].cardsHtml` / `.storyHtml`) — `switchScenario`
só injeta o HTML em `#cards-area`/`#story-area`, sem recomputar nada no browser.

## 3 grupos de cards (`_cards_html`)

| Grupo | Cards | Fonte |
|---|---|---|
| Desempenho do PLL | IAE (rad·s), ISE (rad²·s), tₛ (s, critério ±1.15°) | `metrics` do [[pipeline-dados]] |
| Inversor UFV | ΔP UFV, ΔQ UFV (pu, pós-falta) | idem |
| Sistema 9-Bus | V min (pu, Barra 2, vs LVRT) | idem |

Cada card: nome, valor (ou "—" se `None`), unidade, subtítulo (ex.: "∫|e| dt")
e tooltip via `title=`.

## Semáforo (`_classify`)

Thresholds em `config/settings.py`: `IAE_THRESH`, `ISE_THRESH`,
`TS_DELTA_THRESH`, `DP_THRESH`, `DQ_THRESH`, `VBUS2_MIN_THRESH`.
Classe CSS `good`/`warn`/`bad` (borda/fundo do card) — `lower_is_better=False`
só para V min. Para tₛ o classificado é o **Δt = tₛ − t_fault**, não o tₛ
absoluto (cenários com t_fault diferente ficam comparáveis).

Os mesmos thresholds/classes alimentam as células da tabela comparativa
(`_table_row_data` → `metricsRow`) — ver [[comparison-table]].

## Story: diagnóstico pós-falta (`_story_html`)

Parágrafo narrativo montado por frases condicionais (uma por métrica
disponível: IAE, Δt de acomodação, V min, ΔP), cada frase com redação
específica para good/warn/bad — ex.: "Afundamento severo na Barra 2
(V_min = 0.123 pu) — condição crítica de LVRT."

**Veredito** (chip à direita do texto): pior classe entre as 4 métricas —
`bad` → "Desempenho crítico", `warn` → "Desempenho satisfatório",
`good` → "Desempenho excelente", nenhuma disponível → "Dados insuficientes".
A classe também colore a borda esquerda do bloco `.story`.
