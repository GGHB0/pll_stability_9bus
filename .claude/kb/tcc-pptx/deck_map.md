---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-18: 26 slides, 16:9, com a **demonstração ao vivo do
> painel HTML** (slide 13), alinhado ao TCC entregue (VFinal, 15/10): só o
> que está no TCC, salvo a exceção de método do bloco MODELAGEM (slides 7
> e 9, ver [[defesa-pendencias]]). Arquivo e
> pipeline: skill [tcc-pptx-editor](../../skills/tcc-pptx-editor/SKILL.md).
> Cada slide resume uma parte do TCC: a coluna "TCC" diz onde conferir
> (seções e figuras de [[tcc-docx-content-map]]). Pendências em
> [[defesa-pendencias]].

## Corpo (slides 1-18, 24,9 min de roteiro a 130 ppm + ~1,5 min de cliques na demo; limite 30)

| # | Mensagem (título) | TCC | Números a conferir |
|---|---|---|---|
| 1 | Capa: título, autores, orientadores | capa | |
| 2 | A rede troca inércia mecânica por controle dos conversores | Cap. 2 (IEA) | 600 TWh, ~70%, 5% → 17% |
| 3 | Blecautes recentes passaram pela geração inversorizada | Cap. 2, [[brasil-2023-overview]] | 23.368 MW (§2.4.3), 265 GW·s; > 2,5 GW por sobretensão, 0,63 Hz antes do colapso; 11.066 MW, 73% |
| 4 | SRF-PLL depende de tensão boa, que a falta destrói + objetivos (redação do TCC) | Cap. 1 | 120 Hz |
| 5 | No referencial dq, travar o PLL é zerar vq (3 cartões: grandezas contínuas, vq = erro de fase, P/Q desacoplados) | Fig. 4.3, §3.1, §3.1.3, §3.4 | |
| 6 | A rede vista da Barra 2 se reduz a um equivalente de Thévenin | Fig. 4.1, §4.3.1 | 192 MVA original, 100 MW; sem R_th/L_th na tela |
| 7 | **Novo (exceção de método)**: o primeiro teste pôs o SRF-PLL entre duas fontes ideais | [[psim-modeling]] (fora do TCC) | figura `assets/diagrams/pll_bancada_duas_fontes.svg`; nenhum número |
| 8 | Na bancada, ts = 20 ms levou a Kp 460, Ki 105.820; inadequada −80% (tabela das duas sintonias) | §4.3, [[pll-loop-filter-gains]], [[cenarios-simulados]] | ωn 325,3/145,5; ξ 0,707/0,316; Kp 92, Ki 21.164 |
| 9 | O inversor foi montado em etapas: PWM, filtro LCL e escala para 100 MW (sequência = exceção de método) | Fig. 4.2, §4.3.2 | 5 kHz, 100 MW, CC constante, Lest 30,71 mH, ωres, ξ |
| 10 | Protocolo: falta 0,3-0,4 s, observação até 0,6 s | §4.3.4, Tab. 4.1 | erro de fase em 2° em 40/79 ms; sem contagem de cenários |
| 11 | Pipeline simulação → Python → métricas → painel HTML | [[pipeline-dados]] | retenção 9,2% (definição do TCC) |
| 12 | Energização: inadequada leva ~2× para travar | Fig. 5.3 | 34/40 ms × 42/79 ms |
| 13 | **Demonstração ao vivo** no painel HTML (3 passos, roteiro nas notas) | Fig. 5.18, 5.10 | 98 ms; 8,2%; 66,8%; 0,72 pu |
| 14 | Trifásica: mais perto, mais severa; nominal reconverge (síntese) | Fig. 5.7, Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 15 | Assimétricas expõem a fragilidade estrutural (síntese) | Fig. 5.10, 5.18 | 250×, 98 ms, 106 ms, 754 rad/s = 2,32 ωn |
| 16 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,09 pu com corrente saturada |
| 17 | Conclusões (3 cartões + contribuição) | Cap. 6 | |
| 18 | Trabalhos futuros, limites, agradecimento | Cap. 7 | |

## Demonstração (slide 13)

O HTML (`output/pll_metrics.html`, Plotly embutido, abre sem internet) é
aberto no navegador **antes** da defesa, já no cenário Barra 7 trifásica
nominal, e alternado com Alt+Tab. Roteiro com os cliques entre parênteses
nas notas do slide 13: (1) aba Inversor UFV + Zoom na falta; (2) toggle
para sintonia inadequada (o painel troca para o cenário equivalente);
(3) Barra 7 bifásica nominal, aba Espectro FFT em dq. Se o navegador
falhar, os slides 14-15 cobrem os mesmos números. Na arguição o painel
fica aberto para "e na barra X?".

## Apêndice (19-26, para perguntas; fora do tempo)

| # | Conteúdo | TCC |
|---|---|---|
| 19 | Divisor "Apêndice" (lista o que vem) | |
| 20 | Ganhos menores: compromisso, não piora uniforme (inclui monofásica B7) | Fig. 5.14, Tab. 5.3 |
| 21 | vd e vq nas trifásicas Barra 7 × Barra 6 | Fig. 5.5, 5.6 |
| 22 | Tabelas 5.1 e 5.2 completas | Tab. 5.1, 5.2 |
| 23 | Tabela 5.3 completa (assimétricas), igual à do TCC | Tab. 5.3 |
| 24 | Pós-falta: absorve P em 66,8% do tempo (Barra 7, inadequada) | Fig. 5.20, 5.21 |
| 25 | Classificação estendida de estabilidade | Cap. 2 |
| 26 | Ibéria e Chile 2025 | Cap. 2 |

A coluna "Vd mínima e máxima", sem par no TCC, saiu em 2026-10-17: o deck
só traz o que o TCC traz ([[defesa-pendencias]]).

## Estrutura visual

Visual do template "Project Portfolio" (SlidesCarnival) desde 2026-10-16,
em tons de azul: cabeçalho com linha, linha vertical com o nome da seção
(MOTIVAÇÃO 2-4, MODELAGEM 5-9, MÉTODO 10-11, RESULTADOS 12-16, CONCLUSÃO
17-18, APÊNDICE 19-26), blocos retos sem borda, laranja como único
destaque (azul = nominal, laranja = inadequada). Títulos em frase completa,
pergunta da banca no rodapé. Grade e cores em
[design.md](../../skills/tcc-pptx-editor/referencia/design.md).
