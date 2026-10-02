# Mesclar Comentários de uma Cópia Externa do Oscar

Primeira aplicação: 38 comentários do Cap. 5, em 2026-09-29 (ver
`historico_entregas.md`). Cenário: o Victor recebe do Oscar uma cópia do TCC
(baixada do OneDrive/e-mail, ex.: `TCC_Victor_Bruno_V10 (1).docx`) com
comentários novos, às vezes junto com edições de texto soltas que o Victor
ou o Bruno já começaram a aplicar por cima. Pedido típico: só os comentários
(de uma seção específica), sem as edições de texto.

## Por que não é `word_finalize.ps1 -Comments`

Esse mecanismo (`d.Comments.Add`) serve para o **Claude** anotar um trecho
com um comentário novo, próprio — o autor sai como a conta do Office, daí o
prefixo `[Claude] `. Aqui o comentário já existe, tem autor (Oscar) e data
reais, e **não pode virar um comentário "do Claude"**: a autoria tem que ser
preservada.

## Por que não `Application.CompareDocuments` (Word)

Combinar/comparar os dois documentos no Word traz os comentários dos dois
lados junto com tracked changes, mas mexe na mesma passada nos **103
comentários existentes** (renumeração, threads, `done`-flags) — risco alto
para pouco controle. A cirurgia direta no XML é mais lenta de montar mas dá
controle total sobre o que muda.

## Passo a passo

1. **Extrair com `zipfile` do Python, nunca `unzip` do shell** para
   `comments.xml`: o `unzip` do Git Bash detecta a entrada como texto e faz
   conversão de codepage, embaralhando os acentos (silencioso — o XML
   continua bem formado, só o conteúdo vem errado). `document.xml` não sofreu
   o mesmo no caso de 2026-09-29 (arquivo maior, heurística de detecção
   diferente), mas não dá para confiar nisso: extrair as 5 partes
   (`document.xml` + `comments.xml` + `commentsIds.xml` + `commentsExtended.xml`
   + `commentsExtensible.xml`) sempre por `zipfile`.
2. **Diff de comentários por texto** entre o canônico e a cópia recebida:
   `w:comment` com o mesmo texto (ignorar `w:id`, o Word renumera cada save).
   Um comentário "novo" por esse diff pode já estar mesclado com uma
   diferença mínima de pontuação (aconteceu em 2026-09-29: vírgula a mais) —
   **confirmar por data**: nenhum comentário do Oscar deveria ter a mesma
   data de um já presente no canônico. Se o canônico não tem nada do Oscar
   depois de uma certa data, qualquer coisa datada de antes disso já foi
   mesclada antes, não é novo de verdade.
3. **Escopo pedido** (ex.: só um capítulo): achar o offset de byte do título
   real do capítulo em `document.xml` (não o do sumário, que aparece
   primeiro — procurar todas as ocorrências do título e usar a última) e
   bucketizar cada comentário pelo offset do `commentRangeStart`.
4. **Corresponder blocos** entre os dois arquivos: se a numeração de bloco
   (`dump_headings.py`) tiver um deslocamento constante, mapear por índice;
   qualquer parágrafo dividido no meio (ex.: um heading que veio partido em
   3 blocos por um bug do Word) quebra o deslocamento a partir dali — ajustar
   o deslocamento por trecho.
5. **Mapear o texto-âncora** do arquivo recebido para o texto do canônico
   com `difflib.SequenceMatcher(None, texto_recebido, texto_canonico)` e
   `get_opcodes()`, em vez de reescrever manualmente palavra por palavra: se
   o texto tiver edições soltas por cima (ex.: "Gráfico" no lugar de
   "Figura", ou uma sigla expandida), o alinhamento por conteúdo acerta o
   deslocamento certo no canônico automaticamente, sem precisar prever cada
   variação de gênero/palavra.
6. **Inserir os marcadores** (`commentRangeStart`/`commentRangeEnd` +
   `<w:r>...<w:commentReference/></w:r>`, estilo `Refdecomentrio`) diretamente
   no XML do parágrafo:
   - Bloco de um run só (mais comum): dividir o `<w:t>` nos pontos de corte.
   - Bloco com múltiplos runs (`<w:lastRenderedPageBreak/>` no meio, campo
     `SEQ` de legenda de figura, `w:rsidRPr` diferente por run): tokenizar os
     runs, achar em qual run cada offset cai (convenção *half-open*:
     `toff_i < pos <= toff_i+len_i`, corte no fim de um run em vez de no
     início do próximo, para não empatar), preservando `rPr` de cada run.
   - Comentário ancorado em imagem (range de texto vazio): localizar o
     `<w:r>` que contém o `<w:drawing>` e envolvê-lo inteiro.
   - Reaproveitar `paraId`/`durableId`/data do comentário original ao
     acrescentar em `comments.xml`/`commentsIds.xml`/`commentsExtended.xml`
     (`w15:done="0"`)/`commentsExtensible.xml`: preserva a autoria e a
     metadata do Oscar. Só o `w:id` numérico é novo (faixa livre acima do
     máximo existente).
7. **Verificar antes do repack**: `text_of(bloco_novo) == text_of(bloco_original)`
   (o texto visível não pode mudar, só os marcadores) e o texto entre
   `commentRangeStart`/`End` bate com o âncora esperado, para cada
   comentário.
8. **Repack manual das 5 partes** (não dá para usar `repack.py`, que só troca
   `document.xml`) → `word_finalize.ps1` (confere `comentarios` no resumo) →
   `audit_docx.py` → entrega.

## Relacionados

- `casos/fragmento_externo.md` / `casos/mesclagem_no_canonico.md` — mesclar **texto**
  (rascunho de capítulo), não comentários.
- `referencia/padroes_revisao.md` — comentário que o Claude mesmo redige, via
  `word_finalize.ps1 -Comments`.
