# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-09-12 — Revisão de português do documento inteiro

- **Pedido**: "revise todos os erros de português e concordância, atualize a
  skill se necessário". Leitura integral dos 750 blocos, da capa às referências.
- **Escopo aprovado pelo usuário**: grupos A (22 erros de gramática, regência e
  concordância) e B (6 padronizações). **38 replaces**, todos com count
  verificado, em `C:\Temp\gen_revisao_pt.py`.
- **Amostra do que estava errado**: `implicando em uma redução` (implicar é
  transitivo direto); `capacidade do inversor **em** atender` (3 ocorrências,
  inclusive no Resumo); `serviços anancilares`; `acomplamento`; `onde` com
  antecedente não locativo (2×); duas frases **sem verbo principal** ("A
  Transformada de Park, aplicando uma rotação…", "Apresentar os conceitos…");
  vírgula entre verbo e objeto e entre relativo e verbo; `($d$ e $q$)` resíduo
  de LaTeX; `(Yazdani).` fora do padrão ABNT.
- **Padronizações**: `através de` → `por meio de`; eixos `D`/`Q` → `d`/`q`;
  `105 820`/`21 164` → `105.820`/`21.164`; `Switch On To Fault` → `Switch Onto
  Fault`; PCC em minúsculas no corpo; títulos **2.6 e 3.6** de "Resumo **ou**
  Conclusões do Capítulo" (resto do template UERJ) para "Resumo e conclusões do
  capítulo", casando com o 5.6 — 4 replaces, porque o cache do sumário conta.
- **Decisões do usuário**: manter `reaquisitar` (5 ocorrências, formação
  irregular mas consistente e em parágrafos já fechados); não mexer no
  pré-textual nem nos placeholders.
- **Dois ajustes de acompanhamento**, feitos junto: no bloco 396 o parêntese
  aninhado virou período próprio e o itálico dos runs foi removido (frase
  inteira em itálico ficaria pior que o parêntese); no 474, "análise de
  resultados **desenvolvidos**" → "desenvolvidas".
- **Pipeline**: repack → `word_finalize.ps1` (78 páginas, 16.093 palavras,
  91 campos, 25 figuras, 0 campo com erro, SALVOU sem erro) → `audit_docx.py`
  **0 falhas / 0 avisos** → backup `_backup_20260912_005943` → entrega, MD5
  `db8d1e1c…` conferido nos dois lados. Word estava aberto no canônico no
  início; esperei o usuário fechar e reconferi o MD5 antes de entregar.
- **Skill**: `revisao_pt.md` e `scripts/check_pt.py` novos, ponteiros no
  `SKILL.md` (193 linhas). `content_map.md` atualizado nos títulos 2.6 e 3.6.
- **Pendências levantadas e NÃO corrigidas** (decisão do usuário): Cap. 1 diz
  22.547 MW / 31% e Cap. 2 diz 23.368 MW / 34,5% para o mesmo evento de 2023
  (a KB registra o segundo par); ficha do Resumo com ano 2025 contra 2026 na
  capa, "XXf." e vírgula onde ABNT pede ponto; `[ANO A CONFIRMAR]` no corpo
  (bloco 424); 4 placeholders de figura no Cap. 2 e 3; 6 referências com
  `[A CONFIRMAR]`; restos de template no pré-textual; siglas GFM, SOTF, COI,
  FFR, BESS, TSO, DSO e SCR usadas no texto e ausentes da lista; bloco 451 com
  4 parágrafos fundidos num só e 471 com um parágrafo de frase única; Cap. 7
  vazio; títulos do Cap. 4/5 em caixa baixa contra Title Case no Cap. 2/3.

## 2026-09-12 — Capítulo 6 (Conclusões) redigido e inserido

- **Pedido**: "`Capitulo6.docx` add no TCC" (arquivo vindo da pasta Downloads).
  Era o **template completo do TCC** com quase tudo em placeholder; o único
  conteúdo real eram 4 parágrafos de Cap. 6 e o título vazio do Cap. 7.
- **Estado encontrado no canônico**: Cap. 6 completamente **vazio** (bloco 720
  título + 721 parágrafo em branco), Cap. 7 só título, REFERÊNCIAS logo depois.
  A nota do `content_map.md` dizendo "Conclusão redigida (cycle slipping, LVRT
  formal vs. efetivo)" estava **desatualizada** — não havia texto nenhum.
- **Julgamento do texto recebido** (o usuário pediu explicitamente antes de
  inserir), em 3 rodadas:
  - v1, correção pontual: consertava a promessa do Cap. 7 vazio, a troca
    silenciosa dos objetivos específicos 3 e 5 e a falta da citação
    (ONS, 2023). Recusada: era **o 5.6 reescrito com sinônimos**.
  - v2, análise quantificada: cruzava 5.2 com 5.3 e trazia 16 números.
    Recusada: "virou uma análise ... isso já foi feito no capítulo cinco".
  - v3, **aceita**: consolidação **genérica** do trabalho inteiro, do contexto
    de transição e dos blecautes do Cap. 2 à teoria do Cap. 3, ao desenho do
    estudo do Cap. 4 e à síntese qualitativa do Cap. 5. Cinco parágrafos,
    619 palavras, **zero números**, 0 sequências de 6 palavras em comum com o
    5.6 e com o 5.5.
- **Lição**: a conclusão sobe de **altitude**, não de profundidade. Nem
  repetir o resumo do capítulo (v1) nem aprofundar além dele (v2).
- **DOCX** (`C:\Temp\gen_cap6.py`): bloco 721 (parágrafo vazio `093CA689`)
  substituído por 6 parágrafos, os 5 de corpo (`1FB00221`–`1FB00225`, molde do
  bloco 716) mais a quebra de página (`1FB00226`, molde do bloco 719) antes do
  título do Cap. 7. Campo TOC marcado `w:dirty` (o Cap. 6 ganhou ~2 páginas).
  772 → 777 parágrafos.
- **Armadilha de spec**: a checagem "delta de `<w:p>` == 6" estava errada —
  trocar 1 parágrafo por 6 dá saldo **+5**. O `docx-scripter` travou e pediu
  confirmação em vez de chutar, que é o comportamento correto.
- **Verificado**: texto inserido **byte-idêntico** ao aprovado (comparação
  programática contra o `.txt` de origem, não inspeção visual);
  `word_finalize.ps1` (78 págs, 16 089 palavras, 0 campo com erro, Word
  salvou); `audit_docx.py --util-in 6.30` = **0 falhas / 0 avisos**.
- **Entregue**: 3 693 622 bytes, MD5 `bc33cc4f...` (pré-check do destino
  `0d10057c...` conferido antes de sobrescrever). Backup
  `..._backup_20260912_002951.docx`.
- **Cap. 7 segue vazio** por decisão do usuário; o Cap. 6 foi redigido para
  fechar sem depender dele.

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

## Entregas de agosto/2026

Ver `historico_entregas_2026_08.md` — nova §3.5 (controlador de corrente) +
referências cruzadas Cap.3↔Cap.4, passe de estilo Fase 2, e os ganhos do PLL
(§3.4) / CIGRE (§2.3) / dois cenários (§4.3.3) / duas etapas (§4.3.2).

## Entregas de julho/2026 (2026-07-22 e anteriores)

Ver `historico_entregas_2026_07.md` — inclui a remoção retroativa de
travessão, a remoção de linguagem de código/merge de 4.3.2.1–4.3.3.2, e o
incidente de corrupção que motivou a troca para `TCC_Victor_Bruno_V9_novo_indice_2.docx`.

## Entregas anteriores (V8)

Ver `historico_entregas_v8.md` (fragmentado em 2026-07-22 por limite de linhas).
