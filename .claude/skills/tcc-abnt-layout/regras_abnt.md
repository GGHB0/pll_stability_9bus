# Regras ABNT aplicáveis ao TCC

Referência normativa de consulta. Cada regra traz a NBR que a sustenta e,
quando este documento se afasta dela de propósito, a marca **[desvio]**
apontando para `decisoes.md`.

> As NBR não foram lidas em PDF neste projeto — as regras abaixo vêm da
> prática editorial consolidada e do template UERJ. Onde houver dúvida
> sobre o texto literal da norma, **confirmar com o Oscar** antes de tratar
> como obrigatório.

## Papel, margens e fonte — NBR 14724

| Item | Regra | Estado no documento |
|---|---|---|
| Formato | A4 (21,0 × 29,7 cm) | ✅ `pgSz` 11907 × 16840 twips |
| Margem superior | 3,0 cm | ✅ `w:top="1701"` |
| Margem esquerda | 3,0 cm | ✅ `w:left="1701"` |
| Margem inferior | 2,0 cm | ✅ `w:bottom="1134"` |
| Margem direita | 2,0 cm | ✅ `w:right="1134"` |
| Fonte do texto | única no trabalho, 12 pt | ✅ Times New Roman 12 pt |
| Entrelinhas do texto | 1,5 | ✅ `w:line="360" w:lineRule="auto"` |
| Entrelinhas de legenda, nota, citação longa, ficha | simples | ✅ legenda, `Fonte:`, siglas e referências (2026-09-13) |

Área útil resultante: **16,0 cm** de largura (6,30 in). É o valor que o
`audit_docx.py --util-in 6.30` usa para acusar imagem estourando a margem.

## Paginação — NBR 14724

- **Todas** as folhas a partir da folha de rosto são **contadas**.
- O número só é **impresso** a partir da primeira folha textual (a
  Introdução).
- Posição: canto **superior direito**, a 2 cm da borda superior, em
  algarismos arábicos.
- A capa não é contada.
- Apêndice e anexo continuam a sequência do texto.

Consequência prática: a Introdução imprime o número de folhas
pré-textuais **sem a capa**, mais um. Neste documento ela é a folha física
16 e imprime **15** (D1), nunca 1 nem um `start` fixo. Contagem e número
impresso têm de coincidir.

**Nunca** repetir o número no rodapé. Um número por folha.

## Ordem dos elementos — NBR 14724

```
PRÉ-TEXTUAIS      capa (obrigatório, não conta)
                  folha de rosto (obrigatório, conta a partir daqui)
                  ficha catalográfica (verso da folha de rosto)
                  errata (opcional)
                  folha de aprovação (obrigatório)
                  dedicatória (opcional)
                  agradecimentos (opcional)
                  epígrafe (opcional)
                  resumo em português (obrigatório)
                  resumo em língua estrangeira (obrigatório)
                  listas de ilustrações / tabelas / abreviaturas / símbolos (opcionais)
                  sumário (obrigatório)
TEXTUAIS          introdução, desenvolvimento, conclusão
PÓS-TEXTUAIS      referências (obrigatório)
                  glossário, apêndice, anexo, índice (opcionais)
```

**Cada elemento começa em folha nova.** É a regra que mais quebra na
prática: basta o texto anterior encolher para dois elementos dividirem a
mesma folha.

Elemento opcional que fica no documento precisa ter conteúdo. Lista de
ilustrações vazia é pior que lista ausente — **ver `decisoes.md` D2**, que
mantém quatro elementos opcionais por decisão do autor.

## Numeração progressiva das seções — NBR 6024

- Algarismos arábicos, alinhados à **esquerda**, sem recuo.
- O indicativo é separado do título por **um espaço**, sem ponto, travessão
  ou parêntese depois do último número.
- Até a quinta seção (`4.3.2.1.1`); abaixo disso, usar alínea.
- Títulos sem indicativo (resumo, sumário, referências, anexo) ficam
  **centralizados**.
- Elementos textuais de mesmo nível usam o mesmo recurso tipográfico.

**[desvio]** Este documento usa `2.1.` com ponto final no indicativo e
tamanhos graduados de 24/18/14/12 pt — ver `decisoes.md` D5.

## Ilustrações — NBR 14724

Toda ilustração (figura, gráfico, quadro, desenho, fotografia, esquema) leva:

1. **Acima**: a palavra designativa, o número de ordem em arábico e o
   título. Sem ponto final.
2. **A ilustração**, centralizada, dentro da área útil.
3. **Abaixo**: a fonte consultada — **obrigatória mesmo quando é do
   próprio autor** —, mais legenda e nota, se houver.

Legenda, fonte e nota em **fonte menor** (10 pt) e **espaçamento simples**.

O trio legenda + ilustração + fonte não pode ser dividido por quebra de
página. No Word isso é `keepNext` na legenda **e** na imagem.

Numeração: sequencial por tipo, ao longo do documento inteiro ou por
capítulo (`Figura 5.1`). Uma vez escolhido, vale para todas.

Neste documento: por capítulo, com campo `SEQ` e uma lista por tipo (D3),
legenda à esquerda (D7). Ilustração nova sai de `scripts/campos.py`.

## Tabelas — IBGE, citado pela NBR 14724

Regra diferente da de figura, e a troca é erro comum:

- Título **acima**, fonte **abaixo**.
- Sem fechamento lateral: as bordas da esquerda e da direita ficam abertas.
- Tabela apresenta **dado numérico** como informação central. Se o
  conteúdo é texto ou o dado é acessório, é **quadro**, e quadro é fechado
  dos quatro lados.

Neste documento as 23 `<w:tbl>` são **tabelas de diagramação de equação**,
sem borda e sem título — não são tabelas no sentido da norma e não entram
em lista nenhuma.

## Equações — NBR 14724

- Destacadas do parágrafo, em linha própria.
- Numeradas em **arábicos entre parênteses**, alinhados à **margem
  direita**: `(3.11)`.
- Permitido reduzir entrelinha e corpo de expoentes e índices.
- No texto, referenciar como "Equação (3.11)".

## Citações — NBR 10520

- Até 3 linhas: no corpo, entre **aspas duplas**.
- Mais de 3 linhas: parágrafo próprio, recuo de **4 cm** da margem
  esquerda, fonte **10 pt**, **espaçamento simples**, **sem aspas**.
- Sistema autor-data: `(SOBRENOME, ano)` ou `Sobrenome (ano)`.
- Citação de citação: `apud`.
- Três autores ou mais: `(SOBRENOME et al., ano)`.

## Resumo — NBR 6028

- Parágrafo **único**, sem recuo de primeira linha, espaçamento simples.
- Verbo na **voz ativa** e na terceira pessoa do singular.
- 150 a 500 palavras para trabalho acadêmico.
- Logo abaixo, **palavras-chave** separadas por **ponto**, iniciando por
  maiúscula: `Palavras-chave: SRF-PLL. Sincronismo. Inversores.`
- A referência do próprio trabalho, quando presente no topo, usa o número
  de folhas seguido de `f.`

## Sumário — NBR 6027

- **Último** elemento pré-textual.
- Reproduz os títulos **exatamente** como aparecem no texto, na mesma
  ordem e com os mesmos recursos tipográficos.
- Elementos pré-textuais **não** entram no sumário.
- Referências, glossário, apêndice e anexo **entram**.
- Numeração das folhas à direita, ligada por linha pontilhada.

Por isso o sumário é sempre o **último** item a acertar: qualquer mexida
de paginação anterior o invalida.

## Referências — NBR 6023

- Lista **alfabética** por sobrenome, no fim do trabalho.
- Alinhamento à **esquerda** (não justificado), espaçamento simples,
  separadas entre si por **uma linha em branco**.
- Título `REFERÊNCIAS` centralizado, sem indicativo numérico.
- Sobrenome em caixa alta, prenome abreviado ou por extenso — **um padrão
  só** no trabalho inteiro.
- Título da obra em **negrito**; subtítulo sem destaque.
- Toda entrada da lista precisa ser citada no corpo, e toda citação do
  corpo precisa de entrada na lista. Órfã dos dois lados é erro.
