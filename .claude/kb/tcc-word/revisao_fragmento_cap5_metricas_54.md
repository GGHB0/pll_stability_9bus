---
name: tcc-revisao-fragmento-cap5-metricas-54
description: Métricas da Seção 5.4 do fragmento (perda de sincronismo em bus7/3phase_bad_pll) — rotação acumulada, escorregamento, retenção com valores brutos, argumento 2x2 e ressalvas
metadata:
  type: project
---

# Cap. 5 do Fragmento — Métricas da Seção 5.4

Desmembrado de [[tcc-revisao-fragmento-cap5-metricas]] em 2026-08-25 (limite de
200 linhas). As **definições fechadas** de erro de fase, retenção, `t_s` e
componente de 120 Hz continuam no arquivo pai e valem também aqui.

## 5.4 — perda de sincronismo (`bus7/3phase_bad_pll`)

Seção acrescentada em 2026-08-23 (noite). O cenário é o **único dos 16** que
não reaquisita o sincronismo depois da eliminação da falta.

### Métricas próprias desta seção

| Métrica | Definição | Valor |
|---|---|---|
| Rotação acumulada | `unwrap(atan2(vq_rede, vd_rede))` em graus, de `t_clear` ao fim | 6 916° = 19,2 voltas em 300 ms |
| Escorregamento em regime | `polyfit` de grau 1 no ângulo desenrolado, janelas de 20 ms | ~70 Hz (65 a 81 Hz de 0,76 s em diante) |
| Retenção de `v_d` | mesma receita das demais seções | 8,2% (nominal: 9,2%) |
| P pós-falta | média de `P_ufv_pu` em `[t_clear, t_end]` | −0,30 pu (mín. −1,07) |
| Q pós-falta | mín/máx em `[0,85, 1,0]` s | −0,94 a 1,97 pu |
| Pulsação de `\|v\|` no PAC | `hypot(vd_ufv, vq_ufv)` em `[0,85, 1,0]` s | 0,14 a 1,11 pu, média 0,70 |
| Divergência ref × medido | médias e extremos em `[0,85, 1,0]` s | `i_d` ref 0,92 / med. −0,66 a 1,34; `i_q` ref −0,24 / med. até −1,76 |

### Retenção de `v_d` — valores brutos (numerador/denominador)

Pedido do usuário (2026-08-25): a razão sozinha não mostra de onde vem o
número. Recalculado direto do `sim_data.csv` de cada cenário com a receita da
seção "Definições fechadas" do arquivo pai (média em
`[t_fault + 2 ciclos, t_clear]` sobre média em `[t_fault − 50 ms, t_fault)`):

| Cenário | `t_fault` / `t_clear` | média pré-falta (`v_d`) | média durante a falta (`v_d`, >2 ciclos) | retenção |
|---|---|---|---|---|
| Nominal `bus7/3phase` | 0,3 / 0,4 s | 0,9891 pu | 0,0908 pu | 9,18% ≈ 9,2% |
| Sintonia inadequada `bus7/3phase_bad_pll` | 0,6 / 0,7 s | 0,8229 pu | 0,0676 pu | 8,22% ≈ 8,2% |

O ponto que a tabela deixa explícito: os **denominadores diferem**
(0,989 pu contra 0,823 pu, o ponto de operação degradado da Seção 5.1), mas a
**razão** dá quase o mesmo valor nos dois casos. É essa proximidade nas
razões, apesar das bases pré-falta diferentes, que autoriza o texto a dizer
"a profundidade do afundamento é praticamente a mesma" e atribuir a diferença
de comportamento pós-falta à sintonia, não à severidade.

### Figura didática da retenção (2026-08-26)

O termo "retenção" aparecia no Cap. 5 só com o valor fechado, sem que o texto
mostrasse de onde sai a razão. Usuário: *"apenas lendo o texto não consigo
identificar"*. Duas alternativas foram descartadas por ele: definição em
cláusula curta na primeira ocorrência (§5.2) e subseção nova de métricas no
Cap. 4. **Escolha: uma figura só, o painel duplo, dentro do §5.4**, mantendo a
conta fechada visível dentro da própria figura.

Gerador: `scripts/gen_retencao_didatica.py` (SVG + PNG em `assets/charts/`,
mesma convenção de `gen_fault_waveforms.py`). Produz duas figuras:

| Arquivo | Conteúdo | Destino |
|---|---|---|
| `retencao_comparacao` | painel duplo nominal × sintonia inadequada | §5.4 (escolhido) |
| `retencao_construcao` | painel único, só o caso nominal | gerado a pedido do usuário, sem destino definido no TCC |

Decisões de desenho do painel duplo:

- **Eixo X em tempo relativo ao início da falta**, porque `t_fault` difere entre
  os cenários (0,3 s no nominal, 0,6 s na sintonia inadequada). Sem isso os dois
  painéis não alinham. É a única figura do Cap. 5 que não usa tempo absoluto.
- **Eixo Y compartilhado** (`sharey`), pelo mesmo motivo do `YLIM_GROUPS` de
  `gen_fault_waveforms.py`: é justamente a diferença das bases pré-falta
  (0,989 contra 0,823 pu) que a figura precisa deixar visível.
- A barra vermelha superior marca a **duração real da falta** (0,1 s), distinta
  da janela de medição laranja, que começa 2 ciclos depois. Na primeira versão
  o rótulo "falta" ficava sobre a faixa laranja e dava a entender que a falta
  começava ali.

**Inserida no §5.4 em 2026-08-26** como Figura 5.11, empurrando as antigas
5.11/5.12/5.13 para 5.12/5.13/5.14. Fragmento passou a 113 parágrafos e 18
imagens. Detalhes da inserção, largura escolhida e o defeito de marca-texto
encontrado na revisão visual em [[tcc-revisao-fragmento-cap5-figuras]].

O parágrafo de abertura do §5.4 ganhou, depois da frase da retenção, a chamada
da figura com a definição em palavras: razão entre o valor médio da componente
de eixo direto durante a falta, descartados os dois primeiros ciclos, e o valor
médio nos 50 ms anteriores; mais a observação de que os dois cenários partem de
patamares distintos (0,989 e 0,823 pu) e ainda assim dão razões praticamente
iguais.

### Origem da métrica explicitada no texto (2026-08-28)

Usuário: *"de onde vc pegou a referência de fazer isso [...] de calcular a
retenção como média pré-falta com a falta"*. A resposta é que **o conceito**
(tensão retida durante o afundamento) é a grandeza padrão dos códigos de rede
para parametrizar suportabilidade a subtensões (LVRT, tratada no §2.5.2 do
fragmento), mas **a receita exata** (razão sobre a média medida nos 50 ms
anteriores à falta, e não sobre a tensão nominal; descarte dos 2 primeiros
ciclos; aplicada a `vd_rede`) é escolha interna da auditoria do Cap. 5 de
2026-08-23, registrada só neste KB. Não vem de `src/pipeline` (o `vavg` de
`loader.py` compartilha apenas "média na janela de falta", sem denominador
pré-falta, sem descarte de ciclos, sobre `vbus2`) nem de citação.

Correção registrada: numa fala anterior eu disse que a receita era "idêntica à
de `src/pipeline`" — está errado e foi retratado.

O run[2] (minha adição não realçada) do parágrafo 90 foi reescrito para deixar
isso no próprio texto: a tensão retida é a grandeza dos códigos de rede
(§2.5.2, ali como fração da nominal); normalizar pela média pré-falta medida é
adaptação deste trabalho, feita para descontar o ponto de operação degradado da
Seção 5.1 e isolar o efeito da sintonia. Só o run[2] mudou (497 → 962 chars); o
run[1], anotação amarela do usuário (284 chars), ficou intacto, conferido na
renderização da página em PDF.

**O escorregamento não é artefato de amostragem.** O passo do CSV é 5 µs, então
70 Hz são amostrados a ~0,085° por ponto: as amostras brutas de `v_d`/`v_q`
percorrem a volta suavemente. Conferido linha a linha antes de escrever a seção.
Derivação completa (por que `arctan2` e não `arctg` da razão, por que o
`unwrap` não se engana, e a rota alternativa via `theta_err_rad` já gravado
pelo modelo) em [[pll-cycle-slip-measurement]], com nota técnica em PDF.

**Sinal do escorregamento:** o erro `atan2(vq, vd)` é o ângulo do vetor da rede
**no referencial do PLL**. Ele decresce, logo o referencial estimado gira mais
rápido que a rede (~130 Hz absolutos). O texto afirma "70 Hz acima da frequência
da rede", que é o que a medição sustenta sem depender de convenção de sinal.

### Argumento 2×2 (o que a seção realmente prova)

Nem a profundidade nem a sintonia, isoladas, produzem o fenômeno:

| | Retenção | t_s pós-falta |
|---|---|---|
| Barra 7, sintonia nominal | 9,2% | 98 ms |
| Barra 6, sintonia inadequada | 58,4% | 106 ms |
| **Barra 7, sintonia inadequada** | **8,2%** | **não reaquisita** |

`line7_8/3phase_bad_pll` **não** entra nessa comparação, apesar de caber nela:
é o run anômalo descartado em [[cenarios-simulados]].

### Ressalvas registradas no próprio texto

- A janela termina 300 ms após a eliminação, então a afirmação é "não reaquisita
  dentro da janela simulada", nunca "jamais reaquisita".
- O cenário parte do ponto de operação degradado da safra de julho
  (`v_d` pré-falta 0,823 pu), o mesmo das Figuras 5.2 e 5.3, e é comparado com
  um nominal que parte de 0,989 pu. A retenção quase idêntica (8,2% × 9,2%) é
  o que autoriza atribuir a diferença à sintonia, e isso está dito no texto.

### Escala Y

`bus7/3phase_bad_pll` entrou no grupo `sim_localizacao`. A faixa dq dele
(−1,075 a 1,112) já cabia na união existente, então as Figuras 5.4 e 5.5 saíram
**byte a byte idênticas** da regeneração (MD5 conferido) e a 5.11 passou a
dividir o eixo com elas.
