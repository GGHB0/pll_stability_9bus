# TCC Word — Pendências Priorizadas

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de 200 linhas.
> Mapa completo seção a seção: `content_map.md`.

## P1 — Correções estruturais (rápidas, alto impacto)

1. **[FIGURA 3.1] sem placeholder** — referenciada 2× na seção 4.3.2
   (numeração nova) mas o placeholder não existe no texto. Inserir placeholder
   italic-centralizado:
   `[FIGURA 3.1 – Circuito do VSI trifásico de dois níveis com filtro LCL e blocos de controle PWM.]`
   após o parágrafo "...é ilustrado na Figura 3.1".
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

6. **Cap. 5 (Resultados) quase vazio** — 5.1.1 contém apenas "."; prioridade
   do TCC. A redigir: 5.1.1, 5.1.2, complementos de 5.2.1, 5.3.1, 5.3.2
   ([RESULTADOS A INSERIR] / [A COMPLEMENTAR]).
   **Salto de fase NÃO implementar** — instrução do Oscar.
7. **Referências MATLAB/PSIM** — Oscar comentário #9, seção 4.2 (Plataformas).
   Citar MathWorks (MATLAB) e Powersim Inc. ou artigo (PSIM).
8. **Acentuação da seção 4.3.4** (ex-3.3, Protocolos) — texto adicionado sem
   acentos; corrigir em futura edição.
9. **~~Typo em referência MOW→MOHAN~~** — ✅ FEITO (2026-07-19), corrigido nos 2 lugares.
10. **Versão do MATLAB no 4.3.3** — escrito "R2025a" (inferido do ConfigSet
    25.0 do .slx); confirmar com Bruno a versão real usada nas simulações.

## P3 — Limpeza

11. **Figuras Cap. 2/3** — [FIGURA 2.1], [FIGURA 2.6] e 2 figuras ONS já têm
    placeholder de texto; substituir por imagens quando disponíveis (e
    renumerar figuras para os capítulos novos).
12. **Lista de referências final** — mistura template UERJ + refs reais.
    Remover entradas do template.
13. **Cor legada `1B1C1D`** (cinza quase preto do template) ainda presente em
    títulos herdados do V8 — limpar para preto/auto na próxima edição.
14. **Tracked change restante**: título "2.6. Resumo ou Conclusões do Capítulo"
    ficou sem aceite no Word (w:ins ids 23–26) — aceitar na próxima revisão.

## Fora de escopo (instrução do Oscar)

- Salto de fase (phase-angle jump) — não implementar
- Alto RoCoF — não implementar
- Métricas de desempenho (passo iv do Cap. 3) — pendente decisão do Oscar
