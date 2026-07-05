---
name: python-pipeline
description: Arquitetura Python (src/) que consome sim_data.csv — SimData, ChartBuilder, painéis, métricas
---

# Pipeline Python: `src/`

```
app.py                  ← entry point (python app.py [--out PATH]); varre output/results/**/sim_data.csv
src/
├── __init__.py         → reexporta SimData, ChartBuilder, HTMLRenderer (API pública)
├── config/
│   └── settings.py     → T_FAULT, TOL_RAD, thresholds, paletas, caminhos
├── pipeline/            → CSV → dados → figuras Plotly
│   ├── loader.py         → SimData: lê sim_data.csv + sim_data_angles.csv, calcula métricas
│   └── chart.py           → ChartBuilder: subplots Plotly (usa t_fast p/ painéis de ângulo)
└── report/               → figuras → HTML
    └── renderer.py         → HTMLRenderer: HTML multi-cenário com tema light/dark
```

Reorganizado em subpacotes (2026-07) — antes eram 4 arquivos soltos em `src/`.
`src/__init__.py` continua a única superfície pública; `app.py` não referencia
os subpacotes diretamente. Imports internos usam `..config`/`..pipeline` (relativos
ao nível do subpacote, não ao topo de `src/`).

> ⚠️ **Gotcha `PROJ_ROOT`**: `src/config/settings.py` está um nível mais fundo
> que o antigo `src/config.py`. `PROJ_ROOT = Path(__file__).resolve().parent.parent.parent`
> (3× `.parent` — settings.py → config/ → src/ → raiz). Se um subpacote for
> movido de nível novamente, recalcular essa contagem; um `.parent` a menos
> quebra `CSV_PATH`/`HTML_OUT`/o SVG do mapa unifilar silenciosamente
> (`PROJ_ROOT` aponta para `src/`, `assets/` não é encontrado, mapa some do HTML).

Ver `kb/simulation/export_workflow.md` para o formato de `sim_data.csv` consumido aqui.

## Painéis gerados por `ChartBuilder`

### Seção Inversor (`_inv_rows`)

| Painel | Kind | Condição | Conteúdo |
|--------|------|----------|----------|
| Ângulo (°) | `ang` | `has_ang` | θ Rede + θ̂ PLL |
| Erro de fase (°) | `err` | `theta_err is not None` | erro com banda ±TOL_RAD |
| Corrente dq UFV (pu) | `dq_combined` | `has_dq_ufv` | id/iq medido (+ ref se `has_ref_ufv`) |
| Tensão dq (pu) | `vdq_combined` | `has_vdq_ufv or has_vdq_rede` | Vd/Vq rede + inversor |
| P / Q UFV (pu) | `pq_combined` | sempre | P e Q do UFV |

### Seção Sistema (`_sys_rows`)

Painéis agrupados por barra (não combinados), na ordem Bus 2 → Bus 1 → Bus 3
— facilita comparar cada barra isoladamente:

| Painel | Kind | Condição | Conteúdo |
|--------|------|----------|----------|
| \|V\| Bus 2 (pu) | `vbus2` | `has_vbus2` | \|V\| Bus 2 + linha LVRT |
| \|V\| Bus 1 (pu) | `vbus1` | `has_vbus1` | \|V\| Bus 1 + linha LVRT |
| P Bus 1 (pu) \| Q Bus 1 (pu) | `p_bus1` / `q_bus1` | `has_pq_bus1` | P/Q da Barra 1, lado a lado |
| \|V\| Bus 3 (pu) | `vbus3` | `has_vbus3` | \|V\| Bus 3 + linha LVRT |
| P Bus 3 (pu) \| Q Bus 3 (pu) | `p_bus3` / `q_bus3` | `has_pq_bus3` | P/Q da Barra 3, lado a lado |

> Painéis "Ângulo rotor (δ G1/G3)" e "Pe geradores" foram **removidos** (2026-07) —
> ângulo de rotor não normalizado crescia linearmente e perdeu relevância na análise
> atual. Os dados brutos (`ang_g1`, `pe_g1`, `ang_g3`, `pe_g3`) continuam sendo
> exportados/carregados por `SimData`, só não são mais plotados.

## Formatação dos eixos (`ChartBuilder._apply_layout`)

`update_yaxes(exponentformat="none")` global — desativa o auto-prefixo SI do
Plotly (µ/k/M) nos ticks do eixo Y. Necessário porque pu é adimensional: sem
essa opção, valores pequenos (ex. P/Q de barra em regime) ganhavam rótulos
tipo "2µ", que não fazem sentido fora de unidades físicas (W, V etc.).

> ⚠️ **Gotcha `_label` em linhas `_P` (pair)**: `xref` do rótulo de painel
> **tem** que ser `f"x{ax_idx} domain"` (relativo ao eixo x daquela coluna),
> nunca `"paper"`. Com `"paper"`, `x=0.01` sempre cai na borda esquerda da
> figura inteira — em linha `_S` (largura cheia) isso coincide com a borda do
> próprio painel, mas em linha `_P` o rótulo da coluna 2 (ex. "Q Bus 1 (pu)")
> era desenhado sobre o painel da coluna 1, fantasma atrás da legenda.

## Subtítulo de grupo por barra (`ChartBuilder._group_title`)

Linhas de `_sys_rows()` aceitam um 4º elemento opcional (`str | None`) com o
nome do grupo (ex. `"Barra 1"`) — setado só na 1ª linha de cada barra, `None`
nas seguintes, para não repetir o subtítulo. `_make_figure` detecta
`has_groups = any(len(r) == 4 and r[-1] for r in rows)` e passa `extra_top=True`
para `_apply_layout`, que aumenta a margem superior da figura (`t=34` vs `t=16`)
— sem isso o subtítulo do 1º grupo (que fica *acima* do domínio da 1ª linha,
`y=1.16` em coordenada de domínio) é cortado pela margem padrão.
`_group_title` usa `xref="paper"` (rótulo de grupo é full-width, diferente de
`_label` que é por-coluna) + uma linha divisória (`add_shape`) em `y=1.08`.

## Lógica de leitura em `SimData`

1. Lê `sim_data.csv` → `self.t`, `self.P_ufv`, `self.Q_ufv`, correntes dq UFV.
2. Procura `sim_data_angles.csv` na mesma pasta:
   - **Se existe**: carrega `t_fast`, `theta_pll_fast`, `theta_ref_fast`; aplica
     baseline correction (remove drift pré-falta); interpola `theta_err` para `self.t`.
   - **Fallback legado**: lê colunas de ângulo de `sim_data.csv` se presentes.
3. Cada grupo de colunas opcionais expõe um par `has_X` (bool) + atributo(s) `None`
   quando ausente — permite CSVs antigos carregarem sem erro.

## Atributos expostos por `SimData` (além de ângulo/dq/vdq)

| Atributo | Flag | Descrição |
|---|---|---|
| `vbus1`, `vbus2`, `vbus3` | `has_vbus1/2/3` | \|V\| de barra, pu relativo à média pré-falta |
| `p_bus1`, `q_bus1` | `has_pq_bus1` | P/Q Barra 1, pu (base 100 MVA) |
| `p_bus3`, `q_bus3` | `has_pq_bus3` | P/Q Barra 3, pu (base 100 MVA) |
| `ang_g1`, `pe_g1` | `has_gen1` | ângulo (rad) / Pe (pu) do rotor G1 — **não plotado**, só carregado |
| `ang_g3`, `pe_g3` | `has_gen3` | idem para G3 — **não plotado**, só carregado |

## `t_fault`/`t_clear` por cenário (`SimData.__init__`)

`SimData` lê `fault_info.json` (salvo por `export_sim_data.m` ao lado do CSV,
ver [[export-workflow]]) e expõe `self.t_fault`/`self.t_clear` (float ou `None`).
`fault_type == "regime"` → ambos `None` (sem falta, sem linha nos gráficos).
Fallback: `T_FAULT` de `config/settings.py` só é usado se o JSON não existir.
Este valor real (não a constante global `T_FAULT`) é o que alimenta:
- `ChartBuilder._vline` — duas linhas tracejadas (vermelha em `t_fault`,
  cinza em `t_clear`) em todo painel de série temporal; nenhuma em regime.
- `_compute_metrics` e a baseline correction do ângulo (linha 91-95) — janela
  `t ≥ t_fault` real do cenário, não mais a constante desatualizada.
- `HTMLRenderer` — `sc_js[key]["tFault"/"tClear"]` viaja para o JS; a função
  `updateFaultUI(sc)` atualiza o header e os badges "Falta: t = X – Y s" a
  cada `switchScenario`, e `_cards_html`/`_story_html` usam
  `data.t_fault or T_FAULT` no lugar da constante global para `Δt = ts − t_fault`.

## Métricas calculadas (`_compute_metrics`)

| Métrica (chave dict) | Fórmula | Janela |
|---|---|---|
| `IAE` | ∫\|θ_err\| dt | t ≥ t_fault |
| `ISE` | ∫θ_err² dt | t ≥ t_fault |
| `ts` | último t com \|θ_err\| > TOL_RAD | t ≥ t_fault |
| `dP_ufv` | max(P_ufv) − min(P_ufv) | t ≥ t_fault |
| `dQ_ufv` | max(Q_ufv) − min(Q_ufv) | t ≥ t_fault |
| `vmin` | min(vbus2_pu) | t ≥ t_fault |

`t_fault` acima é `self.t_fault` (real do cenário, fallback `T_FAULT` global).
`np.trapezoid` (NumPy ≥ 2.0). Baseline correction: subtrai `theta_err[idx_fault-1]`
antes de `t_fault` para zerar drift da Repeating Sequence de referência.

## Rodar

```powershell
# Exportar do MATLAB (após simular): >> export_sim_data   (Command Window)

.venv\Scripts\python.exe app.py
.venv\Scripts\python.exe app.py --out output/relatorio.html
```

## Decimação de traces no HTML (`ChartBuilder._add`, 2026-07)

Histórico: nenhuma camada do pipeline fazia downsampling dos arrays antes de
serializar para Plotly — cada trace ia para o JSON embutido no `<script>`
inline do `renderer.py` na resolução nativa do CSV. Com `sim_data.csv` em
120.002 linhas (Tsc) × ~17 traces/cenário, `output/pll_metrics.html` chegou a
**~175 MB** com 4 cenários e **~570 MB** com 12 (incl. `bad_pll`, 200.002
linhas). Sintoma: cards/gráficos vazios no primeiro load — script grande
demais para o browser parsear a tempo (recarregar eventualmente resolvia).

Fix implementado em `_add` ([chart.py](../../../src/pipeline/chart.py)):
decimação por passo uniforme, cap `_MAX_POINTS = 5000` por trace —
`step = ceil(len(x) / 5000)`, depois `x[::step]`, `y[::step]`. Ponto único
de aplicação: todo `go.Scatter` passa por `_add` antes de `fig.add_trace`,
então nenhuma chamada em `_add_panel` precisou mudar.

**Por que não decimar em `loader.py`**: `_compute_metrics` (IAE/ISE/ts/ΔP/ΔQ)
usa os arrays brutos de `SimData` (`theta_err`, `P_ufv`, etc.) — decimar ali
enviesaria as métricas. A decimação fica isolada em `chart.py`, que só cuida
de visualização; `loader.py` continua entregando resolução total.

**Trade-off aceito**: transientes muito estreitos (ex. o instante exato do
afundamento) podem perder forma exata entre duas amostras decimadas — mas
`t_fault`/`t_clear` continuam marcados por `_vline` independente da
decimação, então o instante em si não se perde, só a curva entre amostras.
