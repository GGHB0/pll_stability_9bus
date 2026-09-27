---
name: tcc-equacoes
description: Equações do TCC: formato em tabela invisível, numeração por capítulo, lista completa 3.1-4.2
aliases: [tcc-equacoes]
source: TeseAGP p.42-43 eqs. (3.20)-(3.22) e (3.26), p.84 Fig. 4.5
references:
  - "ALVES, André Gustavo Pereira. Metodologia para Auto-Ajuste de Controladores de Corrente em Conversores Fonte de Tensão Conectados a Redes Sujeitas a Distúrbios Harmônicos. Tese (Doutorado em Engenharia Elétrica) — COPPE/UFRJ, Rio de Janeiro, 2022."
---

# TCC Word — Equações: Formato e Inventário

> Reformatação aplicada em 2026-07-19 (edição direta, sem tracked changes),
> aprovada pelo Victor: texto explicativo em cima, equação centralizada,
> número no fim da linha. **Desde 2026-09-13 o rótulo é `(N.M)`** (NBR 14724;
> decisão D7 da skill `tcc-abnt-layout`); até então era "EQUAÇÃO N.M".

## Formato padrão (tabela invisível)

Cada equação de destaque vive numa **tabela de 2 colunas sem bordas**
(`w:val="nil"` nas 6 bordas), largura total 9072 twips (16 cm úteis do A4):

- Coluna 1 (7087 twips): parágrafo `jc=center` com o `<m:oMathPara>` —
  preserva o estilo *display* (frações grandes), que se perderia no método
  de tabulações (math inline encolhe).
- Coluna 2 (1985 twips): parágrafo `jc=right`, `vAlign=center` na célula,
  run normal `szCs=24` com o rótulo `(N.M)`. Equação nova usa esse
  formato, não o antigo `EQUAÇÃO N.M`.

Armadilha: **duas tabelas adjacentes se fundem no Word** — sempre deixar um
`<w:p>` (pode ser vazio) entre tabelas consecutivas (feito entre 3.2 e 3.3).

## Numeração (por capítulo do novo índice)

| Nº | Conteúdo | Seção |
|---|---|---|
| 3.1–3.3 | Clarke: matricial, vα, vβ | 3.1.1 |
| 3.4–3.7 | Park: rotação αβ→dq, abc→dq, vd, vq | 3.1.2 |
| 3.8–3.9 | P e Q em dq; caso vq=0 | 3.1.3 |
| 3.10–3.17 | Modelo linearizado SRF-PLL: Kpd, PD, PI (K_pPLL, K_iPLL), integrador, L(s), G_PLL(s), E(s), vq(s) | 3.4 |
| 3.18 | Forma canônica de 2ª ordem: G(s) = (2ξω_n·s + ω_n²)/(s² + 2ξω_n·s + ω_n²) | 3.4 |
| 3.19 | Projeto do PLL: K_iPLL = ω_n² e K_pPLL = 2ξω_n | 3.4 |
| 3.20 | Acomodação (critério 1%): t_s = 4,6/(ξω_n) e K_pPLL = 9,2/t_s | 3.4 |
| 3.21 | Planta de corrente por eixo: G(s) = 1/(s·Lest) | 3.5 (nova) |
| 3.22 | Malha fechada com PI: s² + (Kp/Lest)·s + (Ki/Lest) = 0 | 3.5 (nova) |
| 3.23 | Projeto do controlador de corrente: Kp = 2ξω_n·Lest e Ki = ω_n²·Lest | 3.5 (nova) |
| 4.1 | L₁ = V_dc / (24·f_sw·ΔI_max) — ripple (notebook, Alves 2021) | 4.3.2.1 |
| 4.2 | ω_res = √((L₁+L₂)/(L₁·L₂·C_f)) — ressonância LCL | 4.3.2.1 |

**Próximo número livre: 3.24** (Cap. 3). Cap. 4 não ganhou equação nova nesta
rodada — a fórmula do controlador de corrente migrou para o Cap. 3 (ver nota
abaixo).

- **3.21–3.23 (2026-08-05, nova §3.5)**: aplicam a estratégia "sintonia
  teórica vs. aplicação prática" também ao controlador de corrente, que até
  então só tinha a fórmula `Kp=8·fg·Lest`/`Ki=32·fg²·Lest` solta em texto
  corrido no Cap. 4 (§4.3.2.2), sem contrapartida simbólica no Cap. 3. A nova
  §3.5 deriva essas expressões como **reaplicação da mesma forma canônica de
  2ª ordem já estabelecida para o PLL (Equação 3.18)**, não como a derivação
  de cancelamento polo-zero por `Ki/Kp=R/L` (fator 4) documentada em
  `kb/inverter/agp_current_control_theory.md` — ver nota lá e em
  `kb/pll/sintonia/pll_gains_methodology.md`. §4.3.2.2 do Cap. 4 passou a citar
  "Equação (3.23)" e aplicar os parâmetros do projeto, sem rededuzir.

- Os rótulos antigos "EQUAÇÃO 2.N — descrição" (2.5–2.12) viraram texto
  explicativo "Descrição:" acima da tabela; renumerados 2.N → 3.(N+5).
- As 9 equações da seção 3.1 não tinham número — ganharam 3.1–3.9.
- **4.1 e 4.2 são novas**: o texto do Cap.4 citava "Equação (3.1)/(3.2)"
  inexistentes; equações inseridas (fórmulas do notebook de dimensionamento)
  e citações atualizadas para (4.1)/(4.2).
- Referência cruzada no Cap.5 atualizada: "Seção 2.4 (Equações 2.9 e 2.10)"
  → "Seção 3.4 (Equações 3.14 e 3.15)".

## Notação dos ganhos (2026-09-26)

Padrão aprovado pelo Victor, aplicado em texto, OMML e figuras:

- **PI do PLL:** K_pPLL / K_iPLL, com `pPLL` inteiro no subscrito e **sem
  vírgula** (o V10 tinha `K_p,PLL`; a vírgula foi removida de todas as 15
  ocorrências). Vale também para as Eqs. 3.12, 3.14 e 3.15, que usavam
  K_p/K_i. A frase "Adota-se a notação…" fica no parágrafo que abre o
  modelo linearizado (antes da Eq. 3.10), não depois da 3.17.
- **PI de corrente (saída → moduladora do SPWM):** K_p / K_i **sem sufixo**,
  como na TeseAGP (eqs. 3.21-3.22, p.42; Fig. 4.5, p.84). A tese chama o PI
  do PLL de PI_PLL e usa **PI_cc para o elo CC** (cc = corrente contínua):
  por isso não usar sufixo "c"/"cc" no controlador de corrente.
- **Frequência da rede no feed-forward do PLL:** ω_0 (como na Fig. 4.5 da
  tese); ω_n é reservado à frequência natural do laço. Figuras 3.2 e 4.3
  (`srf_pll_blocos_funcionais.svg`, `pll_control_loop.svg`) corrigidas; o
  rodapé da 4.3 trazia por engano as fórmulas do controlador de corrente
  (8·f_g…/32·f_g²…), trocadas por K_pPLL = 2ξω_n e K_iPLL = ω_n².
- **Ângulo e frequência do PLL (comentário #107 do Oscar):** θ_PLL para o
  ângulo estimado (as Eqs. 3.11, 3.13 e 3.15 usavam θ_est), ω_PLL para a
  frequência estimada e ω_0 para a nominal (o parágrafo do VCO dizia ω_nom),
  como na Fig. 3.2. θ_ref (ângulo da rede) fica.
- **Fonte de ω_n = 4√2·f_g e K_p = 8·f_g·L_est / K_i = 32·f_g²·L_est (#110/#112):**
  TeseAGP eqs. (3.20)-(3.22) p.42 e (3.26) p.43; t_ss = 4/(ξω_n) = 1/f_g
  (critério 2%). O André cita ALVES; DIAS; ROLIM 2020 [61] (2ª ordem, ξ =
  0,707), OGATA [62] e YAZDANI [27]; **Teodorescu [8] não é fonte dessas
  equações** (na tese ele entra na estrutura dq e no PI_cc). No TCC, §3.5
  cita (ALVES, 2022; YAZDANI; IRAVANI, 2010) e §4.3.2.2 remete à Eq. (3.23) (#138).
- **K_pd e normalização (2026-09-26, resolvido):** a Eq. 3.10 dizia
  K_pd = (3/2)·V_m, errado pela própria Park do TCC (Eqs. 3.5-3.7, fator
  2/3, invariante em amplitude): virou **K_pd = V_m**; o 3/2 é das equações de
  potência 3.8/3.9. A Eq. 3.10 mostra a derivação em duas linhas na mesma
  célula (sem renumerar): v_q = (2/3)·(3/2)·V_m·sin(θ_ref − θ_PLL) =
  V_m·sin(…) ≈ V_m·(θ_ref − θ_PLL) ⇒ K_pd = V_m; o parágrafo acima substitui
  v_a, v_b, v_c na Eq. (3.7) e diz que a soma das fases dá (3/2)·V_m e o 2/3
  da transformada cancela (pedido do Victor: deixar visível de onde vinha o
  3/2). Antes da Eq.
  3.19, parágrafo explícito: entrada do PLL dividida por 16.329,93 V → V_m = 1
  pu → K_pd = 1, por isso some das relações; sem normalização, dividir os
  ganhos por K_pd (TEODORESCU; LISERRE; RODRIGUEZ, 2011, §4.2.2.3 p.56). Ver
  [[pll-gains-provenance]] e [[pll-gain-voltage-dependence]].

## Notas

- Corredores de ~20 espaços nas equações P/Q lado a lado (3.8, 3.9) foram
  encurtados para 3 em-spaces para caber na coluna de 12,5 cm.
- Novos OMML (4.1/4.2) usam Cambria Math, `szCs=24`, mesmos `ctrlPr` do
  padrão existente; helpers `mr/ssub/frac/rad` em `C:\Temp\gen_eq_format.py`.
- Pipeline completo: `gen_eq_format.py` → `verify_eqfmt.py` → `repack_eqfmt.py`.
- **3.18–3.20 (2026-08-04)**: geradas por `C:\Temp\gen_pll_edits.py`
  reaproveitando os helpers do `gen_eq_format.py`. Padrões confirmados na
  verificação: `ω_n²` sai como `<m:sSubSup>` (não `sSub` + texto "2"), e duas
  relações na mesma linha são separadas por 3 em-spaces (`\u2003`), mesmo
  recurso das equações 3.8/3.9. Conferir com `C:\Temp\check_new_eqs.py`, que
  extrai `<m:t>` e conta `m:f`/`m:sSub`/`m:sSubSup` por equação.

## Relacionados

- [[tcc-full-cap2]] — capítulo que contém as equações 3.1–3.9
- [[tcc-full-cap3]] — capítulo que contém as equações 3.10–3.23
