---
name: brasil-2023-overview
description: Blecaute do SIN em 15/08/2023 — linha do tempo, condições pré-evento e formação de ilhas elétricas (relatório RAP-ONS 00012/2023)
source: ONS, RAP-ONS 00012/2023 — Análise da Perturbação do dia 15/08/2023 às 08h30min, §1–§2, §4, §5.6
---

# Blecaute Brasil — 15 de Agosto de 2023

Motivador central do TCC. Perda de **23.368 MW** de carga do SIN (34,5% da
carga do sistema): 12.689 MW nas macrorregiões Norte/Nordeste e 10.680 MW em
S/SE/CO. Roraima permaneceu isolado do SIN (não afetado). Analisado pelo ONS
em relatório de 572 páginas (RAP-ONS 00012/2023).

## Mecanismo em uma frase

Abertura acidental de 1 linha de transmissão por **atuação indevida de
proteção** (sem curto-circuito) → afundamento de tensão em cascata na região
Nordeste → desligamentos automáticos por proteção de distância/perda de
sincronismo → separação do SIN em ilhas elétricas → colapso de algumas ilhas
por desempenho de suporte de reativo dos parques eólicos/fotovoltaicos muito
abaixo do modelado.

## Condições pré-evento (manhã de 15/08)

- ~05h30: início da geração fotovoltaica no Nordeste, elevando o fluxo
  Norte-Sul (FNS).
- 07h32: ONS desbloqueia o Bipolo Xingu–Terminal Rio para escoar a geração
  renovável do Nordeste; rampas elevam o bipolo de 400→2.000 MW (polo 3/4) e
  o Bipolo Xingu–Estreito de 960→1.150 MW. FNS cai de 2.180 MW para 550 MW.
- ~08h02: geração eólica no Ceará soma-se à fotovoltaica e leva o fluxo
  Nordeste-Norte (FNEN) a ~6.000 MW, violando o limite operativo de 5.800 MW
  (imposto por indisponibilidade temporária de equipamento na SE São João do
  Piauí); ONS reduz a violação para 79 MW via redespacho antes do evento.
- **08h30min36,944s**: a LT 500 kV Quixadá–Fortaleza II atinge seu maior
  carregamento histórico — **1.950 MW**.

## O evento disparador

- **T0 = 08h30min36,946s** — desligamento da LT 500 kV Quixadá–Fortaleza II
  **só no terminal de Quixadá**, por atuação acidental da proteção de
  fechamento sob falta (**Switch Onto Fault — SOTF**) durante operação
  normal da linha (sem curto-circuito real). Também houve atuação incorreta
  do esquema de religamento automático da linha.
- Consequência imediata: parte do fluxo que ia pelo tronco de 500 kV migra
  para o tronco de 230 kV paralelo (Milagres–Fortaleza), sobrecarregando-o.
- **T0+530 ms**: proteção de perda de sincronismo (78) abre a LT 500 kV
  Presidente Dutra–Boa Esperança (SE Presidente Dutra), levando junto (SEP
  4.14.11) as LTs Presidente Dutra–Imperatriz C2 e Presidente Dutra–Teresina
  C1/C2.
- **T0+570 ms**: proteção de distância Zona 1 abre a LT 230 kV Milagres–Icó
  — no desligamento, tensão registrada V = 0,54 pu e corrente 897 A
  (limite normal 810 A).
- Cascata de dezenas de desligamentos por proteção de distância (Zonas 1/2) e
  teleproteção (POTT) na região Nordeste ao longo do primeiro ~1,9 s — ver
  [[brasil-2023-root-causes]] para a árvore de causas completa.

## Separação em ilhas elétricas

O SIN se dividiu em 4 subsistemas, cada um com dinâmica própria:

| Ilha | Separação (desde T0) | Condição | Desfecho |
|---|---|---|---|
| Norte | ~2,6 s | Subfrequência | ERAC atua, mas unidades geradoras desligam → colapso |
| Acre/Rondônia | ~3,5 s | Sobrefrequência + sobretensão | Desligamento de LTs, síncronos e unidades → colapso |
| Parte do Nordeste | ~19,8 s | Sobrefrequência + sobretensão sistêmica | Desligamentos por sobretensão, **mas estabiliza** — ilha remanescente com hidráulicas + eólicas/fotovoltaicas em equilíbrio |
| Sul/SE/CO/Sudoeste BA | — | — | Permanece estável; ERAC restabelece equilíbrio carga-geração |

## Restauração

- 8h43–9h05: restabelecimento do Subsistema Sul.
- 8h52–9h33: restabelecimento do Subsistema Sudeste.
- Black-start em Tucuruí (PA), Balbina (Manaus), Coaracy Nunes (AP), Estreito
  (MA) e Samuel (RO); dificuldades de controle de frequência e múltiplas
  tentativas falhas (ex.: 4 tentativas sem sucesso em Coaracy Nunes).
- 14h49: ONS autoriza restabelecimento total das cargas.
- Diversas falhas operacionais registradas: telecomando indisponível em
  várias subestações, falhas de comunicação/hotline, manobras sem
  coordenação prévia com o ONS, recomposição de cargas por distribuidoras
  antes da estabilização formal da frequência (reincidência de anormalidade
  já vista em 2021/2022).

## Relevância para o TCC

Evento fundador da motivação do trabalho (ver [[iberia-2025-overview]] e
[[chile-2025-overview]] para os paralelos de 2025). Assim como na Ibéria, o
gatilho foi um evento de rede relativamente comum (aqui, um trip acidental
sem curto-circuito) que se tornou severo por causa do desempenho inadequado
do suporte dinâmico de tensão dos IBR — não por falta de inércia ou de
potência de curto-circuito (ver conclusões do ONS em
[[brasil-2023-root-causes]]).
