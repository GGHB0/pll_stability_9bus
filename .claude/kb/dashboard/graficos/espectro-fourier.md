---
name: espectro-fourier
description: Painel de espectro de Fourier segmentado (pré-falta/durante a falta/pós-falta) — SpectrumBuilder, FFT com Hann no referencial abc (fase A), amplitude linear, marcadores harmônicos + f_res LCL
metadata:
  type: project
---

# Espectro de Fourier segmentado (spectrum.py)

Adicionado em 2026-07-12 a pedido do orientador ("espectro de Fourier para ver
as frequências"). Seção "Espectro de amplitude (FFT) — fase A, abc" no HTML,
abaixo de Sistema 9-Bus. Reformulado em 2026-07-13/14 para o formato do
gráfico de referência do AGP (coorientador): amplitude **linear** (não dB),
só sinais **abc fase A** (não dq), e **3 segmentos temporais** em vez de 2.

## Por que abc fase A (não dq)

A versão original usava θ_err/i_q/Q no referencial dq (fundamental → DC,
seq. negativa → 120 Hz). O AGP pediu o formato clássico do artigo dele:
espectro direto da fase A em abc. Trade-off aceito e comunicado ao usuário:
o range de 1,5 MHz / amplitude ~1e-14 do gráfico de referência do AGP não é
reproduzível com os dados do projeto (Nyquist ~10 kHz da simulação, correntes
reais em pu — não ruído numérico). O espectro atual cobre até `SPEC_FMAX_HZ`
(2 kHz) com harmônicas reais do inversor.

No abc a fundamental fica em 60 Hz (não em DC); a seq. negativa da falta
assimétrica cai **também** em 60 Hz (não aparece como pico separado — essa é
a razão de a versão dq antiga isolar melhor a assinatura de 120 Hz; ver KB
antiga no histórico do git se precisar recuperar esse ângulo de análise).

## Implementação — `src/pipeline/spectrum.py`

`SpectrumBuilder(SimData).build() → (fig | None, trace_map)`, chamado no
`app.py` ao lado do `ChartBuilder`; `trace_map` no mesmo formato
`(idx, light, dark)` consumido pelo re-tema do renderer.

**Sinais (`_signals()`, um painel por sinal, rows=n, cols=1) — só fase A:**
1. Corrente i_a UFV (abc) — `t_abc`/`ia_ufv`, só quando `has_iabc_ufv`.
2. Tensão v_a UFV (abc) — `t_abc`/`va_ufv`, só quando `has_vabc_ufv`.

Ambos exigem `sim_data_abc.csv` (re-export do modelo). Cenários sem esse CSV
não mostram o painel de espectro (fig retorna `None`).

**Segmentos (`_segments()`, um traço por segmento, cores em `SPEC_SEG_COLORS`):**

| Segmento | Janela | Cor light/dark |
|---|---|---|
| Pré-falta | `[T_SETTLE, t_fault)` — corta a partida do PLL | cinza `#64748b`/`#94a3b8` |
| Durante a falta | `[t_fault, t_clear)` | vermelho `#dc2626`/`#f87171` |
| Pós-falta | `[t_clear, fim]` — só se `t_clear` existir | azul `#2563eb`/`#60a5fa` |
| Regime (cenário sem falta) | `[T_SETTLE, fim]` — traço único | azul |

`t_fault`/`t_clear` vêm do `fault_info.json` real do cenário (via `SimData`),
não de constantes fixas. Falta permanente (sem `t_clear`) colapsa em 2
segmentos: pré-falta e durante a falta (vai até o fim).

**`T_SETTLE = 0.1 s`** (settings.py): o PLL leva ~0.08 s para travar na
partida da simulação — é inicialização, não falta de desempenho (medido:
|V| Bus 2 acomoda em 0.078 s, o sinal mais lento). A mesma constante clampa
as janelas de métricas do loader ([[pipeline-dados]]).

**FFT (`_amplitude_spectrum`):** reamostra em grade uniforme (`dt` mediano +
`np.interp` — não assume passo fixo do CSV), remove só a média (offset DC;
a fundamental de 60 Hz permanece), janela de Hann, amplitude **linear**
`2·|rfft|/Σw` em pu — escala linear destaca os picos discretos sobre o piso
de ruído (ao contrário de dB, que achata a diferença). Guardas: segmento
< 0,05 s ou < 64 amostras é pulado (df > 20 Hz não resolve os harmônicos).

**Marcadores (`SPEC_MARKERS`, settings.py):** fundamental e harmônicas
ímpares do inversor + ressonância do filtro LCL — `F_FUND_HZ=60`, `3×60=180`,
`5×60=300`, `7×60=420`, `F_RES_LCL_HZ=1443.4`. `SPEC_FMAX_HZ=2000` (corte do
espectro), `SPEC_XRANGE_HZ=1500` (range default do eixo x; duplo-clique
expande até 2 kHz).

## Layout e integração

- Eixo y **amplitude linear (pu)**, `rangemode="tozero"`.
- Vlines tracejadas cinza em cada frequência de `SPEC_MARKERS`, com rótulo
  (f₁, 3f₁, 5f₁, 7f₁, f_res LCL) só na 1ª linha.
- Legenda única horizontal no topo (`legendgroup` por segmento,
  `showlegend` só na row 1).
- Renderer: chaves `specData/specLight/specDark/specIdx/hasSpec` no
  `SCENARIOS`, div `#plot-spec` no painel de aba `#sec-spec` — renderizado
  sob demanda ao abrir a aba ([[tabs-navegacao]]).
- Zoom na falta (eixo em segundos) **não** afeta o espectro — `_applyZoom`
  só toca `TIME_TABS` (res/inv/sys).

## Gotcha de verificação no browser

`SCENARIOS[k].specData.data[i].x`/`.y` vêm como binário base64 (`bdata`) do
`plotly.to_json` — para inspecionar valores no console usar `gd._fullData`
do gráfico renderizado (arrays decodificados), não o JSON cru.

## Nota sobre taxas de amostragem

Nos CSVs `sim_data_abc.csv` a taxa de amostragem do `iabc`/`vabc` pode
diferir da do `sim_data.csv` principal — a reamostragem por `dt` mediano em
`_amplitude_spectrum` torna o espectro imune a isso. Ver [[export-workflow]]
para o alinhamento do export abc ao lado do inversor (2026-07-13).
