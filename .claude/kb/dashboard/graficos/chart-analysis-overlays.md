---
name: chart-analysis-overlays
description: Overlays de análise nos gráficos — janela de falta sombreada, hierarquia θ̂ PLL vs θ Rede, marcador tₛ, envelope LVRT 1547 Cat II e faixa de frequência ONS §5.2.1
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

### Faixa ONS §5.2.1 (2026-07-28)

`add_hrect` verde (58,5–62,5 Hz, operação contínua) + duas `add_hline`
tracejadas vermelhas (56 Hz / 63 Hz, trip instantâneo) sobrepostas à curva
`f̂ PLL` — mesmo padrão visual da banda de tolerância do painel `err` e do
envelope LVRT. Constantes em `config/settings.py`: `FREQ_CONTINUOUS = (58.5,
62.5)`, `FREQ_TRIP_MIN = 56.0`, `FREQ_TRIP_MAX = 63.0`. Fonte: ONS Submódulo
2.10 §5.2.1 (eólica/UFV) — ver
[ons_frequency_ride_through.md](../../standards/ons_frequency_ride_through.md).
Zona intermediária (56–58,5 / 62,5–63 Hz, trip temporizado ≥20 s/10 s) não
entrou como faixa separada — teria critério de tempo mínimo, não um limiar
estático como as demais, e poluiria a leitura sem ganho.

**Tentativa revertida (2026-07-28):** um painel extra "Deslizamento de Fase
PLL" (Δθ vs. relógio nominal de 60 Hz, integrado do ângulo unwrapped) foi
implementado e depois **removido a pedido do usuário** — não era o que tinha
sido pedido. Não reintroduzir essa interpretação sem confirmação explícita;
se o usuário pedir "delta ângulo" de novo, esclarecer o que exatamente ele
quer antes de implementar.

## Envelope LVRT (`_lvrt_envelope`, só no |V| Bus 2)

Curva degrau V×t de **trip mandatório** (Table 8, IEEE Std 1547.2-2023)
Categoria II, ancorada em `t_fault` (constante de classe `_LVRT_STEPS`):

| Δt após a falta | V mínimo antes do trip |
|---|---|
| até 0.16 s | 0.45 pu (UV2) |
| até 10 s   | 0.70 pu (UV1) |
| depois     | 0.88 pu (operação contínua) |

Scatter com `line_shape="hv"`, tracejado vermelho, `hoverinfo="skip"`,
`legend = self._legend_key`, nome "IEEE 1547". Substitui a hline fixa de
`LVRT_THRESHOLD` apenas em `vbus2` com falta; `vbus1`/`vbus3` (e `vbus2` em
regime) mantêm a hline antiga.

### Correção 2026-07-26 — valores alinhados à Table 8 real

Os degraus originais (0,30/0,45/0,65 pu) foram escritos (commit `bc428d7`,
05/07/2026) com atribuição genérica ao IEEE 1547-2018 Cat II, sem citar
tabela/página, antes de qualquer PDF da norma ter sido processado pela
skill `pdf-kb-updater`. Corrigido para os 2 degraus reais de Table 8 (ver
[ieee1547_ride_through.md](../../standards/ieee1547_ride_through.md)):
UV2 = 0,45 pu/0,16 s e UV1 = 0,70 pu/10 s.

**Ressalva semântica que permanece:** Table 8 é a curva de **trip
mandatório** (proteção — abaixo disso o inversor *deve* desconectar), não a
curva de **ride-through contínuo** (Table 14/15/16 do 1547-2018 normativo
puro, que não está disponível no Application Guide extraído). Se a
Table 14/15/16 for obtida no futuro, essa curva pode ser substituída pela de
ride-through de verdade.

### Nome do trace (2026-07-27)

O nome passou por duas iterações — "LVRT 1547 Cat II" (original, sem fonte
verificada) → "V mín. trip 1547 Cat II" (após a correção de valores, mas com
mistura de idiomas e abreviação pouco clara) → **"IEEE 1547"** (simplificado
a pedido do usuário). A ressalva semântica trip-vs-ride-through acima
continua valendo mesmo com o nome curto; fica documentada aqui e em
[ieee1547_ride_through.md](../../standards/ieee1547_ride_through.md) para
quem for interpretar o gráfico.

### Correção 2026-07-27 — recorte não avança degrau que a janela não alcança

`_lvrt_envelope` sempre acrescentava um ponto final `(t_end, 0.88)`,
independente de o degrau UV1 (10 s após a falta) ter de fato ocorrido dentro
da janela simulada. Em cenários com falta em t≈0,3 s e janela de 0,6 s, isso
desenhava um salto falso para 0,88 pu bem na borda direita do gráfico —
sugerindo retomada de operação contínua em 0,6 s, quando a exigência real
(0,70 pu) continuaria valendo até 10,3 s. Achado pelo usuário ao comparar o
print do gráfico com a duração da simulação.

Corrigido: o laço só avança para o próximo degrau (inclusive o final de
0,88 pu) se `t0 + dt_step < t_end`; caso contrário, mantém o último patamar
válido constante até o fim da janela, sem saltos fora do horizonte simulado.

## Gotcha ⚠️ traces adicionados fora de `_add`

`_ts_marker` e `_lvrt_envelope` usam `self._fig.add_trace` direto: não entram
no `trace_map`, então o JS (`themedData`) **não** re-tema a cor deles — por
isso as cores escolhidas (verde/vermelho) precisam funcionar nos dois temas.
Definir `trace.legend = self._legend_key` manualmente, senão o item cai na
legenda do primeiro painel.
