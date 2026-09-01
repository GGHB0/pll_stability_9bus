# Figuras Didáticas

Desmembrado de `README.md` em 2026-09-01 (limite de 200 linhas do repositório).
Este arquivo cobre as figuras que **constroem um conceito sobre o dado real**,
em vez de só exibir a forma de onda, mais a regra de legibilidade que vale para
todas elas. Os oscilogramas comuns continuam no `README.md`.

Racional de por que essas figuras existem (o texto do TCC descrevia a figura em
vez de analisá-la) em `.claude/kb/tcc-word/revisao_fragmento_cap5_analise.md`.
Como desenhá-las, na skill `svg-diagrams` (`data_charts.md`).

## Figuras didáticas da retenção

Gerados por `scripts/gen_retencao_didatica.py`. Diferente dos demais, não são
oscilogramas de um cenário: mostram **como a métrica de retenção é construída**
sobre os dados reais, para o texto do TCC não precisar definir a razão só em
prosa. As faixas sombreadas e as linhas de média são anotação sobre o dado, não
alteração dele — os dois valores saem calculados do CSV a cada geração.

| Arquivo | Conteúdo |
|---|---|
| `retencao_construcao.svg` / `.png` | Painel único, `bus7/3phase` (nominal): janela pré-falta, 2 ciclos descartados, janela de medição e a razão fechada |
| `retencao_comparacao.svg` / `.png` | Painel duplo `bus7/3phase` × `bus7/3phase_bad_pll`, para a Seção 5.4 do TCC |

Receita (a mesma de `src/pipeline` e da KB de métricas):

```
retencao = média(v_d) em [t_fault + 2 ciclos, t_clear]
         / média(v_d) em [t_fault − 50 ms, t_fault)
```

Os 2 ciclos descartados (33,3 ms a 60 Hz) removem o transitório de comutação da
aplicação da falta, que domina o trecho inicial e não representa o afundamento.

Duas convenções que **só** valem para o painel duplo, e por isso ficam
documentadas aqui:

- **Eixo X em tempo relativo ao início da falta.** É a única figura da pasta que
  não usa tempo absoluto. Necessário porque `t_fault` difere entre os cenários
  (0,3 s no nominal, 0,6 s na sintonia inadequada) e sem o deslocamento os dois
  painéis não alinham.
- **Eixo Y compartilhado** (`sharey`), mesmo princípio do `YLIM_GROUPS` de
  `gen_fault_waveforms.py`: a diferença das bases pré-falta (0,989 contra
  0,823 pu) é justamente o que a figura precisa deixar visível.

A barra vermelha superior marca a **duração real da falta** (0,1 s), distinta da
janela de medição em laranja, que começa 2 ciclos depois.

## Potência anotada (série temporal didática)

Gerado por `scripts/gen_potencia_didatica.py` → `potencia_didatica.svg` / `.png`.
Dois painéis empilhados (P em cima, Q embaixo) para `bus7/3phase_bad_pll`.

É o **mesmo oscilograma** de `bus7_3phase_bad_pll_potencia_pq`, com anotação por
cima, em vez de um gráfico novo. Quatro camadas:

1. **Área preenchida onde a potência é negativa.** "O inversor absorve energia"
   deixa de ser afirmação do texto e vira área visível.
2. **Patamar pré-falta** tracejado em verde: o valor ao qual a potência deveria
   ter retornado.
3. **Média pós-falta** tracejada em vermelho: o valor que ela de fato assumiu.
   A distância entre as duas tracejadas é o resultado da seção.
4. **Fração do tempo com potência negativa**, em caixa (63,8% para P, 39,4%
   para Q).

Estatísticas na janela `[t_clear, fim]` — a mesma região sombreada, para que
número e desenho não divirjam. A **escala vertical** de cada painel ignora os
20 ms seguintes à eliminação: o transitório de comutação leva P a −2,4 pu por
~1 ms e esconderia a oscilação. O traço continua desenhado, só sai do recorte.

**Inserir a 6,5 in, não a 5,5 in.** Esta figura e o plano P-Q usam `figsize`
8,3 in justamente para dar a escala 0,79 quando colocadas na largura útil cheia.
A 5,5 in (largura dos oscilogramas comuns) a escala cai para 0,66 e as
anotações despencam para ~6,3 pt. Ver "Legibilidade no DOCX" abaixo.

## Legibilidade no DOCX (regra medida)

Fonte efetiva na página = `font_pt × largura_na_pagina / largura_figsize`.
A largura útil do fragmento é **6,5 in** (Carta, margens de 1 in).

| Figura | `figsize` | Inserida a | Escala | Fonte-base efetiva |
|---|---|---|---|---|
| Oscilogramas (`gen_fault_waveforms`) | 7,0 in | 5,5 in | 0,79 | ~7,9 pt |
| Retenção (`gen_retencao_didatica`) | 8,3 in | 6,5 in | 0,78 | ~7,8 pt |
| Potência anotada / plano P-Q | 8,3 in | **6,5 in** | 0,78 | ~7,8 pt |

Duas armadilhas já pagas:

- **Encolher o `figsize`, nunca aumentar a fonte.** Aumentar `fontsize` deixa o
  PNG isolado feio e não muda a proporção texto/figura na página.
- **Anotação não pode ser menor que a fonte-base.** As primeiras versões usavam
  8,8 pt para os rótulos de valor, que viravam 6,9 pt na página. Passaram para
  9,5 pt (~7,4 pt efetivos).

**Como validar:** reescalar o PNG para `6,5 in × 150 dpi = 975 px` de largura e
olhar ao lado de uma linha em 12 pt (corpo do TCC). É o único teste que pega o
problema; no PNG em tamanho natural tudo parece legível.

## Plano P-Q pós-falta

Gerado por `scripts/gen_plano_pq.py` → `plano_pq_comparacao.svg` / `.png`.
Painel duplo `bus7/3phase` × `bus7/3phase_bad_pll`, mesma família didática da
retenção: mostra sobre o dado real o que a série temporal não mostra.

Em vez de P(t) e Q(t), plota a **trajetória no plano P-Q**. O ponto de operação
pré-falta vira um marcador ("antes") e a média da janela pós-falta vira outro
("depois"). No nominal os dois praticamente coincidem; na sintonia inadequada o
"depois" está **do outro lado da linha P = 0**, ou seja, o inversor passou a
absorver energia. O semiplano `P < 0` fica sombreado em vermelho.

**Métrica destacada: fração do tempo com `P < 0`** (1,1% no nominal contra 64,6%
na sintonia inadequada). Escolhida por ser adimensional e **não depender do
comprimento da janela** — é uma razão, ao contrário dos valores de pico, que
mudam com o recorte. Foi o que substituiu a enumeração de picos no texto, ver
`.claude/kb/tcc-word/revisao_fragmento_cap5_analise.md`.

Janela: `[t_clear + 50 ms, fim]`. Os 50 ms descartados removem o transitório de
comutação da **eliminação** da falta, que no nominal leva P a −3,4 pu por poucos
milissegundos e falsearia a comparação — mesmo racional do descarte de 2 ciclos
na figura da retenção. Eixos compartilhados entre os painéis, porque a diferença
de extensão da órbita é justamente o que a figura precisa mostrar.
