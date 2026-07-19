# TCC Word — Equações: Formato e Inventário

> Reformatação aplicada em 2026-07-19 (edição direta, sem tracked changes),
> aprovada pelo Victor: texto explicativo em cima, equação centralizada,
> número "EQUAÇÃO N.M" no fim da linha.

## Formato padrão (tabela invisível)

Cada equação de destaque vive numa **tabela de 2 colunas sem bordas**
(`w:val="nil"` nas 6 bordas), largura total 9072 twips (16 cm úteis do A4):

- Coluna 1 (7087 twips): parágrafo `jc=center` com o `<m:oMathPara>` —
  preserva o estilo *display* (frações grandes), que se perderia no método
  de tabulações (math inline encolhe).
- Coluna 2 (1985 twips): parágrafo `jc=right`, `vAlign=center` na célula,
  run normal `szCs=24` com o rótulo `EQUAÇÃO N.M`.

Armadilha: **duas tabelas adjacentes se fundem no Word** — sempre deixar um
`<w:p>` (pode ser vazio) entre tabelas consecutivas (feito entre 3.2 e 3.3).

## Numeração (por capítulo do novo índice)

| Nº | Conteúdo | Seção |
|---|---|---|
| 3.1–3.3 | Clarke: matricial, vα, vβ | 3.1.1 |
| 3.4–3.7 | Park: rotação αβ→dq, abc→dq, vd, vq | 3.1.2 |
| 3.8–3.9 | P e Q em dq; caso vq=0 | 3.1.3 |
| 3.10–3.17 | Modelo linearizado SRF-PLL: Kpd, PD, PI, integrador, L(s), G_PLL(s), E(s), vq(s) | 3.4 |
| 4.1 | L₁ = V_dc / (24·f_sw·ΔI_max) — ripple (notebook, Alves 2021) | 4.2.2 |
| 4.2 | ω_res = √((L₁+L₂)/(L₁·L₂·C_f)) — ressonância LCL | 4.2.2 |

- Os rótulos antigos "EQUAÇÃO 2.N — descrição" (2.5–2.12) viraram texto
  explicativo "Descrição:" acima da tabela; renumerados 2.N → 3.(N+5).
- As 9 equações da seção 3.1 não tinham número — ganharam 3.1–3.9.
- **4.1 e 4.2 são novas**: o texto do Cap.4 citava "Equação (3.1)/(3.2)"
  inexistentes; equações inseridas (fórmulas do notebook de dimensionamento)
  e citações atualizadas para (4.1)/(4.2).
- Referência cruzada no Cap.5 atualizada: "Seção 2.4 (Equações 2.9 e 2.10)"
  → "Seção 3.4 (Equações 3.14 e 3.15)".

## Notas

- Corredores de ~20 espaços nas equações P/Q lado a lado (3.8, 3.9) foram
  encurtados para 3 em-spaces para caber na coluna de 12,5 cm.
- Novos OMML (4.1/4.2) usam Cambria Math, `szCs=24`, mesmos `ctrlPr` do
  padrão existente; helpers `mr/ssub/frac/rad` em `C:\Temp\gen_eq_format.py`.
- Pipeline completo: `gen_eq_format.py` → `verify_eqfmt.py` → `repack_eqfmt.py`.
