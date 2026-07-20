---
name: stability-classification-extended
description: Classificação ESTENDIDA de estabilidade para redes dominadas por IBR (IEEE TR77 + German System Stability Roadmap) — nova categoria converter-driven/resonance stability com interação PLL-rede
source: Strauss-Mincu et al., "Inverter-Dominated Future Power Systems: A Roadmap for System Stability", IEEE Power & Energy Magazine, jan/2026, DOI 10.1109/MPE.2025.3617895, p.1–11
---

# Classificação Estendida de Estabilidade — IEEE TR77 / Roadmap Alemão

Base para a seção 2.3 do TCC. Complementa a taxonomia clássica (ver
[[stability-classification-classic]]) com categorias novas, necessárias
porque redes dominadas por inversores (IBR) mudam a física dos fenômenos de
estabilidade em relação a redes com geração majoritariamente síncrona.

## Contexto: o "German System Stability Roadmap"

Desenvolvido 2022–2023 pelo Ministério Federal de Economia da Alemanha,
adotado pelo governo federal. Referência normativa primária: **IEEE TR77**
("Stability Definitions and Characterization of Dynamic Behavior in Systems
with High Penetration of Power Electronic Interfaced Technologies"). Define
**51 processos** e **18 marcos** até 2030, organizados em 4 grupos de
trabalho (frequência, tensão, ressonância/angular, operação de sistema +
curto-circuito + restauração). Meta: viabilizar rede 100% RES na Alemanha
(carga média 2024: 52,5 GW, 56% coberta por RES).

## As categorias (clássicas expandidas + novas)

### 1. Frequency Stability (expandida)
Transição de inércia rotacional (`J·ω̇`) para **inércia sintética** fornecida
por inversores grid-forming (GFM) via resposta rápida de frequência —
eficácia limitada por atrasos de controle (vs. máquina síncrona real).

### 2. Voltage Stability (expandida)
Novo controle de potência reativa quasi-estacionário vs. dinâmico;
coordenação TSO-DSO necessária porque unidades geradoras distribuídas (DGU)
hoje também precisam contribuir com suporte de tensão.

### 3. Rotor Angle / Angular Stability — **mudança de paradigma**
> "In systems with high shares of RES, small-signal stability is shaped by
> the interactions between inverter-based resources and the propagation of
> oscillations throughout the system... shift in focus from rotor-angle
> stability to the behavior of converters and their control systems."

O conceito de "torque sincronizante" (synchronizing torque) das máquinas
síncronas é substituído por **"synchronizing phase angle power"** — grandeza
baseada no controle de corrente dq dos inversores, necessária para manter
sincronismo em sistemas dominados por IBR. Controles saturáveis (POD,
controle de reativo, limitação de corrente) complicam ainda mais a análise
de small-signal nesses sistemas.

### 4. Resonance Stability + **Converter-Driven Stability** (categoria nova)

A categoria central para o TCC. Combina:
- **Ressonância eletromagnética clássica** (paralela/série), faixa
  ~0,5 Hz a ~2 kHz, agravada porque parques eólicos/fotovoltaicos concentram
  inversores sem propriedades de amortecimento próprias, e a geração síncrona
  restante (quando ausente) deixa de fornecer amortecimento à rede.
- **Converter-Driven Instabilities** (elemento novo): instabilidades
  causadas pela **interação entre o PLL do conversor e a impedância da rede
  (fraca)**. Frequência característica citada: **~10 Hz**. Redução da força
  da rede (menos síncronas) torna os controles eletrônicos de potência mais
  suscetíveis a essas instabilidades.
- **Figura 7 do artigo**: mostra oscilações de potência ativa (20–140 MW) em
  IBGs (inverter-based generation) com **PLL lento vs. PLL rápido** — exemplo
  direto de "inverter driven oscillations" na faixa de ~10 Hz.
- **Mitigação recomendada**: sintonia adequada dos controles do PLL (ajuste
  de Kp/Ki) — mesmo mecanismo de projeto de ganhos discutido em
  [[pll-gains-methodology]] deste TCC.
- Ações do roadmap: critérios/métodos de avaliação padronizados para
  estabilidade de ressonância, requisitos sistêmicos e específicos por
  usuário, procedimentos de certificação/teste, revisão de procurement,
  testes de campo coordenados (ex.: projeto **GFI-Pilot**, piloto de
  inversores grid-forming em redes de distribuição alemãs).

### 5. Short-Circuit Current (categoria operacional nova)
Queda da corrente de curto-circuito instantânea com a redução de síncronas;
inversores contribuem também em níveis de tensão mais baixos. O método
clássico de *short-circuit ratio* é considerado **inadequado** para redes
dominadas por IBR — subestima riscos de estabilidade. Comportamento
transitório/subtransitório dos inversores ainda carece de metodologia clara
de avaliação, tanto para grid-following quanto grid-forming.

### 6. System Operation (decentralização)
Coordenação TSO-DSO torna-se um problema formal de estabilidade (Alemanha:
4 TSOs + ~800 DSOs). Indicadores-chave: robustez, adaptabilidade, capacidade
de recuperação. Resiliência cyberphysical como restrição nova (além da
segurança elétrica clássica).

### 7. Grid and Supply Restoration (categoria operacional nova)
Restauração pós-blackout em redes com alta fração RES: conceito de "areal
power plants" (agregação de informação na distribuição), ilhas de rede de
distribuição operando autonomamente como estratégia de resiliência.

## Relevância direta para o TCC

O artigo **formaliza como categoria oficial de estabilidade** exatamente o
fenômeno estudado neste trabalho: instabilidade guiada por conversor via
interação PLL–impedância de rede, mitigável por sintonia de ganhos do PLL.
Isso dá enquadramento teórico para a seção 2.3 e conecta diretamente com:
- [[srf-pll-theory]] — mecanismo do PLL cuja interação com Zth da rede
  fraca é discutida aqui como fonte formal de instabilidade;
- [[pll-gains-methodology]] — sintonia de Kp/Ki como mitigação citada
  explicitamente pelo roadmap;
- Ver também [[stability-classification-classic]] (JPROC) para a taxonomia
  clássica que esta classificação estende.

## Referências normativas citadas no artigo

- **IEEE TR77** — referência primária de todas as categorias.
- **CIGRE CSE N037**, "Suitable Classification of Power System Stability
  Phenomena" — publicação recente que propõe classificação nova alternativa
  (citada, mas TR77 foi a base do roadmap alemão).
- ENTSO-E R&D Innovation Roadmap 2024–2034; NREL Grid-Forming Inverters
  Roadmap; G-PST Consortium; AEMO NEM Engineering Roadmap FY2024 — roadmaps
  internacionais análogos citados para contexto comparativo.
