---
name: ieee1547-ride-through
description: Requisitos detalhados de LVRT/HVRT do IEEE Std 1547-2018 (categorias I/II/III, trip mandatório, Dynamic Voltage Support) extraídos do IEEE Std 1547.2-2023
source: IEEE Std 1547.2-2023 (Application Guide for IEEE Std 1547-2018), §5.2-5.4, §6.4, Annex C, pp.75-127,231-233
---

# IEEE 1547-2018 — Requisitos Detalhados de Ride-Through

## Nota sobre a fonte

O PDF da bibliografia (`805035543-Ieee-Standard-1547-2018.pdf`) é na verdade o
**IEEE Std 1547.2-2023** — o *Application Guide* (guia comentado) para o
IEEE Std 1547-2018, não o standard normativo em si. Ele reproduz e explica os
requisitos do 1547-2018 com racional ("Background"), tabelas e figuras, mas as
tabelas numéricas completas das curvas V×t por categoria (Table 14/15/16 do
1547-2018) não estão neste guia — só as figuras (H.7/H.8/H.9, reproduzidas
como Annex C) e a tabela de trip mandatório (Table 8, abaixo).

## Três Categorias de Performance

| Categoria | Perfil de DER associado |
|---|---|
| I | Acomoda limitações de máquinas rotativas |
| II | Atende necessidades de confiabilidade do sistema de transmissão (bulk system) |
| III | Influenciada pela regulação de alta penetração (CA Rule 21, HI Rule 14H) |

A escolha da categoria é do Area EPS Operator (concessionária), não do fabricante do DER.

## Trip Mandatório — Table 8 (Shall-Trip Voltage Settings)

Independente de ride-through, se a tensão ultrapassar estes limites o DER
**deve** desconectar (`shall trip`) — essas configurações sobrepõem qualquer
capacidade de ride-through:

| Categoria | Função | V default (pu) | t default (s) | Faixa de ajuste V (pu) | Faixa de ajuste t (s) |
|---|---|---|---|---|---|
| I | OV2 | 1,20 | 0,16 | fixo 1,20 | fixo 0,16 |
| I | OV1 | 1,10 | 2,0 | 1,10–1,20 | 1,0–13,0 |
| I | UV1 | 0,70 | 2,0 | 0,0–0,88 | 2,0–21,0 |
| I | UV2 | 0,45 | 0,16 | 0,0–0,50 | 0,16–2,0 |
| II | OV2/OV1 | igual a I | | | |
| II | UV1 | 0,70 | **10,0** | 0,0–0,88 | 2,0–21,0 |
| II | UV2 | 0,45 | 0,16 | 0,0–0,50 | 0,16–2,0 |
| III | OV2 | 1,20 | 0,16 | fixo | fixo |
| III | OV1 | 1,10 | **13,0** | 1,10–1,20 | 1,0–13,0 |
| III | UV1 | **0,88** | **21,0** | 0,0–0,88 | 2,01–50,0 |
| III | UV2 | **0,50** | 2,0 | 0,0–0,50 | 0,16–21,0 |

UV2 = 0,45 pu por 0,16 s é o "buffer" citado em [lvrt.md](lvrt.md): abaixo
desse ponto o ride-through é zero por definição — o DER é obrigado a desligar
mesmo que fosse capaz de continuar operando.

## Regiões de Operação (dentro do envelope de trip)

1. **Continuous operation** (0,88–1,10 pu): operação normal, potência ativa
   proporcional à tensão de fase mínima se abaixo do nominal.
2. **Mandatory operation** (ride-through obrigatório): DER deve manter
   sincronismo, **não pode** parar de trocar corrente com a rede. Categoria
   II/III: corrente aparente total não pode cair abaixo de 80% do valor
   pré-distúrbio (ou da corrente ativa disponível, o que for menor).
3. **Permissive operation**: DER pode manter corrente OU entrar em
   *momentary cessation* (parar de injetar corrente sem desconectar) — a
   critério do AGIR/operador. Uso disseminado de momentary cessation
   prejudica a confiabilidade do sistema de transmissão.
4. **Momentary cessation region** — só existe para Categoria III, em tensões
   muito baixas (< 0,5 pu): a norma **exige** ride-through mesmo em momentary
   cessation (não desconectar, mas também não precisa injetar corrente).

## Dynamic Voltage Support (DVS) — §6.4.2.6

Capacidade **opcional** (não mandatória para nenhuma categoria, requer acordo
mútuo entre operador do DER e da rede) de injetar corrente reativa durante
mandatory/permissive operation:

- Resposta rápida — dentro de alguns ciclos (diferente do volt-var de regime
  permanente, que responde em segundos)
- Corrente reativa **proporcional ao desvio** (`%ΔV`) entre a tensão medida e
  uma **média móvel pré-evento** (`Vaverage`) — não à tensão absoluta
- Usa **Q-priority**: reduz corrente ativa em favor de reativa quando atinge
  o limite total de corrente do inversor
- Ao voltar para a região contínua, continua por até **5 s** antes de
  desativar (mesmo valor do antigo código de rede alemão)

### Tabela 9 — Volt-var de regime permanente vs. DVS

| | Volt-var (§5.3, regime permanente) | DVS (§6.4.2.6, distúrbio) |
|---|---|---|
| Referência de V | absoluta ou média móvel | sempre média móvel |
| Velocidade | lenta (padrão 5 s, ajustável 1–90 s) | rápida (ciclos) |
| Termo popular | "Dynamic Var Support" | "Reactive Current Injection", "Full Dynamic Grid Support" (BDEW) |
| Objetivo | perfil de tensão em regime, colapso pós-contingência | mitigar FIDVR, evitar trip de DER legado |

## Comparação com a ONS_2_11 (Brasil) — ver [[ons-2-11]]

| | IEEE 1547-2018 DVS | ONS Submódulo 2.10 (`ONS_2_11`) |
|---|---|---|
| Obrigatoriedade | Opcional (mútuo acordo) | Mandatória |
| Referência de tensão | Desvio de média móvel pré-evento | Magnitude absoluta de V_pcc |
| Zona de ativação | Dentro da mandatory/permissive operation | V < 0,85 pu ou V > 1,10 pu |
| Prioridade de corrente | Q-priority (idêntico) | Q-priority (`id_max = √(Imax²−iq²)`, idêntico) |
| Hold após recuperação | 5 s | Não implementado (desativa imediatamente com `fault_flag=0`) |

A ONS_2_11 é estruturalmente mais simples (droop linear direto sobre V
absoluto, sem médias móveis) e sempre ativa — mas não tem o "hold" de 5 s do
IEEE, o que é relevante para o "paradoxo detecção vs. injeção" documentado em
[ons_2_11.md](ons_2_11.md): a desativação imediata ao cruzar 0,85 pu pode
coincidir com o momento em que o PLL ainda está instável pós-falta.

## Ver também

- [lvrt.md](lvrt.md) — definição geral de LVRT e ligação com o evento 15/08/2023
- [ons_2_11.md](ons_2_11.md) — implementação real no modelo Simulink
- [ieee1547_case_studies.md](ieee1547_case_studies.md) — estudos de caso reais (CAISO, Entergy) mostrando o impacto de DVS/categoria na recuperação de tensão do sistema
