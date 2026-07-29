---
name: srf-pll-theory
description: Teoria do SRF-PLL — estrutura, modelo linear, projeto de ganhos (Karimi-Ghartemani cap.6)
source: Enhanced Phase-Locked Loop Structures for Power and Energy Applications, Karimi-Ghartemani, 2014, p.133-139
references:
  - "KARIMI-GHARTEMANI, Masoud. Enhanced Phase-Locked Loop Structures for Power and Energy Applications. Hoboken: John Wiley & Sons / IEEE Press, 2014. ISBN 978-1-118-79502-6."
  - "YAZDANI, Amirnaser; IRAVANI, Reza. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. Hoboken: John Wiley & Sons / IEEE Press, 2010. ISBN 978-0-470-52156-4."
---

# SRF-PLL — Synchronous Reference Frame PLL

**Outros nomes:** dqz-PLL, dqo-PLL, DQPLL, QPLL.
Referência clássica trifásica. Evita o erro de dupla frequência do PLL monofásico graças à simetria das tensões trifásicas.

## Estrutura

```
uabc → abc/dqo → uq → PI → ωo → ∫ → φo ↺ (feedback para abc/dqo)
                                ωn ↑ (feed-forward de frequência nominal)
```

O bloco de medição de fase (PD) é a transformada de Park; o VCO gera três senoides em 120°.

## Transformada de Park (abc/dqo)

```
P = (2/3) * | sin(φo)   sin(φo - 2π/3)   sin(φo + 2π/3) |
            | cos(φo)   cos(φo - 2π/3)   cos(φo + 2π/3) |
            |  1/2           1/2               1/2        |
```

Para entrada balanceada `u_abc = U·[sin(φi), sin(φi-2π/3), sin(φi+2π/3)]`:

```
u_dqo = (U·cos(φi - φo),  U·sin(φi - φo),  0)
```

Regulando `uq → 0`, o PLL faz `φo → φi` e `ud → U` (sem ripple de dupla frequência).

## Modelo Linear e Equação Característica

O laço linearizado é de **tipo 2** (integrador no controlador + integrador do VCO):

```
s² + h0·U·s + h1·U = 0
```

onde `H(s) = h0 + h1/s` é a FT do PI. Correspondência com notação do projeto:

| Karimi (h0, h1) | Projeto (Kp, Ki) |
|---|---|
| `h0` | `Kp` |
| `h1` | `Ki` |

**Implicações do tipo 2:**
- Rastreia degraus de frequência com erro nulo em regime permanente.
- Rastreia rampas de fase (variação linear de freq.) com erro zero ou pequeno.
- Desempenho depende da magnitude U → normalização por `√(ud²+uq²)` torna o laço independente de U.

## Projeto dos Ganhos

Escolhendo polos complexos conjugados com frequência natural `ωn` e amortecimento `ξ`:

```
s² + 2ξωn·s + ωn² = 0  →  h0 = 2ξωn/U,  h1 = ωn²/U
```

Trade-off: ganhos maiores → resposta rápida mas sensível a ruído/distorção.

## Frame αβ (Representação Estacionária)

```
u_αβ = Clarke(u_abc),  u_dq = R(φo)·u_αβ
```

onde `R(φo)` é a matriz de rotação. Permite operar com apenas fase-a + sinal ortogonal gerado (base do SRF-PLL monofásico).

## SRF-PLL Monofásico

Requer geração do sinal ortogonal `uβ` (90° defasado de `uα`):
- **Categoria 1:** gera `uβ` diretamente do sinal de entrada (delay, Hilbert, APF, FIR).
- **Categoria 2 (preferida):** gera `uβ` a partir do ângulo `φo` e da amplitude estimada `Uo` via transformada inversa de Park (IP-PLL e variantes).

## Equivalência com EPLL (Monofásico)

Com `uα = u = Ui·sin(φi)` e `uβ = -Uo·cos(φo)`:

```
uq = cos(φo)·uα + sin(φo)·uβ = (u - Uo·sin(φo))·cos(φo) = e·cos(φo)
```

Este `uq` é exatamente o sinal `z` que alimenta o PI no EPLL monofásico (Fig. 2.1 do livro).
A estimação de amplitude `ud ≈ Uo` em regime permanente fecha a equivalência via LPF `ωc/(s+ωc)`.

---

## Projeto do Compensador H(s) — Yazdani-Iravani §8.3.4–8.3.5

### Requisitos de H(s)

1. **Polo em s=0** — para rastrear o componente rampa ω₀t (referência do PLL) com erro nulo.
2. **Zeros complexos em ±j2ω₀** — para atenuar o ripple de 2ª harmônica (120 Hz para 60 Hz) gerado pela componente de sequência negativa da tensão.

Sob tensão desbalanceada com coeficiente de sequência negativa k1:
```
Vsq = −k1·V̂s·sin(2ω₀t + 2θ₀)   ← distúrbio a 2ω₀ que H(s) deve atenuar
```
k1 típico ≈ 0,01 em operação normal; k1 até 0,5 durante falta monofásica.

### H(s) Estruturado — Exemplo 8.1 (ω₀=2π×60, V̂s=391 V, ωc=200 rad/s, MF=60°)

```
H(s) = 685,42 · [s² + (2ω₀)²] · [s² + 166s + 6889]
               ──────────────────────────────────────────────────
               s · [s² + 1508s + (2ω₀)²] · [s² + 964s + 232324]
```

Limites: ωmin = 2π×55 rad/s, ωmax = 2π×65 rad/s.
Transitório de partida: ~70 ms saturado em ωmin → acomodação em ~150 ms.

### PI Simples vs. H(s) Estruturado

| Aspecto | PI simples (H = Kp + Ki/s) | H(s) estruturado |
|---------|--------------------------|------------------|
| Zeros em ±j2ω₀ | não | sim |
| Ripple 120 Hz em ω, ρ | não atenuado | fortemente atenuado |
| Complexidade | baixa | alta (4ª ordem) |

O PLL do projeto usa bloco Simscape (`Sinusoidal Measurement (PLL, Three-Phase)`) com ganhos
equivalentes a PI simples — ver [[pll-gains-methodology]]. Sem zeros em ±j2ω₀, o
cenário de falta assimétrica é o mais crítico — ver [[pll-contingencies]].
