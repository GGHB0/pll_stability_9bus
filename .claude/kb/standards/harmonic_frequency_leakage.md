---
name: harmonic-frequency-leakage
description: Achado 2026-08-10, corrigido 2026-08-11 — o "2º harmônico" elevado na tabela pré-falta de todo cenário era vazamento espectral por F_FUND_HZ fixo; _measure_f1 (cruzamento de zero, modo abc) elimina quase todo o vazamento nas ordens 3ª/4ª, mas deixa residual na 2ª porque a rede está em chirp contínuo, não só deslocada de 60 Hz — residual é físico, não bug
source: investigação direta em output/results/*/sim_data*.csv (2026-08-10, 2026-08-11)
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

## Correção implementada (2026-08-11)

`src/pipeline/spectrum.py` ganhou `_measure_f1(t, y, fallback=F_FUND_HZ)`:
mede a frequência real por cruzamento de zero ascendente (interpolado
linearmente entre amostras), com fallback pro nominal se houver menos de 3
cruzamentos ou o resultado fugir de 50-70 Hz. `_amplitude_spectrum` e
`_harmonics` ganharam o parâmetro `f1`, usado no truncamento da janela e na
busca do bin — replica o "gating" sincronizado que o IEC 61000-4-7
pressupõe (a norma assume um relógio de amostragem travado na frequência
real da rede; o agrupamento de 3 bins do §4.1 existe pra capturar vazamento
residual *dentro* de uma janela bem sincronizada, não pra compensar uma
janela inteira desalinhada — ver
[harmonic_measurement_conditions.md](harmonic_measurement_conditions.md)).
Escopo: só o modo **abc** (`_mode_fig` só chama `_measure_f1` quando
`mode in ("a","b","c")`); o modo **dq** mantém `F_FUND_HZ` fixo, já que ali
a fundamental vira DC e cruzamento de zero não se aplica. Rótulo da linha
na tabela continua pela **ordem nominal** (ex. "120 Hz" pra 2ª) — o índice
`k` de `_harmonics` não muda, só a frequência usada pra buscar o bin.

### Resultado medido — reduz mas não elimina, e por um motivo físico

Regime, corrente, fase a, `f1` medido = 59,673 Hz (vs. 60,000 Hz nominal):

| h | Antes (60 Hz fixo) | Depois (`f1` medido) |
|---|---|---|
| 2ª | 1,70% | 1,42% |
| 3ª | 0,55% | 0,08% |
| 4ª | 0,46% | 0,15% |

A 3ª/4ª quase zeram — confirma que o realinhamento da janela funciona. A 2ª
só caiu ~17% porque a causa raiz **não é um simples deslocamento de 60,000
para 59,673 Hz**: é um **chirp contínuo** — a frequência ainda está caindo
ao longo de toda a janela de 0,5 s (mesma resposta de droop descrita em "O
achado"). Uma única `f1` (média medida por cruzamento de zero em toda a
janela) alinha o *início e fim* da janela corretamente, mas não cancela o
alargamento espectral causado pela variação de frequência *dentro* da
janela — que é maior perto da fundamental (por isso a 2ª sofre mais que a
3ª/4ª, mais distantes). Confirmado em todos os 26 cenários: pré-falta
sistematicamente 1,3-1,6% (BAD_PLL cai abaixo de 1%, 0,88-1,19%, plausível
por ter ganhos de PLL mais lentos = menos ripple no próprio sinal medido).
**Residual é físico, não bug** — reduzir mais exigiria encurtar a janela
(menos ciclos, menos chirp acumulado) às custas da resolução de 5 Hz que o
IEEE 519-2014 §4.1 pede, uma troca já sinalizada como limitação declarada
em `harmonic_measurement_conditions.md` ("Ainda em aberto").

## Em aberto

Confirmar `f∞≈59,32 Hz` com uma rodada de Regime mais longa (Bruno, ver
[[project_bruno_simulations]]) — o valor atual é extrapolação de uma janela
de 0,6 s com resposta de 1ª ordem ainda em curso, não um dado observado.
