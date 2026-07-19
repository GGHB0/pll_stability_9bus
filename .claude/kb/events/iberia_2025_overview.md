---
name: iberia-2025-overview
description: Apagão ibérico de 28/abr/2025 — linha do tempo, números-chave e condições pré-evento (relatório final ENTSO-E)
source: ENTSO-E, Grid Incident in Spain and Portugal on 28 April 2025 — Final Report, mar/2026, §1–§3
---

# Apagão Ibérico — 28 de Abril de 2025

Blackout mais severo da Europa em 20+ anos. Colapso total dos sistemas de
Espanha e Portugal às 12:33 CEST, classificado **escala 3 do ICS** (máxima).
Pequena área da França também afetada (escala 1, ~7 MW de carga + trip de
1 usina nuclear). Investigado por Expert Panel da ENTSO-E com 49 especialistas.

## Mecanismo em uma frase

Subida rápida e descontrolada de tensão → cascata de desconexões de geração
por **sobretensão** (majoritariamente inversorizada) → queda de frequência →
perda de sincronismo com a Europa Continental → colapso.

## Condições pré-evento (manhã de 28/abr)

- Dia típico de primavera: alta geração solar (~18,7 GW no sudoeste), preços
  baixos no day-ahead, exportações da Espanha em 5 GW.
- Produção no sudoeste espanhol muito acima do consumo regional → grandes
  trânsitos de potência para as demais regiões.
- Variabilidade de tensão crescente a partir das 9:00; às 10:30 a tensão em
  parte da rede 400 kV aproximou-se de 435 kV (limite superior espanhol).
- **Duas oscilações na meia hora anterior:**
  - 12:03–12:08 — **0,63 Hz**, local (Ibéria), classificada como fenômeno de
    **instabilidade guiada por conversor** (converter-driven, forçada);
  - 12:19–12:22 — **0,2 Hz**, inter-área, modo Leste-Centro-Oeste da CE SA.
- As medidas de mitigação das oscilações (redução de intercâmbio ES→FR,
  religamento de linhas, mudança de modo do HVDC) funcionaram, **mas
  elevaram a tensão** do sistema ibérico — reatores shunt haviam sido
  desconectados durante os afundamentos das oscilações e não foram religados.

## Linha do tempo do colapso (28/abr/2025, CEST)

| Instante | Evento |
|---|---|
| 12:32:00 | Início da subida de tensão; RES reduzem ~500 MW (fator de potência fixo → perdem absorção de reativo) |
| 12:32:00–57 | +208 MW de geração distribuída desconecta/reduz; +317 MW de aumento líquido de carga nas distribuidoras |
| 12:32:57 | Trip de trafo 400/220 kV (Granada) por sobretensão — perde 355 MW / −165 Mvar |
| 12:33:16 | Trips em 2 subestações 400 kV (Badajoz) — 727 MW PV/termossolar; tensão estimada 432,4 kV |
| 12:33:17–18 | Cascata: 928 MW eólica+solar (Segóvia, Huelva, Badajoz, Sevilha, Cáceres) |
| 12:33:18–21 | Tensão dispara no sul da Espanha; total acumulado > 2,5 GW perdidos |
| 12:33:19 | Início da perda de sincronismo ES/PT ↔ resto da CE SA |
| 12:33:19–22 | Planos de defesa (corte de carga/bombas) atuam conforme projeto, mas não evitam o colapso |
| 12:33:20,5 | Trip da interligação CA com Marrocos (subfrequência) |
| 12:33:21,5 | Linhas CA França–Espanha abrem por perda de sincronismo (proteção DRS) |
| 12:33:24 | HVDC FR-ES desliga — separação elétrica completa; colapso total ES/PT |

RoCoF permaneceu dentro de ±1 Hz/s até 12:33:20,6 (f ≈ 49 Hz); depois disso
excedeu 1 Hz/s com o sistema já degradado.

## Restauração

- Estratégia mista top-down (apoio de França e Marrocos, 3 zonas) +
  bottom-up (black-start de hidrelétricas; várias tentativas falharam).
- Portugal restaurado em ~12 h (00:22 de 29/abr); Espanha em ~16 h (04:00).
- Problemas: falhas de black-start, ilhas instáveis, comunicação de voz de
  DSOs fora do ar, baixa observabilidade de DER na distribuição.

## Relevância para o TCC

Evento análogo ao apagão brasileiro de 15/ago/2023 (23.368 MW): em ambos,
desconexões em cascata de geração inversorizada por atuação de proteção
durante transitório de tensão. Ver [[iberia-2025-root-causes]] e
[[iberia-2025-ibr-lessons]].
