---
name: kb-index-pll
description: Índice da pasta pll/ do KB (gerado por scripts/kb_links.py)
aliases: [kb-index-pll]
---

# KB — pll/

Gerado por `scripts/kb_links.py index`; texto fora dos marcadores é preservado.

<!-- kb-links:begin -->
## Documentos

| Arquivo | Link | Cobre |
|---|---|---|
| [pll_asymmetric_fault_formal_analysis.md](pll_asymmetric_fault_formal_analysis.md) | [[pll-asymmetric-fault-formal-analysis]] | Análise formal do SRF-PLL sob falta assimétrica (Yazdani-Iravani §12.5.2) — equações da sequência negativa, ripple de 2ω₀ e mitigação por f… |
| [pll_contingencies.md](pll_contingencies.md) | [[pll-contingencies]] | Os 4 cenários de contingência simulados, efeitos no SRF-PLL e métricas de avaliação |
| [pll_cycle_slip_measurement.md](pll_cycle_slip_measurement.md) | [[pll-cycle-slip-measurement]] | Receita de medição do escorregamento de ciclo (cycle slipping) do SRF-PLL — arctan2+unwrap sobre vd/vq, com verificação cruzada via ângulos… |
| [pll_gain_voltage_dependence.md](pll_gain_voltage_dependence.md) | [[pll-gain-voltage-dependence]] | A sintonia do SRF-PLL degrada com a profundidade do afundamento (ωn e ξ ∝ √U) porque o laço é normalizado por constante — equivalência algé… |
| [pll_gains_methodology.md](pll_gains_methodology.md) | [[pll-gains-methodology]] | Metodologia TeseAGP (Kp=8·fg·Lest) dos ganhos do CONTROLADOR DE CORRENTE — não é o ganho do PLL, ver pll_loop_filter_gains.md |
| [pll_gains_provenance.md](pll_gains_provenance.md) | [[pll-gains-provenance]] | Procedência dos ganhos do SRF-PLL — literais hardcoded no netlist PSIM, cadeia PSIM→Simulink→params.m, e a dedução de que o laço está norma… |
| [pll_loop_filter_gains.md](pll_loop_filter_gains.md) | [[pll-loop-filter-gains]] | Ganhos do PI do laço do SRF-PLL (kp_pll=460, ki_pll=105820) — projeto de 2ª ordem por tempo de acomodação, ts=20 ms pelo critério de 1% (Te… |
| [pll_notch_implementation.md](pll_notch_implementation.md) | [[pll-notch-implementation]] | Notch de 120 Hz no laco do SRF-PLL - testado em 2026-05, removido do modelo final (2026-07) por ser desnecessario. Registro historico da te… |
| [pll_notch_integration.md](pll_notch_integration.md) | [[pll-notch-integration]] | Onde o notch de 120 Hz entraria no SRF-PLL (dentro do laço vs. por fora), relação com o modelo do projeto e resultado das tentativas de 202… |
| [pll_reactive_inertia.md](pll_reactive_inertia.md) | [[pll-reactive-inertia]] | PLL como "inércia reativa" e dualidade Q-δi (GFL) vs P-δv (síncronos/GFM) — framework estendido de estabilidade de sistemas com alta penetr… |
| [pll_ts_criterion_rationale.md](pll_ts_criterion_rationale.md) | [[pll-ts-criterion-rationale]] | Defesa da escolha do critério de 1% (numerador 4,6) na sintonia do SRF-PLL — argumento a favor, argumento contra (15% mais ripple de 2ω₀) e… |
| [srf_pll_theory.md](srf_pll_theory.md) | [[srf-pll-theory]] | Teoria do SRF-PLL — estrutura, modelo linear, projeto de ganhos (Karimi-Ghartemani cap.6) |

## Pastas relacionadas

- [dashboard/](../dashboard/index.md) — saem 2, chegam 3
- [events/](../events/index.md) — saem 1, chegam 0
- [inverter/](../inverter/index.md) — saem 2, chegam 6
- [power-system/](../power-system/index.md) — saem 3, chegam 6
- [psim/](../psim/index.md) — saem 1, chegam 3
- [simulation/](../simulation/index.md) — saem 2, chegam 3
- [standards/](../standards/index.md) — saem 3, chegam 5
- [tcc-word/](../tcc-word/index.md) — saem 3, chegam 5

Voltar: [índice do KB](../index.md) · [grafo](../grafo.md)
<!-- kb-links:end -->
