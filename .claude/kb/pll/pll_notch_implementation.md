---
name: pll-notch-implementation
description: Aplicacao pratica de notch em SRF-PLL, ponto de insercao em uq, implementacao MATLAB/Simulink e relacao com o bloco de biblioteca do projeto
source: Conversa tecnica do projeto (2026-05) + arquitetura extraida de pll_stability_9bus.slx
---

# Notch no SRF-PLL - Implementacao Pratica

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

Leitura correta para o projeto: o notch continua válido para curtos assimétricos
moderados; para baixa inércia + contingência severa, a limitação dominante passa a
ser o lock-loss do PLL e não apenas a filtragem da segunda harmônica.

## Resumo

- `notch em uq` = reforco do SRF-PLL sem trocar o principio de sincronismo
- `DSOGI/DDSRF` = troca estrutural para lidar melhor com desequilibrio
- em rede de `60 Hz`, o notch deve mirar `120 Hz`
- no projeto, a discretizacao natural e `Tsc = 2e-4 s`
- para `Discrete Transfer Fcn`, `Initial states = [0 0]` e parte da
  configuracao correta, nao um detalhe opcional
