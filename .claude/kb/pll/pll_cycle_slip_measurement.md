---
name: pll-cycle-slip-measurement
description: Receita de medição do escorregamento de ciclo (cycle slipping) do SRF-PLL — arctan2+unwrap sobre vd/vq, com verificação cruzada via ângulos gravados pelo modelo
metadata:
  type: reference
---

# Medição do escorregamento de ciclo — receita e verificação

Documenta a cadeia de cálculo por trás dos números de perda de sincronismo do
§5.4 do fragmento (6 916° / 19,2 voltas em 300 ms / ~70 Hz), cenário
`bus7/3phase_bad_pll`. Ver [[tcc-revisao-fragmento-cap5-metricas]] para a
tabela de métricas da seção.

Nota técnica completa, com dados reais e gráficos, em
`output/medicao_escorregamento_srf_pll.pdf` (gerador:
`scripts/notas/gen_medicao_escorregamento.py`).

**Status no texto do TCC (2026-08-31):** o §5.4 **não cita nenhum destes
números** — nem a rotação acumulada (6 916° / 19,2 voltas), nem a estabilização
da taxa, nem a frequência de escorregamento (~70 Hz). Decisão do usuário: são
parâmetros que não sustentam a conclusão da seção e abrem flanco a
questionamento em banca (o acumulado é do mesmo tipo do ISE tirado do
dashboard). O texto ficou qualitativo: erro de fase cresce sem retornar a valor
estável, sem reaquisição na janela. Esta nota e o PDF seguem como **registro de
método**, órfãos em relação ao texto. Detalhe em
[[tcc-revisao-fragmento-cap5-metricas-54]].

## A cadeia

1. **Fonte:** `vd_rede_pu`/`vq_rede_pu` de `output/results/bus7/3phase_bad_pll/sim_data.csv`, passo 5 µs.
2. **Janela:** de `t_clear` (0,700 s) ao fim da simulação (1,000 s).
3. **`θ_cru = arctan2(vq, vd)`**, em graus, faixa −180° a +180°. Não é o
   arco-tangente de cada coordenada separada — é um único ângulo do par, em
   que os sinais de `vd` e `vq` resolvem o quadrante (`arctg` sozinho tem
   período de 180°, então dois vetores em quadrantes opostos com a mesma
   razão `vq/vd` dão o mesmo `arctg`, mas `arctan2` distingue).
4. **`unwrap`:** corrige os saltos de ±360° quando `θ_cru` cruza a borda
   ±180°, reconstruindo o ângulo contínuo. Confirmado que a premissa do
   `unwrap` (variação real < 180°/amostra) tem folga de 21× até no pior caso
   (passo máximo 8,56°/amostra, no instante de módulo mínimo do vetor).
5. **`Δθ = θ[fim] − θ[início]`**: acumulado total, equivalente à integral do
   erro de frequência na janela. Dividido por 360° dá as voltas.
6. **Escorregamento em regime:** `polyfit` grau 1 sobre `θ` desenrolado, em
   janelas de 20 ms. Varredura fina (passo de 5 ms, a partir de 0,76 s)
   mostra oscilação entre **65 e 81 Hz**, média ~72 Hz — a tabela de seis
   janelas no KB de métricas é uma amostra dessa faixa, não o intervalo
   inteiro. "~70 Hz" no texto é o regime arredondado.

## Verificação cruzada: rota pelo ângulo já gravado

O modelo também grava `theta_pll_rad`, `theta_ref_rad` e a diferença pronta
`theta_err_rad` em `sim_data_angles.csv` (passo 200 µs, 40× mais grosso). Essa
coluna dispensa o `arctan2` mas **não** dispensa o `unwrap`: a rotina de
exportação (`export_sim_data.m`, `wrapToPi`) já recorta esse erro no mesmo
intervalo ±180°, então a mesma trava aparece — 19 travessias de borda, iguais
às da rota das componentes.

Resultado dessa rota: Δθ = +6 938,30° = 19,27 voltas, contra 6 916,42°/19,21
voltas pela rota das componentes. Diferença de 0,32%, compatível com a razão
de resolução temporal (40×). Sinal invertido entre as rotas é convenção (uma
mede o ângulo do vetor da rede no referencial do PLL, a outra mede PLL menos
rede), não discrepância — as duas dizem que o referencial estimado gira mais
rápido que a rede.

**Por que o texto usa a rota das componentes, não a do ângulo pronto:** mesma
tensão do ponto de conexão que alimenta as demais métricas do capítulo
(consistência), e 40× mais resolução temporal (margem para a verificação de
que o escorregamento não é artefato de amostragem).

## Achado da auditoria do PDF (2026-08-25)

Primeira versão da nota tinha uma contradição: a Seção 9 comparava o passo
máximo da rota do ângulo (15,0°/amostra) contra "menos de um grau" da rota
das componentes, mas a Seção 6 já registrava o máximo real dessa rota como
8,558°/amostra (no mesmo instante de módulo mínimo). Corrigido comparando
médias com médias (0,120° vs 4,74°) e máximos com máximos (8,558° vs 15,0°)
explicitamente, em vez de uma frase vaga. Também corrigida a notação decimal
dos eixos dos gráficos (ponto → vírgula, `FuncFormatter` pt-BR) e a faixa de
escorregamento (65–81 Hz, não 68–81 Hz, que só cobria as seis janelas
tabuladas e não a varredura fina). Achado pelo agente `note-validator` ao
recomputar cada número da nota contra o CSV, em vez de conferir só o texto.
