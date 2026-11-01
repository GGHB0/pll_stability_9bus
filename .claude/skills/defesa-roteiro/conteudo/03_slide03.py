# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
instante("T0 + 570 ms a 1,8 s", "O tronco de 230 kV abre pela proteção de distância",
         "Quarenta milissegundos depois, a proteção de distância abriu Milagres–Icó (230 kV) "
         "com <b>0,54 pu e 897 A, 11% acima do limite de 810 A</b>. A linha levava 177 MW e "
         "absorvia 66 Mvar. Para o relé, tensão baixa e corrente alta é cara de curto. Seguem "
         "Aquiraz–Banabuiú (608 ms), São João do Piauí–Ribeiro Gonçalves C2 no 500 kV "
         "(609 ms), Milagres–Banabuiú C3 (669 ms) e C1 (1.773 ms), e o tronco de 230 kV entre "
         "Milagres e Fortaleza fica aberto.")
figura(rap_fig("tronco230", 31, (88, 164, 494, 368)),
       "Sequência de aberturas no tronco de 230 kV entre Milagres e Fortaleza, com o instante "
       "e a proteção de cada uma. Fonte: ONS, RAP-ONS 00012/2023, Figura 3-12 (p. 31).")
n.note("O ONS observa que essas aberturas só anteciparam o que o SEP 5.10.65 faria em 5 a 7 s "
       "pela sobrecarga. O problema não foi a proteção de distância errar, e sim a tensão "
       "estar baixa a ponto de a carga parecer curto.")

instante("~T0 + 1,8 s", "Perda de sincronismo: centros elétricos no tronco de 500 kV",
         "Com tantas linhas abertas, o Nordeste ficou ligado ao resto do SIN por poucos "
         "caminhos, que passaram a carregar mais. O ângulo entre as áreas abriu e começou a "
         "oscilação de potência. Quando duas áreas ficam quase em oposição de fase, aparece "
         "num ponto da linha entre elas uma tensão quase nula, o <b>centro elétrico</b>, e os "
         "relés perto dele veem algo parecido com um curto. Os centros se formaram quase ao "
         "mesmo tempo em várias linhas de 500 kV, e as proteções de perda de sincronismo foram "
         "abrindo uma a uma (Poções III–Padre Paraíso a T0 + 1,788 s e 1,825 s).")
figura(rap_fig("centros", 43, (123, 244, 461, 483)),
       "Centros elétricos identificados por volta de 8h30min38,730s. Fonte: ONS, RAP-ONS "
       "00012/2023, Figura 3-27 (p. 43).", largura=7.0)

instante("T0 + 2,642 s", "O Norte se separa do SIN, levando parte do Ceará e do Piauí",
         "A abertura de Serra da Mesa–Gurupi (C1 e C2, pela proteção de perda de "
         "sincronismo), depois de Gurupi–Peixe II e do tronco Gurupi–Miracema, isolou o "
         "Subsistema Norte do restante do SIN. A ilha do Norte levou junto parte do Ceará, do "
         "Piauí e do Rio Grande do Norte. Faltando geração, a frequência caiu, o corte de "
         "carga atuou, geradores desligaram, e a ilha colapsou.")
figura(rap_fig("sep_norte", 87, (97, 510, 487, 710)),
       "Momento da separação do Subsistema Norte; em amarelo, os desligamentos do tronco que "
       "levaram a ela. Fonte: ONS, RAP-ONS 00012/2023, Figura 3-77 (p. 87).")

instante("T0 + 5 s", "A linha de origem volta e cai de novo",
         "Às 8h30min41,976s o religamento automático fechou a Quixadá–Fortaleza II. A função "
         "de sobrecorrente esquecida continuava ativa: a corrente chegou a 2.600 A, contra o "
         "ajuste de 2.310 A e o limite de 2.390 A, e a linha abriu de novo 153 ms depois. Uma "
         "falha no algoritmo de religamento ainda fechou o segundo disjuntor (T0 + 5,541 s) "
         "sem verificar o sincronismo.")

instante("3,5 s a 19,8 s", "As outras ilhas",
         "Acre/Rondônia se separa por volta de 3,5 s, com sobrefrequência e sobretensão, e "
         "colapsa. Parte do Nordeste vira ilha por volta de 19,8 s e, apesar de "
         "desligamentos por sobretensão, estabiliza. O Sul, o Sudeste, o Centro-Oeste e o "
         "sudoeste da Bahia ficam juntos e se equilibram com o corte de carga. A perda total "
         "foi de 23.368 MW: 12.689 MW no Norte e Nordeste e 10.680 MW no Sul, Sudeste e "
         "Centro-Oeste.")

instante("Esperado × real", "O gráfico que explica o relatório inteiro",
         "Depois do evento, o ONS simulou só a abertura da Quixadá–Fortaleza II, partindo do "
         "estado real da rede naquele minuto. Com os modelos oficiais das usinas (curva azul), "
         "a tensão em Açu III, o ponto mais próximo da linha, afunda por um instante e "
         "<b>volta a cerca de 1 pu</b>: não aconteceria nada. A medição de campo (curva "
         "vermelha) cai continuamente para ~0,7 pu em 0,4 s, ~0,6 pu em 0,6 s e ~0,43 pu em "
         "0,8 s.")
figura(rap_fig("acu", 268, (65, 172, 519, 400)),
       "Tensão em Açu III 500 kV: medição de campo (vermelho), simulação com a base oficial "
       "(azul) e com a base ajustada (verde). Fonte: ONS, RAP-ONS 00012/2023, Figura 5-28 "
       "(p. 268).")
n.p("Para a simulação reproduzir o campo (curva verde), o ONS teve de alterar os modelos das "
    "eólicas e solares em dois pontos: o controle de reativo da usina (PPC) e a "
    "<b>lógica de injeção de corrente reativa sob falta dos inversores</b>. Com isso a "
    "simulação passou a reproduzir até a atuação da proteção em Presidente Dutra. É a prova "
    "do §7.10: a rede caiu porque as usinas entregaram menos reativo do que o modelo "
    "prometia. E injeção de corrente reativa sob falta é exatamente o requisito do "
    "Submódulo 2.10 que o TCC verifica, e que depende do ângulo estimado pelo PLL.")

n.table(["Grandeza", "Real", "Limite ou esperado", "Leitura"], [
    ["Corrente na Quixadá–Fortaleza II", "2.375 A", "limite 2.390 A",
     "99,4% do limite: carregada, mas legal"],
    ["Ajuste da sobrecorrente esquecida", "2.310 A", "acima do carregamento máximo da linha",
     "ajuste 3% abaixo do limite: erro"],
    ["Fluxo Nordeste → Norte", "5.879 MW", "5.800 MW", "1,4% acima, sem relação com o evento"],
    ["Tensão em Açu III (~0,6 s)", "~0,6 pu", "~1,0 pu (simulação oficial)",
     "o modelo das usinas não representava o campo"],
    ["Tensão em Banabuiú e Icó (530 ms)", "0,52 e 0,47 pu", "~1 pu em operação",
     "metade da tensão sem curto"],
    ["Corrente em Pres. Dutra–Boa Esperança", "2.153 A", "2.000 A", "8% acima"],
    ["Velocidade da impedância (P. Dutra)", "55 &#937;/s", "1.500 &#937;/s separa curto "
     "de oscilação", "lenta: lida como oscilação, abre a interligação"],
    ["Corrente em Milagres–Icó", "897 A a 0,54 pu", "810 A", "11% acima: parece curto"],
    ["Religamento da linha de origem", "2.600 A", "2.390 A", "cai de novo pelo mesmo erro"],
], [4.4, 2.6, 3.4, 4.3])
n.gap(8)
n.p("<b>Fundamento: as três proteções da cascata.</b>")
bul("<b>Fechamento sob falta (SOTF):</b> fica armada no instante em que a linha é "
    "energizada e dispara sem retardo se houver sinal de curto, para o caso de fechar o "
    "disjuntor sobre um aterramento esquecido. Em 15/08 uma sobrecorrente ligada a "
    "ela ficou ativa por erro, ajustada abaixo do limite da linha, e abriu a linha com "
    "carga normal: foi uma atuação acidental, e é o gatilho.",
    "<b>Distância:</b> mede a impedância vista pelo relé, Z = V/I, e dispara se ela cair "
    "dentro da zona ajustada. Num curto, V cai e I sobe, e Z fica pequena. O problema é que "
    "afundamento com sobrecarga faz a mesma coisa: com 0,54 pu e 897 A, a linha Milagres–Icó "
    "pareceu estar em falta sem estar.",
    "<b>Perda de sincronismo:</b> acompanha a trajetória da impedância quando o ângulo entre "
    "duas áreas abre demais e separa as áreas antes que oscilem uma contra a outra. Ela "
    "abriu o tronco de 500 kV que ligava o Norte ao Nordeste.")
eq(r"Z_{ap} = \dfrac{V}{I} \quad\downarrow \quad \mathrm{se}\ V\downarrow\ \mathrm{e}\ "
   r"I\uparrow \quad \mathrm{(curto\ ou\ afundamento\ com\ sobrecarga)}",
   onde="É por isso que o colapso de tensão se propaga pela proteção: cada linha que abre "
        "joga o fluxo nas vizinhas, que ficam com tensão menor e corrente maior e passam a "
        "parecer em falta.")
tab(["Ilha", "Separa em", "O que houve", "Desfecho"], [
    ["Norte", "~2,6 s", "Subfrequência; corte de carga atua, geradores desligam",
     "Colapso"],
    ["Acre/Rondônia", "~3,5 s", "Sobrefrequência e sobretensão", "Colapso"],
    ["Parte do Nordeste", "~19,8 s", "Sobrefrequência e sobretensão; desligamentos",
     "Estabiliza"],
    ["Sul/SE/CO e sudoeste da BA", "—", "Corte de carga restabelece o equilíbrio",
     "Permanece estável"],
], [3.6, 2.2, 6.3, 2.6])
n.p("<b>O fator determinante.</b> O ONS conclui que \"o desempenho dos controles em campo, "
    "de usinas eólicas e fotovoltaicas, em especial no que tange à capacidade de suporte "
    "dinâmico de potência reativa, foi muito aquém dos modelos matemáticos fornecidos pelos "
    "agentes\". Cada usina entrega ao ONS um modelo do seu controle, e o ONS usa esses "
    "modelos para decidir quanto a rede pode transportar com segurança. Se no afundamento "
    "a usina injeta menos reativo do que o modelo promete, a tensão cai mais do que o "
    "estudo previa, e um cenário que parecia seguro deixa de ser. O relatório registra a "
    "divergência, mas não aponta o mecanismo dentro do controle que a causou. É nesse "
    "ponto que o TCC entra: o inversor só injeta a corrente reativa certa se o PLL souber "
    "onde está a tensão, e é o PLL sob afundamento que o trabalho simula.")
n.p("<b>O que o ONS descarta.</b>")
bul("<b>Inércia:</b> o SIN tinha cerca de 265 GW&#183;s para uns 73 GW de carga, "
    "proporção acima da de vários sistemas no mundo. O colapso foi de tensão, não de "
    "frequência, e mais inércia não o teria evitado.",
    "<b>Potência de curto-circuito:</b> adequada a todos os critérios dos Procedimentos de "
    "Rede. Mais máquinas síncronas na região não dariam margem para esse fenômeno; o risco "
    "continuaria parecido enquanto persistisse a diferença entre modelo e campo.",
    "<b>Oscilação de potência como causa:</b> não houve nos primeiros instantes; a abertura "
    "angular entre áreas foi consequência da queda de tensão.")
box("alem", "<b>Referência acadêmica sobre o evento.</b> Xiong et al. (2025), citado na "
    "Motivação por indicação do orientador, aponta como uma das causas a falha das "
    "proteções de oscilação de potência baseadas em impedância numa área com muita geração "
    "seguidora de rede: essas proteções foram pensadas para máquinas síncronas, e o "
    "inversor oscila de outro jeito. É também a fonte dos dados das linhas do modelo. O "
    "artigo não traz MW nem porcentagem de carga perdida; esses números são do RAP.",
    "<b>Recomposição:</b> partida autônoma em Tucuruí, Balbina, Coaracy Nunes, Estreito e "
    "Samuel, com várias tentativas falhas; o ONS autorizou a recomposição total das cargas "
    "às 14h49.")
box("prova", "<b>Se não faltou inércia, então o que faltou?</b> Suporte dinâmico de reativo "
    "das eólicas e fotovoltaicas no afundamento, abaixo do que os modelos prometiam.",
    "<b>O PLL causou o blecaute?</b> O ONS não diz isso, nem o TCC. O relatório mostra que "
    "o controle das usinas respondeu pior que o modelo e não aponta o mecanismo; o TCC "
    "estuda um elo necessário dessa resposta, o sincronismo sob afundamento e assimetria.",
    "<b>Não foi uma falta?</b> Não: o gatilho foi uma abertura de linha sem curto. O que o "
    "inversor viu foi um afundamento de tensão, e é isso que as faltas simuladas reproduzem "
    "no ponto de conexão.")

sub("Península Ibérica em detalhe: a tensão que subiu demais")
n.p("Era um dia de primavera com muita geração solar no sudoeste da Espanha (cerca de "
    "18,7 GW), bem acima do consumo da região, e a Espanha exportava 5 GW. A energia "
    "atravessava longas distâncias e a tensão da rede de 400 kV já oscilava desde as 9h, "
    "chegando perto do limite de 435 kV às 10h30. Diferente do Brasil, o problema não foi "
    "tensão baixa: foi <b>tensão alta</b>, e o desligamento das usinas por sobretensão.")
n.table(["Hora (local)", "O que aconteceu"], [  # pode partir: evita vão no fim da página
    ["12h03–12h08", "Oscilação de 0,63 Hz, só na península, imposta por uma usina "
                    "inversorizada (oscilação forçada, guiada por conversor)"],
    ["12h19–12h22", "Oscilação de 0,2 Hz entre áreas: a Ibéria oscila contra o centro da "
                    "Europa"],
    ["12h20–12h30", "As medidas contra as oscilações (religar linhas, reduzir a exportação "
                    "para a França) funcionam, mas sobem a tensão; reatores desligados nas "
                    "oscilações não voltam"],
    ["12h32min57s", "Primeiro desligamento por sobretensão: transformador em Granada"],
    ["12h33min16s–21s", "Badajoz e cascata de eólicas e solares: mais de 2,5 GW perdidos; "
                        "a frequência cai"],
    ["12h33min19s–24s", "Perda de sincronismo com a Europa; abrem as ligações com França e "
                        "Marrocos; colapso de Espanha e Portugal"],
], [3.3, 11.4])
n.gap(8)
n.p("<b>O mecanismo central: fator de potência fixo.</b> As renováveis espanholas operavam "
    "absorvendo reativo numa proporção fixa da potência ativa, e não por tensão medida:")
eq(r"Q = P\,\tan\varphi \quad\rightarrow\quad \Delta Q = \Delta P\,\tan\varphi",
   onde="&#966;: ângulo do fator de potência, fixo por regulamento (0,98 indutivo a 0,98 "
        "capacitivo). Quando o despacho reduz P, a absorção de reativo cai na mesma "
        "proporção, e pela relação &#916;V &#8776; XQ/V acima a tensão sobe. E nada "
        "reage à tensão, porque Q não depende dela.")
n.p("Daí nasce um laço de realimentação positiva:")
bul("o despacho reduz a potência ativa das renováveis (cerca de 0,4 a 0,5 GW às 12h30);",
    "a absorção de reativo cai junto e a tensão sobe;",
    "a proteção de sobretensão desliga usinas, algumas com ajuste fora do exigido e sem "
    "temporização;",
    "a usina desligada deixa de absorver reativo e a tensão sobe mais, até a cascata.")
