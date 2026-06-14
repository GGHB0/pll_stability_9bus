---
name: tcc-full-cap2
description: Conteúdo completo do Capítulo 2 — Fundamentação Teórica: transformadas Clarke/Park, controle P/Q, SRF-PLL, contingências e requisitos LVRT/ONS
metadata:
  type: project
---

# TCC — Capítulo 2: Fundamentação Teórica (texto completo)

Este capítulo apresenta a base conceitual para a compreensão da modelagem e da análise de resultados desenvolvidos neste trabalho. O objetivo é apresentar os conceitos relacionados a operação de inversores conectados à rede e os desafios impostos pelo ambiente elétrico.

## [Sec. sem número] A Necessidade das Transformadas de Referência

*(⚠️ Ttulo2 sem numeração — aparece antes de 2.1 no documento)*

O controle eficaz das grandezas elétricas trifásicas (tensões e correntes), que são senoidais por natureza, apresenta desafios intrínsecos para a aplicação de controladores lineares clássicos, como o Proporcional-Integral (PI). A performance dos controladores PI é otimizada para a regulação de sinais contínuos (CC) com erro nulo em regime permanente. Para superar essa complexidade, a teoria de controle de inversores utiliza transformações de referência que, convertem os sinais do sistema trifásico (abc) para um sistema de coordenadas ortogonal e rotativo (dq). Nesta nova referência, as grandezas senoidais tornam-se valores contínuos em regime permanente, simplificando drasticamente o problema de controle e permitindo o projeto de malhas de alto desempenho [2].

**Transformada de Clarke (abc → αβ):** A Transformada de Clarke constitui o primeiro passo nesse processo de simplificação. Ela projeta os três eixos de fase (a, b, c), defasados espacialmente de 120°, em um sistema de dois eixos ortogonais estacionários, denominados α e β. Fisicamente, essa transformação representa a decomposição do vetor espacial girante das grandezas trifásicas em duas componentes ortogonais fixas. Para um sistema trifásico balanceado e sem componente de sequência zero, a transformação é definida matematicamente, convertendo as três variáveis de fase em apenas duas variáveis ortogonais. Embora reduza a complexidade do sistema de três para duas dimensões, as grandezas no referencial αβ ainda são senoidais no tempo, requerendo um passo adicional para a total simplificação do problema de controle.

**Transformada de Park (αβ → dq):** A Transformada de Park, aplicando uma rotação ao sistema de referência estacionário αβ. Este novo referencial, composto pelos eixos direto (d) e em quadratura (q), gira a uma velocidade angular síncrona (ω), que corresponde exatamente à frequência angular da rede elétrica. (Yazdani). A vantagem desta transformação é que, quando o sistema de referência gira em perfeita sincronia com as grandezas da rede, as componentes trifásicas senoidais são vistas como valores constantes (CC) pelos eixos d e q. Esta conversão de grandezas CA para CC é a chave para o controle moderno de inversores, pois permite o uso de controladores PI, que são extremamente eficazes para eliminar erros em regime permanente de sinais CC, algo que seria impossível de alcançar com a mesma simplicidade ao tentar regular diretamente as grandezas senoidais originais.

**Controle Independente de Potências Ativa e Reativa (P e Q):** A principal vantagem da Transformada de Park no controle de inversores é a capacidade de desacoplar o controle das potências ativa (P) e reativa (Q), proporcionando maior precisão e estabilidade em sistemas conectados à rede [1]. Ao alinhar o eixo d do referencial rotativo com o vetor da tensão da rede (tarefa realizada pelo sistema de sincronismo), as expressões de potência se simplificam: a potência ativa (P) torna-se diretamente proporcional à corrente no eixo direto (id); a potência reativa (Q) torna-se diretamente proporcional à corrente no eixo em quadratura (iq). Ao considerar Vq = 0: essa relação ortogonal permite a implementação de duas malhas de controle de corrente completamente independentes.

**Arquitetura de Controle Baseada em Corrente:** Dentre as abordagens para o controle de conversores CC-CA, o controle por corrente é amplamente preferido em aplicações conectadas à rede devido à sua robustez, elevada largura de banda e à capacidade intrínseca de limitar sobrecorrentes, protegendo os semicondutores de potência. A estratégia consiste em regular diretamente as componentes de corrente injetadas na rede, tratando o inversor como uma fonte de corrente controlada [1]. A arquitetura padrão é o controle em cascata (cascaded control), onde malhas externas geram as referências para as malhas internas de corrente. As equações diferenciais acoplam as componentes id e iq através de termos cruzados dependentes da frequência da rede (ω). A estrutura de controle de corrente é implementada com dois controladores PI para regular os erros entre as correntes medidas id, iq e suas referências. Termos de desacoplamento (decoupling) e feedforward são adicionados para melhorar o desempenho dinâmico.

## 2.1. Geração Distribuída e Inversores Conectados à Rede

A Geração Distribuída (GD) refere-se à produção de energia elétrica realizada junto ou próximo aos centros de consumo, conectada diretamente à rede de distribuição. Impulsionada majoritariamente por fontes renováveis intermitentes, como a solar fotovoltaica e a eólica, a GD tem reconfigurado a arquitetura tradicional e centralizada dos sistemas elétricos [1]. O Inversor Fonte de Tensão (VSI - Voltage Source Inverter) assume um papel central e insubstituível. Ele atua como a interface de eletrônica de potência que converte a energia em corrente contínua (CC), proveniente da fonte primária, em corrente alternada (CA) trifásica, garantindo a compatibilidade de frequência, fase e amplitude para a injeção segura na rede elétrica [2].

[FIGURA 2.1 - Diagrama esquemático de um Inversor Fonte de Tensão (VSI) conectado à rede elétrica.]

A integração em larga escala desses inversores, classificados como Recursos Baseados em Inversores (IBR - Inverter-Based Resources), introduz desafios significativos de controle e estabilidade. Diferente dos inversores seguidores de rede (grid-following), as máquinas síncronas rotativas impõem as grandezas e dão suporte à rede através de sua inércia física. Com o aumento da geração baseada em inversores, a inércia total da rede diminui, dificultando a absorção do impacto de grandes perturbações e colocando em risco a manutenção do sincronismo das usinas [3, 4].

## 2.2. Controle de Inversores e Transformadas de Referência

Os inversores de tensão são dispositivos fundamentais em sistemas de conversão de potência. A topologia mais utilizada em aplicações trifásicas conectadas à rede é o inversor de dois níveis, cuja operação é baseada na Modulação por Largura de Pulso (PWM), essencial para o controle do formato da tensão de saída.

**PWM (Modulação por Largura de Pulso):** Técnica de acionamento utilizada em inversores de tensão para sintetizar uma forma de onda alternada a partir de uma fonte de tensão contínua (CC). No contexto deste trabalho, o PWM é considerado como parte da estrutura geral do conversor, responsável por aplicar ao estágio de potência os sinais de referência produzidos pelo controle vetorial. A modulação é tratada de maneira funcional, isto é, como o elo entre as tensões de referência geradas no referencial síncrono dq e a atuação do inversor sobre o sistema elétrico. Os fenômenos investigados neste trabalho estão associados principalmente à resposta dinâmica do SRF-PLL e ao rastreamento da fase da tensão no PAC.

## 2.3. O Sistema de Sincronismo SRF-PLL

Para que o controle de corrente no referencial dq seja plenamente eficaz, é imperativo que o referencial rotativo do controlador esteja perfeitamente sincronizado, tanto em fase quanto em frequência, com o vetor da tensão da rede. O SRF-PLL é o algoritmo mais amplamente utilizado para realizar essa tarefa crítica, estimando em tempo real o ângulo de fase (θ) e a frequência (ω) da rede [1].

**Estrutura — 3 blocos funcionais:**

1. **Detector de Fase (PD):** A própria Transformada de Park atua como detector de fase. O objetivo do PLL é rotacionar o sistema de referência de tal forma que o eixo d se alinhe perfeitamente com o vetor da tensão da rede. Quando isso ocorre, toda a magnitude da tensão é projetada no eixo D (vd), e a componente no eixo Q se torna nula (vq = 0). A componente vq atua como sinal de erro de fase: um valor de vq diferente de zero indica desalinhamento angular. Para pequenos erros, vq é aproximadamente proporcional ao seno do erro de fase [2].

2. **Controlador Proporcional-Integral (PI):** O sinal de erro de fase (vq) é processado por um controlador PI, que também atua como um filtro passa-baixas. A ação proporcional provê resposta rápida a variações de fase; a ação integral assegura que o erro de fase em regime permanente seja completamente eliminado [3]. O projeto do controlador envolve um compromisso fundamental: ganhos elevados resultam em PLL rápido, mas sensível a ruídos e distúrbios; ganhos baixos aumentam a imunidade a distúrbios, mas tornam o PLL lento [4].

3. **Oscilador Controlado por Tensão (VCO):** Em implementação digital, o VCO é um integrador numérico. Recebe a frequência angular estimada na saída do PI (ω_nom + Δω) e a integra ao longo do tempo para gerar o ângulo de fase estimado (θ). Este ângulo é a saída fundamental do PLL, sendo realimentado para as Transformadas de Park e Clarke.

**Equações do modelo linearizado (placeholders no documento):**
- EQUAÇÃO 2.5 — Ganho do detector de fase (linearizado)
- EQUAÇÃO 2.6 — Modelo linearizado do detector de fase
- EQUAÇÃO 2.7 — Controlador PI
- EQUAÇÃO 2.8 — Integrador que gera o ângulo estimado
- EQUAÇÃO 2.9 — Função de malha aberta do SRF-PLL
- EQUAÇÃO 2.10 — Função de transferência de malha fechada do SRF-PLL
- EQUAÇÃO 2.11 — Erro de fase no domínio da frequência
- EQUAÇÃO 2.12 — Tensão no eixo q em função do erro de fase

## 2.4. Desafios à Estabilidade do Sincronismo: Contingências Elétricas e Requisitos Normativos

### 2.4.1 A Natureza das Contingências na Rede Elétrica *(⚠️ estilo Ttulo4 — deveria ser Ttulo3)*

As contingências em sistemas elétricos englobam desde variações e rejeições de carga até eventos transitórios, como faltas equilibradas e desequilibradas isoladas pela atuação do sistema de proteção. O efeito imediato de um curto-circuito é o afundamento de tensão (voltage sag), caracterizado por uma redução súbita na amplitude da tensão para valores tipicamente entre 0,1 e 0,9 p.u. (BOLLEN, 2000).

Essas quedas de tensão afetam todas as barras do sistema elétrico. Nas máquinas síncronas, o distúrbio provoca um grave desequilíbrio entre a potência mecânica e a potência elétrica (KUNDUR, 1994). Para os inversores, o impacto no Ponto de Acoplamento Comum (PAC) é crítico: o PLL necessita de uma tensão estável para operar. Sem o rastreamento adequado durante o afundamento, o inversor apresenta mau funcionamento e falha em fornecer o suporte de potência exigido pelos códigos de rede.

É fundamental destacar que os afundamentos de tensão raramente se manifestam de forma ideal (simétrica e sem distorção). Dependendo do tipo de falta e da configuração do sistema, esses eventos são frequentemente assimétricos, afetando cada fase de maneira desigual. Além disso, a mudança súbita na topologia da rede e nos fluxos de potência pode induzir um salto no ângulo de fase (phase-angle jump), que desafia diretamente a capacidade de rastreamento do PLL (TEODORESCU et al., 2011).

[FIGURA 2.6 - Perfil característico de um afundamento de tensão.]

### 2.4.2 Requisitos de Códigos de Rede: Suporte Durante Afundamentos de Tensão (LVRT) *(⚠️ Ttulo4)*

Com a crescente penetração de fontes renováveis conectadas por meio de inversores, a desconexão em massa de geradores durante um distúrbio na rede tornou-se um risco sistêmico. Os operadores de rede passaram a estabelecer requisitos mínimos de comportamento dinâmico para centrais geradoras conectadas ao sistema elétrico. Entre esses requisitos, destaca-se a capacidade de permanência em operação durante afundamentos de tensão, frequentemente denominada Low Voltage Ride-Through (LVRT) ou Fault Ride-Through (FRT). Esse requisito estabelece que a central geradora não deve se desconectar imediatamente da rede durante determinados eventos de subtensão, desde que a magnitude e a duração do afundamento permaneçam dentro dos limites especificados pelo operador.

Além da permanência conectada, os códigos de rede estabelecem requisitos associados ao suporte dinâmico de tensão durante o distúrbio. No caso de centrais baseadas em conversores eletrônicos, esse suporte exige a injeção de corrente reativa na rede para auxiliar na recuperação da tensão no PAC (YAZDANI; IRAVANI, 2010). Um PLL que perde o rastreamento ou fornece uma referência de fase imprecisa durante a contingência torna impossível o controle exato das correntes, comprometendo a eficácia do suporte de reativos e a conformidade do inversor.

### 2.4.3 Requisitos do Código de Rede Brasileiro segundo os Procedimentos de Rede do ONS *(⚠️ Ttulo4)*

No contexto brasileiro, os Procedimentos de Rede do Operador Nacional do Sistema Elétrico (ONS) constituem o principal conjunto de documentos técnicos que estabelece os critérios e requisitos mínimos para a conexão, operação e desempenho de instalações integrantes do Sistema Interligado Nacional (SIN). A relevância do cumprimento estrito dessas normas ganhou destaque após o blecaute de agosto de 2023 no SIN, onde o desempenho insatisfatório dos sistemas de controle de usinas renováveis diante de uma falta na rede contribuiu para o agravamento da perturbação sistêmica.

Entre os requisitos estabelecidos no Submódulo 2.10 do ONS, destacam-se aqueles associados à suportabilidade a subtensões decorrentes de faltas na rede (LVRT), determinando o tempo que a planta deve tolerar a queda de tensão antes de ser permitida sua desconexão. Esses critérios são graficamente representados por curvas que relacionam a magnitude da tensão no ponto de conexão com o tempo de duração do evento.

[INSERIR FIGURA 2.X – Curva de suportabilidade a subtensões decorrentes de faltas na rede, conforme Procedimentos de Rede do ONS.] Fonte: Adaptado de ONS (2022).

Além da permanência em operação, os Procedimentos de Rede também exigem o suporte dinâmico de tensão por meio da injeção de corrente reativa adicional durante o período da falta.

[INSERIR FIGURA 2.X – Requisito de injeção de corrente reativa sob defeito, conforme Procedimentos de Rede do ONS.] Fonte: Adaptado de ONS (2022).

A observância desses requisitos depende inteiramente da atuação coordenada das malhas de controle do inversor. Como o ONS impõe rampas e limites específicos para a resposta de corrente durante e logo após a eliminação da falta, a estimação correta do ângulo da tensão no PAC pelo SRF-PLL mostra-se indispensável. Falhas ou lentidão no sincronismo impossibilitam o correto direcionamento dos vetores de corrente nas coordenadas síncronas (d e q), comprometendo o atendimento aos critérios exigidos pelo operador nacional.
