---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-19: 29 slides, 16:9, com a **demonstração ao vivo do
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
| 6 | Título curto "Transformada de Park" + frase de abertura "Girando com a rede, a transformada de Park torna constantes as grandezas trifásicas" (2026-10-19; equação 3.5 em imagem na largura toda, θ em laranja; 2 cartões lado a lado embaixo; gancho "E o ângulo θ?") | Eq. (3.5), §3.1.2, fim da §3.1.3 | figura `assets/diagrams/park_abc_dq_equacao.svg`; nenhum número |
| 7 | Título curto "Estrutura do SRF-PLL" + frase de abertura "O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede" (2026-10-19; Fig. 4.3 redesenhada nas 2 primeiras colunas, com áreas tracejadas PD/PI/VCO da Fig. 3.3, `assets/diagrams/pll_control_loop_defesa.svg`, notação v; cartão "Sintonia do PI" à direita com as equações em texto Cambria Math; cartões PD, PI e VCO em linha embaixo; "Por que o travamento importa?") | Fig. 4.3, §3.5, resumo do Cap. 3 | equações da Fig. 4.3: KpPLL = 2ξωn, KiPLL = ωn², s² + KpPLL·U·s + KiPLL·U = 0 |
| 8 | Título curto "Sistema IEEE 9 barras" + frase de abertura "A UFV assume a Barra 2 e enxerga o resto da rede como um equivalente de Thévenin" (2026-10-19) | Fig. 4.1, §4.3.1 | 192 MVA original, 100 MW; sem R_th/L_th na tela |
| 9 | **Exceção de método**: título curto "Bancada do PLL" + frase de abertura "Antes do inversor, o SRF-PLL foi testado isolado entre duas fontes ideais" (2026-10-19); figura com a geração à esquerda e a rede à direita (fonte ideal, Z, PCC, Z_th, barramento infinito) | [[psim-modeling]] (fora do TCC) | figura `assets/diagrams/pll_bancada_duas_fontes.svg`; nenhum número |
| 10 | Título curto "Sintonia do PLL" + frase de abertura "Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação" (2026-10-19, layout B: 4 etapas empilhadas à esquerda, tensão em pu / linearizar / forma canônica / ξ = 0,707 (pu desde 2026-10-19, noite); régua do ts à direita, `assets/diagrams/pll_ts_regua_defesa.svg`; caixa final com a conta) | §3.4, eqs. (3.10)-(3.20), [[pll-loop-filter-gains]] | 16.329,93 V de pico, Vm = 1 pu, Kpd = 1; ξ 0,707, ~5%; ts = 4,6/(ξωn), Kp = 9,2/ts = 460, ωn 325,3 rad/s (51,8 Hz), Ki 105.820; régua só com "1 período" e 20 ms (sem 16,7 ms) |
| 11 | Título curto "Duas sintonias do PLL" + frase de abertura "A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos amortecido" (slide novo em 2026-10-19; tabela nominal × inadequada com a inadequada em laranja, cartão 2ω0 = 2,32·ωn, "Por que reduzir os ganhos?") | §3.4 (eq. 3.20 e parágrafo seguinte), §4.3, [[cenarios-simulados]] | Kp 460/92, Ki 105.820/21.164, ωn 325,3/145,5, ξ 0,707/0,316; 754 rad/s = 2,32 ωn |
| 12 | O inversor foi montado em etapas: PWM, filtro LCL e escala para 100 MW (sequência = exceção de método) | Fig. 4.2, §4.3.2 | 5 kHz, 100 MW, CC constante, Lest 30,71 mH, ωres, ξ |
| 13 | Título curto "Protocolo de contingência" + frase "Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da falta" (2026-10-19); linha do tempo 0 / 0,1 / 0,3 / 0,4 / 0,6 s; matriz falta × local (analisadas B7, L7-8, L8-9, B6 em azul; B4, B5, B8, B9 em cinza "consultáveis no painel"); cartão "Faltas assimétricas" + "Por que observar até 0,6 s?" | §4.3.4, Tab. 4.1 (atualizada), §5.2 | 0,1 s = exceção de método; matriz = Tab. 4.1 + "I" na monofásica B7; sem contagem de cenários |
| 14 | Título curto "Fluxo de análise" + frase "Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel interativo" (2026-10-20): fluxo **da análise dos resultados** (não as ferramentas da modelagem); 4 cartões Simulink → Arquivos CSV → Python → Painel interativo (destacado); tabela 2 × 5 métrica × como é medida (estilo do slide 11); rodapé-ponte "Dos dados aos resultados" (opção B: partida do inversor, depois o painel ao vivo) | §4.3.3; definições em §5.1-5.3 | retenção em % do pré-falta, pico após o 1º ciclo, retorno a 2° desde a eliminação, 120 Hz do espectro de Vd, P e Q médias na falta; notas: 9,2% (Barra 7 nominal), escorregamento de ciclo (§4.3.3/§5.4) |
| 15 | Energização: inadequada leva ~2× para travar | Fig. 5.3 (dedicada, `assets/charts/defesa/fig_5_3`) | 34/40 ms × 42/79 ms |
| 16 | **Demonstração ao vivo** no painel HTML (3 passos, roteiro nas notas) | Fig. 5.18, 5.10 | 98 ms; 8,2%; 66,8%; 0,72 pu |
| 17 | Trifásica: mais perto, mais severa; nominal reconverge (síntese; figura 5,82 in, tabela e nota estreitadas para 5,83 in em x = 7,12) | Fig. 5.7 (dedicada, `fig_5_7`), Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 18 | Assimétricas expõem a fragilidade estrutural (síntese) | Fig. 5.10, 5.18 (dedicadas, `fig_5_10`/`fig_5_18`) | 250×, 98 ms, 106 ms, 754 rad/s = 2,32 ωn |
| 19 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,09 pu com corrente saturada |
| 20 | Conclusões (3 cartões + contribuição) | Cap. 6 | |
| 21 | Trabalhos futuros, limites, agradecimento | Cap. 7 | |

## Demonstração (slide 16)

O HTML (`output/pll_metrics.html`, Plotly embutido, abre sem internet) é
aberto no navegador **antes** da defesa, já no cenário Barra 7 trifásica
nominal, e alternado com Alt+Tab. Roteiro com os cliques entre parênteses
nas notas do slide 16: (1) aba Inversor UFV + Zoom na falta; (2) toggle
para sintonia inadequada (o painel troca para o cenário equivalente);
(3) Barra 7 bifásica nominal, aba Espectro FFT em dq. Se o navegador
falhar, os slides 17-18 cobrem os mesmos números. Na arguição o painel
fica aberto para "e na barra X?".

Desde 2026-10-20 o painel tem o **modo roteiro** (botão "Roteiro"): 9
passos com legenda, avançados pelo passador (PageDown), do regime ao
comparativo dos casos do TCC ([[roteiro-demonstracao-dashboard]]). As notas
do slide 16 ainda descrevem os 3 cliques antigos, e o tempo da demo (o
roteiro pede 3 a 4 min, contra ~1,5 min) ainda não foi decidido: ver
[[defesa-pendencias]].

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
