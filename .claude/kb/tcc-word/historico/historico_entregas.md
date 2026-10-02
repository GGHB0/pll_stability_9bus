---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-10-01 (23h) — Gráficos de erro de fase no Cap. 5 (V10)

- 4 figuras novas (legenda SEQ + imagem + Fonte via `campos.py` + parágrafo
  de chamada): 5.3 energização, 5.7 trifásicas nominais, 5.12 assimétricas,
  5.16 perda de sincronismo. Cap. 5 passou a 19 figuras, documento a 77
  págs. Mapa em [[tcc-revisao-fragmento-cap5-figuras]].
- Citações em texto fixo renumeradas num passo único pelo mapa antigo→novo.
  **Armadilha:** o Word partiu "A Figura " | `proofErr` | "5.9 mostra" em
  runs separados; o regex por `<w:t>` não pegou e a chamada ficou errada até
  a conferência legenda × chamada. Tratar o caso partido antes do passo geral.
- "Feito." nos 4 pedidos de gráfico angular do Oscar; 4 comentários
  `[Claude]`. Rótulo do painel vazio do gerador virou "fora da comparação".
- 1ª entrega abortou por MD5 (OneDrive sincronizou o save do Word ao fechar;
  texto idêntico). Refeito sobre a versão nova → backup
  `V10_backup_20261001_230942`.

## 2026-10-01 (22h30) — Texto do Cap. 5 para a safra de 01/10 (V10)

- 26 trocas por paraId, segmento a segmento dentro de `<w:t>`, preservando
  as âncoras do Oscar (`C:\Temp\figs\gen_texto_cap5.py`; métricas de
  `medir_cap5.py`, receita de [[tcc-revisao-fragmento-cap5-metricas]]).
- Muda a tese da §5.3: a sintonia inadequada recupera **mais rápido** nas
  assimétricas da Barra 6 (30/31 ms × 48/39 ms; ondulação de Q 4,8→3,0 pu) e
  mais devagar na bifásica da Barra 7 (51→96 ms) e na trifásica da Barra 6
  (76→106 ms); o compromisso passa a depender da severidade. Saiu o "ponto
  de operação degradado" (regime inadequado converge a 1,00 pu, 79 ms), saiu
  o par monofásico da Barra 7 (reprovado), a Linha 7-8 entrou na perda de
  sincronismo (§5.4) e a janela pós-falta passou a 200 ms (Cap. 4 bloco 487
  e §5.4).
- 15 comentários `[Claude]`, um por trecho; "Feito." nos do Oscar sobre
  grandeza/ordem de grandeza, tensão degradada, ponto de operação, escala de
  tempo e 0,823 pu. O "Não entendi." ficou sem resposta (dois comentários
  com o mesmo início). Cap. 6 não foi tocado.
- Finalize (74 págs) → audit 0 falhas → backup `V10_backup_20261001_223143`.

## 2026-10-01 (22h) — Gráficos da safra de 01/10 no V10

- Troca só da mídia (`word/media/imageN.png`) de 12 ilustrações pelos PNGs
  regenerados: Tabela 4.1 (`image11`), Figuras 5.1-5.3 (`image12`-`14`) e
  5.8-5.15 (`image19`-`26`). Proporções idênticas, `cy` inalterado. As
  Figuras 5.4-5.7 já eram iguais a `assets/`. Mapa em
  [[tcc-revisao-fragmento-cap5-figuras]].
- **Texto não mexido**: comentário `[Claude]` na abertura do Cap. 5 avisa da
  troca e dos números antigos (563→79 ms; 34,9°/78 ms→34,5°/30 ms; Linha 7-8
  trifásica também perde sincronismo). Revisão dos números fica pendente,
  com tabela em [[cenarios-simulados]]. Gráficos `erro_fase_*` não inseridos.
- **Pipeline**: `C:\Temp\figs\gen_troca_figuras.py` → finalize com
  `-Comments` (74 págs) → audit 0 falhas → backup `V10_backup_20261001_222015`.

## 2026-10-01 (noite) — Referências pedidas pelo Oscar (V10)

- **Comentários 88, 34, 118 e 140** (pedidos de referência), cada citação no
  fim do trecho ancorado: Clarke 3.1.1 → (YAZDANI; IRAVANI, 2010); "IEEE
  TR77" → (HATZIARGYRIOU et al., 2020); "ωn = 4√2·fg ≈ 339,4 rad/s" →
  (ALVES, 2022); "IEEE 9 barras" → (ANDERSON; FOUAD, 2003; MATHWORKS, 2025).
- **Lista**: entradas novas HATZIARGYRIOU (PES-TR77, maio 2020) e MATHWORKS
  (página "IEEE 9-Bus System", R2025b, que cita Anderson & Fouad como fonte
  dos dados), ambas conferidas na web; paraIds `1FB00310`/`1FB00311`.
- Ficou aberto: "pequena descrição das equações" (2ª metade do 88) e o 44
  (Bruno traz a referência). O 7 já estava atendido (Strauss-Mincu/Shadoul).
- **Pipeline**: `gen_refs_oscar.py` → finalize (74 págs) → audit 0 falhas →
  backup `V10_backup_20261001_204412`. Duas tentativas abortaram por MD5
  (sync de outro aparelho em rajada); lição na seção Entrega da skill.

## 2026-10-01 — Citações de alto risco corrigidas (V10)

- Os 4 trechos de alto risco de [[tcc-revisao-citacoes]], conferidos de novo
  contra os PDFs antes de aplicar:
  - **Cap. 1, flutuação/armazenamento:** a frase passou a "...como a
    variabilidade da geração, que exige maior flexibilidade e capacidade
    despachável do sistema elétrico para preservar sua confiabilidade (IEA,
    2026)". Só trocar a fonte não bastava, porque a IEA p. 12 não fala de
    armazenamento nem de estabilidade dinâmica.
  - **Leis físicas:** "...cujo sincronismo é regido por leis físicas
    inerentes à máquina rotativa (WU; WANG, 2020; XIONG et al., 2025)".
  - **IBRs sem inércia:** a citação passou de Wu e Wang para (STRAUSS-MINCU
    et al., 2026).
  - **Cap. 2, inércia → desvios angulares:** "...a inércia total da rede
    diminui, o que torna mais complexa a manutenção da estabilidade e exige
    que os requisitos de estabilidade transitória do sistema elétrico sejam
    reavaliados (STRAUSS-MINCU et al., 2026)" (p. 95 e 101). O início,
    ancorado nos comentários 105/106, ficou intacto.
- **Sem RoCoF:** a primeira versão do último trecho citava RoCoF (p. 106). O
  Victor vetou, porque RoCoF não é assunto do TCC.
- **MOHAN (2003) removido da lista**: ficou sem citação. O Victor confirmou
  que a citação foi um engano dele.
- **Pipeline**: `gen_citacoes_risco.py` (5 edits; a 1ª execução abortou no
  trecho dos IBRs porque o padrão pulava o run do `commentReference` 12) →
  finalize (74 págs, 0 erro) → audit 0 falhas → MD5 `284f6afc…` conferido →
  backup `_backup_20261001_193644` → entregue (`fd4b7f3c…`).

## Entregas de 2026-09-27 a 2026-09-29

Ver [[tcc-historico-entregas-2026-09-fim]]: citação de "redes fracas" para Wu
e Wang, Xiong na Motivação (comentário 16) e 38 comentários novos do Oscar
mesclados no Cap. 5.

## Entregas de 2026-09-26

Ver [[tcc-historico-entregas-2026-09-26]]: comentários do Oscar no V10
(notação do PLL, Resumo/Abstract, figuras ONS), comentário 16 com o Xiong
(duas tentativas revertidas) e siglas definidas uma vez só.

## Entregas de 2026-09-13

Ver [[tcc-historico-entregas-2026-09-13]]: passagem ABNT completa, lista de
siglas revisada contra o texto, subscrito nos símbolos do texto corrido.

## Entregas de 2026-09-12

Ver `historico_entregas_2026_09_12.md`: referências em amarelo fechadas,
revisão de português do documento inteiro, Cap. 7 e Cap. 6 redigidos.

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

## Relacionados

- [[tcc-historico-entregas-2026-08]] — histórico detalhado de agosto
- [[tcc-historico-entregas-2026-09-26]] — entregas de 2026-09-26 (V10)
