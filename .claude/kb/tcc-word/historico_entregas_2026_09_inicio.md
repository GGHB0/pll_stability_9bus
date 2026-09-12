# TCC Word — Entregas de setembro/2026 (até 2026-09-09)

> Fragmentado de `historico_entregas.md` em 2026-09-12 por limite de
> 200 linhas. As entregas de 2026-09-12 em diante ficam no arquivo
> principal. Ordem: mais recente primeiro.

## 2026-09-09 — Troca de terminologia PAC → PCC (todo o TCC + repositório)

- **Pedido**: "troque todas as referências dos termos usados como PAC para
  PCC, pois é a forma correta" + "faça isso no TCC". Confirmado com o usuário:
  a sigla vira **PCC** e a forma por extenso vira **"Ponto de Conexão Comum"**
  (antes "Ponto de Acoplamento Comum"), preservando a caixa; escopo = TCC
  canônico **e** repositório inteiro.
- **DOCX** (`gen_pac_to_pcc.py`, 8 substrings, todas dentro de um único
  `<w:t>` — sem `w:proofErr` no meio das âncoras):
  - Lista de siglas [bloco 295]: `PAC` → `PCC`, `Ponto de Acoplamento Comum`
    → `Ponto de Conexão Comum` (ordem alfabética mantida: PCC entre ONS e PD).
  - Texto corrido: [389] `ponto de acoplamento comum (PAC)`, [451] `tensão no
    PAC (YAZDANI...)`, [462] `tensão no PAC pelo SRF-PLL`, [465] `Ponto de
    Acoplamento Comum (PAC)`, [531] `no ponto de acoplamento comum`, [590]
    `no Ponto de Acoplamento Comum`.
  - Pós-troca: 0 ocorrência de "PAC" / "Acoplamento Comum"; 5×"PCC" +
    5×"Ponto de Conexão Comum". Nenhum ID alterado. Nenhuma legenda de figura
    continha "PAC", então a Lista de Ilustrações não muda de conteúdo (os
    campos foram atualizados por `word_finalize.ps1` via `Fields.Update()`).
- **Verificado**: `word_finalize.ps1` (75 págs, 15 471 palavras, 0 campo com
  erro, Word salvou), `audit_docx.py --util-in 6.30` = 0 falhas / 0 avisos.
- **Entregue**: `TCC_Victor_Bruno_V9_novo_indice_2.docx`, 3 696 018 bytes
  (antes: 3 695 723 bytes, MD5 `DB9215FB...` conferido no pré-check). Backup
  `..._backup_20260909_001700.docx`. MD5 entregue `51273bed...`.
- **Repositório** (mesmo dia, `sed` em 17 arquivos): KB `pll/`, `power-system/`,
  `simulation/`, `standards/ons_2_11.md` (`V_PAC` → `V_PCC`; `Vpcc_pu` já era
  a coluna correta), `tcc-word/` (siglas_inventory + full_cap2/3 + full_intro +
  revisao_fragmento_cap5*), `skills/svg-diagrams/SKILL.md`, `README.md`,
  `notebooks/pll_stability_9bus_analysis.ipynb` (`v_PAC` → `v_PCC`; JSON
  revalidado). `.claude/worktrees/` intocado de propósito.

## 2026-09-02 — Mesclagem dos Cap. 4 e 5 do fragmento no canônico

- **Pedido**: "quero que vc adicione no tcc original agora", logo depois do
  enxugamento analítico do Cap. 5 no fragmento (entregue no mesmo dia).
- **Achado apresentado antes de editar**: o Cap. 4 do fragmento é **mais raso**
  que o do canônico (43 parágrafos contra ~144 blocos) e a troca apagaria a
  modelagem dos geradores, a topologia da falta, três tabelas e quatro
  comentários do Bruno. Ofereci três caminhos; o usuário escolheu substituir os
  **dois capítulos por inteiro**, ciente da perda.
- **Blocos 591–734 substituídos** pelos 117 parágrafos do fragmento. Receita
  completa (mapeamento de estilos, convenção de figura invertida, reescalonamento
  Carta→A4, IDs, limpeza das partes de comentário) em
  [[tcc-mesclagem-cap45-canonico]].
- **Defeito que só a conferência numérica pegou**: quatro figuras vinham com
  6,50 in de largura (Carta) contra 6,30 in de área útil do TCC (A4), estourando
  a margem direita. Reescaladas em `wp:extent` **e** `a:ext`.
- **Verificado**: XML bem formado, 19 mídias novas sem colisão de nome, todos os
  `r:embed` com relationship e alvo no zip, 28 `docPr` únicos, nenhuma imagem
  acima da área útil, 0 em-dash. Word abriu sem prompt de reparo, exportou
  75 páginas e reconstruiu o sumário com as seis subseções de 5.1 a 5.6.
  Páginas 43, 55, 57 e 61 rasterizadas e conferidas.
- **Entregue**: `TCC_Victor_Bruno_V9_novo_indice_2.docx`, 4 049 514 bytes
  (antes: 1 235 426 bytes). Backup `..._backup_20260902_004347.docx`.

## 2026-09-02 — Enxugamento analítico do Cap. 5 (fragmento)

- 20 edições no `capitulos_4_5_revisados.docx`, poupando a §5.2 a pedido do
  usuário. Critério e antes/depois em
  [[tcc-revisao-fragmento-cap5-enxugamento]].
- Dois parágrafos **cresceram** de propósito: o 111, que trocou um mínimo/máximo
  dependente de janela pela remissão à Figura 5.12, e o 115, que dizia "perde o
  sincronismo de forma permanente" contra a ressalva do parágrafo 107.
- **Entregue**: 3 102 724 bytes; backup `..._backup_20260902_002611.docx`.

