---
name: chile-2025-overview
description: Apagão total do SEN chileno em 25/fev/2025 — causa raiz (intervenção não autorizada em proteção diferencial), formação de duas ilhas elétricas e colapso, medidas corretivas incl. nova norma GFM/GFL
source: Coordinador Eléctrico Nacional (Chile), Resumen Ejecutivo EAF 089/2025 (19/mar/2025) e apresentação "Análisis del Apagón del 25 de Febrero de 2025" ao Congresso (16/abr/2025)
---

# Apagão Chile 2025 — Visão Geral

Evento **independente** do apagão ibérico ([[iberia-2025-overview]]): apagão total do
Sistema Eléctrico Nacional (SEN) do Chile em 25/fev/2025, 15:16h. Mecanismo de
falha totalmente diferente — intervenção humana não autorizada + malfuncionamento
de proteção, não falha de controle de tensão por IBR. Útil como segundo caso de
apagão total 2025 para contextualizar a motivação do TCC.

## Contexto do SEN

Sistema interconectado desde 2017 (fusão SING norte + SIC centro-sul), ~3.100 km
entre Arica e Chiloé, coordenado pelo Coordinador Eléctrico Nacional (CEN) —
organismo técnico independente sem poder de fiscalização/sanção. Pré-evento:
operação estável, critério N-1, 73% da geração instantânea era solar+eólica;
1.800 MW (~90% da capacidade) fluindo norte→sul pela linha 2×500 kV Nueva
Maitencillo–Nueva Pan de Azúcar.

## Causa raiz

| Hora | Evento |
|---|---|
| 13:35 | Interchile informa ao CDC que desabilitou o módulo de comunicações de uma função de proteção diferencial (87L) de um dos circuitos — linha permanece 100% disponível via proteções de backup |
| 15:13 | Interchile **reinicia a controladora de comunicações sem informar nem pedir autorização** ao Coordinador |
| 15:15–15:16 | Resincronização da proteção causa **disparo indevido** dos dois circuitos 500 kV — risco conhecido no manual do fabricante (disparo espúrio sob falta de sincronismo preciso + altas correntes circulantes) sob as condições de transferência do momento; Interchile não isolou fisicamente o equipamento, como o manual exigia |

Ambos os circuitos abrem quase simultaneamente → SEN se divide em **duas ilhas
elétricas em 1,5 s**, por sobrecarga súbita do sistema paralelo de 220 kV.

## Propagação

- **Ilha Norte** (30% da carga, excedente de geração): esquemas automáticos de
  desconexão de geração (EDAG) mantiveram a ilha operante por **~4 min**, mas
  colapsou por **instabilidade de tensão** — subida de tensão por falta de
  controle de reativo em renováveis variáveis + perda de um equipamento de
  compensação reativa.
- **Ilha Centro-Sul** (70% da carga, déficit de geração de ~1.800 MW): instável em
  **4 s**, desbalanço oferta-demanda de ~25%. EDAC (desprendimento automático de
  carga) ativou, mas ~230 MW de corte não operou corretamente. Frequência
  estabilizou em 48,5 Hz em 3 s, depois caiu a 47,5 Hz (gradiente −0,3 Hz/s) —
  ao cruzar 47,5 Hz, mais geração desconectou, acelerando a queda até o colapso
  total. Simulação com proteções ideais (linha verde) indica que a ilha
  **deveria ter permanecido estável** — a falla real (linha vermelha) diverge
  por desempenho deficiente dos recursos de contingência.
- **Resultado**: apagão total — 11.066,23 MW de carga perdidos (100% do SEN).

## Restauração (PRS)

Plano de Recuperação de Serviço acionado em 2 min; recuperação por formação de
ilhas em 8+ áreas geográficas, cada uma com uma empresa designada como Centro de
Operação para Recuperação (COR — ex.: Transelec, Engie, Enel, ISA, ligado a
partidas autônomas). Atraso principal: **Transelec perdeu SCADA, telecontrole e
voz por ~3h**, justo a empresa que exercia COR em Tarapacá/Norte Chico/Centro/Sul,
responsável por 80% da capacidade nacional de partida autônoma. Sem telecomando,
uma manobra que levaria minutos passa a levar horas (deslocamento físico +
operação manual). Normalização completa: ~7–8h, madrugada de 26/fev.

## Incumprimentos identificados

- **Interchile**: desempenho incorreto do esquema de proteção + intervenção sem
  autorização, apesar do risco conhecido no manual do fabricante.
- **Transelec**: indisponibilidade de SCADA/telecontrole/voz durante papel crítico de COR.
- **EDAC**: desempenho deficiente de alguns esquemas + resposta de geradoras
  (incl. PMGD) abaixo do esperado.
- Empresas que não entregaram informação completa/a tempo, atrasando a investigação.

## Medidas corretivas (14, destaques)

1. Transelec deve ter pessoal em terreno pronto em até 30 min nas subestações-chave.
2. Verificação/ajuste dos recursos EDAC, EDAG e PMGD nas empresas coordenadas.
3. Empresas de distribuição devem migrar esquemas EDAC para alimentadores sem PMGD.
5–7. Inspeção técnica + auditorias formais a Interchile (proteção/comunicações) e Transelec (SCADA/telecom).
8–9. Revisão de ajustes de proteção de PMGD + proposta normativa para requisitos técnicos/monitoramento de PMGD.
**10. Publicação de guia + proposta de modificação normativa para inversores GFM e GFL**, para que
   plantas renováveis possam prestar serviços de suporte à segurança do sistema.
11. Consultoria internacional independente (EPRI) sobre o EAF.
12. Equipe de acadêmicos de universidades chilenas para analisar causas da propagação.
13–14. Revisão metodológica de estudos EDAC/PDCE/PRS + medidas de médio/longo prazo de resiliência.

## Uso no TCC

- Segundo apagão total de 2025 (após Ibéria) motivado por dinâmica rápida em
  rede com alta penetração de IBR — reforça a atualidade do tema, mesmo com
  causa raiz distinta (falha de proteção/humana vs. falha de controle de tensão).
- A medida corretiva nº 10 é evidência regulatória direta: o próprio incidente
  motivou o Chile a **normatizar requisitos de GFM/GFL** — paralelo direto ao
  argumento de motivação do TCC sobre a necessidade de PLLs bem ajustados em
  inversores grid-tied.
- Colapso da ilha centro-sul em 4 s com gradiente de frequência de −0,3 Hz/s é
  referência de ordem de grandeza para cenários de alto RoCoF no modelo IEEE 9
  barras. Ver protocolo de proteções de IBR em [[chile-2025-ibr-protections]].
