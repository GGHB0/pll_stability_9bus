# Armadilhas de SVG desenhado à mão

Referência da skill `svg-diagrams`, desmembrada do SKILL.md em 2026-10-02.
Ler antes de escrever o primeiro `<text>` ou `<path>`.

## Armadilha 1 — Subscritos

**Nunca** use underscore literal (`V_dc`, `u_abc`) como substituto de subscrito — isso
renderiza como texto cru, não como notação de engenharia. Sempre use `<tspan>`:

```xml
<text font-style="italic">V<tspan baseline-shift="sub" font-size="75%">dc</tspan></text>
<text font-style="italic">u<tspan baseline-shift="sub" font-size="75%">abc</tspan>(PCC)</text>
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
