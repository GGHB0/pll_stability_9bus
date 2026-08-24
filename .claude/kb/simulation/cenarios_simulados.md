---
name: cenarios-simulados
description: Inventário dos cenários exportados em output/results — 22 nominais + 10 com sintonia inadequada, as duas configurações temporais de falta e as lacunas de cobertura
source: output/results/*/fault_info.json (levantamento 2026-08-19); params.m linhas 13-17, 59-61
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

## Inventário (32 cenários)

### Nominais (22)

| Local | Tipos de falta |
|---|---|
| `bus4`, `bus5`, `bus6`, `bus7`, `bus8`, `bus9` | 1phase, 2phase, 3phase |
| `line7_8` | 3phase |
| `line8_9` | 2phase, 3phase |
| `regime` | (sem falta) |

### Sintonia inadequada (10)

| Local | Tipos de falta |
|---|---|
| `bus6`, `bus7` | 1phase_bad_pll, 2phase_bad_pll, 3phase_bad_pll |
| `line7_8` | 3phase_bad_pll |
| `regime_bad_pll` | (sem falta) |

`bus6` e `bus7` ganharam o conjunto completo (1/2/3phase) em 2026-08-11/12 —
antes só tinham `3phase_bad_pll`, preenchendo a lacuna de falta assimétrica
com sintonia inadequada apontada na revisão anterior deste inventário
(2026-08-04). Todos os 10 têm par nominal correspondente, então o toggle do
dashboard encontra equivalente em ambas as direções.

## ⚠️ Duas safras de modelo nos cenários `_bad_pll`

Descoberto em 2026-08-22 ao redigir o Cap. 5 (ver
[[tcc-revisao-fragmento-cap5]]). Os cenários com sintonia inadequada **não**
vêm todos da mesma versão do modelo. Impressão digital = transitório de
energização, que independe da falta aplicada:

| Safra | Cenários | Acomoda (±5°) | `v_d` pré-falta |
|---|---|---|---|
| **Julho** | `regime_bad_pll`, `bus7/3phase_bad_pll`, `bus6/3phase_bad_pll`, `line7_8/3phase_bad_pll` | ~599 ms | **0,80–0,82 pu** |
| **Agosto (11-12)** | `bus6`/`bus7` × `1phase_bad_pll`/`2phase_bad_pll` | 54 ms | **0,99 pu** |
| *(nominais)* | todos | 32 ms | 0,97–0,99 pu |

### Causa raiz (2026-08-23)

Commit `2a9b6d2` de 2026-07-21, *Fix ONS_2_11 overvoltage sign bug*: antes
dele o ramo de sobretensão da função usava `k_high = -10`, levando `iq_ref`
a −1 acima de 1,10 pu em vez de +1. Ver [[ons-2-11]].

**Teste para classificar qualquer pasta:** `iq_ref` médio enquanto
`hypot(vd_ufv_pu, vq_ufv_pu) > 1,10` nos primeiros 300 ms.

| Grupo | Nº | `iq_ref` em sobretensão |
|---|---|---|
| Pré-correção | 26 (todos os nominais + os 4 `_bad_pll` de julho) | −0,417 a −0,495 |
| Pós-correção | 4 (`bus6`/`bus7` × `1phase`/`2phase_bad_pll`) | +0,110 |

O corte é limpo, sem valores intermediários. Note que **todos os nominais são
pré-correção**, inclusive `bus7/3phase` (21/07) e `line8_9/*` (22/07).

**Alcance:** o bug age só na energização (janela fecha em ~38 ms). Os estados
pré-falta coincidem entre os grupos — `v_d` 0,9894 (pré) contra 0,9963 (pós),
P 0,875 contra 0,869, erro de fase < 0,02° nos dois. Como as faltas entram em
0,3 s ou 0,6 s, **a resposta à falta não é contaminada**; só análises da
partida é que são.

**Regra prática:** para comparar resposta à falta, qualquer par serve. Para
comparar energização ou regime, conferir se os dois lados estão no mesmo
grupo. Confirmado na auditoria de 2026-08-23: os 4 pares do Cap. 5 cruzam a
fronteira (nominal pré, `_bad_pll` pós) e ainda assim os estados pré-falta
ficam a 0,7% um do outro em `v_d` e em P.

Anomalia à parte: `line7_8/3phase_bad_pll` tem retenção de 65,5% (nominal:
11,3%) e 0,416 pu de 120 Hz numa falta **trifásica equilibrada** (nominal:
0,0002 pu). Esse run não corresponde à falta que o nome indica, não usar.
Números refeitos em 2026-08-23 com as definições fechadas em
[[tcc-revisao-fragmento-cap5-metricas]].

## Lacunas de cobertura

1. `bus4`, `bus5`, `bus8`, `bus9` e `line8_9` não têm variante
   `_bad_pll` — só `bus6`, `bus7` e `line7_8` (este último só 3phase).
2. `line7_8` tem só 3phase (nominal e bad_pll); `line8_9` não tem 1phase.
3. Nenhuma falta em `bus1`, `bus2` (barra do inversor) ou `bus3`.

## Nomenclatura de `fault_type`

As pastas usam `1phase` / `2phase` / `3phase`. O [[export-workflow]] lista
também `2phase_ground` e `1phase_ground`, que **não aparecem** em nenhum
cenário exportado até hoje. Ao interpretar os dados, tratar `1phase` e
`2phase` como os tipos efetivamente simulados.
