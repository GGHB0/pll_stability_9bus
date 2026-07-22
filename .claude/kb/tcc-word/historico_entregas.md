# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-07-22 — TCC_Victor_Bruno_V9_novo_indice.docx

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

- **Seção 3.3** — "PROTOCOLOS DE CONTINGÊNCIA E ANÁLISE DE CENÁRIOS" (tracked
  changes; no índice novo virou 4.3.4)
  - Afundamento Simétrico (2 parágrafos + [TABELA 3.1])
  - Afundamento Assimétrico (2 parágrafos + [TABELA 3.2])
  - ⚠️ Texto adicionado **sem acentuação** — corrigir em edição futura

- **Correções dos comentários do Oscar** (jun/2026, script gen_oscar_fixes.py):
  - #1 Resumo: "do algoritmo de sincronismo" → "da técnica de sincronismo de fase"
  - #3 Resumo: sentença IAE/ISE removida (tracked delete)
  - #6 Intro: "os inversores...insubstituível" → texto GFL com serviços ancilares
  - #13 Cap.2 intro: "O objetivo é apresentar" → "Apresentar", "a operação" → "à operação"
  - #14 Cap.2: "sistema de sincronismo " removido (SRF-PLL agora é a sigla direta)
  - #17/#21/#24/#29: Ttulo4 → Ttulo3 com pPrChange (Clarke, Park, Arq.Controle, PWM)
  - Arquivo: `C:\Temp\tcc_oscar_fixes.docx` → copiado para OneDrive como `V8_oscar_fixes.docx`
