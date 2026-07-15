---
name: cards-metricas
description: Cards em 3 grupos (severidade / desempenho PLL / recuperação) com semáforo good/warn/bad, estado "não acomodou", pico de erro de fase e diagnóstico em lista de tópicos com veredito só de desempenho
---

# Cards de Métricas e Diagnóstico Narrativo (renderer.py)

Gerados **em Python** por cenário (`_cards_html`, `_story_html`) e embutidos
prontos no JS (`SCENARIOS[key].cardsHtml` / `.storyHtml`) — `switchScenario`
só injeta o HTML em `#cards-area`/`#story-area`, sem recomputar nada no browser.

## 3 grupos de cards (`_cards_html`)

| Grupo | Cards | Papel |
|---|---|---|
| Severidade do distúrbio | V residual B2 (pu, POC do inversor, vs LVRT), V residual B1/B3 (quando `vbus1_pu`/`vbus3_pu` existem no CSV — propagação do sag; subtítulos "barra do G1 (slack)"/"barra do G3"), Duração da falta (ms, t_fault–t_clear) | **Contexto** — quão dura foi a falta; fora do veredito |
| Desempenho do PLL | IAE (rad·s), ISE (rad²·s), tₛ (s, ±1.15°), \|θ_err\| pico (°) | Julga o PLL |
| Recuperação do inversor | ΔP UFV, ΔQ UFV (pu, **pós-clear**) | Julga a recuperação após eliminar a falta |

Fonte: `metrics` do [[pipeline-dados]] (duas janelas: pós-falta e pós-clear).
Em regime permanente: grupo de severidade vira "Sistema 9-Bus" (sem card de
duração), subtítulo de ΔP/ΔQ vira "regime", story tem narrativa própria.

**"V residual"** (2026-07-14): tensão remanescente do afundamento — termo do
PRODIST Módulo 8 / IEC 61000, escolhido pelo usuário no lugar de "V min" para
comunicar "quanto caiu durante o curto". Em **regime** (sem curto) o nome
volta a "V min B1/B2/B3" (variável `vlab` em `_cards_html`). O texto do item
"Distúrbio" no story também usa "V residual = X pu". A tabela comparativa
mantém "Vmin B1/B2/B3 (pu)" — genérico, vale também para a linha de regime.

Estados especiais:
- **tₛ "não acomodou"** (`settled = False`): valor "> t_end s", classe `bad` —
  substitui o tₛ falso que reportava a última amostra da simulação.
- **\|θ_err\| pico ≥ `SYNC_LOSS_DEG` (90°)**: subtítulo vira
  "perda de sincronismo" (escorregamento do PLL, ex. BAD_PLL com 178°).

Cada card: nome, valor (ou "—" se `None`), unidade, subtítulo e tooltip via `title=`.

## Semáforo (`_classify`)

Thresholds em `config/settings.py`: `IAE_THRESH`, `ISE_THRESH`,
`TS_DELTA_THRESH`, `DP_THRESH`, `DQ_THRESH` (pós-clear),
`PEAK_ERR_DEG_THRESH`, `VBUS_MIN_THRESH` (`lower_is_better=False`; mesma
escala para V min das barras 1, 2 e 3 — mas o veredito LVRT usa só a B2).
Para tₛ o classificado é `ts_delta = tₛ − t_fault` (vem pronto do loader).
Calibrados sobre a distribuição real dos 12 cenários (2026-07): recuperação
limpa ΔP ≈ 0.02–0.06, problemática ≈ 1.7–3.4; pico saudável 1°, faltas
trifásicas remotas ~26–35° (warn), BAD_PLL 178° (bad).

Os mesmos thresholds/classes alimentam a tabela comparativa
(`_table_row_data` → `metricsRow`) — ver [[comparison-table]].

## Story: diagnóstico em tópicos (`_story_html`)

Lista `<ul class="story-list">` (antes era parágrafo corrido). Cada item é
uma tupla `(classe, rótulo, texto)` renderizada como `<li>` com rótulo em
negrito e bolinha `::before` colorida pela classe do semáforo daquela
métrica (mesmas cores dos cards; `neutral` usa `var(--muted)`).

Ordem fixa dos itens: **Distúrbio** (falta de X ms, profundidade do sag vs
LVRT — vira "Cenário" neutro em regime) → **Pico de fase** →
**Acomodação** (ou "não reacomodou") → **Erro acumulado** (IAE) →
**Recuperação** (ΔP pós-clear, rótulo em falta) ou **Oscilação de potência**
(ΔP em regime, para refletir instabilidade induzida pelo PLL sem
contingência). Redação específica por classe, encurtada porque o rótulo já
carrega o assunto. Item só aparece nas mesmas condições das frases antigas
(ex.: pico `good` continua omitido). Sem `parts`, fallback
`<p class="story-text">Dados insuficientes…</p>`.

**Veredito** (chip à direita): pior classe entre as métricas de
**desempenho/recuperação** (IAE, ISE, tₛ/settled, pico, ΔP, ΔQ) — `V min NÃO
entra`: falta severa com PLL exemplar não vira "crítico" (ex. Barra 8
trifásica: V_min 0.107 mas veredito "em atenção"). Labels: `bad` →
"Desempenho crítico", `warn` → "Desempenho em atenção", `good` →
"Desempenho bom", nada disponível → "Dados insuficientes". A classe também
colore a borda esquerda do bloco `.story`; título vira "Diagnóstico —
regime permanente" quando não há falta.
