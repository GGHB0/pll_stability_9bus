# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-08-05 (2ª rodada) — Fase 2: passe de estilo (Cap.3/Cap.4)

- **Motivação**: sequência da revisão acadêmica (Fase 1 = estratégia de
  equações, ver entrega abaixo). Fase 2 aplicou as diretrizes de estilo:
  itálico em estrangeirismos consagrados, neutralização de adjetivos de
  exaltação/promessas absolutas (rigorosa, essencial, crítico, indispensável,
  garantindo, perfeitamente + sinônimos próximos usados em tom de exaltação:
  crucial, fundamental, drasticamente, radicalmente, notável, insubstituível).
- **Levantamento apresentado para aprovação antes de qualquer edição**: 12
  termos estrangeiros sem itálico + 26 ocorrências de adjetivos de exaltação,
  organizados em tabela "antes → depois" por bloco, sem reescrever parágrafos
  inteiros (mudanças pontuais no nível da frase).
- **Achado à parte, fora do escopo original mas sinalizado e aprovado**:
  bloco 650 (§4.3.4.2) citava o nome do script `export_sim_data.m`
  diretamente no texto, contrariando a regra já estabelecida
  (`feedback_docx_no_code_artifacts`, blocos/subcircuitos do PSIM são a única
  exceção). Removido junto com "callback" (termo de implementação).
- **Execução** (script `C:\Temp\gen_style_pass.py`, 27 parágrafos editados):
  a maioria das trocas foi substring direta dentro de um único `<w:t>`; 3
  parágrafos (517, 518, 526, 596, 602, 633, 635, 638, 644) precisaram de
  divisão de `<w:r>` para isolar o termo a itálicizar, preservando o `rPr`
  original de cada segmento; bloco 536 tinha "precisa estar" fragmentado em
  3 runs por histórico de edição do Word (sem diferença de formatação) —
  contornado mirando um trecho mais curto (`perfeitamente sincronizado,`)
  que cabia inteiro num único run, em vez de reconstruir o parágrafo.
- **Cuidado extra**: bloco 650 tem uma âncora de comentário do Bruno
  (`commentRangeStart/End w:id="52"`, "Vai virar a parte do csv e do
  dashboard") que se estende até o bloco seguinte — preservada intacta
  (editei só o texto dos runs, sem tocar as tags de comentário).
- **Verificação em 3 camadas**: (1) `check_ids.py` + XML bem formado + 0
  em-dash; (2) render real via Word (`win32com`, `ExportAsFixedFormat`); (3)
  varredura sistemática das 60 condições (27 frases "antigas" ausentes + 27
  "novas" presentes + termos em itálico) no texto extraído do PDF gerado —
  todas as 60 passaram. TOC não precisou de atualização (nenhum título
  alterado nesta rodada).
- **Entregue**: `TCC_Victor_Bruno_V9_novo_indice_2.docx`, hash
  `943f247d...` (antes: `9db47610...`, entrega da Fase 1 mais cedo no mesmo
  dia). Pré-check de hash bateu com o staging antes da entrega.

## 2026-08-05 — Nova §3.5 (controlador de corrente) + referências cruzadas Cap.3↔Cap.4

- **Motivação**: o usuário pediu uma revisão aplicando a estratégia "Sintonia
  Teórica (Cap.3) vs. Aplicação Prática (Cap.4)": o Cap.4 deveria referenciar
  as equações do Cap.3 pelo número em vez de rededuzi-las. Refinamento
  seguinte: "todas as formulações do capítulo 4 têm que existir no capítulo 3
  antes" — a fórmula do controlador de corrente (`Kp=8·fg·Lest`,
  `Ki=32·fg²·Lest`), até então só em §4.3.2.2 sem numeração, também precisava
  de contrapartida simbólica no Cap.3.
- **Achado de projeto (verificado algebricamente, não citação de terceiros)**:
  os valores `Kp=29,48`/`Ki=7075,6` satisfazem exatamente `ωn²=Ki/Lest`,
  `2ξωn=Kp/Lest` com `ξ=1/√2=0,707` — a mesma forma canônica de 2ª ordem e o
  mesmo amortecimento ótimo já usados para o PLL (§3.4, Equação 3.18),
  confirmado contra `pll_stability_9bus_analysis.ipynb` célula 41
  (`ωn≈339,4 rad/s, ξ=0,707`). Decisão explícita: **não** usar a derivação de
  cancelamento polo-zero por `Ki/Kp=R/L` (fator 4) de
  `kb/inverter/agp_current_control_theory.md` — estruturalmente distinta
  (escala com `R`, não `fg²`), não é a fonte confirmada desta fórmula.
- **Edições aplicadas** (9 blocos novos em Cap.3 + 4 parágrafos reescritos em
  Cap.4, script `C:\Temp\gen_cap3_current_ctrl.py`):
  - **Nova §3.5** "Sintonia do Controlador de Corrente por Forma Canônica de
    Segunda Ordem", inserida entre §3.4 e o Resumo (que virou §3.6, sem
    renumerar as 20 equações existentes): Equações **3.21**
    (`G(s)=1/(s·Lest)`), **3.22** (característica de malha fechada) e
    **3.23** (`Kp=2ξωn·Lest`, `Ki=ωn²·Lest`), citando OGATA (2009) e
    YAZDANI; IRAVANI (2010) — sem página específica da tese do Alves.
  - **§4.3.2.2** [bloco 617→626]: fórmula solta substituída por referência à
    Equação (3.23) + aplicação numérica (mesmos valores finais).
  - **§4.3.2.3** [622→631]: passa a citar "Equações (3.19) e (3.20)"
    explicitamente em vez de só "descrito na Seção 3.4".
  - **§4.3.3** [626→635]: corta a 3ª repetição por extenso dos números do
    PLL nominal, remete a "Seção 4.3.2.3 (Kp,PLL=460...)" entre parênteses.
  - **§4.3.4.2** [650→659]: `2*omega_0 aprox. 753 rad/s` (pseudocódigo ASCII,
    valor arredondado errado) → `2ω0 = 754 rad/s` (Unicode, consistente com
    §3.4), remove adjetivo "crítico".
- **TOC estava em cache**: após a inserção, o Sumário ainda listava "3.5.
  Resumo..." (sem a nova seção) até forçar `doc.Fields.Update()` +
  `TablesOfContents(1).Update()` via automação do Word antes de salvar —
  ExportAsFixedFormat sozinho não recalcula os campos. Lição: **sempre
  atualizar campos via Word antes de considerar a entrega pronta**, mesmo com
  a flag `w:dirty` já marcada no XML.
- **Verificação em duas camadas**: (1) estrutural — `check_ids.py`, XML bem
  formado, 0 em-dash, todas as 5 edições presentes 1x cada; (2) visual real —
  render para PDF via automação do Word (`win32com`, `ExportAsFixedFormat`) e
  inspeção das páginas renderizadas (fórmulas OMML corretas, Sumário
  atualizado com "3.5. Sintonia..." e "3.6. Resumo...").
- **Entregue**: `TCC_Victor_Bruno_V9_novo_indice_2.docx`, 1.243.858 bytes,
  05/08/2026 01:27 (antes: 1.237.685 bytes, 04/08 01:41). Pré-check de hash
  bateu com o staging antes da entrega — sem edição concorrente.

## 2026-08-04 — Ganhos do PLL (§3.4), CIGRE (§2.3), dois cenários (§4.3.3), duas etapas (§4.3.2)

- **Motivação**: o Victor forneceu texto pronto para inserir no §3.4 sobre os
  ganhos do PI do PLL, pedindo explicitamente "sem confundir os ganhos". A
  inspeção mostrou que o texto fornecido apresentava a fórmula do
  **controlador de corrente** (`Kp = 8·fg·(L1+L2+Lest)` = 29,48 / 7075,6)
  rotulada como ganho do PLL, exatamente a confusão a evitar. Correção
  aprovada pelo Victor antes da edição.
- **Achados que mudaram o conteúdo** (detalhe em
  `kb/pll/pll_gains_methodology.md` § Armadilhas de leitura):
  1. os ganhos reais do laço são `kp_pll = 460` / `ki_pll = 105 820`,
     projetados por 2ª ordem (ξ = 0,707, `ts` = 20 ms pelo critério de 1%);
  2. a fórmula usa `fg` em hertz, não `ω0` em rad/s;
  3. `Lest = L1+L2 = 30,71 mH`, não `Lth = 1,16 mH` (o `Lth` é a fonte
     equivalente da fase PSIM, ver `kb/psim/psim_modeling.md`);
  4. a divisão por 4 é exclusiva do controlador de corrente e acompanha o
     escalamento da planta; os ganhos do PLL entram sem escala;
  5. a janela do cenário desajustado é **1,0 s** (não 0,9 s), e a falta é
     aplicada em 0,6 s, confirmado pelos `fault_info.json` (ver
     `kb/simulation/cenarios_simulados.md`).
- **Edições aplicadas** (17 blocos novos, 729 → 746):
  - **A** §3.4: 10 blocos após EQUAÇÃO 3.17, incluindo as equações novas
    **3.18** (forma canônica de 2ª ordem), **3.19** (`Ki,PLL = ωn²` e
    `Kp,PLL = 2ξωn`) e **3.20** (`ts = 4,6/(ξωn)` e `Kp,PLL = 9,2/ts`).
    Fecha ligando `2ω0` = 754 rad/s a 2,32·`ωn`.
  - **A'** §4.3.2.2 [605]: fórmula `8·fg·L` movida para cá, onde é correta;
    §4.3.2.3 [609]/[610]: notação `Kp,PLL`/`Ki,PLL` e remissão ao §3.4.
  - **B** §2.3 [426]: CIGRE como classificação alternativa; [433] notação;
    parágrafo novo com o mecanismo sequência negativa → 120 Hz → cycle
    slipping → colapso do controle vetorial.
  - **C** §4.3.3 [613] + parágrafo novo: dois modelos (460/105 820 contra
    92/21 164, `ωn` e ξ caindo juntos por √0,2); §4.3.3.1 [616]: baixa
    inércia amplifica a divergência; §4.3.3.2 [618]: duas configurações
    temporais (0,3/0,4 até 0,6 s e 0,6/0,7 até 1,0 s).
  - **D** §4.3.2: parágrafo declarando as duas etapas, PSIM sobre Thévenin
    e Simulink sobre o IEEE 9 barras, com o `.slx` como plataforma oficial.
  - **E** Referências: 4 entradas novas (ALVES; DIAS; ROLIM 2020; CIGRE;
    OGATA 2009; STRAUSS-MINCU et al. 2026), em ordem alfabética.
- **Notação adotada**: `Kp,PLL`/`Ki,PLL` para o laço de sincronismo,
  `Kp`/`Ki` para o controlador de corrente. Aplicada em 2.3, 3.4, 4.3.2 e
  4.3.3.
- **Armadilha reencontrada**: `w:proofErr` do Word quebrava as substrings em
  [609], [433] e [613]; o `docx-scripter` resolveu extraindo as âncoras
  programaticamente por `paraId` em vez de transcrevê-las como literais.
- **Script perigoso descartado**: `C:\Temp\set_toc_dirty_true.py` usa
  `ET.parse` + `tree.write()` no `document.xml` inteiro, o que colapsa
  namespaces de `mc:Ignorable` e corrompe o DOCX. Substituído por
  `C:\Temp\set_toc_dirty_pll.py`, que marca **só** o campo TOC por
  manipulação de texto bruto e valida com `ET.fromstring` antes de gravar.
- **Verificado**: XML bem formado, 0 em-dash, 0 tabelas adjacentes sem `<w:p>`
  entre elas, `EQUAÇÃO 3.18/3.19/3.20` uma vez cada, OMML com `oMathPara` e
  Cambria Math (3.18: 1 fração + 2 `sSubSup`; 3.20: 2 frações), paraIds
  `1FB00201`–`1FB00214` sem colisão.
- **Entregue**: `TCC_Victor_Bruno_V9_novo_indice_2.docx`, 1 237 685 bytes,
  04/08/2026 01:41 (antes: 1 234 318 bytes, 22/07 18:34). TOC marcado dirty.

## Entregas de julho/2026 (2026-07-22 e anteriores)

Ver `historico_entregas_2026_07.md` — inclui a remoção retroativa de
travessão, a remoção de linguagem de código/merge de 4.3.2.1–4.3.3.2, e o
incidente de corrupção que motivou a troca para `TCC_Victor_Bruno_V9_novo_indice_2.docx`.

## Entregas anteriores (V8)

Ver `historico_entregas_v8.md` (fragmentado em 2026-07-22 por limite de linhas).
