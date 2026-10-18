---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-18: 27 slides, 16:9, com a **demonstração ao vivo do
> painel HTML** (slide 14), alinhado ao TCC entregue (VFinal, 15/10): só o
> que está no TCC, salvo a exceção de método do bloco MODELAGEM (slides 8
> e 10, ver [[defesa-pendencias]]). Arquivo e
> pipeline: skill [tcc-pptx-editor](../../skills/tcc-pptx-editor/SKILL.md).
> Cada slide resume uma parte do TCC: a coluna "TCC" diz onde conferir
> (seções e figuras de [[tcc-docx-content-map]]). Pendências em
> [[defesa-pendencias]].

## Corpo (slides 1-19, 23,2 min de roteiro a 130 ppm + ~1,5 min de cliques na demo; limite 30)

| # | Mensagem (título) | TCC | Números a conferir |
|---|---|---|---|
| 1 | Capa: título, autores, orientadores | capa | |
| 2 | A rede troca inércia mecânica por controle dos conversores | Cap. 2 (IEA) | 600 TWh, ~70%, 5% → 17% |
| 3 | Blecautes recentes passaram pela geração inversorizada | Cap. 2, [[brasil-2023-overview]] | 23.368 MW (§2.4.3), 265 GW·s; > 2,5 GW por sobretensão, 0,63 Hz antes do colapso; 11.066 MW, 73% |
| 4 | SRF-PLL depende de tensão boa, que a falta destrói + objetivos (redação do TCC) | Cap. 1 | 120 Hz |
| 5 | Girando com a rede, a transformada de Park torna constantes as grandezas trifásicas (equação 3.5 em imagem na largura toda, θ em laranja; 2 cartões lado a lado embaixo; gancho "E o ângulo θ?") | Eq. (3.5), §3.1.2, fim da §3.1.3 | figura `assets/diagrams/park_abc_dq_equacao.svg`; nenhum número |
| 6 | O SRF-PLL usa a própria transformada de Park para estimar θ (Fig. 4.3 redesenhada nas 2 primeiras colunas, com áreas tracejadas PD/PI/VCO da Fig. 3.3, `assets/diagrams/pll_control_loop_defesa.svg`, notação v; cartão "Sintonia do PI" à direita com as equações em texto Cambria Math; cartões PD, PI e VCO em linha embaixo; "Por que o travamento importa?") | Fig. 4.3, §3.5, resumo do Cap. 3 | equações da Fig. 4.3: KpPLL = 2ξωn, KiPLL = ωn², s² + KpPLL·U·s + KiPLL·U = 0 |
| 7 | A rede vista da Barra 2 se reduz a um equivalente de Thévenin | Fig. 4.1, §4.3.1 | 192 MVA original, 100 MW; sem R_th/L_th na tela |
| 8 | **Novo (exceção de método)**: o primeiro teste pôs o SRF-PLL entre duas fontes ideais | [[psim-modeling]] (fora do TCC) | figura `assets/diagrams/pll_bancada_duas_fontes.svg`; nenhum número |
| 9 | Na bancada, ts = 20 ms levou a Kp 460, Ki 105.820; inadequada −80% (tabela das duas sintonias) | §4.3, [[pll-loop-filter-gains]], [[cenarios-simulados]] | ωn 325,3/145,5; ξ 0,707/0,316; Kp 92, Ki 21.164 |
| 10 | O inversor foi montado em etapas: PWM, filtro LCL e escala para 100 MW (sequência = exceção de método) | Fig. 4.2, §4.3.2 | 5 kHz, 100 MW, CC constante, Lest 30,71 mH, ωres, ξ |
| 11 | Protocolo: falta 0,3-0,4 s, observação até 0,6 s | §4.3.4, Tab. 4.1 | erro de fase em 2° em 40/79 ms; sem contagem de cenários |
| 12 | Pipeline simulação → Python → métricas → painel HTML | [[pipeline-dados]] | retenção 9,2% (definição do TCC) |
| 13 | Energização: inadequada leva ~2× para travar | Fig. 5.3 (dedicada, `assets/charts/defesa/fig_5_3`) | 34/40 ms × 42/79 ms |
| 14 | **Demonstração ao vivo** no painel HTML (3 passos, roteiro nas notas) | Fig. 5.18, 5.10 | 98 ms; 8,2%; 66,8%; 0,72 pu |
| 15 | Trifásica: mais perto, mais severa; nominal reconverge (síntese; figura 5,82 in, tabela e nota estreitadas para 5,83 in em x = 7,12) | Fig. 5.7 (dedicada, `fig_5_7`), Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 16 | Assimétricas expõem a fragilidade estrutural (síntese) | Fig. 5.10, 5.18 (dedicadas, `fig_5_10`/`fig_5_18`) | 250×, 98 ms, 106 ms, 754 rad/s = 2,32 ωn |
| 17 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,09 pu com corrente saturada |
| 18 | Conclusões (3 cartões + contribuição) | Cap. 6 | |
| 19 | Trabalhos futuros, limites, agradecimento | Cap. 7 | |

## Demonstração (slide 14)

O HTML (`output/pll_metrics.html`, Plotly embutido, abre sem internet) é
aberto no navegador **antes** da defesa, já no cenário Barra 7 trifásica
nominal, e alternado com Alt+Tab. Roteiro com os cliques entre parênteses
nas notas do slide 14: (1) aba Inversor UFV + Zoom na falta; (2) toggle
para sintonia inadequada (o painel troca para o cenário equivalente);
(3) Barra 7 bifásica nominal, aba Espectro FFT em dq. Se o navegador
falhar, os slides 15-16 cobrem os mesmos números. Na arguição o painel
fica aberto para "e na barra X?".

## Apêndice (20-27, para perguntas; fora do tempo)

| # | Conteúdo | TCC |
|---|---|---|
| 20 | Divisor "Apêndice" (lista o que vem) | |
| 21 | Ganhos menores: compromisso, não piora uniforme (inclui monofásica B7) | Fig. 5.14, Tab. 5.3 |
| 22 | vd e vq nas trifásicas Barra 7 × Barra 6 | Fig. 5.5, 5.6 |
| 23 | Tabelas 5.1 e 5.2 completas | Tab. 5.1, 5.2 |
| 24 | Tabela 5.3 completa (assimétricas), igual à do TCC | Tab. 5.3 |
| 25 | Pós-falta: absorve P em 66,8% do tempo (Barra 7, inadequada) | Fig. 5.20, 5.21 |
| 26 | Classificação estendida de estabilidade | Cap. 2 |
| 27 | Ibéria e Chile 2025 | Cap. 2 |

A coluna "Vd mínima e máxima", sem par no TCC, saiu em 2026-10-17: o deck
só traz o que o TCC traz ([[defesa-pendencias]]).

## Estrutura visual

Visual do template "Project Portfolio" (SlidesCarnival) desde 2026-10-16,
em tons de azul: cabeçalho com linha, linha vertical com o nome da seção
(MOTIVAÇÃO 2-4, MODELAGEM 5-10, MÉTODO 11-12, RESULTADOS 13-17, CONCLUSÃO
18-19, APÊNDICE 20-27), blocos retos sem borda, laranja como único
destaque (azul = nominal, laranja = inadequada). Títulos em frase completa,
pergunta da banca no rodapé. Grade e cores em
[design.md](../../skills/tcc-pptx-editor/referencia/design.md).
