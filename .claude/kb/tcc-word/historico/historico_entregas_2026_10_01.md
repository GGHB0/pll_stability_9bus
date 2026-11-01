---
name: tcc-historico-entregas-2026-10-01
description: Entregas de 2026-10-01 no V10 — safra de 01/10 no Cap. 5, texto antes das figuras, reaquisitar, citações e referências do Oscar
aliases: [tcc-historico-entregas-2026-10-01]
---

# TCC Word — Entregas de 2026-10-01

> Fragmentado de [[tcc-historico-entregas]] em 2026-10-02 por limite de
> 200 linhas. Ordem: mais recente primeiro.

## 2026-10-01 (23h30) — "Reaquisitar" fora do texto (V10)

- 14 trocas por "recuperar/retomada do sincronismo" (Cap. 4 a 7), segmento a
  segmento nos `<w:t>` (`C:\Temp\figs\gen_reaquisita.py`). Três já tinham
  virado "requisitar" no Word, que também está errado. Comentário `[Claude]`
  em cada trecho; "Feito." no do Oscar ("Acho que essa palavra não existe").
- O Victor reverteu a decisão de 2026-09-12 de manter a palavra; regra em
  `revisao_pt.md` da skill. 1ª entrega abortou por MD5 (save sincronizado,
  texto idêntico) → backup `V10_backup_20261001_233613`.

## 2026-10-01 (23h59) — Texto antes das figuras nos Caps. 4 e 5 (V10)

- 19 parágrafos "A Figura X…" movidos (`w:p` inteiro, âncoras do Oscar
  junto) para antes da legenda: Figuras 4.1-4.3, Tabela 4.1 e todo o Cap. 5;
  pares 5.1/5.2, 5.5/5.6 e 5.10/5.11 com o texto acima do par. Regra nova no
  item 6 de `padroes_revisao.md` da skill tcc-docx-editor.
- Remissões com número antigo corrigidas: 5.5→5.6, 5.6→5.8, 5.12→5.15,
  5.4→5.5, 5.13→5.17, 5.15→5.19 e o par 5.12/5.13→5.16/5.17.
- Figuras 5.10/5.11 reescritas: mesmas escalas de tempo e de amplitude;
  v_d de −0,02 a 1,35 pu (nominal) contra 0,30 a 1,32 pu (inadequada).
- Números do Cap. 5 reconferidos com `medir_cap5.py`, todos batem (falta de
  0,3 a 0,4 s nos 28 cenários). Duas ressalvas viraram texto: 120 Hz ≤
  0,002 pu e "duas ordens de grandeza" só com sintonia nominal (a trifásica
  da Barra 6 inadequada dá 0,006 pu); §5.5, prolongamento da recuperação
  só "nas contingências mais severas".
- 4 comentários `[Claude]` e resposta ao Oscar no "tensão em regime
  permanente está em 1 p.u." (as duas sintonias partem de 1,00 pu).
- **Pipeline**: `C:\Temp\figs\gen_figuras_antes.py` (refeito sobre o save do
  Victor das 23h52) → finalize (78 págs) → audit 0 falhas → backup
  `V10_backup_20261001_235907`.

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
