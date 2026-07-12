---
name: espectro-fourier
description: Painel de espectro de Fourier segmentado (pré-falta/falta/pós-falta) — SpectrumBuilder, FFT com Hann no referencial dq, marcadores 120 Hz e f_res LCL
---

# Espectro de Fourier segmentado (spectrum.py)

Adicionado em 2026-07-12 a pedido do orientador ("espectro de Fourier para ver
as frequências"). Nova seção "Espectro de Fourier — referencial dq" no HTML,
abaixo de Sistema 9-Bus.

## Por que o referencial dq

A transformada de Park desloca o espectro em −60 Hz. Consequências:

| Fenômeno em abc | Aparece no dq em |
|---|---|
| Fundamental seq. positiva | DC (removida junto com a média) |
| Sequência negativa (falta assimétrica) | **120 Hz** — assinatura central do TCC |
| 5º harm. (seq−) e 7º harm. (seq+) | 360 Hz |
| Ressonância LCL (ω_res = 9068,99 rad/s) | ~1443 Hz |

Sequência zero não aparece (não existe no dq). O pico de 120 Hz durante a
falta é a evidência direta da oscilação de 2ª harmônica no PLL sob sequência
negativa — validado: falta 1φ na barra 6 dá 2,73e-2 rad @ 120 Hz no θ_err
durante a falta, vs 2,20e-3 na 3φ equivalente (12×).

## Implementação — `src/pipeline/spectrum.py`

`SpectrumBuilder(SimData).build() → (fig | None, trace_map)`, chamado no
`app.py` ao lado do `ChartBuilder`; `trace_map` no mesmo formato
`(idx, light, dark)` consumido pelo re-tema do renderer.

**Sinais (um painel por sinal, rows=n, cols=1):**
1. θ_err — eixo rápido (`t_fast`) quando disponível
2. i_q UFV medida
3. Q UFV
4. i_a UFV em abc (`t_abc`/`ia_ufv`) — só quando `sim_data_abc.csv` existe
   (requer re-export). Em abc a fundamental fica em 60 Hz (~0 dB) e a
   **sequência negativa cai também em 60 Hz** — invisível como pico separado
   (medido: +0.1 dB na falta 1φ); o ripple dq de 120 Hz vira banda lateral
   em 180 Hz. O painel abc complementa os dq (formato familiar, harmônicas
   em 300/420 Hz), mas a assinatura do TCC vive nos painéis dq.

**Segmentos (um traço por segmento, cores fixas em `SPEC_SEG_COLORS`):**

| Segmento | Janela | Cor light/dark |
|---|---|---|
| Pré-falta | `[T_SETTLE, t_fault)` — corta a partida do PLL | cinza `#64748b`/`#94a3b8` |
| Falta | `[t_fault, t_clear)` | vermelho `#dc2626`/`#f87171` |
| Pós-falta | `[t_clear, fim]` | azul `#2563eb`/`#60a5fa` |
| Regime (cenário sem falta) | `[T_SETTLE, fim]` — traço único | azul |

**`T_SETTLE = 0.1 s`** (settings.py, 2026-07-12): o PLL leva ~0.08 s para
travar na partida da simulação — é inicialização, não falta de desempenho
(medido: |V| Bus 2 acomoda em 0.078 s, o sinal mais lento). Antes a
pré-falta começava em `T_FAULT = 0.2` por acidente da constante de fallback;
com T_SETTLE a janela [0.1, 0.3] dobra de tamanho → resolução 10 Hz → 5 Hz.
A mesma constante clampa as janelas de métricas do loader
([[pipeline-dados]]).

**FFT (`_amplitude_spectrum`):** reamostra em grade uniforme (`dt` mediano +
`np.interp` — não assume passo fixo do CSV), remove a média (fundamental → DC),
janela de Hann, amplitude `2·|rfft|/Σw` convertida para **dB re 1 pu/rad**
(`20·log10`, piso `_AMP_FLOOR = 1e-5` → −100 dB), formato acadêmico pedido
pelo orientador (Amplitude dB × Hz). Guardas: segmento < 0,05 s ou < 64
amostras é pulado (df > 20 Hz não resolve 120 Hz).

**Constantes em `settings.py`:** `SPEC_FMAX_HZ = 2000` (corte do espectro),
`SPEC_XRANGE_HZ = 1500` (range default do eixo x — cobre harmônicas e f_res
LCL; duplo-clique expande até 2 kHz), `F_2H_HZ = 120`, `F_RES_LCL_HZ = 1443.4`.

## Layout e integração

- Eixo y **linear em dB** (título "Amplitude (dB)"); em dB o salto do pico
  de 120 Hz na falta assimétrica fica em ~+22 dB vs pré-falta.
- Vlines tracejadas em 120 Hz (vermelha, "2f = 120 Hz") e 1443 Hz (violeta,
  "f_res LCL") em todos os painéis; anotação só na 1ª linha. f_res fica fora
  do range default — aparece no duplo-clique (autorange).
- Legenda única horizontal no topo (`legendgroup` por segmento,
  `showlegend` só na row 1) — diferente das legendas por eixo do ChartBuilder.
- Renderer: chaves `specData/specLight/specDark/specIdx/hasSpec` no
  `SCENARIOS`, div `#plot-spec` na seção `#sec-spec`, re-render em
  `switchScenario` e `toggleTheme`.
- **Ghost/fantasma funciona no espectro**: `_ghostData("spec")` sobrepõe o
  cenário PLL equivalente pontilhado — comparação direta do pico de 120 Hz
  nominal × mal dimensionado.
- Zoom na falta (eixo em segundos) **não** afeta o espectro — `_applyZoom`
  só toca `gdInv`/`gdSys`.
- Custo: ~95 KB de JSON por cenário (~1,7 MB no HTML total).

## Gotcha de verificação no browser

`SCENARIOS[k].specData.data[i].x` vem como binário base64 (`bdata`) do
`plotly.to_json` — para inspecionar valores usar `gd._fullData` do gráfico
renderizado, não o JSON cru.

## Nota sobre taxas de amostragem (2026-07-12)

Nos CSVs atuais as taxas estão **invertidas** em relação ao CLAUDE.md:
`sim_data.csv` está a 5 µs (200 kHz) e `sim_data_angles.csv` a 200 µs
(5 kHz). A reamostragem por `dt` mediano torna o espectro imune a isso,
mas vale conferir a origem no logging do modelo. Ver [[pipeline-dados]].
