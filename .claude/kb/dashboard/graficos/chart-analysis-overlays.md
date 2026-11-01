---
name: chart-analysis-overlays
aliases: [chart-analysis-overlays]
description: Overlays de análise nos gráficos — janela de falta sombreada, hierarquia θ̂ PLL vs θ Rede, marcador tₛ e curva de suportabilidade do ONS
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

- `add_hrect(±TOL_DEG)` verde translúcido (`rgba(22,163,74,0.08)`), com a
  faixa de **2°** do TCC desde 2026-10-20 (antes ±1,15°, `TOL_RAD`); bordas
  em linha pontilhada fina verde. O 1º ciclo após `t_fault` ganha uma faixa
  cinza: é o salto de fase da aplicação da falta, fora do pico. O sinal é
  `atan2(v_q, v_d)` da rede, com a linha quebrada nos saltos de ±180°. Ver
  [[indicadores-tcc-dashboard]].
- `_ts_marker()`: diamante verde em `(ts, erro(ts))` com texto `t_s`. Trace
  adicionado **direto** com `showlegend=False` e
  `marker.legend = self._legend_key` — não passa por `_add`, logo fica fora
  do `trace_map` e mantém cor fixa nos dois temas.

`metrics["ts"]` é o instante absoluto `t_clear + retorno` (2026-10-20); o
tooltip do diamante mostra o retorno em ms, o mesmo valor do card "Retorno à
faixa de 2°" e das Tabelas 5.1/5.3. Sem retorno na janela, não há marcador.

## Painel de frequência (removido 2026-07-30)

Existiu um painel "Frequência PLL (Hz)" (`kind == "freq"`), com
`SimData._estimate_freq()` em `loader.py` (`f̂ = dθ̂/dt / 2π`, diferença
central sobre `theta_pll_fast`) e faixa ONS §5.2.1 (`FREQ_CONTINUOUS`,
`FREQ_TRIP_MIN`, `FREQ_TRIP_MAX` em `config/settings.py`). Removido a
pedido do usuário — não fazia sentido para a análise do TCC. `_estimate_freq`,
os atributos `t_freq`/`f_pll`/`has_freq` e as 3 constantes foram deletados;
não reintroduzir sem pedido explícito.

**Tentativa revertida (2026-07-28):** um painel extra "Deslizamento de Fase
PLL" (Δθ vs. relógio nominal de 60 Hz, integrado do ângulo unwrapped) foi
implementado e depois **removido a pedido do usuário** — não era o que tinha
sido pedido. Não reintroduzir essa interpretação sem confirmação explícita;
se o usuário pedir "delta ângulo" de novo, esclarecer o que exatamente ele
quer antes de implementar.

## Curva de suportabilidade do ONS (`_lvrt_envelope`, só no |V| Bus 2)

Desde 2026-10-25 é a borda inferior da curva de suportabilidade a
subtensões do ONS (Submódulo 2.10, Figura 2.1 do TCC;
[[ons-voltage-ride-through]]), a mesma do capítulo Código de rede do
palco e do card "Suportabilidade ONS" ([[indicadores-tcc-dashboard]]).
Pontos `LVRT_T`/`LVRT_V` de `pipeline/indicadores.py` (0,2 pu até 0,5 s,
rampa até 0,85 pu em 1 s), ancorados em `t_fault`, interpolados
linearmente e recortados no fim da janela: com falta em 0,3 s e janela de
0,6 s, só o patamar de 0,2 pu aparece. Tracejado vermelho,
`hoverinfo="skip"`, nome "Suportabilidade ONS". `vbus1`/`vbus3` (e `vbus2`
em regime) mantêm a hline de `LVRT_THRESHOLD`.

O painel mostra |V| da Barra 2, e o veredito do card usa a fase mais
afundada no inversor: a curva é referência visual, a classificação vem
do card.

**Histórico.** De 2026-07-05 a 2026-10-24 o envelope era o degrau de trip
mandatório da Table 8 do IEEE Std 1547.2-2023, Categoria II (UV2 0,45 pu
por 0,16 s, UV1 0,70 pu por 10 s; [[ieee1547-ride-through]]), nome "IEEE
1547". Saiu porque o TCC e o deck avaliam pela curva do ONS, e a banca
veria duas normas diferentes no mesmo painel. A lição do recorte
(2026-07-27: não desenhar degrau que a janela não alcança) continua
valendo.

## Gotcha ⚠️ traces adicionados fora de `_add`

`_ts_marker` e `_lvrt_envelope` usam `self._fig.add_trace` direto: não entram
no `trace_map`, então o JS (`themedData`) **não** re-tema a cor deles — por
isso as cores escolhidas (verde/vermelho) precisam funcionar nos dois temas.
Definir `trace.legend = self._legend_key` manualmente, senão o item cai na
legenda do primeiro painel.
