# Legibilidade em Figuras do TCC/DOCX

Referência da skill `svg-diagrams`, desmembrada do SKILL.md em 2026-10-02.
Vale para SVG desenhado à mão; figura de matplotlib tem a conta própria em
`data_charts.md`.

Quando o usuário reclamar que "a fonte fica pequena no relatório", a causa quase
sempre não é o export e sim o **tamanho da fonte relativo ao `viewBox`**. Uma figura
inserida ocupando a largura útil da página (~16 cm) é reduzida por um fator ~0,49
(para um `viewBox` de ~920 px de largura). Regra prática:

```
pt_no_docx ≈ 0,49 × font_px         (viewBox ~920 px, figura na largura da página)
```

Generalizando p/ qualquer largura de `viewBox` W (px) e largura no papel L_cm:

```
pt_no_docx ≈ font_px × L_cm × 28,35 / W        (1 cm = 28,35 pt)
```

Confere com a regra prática acima: W = 920 e L = 16 cm dão 16 × 28,35 / 920 =
**0,49 pt por px**. (A versão anterior desta linha trazia um `/ 12` a mais e
devolvia 0,041 — ~12× baixo, contradizendo a própria tabela abaixo. Corrigida
em 2026-08-23.)

Largura de inserção usual no fragmento do TCC: 5,5" = 13,97 cm; a largura útil
da página Letter com margens de 1" é 6,5" = 16,51 cm (medido no próprio DOCX em
2026-09-01; os oscilogramas entram a 5,5" e as figuras didáticas a 6,5"). Desde a
mesclagem no canônico A4, a largura útil é 6,30" = 16 cm (ver o roteiro no fim).

> Esta seção vale para **SVG desenhado à mão**, onde a escala vem do `viewBox`
> em px. Para figura de **matplotlib** a conta é outra —
> `font_pt × largura_na_pagina / largura_figsize`, com `figsize` em polegadas.
> Ver `data_charts.md`, "Validar a legibilidade no tamanho da página". O
> princípio é o mesmo: encolher o canvas, nunca aumentar a fonte.

| Fonte no SVG (W≈920) | ~pt no DOCX | Veredito |
|---|---|---|
| 9 px | ~4,4 pt | ilegível |
| 13 px | ~6,4 pt | mínimo aceitável p/ rótulos secundários |
| 15 px | ~7,4 pt | ok |
| ≥18 px | ≥8,9 pt | confortável (use p/ títulos) |

**Quando o piso não cabe, encolha o `viewBox`, não aumente a fonte.** O que
manda é a razão `font_px / W`, então re-desenhar o mesmo conteúdo num
`viewBox` mais estreito sobe o tamanho aparente sem tocar em nenhuma fonte.
Foi o que resolveu o `pll_control_loop.svg` em 2026-08-23: 920×340 → 680×350
levou os rótulos de 4,9 pt para 7,6 pt. Subir a fonte no layout largo teria
estourado as caixas — num diagrama denso, +30% de fonte é colisão garantida.

**Piso de fonte**: em figura destinada ao DOCX, nenhum texto abaixo de ~13 px
(para W≈920). Se o piso não couber sem colisão, o problema é densidade — reduza
conteúdo, divida em duas figuras, ou oriente o usuário a inserir a imagem maior
(paisagem / página inteira). Não compense com export em escala maior: escala só
melhora **nitidez**, não o tamanho aparente do texto na página.

Ao **aumentar fontes de um SVG existente**, lembre que os grupos de texto empilhados
(ex.: R/X/B de linha, kV de trafo, MW/MVAr de carga) têm espaçamento de linha fixo —
aumente o `font-size` **e** reposicione os `y` (espaçamento ≈ 1,15× a fonte) senão as
linhas colidem. Confira sempre no PNG rasterizado antes de dar por pronto.

## Roteiro: "a letra da figura está pequena" (Figura 4.2, 2026-10-03)

O TCC hoje é **A4, largura útil 6,30 in = 16 cm** (não mais Carta 6,5"): com
W = 900, dá 0,50 pt/px. O `vsi_lcl_pwm_circuit.svg` tinha 8-15 px (4-7,5 pt) e
saiu com 14-18 px (7,6-9,8 pt), sem estourar caixa:

1. **Tirar o título interno**: em figura do TCC ele repete a legenda (ABNT).
2. **Recortar o `viewBox` ao conteúdo** (`40 45 840 730`, origem deslocada):
   cada px de margem vazia cortado sobe todas as fontes de graça.
3. **Subir as fontes por classe**: rótulos de sinal 16, blocos 16-18 bold,
   notas 14; subscrito de 75% para 80%.
4. **Afastar texto de linha**: no Edge o `baseline-shift="sub"` desce o
   subscrito ~0,4 em, então o rótulo sobre uma seta horizontal precisa da
   linha de base ≥ ~10 px acima dela. Rótulo perto de borda tracejada vai com
   `text-anchor="end"` do lado de fora. Nota longa quebra em duas linhas
   (e a zona cresce para baixo), em vez de ficar com fonte menor.
5. Conferir no PNG e **na página do PDF** do finalize: o tamanho ali é o que
   o professor vê, comparado à legenda de 10 pt.

Para levar o PNG ao DOCX: `tcc-docx-editor/scripts/troca_imagem.py`.
