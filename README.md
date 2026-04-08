# Estabilidade de PLL em um Sistema de 9 Barras

<p align="center">
  <img src="assets/banner.svg" alt="PLL Stability banner" width="100%">
</p>

<p align="center">
  <img alt="Jupyter Notebook" src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
  <img alt="MATLAB" src="https://img.shields.io/badge/MATLAB-R202x-FF6F00?style=for-the-badge&logo=mathworks&logoColor=white">
  <img alt="Simulink" src="https://img.shields.io/badge/Simulink-Model-FF8C00?style=for-the-badge">
  <img alt="Power Systems" src="https://img.shields.io/badge/Power%20Systems-9%20Bus-0F766E?style=for-the-badge">
</p>

## Visao Geral

Este repositorio reune os materiais de estudo e os artefatos de simulacao usados na analise da **estabilidade de PLL em um sistema eletrico de 9 barras**, combinando:

- analise numerica em Jupyter Notebook;
- modelagem e simulacao em Simulink;
- uma base organizada para publicacao no GitHub.

## Conteudo do Repositorio

| Arquivo | Descricao |
| --- | --- |
| `TCC.ipynb` | Notebook principal com o fluxo analitico e computacional do estudo. |
| `GridTiedInverterOptimalI2.slx` | Modelo em Simulink usado nas simulacoes do sistema. |

## Destaques

- Fluxo integrado com **notebook + modelo em Simulink**
- Estrutura pronta para **apresentacao academica e tecnica**
- README visual ja preparado para receber resumo, metodologia, resultados e conclusoes

## Fluxo Sugerido

1. Abrir `TCC.ipynb` para revisar a analise numerica e teorica.
2. Abrir `GridTiedInverterOptimalI2.slx` no MATLAB/Simulink para executar o modelo.
3. Comparar os resultados analiticos com as respostas simuladas.

## Estrutura do Projeto

```text
.
|-- assets/
|   `-- banner.svg
|-- GridTiedInverterOptimalI2.slx
|-- TCC.ipynb
|-- .gitignore
`-- README.md
```

## Status

Este repositorio esta na **fase inicial de organizacao**.

A proxima versao do README pode incluir:

- motivacao do projeto;
- hipoteses de modelagem;
- cenarios de teste;
- metricas de estabilidade;
- graficos e capturas de resultado;
- autoria e agradecimentos.

## Observacoes

- Os arquivos tecnicos foram mantidos na raiz por enquanto para evitar quebrar caminhos ja existentes.
- O README foi montado como uma base visual inicial e pode ser refinado assim que voce me passar a descricao final do projeto.
