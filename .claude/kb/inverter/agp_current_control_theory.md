---
name: agp-current-control-theory
description: Fundamentação teórica de controle de corrente do VSC (plantas RL/LCL, cancelamento polo-zero, amortecimento ativo) — Cap.3 da tese do coorientador AGP, segunda fonte para o Cap.3 do TCC ao lado de Yazdani
source: TeseAGP.pdf (Alves, A.G.P., COPPE/UFRJ, 2022), Cap.3 "Fundamentação Teórica", p.61-101
---

# Fundamentação Teórica de Controle de Corrente — TeseAGP Cap. 3

Segunda fonte teórica pedida pelo professor para o Cap. 3 do TCC (ao lado do
Yazdani, ver [[vsc-topology-and-transforms]] e [[vsc-reference]]). A tese do
coorientador André G. P. Alves ("Metodologia para Auto-Ajuste de
Controladores de Corrente em Conversores Fonte de Tensão Conectados a Redes
Sujeitas a Distúrbios Harmônicos") tem seu próprio Cap. 3 de fundamentação
teórica — cobre exatamente o par planta RL/LCL + projeto de controlador de
corrente que já embasa a metodologia de ganhos do projeto
([[pll-gains-methodology]], [[lcl-filter]]), mas aqui na forma de derivação
teórica completa, útil para citar diretamente na seção 3.1/3.3 do TCC.

> **Nota de precisão bibliográfica:** as equações de projeto (cancelamento
> polo-zero) estão nas páginas 61-65 do PDF, numeradas (3.10)-(3.14) no
> texto da tese — não (3.21)-(3.22) como registrado em
> [[pll-gains-methodology]] (citação a corrigir numa próxima revisão desse
> arquivo; o conteúdo e a fórmula batem, só o número da equação/página
> estava impreciso).

## Planta RL (§3.1) — equivalente monofásico

```
vinv − vg = (R1+R2)·iL + (L1+L2)·diL/dt
```

Função de transferência corrente/tensão do inversor:
```
IL(s)/Vinv(s) = [1/(L1+L2)] / [s + (R1+R2)/(L1+L2)]
```
— 1ª ordem, polo estável, projeto de controlador simples.

### Passagem para abc→dq (eqs. 3.4-3.9)

Mesma técnica de fasor espacial do Yazdani ([[vsc-topology-and-transforms]]):
multiplicar as 3 equações de fase por `e^(j0)`, `e^(j2π/3)`, `e^(-j2π/3)` e
somar. Resultado em dq (separando parte real/imaginária):

```
vd,inv − vd,g = (R1+R2)·id + (L1+L2)·did/dt − ω(L1+L2)·iq
vq,inv − vq,g = (R1+R2)·iq + (L1+L2)·diq/dt + ω(L1+L2)·id
```

Termos cruzados `ω(L1+L2)` — mesmo acoplamento discutido em [[vsc-reference]]
(eqs. 8.45-8.46 do Yazdani) — removidos por técnica de desacoplamento
(feedforward), deixando cada eixo como planta de 1ª ordem independente.

### Projeto por cancelamento polo-zero (eqs. 3.10-3.14)

Compensador PI, zero cancela o polo da planta:
```
Ki/Kp = (R1+R2)/(L1+L2)
```

Malha fechada resultante (1ª ordem, ganho unitário):
```
Id(s)/Id*(s) = 1 / [((L1+L2)/Kp)·s + 1]
```

Critério de acomodação em ~1 período de rede (`tss = 1/fg`, critério 2%):
```
Kp = 4·fg·(L1+L2)
Ki = 4·fg·(R1+R2)
ωB = 4·fg   (banda passante de malha fechada)
```

Esta é **a mesma estrutura funcional** (`Kp = k·fg·L`) usada no projeto para
os ganhos do bloco de sincronismo — ver [[pll-gains-methodology]], que
aplica a mesma lógica de cancelamento polo-zero (ali com fator 8 em vez de
4, e usando `Lest` em vez de `L1+L2` isolado) para dimensionar o PI do PLL,
não apenas o do controlador de corrente. Útil para o TCC explicitar, na
seção 3.1/3.3, que a técnica de cancelamento polo-zero é comum a ambas as
malhas (corrente e sincronismo) por compartilharem a mesma planta
equivalente (indutância série).

## Planta LCL (§3.2) — modelo em espaço de estados

```
vinv − vC1 = L1·diL1/dt
vC1 − vg   = L2·diL2/dt
iC1        = C1·dvC1/dt
iL1 = iL2 + iC1
```

Variáveis de estado `[iL1, iL2, vC1]`, entrada `vinv`, perturbação `vg`:
```
ẋ = A·x + B·vinv + E·vg
```
com `A` contendo os termos de acoplamento `1/L1`, `1/L2`, `1/C1` entre os
três estados — modelo de 3ª ordem, mais complexo que o RL de 1ª ordem, com
frequência de ressonância própria (mesmo fenômeno dimensionado no projeto
via [[lcl-filter]], `ω_res`).

## Estratégias de Amortecimento (§3.3-3.4)

A planta LCL tem polos complexos pouco amortecidos na frequência de
ressonância — malha de corrente simples (realimentando só `iL2`, a corrente
de saída para a rede) pode ser instável. A tese trata 4 estratégias de
**amortecimento ativo** (via realimentação de sinais internos do filtro) e
uma de **amortecimento passivo**:

| Estratégia | Mecanismo |
|---|---|
| Filtro Notch | Atenua a banda estreita ao redor de `ω_res` no laço de controle |
| Realimentação de `iC1` | Corrente do capacitor como sinal extra de amortecimento |
| Filtragem derivativa de `vC1` | Derivada da tensão do capacitor injetada na malha |
| Realimentação de `iL2` com compensação | Variante direta na corrente de saída |
| Amortecimento passivo (`Rd` série com `C1`) | Resistor físico em série com o capacitor — dissipa energia na ressonância, sem necessidade de sensor extra, mas com perda de eficiência |

Conclusão da tese (§3.6): PI simples é suficiente para planta RL; planta
LCL **exige** amortecimento (ativo ou passivo) para estabilidade; o atraso
de processamento do VSC reduz a margem de fase disponível em ambos os
casos — ponto relevante para o TCC ao discutir por que o SRF-PLL (mais um
laço com atraso equivalente) é sensível a más sintonias sob contingência.

## Uso no TCC

Fonte teórica primária e mais alinhada à metodologia real do projeto
(mesmo autor da metodologia de ganhos já usada) — complementa Yazdani com
uma derivação equivalente, em português, e com a mesma notação (`id, iq, ω`)
usada no restante do TCC. Reforça a seção 3.1 (transformadas aplicadas ao
modelo RL/LCL) e 3.3 (arquitetura de controle em cascata, malha de
corrente) com uma segunda fonte independente que corrobora a técnica de
cancelamento polo-zero também usada no SRF-PLL do projeto.
