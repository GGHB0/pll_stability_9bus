---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-16 (esboço inicial, 24 slides, 16:9). Arquivo e
> pipeline: skill [tcc-pptx-editor](../../skills/tcc-pptx-editor/SKILL.md).
> Cada slide resume uma parte do TCC: a coluna "TCC" diz onde conferir
> (seções e figuras de [[tcc-docx-content-map]]). Pendências em
> [[defesa-pendencias]].

## Corpo (slides 1-16, ~31 min de roteiro a 130 ppm; limite 30)

| # | Mensagem (título) | TCC | Números a conferir |
|---|---|---|---|
| 1 | Capa: título, autores, orientadores | capa | |
| 2 | A rede troca inércia mecânica por controle dos conversores | Cap. 2 (IEA) | 600 TWh, ~70%, 5% → 17% |
| 3 | Blecautes recentes passaram pela geração inversorizada | Cap. 2, [[brasil-2023-overview]] | ~1/3 da carga, 265 GW·s; > 2,5 GW, 0,63 Hz; 11.066 MW, 73% |
| 4 | SRF-PLL depende de tensão boa, que a falta destrói + objetivos | Cap. 1 | 120 Hz |
| 5 | VSI de dois níveis, LCL, barramento CC ideal | Fig. 4.2, §4.3 | 5 kHz, 100 MW, Vcc 136,36 kV, L1/L2/Cf, Rd |
| 6 | SRF-PLL orienta as malhas dq; banda do PI é compromisso | Fig. 4.3, 3.1 | |
| 7 | Memorial: ts = 20 ms → Kp = 460, Ki = 105.820 | §4.3, [[pll-loop-filter-gains]] | ωn 325,3 rad/s (51,8 Hz), ξ 0,707 |
| 8 | Sintonia inadequada: ganhos −80% | §4.3, [[cenarios-simulados]] | Kp 92, Ki 21.164, ωn 145,5, ξ 0,316 |
| 9 | IEEE 9 barras com UFV de 100 MW na Barra 2 | Fig. 4.1 | 192 MVA original |
| 10 | Protocolo: falta 0,3-0,4 s, observação até 0,6 s | §4.3.4, Tab. 4.1 | travamento 40/79 ms; **contagem de cenários** |
| 11 | Energização: inadequada leva ~2× para travar | Fig. 5.3 | 34/40 ms × 42/79 ms |
| 12 | Trifásica: mais perto, mais severa; nominal reconverge | Fig. 5.7, Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 13 | Assimétricas expõem a fragilidade (cycle slipping) | Fig. 5.10, 5.18 | 250×, 98 ms, 754 rad/s = 2,32 ωn |
| 14 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,14 pu com corrente saturada |
| 15 | Conclusões (3 cartões + contribuição) | Cap. 6 | |
| 16 | Trabalhos futuros, limites, agradecimento | Cap. 7 | |

## Apêndice (17-24, para perguntas; fora do tempo)

| # | Conteúdo | TCC |
|---|---|---|
| 17 | Divisor "Apêndice" (lista o que vem) | |
| 18 | Ganhos menores: compromisso, não piora uniforme | Fig. 5.14, Tab. 5.3 |
| 19 | vd e vq nas trifásicas Barra 7 × Barra 6 | Fig. 5.5, 5.6 |
| 20 | Tabelas 5.1 e 5.2 completas | Tab. 5.1, 5.2 |
| 21 | Tabela 5.3 completa (assimétricas) | Tab. 5.3 |
| 22 | Pós-falta: absorve P em 66,8% do tempo (Barra 7, inadequada) | Fig. 5.20, 5.21 |
| 23 | Classificação estendida de estabilidade | Cap. 2 |
| 24 | Ibéria e Chile 2025 | Cap. 2 |

## Estrutura visual

Fundo creme, primária petróleo, um destaque laranja por slide, títulos em
frase completa, caixa "Justificativa de ouro" no rodapé da maioria dos
slides de conteúdo. Grade e cores em
[design.md](../../skills/tcc-pptx-editor/referencia/design.md).
