# Skill: tcc-docx-editor

Edita o TCC DOCX (arquivo atual definido em `config.py` — hoje
`TCC_Victor_Bruno_V9_novo_indice.docx`) manipulando o OOXML diretamente.
Modo aceito pelo Victor: **edições diretas no XML, sem tracked changes**
(`helpers.py` mantém os geradores com `w:ins` caso volte a ser necessário).

## Divisão de trabalho por modelo

| Quem | Faz |
|---|---|
| **Modelo principal (Sonnet/Opus)** | Interpretar o pedido; ler os dumps e mapear blocos; redigir o conteúdo; escrever os scripts `gen_*.py` (XML, IDs e counts — a parte que dá errado); revisar a saída de verificação; decidir a entrega; atualizar KB |
| **Agente `docx-runner` (Haiku)** | Staging (copiar/desempacotar), rodar dumps de inspeção, executar os `gen_*.py`, repack e entrega ao OneDrive — tudo mecânico, com regras de aborto |

Delegar via Agent tool (`subagent_type: "docx-runner"`), com prompt
autocontido: paths exatos, scripts a rodar com argumentos, e o que é
"saída esperada" (para o agente saber quando abortar). Para edições
triviais (1 comando), rodar direto sem agente — o overhead não compensa.

## Dependências

- `config.py` (nesta pasta) — paths pessoais (gitignored)
- `helpers.py` (nesta pasta) — geradores de parágrafo OOXML com `w:ins`
- `scripts/` (nesta pasta) — utilitários fixos, todos `python.exe <script> <args>`:
  - `dump_headings.py <xml>` — mapa de títulos com índice de bloco
  - `dump_blocks.py <xml> <ini> <fim> [--raw]` — texto/XML de intervalo de blocos
  - `find_text.py <xml> <padrão> [--regex]` — ocorrências com bloco + contexto
  - `check_ids.py <xml>` — máximos de bookmark/ins/paraId + flag dirty do TOC
  - `repack.py <template.docx> <xml> <saida.docx>` — injeta document.xml no ZIP

## Workflow padrão

```
1. STAGING (docx-runner): OneDrive → C:\Temp\tcc_edit.docx →
   extrair word/document.xml → C:\Temp\doc_tcc_edit.xml
   (guardar timestamp/bytes do DOCX no OneDrive p/ pré-check da entrega)
2. INSPEÇÃO (docx-runner): dump_headings / dump_blocks / find_text / check_ids
3. PLANO (principal): mapear blocos, redigir conteúdo, apresentar ao usuário
   e AGUARDAR APROVAÇÃO antes de editar
4. SCRIPT (principal): escrever C:\Temp\gen_<tema>.py — ler doc_tcc_edit.xml,
   aplicar edits com counts verificados, sanity checks, gravar doc_tcc_<tema>.xml
5. EXECUÇÃO (docx-runner): rodar o gen + dumps de verificação sobre a saída
6. REVISÃO (principal): conferir a saída dos checks
7. ENTREGA (docx-runner): pré-check timestamp OneDrive → repack.py →
   cp ao OneDrive → ls -la de confirmação
8. KB (principal): atualizar docx_structure.md / historico_entregas.md /
   content_map.md / pendencias.md conforme o caso
```

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
- **PowerShell + `python -c` inline quebra** com regex `[...]` — sempre
  escrever script em arquivo e rodar o arquivo.
- **Sumário (TOC)**: texto das entradas fica em cache no XML — um replace de
  título deve esperar 2 ocorrências (título real + cache), e o campo deve
  estar com `w:dirty="true"` para o Word reconstruir ao abrir.
- **gen_*.py**: todo replace com count esperado explícito (falhar se
  divergir); `ET.fromstring` no resultado antes de gravar; wrapper UTF-8 no
  stdout (`io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
  errors='replace')`) ou o print quebra em cp1252.

## Referência de IDs e armadilhas XML

Ver `.claude/kb/tcc-word/docx_structure.md` — registro de IDs usados/próximos
e "Armadilhas de edição XML" (sectPr final via `rindex`, falso positivo
`<w:p` vs `<w:pgSz`, etc.). Histórico de entregas: `historico_entregas.md`.
