---
name: resimulacao-abc
description: Runbook de re-simulação (Bruno) — regenerar os 18 cenários para exportar sim_data_abc.csv (correntes trifásicas, painel abc do espectro)
---

# Re-simulação para export abc (runbook)

**Responsável: Bruno.** Objetivo: re-rodar os cenários já existentes para que
o export gere o novo `sim_data_abc.csv` (correntes trifásicas `iabc_inverter`
/`iabc_grid`) — ele alimenta o painel "Corrente i_a UFV (abc)" do espectro de
Fourier no dashboard ([[espectro-fourier]]).

Nada mais mudou no modelo: são as mesmas simulações de antes, só o script de
export (`scripts/export_sim_data.m`) ganhou um CSV a mais. Detalhes do export:
[[export-workflow]].

## Passo a passo (por cenário)

1. Abrir `pll_stability_9bus.slx` (raiz do repo) no MATLAB.
2. Editar o topo de `params.m` com o cenário da tabela abaixo e rodar
   `>> params` no Command Window.
3. Simular (▶). Ao terminar, o `StopFcn` exporta sozinho — conferir no
   Command Window a linha `Correntes abc: N amostras → ...`.
4. Verificar que `sim_data_abc.csv` apareceu na pasta do cenário em
   `output/results/`.

> ⚠️ Se a linha "Correntes abc" **não** aparecer no log, o sinal
> `iabc_inverter` não está no logsout (a função pula em silêncio) —
> avisar o Victor para inspecionar o modelo.

## Checklist — 18 cenários (estado de 2026-07-12)

Variáveis em `params.m`: `FAULT_BUS`, `FAULT_LINE`, `FAULT_TYPE`, `BAD_PLL`.

| # | Pasta | FAULT_BUS | FAULT_LINE | FAULT_TYPE | BAD_PLL |
|---|---|---|---|---|---|
| 1 | `regime` | 0 | `[]` | `'regime'` | false |
| 2 | `regime_bad_pll` | 0 | `[]` | `'regime'` | **true** |
| 3 | `bus4/3phase` | 4 | `[]` | `'3phase'` | false |
| 4 | `bus5/3phase` | 5 | `[]` | `'3phase'` | false |
| 5 | `bus6/1phase` | 6 | `[]` | `'1phase'` | false |
| 6 | `bus6/2phase` | 6 | `[]` | `'2phase'` | false |
| 7 | `bus6/3phase` | 6 | `[]` | `'3phase'` | false |
| 8 | `bus6/3phase_bad_pll` | 6 | `[]` | `'3phase'` | **true** |
| 9 | `bus7/1phase` | 7 | `[]` | `'1phase'` | false |
| 10 | `bus7/3phase` | 7 | `[]` | `'3phase'` | false |
| 11 | `bus7/3phase_bad_pll` | 7 | `[]` | `'3phase'` | **true** |
| 12 | `bus8/3phase` | 8 | `[]` | `'3phase'` | false |
| 13 | `bus8/3phase_bad_pll` | 8 | `[]` | `'3phase'` | **true** |
| 14 | `bus9/3phase` | 9 | `[]` | `'3phase'` | false |
| 15 | `line7_8/1phase` | 0 | `[7 8]` | `'1phase'` | false |
| 16 | `line7_8/2phase_ground` | 0 | `[7 8]` | `'2phase_ground'` | false |
| 17 | `line7_8/3phase` | 0 | `[7 8]` | `'3phase'` | false |
| 18 | `line7_8/3phase_bad_pll` | 0 | `[7 8]` | `'3phase'` | **true** |

A pasta de saída é montada sozinha pelo export a partir dessas variáveis —
não precisa criar pasta nem mover arquivo. Cenários `_bad_pll` usam o
`kp_pll × 0.2` automático do `params.m` (ver [[bad-pll-scenario]]).

Prioridade se não der tempo de rodar tudo: **#5 (bus6/1phase)** — é a falta
assimétrica com a assinatura de sequência negativa mais clara.

## Depois de simular

```powershell
.venv\Scripts\python.exe app.py
```

Regenera `output/pll_metrics.html`; o painel abc aparece automaticamente em
cada cenário que tiver o `sim_data_abc.csv`. Cenários ainda não re-simulados
continuam funcionando com os 3 painéis dq (o CSV abc é opcional).
