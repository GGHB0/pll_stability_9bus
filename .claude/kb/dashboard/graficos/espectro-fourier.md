---
name: espectro-fourier
description: Aba de espectro FFT segmentado (pré/durante/pós-falta) — SpectrumBuilder multi-modo (fases a/b/c + eixos d/q), seletor de fase no HTML, truncamento a ciclos inteiros, componente DC; a tabela de harmônicas fica em espectro-tabela-harmonicas.md
metadata:
  type: project
---

# Espectro de Fourier segmentado (spectrum.py)

Adicionado em 2026-07-12 a pedido do orientador ("espectro de Fourier para ver
as frequências"). Reformulado em 2026-07-13/14 para o formato do gráfico de
referência do AGP (coorientador): amplitude **linear** (não dB) e **3
segmentos temporais**. Estendido em 2026-07-15: além da fase A, espectros das
fases **b/c** e dos eixos **d/q**, com seletor de fase no HTML e tabela de
amplitude das harmônicas 1–12. Estendido em 2026-08-05: linha de 0 Hz (DC)
na tabela dq (valor antes descartado como offset).

## abc × dq

- **abc**: fundamental fica em 60 Hz; a seq. negativa da falta assimétrica
  cai **também** em 60 Hz (não aparece como pico separado).
- **dq**: fundamental vira DC (`_amplitude_spectrum` remove a média antes da
  FFT, mas guarda o valor — ver seção "Componente DC" abaixo); a seq.
  negativa aparece isolada em **120 Hz** (2f₁) — assinatura da falta
  assimétrica. Harmônicas 5ª/7ª do abc caem juntas em 6f₁; 11ª/13ª em 12f₁.

O range de 1,5 MHz / amplitude ~1e-14 do gráfico de referência do AGP não é
reproduzível com os dados do projeto (Nyquist ~10 kHz da simulação). O
espectro cobre até `SPEC_FMAX_HZ` (2 kHz) com harmônicas reais do inversor.

## Implementação — `src/pipeline/spectrum.py`

`SpectrumBuilder(SimData).build() → (figs, tms, harm)`:

- `figs`/`tms`: **dicts por modo** `{"a","b","c","d","q"}` — cada modo é uma
  figura própria (painel de corrente + painel de tensão UFV) com trace_map
  `(idx, light, dark)` no formato do re-tema do renderer.
- `harm`: dados da tabela de harmônicas —
  `{"segs": [...], "i"|"v": {segmento: {modo: [dc, amp h1…h12]}}}` — índice
  0 é o componente DC (ver "Componente DC" abaixo), índice k é a k-ésima
  harmônica.

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
ciclos exatos, mas a garantia agora está no código). Depois: remove a média
(guardada em `dc`, ver abaixo), janela de Hann, amplitude linear
`2·|rfft|/Σw` em pu. Guardas: segmento < 0,05 s ou < 64 amostras é pulado.
Retorna `(f, amp, dc)`.

**Harmônicas (`_harmonics`):** amplitude em k·60 Hz (k=1…12) = pico local em
±1,5 bin do alvo (Hann espalha um tom bin-centrado em 3 bins, pico verdadeiro
no bin central), mais o componente DC no índice 0. **Componente DC
(2026-08-05)**: antes descartado (`_amplitude_spectrum` removia a média para
não vazar energia no bin de 60 Hz, sem guardar o valor); agora `dc` é
retornado e vira `|dc|` no índice 0. Em **abc** é só o offset de medição
(perto de zero, não exibido); em **dq**, pela derivação de fasor espacial do
Yazdani (`kb/standards/harmonic_dq_frame_mapping.md` §4.3), é a própria
**fundamental representada em DC** — id/iq no ponto de operação — por isso
entra na tabela dq (linha "0 Hz / fund. (DC)") como referência de escala
para o pico de 120 Hz.

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
  modo não existir no cenário novo, cai para o primeiro disponível. Esse
  seletor só controla **qual gráfico** aparece acima; a tabela de
  harmônicas abaixo é independente dele (mostra todos os modos sempre).
- `_renderChart("spec")` resolve a figura via `_specFig(sc)`; filename do
  PNG ganha sufixo do modo (`pll_<cenário>_spec_<modo>`).
- **Tabela de harmônicas abaixo dos gráficos** (4 tabelas: abc/dq × corrente/
  tensão), destaque normativo por célula e legenda: fragmentada em
  [espectro-tabela-harmonicas.md](espectro-tabela-harmonicas.md).

## Layout e integração

- Eixo y amplitude linear (pu), título `"Amplitude (pu)"` na **vertical**
  (encostado no eixo); `SPEC_XRANGE_HZ=1500` default, duplo-clique expande
  até 2 kHz.
- **Teto do eixo Y fixo em 1 pu por painel** (2026-08-02, a pedido do
  usuário): antes o eixo usava `rangemode="tozero"` (autorange do Plotly),
  que ajustava o topo ao maior valor da própria série — um pico de 0,012 pu
  virava "o topo do gráfico", fazendo o ruído de fundo parecer proeminente.
  Agora `_apply_layout` recebe `row_maxes` (pico real por subplot, calculado
  em `_mode_fig` a partir de `amp.max()` de cada segmento) e fixa
  `range=[0, max(1.0, row_max·1.05)]` — teto em 1 pu (escala plena) por
  padrão, só sobe se o pico real ultrapassar 1 pu. Corrente e tensão (linhas
  separadas da mesma figura) têm tetos **independentes**, não compartilhados
  — cada subplot já tinha seu próprio eixo Y antes disso, mudou só a forma
  como o teto é calculado. `_Y_CEIL_MARGIN=1.05` é a folga acima do pico
  antes do piso de 1 pu entrar. Escopo é só `spectrum.py` — os outros
  gráficos do dashboard (séries temporais em `chart.py`) continuam com
  autorange normal.
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
- Nota de 2026-07-15 ("só `bus1/2phase` tem `sim_data_abc.csv`") está
  **desatualizada**: confirmado em 2026-08-05 que os 26 cenários têm
  `sim_data_abc.csv` (`specModes`="abcdq" em todos). Runbook de
  re-exportação para cenário novo sem esse CSV: [[resimulacao-abc]].
