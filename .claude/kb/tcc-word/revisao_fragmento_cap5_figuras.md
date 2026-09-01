---
name: tcc-revisao-fragmento-cap5-figuras
description: Estrutura de seções, mapa das 13 figuras e histórico de geração dos gráficos do Cap.5 do fragmento capitulos_4_5_revisados.docx
metadata:
  type: project
---

# Cap. 5 do Fragmento — Estrutura e Figuras

Desmembrado de [[tcc-revisao-fragmento-cap5]] em 2026-08-23 pelo limite de
200 linhas. Números e receitas de métrica ficam em
[[tcc-revisao-fragmento-cap5-metricas]].

## Estrutura aplicada (41 parágrafos, índices 36-76, substituição 1:1)

```
5.1 Validação da operação em regime permanente        Fig 5.1, 5.2, 5.3
5.2 Faltas simétricas: severidade e localização        Fig 5.4, 5.5, 5.6
5.3 Faltas assimétricas: sequência negativa e sintonia Fig 5.7 a 5.10
5.4 Perda de sincronismo sob falta simétrica no PAC     Fig 5.11 a 5.13
5.5 Conformidade com o código de rede   (promovido do antigo 5.3.1 órfão)
5.6 Resumo e conclusões do capítulo
```

A 5.4 entrou em 2026-08-23 (noite), a pedido do usuário. Fica **depois** da
5.3 de propósito: o capítulo passa a construir gradiente de localização →
compromisso de banda passante → caso-limite em que o compromisso deixa de
valer. Isso preservou a numeração das Figuras 5.1 a 5.10.

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
| 5.11 | `bus7_3phase_bad_pll_tensao_dq_rede` |
| 5.12 | `bus7_3phase_bad_pll_potencia_pq` |
| 5.13 | `bus7_3phase_bad_pll_corrente_dq` |

As Figuras 5.8 e 5.9 substituíram o par `bus7/2phase`, que satura em 180° nas
duas sintonias e por isso não ilustrava o efeito da parametrização. Motivo e
escalas compartilhadas em [[tcc-revisao-fragmento-cap5-metricas]].

### Figura 5.11 nova: `retencao_comparacao` (inserida em 2026-08-26)

Entrou na abertura do §5.4 para mostrar de onde sai a razão da retenção, que
antes aparecia no texto só com o valor fechado. Racional e decisões de desenho
em [[tcc-revisao-fragmento-cap5-metricas-54]].

Renumeração aplicada em ordem **decrescente** (5.13→5.14 antes de 5.12→5.13),
2 ocorrências por figura (legenda + chamada no corpo):

| Antes | Depois | Arquivo |
|---|---|---|
| (nova) | 5.11 | `retencao_comparacao` |
| 5.11 | 5.12 | `bus7_3phase_bad_pll_tensao_dq_rede` |
| 5.12 | 5.13 | `bus7_3phase_bad_pll_potencia_pq` |
| 5.13 | 5.14 | `bus7_3phase_bad_pll_corrente_dq` |

Documento passou de **111 para 113 parágrafos e de 17 para 18 imagens**. Ao
parágrafo de abertura (índice 90) foi acrescentada a frase que chama a figura
e define a retenção em palavras.

**Largura da figura: 6,5 in, não 5,5 in como as demais.** O figsize do
matplotlib também mudou, de 10,4 para 8,3 in, e o motivo é a fonte efetiva no
documento, que vale `font_pt × largura_na_pagina / figsize`. As demais figuras
do Cap. 5 usam figsize 7,0 a 5,5 in na página (escala 0,79, ~7,9 pt efetivos);
8,3 a 6,5 in dá a mesma escala. A 10,4 in de figsize a fonte cairia para
5,6 pt. Regra do projeto: **encolher o viewBox, nunca aumentar a fonte**.

**Não viola a regra de `assets/`** (*"tudo que está em assets é o resultado a
ser usado, são os dados reais, nada de manipulações"*, registrada abaixo no
caso do `regime_bad_pll_v2`): a figura plota `bus7/3phase` e
`bus7/3phase_bad_pll` sem truncar nem sintetizar nada. As faixas e as linhas
de média são anotação sobre o dado real, não alteração dele, e saem calculadas
do CSV em tempo de geração.

**Defeito encontrado e corrigido na mesma sessão:** a frase nova foi anexada a
`p.runs[-1]`, que por acaso era um trecho marcado com **marca-texto amarelo
pelo usuário** (a própria frase da retenção, que ele tinha destacado ao
perguntar sobre ela). O run passou de 284 para 781 caracteres e o realce
vazou para o texto novo. Nenhuma conferência textual pegou isso, só a
renderização da página em PDF. Corrigido separando em dois runs, o amarelo de
volta aos 284 caracteres originais e a frase nova em run próprio sem
`w:highlight`. Lição registrada em `fragmento_externo.md` da skill.

As imagens ficam empilhadas verticalmente no Word (pouco espaço horizontal),
não lado a lado. **Inseridas no fragmento em 2026-08-22**: parágrafo de imagem
(centralizado, 5,5" de largura — página Letter, margens 1", 6,5" úteis)
logo acima de cada legenda "Figura 5.X - ...". Documento passou de 77 para
85 parágrafos, para 88 com a Figura 5.3, para 91 com a Figura 5.9 e para
**105 parágrafos e 13 imagens** com a Seção 5.4 (2026-08-23). Cap. 4 não foi tocado (legendas de Fig. 4.1/4.2 continuam sem
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

