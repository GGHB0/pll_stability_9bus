---
name: chart-analysis-overlays
description: Overlays de análise nos gráficos — janela de falta sombreada, hierarquia θ̂ PLL vs θ Rede, marcador tₛ, envelope LVRT 1547 Cat II e painel de frequência estimada
---

# Overlays de Análise (chart.py / loader.py)

Adicionados em 2026-07 (pedido do usuário + sugestões aprovadas via AskUserQuestion).

## Janela de falta (`_vline`)

Substituiu as duas vlines finas por um destaque em três camadas, por painel:

- `add_vrect(t_fault → t_clear)` com `fillcolor="rgba(220,50,50,0.07)"`,
  `layer="below"` — a janela inteira do curto fica sombreada;
- vline de **início** vermelha `rgba(220,50,50,0.75)`, `width 2.0`;
- vline de **limpeza** verde `rgba(22,163,74,0.65)`, `width 2.0` (antes era
  cinza — verde comunica "falta eliminada").

Regime permanente (t_fault=None) continua sem marca nenhuma.

## Hierarquia no painel de ângulo (`kind == "ang"`)

θ̂ PLL é o protagonista: **sólido, width 2.4, adicionado primeiro** (pega a
1ª cor da paleta e abre a legenda). θ Rede virou referência de fundo: fino
(1.1), tracejado. Antes era o inverso — a rede tinha mais destaque que o
sinal sob análise.

## Banda de tolerância + marcador tₛ (`kind == "err"`)

- `add_hrect(±TOL_RAD)` verde translúcido (`rgba(22,163,74,0.08)`) — "dentro
  da banda = acomodado"; bordas em linha pontilhada fina verde.
- `_ts_marker()`: diamante verde em `(ts, erro(ts))` com texto `t_s`,
  conectando o card de métrica ao gráfico. Trace adicionado **direto** com
  `showlegend=False` e `marker.legend = self._legend_key` — não passa por
  `_add`, logo fica fora do `trace_map` e mantém cor fixa nos dois temas.

## Painel de frequência (`kind == "freq"`)

`SimData._estimate_freq()` em `loader.py`: `f̂ = dθ̂/dt / 2π` sobre
`theta_pll_fast` (fallback: eixo lento). Diferença central com passo largo
(`k ≈ 0,5 ms` para cada lado) — o passo largo já é o filtro passa-baixa,
sem convolução sobre milhões de pontos:

```python
th_u = np.unwrap(th)
k = max(1, int(round(5e-4 / dt)))
self.f_pll  = (th_u[2*k:] - th_u[:-2*k]) / (t[2*k:] - t[:-2*k]) / (2*np.pi)
self.t_freq = t[k:-k]
```

Atributos novos: `t_freq`, `f_pll`, flag `has_freq`. Painel com hline de
60 Hz. É o sinal clássico de excursão de frequência/RoCoF do PLL.

## Envelope LVRT (`_lvrt_envelope`, só no |V| Bus 2)

Curva degrau V×t do ride-through obrigatório IEEE 1547-2018 **Categoria II**,
ancorada em `t_fault` (constante de classe `_LVRT_STEPS`):

| Δt após a falta | V mínimo |
|---|---|
| até 0.16 s | 0.30 pu |
| até 0.32 s | 0.45 pu |
| até 3.0 s  | 0.65 pu |
| depois     | 0.88 pu (operação contínua) |

Scatter com `line_shape="hv"`, tracejado vermelho, `hoverinfo="skip"`,
`legend = self._legend_key`. Substitui a hline fixa de `LVRT_THRESHOLD`
apenas em `vbus2` com falta; `vbus1`/`vbus3` (e `vbus2` em regime) mantêm a
hline antiga.

## Gotcha ⚠️ traces adicionados fora de `_add`

`_ts_marker` e `_lvrt_envelope` usam `self._fig.add_trace` direto: não entram
no `trace_map`, então o JS (`themedData`) **não** re-tema a cor deles — por
isso as cores escolhidas (verde/vermelho) precisam funcionar nos dois temas.
Definir `trace.legend = self._legend_key` manualmente, senão o item cai na
legenda do primeiro painel.
