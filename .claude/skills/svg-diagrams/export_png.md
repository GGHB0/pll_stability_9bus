# Exportação de SVG para PNG

Referência da skill `svg-diagrams`. Vale para SVG **desenhado à mão**; gráfico
de dados reais sai direto do matplotlib (`savefig` gera SVG e PNG).

## Caminho padrão: `scripts/export_png.ps1`

```powershell
.claude\skills\svg-diagrams\scripts\export_png.ps1 assets\diagrams\figura.svg [-Scale 3] [-Out saida.png]
```

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .claude/skills/svg-diagrams/scripts/export_png.ps1 assets/diagrams/figura.svg
```

O que o script faz (para não repetir à mão):

1. Lê largura e altura do `viewBox` (origem deslocada, `0 30 820 430`,
   funciona: a janela recebe só largura × altura).
2. Copia o SVG para `C:\Temp\svgexport\`: caminho do repo com espaço ou
   acento quebra a URL `file:///`.
3. Chama o Edge do Windows em headless com `--window-size` = viewBox e
   `--force-device-scale-factor=3`. O fator multiplica a **resolução**
   (820×430 → 2460×1290), não o tamanho aparente do texto na página.
4. Grava o PNG ao lado do SVG e imprime `OK <caminho> (px, viewBox, escala)`.

Depois, **ler o PNG com `Read`**: colisão de rótulo, subscrito e ponta de
seta só aparecem no raster.

### Por que script e não linha de comando avulsa

Histórico que o script já resolve (não reintroduzir ao editar):

- Chamar o `msedge.exe` direto pelo Git Bash saiu sem erro e **sem arquivo**
  (2026-10-02).
- No PowerShell, `& msedge ...` com `ErrorActionPreference=Stop` vira erro
  porque o Edge escreve avisos inofensivos no stderr; o script usa
  `Start-Process -Wait`.
- O Edge pode devolver antes de gravar: o script espera até 5 s pelo arquivo.
- O `.ps1` está salvo em UTF-8 **com BOM**: o PowerShell 5.1 lê sem BOM como
  ANSI e estraga os acentos das mensagens.

## Alternativa: navegador do MCP (`mcp__Claude_Browser__*`)

Só se o Edge não existir na máquina. Toda chamada exige o `tabId` devolvido
pelo `preview_start`.

1. Subir o servidor **por `name`** (`{name: "assets-static"}`, porta 8744,
   config em `.claude/launch.json`). `preview_start` com `{url: ...}` não sobe
   a porta: devolve `navOk: true` com aba vazia, e o erro só aparece depois
   como `javascript_tool failed: Event`. Diagnóstico:
   `document.documentElement.tagName` tem que dar `svg`.
2. `resize_window` com o tamanho do viewBox e `colorScheme: "light"`.
3. Rasterizar num canvas e guardar em `window`, devolvendo só o tamanho:

```js
(async () => {
  const xml = new XMLSerializer().serializeToString(document.documentElement);
  const url = URL.createObjectURL(new Blob([xml], {type: 'image/svg+xml;charset=utf-8'}));
  const img = new Image();
  await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = url; });
  const canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');
  const scale = 3;
  canvas.width = <VIEWBOX_W> * scale; canvas.height = <VIEWBOX_H> * scale;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  window.__pngData = canvas.toDataURL('image/png');
  return window.__pngData.length;
})()
```

4. Em outra chamada, devolver `window.__pngData` (reload zera o `window`). O
   retorno estoura o limite e vai para um `.txt` de tool-results em JSON
   `[{type, text}]`:

```python
import json, base64
d = json.load(open(TOOL_RESULT_TXT, encoding='utf-8'))
open(OUT_PNG, 'wb').write(base64.b64decode(d[0]['text'].split('base64,', 1)[1]))
```

Aba travada: `preview_stop` + `preview_start` de novo; não insistir em
screenshot.
