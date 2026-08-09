---
name: pipeline-dados
description: SimData (loader.py) — leitura dos CSVs do MATLAB, correção do erro de fase, métricas na janela pós-falta (tₛ de acomodação e V médio por barra) e frequência estimada do PLL
---

# Pipeline de Dados (src/pipeline/loader.py)

`SimData(csv_path)` carrega um cenário e expõe arrays NumPy + `metrics`.
Descoberta de cenários e roteamento BAD_PLL: ver `kb/simulation/export_workflow.md`.

## Três CSVs por cenário + fault_info.json

| Arquivo | Taxa nominal | Conteúdo |
|---|---|---|
| `sim_data.csv` | Tsc = 200 µs (eixo `t`) | P/Q UFV, correntes dq, tensões de barra, P/Q de barra, geradores |
| `sim_data_angles.csv` | Ts = 5 µs (eixo `t_fast`) | `theta_pll_rad`, `theta_ref_rad`, `theta_err_rad` |
| `sim_data_abc.csv` | nativa de `iabc_inverter` (eixo `t_abc`) | `ia/ib/ic_ufv_pu` + `va/vb/vc_ufv_pu` (+ `_grid_pu` de ambos se logado) — flags `has_iabc_ufv`/`has_vabc_ufv`/`_grid`; opcional, paineis abc do espectro |
| `fault_info.json` | — | `fault_type`, `t_fault`, `t_clear` reais do cenário |

> ⚠️ **Taxas invertidas nos CSVs atuais** (medido 2026-07-12): `sim_data.csv`
> está com dt = 5 µs (120.001 amostras/0,6 s) e `sim_data_angles.csv` com
> dt = 200 µs (3.001 amostras) — o oposto do nominal acima. Loader e
> SpectrumBuilder são imunes (interpolação/`dt` mediano), mas o "eixo rápido"
> dos ângulos hoje tem MENOS resolução que o lento. Verificar no modelo se a
> troca de decimação no logging foi intencional antes de confiar em análises
> que dependam da resolução de θ (ripple de chaveamento, por ex.).

- `fault_type == "regime"` → `t_fault = t_clear = None` (sem linhas de falta,
  botão de zoom desabilitado no HTML).
- Sem `fault_info.json` → fallback `T_FAULT` de `config/settings.py`.
- Colunas opcionais viram flags `has_*` (`has_dq_ufv`, `has_vbus2`, `has_gen1`,
  `has_pq_bus1`, `has_vdq_ufv`, …) — o ChartBuilder só monta painel se a flag
  estiver ligada. Geradores usam sufixo `_g1`/`_g3`.

## Correção do erro de fase (theta_err)

1. **Wrapping**: `Ang_pll`/`Ang_Rede` são dente-de-serra (0→2π→0); a diferença
   bruta tem spikes de ±2π em resets desalinhados. `arctan2(sin, cos)` leva
   para [−π, π].
2. **Baseline**: subtrai o valor do erro na última amostra antes de `t_fault`,
   re-wrapping em seguida — tₛ e o painel de erro mostram só o desvio induzido
   pela falta, não o drift pré-existente do Repeating Sequence de referência.
3. A mesma correção (wrapping + baseline do eixo lento) é aplicada ao eixo
   rápido `theta_err_fast`.

O erro do eixo rápido é interpolado para o eixo lento (`np.interp`) antes da
correção — as métricas são calculadas no eixo lento.

## Métricas (`_compute_metrics`) — janela pós-falta

- **Pós-falta** (`t ≥ max(t_fault, T_SETTLE)`): acomodação do erro de fase (tₛ).
- **Regime** (`t_fault` None): `t ≥ T_SETTLE`.
- **`vavg`/`vavg_bus1`/`vavg_bus3`** usam uma janela própria, diferente da
  acima (2026-07-25): sempre começam em `t_start` (mesmo piso `T_SETTLE`),
  mas em falta **terminam em `t_clear`** — não vão até o fim da simulação.
  Ver linha da tabela abaixo.

Métricas removidas do `metrics` ao longo do tempo:

- `dP_ufv`/`dQ_ufv` (excursão máx-mín de P/Q na janela pós-clear), 2026-07-24
  — não faziam sentido como métrica de desempenho do PLL.
- **`IAE`, `ISE`, `peak_err`, `ts_delta`, `t_ss`, `err_ss_mean`,
  `err_ss_rms`, 2026-08-09** — todas derivadas do erro de ângulo, sem fonte
  que sustente acúmulo/média/pico como medida de desempenho do PLL; saíram
  junto com os cards que as exibiam (ver [[cards-metricas]]).

Em ambos os casos, só a métrica derivada saiu: `t_clear` continua sendo lido
de `fault_info.json` (card de duração da falta, linhas de falta no gráfico)
e `theta_err`/`theta_err_fast` continuam alimentando o painel "Erro de fase".

**`T_SETTLE = 0.1 s`** (settings.py, 2026-07-12): nenhuma janela de cálculo
começa antes disso — a partida do PLL (trava em ~0.08 s; pior sinal é |V|
Bus 2 em 0.078 s) é inicialização, não desempenho, e fica fora do cálculo de
tₛ, da média de |V| e da FFT ([[espectro-fourier]]). Com `t_fault = 0.3 s` o
clamp é inócuo nas faltas; muda o regime (antes usava `T_FAULT = 0.2` de
fallback). ⚠️ A normalização pu do MATLAB (`Vnom = mean(vmag(t < T_FAULT))`
em `export_sim_data.m`) ainda inclui a partida → viés de ~1.1% em
`vbus*_pu`/`vd/vq` (regime lê 0.9887 pu); correção ficou fora do escopo
(decisão do usuário: só Python) e exigiria re-exportar.

| Métrica | Definição |
|---|---|
| `ts` / `settled` | última amostra com \|e\| > `TOL_RAD` (±0.02 rad ≈ ±1.15°). Se \|e\| ainda está fora nos últimos 2 ms da janela → `ts = None`, `settled = False` ("não acomodou" — evita tₛ falso no fim da simulação). **Regime → sempre `None`/`None`**: sem distúrbio não há o que acomodar. Único consumidor hoje é o marcador tₛ do gráfico ([[chart-analysis-overlays]]) |
| `vavg` | **média** (não mínimo, desde 2026-07-25) de `vbus2` — regime: janela inteira `[T_SETTLE, fim]`; falta: só o período do curto `[t_start, t_clear]` (ou fim, se `t_clear` for `None`) — severidade vs LVRT |
| `vavg_bus1`, `vavg_bus3` | idem para `vbus1`/`vbus3` — propagação do sag pela rede (cards de severidade + colunas V méd. B1/B3 na tabela) |

Sinal ausente → métrica `None` → "—" nos cards/tabela.

`ts`/`settled` sobreviveram à limpeza de 2026-08-09 porque o **instante de
acomodação importa**: interessa saber como o PLL retorna pós-falta. O que caiu
foi a exibição como card com semáforo; o critério em si segue em revisão —
[[pll-ts-criterion-rationale]].

## Consumidores do SimData

- `ChartBuilder` (séries temporais) — [[construcao-graficos]]; usa
  `metrics["ts"]` no marcador de acomodação.
- `SpectrumBuilder` (FFT segmentada pré-falta/falta/pós-falta em dB) —
  consome `t`/`t_fast`, `theta_err(_fast)`, `iq_ufv_meas`, `Q_ufv` e
  `t_fault`/`t_clear`; ver [[espectro-fourier]].
- `HTMLRenderer` (cards/story/tabela) — usa `metrics` direto, hoje só
  `vavg*` e `t_fault`/`t_clear`.
