---
name: tcc-full-prefacio
description: Conteúdo completo das páginas pré-textuais do TCC — capa, folha de rosto, resumo, abstract, listas e sumário
metadata:
  type: project
---

# TCC — Páginas Pré-Textuais

## Capa / Folha de Rosto

**Instituição:** Universidade do Estado do Rio de Janeiro · Centro de Tecnologia e Ciências · Faculdade de Engenharia

**Autores:** Bruno Henrique De Oliveira · Victor Hugo De Avelar Rezende

**Título:** Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos

**Tipo:** Projeto de graduação — Engenheiro Eletricista — UERJ · Rio de Janeiro · 2025

**Orientador:** Prof. Dr. Oscar Cuaresma Zevallos

**Coorientador:** Prof. Dr. André Guilherme Peixoto Alves

## Resumo

OLIVEIRA, Bruno Henrique de; REZENDE, Victor Hugo de Avelar. Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos. XXf. Projeto Final (Graduação em Engenharia Elétrica, Ênfase: Sistema de Potência) – Faculdade de Engenharia, Universidade do Estado do Rio de Janeiro, Rio de Janeiro, 2025.

Este trabalho analisa o desempenho dinâmico do algoritmo de sincronismo Synchronous Reference Frame Phase-Locked Loop (SRF-PLL) sob contingências em sistemas elétricos. Impulsionado pela crescente penetração de Recursos Energéticos Baseados em Inversores (IBRs) e pela consequente redução da inércia sistêmica, o sincronismo robusto tornou-se um pilar para a estabilidade da rede. A motivação central advém de eventos reais, como a perturbação de 15 de agosto de 2023 reportada pelo Operador Nacional do Sistema Elétrico (ONS), que expôs a vulnerabilidade dos IBRs. A metodologia emprega simulação computacional em ambiente EMT (MATLAB/Simulink) para submeter um modelo de inversor conectado à rede (VSI) a um conjunto de cenários críticos, destacando-se as faltas simétricas, assimétricas e distúrbios com afundamentos de tensão expressivos. O desempenho é quantificado por métricas de erro, como a Integral do Erro Absoluto (IAE) e a Integral do Erro Quadrático (ISE), além do tempo de acomodação do erro de fase. Os resultados identificam as limitações operacionais do SRF-PLL padrão, notadamente sua suscetibilidade a componentes de sequência negativa durante desequilíbrios, que geram oscilações de segunda harmônica no referencial síncrono. O trabalho conclui avaliando a capacidade da técnica em manter o sincronismo e cumprir requisitos de Low Voltage Ride-Through (LVRT), propondo recomendações para o aumento de sua robustez.

**Palavras-chave:** SRF-PLL. Sincronismo. Inversores Conectados à Rede. Contingências Elétricas. Estabilidade de Sistema de Potência.

## Abstract

This paper presents … . *(placeholder — a ser redigido)*

**Keywords:** Formatting. Final project. Engineering.

## Sumário (estrutura de seções)

- INTRODUÇÃO
- Capítulo 2 – Fundamentação Teórica
  - 3.1. A Necessidade das Transformadas de Referência *(número incorreto no ToC)*
  - 2.1. Geração Distribuída e Inversores Conectados à Rede
  - 2.2. Controle de Inversores e Transformadas de Referência
  - 2.3. O Sistema de Sincronismo SRF-PLL
  - 2.4. Desafios à Estabilidade do Sincronismo: Contingências Elétricas e Requisitos Normativos
- 3 CAPÍTULO – METODOLOGIA DE PROJETO E SIMULAÇÃO
  - 3.1. PLATAFORMA DE SIMULAÇÃO E JUSTIFICATIVA TÉCNICA
  - 3.2. MODELAGEM E DIMENSIONAMENTO DO SISTEMA DE ESTUDO
    - 3.2.1. Modelo da Rede Elétrica: Sistema IEEE 9 Barras Modificado
    - 3.2.2. Projeto do Conversor e dos Controladores
- Capítulo 4 – Análise e Discussão de Resultados
  - 4.1. Desempenho do SRF-PLL sob Afundamentos de Tensão Simétricos
    - 4.1.1. Resposta Dinâmica e Tempo de Acomodação
    - 4.1.2. Impacto na Injeção de Potência Ativa e Reativa
  - 4.2. Limites de Robustez sob Contingências Assimétricas e Saltos de Fase
    - 4.2.1. Instabilidade sob Faltas Assimétricas
    - 4.2.2. Impacto do Salto de Fase (Phase-Angle Jump)
  - 4.3. Análise de Sensibilidade e Diretrizes de Projeto
    - 4.3.1. Influência dos Ganhos do Controlador PI do PLL
    - 4.3.2. Conformidade com o Código de Rede (LVRT)
