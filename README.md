# Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos

<p align="center">
  <img src="assets/banner.svg" alt="PLL Stability banner" width="100%">
</p>

<p align="center">
  <img alt="Jupyter Notebook" src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
  <img alt="MATLAB" src="https://img.shields.io/badge/MATLAB-R202x-FF6F00?style=for-the-badge&logo=mathworks&logoColor=white">
  <img alt="Simulink" src="https://img.shields.io/badge/Simulink-Model-FF8C00?style=for-the-badge">
  <img alt="Power Systems" src="https://img.shields.io/badge/Power%20Systems-9%20Bus-0F766E?style=for-the-badge">
</p>

**TCC — Engenharia Elétrica (Sistemas de Potência)**
UERJ — Faculdade de Engenharia | 2025
Autores: Bruno Henrique de Oliveira & Victor Hugo de Avelar Rezende
Orientador: Prof. Dr. Oscar Cuaresma Zevallos | Coorientador: Prof. Dr. Andre Guilherme Peixoto Alves

---

## Motivacao

A perturbacao de **15 de agosto de 2023** no Sistema Interligado Nacional (SIN) resultou no desligamento de **22.547 MW** — cerca de 31% da carga nacional. O Relatorio de Analise de Perturbacao (RAP) do ONS concluiu que o desempenho dos equipamentos de controle de usinas eolicas e fotovoltaicas ficou **aquem do previsto nos modelos matematicos**.

Este trabalho investiga o algoritmo **SRF-PLL** (Synchronous Reference Frame Phase-Locked Loop) como possivel causa central dessa falha, analisando seu comportamento dinamico frente a contingencias severas na rede eletrica.

---

## Objetivo

Analisar o desempenho dinamico e a robustez do SRF-PLL de inversores conectados a rede frente a um espectro de contingencias eletricas, avaliando os impactos sobre o rastreamento de fase, a injecao de potencia e a conformidade com requisitos de LVRT.

---

## Sistema Modelado

### Topologia

- **Inversor:** VSI (Voltage Source Inverter) trifasico de dois niveis
- **Filtro de acoplamento:** LCL (Indutor-Capacitor-Indutor)
- **Rede:** Sistema IEEE de 9 barras (base 20 kV / 100 MVA, 60 Hz)

### Parametros do Filtro LCL

| Parametro | Descricao |
|---|---|
| `L1` | Indutor do lado do inversor |
| `L2` | Indutor do lado da rede |
| `Cf` | Capacitor do filtro |
| `omega_res` | Frequencia de ressonancia: 9068,99 rad/s |
| `xi` | Fator de amortecimento: 0,707 |
| `fs` | Frequencia de chaveamento: 5 kHz |

### SRF-PLL

1. **Detector de Fase** — baseado na componente dq da tensao no PAC
2. **Filtro de Loop** — controlador PI (ganhos `Kp` e `Ki`)
3. **VCO** — Oscilador Controlado por Tensao

### Controle de Corrente

- Referencial sincrono dq — controle desacoplado de P e Q
- Sintonia por cancelamento de polo e zero
- Transformadas de Clarke (αβ) e Park (dq)

---

## Arquitetura do SRF-PLL

> Diagramas em Mermaid (renderizados nativamente pelo GitHub). Fontes editaveis em [`assets/diagrams/`](assets/diagrams/).

### 1. Estrutura do laco com os ganhos do projeto

Detector de fase = transformada de Park; quando `u_q -> 0`, entao `phi_estimado -> phi_real` e `u_d -> U`. Malha de **tipo 2** (integrador no PI + integrador do VCO) → rastreia degraus de frequencia com erro nulo em regime.

```mermaid
flowchart LR
    subgraph REDE["Rede - Barra 2 (IEEE 9)"]
        Vabc["u_abc<br/>20 kV / 60 Hz"]
    end

    subgraph PLL["SRF-PLL (dqo-PLL)"]
        direction LR
        Park["abc -> dqo<br/>Transformada<br/>de Park"]
        Ud["u_d ~ U"]
        Uq(["u_q -> 0"])
        PI["PI<br/>Kp = 8 . fg . (L1+L2+Lest)<br/>Ki = 32 . fg^2 . (L1+L2+Lest)"]
        Som((+))
        Wn["w_n = 2.pi.60"]
        Integ["1/s"]
        Phi["phi_estimado"]
    end

    Vabc --> Park
    Park --> Ud
    Park --> Uq
    Uq --> PI --> Som
    Wn --> Som
    Som -- "w_estimado" --> Integ --> Phi
    Phi -. realimentacao .-> Park

    classDef fb fill:#fff3bf,stroke:#c79c00,color:#000
    classDef io fill:#e7f5ff,stroke:#1971c2,color:#000
    class Phi fb
    class Vabc io
```

**Modelo linear:** `s² + Kp.U.s + Ki.U = 0` → polos por `2.xi.wn` e `wn²/U`.

### 2. Como cada contingencia ataca o laco

```mermaid
flowchart LR
    SagSim["1. Sag simetrico<br/>U cai -> ganho<br/>efetivo cai"]:::c1
    SagAss["2. Sag assimetrico<br/>seq. negativa -><br/>ripple 120 Hz em u_q"]:::c2
    Salto["3. Salto de fase<br/>delta-phi subito >><br/>banda do PLL"]:::c3
    RoCoF["4. Alto RoCoF<br/>dw/dt elevado<br/>(H baixo)"]:::c4

    Vabc["u_abc"] --> Park["Park abc/dqo"]
    Park --> Uq["u_q"] --> PI["PI Kp/Ki"] --> Som((+))
    Wn["w_n"] --> Som --> Integ["1/s"] --> Phi["phi_estimado"]
    Phi -. realimentacao .-> Park

    SagSim -. afeta U .-> Vabc
    SagAss -. injeta seq- em .-> Vabc
    Salto  -. descontinuidade em phi_i .-> Vabc
    RoCoF  -. rampa de w em .-> Vabc

    Saida["I_d, I_q corrompidos<br/>se erro de fase > ~60 graus<br/>=> P_inv -> 0"]:::out
    Phi --> Saida

    classDef c1 fill:#d0ebff,stroke:#1971c2,color:#000
    classDef c2 fill:#ffe0e0,stroke:#c92a2a,color:#000
    classDef c3 fill:#e6fcf5,stroke:#0ca678,color:#000
    classDef c4 fill:#fff4e6,stroke:#e8590c,color:#000
    classDef out fill:#f3f0ff,stroke:#5f3dc4,color:#000
```

### 3. Trade-off central de Kp / Ki (Secao 4.3)

```mermaid
flowchart TB
    Centro(("Ganhos Kp / Ki<br/>do PI"))
    Alto["Kp, Ki <b>altos</b><br/>resposta rapida"]:::a
    Baixo["Kp, Ki <b>baixos</b><br/>imunidade a ruido"]:::b

    Centro --> Alto
    Centro --> Baixo

    Alto -- "bom em" --> R1["3. Salto de fase<br/>4. RoCoF alto"]:::good
    Alto -- "ruim em" --> R2["2. Sag assimetrico<br/>(amplifica 120 Hz)"]:::bad
    Baixo -- "bom em" --> R3["2. Sag assimetrico<br/>(filtra seq-)"]:::good
    Baixo -- "ruim em" --> R4["3. Salto de fase<br/>4. RoCoF alto<br/>(perde lock)"]:::bad

    classDef a fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef b fill:#dbe4ff,stroke:#364fc7,color:#000
    classDef good fill:#e6fcf5,stroke:#087f5b,color:#000
    classDef bad  fill:#ffe3e3,stroke:#c92a2a,color:#000
```

---

## Sistema de 9 Barras

A rede eletrica e representada pelo classico **sistema IEEE de 9 barras**, com 3 geradores sincronos, 3 transformadores e 6 linhas de transmissao.

### Geradores

| Gerador | MVA | kV | xd (pu) | xd' (pu) | xq (pu) |
|---|---|---|---|---|---|
| G1 | 247,5 | 16,5 | 0,1460 | 0,0608 | 0,0969 |
| G2 | 192,0 | 18,0 | 0,8958 | 0,1198 | 0,8645 |
| G3 | 128,0 | 13,8 | 1,3125 | 0,1813 | 1,2578 |

### Impedancia de Thevenin

A impedancia equivalente de Thevenin vista pelo inversor na barra de conexao e calculada a partir do elemento diagonal da **matriz de impedancia nodal (Zbarra)**:

```
Zbarra = inv(Ybarra)
Z_th = Z_ii  (barra de conexao do inversor)
```

Esse valor e usado como parametro de rede no dimensionamento do filtro e no projeto do controlador.

---

## Cenarios de Contingencia

| Cenario | Descricao |
|---|---|
| Afundamento simetrico | Falta trifasica — reducao de amplitude sem sequencia negativa |
| Afundamento assimetrico | Introduz sequencia negativa — gera oscilacoes de 2a harmonica no PLL |
| Salto de fase (Phase-Angle Jump) | Mudanca abrupta de fase — pode causar perda de sincronismo |
| Alta RoCoF | Elevada taxa de variacao de frequencia — desafio ao rastreamento |

---

## Metricas de Desempenho

- **IAE** — Integral do Erro Absoluto do angulo de fase
- **ISE** — Integral do Erro Quadratico do angulo de fase
- **Tempo de acomodacao** do erro de fase
- Oscilacoes de potencia ativa e reativa durante a contingencia
- Conformidade com **LVRT** (IEEE 1547-2018)

---

## Metodologia

1. **Modelagem da rede** — montagem da Ybarra/Zbarra e calculo da impedancia de Thevenin
2. **Dimensionamento do filtro LCL** — calculo de L1, L2, Cf e resistores de amortecimento
3. **Projeto dos controladores** — ganhos Kp e Ki do PLL e do controlador de corrente
4. **Simulacao EMT** — execucao dos cenarios de contingencia no Simulink
5. **Analise de resultados** — IAE, ISE, tempo de acomodacao e conformidade LVRT

---

## Conteudo do Repositorio

| Arquivo | Descricao |
|---|---|
| `pll_stability_9bus_analysis.ipynb` | Calculo analitico: Ybarra/Zbarra, Thevenin, filtro LCL e ganhos do controlador |
| `pll_stability_9bus.slx` | Modelo Simulink do inversor grid-tied com SRF-PLL no sistema de 9 barras |

---

## Ferramentas

- **MATLAB/Simulink** — simulacao EMT e analise de sistemas de controle
- **PSIM** — eletronica de potencia, harmonicos e transitorios
- **Python / Jupyter** — calculo analitico de parametros

---

## Referencias

- YAZDANI, A.; IRAVANI, R. *Voltage-Sourced Converters in Power Systems*. Wiley, 2010.
- TEODORESCU, R.; LISERRE, M.; RODRIGUEZ, P. *Grid Converters for Photovoltaic and Wind Power Systems*. Wiley, 2011.
- BOLLEN, M. H. J. *Understanding Power Quality Problems*. IEEE Press, 2000.
- IEEE Std 1547-2018 — *Interconnection and Interoperability of Distributed Energy Resources*
- ONS — *Relatorio de Analise de Perturbacao (RAP) — 15/08/2023*
