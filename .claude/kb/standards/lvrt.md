---
name: lvrt-standards
description: Requisitos LVRT e IEEE 1547-2018 relevantes para avaliação do SRF-PLL
source: TCCs V8 cap.2.4.2; IEEE Std 1547-2018 (requisitos detalhados extraídos via IEEE Std 1547.2-2023, ver ieee1547_ride_through.md)
---

# LVRT — Low Voltage Ride-Through

## Definição

Capacidade do inversor de **permanecer conectado** à rede durante afundamentos de tensão,
desde que o perfil do evento (magnitude × duração) esteja dentro da curva de tolerância.

## Requisito IEEE 1547-2018

- Sistemas de geração distribuída **não devem desconectar** durante afundamentos dentro da curva V×t
- Durante o afundamento: **injetar corrente reativa** proporcional à profundidade do afundamento
  (suporte dinâmico de tensão)
- Objetivo: evitar perda em cascata de geração que agravaria a instabilidade

## Condição para Conformidade

A injeção correta de corrente reativa requer que:
1. O PLL mantenha rastreamento preciso de θ e ω durante o evento
2. O controle dq consiga separar id (ativa) de iq (reativa) corretamente

→ Se o PLL perde o lock ou fornece θ errado: controle dq corrompe →
  corrente reativa injetada na direção errada → falha LVRT

## Ligação com o Evento 15/08/2023

O RAP do ONS concluiu que inversores eólicos/fotovoltaicos **se desconectaram inesperadamente**
durante a perturbação — evidência direta de falha de LVRT em escala real.
O TCC investiga o mecanismo de controle (SRF-PLL) responsável por essa falha.

## Avaliação no Capítulo 4 (Seção 4.3.2)

Para cada cenário simulado, verificar se:
- O erro de fase θ_erro converge dentro do tempo de acomodação ts permitido
- A corrente reativa injetada (iq) atinge o valor de referência durante o afundamento
- A potência ativa P não colapsa abaixo do mínimo regulatório

## Ver também

- [ieee1547_ride_through.md](ieee1547_ride_through.md) — categorias I/II/III,
  tabela de trip mandatório (UV1/UV2/OV1/OV2), regiões de operação e Dynamic
  Voltage Support (DVS), com comparação direta à `ONS_2_11`
- [ieee1547_case_studies.md](ieee1547_case_studies.md) — estudos de caso reais
  (CAISO, Entergy) sobre o efeito da categoria/DVS na recuperação de tensão
- [ons_2_11.md](ons_2_11.md) — implementação real no modelo Simulink do TCC
