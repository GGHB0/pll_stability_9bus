# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
# =============================================================================
# PARTE I
# =============================================================================
parte("PARTE I · PowerPoint, slides 1 a 17",
      "Motivação (2-4), modelagem (5-15) e método (16-17). A modelagem é a parte mais "
      "teórica da defesa e a que mais rende pergunta: cada slide dela tem um bloco de "
      "fundamentos.")

# --- 1
slide(1, "Capa", "Abertura", "Bruno", "capa")
box("msg", "Quem somos, o título e os cinco blocos: contexto, fundamentação e modelagem, "
    "metodologia, resultados e conclusões.")
n.p("O título já diz o objeto (o SRF-PLL, não o inversor inteiro) e a condição "
    "(contingências). Orientador: Prof. Oscar Cuaresma Zevallos. Coorientador: Prof. André "
    "Guilherme Peixoto Alves, autor da tese de onde vêm o controle de corrente e parte do "
    "método de sintonia (Alves, Dias e Rolim, 2020).")
ponte("&#8220;Vamos começar pelo contexto que motivou este estudo.&#8221;")

# --- 2
slide(2, "Expansão das renováveis", "Motivação", "Bruno", "Cap. 2 (IEA 2026, ONS 2025)")
box("msg", "Solar e eólica saltaram de 5% para 17% da geração mundial em uma década; no "
    "Brasil a capacidade já passa da carga média.")
sub("Fundamento: o que a máquina síncrona faz sem ninguém mandar")
n.p("Uma máquina síncrona é uma massa girando, acoplada eletromagneticamente à rede. Ela "
    "presta três serviços por pura física:")
bul("<b>Inércia</b>: quando falta potência, a energia cinética do rotor sai sozinha e "
    "freia a queda de frequência.",
    "<b>Corrente de curto</b>: numa falta, entrega várias vezes a corrente nominal, o que "
    "sustenta a tensão e faz a proteção enxergar o defeito.",
    "<b>Tensão interna</b>: é uma fonte de tensão atrás de uma reatância; impõe tensão e "
    "ângulo à rede.")
eq(r"E_c = \dfrac{1}{2} J \omega_m^2 \qquad H = \dfrac{E_c}{S_n}\ \ [\mathrm{s}]",
   onde="J: momento de inércia; &#969;<sub>m</sub>: velocidade mecânica; S<sub>n</sub>: "
        "potência nominal. A constante H é a energia armazenada em segundos de potência "
        "nominal. Somando H&#183;S de todas as máquinas, a inércia de um sistema sai em "
        "GW&#183;s: é a unidade dos 265 GW&#183;s do slide 3.")
n.p("O inversor não tem nada disso por natureza. Ele se comporta como uma <b>fonte de "
    "corrente controlada</b>, com corrente limitada perto da nominal pelos semicondutores, "
    "e entrega o que o controle manda. Trocar máquinas por inversores transfere a "
    "sustentação da rede da física para o algoritmo, e o SRF-PLL é a peça do algoritmo que "
    "diz ao inversor onde a rede está.")
nums([["600 TWh", "crescimento da geração solar mundial em 2025, ~70% do aumento global"],
      ["5% &#8594; 17%", "participação de solar + eólica no mundo em uma década"],
      ["~30% / 35%", "União Europeia / Brasil com MMGD (na fala)"],
      ["96,8 GW", "eólica, solar e MMGD no SIN em 2025 (+279% desde 2020)"],
      ["85,8 GWmed", "carga média nacional, já superada pela capacidade acima"],
      ["800 GW", "adições renováveis no mundo em 2025, 23º recorde (só na fala)"]])
box("banca", "<b>Qual é a consequência para a rede?</b> A geração nova chega por inversores, "
    "e a síncrona, que impõe tensão e frequência pela inércia, perde espaço.")
box("cuidado", "MMGD = micro e minigeração distribuída. Capacidade (GW) não é energia "
    "(GWmed): 96,8 GW contra 85,8 GWmed mostra escala, não que a carga é atendida só por "
    "renováveis.")
ponte("se a rede depende do controle, falhas de controle deveriam aparecer em eventos "
      "reais. E aparecem.")

# --- 3
slide(3, "Eventos no mundo real", "Motivação", "Bruno",
      "Cap. 2, §2.4 (RAP do ONS, ENTSO-E, CEN)")
box("msg", "Os três grandes blecautes recentes passaram pela geração conectada por "
    "inversores.")
sub("Os três eventos")
bul("<b>Brasil, 15/08/2023.</b> Abertura de uma linha de 500 kV pela proteção, afundamento "
    "de tensão no Nordeste, desligamentos em cascata e quatro ilhas. O ONS descartou falta "
    "de inércia (cerca de 265 GW&#183;s) e de potência de curto: foi colapso de tensão, "
    "porque o suporte dinâmico de reativos das eólicas e fotovoltaicas ficou muito aquém "
    "dos modelos. É o evento que motiva o TCC.",
    "<b>Península Ibérica, 28/04/2025.</b> Oscilação de 0,63 Hz classificada pela ENTSO-E "
    "como instabilidade guiada por conversores: usinas em fator de potência fixo, sem "
    "suporte dinâmico de tensão; mais de 2,5 GW desconectaram por sobretensão e a "
    "península perdeu o sincronismo com a Europa.",
    "<b>Chile, 25/02/2025.</b> Desligamento em 500 kV dividiu o país em duas ilhas em "
    "1,5 s; a norte colapsou por instabilidade de tensão e a centro-sul por queda de "
    "frequência; 11.066 MW de carga perdida num sistema com 73% "
    "de solar e eólica. O CEN passou a rever requisitos de controle seguidor (GFL) e "
    "formador de rede (GFM).")
sub("Fundamento: por que reativo segura a tensão")
n.p("Numa linha de transmissão, a queda de tensão entre as pontas depende da potência que "
    "passa por ela. Como a reatância X é muito maior que a resistência R, o termo do reativo "
    "manda:")
eq(r"\Delta V \approx \dfrac{R\,P + X\,Q}{V} \approx \dfrac{X\,Q}{V} \qquad (X \gg R)",
   onde="Quem injeta reativo perto da carga reduz a queda e sustenta a tensão; sem esse "
        "suporte, a tensão cai, as cargas puxam mais corrente e a queda piora: é o colapso "
        "de tensão. Por isso o diagnóstico do ONS fala em suporte dinâmico de reativos, e "
        "por isso o Submódulo 2.10 (slide 14) pede corrente reativa na falta.")
sub("Fundamento: seguidor (GFL) e formador de rede (GFM)")
n.p("O <b>seguidor de rede</b> (grid-following, o deste TCC) mede a tensão, estima o "
    "ângulo com o PLL e injeta corrente nesse ângulo: depende de uma rede que já exista e "
    "tenha tensão bem definida. O <b>formador de rede</b> (grid-forming) impõe a própria "
    "tensão e o próprio ângulo, como uma máquina. GFM está fora do escopo.")

sub("Brasil em detalhe: o que o relatório do ONS conta")
n.p("O relatório de análise de perturbação do ONS (RAP-ONS 00012/2023, 572 páginas) é a "
    "fonte do §2.4.3. A perda foi de 23.368 MW: 12.689 MW no Norte e Nordeste e 10.680 MW "
    "no Sul, Sudeste e Centro-Oeste.")
box("cuidado", "Tudo o que vem a seguir sai do relatório do ONS e <b>não está no TCC</b>: "
    "serve para entender o evento e responder à banca, não para a fala. As figuras são "
    "recortes do próprio RAP. Nos mapas do ONS, linha vermelha é 500 kV e linha verde é "
    "230 kV.")
instante("08h30 · antes", "O SIN na hora do evento: o Nordeste exportando",
         "A partir das 5h30 a geração solar do Nordeste cresceu, e às 8h a eólica do Ceará "
         "somou-se a ela. No minuto anterior ao evento, o Nordeste gerava 22.454 MW (16.317 MW "
         "de eólica e 3.211 MW de solar) para uma carga de 10.151 MW. Os cerca de 12.300 MW de "
         "sobra saíam da região por dois caminhos: para o Norte (FNEN) e para o Sudeste "
         "(FNESE). O mapa abaixo é o retrato do SIN que o ONS usa no relatório.")
figura(rap_fig("mapa_sin", 16, (60, 206, 524, 549)),
       "Mapa do SIN às 08h30, com geração e carga por região e os fluxos entre regiões com "
       "seus limites. Fonte: ONS, RAP-ONS 00012/2023, Figura 2-1 (p. 16).")
n.p("Como ler o mapa: cada região tem a sua tabela de geração e carga, e as setas são os "
    "fluxos entre regiões com o valor medido e o limite operativo. Os limites vêm de estudos "
    "que simulam a perda de linhas: é o máximo que pode passar e ainda sobreviver a uma "
    "contingência.")
n.table(["Fluxo entre regiões", "Medido", "Limite", "Situação"], [
    ["Nordeste → Norte (FNEN)", "5.879 MW", "5.800 MW",
     "79 MW acima (1,4%), resto de uma violação de ~6.000 MW às 8h02 que o ONS vinha "
     "reduzindo por redespacho"],
    ["Nordeste → Sudeste (FNESE)", "6.392 MW", "7.000 MW", "91% do limite"],
    ["Norte → Sudeste (FNS)", "528 MW", "4.000 MW", "folgado"],
    ["FNS + FNESE", "6.920 MW", "9.800 MW", "folgado"],
], [4.0, 2.0, 2.0, 6.7])
n.gap(4)
n.note("O limite de 5.800 MW do FNEN era temporário, por causa de um disjuntor em manutenção "
       "na SE São João do Piauí. O próprio ONS registra que essa pequena violação não tem "
       "relação com a perturbação nem com as suas consequências.")

instante("08h30 · Ceará", "Zoom no Ceará: a linha mais carregada da sua história",
         "Fortaleza é um centro de carga alimentado por dois caminhos paralelos: a linha de "
         "500 kV Quixadá–Fortaleza II e o tronco de 230 kV que desce por Aquiraz, Banabuiú e "
         "Milagres. Com a eólica do Ceará no máximo, a linha de 500 kV levava 1.950 MW, o "
         "maior carregamento da sua história.")
figura(rap_fig("ceara_pre", 263, (93, 238, 491, 440)),
       "Fluxos no Ceará imediatamente antes da perda da linha: 1.950 MW em Quixadá–Fortaleza "
       "II. Fonte: ONS, RAP-ONS 00012/2023, Figura 5-24 (p. 263).")

instante("T0 = 36,946 s", "A linha abre sem curto: a proteção estava ajustada abaixo do limite",
         "A linha operava com 2.375 A, e o limite normal dela é 2.390 A: estava a 99,4% do "
         "limite, mas dentro dele. Ela não deveria ter aberto. Abriu porque uma função de "
         "sobrecorrente, que só deveria existir nos primeiros instantes depois de energizar a "
         "linha (lógica SOTF), ficou ativa por erro de implementação, e com ajuste de "
         "<b>2.310 A</b>, abaixo do próprio limite da linha. Bastou a carga normal passar de "
         "2.310 A. O terminal de Quixadá abriu às 8h30min36,946s (T0) e a linha saiu de "
         "serviço sem nenhum curto-circuito.")
figura(rap_fig("origem", 14, (60, 256, 524, 489)),
       "Área de origem da perturbação: em verde, o tronco de 230 kV paralelo à linha "
       "Quixadá–Fortaleza II. Fonte: ONS, RAP-ONS 00012/2023, Figura 1-1 (p. 14).")
n.p("<b>O que era esperado.</b> Perder uma linha é uma contingência simples, das que a rede "
    "é planejada para aguentar. Essa perda era até prevista: existe um esquema (SEP 5.10.65) "
    "que, se a Quixadá–Fortaleza II cair, desliga por sobrecorrente em 5, 6 e 7 s as três "
    "linhas de 230 kV Banabuiú–Aquiraz, para não passarem do limite de emergência. E os "
    "estudos do ONS, feitos com os modelos das usinas, previam tensões adequadas depois da "
    "perda (Figura 5-28, mais abaixo). O que fez da perda de uma linha um blecaute foi a "
    "tensão.")

instante("T0 até 530 ms", "O fluxo migra para o 230 kV e a tensão desaba no Ceará",
         "Sem a linha de 500 kV, o fluxo que ia por ela passa ao tronco de 230 kV, mais fraco. "
         "Corrente maior numa linha de reatância alta significa mais queda de tensão "
         "(&#916;V &#8776; XQ/V) e mais consumo de reativo pela própria linha. Quem deveria "
         "sustentar a tensão eram as eólicas e solares da região, injetando reativo. Em meio "
         "segundo, a tensão no Ceará estava pela metade.")
figura(rap_fig("tensoes530", 24, (60, 140, 524, 403)),
       "Fluxos e tensões em T0 + 530 ms, com a linha Quixadá–Fortaleza II marcada com X. "
       "Fonte: ONS, RAP-ONS 00012/2023, Figura 3-4 (p. 24).")
tab(["Barra (T0 + 530 ms)", "Tensão", "Barra (T0 + 530 ms)", "Tensão"], [
    ["Icó 230 kV", "0,47 pu", "Açu III 500 kV", "0,57 pu"],
    ["Banabuiú 230 kV", "0,52 pu", "Campo Grande III", "0,57 pu"],
    ["Milagres 230 kV", "0,54 pu", "Boa Esperança", "0,68 pu"],
    ["Milagres II", "0,56 pu", "Presidente Dutra", "0,92 pu"],
], [4.2, 3.15, 4.2, 3.15])
n.p("Para ter escala: no Submódulo 2.10, abaixo de 0,85 pu a usina já tem de injetar "
    "corrente reativa adicional (slide 14), e 0,5 pu fica no meio da rampa. Barras de 230 kV "
    "a 0,5 pu sem curto nenhum, meio segundo depois de uma única linha abrir, é a medida da "
    "gravidade.")

instante("T0 + 530 ms", "Presidente Dutra: a proteção vê uma oscilação e separa Norte e Nordeste",
         "Com a tensão baixa, a impedância vista pelo relé no terminal de Presidente Dutra da "
         "linha Presidente Dutra–Boa Esperança (500 kV) foi caindo devagar, a 55 &#937;/s. O "
         "relé distingue curto de oscilação pela velocidade: abaixo de 1.500 &#937;/s, ele "
         "entende oscilação de potência. Ao chegar à característica ajustada, a proteção de "
         "perda de sincronismo disparou e, pelo esquema ECE 4.14.11, levou junto as linhas "
         "para Teresina (C1 e C2) e Imperatriz (C2). A corrente estava em 2.153 A, 8% acima do "
         "limite de longa duração de 2.000 A. Com isso, a interligação Norte–Nordeste por "
         "Presidente Dutra se abriu.")
