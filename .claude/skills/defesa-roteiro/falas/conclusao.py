"""Slides 20 e 21, apêndice e reserva (22-29) em fala curta."""

SLIDES_CONCLUSAO = [
    # -------------------------------------------------------------------------
    # PARTE IV: SLIDES 20 E 21 (CONCLUSÃO E ENCERRAMENTO)
    # -------------------------------------------------------------------------
    {
        "tipo": "SLIDE",
        "num": 20,
        "titulo": "Síntese dos resultados (Conclusão)",
        "bloco": "Conclusão",
        "tcc": "Cap. 6",
        "quem": "Bruno → Victor → Bruno → Victor",
        "dur_s": 70,
        "msg": "O sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico.",
        "pontos": [
            ("Bruno", "Cartão 1 ('1. Faltas simétricas'): com a sintonia nominal, o SRF-PLL preserva o sincronismo e reconverge em todos os pontos; a severidade do afundamento depende diretamente da distância elétrica até a usina."),
            ("Victor", "Cartão 2 ('2. Faltas assimétricas'): a fragilidade do SRF-PLL é estrutural — a componente de sequência negativa introduz oscilação de 120 Hz que o controlador PI não rejeita, contaminando as potências injetadas P e Q."),
            ("Bruno", "Cartão 3 ('3. Sensibilidade de ganhos'): reduzir os ganhos atenua a falta moderada, mas retarda o restabelecimento e leva ao escorregamento de ciclo na Barra 7, fazendo o inversor drenar potência ativa da rede."),
            ("Victor", "Caixa de rodapé ('Qual é a conclusão central da defesa?'): permanecer conectado é insuficiente para garantir a estabilidade; a conformidade regulatória deve auditar o erro angular dinâmico durante a falta e em toda a recomposição da rede."),
        ],
        "falas": [
            ("Bruno", "De volta aos slides para sintetizar nossas conclusões nos três pontos principais de apoio. Primeiro, nas faltas simétricas: com a sintonia nominal, o SRF-PLL preserva a estabilidade e reconverge em todos os pontos da rede, sendo a severidade do afundamento ditada diretamente pela distância elétrica até a usina."),
            ("Victor", "Segundo, nas faltas assimétricas: demonstramos que a fragilidade do SRF-PLL clássico é estrutural, pois a componente de sequência negativa introduz uma oscilação de 120 hertz que o controlador PI não consegue rejeitar, contaminando diretamente as potências ativa e reativa injetadas."),
            ("Bruno", "Terceiro, na sensibilidade de ganhos: reduzir os ganhos do PI atenua a oscilação durante faltas distantes, mas retarda o restabelecimento pós-falta e leva à perda de sincronismo por escorregamento de ciclo na falta severa da Barra 7, fazendo o inversor drenar potência ativa da rede."),
            ("Victor", "Por tudo isso, nossa conclusão central no rodapé é que o sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico: permanecer conectado não basta; a verificação de conformidade precisa auditar o erro angular dinâmico durante a falta e em toda a recomposição da rede."),
        ],
        "atencao": "Slide 20 atualizado: foco 100% nos 3 pontos conceituais dos cartões (sem números isolados no topo).",
    },
    {
        "tipo": "SLIDE",
        "num": 21,
        "titulo": "Trabalhos futuros e encerramento",
        "bloco": "Conclusão",
        "tcc": "Cap. 7",
        "quem": "Victor → Bruno → Victor",
        "dur_s": 60,
        "msg": "Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho.",
        "pontos": [
            ("Victor", "Caixa inferior ('Limites do estudo', dizer com naturalidade e transparência): resultados obtidos no sistema IEEE 9 barras com nível fixo de curto-circuito, duas sintonias contrastantes e janela de simulação de 200 ms pós-falta — o estudo descreve um mecanismo físico-dinâmico rigoroso, não um envelope universal de projeto."),
            ("Bruno", "Cartões 1 e 2 ('Trabalhos futuros'): (1) implementar novas estruturas de sincronismo como DDSRF-PLL e DSOGI-PLL, que desacoplam as componentes de sequência positiva e negativa antes do laço PI para rejeitar o 120 Hz sem reduzir a banda passante; (2) varrer a relação de curto-circuito (SCR / impedância de Thévenin) para mapear a fronteira crítica de perda de sincronismo e investigar múltiplos inversores interagindo em redes fracas."),
            ("Victor", "Cartão azul à direita ('Obrigado!'): agradecer novamente aos orientadores Prof. Oscar e Prof. André, aos membros da banca e à UERJ, colocando-se à disposição para a arguição com o painel interativo aberto."),
        ],
        "falas": [
            ("Victor", "Para encerrar, registramos com transparência os limites metodológicos deste trabalho: analisamos o sistema IEEE 9 barras com nível de curto-circuito fixo, duas sintonias contrastantes e janela de observação de 200 milissegundos pós-falta; portanto, nossos resultados caracterizam um mecanismo físico-dinâmico e não um envelope universal de projeto."),
            ("Bruno", "A partir desses limites, dois eixos dão continuidade direta à pesquisa: o primeiro é implementar estruturas avançadas de sincronismo, como o DDSRF-PLL e o DSOGI-PLL, capazes de separar as componentes de sequência antes do filtro PI para rejeitar a oscilação de 120 hertz preservando a largura de banda e a rapidez de recomposição; o segundo é varrer a relação de curto-circuito da rede para mapear a fronteira crítica de perda de sincronismo e investigar a interação entre múltiplos inversores em redes fracas."),
            ("Victor", "Agradecemos mais uma vez aos nossos orientadores, professor Oscar e professor André, aos membros da banca pela leitura cuidadosa e à UERJ. Muito obrigado, e estamos à disposição para as perguntas da banca."),
        ],
        "atencao": "Não propor salto de fase nem RoCoF como trabalhos futuros (foram descartados). Deixar o painel interativo pronto para abrir no botão da tela durante as perguntas.",
    },
]

APENDICE_E_RESERVA = [
    (22, "Apêndice 1", "Defesa Técnica 1: Rede, Filtro LCL e Controle", "Cap. 3 e 4",
     "Acionar se a banca perguntar valores construtivos internos: V_cc = 136,36 kV (1,5 × 90,91 kV para evitar sobremodulação PWM), R_th = 10,04 mΩ, L_th = 1,16 mH, passos Ts = 5 μs (elétrico) e Tsc = 200 μs (controle), L_1 = 30,42 mH, L_2 = 0,289 mH, C_f = 42,47 μF e ganhos da malha de corrente (Kp,i = 14,74 e Ki,i = 3.537,8, aplicados ÷4 no Simulink).",
     "[Bruno] Neste slide de apêndice reunimos todas as especificações elétricas da rede IEEE 9 barras, do equivalente de Thévenin, dos elementos individuais do filtro LCL e da sintonia analítica das malhas de corrente e do SRF-PLL."),
    (23, "Apêndice 2", "Defesa Técnica 2: Tabelas 5.1, 5.2 e 5.3 Completas", "Cap. 5",
     "Acionar se a banca quiser ver todas as métricas numéricas em formato estático de slide (equivale ao Capítulo 8 do painel HTML).",
     "[Victor] Este slide consolida integralmente as Tabelas 5.1, 5.2 e 5.3 do Capítulo 5, permitindo comparar lado a lado as faltas trifásicas com suporte LVRT do ONS e as faltas assimétricas nas duas sintonias."),
    (24, "Reserva Cap. 2", "Na energização, o PLL inadequado leva cerca do dobro do tempo para travar", "Fig. 5.3",
     "Reserva estática do Capítulo 2 do painel HTML (34/40 ms nominal vs. 42/79 ms inadequada).",
     "[Victor] (Reserva do Cap. 2) Na energização sem falta, a sintonia nominal acomoda vd em 34 ms e o erro em 2° em 40 ms; a inadequada leva 42 ms e 79 ms, mas ambas operam travadas antes da falta."),
    (25, "Reserva Cap. 3", "Quanto mais perto da usina, mais severa a falta trifásica, mas o PLL nominal reconverge", "Fig. 5.7, Tab. 5.1",
     "Reserva estática do Capítulo 3 do painel HTML (retenção de 9,2% a 58,4%, pico de 37,3° a 7,3°, retorno de 76 a 112 ms).",
     "[Bruno] (Reserva do Cap. 3) Nas faltas trifásicas com sintonia nominal, a retenção de vd vai de 9,2% na Barra 7 a 58,4% na Barra 6, mas sem sequência negativa o PLL reconverge em todos os casos em até 112 ms."),
    (26, "Reserva Cap. 4", "Faltas assimétricas expõem a fragilidade estrutural do SRF-PLL", "Figs. 5.10 e 5.18",
     "Reserva estática do Capítulo 4 do painel HTML (120 Hz entre 0,29 e 0,72 pu, > 250× maior que nas trifásicas).",
     "[Victor] (Reserva do Cap. 4) Nas faltas assimétricas, a sequência negativa gera oscilação de 120 Hz em dq entre 0,29 e 0,72 pu, mais de 250 vezes maior que nas trifásicas, contaminando o ângulo pois 754 rad/s é apenas 2,32 vezes ωn."),
    (27, "Reserva Cap. 5", "Ganhos menores: compromisso entre filtragem na falta e lentidão na recuperação", "Fig. 5.14, Tab. 5.3",
     "Reserva estática do Capítulo 5 do painel HTML (B6 bifásica cai de 96,0° para 34,5°, mas retorno na B7 dobra de ~50 para ~96 ms).",
     "[Bruno] (Reserva do Cap. 5) Reduzir os ganhos atenua o pico do erro na Barra 6 bifásica de 96,0° para 34,5°, mas na Barra 7 quase dobra o tempo de retorno pós-falta, preparando a perda de sincronismo."),
    (28, "Reserva Cap. 6", "Dinâmica pós-falta: sob sintonia inadequada, o inversor absorve P em 66,8% do tempo", "Figs. 5.20 e 5.21",
     "Reserva estática do Capítulo 6 do painel HTML (escorregamento de ciclo na B7 trifásica, absorção ativa em 66,8% do pós-falta, média −0,40 pu).",
     "[Bruno] (Reserva do Cap. 6) Sob falta trifásica na Barra 7 com sintonia inadequada, o escorregamento de ciclo faz o inversor absorver potência ativa em 66,8% do pós-falta, com média de −0,40 pu."),
    (29, "Reserva Cap. 7", "Cumprir o Submódulo 2.10 do ONS exige mais do que permanecer conectado", "Fig. 2.2, Tab. 5.2",
     "Reserva estática do Capítulo 7 do painel HTML (Iq = 1,00 pu na B7 entrega só Q = 0,09 pu porque V = 0,10 pu).",
     "[Victor] (Reserva do Cap. 7) Nas trifásicas o inversor cumpre a rampa do Submódulo 2.10, mas na Barra 7 a corrente máxima entrega apenas 0,09 pu de reativo devido à tensão de 0,10 pu, provando que permanecer conectado não basta."),
]
