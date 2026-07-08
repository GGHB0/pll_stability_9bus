---
name: tcc-full-intro
description: Conteúdo completo da Introdução do TCC — contextualização, motivação (apagão 08/2023), objetivos e referências [1]–[9]
metadata:
  type: project
---

# TCC — Introdução (texto completo)

## Contextualização

A transição da matriz energética global representa, a mais profunda e complexa transformação tecnológica do setor elétrico no último século. Este movimento é impulsionado por uma confluência de fatores interdependentes e de crescente urgência: as metas de descarbonização estabelecidas mundialmente para mitigar os efeitos adversos das mudanças climáticas; a busca estratégica das nações por maior segurança e independência energética frente à volatilidade geopolítica e econômica dos combustíveis fósseis; e a notável evolução tecnológica que, aliada às economias de escala, tornou as fontes renováveis, como a solar e a eólica, economicamente competitivas em muitos mercados. Esse cenário, embora promissor, impõe novos desafios de ordem técnica, regulatória e operacional que exigem soluções inovadoras.

Entre os principais desafios técnicos da transição energética está a integração de fontes renováveis intermitentes à infraestrutura elétrica convencional. Diferentemente das usinas tradicionais, que operam de forma contínua e com inércia mecânica intrínseca, os sistemas de geração distribuída (GD) apresentam variações abruptas. A incorporação dessas fontes enfrenta obstáculos críticos, como a flutuação da geração e a ausência de sistemas de armazenamento em grande escala, que comprometem a confiabilidade e a estabilidade dinâmica do sistema elétrico [1].

Nesse contexto, os inversores conectados à rede (grid-following inverters) assumem um papel central e insubstituível. Essas funções, além da conversão de energia, dependem de algoritmos digitais de controle, ao contrário das máquinas síncronas que conferem estabilidade pela inércia física das máquinas rotativas [2]. Conforme apontado por Yazdani e Iravani [3], a estabilidade e a robustez dos sistemas baseados em inversores estão diretamente relacionadas à eficácia das técnicas de controle implementadas em seus microprocessadores.

Dentre os diversos aspectos do controle de inversores, o sincronismo com a rede elétrica se apresenta como requisito fundamental. Trata-se da capacidade de manter-se alinhado em fase e frequência com o vetor de tensão do ponto de acoplamento comum (PAC), assegurando a qualidade da potência injetada. Para garantir essa sincronia, utiliza-se amplamente a técnica do Phase-Locked Loop (PLL), responsável por rastrear continuamente a fase da tensão da rede e ajustar em tempo real o referencial interno do inversor [4].

Apesar de sua ampla aplicação industrial, o algoritmo Synchronous Reference Frame PLL (SRF-PLL) possui limitações intrínsecas quando submetido a regimes dinâmicos severos na rede elétrica. Distúrbios e contingências sistêmicas podem induzir erros significativos de rastreamento angular, degradando a qualidade da potência injetada e desafiando a estabilidade do controle do inversor.

Apesar de sua ampla aplicação, a técnica Synchronous Reference Frame PLL (SRF-PLL), apresenta limitações significativas. Sua robustez é severamente desafiada por contingências na rede elétrica, como afundamentos de tensão (voltage sags), variações de impedância em redes fracas e saltos de fase (phase-angle jumps) [5]. Essas condições não ideais podem induzir erros de rastreamento consideráveis, resultando em oscilações indesejadas na potência e degradação da qualidade de energia, além de comprometer a capacidade do inversor em cumprir exigências normativas, como o suporte reativo à rede.

Diante dessas limitações, o uso de ferramentas de simulação computacional, como MATLAB/Simulink e PSIM, constitui um recurso essencial para reproduzir cenários de operação críticos, avaliar o desempenho dinâmico dos algoritmos e validar estratégias de controle em condições próximas às reais. Enquanto o MATLAB se destaca pela flexibilidade na modelagem e análise de sistemas dinâmicos (MATHWORKS, 2023), o PSIM oferece simulações otimizadas em eletrônica de potência, permitindo analisar perdas, harmônicos e efeitos transitórios (POWERSIM, 2022). A utilização conjunta dessas ferramentas potencializa a confiabilidade dos resultados e fortalece a fundamentação técnica das soluções propostas.

Dessa forma, pode-se afirmar que a integração das fontes renováveis à rede elétrica, embora indispensável para o avanço da transição energética, impõe desafios técnicos que têm no sincronismo dos inversores um de seus pontos mais críticos. Assim, a investigação do desempenho e das limitações do SRF-PLL sob diferentes condições de rede torna-se não apenas uma questão de interesse acadêmico, mas também um requisito essencial para assegurar a estabilidade, a confiabilidade e a sustentabilidade do setor elétrico no futuro.

## Motivação e Justificativa

A crescente inserção de IBRs na matriz energética tem transformado a dinâmica dos sistemas elétricos, implicando em uma redução substancial da inércia do sistema [6].

No Brasil, esse desafio foi evidenciado de forma contundente na perturbação ocorrida em 15 de agosto de 2023. Naquela ocasião, uma falha no Sistema Interligado Nacional (SIN) culminou em uma sequência de desligamentos em cascata, resultando na interrupção de 23.368 MW, cerca de 34,5% da carga do Sistema Interligado Nacional (SIN) [7]. O Relatório de Análise de Perturbação (RAP) do ONS concluiu que a severidade do evento foi agravada pelo desempenho dos equipamentos de controle de tensão das usinas eólicas e fotovoltaicas. Eles ficaram "aquém do previsto nos modelos matemáticos" e se desconectaram de forma inesperada, mesmo sem o relatório apontar um motivo específico para essa falha. Esse episódio expôs uma clara diferença entre o que é simulado e o desempenho real dos inversores. Esse problema é ainda maior porque os algoritmos de controle são propriedade intelectual dos fabricantes, o que dificulta bastante o trabalho de simulação para avaliar o desempenho dos equipamentos. Com isso, a robustez dos métodos de sincronismo, como o SRF-PLL, acaba sendo colocada em xeque quando a rede passa por condições de estresse.

A vulnerabilidade do SRF-PLL reside em sua dependência de um sinal de tensão de referência de boa qualidade, premissa que é violada durante contingências na rede. Entre os fatores mais críticos que afetam seu desempenho, destacam-se: afundamentos de tensão, que reduzem a amplitude do sinal; desequilíbrios de fase, que introduzem oscilações de segunda harmônica no referencial síncrono (dq); e, de forma mais severa, os saltos angulares abruptos (phase-angle jumps). Como o PLL é um sistema de rastreamento com largura de banda finita, ele pode ser incapaz de seguir uma mudança de fase instantânea e de grande magnitude, perdendo parcial ou completamente o passo sincronizado com a rede. Nessas condições, o algoritmo falha em sua tarefa de estimar corretamente a fase do sinal fundamental [8].

A consequência direta não é necessariamente a desconexão imediata do inversor, mas a degradação de sua capacidade de controlar adequadamente as correntes injetadas na rede. Durante distúrbios, a perda de precisão no rastreamento angular pode comprometer o fornecimento de potência ativa e reativa requerido pelas estratégias de controle e pelos códigos de rede. Dessa forma, a dinâmica do PLL torna-se um fator relevante para a resposta transitória de conversores conectados à rede, especialmente em redes fracas [9].

Portanto, a justificativa para este trabalho é a necessidade crítica de preencher a lacuna de modelagem identificada pelo ONS, explicando em nível de controle por que os equipamentos falharam. É imperativo investigar o comportamento dinâmico do SRF-PLL sob essas contingências severas, confrontando o algoritmo com as complexidades reais dos distúrbios de rede. O objetivo é compreender seus mecanismos de falha para que modelos mais precisos possam ser desenvolvidos e, futuramente, para que soluções de controle mais robustas garantam que os inversores atuem como agentes estabilizadores, contribuindo para uma transição energética segura e confiável.

## Objetivos do Trabalho

Diante do exposto, o objetivo geral deste trabalho é analisar, de forma crítica e detalhada, o desempenho dinâmico e a robustez do SRF-PLL de inversores conectados à rede frente a um espectro de contingências elétricas.

**Objetivos específicos:**
1. Desenvolver a modelagem matemática do sistema inversor-rede e suas malhas de controle, com foco na dinâmica do PLL em referencial síncrono (dq)
2. Identificar, por meio de simulações computacionais em ambiente de transitórios eletromagnéticos (EMT), as condições operacionais que comprometem o rastreamento de fase e frequência
3. Avaliar os impactos da perda de desempenho, como oscilações de potência e sobrecorrentes
4. Analisar a capacidade do inversor em atender aos requisitos de suporte de reativos dos códigos de rede
5. Identificar os fatores críticos que afetam a estabilidade do sincronismo, como os ganhos do controlador PI e a impedância da rede

## Referências (Introdução)

[1] MOW, N. Power Electronics: Converters, Applications, and Design. 3. ed. John Wiley & Sons, 2003.

[2] XIONG, Y. et al. Comparison of Power Swing Characteristics and Efficacy Analysis of Impedance-based Detections in Synchronous Generators and Grid-following Systems. IEEE Transactions on Power Systems, 2024.

[3] YAZDANI, A.; IRAVANI, R. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. John Wiley & Sons, 2010.

[4] TEODORESCU, R.; LISERRE, M.; RODRIGUEZ, P. Grid Converters for Photovoltaic and Wind Power Systems. John Wiley & Sons, 2011.

[5] ENHANCED_PHASE-LOCKED_LOOP_STRUCTURES_FOR_POWER_AND_ENERGY_APPLICATIONS. IEEE Transactions on Power Electronics, 2024.

[6] WU, H.; WANG, X. Design-Oriented Transient Stability Analysis of PLL-Synchronized Voltage-Source Converters. IEEE Transactions on Power Systems, 2024.

[7] RELATÓRIO DE ANÁLISE DE PERTURBAÇÃO - RAP. ANÁLISE DA PERTURBAÇÃO DO DIA 15/08/2023 ÀS 08H30MIN. ONS, 2023.

[8] WU, H.; WANG, X. Design-Oriented Transient Stability Analysis of PLL-Synchronized Voltage-Source Converters. IEEE Transactions on Power Systems, 2024.

[9] XIONG, Y. et al. Comparison of Power Swing Characteristics and Efficacy Analysis of Impedance-based Detections in Synchronous Generators and Grid-following Systems. IEEE Transactions on Power Systems, 2024.
