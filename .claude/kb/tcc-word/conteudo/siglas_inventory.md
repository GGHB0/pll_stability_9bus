---
name: tcc-siglas-inventory
description: Inventário de 36 siglas do TCC: lista ordenada, revisão 2026-09-13, formatação, ferramenta varredura
aliases: [tcc-siglas-inventory]
---

# TCC Word — Inventário de Siglas e Abreviaturas

> **Revisão de 2026-09-13** sobre `TCC_Victor_Bruno_V9_novo_indice_2.docx`
> (decisão do Victor): a lista pré-textual passa a ter **só siglas usadas no
> texto**. Das 31 inseridas em 2026-07-19, 9 não apareciam mais em lugar
> nenhum e saíram; 14 usadas no corpo (quase todas do Cap. 2) entraram. Total: **36**.
> Varredura: todo o documento, incluindo tabelas, legendas e caixas de texto,
> excluindo a própria lista.

## Lista atual (36, ordem alfabética)

| Sigla | Significado |
|---|---|
| BESS | Battery Energy Storage System (Sistema de Armazenamento de Energia em Baterias) |
| CA | Corrente Alternada |
| CC | Corrente Contínua |
| CIGRE | Conseil International des Grands Réseaux Électriques |
| COI | Center of Inertia (Centro de Inércia) |
| DDSRF-PLL | Decoupled Double Synchronous Reference Frame Phase-Locked Loop |
| DSO | Distribution System Operator (Operador do Sistema de Distribuição) |
| EMT | Electromagnetic Transients (Transitórios Eletromagnéticos) |
| ENTSO-E | European Network of Transmission System Operators for Electricity |
| FFR | Fast Frequency Response (Resposta Rápida de Frequência) |
| FRT | Fault Ride-Through |
| GD | Geração Distribuída |
| GFL | Grid-Following (Seguidor de Rede) |
| GFM | Grid-Forming (Formador de Rede) |
| IBR | Inverter-Based Resources (Recursos Baseados em Inversores) |
| IEA | International Energy Agency (Agência Internacional de Energia) |
| IEEE | Institute of Electrical and Electronics Engineers |
| LCL | Filtro Indutivo–Capacitivo–Indutivo |
| LVRT | Low Voltage Ride-Through (Suportabilidade a Afundamentos de Tensão) |
| ONS | Operador Nacional do Sistema Elétrico |
| PCC | Ponto de Conexão Comum |
| PD | Phase Detector (Detector de Fase) |
| PI | Proporcional-Integral |
| PLL | Phase-Locked Loop (Malha de Captura de Fase) |
| PWM | Pulse Width Modulation (Modulação por Largura de Pulso) |
| RAP | Relatório de Análise de Perturbação |
| SCR | Short-Circuit Ratio (Relação de Curto-Circuito) |
| SEN | Sistema Eléctrico Nacional (Chile) |
| SEP | Sistema Elétrico de Potência |
| SIN | Sistema Interligado Nacional |
| SOTF | Switch Onto Fault (Fechamento sob Falta) |
| SRF-PLL | Synchronous Reference Frame Phase-Locked Loop (65 ocorrências, a mais usada) |
| TSO | Transmission System Operator (Operador do Sistema de Transmissão) |
| UFV | Usina Fotovoltaica (só na legenda da Figura 4.1) |
| VCO | Voltage-Controlled Oscillator (Oscilador Controlado por Tensão) |
| VSI | Voltage Source Inverter (Inversor Fonte de Tensão) |

Instituições com nome próprio (IEEE, CIGRE, ENTSO-E) ficam sem tradução,
também para não quebrar linha.

## Regra de definição no texto (2026-09-26, aprovada pelo Victor)

No corpo (Cap. 1 até Referências), a sigla aparece por extenso **só na 1ª
ocorrência**, no padrão `Nome (SIGLA)`, e depois só como sigla. Termo em
inglês com tradução: `tradução, ou *English Name* (SIGLA)`, com o nome inglês
em itálico (SCR, FFR, SOTF). Ficam fora: Resumo/Abstract (textos
independentes), títulos de seção (mudariam o sumário) e legendas (lista de
figuras). Sigla citada uma vez só (DDSRF-PLL, UFV) e instituição (IEEE,
CIGRE, ENTSO-E) não entram na regra.

Aplicada no V10 (52 trocas, [[tcc-historico-entregas]]): redefinições
removidas em PLL, SRF-PLL, PI, CC, SIN, LVRT, PCC, GFL, PWM, VSI, IBR, EMT e
ONS; definição movida para a 1ª ocorrência em IBR (Intro), PI (objetivos,
Cap. 1), CA (§3.1.2), PWM (§3.1.4) e ONS (Intro, RAP); LCL ganhou definição
(§4.2). Formas soltas por extenso depois da definição também viraram sigla
("ponto de conexão comum", "transitórios eletromagnéticos", "Recursos
Baseados em Inversores"). Varredura: `C:\Temp\scan_siglas.py` (marca "DEF"
em sigla seguida de parênteses; sigla seguida de citação dá falso positivo).

## Removidas em 2026-09-13 (zero ocorrências fora da lista)

AVR, IAE, ISE, ITAE, LG, LLG, MPPT, PSS, SPWM. Vieram do inventário de
julho e deixaram de aparecer no texto em alguma edição posterior (não
rastreado qual).

## Fora da lista de propósito

- **CSV**: aparece 1× (4.3.3); o Victor pediu para não listar.
- **Unidades**: MW, GW, TWh, MVA.
- **Software**: MATLAB, PSIM, NumPy.
- **TR77**: nome de relatório (IEEE TR77), não sigla.
- **CC-CA**: composição de CC e CA, já listadas.
- **Plurais**: IBRs, SEPs.
- Nomes de modelo/bloco do Simulink/PSIM (AC1C, PSS1A, SM, SPST), tipo de
  barra (PV), SRF-EPLL (só em título de referência) e sobrenomes de autores.

## Formatação da lista

36 linhas cabem numa folha (folha 13) com: `spacing after=60`, `line=240`;
**uma** parada de tab em 1701 twips (3 cm) + `ind left=1701 hanging=1701` +
`jc=left`; **um** `<w:tab/>` entre sigla e significado. O formato antigo (dois
tabs padrão, justificado) desalinhava toda sigla com mais de ~6 caracteres
(CIGRE, DDSRF-PLL, ENTSO-E, SRF-PLL) e jogava a 2ª linha do BESS na margem.
Sigla nova entra clonando qualquer parágrafo da lista e trocando só os textos.

## Ferramenta

Varredura: regex `(?<![\w-])[A-Z][A-Z0-9]{1,}(?:[-/][A-Z0-9]+)*(?![\w-])`
sobre o texto dos `<w:t>`, do título "Capítulo 1" até REFERÊNCIAS, mais uma
segunda passada para sigla com minúscula (`IBRs`, `RoCoF`). Contagem por
sigla com lookaround, nunca substring (ISE casa LISERRE).

## Histórico (2026-07-19)

31 siglas inseridas no lugar das sobras do template (CTC/B, UERJ);
padronização RBI/ICR → IBR; typo MOW → MOHAN. Detalhe em
`historico_entregas_2026_07.md`.

## Relacionados

- [[tcc-docx-content-map]] — estrutura do documento que usa estas siglas
- [[tcc-full-prefacio]] — localização da lista nas páginas pré-textuais
