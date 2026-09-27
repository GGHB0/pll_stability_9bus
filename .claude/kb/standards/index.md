---
name: kb-index-standards
description: Índice da pasta standards/ do KB (gerado por scripts/kb_links.py)
aliases: [kb-index-standards]
---

# KB — standards/

Gerado por `scripts/kb_links.py index`; texto fora dos marcadores é preservado.

<!-- kb-links:begin -->
## Documentos

### qualidade-energia/

| Arquivo | Link | Cobre |
|---|---|---|
| [harmonic_dq_frame_mapping.md](qualidade-energia/harmonic_dq_frame_mapping.md) | [[harmonic-dq-frame-mapping]] | Mapeamento formal ordem harmônica → bin do espectro dq (Yazdani & Iravani §4.2.4/4.3, fasor espacial + rotação dq) — por que a fundamental… |
| [harmonic_frequency_leakage.md](qualidade-energia/harmonic_frequency_leakage.md) | [[harmonic-frequency-leakage]] | Achado 2026-08-10, corrigido 2026-08-11 — o "2º harmônico" elevado na tabela pré-falta de todo cenário era vazamento espectral por F_FUND_H… |
| [harmonic_measurement_conditions.md](qualidade-energia/harmonic_measurement_conditions.md) | [[harmonic-measurement-conditions]] | Condições de medição de harmônico (IEEE 519-2014 Cl.4 + nota 118 do IEEE 1547.2-2023) confrontadas com a FFT implementada em spectrum.py —… |
| [harmonic_norm_application.md](qualidade-energia/harmonic_norm_application.md) | [[harmonic-norm-application]] | Como os critérios de significância de harmônico (ver harmonic-significance-criteria) se aplicam aos dados deste projeto — checagem por orde… |
| [harmonic_physical_origin_teodorescu.md](qualidade-energia/harmonic_physical_origin_teodorescu.md) | [[harmonic-physical-origin-teodorescu]] | Fundamentação bibliográfica (Teodorescu, Liserre & Rodríguez 2011) para a origem física de harmônicos pares vs ímpares em inversores e a ge… |
| [harmonic_significance_criteria.md](qualidade-energia/harmonic_significance_criteria.md) | [[harmonic-significance-criteria]] | Critérios da literatura para o que conta como harmônico de tensão/corrente "significativo" em pu — normas de conformidade (IEEE 519/1547) v… |
| [ieee1547_power_quality_clause7.md](qualidade-energia/ieee1547_power_quality_clause7.md) | [[ieee1547-power-quality-clause7]] | Mapa da Cláusula 7 (Power quality) do guia IEEE 1547.2-2023 — Tabelas 15-18, notas 118/119, a condição de ensaio de laboratório do §7.3.1,… |
| [ieee1547_pq_other_clauses.md](qualidade-energia/ieee1547_pq_other_clauses.md) | [[ieee1547-pq-other-clauses]] | Requisitos de QEE do IEEE 1547-2018 que NÃO são de harmônico — RVC (Tabela 16), flicker, sobretensão (§7.4) e o roteiro de estudo de QEE do… |
| [ieee519_structure.md](qualidade-energia/ieee519_structure.md) | [[ieee519-structure]] | Mapa de cláusulas e das cinco tabelas do IEEE 519-2014 — valores, páginas (PDF vs impressa), notas de rodapé e o que se aplica ou não à Bar… |

### ride-through/

| Arquivo | Link | Cobre |
|---|---|---|
| [china_lvrt_windfarm_test.md](ride-through/china_lvrt_windfarm_test.md) | [[china-lvrt-windfarm-test]] | Norma chinesa Q/GDW392-2009 de LVRT e teste de campo em turbina eólica PMSG (Mongólia Interior) — dados empíricos de falta simétrica vs. as… |
| [ieee1547_case_studies.md](ride-through/ieee1547_case_studies.md) | [[ieee1547-case-studies]] | Estudos de caso reais (CAISO, Entergy) sobre o impacto de ride-through/DVS de DER na recuperação de tensão do sistema — Annex I do IEEE Std… |
| [ieee1547_ride_through.md](ride-through/ieee1547_ride_through.md) | [[ieee1547-ride-through]] | Requisitos detalhados de LVRT/HVRT do IEEE Std 1547-2018 (categorias I/II/III, trip mandatório, Dynamic Voltage Support) extraídos do IEEE… |
| [lvrt.md](ride-through/lvrt.md) | [[lvrt-standards]] | Requisitos LVRT e IEEE 1547-2018 relevantes para avaliação do SRF-PLL |
| [ons_2_11.md](ride-through/ons_2_11.md) | [[ons-2-11]] | Função MATLAB ONS_2_11 — injeção de corrente reativa sob defeito (ONS Subm. 2.10 §5.8); código completo extraído do pll_stability_9bus.slx |
| [ons_frequency_ride_through.md](ride-through/ons_frequency_ride_through.md) | [[ons-frequency-ride-through]] | Faixas de operação em frequência não nominal (Submódulo 2.10 ONS) para centrais eólicas/fotovoltaicas — trip/ride-through, controle primári… |

## Pastas relacionadas

- [dashboard/](../dashboard/index.md) — saem 3, chegam 1
- [events/](../events/index.md) — saem 2, chegam 1
- [inverter/](../inverter/index.md) — saem 3, chegam 1
- [pll/](../pll/index.md) — saem 5, chegam 3
- [power-system/](../power-system/index.md) — saem 3, chegam 2
- [simulation/](../simulation/index.md) — saem 2, chegam 1
- [tcc-word/](../tcc-word/index.md) — saem 0, chegam 2

Voltar: [índice do KB](../index.md) · [grafo](../grafo.md)
<!-- kb-links:end -->
