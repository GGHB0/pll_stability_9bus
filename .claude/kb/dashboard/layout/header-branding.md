---
name: header-branding
description: Logo UERJ embutido no header do dashboard HTML (base64) + fix do label invertido do toggle de mapa
---

# Branding do Header e Toggle do Mapa

## Logo UERJ (`renderer.py`)

Adicionado em 2026-07 a pedido do usuário ("colocar esse logo da UERJ no canto
superior esquerdo"). Segue o mesmo padrão de auto-contenção já usado pelo SVG
do diagrama unifilar (`_svg_section_html`): embutir como base64 para o HTML
continuar sendo um artefato único e portátil.

```python
def _uerj_logo_html(self) -> str:
    from ..config import PROJ_ROOT
    import base64
    logo_path = PROJ_ROOT / "assets" / "uerj.png"
    try:
        b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except FileNotFoundError:
        return ""
    return f'<img class="h-uerj-logo" src="data:image/png;base64,{b64}" alt="UERJ">'
```

Arquivo fonte: `assets/uerj.png` (16.643 bytes, salvo manualmente pelo usuário
— não em `assets/logos/`). Chamado em `_build_html` junto com `select_html`/
`pll_toggle_html` e injetado como primeiro elemento de `.h-left`:

```html
<div class="h-left">
  {uerj_logo_html}
  <div>
    <div class="h-title">...
```

> O quadrado roxo `.h-logo` (φ) que existia ao lado foi **removido** em
> 2026-07 a pedido do usuário — o logo da UERJ passou a ser a única marca
> visual do header (HTML e bloco CSS `.h-logo` apagados do `renderer.py`).

CSS: `.h-uerj-logo { height: 36px; width: auto; flex-shrink: 0 }`.

Se `assets/uerj.png` não existir, `_uerj_logo_html` retorna string vazia —
degrada silenciosamente sem quebrar o header (mesmo tratamento de ausência já
usado para o SVG do diagrama).

## Fix: label do toggle de mapa invertida

Reportado em 2026-07: "Ocultar mapa aparece quando o mapa já está oculto".
`toggleDiagram()` tinha os ramos do ternário trocados — mostrava "Ocultar
mapa" quando `hidden === true` (mapa já oculto) e vice-versa.

```javascript
// antes (bug): hidden ? "🗺 Mapa IEEE 9-bus" : "🗺 Ocultar mapa"
// depois (correto):
btn.innerHTML = hidden ? "🗺&nbsp;Ocultar mapa" : "🗺&nbsp;Mapa IEEE 9-bus";
```

`hidden` reflete o estado **antes** do clique atual ser processado — ou seja,
quando `hidden === true` o clique acabou de reexibir o mapa, então o botão
deve oferecer a ação oposta ("Ocultar mapa"). Vale o mesmo raciocínio para
qualquer outro toggle símile no dashboard (`table-toggle`, `pll-btn`): o label
do botão sempre descreve a **próxima ação disponível**, nunca o estado atual.
