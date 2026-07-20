---
name: brasil-2023-root-causes
description: Conclusões oficiais do ONS sobre o blecaute de 15/08/2023 — cadeia de causa raiz e descarte de inércia/potência de curto-circuito como fator determinante
source: ONS, RAP-ONS 00012/2023, §7 Conclusões (p.370–379)
---

# Blecaute Brasil 2023 — Causas Raiz e Conclusões do ONS

Ver [[brasil-2023-overview]] para linha do tempo e contexto pré-evento.

## Cadeia de causa raiz (§7.1–7.9 do relatório)

1. Abertura da LT 500 kV Quixadá–Fortaleza II por atuação **acidental** da
   proteção SOTF (Switch Onto Fault) — sem curto-circuito real — durante
   operação normal, mais falha do esquema de religamento automático.
2. Redistribuição do fluxo de potência no Subsistema Nordeste →
   **afundamento de tensão** no tronco de 230 kV do Ceará e em subestações
   de 500 kV (Boa Esperança, Buritirama, Queimada Nova 2, Açu III, Campo
   Grande III).
3. Abertura da LT 500 kV Presidente Dutra–Boa Esperança por **proteção de
   perda de sincronismo (PPS)** — arrasta junto Presidente Dutra–Teresina II
   C1/C2 e Presidente Dutra–Imperatriz C2.
4. Afundamento de tensão + aumento de fluxo de reativo no tronco 230 kV
   (Aquiraz–Milagres) → atuação de **proteções de distância**, desligando
   mais linhas nesse tronco.
5. Nova configuração operativa aumenta carregamento de linhas remanescentes
   → início de **oscilação de potência** → perda de sincronismo entre áreas
   e instabilidades locais.
6. Mais desligamentos por proteção de distância e por **PPS** (disparo por
   oscilação de potência), separando progressivamente os subsistemas fora
   de sincronismo.
7. Desligamentos automáticos + perda de carga natural + atuação do ERAC →
   **sobretensões** em regiões do Nordeste → proteções de sobretensão
   sistêmicas desligam mais linhas e bancos de capacitores shunt.
8. Resultado: SIN se separa em 4 ilhas elétricas (Norte, Acre/Rondônia,
   parte do Nordeste, S/SE/CO/Sudoeste-BA) — cada uma com desfecho próprio
   (ver tabela em [[brasil-2023-overview]]).

## Fator determinante identificado pelo ONS (§7.10)

> "O desempenho dos controles em campo, de usinas eólicas e fotovoltaicas,
> em especial no que tange à capacidade de suporte dinâmico de potência
> reativa, foi muito aquém dos modelos matemáticos fornecidos pelos
> agentes" (§7.10).

Essa discrepância entre o modelo declarado pelos agentes (usado nos estudos
pré-operacionais do ONS) e o desempenho real em campo impediu que o ONS
antecipasse o risco do cenário operativo pré-distúrbio. O ONS recomenda
providências aos agentes eólicos/fotovoltaicos para corrigir a
representatividade dos modelos (§7.11) — é exatamente o tipo de gap entre
"modelo de controle declarado" e "comportamento dinâmico real do PLL/malhas
de corrente" que este TCC busca investigar em ambiente simulado.

## O que o ONS descarta como causa (§7.44, "esclarecimentos adicionais")

- **Inércia**: SIN operava com ~265 GW·s de inércia total para ~73 GW de
  carga — proporção inércia/carga *acima* da observada em vários sistemas
  internacionais (referência: JWG C2/C4.41 do Cigre, 2020). "Não há relação
  direta da ocorrência da perturbação com a inércia sistêmica"; o colapso
  foi de **tensão**, não de frequência, e a resposta inercial não teria
  evitado o fenômeno.
- **Potência de curto-circuito**: nível considerado adequado a todos os
  critérios dos Procedimentos de Rede; mais máquinas síncronas na região
  não teria agregado margem de estabilidade para este fenômeno específico.
  Aumentar SCC ajudaria a explorar mais os limites de transmissão, mas "o
  sistema permaneceria em risco similar" enquanto persistir a discrepância
  de suporte de reativo das usinas eólicas/fotovoltaicas.
- **Abertura angular / oscilação de potência**: não houve oscilação de
  potência nos instantes iniciais; a abertura angular observada foi
  consequência da queda de tensão e do impacto na transferência de
  potência entre áreas, não causa primária.
- Conclusão do ONS: a causa não está relacionada ao *tipo de fonte* nem ao
  *número de síncronas em operação*, e sim à discrepância modelo↔campo no
  suporte dinâmico de reativo dos IBR.

## Contexto de transição energética (§7.45)

O próprio relatório enquadra o evento como parte dos "aprendizados
associados à transição energética, desafiando os operadores de sistemas
elétricos por todo o mundo" — paralelo direto aos eventos de
[[iberia-2025-root-causes]] (falha de controle de tensão por IBR) e
[[chile-2025-overview]] (falha de proteção em rede de alta penetração IBR),
os três casos usados no Cap. 2 do TCC (seção 2.4) para motivar a análise de
robustez do SRF-PLL sob contingência.

## Uso no TCC

- Evidência oficial e direta de que **suporte de reativo/dinâmica de
  controle dos inversores** — não inércia, não potência de curto-circuito —
  foi o fator determinante do agravamento do distúrbio brasileiro.
- Reforça o argumento central do TCC: o desempenho dinâmico do sistema de
  sincronismo (SRF-PLL) e das malhas de controle de corrente do inversor,
  sob contingência severa, é crítico mesmo quando os indicadores estáticos
  do sistema (inércia, SCC) estão dentro dos critérios normativos.
