# Decisões de formatação deste TCC (continuação)

Continuação de `decisoes.md` (D1-D10, limite de 200 linhas). Mesmas regras:
ler antes de propor mudança de formatação; pedido que conflite com uma
decisão daqui → perguntar.

---

## D11 — Tabela Word real, estilo IBGE · 2026-10-03

Nos comentários do Oscar após a Figura 5.8, o Victor achou que "nosso
relatório carece de tabelas" e que muito número no texto atrapalha. Entraram
as Tabelas 5.1-5.3, aprovadas como estão:

- **Tabela Word** (`<w:tbl>`), não imagem: o número é selecionável e a
  tabela entra na Lista de Tabelas pelo `SEQ Tabela` da legenda.
- **IBGE**: título acima, `Fonte:` abaixo, **sem bordas laterais nem
  internas**; filete acima e abaixo do cabeçalho e abaixo da última linha.
- 10 pt, espaçamento simples, largura útil inteira (9072 dxa), centralizada;
  primeira coluna (rótulo) à esquerda, valores centralizados, unidade no
  cabeçalho ("Pico do erro de fase (°)"), vírgula decimal.
- Cabeçalho repete se a tabela quebrar (`tblHeader`), linha não se parte
  (`cantSplit`) e **todas** as linhas levam `keepNext`, inclusive a última,
  para o `Fonte:` não descolar da tabela.
- "Os autores (2026)." como fonte (dado de simulação, D10).
- Texto **antes** da tabela ("A Tabela 5.1 reúne…"), e o parágrafo fica com
  os extremos e a leitura; a sequência de valores sai do texto.

Implementação: `scripts/campos.py`, `tabela_completa()`. Primeira coluna
estreita quebra o rótulo ("Bifásica na Barra 7"): conferir no PDF do
`word_finalize.ps1` e redistribuir as larguras.

Quando propor: 3 ou mais valores por cenário num parágrafo de resultados.
