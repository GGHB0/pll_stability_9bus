---
name: machine-inertia
description: Inércia das máquinas síncronas, equação de oscilação, RoCoF e impacto na SRF-PLL — inclui observação experimental do teste Simulink
source: análise do TCC — teste de curto-circuito com H reduzido (2026-05); Anderson-Fouad cap.2
---

# Inércia das Máquinas e Impacto na SRF-PLL

## Constante de Inércia H

```
H = E_cinética_na_velocidade_síncrona / S_nominal   [s]
```

Valores típicos: geradores a vapor 2–9 s, hídro 2–4 s, IBRs → H ≈ 0 (sem inércia física).
No IEEE 9-bus do TCC: G1 H ≈ 23,6 s; G2 H ≈ 6,4 s; G3 H ≈ 3,0 s (Anderson-Fouad).

## Equação de Oscilação (Swing Equation)

```
(2H / ωs) · d²δ/dt² = Pm - Pe = Pa    (potência acelerante)
```

- `M = 2H/ωs` — constante de inércia em [s²/rad]
- Quanto menor H → maior aceleração angular para o mesmo desequilíbrio Pm - Pe
- RoCoF aproximado imediatamente após o distúrbio:
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
→ δcl cresce → maior probabilidade de δcl > δcr → perda de sincronismo das máquinas síncronas.

## Cadeia de Causa e Efeito Observada no Simulink

**Teste:** H de G1/G3 reduzido artificialmente + curto-circuito trifásico aplicado (t=0,3 s)
e eliminado (t=0,5 s).

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

## Por que o PLL Perde Lock?

A SRF-PLL tem largura de banda finita determinada por Kp/Ki:

```
ωn_PLL ≈ √(Ki · U)   [rad/s]
```

Se o RoCoF da rede excede a taxa máxima rastreável pelo laço:
- O integrador do PI acumula erro mais rápido do que o VCO consegue corrigir
- θ̂ (estimado) diverge de θ (real) de forma crescente
- Referencial dq fica desalinhado → componentes Id, Iq computadas erroneamente
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
