# Design do deck da defesa

Continuação de `SKILL.md`. Levantado do XML do deck em 2026-10-16 (24
slides). Slide novo ou forma nova segue isto; na dúvida, **duplicar a forma
de um slide existente** (`copy.deepcopy(sh._element)` + `spTree.append`) em
vez de desenhar com `add_shape`, que nasce com o estilo padrão do Office.

## Página

- 16:9, **13,333 × 7,5 in**. Fundo creme `FBF7F0` (vem do layout).
- Layouts: `COVER` (slide 1), `CONTENT` (todos os de conteúdo), `DIVIDER`
  (abre o apêndice), `CLOSING` (não usado), `DEFAULT` (vazio, não usar).
- O layout `CONTENT` já traz logo UERJ + "UERJ, Engenharia Elétrica" no
  canto superior esquerdo, "Defesa de TCC 2026" no direito e o número do
  slide em (12,13; 7,00). Não redesenhar isso no slide.

## Grade (polegadas)

| Elemento | x | y | largura × altura |
|---|---|---|---|
| Título (frase) | 0,60 | 0,98 | 12,13 × 1,05 |
| Área de conteúdo | 0,60 | 2,20 | até 12,73 em x, até ~6,85 em y |
| Caixa de rodapé ("Pergunta da banca", "Contribuição") | 0,60 | 5,55 a 6,05 | 12,13 × 0,70 a 1,25 |

- Margem lateral 0,60; vão entre colunas 0,20.
- **2 colunas**: 5,96 de largura em x = 0,60 e 6,76.
- **3 colunas**: 3,91 em x = 0,60 / 4,71 / 8,82.
- **4 etapas com seta**: 2,55 a 2,73 de largura, seta (`rightArrow`) de
  ~0,3-0,4 no vão.
- Texto dentro de cartão: recuo de 0,22 a 0,30 da borda do cartão.
- Figura: "Moldura da figura" com a imagem 0,15 para dentro e a legenda
  numa caixa de 0,30 de altura logo abaixo da imagem, dentro da moldura.

## Cores (tema; usar `schemeClr`, não RGB solto)

| Papel | Tema | RGB |
|---|---|---|
| Texto | `tx1` / dk1 | `1E1E1E` |
| Primária (petróleo): título de cartão, cabeçalho de tabela, pergunta da caixa de rodapé | `accent1` / dk2 | `1B6B7F` |
| Destaque (laranja): número que a banca deve ver, linha "inadequada"/Barra 7 em tabela | `accent2` | `EA580C` |
| Azul (raro, gráfico) | `accent3` | `2563EB` |
| Borda de cartão (bege) | `accent4` | `D8D2C4` |
| Texto secundário, legenda de figura | `accent5` | `5B6B73` |
| Fundo de caixa de ênfase ("Pergunta da banca", "Nota", "Síntese") | `accent6` | `E3F0F2` |
| Fundo de cartão | `bg1` | `FFFFFF` |

O laranja é o único destaque: no máximo 1 ou 2 elementos por slide.

## Fontes e tamanhos

- Tema: **Arial** (títulos), **Calibri** (corpo). Fonte explícita fora disso
  é aviso do `check_pptx.py`. "Aptos" aparece no PowerPoint por padrão de
  tabela; não introduzir.
- Título 28 pt negrito `tx1`. Número de cartão de destaque 36 pt negrito
  (`accent1` ou `accent2`). Título de cartão 16-18 pt negrito `accent1`.
  Corpo 14 pt. Legenda de figura 11 pt `accent5`. Nada abaixo de 11 pt.
- Tabela: cabeçalho 14 pt negrito branco sobre `accent1`; corpo 14 pt;
  borda bege; linha em destaque em `accent2` negrito.

## Caixas que se repetem (nome da forma = papel)

Todas `roundRect`, fundo `bg1` e borda `accent4`, salvo indicação.

| Nome | Uso | Diferença |
|---|---|---|
| Cartão de destaque | número grande + legenda curta | borda `accent2` quando o número é laranja |
| Moldura da figura | figura + legenda "Figura X.Y do TCC" | |
| Especificação | rótulo + valor (parâmetros) | |
| Pergunta da banca | "Por que X?" em `accent1` + resposta de 1-2 linhas (sem rótulo antes desde 2026-10-16) | fundo `accent6`, borda `accent1` |
| Nota / Síntese / Contribuição | frase de fechamento do slide | fundo `accent6` (Contribuição: fundo `accent1`, texto branco) |
| Etapa do problema / Etapa do cálculo | cadeia causal com setas | última etapa com borda `accent1` |
| Cartão de evento / de conclusão / Trabalho futuro | colunas paralelas | |
| Número / Círculo do ícone | `ellipse` `accent1` com número ou ícone branco | |

O texto fica numa caixa de texto **separada**, por cima da forma (a forma
não tem texto próprio). Quem move um cartão move os dois.
