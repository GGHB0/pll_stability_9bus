---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-27: 31 slides, com o "Filtro LCL" novo no 13 (da linha
> "13 Controle de corrente" em diante, somar +1). Em 2026-10-21: 30 slides (12 e 13 do inversor, 14-17 do ONS e
> sistema completo; as linhas abaixo do 17 ainda usam a numeração antiga:
> somar +5; outra sessão também passou a demo para antes da energização). Em 2026-10-19: 29 slides, 16:9, com a **demonstração ao vivo do
> painel HTML** (slide 16), alinhado ao TCC entregue (VFinal, 15/10): só o
> que está no TCC, salvo a exceção de método do bloco MODELAGEM (slides 9
> e 12, ver [[defesa-pendencias]]). Arquivo e
> pipeline: skill [tcc-pptx-editor](../../skills/tcc-pptx-editor/SKILL.md).
> Cada slide resume uma parte do TCC: a coluna "TCC" diz onde conferir
> (seções e figuras de [[tcc-docx-content-map]]). Pendências em
> [[defesa-pendencias]].

## Corpo (slides 1-21, 25,4 min de roteiro a 130 ppm + ~1,5 min de cliques na demo; limite 30)

| # | Mensagem (título) | TCC | Números a conferir |
|---|---|---|---|
| 1 | Capa: título, autores, orientadores | capa | |
| 2 | A rede troca inércia mecânica por controle dos conversores | Cap. 2 (IEA) | 600 TWh, ~70%, 5% → 17% |
| 3 | Blecautes recentes passaram pela geração inversorizada | Cap. 2, [[brasil-2023-overview]] | 23.368 MW (§2.4.3), 265 GW·s; > 2,5 GW por sobretensão, 0,63 Hz antes do colapso; 11.066 MW, 73% |
| 4 | SRF-PLL depende de tensão boa, que a falta destrói + objetivos (redação do TCC) | Cap. 1 | 120 Hz |
| 5 | Título curto "Fonte renovável" + frase de abertura "A usina fotovoltaica ou eólica se conecta à rede por um inversor seguidor de rede" (barra azul, 2026-10-19; abre a MODELAGEM e resume o que vem: Fig. 3.2 redesenhada na largura da moldura, `assets/diagrams/vsi_grid_blocos_defesa.svg`, notação v, SRF-PLL em laranja; cartões Fonte primária, Conversão, Seguidor de rede; gancho para Park "Como o inversor segue a rede?") | Fig. 3.2, §3.2, §4.1, §4.3.1 | 100 MW; CC ideal, elo CC e MPPT fora do escopo; nenhum outro número |
| 6 | Título curto "Transformada de Park" + frase de abertura "Girando com a rede, a transformada de Park torna constantes as grandezas trifásicas" (2026-10-19; equação 3.5 em imagem, θ em laranja; 2 cartões lado a lado embaixo; gancho "E o ângulo θ?"). Desde 2026-10-24 a moldura tem dois painéis: equação com 5,45 in à esquerda, divisória, e à direita **exceção de método** com `park_dq_vetor_defesa.svg` (abc + dq girante, v projetado) e `park_senoides_constantes_defesa.svg` (senoides → Park → constantes). Desde 2026-10-27, sob a matriz, `park_vdq_pll.png` (v_d e v_q com θ = θ_PLL; v_d fora do TCC, ver pendências) | Eq. (3.5), §3.1.2, fim da §3.1.3, §3.4 (antes da 3.10) | figura `assets/diagrams/park_abc_dq_equacao.svg`; nenhum número |
| 7 | Título curto "Estrutura do SRF-PLL" + frase de abertura "O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede" (2026-10-19; Fig. 4.3 redesenhada nas 2 primeiras colunas, com áreas tracejadas PD/PI/VCO da Fig. 3.3, `assets/diagrams/pll_control_loop_defesa.svg`, notação v; cartão "Sintonia do PI" à direita com as equações em texto Cambria Math; cartões PD, PI e VCO em linha embaixo; "Por que o travamento importa?") | Fig. 4.3, §3.5, resumo do Cap. 3 | equações da Fig. 4.3: KpPLL = 2ξωn, KiPLL = ωn², s² + KpPLL·U·s + KiPLL·U = 0 |
| 8 | Título curto "Sistema IEEE 9 barras" + frase de abertura "A UFV assume a Barra 2 e enxerga o resto da rede como um equivalente de Thévenin" (2026-10-19) | Fig. 4.1, §4.3.1 | 192 MVA original, 100 MW; sem R_th/L_th na tela |
| 9 | **Exceção de método**: título curto "Bancada do PLL" + frase de abertura "Antes do inversor, o SRF-PLL foi testado isolado entre duas fontes ideais" (2026-10-19); figura com a geração à esquerda e a rede à direita (fonte ideal, Z, PCC, Z_th, barramento infinito) | [[psim-modeling]] (fora do TCC) | figura `assets/diagrams/pll_bancada_duas_fontes.svg`; nenhum número |
| 10 | Título curto "Sintonia do PLL" + frase de abertura "Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação" (2026-10-19, layout B: 4 etapas empilhadas à esquerda, tensão em pu / linearizar / forma canônica / ξ = 0,707 (pu desde 2026-10-19, noite); régua do ts à direita, `assets/diagrams/pll_ts_regua_defesa.svg`; caixa final com a conta) | §3.4, eqs. (3.10)-(3.20), [[pll-loop-filter-gains]] | 16.329,93 V de pico, Vm = 1 pu, Kpd = 1; ξ 0,707, ~5%; ts = 4,6/(ξωn), Kp = 9,2/ts = 460, ωn 325,3 rad/s (51,8 Hz), Ki 105.820; régua só com "1 período" e 20 ms (sem 16,7 ms) |
| 11 | Título curto "Duas sintonias do PLL" + frase de abertura "A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos amortecido" (slide novo em 2026-10-19; tabela nominal × inadequada com a inadequada em laranja, cartão 2ω0 = 2,32·ωn, "Por que reduzir os ganhos?") | §3.4 (eq. 3.20 e parágrafo seguinte), §4.3, [[cenarios-simulados]] | Kp 460/92, Ki 105.820/21.164, ωn 325,3/145,5, ξ 0,707/0,316; 754 rad/s = 2,32 ωn |
| 12 | Título curto "Referência de corrente" + frase "Na primeira versão do inversor, a referência de corrente saía direto da potência desejada" (2026-10-20, exceção de método): diagrama da 1ª versão no PSIM (`assets/diagrams/referencia_corrente_psim.svg`: Pref 1 pu com "t = 35 ms", Qref = 0, ÷ vd do SRF-PLL, malha e PWM tracejados); cartão Eq. 3.9 invertida; "Por que o PLL importa aqui?" | §3.1.3, §3.1.4, §4.3.1, [[psim-netlists]] | id,ref = 2P/(3vd), iq,ref = −2Q/(3vd); 1 pu = 100 MW; 35 ms (único número fora do TCC, aprovado) |
| 13 | **Novo em 2026-10-27.** Título curto "Filtro LCL" + frase "Quatro passos fixam o filtro, com a ressonância entre a rede e o chaveamento": `assets/diagrams/lcl_filtro_defesa.svg` (circuito por fase com Vcc constante, régua 60 Hz / ωres / 5 kHz); 4 cartões (L1 pelo ripple, L2 = k·L1, ωres, Rd = 5% da reatância); rodapé "Por que a ressonância fica no meio?" e "E o barramento CC?" | §4.3.2, §4.3.2.1 (equações: exceção de método, [[lcl-filter]]) | Lest 30,71 mH, ωres 9.068,99 rad/s, Rd1/Rd2/Rd3 0,5734/0,0054/3,1228 Ω, 5 kHz, 60 Hz; sem L1, L2, C nem Vcc |
| 13 | Título curto "Controle de corrente" + frase "Um PI com notch em cada eixo faz a corrente do inversor seguir a referência" (2026-10-20): Fig. 3.1 à esquerda; cartões PWM, Filtro LCL, PI de corrente; "Por que dois PIs?" | Fig. 3.1, §3.5, §4.3.2 | 5 kHz; Lest 30,71 mH, ωres 9.068,99 rad/s, ξ 0,707; ξ 0,707, ωn = 4√2·fg, Kp = 8·fg·Lest, Ki = 32·fg²·Lest |
| 14 | Título curto "Referência pelo ONS" + frase "No modelo final, as referências fixas deram lugar ao bloco do Submódulo 2.10" (2026-10-21): `assets/diagrams/referencia_corrente_ons.svg` (esqueleto do 12, bloco laranja com V_PCC, i_d,nom, I_max; θ_PLL na malha); cartão f(V_PCC); "Quem orienta as correntes?" | Fig. 4.2, §4.3.2 | nenhum número novo; "antes fixas (P = 1 pu, Q = 0)" remete à exceção do 12 |
| 15 | Título curto "Dentro do Submódulo 2.10" + frase "A tensão medida define o reativo, e o ativo fica com o que sobra" (2026-10-21, **gráfico aprovado, não tirar**): `assets/diagrams/ons_logica_defesa.svg` (rampa + círculo de raio I_max); "Por que priorizar o reativo?" | Fig. 2.2, §2.5.2, §5.2 (Tab. 5.2) | rampa (0,85 − V)/0,35, nula em 0,85, nominal em 0,5; círculo = exceção de método; **sem a faixa de sobretensão, de propósito**: incremento de carga e sobretensão estão fora do escopo do trabalho inteiro ([[project-scope]]) |
| 16 | Título curto "Lógica em blocos" + frase "No código, a faixa de tensão escolhe o caminho e a prioridade divide a corrente" (2026-10-21): fluxograma `assets/diagrams/ons_fluxo_defesa.svg`; "E quando a falta é eliminada?" | Fig. 2.2, §5.2 | 0,85, 1,1, 1,2 pu (Fig. 2.2); prioridade = exceção de método |
| 17 | Título curto "Sistema completo" + frase "Juntando as partes, este é o inversor usado em todas as simulações" (2026-10-21): Fig. 4.2 do TCC; cartões Sincronismo, Referência, Corrente e PWM; "E agora?" | Fig. 4.2, §4.3.2 | nenhum número |
| 13 | Título curto "Protocolo de contingência" + frase "Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da falta" (2026-10-19); linha do tempo 0 / 0,1 / 0,3 / 0,4 / 0,6 s; matriz falta × local (analisadas B7, L7-8, L8-9, B6 em azul; B4, B5, B8, B9 em cinza "consultáveis no painel"); cartão "Faltas assimétricas" + "Por que observar até 0,6 s?" | §4.3.4, Tab. 4.1 (atualizada), §5.2 | 0,1 s = exceção de método; matriz = Tab. 4.1 + "I" na monofásica B7; sem contagem de cenários |
| 14 | Título curto "Fluxo de análise" + frase "Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel interativo" (2026-10-20): fluxo **da análise dos resultados** (não as ferramentas da modelagem); 4 cartões Simulink → Arquivos CSV → Python → Painel interativo (destacado); tabela 2 × 5 métrica × como é medida (estilo do slide 11); rodapé-ponte "Dos dados aos resultados" (opção B: partida do inversor, depois o painel ao vivo) | §4.3.3; definições em §5.1-5.3 | retenção em % do pré-falta, pico após o 1º ciclo, retorno a 2° desde a eliminação, 120 Hz do espectro de Vd, P e Q médias na falta; notas: 9,2% (Barra 7 nominal), escorregamento de ciclo (§4.3.3/§5.4) |
| 15 | Energização: inadequada leva ~2× para travar | Fig. 5.3 (dedicada, `assets/charts/defesa/fig_5_3`) | 34/40 ms × 42/79 ms |
| 16 | **Demonstração ao vivo** no painel HTML (3 passos, roteiro nas notas); hoje slide 20: título curto + frase "No painel interativo, três casos resumem o comportamento dos 28 cenários" e layout na grade (2026-10-21, moldura + botão à esquerda, 3 cartões chapados + faixa à direita, Calibri 12 pt) | Fig. 5.18, 5.10 | 98 ms; 8,2%; 66,8%; 0,72 pu |
| 17 | Trifásica: mais perto, mais severa; nominal reconverge (síntese; figura 5,82 in, tabela e nota estreitadas para 5,83 in em x = 7,12) | Fig. 5.7 (dedicada, `fig_5_7`), Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 18 | Assimétricas expõem a fragilidade estrutural (síntese) | Fig. 5.10, 5.18 (dedicadas, `fig_5_10`/`fig_5_18`) | 250×, 98 ms, 106 ms, 754 rad/s = 2,32 ωn |
| 19 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,09 pu com corrente saturada |
| 20 | Conclusões (3 cartões + contribuição); hoje slide 21: título curto "Conclusão" + frase = título antigo, destaque "decisão de estabilidade" (2026-10-21) | Cap. 6 | |
| 21 | Trabalhos futuros, limites, agradecimento; hoje slide 22: frase "Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho", caixas chapadas, Calibri (2026-10-21) | Cap. 7 | |

## Demonstração (slide 16)

O HTML (`output/pll_metrics.html`, Plotly embutido, abre sem internet) é
aberto no navegador **antes** da defesa, já no cenário Barra 7 trifásica
nominal, e alternado com Alt+Tab. Roteiro com os cliques entre parênteses
nas notas do slide 16: (1) aba Inversor UFV + Zoom na falta; (2) toggle
para sintonia inadequada (o painel troca para o cenário equivalente);
(3) Barra 7 bifásica nominal, aba Espectro FFT em dq. Se o navegador
falhar, os slides 17-18 cobrem os mesmos números. Na arguição o painel
fica aberto para "e na barra X?".

De 2026-10-20 a 2026-10-25 o painel abria na aba "Análise TCC"; a aba
saiu e hoje ele abre no **Resumo**, com os capítulos do Cap. 5 só no botão
"Modo apresentação", avançados pelo passador (PageDown)
([[roteiro-demonstracao-dashboard]]). As notas do slide
16 ainda descrevem os 3 cliques antigos, e o tempo da demo (a aba pede 3 a
4 min, contra ~1,5 min) ainda não foi decidido: ver [[defesa-pendencias]].

## Roteiro de estudo (PDF)

`scripts/notas/gen_roteiro_estudo_defesa.py` → `output/roteiro_estudo_defesa.pdf`
(2026-10-25): slide a slide e capítulo a capítulo do palco, na ordem PPTX 1-19 →
slide 20 → palco 1-8 → PPTX 21-22 → apêndice, sem fala decorada; na
modelagem (5-17) a caixa "O que falar" dá os tópicos por pessoa, tirados das
notas do deck e apontando para a parte do slide (dicionário `FALAS`; mudou a
nota ou a posição de um cartão → ajustar ali). Miniaturas: slides
renderizados pelo `render.ps1` em `C:\Temp\defesa_roteiro\png` e prints de
`output/verifica_palco/1920x1080/`. Mudou o deck ou o palco → renderizar de
novo e rodar o gerador.

## Apêndice (22-29, para perguntas; fora do tempo)

| # | Conteúdo | TCC |
|---|---|---|
| 22 | Divisor "Apêndice" (lista o que vem) | |
| 23 | Ganhos menores: compromisso, não piora uniforme (inclui monofásica B7) | Fig. 5.14, Tab. 5.3 |
| 24 | vd e vq nas trifásicas Barra 7 × Barra 6 | Fig. 5.5, 5.6 |
| 25 | Tabelas 5.1 e 5.2 completas | Tab. 5.1, 5.2 |
| 26 | Tabela 5.3 completa (assimétricas), igual à do TCC | Tab. 5.3 |
| 27 | Pós-falta: absorve P em 66,8% do tempo (Barra 7, inadequada) | Fig. 5.20, 5.21 |
| 28 | Classificação estendida de estabilidade | Cap. 2 |
| 29 | Ibéria e Chile 2025 | Cap. 2 |

A coluna "Vd mínima e máxima", sem par no TCC, saiu em 2026-10-17: o deck
só traz o que o TCC traz ([[defesa-pendencias]]).

## Estrutura visual

Visual do template "Project Portfolio" (SlidesCarnival) desde 2026-10-16,
em tons de azul: cabeçalho com linha, linha vertical com o nome da seção
(MOTIVAÇÃO 2-4, MODELAGEM 5-12, MÉTODO 13-14, RESULTADOS 15-19, CONCLUSÃO
20-21, APÊNDICE 22-29), blocos retos sem borda, laranja como único
destaque (azul = nominal, laranja = inadequada). Títulos em frase completa,
pergunta da banca no rodapé. Grade e cores em
[design.md](../../skills/tcc-pptx-editor/referencia/design.md).
