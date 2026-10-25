---
name: dashboard-previa-standalone
description: Como prototipar um elemento novo do dashboard (capítulo do palco, diagrama, layout) num HTML standalone no scratchpad, com screenshots do Edge headless por passo, antes de tocar em src/
---

# Prévia standalone de elemento novo

Usar quando o pedido é um elemento **novo** cujo visual ainda não está
decidido: capítulo do modo apresentação, diagrama interativo, layout de
palco. Para retocar um elemento que já existe (cor, tema), a injeção de CSS
sobre o HTML gerado (ver "Armadilhas" no SKILL.md) continua melhor.

Origem: capítulo 0 "Faltas destacadas" (2026-10-21), três rodadas de prévia
na mesma conversa até o "ficou muito bom".

## Passos

1. **Ler o que já existe**: o doc de KB do elemento vizinho (ex.:
   `layout/roteiro-casos-tcc.md`) e o SVG ou CSS que a prévia vai imitar
   (`assets/diagrams/ieee9bus_unifilar.svg`, variáveis de `.pres`). A
   prévia herda as coordenadas e as cores, para a migração ser cópia.
2. **Um arquivo só** no scratchpad: `previa_<tema>.html`, CSS e JS inline,
   sem Plotly e sem dados reais. O roteiro fica num array `steps` (título,
   etiqueta, parágrafos, ids a destacar), o mesmo formato que vai virar
   entrada de `CAPITULOS` em `roteiro.py`.
3. **Passo pela URL**: `location.hash` define o passo inicial
   (`previa.html#3`). Assim cada passo vira um PNG sem Playwright:

   ```bash
   EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
   "$EDGE" --headless --disable-gpu --window-size=1600,900 \
     --screenshot="$(pwd -W)/passo$n.png" "file:///$(pwd -W)/previa.html#$n"
   ```

   Ler 2 ou 3 PNGs (o passo mais denso e o resumo), não todos.
4. **Conferir antes de mostrar**: corte no `viewBox` (gerador na borda),
   rótulo sobre linha, texto que estoura o cartão. Na primeira rodada, o G3
   e o G1 saíram cortados.
5. **Afirmação técnica no texto** (severidade, ordem, distância): conferir
   com cálculo ou com o TCC. Número fica fora da tela se não estiver no TCC
   (regra do deck exato); pode guiar uma posição relativa, como a régua.
6. **Entregar** o caminho absoluto do HTML (o usuário abre e usa seta ou
   clique) e o dos PNGs. Listar só o que o usuário precisa decidir.
7. **Aprovado → registrar antes de implementar**: doc de KB com o design e
   os textos (o scratchpad some com a sessão), depois implementar pelo
   workflow normal do SKILL.md.

## Variante: injetar no palco real

Quando o elemento novo **acompanha um gráfico que já existe** (painel ao
lado, número sobre a curva, passos de um capítulo), injetar no HTML gerado
dá a prévia com os dados de verdade, sem redesenhar nada. Usado em
2026-10-24 (fasor, mini-mapa, passos, destaque; aprovados de primeira).

1. Playwright no venv do scratchpad, `chromium.launch(channel="msedge")`,
   viewport 1920×1080, `file://` do `output/pll_metrics.html`.
2. Abrir o capítulo: `tccCap = CAPS.findIndex(c => c.id === "<id>");
   presToggle()`.
3. `page.evaluate(js)` monta o elemento: mover `#pres-plot` para uma linha
   flex com um painel ao lado, `Plotly.relayout`/`addTraces` para
   anotações. Os dados de curva vêm de `gd._fullData` (os de `SCENARIOS`
   estão em base64).
4. Elemento animado: um PNG por instante (passar `t` ao `evaluate`), não
   um vídeo.
5. Ler todos os PNGs antes de mostrar: na rodada de 10-24, o rótulo de
   retenção cortou no mapa e o vetor da rede sumiu sob o da nominal.

Na migração para `src/`, o que a prévia fez com `relayout` vira campo em
`CAPITULOS` + função num arquivo de `src/report/js/`; a largura do gráfico passa a ser
explícita no `Plotly.react` (senão cobre o painel ao lado).

## Armadilhas

- O arquivo da prévia pode ser alterado por fora entre rodadas (o usuário
  abre no editor). O `Write` recusa: reler e então reescrever. Guardar uma
  cópia `_v2` antes de reescrever por inteiro.
- O alvo de clique tem de ser um `<rect class="hit">` transparente com
  `pointer-events: all`. Uma linha de 2 px sozinha é difícil de clicar no
  projetor.
- Os raios e rótulos por cima precisam de `pointer-events="none"`, senão
  roubam o clique do ponto.
