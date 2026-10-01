# Skill: tcc-docx-editor

Edita o TCC DOCX (`config.py`; hoje `TCC_Victor_Bruno_V10.docx`) no OOXML.
**Padrões fixos** (Resumo↔Abstract + comentário, fechar/reabrir Word): `padroes_revisao.md`.
Modo aceito pelo Victor: **edições diretas no XML, sem tracked changes**
(`helpers.py` mantém os geradores com `w:ins` caso volte a ser necessário).

## Fragmento externo (não o canônico) — ver `fragmento_externo.md`

Quando o alvo é um rascunho externo isolado (ex.: `capitulos_4_5_revisados.docx`,
na pasta `Fragmentos/` do TCC no OneDrive, plain-Normal-style, sem tracked
changes/comentários/tabelas), o OOXML-surgery deste arquivo é overkill: usa-se
**python-docx direto**, sem staging, sem `repack.py`, sem IDs a rastrear. Todo
o workflow, as armadilhas (inserção de figura, renumeração, troca de termo,
`docPr` duplicado, conferência de MD5) e as lições de redação estão em
**`fragmento_externo.md`**. Ler antes de tocar num fragmento.

Para levar um fragmento **para dentro** do canônico, ver
**`mesclagem_no_canonico.md`**: comparar as árvores de seção antes de trocar
(o fragmento pode ser mais raso que o capítulo que substitui), mapear os
títulos para `Ttulo1`–`Ttulo4` ou eles somem do sumário, inverter a convenção
de legenda, e **reescalar as figuras da largura útil de origem para a de
destino** (o fragmento é Carta, 6,50 in; o TCC é A4, 6,30 in).

## Cópia comentada externa (Oscar) — ver `mesclagem_comentarios.md`

Cópia do TCC com comentários novos do Oscar (não um rascunho de texto — ver
"Fragmento externo" acima): mesclar só os comentários, sem as edições de
texto soltas que vierem junto. Achar os novos por diff de texto e confirmar
por **data** (não por ID, que o Word renumera) contra o comentário mais
recente já no canônico, para não duplicar o que já foi mesclado com redação
levemente diferente. Detalhe da mesclagem cirúrgica nas 4 partes XML de
comentário em `mesclagem_comentarios.md`.

## Revisão de português — ver `revisao_pt.md`

Passagem linguística separada das edições de conteúdo. `scripts/check_pt.py`
varre o `document.xml` atrás das classes já vistas (regência `capacidade …
em`, `onde` não locativo, `através de`, vírgula entre relativo e verbo,
resíduo de LaTeX, duplo espaço, placeholder, em-dash). **Não** pega
concordância, coesão nem frase sem verbo principal: isso só sai lendo o
`dump_blocks.py` do corpo inteiro. Detalhes e falsos positivos em
`revisao_pt.md`.

## Formatação ABNT e paginação — skill `tcc-abnt-layout`

Passagem de **forma** (paginação, legendas, recuo, listas, equações), com
verificadores e `decisoes.md`; o pipeline é o deste arquivo. **Ilustração ou
equação nova no canônico** segue o padrão aplicado: legenda `SEQ` por
`tcc-abnt-layout/scripts/campos.py`, tipo certo (Figura ou Tabela, D9) na
legenda e na remissão, rótulo `(N.M)`.

## Convenções de escrita

- **Nunca usar travessão/em-dash ("—") no texto do TCC.** Reescrever com
  vírgula, ponto-e-vírgula, parênteses ou período. Vale para texto novo e
  para revisão: parágrafo editado com "—" perde o travessão na mesma edição.
- Não citar arquivo/script/variável de código no texto (`params.m`,
  `nome.txt`, `VARIAVEL_MAIUSCULA`) — usar termos de engenharia/modelagem.
  Nomes de bloco/subcircuito de esquemático (`RESETI_I1`, `.SUB Clarke`)
  são exceção. Ver `feedback_docx_no_code_artifacts` na memória.
- **Conclusão (Cap. 6) sobe de altitude, não de profundidade**: consolidação
  genérica do trabalho inteiro, nem parafraseando o "Resumo e conclusões" do
  capítulo de resultados nem aprofundando além dele. Percorrer o arco
  (contexto → teoria → método → síntese qualitativa) e fechar com
  contribuição, limites de validade e implicação prática — sobreposição
  literal zero com o resumo não basta, dá para dizer a mesma coisa. Ver
  `tcc-conclusion-altitude` na memória (2 versões recusadas em 2026-09-12).

## Divisão de trabalho por modelo (3 níveis)

| Nível | Quem | Faz |
|---|---|---|
| **Síntese** | Opus — *só quando necessário* | Redigir conteúdo acadêmico novo (seções/parágrafos do zero), decisões estruturais com trade-offs (ex.: reestruturar capítulo) |
| **Planejamento + scripting** | Sonnet — o default | Mapear blocos a partir dos dumps, redigir edições rotineiras (renumeração, refs cruzadas, typos, formatação), escrever os `gen_*.py`, revisar checks, atualizar KB |
| **Execução** | Haiku (agente `docx-runner`) | Staging, dumps, rodar scripts, repack, entrega ao OneDrive |

### Regras de escalonamento

- **Sessão rodando em Sonnet**: fazer planejamento, conteúdo e scripting
  direto; delegar só o mecânico ao `docx-runner`. **Nunca** escalar para
  Opus por conta própria — se a tarefa parecer exigir síntese pesada,
  dizer isso ao usuário e deixar a troca de modelo com ele.
- **Sessão rodando em Opus**: usar Opus apenas para interpretar o pedido,
  redigir conteúdo novo e revisar/aprovar. O scripting desce para o agente
  `docx-scripter` (Sonnet) com uma **spec precisa** (blocos-alvo, strings
  old→new com counts esperados, conteúdo já redigido, IDs); o mecânico
  desce para o `docx-runner` (Haiku).
- **Edição trivial** (1–2 replaces óbvios): qualquer modelo faz direto,
  sem agente — o overhead de delegar não compensa.

Delegar via Agent tool (`subagent_type: "docx-scripter"` / `"docx-runner"`),
com prompt autocontido: paths exatos, o que rodar, e qual é a "saída
esperada" (para o agente saber quando abortar/perguntar).

## Dependências

- `config.py` (nesta pasta) — paths pessoais (gitignored)
- `helpers.py` (nesta pasta) — geradores de parágrafo OOXML com `w:ins`
- `scripts/` (nesta pasta) — utilitários fixos, todos `python.exe <script> <args>`:
  - `dump_headings.py <xml>` — mapa de títulos com índice de bloco
  - `dump_blocks.py <xml> <ini> <fim> [--raw]` — texto/XML de intervalo de blocos
  - `find_text.py <xml> <padrão> [--regex]` — ocorrências com bloco + contexto
  - `check_ids.py <xml>` — máximos de bookmark/ins/paraId + flag dirty do TOC
  - `check_pt.py <xml> [--corpo N]` — varredura de português (ver
    `revisao_pt.md`); rodar também sobre o XML de saída, antes do repack
  - `repack.py <template.docx> <xml> <saida.docx>` — injeta document.xml no ZIP
  - `audit_docx.py <arquivo.docx> [--util-in N]` — auditoria estrutural
    pré-entrega (comentários, bookmarks, campos, `PAGEREF` órfão, imagens,
    content-types, em-dash); sai com código 1 se algo falhou
  - `word_finalize.ps1 -In <montado> -Out <final> [-Pdf <pdf>] [-Comments <json>] [-Replies <json>]` — passa o DOCX
    pelo próprio Word: reconstrói o sumário, zera `w:dirty` e **prova que o
    Word consegue salvar**, não só abrir

## Workflow padrão

```
1. STAGING (docx-runner): OneDrive → C:\Temp\tcc_edit.docx →
   extrair word/document.xml → C:\Temp\doc_tcc_edit.xml
   (guardar o **MD5** do DOCX no OneDrive p/ pré-check da entrega;
   timestamp e bytes não bastam, ver "Entrega" abaixo)
2. INSPEÇÃO (docx-runner): dump_headings / dump_blocks / find_text / check_ids
   (o estado real é o do XML recém-extraído; `content_map.md` pode estar
   desatualizado — ver "Notas críticas")
3. PLANO (principal): mapear blocos, redigir conteúdo, apresentar ao usuário
   e AGUARDAR APROVAÇÃO antes de editar
4. SCRIPT: escrever C:\Temp\gen_<tema>.py — ler doc_tcc_edit.xml, aplicar
   edits com counts verificados, sanity checks, gravar doc_tcc_<tema>.xml.
   Sessão em Sonnet → o próprio principal; sessão em Opus → docx-scripter
   via spec (o scripter também roda o script e a verificação, cobrindo o 5)
5. EXECUÇÃO (docx-runner): rodar o gen + dumps de verificação sobre a saída
6. REVISÃO (principal): conferir a saída dos checks
7. FINALIZAÇÃO: word_finalize.ps1 → audit_docx.py (tem que dar 0 falhas)
8. ENTREGA (docx-runner): Word fechado + sem lock `~$` → **MD5 do
   OneDrive igual ao do staging** → backup datado → cp → ls -la
9. KB (principal): atualizar docx_structure.md / historico_entregas.md /
   content_map.md / pendencias.md conforme o caso
```

## Entrega (aprendido em 2026-09-02, na marra)

- **Pré-check por MD5, não por timestamp/bytes** (o MD5 pegou um save do Victor
  8 min depois da cópia). MD5 mudou → refazer staging e reaplicar o `gen_*.py`
  (que só lê o XML do staging); sync de outro aparelho (Bruno) chega em rajadas,
  até com mtime voltando: esperar parar de mudar antes de refazer (2026-10-01).
- **Backup datado antes de sobrescrever, sempre**: `<nome>_backup_YYYYMMDD_HHMMSS.docx`
  em `_backups/<versão>/` ao lado do arquivo (`comentado/_backups/V10/`).
- **Conferir que o Word está fechado** (`tasklist | grep -i winword`) e sem
  lock `~$*` na pasta — trocar os bytes por baixo de uma sessão viva quebra o
  sincronismo do OneDrive ("CARREGAMENTO BLOQUEADO", upload recusado).
- **Nunca entregar um zip montado à mão direto**: rodar `word_finalize.ps1`
  antes — o zip à mão abre e até exporta PDF, mas o `w:dirty` do sumário
  deixa o documento modificado ao abrir, disparando o mesmo bloqueio, e os
  `PAGEREF` de seções removidas ficam "Erro! Indicador não definido".
- **`audit_docx.py` distingue "arquivo corrompido" de "problema de
  sincronismo"**: 0 falhas quando o Word reclamar = conteúdo são, problema é
  de upload.

## Notas críticas

- **VFS isolation**: o `python.exe` do Windows NÃO acessa
  `/c/Users/victo/AppData/Roaming/Claude/...` (VFS do Claude Desktop).
  Trabalhar sempre com arquivos em `C:\Temp\` ou no repositório.
- **OneDrive lock**: nunca editar no path do OneDrive; copiar para C:\Temp.
  A cópia de VOLTA falha se o documento estiver aberto no Word
  ("Device or resource busy") — pedir para fechar antes da entrega.
- **Word renumera IDs ao salvar**: se o usuário salvou o DOCX no Word, o
  registro de IDs do KB fica obsoleto — rodar `check_ids.py` no XML recém-
  extraído antes de inserir qualquer elemento novo.
- **paraId**: máximo `0x7FFFFFFF`; prefixos A–F estouram. Usar `1FB0xxxx`
  (sequência registrada no KB) e conferir colisão com grep antes.
- **PowerShell + `python -c` inline quebra** com regex `[...]` — escrever
  script em arquivo e rodar o arquivo.
- **Sumário (TOC)**: texto das entradas fica em cache no XML — um replace de
  título espera 2 ocorrências (título real + cache), e o campo precisa de
  `w:dirty="true"` para o Word reconstruir ao abrir.
- **Delta de contagem em substituição**: trocar 1 bloco por N parágrafos dá
  `<w:p` **+(N-1)**, não +N — errar isso faz o `docx-scripter` abortar
  (corretamente); conferir a aritmética antes de mandar a spec.
- **Grep com classe de caracteres acentuada não casa** (`invers[ãa]o` etc.
  retornam zero em locale C, multibyte quebrado dentro do `[...]`): repetir
  com padrão literal antes de concluir ausência. `grep -c` casa substring
  ("ISE" deu 12 ocorrências, todas "LISERRE"): usar `-w` ou ver o contexto.
- **KB de conteúdo pode mentir sobre o que já foi escrito** (`content_map.md`
  dava o Cap. 6 como redigido com o capítulo vazio no arquivo vivo): confirmar
  no XML recém-extraído antes de julgar/editar, corrigir o KB no passo 9.
- **gen_*.py**: todo replace com count esperado explícito (falhar se
  divergir); `ET.fromstring` no resultado antes de gravar; UTF-8 no stdout
  com `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`, não
  `io.TextIOWrapper(sys.stdout.buffer, ...)` — dois módulos que se importam
  e fazem isso cada um por si fecham o buffer compartilhado ao ser coletado
  o primeiro wrapper (`ValueError: I/O operation on closed file`), achado ao
  escrever `build_plan.py` + `gen_oscar_cap5_comments.py` em 2026-09-29.

## Referência de IDs e armadilhas XML

Ver `.claude/kb/tcc-word/docx/docx_structure.md` — registro de IDs usados/próximos
e "Armadilhas de edição XML" (sectPr final via `rindex`, falso positivo
`<w:p` vs `<w:pgSz`, etc.). Histórico de entregas: `historico_entregas.md`.
