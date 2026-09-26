# Interligação dos .md do KB

Todo conhecimento do KB fica ligado a pelo menos um tema. Nenhum doc nasce
solto, nenhum doc fica sem ninguém apontando para ele.

## Ao criar um doc em `.claude/kb/`

1. Frontmatter com `name:` (slug kebab-case, único em todo `.claude/`, sem
   reutilizar nome de skill), `description:` (uma linha) e
   `aliases: [<mesmo slug>]`.
2. **Referenciar pelo menos um tema existente** com `[[slug]]`: no texto, onde
   o assunto aparece, ou numa seção `## Relacionados` no final (1 a 3 itens,
   `- [[slug]] — motivo`). Preferir ligação a outra pasta quando houver
   (teoria em `pll/` ↔ aplicação em `simulation/`, norma em `standards/` ↔
   evento em `events/`, capítulo em `tcc-word/` ↔ base técnica).
3. Se o doc for fragmento de outro, os dois se apontam:
   `Continuação de [[origem]]` no novo, `... em [[fragmento]]` no original.
4. Rodar `.venv\Scripts\python.exe scripts\kb_links.py all`: acrescenta o doc
   ao `_index.yaml` da pasta, regenera índices e grafo, e audita. Conferir
   `0 links quebrados · 0 órfãos · 0 sem referência` e zero nas demais linhas.

## Ao editar um doc

- Se o texto passa a citar um assunto que tem doc próprio, trocar a menção por
  `[[slug]]`. Menção por nome de arquivo (`ver pll_loop_filter_gains.md`) vira
  `[[pll-loop-filter-gains]]`.
- Ao renomear ou remover um doc, rodar o script: o `check` lista quem ficou
  com link quebrado.

## Antes do commit

O hook `.githooks/pre-commit` roda o `check` sempre que o commit mexe em
`.md`, `_index.yaml` ou no script, e **bloqueia** se houver: link quebrado (KB
ou CLAUDE.md), slug duplicado, `.md` acima de 200 linhas no repo (README fora),
frontmatter sem `name`/`description`/`aliases`, doc fora do `_index.yaml` ou
índice gerado desatualizado. Órfão e doc sem referência só avisam. Bloqueou →
rodar o `all`, corrigir o resto, `git add` nos regenerados. Nunca
`--no-verify`. O que o script não julga (KB acompanhou o código? CHANGELOG?)
está no checklist de [git.yaml](../commands/git.yaml).

## Convenções

- `[[slug]]` aponta para o `name:` do destino, não para o nome do arquivo. O
  `aliases:` é o que faz o Obsidian/Foam abrir o link (`pll_contingencies.md`
  ≠ `pll-contingencies`).
- Nunca apontar `[[...]]` para a memória do Claude (fora do repo): usar o doc
  do KB equivalente.
- `index.md` de cada pasta, `kb/index.md` e `kb/grafo.md` são **gerados**: não
  editar entre os marcadores `kb-links:begin/end`. Índice sem marcadores
  (`dashboard/`, `python/`) é manual: acrescentar a linha à mão.
- `_index.yaml`: o `all` só **acrescenta** entradas que faltam (do
  frontmatter); descrição de pasta e ordem são manuais e preservadas. Doc
  removido: apagar a entrada à mão (o `check` acusa `ENTRADA SEM ARQUIVO`).
- **CLAUDE.md** guarda só o estável (projeto, mapa de pastas de topo, fluxo,
  armadilhas) e aponta para o KB por link markdown relativo. Nunca listar
  arquivos do KB nem copiar detalhe que muda (sinais, cenários, ganhos), nunca
  `@import` (carregaria o doc inteiro em toda sessão), nunca `[[slug]]` (fica
  fora do vault). O `check` também confere os links dele.
- Links para skills, agentes e regras usam link markdown relativo
  (`[svg-diagrams](../skills/svg-diagrams/SKILL.md)`), não `[[...]]`.

**Why:** o KB passou de 150 docs. Sem links, o conhecimento vira ilha: doc
novo não é achado, fragmento perde a origem e o Graph View do Obsidian não
mostra a relação entre teoria, simulação, norma e capítulo do TCC.

**How to apply:** vale para qualquer sessão ou skill que escreva em
`.claude/kb/` (`pdf-kb-updater`, `dashboard-html-editor`, `tcc-docx-editor`,
etc.). O script é determinístico, então rodar sempre, sem gastar subagente.
Escolher vizinhos para muitos docs de uma vez é trabalho repetitivo e vai para
subagente Haiku.
