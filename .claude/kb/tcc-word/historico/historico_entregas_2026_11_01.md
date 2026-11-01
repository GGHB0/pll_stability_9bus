---
name: tcc-historico-entregas-2026-11-01
description: Entrega de 2026-11-01 (03h12): Figura 2.2 com a planta LCL da TeseAGP no lugar do RL, fonte com Alves (2022)
aliases: [tcc-historico-entregas-2026-11-01]
---

# TCC Word — Entrega de 2026-11-01 (03h12)

Continuação de [[tcc-historico-entregas]].

## Figura 2.2: planta LCL no lugar de 1/(Ls+R)

O bloco amarelo da malha de corrente dq era a planta RL de 1ª ordem
(L = L1+L2, R = R1+R2), que não é a do modelo: o filtro é LCL e a corrente
realimentada é iL2. Passou a ser 1/(s·L1·L2·C1) · 1/(s²+ωres²), eq. 3.49 da
TeseAGP (Alves, 2022), com o desenho em duas frações como na Fig. 3.23 da tese.
Rodapé da figura: ωres² = (L1+L2)/(L1·L2·C1) e "N(s): filtro notch". O resto
(PI Kp/4 + Ki/4s, notch, Vcc/2, eixos d e q, realimentação) ficou igual.

- `troca_imagem.py --rid rId16` (PNG 2340×1080, mesma largura de 6,30 in);
  fonte da figura: "Adaptado de Yazdani e Iravani (2010) e Alves (2022)"
  (Alves 2022 já estava nas referências). Cor vermelha da legenda e da fonte
  mantida como estava.
- `diff_texto` backup × canônico: 1 trecho (a linha da fonte); 0 comentários.
  Backup `_backups\VF\..._20261101_031249`; auditoria 0 falhas, 89 páginas.
- O OneDrive foi reorganizado: o canônico agora está em
  `Template Modelo TCC\01_TCC_Monografia_Final\` (config.py ajustado).

**Pendente, fora desta entrega:** o §3.3.2 (bloco 475) diz que há "termos de
desacoplamento" e que cada eixo vira "planta de primeira ordem". O modelo não
tem desacoplamento e a planta é LCL (ver [[agp-current-control-theory]],
[[simulink-model]]); a Seção 2.3.2 já diz isso certo. Decidir com o Victor.
