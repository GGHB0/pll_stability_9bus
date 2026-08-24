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
da falta aplicada). Causa raiz, teste de classificação e alcance ficam em
[[cenarios-simulados]]: é o commit `2a9b6d2` (2026-07-21), *Fix ONS_2_11
overvoltage sign bug*, ver [[ons-2-11]].

O que importa para este capítulo: **todos os nominais e os 4 `_bad_pll` de
julho são pré-correção; só os 4 pares de agosto são pós-correção**. Como o bug
age apenas nos ~38 ms da energização e os estados pré-falta coincidem, 5.2 e
5.3 não são afetadas. Só a 5.1 é, porque analisa justamente a partida.

> **Não usar o pico do erro de fase na energização como métrica.** Ele é
> dominado pela singularidade de `atan2` quando a tensão passa por zero: o
> valor cai de 172° para 22° só movendo o corte inicial de 1 ms para 5 ms, nos
> dois cenários. Foi essa métrica que produziu os "26,4° contra 45,2°" do
> texto antigo. Retirada do fragmento em 2026-08-23.

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

Anomalia adicional: `line7_8/3phase_bad_pll` tem retenção de 65,5% contra
11,3% do nominal na mesma linha, e 0,416 pu de 120 Hz numa falta trifásica
**equilibrada** (o nominal tem 0,0002 pu). Esse run não é a falta que o nome
indica. Descartado. Valores refeitos com as definições de
[[tcc-revisao-fragmento-cap5-metricas]].

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

Receitas de cálculo e valores conferidos em
[[tcc-revisao-fragmento-cap5-metricas]]. Os números desta seção na versão
anterior deste arquivo estavam errados e foram corrigidos em 2026-08-23.

O laço subdimensionado **não** é uniformemente pior, é um compromisso:

- **Durante a falta:** excursão angular **menor** em 3 dos 4 pares
  (96,0°→34,9° na Barra 6 bifásica; 89,7°→72,2° na Barra 7 monofásica). No
  par mais brando (Barra 6 monofásica) empatam, 12,0° contra 13,2°. Na Barra
  7 bifásica os dois saturam em 180°.
- **Na recuperação:** reaquisição ~2× mais lenta (51→99 ms; 46→98 ms;
  48→78 ms; 39→47 ms). Ondulação de Q pós-falta na Barra 6 bifásica vai de
  4,8 a 11,7 pu.
- **Em regime:** o que degrada é o ponto de operação (`v_d` 0,983 contra
  0,808 pu). O erro de fase estático é **igual** nos dois modelos (rms 0,442°
  contra 0,444°); o "~2× maior" registrado antes era falso.

**Resultado mais sólido do capítulo** (independe de sintonia): a componente de
120 Hz em `v_d` vale 0,0001–0,0013 pu nas faltas trifásicas contra 0,29–0,71 pu
nas assimétricas, mais de duas ordens de grandeza. É a confirmação empírica do
mecanismo de sequência negativa descrito no Cap. 3.

## Gradiente de localização (5.2, só nominal, falta trifásica)

Barra 7 é o ponto de injeção da UFV (via T2); Barra 6 é a barra
eletricamente mais distante (3 linhas). Ver [[ieee9bus-topology]].

| Local | Retenção `v_d` | Pico erro de fase | P durante | `i_q,ref` |
|---|---|---|---|---|
| Barra 7 (PAC) | 9,2% | 37,3° | 0,00 pu | 1,000 |
| Linha 7-8 | 11,3% | 32,5° | 0,01 pu | 1,000 |
| Linha 8-9 | 47,1% | 29,8° | 0,00 pu | 1,000 |
| Barra 6 (remota) | 58,4% | 7,3° | 0,34 pu | 0,776 |

Progressão monotônica em todas as colunas. O erro volta a ±2° em até 112 ms
após a eliminação; o pior caso é a Linha 8-9, e o "100 ms" registrado antes
era furado por ela. Pico medido a partir do 1º ciclo após a aplicação, para
excluir o transitório de comutação, ver
[[tcc-revisao-fragmento-cap5-metricas]].

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
5.3 Faltas assimétricas: sequência negativa e sintonia Fig 5.7 a 5.10
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
| 5.8 | `bus6_2phase_tensao_dq_rede` |
| 5.9 | `bus6_2phase_bad_pll_tensao_dq_rede` |
| 5.10 | `bus6_2phase_bad_pll_potencia_pq` |

As Figuras 5.8 e 5.9 substituíram o par `bus7/2phase`, que satura em 180° nas
duas sintonias e por isso não ilustrava o efeito da parametrização. Motivo e
escalas compartilhadas em [[tcc-revisao-fragmento-cap5-metricas]].

As imagens ficam empilhadas verticalmente no Word (pouco espaço horizontal),
não lado a lado. **Inseridas no fragmento em 2026-08-22**: parágrafo de imagem
(centralizado, 5,5" de largura — página Letter, margens 1", 6,5" úteis)
logo acima de cada legenda "Figura 5.X - ...". Documento passou de 77 para
85 parágrafos, para 88 com a Figura 5.3 e para 91 com a Figura 5.9
(2026-08-23). Cap. 4 não foi tocado (legendas de Fig. 4.1/4.2 continuam sem
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
- Toda métrica nova do capítulo precisa entrar em
  [[tcc-revisao-fragmento-cap5-metricas]] com a receita junto. Números sem
  receita foi exatamente o que a auditoria de 2026-08-23 teve de desfazer.
- Mesclagem no canônico segue sem data definida.
