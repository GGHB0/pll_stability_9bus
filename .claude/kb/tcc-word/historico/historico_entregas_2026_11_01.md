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

## Promoção da versão do Victor e Equação (3.1) do ONS (16h39)

Promovido o backup mais recente do Victor (_20261101_042452, 897 parágrafos,
com todas as revisões de Rafael em azul, André em verde e Cleiton em vermelho)
para o arquivo canônico TCC_Victor_Bruno_VFinal.docx.

Formatação formal da restrição de corrente reativa do ONS (§3.3.2.1):
- A fórmula em pseudo-código id,ref = min(1.0, sqrt(Imax² - iq,ref²)) foi
  removida do texto corrido e convertida na Equação (3.1) em tabela sem
  bordas com OMML nativo: id,ref = min(1,0; sqrt(Imax² - iq,ref²)).
  Rótulo (3.1) e texto introdutório mantidos em vermelho (#FF0000, Prof. Cleiton).
- A teoria p-q de Akagi (§3.3.3) foi renumerada de (3.1) para (3.2)
  (menção no texto e rótulo na tabela), mantendo a cor azul (#0070C0, Prof. Rafael).
- audit_docx: 0 falhas, 0 avisos; diff_texto: 3 trechos (897 → 899 parágrafos).
  Backup datado em _backups\VF\TCC_Victor_Bruno_VFinal_backup_20261101_163920.docx.
