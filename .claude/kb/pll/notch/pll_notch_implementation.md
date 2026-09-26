---
name: pll-notch-implementation
aliases: [pll-notch-implementation]
description: Notch de 120 Hz no laco do SRF-PLL - testado em 2026-05, removido do modelo final (2026-07) por ser desnecessario. Registro historico da tentativa, nao o estado atual.
source: Conversa tecnica do projeto (2026-05) + arquitetura extraida de pll_stability_9bus.slx
---

# Notch no SRF-PLL - Implementacao Pratica (HISTORICO - removido do modelo)

> **Status atual (2026-07):** este notch foi retirado do `pll_stability_9bus.slx`
> pelo usuario - era de um teste e foi considerado desnecessario. Este arquivo
> documenta a tentativa e o raciocinio de projeto, nao o estado atual do PLL.
> Nao usar como referencia do modelo em vigor. Ver [[pll-loop-filter-gains]].

## Ponto conceitualmente correto

Em falta monofasica-terra, a sequencia negativa aparece no referencial sincrono como
ripple de `2*w0` em `uq`, isto e, `120 Hz` para rede de `60 Hz`.

No SRF-PLL, o notch deve entrar em:

```text
uabc -> abc/dq0 -> uq -> notch(120 Hz) -> PI -> wo -> integrador -> theta
```

Em outras palavras: **entre a componente `q` e o PI do Loop Filter**.

Esse e o ponto certo porque o distubio de `120 Hz` nasce na projecao `dq`. Colocar um
notch simples nas tres fases `abc` antes da Park nao remove o fenomeno correto.

## Formula do notch

Forma geral:

```text
H_notch(s) = (s^2 + 2*zeta_z*wn*s + wn^2) / (s^2 + 2*zeta_p*wn*s + wn^2)
```

Onde:
- `wn = 2*pi*120 rad/s` para sistema de 60 Hz
- `zeta_z` pequeno cria o vale do notch
- `zeta_p` maior define largura e amortecimento

Ponto de partida para estudo:
- `zeta_z = 0.01`
- `zeta_p = 0.15` a `0.30`

Forma simplificada, util para testes:

```text
H_notch(s) = (s^2 + wn^2) / (s^2 + 2*zeta*wn*s + wn^2)
```

## Exemplo MATLAB

```matlab
f_grid  = 60;
f_notch = 2*f_grid;      % 120 Hz
wn      = 2*pi*f_notch;  % rad/s

zeta_z = 0.01;
zeta_p = 0.20;

s = tf('s');
H_notch = (s^2 + 2*zeta_z*wn*s + wn^2) / ...
          (s^2 + 2*zeta_p*wn*s + wn^2);
```

Para implementacao discreta usando a malha de controle do projeto:

```matlab
Tsc = 2e-4;
Hd  = c2d(H_notch, Tsc, 'tustin');
[numd, dend] = tfdata(Hd, 'v');
```

Uso no Simulink:
- `Transfer Fcn` para implementacao continua
- `Discrete Transfer Fcn` com `Sample time = Tsc` para implementacao digital

## Coeficientes discretos validados no projeto

No modelo `pll_stability_9bus.slx`, o notch foi validado com `Tsc = 2e-4 s`,
`f_notch = 120 Hz`, `zeta_z = 0.01` e `zeta_p = 0.20`. Para o bloco
`Discrete Transfer Fcn`, use os coeficientes abaixo:

```matlab
num_notch_d = [0.9723401207349347, -1.9198159829792367, 0.9694285544965067];
den_notch_d = [1.0, -1.9198159829792367, 0.9417686752314415];
```

Configuracao recomendada do bloco:

```text
Numerator:     num_notch_d
Denominator:   den_notch_d
Initial states: [0 0]
Sample time:    Tsc
```

Observacao pratica:
- o campo `Initial states` nao deve receber `Tsc`
- coeficientes no formato `s^2 + a*s + b` precisam ser discretizados antes de
  entrar no `Discrete Transfer Fcn`
- se o bloco estiver em um caminho de controle rapido, manter a implementacao
  em `Discrete Transfer Fcn` evita misturar dinamica continua com amostragem

## Integração no laço e resultados

Posicionamento (dentro do laço vs. por fora), relação com o modelo e resultado
das tentativas de 2026-05 em [[pll-notch-integration]].

## Resumo

- `notch em uq` = reforco do SRF-PLL sem trocar o principio de sincronismo
- `DSOGI/DDSRF` = troca estrutural para lidar melhor com desequilibrio
- em rede de `60 Hz`, o notch deve mirar `120 Hz`
- no projeto, a discretizacao natural e `Tsc = 2e-4 s`
- para `Discrete Transfer Fcn`, `Initial states = [0 0]` e parte da
  configuracao correta, nao um detalhe opcional
