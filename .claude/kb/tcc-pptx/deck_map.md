---
name: defesa-deck-map
description: Mapa slide a slide do deck da defesa (Defesa_TCC_SRF-PLL.pptx) — mensagem, seção e figuras do TCC de onde vem, números que precisam bater
aliases: [defesa-deck-map]
---

# Deck da defesa — mapa slide a slide

> Estado em 2026-10-16 (noite): 25 slides, 16:9, reestruturado para a
> **demonstração ao vivo do painel HTML** (slide 12) e com a paleta do
> dashboard; entrega pendente. Arquivo e
> pipeline: skill [tcc-pptx-editor](../../skills/tcc-pptx-editor/SKILL.md).
> Cada slide resume uma parte do TCC: a coluna "TCC" diz onde conferir
> (seções e figuras de [[tcc-docx-content-map]]). Pendências em
> [[defesa-pendencias]].

## Corpo (slides 1-17, 25,2 min de roteiro a 130 ppm + ~1,5 min de cliques na demo; limite 30)

| # | Mensagem (título) | TCC | Números a conferir |
|---|---|---|---|
| 1 | Capa: título, autores, orientadores | capa | |
| 2 | A rede troca inércia mecânica por controle dos conversores | Cap. 2 (IEA) | 600 TWh, ~70%, 5% → 17% |
| 3 | Blecautes recentes passaram pela geração inversorizada | Cap. 2, [[brasil-2023-overview]] | ~1/3 da carga, 265 GW·s; > 2,5 GW, 0,63 Hz; 11.066 MW, 73% |
| 4 | SRF-PLL depende de tensão boa, que a falta destrói + objetivos | Cap. 1 | 120 Hz |
| 5 | VSI de dois níveis, LCL, barramento CC ideal | Fig. 4.2, §4.3 | 5 kHz, 100 MW, Vcc 136,36 kV, L1/L2/Cf, Rd |
| 6 | SRF-PLL orienta as malhas dq; banda do PI é compromisso | Fig. 4.3, 3.1 | |
| 7 | ts = 20 ms → Kp 460, Ki 105.820; inadequada −80% (tabela das duas sintonias) | §4.3, [[pll-loop-filter-gains]], [[cenarios-simulados]] | ωn 325,3/145,5; ξ 0,707/0,316; Kp 92, Ki 21.164 |
| 8 | IEEE 9 barras com UFV de 100 MW na Barra 2 | Fig. 4.1 | 192 MVA original |
| 9 | Protocolo: falta 0,3-0,4 s, observação até 0,6 s | §4.3.4, Tab. 4.1 | travamento 40/79 ms; 29 cenários (21 + 8) |
| 10 | Pipeline simulação → Python → métricas → painel HTML | [[pipeline-dados]] | retenção 0,091/0,989 = 9,2% (notas) |
| 11 | Energização: inadequada leva ~2× para travar | Fig. 5.3 | 34/40 ms × 42/79 ms |
| 12 | **Demonstração ao vivo** no painel HTML (3 passos, roteiro nas notas) | Fig. 5.18, 5.10 | 98 ms; 8,2%; 66,8%; 0,72 pu |
| 13 | Trifásica: mais perto, mais severa; nominal reconverge (síntese) | Fig. 5.7, Tab. 5.1 | retenção 9,2-58,4%, pico 7,3-37,3°, retorno 76-112 ms |
| 14 | Assimétricas expõem a fragilidade (síntese) | Fig. 5.10, 5.18 | 250×, 98 ms, 106 ms, 754 rad/s = 2,32 ωn |
| 15 | ONS Submódulo 2.10 exige mais que ficar conectado | Fig. 2.2, Tab. 5.2 | Q 0,09 pu com corrente saturada |
| 16 | Conclusões (3 cartões + contribuição) | Cap. 6 | |
| 17 | Trabalhos futuros, limites, agradecimento | Cap. 7 | |

## Demonstração (slide 12)

O HTML (`output/pll_metrics.html`, Plotly embutido, abre sem internet) é
aberto no navegador **antes** da defesa, já no cenário Barra 7 trifásica
nominal, e alternado com Alt+Tab. Roteiro com os cliques entre parênteses
nas notas do slide 12: (1) aba Inversor UFV + Zoom na falta; (2) toggle
para sintonia inadequada (o painel troca para o cenário equivalente);
(3) Barra 7 bifásica nominal, aba Espectro FFT em dq. Se o navegador
falhar, os slides 13-14 cobrem os mesmos números. Na arguição o painel
fica aberto para "e na barra X?".

## Apêndice (18-25, para perguntas; fora do tempo)

| # | Conteúdo | TCC |
|---|---|---|
| 18 | Divisor "Apêndice" (lista o que vem) | |
| 19 | Ganhos menores: compromisso, não piora uniforme (inclui monofásica B7) | Fig. 5.14, Tab. 5.3 |
| 20 | vd e vq nas trifásicas Barra 7 × Barra 6 | Fig. 5.5, 5.6 |
| 21 | Tabelas 5.1 e 5.2 completas | Tab. 5.1, 5.2 |
| 22 | Tabela 5.3 completa (assimétricas) + coluna Vd mín./máx.* | Tab. 5.3 |
| 23 | Pós-falta: absorve P em 66,8% do tempo (Barra 7, inadequada) | Fig. 5.20, 5.21 |
| 24 | Classificação estendida de estabilidade | Cap. 2 |
| 25 | Ibéria e Chile 2025 | Cap. 2 |

\* Coluna sem par no TCC: `vd_rede_pu` mínimo e máximo na falta, de 0,3 s +
1 ciclo (1/60 s) a 0,4 s, lido por `le_sim_data`; reproduz as linhas do
esboço. Monofásica B7 inadequada: 0,03 a 1,39.

## Estrutura visual

Visual do template "Project Portfolio" (SlidesCarnival) desde 2026-10-16,
em tons de azul: cabeçalho com linha, linha vertical com o nome da seção
(MOTIVAÇÃO 2-4, MODELAGEM 5-8, MÉTODO 9-10, RESULTADOS 11-15, CONCLUSÃO
16-17, APÊNDICE 18-25), blocos retos sem borda, laranja como único
destaque (azul = nominal, laranja = inadequada). Títulos em frase completa,
pergunta da banca no rodapé. Grade e cores em
[design.md](../../skills/tcc-pptx-editor/referencia/design.md).
