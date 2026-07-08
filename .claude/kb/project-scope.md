---
name: project-scope
description: Escopo completo do TCC — título, autores, estrutura de capítulos, status e conexões entre os artefatos do projeto
source: TCCs Victor e Bruno_V8.docx (comentado)
---

# Escopo do TCC — Visão Geral

**Título:** Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos
**Autores:** Bruno Henrique De Oliveira · Victor Hugo De Avelar Rezende
**Orientador:** Prof. Dr. Oscar Cuaresma Zevallos
**Coorientador:** Prof. Dr. André Guilherme Peixoto Alves (AGP) ← autor da TeseAGP.pdf
**Instituição:** UERJ — Faculdade de Engenharia, 2025

## Motivação Central

Perturbação de 15/08/2023 no SIN brasileiro: 23.368 MW desconectados = 34,5% da carga do SIN.
ONS concluiu que inversores eólicos/fotovoltaicos tiveram desempenho "aquém dos modelos matemáticos".
→ Lacuna entre comportamento simulado e real dos algoritmos de sincronismo.

## Estrutura dos Capítulos

| Cap. | Título | Status |
|------|--------|--------|
| 1 | Introdução + Motivação + Objetivos | **Redigido** |
| 2 | Fundamentação Teórica | **Redigido** |
| 3 | Metodologia de Projeto e Simulação | **Redigido** |
| 4 | Análise e Discussão de Resultados | **Vazio** (só placeholders) |
| — | Conclusão | Placeholder |

**O capítulo 4 é a prioridade pendente do trabalho.**

> Estado granular Cap. 4 (2026-06): apenas títulos existem. 4.1.1 contém só ".".
> Subseções a redigir: 4.1.1, 4.1.2, 4.2.1, 4.3.1, 4.3.2.
> **4.2.2 (salto de fase) NÃO será implementado** — instrução do Oscar.
> Mapa completo do documento: `.claude/kb/tcc-word/content_map.md`.

## Objetivos Específicos (Cap. 1)

1. Modelagem matemática do sistema inversor-rede (foco na dinâmica do PLL em dq)
2. Identificar condições que comprometem rastreamento de fase/frequência (via simulação EMT)
3. Avaliar impactos: oscilações de potência, sobrecorrentes
4. Analisar capacidade de suporte reativo (LVRT)
5. Identificar fatores críticos: ganhos Kp/Ki do PI e impedância da rede

## Plataforma Híbrida (Cap. 3)

| Ferramenta | Papel |
|---|---|
| Python + NumPy/Pandas | Dimensionamento analítico LCL; Ybarra→Zbarra; Thevenin |
| PSIM | Validação do estágio de potência; PWM; transitórios rápidos |
| MATLAB/Simulink | Rede IEEE 9 barras completa; propagação de distúrbios |

## Sistema Elétrico (Cap. 3.2.1)

- **Base:** IEEE 9 barras (benchmark Anderson-Fouad)
- **Adaptação:** G2 (Barra 2) substituído pelo VSI (IBR)
- **Sistema híbrido:** G1 e G3 síncronos + VSI na Barra 2
- **Thevenin para PSIM:** Z_th = Z22 da Zbarra (diagonal da inversa de Ybarra)
- Ver [[pll-gains-methodology]] para os valores numéricos

## Contingências Simuladas (4 cenários)

| Cenário | Efeito no PLL |
|---|---|
| Afundamento simétrico | Redução de amplitude; sem sequência negativa |
| Afundamento assimétrico | Introduz sequência negativa → oscilação de 2ª harmônica no dq |
| Salto de fase (phase-angle jump) | Pode fazer o PLL perder o lock completamente |
| Alto RoCoF | Rastreamento de frequência limitado pela largura de banda do PI |

## Métricas de Avaliação

- **IAE** — Integral do Erro Absoluto do ângulo de fase
- **ISE** — Integral do Erro Quadrático
- **ts** — Tempo de acomodação do erro de fase
- Oscilações de potência ativa P e reativa Q
- Conformidade com LVRT (IEEE 1547-2018)

## Conexões entre Artefatos

```
TeseAGP.pdf (co-orientador AGP)
  └─ Metodologia Kp/Ki → notebooks/pll_stability_9bus_analysis.ipynb
       └─ Parâmetros → pll_stability_9bus.slx (MATLAB/Simulink)

Karimi-Ghartemani cap.6 → teoria SRF-PLL
  └─ Modelo linearizado → projeto PI do PLL (Cap. 3.2.2)
```

## Ponto Crítico: Sequência Negativa

Afundamentos assimétricos introduzem componente de sequência negativa.
No referencial síncrono (dq), essa componente aparece como oscilação de **2ª harmônica** (120 Hz em 60 Hz).
O SRF-PLL padrão não filtra essa oscilação → erro de rastreamento oscilatório → degradação de P e Q.
Essa é a limitação central identificada no trabalho.

## Achados Recentes para o Capítulo 4 (2026-05)

- A análise de resultados deve destacar a interação entre **baixa inércia nas máquinas
  G1/G3**, severidade do curto e perda de sincronismo do SRF-PLL.
- Foi feita varredura com `H` das máquinas e reatância de curto entre **2% e 20%**
  de **529 ohms**.
- Nos testes atuais, `H > 0,1 s` evitou o colapso total; abaixo/próximo desse valor,
  o sistema entra em região crítica.
- O colapso observado ocorre na recuperação pós-contingência: o PLL tenta retornar,
  acumula erro/oscila em loop e deixa de fornecer uma referência angular útil.
- `Id` e `Iq` deixam de seguir trajetória coerente quando `theta_hat` se perde.
- As tentativas de notch/filtro para remover componentes de `120 Hz` não resolveram
  os casos severos; elas seguem relevantes para curtos assimétricos moderados, mas
  não substituem uma solução estrutural para baixa inércia e lock-loss.

## Problemas Estruturais do DOCX (2026-06)

Levantados na revisão completa do `TCCs Victor e Bruno_V8_revisado.docx` (307 parágrafos):

1. Seção "A Necessidade das Transformadas de Referência" sem número (Ttulo2 antes de 2.1).
2. Subseções 2.4.1/2.4.2/2.4.3 com estilo `Ttulo4` em vez de `Ttulo3`.
3. [FIGURA 3.1] referenciada 2× em 3.2.2 (§215, §220) sem placeholder no texto.
4. Seção 3.3 (adicionada por Claude) sem acentuação correta em todo o texto.
5. Lista de referências final mistura template UERJ com refs reais do TCC.

Tratamento e priorização: `.claude/kb/tcc-word/docx_structure.md` → "Pendências Priorizadas".
