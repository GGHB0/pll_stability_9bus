---
name: iberia-2025-oscillations
description: Análise modal das oscilações do apagão ibérico (§4.2) — classificação da 0,63 Hz como forçada converter-driven, ressonância com o modo inter-área 0,2 Hz e sensibilidades de amortecimento
source: ENTSO-E, Grid Incident in Spain and Portugal on 28 April 2025 — Final Report, mar/2026, §4.2 (p.231–277)
---

# Apagão Ibérico 2025 — Análise das Oscilações (§4.2)

Análise detalhada dos dois episódios oscilatórios de 12:00–12:30 que
precederam o colapso. Ver contexto em [[iberia-2025-overview]] e
[[iberia-2025-root-causes]].

## Metodologia

- Modelo dinâmico completo da **CE SA** ("Dynamic model of continental
  Europe v2") + modelo detalhado do sistema peninsular espanhol (SPES) via
  estimador de estado — snapshots de 12:21 (inter-área) e 12:08:30 (0,63 Hz).
- Duas técnicas complementares: **análise de autovalores** (DIgSILENT
  PowerFactory) e **simulação RMS** fasorial.
- Cargas: modelo IZ (P = corrente constante, Q = impedância constante).
- Oscilação ambiente reproduzida com processo estocástico de
  **Ornstein–Uhlenbeck** nas cargas — inter-área dispara até sem contingência.
- A 0,63 Hz **não aparece no modelo** (nenhum modo mal amortecido em
  0,4–0,8 Hz) → reproduzida injetando sinal sintético de P/Q no nó ativo
  (reconstruído de PMU vizinha + médias SCADA).

## Classificação da 0,63 Hz: forçada, converter-driven

Cadeia de evidências (métodos independentes, todos convergentes):

1. **Análise modal UKF** (Unscented Kalman Filter) em 128 medidas PMU de
   100 ms: modo 0,63 Hz dominante, confinado à Península Ibérica; mode shape
   atípico (não inter-área), maior atividade de tensão entre Carmona e
   Almaraz (Fig. 4-26 a 4-28).
2. **Histórico jan–abr/2025** (janelas de 20 min): 0,63 Hz **não é modo
   natural** do sistema. Em 28/abr, ocorrências em Carmona: 48 (10–11h) →
   140 (11–12h) → 101 (12–13h, de 101 possíveis). FSSI em 4 PMUs confirma
   ausência de modo 0,6 Hz nos dias normais de abril.
3. **Método DEF** (Dissipative Energy Flow, 12:00–12:15): Ibéria exporta
   energia de oscilação para França (DEF 2,39) e Marrocos (1,16); área
   fonte candidata no interior (DEF 0,5).
4. **Harmônicas da forçada**: 2ª harmônica (1,26 Hz) presente em P e Q
   (3,2 % / 1,2 % da fundamental); maior observabilidade na PMU
   Almaraz–Bienvenida, junto ao gerador da região de **Badajoz**.
5. **Método SCADA da IEEE Forced Oscillation Task Force** (código aberto da
   RTE) sobre 144 geradores > 50 MW: converge para o mesmo gerador de
   Badajoz; correlação clara de Q com a oscilação 0,63 Hz.

Perfil da usina fonte ("plant A"): inversorizada, grande porte,
classificada como *existing generator* (pré-código RfG — sem os requisitos
modernos); durante 12:03–12:15 operava **limitada** (curtailment, potência
intermediária) — condição conhecida na literatura por instabilidade em
inversores antigos. Às 12:16, ao subir o setpoint de P, a oscilação
diminuiu. Conclusão: fenômeno **converter-driven** induziu oscilação
forçada; a usina interagiu com os demais geradores da área e dominou a
oscilação.

## Prova da origem forçada e ressonância entre modos

- **Decaimento em ~10 s**: interrompendo a injeção sintética na simulação,
  as oscilações amortecem quase imediatamente (Fig. 4-50) — o modo não é
  intrínseco à rede.
- **Ressonância 0,63 → 0,2 Hz**: com amortecimento inter-área baixo
  (ζ = 0,28 % no caso real A₀), a forçada **excita o modo inter-área**
  (Fig. 4-51); a FFT de janela deslizante mostra a componente 0,2 Hz
  crescendo ao longo da simulação enquanto a 0,63 Hz domina o início.
- Corolário do relatório: oscilação forçada só é totalmente eliminada
  **desconectando a fonte**; medidas de amortecimento eletromecânico
  (POD, redução de intercâmbio, manobras) ajudam apenas na componente
  eletromecânica excitada.

## Oscilação inter-área 0,2 Hz (12:19–12:22)

Modo Leste-Centro-Oeste clássico da CE SA (menor amortecimento médio do
sistema). Precondições: ângulo de transmissão ~80° (Carmona ↔ S. Llogaia),
linhas fora de serviço, PSS insuficientes. Ibéria + Turquia oscilam contra
o centro da Europa (~180°).

## Sensibilidades de amortecimento (caso base A₀: ζ = 0,28 %, f = 0,20 Hz)

| Medida | Δζ (%) | Obs |
|---|---|---|
| HVDC INELFE-1: ADC→CPC + 500 MW/link + reduzir ES–FR | +1,30 (de −1,03 a +0,28) | ações reais do operador (Tab. 4-6) |
| POD-P + POD-Q do INELFE-1 ligados | +2,46 | POD-Q > POD-P neste cenário (Tab. 4-7) |
| Ganho POD-P 500 → 2.500 MW/Hz/link (retrofit 2022) | +0,30 → +0,46 | Tab. 4-8 |
| Religamento de linhas (manobras reais) | +0,20 | Tab. 4-9 |
| STATCOM Vitória 150 Mvar com POD-Q | evita −0,08 (V-mode); +0,06 (Q-mode) | Tab. 4-10/4-11 |
| PSS de todas as CCGTs desligados | **−1,12** | criticidade dos PSS (Tab. 4-12) |
| PSS (hipotético) nas nucleares | +1,27 | Tab. 4-13 |
| +5 geradores síncronos com PSS | +1,12 | Tab. 4-14 |
| Inércia 2×/3× | +0,93 / +2,76 | **insuficiente sozinha** (Tab. 4-15) |
| Fluxo AC ES–FR −400 MW / +450 MW | +0,90 / −0,79 | Tab. 4-16 |
| 8 condensadores síncronos (plano MAP2) | +0,69 | H = 6 s @ 250 MVA cada (Tab. 4-17) |
| 4 STATCOMs com POD-Q | +0,53 | Tab. 4-18 |
| 2 VSCs GFL 100 MVA com POD-P/Q (Carmona + La Cereal) | **+1,84** | POD-P > POD-Q; BESS/E-STATCOM (Tab. 4-19) |
| Cenário futuro combinado (SCs + STATCOMs + VSCs + POD-Q HVDC) | +2,62 | Tab. 4-20 |

Nota: o POD-Q do INELFE-1 foi **auto-desabilitado** durante a 0,63 Hz
(saturações repetidas nos limites) e ficou fora na inter-área seguinte,
quando teria sido valioso — recomendação de alarme/reativação automática.

## Ações sistêmicas recomendadas (conclusão da §4.2.5.4)

1. Inspeções e testes de campo coordenados pelos TSOs para certificar
   estabilidade de geradores, BESS e novas cargas (eletrolisadores, data
   centers); 2. intensificar monitoramento de alta frequência e qualidade
   de energia por usina; 3. **aprofundar converter-driven instability com
   estudos de sistema e ensaios de laboratório**; 4. estudar sistemas de
   defesa com ações automáticas de contenção; 5. tuning periódico de
   PSS/POD; 6. melhorar monitoração e controles de usinas existentes;
   7. estender obrigatoriedade de PSS a usinas com sensibilidade relevante;
   8. reforçar requisitos anti converter-driven para demanda/geração/HVDC/
   FACTS.

## Uso no TCC

- A cadeia de evidências (modal + DEF + harmônicas + SCADA) é referência
  metodológica para caracterizar oscilações de origem inversorizada —
  dialoga com o espectro dq segmentado do dashboard.
- A ressonância forçada→inter-área é candidata a cenário do Cap. 4:
  inversor GFL com sintonia inadequada (cenário BAD_PLL) injetando
  oscilação sustentada em rede com modo pouco amortecido.
- O achado "inércia não resolve" reforça a motivação de estudar o PLL
  (controle), não apenas inércia — ver kb/power-system/virtual_inertia.
- Ver também [[iberia-2025-ibr-lessons]] para as recomendações gerais.
