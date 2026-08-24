---
name: tcc-revisao-fragmento-cap5
description: Reescrita do Cap.5 do fragmento capitulos_4_5_revisados.docx — duas safras de modelo nos cenários bad_pll, tese trocada para compromisso de banda passante, estrutura 5.1-5.5
metadata:
  type: project
---

# Revisão do Fragmento Externo — Capítulo 5 (2026-08-22)

Continuação de [[tcc-revisao-fragmento-cap4]]. Mesmo arquivo externo
(`capitulos_4_5_revisados.docx` em Downloads), ainda **não** mesclado no
canônico.

## Achado crítico: duas safras de modelo nos cenários `_bad_pll`

Levantado pela impressão digital do transitório de **energização** (independe
da falta aplicada). Os ganhos reduzidos estão aplicados nas duas safras, mas o
resto do modelo mudou:

> **Não usar o pico do erro de fase na energização como métrica.** Ele é
> dominado pela singularidade de `atan2` quando a tensão passa por zero: o
> valor cai de 172° para 22° só movendo o corte inicial de 1 ms para 5 ms, nos
> dois cenários. Foi essa métrica que produziu os "26,4° contra 45,2°" do
> texto antigo. Retirada do fragmento em 2026-08-23.

| Safra | Cenários | Acomoda (±5°) | v_d pré-falta |
|---|---|---|---|
| **Julho** | `regime_bad_pll`, `bus7/3phase_bad_pll`, `bus6/3phase_bad_pll`, `line7_8/3phase_bad_pll` | ~599 ms | **0,80–0,82 pu** |
| **Agosto (11-12)** | `bus7/1phase_bad_pll`, `bus7/2phase_bad_pll`, `bus6/1phase_bad_pll`, `bus6/2phase_bad_pll` | 54 ms | **0,99 pu** |
| *(nominal, julho)* | todos | 32 ms | 0,97–0,99 pu |

### Causa raiz identificada (2026-08-23)

A divisão não é "julho vs agosto" genérica: é o commit `2a9b6d2`
(2026-07-21), *Fix ONS_2_11 overvoltage sign bug*. Antes dele o ramo de
sobretensão usava `k_high = -10`, levando `iq_ref` a −1 acima de 1,10 pu em
vez de +1. Ver [[ons-2-11]].

Teste que separa os 30 cenários sem ambiguidade: `iq_ref` médio enquanto
a magnitude no PAC excede 1,10 pu durante a energização.

| Grupo | Cenários | `iq_ref` em sobretensão |
|---|---|---|
| Pré-correção | 26 (todos os nominais + os 4 `_bad_pll` de julho) | −0,417 a −0,495 |
| Pós-correção | 4 (`bus6`/`bus7` × `1phase`/`2phase_bad_pll`) | +0,110 |

**Alcance é limitado à energização.** Os estados pré-falta dos dois lados
coincidem (`v_d` 0,9894 pré contra 0,9963 pós; P 0,875 contra 0,869; erro
< 0,02°), e a janela do bug fecha em ~38 ms, muito antes das faltas em 0,3 s
ou 0,6 s. Logo 5.2 e 5.3 não são afetadas; só a 5.1, que analisa justamente
a energização.

### Decisão do usuário (2026-08-23)

Optou por **usar o `regime_bad_pll` como está**, atribuindo o intervalo de
450 ms com `id_ref` nula e `iq_ref` saturada ao **atraso do estimador** com
ganhos subdimensionados: o laço lento mantém a excursão de energização fora
da faixa normal por 37 ms contra 18 ms do nominal, e é esse alongamento que
prolonga a atuação do suporte reativo. Sem re-simulação.

Ressalva registrada e não resolvida: o Cap. 4 do fragmento estabelece
ωn = 325,3 → 145,5 rad/s e ξ = 0,707 → 0,316, o que prevê acomodação ~5×
mais lenta; o `regime_bad_pll` dá 17×, e os cenários de agosto com os mesmos
ganhos dão 2,3×. Ver também [[cenarios-simulados]].

Anomalia adicional: `line7_8/3phase_bad_pll` tem retenção de 64,9% contra
10,4% do nominal na mesma linha, e 0,384 pu de 120 Hz numa falta trifásica
**equilibrada** (o nominal tem 0,008 pu). Esse run não parece ser a falta que
o nome indica. Descartado.

## Decisões do usuário (2026-08-22)

Optou por **não re-simular**. Os cenários de sintonia inadequada passam a ter
papel ilustrativo do impacto de um PLL mal dimensionado, não de matriz
comparativa completa.

1. **Tese do capítulo → "compromisso honesto".** Usa só os 4 pares de agosto.
   Não se afirma *cycle slipping* nem instabilidade, porque os dados
   consistentes não mostram isso.
2. **5.2 só com nominal.** Varredura de localização; a comparação de sintonia
   fica toda em 5.3.

## A tese que os dados sustentam

O laço subdimensionado **não** é uniformemente pior — é um compromisso:

- **Durante a falta:** excursão angular **menor** nos 4 pares (40,1°→34,2°;
  58,9°→46,8°; 44,3°→19,0°; 15,0°→9,2°). Menor banda passante rejeita melhor
  a oscilação de 120 Hz.
- **Na recuperação:** reaquisição 2 a 3× mais lenta (55→187 ms; 47→103 ms;
  39→95 ms). Ondulação de Q pós-falta na Barra 6 bifásica vai de 4,8 a
  11,7 pu.
- **Em regime:** sincronização ~2× mais lenta (34→74 ms para ±2°) e erro de
  fase estático ~2× maior (0,81°→1,48°). Mesmo ponto de operação final.

**Resultado mais sólido do capítulo** (independe de sintonia): a componente de
120 Hz em `v_d` vale 0,008–0,014 pu nas faltas trifásicas contra 0,28–0,71 pu
nas assimétricas — uma a quase duas ordens de grandeza. É a confirmação
empírica do mecanismo de sequência negativa descrito no Cap. 3.

## Gradiente de localização (5.2, só nominal, falta trifásica)

Barra 7 é o ponto de injeção da UFV (via T2); Barra 6 é a barra
eletricamente mais distante (3 linhas). Ver [[ieee9bus-topology]].

| Local | Retenção `v_d` | Pico erro de fase | P durante | `i_q,ref` |
|---|---|---|---|---|
| Barra 7 (PAC) | 8,5% | 53,9° | 0,00 pu | −0,97 |
| Linha 7-8 | 10,4% | 44,3° | 0,00 pu | −0,97 |
| Linha 8-9 | 46,4% | 23,5° | 0,04 pu | −0,94 |
| Barra 6 (remota) | 58,4% | 21,0° | 0,36 pu | −0,67 |

Progressão monotônica em todas as colunas. Em todos os casos o erro volta a
±2° em até 100 ms após a eliminação.

## Correções de fato no texto anterior

- "despacha a potência ativa de **1 p.u.**" → medido **0,87 pu**.
- "os dois modelos convergem para o mesmo ponto de operação" → **falso** com
  o `regime_bad_pll`: 0,983 pu (nominal) contra 0,808 pu, ainda subindo ao
  final da janela. Texto reescrito em 2026-08-23.
- O critério de ±1,15° (`TOL_RAD`, `src/config/settings.py`) **nunca** é
  atingido: a ondulação residual é de ~2,0° (nominal) e ~3,1° (inadequada).
  O capítulo usa ±2° para erro de fase e ±5% para `v_d`.

## Estrutura aplicada (41 parágrafos, índices 36-76, substituição 1:1)

```
5.1 Validação da operação em regime permanente        Fig 5.1, 5.2, 5.3
5.2 Faltas simétricas: severidade e localização        Fig 5.4, 5.5, 5.6
5.3 Faltas assimétricas: sequência negativa e sintonia Fig 5.7, 5.8, 5.9
5.4 Conformidade com o código de rede   (promovido do antigo 5.3.1 órfão)
5.5 Resumo e conclusões do capítulo
```

Títulos X.X em 18 pt negrito, legendas em 11 pt itálico centralizado, corpo
herda o estilo Normal — conforme já praticado no Cap. 4 do fragmento.

## Figuras (só dq e potência; sem abc, por decisão do usuário)

| Fig | Arquivo em `assets/charts/` |
|---|---|
| 5.1 | `regime_tensao_dq_rede` |
| 5.2 | `regime_bad_pll_tensao_dq_rede` |
| 5.3 | `regime_bad_pll_potencia_pq` |
| 5.4 | `bus7_3phase_tensao_dq_rede` |
| 5.5 | `bus6_3phase_tensao_dq_rede` |
| 5.6 | `bus7_3phase_potencia_pq` |
| 5.7 | `bus7_2phase_tensao_dq_rede` |
| 5.8 | `bus7_2phase_bad_pll_tensao_dq_rede` |
| 5.9 | `bus6_2phase_bad_pll_potencia_pq` |

As imagens ficam empilhadas verticalmente no Word (pouco espaço horizontal),
não lado a lado. **Inseridas no fragmento em 2026-08-22**: parágrafo de imagem
(centralizado, 5,5" de largura — página Letter, margens 1", 6,5" úteis)
logo acima de cada legenda "Figura 5.X - ...". Documento passou de 77 para
85 parágrafos, e para 88 com a Figura 5.3 (2026-08-23). Cap. 4 não foi tocado (legendas de Fig. 4.1/4.2 continuam sem
imagem, fora de escopo).

### `regime_bad_pll_v2` — criado e removido

Existiu entre 22 e 23/08 como regime da sintonia inadequada da safra de
agosto, construído a partir da **janela pré-falta** de `bus6/1phase_bad_pll`
truncada em 0,6 s (campo `t_max` no gerador).

**Removido em 2026-08-23**, por regra do usuário: *"tudo que está em assets é
o resultado a ser usado, são os dados reais, nada de manipulações"*. Cenário
sintético não entra em `assets/`. O campo `t_max` saiu junto de
`gen_regime_waveforms.py` (não era usado por mais nada), e entrou
`ylim_dq`/`YLIM_DQ_REGIME`, que fixa a escala dq comum a `regime` e
`regime_bad_pll` para as Figuras 5.1 e 5.2 poderem ser lidas na mesma escala.

### SVGs gerados nesta sessão

`bus7_2phase`, `bus7_2phase_bad_pll`, `bus6_1phase`, `bus6_1phase_bad_pll`
(6 gráficos cada) — completam a matriz assimétrica 2 barras × 2 tipos ×
2 sintonias. Dados já existiam, só faltava gerar.

## Pendências

- **Cap. 4 cita "*cycle slipping*"** no parágrafo do painel interativo (índice
  28) como fenômeno visualizável. O Cap. 5 não afirma mais esse fenômeno —
  conferir se o Cap. 4 deve ser ajustado (o Cap. 4 estava fechado).
- **Cap. 6/Conclusões do canônico** afirmam *cycle slipping* como resultado
  observado; precisam do mesmo alinhamento quando a mesclagem acontecer.
- **Aberta:** por que os mesmos ganhos dão 563 ms de acomodação no
  `regime_bad_pll` e 79 ms nos cenários de agosto, se a teoria de segunda
  ordem do Cap. 4 prevê ~5×? Usuário optou por seguir sem resolver.
- Se o Bruno re-simular os 4 cenários de julho no modelo atual, vale reavaliar
  se a perda de sincronismo do `bus7/3phase_bad_pll` (erro pós-falta de 180°,
  excursão de 359,8°) sobrevive — seria a tese *afundamento profundo + laço
  lento*, mais forte que a atual.
- Mesclagem no canônico segue sem data definida.
