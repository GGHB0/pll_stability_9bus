---
name: pll-phase-jump-fault-inception
aliases: [pll-phase-jump-fault-inception]
description: Por que o primeiro ciclo da falta fica fora do pico do erro de fase — salto de fase da tensão (Bollen §4.5) e oscilação do fasor no início do afundamento, mais rápidos que o SRF-PLL; fundamentação do §543 (comentário #131 do Oscar)
source: IEEE 1547-2018 §6.5.2.6 p.58; Bollen 2000 §4.2 p.142, §4.5 p.198-199, §4.7.1 p.231, §4.8 p.239, §5.4.4 p.312; Fan-Wang-Miao 2024 §III p.369-370 eq.(6) Fig.4; scripts/medir_salto_fase.py
references:
  - "IEEE. IEEE Std 1547-2018: IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. New York: IEEE, 2018."
  - "BOLLEN, Math H. J. Understanding Power Quality Problems: Voltage Sags and Interruptions. New York: IEEE Press; Hoboken: John Wiley & Sons, 2000. (IEEE Press Series on Power Engineering). ISBN 0-7803-4713-7."
  - "FAN, Lingling; WANG, Zhengyu; MIAO, Zhixin. Large Angle Deviation in Grid-Following IBRs Upon Grid Voltage Dip. IEEE Transactions on Energy Conversion, v. 39, n. 1, p. 368-378, mar. 2024. DOI: 10.1109/TEC.2023.3302812."
---

# Salto de Fase no Início da Falta e o Primeiro Ciclo do Erro de Fase

O pico do erro de fase do Cap. 5 é medido de `t_falta + 1 ciclo` até a
eliminação (receita em [[tcc-revisao-fragmento-cap5-metricas]]). O TCC
justificava o recorte como "transitório de comutação", e o Oscar pediu
referência (comentário #131, §543, 11/10/2026). Este doc reúne a base.

## O termo: a literatura não diz "transitório de comutação"

- Nenhum dos textos extraídos da bibliografia (tese do André, Alves 2020,
  Yazdani, Teodorescu, ONS 2.10/2.11, IEEE 1547) usa o termo para a aplicação
  de falta. "Comutação" aparece como chaveamento do conversor (Yazdani,
  "modelo com comutação") ou falha de comutação de HVDC (ONS).
- O Bollen usa *commutation transients (notches)* para o entalhe de
  retificadores controlados durante o afundamento (§4.8, p.239), outra coisa.
- O nome do fenômeno é **salto de fase** (*phase-angle jump*, Bollen §4.5).
  A IEEE 1547-2018 §6.5.2.6 (p.58) fala em *voltage phase angle changes*: DER
  trifásico deve suportar salto de sequência positiva de até 20° "within a
  sub-cycle-to-cycle time frame" (60° por fase; monofásico, 60°), com
  oscilação amortecida ou cessação momentânea de até 0,5 s aceitas. A IEEE
  1547.2-2023 §6.2.1.5.8 chama de *voltage phase angle jump/vector shift*.

## O que o Bollen sustenta (páginas impressas = página do PDF − 16)

| Onde | O que diz |
|---|---|
| §4.5, p.198 | "A short circuit [...] not only causes a drop in voltage magnitude but also a change in the phase angle of the voltage. [...] the phase-angle jump associated with the voltage sag." Na falta trifásica, vem da diferença de X/R entre fonte e alimentador. |
| §4.5.1, p.199 | O salto se mede comparando a fase durante a falta com a pré-falta, por demodulação `vd`/`vq` com média de meio ou um ciclo. A transição tem *overshoot* de fase; janela maior deixa a transição mais lenta e o *overshoot* menor. |
| §4.2, p.142 | O rms em janela de um ciclo "takes one cycle for the transition"; janela menor que meio ciclo não serve. |
| §4.7.1, p.231 | Magnitude e salto de fase são grandezas da componente fundamental e exigem cálculo sobre meio ciclo ou mais; o instante de início do afundamento pede outra técnica. |
| §5.4.4, p.312 | O instante de disparo vem da saída do PLL, "which takes at least several cycles to react to the phase-angle jump". PLL mais rápido fica mais sensível a harmônicos. |

## O que o Fan et al. (2024) acrescenta

Artigo sobre o evento de Odessa (Texas, 2021), PLL em inversor GFL. §III,
p.369-370: o afundamento "results in an immediate phase angle jump for the
PCC bus voltage" (eq. 6: `Δθ = atan(ΔVg·sinθPCC / (V − ΔVg·cosθPCC))`). Na
Fig. 4(b), com `Xg = 0,35 pu`, o ângulo do PCC salta mais de 10° em menos de
10 ms, e o PLL só atinge o máximo em 50 ms; com `Xg = 0,05 pu` o salto fica
abaixo de 5°. Não está na lista de referências do TCC (em 12/10/2026).

## O que os dados do modelo mostram

`scripts/medir_salto_fase.py`, faltas trifásicas com sintonia nominal (os
quatro cenários da Figura 5.7). Fase da tensão tirada direto das tensões abc
do inversor, sem passar pelo PLL.

| Cenário | Salto sustentado (ciclos 2-5) | Fase da tensão no 1º ciclo | \|v\| no 1º ciclo | Fase do PLL no 1º ciclo | Erro 1º ciclo | Erro depois |
|---|---|---|---|---|---|---|
| Barra 7 | −118,5° | −98,9° a +138,0° | 0,00 a 0,82 pu | −57,6° a +7,8° | 135,8° | 37,3° |
| Linha 7-8 | −90,1° | −87,6° a +137,1° | 0,02 a 1,01 pu | −54,0° a +9,3° | 132,7° | 32,5° |
| Linha 8-9 | −20,8° | −41,8° a +66,9° | 0,25 a 1,02 pu | −29,9° a +21,5° | 56,4° | 29,8° |
| Barra 6 | −2,9° | −23,9° a +45,3° | 0,47 a 1,01 pu | −11,6° a +19,5° | 40,1° | 7,3° |

"Erro depois" é o pico da Tabela 5.1 do TCC (bate com o texto).

Leitura:

1. **Dois efeitos somados no 1º ciclo.** O salto sustentado do Bollen (grande
   perto do inversor, quase nulo na Barra 6) e uma oscilação do fasor de
   tensão em fase e amplitude, que ultrapassa o valor final e se amortece em
   cerca de um ciclo. Em `bus6/3phase`, a fase vai a +44,9° em 2 ms e a
   −20,4° em 6 ms, e está em −0,3° aos 16,7 ms; o desvio do |v| cai de 0,120
   no 1º ciclo para 0,045 no 2º.
2. **O PLL não acompanha nesse intervalo.** Aos 2 ms, a tensão está em +44,9°
   e o PLL em +4,5° (erro de 40,1°). O pico do 1º ciclo mede a tensão mudando
   mais depressa que o laço, não o rastreamento: é o que o Bollen (§5.4.4) e o
   Fan (Fig. 4b) descrevem.
3. **Um ciclo é a janela natural.** As grandezas de fundamental só se definem
   com janela de meio ciclo ou mais, e a transição de um afundamento ocupa
   cerca de um ciclo (Bollen §4.2, §4.7.1). A sintonia nominal do PLL
   (`ts` = 20 ms, [[pll-loop-filter-gains]]) também fica nessa escala.

Os saltos sustentados de −118,5°, −90,1° e −20,8° passam do limite de 20°
da IEEE 1547-2018 §6.5.2.6; só a Barra 6 fica dentro. Dado de KB, ainda fora
do texto do TCC.

**Ressalva:** na Barra 7 e na Linha 7-8 o |v| chega a ~0 pu no 1º ciclo, e a
fase de um vetor quase nulo é mal condicionada. Os ângulos dessas duas linhas
servem como ordem de grandeza, não como valor exato.

## Uso no TCC (§543, comentário #131)

Aplicado em 12/10/2026 (só BOLLEN, 2000, que já estava nas referências; Fan
et al. ficou de fora por decisão do Victor): "O primeiro ciclo após a
aplicação da falta, sombreado, corresponde ao salto de fase que o
curto-circuito impõe à tensão, ao qual o SRF-PLL só responde com atraso
(BOLLEN, 2000), e fica fora da medição do pico". Entrega em
[[tcc-historico-entregas]].

## Relacionados

- [[pll-contingencies]] — cenários de falta e métricas do SRF-PLL
- [[tcc-revisao-fragmento-cap5-metricas]] — receita do pico com o 1º ciclo descartado
- [[pll-cycle-slip-measurement]] — outra medição sobre `vd`/`vq` e ângulos gravados
