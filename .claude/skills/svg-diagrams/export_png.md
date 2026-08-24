# Exportação de SVG para PNG

Referência da skill `svg-diagrams`, desmembrada em 2026-08-23 pelo limite de
200 linhas. Vale para SVG **desenhado à mão**; gráfico de dados reais sai
direto do matplotlib (`savefig` gera SVG e PNG), sem passar por aqui.

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

1. **Suba o servidor por `name`, não por `url`.** `preview_start` com
   `{name: "assets-static"}` (config do `.claude/launch.json`, serve
   `assets/diagrams` na porta 8744; para `assets/` ajuste o `--directory`).
   Guarde o `tabId` que ele devolve. Depois `navigate` para
   `http://localhost:8744/<arquivo>.svg`.

   > ⚠️ **`preview_start` com `{url: ...}` NÃO sobe o servidor** — só abre uma
   > aba apontando para lá. Se ninguém subiu a porta 8744, ele ainda devolve
   > `navOk: true` e um `tabId`, mas a aba fica vazia. O sintoma aparece só
   > depois, na rasterização, como `javascript_tool failed: Event` (é o
   > `img.onerror` do snippet). Diagnóstico em uma linha:
   > `document.documentElement.tagName` — se vier `HTML` em vez de `svg`, a
   > página não é o SVG. Corrigido em 2026-08-23, quando a versão antiga desta
   > instrução (que mandava usar `url`) custou duas rodadas.
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
