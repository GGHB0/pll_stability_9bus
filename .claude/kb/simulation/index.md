---
name: kb-index-simulation
description: Índice da pasta simulation/ do KB (gerado por scripts/kb_links.py)
aliases: [kb-index-simulation]
---

# KB — simulation/

Gerado por `scripts/kb_links.py index`; texto fora dos marcadores é preservado.

<!-- kb-links:begin -->
## Documentos

| Arquivo | Link | Cobre |
|---|---|---|
| [cenarios_simulados.md](cenarios_simulados.md) | [[cenarios-simulados]] | Inventário dos cenários exportados em output/results — 22 nominais + 8 com sintonia inadequada, as duas configurações temporais de falta e… |
| [export_workflow.md](export_workflow.md) | [[export-workflow]] | Workflow validado Simulink → MATLAB → Python para o modelo pll_stability_9bus (logsout, sinais de barra, sim_data.csv) |
| [params_workflow.md](params_workflow.md) | [[params-workflow]] | Workflow notebook -> MATLAB/Simulink for separating theoretical AGP calculations from runtime params.m values, including the intentional Vc… |
| [python_pipeline.md](python_pipeline.md) | [[python-pipeline]] | Arquitetura Python (src/) que consome sim_data.csv — SimData, ChartBuilder, painéis, métricas |
| [resimulacao-abc.md](resimulacao-abc.md) | [[resimulacao-abc]] | Runbook de re-simulação (Bruno) — regenerar os 18 cenários para exportar sim_data_abc.csv (correntes e tensões trifásicas, painéis abc do e… |
| [reuniao_2026_05_inercia_pll.md](reuniao_2026_05_inercia_pll.md) | [[reuniao-2026-05-inercia-pll]] | Texto de apoio para reuniao sobre novos testes de inercia, reatancia de curto, colapso do PLL e tentativas de filtragem notch |

## Pastas relacionadas

- [dashboard/](../dashboard/index.md) — saem 6, chegam 3
- [inverter/](../inverter/index.md) — saem 0, chegam 2
- [pll/](../pll/index.md) — saem 3, chegam 2
- [power-system/](../power-system/index.md) — saem 1, chegam 0
- [psim/](../psim/index.md) — saem 0, chegam 4
- [standards/](../standards/index.md) — saem 1, chegam 2
- [tcc-word/](../tcc-word/index.md) — saem 4, chegam 4

Voltar: [índice do KB](../index.md) · [grafo](../grafo.md)
<!-- kb-links:end -->
