---
name: harmonic-frequency-leakage
description: Achado 2026-08-10 — o "2º harmônico" elevado na tabela pré-falta de todo cenário é vazamento espectral, não distorção real; a rede simulada nunca fecha em 60,000 Hz exatos (ainda em resposta primária de droop) e a FFT trunca a janela assumindo F_FUND_HZ=60 fixo
source: investigação direta em output/results/*/sim_data*.csv (2026-08-10)
metadata:
  type: reference
---

# Vazamento espectral por desvio de frequência — achado 2026-08-10

Continuação de [harmonic_measurement_conditions.md](harmonic_measurement_conditions.md)
("Ainda em aberto"). Disparado por uma observação do usuário: o limite de
1,0% pra 2ª harmônica (`CURR_EVEN_LIMITS_PU[2]`) parecia baixo demais frente
aos 1,3%-2,1% que a tabela da Regime mostrava.

## O achado

A "2ª harmônica" elevada que aparece na coluna pré-falta/Regime de **todo**
cenário testado **não é distorção real do inversor** — é vazamento
espectral por dois fatores combinados:

1. **A rede simulada nunca fecha em 60,000 Hz exatos.** Frequência
   instantânea (cruzamento de zero em `ang_g1_rad`/corrente de fase) parte
   de ~59,88 Hz e continua caindo até o fim dos 0,6 s de simulação
   (~59,45-59,70 Hz, variando por cenário). Ajuste exponencial
   `f(t)=f∞+A·e^(-t/τ)` na Regime: **f∞≈59,32 Hz, τ≈0,48 s** — valor
   **extrapolado**, não observado (a simulação não roda tempo suficiente
   pra confirmar). Consistente com resposta primária de droop dos
   geradores síncronos G1/G3 sem AGC fechando o balanço P depois que G2 foi
   substituído pelo inversor (fonte de corrente, não participa de
   regulação de frequência).
2. `_amplitude_spectrum` (`spectrum.py`) trunca a janela da FFT assumindo
   `F_FUND_HZ=60.0` **fixo**, não a frequência real do segmento. Com a rede
   em ~59,67 Hz em vez de 60,000 Hz, a janela não fecha em um número
   inteiro de ciclos do sinal real — vazamento clássico de janela
   retangular desalinhada da fundamental.

## Evidência

Reproduzido com um **tom sintético puro** (seno de 59,67337 Hz, zero
harmônico real) processado pela mesma lógica de janela do código:

| h | Sintético (tom puro, zero distorção) | Observado no dashboard (Regime) |
|---|---|---|
| 2ª | 0,00976 | 0,0135-0,0209 |
| 3ª | 0,00526 | 0,0055-0,0067 |
| 4ª | 0,00369 | ~0,0032 |

A ordem de grandeza bate — o "harmônico" reportado é majoritariamente
vazamento da fundamental, não conteúdo real de alta ordem. O espectro de
0-600 Hz confirma: em vez de um pico isolado em 120 Hz, há um piso
decrescente suave a partir de 60 Hz, não a assinatura de um harmônico
discreto.

**É sistêmico, não pontual da Regime.** A mesma medição de frequência em
5 cenários de falta (bus4/1phase, bus4/3phase, bus6/3phase, bus9/1phase,
line7_8/3phase) mostra trajetória pré-falta **idêntica** (59,88→59,71 Hz em
0,1-0,3 s) — esperado, já que todos partem da mesma condição inicial antes
da falta diferenciá-los — e a mesma "2ª harmônica fantasma" recalculada
direto do CSV bate com a Regime (ex.: bus4/1phase 1,32%/1,88%/1,39% nas
fases a/b/c; bus9/1phase 1,54%/1,85%/1,50%). Toda célula de 2ª (e, em menor
grau, 4ª) harmônica na coluna pré-falta de qualquer cenário com
`sim_data_abc.csv` está inflada pelo mesmo efeito.

## Correção proposta (aprovada pelo usuário 2026-08-10, pendente de implementação)

Medir a frequência real do segmento (cruzamento de zero no próprio sinal
sendo analisado, com fallback pra `F_FUND_HZ` nominal se o sinal não tiver
cruzamentos suficientes ou a frequência medida fugir de uma faixa sã, ex.
50-70 Hz) e truncar a janela por essa frequência medida em vez de 60 Hz
fixo — replica o "gating" sincronizado que o IEC 61000-4-7 pressupõe (a
norma assume um relógio de amostragem travado na frequência real da rede;
o agrupamento de 3 bins do §4.1 existe pra capturar vazamento residual
*dentro* de uma janela bem sincronizada, não pra compensar uma janela
inteira desalinhada — ver
[harmonic_measurement_conditions.md](harmonic_measurement_conditions.md)).
Escopo: só o modo **abc** (onde a fundamental realmente oscila em ~60 Hz);
o modo **dq** mantém `F_FUND_HZ` fixo, já que ali a fundamental vira DC e
cruzamento de zero não se aplica. Rótulo da linha na tabela continua pela
**ordem nominal** (ex. "120 Hz" pra 2ª), só a janela de busca do bin se
desloca pra perto da frequência medida.

## Em aberto

Confirmar `f∞≈59,32 Hz` com uma rodada de Regime mais longa (Bruno, ver
[[project_bruno_simulations]]) — o valor atual é extrapolação de uma janela
de 0,6 s com resposta de 1ª ordem ainda em curso, não um dado observado.
