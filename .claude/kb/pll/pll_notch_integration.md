---
name: pll-notch-integration
description: Onde o notch de 120 Hz entraria no SRF-PLL (dentro do laço vs. por fora), relação com o modelo do projeto e resultado das tentativas de 2026-05 (HISTÓRICO, removido do modelo)
aliases: [pll-notch-integration]
source: Conversa tecnica do projeto (2026-05) + arquitetura extraida de pll_stability_9bus.slx
---

# Notch no SRF-PLL - Integração e Resultados (HISTÓRICO)

Continuação de [[pll-notch-implementation]] (fórmula, exemplo MATLAB e coeficientes discretos).
Contexto do laço em [[pll-loop-filter-gains]] e [[srf-pll-theory]].

## Como seria dentro do PLL

Se o PLL estiver aberto em blocos:

```text
abc
 -> Park Transform
 -> Selector/Demux da componente q
 -> Discrete Transfer Fcn (notch 120 Hz)
 -> PI
 -> soma com w0 = 2*pi*60
 -> Discrete-Time Integrator
 -> theta
```

Blocos Simulink tipicos:
- `Park Transform`
- `Selector` ou `Demux`
- `Discrete Transfer Fcn`
- `Discrete PID Controller` em modo PI, ou `Gain + Discrete-Time Integrator`
- `Sum`
- `Discrete-Time Integrator`
- `Constant`

## Como seria "por fora"

Se o PLL estiver encapsulado em bloco pronto, ha duas leituras corretas para "por fora":

1. Substituir o bloco pronto por um subsistema proprio, reproduzindo:

```text
Park -> uq -> notch -> PI -> VCO
```

2. Fazer pre-processamento da medicao com separacao de sequencia positiva:
- `DSOGI`
- `DDSRF`

O que **nao** e recomendado:
- notch simples de `120 Hz` nas tres fases `abc`
- filtrar apenas `mag`
- filtrar `theta` depois do VCO como solucao principal

## Relacao com o modelo do projeto

No projeto `pll_stability_9bus.slx`, o PLL atual esta no subsistema:

```text
UFV Model / Optimal controller / Sinusoidal Measurement (PLL, Three-Phase)
```

Pela inspecao do bloco interno, a cadeia e:

```text
abc -> abc/dq0 -> seletor do eixo q -> Loop Filter (PI) -> VCO -> theta
```

Saidas expostas:
- `freq`
- `angle`
- `mag`

Parametros internos observados:
- `Kp_LF = 460`
- `Ki_LF = 105820`
- `F0 = 60`
 - o bloco de notch discreto deve ser alimentado com `num_notch_d` e `den_notch_d`
   vindos do `params.m`, nao com coeficientes de dominio `s`

Se esse bloco fosse reimplementado de forma aberta no `Optimal controller`, o notch
entraria exatamente entre o seletor do eixo `q` e o PI do `Loop Filter`.

## Resultado das tentativas recentes (2026-05)

Foram testadas mudanças de filtragem para reduzir a influência das variáveis de
`120 Hz` na leitura do PLL durante curtos assimétricos. A hipótese era que um novo
filtro notch, ajustado para `2*f0`, poderia impedir que a sequência negativa
contaminasse `uq`, `theta`, `Id` e `Iq`.

**Resultado prático:** as tentativas não foram bem sucedidas para os colapsos mais
severos de baixa inércia. O notch ajuda a explicar e atacar o ripple de `120 Hz`,
mas não resolve a perda de referência quando a dinâmica eletromecânica pós-falta
leva o PLL para fora da sua região de captura.

Decisão final (2026-07): removido do modelo — ver status no topo do arquivo.

