---
name: tcc-docx-content-map
description: Mapa de conteúdo seção a seção do TCC_Victor_Bruno_V9_novo_indice.docx — estado atual, problemas estruturais e inventário de figuras
metadata:
  type: project
---

# TCC Word — Mapa de Conteúdo do Documento

> Estado de cada seção do `TCC_Victor_Bruno_V9_novo_indice.docx` (numeração
> do índice do professor, atualizado 2026-07-19 após reestruturação do Cap.4).
> Padrões de edição OOXML e IDs: ver `docx_structure.md`.

## Legenda

- ✅ Redigido · ✏️ Parcial/problema · ⬜ Vazio · ⚠️ Problema estrutural

## Cap. 1 — Introdução

- ✅ Contextualização, motivação (apagão 15/08/2023 — 23.368 MW = 34,5% do SIN),
  vulnerabilidade do SRF-PLL, objetivos específicos (5 itens)

## Cap. 2 — Desafios à Estabilidade em Redes Dominadas por Inversores (NOVO)

- ✅ **2.1** Redes elétricas em transição — redigido 2026-07-19 (IEA GER2026:
  demanda elétrica +3%, solar PV +600 TWh, IBR 5%→17% da matriz em 1 década)
- ✅ **2.2** Classificação Clássica da Estabilidade — redigido 2026-07-19
  (Gu & Green/JPROC: definição IEEE/CIGRE 2004, 3 dimensões, GFL vs. GFM)
- ✅ **2.3** Classificação Estendida da Estabilidade — redigido 2026-07-19
  (Strauss-Mincu et al./Roadmap alemão: IEEE TR77, converter-driven stability
  ~10 Hz, mitigação = sintonia Kp/Ki do PLL)
- ✅ **2.4** Principais blecautes — redigido 2026-07-19: intro + 2.4.1 Ibéria
  2025 (ENTSO-E) · 2.4.2 Chile 2025 (Coordinador Eléctrico Nacional) ·
  2.4.3 Brasil 2023 (ONS RAP-ONS 00012/2023 — inércia/SCC descartados como
  causa, suporte de reativo dos IBR é o fator determinante)
- ✅ **2.5** Contingências e Requisitos Normativos (migrado do antigo Cap.2):
  2.5.1 LVRT/FRT · 2.5.2 ONS Submódulo 2.10 · 2.5.3 natureza das contingências
- ⬜ **2.6** Resumo do capítulo — vazio (título com tracked change não aceito)

> 2.1-2.4.3 redigidos em sessão Opus (2026-07-19), fontes preparadas em sessão
> Sonnet anterior — ver `kb/power-system/energy_transition_iea2026.md`,
> `stability_classification_classic.md`, `stability_classification_extended.md`,
> `kb/events/brasil_2023_overview.md` + `brasil_2023_root_causes.md`. Novas
> referências que passam a ser citadas no texto e ainda **não estão** na lista
> de Referências do documento: IEA (2026), KUNDUR et al. (2004) [distinta de
> KUNDUR (1994) já citada em 2.5.3], GU; GREEN (2023), STRAUSS-MINCU et al.
> (2026), ENTSO-E (2026), COORDINADOR ELÉCTRICO NACIONAL (2025), ONS (2023)
> [distinta de ONS (2022), já citada]. Ver `pendencias.md` item 15.

## Cap. 3 — Fundamentação Teórica

- ✅ **3.1** Transformadas de referência (3.1.1 Clarke · 3.1.2 Park ·
  3.1.3 controle P/Q desacoplado · 3.1.4 arquitetura em cascata)
- ✅ **3.2** Geração Distribuída e Inversores Conectados à Rede ([FIGURA 2.1])
- ✅ **3.3** Controle de Inversores (3.3.1 PWM — funcional, escopo delimitado)
- ✅ **3.4** O Sistema de Sincronismo SRF-PLL — PD/PI/VCO, linearização,
  equações 3.1–3.17 em tabela invisível (ver `equacoes.md`)
- ⬜ **3.5** Resumo ou Conclusões do Capítulo

## Cap. 4 — Metodologia de Análise (reestruturado 2026-07-19)

- ✅ Intro do capítulo (abordagem quantitativa + 4 etapas)
- ✅ **4.1** Foco do Estudo — NOVO (2 §§: SRF-PLL grid-following sob
  contingência; IEEE 9 barras modificado; CC/MPPT fora do escopo)
- ✅ **4.2** Plataformas de Simulação – Características Individuais
  (Python/NumPy/Pandas, PSIM, MATLAB/Simulink)
  - ⚠️ Refs MATLAB/PSIM pendentes (Oscar comentário #9)
- ✅ **4.3** Modelagem e Dimensionamento do Sistema de Estudo
  - ✅ **4.3.1** IEEE 9 barras modificado (G2→VSI; Thevenin Z22 p/ PSIM)
  - ✅ **4.3.2** Projeto do Conversor Fonte de Tensão e dos Controladores
    - 4.3.2.1 Filtro LCL (eqs 4.1/4.2) · 4.3.2.2 PI de corrente ·
      4.3.2.3 SRF-PLL (bloco Sinusoidal Measurement, notch 120 Hz, Kp/Ki)
    - ⚠️ Referencia [FIGURA 3.1] mas **placeholder não existe** → P1
  - ✅ **4.3.3** Configuração da Simulação e Modelagem Dinâmica dos Geradores
    - Intro: ode23t (trapezoidal implícito, passo variável), RelTol 10⁻³,
      Ts=5 µs, Tsc=200 µs (5 kHz), janela 0,6 s, R2025a (confirmar versão)
    - 4.3.3.1 Geradores G1/G3 (H₁=9,478 s, H₃=2,351 s, AVR AC1C, PSS1A)
    - 4.3.3.2 Falta: bloco Fault Three-Phase + chaves SPST, 0,3→0,4 s
      (6 ciclos), 4 tipos, FAULT_TYPE/BUS/LINE via params.m, **sem local fixo**
    - 4.3.3.3 Monitoramento: logsout em 5 grupos de sinais, 2 taxas +
      interpolação, export automático (CSV+metadados por cenário),
      pipeline Python (IAE/ISE/ts/pico/ΔP/ΔQ, FFT segmentada, LVRT 1547,
      tabela comparativa)
  - ✏️ **4.3.4** Protocolos de Contingência (rebaixado de Ttulo2; era 3.3 no V8)
    - 4.3.4.1 Afundamento Simétrico ([TABELA 3.1]) ·
      4.3.4.2 Assimétrico ([TABELA 3.2]) — Ttulo4, fora do Sumário
    - ⚠️ Texto original sem acentuação — corrigir em edição futura
- ⬜ **4.4** Resumo do Capítulo

## Cap. 5 — Análise e Discussão de Resultados (PRIORIDADE)

- ⬜ **5.1** Desempenho sob Afundamentos Simétricos
  - ✏️ **5.1.1** Resposta Dinâmica e Tempo de Acomodação — contém apenas "."
  - ⬜ **5.1.2** Impacto na Injeção de P e Q — vazio
- ✏️ **5.2** Limites de Robustez sob Contingências Assimétricas e Saltos de Fase
  - ✏️ **5.2.1** Instabilidade sob Faltas Assimétricas — cycle slipping descrito
  - **Salto de fase NÃO implementar** (instrução do Oscar)
- ✏️ **5.3** Impacto dos Ganhos do Controlador do SRF-PLL
  - ✏️ **5.3.1** Influência dos Ganhos do PI — texto + [RESULTADOS A INSERIR]
  - ✏️ **5.3.2** Conformidade com LVRT — texto + [A COMPLEMENTAR: curva ONS]
- ⬜ **5.4** (Resumo/fechamento)

## Cap. 6 — Conclusões · Cap. 7 — Trabalhos Futuros

- ✏️ Conclusão redigida (cycle slipping, LVRT formal vs. efetivo);
  Trabalhos Futuros separado como capítulo próprio (índice novo)

## Referências (seção final)

- ⚠️ Mistura template UERJ (refs fictícias) com refs reais — limpar
- ⚠️ Parágrafo "REFERÊNCIAS" sem estilo de título (fora do Sumário)

## Inventário de Figuras

| Figura | Descrição | Estado |
|---|---|---|
| 2.1 | Diagrama esquemático de VSI conectado à rede | placeholder texto OK |
| 2.6 | Perfil característico de afundamento de tensão | placeholder texto OK |
| 2.X (ONS) | Curva de suportabilidade LVRT — ONS Sub. 2.10 | placeholder texto OK |
| 2.X (ONS) | Requisito de injeção de reativo — ONS Sub. 2.10 | placeholder texto OK |
| **3.1** | **Circuito VSI trifásico com filtro LCL e blocos PWM** | **SEM placeholder ⚠️** (citada em 4.3.2) |

> Numeração das figuras ainda é a herdada do V8 (2.1, 2.6, 3.1...) — não foi
> renumerada junto com os capítulos; revisar quando as imagens forem inseridas.
