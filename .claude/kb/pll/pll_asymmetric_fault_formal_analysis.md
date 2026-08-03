---
name: pll-asymmetric-fault-formal-analysis
description: Análise formal do SRF-PLL sob falta assimétrica (Yazdani-Iravani §12.5.2) — equações da sequência negativa, ripple de 2ω₀ e mitigação por feed-forward
source: Yazdani & Iravani, "Voltage-Sourced Converters in Power Systems", §12.5.2-12.5.3
references:
  - "YAZDANI, Amirnaser; IRAVANI, Reza. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. Hoboken: John Wiley & Sons / IEEE Press, 2010. ISBN 978-0-470-52156-4."
---

# Análise Formal — PLL sob Falta Assimétrica (Yazdani-Iravani §12.5.2)

Detalhamento formal do Cenário 2 (Afundamento de Tensão Assimétrico) de
[[pll-contingencies]] — equações da sequência negativa que geram o ripple de
2ª harmônica citado ali.

## Tensão no PCC sob Falta (eq. 12.50)

```
→Vs = a·V̂s·e^{j(ω₀t+θ₀)} + b·V̂s·e^{-j(ω₀t+θ₀+ψ)}
      ╙─ seq. positiva ─╜   ╙─── seq. negativa ─────╜
```

**Para falta linha-terra:** a = 2/3, b = 1/3, ψ = −π/3.
**Para operação normal:** a = 1, b = 0.

## Efeito no PLL (ρ ≈ ω₀t + θ₀)

Com o PLL em quasi-lock, Vsq fica (eq. 12.64):
```
Vsq ≈ a·V̂s·[ω₀t + θ₀ − ρ] − b·V̂s·sin[2(ω₀t + θ₀) + ψ]
          ╙──── erro útil ───╜   ╙──── distúrbio 2ω₀ ────╜
```

Equação diferencial do PLL com distúrbio (eq. 12.65):
```
dρ/dt = a·V̂s·H(p)·[ω₀t+θ₀−ρ] − b·V̂s·H(p)·sin[2(ω₀t+θ₀)+ψ]
```

## Consequências Quantitativas

| Efeito | Expressão | Falta L-T (a=2/3, b=1/3) |
|--------|-----------|--------------------------|
| Queda no ganho da malha | 100·(1−a) % | −33% |
| Frequência do distúrbio | 2ω₀ | 120 Hz |
| Oscilação em ω e ρ | amplitude ∝ b·\|H(j2ω₀)\| | depende de H(s) |
| Ripple em P e Q | amplitude ≈ b·Ps | ≈ Ps/3 |

## Solução Formal

Para atenuar o distúrbio: incluir zeros complexos em H(s):
```
zeros em s = ±j2ω₀   →   |H(j2ω₀)| ≪ 1
```

PI simples (H = Kp + Ki/s) não possui esses zeros → ripple de 120 Hz não é atenuado.
Soluções alternativas: notch externo em 2ω₀, DSOGI-PLL, DDSRF-PLL (ver [[srf-pll-theory]]).

Dado de campo real (turbina eólica PMSG) mostrando desequilíbrio de corrente entre
fases sob falta assimétrica — manifestação física deste mesmo efeito — em
[china_lvrt_windfarm_test.md](../standards/china_lvrt_windfarm_test.md).

## Feed-forward de Tensão no Controle de Corrente (§12.5.3)

Mesmo com ripple em ω/ρ, o controle de corrente pode mitigar a propagação do distúrbio via
feed-forward filtrado de Vsd/Vsq nos geradores de md/mq (banda de Gff >> 2ω₀).
No Simulink do projeto: `PWM Control` inclui feed-forward de Vsd/Vsq — ver [[simulink-model]].

## Geração de Harmônico de 3ª Ordem via Ripple do Barramento CC (§12.5.5)

Se o PWM não usa feed-forward da tensão CC (ou a atenua mal), o ripple de 2ω₀
em V²_DC (causado pelo mesmo `b` da seção acima) se propaga para o sinal de
modulação e gera, no lado AC, dois componentes indesejados: uma componente
fundamental de **sequência negativa** e um **harmônico de 3ª ordem de sequência
positiva** — ambos com amplitude proporcional à razão `Vov/VDCref` (eq. 12.106),
onde `Vov` é a amplitude da sobretensão CC de 2ω₀ (eq. 12.101). Mitigação:
feed-forward de `VDC(t)` real (não `VDCref` constante) no cálculo de `md`/`mq`,
com banda de medição e frequência de chaveamento adequadamente maiores que 2ω₀.

**Exemplo numérico (Yazdani Example 12.2, HVDC, `Ceq=500µF`, `Psref1=24MW`):**
falta linha-terra em um PCC (`a=2/3, b=1/3`) → sobretensão CC `Vov≈0,6-0,9 kV`
(**1,7-2,6%** de `VDCref=35kV`) e ripple de potência ativa de **até ±50% do
valor médio** (±8MW em torno de 16MW). Mostra que a severidade do harmônico
gerado escala com `b` (fração de sequência negativa vista nos terminais), não
com um limiar fixo — ver [harmonic_significance_criteria.md](../standards/harmonic_significance_criteria.md)
para como isso se compara a critérios normativos de conformidade.
