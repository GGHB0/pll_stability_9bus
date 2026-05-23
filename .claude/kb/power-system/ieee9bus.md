---
name: ieee9bus
description: Sistema IEEE 9 barras modificado — topologia, parâmetros, Thevenin na Barra 2
source: pll_stability_9bus_analysis.ipynb; TCCs V8 cap.3.2.1
---

# Sistema IEEE 9 Barras — Modelo do Projeto

## Topologia e Adaptação

Benchmark Anderson-Fouad. Adaptação para o TCC:
- **G2 (Barra 2) substituído pelo VSI** → sistema híbrido: G1, G3 síncronos + IBR na Barra 2
- G1 → Barra 1 (via trafo 1-4), G3 → Barra 3 (via trafo 3-9)
- Cargas nas Barras 5, 6, 8

## Base do Sistema

```
V_base = 20 kV    S_base = 100 MVA    Z_base = 4 Ω    f = 60 Hz
```

## Impedâncias de Ramos (p.u.)

| De | Para | Z (p.u.) |
|----|------|----------|
| 1  | 4    | j0.0576 (trafo) |
| 2  | 7    | j0.0625 (trafo) |
| 3  | 9    | j0.0586 (trafo) |
| 7  | 8    | 0.0085 + j0.0576 |
| 8  | 9    | 0.0119 + j0.1008 |
| 7  | 5    | 0.032 + j0.161 |
| 4  | 5    | 0.01 + j0.068 |
| 4  | 6    | 0.017 + j0.092 |
| 9  | 6    | 0.039 + j0.1738 |

## Impedâncias de Geração (shunt nas barras, p.u.)

| Barra | Zg (p.u.) |
|-------|-----------|
| 1     | j0.1184 |
| 2     | j0.1823 |
| 3     | j0.2399 |

## Matriz Ybarra e Thevenin

```python
# Construção via montar_Ybarra() — notebook célula 13
Ybarra = montar_Ybarra(n_barras=9, entrebarras=..., impedancias_barra=..., retornar='Y')
Zbarra = montar_Ybarra(..., retornar='Z')          # inverte internamente via np.linalg.inv
Zbarra_ohm = Zbarra * Z_base                        # converte para ohms

# Thevenin na Barra 2 (ponto de conexão do VSI)
Z_th = Zbarra_ohm.loc["Barra 2", "Barra 2"]        # elemento diagonal Z22
Rth  = Z_th.real
Lth  = Z_th.imag / (2 * pi * 60)
```

Z22 representa a impedância vista pelo inversor no PAC — usada para dimensionar o equivalente
de Thévenin no PSIM (simulações de estágio de potência isolado).

## Uso Dual das Plataformas

- **PSIM:** usa apenas o equivalente Thevenin (Z_th) → foco na dinâmica local do VSI/PLL
- **MATLAB/Simulink:** rede completa 9 barras → simula propagação real dos afundamentos
  de tensão desde o ponto de falta até o PAC (Barra 2)
