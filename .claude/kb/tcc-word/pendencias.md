# TCC Word — Pendências Priorizadas

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de 200 linhas.
> Mapa completo seção a seção: `content_map.md`.

## P1 — Correções estruturais (rápidas, alto impacto)

1. **[FIGURA 3.1] sem placeholder** — referenciada 2× em 3.2.2 (§215 e §220)
   mas o placeholder não existe no texto. Inserir placeholder italic-centralizado:
   `[FIGURA 3.1 – Circuito do VSI trifásico de dois níveis com filtro LCL e blocos de controle PWM.]`
   após o parágrafo §220 (após "...é ilustrado na Figura 3.1").
2. **~~Estilo errado em 2.4.1/2.4.2/2.4.3~~** — ✅ FEITO (gen_oscar_fixes.py): Clarke, Park,
   Arquitetura de Controle e PWM agora são Ttulo3 (tracked change).
3. **Seção sem número** — "A Necessidade das Transformadas de Referência" é `Ttulo2`
   antes de 2.1, sem numeração. Renumerar como "2.0" ou rebaixar a corpo.
   **NÃO alterar sem confirmação do Oscar/Victor.**
4. **~~Lista de Abreviaturas vazia~~** — ✅ FEITO (2026-07-19): 31 siglas inseridas
   no lugar das sobras do template; RBI/ICR padronizados em IBR. Ver `siglas_inventory.md`.
5. **REFERÊNCIAS sem estilo de título** — o parágrafo "REFERÊNCIAS" (§663) não
   tem `pStyle` de heading, então fica fora do Sumário. ABNT pede no sumário.
   Aplicar Ttulo1 (ou estilo próprio sem numeração de capítulo) em edição futura.

## P2 — Conteúdo pendente

6. **Cap. 4 quase vazio** (numeração antiga; Cap. 5 no índice novo) — só títulos;
   4.1.1 contém apenas ".". Prioridade do TCC.
   A redigir: 4.1.1, 4.1.2, 4.2.1, 4.3.1, 4.3.2.
   **4.2.2 (salto de fase) NÃO implementar** — instrução do Oscar.
7. **Referências MATLAB/PSIM** — Oscar comentário #9, Seção 3.1. Citar MathWorks
   (MATLAB) e Powersim Inc. ou artigo (PSIM).
8. **Acentuação da Seção 3.3** — texto adicionado sem acentos; corrigir em futura edição.
9. **~~Typo em referência MOW→MOHAN~~** — ✅ FEITO (2026-07-19), corrigido nos 2 lugares.

## P3 — Limpeza

10. **Figuras Cap. 2** — [FIGURA 2.1], [FIGURA 2.6] e 2 figuras ONS já têm placeholder
    de texto; substituir por imagens quando disponíveis.
11. **Lista de referências final** — mistura template UERJ + refs reais [1]–[9].
    Remover entradas do template.
12. **Cor legada `1B1C1D`** (cinza quase preto do template) ainda presente nos
    títulos 2.5, 3.1, 3.2, 3.3, 3.4 — limpar para preto/auto na próxima edição.
13. **Tracked change restante**: título "2.6. Resumo ou Conclusões do Capítulo"
    ficou sem aceite no Word (w:ins ids 23–26) — aceitar na próxima revisão.

## Fora de escopo (instrução do Oscar)

- Salto de fase (phase-angle jump) — não implementar
- Alto RoCoF — não implementar
- Métricas de desempenho (passo iv do Cap. 3) — pendente decisão do Oscar
