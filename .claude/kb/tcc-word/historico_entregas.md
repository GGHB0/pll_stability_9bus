# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-09-12 (noite) — Referências em amarelo fechadas

- **Pedido**: "adicionamos o capítulo 7, porém deixamos de amarelo textos que
  vc pode preencher". O Cap. 7 continua **só com o título**; as 6 marcas
  amarelas estavam todas na lista de REFERÊNCIAS (mais o `XX` da ficha
  catalográfica, que é o número de folhas e fica para o fim).
- **Resolvidas com fonte**: ALVES (2022) ganhou o título completo da tese
  (folha de rosto do `TeseAGP.pdf`); CIGRE CSE N°37 é de **junho de 2025**,
  elaborado por M. Lindner et al. (fechado em cse.cigre.org, ver
  `pendencias.md` item 16, agora ✅).
- **Dois erros que o amarelo escondia**: WU; WANG não é *Power Systems*/2024
  e sim **IEEE Trans. on Power Electronics, v. 35, n. 4, p. 3573-3589, abr.
  2020** (DOI 10.1109/TPEL.2019.2937942, conferido no PDF e no Crossref);
  XIONG et al. saiu da publicação antecipada e virou **v. 40, n. 3, p.
  2545-2556, maio 2025**. Levou 7 citações no corpo junto: 1× CIGRE,
  3× (WU; WANG, 2024→2020), 3× (XIONG et al., 2024→2025).
- **Duas entradas órfãs removidas**: `ALVES … 2021` (critérios de LCL) e
  `SOUSA, et al. 2021` (PSIM). Nenhuma das duas é citada no corpo — a §4.2
  foi reescrita e não cita mais o PSIM, e os critérios de LCL vêm da tese de
  2022. A pendência 7 (citar MATLAB/PSIM no §4.2) **continua aberta**.
- **Pipeline**: `gen_refs_fill.py` (11 replaces com count + remoção de 2
  parágrafos) → repack → `word_finalize.ps1` (78 páginas, 91 campos, 0 campo
  com erro, SALVOU sem erro) → `audit_docx.py` **0 falhas / 0 avisos** →
  backup `..._backup_20260912_191732.docx` → entrega, MD5 `3ecb43eb…`
  conferido nos dois lados.

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

## 2026-09-12 (noite) — Capítulo 7 (Trabalhos Futuros) redigido e inserido

- **Conteúdo**: 2 parágrafos, 311 palavras, sem subseções. Eixo 1 (trocar a
  estrutura de sincronismo) e Eixo 3 (ampliar as condições de rede), conforme
  [[tcc-trabalhos-futuros]]. Texto e histórico dos cortes naquele arquivo.
- **Achado no arquivo vivo**: o REFERÊNCIAS vinha **colado** no título do
  Cap. 7, sem quebra de página, então os dois dividiam a mesma página. A
  quebra entrou junto com o texto.
- **Sigla órfã resolvida**: `DDSRF-PLL` constava da Lista de Abreviaturas
  (bloco 279) e não aparecia em nenhum outro ponto do corpo. O Eixo 1 passou
  a usá-la.
- **Zero referência nova** (decisão, não acaso): as 4 citações escolhidas já
  estavam na lista final e já eram citadas no corpo, o que manteve a
  pendência 15 do mesmo tamanho.
- **DOCX** (`C:\Temp\gen_cap7.py`): inserção após o bloco 727 (título,
  `paraId 1FB0000F`, âncora única), 2 parágrafos de corpo
  (`1FB00227`–`1FB00228`, molde do bloco 725) mais a quebra de página
  (`1FB00229`, molde do 726). 775 → 778 parágrafos (delta +3). TOC marcado
  `w:dirty`.
- **Verificado**: `check_pt.py` sem nenhum flag nos blocos novos (todos os
  achados são pré-existentes: lista de siglas, placeholders, `onde` do
  Cap. 4); texto reconstruído a partir do XML final e conferido contra o
  aprovado; `word_finalize.ps1` (**79 páginas**, 16 390 palavras, 0 campo com
  erro, Word salvou); `audit_docx.py --util-in 6.30` = **0 falhas / 0 avisos**.
- **Entregue**: 3 694 150 bytes, MD5 `91c13b5c...` (pré-check do destino
  `3ecb43eb...` conferido contra o staging antes de sobrescrever). Backup
  `..._backup_20260912_203154.docx`.
- **Destrava a pendência 20**: com o capítulo escrito, o Word conta 79
  páginas, então o `XX` f. da ficha catalográfica pode ser fechado (falta só
  confirmar com o Oscar qual contagem a ficha usa).

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

## Entregas de setembro/2026 até o dia 09

Ver `historico_entregas_2026_09_inicio.md` — troca de terminologia
PAC → PCC (2026-09-09), mesclagem dos Cap. 4 e 5 do fragmento no
canônico e enxugamento analítico do Cap. 5 (ambas de 2026-09-02).

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
