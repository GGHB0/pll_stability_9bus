---
name: tcc-docx-content-map
description: Mapa de conteúdo seção a seção do TCC_Victor_Bruno_V9_novo_indice_2.docx — estado atual, problemas estruturais e inventário de figuras
metadata:
  type: project
---

# TCC Word — Mapa de Conteúdo do Documento

> Estado de cada seção do `TCC_Victor_Bruno_V9_novo_indice_2.docx` (arquivo
> canônico desde 2026-07-22, ver `tcc-docx-canonical-file` na memória e
> `historico_entregas.md`). Cap. 1 a 3 conforme `dump_headings.py` de
> 2026-07-22; **Cap. 4 e 5 substituídos em 2026-09-02** pelo fragmento
> revisado (ver [[tcc-mesclagem-cap45-canonico]]). Sempre rodar
> `dump_headings.py` antes de confiar em números de seção — o Word renumera e
> o usuário edita entre sessões.
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
- ✅ **3.5** Sintonia do Controlador de Corrente por Forma Canônica de
  Segunda Ordem (**NOVA, 2026-08-05**) — reaplica a forma canônica de 2ª
  ordem da Equação (3.18) à planta de corrente `G(s)=1/(s·Lest)` (equações
  3.21–3.23), chegando às expressões `Kp=8·fg·Lest`/`Ki=32·fg²·Lest`
  efetivamente usadas em §4.3.2.2. Motivação: pedido do usuário de que
  "todas as formulações do capítulo 4" tenham contrapartida simbólica no
  Cap. 3 antes de serem aplicadas — ver `historico_entregas.md`
- ⬜ **3.6** Resumo ou Conclusões do Capítulo (renumerado de 3.5 → 3.6)

## Cap. 4 — Metodologia de Análise

> **Substituído por inteiro em 2026-09-02** pelo Cap. 4 do fragmento
> `capitulos_4_5_revisados.docx`. O mapa detalhado do texto antigo saiu daqui
> junto com o texto; o inventário do que foi descartado está em
> [[tcc-mesclagem-cap45-canonico]] e o texto integral, no backup
> `..._backup_20260902_004347.docx`.

- ✅ **4.1** Foco do estudo
- ✅ **4.2** Plataformas de simulação e características individuais
  (Python analítico · PSIM em nível de circuito · Simulink sistêmico)
- ✅ **4.3** Modelagem e dimensionamento do sistema de estudo
  - **4.3.1** Modelo da rede elétrica e equivalente de Thévenin — Figura 4.1
    (unifilar IEEE 9 barras com a UFV na Barra 2)
  - **4.3.2** Projeto do conversor e dos controladores — 4.3.2.1 filtro LCL
    (Figura 4.2; `ω_res` = 9068,99 rad/s, R_d1/R_d2/R_d3), 4.3.2.2 controle de
    corrente, 4.3.2.3 SRF-PLL (Figura 4.3; `Kp,PLL` = 460 / `Ki,PLL` = 105 820,
    sintonia inadequada a 20% → `ω_n` = 145,5, ξ = 0,316)
  - **4.3.3** Configuração do sistema de monitoramento e tratamento de dados —
    Figura 4.4 (organização dos cenários por falta e sintonia)
  - **4.3.4** Protocolos de contingência — falta de 0,1 s (6 ciclos); nominal
    0,3→0,4 s com janela até 0,6 s, inadequada 0,6→0,7 s com janela até 1,0 s
- ✅ **4.4** Síntese da metodologia

> ⚠️ O Cap. 4 ficou **mais raso** que o anterior: saíram a modelagem dinâmica
> dos geradores (H₁/H₃, AVR/PSS/Governor), a topologia do bloco de falta, o
> parágrafo de solver e taxas e três tabelas. Conferir
> [[tcc-mesclagem-cap45-canonico]] antes de concluir que algo "nunca foi
> escrito".

## Cap. 5 — Análise e Discussão de Resultados

> **Substituído por inteiro em 2026-09-02**, na mesma operação. Números
> auditados (ver [[tcc-revisao-fragmento-cap5-metricas]] e o `_54`), 15 figuras.

- ✅ **5.1** Validação da operação em regime permanente — Figuras 5.1 a 5.3
- ✅ **5.2** Faltas simétricas: severidade e localização — Figuras 5.4 a 5.6
- ✅ **5.3** Faltas assimétricas: sequência negativa e efeito da sintonia —
  Figuras 5.7 a 5.10
- ✅ **5.4** Perda de sincronismo sob falta simétrica no ponto de conexão —
  Figuras 5.11 a 5.15, o caso-limite `bus7/3phase_bad_pll`
- ✅ **5.5** Conformidade com o código de rede
- ✅ **5.6** Resumo e conclusões do capítulo

> Tese: a sintonia inadequada é um **compromisso** entre imunidade durante a
> falta e velocidade na recuperação, com um caso-limite em que o compromisso
> deixa de valer e o SRF-PLL não reaquisita o sincronismo dentro da janela
> simulada. Instrução do Oscar de **não** implementar salto de fase segue
> valendo.

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
| **3.1** | **Circuito VSI trifásico com filtro LCL e blocos PWM** | ✅ virou a Fig. 4.2 do fragmento ([[tcc-revisao-fragmento-cap4]]) |

> Os placeholders acima são dos Cap. 2 e 3 e seguem com a numeração herdada
> do V8 (2.1, 2.6...), não renumerada junto com os capítulos. Os Cap. 4 e 5 já
> têm **19 figuras reais** (4.1 a 4.4 e 5.1 a 5.15), inseridas na mesclagem de
> 2026-09-02 com legenda acima, "Fonte: Os autores (2026)." abaixo e largura
> ajustada à área útil A4 de 6,30 in.
