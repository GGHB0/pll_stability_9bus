# TCC Word — Inventário de Siglas e Abreviaturas

> Levantamento por varredura do XML (Cap.1 em diante) em 2026-07-19, sobre
> `TCC_Victor_Bruno_V9_novo_indice.docx`. ✅ **INSERIDO em 2026-07-19**: as 31
> siglas abaixo substituíram as sobras do template (CTC/B, UERJ) na lista
> pré-textual, como edição direta (sem tracked change), formato
> `SIGLA<tab><tab>Significado` clonando o parágrafo do template.

## Siglas usadas no texto (31, após padronização IBR)

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
| IBR | Inverter-Based Resources (Recursos Baseados em Inversores) |
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

## Achados de revisão (resolvidos em 2026-07-19)

1. ✅ **IBR / RBI / ICR padronizados em IBR** (decisão do Victor): 2 ocorrências
   de RBI (Cap.4) e 2 de ICR (Introdução) reescritas como "Recurso(s) Baseado(s)
   em Inversor(es) (IBR/IBRs)". O título "3.2. Geração Distribuída e Inversores
   Conectados à Rede" ficou como está (prosa, sem sigla).
2. ✅ **Typo de referência corrigido**: "MOW, N." → **MOHAN, N.** nos 2 lugares
   (citação "(MOW, 2003)" na Introdução + entrada nas REFERÊNCIAS).
3. Ferramenta: o script de varredura vive em `C:\Temp\scan_siglas.py`
   (regex `\b[A-Z][A-Z0-9]{1,}(?:[-/][A-Z0-9]+)*\b` sobre o texto dos `<w:t>`,
   a partir do Ttulo1 "Capítulo 1" para pular pré-textual e cache do Sumário).
