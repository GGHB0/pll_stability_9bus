# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

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

## 2026-07-22 — TCC_Victor_Bruno_V9_novo_indice.docx (arquivo obsoleto, ver acima)

- **Correção 4.2.2.3 (SRF-PLL): Simulink → PSIM**: ✅ ENTREGUE — a seção
  descrevia a implementação do SRF-PLL no Simscape Electrical (bloco
  Sinusoidal Measurement, params.m, notch discreto 120 Hz via Tustin). Na
  verdade essa fase (4.2.2 — conversor/filtro/PI de corrente/PLL) foi
  inteiramente modelada no **PSIM**, não no Simulink; 4.2.3 (geradores/rede/
  falta) permanece Simulink, sem alteração. 3 blocos reescritos: [527] troca
  "Simscape Electrical do MATLAB/Simulink" → "PSIM (Altair Engineering)";
  [528] reescrito descrevendo os subcircuitos `Clarke`/`Park` (detector de
  fase), Loop Filter PI, VCO via bloco `RESETI_I` com reset em 2π, ganhos
  carregados de `parameters100MVA.txt` — **sem menção a notch 120 Hz**
  (confirmado por rastreio do netlist `PSim\01_Sistema PLL_vfinal_100MVA
  (backup)1.txt`: o único notch do PSIM é o de ressonância LCL na malha de
  corrente, TFCN1/TFCN2, não relacionado ao PLL); [529] "modelo Simulink" →
  "PSIM" e "bloco de controle" → "blocos de ganho do compensador PI
  implementado no circuito". Fonte técnica: `kb/psim/psim_modeling.md` +
  `kb/psim/psim_netlists.md`. Pipeline: `gen_psim_422.py` (regex por
  paraId, evita erro de transcrição Unicode) → TOC marcado dirty (49
  fldChar) → `repack.py`. Estado do XML: `C:\Temp\doc_tcc_psim422.xml`;
  DOCX final: `C:\Temp\tcc_final.docx` (500979 bytes de document.xml),
  entregue ao OneDrive às 01:03 (569972 bytes).

- **Descoberta de renumeração do Cap.4 desde 19/07**: durante a inspeção
  para a correção acima, `dump_headings.py` revelou que a numeração do
  Cap.4 registrada em `content_map.md` (4.1 Foco do Estudo / 4.2
  Plataformas de Simulação / 4.3 Modelagem, filhos 4.3.1–4.3.4) estava
  desatualizada — o usuário reestruturou no Word depois da sessão de
  19/07: 4.1+4.2 antigos fundidos em **4.1** único, antigo 4.3 → **4.2**
  (filhos um nível acima: 4.2.1–4.2.3), Protocolos de Contingência voltou
  a Ttulo2 como **4.3** (era Ttulo4 em 4.3.4.x). `content_map.md`
  atualizado para refletir a numeração real e verificada.

- **Limpeza do notch 120 Hz do PLL na KB** (texto/documentação apenas — o
  bloco já havia sido removido do `.slx` anteriormente, foi um teste
  descartado): `kb/pll/pll_notch_implementation.md` marcado como histórico
  (status no topo, título "(HISTORICO - removido do modelo)"),
  `kb/pll/_index.yaml` e `kb/simulation/params_workflow.md` ajustados para
  não descrever o notch como recurso atual. Não tocado: o notch de
  ressonância LCL na malha de corrente (`simulink_model.md`,
  `lcl_filter.md`, `agp_current_control_theory.md`, `psim_netlists.md`,
  `psim_modeling.md`) — é outro filtro, ainda válido, não relacionado ao
  PLL.

## 2026-07-19 — TCC_Victor_Bruno_V9_novo_indice.docx

- **Reestruturação interna do Cap.4** (19:49): ✅ ENTREGUE —
  Cap.4 agora segue 100% o índice do professor: novo **4.1 Foco do Estudo**
  (título + 2 §§ novos, paraIds 1FB00057–59); 4.1 antigo → **4.2 Plataformas
  de Simulação – Características Individuais**; 4.2 antigo → **4.3** (filhos
  4.3.1, 4.3.2 renomeado "Projeto do Conversor Fonte de Tensão e dos
  Controladores", 4.3.2.1–3, 4.3.3 + 4.3.3.1–3); Protocolos rebaixado
  Ttulo2→Ttulo3 como **4.3.4** (afundamentos viram Ttulo4 4.3.4.1/4.3.4.2,
  fora do Sumário de 3 níveis). Reescritas: intro do 4.3.3 (ode23t =
  trapezoidal implícito passo variável, RelTol 10⁻³, Ts=5 µs, janela 0,6 s,
  **R2025a** — versão inferida do .slx, confirmar com Bruno), 4.3.3.2 (falta
  sem local fixo; 0,3→0,4 s = 6 ciclos; 4 tipos; FAULT_TYPE/BUS/LINE via
  params.m) e 4.3.3.3 (monitoramento alinhado ao dashboard: 5 grupos de
  sinais, 2 taxas + interpolação, export StopFcn→CSV+metadados, métricas
  IAE/ISE/ts/pico/ΔP/ΔQ/LVRT 1547-2018, tabela comparativa). 6 refs
  cruzadas obsoletas corrigidas (4.2.1→5.2.1 ×3, 4.3.1→5.3.1 ×3,
  4.1→5.1, 3.3→4.3.4). Comentários 43/46/48/49 preservados. Edições
  diretas, sem `<w:ins>`. Pipeline: `gen_cap4_restructure.py` +
  `repack_cap4.py`; estado atual do XML = `C:\Temp\doc_tcc_cap4.xml`,
  template ZIP = `C:\Temp\tcc_v9_cap4.docx`.

- **Reformatação das equações**: ✅ ENTREGUE — 17 equações em
  tabela invisível (equação centralizada + "EQUAÇÃO N.M" à direita),
  numeradas 3.1–3.17; eqs 4.1/4.2 do LCL inseridas; refs cruzadas
  atualizadas. Detalhes e padrão XML: `equacoes.md`.

- **Siglas + padronização IBR + fix MOHAN**: ✅ ENTREGUE no mesmo
  DOCX — lista pré-textual com 31 siglas (ver `siglas_inventory.md`), RBI/ICR →
  IBR (4 ocorrências), MOW → MOHAN (2 ocorrências). **Edições diretas, sem
  `<w:ins>`** (aprovadas explicitamente pelo Victor; mesmo trade-off da
  renumeração). Pipeline: `gen_move_anexos.py` → `gen_siglas_fixes.py` →
  `repack_final.py` (todos em C:\Temp).

- **Move do ANEXOS**: ✅ ENTREGUE — título ANEXOS (Ttulo1) movido
  para o fim absoluto, após REFERÊNCIAS (ordem ABNT). A primeira versão ficou
  obsoleta (usuário salvou no Word às 12:04 aceitando as tracked changes);
  refeito sobre a versão nova e copiado ao OneDrive às 12:20.

## Entregas anteriores (V8)

Ver `historico_entregas_v8.md` (fragmentado em 2026-07-22 por limite de linhas).
