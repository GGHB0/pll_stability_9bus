# Armadilhas do pipeline DOCX

Continuação de `SKILL.md` (antes "Notas críticas"). Armadilhas do próprio XML
(sectPr via `rindex`, `<w:p` vs `<w:pgSz`, registro de IDs) ficam no KB, em
`.claude/kb/tcc-word/docx/docx_structure.md`.

## Ambiente

- **VFS isolation**: o `python.exe` do Windows não vê o VFS do Claude Desktop
  (`AppData/Roaming/Claude/...`); trabalhar em `C:\Temp\` ou no repositório.
- **OneDrive lock**: nunca editar no path do OneDrive; copiar para C:\Temp
  (`Copy-Item`/CopyFileW leem com o Word aberto; `zipfile` direto, não). A
  volta falha com o Word aberto.
- **PowerShell + `python -c` inline quebra** com regex `[...]`: escrever o
  script em arquivo e rodar o arquivo.

## IDs e comentários

- **Word renumera IDs ao salvar** (bookmark, comentário, paraId de
  comentário): o registro de IDs do KB fica obsoleto. Rodar `check_ids.py` no
  XML recém-extraído antes de inserir qualquer elemento novo.
- **Comentários são renumerados pela ordem no documento**: em 2026-10-02,
  reancorar o 87 antes do 86 fez o Word trocar os dois de número ao salvar
  (conteúdo e âncora certos). Conferir e responder comentário **pelo texto**,
  nunca pelo ID que estava no staging.
- **paraId**: máximo `0x7FFFFFFF`; prefixos A–F estouram. Usar `1FB0xxxx`
  (sequência registrada no KB) e conferir colisão com grep antes.
- **Parágrafo substituído leva os comentários ancorados nele**: o gen tem que
  recolocar `commentRangeStart`, `commentRangeEnd` e o run de
  `commentReference` de cada ID, e conferir que cada um aparece 1 vez.

## Contagens e buscas

- **Sumário (TOC)**: o texto das entradas fica em cache no XML. Um replace de
  título espera 2 ocorrências (título real + cache), e o campo precisa de
  `w:dirty="true"` para o Word reconstruir ao abrir.
- **Delta de contagem em substituição**: trocar 1 bloco por N parágrafos dá
  `<w:p` **+(N-1)**, não +N. Errar isso faz o `docx-scripter` abortar
  (corretamente); conferir a aritmética antes de mandar a spec.
- **Grep com classe acentuada não casa** (`invers[ãa]o` em locale C): repetir
  com padrão literal antes de concluir ausência. `grep -c` casa substring
  ("ISE" deu 12, todas "LISERRE"): usar `-w` ou ver o contexto.
- **Lista de siglas usa tabulação** entre sigla e significado: até 2026-10-02
  o `find_text.py` colava "GD" + "Geração" e `\bGD\b` dava zero. Corrigido
  (tab e quebra viram separador); em grep cru, procurar `'>GD<'`.
- **Equação é tabela com OMML**: `dump_blocks.py` mostra só "(TBL) (3.5)".
  Para saber o que a equação é, `--math`.

## Conteúdo

- **KB de conteúdo pode mentir sobre o que já foi escrito** (`content_map.md`
  dava o Cap. 6 como redigido com o capítulo vazio): confirmar no XML
  recém-extraído e corrigir o KB no passo 9.
- **Texto pronto do Victor também se confere**: em 2026-10-02 o texto pedido
  para a 3.1.2 dizia que (3.7) era a inversa dq→αβ; o `--math` mostrou que é
  v_q. Corrigir só a remissão, apresentar a correção no plano.
- **O nome de seção no pedido pode não ser o do arquivo** ("3.1. Modelagem
  Matemática" era "3.1. A Necessidade das Transformadas de Referência"):
  localizar pelo `dump_headings.py`, avisar, não renomear sem pedido.

## gen_*.py

Todo replace com count esperado explícito (falhar se divergir);
`ET.fromstring` no resultado antes de gravar; UTF-8 no stdout com
`sys.stdout.reconfigure(encoding='utf-8', errors='replace')`, não
`io.TextIOWrapper(sys.stdout.buffer, ...)`: dois módulos que se importam e
fazem isso cada um por si fecham o buffer compartilhado
(`ValueError: I/O operation on closed file`, 2026-09-29).
