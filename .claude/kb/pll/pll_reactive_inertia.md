---
name: pll-reactive-inertia
description: PLL como "inércia reativa" e dualidade Q-δi (GFL) vs P-δv (síncronos/GFM) — framework estendido de estabilidade de sistemas com alta penetração de IBR
source: Gu, Y. e Green, T. C., "Power System Stability With a High Penetration of Inverter-Based Resources", Proceedings of the IEEE, vol. 111, n.7, p.836-854, jul/2023
---

# PLL como Inércia Reativa — Dinâmica de Ângulo Generalizada

Framework teórico (não ligado a nenhum evento) que estende a categorização
clássica de estabilidade (IEEE/CIGRE 2004) para redes com alta penetração de
IBR. Complementa [[srf-pll-theory]] com o porquê estrutural de o PLL se
comportar como comporta. Referência-chave para o Cap. 2 (fundamentação
teórica) do TCC.

## Framework clássico (IEEE/CIGRE 2004) e seus índices

Estabilidade = capacidade de, partindo de um ponto de operação, reconvergir a
um equilíbrio após um distúrbio, com variáveis limitadas. Três categorias
clássicas — ângulo, frequência, tensão — cada uma com um índice:

| Categoria | Índice |
|---|---|
| Frequência | Inércia (global) |
| Ângulo, pequeno distúrbio | Coeficientes de sincronização e amortecimento (local/global) |
| Ângulo, grande distúrbio | Energia crítica (global, depende do local da falta) |
| Tensão, pequeno distúrbio | Sensibilidade ∂V/∂Q (local/global) |

## GFL vs. GFM: a diferença estrutural

- **GFL (grid-following)**: inversor sincronizado à tensão local via **PLL**,
  injeta um vetor de corrente regulado por potência disponível/posição de
  mercado — formato dominante hoje.
- **GFM (grid-forming)**: controlado como fonte de tensão, com frequência que
  cai proporcionalmente à potência drenada (droop) — comportamento
  sincronizante similar a um gerador síncrono, mas **sem capacidade de
  sobrecorrente** em curto-circuito (diferença crítica em faltas).

## A dualidade: PLL = inércia reativa

Resultado central do paper. A dinâmica de um PLL PI (equação 2 do artigo) tem a
mesma forma de uma mecânica newtoniana — mas a aceleração angular de ω é
governada por **potência reativa**, não ativa:

- **Síncronos e GFM**: sincronização via swing **P–δᵥ** (ângulo entre fasores
  de tensão), governado pela reatância de linha X — a "inércia ativa" clássica
  do rotor.
- **GFL**: sincronização via swing **Q–δᵢ** (ângulo entre fasores de corrente),
  governado pela resistência de carga R — o PLL atua como uma **inércia
  reativa**, dual à inércia ativa do rotor.

Essa dualidade unifica a teoria de sincronização de síncronos, GFM e GFL em uma
única "dinâmica de ângulo generalizada", habilitando análise formal de
interação GFM–GFL — relevante para decidir onde posicionar dispositivos GFM e
se GFM pode fazer *fallback* para modo GFL durante faltas (evitando
sobredimensionamento para suportar sobrecarga de curto prazo).

**Implicação contraintuitiva**: uma rede ilhada alimentada só por inversores
GFL (sem síncronos nem GFM) ainda pode operar — mas a frequência da rede passa
a ser governada por **balanço de potência reativa**, não ativa. Um desbalanço
de Q causa aceleração/desaceleração sustentada da frequência estimada pelo PLL.

## Nova categoria: estabilidade eletromagnética (EM stability)

Faixa de frequência: subsíncrona (~metade da fundamental) a poucos kHz —
também chamada "harmonic stability" na literatura no lado supersíncrono.
Fontes de amortecimento negativo identificadas:

1. Atraso de ciclo de chaveamento da modulação/controle (GFL e GFM).
2. Malha de corrente interna do GFL interagindo com o efeito de geração por
   indução de DFIGs.
3. **Malhas de PLL e de controle de tensão de barramento CC** também podem
   induzir amortecimento negativo em frequência subsíncrona — categorizadas
   como parte da dinâmica de ângulo generalizada (não como EM stability pura).

EM stability é tipicamente um fenômeno **local** (um inversor ou cluster
eletricamente/fisicamente próximo), ao contrário das categorias clássicas de
alcance sistêmico.

## Extensão do framework (Fig. 2 do artigo)

O framework clássico ganha: a nova categoria EM stability, mais três "features"
que penetram as categorias existentes — controle de tensão indireto,
dinâmica de ângulo generalizada, dinâmica de frequência rápida. Essas
extensões **se sobrepõem em escala de tempo** e podem interagir dinamicamente
entre si (setas cinzas na Fig. 2), complicando a análise em relação ao
framework clássico particionado.

## Problemas em aberto (Seção V do artigo)

- Modo de interação entre múltiplos IBR numa rede ainda pouco compreendido além
  do caso local (1 IBR ou cluster + rede fraca).
- Acoplamento cruzado entre categorias de estabilidade (ex.: tensão×ângulo)
  complica ainda mais o modo de interação.
- Horizonte de rede ~100% IBR: a estrutura dinâmica do sistema de potência
  será remodelada mais radicalmente do que as extensões atuais capturam.

## Uso no TCC

- Fundamenta teoricamente **por que** a sintonia de Kp/Ki do SRF-PLL
  (ver [[pll-gains-methodology]]) não é só sobre velocidade de rastreamento:
  ela define a "inércia reativa" do inversor e, portanto, a dinâmica do swing
  Q–δᵢ que governa sua estabilidade de sincronização sob contingência.
- O cenário BAD_PLL (kp_pll×0,2, [[iberia-2025-oscillations]]) pode ser
  reinterpretado como uma inércia reativa mal dimensionada — paralelo direto
  ao papel da inércia ativa em síncronos.
- Justifica por que o inversor do TCC deve ser analisado pela lente do swing
  Q–δᵢ (categoria GFL), não pela lente P–δᵥ tradicionalmente aplicada a
  geradores síncronos — ver também [[machine-inertia]] para o contraste.
