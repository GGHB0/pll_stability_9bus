---
name: tcc-abnt-layout-estado
aliases: [tcc-abnt-layout-estado]
description: Estado da formatação ABNT e da paginação do TCC DOCX canônico — diagnóstico de 2026-09-12, passagem completa entregue em 2026-09-13, o que ainda está aberto
source: TCC_Victor_Bruno_V9_novo_indice_2.docx (antes MD5 91c13b5c…, 79 folhas; depois MD5 17de36b4…, 74 folhas)
references:
  - "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 14724: informação e documentação: trabalhos acadêmicos: apresentação. Rio de Janeiro: ABNT, 2011. (edição a confirmar)"
  - "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 6023: informação e documentação: referências: elaboração. Rio de Janeiro: ABNT, 2018. (edição a confirmar)"
  - "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 6024: informação e documentação: numeração progressiva das seções de um documento: apresentação. Rio de Janeiro: ABNT, 2012. (edição a confirmar)"
  - "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 6027: informação e documentação: sumário: apresentação. Rio de Janeiro: ABNT, 2012. (edição a confirmar)"
  - "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 6028: informação e documentação: resumo, resenha e recensão: apresentação. Rio de Janeiro: ABNT, 2021. (edição a confirmar)"
---

# Estado ABNT do TCC DOCX

Diagnóstico em **2026-09-12** sobre o canônico de 79 folhas; passagem
completa entregue em **2026-09-13**. O documento tem hoje **74 folhas**.

> As NBR não foram extraídas em PDF neste projeto. As regras aplicadas vêm
> da prática editorial consolidada e do template UERJ, e as entradas de
> `references:` estão com a **edição a confirmar**. Conferir com o Oscar
> antes de tratar qualquer item como obrigatório.

Decisões de forma (D1-D8): `.claude/skills/tcc-abnt-layout/decisoes.md`.
Regras: `regras_abnt.md` da mesma skill. Gerador da passagem:
`C:\Temp\abnt_work\gen_abnt.py` (fora do repo, índices de parágrafo do
documento daquela data). O que se reaproveita foi para a skill:
`scripts/ppr.py` (edição de `pPr`) e `scripts/campos.py` (legenda com
`SEQ`, imagem e `Fonte:` de ilustração nova).

## Resultado medido

| Conferência | Antes (09-12) | Depois (09-13) |
|---|---|---|
| `check_abnt.py` | 7 falhas | **0 falhas**; 3 avisos (dedicatória e epígrafe a escrever; footer `even` ausente, sem efeito com even/odd desligado) |
| `pagecheck.py` | 4 grupos | **1 grupo**: ANEXOS sem conteúdo na última folha |
| `audit_docx.py` | 0 falhas | 0 falhas |
| `word_finalize.ps1` | — | 74 páginas, 0 campo com erro, salvou |
| `keepNext` | 0 | 97 |
| Legendas com `SEQ` | 0 de 21 | 24 de 24 |

## O que já estava conforme

| Item | Valor |
|---|---|
| Formato | A4, `pgSz` 11907 × 16840 twips |
| Margens | 3,0 / 3,0 / 2,0 / 2,0 cm (`w:top/left` 1701, `w:bottom/right` 1134) |
| Área útil | 16,0 cm = 6,30 in (é o `--util-in` do `audit_docx.py`) |
| Fonte do corpo | Times New Roman 12 pt, entrelinhas 1,5 |
| Estilos de título | uniformes dentro de cada nível |
| Tabelas | as 23 `<w:tbl>` são diagramação de equação; não há tabela de dados, nem LISTA DE TABELAS |

## O que foi corrigido em 2026-09-13

### Paginação (D1)

**Causa raiz:** `evenAndOddHeaders` ligado em `settings.xml` (global) e a
seção 2 sem nenhum `footerReference`, herdando o `footer1` numerado da
seção 1 nas folhas pares; mais `start="12"` no corpo.

**Agora:** even/odd desligado; seção 1 com header/footer vazios e
`start="0"` na capa; seção 2 com header `PAGE` e footer vazio declarado,
contagem contínua; `w:header="1134"` (2 cm). A Introdução é a folha 16 e
imprime 15; a última folha imprime 73.

### Quebras

- `keepNext` em 24 legendas e 24 imagens: as 9 quebras legenda/imagem/fonte
  do diagnóstico foram a zero.
- Capítulos abrem por `pageBreakBefore` no título. O parágrafo antigo só
  com `<w:br>` gerava uma folha em branco inteira no fim do Cap. 5.
- Quebras no meio de capítulo removidas (antes de "Motivação e
  Justificativa", de 2.5.3 e de 3.1).

### Ilustrações (D2, D3, D4, D7)

- 24 ilustrações: **5 Figuras, 18 Gráficos, 1 Quadro**, numeradas por
  capítulo com `SEQ`; três listas automáticas.
- Caps. 2 e 3: os 4 textos entre colchetes eram as legendas (imagem já
  presente). Viraram Gráficos 2.1-2.3 e Figura 3.1. Fontes: as duas ONS
  já tinham "Adaptado de ONS (2022)"; o afundamento e o VSI são SVGs do
  projeto (`voltage_sag_profile.svg`, `vsi_grid_schematic.svg`), então
  "Os autores (2026)".
- SRF-PLL: Figura 3.2 autoral (D4). A imagem antiga foi copiada de outro
  trabalho acadêmico, sem citação.
- Remissões do Cap. 5 e do Quadro 4.1 reescritas com concordância.
- **2026-09-26 (D9, pedido do Oscar):** tudo virou Figura (23) e o Quadro
  virou Tabela 4.1; Lista de Gráficos removida, Lista de Quadros → Lista de
  Tabelas; numeração inalterada. Documento com 75 folhas, resumo `75 f.`

### Corpo (D5, D6)

160 parágrafos com recuo de 1,25 cm, justificados e sem espaço entre
parágrafos; títulos com `keepNext` e espaçamento uniforme; 23 rótulos de
equação em `(3.1)`.

### Pré-texto e seções finais (D8)

Cada elemento abre folha; ~140 parágrafos vazios de enchimento removidos;
dedicatória criada (não existia) e epígrafe no terço inferior; siglas em
espaço simples; REFERÊNCIAS vira `Ttulo1` centralizado (entra no sumário),
entradas à esquerda em espaço simples; ANEXOS centralizado; `XXf.` e ano
2025 do resumo → `74 f.` e 2026.

## O que continua aberto

- **ANEXOS sem conteúdo** — título sozinho na última folha e no sumário.
- **Dedicatória e epígrafe** — marcadores à espera do texto dos autores.
- **`75 f.`** (desde 2026-09-26) — confirmar com o Oscar se conta o total de folhas ou a
  última numerada (73); atualizar se o documento mudar de tamanho.
- **Subseções do Cap. 1** são itens de lista numerada ("1. Contextualização"),
  não `Ttulo2`: ficam fora do sumário e fogem da NBR 6024 ("1.1").
- **Título gravado dentro da imagem** em pelo menos Figura 3.1, Figura 4.3,
  Tabela 4.1 e Figura 2.3, repetindo a legenda.

## Como reconferir

```bash
# estatico, sobre o XML extraido (settings.xml precisa ir junto)
python.exe .claude/skills/tcc-abnt-layout/scripts/check_abnt.py <dir>/word/document.xml

# sobre o PDF exportado pelo word_finalize.ps1 -Pdf
python.exe .claude/skills/tcc-abnt-layout/scripts/pagecheck.py C:\Temp\tcc_check.pdf
```

## Relacionados

- [[tcc-docx-structure]] — padrões e convenções XML subjacentes
- [[tcc-docx-content-map]] — mapa estrutural do documento que precisa estar conforme
