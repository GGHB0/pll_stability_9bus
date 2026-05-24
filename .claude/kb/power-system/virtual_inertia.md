---
name: virtual-inertia
description: Inércia virtual/sintética em IBRs — VSG/VSM, parâmetros J_virt e D, grid-forming vs grid-following, e posição como trabalho futuro do TCC
source: MDPI Energies 15(20) 7767 (2022); MDPI Energies 15(22) 8406 (2022)
---

# Inércia Virtual / Sintética em Inversores

## Motivação

IBRs grid-following (como o inversor modelado no TCC) não possuem inércia física.
À medida que substituem geradores síncronos, H_sys cai → RoCoF pós-contingência sobe
→ PLLs perdem lock (ver [[machine-inertia]]). Inversores grid-forming resolvem isso
emulando a resposta inercial por software.

## Virtual Synchronous Generator (VSG / VSM)

Implementa digitalmente a equação de swing do gerador síncrono:

```
J_virt · dω/dt = Pm_virt - Pe - D·(ω - ωs)
```

- `J_virt` [kg·m²]: momento de inércia virtual — parâmetro de software, ajustável em tempo real
- `D` [N·m·s/rad]: coeficiente de amortecimento virtual — controla supressão de oscilações
- `H_equiv = ½·J_virt·ωs² / S_nom` [s] — contribui diretamente para H_sys do sistema

Ao contrário da inércia física, J_virt pode ser adaptado dinamicamente conforme o estado da rede.

## Grid-Following vs Grid-Forming

| Característica | Grid-Following (TCC) | Grid-Forming (VSG/VSM) |
|---|---|---|
| Sincronização | SRF-PLL (extrai θ da rede) | Droop/VSM interno (impõe θ) |
| Inércia contribuída | Zero (sem emulação) | H_equiv configurável |
| Resposta a RoCoF alto | Perde lock (θ̂ diverge) | Resiliente — inércia própria |
| Necessita rede forte | Sim (depende de V e θ estáveis) | Não (pode operar como grid-ref) |
| Implantação no TCC | Inversor modelado | Não modelado |

## Parâmetros e Trade-offs

- **J_virt alto** → maior amortecimento de RoCoF, porém resposta mais lenta a transitórios
- **J_virt baixo** → resposta rápida, porém contribuição inercial pequena
- **D alto** → maior amortecimento de oscilações pós-distúrbio
- Ajuste ótimo de J_virt e D é tema de pesquisa ativa (ex.: controle adaptativo de inércia)

## Posição no TCC

O inversor modelado (grid-following + SRF-PLL) é o tipo mais vulnerável a baixa inércia
sistêmica — exatamente o cenário investigado. A migração para grid-forming resolveria o
lock-loss mas está fora do escopo do trabalho.

Sugestão de trabalho futuro: implementar VSG no modelo Simulink e comparar a resposta
de P e Q durante o Cenário 4 (Alto RoCoF) com o inversor atual.

## Cross-refs

Ver [[machine-inertia]] — cadeia H↓ → RoCoF↑ → lock-loss e estimativa de BW do PLL.
Ver [[inertia-estimation]] — como H_sys é monitorado e por que cai com IBRs.
Ver [[pll-contingencies]] — Cenário 4 (Alto RoCoF) onde o lock-loss ocorre.
