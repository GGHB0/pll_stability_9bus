---
name: psim-modeling
description: Fase inicial de modelagem do PLL no PSIM (Altair) — inventário, parâmetros e Vcc, antes da migração para Simulink
source: pasta PSim/ (netlists .txt + parameters100MVA.txt, GGHB, 2026-07-22)
---

# Modelagem Inicial no PSIM (Fase Pré-Simulink)

Antes de o sistema ser migrado para o Simulink atual
(`pll_stability_9bus.slx`), o inversor conectado à rede com SRF-PLL foi
**primeiro modelado no PSIM** (Altair Engineering). Esta é a fase inicial
do trabalho — relevante para o TCC ao descrever *como a implementação
começou*.

- **Quem tem o PSIM:** GGHB. Arquivos binários commitados em 2026-07-21
  (`0a364aa`); **netlists em texto** commitadas em 2026-07-22 na branch
  `agent-include-output-folder` ("Add PSim text exports").
- **Objetivo destes arquivos no repo:** registro histórico. **Não** há
  intenção de reaproveitar os dados do PSIM na análise atual (essa roda em
  Simulink → Python).
- **Topologia dos circuitos:** ver [[psim-netlists]].

## Inventário dos Arquivos (`PSim/`)

| Arquivo | Tipo | Legível? |
|---|---|---|
| `01_..._100MVA (backup)1.psimsch` | Esquemático (v25.1.0) | ✗ binário |
| `01_..._100MVA.smv` | Resultados SimView (14,8 MB) | ✗ binário |
| `04_...Filtro 100MVA.psimsch` | Esquemático (v25.0.0) | ✗ binário |
| `04_...Filtro 100MVA.smv` | Resultados SimView (245 KB) | ✗ binário |
| `01_..._100MVA (backup)1.txt` | **Netlist do circuito 01** | ✓ texto |
| `04_...Filtro 100MVA.txt` | **Netlist do circuito 04** | ✓ texto |
| `parameters100MVA.txt` | **Parâmetros** (UTF-16) | ✓ texto |

- `.psimsch`/`.smv` são **binários proprietários da Altair** — só abrem no
  PSIM/SimView, corpo ofuscado (não zip/zlib), sem tabela de sinais. Não
  tentar parsear por script (já verificado).
- Os `.txt` são **exports em texto do próprio PSIM** (netlist + parâmetros)
  — é por eles que a topologia foi documentada.

## Parâmetros (`parameters100MVA.txt`) — base 100 MVA

| Símbolo | Valor | Nota |
|---|---|---|
| `Vcc` | **90 909 V (90,9 kV)** | valor base (= notebook/AGP) |
| `L1` | 0,030421 / 4 | indutor lado inversor |
| `L2` | 0,00028900 / 4 | indutor lado rede |
| `C1` | 4,2471e-5 / 4 | capacitor do LCL |
| `Rd1`,`Rd2`,`Rd3` | 0,57342 / 0,0054475 / 3,1228 (÷4) | resistências série/amortecimento |
| `Kp` | 29,4815 / 4 = **7,370** | PI de corrente |
| `Ki` | 7075,56 / 4 = **1768,89** | PI de corrente |
| `qsi` (ξ) | 0,707 | amortecimento do notch |
| `wres` | **9068,997 rad/s** | ressonância do LCL |
| `Rth`,`Lth` | 0,010039 / 0,0011602 | impedância de Thévenin |

Consistências com o projeto atual (`CLAUDE.md`):
- `wres`, `ξ`, `fs = 5 kHz`, e a **divisão por 4** dos ganhos/impedâncias
  (conversão pu, `Z_base = 4 Ω`) batem com a modelagem atual.
- **Vcc — o override já existia no PSIM:** o arquivo base usa 90,9 kV, mas
  a netlist do circuito 01 referencia `parameters100MVA_VCCnovo.txt` e usa
  **VDC = 136,4 kV** (o `VDC4` da ponte). É a origem da divergência
  registrada em [[project_vcc_convention]].

> **Numeração arbitrária:** os prefixos `01`/`04` dos arquivos não indicam
> ordem nem sequência — são só rótulos. São dois esquemáticos
> independentes (um sistema EMT completo e uma bancada de controle).

## Lacunas — PENDENTE (opcional, coletar com o GGHB)

- `parameters100MVA_VCCnovo.txt` (variante com Vcc = 136,4 kV usada no
  sistema completo) — **não** foi exportado; só temos o arquivo base.
- Formas de onda do SimView — **não necessárias** (não vamos reprocessar).

## Fio Narrativo para o TCC

No PSIM foram construídos dois esquemáticos: uma **bancada de projeto do
controle de corrente** (planta RL × LCL) e o **sistema EMT completo**
(VSC + LCL + SRF-PLL com PD/PI/VCO + SPWM, com degrau de referência).
Dessa fase inicial o trabalho migrou para **Simulink/MATLAB**
(`pll_stability_9bus.slx`, ver [[export-workflow]] e
`kb/inverter/simulink_model.md`) → análise em **Python** ([[python-pipeline]]).
