---
name: cenarios-simulados
aliases: [cenarios-simulados]
description: Inventário dos cenários exportados em output/results, validação depois de cada pull (validar_cenarios.py), as safras de modelo dos cenários com sintonia inadequada e as lacunas de cobertura
source: output/results/*/fault_info.json (levantamento 2026-10-01); scripts/validar_cenarios.py; params.m linhas 13-17, 36-61
---

# Cenários Simulados — Inventário, Validação e Safras

Levantado direto dos `fault_info.json` e dos CSVs. Complementa
[[export-workflow]] (como exportar), [[resimulacao-abc]] (runbook do Bruno) e
[[bad-pll-dashboard-filter]] (como o dashboard filtra por modo).

## Configuração temporal

| | Nominal | Sintonia inadequada |
|---|---|---|
| `kp_pll` / `ki_pll` | 460 / 105 820 | 92 / 21 164 (×0,2 nos dois) |
| `ω_n` / ξ | 325,3 rad/s / 0,707 | 145,5 rad/s / 0,316 |
| Falta / eliminação / fim | 0,3 / 0,4 / 0,6 s | 0,3 / 0,4 / 0,6 s (safra de 01/10/2026) |

Até 30/09/2026 a sintonia inadequada usava falta em 0,6 s, eliminação em
0,7 s e fim em 1,0 s. A justificativa era que o modelo antigo levava ~0,55 s
para assentar a energização. Na re-simulação de 01/10/2026, o modelo com
sintonia inadequada assenta em ~74 ms (nominal: ~45 ms; critério P/Q a
0,08 pu do valor final), e o Bruno passou para a mesma janela do nominal.
A última pasta da safra antiga, `bus6/1phase_bad_pll`, foi apagada em
01/10/2026; a monofásica da Barra 6 agora é `bus6/1phase_ground_bad_pll`.

> ⚠️ O `params.m` guarda apenas o **estado atual** de `T_FAULT`/`T_CLEAR`.
> A fonte do que cada cenário usou é o `fault_info.json` de cada pasta.
> Geradores de figura usam `settle_de()` de `gen_fault_waveforms.py`, que
> corta em 0,55 s só quando a falta cai depois disso (safra antiga).

## Validação depois de cada `git pull` com simulação nova

```text
.venv\Scripts\python.exe scripts\validar_cenarios.py
```

| Nível | Código | O que pega |
|---|---|---|
| ERRO | `duplicado` | `sim_data.csv` idêntico byte a byte a outra pasta, e esta é a cópia (assinatura errada) |
| ERRO | `assinatura` | trifásica desequilibrada, ou mono/bifásica com afundamento equilibrado nas tensões abc do inversor |
| AVISO | `duplicado` | idêntico a outra pasta, mas esta tem a assinatura coerente (é o original) |
| AVISO | `safra` | sintonia inadequada com falta fora de 0,3 s |
| AVISO | `redundante` | `1phase_bad_pll` e `1phase_ground_bad_pll` na mesma barra |

Assinatura: RMS de cada fase (30 ms após a falta até a eliminação) dividido
pelo RMS pré-falta; desequilíbrio = maior menos menor. Trifásica fica abaixo
de 0,05. Mono e bifásica reais ficam entre 0,23 e 0,98.

Os geradores (`gen_erro_fase`, `gen_fault_waveforms`, `gen_matriz_cenarios`)
importam `cenario_ok()` e `pasta_inadequada()` e **pulam pasta reprovada**.
`pasta_inadequada()` prefere `1phase_ground_bad_pll` e a safra atual.

### Resultado em 01/10/2026 (commit `c07457a`)

| Pasta | Situação |
|---|---|
| `bus7/1phase_bad_pll` | **ERRO**: cópia de `line7_8/3phase_bad_pll` (afundamento equilibrado de 0,10 pu) |
| `bus7/1phase_ground_bad_pll` | **ERRO**: cópia de `bus7/3phase_bad_pll` |
| `line8_9/2phase` (nominal, jul/2026) | **ERRO**: afundamento equilibrado (0,01 pu); é trifásica com nome de bifásica |
| `bus6/1phase_ground_bad_pll` | válida; a `bus6/1phase_bad_pll` (safra antiga) foi apagada |
| `bus7/3phase_bad_pll`, `line7_8/3phase_bad_pll` | válidas (originais das duas cópias) |

A causa provável das cópias é um export com `logsout` de uma rodada anterior.
**A monofásica na Barra 7 com sintonia inadequada precisa ser re-simulada.**

## Inventário (30 pastas, 28 aprovadas)

| Local | Nominal | Sintonia inadequada |
|---|---|---|
| `bus4`, `bus5`, `bus8`, `bus9` | 1phase, 2phase, 3phase | — |
| `bus6` | 1phase, 2phase, 3phase | 1phase_ground, 2phase, 3phase |
| `bus7` | 1phase, 2phase, 3phase | 2phase, 3phase (`1phase_ground` reprovada; `1phase_bad_pll` apagada em 01/10) |
| `line7_8` | 3phase | 3phase |
| `line8_9` | 3phase (2phase reprovado) | — |
| `regime` | sem falta | sem falta |

A matriz de cenários é gerada por `scripts/gen_matriz_cenarios.py`
(`assets/diagrams/matriz_cenarios.svg`, Tabela 4.1 do canônico; ver
[[tcc-revisao-fragmento-cap4]]) e conta só pasta aprovada. O PNG sai pelo
Edge headless (ver a skill svg-diagrams).

## Safras de modelo dos cenários com sintonia inadequada

| Safra | Cenários | `v_d` pré-falta | Falta |
|---|---|---|---|
| Julho/2026 | todos substituídos em 01/10 | 0,80–0,82 pu | 0,6 s |
| Agosto (11-12) | todos substituídos em 01/10 | 0,99 pu | 0,6 s |
| **01/10/2026** | `regime`, `bus6` 1φ-terra/2φ/3φ, `bus7` 2φ/3φ, `line7_8` 3φ | **1,00 pu** | 0,3 s |
| *(nominais, jul/2026)* | todos | 0,99 pu | 0,3 s |

O `v_d` de 0,82 pu da safra de julho é o que o Oscar questionou nos
comentários do V10 (ver [[tcc-revisao-fragmento-cap5]]).

**Bug de sinal da ONS 2.11 (histórico).** Commit `2a9b6d2` (21/07/2026):
antes dele, `iq_ref` ia a −1 acima de 1,10 pu (ver [[ons-2-11]]). Ele afeta só
a energização (~38 ms), não a resposta à falta. Teste: `iq_ref` médio enquanto
`hypot(vd_ufv_pu, vq_ufv_pu) > 1,10` nos primeiros 300 ms (pré-correção dá
−0,42 a −0,50; pós-correção dá +0,11). **Todos os nominais são pré-correção.**
Para comparar resposta à falta, qualquer par serve. Para comparar
energização, conferir o grupo.

## Erro de fase com a safra de 01/10 (comparado ao texto do Cap. 5)

Medido por `scripts/gen_erro_fase.py`, com a receita de
[[tcc-revisao-fragmento-cap5-metricas]]. Os nominais batem com o texto.

| Cenário com sintonia inadequada | Pico na falta | Retorno a ±2° | Antes (V10 ou safra antiga) |
|---|---|---|---|
| regime (energização) | — | 79 ms | 563 ms (V10) |
| `bus6/2phase` | 34,5° | 30 ms | 34,9° / 78 ms (V10) |
| `bus6/1phase_ground` | 12,8° | 31 ms | 13,2° / 47 ms (safra de agosto) |
| `bus7/1phase` | reprovado | — | 72,2° / 98 ms (V10) |
| `bus7/2phase` | 179,9° | 96 ms | — |
| `bus7/3phase` | 44,0° | não retorna | perda de sincronismo |
| `line7_8/3phase` | 34,6° | não retorna | (sem texto) |

Recuperação (t_s) nominal → inadequada: `bus6/2phase` 48 → 30 ms,
`bus6/1phase` 39 → 31 ms, `bus7/2phase` 51 → 96 ms, `bus6/3phase` 76 →
106 ms. Retenção `v_d`: `bus7/3phase` 9,2% → 8,2% (pré-falta 0,989 → 1,002
pu), `line7_8/3phase_bad_pll` 9,7%. Já aplicado ao texto do V10 em 01/10
(ver [[tcc-historico-entregas]]).

**`bus7/3phase_bad_pll` e `line7_8/3phase_bad_pll` perdem o sincronismo**
depois da eliminação: o erro de fase gira continuamente e P se inverte até o
fim da janela. Antes de 01/10, só a Barra 7 perdia sincronismo, e o
`line7_8/3phase_bad_pll` antigo era uma rodada inválida. Os números do §5.4
precisam ser refeitos (ver [[tcc-revisao-fragmento-cap5-metricas-54]]).

## Lacunas de cobertura

1. `bus4`, `bus5`, `bus8`, `bus9` e `line8_9` não têm sintonia inadequada.
2. `line7_8` só tem trifásica; `line8_9` não tem monofásica, e a bifásica foi
   reprovada.
3. Nenhuma falta em `bus1`, `bus2` (barra do inversor) ou `bus3`.

## Nomenclatura de `fault_type`

O export atual grava `1phase_ground` e `2phase_ground` (tabela do `params.m`).
As pastas nominais antigas usam `1phase`, que é o mesmo tipo de falta
(monofásica à terra). O `app.py` já rotula as duas formas.
