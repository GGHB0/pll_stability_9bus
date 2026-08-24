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

