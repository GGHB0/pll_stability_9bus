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

Este repositorio reune os materiais de estudo e os artefatos de simulacao usados na analise da **estabilidade de PLL (Phase-Locked Loop) em um sistema eletrico de 9 barras**, com foco em inversores conectados a rede via filtro LCL.

A analise combina:

- calculo analitico da impedancia de Thevenin vista pelo inversor a partir da rede de 9 barras;
- projeto do filtro LCL e dos ganhos do controlador PI de corrente;
- modelagem e simulacao do inversor grid-tied em Simulink.

## Conteudo do Repositorio

| Arquivo | Descricao |
| --- | --- |
| `pll_stability_9bus_analysis.ipynb` | Notebook principal com o fluxo analitico e computacional do estudo. |
| `pll_stability_9bus.slx` | Modelo em Simulink do inversor grid-tied conectado ao sistema de 9 barras. |

## Sistema de 9 Barras

O sistema utilizado e o classico **IEEE 9 barras**, com base de:

- **Tensao de base:** 20 kV
- **Potencia de base:** 100 MVA

### Geradores

| Gerador | MVA | kV | xd (pu) | xd' (pu) |
| --- | --- | --- | --- | --- |
| G1 | 247,5 | 16,5 | 0,1460 | 0,0608 |
| G2 | 192,0 | 18,0 | 0,8958 | 0,1198 |
| G3 | 128,0 | 13,8 | 1,3125 | 0,1813 |

### Topologia

O circuito e formado por 3 geradores, 3 transformadores e 6 linhas de transmissao interligando as 9 barras. As impedancias sao representadas em pu na base do sistema.

## Metodologia

### 1. Montagem da Matriz Ybarra / Zbarra

A partir das impedancias de linha, transformador e geracao, e montada a **matriz de admitancia nodal (Ybarra)** de dimensao 9x9. A **matriz de impedancia nodal (Zbarra)** e obtida pela inversao de Ybarra:

```
Zbarra = inv(Ybarra)
```

### 2. Impedancia de Thevenin

A impedancia de Thevenin vista pela barra de conexao do inversor (Barra 2) e extraida diretamente do elemento diagonal da Zbarra:

```
Z_th = Z22 (em ohms, convertido pela base)
```

Esse valor e usado como parametro de rede no projeto do controlador e na simulacao Simulink.

### 3. Projeto do Filtro LCL

O filtro LCL do inversor e dimensionado com base nos parametros do sistema:

| Parametro | Descricao |
| --- | --- |
| `L1` | Indutor do lado do inversor |
| `L2` | Indutor do lado da rede (razao `k = L2/L1 = 0,0095`) |
| `C1` | Capacitor do filtro |
| `Rd1`, `Rd2`, `Rd3` | Resistores de amortecimento (5% do Z ressonante) |

A frequencia de ressonancia do filtro e calculada por:

```
w_res = sqrt((L1 + L2) / (L1 * L2 * C1))
```

### 4. Ganhos do Controlador PI

Os ganhos do controlador PI de corrente sao calculados em funcao dos parametros do filtro e da frequencia da rede (60 Hz):

```
Kp = 8 * 60 * (L1 + L2 + Lest)
Ki = 32 * 60^2 * (L1 + L2 + Lest)
```

onde `Lest = L1 + L2 + Lg` e a indutancia total estimada vista pelo controlador.

## Fluxo de Trabalho

1. Executar `pll_stability_9bus_analysis.ipynb` para obter a impedancia de Thevenin e os parametros do filtro LCL.
2. Inserir os valores calculados no modelo `pll_stability_9bus.slx` (MATLAB/Simulink).
3. Simular e analisar a estabilidade do PLL sob diferentes condicoes de rede.

## Estrutura do Projeto

```text
.
|-- assets/
|   `-- banner.svg
|-- pll_stability_9bus.slx
|-- pll_stability_9bus_analysis.ipynb
|-- .gitignore
`-- README.md
```
