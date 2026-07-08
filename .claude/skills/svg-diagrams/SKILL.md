---
name: svg-diagrams
description: Cria qualquer SVG do projeto (diagramas, esquemáticos, curvas de norma, banners, ilustrações para README/KB/TCC) e exporta para PNG. Ativar sempre que o usuário pedir para criar/desenhar/gerar/ajustar um SVG, PNG, diagrama, esquemático, figura, banner ou ilustração — mesmo sem mencionar o formato (ex.: "precisa de uma figura do circuito do filtro LCL", "desenha o esquemático do VSI", "cria a curva do ONS", "atualiza o banner"). Também usar para converter um SVG existente do repositório em PNG.
version: 1.1.0
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
`mcp__Claude_Preview` e extrair o PNG por `canvas.toDataURL`.

1. **Sirva a pasta do SVG** — confirme/adicione em `.claude/launch.json` um config
   `assets-static` (`python -m http.server 8744 --directory assets/diagrams`) e chame
   `mcp__Claude_Preview__preview_start` com esse nome. Se o SVG estiver em outra
   pasta (ex.: `assets/`), ajuste o `--directory` do config ou crie um config irmão.
2. **Ajuste o viewport ao viewBox exato** do SVG:
   `mcp__Claude_Preview__preview_resize` com `width`/`height` = viewBox, `colorScheme: "light"`
   (sem isso o fundo fora do SVG some com o dark mode do navegador).
3. **Navegue direto para o arquivo**: `preview_eval` com
   `window.location.href = 'http://localhost:8744/<arquivo>.svg'`.
4. **Rasterize em canvas** (não devolva o data URL inteiro — só o tamanho, senão
   estoura o limite de tokens da ferramenta):

```js
(async () => {
  const svgEl = document.documentElement;
  const xml = new XMLSerializer().serializeToString(svgEl);
  const url = URL.createObjectURL(new Blob([xml], {type: 'image/svg+xml;charset=utf-8'}));
  const img = new Image();
  const loaded = new Promise((res, rej) => { img.onload = res; img.onerror = rej; });
  img.src = url; await loaded;
  // document.createElement falha aqui: o documento de um SVG standalone não é HTML.
  const canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');
  const scale = 2; // retina
  canvas.width = <VIEWBOX_W> * scale; canvas.height = <VIEWBOX_H> * scale;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  window.__pngData = canvas.toDataURL('image/png');
  return window.__pngData.length;
})()
```

5. **Recupere o PNG**: rode `preview_eval` de novo retornando `window.__pngData`.
   Isso estoura o limite inline e é salvo automaticamente num `.txt` de
   tool-results — leia esse arquivo, remova as aspas de string JSON e o prefixo
   `data:image/png;base64,`, decodifique base64 e grave o `.png` ao lado do `.svg`:

```python
data = open(TOOL_RESULT_TXT, encoding='utf-8').read().strip()
if data.startswith('"') and data.endswith('"'):
    data = data[1:-1]
b64 = data.split('base64,', 1)[1]
open(OUT_PNG, 'wb').write(base64.b64decode(b64))
```

6. **Confira o resultado** lendo o PNG gerado com a ferramenta `Read` antes de
   considerar a figura pronta — problemas de subscrito/seta só aparecem no raster.

### Se a aba travar

`preview_screenshot` pode travar (timeout) depois de um `window.location.reload()`.
Não insista na mesma aba: `preview_stop` no server e `preview_start` de novo cria
uma aba limpa — mais rápido que depurar a trava.

## Depois de Criar a Figura

- Se o arquivo ficou em `assets/diagrams/`, adicione uma linha na tabela de
  `assets/diagrams/README.md` (arquivo, tipo, tema, fonte de conteúdo).
- Confirme que o `.svg` e este próprio `SKILL.md` continuam ≤ 200 linhas
  (`.claude/rules/limits.md`) — se crescer, quebre em elementos reutilizáveis
  (`<defs>`/`<use>`) em vez de duplicar blocos.
- Não toque no `.docx` — a inserção da figura no Word é manual pelo usuário.
