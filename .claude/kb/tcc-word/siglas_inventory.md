# TCC Word — Inventário de Siglas e Abreviaturas

> Levantamento por varredura do XML (Cap.1 em diante) em 2026-07-19, sobre
> `TCC_Victor_Bruno_V9_novo_indice.docx`. A LISTA DE ABREVIATURAS E SIGLAS
> pré-textual do documento contém apenas sobras do template (CTC/B, UERJ) —
> precisa ser substituída por esta lista. **Inserção pendente de aprovação.**

## Siglas usadas no texto (33)

| Sigla | Significado |
|---|---|
| AVR | Automatic Voltage Regulator (Regulador Automático de Tensão) |
| CA | Corrente Alternada |
| CC | Corrente Contínua |
| DDSRF-PLL | Decoupled Double Synchronous Reference Frame PLL |
| EMT | Electromagnetic Transients (Transitórios Eletromagnéticos) |
| FRT | Fault Ride-Through |
| GD | Geração Distribuída |
| GFL | Grid-Following (seguidor de rede) |
| IAE | Integral of Absolute Error |
| IBR | Inverter-Based Resources (Recursos Energéticos Baseados em Inversores) |
| ICR | Inversor Conectado à Rede |
| IEEE | Institute of Electrical and Electronics Engineers |
| ISE | Integral of Squared Error |
| ITAE | Integral of Time-weighted Absolute Error |
| LCL | filtro Indutivo–Capacitivo–Indutivo |
| LG | falta monofásica à terra (Line-to-Ground) |
| LLG | falta bifásica à terra (Line-to-Line-to-Ground) |
| LVRT | Low Voltage Ride-Through |
| MPPT | Maximum Power Point Tracking |
| ONS | Operador Nacional do Sistema Elétrico |
| PAC | Ponto de Acoplamento Comum |
| PD | Phase Detector (Detector de Fase) |
| PI | Proporcional-Integral |
| PLL | Phase-Locked Loop |
| PSS | Power System Stabilizer (Estabilizador de Potência) |
| PWM | Pulse Width Modulation (Modulação por Largura de Pulso) |
| RAP | Relatório de Análise de Perturbação |
| RBI | Recurso Baseado em Inversor |
| SIN | Sistema Interligado Nacional |
| SPWM | Sinusoidal Pulse Width Modulation |
| SRF-PLL | Synchronous Reference Frame Phase-Locked Loop |
| VCO | Voltage-Controlled Oscillator (Oscilador Controlado por Tensão) |
| VSI | Voltage Source Inverter (Inversor Fonte de Tensão) |

## Excluídas de propósito

- **MATLAB, PSIM** — nomes de software, não siglas
- **AC1C, PSS1A, SM** — nomes de modelos de excitatriz/estabilizador (Simulink)
- **SPST** — nome do bloco de chave no PSIM (aparece 1×, descrição de circuito)
- **PV** — tipo de barra (aparece 1×, "Barra 3, PV a 1,025 pu")
- **SRF-EPLL** — só aparece no título de uma referência (Escobar 2021)
- Nomes de autores em citações (KUNDUR, LISERRE, RODRIGUEZ etc.)

## Achados de revisão

1. **Inconsistência IBR / RBI / ICR** — três siglas para conceitos praticamente
   iguais: IBR no Resumo/Abstract e Cap.2, RBI no Cap.4 (metodologia), ICR na
   Introdução e Cap.3. Padronizar ou listar as três com remissão — decisão do Victor.
2. **Typo de referência**: "MOW, N." → autor correto é **MOHAN, N.**
   (Power Electronics: Converters, Applications, and Design). Ver `pendencias.md` P2.
3. Ferramenta: o script de varredura vive em `C:\Temp\scan_siglas.py`
   (regex `\b[A-Z][A-Z0-9]{1,}(?:[-/][A-Z0-9]+)*\b` sobre o texto dos `<w:t>`,
   a partir do Ttulo1 "Capítulo 1" para pular pré-textual e cache do Sumário).
