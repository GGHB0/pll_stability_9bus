---
name: inertia-estimation
description: Centro de Inércia (CoI), tendência de queda sistêmica, e 5 técnicas de estimação de H — revisão MDPI Energies 15/20/7767 com avaliação Monte Carlo no IEEE 9-bus
source: MDPI Energies 15(20) 7767 (2022) — Inertia Estimation of Synchronous Devices
---

# Estimação de Inércia em Sistemas de Potência

## Centro de Inércia (CoI) do Sistema

A frequência do Centro de Inércia é o indicador global usado em estudos de estabilidade:

```
f_CoI(t) = Σ(Hi · Si · fi(t)) / Σ(Hi · Si)

RoCoF_CoI ≈ -fn · ΔP / (2 · H_sys · S_total)
```

`H_sys = Σ(Hi · Si) / S_total` — inércia equivalente do sistema [s].

Importante: métodos de estimação baseados em RoCoF são válidos apenas para f_CoI
(indicador global), não para medição local em um nó arbitrário da rede.

## Tendência de Redução de Inércia Sistêmica

Com crescente penetração de IBRs:
- H_sys cai à medida que geradores síncronos são desligados ou operam a carga reduzida
- Brasil ago/2023: alta participação de solar + IBRs → H_sys baixo; contingência gerou
  RoCoF alto → PLLs de IBRs perderam lock → ciclo de realimentação → cascata
- ENTSO-E projeta queda de 30–50 % na inércia sistêmica europeia até 2030
- Limites regulatórios de RoCoF (ex.: ±2 Hz/s IEEE 1547, ±0,5 Hz/s em TSOs europeus)
  tornam-se ativos antes mesmo do lock-loss do PLL

## Técnicas de Estimação de Inércia

Revisão e avaliação comparativa via Monte Carlo no sistema IEEE 9-bus.
Fonte: MDPI Energies 15(20) 7767 (2022).

### Método 1 — RoCoF Direto

```
H = fn · ΔP / (2 · RoCoF_0⁺ · S_base)
```

Sensível a ruído; requer aproximação polinomial de RoCoF em t → 0⁺ para mitigar
componentes oscilatórios e de medição na estimativa do slope inicial.

### Método 2 — Área da Frequência (Integral até o nadir)

```
H ≈ fn · ΔP · t_nadir / (2 · S_base · Δf_nadir)
```

Menos sensível a ruído que o Método 1. Integra o desvio Δf(t) até o ponto de nadir
— suaviza oscilações locais. Melhor balanço precisão/robustez em contingências severas.

### Método 3 — Ajuste de Função de Transferência

Reduz a resposta dinâmica a uma FT de 1ª ou 2ª ordem e extrai H da constante de tempo
resultante. Requer excitação persistente — funciona bem em operação normal, mas
degrada durante faltas (regime transiente não-linear).

### Método 4 — PMU / Sincrofasor

Usa medições de frequência e potência a alta taxa (≥ 50 frames/s).
Aplica a swing equation discretizada em janela deslizante.
Preciso quando PMUs disponíveis; degradado por ruído de medição de RoCoF.

### Método 5 — Mínimos Quadrados (Swing Equation)

Minimiza `||2H/ωs · d²δ/dt² - (Pm - Pe)||²` sobre janela temporal.
Robusto a ruído, mas requer estimativa de Pm (potência mecânica), muitas vezes
indisponível em tempo real para geradores de terceiros.

## Achados do Monte Carlo

- Ruído de medição de RoCoF → maior fonte de erro nos Métodos 1 e 4
- Distorções de tensão (afundamentos, harmônicos) degradam todos os métodos
- Método 2 (área/nadir) apresenta o melhor balanço precisão × robustez
- Precisão de todos os métodos cai significativamente com geradores IBR no mix
  (f_CoI deixa de representar bem qualquer f_local)

## Cross-refs

Ver [[machine-inertia]] — definição de H, swing equation e cadeia de lock-loss.
Ver [[virtual-inertia]] — como IBRs grid-forming contribuem com H_equiv para H_sys.
Ver [[ieee9bus]] — rede onde as simulações Monte Carlo do artigo foram rodadas.
