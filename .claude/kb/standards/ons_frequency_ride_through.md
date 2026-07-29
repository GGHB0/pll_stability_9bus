---
name: ons-frequency-ride-through
description: Faixas de operação em frequência não nominal (Submódulo 2.10 ONS) para centrais eólicas/fotovoltaicas — trip/ride-through, controle primário de frequência e limites de redução de potência
source: ONS, Submódulo 2.10 — Requisitos técnicos mínimos para a conexão às instalações de transmissão, rev. 2025.02 (vigência 01/03/2025), itens 4.2.1, 5.2.1, 5.2.7-5.2.9, pp.10, 21-28
---

# ONS Submódulo 2.10 — Requisito de Frequência Não Nominal (UFV/Eólica)

## Duas Curvas Distintas no Mesmo Submódulo — Não Confundir

O Submódulo 2.10 define **faixas de frequência diferentes por tipo de fonte**:

| Seção | Fonte | Figura |
|---|---|---|
| 4.2.1 | Hidrelétrica | Figura 1 |
| 4.2.2 | Termelétrica | Figura 2 |
| **5.2.1** | **Eólica e fotovoltaica (UFV)** | **Figura 5** |

O caso deste TCC (UFV via inversor grid-following) usa **5.2.1**, não 4.2.1. As
faixas não são iguais — a de eólica/fotovoltaica é mais estreita.

## 5.2.1 — Faixa de Operação em Frequência Não Nominal (Figura 5)

| Faixa | Condição |
|---|---|
| < 56 Hz | Desligamento/desconexão instantânea permitida |
| 56 – 58,5 Hz | Desligamento/desconexão permitida após tempo mínimo de **20 s** |
| 58,5 – 62,5 Hz | **Operação contínua** (tempo ilimitado) |
| 62,5 – 63 Hz | Desligamento/desconexão permitida após tempo mínimo de **10 s** (temporização definida por avaliação de desempenho dinâmico, a critério do ONS) |
| > 63 Hz | Desligamento/desconexão instantânea permitida |

### Comparação com Hidrelétrica (4.2.1, Figura 1)

| Limite | Hidro (4.2.1) | Eólica/FV (5.2.1) |
|---|---|---|
| Trip instantâneo inferior | < 56 Hz | < 56 Hz (igual) |
| Trip temporizado inferior | < 58,5 Hz (20 s) | < 58,5 Hz (20 s) (igual) |
| Banda de operação contínua | 58,5 – **63** Hz | 58,5 – **62,5** Hz |
| Trip temporizado superior | > 63 Hz (10 s) | > 62,5 Hz (10 s) |
| Trip instantâneo superior | > **66** Hz | > **63** Hz |

A banda contínua da UFV é 4,5 Hz mais estreita no lado superior (teto de trip
instantâneo em 63 Hz, contra 66 Hz da hidro) — fontes baseadas em eletrônica de
potência têm tolerância normativa menor a sobrefrequência sustentada.

## 5.2.7 — Potência Ativa de Saída vs. Frequência

- **(c)** Sem redução de potência permitida para frequência entre **58,5–60,0 Hz**
  e tensão entre 0,85–1,10 pu no ponto de conexão.
- **(d)** Para frequência entre **57–58,5 Hz**, admite-se redução de até **10%**
  na potência de saída.
- **5.2.7.1** Esses requisitos valem para regime quase-estático: gradiente de
  frequência ≤ 0,5%/min e gradiente de tensão ≤ 5%/min — não se aplicam
  diretamente a transitórios rápidos (RoCoF elevado), que é o regime dos
  cenários simulados no TCC.

## 5.2.9 + Tabela 2 — Controle Primário de Frequência (Droop)

Centrais >10 MW devem ter controlador proporcional sensível a desvio de
frequência (Figura 11):

| Parâmetro | Padrão | Mínimo | Máximo |
|---|---|---|---|
| Banda morta subfrequência (bmUF) | 0,1 Hz | 0,040 Hz | 0,2 Hz |
| Banda morta sobrefrequência (bmOF) | 0,1 Hz | 0,040 Hz | 0,2 Hz |
| Estatismo subfrequência (kUF) | 5% | 2% | 8% |
| Estatismo sobrefrequência (kOF) | 5% | 2% | 8% |
| PMAX | 100% | — | 100% |
| PMIN | 25% | — | 25% |

## 5.2.8 — Inércia Sintética: Item Específico de EÓLICA, Não de UFV

Atenção: o item 5.2.8 é titulado **"Inércia sintética da central geradora
eólica"** — texto normativo restrito a aerogeradores (potência >10 MW,
contribuição mínima de 10% da potência nominal por 5 s, limiar de ativação em
desvio de frequência >0,2 Hz, taxa de 0,8 pu/Hz). **Não há menção equivalente
para central fotovoltaica** neste submódulo. Não assumir que o requisito de
inércia sintética se aplica à UFV do modelo sem confirmação em outra norma —
tratar como **gap/assimetria normativa** relevante à discussão do TCC sobre
baixa inércia e IBRs (ver [[machine-inertia]], [[virtual-inertia]]).

## Relação com os Cenários do TCC

- **Cenário 4 (Alto RoCoF)** em [[pll-contingencies]]: o achado empírico de
  H > 0,1 s como limiar de colapso é observação de simulação, sem vínculo
  normativo direto — 5.2.1 define *até onde* a frequência pode variar antes do
  trip ser permitido, não *quão rápido* (RoCoF) esse desvio pode ocorrer. O
  Submódulo 2.10 não define limite de RoCoF explícito nesta seção.
- **Cenário 3 (Salto de Fase)**: a nota de gap em [[pll-contingencies]] sobre
  "phase jump ride-through" (Submódulo 2.8/3.6, não confirmado) continua
  distinta deste achado — frequência (5.2.1) e ângulo de fase são grandezas
  diferentes; não usar 5.2.1 para preencher aquele gap.
- Complementa [[ons-2-11]] (mesmo Submódulo 2.10, item §5.8 — suporte de
  tensão/corrente reativa sob defeito), que trata de amplitude de V, não de
  frequência.

## Fonte

ONS, Submódulo 2.10 — Requisitos técnicos mínimos para a conexão às
instalações de transmissão, revisão 2025.02, vigência 01/03/2025. Itens 4.2.1
(p.10), 5.2.1 (pp.21-22), 5.2.7-5.2.9 (pp.25-28). PDF:
`Submodulo 2.10 ONS procedimento de rede.pdf` (bibliografia do TCC).
