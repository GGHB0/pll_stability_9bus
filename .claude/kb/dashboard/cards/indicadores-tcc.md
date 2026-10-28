---
name: indicadores-tcc-dashboard
aliases: [indicadores-tcc-dashboard]
description: Indicadores do Cap. 5 do TCC no dashboard (2026-10-20) — módulo único indicadores.py, erro de fase atan2(v_q, v_d) da rede, faixa de 2°, cards por cenário, colunas da tabela comparativa e destaque de 120 Hz na aba Espectro
---

# Indicadores do TCC no Dashboard

Motivação (2026-10-20): o slide 14 do deck da defesa passa direto para a
demonstração ao vivo no HTML, e o painel precisava mostrar **os mesmos
números do Cap. 5** ([[tcc-revisao-fragmento-cap5-metricas]]). Não mostrava:
faltavam indicadores, e o painel "Erro de fase" usava outra definição. O
resultado contradizia as Tabelas 5.1 e 5.3:

| Cenário | Pico HTML antigo | Pico TCC | Retorno HTML antigo | Retorno TCC |
|---|---|---|---|---|
| `bus7/3phase` | 53,1° | 37,3° | 97 ms | 98 ms |
| `line8_9/3phase` | 24,0° | 29,8° | 106 ms | 112 ms |
| `bus6/2phase` | 45,0° | 96,0° | "não acomoda" | 48 ms |
| `bus7/1phase_bad_pll` | 48,3° | 70,6° | 134 ms | 95 ms |

Causa: o HTML calculava `θ̂_PLL − θ_rede` (bloco de ângulos, com desconto do
valor pré-falta) e usava a faixa ±1,15° (`TOL_RAD`). O TCC usa `atan2(v_q, v_d)`
da tensão da rede, faixa de 2° e descarta o 1º ciclo no pico.

## Fonte única: `src/pipeline/indicadores.py`

As receitas fechadas saíram de `scripts/medir_tabelas_cap5.py` e de
`gen_erro_fase.metrics` para o pacote. Os dois scripts agora chamam o módulo
(a regeneração de `output/tabelas_cap5.csv` deu diferença zero), e o
`SimData` também. Número novo do Cap. 5 e número do painel saem da mesma
função.

| Função | Entrega |
|---|---|
| `erro_fase_deg` | `atan2(v_q, v_d)` da rede, em graus |
| `pico_e_retorno` | pico em `[t_fault + 1 ciclo, t_clear]`; retorno = último \|e\| > 2° após `t_clear`, em ms (`None` = não volta na janela) |
| `indicadores_falta` | retenção de v_d, v_d médio/mín./máx., 120 Hz (Hann, `[t_fault + 2 ciclos, t_clear]`), % do tempo com \|e\| > 90° em `[t_fault, t_clear]`, \|V\| médio do inversor, rampa ONS, i_q,ref médio, P e Q médios, % do tempo com P < 0 e Q ≥ 0 após `t_clear`; `err_ts` = erro no instante do retorno, que vai com t_clear e ts para `tccInd.retorno` (marcação do palco) |
| `indicadores_partida` | regime: v_d na faixa de ±5% do valor final (média dos últimos 50 ms) e erro na faixa de 2°, em ms desde t = 0; também `vd_fin` e o valor de cada sinal nesse instante (`vd_t5`, `err_t2`), que vão para `tccInd.partida` e marcam o capítulo Energização |
| `suportabilidade_ons` | falta: amplitude de 60 Hz de cada fase de `v_abc` do inversor (janela móvel de 1 ciclo), mínimo entre fases; "fora" se cai abaixo da borda da Figura 2.1 depois do 1º ciclo (classificado na taxa nativa; a série embutida é reamostrada a 2 ms). Usado só pelo capítulo "Código de rede" ([[ons-voltage-ride-through]]) |

Conferido contra o TCC: Tabelas 5.1 a 5.3 inteiras, 8,2% / 9,7% de retenção
(§5.4), 106 ms (`bus6/3phase_bad_pll`), 34/40 e 42/79 ms (§5.1), 17,8% e
14,0% acima de 90° (§5.3), e 66,8% / 58,0% de sentido do fluxo (§5.4).

`spectrum.py` passou a importar `SimData` só sob `TYPE_CHECKING`, para
quebrar o ciclo `loader → indicadores → spectrum → loader`.

## Onde aparece

- **Loader**: `theta_err` vem de `atan2(vq_rede, vd_rede)` sempre que o CSV
  tem v_dq da rede (o caminho antigo vira fallback de CSV legado).
  `metrics["ind"]` (faltas eliminadas) e `metrics["partida"]` (regime);
  `metrics["ts"]` passa a ser o instante absoluto `t_clear + retorno`. Ver
  [[pipeline-dados]].
- **Painel "Erro de fase"**: faixa de 2°, 1º ciclo da falta sombreado em
  cinza (fora do pico) e linha quebrada nos saltos de ±180° (escorregamento
  de ciclo, como na Fig. 5.18). O tooltip do marcador tₛ dá o retorno em ms.
  Ver [[chart-analysis-overlays]].
- **Cards** (aba Resumo, acima da severidade), sem semáforo porque o TCC não
  classifica por limiar:
  - *Sincronismo do SRF-PLL*: pico, retorno à faixa de 2° ("não retorna" em
    vermelho), 120 Hz; "Erro acima de 90°" só nas assimétricas (na trifásica
    a fração vem só do salto de fase da aplicação da falta); "Q injetada" só
    quando não há retorno (§5.4). "P absorvida" saiu dos cards, da frase do
    resumo e do palco em 2026-10-28, a pedido do usuário (`frac_P_absorve`
    segue calculado em `indicadores.py`).
  - *Tensão e suporte de reativo*: "Suportabilidade ONS" (dentro/fora,
    desde 2026-10-25), retenção de v_d, v_d médio (mín./máx.), tensão no
    inversor, i_q,ref médio com a rampa ONS no subtítulo, P média.
  - O card "Suportabilidade ONS" é o único com semáforo (verde dentro,
    vermelho fora), porque o TCC classifica por essa borda. Lê
    `metrics["lvrt"]` (`suportabilidade_ons`, a mesma conta do capítulo
    Código de rede do palco): "fora" = fase mais afundada abaixo da borda
    depois do 1º ciclo; subtítulo com o mínimo dela. Clique abre |V| Bus 2,
    onde a curva está desenhada ([[chart-analysis-overlays]]). Nas 4
    trifásicas: B7 e L7-8 fora, B6 e L8-9 dentro.
  - *Energização do inversor* (regime): 5% de v_d e 2° do erro.
  - A narrativa ganhou o item "Sincronismo" (falta) ou "Energização" (regime).
- **Tabela comparativa**: 9 colunas novas antes das de V médio; ver
  [[comparison-table]].
- **Aba Espectro**: destaque com o 120 Hz pela receita do TCC. A tabela de
  harmônicas usa outra janela (retangular com agrupamento IEEE 519, falta
  inteira, v_d do inversor) e dá 0,40 contra 0,39 em `bus6/2phase` e 0,013
  contra 0,0002 em `bus7/3phase`. Ela segue como está, porque serve à
  comparação com a norma ([[espectro-tabela-harmonicas]]).

Formato: casas decimais iguais às do TCC (pico e retenção com 1 casa, ms
inteiros, pu com 2 casas, 120 Hz com 4 casas abaixo de 0,01). O ponto
decimal segue o do resto do HTML (ponto, não vírgula).

## Relacionados

- [[cards-metricas]] — grupo de severidade, que segue igual
- [[pll-ts-criterion-rationale]] — revisão do critério de acomodação, agora fechado em 2°
