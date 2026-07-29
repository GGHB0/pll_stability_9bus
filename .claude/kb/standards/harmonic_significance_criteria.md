---
name: harmonic-significance-criteria
description: Critérios da literatura para o que conta como harmônico de tensão/corrente "significativo" em pu — normas de conformidade (IEEE 519/1547) vs. rejeição a distúrbio (TeseAGP) vs. criério funcional de PLL (Yazdani)
source: TeseAGP p.31-39,58-60,135-138,189-193; Yazdani & Iravani §4.2.4,4.3.3,12.5.1-12.5.7 (p.103-113,376-393)
---

# Critérios de Harmônico Significativo — Normas vs. Literatura

Não existe um único número universal. Três noções diferentes de "significativo"
aparecem na literatura consultada, cada uma útil para um propósito distinto.

## 1. Conformidade normativa (limite máximo aceitável)

TeseAGP (p.58, §2.5) cita explicitamente: "normas como a **IEEE 519-2014**[14]
e **IEEE 1547-2018**[15] estabelecem limites para as componentes harmônicas de
corrente em **unidades geradoras**". Como o inversor deste TCC é uma unidade
geradora conectada ao SIN (Barra 2), essas duas normas são as aplicáveis — **não
o PRODIST Módulo 8** (ANEEL), que rege apenas conexões de distribuição (BT/MT).
Correção registrada em 2026-07-28 (usuário).

IEEE 519-2014 (contexto — não extraído do PDF deste projeto, ver resposta em
chat): limites individuais de 1-5% e THD de 1,5-8% dependendo da classe de
tensão. IEEE 1547-2018 tem cláusula própria de distorção harmônica (diferente
da cláusula de ride-through já documentada em [ieee1547_ride_through.md](ieee1547_ride_through.md))
— ainda não extraída para este projeto.

## 2. Rejeição a distúrbio (significância funcional/empírica)

TeseAGP §5.2.2 "Susceptibilidade a harmônicos de ordem elevada" (p.135):
um **distúrbio de tensão de 3% (0,03 pu)** na frequência de ressonância do
filtro LCL, sem compensação, amplifica para **7,02% (0,07 pu)** de harmônico
de corrente em regime permanente — chamado explicitamente de "indesejado".
Com controlador ressonante ajustado nessa frequência, cai para 2,92%.

TeseAGP p.59 cita um estudo (inversor PV monofásico, refs [56,57]) que reduziu,
via controladores ressonantes, os harmônicos de 3ª/5ª/7ª ordem de
**8,53% / 3,44% / 1,65% → 0,613% / 0,474% / 0,388%**. Padrão implícito na
literatura: acima de ~2-3% já é tratado como problema a mitigar; resultado
"bom" pós-mitigação fica na faixa de 0,4-0,6%.

## 3. Critério funcional de PLL (primeiros princípios, sem limiar fixo)

Yazdani & Iravani não definem um valor fixo — mostram que a magnitude do
distúrbio de 2ω₀ no PLL e do harmônico de 3ª ordem gerado é **proporcional**
à fração de sequência negativa `b` (adimensional, 0 a 1 pu de V̂s), não um
degrau discreto. Ver desenvolvimento completo em
[pll_asymmetric_fault_formal_analysis.md](../pll/pll_asymmetric_fault_formal_analysis.md).

Exemplo extremo (falta linha-terra no próprio PCC, Yazdani Example 12.2):
`a=2/3, b=1/3` → ripple de potência ativa de **até ±50% do valor médio**
(±8 MW em torno de 16 MW) e sobretensão no barramento CC de **1,7-2,6%**.
Ou seja: o "quanto importa" depende inteiramente de quão severo é o
desequilíbrio visto nos terminais do inversor (que depende da localização/tipo
de falta), não de uma tabela de limites.

## Como isso se conecta ao dashboard deste projeto

`_HARM_LO_PU = 0,02` (2%) e `_HARM_HI_PU = 0,4` (40%) em
[espectro-fourier.md](../dashboard/graficos/espectro-fourier.md) são escolhas
estéticas do relatório, não limites normativos. O piso de 2% coincide,
por coincidência, com a ordem de grandeza do que a literatura de rejeição a
distúrbio (item 2 acima) já trata como "pequeno o suficiente" — mas não foi
derivado de nenhuma norma.
