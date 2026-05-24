---
name: pll-contingencies
description: Os 4 cenários de contingência simulados, efeitos no SRF-PLL e métricas de avaliação
source: TCCs V8 cap.2.4, cap.4 (estrutura); pll_stability_9bus.slx
---

# Contingências e Métricas de Avaliação

## Os 4 Cenários de Contingência

### 1. Afundamento de Tensão Simétrico
- **Causa:** Falta trifásica distante
- **Efeito na tensão:** Redução de amplitude (0,1–0,9 p.u.), sem desequilíbrio
- **Efeito no PLL:** Detector de fase recebe sinal enfraquecido → ganho efetivo da malha cai (depende de U)
- **Análise:** Sem sequência negativa; comportamento mais previsível; avalia resposta em amplitude

### 2. Afundamento de Tensão Assimétrico
- **Causa:** Falta monofásica ou bifásica
- **Efeito na tensão:** Desequilíbrio entre fases → introduz componente de **sequência negativa**
- **Efeito no PLL:** Sequência negativa gira em sentido oposto ao referencial dq
  → aparece como oscilação de **2ª harmônica (120 Hz)** em vq
  → PLL propaga o erro → P e Q oscilam no dobro da frequência
- **Esta é a limitação central do SRF-PLL padrão** (não filtra sequência negativa)

### 3. Salto de Fase (Phase-Angle Jump)
- **Causa:** Mudança abrupta de topologia da rede (chaveamento de falta, reconexão)
- **Efeito na tensão:** Descontinuidade angular súbita no ângulo de fase
- **Efeito no PLL:** O PLL tem largura de banda finita; um salto grande e instantâneo pode superar
  a capacidade de rastreamento → perda de lock
- **Resultado extremo:** Inversor perde sincronismo e precisa ser desconectado

### 4. Alto RoCoF (Rate of Change of Frequency)
- **Causa:** Perda súbita de geração inercial; alta penetração de IBRs
- **Efeito na tensão:** Frequência varia rapidamente (dω/dt elevado)
- **Efeito no PLL:** Malha tipo 2 rastreia rampas de frequência com erro nulo em regime permanente,
  mas a resposta transitória depende dos ganhos Kp/Ki → trade-off velocidade vs. ruído
- **Contexto:** Problema sistêmico ligado à redução de inércia por IBRs (motivação do evento 15/08/2023)

#### Observação Experimental — Teste com H Reduzido (Simulink, 2026-05)
- **Setup:** H das máquinas G1/G3 reduzido artificialmente + curto-circuito trifásico aplicado e eliminado
- **Resultado:** após eliminação do curto, `Pinv → 0` — inversor para de injetar mesmo com a rede restaurada
- **Mecanismo passo a passo:**
  1. H baixo → rotores de G1/G3 oscilam com amplitude muito maior (swing eq.: `M = 2H/ωs`)
  2. Após clearance → RoCoF excede a largura de banda da SRF-PLL
  3. Erro de fase PLL > 60° → estimativa θ̂ diverge de θ_real de forma crescente
  4. Referencial dq corrompido → Id e Iq calculados com ângulo errado
  5. Controlador injeta corrente em quadratura com a rede → P_ativa efetiva → 0
- **Ligação com critério das áreas iguais:** com H baixo, o rotor ultrapassa o ângulo crítico
  δ_cr durante o curto → área acelerante > desacelerante → máquinas perdem sincronismo
  → tensão na Barra 2 torna-se caótica do ponto de vista da SRF-PLL
- Ver [[machine-inertia]] para as equações e análise detalhada

## Métricas de Avaliação de Desempenho

```
IAE  = ∫|θ_erro(t)| dt        — Integral do Erro Absoluto (ângulo de fase)
ISE  = ∫ θ_erro²(t) dt        — Integral do Erro Quadrático
ts                             — Tempo de acomodação do erro de fase
ΔP, ΔQ                        — Amplitude das oscilações de potência ativa e reativa
LVRT                           — Conformidade com IEEE 1547-2018 (curva V×t)
```

## Requisito LVRT (IEEE 1547-2018)

- Inversor não deve desconectar durante afundamento se o evento estiver dentro da curva V×t
- Durante o afundamento: deve injetar corrente reativa para suporte de tensão
- **Condição de conformidade:** PLL deve manter rastreamento preciso o suficiente para que
  o controle dq consiga direcionar a corrente reativa corretamente
- Um PLL que perde lock durante afundamento → impossibilidade de cumprir LVRT

## Trade-off Central dos Ganhos PI do PLL

```
Kp/Ki altos → resposta rápida → sensível a ruído e sequência negativa (agrava cenário 2)
Kp/Ki baixos → imunidade a distúrbios → PLL lento (agrava cenários 3 e 4)
```

Esse trade-off é o foco da **Seção 4.3 (Análise de Sensibilidade)** — ainda vazia no documento.
Ver [[pll-gains-methodology]] para as equações de dimensionamento.

---

## Análise Formal — PLL sob Falta Assimétrica (Yazdani-Iravani §12.5.2)

### Tensão no PCC sob falta (eq. 12.50)

```
→Vs = a·V̂s·e^{j(ω₀t+θ₀)} + b·V̂s·e^{-j(ω₀t+θ₀+ψ)}
      ╙─ seq. positiva ─╜   ╙─── seq. negativa ─────╜
```

**Para falta linha-terra:** a = 2/3, b = 1/3, ψ = −π/3.
**Para operação normal:** a = 1, b = 0.

### Efeito no PLL (ρ ≈ ω₀t + θ₀)

Com o PLL em quasi-lock, Vsq fica (eq. 12.64):
```
Vsq ≈ a·V̂s·[ω₀t + θ₀ − ρ] − b·V̂s·sin[2(ω₀t + θ₀) + ψ]
          ╙──── erro útil ───╜   ╙──── distúrbio 2ω₀ ────╜
```

Equação diferencial do PLL com distúrbio (eq. 12.65):
```
dρ/dt = a·V̂s·H(p)·[ω₀t+θ₀−ρ] − b·V̂s·H(p)·sin[2(ω₀t+θ₀)+ψ]
```

### Consequências Quantitativas

| Efeito | Expressão | Falta L-T (a=2/3, b=1/3) |
|--------|-----------|--------------------------|
| Queda no ganho da malha | 100·(1−a) % | −33% |
| Frequência do distúrbio | 2ω₀ | 120 Hz |
| Oscilação em ω e ρ | amplitude ∝ b·\|H(j2ω₀)\| | depende de H(s) |
| Ripple em P e Q | amplitude ≈ b·Ps | ≈ Ps/3 |

### Solução Formal

Para atenuar o distúrbio: incluir zeros complexos em H(s):
```
zeros em s = ±j2ω₀   →   |H(j2ω₀)| ≪ 1
```

PI simples (H = Kp + Ki/s) não possui esses zeros → ripple de 120 Hz não é atenuado.
Soluções alternativas: notch externo em 2ω₀, DSOGI-PLL, DDSRF-PLL (ver [[srf-pll-theory]]).

### Feed-forward de Tensão no Controle de Corrente (§12.5.3)

Mesmo com ripple em ω/ρ, o controle de corrente pode mitigar a propagação do distúrbio via
feed-forward filtrado de Vsd/Vsq nos geradores de md/mq (banda de Gff >> 2ω₀).
No Simulink do projeto: `PWM Control` inclui feed-forward de Vsd/Vsq — ver [[simulink-model]].
