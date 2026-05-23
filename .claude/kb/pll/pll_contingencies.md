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
