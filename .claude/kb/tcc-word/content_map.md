---
name: tcc-docx-content-map
description: Mapa de conteúdo seção a seção do TCC_Victor_Bruno_V9_novo_indice_2.docx — estado atual, problemas estruturais e inventário de figuras
metadata:
  type: project
---

# TCC Word — Mapa de Conteúdo do Documento

> Estado de cada seção do `TCC_Victor_Bruno_V9_novo_indice_2.docx` (arquivo
> canônico desde 2026-07-22, ver `tcc-docx-canonical-file` na memória e
> `historico_entregas.md`). Numeração confirmada via `dump_headings.py`
> em 2026-07-22 (tarde): retém a estrutura da reestruturação de 2026-07-19
> (4.1/4.2/4.3.1–4.3.4/4.4) — **diferente** da numeração do arquivo sem
> sufixo (obsoleto), que o usuário reestruturou mais uma vez por conta
> própria. Sempre rodar `dump_headings.py` antes de confiar em números de
> seção — o Word renumera e o usuário edita os dois arquivos de formas
> diferentes entre sessões.
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
  ~10 Hz, mitigação = sintonia `Kp,PLL`/`Ki,PLL` do PLL). **Ampliado
  2026-08-04**: CIGRE CSE N037 citada como classificação alternativa (TR77
  segue como base) e parágrafo novo com o mecanismo físico completo
  (sequência negativa → 120 Hz em `v_q` → perda de travamento → cycle
  slipping → colapso do controle vetorial)
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
  equações 3.10–3.17 em tabela invisível (ver `equacoes.md`). **Ampliado
  2026-08-04**: metodologia de projeto dos ganhos do laço (equações
  3.18–3.20), `Kp,PLL = 460` e `Ki,PLL = 105 820` por 2ª ordem com ξ = 0,707
  e `t_s` = 20 ms, fechando com `2ω_0` = 754 rad/s a 2,32·`ω_n`. É aqui que a
  distinção contra os ganhos do controlador de corrente é estabelecida
- ⬜ **3.5** Resumo ou Conclusões do Capítulo

## Cap. 4 — Metodologia de Análise (numeração confirmada 2026-07-22, tarde)

- ✅ **4.1** Foco do Estudo
- ✅ **4.2** Plataformas de Simulação – Características Individuais
  - ⚠️ Refs MATLAB/PSIM pendentes (Oscar comentário #9)
- ✅ **4.3** Modelagem e Dimensionamento do Sistema de Estudo
  - ✅ **4.3.1** Modelo da Rede Elétrica: Sistema IEEE 9 Barras Modificado
    (G2→VSI; Thevenin Z22 p/ PSIM)
  - ✅ **4.3.2** Projeto do Conversor Fonte de Tensão e dos Controladores
    - **4.3.2.1** Dimensionamento do Filtro de Acoplamento (LCL) — eqs 4.1/4.2;
      inclui validação no bloco PSIM `PlantaLCL1` (ω_res = 9068,9968 rad/s) e
      amortecimento com valores de R_d1/R_d2/R_d3 (adicionado 2026-07-22)
    - **4.3.2** abre (desde 2026-08-04) declarando as **duas etapas de
      modelagem**: PSIM contra equivalente de Thévenin (`Rth` = 0,0100 Ω,
      `Lth` = 1,16 mH) e depois Simulink sobre o IEEE 9 barras, com o `.slx`
      como plataforma oficial dos resultados (ver [[psim-modeling]])
    - **4.3.2.2** Sintonia da Estratégia de Controle de Corrente — inclui
      parágrafo sobre a malha PSIM (I_d,ref/I_q,ref → m_a, portadora VTRI2,
      5 kHz) adicionado 2026-07-22. **Desde 2026-08-04** é aqui que vive a
      fórmula `Kp = 8·f_g·(L1+L2+Lest)` / `Ki = 32·f_g²·(...)` = 29,48 /
      7075,6, com o escalamento para pu (7,37 / 1768,9). Ela estava
      erradamente no 4.3.2.3 rotulada como ganho do PLL
    - **4.3.2.3 Modelagem do Sistema de Sincronismo (SRF-PLL)** — descreve
      implementação no **PSIM** (subcircuitos `.SUB Clarke`/`.SUB Park`, Loop
      Filter PI, VCO via bloco `RESETI_I1`); sem menção a arquivo/script de
      parâmetros nem ao notch 120 Hz (nunca existiu no PSIM, ver
      [[psim-modeling]]) — linguagem de código removida 2026-07-22
      (ver `feedback_docx_no_code_artifacts` na memória). **Corrigido
      2026-08-04**: passa a citar `Kp,PLL` = 460 / `Ki,PLL` = 105 820 e
      remeter ao §3.4, com aviso explícito de não confundir com os ganhos do
      controlador de corrente
    - ⚠️ Referencia [FIGURA 3.1] mas **placeholder não existe** → P1
  - ✅ **4.3.3** Configuração da Simulação e Modelagem Dinâmica dos Geradores
    — **desde 2026-08-04** apresenta os **dois cenários de sintonia**: Modelo
      Nominal (460 / 105 820, `ω_n` = 325,3, ξ = 0,707) e Modelo com Sintonia
      Inadequada (92 / 21 164, `ω_n` = 145,5, ξ = 0,316), com a sintonia do
      PLL como única variável independente
    - 4.3.3.1 Modelagem Dinâmica dos Geradores Síncronos (G1/G3) — fecha
      ligando a baixa inércia (`H₁`, `H₃`) à sensibilidade ao PLL
    - **4.3.3.2** Topologia da Falta e Configuração do Bloco de Contingência —
      Simulink (bloco `Fault Three-Phase` + chaves SPST), 4 tipos;
      "parâmetros configuráveis do modelo de simulação" (sem citar
      variáveis/script — corrigido 2026-07-22). **Desde 2026-08-04** traz as
      **duas configurações temporais**: Nominal 0,3→0,4 s com janela até
      0,6 s; Sintonia Inadequada 0,6→0,7 s com janela até 1,0 s, duração de
      0,1 s (6 ciclos) nos dois. Confere com os `fault_info.json` exportados
      (ver [[cenarios-simulados]])
    - 4.3.3.3 Configuração do Sistema de Monitoramento, Variáveis Relevantes e
      Tratamento de Dados
  - ✏️ **4.3.4** Protocolos de Contingência e Análise de Cenários
    - 4.3.4.1 Afundamento de Tensão Simétrico · 4.3.4.2 Afundamento de Tensão
      Assimétrico
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
  - ✏️ **5.3.1** Influência dos Ganhos do PI — texto + [RESULTADOS A INSERIR];
    referência à divisão adicional por 4 no Simulink limpa de "params.m"/
    "bloco de controle" 2026-07-22 (mantém atribuição a Simulink, que é
    correta aqui — ver `feedback_docx_no_code_artifacts`)
  - ✏️ **5.3.2** Conformidade com LVRT — texto + [A COMPLEMENTAR: curva ONS]
- ⬜ **5.4** (Resumo/fechamento)

## Cap. 6 — Conclusões · Cap. 7 — Trabalhos Futuros

- ✏️ Conclusão redigida (cycle slipping, LVRT formal vs. efetivo);
  Trabalhos Futuros separado como capítulo próprio (índice novo)

## Referências (seção final)

- ⚠️ Mistura template UERJ (refs fictícias) com refs reais — limpar
- ⚠️ Parágrafo "REFERÊNCIAS" sem estilo de título (fora do Sumário)
- **+4 entradas em 2026-08-04**: ALVES; DIAS; ROLIM (2020, DOI
  10.1007/s40313-020-00576-x), CIGRE (CSE N037, **ano a confirmar**, ver
  `pendencias.md` item 16), OGATA (2009) e STRAUSS-MINCU et al. (2026, DOI
  10.1109/MPE.2025.3617895). As três últimas já eram citadas no texto sem
  constar da lista

## Inventário de Figuras

| Figura | Descrição | Estado |
|---|---|---|
| 2.1 | Diagrama esquemático de VSI conectado à rede | placeholder texto OK |
| 2.6 | Perfil característico de afundamento de tensão | placeholder texto OK |
| 2.X (ONS) | Curva de suportabilidade LVRT — ONS Sub. 2.10 | placeholder texto OK |
| 2.X (ONS) | Requisito de injeção de reativo — ONS Sub. 2.10 | placeholder texto OK |
| **3.1** | **Circuito VSI trifásico com filtro LCL e blocos PWM** | **SEM placeholder ⚠️** (citada em 4.3.2.1) |

> Numeração das figuras ainda é a herdada do V8 (2.1, 2.6, 3.1...) — não foi
> renumerada junto com os capítulos; revisar quando as imagens forem inseridas.
