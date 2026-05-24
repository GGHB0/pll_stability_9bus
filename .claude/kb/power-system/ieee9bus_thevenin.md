---
name: ieee9bus-thevenin
description: Cálculo de Ybarra/Zbarra, Thevenin Z22 na Barra 2, Rth/Lth para PLL
---

# IEEE 9-bus — Thevenin na Barra 2

## Objetivo

Calcular a impedância equivalente de Thévenin vista pelo inversor no PAC (Barra 2).
Resultado usado para dimensionar Kp/Ki do PLL SRF e alimentar o InitFcn do .slx.

## Construção da Ybarra

```python
# notebook célula 8 — dados de entrada
entrebarras = [
    (1, 4, 0.0576j),          # trafo
    (2, 7, 0.0625j),          # trafo
    (3, 9, 0.0586j),          # trafo
    (7, 8, 0.0085 + 0.0576j),
    (8, 9, 0.0119 + 0.1008j),
    (7, 5, 0.032  + 0.161j),
    (4, 5, 0.01   + 0.068j),
    (4, 6, 0.017  + 0.092j),
    (9, 6, 0.039  + 0.1738j),
]
impedancias_barra = {1: 0.1184j, 2: 0.1823j, 3: 0.2399j}

# notebook célula 13 — montar_Ybarra()
# Para ramo (i,j,Z): Y[i,i] += 1/Z; Y[j,j] += 1/Z; Y[i,j] -= 1/Z; Y[j,i] -= 1/Z
# Para shunt {k: Zg}: Y[k,k] += 1/Zg
Ybarra = montar_Ybarra(n_barras=9, entrebarras=entrebarras,
                        impedancias_barra=impedancias_barra, retornar='Y')
```

## Inversão e Extração do Z22

```python
Zbarra     = montar_Ybarra(..., retornar='Z')   # inverte via np.linalg.inv internamente
Zbarra_ohm = Zbarra * Z_base                    # Z_base = 4 Ω  (20 kV / 100 MVA)

Z_th = Zbarra_ohm.loc["Barra 2", "Barra 2"]    # elemento diagonal Z22
Rth  = Z_th.real                               # resistência Thevenin [Ω]
Lth  = Z_th.imag / (2 * pi * 60)              # indutância Thevenin [H]
```

## Valores Resultantes (InitFcn do .slx)

```matlab
Rth = 0.010038656529756919   % Ω
Lth = 0.0011601815110534163  % H  →  Xth = 0.4374 Ω @ 60 Hz
```

## Impacto da Divergência Linha 4-5

A linha 4-5 tem X=0.068 no notebook e X≈0.085 no .slx.
Esse ramo liga as Barras 4 e 5 — não está no caminho direto entre a Barra 2 e a rede.
O Thevenin na Barra 2 é dominado por:
1. Trafo 2-7 (X=0.0625 pu, em série direta)
2. Impedâncias dos geradores G1, G3 vistos através da rede

Portanto, o impacto da divergência da linha 4-5 sobre Rth/Lth é secundário.

## Uso nas Plataformas

| Plataforma | Uso do Thevenin |
|------------|----------------|
| **Notebook** | Calcula Z_th → dimensiona Kp/Ki do PLL (células 20-21, 30+) |
| **InitFcn (.slx)** | Rth e Lth carregados como variáveis de workspace → usados em blocos de parâmetro do controlador |
| **PSIM** | Equivalente Thevenin direto (Z_th) → simula dinâmica local VSI/PLL sem rede completa |
| **Simulink** | Rede completa 9-bus com parâmetros físicos → simula propagação real dos afundamentos |

## Relação com o Projeto

O Z22 representa a rigidez da rede vista pelo PLL. Quanto menor Z_th, mais rígida
a rede e mais estável o PLL. Contingências que aumentam Z_th (perda de gerador,
abertura de linha) degradam a estabilidade do PLL — esse é o fenômeno central
investigado no TCC.
