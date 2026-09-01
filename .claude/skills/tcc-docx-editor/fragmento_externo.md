# Fragmento Externo (não o canônico)

Workflow simplificado para rascunho externo isolado, extraído de `SKILL.md`
em 2026-08-26 pelo limite de 200 linhas. O `SKILL.md` cobre o **canônico**
(OOXML direto, staging, repack); este arquivo cobre o fragmento.

Quando o alvo é um rascunho externo isolado (ex.: `capitulos_4_5_revisados.docx`
em Downloads, plain-Normal-style, sem tracked changes/comentários/tabelas), o
OOXML-surgery do `SKILL.md` é overkill. Usar **python-docx direto**:

- `docx.Document(path)` → editar `d.paragraphs[i].runs`/`insert_paragraph_before()`
  → `d.save(path)`. Sem staging, sem `repack.py`, sem IDs a rastrear.
- Reescrever texto de um parágrafo: remover todos os `w:r` (`for r in
  list(p.runs): r._element.getparent().remove(r._element)`) e recriar com
  `p.add_run(...)`, setando `bold`/`italic`/`font.name`/`font.size` (`Pt(...)`).
- Inserir parágrafo novo: `paragraph.insert_paragraph_before()` — desloca em
  +1 o índice de **todo** parágrafo seguinte; se for inserir vários, ou
  buscar cada alvo por texto (`p.text.startswith(...)`) em vez de índice fixo,
  ou processar em ordem que não invalide os índices já usados.
- Inserir imagem: `paragraph.add_run().add_picture(path, width=Inches(...))`;
  conferir `section.page_width - left_margin - right_margin` antes de escolher
  a largura (não há tracked changes/OOXML a ajustar para caber).
- **Trocar a imagem de uma figura sem mexer no parágrafo:** sobrescrever o
  blob da parte, não o desenho — `rel.target_part._blob = open(png,'rb').read()`
  para o `rel` de `d.part.rels.values()` cujo `target_part.partname` termina
  no `imageN.png` desejado. Preserva extent, alinhamento e legenda.
- **Inserir figura no meio do documento** preservando a formatação das
  existentes: `copy.deepcopy` do `w:p` de uma figura já pronta, depois
  `rId, _ = d.part.get_or_add_image(png)`, `blip.set(qn('r:embed'), rId)` e
  `docPr.set('id', ...)`/`set('name', ...)` com valores únicos.
  - **Reescale nos dois lugares.** O clone traz as dimensões da figura de
    origem. Se a nova imagem tem outra proporção, é preciso setar `cx`/`cy`
    em **`wp:extent` E em `a:ext`** (dentro do `pic:spPr/a:xfrm`) — mexer só
    no primeiro entrega a figura esticada. Calcular `cy` a partir do PNG:
    `w_px, h_px = struct.unpack(">II", blob[16:24])`, `cy = cx * h_px / w_px`.
  - **Para colocar a imagem acima de uma legenda que já existe, use
    `legenda._p.addprevious(node)`** em vez de `addnext` no parágrafo
    anterior: dispensa raciocinar sobre ordem inversa. Processando as âncoras
    em ordem **decrescente** de índice, os índices menores continuam válidos e
    dá para usar a lista `d.paragraphs` original o tempo todo.
- **Renumerar figuras:** nunca dar `replace("5.3", "5.4")` solto no texto —
  isso acerta também os títulos de seção (`5.3 Faltas assimétricas`) e as
  referências cruzadas. Renumerar em ordem **decrescente** (5.8→5.9 antes de
  5.7→5.8) e conferir depois se algum título `X.Y` foi arrastado junto.
- **Conferir sempre ao final:** MD5 de cada `word/media/*` contra
  `assets/charts/*.png` e `assets/diagrams/*.png`, ordem das imagens na
  sequência do documento, legenda × chamada no corpo, títulos de seção,
  numeração de figura sem buraco, **unicidade dos `docPr`**, e varredura de
  em-dash e de artefatos de código. Ver [[tcc-revisao-fragmento-cap5]].
- **`docPr` duplicado é silencioso.** `copy.deepcopy` sem reatribuir o `id`
  gera desenhos com identificador repetido; o Word abre assim mesmo e
  renumera ao salvar, então nada denuncia o problema até outra ferramenta
  reclamar. Só se descobriu em 2026-08-23, uma sessão depois de ter sido
  introduzido. Vale rodar uma varredura de `wp:docPr`/`pic:cNvPr`
  reatribuindo todos sequencialmente ao fim de qualquer inserção de figura.
- **Regenerou gráfico em `assets/`? Todo blob do documento fica suspeito.**
  Mexer no gerador muda o PNG de figuras que você nem pretendia tocar (uma
  escala compartilhada nova redesenha o par inteiro). O MD5 do item anterior é
  o que pega isso: qualquer `word/media/*` sem correspondência em `assets/` é
  figura desatualizada, não erro de conferência. Reescrever o blob e rodar a
  conferência de novo.
- **Legenda sem imagem deixa rastro no texto ao redor.** Frases como "A
  Figura 4.1 *pode ser utilizada para* representar" / "*pode ser empregada
  para* situar o leitor" são andaime de quem escreveu a legenda sem ter a
  figura. Ao inserir a imagem, converter em afirmação direta — e conferir
  no final que nenhum "pode ser utilizad/empregad" sobrou.
- **Nunca anexar texto ao último run sem olhar o `rPr` dele.**
  `p.runs[-1].text += frase` herda **toda** a formatação daquele run, inclusive
  `w:highlight`. Em 2026-08-26 uma frase acrescentada ao fim de um parágrafo
  saiu amarela porque o último run era um trecho que o **usuário** tinha
  marcado com marca-texto: o run passou de 284 para 781 caracteres e o realce,
  que era anotação dele delimitando a frase em discussão, passou a cobrir texto
  meu. Nenhuma conferência textual pega isso (o texto está correto); só apareceu
  ao renderizar a página. Ao acrescentar texto, **criar um run novo**
  (`copy.deepcopy` do vizinho, remover `w:highlight` do `rPr`, setar o `w:t` com
  `xml:space="preserve"`) e inseri-lo com `addnext`. Vale para qualquer
  formatação de anotação: realce, cor de fonte, tachado.
- **Renderizar a página antes de dar por pronto.** Exportar para PDF via Word
  (`win32com`, `ExportAsFixedFormat(caminho, 17)`) e rasterizar a página com
  `fitz` (PyMuPDF). Foi o único passo que revelou o vazamento de marca-texto
  acima, e é o que confere de fato a legibilidade da figura no tamanho impresso.
- **Troca de termo no fragmento inteiro:** iterar `d.paragraphs` → `p.runs`
  e aplicar `r.text.replace(...)` só nos runs que contêm o termo (não
  reescrever o parágrafo inteiro — perderia negrito/itálico de runs vizinhos
  sem motivo). Se houver uma forma composta do termo ("laço de sincronismo")
  e uma forma solta ("laço"), substituir a composta **primeiro** ou ela
  quebra em duas peças. Verificar com `assert`: contagem de substituições
  feitas == contagem de ocorrências antes de editar, e 0 ocorrências do termo
  antigo depois. Checar também que a troca não gerou duplicata boba (ex.:
  "SRF-PLL de sincronismo" ou "SRF-SRF") antes de salvar. Ver
  [[tcc-revisao-fragmento-cap4]] (troca "laço" → "SRF-PLL", 26 ocorrências).
- **Número no texto exige receita no KB.** Toda métrica escrita no documento
  precisa ter a definição registrada (janela, sinal, estatística) junto do
  valor. Métrica sem receita não é reproduzível e não sobrevive à próxima
  auditoria — foi assim que meia dúzia de valores do Cap. 5 caiu em
  2026-08-23. Ver [[tcc-revisao-fragmento-cap5-metricas]].
- **Receita no KB não basta para o LEITOR.** A regra acima protege a
  reprodutibilidade, mas quem lê o TCC não tem acesso ao KB: um valor fechado
  ("retenção de 8,2%") continua caindo do céu. Quando uma métrica derivada é
  reaproveitada em várias seções, definir na **primeira ocorrência**. Três
  formas, em ordem crescente de custo: cláusula curta embutida na frase;
  subseção de métricas no capítulo de metodologia; ou **figura mostrando a
  construção sobre o dado real**, que foi a escolha do usuário em 2026-08-26
  (ver "Gráfico Didático de Métrica" na skill `svg-diagrams`). A figura tem a
  vantagem de servir a todas as reaproveitações seguintes sem repetir nada.
  Perguntar qual das três antes de redigir: a escolha muda a numeração de
  figuras e/ou a estrutura de seções.
- **Entrega pode falhar com o arquivo aberto no Word:** `Copy-Item` devolve
  `IOException ... sendo usado por outro processo`. Não renomear o destino
  para contornar (gera arquivo canônico duplicado): pedir para fechar o Word e
  repetir a cópia.
- Verificar acentuação: nunca confiar no stdout do terminal (mojibake mesmo
  com conteúdo correto) — escrever um dump UTF-8 (`io.open(..., 'w',
  encoding='utf-8')`) e reler com a ferramenta de leitura de arquivo.
- KB desse workflow fica em `kb/tcc-word/revisao_fragmento_cap4.md` e
  `revisao_fragmento_cap5.md`, não em `docx_structure.md`/`historico_entregas.md`
  (que são só do canônico).

