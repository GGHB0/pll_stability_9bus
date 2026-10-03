# Skill: tcc-docx-editor

Edita o TCC DOCX (`config.py`; hoje `TCC_Victor_Bruno_V10.docx`) no OOXML.
**Padrões fixos** (Resumo↔Abstract + comentário, fechar/reabrir Word, "Feito." ao Oscar, siglas): `referencia/padroes_revisao.md`.
Modo aceito pelo Victor: **edições diretas no XML, sem tracked changes**
(`helpers.py` mantém os geradores com `w:ins` caso volte a ser necessário).

Pastas: `casos/` (fluxos de uso ocasional: fragmento, mesclagens, revisão de
português), `referencia/` (lido em toda edição: padrões, entrega,
armadilhas), `scripts/`. Guia novo vai na pasta do seu tipo; caminhos são
citados a partir da raiz da skill.

## Fragmento externo (não o canônico) — ver `casos/fragmento_externo.md`

Quando o alvo é um rascunho externo isolado (ex.: `capitulos_4_5_revisados.docx`,
na pasta `Fragmentos/` do TCC no OneDrive, plain-Normal-style, sem tracked
changes/comentários/tabelas), o OOXML-surgery deste arquivo é overkill: usa-se
**python-docx direto**, sem staging, sem `repack.py`, sem IDs a rastrear. Todo
o workflow, as armadilhas (inserção de figura, renumeração, troca de termo,
`docPr` duplicado, conferência de MD5) e as lições de redação estão em
**`casos/fragmento_externo.md`**. Ler antes de tocar num fragmento.

Para levar um fragmento **para dentro** do canônico, ver
**`casos/mesclagem_no_canonico.md`**: comparar as árvores de seção antes de trocar
(o fragmento pode ser mais raso que o capítulo que substitui), mapear os
títulos para `Ttulo1`–`Ttulo4` ou eles somem do sumário, inverter a convenção
de legenda, e **reescalar as figuras da largura útil de origem para a de
destino** (o fragmento é Carta, 6,50 in; o TCC é A4, 6,30 in).

## Cópia comentada externa (Oscar) — ver `casos/mesclagem_comentarios.md`

Cópia do TCC com comentários novos do Oscar (não um rascunho de texto — ver
"Fragmento externo" acima): mesclar só os comentários, sem as edições de
texto soltas que vierem junto. Achar os novos por diff de texto e confirmar
por **data** (não por ID, que o Word renumera) contra o comentário mais
recente já no canônico, para não duplicar o que já foi mesclado com redação
levemente diferente. Detalhe da mesclagem cirúrgica nas 4 partes XML de
comentário em `casos/mesclagem_comentarios.md`.

## Revisão de português — ver `casos/revisao_pt.md`

Passagem linguística separada das edições de conteúdo. `scripts/check_pt.py`
varre o `document.xml` atrás das classes já vistas (regência `capacidade …
em`, `onde` não locativo, `através de`, vírgula entre relativo e verbo,
resíduo de LaTeX, duplo espaço, placeholder, em-dash). **Não** pega
concordância, coesão nem frase sem verbo principal: isso só sai lendo o
`dump_blocks.py` do corpo inteiro. Detalhes e falsos positivos em
`casos/revisao_pt.md`.

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
| **Síntese** | Opus, *só quando necessário* | Redigir conteúdo acadêmico novo, decisões estruturais com trade-offs |
| **Planejamento + scripting** | Sonnet, o default | Mapear blocos, edições rotineiras, escrever os `gen_*.py`, revisar checks, KB |
| **Execução** | Haiku (`docx-runner`) | Staging, dumps, rodar scripts, repack, entrega |

O critério é **custo total**, não o nível do modelo: delegar só compensa
quando a spec sai bem menor que o trabalho que ela descreve.

- **Sessão em Sonnet**: planejamento, conteúdo e scripting direto; só o
  mecânico vai ao `docx-runner`. **Nunca** escalar para Opus por conta
  própria: dizer ao usuário e deixar a troca de modelo com ele.
- **Sessão em Opus**: o Opus interpreta, redige e revisa. Scripting vai ao
  `docx-scripter` (Sonnet) com **spec precisa** (blocos-alvo, old→new com
  counts, conteúdo pronto, IDs e comentários a reancorar) quando a edição é
  **grande ou repetitiva** (renumeração de capítulo, troca de termo em dezenas
  de pontos, muitas figuras): aí a spec é curta e o script, longo.
- **Faz direto, sem agente, em qualquer modelo**: (a) edição trivial, 1-2
  replaces; (b) **texto pronto do Victor, até ~10 parágrafos**: a spec teria
  o tamanho do próprio script (cada parágrafo inteiro, mais comentários a
  reancorar) e o agente ainda reabriria os dumps. Confirmado com o Victor em
  2026-10-02. Staging, finalize e entrega também podem ficar no principal
  nesses casos, pois são 3-4 comandos.

Delegar via Agent tool (`subagent_type: "docx-scripter"` / `"docx-runner"`),
com prompt autocontido: paths exatos, o que rodar e a "saída esperada".

## Dependências

- `config.py` (nesta pasta): paths pessoais (gitignored)
- `helpers.py` (nesta pasta): geradores de parágrafo OOXML com `w:ins`
- `scripts/` (nesta pasta), todos `python.exe <script> <args>`:
  - `dump_headings.py <xml>`: mapa de títulos com índice de bloco
  - `dump_blocks.py <xml> <ini> <fim> [--raw] [--math]`: texto/XML de um
    intervalo; `--math` mostra o conteúdo de cada equação OMML
  - `find_text.py <xml> <padrão> [--regex]`: ocorrências com bloco + contexto
  - `dump_comments.py <docx> [--grep re] [--autor x] [--abertos] [--blocos ini-fim]`:
    comentários com trecho, bloco e respostas; lê com o Word aberto
  - `check_ids.py <xml>`: máximos de bookmark/ins/paraId + dirty do TOC
  - `check_pt.py <xml> [--corpo N]`: varredura de português (`casos/revisao_pt.md`)
  - `repack.py <template.docx> <xml> <saida.docx>`: injeta o document.xml
  - `audit_docx.py <docx> [--util-in N]`: auditoria pré-entrega; código 1 se falhou
  - `word_finalize.ps1 -In <montado> -Out <final> [-Pdf] [-Comments <json>] [-Replies <json>]`:
    passa pelo Word, reconstrói o sumário e **prova que o Word salva**
  - `renumera_figuras.py`: `renumera(doc, cap, a_partir, delta[, 'Tabela'])`
    para as remissões no texto quando entra ilustração no meio do capítulo
  - `entrega.ps1 -Final <final> -Dest <canônico> -Md5Staging <md5>`: passo 9
    inteiro, com aborto (`referencia/entrega.md`)
- Ilustração e tabela nova: `tcc-abnt-layout/scripts/campos.py`
  (`figura_nova`, `tabela_completa`, `legenda`/`imagem`/`fonte`)

## Workflow padrão

```
1. STAGING: OneDrive → C:\Temp\tcc_<tema>\ (ou o padrão de config.py, se
   não houver outra sessão) → extrair word/document.xml; guardar o MD5
2. INSPEÇÃO: dump_headings / dump_blocks (--math onde houver equação) /
   find_text / check_ids. O estado real é o do XML recém-extraído
3. MAPA DE COMENTÁRIOS: dump_comments.py --blocos <ini>-<fim> do trecho.
   Para cada comentário: âncora some com a edição? (reancorar no texto
   novo equivalente) · a edição o atende? (vai receber "Feito.")
4. CONFERÊNCIA TÉCNICA: toda remissão do texto novo (equação, figura,
   seção, sigla) contra o conteúdo real; termo com sigla que entra ou sai
   → conferir a lista de siglas (referencia/padroes_revisao.md §7)
5. PLANO (principal): blocos, texto, tabela de comentários (id curto,
   pedido, atendido?, Feito?), correções técnicas. 3+ valores por cenário
   no texto → propor Tabela (D11). AGUARDAR APROVAÇÃO
6. SCRIPT: C:\Temp\gen_<tema>.py com counts verificados, comentários
   reancorados (Start/End/Reference = 1 cada), ET.fromstring, grava saída
   (quem escreve: ver "Divisão de trabalho")
7. REVISÃO: dump_blocks da saída + check_pt
8. FINALIZAÇÃO: repack → word_finalize.ps1 -Replies <json com os Feito.>
   → audit_docx.py (0 falhas) → conferir o delta de "Feito." no comments.xml
9. ENTREGA: scripts/entrega.ps1 (referencia/entrega.md)
10. KB: historico_entregas / content_map / pendencias / siglas, conforme o caso
```

Passos 3 e 4 entraram em 2026-10-02: na entrega daquele dia o "Feito." foi
esquecido (o padrão existia, mas fora do workflow) e o texto pedido trocava
o papel das equações (3.5)-(3.7).

## Entrega e armadilhas

- `referencia/entrega.md`: checklist, MD5 que muda antes/depois, sessões em paralelo.
- `referencia/armadilhas.md`: ambiente, IDs e comentários, contagens e buscas, conteúdo.
- KB: `.claude/kb/tcc-word/docx/docx_structure.md` (registro de IDs e
  armadilhas XML) e `historico_entregas.md`.
