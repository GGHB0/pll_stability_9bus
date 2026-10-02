---
name: tcc-historico-entregas-2026-10-01
description: Entregas de 2026-10-01 (dia) no V10 — citações de alto risco corrigidas e referências pedidas pelo Oscar
aliases: [tcc-historico-entregas-2026-10-01]
---

# TCC Word — Entregas de 2026-10-01 (dia)

> Fragmentado de [[tcc-historico-entregas]] em 2026-10-02 por limite de
> 200 linhas. Ordem: mais recente primeiro.

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
