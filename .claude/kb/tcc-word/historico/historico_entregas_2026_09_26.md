---
name: tcc-historico-entregas-2026-09-26
description: Entregas de 2026-09-26 no V10 (comentários do Oscar, notação do PLL, comentário 16 e Xiong, figuras ONS)
aliases: [tcc-historico-entregas-2026-09-26]
---

# TCC Word — Entregas de 2026-09-26

> Fragmentado de [[tcc-historico-entregas]] em 2026-09-27 por limite de
> 200 linhas. Ordem: mais recente primeiro.

## 2026-09-26 (noite, 9) — Figuras 2.1 e 2.2 (ONS) com áreas rotuladas (V10)

- Victor: "não dá para saber o significado da área olhando o gráfico". Só
  a mídia foi trocada (`image3.png`, `image4.png`), mais a remoção do
  `srcRect` e o recálculo de `cy` para a proporção nova. Largura (16 cm),
  legendas e fontes não mudaram. Continuam 74 páginas; `audit_docx` deu 0 falhas.
- Leitura das áreas e sinal da Figura 2.2: [[ons-voltage-ride-through]].
- Legenda da Figura 2.1 ("subtensões") mantida; a figura mostra também a
  borda de sobretensão (§5.7). Em aberto, a critério do Victor.
- Backup: `_backups/V10/TCC_Victor_Bruno_V10_backup_20260926_225822.docx`.

## 2026-09-26 (noite, 8) — Motivação restaurada ao original (V10)

- Victor achou as alterações das entregas 6 e 7 ruins ("ficaram horríveis")
  e pediu para voltar ao que estava. V10 restaurado byte a byte do backup
  `_backup_20260926_221022` (MD5 `608bc74e…`, anterior às duas). Isso também
  remove o "Feito." da thread do comentário 16, que segue **aberto**.
- Estado descartado guardado em `_backup_20260926_221616` (`30cc8fc6…`).
- Lição: para o comentário 16, não propor redação por conta própria. Mostrar
  a frase no chat e esperar o ok antes de mexer no Word.
- Depois: Victor pediu manter "identificada pelo ONS" e só somar a
  citação; opções A/B em [[tcc-pendencias]] item 25, aguardando escolha.

## 2026-09-26 (noite, 7) — Xiong movido para a âncora do comentário 16 (V10)

- **Correção pedida pelo Victor**: a citação da entrega 6 foi no lugar
  errado. Revertido o acréscimo no 2º parágrafo (volta ao texto original) e,
  **só no trecho que o comentário 16 marca**, "lacuna de modelagem
  identificada pelo ONS" virou "lacuna de modelagem identificada por Xiong
  et al. (2025)". Regra: a citação pedida em comentário entra no trecho
  ancorado (`commentRangeStart/End`), não onde parece caber melhor.
- **Pipeline**: `gen_xiong_ancora.py` (2 replaces) → finalize (74 págs, 0
  erro) → audit 0 falhas → MD5 `d806bfa5…` conferido → backup
  `_backup_20260926_221402` → entregue (`30cc8fc6…`) e reaberto.

## 2026-09-26 (noite, 6) — Xiong et al. (2025) citado na Motivação (V10), REVERTIDO na 7

- **Comentário 16 do Oscar** ("colocar a referência que passei para vocês do
  artigo que faz referência ao evento no sistema elétrico brasileiro"): o
  artigo é XIONG et al. (2025), confirmado pelo Victor; único PDF da
  `Bibliografia/` que menciona o apagão de 08/2023. Já estava na lista de
  referências, então não entrou entrada nova.
- **Aplicado e depois revertido**: acréscimo de oração com (XIONG et al.,
  2025) na 1ª frase do 2º parágrafo, fora da âncora. "Feito." na thread (ficou).
- **Não mexido, a pedido** ("não criar confusão"): o mesmo parágrafo diz
  22.547 MW / 31% (ONS, 2023), e o Cap. 2 diz 23.368 MW / 34,5% (valor do
  RAP). O Victor atribuiu o número ao Xiong, mas o PDF não traz nenhum dos
  dois. Pendência em aberto.
- **Pipeline**: `gen_xiong_motivacao.py` (1 replace) → finalize com
  `-Replies` (74 págs, 0 erro) → audit 0 falhas → MD5 `608bc74e…` conferido
  → backup `_backup_20260926_221022` → entregue (`d806bfa5…`) e reaberto.
- **Armadilha**: o `match` do `-Replies` com "ê" casou 0 comentários
  (`StartsWith` no Word). Usar prefixo sem acento que ainda seja único.

## 2026-09-26 (noite, 5) — VCO na Motivação e siglas definidas uma vez só (V10)

- **Comentário 13 do Oscar**: "convergência do integrador do VCO" virou
  "convergência do controlador do PLL" (VCO só aparecia definido no §3.4).
  "Feito." na thread do 13 e do 51 (SIN já definido antes).
- **Regra aplicada** (aprovada pelo Victor): no corpo, a sigla sai por extenso
  só na 1ª ocorrência, no padrão `Nome (SIGLA)`; depois, só a sigla. Resumo,
  Abstract, títulos de seção e legendas ficam fora. Detalhe e lista das
  correções em [[tcc-siglas-inventory]].
- **Pipeline**: `gen_siglas.py` (52 replaces + 3 itálicos) → finalize (74
  págs, 0 erro) → audit 0 falhas → MD5 `8431436e…` conferido → backup
  `_backup_20260926_215815` → entregue (`bac97281…`) e reaberto.

## 2026-09-26 (noite, 4) — "Soluções inovadoras" com referência na Contextualização (V10)

- Comentário do Oscar ("colocar alguma referência"): a frase final do 1º
  parágrafo ganhou 3 exemplos citados: grid-forming (STRAUSS-MINCU et al.,
  2026), inércia sintética/VSG (SHADOUL et al., 2022), requisitos dos
  operadores (ENTSO-E, 2026). Texto em [[tcc-full-intro]]. "Feito." na thread.
- **Referências**: + SHADOUL 2022 e + ENTSO-E 2026 (já citada no Cap. 2, mas
  faltava na lista), paraIds `1FB0030E`/`1FB0030F`, comentário [Claude].
- **Pipeline**: `gen_solucoes_inovadoras.py` → finalize (75 págs, 0 erro) →
  audit 0 falhas → MD5 `a54694dc…` conferido → backup
  `_backup_20260926_214609` → entregue (`03a410ec…`) e reaberto.

## 2026-09-26 (noite, 3) — Derivação do K_pd = V_m na Eq. 3.10 (V10)

- Rótulo da 3.10 virou parágrafo que substitui v_a, v_b, v_c na Eq. (3.7):
  soma das fases = (3/2)·V_m, cancelada pelo 2/3. A 3.10 ganhou 2 linhas na
  mesma célula (paraId novo `1FB0D101`), sem renumeração; 3.19 intocada.
- **Pipeline**: `gen_kpd_deriv.py` → finalize (75 págs, 0 erro) → audit 0
  falhas → MD5 `bf29ed81…` conferido → backup `_backup_20260926_212456` →
  entregue (`d8078502…`) e reaberto.

## 2026-09-26 (noite, 2) — K_pd = V_m e normalização explícita (V10)

- **Eq. 3.10**: K_pd = (3/2)·V_m → K_pd = V_m (Park com 2/3); rótulo cita as
  Eqs. (3.5)-(3.7). **Parágrafo antes da Eq. 3.19** reescrito: normalização
  por 16.329,93 V, K_pd = 1, citação Teodorescu. Texto aprovado pelo Victor.
  Regra em [[tcc-equacoes]]. Sem "Feito." (Oscar não comentou).
- **Pipeline**: `gen_kpd_norm.py` → `word_finalize.ps1` (75 págs, 0 erro) →
  `audit_docx` 0 falhas → MD5 conferido (`e572ee10…`) → backup
  `_backup_20260926_211707` → entregue (`bf29ed81…`) e reaberto.

## 2026-09-26 (noite) — Notação dos ganhos e comentários 107/110/112/138/142 do Oscar (V10)

- **Ganhos**: PLL = K_pPLL/K_iPLL sem vírgula (15 ocorrências + Eqs. 3.12,
  3.14, 3.15, que estavam sem sufixo); corrente = K_p/K_i, padrão da TeseAGP.
  Frase "Adota-se a notação…" subiu para antes da Eq. 3.10. Regra em [[tcc-equacoes]].
- **Figuras 3.2 e 4.3** (image7/image10) re-exportadas: bloco PI com sufixo,
  feed-forward ω_0; rodapé da 4.3 com as relações do PLL, no lugar das
  fórmulas do controlador de corrente (#142).
- **#107**: VCO com ω_PLL/ω_0/θ_PLL; θ_est → θ_PLL nas Eqs. 3.11/3.13/3.15.
  **#110/#112**: §3.5 explica ω_n = 4√2·f_g e cita (ALVES, 2022; YAZDANI;
  IRAVANI, 2010); Teodorescu não, por não ser fonte dessas equações na tese.
  **#138**: §4.3.2.2 remete à Eq. (3.23). Comentários mantidos no Word.
- **Pipeline**: `gen_ganhos_pll.py` + `gen_oscar_107_110_138.py` (o ID do
  comentário 138 virou 141 após o D9: casar pelo texto, não pelo ID) →
  `word_finalize.ps1` (75 págs, 0 campo com erro) → `audit_docx` 0 falhas →
  MD5 conferido → backup `_backups/V10/…_backup_20260926_204006` → entregue.
- **Respostas "Feito."** (entrega seguinte, só comentários): 6 respostas na
  thread do Oscar (#107, #110, #112, #118, #138, #142) via `word_finalize.ps1
  -Replies` (opção nova; 92 → 98 comentários, `audit_docx` 0 falhas) → backup
  `_backup_20260926_204700` → entregue e reaberto. Regra no item 5 de `padroes_revisao.md`.

## 2026-09-26 — Tudo Figura, Quadro vira Tabela (V10, comentários 3-5 do Oscar)

- 18 legendas Gráfico → Figura (`SEQ Figura`, mesma numeração), Quadro 4.1 →
  Tabela 4.1 (`SEQ Tabela`); Lista de Gráficos removida (21 parágrafos),
  Lista de Quadros → Lista de Tabelas; 23 remissões com concordância; resumo
  `74 f.` → `75 f.` (o run "74" era separado do " f."). Decisão D9.
- `audit_docx` 0 falhas, `check_abnt` 0 falhas; `pagecheck` só acusa a folha
  de ANEXOS (pendência antiga). Backup `_backup_20260926_202622`.

## 2026-09-26 — Sintonia inadequada no Resumo e no Abstract (V10)

- **Canônico passou a ser `TCC_Victor_Bruno_V10.docx`**, com os comentários
  do Oscar (e respostas do Bruno). O `_2` saiu da pasta; `config.py` foi atualizado.
- **Pedido**: incluir o caso da sintonia inadequada no Resumo, atendendo ao
  comentário 1 do Oscar. A primeira versão trazia o desfecho (perda de
  sincronismo) e foi recusada, porque o Resumo apresenta e não conclui.
- **Aplicado** (bloco 116, antes de "O trabalho conclui avaliando"):
  "Analisa-se também um cenário de sintonia inadequada, com os ganhos do
  controlador PI do PLL reduzidos em relação ao projeto nominal, comparando
  sua resposta dinâmica à do caso nominal."
- **Abstract** (bloco 123, espelho, atendendo ao comentário 2): "An
  inadequate-tuning scenario is also analyzed, …". A tradução não foi
  aprovada no chat: leva um comentário `[Claude]` no Word para o Victor dar
  o ok lá. Comentários do Oscar intactos (92 → 93).
- **Pipeline**: `gen_resumo_sintonia.py` → `word_finalize.ps1 -Comments`
  (parâmetro novo; 75 págs, 0 campo com erro) → `audit_docx.py` 0 falhas →
  MD5 conferido → backup `V10_backup_20260926_195650` → entregue e reaberto
  no Word. Os padrões que ficaram estão em `padroes_revisao.md` da skill.

## Relacionados

- [[tcc-historico-entregas]] — entregas mais recentes
- [[tcc-pendencias]] — item 25 (comentário 16) e item 26 (revisão de citações)
