---
name: dashboard-html-editor-historico
description: Histórico de versões da skill dashboard-html-editor (v1.0.0 a v1.6.0) e as lições de cada rodada
---

# Histórico da skill dashboard-html-editor

Saiu do SKILL.md em 2026-10-21 (v1.6.0), que estava em 186 de 200 linhas.
O SKILL.md mantém só o workflow, a tabela de arquivos, as armadilhas e as
convenções.

v1.0.0 (2026-07-24): criada a partir do padrão observado na remoção das
métricas ΔP/ΔQ e dos emoji dos botões/abas.

v1.1.0 (2026-07-24): adicionada a linha "remover aba/gráfico inteiro" na
tabela (padrão da remoção do `build_resume`); nova seção "Armadilhas
conhecidas" com o bug do `goToChart`/`xref` achado durante a verificação
desta mesma mudança; passo de verificação reforçado para interações
clicáveis, com a regra de não expandir escopo ao achar bugs não
relacionados (usar `spawn_task`).

v1.2.0 (2026-07-25): nova linha "redefinir cálculo de métrica existente" na
tabela — padrão da troca de V min→V médio (mínimo instantâneo virou média
numa janela por regra de cenário), que tocou `loader.py`, `settings.py`
(threshold renomeado) e toda referência à chave antiga em `renderer.py`
(cards, tabela comparativa, JS de ordenação, story) simultaneamente — grepar
o nome da chave/threshold no `src/` inteiro antes de considerar a renomeação
completa, não só nos arquivos "óbvios".

v1.3.0 (2026-07-25): removido o overlay "Comparar PLL" (`ghost-toggle`,
`ghostMode`/`_exactEquiv`/`_ghostData`/`toggleGhost` em `renderer.py`) por
não estar sendo usado — não confundir com o toggle nominal/sintonia
inadequada (`pllMode`), que é feature separada e não foi tocado; doc
`graficos/dashboard-zoom-ghost.md` virou `graficos/dashboard-zoom-export.md`
(nome não fazia mais sentido sem o fantasma). Também corrigido um bug real
achado ao investigar "título dos gráficos deveria ser branco": a barra de
título do painel (`_label`) já era branca no Python, mas o JS
`themedLayout` a confundia com `_group_title` (ambos usam `xref="paper"`
desde o redesign de títulos) e sobrescrevia para cinza — fix por `yref`,
detalhes em `layout/dark-mode-legend-title-fixes.md` (Fix 5).

v1.4.0 (2026-07-25): correção da 3ª mudança do v1.3.0 — a 1ª tentativa do
eixo Y (copiar o texto completo do painel, ex. `"P / Q UFV (pu)"`) foi
rejeitada pelo usuário: o pedido real era identificar a **grandeza física
genérica** (`"Tensão (pu)"`, `"Potência (pu)"`, `"Frequência (Hz)"`), o
mesmo critério já usado no `"Tempo (s)"` do eixo X — não o título
específico daquele painel. Fix: `_AXIS_LABELS` (dicionário `kind →
grandeza`) em `chart.py`, ver `graficos/construcao-graficos.md`. **Lição
para novos painéis/labels**: quando o pedido é "identificar o que é" um
eixo/valor, checar se existe uma convenção já usada em outro eixo do
mesmo gráfico antes de assumir que copiar o texto mais específico
disponível resolve — geralmente não resolve.

v1.5.0 (2026-07-28): faixa ONS §5.2.1 no painel de frequência (`add_hrect`/
`add_hline`) — mantida. Verificação no browser pane revelou uma armadilha
nova (não relacionada ao código): Plotly não carrega em preview `file://`
(script CDN bloqueado, sem erro de console) — resolvido servindo `output/`
via `python -m http.server` local. Registrado em "Armadilhas conhecidas" e
no passo 5 do workflow.

Também nesta sessão: um painel extra "Deslizamento de Fase PLL" (Δθ vs.
relógio nominal de 60 Hz, a partir da pergunta "dá pra fazer um delta ângulo
comparando essas frequências com 60Hz?") foi implementado com plano
apresentado e aprovado — mas o usuário rejeitou o resultado ("Não era esse
deslizamento de Fase PLL que eu pedi") e pediu para reverter. Reverted em
`chart.py`/`loader.py`, doc e CHANGELOG. **Lição**: aprovação de um plano
escrito não é garantia de que a interpretação bateu com o pedido — pedidos
formulados como pergunta aberta ("dá pra fazer X comparando Y?") merecem
uma repetição mais explícita do que vai ser mostrado (ex.: confirmar se é
um valor acumulado/integrado ou outra coisa) antes de implementar, mesmo
com plano aprovado.

v1.6.0 (2026-10-21): capítulo "Faltas destacadas" (implementado no mesmo dia) do modo apresentação
(ver `kb/dashboard/layout/faltas-destacadas.md`). Saiu de três prévias
**standalone**: um HTML no scratchpad com o unifilar redesenhado e o roteiro
de passos, sem passar pelo `app.py`. Cada rodada levou segundos (Edge
headless `--screenshot` com `#passo` na URL), contra minutos de regenerar
o dashboard. O fluxo virou o guia `previa-standalone.md`, e este histórico
saiu do SKILL.md para liberar espaço. **Lição**: frase de severidade ("mais
severo", "mais distante") num cartão é afirmação técnica. Conferir com
cálculo (Zbarra) ou com o TCC antes de mostrar, mesmo numa prévia.

v1.7.0 (2026-10-24): palco enriquecido. Marcação de acomodação na
Energização (linha + ponto + faixa de ±5% em v_d, eixo do erro em ±20°),
depois quatro elementos aprovados juntos: passos com frase-mensagem,
fasor animado, mini-mapa com retenção e número de destaque (ver
`kb/dashboard/layout/modo-apresentacao.md`). As prévias saíram por
**injeção no palco real** (seção nova em `previa-standalone.md`), com os
dados de verdade. **Lição**: a verificação no Edge headless clicando de
fato achou o gráfico cobrindo o painel ao lado (`Plotly.react` guarda a
largura antiga); a tela parada parecia certa.

v1.8.0 (2026-10-24, mesma conversa): ferramentas para o palco. O JS da aba
Análise TCC e do palco saiu da string `_TCC_JS` para 9 arquivos em
`src/report/js/` (HTML gerado idêntico byte a byte, `node --check` no
pre-commit); `scripts/verifica_palco.py` versiona a verificação que antes
morava no scratchpad; agente `palco-validator` lê as telas. Na mesma
rodada: vírgula decimal nos cartões e na tabela do palco, e marcação do
retorno à faixa de 2° nos capítulos com falta (seta a partir da eliminação,
porque o tempo é contado de t_clear). **Lição**: `tickvals` sem `ticktext`
herda o `hoverformat` (".3f") e escreve "60.000" no eixo; o mesmo erro
apareceu duas vezes na sessão.

v1.9.0 (2026-10-24, mesma conversa): tela 5 (Sequência negativa) do
palco. Trifásica da Barra 7 grafite, grossa e por cima, com caixa de seta
(`notas`); cor = barra e traço = curto (estilo opcional no 3º item de
`casos`); chips agrupados por barra; cartões trocados por uma matriz barra
× curto (`matriz`), que traz a trifásica da Barra 6 (0,0011 pu) citada no
texto e que não aparecia na tela. Prévias por injeção nas duas resoluções
antes de cada passo. **Lição**: ao injetar painel ou tabela numa prévia,
chamar `Plotly.relayout` com a largura e a altura novas do `#pres-plot`;
sem isso o SVG antigo cobre o elemento injetado e a prévia parece quebrada.
