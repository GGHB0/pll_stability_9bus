---
name: tcc-docx-content-map
description: Mapa de conteúdo seção a seção do TCCs Victor e Bruno_V8_revisado.docx — estado atual, problemas estruturais e inventário de figuras
metadata:
  type: project
---

# TCC Word — Mapa de Conteúdo do Documento

> Estado de cada seção do `TCCs Victor e Bruno_V8_revisado.docx` (307 parágrafos — junho/2026).
> Padrões de edição OOXML e IDs: ver `docx_structure.md`.

## Legenda

- ✅ Redigido · ✏️ Parcial/problema · ⬜ Vazio · ⚠️ Problema estrutural

## Introdução (sem número)

- ✅ Contextualização: transição energética, desafios de integração de renováveis
- ✅ Motivação: apagão 15/08/2023 no SIN — 23.368 MW = 34,5% da carga do SIN; ONS concluiu que inversores tiveram desempenho "aquém dos modelos matemáticos"
- ✅ Vulnerabilidade do SRF-PLL: dependência de sinal de tensão de boa qualidade
- ✅ Objetivos específicos (5 itens)
- ✅ Referências [1]–[9] (Mohan, Xiong, Yazdani, Teodorescu, Enhanced PLL, Wu-Wang, RAP-ONS)

## Cap. 2 — Fundamentação Teórica

- ⚠️ **"A Necessidade das Transformadas de Referência"** — Ttulo2 SEM número, aparece antes de 2.1
  - ✅ Clarke (abc→αβ): sistema estacionário, ainda senoidal
  - ✅ Park (αβ→dq): referencial girante a ω; grandezas viram CC em regime permanente
  - ✅ Controle P/Q desacoplado: P ∝ id, Q ∝ iq quando Vq=0
  - ✅ Arquitetura de controle por corrente em cascata (malha interna)
- ✅ **2.1** Geração Distribuída e Inversores Conectados à Rede
  - VSI como interface CC→CA; IBRs; redução de inércia do sistema; [FIGURA 2.1]
- ✅ **2.2** Controle de Inversores e Transformadas de Referência
  - PWM tratado funcionalmente (escopo delimitado — não detalha estratégias)
- ✅ **2.3** O Sistema de Sincronismo SRF-PLL
  - PD = Transformada de Park (vq como erro de fase)
  - PI: velocidade vs. imunidade a ruído (trade-off Kp/Ki)
  - VCO = integrador digital → θ estimado
  - Linearização; Equações 2.5–2.12 (placeholder de equações no texto)
  - Referências: Teodorescu, Yazdani, Rodriguez, AGP/Alves 2022, Escobar 2021
- ✅ **2.4** Desafios à Estabilidade do Sincronismo
  - ⚠️ **2.4.1** Natureza das contingências (voltage sag, phase-angle jump, assimetria) — **estilo Ttulo4, deveria ser Ttulo3**
  - ⚠️ **2.4.2** Requisitos LVRT/FRT (permanência conectada, injeção reativa) — **estilo Ttulo4**
  - ⚠️ **2.4.3** Código de Rede ONS Submódulo 2.10 (curvas LVRT, injeção reativo) — **estilo Ttulo4**
    - [FIGURA ONS curva LVRT] placeholder presente (§190)
    - [FIGURA ONS injeção reativo] placeholder presente (§193)

## Cap. 3 — Metodologia de Projeto e Simulação

- ✅ **3.1** Plataforma Multiplataforma
  - Python/NumPy: dimensionamento LCL, Ybarra→Zbarra, Thevenin
  - PSIM: validação circuito, PWM/alta frequência, semicondutores
  - MATLAB/Simulink: rede IEEE 9 barras, máquinas síncronas (modelo completo dq), EMT sistêmico
  - ⚠️ Refs MATLAB/PSIM pendentes (Oscar comentário #9)
- ✅ **3.2** Modelagem e Dimensionamento
  - ✅ **3.2.1** IEEE 9 barras modificado: G2 → VSI; Thevenin Z22 da Zbarra para PSIM
  - ⚠️ **3.2.2** Projeto do Conversor (VSI 2 níveis, SPWM, filtro LCL, PI corrente, SRF-PLL)
    - Referencia [FIGURA 3.1] em §215 e §220 mas **placeholder não existe** → P1 em docx_structure.md
    - Dimensionamento LCL: L1 (ripple), C (5% Q reativo), ressonância, amortecimento
    - Sintonia PI: cancelamento polo-zero no referencial síncrono
- ✏️ **3.3** Protocolos de Contingência (adicionado por Claude com tracked changes)
  - ✏️ **3.3.1** Afundamento Simétrico (3LG; sem seq. negativa; mais favorável ao PLL; [TABELA 3.1])
  - ✏️ **3.3.2** Afundamento Assimétrico (LG/LLG; seq. negativa → 2ω₀ ≈ 753 rad/s em vq; [TABELA 3.2])
  - ⚠️ **Todo o texto sem acentuação** — redigido sem UTF-8 correto, corrigir em futura edição

## Cap. 4 — Análise e Discussão de Resultados (PRIORIDADE)

- ✅ Introdução do capítulo (2 parágrafos sobre EMT em PSIM + Simulink)
- ⬜ **4.1** Desempenho sob Afundamentos Simétricos
  - ✏️ **4.1.1** Resposta Dinâmica e Tempo de Acomodação — contém apenas "."
  - ⬜ **4.1.2** Impacto na Injeção de P e Q — vazio
- ⬜ **4.2** Limites de Robustez sob Contingências Assimétricas e Saltos de Fase
  - ⬜ **4.2.1** Instabilidade sob Faltas Assimétricas — vazio
  - ⬜ **4.2.2** Impacto do Salto de Fase — vazio · **NÃO implementar (Oscar)**
- ⬜ **4.3** Análise de Sensibilidade e Diretrizes de Projeto
  - ✅ Parágrafo introdutório (menciona ganhos PI e robustez)
  - ⬜ **4.3.1** Influência dos Ganhos do PI — vazio
  - ⬜ **4.3.2** Conformidade com LVRT — vazio

## Conclusão

- ⬜ Placeholder (não redigida)

## Referências (seção final)

- ⚠️ Mistura do template UERJ (referências fictícias de exemplo) com as refs reais [1]–[9] do TCC
- Limpar: remover entradas do template, manter apenas as refs citadas no texto

## Inventário de Figuras

| Figura | Descrição | Parágrafo (~) | Estado |
|---|---|---|---|
| 2.1 | Diagrama esquemático de VSI conectado à rede | §139 | placeholder texto OK |
| 2.6 | Perfil característico de afundamento de tensão | §184 | placeholder texto OK |
| 2.X (ONS) | Curva de suportabilidade LVRT — ONS Sub. 2.10 | §190 | placeholder texto OK |
| 2.X (ONS) | Requisito de injeção de reativo — ONS Sub. 2.10 | §193 | placeholder texto OK |
| **3.1** | **Circuito VSI trifásico com filtro LCL e blocos PWM** | **§215, §220** | **SEM placeholder ⚠️** |
