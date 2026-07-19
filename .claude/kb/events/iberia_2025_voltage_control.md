---
name: iberia-2025-voltage-control
description: Análise do controle de tensão do apagão ibérico (§4.1) — falha dos recursos de reativo, mecanismo P↓→Q↓→V↑ dos inversores em fator de potência fixo, e o achado de que modelos estáticos subestimam a subida real de tensão
source: ENTSO-E, Grid Incident in Spain and Portugal on 28 April 2025 — Final Report, mar/2026, §4.1 (p.206–231)
---

# Apagão Ibérico 2025 — Controle de Tensão (§4.1)

Análise de por que os recursos de potência reativa da Espanha não conseguiram
conter a subida de tensão de 12:32–12:33 que precedeu o colapso em cascata.
Ver oscilações em [[iberia-2025-oscillations]] e causas raiz em
[[iberia-2025-root-causes]].

## 4.1.2 — Recursos de potência reativa: por que nada respondeu

Três modos de controle de reativo definidos pelo relatório (NC RfG Art. 21):
**controle de Q** (setpoint em MVAr), **controle de V** (setpoint de tensão) e
**fator de potência fixo** (Q proporcional a P instantâneo).

- **RES espanholas (inversorizadas)**: travadas em **fator de potência fixo**
  (RD 413/2014, faixa 0,98 ind.–0,98 cap.), sem exceção prática — eram
  majoritariamente pré-RfG, isentas da obrigação dos 3 modos. Consequência
  dupla: (1) toda rampa de P vira rampa de Q, injetando tensão na rede; (2) Q
  não responde a condições de rede — zero suporte a flutuações de tensão.
- **Síncronos convencionais > 30 MW**: regidos pelo **PO 7.4 (2000)**,
  procedimento operacional que calcula Q de referência via função
  Q(U-atual, P-instalada, U-referência), com referência de tensão do sistema
  fixada em 405–410 kV. Cumprimento exigido em apenas 75% das amostras
  horárias (9 de 12); sem penalidade econômica aplicada na prática (regime
  não desenvolvido); sem definição explícita de velocidade de resposta.
  Alguns geradores participavam voluntariamente de um **projeto-piloto** com
  setpoint direto de tensão enviado a cada minuto — a maioria não.
- **Reatores shunt** (~90 unidades, 13.300 MVAr): operação **manual** na
  Espanha (RTE na França tem ~50% automatizado, resposta 5–10 s). Sem tempo
  de decisão hábil para responder a uma subida de ~1 minuto.
- **STATCOM**: apenas **1 em operação** no dia; outro em testes de comissionamento.
- **HVDC Espanha–França** (2×1000 MW VSC): fazia controle de tensão em ambos
  os terminais — perdido integralmente quando o elo desconectou após o
  blackout ibérico (inclusive no lado francês, que seguiu energizado).

Comparação com Portugal: síncronos recebem setpoint de V ou Q por telefone
direto do TSO; RES (solar > 1 MW, eólica nova) recebem setpoint em tempo real
via SCADA, tipicamente de tensão; **PV solar faz controle de tensão inclusive
à noite**, sem geração ativa.

**Tabela 4-2 (resumo)**: de todos os ativos, RES tinha a maior capacidade
remanescente não utilizada — equivalente a 7 reatores de 150 MVAr às
12:33:00, contra 3 equivalentes para os geradores PO 7.4.

## 4.1.3 — Gestão de tensão: fatores concorrentes

- Margem de segurança **inexistente**: limite operacional 435 kV coincidia
  com o limiar de desconexão automática de geradores pré-RfG (435 kV); pós-RfG
  tinha 5 kV de margem (440 kV). Faixa espanhola (435 kV) é exceção europeia —
  demais EM operam até 420 kV.
- 1.026 alarmes de subtensão e 137 de sobretensão entre 12:00–12:30 (parte
  por oscilação). O primeiro alarme de 430 kV pós-12:30 disparou às 12:33:01
  — **15 s antes** da 2ª desconexão em cascata, tempo insuficiente para ação manual.
  SCADA não distingue tensão por fase (relevante: assimetria de até 9 kV entre fases).
  Não havia handbook formal de ações corretivas de tensão (Portugal/REN tinha).
- Às 12:30, a região sudoeste (Andaluzia/Castilla-La Mancha/Extremadura) tinha
  apenas 1 nuclear (~1.000 MW), 2 CCGT (~800 MW) e 1 hídrica (~70 MW)
  conectados como síncronos — **o resto era 100% inversorizado**.
  Despacho emergencial de CCGT adicional (12:26, para reforçar amortecimento
  via PSS) chegou tarde: partida de CCGT leva 2–8 h.
- Desconexões rápidas de RES (dentro dos limites de tensão) e ciclos de
  desconexão/reconexão de PV doméstica após cada oscilação agravaram ainda
  mais a tensão.

## 4.1.4 — Cronologia e o mecanismo da subida de tensão

**Manhã (09:00–12:00)**: picos pontuais (433 kV às 10:49; 435,7 kV às 11:47,
0,7 kV acima do limite por segundos).

**12:00–12:30**: oscilações de até 30 kV pico-a-pico em 400 kV (ver
[[iberia-2025-oscillations]]). Ações de amortecimento: 6 linhas conectadas
(12:00–12:20); 3 reatores desconectados por baixa tensão + 4 linhas 400 kV
conectadas (12:20–12:25, protocolo bilateral "oscillation and low damping");
5 reatores conectados (700 MVAr, 12:25–12:29) — tensão volta à faixa até 12:30.

**Mecanismo de retroalimentação positiva (12:30–12:33)**: mudança de
despacho (~0,4–0,5 GW, redução de exportação Espanha→Portugal) + aFRR
descendente (até 0,4 GW) reduziram P das RES. Como operam em **fator de
potência fixo indutivo**, redução de P → redução proporcional de absorção de
Q → **tensão sobe ainda mais** — o mesmo mecanismo que impede resposta à
oscilação agora amplifica a rampa de despacho.

- **Evento "A" — 400 kV TS1 Granada** (12:32:57, 1ª desconexão por
  sobretensão): tensão subiu de 400,6→417,2 kV em 1 min (22,6 kV/min); Q
  subiu de −165→−96 MVAr (+94 MVAr/min); sensibilidade **0,24 kV por MVAr**.
  3 geradores RES (150 MW) reduziram P em 78,8 MW (123,4→41,6 MW) em 24 s,
  reduzindo absorção de Q em 33,3 MVAr. Transformador 400/220 kV disparou por
  sobretensão no lado 220 kV (tap fixo durante a subida rápida → relação de
  transformação amplificou a tensão pu no lado 220 kV) — proteção sem atraso
  (1,1 pu, 0 s), não coordenada com a proteção de transmissão.
- **Evento "B" — 400 kV TS1 Badajoz** (19 s depois): mais 165 MVAr de
  absorção perdidos. Assimetria de fase de até ~9 kV observada (fase B mais alta).
- Após "B": mais 12 desconexões por sobretensão em 2,5 s → cascata →
  fenômenos de frequência → blackout.
- **Precursor 22 de abril**: evento quase idêntico (queda de 1,6 GW na
  posição comercial + solar caindo ao entardecer + convencionais entrando),
  pico de 452 kV (455 kV fase B) em ARN4ALD — mas **sem oscilação prévia**,
  não escalou a incidente.

## 4.1.5 — Análises de sensibilidade: o modelo estático subestima o real

Coreso rodou sensibilidades em modelos estáticos (RTSN, formatos UCTE/CGMES),
com a limitação central de que **análises dinâmicas não são possíveis** nesse
tipo de modelo.

- Setpoint de tensão 407,5 kV nas RES → dispersão de tensão cai (IQR
  6,6→3,6 kV em UCTE; 8,5→7,9 kV em CGMES) — confirma que sair do FP fixo ajudaria.
- Variação de tap em TS1 Granada: +1,19 kV/tap (lado 220 kV), −0,78 kV/tap
  (lado 400 kV) — CGMES.
- Reator shunt em TS1 Badajoz: 3–4 kV por 150 MVAr (0,023 kV/MVAr).
- **Achado crítico**: variação máxima de tensão calculada por injeção de P/Q
  em TS1 Granada foi de **3–4 kV**, contra **16–17 kV medidos no SCADA real**
  — o modelo estático subestima em ~4–5× o efeito observado.

## Uso no TCC

- O mecanismo P↓→Q↓→V↑ em FP fixo é o caso real do que a dissertação testa
  em simulação dinâmica com o SRF-PLL: resposta de inversor GFL sob rampa de
  despacho/RoCoF, não apenas sob falta.
- O achado "modelo estático 3–4 kV vs. real 16–17 kV" é citação direta para
  justificar a escolha metodológica de simulação **EMT/dinâmica** (vs.
  fluxo de potência) no Cap. 3 — o próprio ENTSO-E documenta a limitação do
  modelo estático no evento real.
- Contraste RES-Espanha (FP fixo, sem resposta) vs. RES-Portugal (setpoint
  de V em tempo real, inclusive à noite) é material de discussão para
  recomendações de modo de controle do inversor — ver [[iberia-2025-ibr-lessons]].
- Sensibilidade de tensão medida em campo (0,24 kV/MVAr, TS1 Granada) é
  referência de ordem de grandeza para validar a resposta de Q do modelo
  IEEE 9 barras sob variação de despacho.
