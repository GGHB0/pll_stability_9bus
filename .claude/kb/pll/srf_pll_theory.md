---
name: srf-pll-theory
description: Teoria do SRF-PLL — estrutura, modelo linear, projeto de ganhos (Karimi-Ghartemani cap.6)
source: Enhanced Phase-Locked Loop Structures for Power and Energy Applications, Karimi-Ghartemani, 2014, p.133-139
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
