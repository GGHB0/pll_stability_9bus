---
name: tcc-historico-entregas-2026-10-25
description: Entregas ao TCC de 25 a 31/10/2026: sigla pedida pelo Oscar fora, revisão do Cleiton em vermelho, 1ª rodada Rafael/André
aliases: [tcc-historico-entregas-2026-10-25]
---

# TCC Word — Entregas de 2026-10-25 a 2026-10-31

Continuação de [[tcc-historico-entregas]]. Mais recente primeiro.

## 2026-10-31 (22h39) — Banca: Rafael em azul, André em verde (1ª rodada)

Cores da revisão da banca: Cleiton `FF0000` (Bruno), Rafael `0070C0`, André
`00B050`; pinta só o texto alterado. Script em
`C:\Temp\tcc_banca_rafael_andre\gen_banca_r7_a3.py`; backup da origem em
`_backups\VF\..._backup_20261031_223646.docx`.
- **R7 (azul):** §3.3.3 ganhou a teoria p-q do bloco de P e Q, Eq. (3.1)
  e ref. AKAGI; WATANABE; AREDES (2017, 2. ed.; o PDF da Bibliografia
  se chama "2007_..." mas é a 2ª ed.). Ver [[simulink-model]].
- **A3 (verde):** §3.3.3, método da FFT: 2 ciclos descartados, 3 ciclos
  (50 ms) analisados, Hann, df = 20 Hz. O código usa 3 dos 4 ciclos que
  sobram (opção "descrever como está", aprovada; números do Cap. 4 intactos).
- **Vermelho (resto da renumeração do Cleiton):** rótulos e 38 menções
  (3.N) → (2.N) no Cap. 2; legenda da Figura 3.3 (ONS) virou campo SEQ (era
  texto fixo e, com os campos atualizados, dava duas 3.3); 5 runs com espaço
  de borda sem `xml:space` ("AFigura", "ressalvas.As") recebem preserve.
- **Pendentes da banca:** R1 GitHub (CITATION.cff no repositório; DOI do
  Zenodo a caminho; URL do TCC dá 404), R2, R3 GFL×GFM, R4/R9 DSOGI,
  R5 2º parágrafo da Introdução, R6 gráficos e componentes simétricas,
  R8 Roteiro UERJ, A2 Mvar na
  Figura 3.1; Apêndice A com afirmações a corrigir.

## 2026-10-31 — Revisão da banca examinadora (Prof. Cleiton) com alterações em vermelho

Atendimento integral aos apontamentos do Prof. Cleiton (leitura, apresentação oral e anotações a caneta no PDF). 100% das alterações ressaltadas na cor VERMELHA (#FF0000):
- Padrão UERJ: Introdução e Conclusão sem indicativo numérico, seções 1 a 4 em caixa alta, Trabalhos Futuros como subseção da Conclusão.
- Seção 2.3.2: Deslocamento da arquitetura de controle, explicação da divisão dos ganhos por 4 (Zbase = 4,0 Ω) e remissões corrigidas das Figuras 2.1 e 2.2.
- Seção 3.3.1: Cálculo formal de Scc = 914,2 MVA, SCR = 9,14 e classificação de rede forte (IEEE Std 1204 / CIGRE TB 671).
- Seções 2.4 e 3.3.2.3: Formulação analítica de largura de banda do SRF-PLL (Teodorescu) e valores nominais (106,5 Hz) e inadequados (38,5 Hz).
- Seções 1.5.2 e 3.3.2: Lógica do Submódulo 2.10 do ONS (Figura 3.3), priorização de corrente reativa com saturação quadrática e renumeração da Figura 3.4.
- Conclusão: Premissa de elo CC ideal e linha de MPPT/controle CC em Trabalhos Futuros.
- Apêndice A: Painel interativo com visão geral e sequência de telas guiadas em 1080p (Figuras A.1 a A.5).
- Referências, pontuação e texto: 5 novas referências (CEN, Gu & Green, IEA, Kundur, GitHub), pontuação nas Equações (3.1) a (3.23), termos em itálico e correções textuais.
Backup datado em _backups\Revisao_Banca_Cleiton_Vermelho_Total.

## 2026-10-25 — Sigla de transitórios eletromagnéticos fora do TCC (pedido do Oscar)

5 trocas no VFinal, todas em texto bruto: Resumo ("simulação computacional
de transitórios eletromagnéticos"), Abstract (espelho, sem comentário: o
VFinal não tem comentários e ficou assim), objetivo específico 2, dois
trechos da Conclusão ("simulações computacionais"). A sigla não estava na
lista de siglas. fb061b4a… → a69b1839c7f0faf1d6ff5801a6d2ff43, backup
`_backups\VF\..._20261025_162820`. `diff_texto.py`: 5 trechos, 813 → 813
parágrafos, comentários 0 → 0. O PDF ao lado do VFinal não foi regerado.

## Relacionados

- [[tcc-historico-entregas]] — entregas mais recentes (banca, novembro)
