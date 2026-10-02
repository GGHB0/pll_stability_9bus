# Decisões de formatação deste TCC

A NBR deixa escolha em vários pontos. O que o Victor decidiu para **este**
documento está aqui, com data e motivo.

**Ler antes de propor qualquer mudança de formatação.** Uma "correção" que
contraria uma decisão daqui é regressão, não melhoria. Se um pedido novo
conflitar com uma decisão registrada, **perguntar** — e atualizar este
arquivo quando a resposta mudar a decisão.

Todas as decisões abaixo foram **implementadas na entrega de 2026-09-13**
(ver `kb/tcc-word/docx/abnt_layout.md`).

---

## D1 — Paginação ABNT estrita · 2026-09-12

Contagem contínua a partir da folha de rosto (a capa **não** conta);
número impresso **só a partir da Introdução**, no canto superior direito,
a 2 cm da borda; **sem número no rodapé**.

Implementação: `evenAndOddHeaders` desligado; seção 1 com header e footer
`default` vazios e `pgNumType w:start="0"` na capa; seção 2 com header
`PAGE` e footer vazio **declarado**, sem `pgNumType` (a contagem só
continua). Na entrega de 2026-09-13 (74 folhas) a Introdução é a folha
física 16 e imprime **15**.

**Corrigido em 2026-09-13:** a versão anterior fixava "a Introdução imprime
18". Errava duas vezes: contava a capa, e supunha 17 folhas de pré-texto
que a limpeza do próprio pré-texto encolheu. Nunca fixar número inicial no
corpo: deixar a contagem correr desde a capa.

**Por quê:** três defeitos somados — número repetido no topo e no rodapé
de toda folha par, numeração no pré-texto, e `start="12"` no corpo.

**Recusadas:** numerar o pré-texto em romanos (i, ii, iii) — a NBR 14724
não prevê, e o sumário conviveria com dois sistemas de numeração.

## D2 — Os quatro elementos opcionais do pré-texto ficam · 2026-09-12

Dedicatória e epígrafe **permanecem**: são texto pessoal que os autores
vão escrever. As listas de Quadros e de Gráficos caíram em 2026-09-26 (D9).

**Histórico (superado por D9) — reclassificação de 2026-09-13.** Todas eram
"Figura", e as duas listas ficariam vazias. Pelo conteúdo de cada imagem:

| Tipo | Qtd. | Quais |
|---|---|---|
| Figura | 5 | 3.1 VSI, 3.2 SRF-PLL, 4.1 unifilar, 4.2 inversor, 4.3 laço do PLL |
| Quadro | 1 | 4.1, matriz de cenários (antiga Figura 4.4): texto em linhas e colunas |
| Gráfico | 18 | 2.1-2.3 (curvas ONS e afundamento) e 5.1-5.15 (simulação) |

Critério: curva de grandeza quantitativa é Gráfico, inclusive curva
normativa adaptada. As três do Cap. 2 eram o caso discutível; foi adotada a
recomendação (Gráfico) quando o Victor mandou seguir. Voltar para Figura é
localizado: as 3 legendas do Cap. 2 (rótulo e identificador do `SEQ`).
Custo pago: 23 trechos do corpo reescritos com concordância ("A Figura 5.4
mostra" → "O Gráfico 5.4 mostra").

**A dedicatória não existia no arquivo:** a "folha 4" era sobra de
parágrafos vazios depois da ficha. Criada onde a NBR 14724 manda (depois da
folha de aprovação), com o marcador "Dedicatória opcional.", no padrão da
epígrafe.

## D3 — Listas automáticas por campo `SEQ` · 2026-09-12

As 24 legendas são campo: rótulo e capítulo em texto literal, número em
`SEQ <id> \* ARABIC \s 1`, que reinicia a cada Título 1. Identificadores em
ASCII: desde D9, só `Figura` e `Tabela`. As listas são campos
`TOC \h \z \c "<id>"`, reconstruídas pelo `word_finalize.ps1`.

Com uma lista por tipo, a antiga "LISTA DE ILUSTRAÇÕES" ficou só com
figuras e virou **LISTA DE FIGURAS** (NBR 14724: lista própria para cada
tipo de ilustração).

**Não usar `STYLEREF 1 \s`** para o capítulo: os títulos são "Capítulo N –"
em texto, sem numeração automática, e o campo não teria de onde tirar o N.

**Por quê:** a lista estava com **uma** entrada fictícia. Convertido uma
vez, número e página se atualizam sozinhos.

## D4 — Figura autoral única no lugar dos dois diagramas do SRF-PLL · 2026-09-12

As duas imagens do SRF-PLL, sem legenda e sem fonte, deram lugar à
**Figura 3.2**, autoral e em português
(`assets/diagrams/srf_pll_blocos_funcionais.svg`): o laço agrupado nos três
blocos funcionais que a Seção 3.4 descreve, com os símbolos da Figura 4.3.
Fonte: "Os autores (2026)".

**Por quê:** nenhuma tinha fonte. A primeira tinha como texto alternativo o
**título de outro trabalho acadêmico** ("Análise de SRF-PLL e DSOGI-PLL
Aplicados em um VSC Quatro Fios..."), ou seja, foi copiada sem citação. A
segunda trazia erros de inglês no bitmap: "Phase-Detective", "Low Filter".

**Corrigido em 2026-09-13:** a versão anterior dizia que eram "o mesmo
diagrama duas vezes". Não eram: uma era o diagrama compacto com a
matemática, a outra o funcional em três blocos.

**Por que não repetir a Figura 4.3:** ela é o laço implementado no estudo;
a 3.2 é a leitura teórica em blocos.

## D5 — Títulos mantêm a graduação de tamanho · 2026-09-12

Capítulo 24 pt, seção 18 pt, subseção 14 pt, sub-subseção 12 pt, todos em
Times New Roman negrito.

**Por quê:** a NBR 14724 pede todos os títulos em 12 pt, diferenciados só
por caixa e negrito. O Victor preferiu não mudar a aparência que o
orientador já viu, faltando pouco para a entrega.

**O que se corrigiu apesar disso:** `keepNext` em todos; espaço antes 0 e
depois 18 pt no capítulo; antes e depois 18 pt nos demais níveis. O desvio
autorizado é **só** o tamanho.

**Recusado:** meio-termo 16/14/12/12.

## D6 — Recuo de primeira linha de 1,25 cm · 2026-09-12

Todo parágrafo de corpo com recuo de 1,25 cm (708 twips), justificado e
**sem** espaço extra entre parágrafos. Em 2026-09-13: 160 parágrafos.

**Atenção:** era o padrão **minoritário** no documento. Não inverter por
achar que "o dominante estava certo".

Não recebem recuo: legenda, fonte, citação longa, resumo, entrada de
referência, título, item de lista numerada.

## D7 — Legendas e equações no padrão ABNT completo · 2026-09-12

**Legenda:** acima da ilustração; `Fonte:` abaixo; ambas à **esquerda**,
10 pt, espaçamento simples. **Equação:** `EQUAÇÃO 3.1` vira `(3.1)` à
direita. Vale para as 24 ilustrações e as 23 equações.

**Por quê:** as legendas estavam centralizadas em 12 pt, sem se distinguir
do corpo; o rótulo em caixa alta não é forma prevista na norma.

**Ilustração nova** depois da entrega: montar o trio com
`scripts/campos.py`, que reproduz exatamente esse padrão.

## D8 — Pré-texto e títulos sem indicativo · 2026-09-13

- **Cada elemento pré-textual abre folha** com `pageBreakBefore` no título;
  saíram os parágrafos vazios que empurravam o texto. Enchimento com
  parágrafo vazio é o que produzia folha em branco.
- **Dedicatória e epígrafe** no terço inferior, à direita: parágrafo vazio
  com a quebra, e o texto com espaço-antes no seguinte (o Word ignora
  espaço-antes logo após a quebra).
- **Siglas em espaço simples**: em 1,5 a última caía sozinha numa folha.
  Com 36 siglas (revisão da noite), `after=60`, tab único em 3 cm, recuo
  deslocado de 3 cm e `jc=left`: dois tabs padrão desalinhavam sigla longa
  (SRF-PLL, DDSRF-PLL). Detalhe em `kb/tcc-word/conteudo/siglas_inventory.md`.
- **REFERÊNCIAS e ANEXOS** são `Ttulo1` **centralizados** (NBR 14724:
  título sem indicativo numérico é centralizado) e entram no sumário.
- **Capítulo abre folha** por `pageBreakBefore` no título, nunca por
  parágrafo só com `<w:br w:type="page"/>`, que em folha já cheia deixa uma
  folha em branco. Sem quebra no meio de capítulo.
- **"A ser elaborada pela Biblioteca"** na ficha **não é resíduo**: é a
  instrução real da UERJ e fica até a biblioteca emitir a ficha.

## D9 — Tudo é Figura; o antigo Quadro é Tabela · 2026-09-26

Comentários 3, 4 e 5 do Oscar no V10 ("Porque tem uma lista de Figs e outra
de gráficos?", "Quadros ou tabela?", "Não tem uma lista de tabelas??"). O
Victor mandou fazer como o Oscar pediu.

- **Figura** para toda ilustração: as 18 ex-Gráfico (2.1-2.3, 5.1-5.15)
  mantiveram o número, porque os Caps. 2 e 5 não tinham Figura.
- **Tabela 4.1** para a matriz de cenários (ex-Quadro 4.1).
- Pré-texto: Lista de Figuras (23) e **Lista de Tabelas** (1); a Lista de
  Gráficos foi removida. Remissões com concordância ("A Figura 5.4").

**Ressalva conhecida, aceita:** pelo IBGE (citado pela NBR 14724), texto em
grade sem dado numérico seria quadro. O Victor preferiu seguir o avaliador.
A NBR 14724 só **recomenda** lista por tipo de ilustração, então a lista
única de Figuras está dentro da norma. Não reabrir.

---

## Onde isso não se aplica

- **Fragmento externo** (`Fragmentos/*.docx`) — rascunho de trabalho, sem
  compromisso de forma. Ver `tcc-docx-editor/casos/fragmento_externo.md`.
- **Notas técnicas em PDF** (`output/*.pdf`) — layout próprio, feito com
  reportlab. Ver a skill `tcc-pdf-notes`.
- **Relatório HTML** (`output/pll_metrics.html`) — nada a ver com ABNT.
