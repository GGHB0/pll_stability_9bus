---
name: tcc-full-cap3
description: Conteúdo completo do Capítulo 3 — Metodologia: plataforma híbrida (Python/PSIM/MATLAB), IEEE 9 barras, filtro LCL, PI corrente, SRF-PLL, protocolos de contingência
metadata:
  type: project
---

# TCC — Capítulo 3: Metodologia de Projeto e Simulação (texto completo)

A metodologia desenvolvida neste trabalho fundamenta-se em uma abordagem quantitativa e analítica, estruturada sobre a modelagem matemática e a simulação computacional de transitórios eletromagnéticos (EMT). O objetivo central consiste em avaliar a robustez e o desempenho dinâmico do algoritmo de sincronismo SRF-PLL aplicado a inversores conectados à rede frente a diferentes cenários de contingência.

**Estrutura metodológica — 4 etapas sequenciais:**
- (i) definição e justificativa técnica do ecossistema multiplataforma de simulação
- (ii) modelagem do estágio de potência do conversor, dimensionamento do filtro de acoplamento e projeto de sintonia das malhas de controle e sincronismo
- (iii) estabelecimento dos protocolos de contingência e faltas na rede
- (iv) definição das métricas analíticas para avaliação do erro de fase e frequência

## 3.1. PLATAFORMA DE SIMULAÇÃO E JUSTIFICATIVA TÉCNICA

A execução das análises propostas foi conduzida através de um fluxo de trabalho híbrido, integrando ferramentas de cálculo numérico e softwares de simulação de sistemas de potência. Essa abordagem multiplataforma foi adotada para mitigar as limitações inerentes a cada ambiente de simulação individual, garantindo a fidelidade dos resultados tanto no domínio da comutação de alta frequência quanto na análise sistêmica da rede elétrica.

Para o dimensionamento analítico dos componentes passivos do filtro LCL e a sintonia preliminar dos controladores lineares, utilizou-se a linguagem Python, com suporte das bibliotecas Numpy e Pandas. Esta etapa garantiu a precisão dos parâmetros iniciais através da automação de cálculos matriciais complexos, destacando-se a inversão da matriz de admitância nodal para a obtenção da impedância de Thévenin equivalente vista pelo inversor no ponto de acoplamento comum (PAC) do sistema teste IEEE 9 barras (ANDERSON; FOUAD, 2003).

A validação dinâmica e a análise de robustez foram realizadas através do uso complementar dos softwares PSIM e MATLAB/Simulink:

**PSIM (Power Simulation):** Foi empregado para a validação detalhada e em nível de circuito do estágio de potência. A escolha fundamenta-se no fato de que o PSIM apresenta desempenho computacional superior na modelagem de dispositivos semicondutores e na simulação de fenômenos de alta frequência, como a Modulação por Largura de Pulso (PWM) e a resposta transitória de filtros LCL (SOUSA et al., 2021). Sua capacidade de executar simulações com passos de tempo reduzidos (fixed-step na ordem de microssegundos), mantendo a estabilidade numérica e a convergência, torna-o ideal para investigar transitórios rápidos de chaveamento que afetam diretamente o detector de fase do algoritmo SRF-PLL.

**MATLAB/Simulink:** Foi utilizado para a análise sistêmica, eletromecânica e topológica da rede elétrica. O ambiente Simscape Electrical permitiu a modelagem completa da rede de transmissão em malha, eliminando a dependência exclusiva de equivalentes de Thévenin simplificados no PAC e viabilizando a simulação de curtos-circuitos em pontos distantes para avaliar a propagação real dos afundamentos de tensão. Uma diferenciação metodológica crucial para a escolha do Simulink reside na modelagem das máquinas síncronas do sistema elétrico: enquanto o PSIM adota representações simplificadas de fontes, o Simulink computa o modelo matemático completo dos geradores baseado em suas equações diferenciais de estado expressas no referencial síncrono. Essa rigidez de modelagem é indispensável para capturar as oscilações de potência (power swings) e a interação dinâmica mútua entre os geradores convencionais e as malhas de sincronismo do inversor sob contingência.

*(⚠️ Oscar comentário #9: referências MATLAB/PSIM pendentes — citar MathWorks e Powersim Inc.)*

## 3.2. MODELAGEM E DIMENSIONAMENTO DO SISTEMA DE ESTUDO

A representação do sistema elétrico é necessária para a avaliação da estabilidade de sincronização. Para isso, o estudo adota uma topologia de rede em malha, permitindo a análise de fluxos de potência e a propagação de distúrbios através de diferentes impedâncias de rede.

### 3.2.1. Modelo da Rede Elétrica: Sistema IEEE 9 Barras Modificado

O sistema teste utilizado para a análise sistêmica no ambiente MATLAB/Simulink baseia-se no padrão IEEE 9 barras, conhecido como sistema Anderson-Fouad, cujos dados de parâmetros estão descritos em Anderson e Fouad (2003, p. 38). A principal adaptação realizada consiste na substituição da máquina síncrona originalmente conectada à Barra 2 (G2) pelo modelo do VSI. Desta forma, o sistema passa a ser composto por geradores síncronos (G1 e G3) e pelo Recurso Baseado em Inversor (RBI) conectado à Barra 2.

Para a simulação de transitórios eletromagnéticos (EMT) no PSIM, o sistema de transmissão foi reduzido a um equivalente de Thévenin no Ponto de Acoplamento Comum (PAC), definido como Barra 2. Essa simplificação é adotada para isolar a análise da dinâmica do VSI e do SRF-PLL, focando no comportamento do ponto de conexão.

A impedância de Thévenin vista pelo inversor foi obtida por meio da matriz de impedância nodal (Z-barra). Inicialmente, procedeu-se à montagem da matriz de admitância nodal (Y-barra) do sistema IEEE 9 barras. Em seguida, a inversão da matriz Y-barra resultou na matriz Z-barra. A impedância de Thévenin é dada pelo elemento diagonal da matriz Z-barra. Essa abordagem garante que a simplificação incorpore a influência das linhas e geradores do sistema base no equivalente utilizado no PSIM.

### 3.2.2. Projeto do Conversor e dos Controladores

A interface de conexão do RBI com a rede elétrica foi modelada como um VSI trifásico de dois níveis. Essa topologia utiliza seis interruptores semicondutores controlados, cujo acionamento é realizado por meio de técnicas de PWM senoidal. O circuito de potência, os sinais de comando PWM e a disposição dos sensores de medição do sistema são detalhados na Figura 3.1.

*(⚠️ [FIGURA 3.1] referenciada mas sem placeholder no texto — P1 pendente)*

O dimensionamento e a modelagem dessa estrutura foram divididos em três subsistemas principais: o filtro de acoplamento, a malha de controle de corrente e o algoritmo de sincronismo.

Neste estudo, as malhas externas de controle de tensão do barramento CC e o algoritmo de rastreamento do ponto de máxima potência (MPPT) não foram modelados. Essa simplificação fundamenta-se no desacoplamento das constantes de tempo dinâmicas. Como as contingências de rede avaliadas ocorrem em uma escala de tempo transitória rápida (na ordem de microssegundos a milissegundos), os impactos associados ao MPPT e à regulação do ponto de acoplamento CC operam em uma faixa de frequência significativamente menor (mais lenta). Desse modo, o barramento CC é representado como uma fonte de tensão contínua constante ideal, sem prejuízo à avaliação da estabilidade de sincronização do SRF-PLL.

**Dimensionamento do Filtro de Acoplamento (LCL):** O filtro de acoplamento é um componente passivo essencial que tem a função de atenuar as componentes harmônicas de alta frequência geradas pela comutação do inversor (PWM), garantindo que a energia injetada na rede possua alta qualidade. Optou-se pela topologia LCL (Indutor-Capacitor-Indutor) devido à sua superior capacidade de atenuação (60 dB/década) em comparação com um filtro puramente indutivo (L), o que permite o uso de componentes menores e mais leves.

O circuito elétrico do filtro, composto pela indutância do lado do inversor (L1), pela capacitância de desvio (C) e pela indutância do lado da rede (L2), é ilustrado na Figura 3.1. O cálculo dos parâmetros passivos foi realizado por meio de formulações analíticas implementadas em Python, baseando-se nos critérios de projeto estabelecidos por Alves (2021):

- **Limitação do Ripple de Corrente:** O indutor L1 foi dimensionado com base na tensão de barramento CC (Vcc) e na frequência de chaveamento (fsw), de modo a limitar a ondulação máxima de corrente a um percentual da corrente nominal de pico do conversor — Equação (3.1)
- **Capacitância do Filtro:** O valor de C foi definido de maneira a limitar a absorção de potência reativa em frequência fundamental a uma fração da potência nominal do sistema (geralmente ≤ 5%), minimizando a perda de fator de potência no PAC
- **Frequência de Ressonância:** A combinação entre os elementos indutivos e capacitivos foi calculada para posicionar a frequência de ressonância do filtro (ω_res) em uma faixa intermediária segura, distante da frequência fundamental da rede (ω_0) e da frequência de chaveamento (ω_sw) — Equação (3.2)
- **Amortecimento:** O comportamento dinâmico foi projetado considerando um fator de amortecimento (ξ) inserido na malha de controle para mitigar o pico de ressonância e atenuar oscilações transitórias no ponto de conexão

**Sintonia da Estratégia de Controle de Corrente:** O controle da injeção de potência baseia-se na teoria do referencial síncrono (dq), que permite o controle desacoplado das potências ativa e reativa [2]. O controle é realizado por uma malha interna de corrente, utilizando controladores PI. A sintonia dos ganhos do controlador PI é crucial para o desempenho dinâmico do inversor. O método de sintonia utilizado baseou-se na técnica de cancelamento de polo e zero, adaptada para o referencial síncrono.

**Modelagem do Sistema de Sincronismo (SRF-PLL):** O elemento central desta análise é o SRF-PLL, responsável por estimar o ângulo de fase (θ) e a frequência (ω) da tensão no PAC. A estrutura implementada segue o modelo padrão da literatura [3], composta por: Detector de Fase, Filtro de Loop (Controlador PI) e Oscilador Controlado por Tensão (VCO). O projeto dos ganhos (Kp e Ki) do controlador do PLL é o foco da análise de sensibilidade, pois envolve um compromisso crítico: ganhos elevados aumentam a velocidade de rastreamento, mas comprometem a rejeição a distúrbios harmônicos e ruídos de medição [4].

## 3.3. PROTOCOLOS DE CONTINGÊNCIA E ANÁLISE DE CENÁRIOS

*(Adicionado por Claude com tracked changes — ⚠️ texto sem acentuação)*

Para a avaliação da robustez do SRF-PLL, foram definidos dois protocolos de contingência elétrica, selecionados por sua representatividade nos sistemas de potência modernos e por sua capacidade de excitar diferentes aspectos da dinâmica do sincronismo. Em ambos os casos, as faltas são aplicadas na rede de transmissão do sistema IEEE 9 barras e têm seus efeitos avaliados no Ponto de Acoplamento Comum (PAC) da Barra 2, onde o inversor está conectado. A implementação computacional utiliza os blocos de falta do ambiente Simscape Electrical do MATLAB/Simulink, com parâmetros de severidade e duração configurados individualmente para cada cenário.

### 3.3.1. Afundamento de Tensão Simétrico

O afundamento de tensão simétrico resulta de faltas trifásicas equilibradas (3LG) e se caracteriza por uma redução simultânea e proporcional do módulo das três tensões de fase, sem alteração na simetria do sistema ou geração de componentes de sequência negativa. Trata-se, portanto, da condição de perturbação mais favorável ao algoritmo SRF-PLL, pois o sinal de tensão no PAC permanece equilibrado durante o distúrbio.

Do ponto de vista do sincronismo, a severidade do afundamento determina a degradação do sinal de referência disponível ao detector de fase do PLL. Afundamentos profundos reduzem a relação sinal-ruído e podem comprometer a velocidade de rastreamento angular. Os cenários são simulados para diferentes níveis de retenção de tensão no PAC, permitindo quantificar o tempo de acomodação do ângulo estimado e o impacto transitório nas potências injetadas.

[TABELA 3.1 - Parâmetros dos cenários de afundamento de tensão simétrico simulados.]

### 3.3.2. Afundamento de Tensão Assimétrico

O afundamento de tensão assimétrico é produzido por faltas desequilibradas, como a falta monofásica a terra (LG) ou bifásica a terra (LLG), que afetam apenas uma ou duas fases do sistema elétrico. Diferentemente do cenário simétrico, esse tipo de contingência introduz componentes de sequência negativa na tensão do PAC, resultando em um sinal trifásico desequilibrado durante o período de falta.

A presença de tensão de sequência negativa impõe um desafio crítico ao SRF-PLL convencional. No referencial síncrono dq, a componente de sequência negativa gira em sentido contrário ao referencial positivo, produzindo uma oscilação de frequência dupla (2·ω₀ ≈ 753 rad/s para ω₀ = 2π·60 rad/s) no sinal de erro de fase vq. Essa perturbação atravessa a malha de controle do PI e se manifesta como uma ondulação oscilatória no ângulo estimado e na frequência angular estimada, comprometendo a qualidade do sincronismo e deteriorando o controle desacoplado das potências.

[TABELA 3.2 - Parâmetros dos cenários de afundamento de tensão assimétrico simulados.]
