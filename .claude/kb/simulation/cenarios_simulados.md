---
name: cenarios-simulados
description: Inventário dos cenários exportados em output/results — 22 nominais + 4 com sintonia inadequada, as duas configurações temporais de falta e as lacunas de cobertura
source: output/results/*/fault_info.json (levantamento 2026-08-04); params.m linhas 13-17, 59-61
---

# Cenários Simulados — Inventário e Configuração Temporal

Levantado direto dos `fault_info.json` e do alcance de `t_s` nos CSVs.
Complementa [[export-workflow]] (como exportar) e
[[bad-pll-dashboard-filter]] (como o dashboard filtra por modo).

## As duas configurações temporais

**Ponto crítico:** os dois modelos **não** compartilham a mesma janela nem o
mesmo instante de falta.

| | Modelo Nominal | Modelo com Sintonia Inadequada |
|---|---|---|
| `kp_pll` / `ki_pll` | 460 / 105 820 | 92 / 21 164 (×0,2 nos dois) |
| `ω_n` / ξ | 325,3 rad/s / 0,707 | 145,5 rad/s / 0,316 |
| Aplicação da falta | `t` = 0,3 s | `t` = 0,6 s |
| Eliminação | `t` = 0,4 s | `t` = 0,7 s |
| Duração | 0,1 s (6 ciclos) | 0,1 s (6 ciclos) |
| Fim da simulação | `t` = 0,6 s | `t` = 1,0 s |

Motivo do deslocamento: com ξ = 0,316 o transitório de energização demora
muito mais a se acomodar. Aplicar a falta em 0,3 s no modelo desajustado
faria a perturbação incidir sobre um sistema ainda não estabilizado,
misturando o transitório de partida com a resposta à contingência. Atrasar
para 0,6 s garante que a falta atinja um sistema já em regime.

> ⚠️ O `params.m` guarda apenas o **estado atual** de `T_FAULT`/`T_CLEAR`
> (hoje 0,3/0,4). Ele **não** é fonte confiável do que cada cenário exportado
> usou. A fonte correta é o `fault_info.json` de cada pasta.

## Inventário (26 cenários)

### Nominais (22)

| Local | Tipos de falta |
|---|---|
| `bus4`, `bus5`, `bus6`, `bus7`, `bus8`, `bus9` | 1phase, 2phase, 3phase |
| `line7_8` | 3phase |
| `line8_9` | 2phase, 3phase |
| `regime` | (sem falta) |

### Sintonia inadequada (4)

`bus6/3phase_bad_pll`, `bus7/3phase_bad_pll`, `line7_8/3phase_bad_pll`,
`regime_bad_pll`.

Todos os 4 têm par nominal correspondente, então o toggle do dashboard
encontra equivalente em ambas as direções nos 4 casos.

## Lacunas de cobertura

1. **Nenhum cenário de sintonia inadequada com falta assimétrica.** Os 4
   existentes são trifásicos ou regime permanente. O mecanismo central do
   trabalho (sequência negativa → oscilação a `2ω_0` = 120 Hz em `v_q` →
   *cycle slipping*, ver [[pll-asymmetric-fault-formal-analysis]]) só se
   manifesta em falta assimétrica. O caso mais demonstrativo da tese,
   nominal × desajustado sob falta monofásica ou bifásica, **não existe nos
   dados**. Sugestão: `bus7/1phase_bad_pll` e `bus7/2phase_bad_pll`.
2. `line7_8` tem só 3phase; `line8_9` não tem 1phase.
3. Nenhuma falta em `bus1`, `bus2` (barra do inversor) ou `bus3`.

## Nomenclatura de `fault_type`

As pastas usam `1phase` / `2phase` / `3phase`. O [[export-workflow]] lista
também `2phase_ground` e `1phase_ground`, que **não aparecem** em nenhum
cenário exportado até hoje. Ao interpretar os dados, tratar `1phase` e
`2phase` como os tipos efetivamente simulados.
