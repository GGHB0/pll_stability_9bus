---
name: espectro-fourier
description: Aba de espectro FFT segmentado (pré/durante/pós-falta) — SpectrumBuilder multi-modo (fases a/b/c + eixos d/q), seletor de fase no HTML, truncamento a ciclos inteiros, tabela de harmônicas 1–7
metadata:
  type: project
---

# Espectro de Fourier segmentado (spectrum.py)

Adicionado em 2026-07-12 a pedido do orientador ("espectro de Fourier para ver
as frequências"). Reformulado em 2026-07-13/14 para o formato do gráfico de
referência do AGP (coorientador): amplitude **linear** (não dB) e **3
segmentos temporais**. Estendido em 2026-07-15: além da fase A, espectros das
fases **b/c** e dos eixos **d/q**, com seletor de fase no HTML e tabela de
amplitude das harmônicas 1–7.

## abc × dq

- **abc**: fundamental fica em 60 Hz; a seq. negativa da falta assimétrica
  cai **também** em 60 Hz (não aparece como pico separado).
- **dq**: fundamental vira DC (removida junto com a média); a seq. negativa
  aparece isolada em **120 Hz** (2f₁) — assinatura da falta assimétrica.
  Harmônicas 5ª/7ª do abc caem juntas em 6f₁; 11ª/13ª em 12f₁.

O range de 1,5 MHz / amplitude ~1e-14 do gráfico de referência do AGP não é
reproduzível com os dados do projeto (Nyquist ~10 kHz da simulação). O
espectro cobre até `SPEC_FMAX_HZ` (2 kHz) com harmônicas reais do inversor.

## Implementação — `src/pipeline/spectrum.py`

`SpectrumBuilder(SimData).build() → (figs, tms, harm)`:

- `figs`/`tms`: **dicts por modo** `{"a","b","c","d","q"}` — cada modo é uma
  figura própria (painel de corrente + painel de tensão UFV) com trace_map
  `(idx, light, dark)` no formato do re-tema do renderer.
- `harm`: dados da tabela de harmônicas —
  `{"segs": [...], "i"|"v": {segmento: {modo: [amp h1…h7]}}}`.

**Modos (`_modes()`):** fases a/b/c usam `t_abc`/`i{f}_ufv`/`v{f}_ufv`
(precisam de `sim_data_abc.csv` — cenários sem esse CSV só mostram d/q);
eixos d/q usam `t`/`id_ufv_meas`/`iq_ufv_meas`/`vd_ufv`/`vq_ufv` (Tsc=200 µs
→ Nyquist 2,5 kHz, cobre o fmax de 2 kHz).

**Segmentos (`_segments()`, cores em `SPEC_SEG_COLORS`):**

| Segmento | Janela | Cor light/dark |
|---|---|---|
| Pré-falta | `[T_SETTLE, t_fault)` — corta a partida do PLL | cinza `#64748b`/`#94a3b8` |
| Durante a falta | `[t_fault, t_clear)` | vermelho `#dc2626`/`#f87171` |
| Pós-falta | `[t_clear, fim]` — só se `t_clear` existir | azul `#2563eb`/`#60a5fa` |
| Regime (sem falta) | `[T_SETTLE, fim]` — traço único | azul |

`t_fault`/`t_clear` vêm do `fault_info.json` real do cenário (via `SimData`).

**FFT (`_amplitude_spectrum`):** reamostra em grade uniforme (`dt` mediano +
`np.interp`), **trunca a janela para um nº INTEIRO de ciclos de 60 Hz**
(`floor(T·60)/60`) — garante que a fundamental caia exata num bin da FFT,
sem vazamento por janela cortada no meio do ciclo, independentemente dos
tempos do cenário (com t=0.1/0.3/0.4/0.6 s os segmentos já eram 12/6/12
ciclos exatos, mas a garantia agora está no código). Depois: remove a média,
janela de Hann, amplitude linear `2·|rfft|/Σw` em pu. Guardas: segmento
< 0,05 s ou < 64 amostras é pulado.

**Harmônicas (`_harmonics`):** amplitude em k·60 Hz (k=1…7) = pico local em
±1,5 bin do alvo (Hann espalha um tom bin-centrado em 3 bins, pico verdadeiro
no bin central). Alimenta a tabela do relatório.

**Marcadores:** abc usa `SPEC_MARKERS` (f₁, 3f₁, 5f₁, 7f₁, f_res LCL);
dq usa `SPEC_MARKERS_DQ` (2f₁=120, 6f₁=360, 12f₁=720, f_res LCL) —
ambos em settings.py.

## Seletor de fase + tabela no HTML (renderer.py)

- `SCENARIOS[k].specData/specLight/specDark/specIdx` são **objetos por modo**;
  `specModes` lista os modos disponíveis no cenário; `hasSpec = bool(figs)`.
- Barra `.spec-phase-bar` (abaixo do header da seção): botões a/b/c/d/q
  (`.spec-ph-btn`, estilo `pll-toggle`). `setSpecPhase(p)` marca `_dirty.spec`
  e re-renderiza; `_syncSpecPhaseUI()` esconde botões sem dados no cenário e
  atualiza o título (`#spec-mode-lbl`: "fase a (abc)" / "eixo d (dq)") e o
  hint (`#spec-phase-hint`). `specPhase` é **sticky** entre cenários — se o
  modo não existir no cenário novo, cai para o primeiro disponível.
- `_renderChart("spec")` resolve a figura via `_specFig(sc)`; filename do
  PNG ganha sufixo do modo (`pll_<cenário>_spec_<modo>`). `_ghostData`
  compara o mesmo modo do cenário PLL equivalente.
- **Tabela de harmônicas** (`_spec_table_html`, por cenário, injetada em
  `#spec-harm-area` no `switchScenario`): duas tabelas (Corrente UFV /
  Tensão UFV), linhas h=1ª…7ª (60–420 Hz), colunas agrupadas por segmento ×
  fase/eixo (a b c d q). Célula sem dado = "—" (ex.: a/b/c em cenário sem
  `sim_data_abc.csv`). Valores `%.3g` pu. CSS: `.harm-table`, separador
  vertical `.harm-first` entre segmentos.
- **Limiares absolutos em pu** (`_HARM_HI_PU=0.4`, `_HARM_LO_PU=0.02`, attrs
  de classe do renderer; aplicados em `_spec_table_html`): amp ≥ 0,4 pu →
  `.harm-top` (negrito + accent + fundo `color-mix` 12%, acompanha o tema);
  amp < 0,02 pu → `.harm-lo` (muted, opacity .5); meio-termo normal. Pedido
  do usuário (2026-07-15): destaque só para amplitude na ordem da nominal —
  na prática só as fundamentais abc destacam (0,49–1,01 pu); os valores dq
  (0,03–0,2 pu) ficam normais/apagados, sem negrito em valor pequeno.

## Layout e integração

- Eixo y amplitude linear (pu), `rangemode="tozero"`, título `"Amplitude (pu)"`
  na **vertical** (encostado no eixo); `SPEC_XRANGE_HZ=1500` default,
  duplo-clique expande até 2 kHz.
- **Barra de título no topo** (`_label`, 2026-07-21, Ponto 2 do professor):
  retângulo preenchido `#185FA5` com o nome do sinal ("Corrente iₐ UFV (abc)")
  em branco/negrito, posicionado **acima** das marcações de frequência
  (`y0 = y_top + 16/(240·n)`, altura 22 px). Antes era annotation horizontal no
  canto com "— amplitude (pu)" no texto (redundante com o eixo Y).
  `vertical_spacing` subiu p/ 0.13, margem `l=64`/`t=64`, legenda subiu p/
  `y=1.22` para não colidir com a barra. Ver [[construcao-graficos]].
- Legenda única horizontal no topo (`legendgroup` por segmento).
- Renderizado sob demanda ao abrir a aba ([[tabs-navegacao]]); zoom na falta
  não afeta o espectro (`_applyZoom` só toca res/inv/sys).

## Gotchas

- `specData[modo].data[i].x/.y` vêm como binário base64 (`bdata`) do
  `plotly.to_json` — inspecionar via `gd.spec._fullData` no console.
- A taxa de amostragem do `sim_data_abc.csv` pode diferir do CSV principal —
  a reamostragem por `dt` mediano torna o espectro imune a isso
  ([[export-workflow]]).
- Hoje (2026-07-15) só `bus1/2phase` tem `sim_data_abc.csv`; `regime` e
  `bus7/2phase` mostram apenas d/q até o Bruno re-exportar
  ([[resimulacao-abc|kb/simulation/resimulacao-abc]]).
