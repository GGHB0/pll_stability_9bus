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
4. Registrar no `_index.yaml` da pasta.
5. Rodar `.venv\Scripts\python.exe scripts\kb_links.py all` e conferir
   `0 links quebrados · 0 órfãos · 0 sem referência`.

## Ao editar um doc

- Se o texto passa a citar um assunto que tem doc próprio, trocar a menção por
  `[[slug]]`. Menção por nome de arquivo (`ver pll_loop_filter_gains.md`) vira
  `[[pll-loop-filter-gains]]`.
- Ao renomear ou remover um doc, rodar o script: o `check` lista quem ficou
  com link quebrado.

## Convenções

- `[[slug]]` aponta para o `name:` do destino, não para o nome do arquivo. O
  `aliases:` é o que faz o Obsidian/Foam abrir o link (`pll_contingencies.md`
  ≠ `pll-contingencies`).
- Nunca apontar `[[...]]` para a memória do Claude (fora do repo): usar o doc
  do KB equivalente.
- `index.md` de cada pasta, `kb/index.md` e `kb/grafo.md` são **gerados**: não
  editar entre os marcadores `kb-links:begin/end`. Índice sem marcadores
  (`dashboard/`, `python/`) é manual: acrescentar a linha à mão.
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
