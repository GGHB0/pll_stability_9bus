# Revisão de português do TCC

Passagem de revisão linguística sobre o canônico, separada das edições de
conteúdo. Rodada completa em 2026-09-12 (38 edições, ver
`historico_entregas.md`). Este arquivo registra o que a varredura pega, o que
ela **não** pega e como decidir cada classe.

## Ferramenta

```
python.exe scripts/check_pt.py C:\Temp\doc_tcc_edit.xml --corpo 384
```

`--corpo N` ignora o pré-textual (capa, folha de rosto, listas, sumário), que é
cheio de resto de template e afoga o resultado. O `N` muda a cada
reestruturação: pegar o índice do bloco "Capítulo 1" no `dump_headings.py`.

O script **não corrige nada** e não substitui a leitura. Ele mira as classes que
já apareceram de fato neste documento; concordância verbal e nominal, coesão e
frase sem verbo principal **não são detectáveis por regex** e só saem lendo o
`dump_blocks.py` do corpo inteiro de ponta a ponta.

## O que é erro e o que é falso positivo

| Classe | Decidir assim |
|---|---|
| `capacidade … EM + infinitivo` | sempre erro: a regência é `de`. "capacidade do inversor **de** atender" |
| `implicar EM` | sempre erro: é transitivo direto. "implicando **uma** redução" |
| `onde` | erro quando o antecedente não é lugar físico ("no SIN, onde o desempenho…" → "no qual"). Barra e ponto de aplicação de falta **são** lugar, ficam |
| `através de` | trocar por "por meio de" quando não houver travessia física |
| `Diferente de` no início de período | erro: o adverbial é "Diferentemente de". Mas "valor diferente de zero" é adjetivo, fica |
| vírgula entre relativo e verbo | erro ("referência que, convertem"). Falso positivo quando há par de vírgulas intercalando aposto ("que, aliada às economias de escala, tornou") |
| resíduo de LaTeX (`$d$`) | sempre erro; veio de rascunho colado de outro editor |
| duplo espaço | sempre; costuma marcar parágrafos que foram **fundidos** num só (ver abaixo) |
| separador de milhar com espaço | padronizar em ponto (`105.820`), que é o que o resto do texto usa |
| placeholder (`[A CONFIRMAR]`, `[INSERIR FIGURA]`) | **não é erro de português, é pendência**: listar para o usuário, nunca preencher por conta própria |

## O que só sai lendo

- **Frase sem verbo principal.** Apareceu duas vezes, sempre em parágrafo de
  abertura de seção reescrito pela metade: "A Transformada de Park, aplicando
  uma rotação ao sistema αβ." e "Apresentar os conceitos relacionados…".
- **Parágrafo fundido.** Um `<w:p>` só carregando quatro parágrafos, colados por
  duplo espaço em vez de quebra (bloco 451 na rodada de 2026-09-12). O duplo
  espaço denuncia; a decisão de separar em quatro `<w:p>` é do usuário, porque
  mexe na paginação.
- **Divergência factual entre capítulos.** O Cap. 1 dava 22.547 MW/31% para o
  evento de 2023 e o Cap. 2 dava 23.368 MW/34,5%. Regex nenhuma pega isso:
  **conferir todo número repetido contra a KB** (`kb/events/`, `params.m`).
- **Citação fora do padrão ABNT** no meio do texto ("(Yazdani)." solto).
- **Título herdado do template.** "Resumo **ou** Conclusões do Capítulo" ficou em
  2.6 e 3.6 enquanto 5.6 já dizia "Resumo e conclusões do capítulo".

## Armadilhas de execução

- **Trocar texto de título custa 4 replaces, não 2.** Dois títulos reais mais o
  cache do sumário de cada um. Conferir o count antes de rodar.
- **Espaço no fim de `<w:t>` sem `xml:space="preserve"` é descartado.** Ao
  transformar "abruptos (" em "abruptos. ", adicionar o atributo no mesmo edit.
- **Remover parêntese aninhado costuma deixar itálico órfão.** O trecho inteiro
  entre parênteses estava em `<w:i/>`; virar período próprio exige tirar o
  itálico dos runs, senão fica uma frase em itálico no meio do parágrafo.
- **Não mexer no que o usuário já aprovou** sem perguntar. "reaquisitar"
  (formação irregular, 5 ocorrências no Cap. 4 a 6) ficou como está por decisão
  dele em 2026-09-12 — a troca mexeria em parágrafos já fechados.
- Rodar `check_pt.py` de novo **sobre o XML de saída** antes do repack: as
  classes corrigidas têm que ir a zero.
