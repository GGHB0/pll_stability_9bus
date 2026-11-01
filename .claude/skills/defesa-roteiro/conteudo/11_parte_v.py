# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
tab(["Material", "Para quê"], [
    ["defesa_qa.pdf", "respostas prontas para os pontos em que deck e TCC se cruzam "
     "(contagem de cenários, 22.547 &#215; 23.368 MW, sobrecorrentes, grid-forming)"],
    ["criterio_acomodacao_srf_pll.pdf", "por que o critério de 1% no t<sub>s</sub>"],
    ["sintonia_srf_pll_nota_tecnica.pdf", "derivação completa dos ganhos do PLL"],
    ["medicao_escorregamento_srf_pll.pdf", "como o escorregamento de ciclo é medido"],
], [5.6, 9.1])

# =============================================================================
n.pagebreak()
n.h("Folha de números")
tab(["Grupo", "Número", "O que é"], [
    ["Motivação", "23.368 MW (34,5%); 265 GW&#183;s", "Brasil 2023: carga perdida; inércia"],
    ["", "> 2,5 GW; 0,63 Hz", "Ibéria 2025"],
    ["", "11.066 MW; 73%", "Chile 2025"],
    ["Modelo", "100 MW = 1 pu; 100 MVA; 60 Hz", "UFV na Barra 2 (era G2 de 192 MVA)"],
    ["", "16.329,93 V", "pico nominal de fase, base do pu do PLL"],
    ["", "5 kHz; 30,71 mH; 9.068,99 rad/s", "PWM; L<sub>est</sub>; ressonância do LCL"],
    ["PLL nominal", "460; 105.820", "K<sub>p</sub>; K<sub>i</sub>"],
    ["", "325,3 rad/s (51,8 Hz); 0,707; 20 ms", "&#969;<sub>n</sub>; &#958;; t<sub>s</sub>"],
    ["PLL inadequada", "92; 21.164", "&#215; 0,2"],
    ["", "145,5 rad/s; 0,316", "&#969;<sub>n</sub>; &#958;"],
    ["", "754 rad/s = 2,32&#183;&#969;<sub>n</sub>", "120 Hz contra a banda nominal"],
    ["Protocolo", "0,1 / 0,3 / 0,4 / 0,6 s", "inicialização / falta / eliminação / fim"],
    ["Energização", "40 / 79 ms; 34 / 42 ms", "erro em 2°; v<sub>d</sub> em 5%"],
    ["Trifásicas", "9,2 / 11,3 / 47,1 / 58,4%", "retenção B7 / L7-8 / L8-9 / B6"],
    ["", "37,3 / 32,5 / 29,8 / 7,3°", "pico do erro"],
    ["", "98 / 98 / 112 / 76 ms", "retorno a 2°"],
    ["", "0,0002 a 0,0011 pu", "120 Hz nas trifásicas"],
    ["Assimétricas", "0,29 a 0,72 pu; &gt; 250&#215;", "120 Hz em v<sub>d</sub>"],
    ["", "17,8% / 14,0%", "tempo com erro &gt; 90°, B7 bifásica, nom. / inad."],
    ["Compromisso", "96,0° &#8594; 34,5°; 48 &#8594; 30 ms", "B6 bifásica, pico; retorno"],
    ["", "46 &#8594; 95; 51 &#8594; 96; 76 &#8594; 106 ms", "retorno B7 mono; B7 bi; B6 tri"],
    ["Sincronismo", "9,2% / 8,2%; 98 ms / não retorna", "B7 trifásica nom. / inad."],
    ["", "66,8% (média &#8722;0,40 pu); 9,7%", "P absorvida, inadequada; retenção L7-8 inad."],
    ["ONS", "(0,85 &#8722; V)/0,35; 0,5 pu", "rampa; saturação em 1 pu"],
    ["", "0,10 pu &#8594; Q = 0,09 pu; 0,72 contra 0,76",
     "B7: tensão e reativo; B6: i<sub>q,ref</sub> contra a rampa"],
], [2.8, 5.6, 6.3])
