# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Este arquivo guarda só o que é estável e vale para toda sessão. Detalhe que
> muda (sinais, cenários, ganhos, arquivos de cada pasta) mora no KB e é
> referenciado por link: nunca copiar listas de arquivos para cá.

## Projeto

TCC (Trabalho de Conclusão de Curso) em Engenharia Elétrica — UERJ 2025. Investiga o
comportamento dinâmico do **SRF-PLL** (Synchronous Reference Frame Phase-Locked Loop)
em inversores conectados à rede sob contingências severas, motivado pela perturbação de
15/08/2023 no SIN (23 368 MW desligados, ~34,5% da carga).

- Rede IEEE 9 barras, base 20 kV / 100 MVA / 60 Hz; o G2 foi substituído pelo inversor
  UFV na Barra 2.
- Escopo, capítulos e status: [project-scope.md](.claude/kb/project-scope.md).

## Onde está cada coisa

| Caminho | Conteúdo |
|---|---|
| [pll_stability_9bus.slx](pll_stability_9bus.slx) + [params.m](params.m) | Modelo Simulink principal e parâmetros de runtime |
| [simulink/](simulink/) | Modelos auxiliares standalone (não referenciados pelo principal) |
| [PSim/](PSim/) | Fase inicial de modelagem no PSIM (legado) — [kb/psim/](.claude/kb/psim/index.md) |
| [notebooks/](notebooks/) | Cálculo analítico dos parâmetros (rodar células de cima para baixo) |
| [src/](src/) + [app.py](app.py) | Pacote Python do dashboard: `SimData → ChartBuilder/SpectrumBuilder → HTMLRenderer` |
| [scripts/](scripts/) | Export MATLAB, geradores de figuras e notas, [kb_links.py](scripts/kb_links.py) |
| `output/` | Gerado em runtime, não versionado (`results/`, `pll_metrics.html`) |
| [assets/](assets/) | Diagramas, gráficos, banner |
| [CHANGELOG.md](CHANGELOG.md), [docs/changelog/](docs/changelog/) | Histórico de mudanças do dashboard |
| [.claude/](.claude/INDEX.md) | Base de conhecimento, skills, agentes, regras |

## Fluxo de trabalho

```text
1. MATLAB: >> params   → simular pll_stability_9bus.slx
   (o StopFcn exporta sozinho para output/results/<barra ou linha>/<falta>/)
2. Python: .venv\Scripts\python.exe app.py   → output/pll_metrics.html
```

Setup (uma vez por clone): `python -m venv .venv`,
`.venv\Scripts\pip install -r requirements.txt` e
`git config core.hooksPath .githooks` (ativa o pre-commit que audita o KB).

- Export, sinais do `logsout` e taxas de amostragem: [export_workflow.md](.claude/kb/simulation/export_workflow.md)
- Cenários simulados (nominais e sintonia inadequada): [cenarios_simulados.md](.claude/kb/simulation/cenarios_simulados.md)
- Re-simulação: [resimulacao-abc.md](.claude/kb/simulation/resimulacao-abc.md)
- Pipeline do dashboard e métricas: [kb/dashboard/](.claude/kb/dashboard/index.md)

## Base de conhecimento

Ponto de entrada: **[.claude/kb/index.md](.claude/kb/index.md)**, que aponta para o
índice de cada pasta. Relações entre temas: [grafo.md](.claude/kb/grafo.md). Os
índices são gerados por `scripts/kb_links.py`, então doc novo aparece sozinho.
Convenção de links `[[slug]]`: [rules/kb-links.md](.claude/rules/kb-links.md).

## Armadilhas que valem para toda sessão

- **Ganhos de corrente ≠ ganhos do PLL.** `Kp = 8·fg·Lest` (TeseAGP) é do controlador
  de corrente ([pll_gains_methodology.md](.claude/kb/pll/sintonia/pll_gains_methodology.md)).
  O PI do PLL tem projeto próprio ([pll_loop_filter_gains.md](.claude/kb/pll/sintonia/pll_loop_filter_gains.md)).
- **Ganhos de corrente divididos por 4 duas vezes** (notebook + blocos Gain), de
  propósito: [simulink_model.md](.claude/kb/inverter/simulink_model.md).
- **Vcc diverge de propósito:** `params.m` usa ×1,5 do valor do notebook:
  [params_workflow.md](.claude/kb/simulation/params_workflow.md).
- **Sinais em duas taxas** (rápida e lenta), interpolar sobre o eixo lento; **não
  existe abc do lado da rede**: [export_workflow.md](.claude/kb/simulation/export_workflow.md).
- **Cenário de sintonia inadequada (BAD_PLL):** `kp_pll` e `ki_pll` ×0,2; desde a rodada
  de 01/10/2026 a janela de falta é a mesma do nominal: [cenarios_simulados.md](.claude/kb/simulation/cenarios_simulados.md).
- **`.slx` é um ZIP de XML:** inspecionar sem MATLAB pela skill `slx-explorer`; mapa
  de subsistemas e SIDs em [simulink_model.md](.claude/kb/inverter/simulink_model.md).

## Regras

- [limits.md](.claude/rules/limits.md): máx. 200 linhas por `.md`, estrutura de pastas do KB
- [references.md](.claude/rules/references.md): referência bibliográfica completa no KB
- [kb-links.md](.claude/rules/kb-links.md): todo doc do KB referencia ao menos um tema
- [git.yaml](.claude/commands/git.yaml): commit, push e checklist de pré-commit
  (o hook bloqueia KB inconsistente; nunca `--no-verify`)
- Variáveis de geradores no pipeline Python levam sufixo `_gen1`, `_gen2` etc.
