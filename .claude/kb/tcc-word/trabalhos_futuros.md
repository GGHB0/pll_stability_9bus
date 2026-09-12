---
name: tcc-trabalhos-futuros
description: Eixos definidos para o Cap. 7 (Trabalhos Futuros) do TCC — quais entraram, qual foi descartado e por quê
source: Discussão com o usuário em 2026-09-12
metadata:
  type: project
---

# Cap. 7 — Trabalhos Futuros: eixos definidos

> Discussão de 2026-09-12. O capítulo **já foi redigido e entregue** na
> mesma data (ver § Redação no fim deste arquivo e `pendencias.md` item 19);
> este arquivo fixa o conteúdo acordado e o que ficou de fora. Recorte pedido pelo usuário: trabalhos futuros de **melhoria do
> sistema GFL**, não migração para GFM.

## Fio condutor

A tese do Cap. 5 é que a sintonia do PLL é um **compromisso** entre imunidade
durante a falta e velocidade na recuperação, com um caso-limite
(`bus7/3phase_bad_pll`) em que o compromisso deixa de valer. Todo eixo abaixo
é uma tentativa de **quebrar esse compromisso** sem sair do paradigma GFL.

**O capítulo ficou com dois eixos: 1 e 3.** Os Eixos 2 e 4 foram propostos e
descartados pelo usuário; ficam registrados abaixo só para não serem
represtados em sessão futura.

Critério usado para aceitar um eixo: (a) nasce de um limite declarado do
próprio trabalho e (b) reaproveita a bancada já construída (32 cenários,
IAE/ISE/`t_s`, medição de escorregamento, dashboard).

## Eixo 1 — Trocar a estrutura de sincronismo ✅ aprovado

Ataca o mecanismo físico demonstrado no trabalho: sequência negativa → 120 Hz
em `v_q` → o SRF-PLL puro não distingue isso de erro de fase real.

- **DSOGI-PLL / DDSRF-PLL**: separação explícita de sequência positiva/negativa
  antes do laço.
- **MAF-PLL** ou notch adaptativo: filtragem seletiva do 120 Hz.

Gancho de honestidade disponível: o **notch fixo de 120 Hz já foi testado e
removido** do modelo (ver [[pll-notch-implementation]]). Permite redigir "a
filtragem fixa foi avaliada e descartada; a rota promissora é a separação de
sequência, que remove o distúrbio sem penalizar a banda do laço".

> Nota do usuário: linha já discutida internamente pela dupla, não coube no
> prazo do trabalho.

## Eixo 3 — Explorar a fronteira não varrida ✅ aprovado

Limite que o **próprio Cap. 6 já admite**: a impedância da rede foi observada
pela *localização da falta*, não por varredura de SCR.

- **Varredura de SCR** até o SCR crítico de perda de sincronismo, por sintonia.
- **Análise por impedância/admitância dq** (pequenos sinais), que conecta com a
  *converter-driven stability* ~10 Hz já citada no Cap. 2
  ([[stability-classification-extended]]).
- **Múltiplos IBR**: hoje só a Barra 2 é inversor. Substituir também G1 ou G3
  abre interação entre PLLs, que é onde o problema do SIN de fato mora.

> Nota do usuário: mesma situação do Eixo 1 — já conversado internamente.

## Eixo 2 — Sintonia adaptativa / normalização ❌ descartado

Primeira versão do argumento ("adicionar lógica de gain scheduling ou
congelamento do PLL") **não convenceu** o usuário. Reformulado a partir de
[[pll-gain-voltage-dependence]], que estabelece o fato técnico:

- O laço é normalizado por **constante** (`1/16.329,93 V`, pico de fase
  nominal), não pela amplitude medida.
- Logo `ω_n = √(Ki·U)` e `ξ = (Kp/2)·√(U/Ki)`: a sintonia **degrada sozinha**
  conforme a tensão afunda.
- `U = 0,2 pu` com ganhos nominais dá `ω_n = 145,5` / `ξ = 0,316` —
  **exatamente** o cenário de sintonia inadequada (ganhos ×0,2). Equivalência
  algébrica exata no modelo linearizado.

Proposta resultante, mais específica e mais barata que a primeira versão:
**normalizar o erro de fase pela amplitude estimada** (`v_q/|v|`), fixando o
ganho de laço e tornando a dinâmica invariante à profundidade do afundamento.
Congelamento do PLL e gain scheduling ficam como **segundo nível**, para o que
a normalização não cobre (`U → 0` exige limiar; o 120 Hz continua lá — daí a
dependência do Eixo 1).

**Status: descartado pelo usuário em 2026-09-12**, depois de **duas**
tentativas de argumento (gain scheduling/congelamento; e a normalização por
`v_q/|v|` a partir da dependência com `√U`). Não repropor.

O fato técnico por trás dele **continua válido e registrado** em
[[pll-gain-voltage-dependence]] — o que caiu foi transformá-lo em trabalho
futuro, não a equivalência algébrica em si.

## Eixo 4 — Suporte dinâmico de reativo (K-factor) ❌ descartado

Proposto e **rejeitado pelo usuário** em 2026-09-12. Era: implementar injeção
de reativo durante a falta conforme norma e medir o efeito sobre o PLL,
amarrando com a conclusão do ONS sobre 2023. Não repropor.

## Fora de escopo por decisão do orientador

**Salto de fase** não deve ser sugerido como trabalho futuro sem falar antes
com o Oscar — a instrução de mantê-lo fora do escopo segue valendo (ver
`content_map.md`, Cap. 5). Se voltar, volta como decisão dele.

## Redação — ✅ FEITA em 2026-09-12 (noite)

**Formato escolhido:** capítulo curto, **sem subseções numeradas**, um
parágrafo por eixo (311 palavras no total). Com dois eixos, um 7.1 e um 7.2
de um parágrafo cada ficariam raquíticos, e o Cap. 6 também não tem subseção.

**Sem referência bibliográfica nova**, de propósito: as 4 citações usadas
(RODRIGUEZ et al., 2007; TEODORESCU; LISERRE; RODRIGUEZ, 2011; WU; WANG, 2020;
STRAUSS-MINCU et al., 2026) já constavam da lista final **e** já eram citadas
em outros pontos do corpo, o que evitou engordar a pendência 15.

**Ganho colateral:** a sigla **DDSRF-PLL** estava na Lista de Abreviaturas sem
aparecer em lugar nenhum do corpo; o Eixo 1 passou a usá-la. DSOGI e MAF
ficaram por extenso ("integradores generalizados de segunda ordem duplos",
"filtragem de média móvel") justamente para não abrir siglas novas. Termos
colados do próprio texto: "Estabilidade Guiada por Conversores" (Cap. 2) e
"relação de curto-circuito".

**Cortes pedidos pelo usuário, em 4 rodadas** (registro do que NÃO voltar a
propor):

1. Versão de 4 parágrafos (~510 palavras): "tá muito grande, faz algo com
   dois parágrafos no máximo".
2. Versão de 2 parágrafos, mas rebuscada: o parágrafo 1 foi reescrito com
   frases curtas (saíram "uma vez que", "às custas de", "submetendo-as",
   "não apenas presumido"). O parágrafo 2 foi **aprovado sem alteração** e
   ficou como estava.
3. "Este trabalho caracterizou um mecanismo, não um envelope de projeto":
   removida a pedido.
4. Abertura final **escrita pelo próprio usuário**: "Para a continuidade desta
   pesquisa, mantendo a premissa de inversores operando como seguidores de
   rede, propõem-se duas frentes de investigação." (o "principais" que eu
   havia sugerido manter foi cortado por ele). Forçou concordância feminina no
   resto: "A primeira é..." / "A segunda frente é...".

**Menção ao notch já testado: cortada.** A versão de 4 parágrafos dizia que o
filtro rejeita-faixa fixo "foi avaliada em caráter preliminar ao longo do
desenvolvimento deste trabalho"; ao enxugar, a frase virou afirmação genérica
("um filtro rejeita-faixa fixo reduz essa ondulação, mas reduz junto a banda
passante"), sem expor um teste que não está no Cap. 5. Ver
[[pll-notch-implementation]].
