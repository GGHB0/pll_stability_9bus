---
name: iberia-2025-root-causes
description: Árvore de causa raiz do apagão ibérico de 28/abr/2025 — falha de controle de tensão, oscilações 0,63 Hz (converter-driven) e 0,2 Hz (inter-área)
source: ENTSO-E, Grid Incident in Spain and Portugal on 28 April 2025 — Final Report, mar/2026, §1.4, §4.6 (p.331–334)
---

# Apagão Ibérico 2025 — Causas Raiz

Metodologia: Root Cause Analysis ("cinco porquês") a partir de "por que houve
blackout em 28/abr/2025?". A árvore (Fig. 4-124/9-1 do relatório) tem duas
partes: base = fatores que causaram a **subida rápida de tensão**; topo =
sequência final (defesa do sistema → perda de sincronismo → colapso).

## Fatores da subida rápida de tensão (numeração do relatório)

1. **Reativo dos síncronos abaixo do exigido** — várias unidades convencionais
   atingiram o Q-reference em menos de 75 % das amostras horárias (PO 7.4);
   mais absorção teria segurado a tensão.
2. **Quadro regulatório sem critério dinâmico nem penalidade** — a PO 7.4 não
   especificava comportamento dinâmico de tensão e o esquema econômico de
   penalidades nunca foi implementado.
3. **RES com fator de potência fixo** — Q proporcional a P: (i) toda mudança
   de despacho gerava degrau de reativo (e de tensão); (ii) nenhuma resposta
   de reativo às flutuações de tensão da rede.
4. **Controle de tensão das redes coletoras mal projetado** — redes internas
   de usinas (atrás do ponto de conexão) com controle/ajustes de desconexão
   desalinhados do sistema; unidades caíram com tensão ainda dentro dos
   limites no ponto de conexão.
5. **Sem limite de rampa para geradores com FP fixo** — rampas rápidas de P
   ↓ ⇒ perda rápida de absorção de Q ⇒ subida rápida de tensão.
6. **Reatores shunt manuais** — religamento exige decisão + tempo de manobra;
   a tensão subiu rápido demais para a atuação manual.
7. **Ajustes de proteção de sobretensão divergentes dos requisitos** —
   unidades/trafos/linhas desligaram antes das condições de tensão e de
   temporização no ponto de conexão serem atingidas (≥ 10 desconexões
   comprovadamente fora dos requisitos).
8. **Instabilidade guiada por conversor (converter-driven)** — interação com
   outros geradores da mesma área produziu a oscilação forçada de 0,63 Hz.
9. **Ausência/insuficiência de PSS** em grandes unidades síncronas.
10. **As duas oscilações** — mitigá-las era prioridade operacional, mas as
    medidas (redução de intercâmbio, religar linhas) elevaram a tensão.
11. **Trips de PV < 1 MW por sobretensão** na baixa tensão (dados de 2
    fabricantes de inversores) → mudança do padrão de fluxo TSO–DSO.
12. **Faixa de tensão 400 kV mais larga na Espanha** (380–435 kV vs 380–420 kV
    harmonizado) — margem pequena ou nula até a tensão de desconexão dos
    geradores (435/440 kV).
13. **Corte de carga/bombas aumentou a tensão** — desligar consumidores que
    absorviam reativo agravou a sobretensão (embora tenha ajudado a frequência).
14. **Cascata venceu a defesa** — perda de geração por sobretensão +
    subfrequência superou o corte de carga; frequência seguiu caindo até o
    colapso.

## As duas oscilações (análise §4.2)

- **0,63 Hz (12:03–12:08)** — oscilação **forçada**, não é modo natural do
  sistema; localizada na Ibéria, maior atividade entre Carmona e Almaraz.
  Junto ao nó de maior amplitude há uma usina inversorizada ("existing
  generator" no quadro espanhol). Conclusão: *converter-driven forced
  oscillation*. As medidas do operador (não projetadas p/ essa faixa) tiveram
  efeito positivo menor.
- **0,2 Hz (12:19–12:22)** — inter-área clássica, modo Leste-Centro-Oeste.
  Precondições na Ibéria: ângulo de transmissão ~80° (Carmona ↔ S. Llogaia),
  linhas fora de serviço, ausência de PSS em grandes unidades, amortecimento
  insuficiente. Simulações mostram que o modo 0,63 Hz pode ter contribuído
  para excitar o 0,2 Hz. Medidas operacionais foram eficazes.

## Sequência final (topo da árvore)

Cascata de desconexões por sobretensão → queda de frequência ES/PT + aumento
do ângulo com a CE SA + reversão de fluxo na fronteira FR-ES + queda do torque
sincronizante → **"ponto de não retorno"** (perda de sincronismo) → DRS abre
ES–FR, SPS de frequência abre ES–MA → blackout ES e PT.

Nota da análise de inércia (§1.4.4): mesmo com inércia significativamente
maior, a perda de sincronismo **não teria sido evitada** — o torque
sincronizante caiu rápido demais com a cascata de trips.

Conclusão-chave do painel: o fenômeno central foi a **inefetividade do
controle de tensão** no sistema espanhol; simulações mostram que maiores
margens de reativo teriam evitado o colapso. Ver [[iberia-2025-overview]] e
[[iberia-2025-ibr-lessons]].
