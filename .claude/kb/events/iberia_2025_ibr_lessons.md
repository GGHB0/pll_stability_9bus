---
name: iberia-2025-ibr-lessons
description: Lições do apagão ibérico 2025 para recursos inversorizados (IBR) — converter-driven instability, trips de inversores, recomendações e paralelo com o TCC
source: ENTSO-E, Grid Incident in Spain and Portugal on 28 April 2025 — Final Report, mar/2026, §4.2, §4.3, §9.3–9.4
---

# Apagão Ibérico 2025 — Lições para Recursos Inversorizados

## Papel dos IBR no evento

- A geração desconectada na cascata era **majoritariamente inversorizada**
  (PV, eólica, termossolar): > 2,5 GW em ~78 s.
- **Oscilação forçada de 0,63 Hz** classificada como *converter-driven
  instability* interagindo com outros geradores da área — controle de
  conversor (malhas de sincronização/corrente) como fonte de instabilidade,
  o mesmo domínio físico investigado no TCC via SRF-PLL.
- RES em **fator de potência fixo**: nenhum suporte dinâmico de tensão;
  rampas de P viravam rampas de Q (e de tensão).
- **Inversores de PV < 1 MW** (rooftop) desligaram por proteção de
  sobretensão durante rampas e flutuações de tensão; o tempo de reconexão
  (~4 min na estimativa) amplificou a perda de geração. Correlação medida
  entre tensão na rede 400 kV, fluxos TSO–DSO e proporção de trips.
- Ajustes de proteção de sobretensão de usinas utility-scale **abaixo dos
  requisitos** ou medidos longe do ponto de conexão, alguns com trip
  instantâneo sem temporização.

## Recomendações mais relevantes ao TCC (R250428_x)

| # | Tema | Essência |
|---|---|---|
| 1 | Modo de controle de tensão | Geradores devem operar em voltage control mode (não FP fixo); explorar regulação zonal automática de Q |
| 2 | Adequação de reativo | Margens estáticas + dinâmicas de Q dimensionadas para rampas rápidas de tensão |
| 3 | Ativação automática | Automatizar reatores shunt; considerar STATCOMs/reatores variáveis |
| 4 | Faixa de tensão | Aplicar faixa harmonizada 380–420 kV (SO GL) — margem até a desconexão |
| 5 | Rampas | Limitar rampas de P de unidades com FP fixo (rampa de P = rampa de Q) |
| 6 | Inter-área | Framework CE SA de amortecimento: PSS/POD, modelos dinâmicos compartilhados; priorizar POD-P/Q em IBR, condensadores síncronos, STATCOMs |
| 7 | Monitoramento | PMUs + detecção automática de oscilações (inter-área e forçadas) com localização de fonte |
| 8 | Proteções | Validar ajustes de sobre/subtensão e temporizações (≥ 100 ms, até > 1 s) vs requisitos |
| 9 | HVRT tipo A | Criar requisito de high-voltage ride-through com perfil V×t para módulos tipo A (PV pequeno) |
| 10 | Verificação contínua | Auditar comportamento real de ride-through (HVRT/LVRT/RoCoF) após cada trip |
| 11 | DER não observável | Investigar desconexão/reconexão de inversores < 1 MW com fabricantes |

Demais (12–21): STATCOM-mode de HVDC sem transferência ativa, snapshot de
modelo comum pós-evento, governança de dados, LFDD ciente de DER, defesa
modernizada p/ fenômenos rápidos de tensão, testes reais de black-start,
reconexão controlada de DER, treinos conjuntos, comunicação à prova de
blackout por 24 h.

## Paralelo com o apagão BR de 15/ago/2023

| Aspecto | Brasil ago/2023 | Ibéria abr/2025 |
|---|---|---|
| Gatilho | Abertura de linha 500 kV (Quixadá–Fortaleza II) | Subida descontrolada de tensão |
| Fenômeno dominante | Desconexão em cascata de eólicas/PV por atuação de proteções durante transitório | Cascata de trips por sobretensão, maioria IBR |
| Papel do controle do conversor | Suspeita de resposta inadequada de controles (foco do TCC: PLL) | Converter-driven forced oscillation confirmada (0,63 Hz) |
| Perda | 23.368 MW (~34,5 % da carga do SIN) | > 2,5 GW pré-colapso; blackout total ES/PT |
| Lição comum | Comportamento de IBR sob contingência severa e ajustes de proteção determinam se o distúrbio se contém ou cascateia | idem |

## Uso no TCC

- **Motivação (Cap. 1)**: segundo grande evento mundial recente com IBR como
  protagonista — reforça a relevância de estudar a dinâmica do SRF-PLL sob
  contingências severas (o evento BR de 2023 já é a motivação principal).
- **Cenários (Cap. 4)**: o relatório documenta afundamento/elevação de tensão,
  salto de ângulo (~80° de ângulo de transmissão) e RoCoF > 1 Hz/s — os mesmos
  tipos de contingência simulados no modelo IEEE 9 barras.
- Citar como: ENTSO-E ICS Investigation Expert Panel, *Grid Incident in Spain
  and Portugal on 28 April 2025 — Final Report*, 2026.

Ver [[iberia-2025-overview]], [[iberia-2025-root-causes]].
