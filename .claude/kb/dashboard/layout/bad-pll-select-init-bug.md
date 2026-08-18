---
name: bad-pll-select-init-bug
description: Bug corrigido — filtro do select de cenário não era aplicado na carga inicial do HTML (mostrava casos _bad_pll com toggle em Nominal)
---

# Bug: filtro do `<select>` não aplicado na carga inicial

Ver design geral do toggle em [[bad-pll-dashboard-filter]].

## Sintoma

Ao abrir o HTML pela primeira vez, com o toggle "Nominal" ativo, o
`<select>` de cenário mostrava (e permitia abrir) todos os casos de
sintonia inadequada (`_bad_pll`) também. Só depois de alternar manualmente
para "Sintonia inadequada" e voltar para "Nominal" o filtro passava a
funcionar corretamente.

## Causa

A filtragem das `<option>` do `#scenario-picker` (`opt.hidden = ...`) só
roda **dentro de `setPllMode`** — nunca na simples inicialização. A última
linha do `<script>` chamava só `switchScenario(currentKey)`, então o
`<select>` nascia com todas as opções visíveis (inclusive `_bad_pll`),
mesmo com `pllMode = "nominal"` já definido em JS e o botão "Nominal"
marcado como ativo no HTML. Só depois de alternar o toggle manualmente (o
que dispara `setPllMode` de verdade) o filtro passava a valer.

## Fix (2026-08-18)

Em `src/report/renderer.py`, trocado, na última linha do `<script>`:

```javascript
switchScenario(currentKey);
```
por
```javascript
setPllMode(pllMode);
```

`setPllMode("nominal")` já reencontra o cenário equivalente (o próprio
`currentKey`, pois os cenários nominais vêm primeiro na ordenação — ver
`_sort_key` em [[bad-pll-dashboard-filter]]) e chama `switchScenario`
internamente via `_findEquiv`, então o cenário inicial exibido não muda —
só passa a aplicar o filtro do `<select>` desde o primeiro carregamento.

## Verificação

No browser pane (via `http.server` local, `file://` não carrega o Plotly
CDN — ver armadilha em `dashboard-html-editor` SKILL.md): na carga inicial,
30 opções totais, 22 visíveis, 0 `_bad_pll` visíveis (as 8 corretamente
ocultas). Alternância manual "Sintonia inadequada" ↔ "Nominal" continua
funcionando nos dois sentidos.

## Lição

Para qualquer novo elemento filtrado por `pllMode` (select, optgroup,
tooltip do SVG, tabela comparativa...), checar se a filtragem depende de
alguma função ser chamada explicitamente (`setPllMode`) ou se lê a
variável `pllMode` direto a cada render (`renderComparisonTable`,
`selectLocation`) — só o primeiro tipo precisa de uma chamada de
inicialização explícita para não nascer "sem filtro" na carga da página.
