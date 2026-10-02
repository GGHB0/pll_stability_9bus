# Padrões de revisão do canônico (definidos pelo Victor em 2026-09-26)

Valem para qualquer edição de conteúdo no canônico, sem perguntar de novo.

## 1. Resumo ↔ Abstract andam juntos

O comentário do Oscar no Abstract pede que tudo que mudar no Resumo mude
também no Abstract. Toda edição aprovada no Resumo é **espelhada no Abstract
na mesma entrega**, sem esperar o Victor aprovar a tradução no chat.

- A tradução vai direto para o texto, e o trecho recebe um **comentário curto
  no Word** dizendo o que foi feito e que a tradução espera o ok dele. Quem
  aprova é o Victor, no próprio Word.
- O comentário é criado pelo Word, com `word_finalize.ps1 -Comments <json>`:
  `[{"anchor": "<trecho exato, ≤ 255 caracteres, 1 ocorrência>", "text": "..."}]`.
  O script prefixa `[Claude]` no texto, porque o Word ignora
  `Application.UserName` e grava o autor como a conta logada no Office.
- **Nunca montar comentário à mão no OOXML**: ele mexe em 4 partes do pacote
  (`comments`, `commentsIds`, `commentsExtended`, `commentsExtensible`).
- Mesma lógica para qualquer texto que o Victor ainda não viu (ex.: frase de
  ligação que a edição exigiu): entra no texto com comentário curto, e não
  como pergunta no chat.

## 2. Resumo apresenta, não conclui

O Resumo diz o que o trabalho trata; resultado, número e desfecho de cenário
ficam no Cap. 5 e na Conclusão. Uma primeira versão com o desfecho da
sintonia inadequada ("perde o sincronismo e não o recupera") foi recusada.
Ver `feedback_tcc_conclusion_altitude` na memória, que vai no sentido oposto
(a Conclusão sobe de altitude; o Resumo fica na de abertura).

## 3. Word aberto: fechar, executar, reabrir

Regra do Victor: **eu fecho o Word, executo e abro de novo**, sempre, sem
perguntar. Vale para qualquer passo que precise do Word fechado (a
finalização e a entrega).

1. Via COM: `[Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")`,
   anotar o `FullName` de cada documento, `Save()` nos que tiverem
   `Saved = $false` e depois `Quit()`. Se o `GetActiveObject` falhar
   (`MK_E_UNAVAILABLE`) e `Get-Process winword` ainda listar o processo,
   usar `(Get-Process winword).CloseMainWindow()` (fechamento normal) e
   esperar sair. Sem documento anotado, reabrir pelo menos o canônico.
   **Nunca** `Stop-Process`, que perde trabalho não salvo.
2. Salvar pelo Word muda o MD5 do canônico: o pré-check da entrega acusa, e a
   edição é refeita sobre a versão nova. É o comportamento certo, não um erro.
3. Depois da entrega, reabrir o canônico (e o que estava aberto) com
   `Start-Process "<path>"`.

## 4. Canônico atual

`TCC_Victor_Bruno_V10.docx` (desde 2026-09-26; o `_2` saiu da pasta). A fonte
da verdade é `config.py`. Se o arquivo de `config.py` sumir, listar a pasta,
propor o mais recente e **confirmar com o Victor** antes de editar.

## 5. Comentário do Oscar atendido: responder "Feito." na thread

Definido pelo Victor em 2026-09-26. Quando uma edição atende a um comentário
do Oscar, a entrega **responde dentro da thread** daquele comentário com
`Feito.`, sem marcar como resolvido e sem explicar a mudança (o Oscar confere
no texto).

- Pelo Word: `word_finalize.ps1 -Replies <json>`, com
  `[{"match": "<início do texto do comentário do Oscar>", "text": "Feito."}]`.
  O `match` tem que casar exatamente um comentário de nível superior; o
  script aborta se casar zero ou mais de um.
- Sem prefixo `[Claude]`: a resposta sai pela conta do Victor no Office, e é
  ele quem responde ao Oscar. O prefixo continua só nos comentários do item 1.
- Casar pelo texto, nunca pelo ID: o Word renumera os IDs ao salvar.
- Conferir depois no `commentsExtended.xml` que cada `Feito.` tem
  `paraIdParent` apontando para o comentário certo.

## 6. O texto que apresenta a figura vem antes dela

Definido pelo Victor em 2026-10-01. O parágrafo "A Figura X mostra…" fica
**acima** da legenda, nunca depois do "Fonte". Figuras lidas lado a lado
(ex.: nominal × inadequada) têm um texto só, acima do par. Parágrafos de
análise que não apresentam a figura continuam onde estão. Ilustração nova
entra já assim; ao mover, levar o `w:p` inteiro (as âncoras de comentário
precisam abrir e fechar no mesmo parágrafo).
