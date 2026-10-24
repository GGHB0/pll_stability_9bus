# Design do deck da defesa

Continuação de `SKILL.md`. Desde 2026-10-16 o deck segue o visual do
template **"Project Portfolio" (SlidesCarnival, CC BY 4.0)**, escolhido pelo
Victor entre 9 candidatos, em tons de azul. Como adotar outro template:
`casos/troca_template.md`. Slide novo ou forma nova segue isto; na dúvida,
**duplicar a forma de um slide existente** (`copy.deepcopy(sh._element)` +
`spTree.append`) em vez de desenhar com `add_shape`, que nasce com o
estilo padrão do Office.

## Página

- 16:9, **13,333 × 7,5 in**. Fundo `F6F6F6` (vem do layout).
- Layouts: `COVER` (slide 1), `CONTENT` (todos os de conteúdo), `DIVIDER`
  (abre o apêndice), `CLOSING` (não usado), `DEFAULT` (vazio, não usar).
- Os layouts `COVER`, `CONTENT` e `DIVIDER` trazem o **cabeçalho do
  template**: logo UERJ em (0,22; 0,10), "UERJ · ENGENHARIA ELÉTRICA",
  "DEFESA DE TCC · SRF-PLL" e "2026" em 12 pt, linha de 1 pt em y = 0,63.
  `CONTENT` e `DIVIDER` trazem também a **linha vertical** em x = 0,77
  (de y = 0,75 ao pé). Número do slide em (12,13; 7,00). Não redesenhar
  nada disso no slide.
- **Nome da seção** (forma "Seção", no slide, não no layout): caixa de
  texto girada 270°, 18 pt negrito, centrada em (0,40; 4,10). Seções:
  MOTIVAÇÃO 2-4, MODELAGEM 5-12, MÉTODO 13-14, RESULTADOS 15-19, CONCLUSÃO
  20-21, APÊNDICE 22-29. Slide novo: copiar a "Seção" do vizinho e trocar
  o texto, se mudar de seção.
- Capa: faixa de y 0,75 a 4,55 com três fotos de usinas (FV, eólica, FV;
  Pexels, licença livre, sem crédito obrigatório), cada uma preenchendo o
  bloco com corte central ("Foto da capa N"), divisórias brancas de 3 pt,
  linha de 1 pt em 4,55; título 26 pt negrito em (0,75; 4,78), subtítulo
  abaixo, autores e orientadores em x = 9,85. Só usina inversorizada:
  heliotérmica (espelhos + torre) e eólica antiga de indução ficam de fora.

## Grade (polegadas)

| Elemento | x | y | largura × altura |
|---|---|---|---|
| Título (frase) | 1,10 | 0,98 | 11,85 × 1,05 |
| Área de conteúdo | 1,10 | 2,20 | até 12,95 em x, até ~6,85 em y |
| Caixa de rodapé ("Pergunta da banca", "Contribuição") | 1,10 | 5,55 a 6,05 | 11,85 × 0,70 a 1,25 |

- Nada à esquerda de x = 1,05 (linha da seção em 0,77); vão entre colunas 0,20.
- **2 colunas**: 5,82 de largura em x = 1,10 e 7,12.
- **3 colunas**: 3,82 em x = 1,10 / 5,12 / 9,13.
- **4 etapas com seta**: ~2,67 de largura, seta (`rightArrow`) de
  ~0,3-0,4 no vão.
- Texto dentro de bloco: recuo de 0,22 a 0,30 da borda.
- Figura: "Moldura da figura" com a imagem 0,15 para dentro e a legenda
  numa caixa de 0,30 de altura logo abaixo da imagem, dentro da moldura.

## Cores

Tons de azul pedidos pelo Victor sobre o cinza do template; o laranja do
HTML segue como destaque (azul = nominal, laranja = inadequada, como nas
figuras). O deck mistura RGB fixo (`srgbClr`, ~1.100 lugares) e cor de
tema (`schemeClr`): trocar uma cor exige tratar os dois (ver
`casos/troca_template.md`).

| Papel | Onde | RGB |
|---|---|---|
| Texto, linhas do cabeçalho e da seção | `tx1` | `0F172A` |
| Fundo da página | layout | `F6F6F6` |
| Bloco cheio: cabeçalho de tabela, "Contribuição", "Número", "Círculo do ícone" | RGB fixo | `1E3A8A` (marinho) |
| Título de cartão, pergunta da caixa de rodapé, acentos de texto | `accent1` | `2563EB` |
| Caixa de ênfase ("Pergunta da banca", "Nota", "Síntese") | RGB fixo | `DBEAFE` |
| Destaque (laranja): número que a banca deve ver, linha "inadequada"/Barra 7 em tabela | `accent2` | `EA580C` |
| Bloco comum (cartão, moldura) | `bg1` | `FFFFFF` |
| Texto secundário, legenda de figura | `accent5` | `64748B` |
| Divisória fina (capa, tabela) | RGB fixo | `CBCBCB` / `CBD5E1` |

O laranja é o único destaque: no máximo 1 ou 2 elementos por slide.

## Fontes e tamanhos

- Tema: **Arial** (títulos e cabeçalho), **Calibri** (corpo). O template
  usa Roboto; ficou de fora para não depender de fonte instalada no
  notebook da defesa. Fonte explícita fora disso é aviso do
  `check_pptx.py`. "Aptos" aparece no PowerPoint por padrão de tabela; não
  introduzir.
- **Equações** (padrão de 2026-10-24, notação do TCC: K<sub>pPLL</sub>,
  K<sub>iPLL</sub>, ω<sub>n</sub>, v<sub>q</sub>, θ<sub>PLL</sub>; nunca "Kp<sub>PLL</sub>"):
  - *Em destaque* (linha própria): **Cambria Math 20 pt** `1E3A8A`,
    centralizada; letras em itálico, números, operadores, rótulos de
    subscrito (PLL, ref, est) e o "e" do português retos.
  - *No texto*: fonte e cor do texto em volta, sem itálico.
  - Sempre subscrito/sobrescrito de verdade (`baseline`), nunca "vq" corrido
    nem o "²" do Unicode. Número grande de cartão de destaque (slide 11)
    segue a regra do cartão, não a de equação.
- Título 28 pt negrito `tx1`. Número de cartão de destaque 36 pt negrito
  (`accent1` ou `accent2`). Título de cartão 16-18 pt negrito `accent1`.
  Corpo 14 pt. Legenda de figura 11 pt `accent5`. Nada abaixo de 11 pt.
- Tabela: cabeçalho 14 pt negrito branco sobre marinho; corpo 14 pt;
  divisórias finas; linha em destaque em `accent2` negrito.

## Caixas que se repetem (nome da forma = papel)

Todas **`rect` chapado, sem borda** (estilo do template), fundo `bg1`,
salvo indicação.

| Nome | Uso | Diferença |
|---|---|---|
| Cartão de destaque | número grande + legenda curta | borda `accent2` quando o número é laranja |
| Moldura da figura | figura + legenda "Figura X.Y do TCC" | |
| Especificação | rótulo + valor (parâmetros) | |
| Pergunta da banca | "Por que X?" em `accent1` + resposta de 1-2 linhas | fundo `DBEAFE` |
| Nota / Síntese | frase de fechamento do slide | fundo `DBEAFE` |
| Contribuição | fecho de slide em faixa cheia | fundo marinho, texto branco |
| Etapa do problema / Etapa do cálculo | cadeia causal com setas | última etapa com borda `accent1` |
| Cartão de evento / de conclusão / Trabalho futuro | colunas paralelas | |
| Frase de abertura | 2º parágrafo do título curto (slide 5) | 20 pt `1E3A8A`, termo-chave em negrito, `spcBef` 6 pt, `marL` 0,22 in; barra `rect` `2563EB` 0,07 × 0,36 in em (1,10; 1,56), sem borda nem sombra |
| Número / Círculo do ícone | `ellipse` marinho com número ou ícone branco | |

O texto fica numa caixa de texto **separada**, por cima da forma (a forma
não tem texto próprio). Quem move um cartão move os dois.
