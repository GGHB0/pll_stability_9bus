---
name: tcc-historico-entregas-2026-07
description: Histórico de entregas no DOCX do TCC em 2026-07-22 (tarde e noite) — troca para o arquivo _2, remoção de linguagem de código e de travessões
aliases: [tcc-historico-entregas-2026-07]
---

# TCC Word — Histórico de Entregas (julho/2026, entregas antigas)

> Entregas anteriores (2026-07-19 e 2026-07-22 no arquivo obsoleto) em [[tcc-historico-entregas-2026-07-inicio]].

> Fragmentado de `historico_entregas.md` em 2026-08-04 (e novamente em
> 2026-08-05) para respeitar o limite de 200 linhas. Entregas mais recentes
> ficam no arquivo principal.

## 2026-07-22 (noite, 2ª rodada) — Remoção retroativa de travessão/em-dash

- **Motivação**: o Victor pediu para nunca usar travessão ("—") no texto do
  TCC (regra registrada em `SKILL.md` § Convenções de escrita e na memória
  `feedback_docx_no_em_dash`). Após adicionar a regra, ele pediu a limpeza
  retroativa do texto já existente no `_2.docx`.
- **Escopo**: 13 parágrafos continham travessão no corpo do documento
  (`document.xml`); todos localizados por busca direta do caractere "—" +
  paraId. Em todos os casos o travessão estava dentro de um único `<w:t>`
  contínuo (sem `<w:proofErr>` interrompendo o trecho exato do travessão),
  então optei por **replace cirúrgico de substring** em vez de reescrever o
  parágrafo inteiro — mais seguro, preserva toda a formatação/OMML ao redor.
  Duas ocorrências (`75AF0000`, `5E6D6F65`) precisaram ser divididas em duas
  buscas menores porque a string alvo original cruzava um `<w:proofErr>`
  em torno de "Kp" inserido pelo corretor do Word.
- Substituições: vírgula, ponto e vírgula ou parênteses no lugar do
  travessão, conforme o papel sintático (aposto, parentético, oração
  coordenada). paraIds afetados: `16000003`, `16100002`, `16100004`,
  `16100005`, `16100007`, `16200002`, `494DB39C`, `3BDB772E`, `75AF0001`,
  `75AF0000`, `604CA2E5`, `5E6D6F64` (2×), `5E6D6F65` (2×).
- **Deixado de fora do escopo**: paraId `75AF0001` ainda cita "notebook de
  dimensionamento" (artefato de código/ferramenta) — não foi removido nesta
  passada por não ter sido pedido explicitamente; sinalizado ao Victor.
- Verificado: 0 travessões restantes no corpo, XML bem formado, tag raiz
  idêntica ao staging. Entregue ao OneDrive às 18:34 (1.234.318 bytes).
  Pré-check de timestamp/tamanho bateu com o staging (18:13:05) antes da
  entrega — sem edições concorrentes (conteúdo textual também comparado
  byte a byte contra a entrega anterior de 17:57: idêntico, a diferença de
  tamanho era só ruído de reabertura do Word).

## 2026-07-22 (noite) — Remoção de linguagem de código + merge de conteúdo (4.3.2.1–4.3.3.2)

- **Motivação**: o Victor pediu para não citar arquivos/scripts/variáveis de
  código (`params.m`, `parameters100MVA.txt`, `FAULT_TYPE/BUS/LINE`) no texto
  do TCC — projeto de engenharia deve usar termos de componentes/modelagem
  matemática, não de implementação. Nomes de bloco/subcircuito do PSIM
  (`RESETI_I1`, `.SUB Clarke`, `VTRI2`, `PlantaLCL1`) foram mantidos — são
  referências de esquemático, não de código. Ver memória
  `feedback_docx_no_code_artifacts`.
- **Conteúdo novo fornecido pelo Victor**, mesclado com o texto existente em
  vez de substituí-lo por inteiro: menção ao bloco `PlantaLCL1` + ω_res
  (4.3.2.1), resistências de amortecimento R_d1/R_d2/R_d3 (4.3.2.1), novo
  parágrafo sobre a malha de corrente no PSIM (I_d,ref/I_q,ref → m_a,
  portadora `VTRI2`, 4.3.2.2), nomes `.SUB Clarke`/`.SUB Park`/`RESETI_I1`
  no lugar de `Clarke`/`Park`/`RESETI_I` (4.3.2.3).
- **Achado**: o Victor havia colado manualmente no Word uma versão bruta
  desse mesmo texto (com artefato de LaTeX quebrado, ex.:
  "ωres=9068,9968\omega_{res}...") como parágrafo duplicado antes do
  parágrafo original de 4.3.2.1. Esse duplicado foi removido e o conteúdo
  novo foi integrado no parágrafo original (com variáveis em OMML nativo do
  Word, reaproveitando os helpers `mr`/`ssub` de `gen_eq_format.py`), em vez
  de manter o texto colado cru.
- **Edição concorrente detectada**: entre a entrega das 01:28 e esta sessão,
  o Victor editou e salvou o `_2.docx` no Word (17:22, +12 KB). O pré-check
  de timestamp/tamanho pegou a divergência antes de sobrescrever — evitou
  perda do trabalho dele. Re-staging feito a partir do arquivo das 17:22;
  os 6 pontos de edição foram relocalizados por `paraId` (não por índice de
  bloco, que muda) e 3 deles (`16000001`, `16100007`, `75AF0001`) precisaram
  de reescrita completa do parágrafo em vez de replace cirúrgico, porque o
  Word tinha inserido tags `<w:proofErr>` entre os runs desde o save do
  Victor — quebrando os `replace_once` originais que esperavam runs
  contíguos. Lição: **preferir replace por `paraId` inteiro** (regex
  `<w:p w14:paraId="X"[^>]*>.*?</w:p>`) em vez de substring cirúrgica sempre
  que o parágrafo já tiver passado por um save do Word desde a última
  inspeção — `<w:proofErr>` pode aparecer a qualquer momento.
- **Numeração confirmada nesta sessão**: o `_2.docx` retém a estrutura da
  reestruturação de 2026-07-19 (4.1/4.2/4.3.1–4.3.4/4.4), diferente da
  numeração do arquivo sem sufixo (obsoleto). `content_map.md` e
  `equacoes.md` corrigidos de volta para essa numeração.
- Entregue ao OneDrive às 17:57 (1.234.570 bytes). Pré-check de
  timestamp/tamanho bateu com o baseline de 17:22 antes da entrega.

## 2026-07-22 (tarde) — Corrupção + troca para TCC_Victor_Bruno_V9_novo_indice_2.docx

- **Incidente**: o Word acusou "conteúdo ilegível" ao abrir
  `TCC_Victor_Bruno_V9_novo_indice.docx` após a entrega da manhã. Causa raiz
  identificada: dois scripts usados para marcar o Sumário como `w:dirty`
  (`adjust_toc_dirty.py`, `set_toc_dirty_true.py`) fizeram
  `ET.parse()` + `tree.write()` no `document.xml` **inteiro**. O
  `ElementTree` do Python só emite declarações `xmlns:*` para namespaces
  que ele detecta em uso na árvore — namespaces declarados na raiz mas só
  referenciados como texto (em `mc:Ignorable="w15 w16se ..."` e em
  `Requires="wps"` dentro de `mc:AlternateContent`) foram descartados
  silenciosamente, mesmo com `ET.register_namespace()` chamado para todos
  eles. A tag raiz `<w:document>` encolheu de 2390 para 959 bytes; o XML
  continuava bem formado (`ET.fromstring` passava), então nenhum check do
  pipeline pegou o problema — só o parser estrito do Word. **Lição: nunca
  usar `ET.parse`+`tree.write` no documento inteiro; só regex/substituição
  de string sobre o texto bruto** (como o próprio `set_toc_dirty_regex.py`
  já fazia — ele rodou por último mas sobre o arquivo já corrompido pelos
  dois anteriores).
- **Descoberta durante a investigação**: existe um segundo arquivo,
  `TCC_Victor_Bruno_V9_novo_indice_2.docx` (OneDrive, mesma pasta), maior
  (1,2 MB) e mais recente (21/jul 22:53) que o arquivo sem sufixo. Segundo
  o Victor, ele contém uma correção manual dele por cima de uma edição
  minha anterior — é a versão real/atual do documento. O arquivo sem
  sufixo ficou desatualizado **e agora corrompido**; não usar mais.
  `config.py` (`DOCX_SOURCE`) atualizado para apontar para o `_2`.
- **Correção**: reaplicada a correção do 4.2.2.3 (ver entrega abaixo) direto
  sobre `doc_tcc_v2.xml` (extraído do `_2`, namespaces intactos,
  2565 bytes na tag raiz — igual ao original) usando só `str.replace`/regex,
  sem nenhum parse+write de árvore inteira. TOC marcado dirty (48
  `fldChar`) pelo mesmo método regex. Validado: zip íntegro, `document.xml`
  bem formado, tag raiz idêntica à original antes e depois do repack.
  Entregue ao `_2` no OneDrive às 01:28 (1.230.587 bytes). Pré-check de
  timestamp/tamanho do OneDrive antes da entrega bateu com o baseline do
  staging (1.235.451 bytes, 21/jul 22:53) — sem edições concorrentes.
