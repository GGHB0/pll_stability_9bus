---
name: tcc-abnt-layout
description: Confere e corrige a formatação ABNT e a paginação do TCC DOCX — numeração de páginas, quebras entre legenda e figura, legendas/fontes, recuo de parágrafo, títulos, listas pré-textuais, numeração de equações. Ativar quando o usuário pedir para "ajustar página", "deixar nas normas da ABNT", "conferir paginação/layout/formatação", "figura separada da legenda", "arrumar o pré-texto", ou reclamar que "o número da página está errado/repetido". Não redige conteúdo — para isso, ver tcc-docx-editor.
version: 1.1.0
---

# TCC ABNT Layout — Formatação e Paginação

Passagem de **forma**, não de conteúdo. Responde a "está nas normas?" e
"a página quebrou no lugar certo?". O texto em si é escopo do
`tcc-docx-editor`.

**Esta skill não tem pipeline próprio.** Staging, `repack.py`,
`word_finalize.ps1`, `audit_docx.py` e a entrega ao OneDrive são todos do
`tcc-docx-editor` — inclusive o pré-check por MD5 e o backup datado. Aqui
entram só as **regras** (`regras_abnt.md`), as **decisões já tomadas neste
documento** (`decisoes.md`) e os **dois verificadores** abaixo.

## Os dois verificadores

| Script | Lê | Pega |
|---|---|---|
| `scripts/check_abnt.py <document.xml>` | o XML, sem Word | numeração de páginas (seções, `pgNumType`, header/footer even-odd), `keepNext` ausente em legenda/imagem, legenda e `Fonte:` fora do padrão, recuo de parágrafo inconsistente, estilo de título, placeholders de template, rótulo de equação |
| `scripts/pagecheck.py <arquivo.pdf>` | o PDF exportado pelo Word | o que só existe depois de paginado: página em branco, legenda numa folha e imagem na seguinte, `Fonte:` órfã, título no pé da página, lista pré-textual vazia |

`check_abnt.py` é barato e roda a qualquer momento. `pagecheck.py` exige o
PDF, que sai do `word_finalize.ps1 -Pdf` do `tcc-docx-editor`:

```bash
powershell -ExecutionPolicy Bypass -File <tcc-docx-editor>/scripts/word_finalize.ps1 \
  -In C:\Temp\tcc_edit.docx -Out C:\Temp\tcc_check.docx -Pdf C:\Temp\tcc_check.pdf
python.exe scripts/pagecheck.py C:\Temp\tcc_check.pdf
```

Os dois são **read-only**. Nenhum deles altera o documento. Cada um é uma
CLI fina sobre um módulo de conferências ao lado (`checks_xml.py`,
`checks_pdf.py`) — a regra de 200 linhas por arquivo vale para script
também. Conferência nova entra no módulo, não na CLI.

## Por que o PDF é indispensável

Metade dos defeitos de paginação **não existe no XML**. `keepNext` ausente
só vira problema quando a legenda calha de cair no pé de uma folha; um
número de página duplicado só aparece quando o Word resolve a herança de
cabeçalho entre seções. Auditar só o `document.xml` dá falso "tudo certo".

A recíproca também vale: o PDF não diz **por que** quebrou. O fluxo é
sempre `pagecheck.py` para achar → `check_abnt.py` para explicar.

## Ordem de ataque

Corrigir fora de ordem obriga a refazer. A sequência que funciona:

1. **Numeração de páginas** (`sectPr`, `pgNumType`, header/footer) — muda
   todos os números do sumário de uma vez; qualquer conferência de página
   feita antes disso vira lixo.
2. **`keepNext` em legenda + imagem** — fecha as quebras entre legenda e
   figura e **altera a paginação**, então vem antes de qualquer lista.
3. **Recuo, espaçamento e estilo de título** — também mexem na paginação.
4. **Legendas e `Fonte:`** no padrão, com campo `SEQ` se a lista for
   automática.
5. **Pré-texto** (dedicatória, epígrafe, listas, resumo).
6. **Listas de ilustrações/quadros/gráficos e sumário** — por último,
   porque só aí os números de página param de mudar.
7. **Reexportar o PDF e rodar `pagecheck.py` de novo.** A correção de uma
   quebra empurra o texto e pode criar outra adiante.

O passo 7 não é opcional. Em documento com muita figura, uma rodada só
não converge.

## Decisões deste documento — ver `decisoes.md`

A NBR deixa escolha em vários pontos (tamanho de título, recuo,
alinhamento de legenda). O que o Victor decidiu para **este** TCC está em
`decisoes.md` (D1-D10) e `decisoes_2.md` (D11 em diante), com a data e o motivo. **Ler antes de propor qualquer
mudança de formatação**: uma "correção" que contraria uma decisão
registrada é regressão, não melhoria.

Se o pedido novo conflitar com uma decisão de lá, perguntar — não decidir
sozinho, e atualizar o arquivo quando a decisão mudar.

## Regras normativas — ver `regras_abnt.md`

Margens, paginação, ordem dos elementos pré-textuais, legenda de
ilustração, numeração progressiva, equações, citação longa, resumo. Cada
regra com a NBR e o item que a sustenta, e a marca de quando este
documento se afasta dela de propósito.

## Divisão de trabalho por modelo

Mesma lógica do `tcc-docx-editor`:

- **Opus** — só para decisão de formatação com trade-off (mudar escala de
  título, reclassificar figura em quadro/gráfico) e para redigir legenda
  que não existe.
- **Sonnet** (default) — rodar os verificadores, ler a saída, mapear
  blocos, escrever os `gen_*.py`.
- **Haiku** (`docx-runner`) — staging, repack, finalize, entrega.

## Ilustração ou equação nova depois da passagem

O documento já está no padrão (entrega de 2026-09-13). Conteúdo novo entra
nele, senão a próxima passagem tem de desfazer:

- **Ilustração**: trio `legenda()` + `imagem()` + `fonte()` de
  `scripts/campos.py`. Tipo por D9: toda ilustração é **Figura** (esquema
  ou curva); grade de texto/dados é **Tabela**. Não existe mais Gráfico nem
  Quadro. PNG ainda fora do pacote: `figura_nova()`. Tabela de dados:
  `tabela_completa()`, estilo IBGE (D11). O número passado é só o cache; o `word_finalize.ps1` renumera e
  reconstrói as listas.
- **Remissão** concorda com o tipo ("a Figura 5.16", "a Tabela 4.1").
  Inserir no meio do capítulo desloca as seguintes: varrer com `find_text.py`.
- **Equação**: rótulo `(N.M)` na coluna direita da tabela invisível
  (`kb/tcc-word/docx/equacoes.md`), nunca `EQUAÇÃO N.M`.
- **Parágrafo de corpo**: recuo 708, justificado, sem espaço antes e
  depois (D6), via `ppr_edit`.
- **Documento mudou de tamanho**: atualizar o `74 f.` da referência do resumo.
- Fechar com `check_abnt.py` e `pagecheck.py`, como na passagem.

## Armadilhas desta passagem

- **`keepNext` em legenda **e** imagem.** Antes da passagem eram zero
  ocorrências; hoje são 97. A legenda segura a imagem, a imagem segura o
  `Fonte:`. Ilustração nova sem os dois volta a quebrar entre folhas.
- **Um `sectPr` sem `footerReference` herda o da seção anterior.** Foi
  isso que produziu número no topo e no rodapé em toda página par. Não
  basta limpar a seção 1: a seção seguinte precisa declarar o próprio
  rodapé, mesmo que vazio.
- **`evenAndOddHeaders` é global** (`settings.xml`), não por seção. Com
  ele ligado, toda seção precisa dos quatro pares header/footer
  even+default, ou herda o que sobrou.
- **Legenda como texto corrido não gera lista automática.** Sem campo
  `SEQ`, a ilustração some da lista do seu tipo. Montar por
  `scripts/campos.py`.
- **Contar folha ≠ número impresso.** Depois de um `pgNumType w:start`, o
  número da folha e o número impresso divergem. Em relatório para o
  usuário, **sempre dizer qual dos dois** está sendo citado; o padrão
  aqui é "folha" = posição física no PDF.
- **O sumário e as listas se reconstroem sozinhos** no `word_finalize.ps1`
  (duas voltas, porque a lista pode crescer e empurrar o sumário). Nunca
  editar número de página de entrada à mão.
- **Editar `pPr` sempre por `scripts/ppr.py`.** O schema tem ordem de
  filhos, e a regex plana de parágrafo engole o `<w:p .../>` auto-fechado
  junto com o seguinte: editar esse span sem tratar o prefixo deixou uma
  tag aberta em 2026-09-13 e o XML não parseou.
- **O Word ignora espaço-antes logo depois de `pageBreakBefore`.** Para
  levar dedicatória e epígrafe ao pé da folha, a quebra vai num parágrafo
  vazio e o espaço no parágrafo seguinte.
- **Parágrafo só com `<w:br w:type="page"/>` gera folha em branco** quando
  cai numa folha que já acabou cheia. Capítulo abre por `pageBreakBefore`
  no título.
- **O heredoc do Bash neste ambiente reduz barra dupla a simples.** Gerador
  com regex ou instrução de campo (`SEQ Figura \* ARABIC \s 1`) vai para
  arquivo pela ferramenta Write, nunca por `cat <<EOF`.
- **Olhar o PDF renderizado, não só o `pagecheck.py`.** Ele não viu a
  dedicatória no topo nem os parágrafos sem justificar; o render viu.
- As armadilhas gerais de OOXML (`ET.write` que corrompe, `proofErr`,
  `sectPr` por `rindex`) continuam valendo — `kb/tcc-word/docx/armadilhas_xml.md`.

## KB

Estado ABNT do documento e histórico das passagens de formatação:
`kb/tcc-word/docx/abnt_layout.md`. Atualizar junto com a entrega, como manda
`feedback_document_everything`.
