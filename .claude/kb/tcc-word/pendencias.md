---
name: tcc-pendencias
description: Pendências do TCC priorizadas em P1/P2/P3: estruturais, conteúdo, limpeza, fora de escopo
aliases: [tcc-pendencias]
---

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
   no lugar das sobras do template; RBI/ICR padronizados em IBR. Revisada em
   2026-09-13: 36 siglas, só as usadas no texto (GFM, SOTF, COI, FFR, BESS, TSO,
   DSO, SCR agora na lista). Ver `siglas_inventory.md`.
5. **~~REFERÊNCIAS sem estilo de título~~** — ✅ FEITO (2026-09-13): virou
   `Ttulo1` centralizado e entra no sumário, junto com ANEXOS. Ver `abnt_layout.md`.

## P2 — Conteúdo pendente

6. **Cap. 5 (Resultados) quase vazio no canônico** — ver item 18 (P2) para o
   estado atual: já redigido no fragmento externo, falta mesclar.
   **Salto de fase NÃO implementar** — instrução do Oscar.
7. **Referências MATLAB/PSIM** — Oscar comentário #9, seção 4.2 (Plataformas).
   Citar MathWorks (MATLAB) e Powersim Inc. ou artigo (PSIM). **Ficou mais
   urgente em 2026-09-12**: a entrada `SOUSA, et al. 2021 [PSIM]` foi removida
   da lista por ser órfã (o §4.2 reescrito não cita mais ninguém), então hoje
   o PSIM aparece no texto sem nenhuma referência.
8. **Acentuação da seção 4.3.4** (ex-3.3, Protocolos) — texto adicionado sem
   acentos; corrigir em futura edição.
9. **~~Typo em referência MOW→MOHAN~~** — ✅ FEITO (2026-07-19), corrigido nos 2 lugares.
10. **Versão do MATLAB no 4.3.3** — escrito "R2025a" (inferido do ConfigSet
    25.0 do .slx); confirmar com Bruno a versão real usada nas simulações.
15. **Referências novas de 2.1-2.4.3 faltando na lista final** — texto
    redigido 2026-07-19 cita IEA (2026), KUNDUR et al. (2004), GU; GREEN
    (2023), STRAUSS-MINCU et al. (2026), ENTSO-E (2026), COORDINADOR
    ELÉCTRICO NACIONAL (2025) e ONS (2023); nenhuma está na seção de
    Referências ainda. Ver `content_map.md` (Cap.2) para o detalhe de cada
    citação e o KB-fonte correspondente.

16. ~~**Ano da CIGRE CSE N037**~~ — ✅ RESOLVIDO (2026-09-12): a edição N°37
    da CIGRE Science & Engineering é de **junho de 2025**, e o artigo foi
    elaborado por M. Lindner, H. Abele, C. John, J. Lehner, K. Vennemann,
    T. Hennig, R. Dimitrovski, N. Klötzl, H. Just e R. Stornowski (fonte:
    cse.cigre.org/cse-n037). A entrada foi fechada como `… n. 37, jun. 2025.
    Elaborado por M. Lindner et al.` e o §2.3 passou a `(CIGRE, 2025)`.
17. ~~**Tempos de falta a re-simular**~~ — ✅ RESOLVIDO (2026-08-11/12): a
    lacuna de falta assimétrica com sintonia inadequada foi preenchida
    (`bus6`/`bus7` × 1phase/2phase_bad_pll). **Mas ver achado novo em
    2026-08-22**: esses cenários são de uma safra de modelo diferente da dos
    `_bad_pll` trifásicos/regime de julho (`v_d` pré-falta 0,99 vs. 0,80 pu) —
    só a safra de agosto é pareável com os nominais. Detalhe completo em
    `kb/simulation/cenarios_simulados.md` § Duas safras de modelo e em
    `kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5.md`.

18. **Cap. 5 canônico segue vazio** (5.1.1 só tem "."; 5.1.2, 5.3.1, 5.3.2
    com placeholders) — o fragmento `capitulos_4_5_revisados.docx` já tem
    esse capítulo redigido por completo, com números medidos e figuras
    inseridas. Ver `kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5.md` para o texto e a
    tese aplicada (compromisso de banda passante, sem *cycle slipping*
    observado); mesclagem no canônico ainda não tem data.

19. ~~**Cap. 7 (Trabalhos Futuros) vazio**~~ — ✅ **RESOLVIDO (2026-09-12,
    noite)**: dois parágrafos inseridos (311 palavras, blocos 728-729), mais a
    quebra de página antes do REFERÊNCIAS, que não existia (o título do Cap. 7
    e o início das referências dividiam a mesma página). Eixo 1 (estrutura de
    sincronismo) e Eixo 3 (varredura de SCR/múltiplos IBR), conforme
    [[tcc-trabalhos-futuros]]. **Zero referência nova**: as 4 citações já
    constavam da lista e já eram citadas no corpo.

20. **`XX` f. na referência do resumo** — ✅ preenchido com **74 f.** em
    2026-09-13, o total de folhas do PDF depois da passagem ABNT. O `XX`
    estava na referência bibliográfica do RESUMO, não na ficha (que a
    biblioteca emite). **Ainda confirmar com o Oscar** se conta o total de
    folhas ou a última folha numerada (hoje 73), e atualizar se o documento
    mudar de tamanho.
25. **Comentário 16 do Oscar (Motivação, Xiong et al. 2025) aberto** — duas
    tentativas rejeitadas e revertidas em 2026-09-26 ([[tcc-historico-entregas]],
    noite 6-8). Victor quer manter "modelagem identificada pelo ONS" e só
    acrescentar a citação. Opções no chat, **aguardando escolha**: A) "...pelo
    ONS (XIONG et al., 2025), explicando..."; B) "...pelo ONS e discutida por
    Xiong et al. (2025), explicando...". Não tocar no Word sem o ok.

## P3 — Limpeza

11. **~~Figuras Cap. 2/3~~** — ✅ FEITO (2026-09-13): as imagens já estavam
    no documento; os placeholders viraram Gráficos 2.1-2.3 e Figura 3.1, com
    fonte, e o SRF-PLL virou a Figura 3.2 autoral. Ver `abnt_layout.md`.
12. **Lista de referências final** — mistura template UERJ + refs reais.
    Remover entradas do template.
13. **Cor legada `1B1C1D`** (cinza quase preto do template) ainda presente em
    títulos herdados do V8 — limpar para preto/auto na próxima edição.
14. ~~**Tracked change restante** no título "2.6. Resumo ou Conclusões do
    Capítulo"~~ — ✅ RESOLVIDO: `check_ids.py` em 2026-09-12 mostra o documento
    sem nenhum `w:ins` e sem nenhum `w:del`.
21. **ANEXOS sem conteúdo** — título sozinho na última folha e no sumário.
    Escrever os anexos ou remover a seção (decisão dos autores).
22. **Dedicatória e epígrafe** — marcadores "Dedicatória opcional." e "Frase
    opcional. / Autor" nas folhas 5 e 7, à espera do texto dos autores.
23. **Subseções do Cap. 1 fora do sumário** — "Contextualização", "Motivação
    e Justificativa" e "Objetivos do Trabalho" são itens de lista numerada
    ("1.", "2."), não `Ttulo2`: não aparecem no sumário e fogem da NBR 6024
    ("1.1"). Mexe na estrutura, então só com aval.
24. **Título gravado dentro da imagem** — pelo menos Figura 3.1, Figura 4.3,
    Quadro 4.1 e Gráfico 2.3 repetem a legenda como título no próprio bitmap;
    a ABNT põe o título só na legenda. Reexportar dos SVGs de
    `assets/diagrams/` sem o `<text>` do título.

## Fora de escopo (instrução do Oscar)

- Salto de fase (phase-angle jump) — não implementar
- Alto RoCoF — não implementar
- Métricas de desempenho (passo iv do Cap. 3) — pendente decisão do Oscar
