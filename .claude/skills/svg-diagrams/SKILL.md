---
name: svg-diagrams
description: Cria qualquer SVG do projeto (diagramas, esquemáticos, curvas de norma, banners, ilustrações para README/KB/TCC) e exporta para PNG. Ativar sempre que o usuário pedir para criar/desenhar/gerar/ajustar um SVG, PNG, diagrama, esquemático, figura, banner ou ilustração — mesmo sem mencionar o formato (ex.: "precisa de uma figura do circuito do filtro LCL", "desenha o esquemático do VSI", "cria a curva do ONS", "atualiza o banner"). Também cobre gráficos com dados reais de simulação (waveforms, séries temporais do dashboard) para o TCC — ver seção "Gráficos de Dados Reais". Também usar para converter um SVG existente do repositório em PNG.
version: 1.5.0
---

# SVG Diagrams — Skill de Criação de Figuras e Exportação PNG

Cria SVGs no padrão visual do projeto e exporta o PNG correspondente. Vale para
qualquer arte vetorial do repositório: figuras do TCC (inseridas manualmente pelo
usuário no `TCC_Victor_Bruno_V9.docx` — esta skill **não edita o docx**, ver
`tcc-docx-editor`), diagramas do README, ilustrações da KB e banner.

Destino padrão: `assets/diagrams/` para diagramas técnicos; `assets/` para artes
gerais (banner etc.). Na dúvida sobre o destino, pergunte.

Antes de desenhar, olhe 1-2 SVGs existentes em `assets/diagrams/` (ex.:
`pll_system_circuit.svg`, `vsi_grid_schematic.svg`) para absorver o estilo real,
não só a tabela abaixo.

## Gráficos de Dados Reais (não desenhados à mão)

Para gráfico plotando **dados reais de simulação** (correntes/tensões abc,
dq, P/Q, séries temporais de `output/results/*/sim_data*.csv`) — não desenhar
o SVG à mão. Usar **matplotlib** direto do CSV (`svg.fonttype: "none"` p/
manter texto editável), com a paleta de `src/config/settings.py`
(`LIGHT_COLORS`) e as convenções de série do dashboard (`src/pipeline/chart.py`:
medido sólido + ref tracejado; Rede sólido + Inversor pontilhado). `savefig`
gera SVG **e** PNG direto — dispensa o workflow de rasterização via browser
abaixo, que é só para SVG desenhado à mão.

Destino: `assets/charts/` (não `assets/diagrams/`), um SVG por gráfico
(não empacotar vários painéis numa figura só, a menos que pedido). Script
gerador versionado em `scripts/gen_<nome>.py`, reproduzível a cada
re-simulação. Ver `assets/charts/README.md` e `scripts/gen_regime_waveforms.py`
como referência de estilo (legenda com fundo branco fora das curvas,
`T_SETTLE` sombreado, título com `pad` quando a legenda fica acima do eixo).

## Figura Desenhada à Mão, Conteúdo Lido do Disco

Caso intermediário entre os dois acima: o **layout** é desenhado (uma matriz,
um quadro-síntese, um inventário), mas o **conteúdo** vem do repositório e
muda a cada re-simulação. Aí não se escreve o SVG à mão nem se usa matplotlib:
escreve-se um gerador que lê a fonte e emite o SVG.

Referência: `scripts/gen_matriz_cenarios.py`, que varre `output/results/` e
gera `assets/diagrams/matriz_cenarios.svg` (a Figura 4.4 do TCC). Ganho real:
a figura não pode divergir do que foi simulado, e a contagem impressa no
rodapé é contada, não digitada — foi assim que se descobriu que a KB dizia 32
cenários onde havia 30.

Vale a pena quando o conteúdo é volátil ou quando errar o número tem custo.
Para um diagrama conceitual estável (circuito, laço de controle), continua
sendo SVG escrito à mão.

## Convenção Visual

| Elemento | Cor | Uso |
|---|---|---|
| Traços de circuito, texto principal | `#0B132B` (navy) | linhas, caixas neutras, títulos |
| Destaque / controle digital | `#F97316` (laranja) | blocos de controle, setas de comando |
| Fonte CC / grandezas "boas" | `#166534` (verde) | fonte primária, indicadores positivos |
| Conversor / VSI | `#1d4ed8` (azul forte), fundo `#dbeafe` | bloco do inversor |
| Filtro / elemento passivo | `#b45309` (âmbar), fundo `#fef3c7` | filtro LCL, elementos de acoplamento |
| Sensoriamento / medição | `#1971c2` (azul) | sondas de tensão/corrente, realimentação |
| Contingência (sag simétrico/assimétrico) | `#c92a2a` (vermelho) | ver `README.md` da pasta para o restante da paleta de faltas |

Regras fixas:
- `viewBox` proporcional ao conteúdo (não fixar `width`/`height` no elemento raiz — deixe o
  viewport de exportação controlar a escala real).
- Fundo branco explícito: `<rect width="..." height="..." fill="#ffffff"/>` como primeiro filho.
- Fonte: `font-family="ui-sans-serif, system-ui, -apple-system, sans-serif"`.
- Texto em português com acentos é permitido no SVG (diferente dos `.mmd`, que devem ficar sem acento).

## Legibilidade em Figuras do TCC/DOCX

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
da página Letter com margens de 1" é 6,5" = 16,51 cm.

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

## Armadilha 1 — Subscritos

**Nunca** use underscore literal (`V_dc`, `u_abc`) como substituto de subscrito — isso
renderiza como texto cru, não como notação de engenharia. Sempre use `<tspan>`:

```xml
<text font-style="italic">V<tspan baseline-shift="sub" font-size="75%">dc</tspan></text>
<text font-style="italic">u<tspan baseline-shift="sub" font-size="75%">abc</tspan>(PAC)</text>
```

## Armadilha 2 — Acento circunflexo de estimativa (`ω̂`, `φ̂`)

O chapéu de "valor estimado" é um **diacrítico combinante** (U+0302). O
navegador não o centraliza sobre a letra: ele sai deslocado para a direita e
lido como erro de digitação. Não use em figura que vá para o TCC.

Troque pela notação com subscrito, que ainda diz "estimado pelo PLL" e casa
com as outras figuras:

```xml
<text font-style="italic">θ<tspan baseline-shift="sub" font-size="75%">PLL</tspan>(t)</text>
```

Regra geral: **símbolo tem que bater entre figuras do mesmo capítulo.** Se o
esquemático do circuito rotula a saída do PLL como `θ_PLL`, o diagrama de
blocos que detalha esse mesmo PLL não pode chamá-la de `φ̂`.

## Armadilha 3 — Setas que não "entram" no destino

As setas usam marcador com `orient="auto-start-reverse"`, que orienta a ponta pela
direção do **último segmento do path**. Isso significa que o segmento final precisa
apontar de frente para dentro da caixa de destino — se ele for tangente à borda
(ex.: sobe rente à lateral de uma caixa em vez de entrar nela), a seta parece
"deslizar" pela borda em vez de apontar para dentro. Ao rotear um path em L/Z até um
bloco, garanta que o **último trecho** cruze a borda do bloco de frente.

Defina um marcador por cor usada (a ponta da seta deve casar com a cor da linha):

```xml
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#0B132B"/>
</marker>
```

## Workflow de Exportação para PNG

Não há rasterizador de SVG por CLI neste ambiente (sem inkscape,
rsvg-convert, cairosvg ou imagemagick). O caminho que funciona é renderizar
no Chrome via `mcp__Claude_Browser__*` e extrair o PNG por `canvas.toDataURL`.
Passo a passo, armadilhas e o snippet de rasterização em `export_png.md`.

## Depois de Criar a Figura

- Se o arquivo ficou em `assets/diagrams/`, adicione uma linha na tabela de
  `assets/diagrams/README.md` (arquivo, tipo, tema, fonte de conteúdo).
- Confirme que o `.svg` e este próprio `SKILL.md` continuam ≤ 200 linhas
  (`.claude/rules/limits.md`) — se crescer, quebre em elementos reutilizáveis
  (`<defs>`/`<use>`) em vez de duplicar blocos.
- Não toque no `.docx` — a inserção da figura no Word é manual pelo usuário.
