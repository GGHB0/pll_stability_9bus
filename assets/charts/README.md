# Charts — Gráficos de Dados Reais

Diferente de `assets/diagrams/` (esquemáticos e curvas desenhados à mão em SVG
puro), esta pasta guarda **gráficos gerados a partir dos dados reais de
simulação** (`output/results/*/sim_data*.csv`), sem o layout interativo do
Plotly usado no dashboard — destinados a figuras estáticas do TCC.

Gerados com **matplotlib** (`svg.fonttype: none`, texto permanece editável no
SVG), usando a paleta de cores do projeto (`src/config/settings.py`,
`LIGHT_COLORS`) e as mesmas convenções do dashboard (ex.: `T_SETTLE`).

Todos os gráficos abaixo vêm do cenário `regime` (regime permanente, sem
falta, PLL nominal) e são gerados por `scripts/gen_regime_waveforms.py`.

| Arquivo | Conteúdo | Janela |
|---|---|---|
| `regime_correntes_abc.svg` / `.png` | Correntes trifásicas do inversor (`i_a, i_b, i_c`) | 0,55–0,60 s (3 ciclos) |
| `regime_tensoes_abc.svg` / `.png` | Tensões trifásicas do inversor (`v_a, v_b, v_c`) | 0,55–0,60 s (3 ciclos) |
| `regime_potencia_pq.svg` / `.png` | Potência ativa e reativa do inversor (`P, Q`) | 0–0,6 s completo |
| `regime_corrente_dq.svg` / `.png` | Corrente no referencial dq, medida (sólido) + referência (tracejado) — `i_d, i_q` | 0–0,6 s completo |
| `regime_tensao_dq.svg` / `.png` | Tensão no referencial dq, Rede (sólido) + Inversor (pontilhado) — `v_d, v_q` | 0–0,6 s completo |

Todos com marcador do transitório de partida (`T_settle = 0,1 s`, excluído de
todo cálculo do dashboard) exceto os dois em janela zoomada, que já começam
bem depois dele. Convenções de série (medido vs. ref, Rede vs. Inversor)
seguem `src/pipeline/chart.py` (`kind="dq_combined"`/`"vdq_combined"`).

Fonte de dados: `output/results/regime/sim_data.csv` (P, Q, dq) e
`output/results/regime/sim_data_abc.csv` (abc).

## Gerar / regenerar

```powershell
.venv\Scripts\pip install matplotlib   # não está no requirements.txt do pipeline principal
.venv\Scripts\python.exe scripts\gen_regime_waveforms.py
```

Reproduzível sempre que os dados de simulação forem atualizados (regera os
5 arquivos de uma vez).
