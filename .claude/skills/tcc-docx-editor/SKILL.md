# Skill: tcc-docx-editor

Edita o TCC DOCX (arquivo atual definido em `config.py` — hoje
`TCC_Victor_Bruno_V9_novo_indice_2.docx`) manipulando o OOXML diretamente.
Modo aceito pelo Victor: **edições diretas no XML, sem tracked changes**
(`helpers.py` mantém os geradores com `w:ins` caso volte a ser necessário).

## Fragmento externo (não o canônico) — ver `fragmento_externo.md`

Quando o alvo é um rascunho externo isolado (ex.: `capitulos_4_5_revisados.docx`,
na pasta `Fragmentos/` do TCC no OneDrive, plain-Normal-style, sem tracked
changes/comentários/tabelas), o OOXML-surgery deste arquivo é overkill: usa-se
**python-docx direto**, sem staging, sem `repack.py`, sem IDs a rastrear. Caminho
completo em `fragmento_externo.md`.

Todo o workflow, as armadilhas (inserção de figura, renumeração, troca de termo,
`docPr` duplicado, conferência de MD5) e as lições de redação estão em
**`fragmento_externo.md`**. Ler antes de tocar num fragmento.

Para levar um fragmento **para dentro** do canônico, ver
**`mesclagem_no_canonico.md`**: comparar as árvores de seção antes de trocar
(o fragmento pode ser mais raso que o capítulo que substitui), mapear os
títulos para `Ttulo1`–`Ttulo4` ou eles somem do sumário, inverter a convenção
de legenda, e **reescalar as figuras da largura útil de origem para a de
destino** (o fragmento é Carta, 6,50 in; o TCC é A4, 6,30 in).

## Revisão de português — ver `revisao_pt.md`

Passagem linguística separada das edições de conteúdo. `scripts/check_pt.py`
varre o `document.xml` atrás das classes que já apareceram neste documento
(regência `capacidade … em`, `onde` não locativo, `através de`, vírgula entre
relativo e verbo, resíduo de LaTeX, duplo espaço, placeholder, em-dash). Ele
**não** pega concordância, coesão nem frase sem verbo principal: isso só sai
lendo o `dump_blocks.py` do corpo inteiro. `revisao_pt.md` diz o que é erro, o
que é falso positivo e quais armadilhas de execução a rodada de 2026-09-12
encontrou.

## Convenções de escrita

- **Nunca usar travessão/em-dash ("—") no texto do TCC.** Reescrever a
  frase com vírgula, ponto-e-vírgula, parênteses ou período em vez de
  intercalar com "—". Vale para texto novo e para revisão de texto
  existente — se um parágrafo editado tiver "—", removê-lo como parte da
  mesma edição.
- Não citar arquivo/script/variável de código no texto (`params.m`,
  `nome.txt`, `VARIAVEL_MAIUSCULA`) — usar termos de engenharia/modelagem.
  Nomes de bloco/subcircuito de esquemático (`RESETI_I1`, `.SUB Clarke`,
  `Sinusoidal Measurement`) são exceção e podem ficar. Ver
  `feedback_docx_no_code_artifacts` na memória.
- **Conclusão (Cap. 6) sobe de altitude, não de profundidade.** É uma
  consolidação genérica do trabalho inteiro: nem parafrasear o "Resumo e
  conclusões" do capítulo de resultados, nem aprofundar além dele com
  números e cruzamentos novos. Percorrer o arco (contexto → teoria →
  método → síntese qualitativa dos resultados) e fechar com contribuição,
  limites de validade e implicação prática. Medir sobreposição literal com
  o resumo do capítulo é teste mecânico útil, mas insuficiente: dá para ter
  sobreposição zero e ainda estar dizendo a mesma coisa. Ver
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
  - `word_finalize.ps1 -In <montado> -Out <final> [-Pdf <pdf>]` — passa o DOCX
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

- **Pré-check por MD5, não por timestamp/bytes.** Uma edição do usuário no Word
  pode manter o tamanho. Foi o MD5 que pegou, numa entrega do fragmento, que ele
  havia salvo o arquivo 8 minutos depois da minha cópia; entregar teria apagado
  o trabalho dele em silêncio.
- **Backup datado antes de sobrescrever, sempre**
  (`<nome>_backup_YYYYMMDD_HHMMSS.docx`, na mesma pasta).
- **Conferir que o Word está fechado** (`tasklist | grep -i winword`) e que não
  há arquivo de lock `~$*` na pasta. Trocar os bytes por baixo de uma sessão
  viva quebra o sincronismo do OneDrive: o Word passa a mostrar
  **"CARREGAMENTO BLOQUEADO"** e a recusar o upload.
- **Nunca entregar um zip montado à mão direto.** Rodar `word_finalize.ps1`
  antes. O arquivo montado abre e até exporta PDF, mas o `w:dirty` do sumário
  deixa o documento modificado no instante em que abre, o que dispara o mesmo
  bloqueio de upload. E os `PAGEREF` de seções removidas ficariam como
  "Erro! Indicador não definido" até alguém atualizar na mão.
- **`audit_docx.py` é o que distingue "arquivo corrompido" de "problema de
  sincronismo".** Quando o Word reclamar, rodar antes de mexer em qualquer
  coisa: se der 0 falhas, o conteúdo está são e o problema é de upload.

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
- **Delta de contagem em substituição**: trocar 1 bloco por N parágrafos
  dá `<w:p` **+(N-1)**, não +N. Errar isso na spec faz o `docx-scripter`
  abortar (corretamente) em vez de entregar. Conferir a aritmética antes de
  mandar a spec.
- **Grep com classe de caracteres acentuada não casa**: `invers[ãa]o`,
  `imped[âa]ncia` retornam **zero** em locale C, porque o multibyte é
  quebrado dentro do `[...]`. Zero resultado aqui é falso negativo, não
  ausência — repetir com padrão literal. E `grep -c` casa substring:
  "ISE" deu 12 ocorrências que eram todas "LISERRE"; usar `-w` ou olhar o
  contexto antes de concluir que um termo é usado no texto.
- **KB de conteúdo pode mentir sobre o que já foi escrito.** O
  `content_map.md` dava o Cap. 6 como "conclusão redigida" e o capítulo
  estava vazio no arquivo vivo. Antes de julgar/editar uma seção, confirmar
  o estado no XML recém-extraído e corrigir o KB no passo 9.
- **gen_*.py**: todo replace com count esperado explícito (falhar se
  divergir); `ET.fromstring` no resultado antes de gravar; wrapper UTF-8 no
  stdout (`io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
  errors='replace')`) ou o print quebra em cp1252.

## Referência de IDs e armadilhas XML

Ver `.claude/kb/tcc-word/docx_structure.md` — registro de IDs usados/próximos
e "Armadilhas de edição XML" (sectPr final via `rindex`, falso positivo
`<w:p` vs `<w:pgSz`, etc.). Histórico de entregas: `historico_entregas.md`.
