---
name: machine-inertia
description: Constante H, swing equation, critério das áreas iguais e impacto direto na SRF-PLL — cadeia H↓ → RoCoF↑ → lock-loss observada no Simulink
source: Anderson-Fouad cap.2; teste Simulink TCC 2026-05
---

# Inércia das Máquinas e Impacto na SRF-PLL

## Constante de Inércia H

Fórmula: `H = ½·J·ωs² / S_nom` [s] — tempo que a máquina forneceria potência nominal só com energia cinética.

| Tipo de Gerador | H [s] | Observação |
|---|---|---|
| Turbina a vapor (grande) | 4–9 | Alta velocidade, grande volante |
| Turbina a gás | 2–4 | Menores que vapor |
| Gerador hídrico | 2–4 | Depende do rotor e velocidade |
| Nuclear | 5–7 | Grandes rotores de baixa velocidade |
| IEEE 9-bus G1 | 23,64 | Hidro, 247,5 MVA — H_máq=9,55 s na base própria, convertido para 100 MVA |
| IEEE 9-bus G2 | 6,40  | Vapor, 192 MVA — H_máq=3,33 s na base própria, convertido para 100 MVA |
| IEEE 9-bus G3 | 3,01  | Vapor, 128 MVA — H_máq=2,35 s na base própria, convertido para 100 MVA |
| IBR (solar/eólica) | ≈ 0 | Sem acoplamento eletromecânico |

IBRs não contribuem para H do sistema a menos que emulação de inércia virtual esteja ativa (ver [[virtual-inertia]]).

## Equação de Oscilação (Swing Equation)

```
(2H / ωs) · d²δ/dt² = Pm - Pe = Pa    (potência acelerante)
```

- `M = 2H/ωs` — constante de inércia em [s²/rad]
- Quanto menor H → maior aceleração angular para o mesmo desequilíbrio Pm - Pe
- RoCoF imediatamente após o distúrbio:
  ```
  RoCoF ≈ (fn / 2H) · (ΔP / S_base)   [Hz/s]
  ```

## Critério das Áreas Iguais

Estabilidade transitória exige que a área acelerante (durante o curto) seja compensada
pela área desacelerante (pós-clearance):

```
A1 (acelerante)   = ∫[δ0  → δcl] (Pm - Pe_falta) dδ
A2 (desacelerante)= ∫[δcl → δmax] (Pe_pós - Pm)  dδ

Estável  → A2 ≥ A1   (δcl ≤ δcr)
Instável → δcl > δcr  (rotor ultrapassa o ângulo crítico)
```

Com H baixo: o rotor percorre muito mais ângulo durante o mesmo tempo de falta
→ δcl cresce → maior probabilidade de δcl > δcr → perda de sincronismo.

## Cadeia de Causa e Efeito Observada no Simulink

**Teste:** H de G1/G3 reduzido artificialmente + curto-circuito trifásico (t=0,3 s → t=0,5 s).

```
H ↓
 └→ Oscilação de ângulo ampliada (A1 > A2)
      └→ RoCoF alto após clearance
           └→ SRF-PLL perde sincronismo (erro de fase > 60°)
                └→ Referencial dq corrompido (θ̂ ≠ θ_real)
                     └→ Id, Iq calculados com ângulo errado
                          └→ Pinv → 0  (colapso da injeção)
```

**Resultado observado:** após a eliminação do curto, a potência ativa do inversor vai a
zero em vez de recuperar — mesmo que a tensão da rede volte. O PLL perdeu o lock.

## Varredura Recente de H e Reatância de Curto (2026-05)

**Parâmetros testados:**
- Máquinas síncronas alteradas: **G1 e G3**
- Entrada variada: segundos de inércia `H` das máquinas
- Severidade da falta: reatância de curto entre **2% e 20%** do valor base
- Valor base adotado para a reatância: **529 ohms**
- Faixa absoluta aproximada: `10,58 ohms` a `105,8 ohms`

**Achado principal:** nos testes recentes, qualquer valor de inércia acima de
aproximadamente **0,1 s** nas máquinas G1/G3 foi suficiente para evitar o colapso
total observado no caso de baixíssima inércia.

Interpretação: abaixo desse limiar, o sistema fica muito leve do ponto de vista
eletromecânico. A falta acelera/desacelera os rotores de forma brusca e, depois da
eliminação da contingência, a tensão tenta retornar, mas o ângulo e a frequência
locais variam rápido demais para a SRF-PLL se manter sincronizada.

Esse resultado não deve ser tratado como limite universal de estabilidade. Ele é um
limiar empírico do modelo atual, com a topologia IEEE 9 barras, parametrização atual
do inversor, ganhos atuais do PLL e faixa de reatância de curto testada.

## Por que o PLL Perde Lock?

A SRF-PLL tem largura de banda finita determinada por Kp/Ki:

```
ωn_PLL ≈ √(Ki · U)   [rad/s]
```

Se o RoCoF da rede excede a taxa máxima rastreável pelo laço:
- O integrador do PI acumula erro mais rápido do que o VCO consegue corrigir
- θ̂ (estimado) diverge de θ (real) de forma crescente
- Referencial dq fica desalinhado → Id, Iq computados erroneamente
- O controlador de corrente injeta potência em quadratura com a rede → P_ativa → 0

## Estimativa da Largura de Banda Prática (IEEE 9-bus TCC)

Com os ganhos dimensionados para U = 1 pu, ξ = 0,707:

```
ωn ≈ 2π × 25 rad/s  →  RoCoF máximo rastreável ≈ 25 Hz/s
```

IEEE 1547-2018 limita trip por RoCoF em ±2 Hz/s; o PLL pode perder lock muito antes
do inversor tripar por proteção, caso os ganhos não sejam adequados.

## Relevância para o Evento 15/08/2023 (Brasil)

O teste com H reduzido reproduz exatamente o contexto do apagão:
- Alta penetração de IBRs reduz H efetivo do sistema
- Contingência gera RoCoF alto → PLLs de IBRs perdem lock → IBRs param de injetar
- Ciclo de realimentação: menos injeção → tensão cai → mais IBRs perdem lock → cascata

Ver [[pll-contingencies]] — Cenário 4 (Alto RoCoF) para o trade-off Kp/Ki.
Ver [[lvrt]] para requisitos durante o afundamento que precede o lock-loss.
Ver [[ieee9bus]] para os parâmetros da rede onde o teste foi executado.
Ver [[ons-2-11]] — paradoxo detecção vs. injeção: ONS_2_11 detecta a falta corretamente
mas a injeção falha porque depende de θ̂ que está corrompido quando H é baixo.
Ver [[inertia-estimation]] — como H_sys é medido e por que cai com IBRs.
Ver [[virtual-inertia]] — como inversores grid-forming emulam H para mitigar o problema.
