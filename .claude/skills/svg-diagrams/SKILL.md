---
name: svg-diagrams
description: Cria qualquer SVG do projeto (diagramas, esquemáticos, curvas de norma, banners, ilustrações para README/KB/TCC) e exporta para PNG. Ativar sempre que o usuário pedir para criar/desenhar/gerar/ajustar um SVG, PNG, diagrama, esquemático, figura, banner ou ilustração — mesmo sem mencionar o formato (ex.: "precisa de uma figura do circuito do filtro LCL", "desenha o esquemático do VSI", "cria a curva do ONS", "atualiza o banner"). Também usar para converter um SVG existente do repositório em PNG.
version: 1.3.0
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

Generalizando p/ qualquer largura de `viewBox` W e largura no papel L_cm:
`pt_no_docx ≈ font_px × (L_cm / W) × 28,35 / 12` ≈ `font_px × L_cm / W × 2,36`.

| Fonte no SVG (W≈920) | ~pt no DOCX | Veredito |
|---|---|---|
| 9 px | ~4,4 pt | ilegível |
| 13 px | ~6,4 pt | mínimo aceitável p/ rótulos secundários |
| 15 px | ~7,4 pt | ok |
| ≥18 px | ≥8,9 pt | confortável (use p/ títulos) |

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

## Armadilha 2 — Setas que não "entram" no destino

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

Não há rasterizador de SVG por CLI neste ambiente (sem inkscape, rsvg-convert,
cairosvg ou imagemagick). O caminho que funciona é renderizar no Chrome via
`mcp__Claude_Browser__*` e extrair o PNG por `canvas.toDataURL`.

> **Namespace atual**: `mcp__Claude_Browser__*` — o antigo `mcp__Claude_Preview__*`
> não existe mais. **Toda** chamada exige `tabId`: capture o `tabId` devolvido pelo
> `preview_start` e repasse em `resize_window`, `javascript_tool` e `computer`.
>
> **Custo**: desenhar e decidir o layout é trabalho de modelo premium; o loop
> mecânico abaixo (rodar o gerador, rasterizar, conferir, reajustar) é simples e
> pode rodar em modelo mais barato.

1. **Abra o SVG numa aba** — mais robusto que subir server por `name`:
   `mcp__Claude_Browser__preview_start` com
   `{url: "http://localhost:8744/<arquivo>.svg"}`. Funciona mesmo se a porta 8744 já
   estiver tomada por outro chat (o config `assets-static` do `.claude/launch.json`
   serve `assets/diagrams`; para `assets/` ajuste o `--directory`). Guarde o `tabId`.
2. **Ajuste o viewport ao viewBox exato**: `mcp__Claude_Browser__resize_window` com
   `tabId`, `width`/`height` = viewBox e `colorScheme: "light"` (sem isso o fundo fora
   do SVG some no dark mode do navegador).
3. **Rasterize em canvas** via `mcp__Claude_Browser__javascript_tool`
   (`action: "javascript_exec"`, `tabId`) — devolva só o tamanho, senão estoura o
   limite de tokens:

```js
(async () => {
  const xml = new XMLSerializer().serializeToString(document.documentElement);
  const url = URL.createObjectURL(new Blob([xml], {type: 'image/svg+xml;charset=utf-8'}));
  const img = new Image();
  await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = url; });
  // document.createElement falha aqui: o documento de um SVG standalone não é HTML.
  const canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');
  const scale = 3; // 3× p/ nitidez em impressão/DOCX (2× ainda serve p/ tela)
  canvas.width = <VIEWBOX_W> * scale; canvas.height = <VIEWBOX_H> * scale;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  window.__pngData = canvas.toDataURL('image/png');
  return window.__pngData.length;
})()
```

4. **Recupere o PNG** com outra chamada `javascript_tool` retornando `window.__pngData`.
   ⚠️ **`window` é zerado por reload/navegação** — nunca rasterize e recupere através de
   um `window.location.reload()`. Ao regenerar o SVG a ordem é: reload → (chamada nova)
   rasterizar → (chamada nova) recuperar. O retorno estoura o limite e é salvo num
   `.txt` de tool-results, no formato **JSON array `[{type, text}]`** (não string crua):

```python
import json, base64
d = json.load(open(TOOL_RESULT_TXT, encoding='utf-8'))
b64 = d[0]['text'].split('base64,', 1)[1]
open(OUT_PNG, 'wb').write(base64.b64decode(b64))
```

5. **Confira o resultado** lendo o PNG com `Read` antes de considerar pronto —
   subscrito/seta/contraste só aparecem no raster.

### Se a aba travar

`mcp__Claude_Browser__computer {action:"screenshot"}` pode dar timeout (30s), às vezes
logo após um reload. Não insista: o caminho de canvas acima **não precisa de
screenshot**. Se a aba travar de fato, `preview_stop` no `serverId` + `preview_start`
de novo cria aba limpa — mais rápido que depurar a trava.

## Depois de Criar a Figura

- Se o arquivo ficou em `assets/diagrams/`, adicione uma linha na tabela de
  `assets/diagrams/README.md` (arquivo, tipo, tema, fonte de conteúdo).
- Confirme que o `.svg` e este próprio `SKILL.md` continuam ≤ 200 linhas
  (`.claude/rules/limits.md`) — se crescer, quebre em elementos reutilizáveis
  (`<defs>`/`<use>`) em vez de duplicar blocos.
- Não toque no `.docx` — a inserção da figura no Word é manual pelo usuário.
