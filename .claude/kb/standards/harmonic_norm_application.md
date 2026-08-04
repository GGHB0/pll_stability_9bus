---
name: harmonic-norm-application
description: Como os critérios de significância de harmônico (ver harmonic-significance-criteria) se aplicam aos dados deste projeto — checagem por ordem em abc vs dq, isenção por segmento, e notação única para as variáveis de base de corrente (Isc/IL/I_rated), evitando invocar TDD
source: IEEE 519-2014 §5 Tabela 2 e nota "c" (p.18-19); IEEE 1547.2-2023 §7.3 Tabela 15 (p.144-147)
references:
  - "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems. IEEE Std 519-2014, 2014."
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
metadata:
  type: reference
---

# Aplicação dos critérios de harmônico ao dashboard

Continuação de [harmonic_significance_criteria.md](harmonic_significance_criteria.md)
(as três noções de "significativo" e os limites originais). Este arquivo
cobre como isso vira checagem célula a célula na tabela do dashboard.

## abc × dq — qual norma vale em qual domínio

Os limites por ordem harmônica `h` (Tabela 2 do IEEE 519-2014, §7.3 do IEEE
1547-2018) só são bem definidos no domínio **abc** — a transformada de Park
desloca cada componente por `±f₁` conforme a sequência (positiva: ordem `n` →
`(n-1)·f₁` no dq; negativa: ordem `n` → `(n+1)·f₁`), então dois harmônicos de
ordens diferentes podem cair no **mesmo bin** do espectro dq (5ª
negativa + 7ª positiva → ambas em 6f₁ = 360 Hz; 11ª + 13ª → ambas em
12f₁ = 720 Hz — derivação formal e mapa completo de bins em
[harmonic_dq_frame_mapping.md](harmonic_dq_frame_mapping.md)).
Um pico dq nesses bins não é atribuível a uma ordem `h`
específica, então não dá pra comparar direto com a linha correspondente da
Tabela 2.

Consequência prática: checagem de conformidade com IEEE 519/1547 deve usar o
espectro em modo **abc** (fases a/b/c), casando os marcadores `SPEC_MARKERS`
(f₁, 3f₁, 5f₁, 7f₁) com a tabela de harmônicas 1–7. O espectro em modo **dq**
não serve para essa checagem — ele é um proxy da **fração de sequência
negativa** (pico isolado em 2f₁ = 120 Hz), critério de desequilíbrio
(limiar empírico da TeseAGP, análise da fração `b` do Yazdani — itens 2/3 de
`harmonic_significance_criteria.md`), não um limite de distorção harmônica
por ordem. A maioria dos cenários já tem `sim_data_abc.csv` (re-exportado
pelo Bruno desde [[resimulacao-abc|kb/simulation/resimulacao-abc]]), então a
checagem por ordem em abc está disponível na maior parte do dashboard — os
poucos cenários sem esse CSV mostram só dq, útil para severidade de
desequilíbrio, não para conformidade normativa.

**A fundamental do dq não existe no espectro exibido**: `_amplitude_spectrum`
remove a média antes da FFT (`y_u -= y_u.mean()`), e a fundamental do dq é
justamente essa componente DC — ela sai junto com o offset, não sobra como
pico em 60 Hz. Isso não é só efeito do código: é a mesma rotação dq da seção
acima aplicada à própria fundamental (ordem `n=1`, sequência positiva) —
`(n-1)·f₁ = 0`, derivação completa em
[harmonic_dq_frame_mapping.md](harmonic_dq_frame_mapping.md). A linha h=1ª das
colunas d/q na tabela não é "a fundamental dq"; é o resíduo em 60 Hz que sobra
depois de remover o DC (~0,0008 pu em regime, cresce quando há conteúdo não
estacionário no sinal).

**Achado da verificação (2026-07-29):** o critério de desequilíbrio dq **não
pode** herdar a mesma isenção do segmento "Durante a falta" que a checagem
abc/IEEE usa — a sequência negativa só é grande justamente durante a falta;
isentar os dois critérios juntos faz o alerta de desequilíbrio nunca disparar
na prática (confirmado em `bus4/1phase`: 30%+ em h=2ª durante a falta, zero
alerta até a correção). Os dois critérios têm naturezas diferentes: IEEE
519/1547 são normas de **regime permanente** (não fazem sentido durante o
curto-circuito em si); o patamar da TeseAGP é sobre **severidade do
distúrbio**, que é maior exatamente durante a falta.

## Normalização das variáveis de corrente — notação única deste projeto

Cada norma citada nomeia a base de corrente com um símbolo diferente, o que
confunde ao reler depois. Este projeto usa **uma notação única**, mesmo
citando normas distintas:

| Símbolo | Papel na norma de origem | Usado neste projeto? | Valor aqui |
|---|---|---|---|
| `Isc` | corrente de curto-circuito disponível no PCC — só serve para escolher a linha da Tab.2 do IEEE 519-2014 (razão Isc/IL) | **Não.** A nota "c" da Tab.2 fixa a linha `<20` (a mais restritiva) para toda unidade geradora, independente do Isc/IL real na Barra 2 | — |
| `IL` | corrente de demanda máxima, média móvel de 12 meses de operação real — base de TODOS os limites da Tab.2 do IEEE 519-2014, individuais e do índice agregado (TDD) | **Não.** Não existe numa simulação EMT de segundos | — |
| `I_rated` | corrente nominal do inversor (dado de projeto) — substitui `IL` em toda a Tabela 15 do guia 1547.2-2023: limites individuais **e** o índice agregado, que muda de nome para TRD | **Sim — é a base de todos os limites de corrente do dashboard** | `1,0 pu`, confirmado por `id_ufv_ref_pu = 1,0` constante em regime permanente (`output/results/regime/sim_data.csv`) |

Consequência: os limites de corrente do dashboard (4% h ímpar; 1%/2%/3% em
h=2ª/4ª/6ª) são sempre "**% de `I_rated`**", nunca "% de `IL`" — mesmo quando
o valor numérico coincide com a Tab.2 do IEEE 519-2014 (definida sobre `IL`).
A fonte efetiva de todo limite de corrente aplicado no dashboard é o **IEEE
1547-2018 §7.3** (Tabela 15 do guia 1547.2-2023); o IEEE 519-2014 só explica
de onde os valores vieram originalmente (linha `<20` da Tab.2 — ver item 1
de `harmonic_significance_criteria.md`).

## O que vai na tela vs. o que fica no KB

Separação decidida em 2026-08-02, ao reformular a legenda da tabela de
harmônicas do dashboard: **a tela carrega a regra aplicada; o KB carrega o
percurso até ela.**

| Vai na legenda do dashboard | Fica só aqui no KB |
|---|---|
| o limite numérico (4% ímpar; 1/2/3% na 2ª/4ª/6ª; 3% de tensão) | a razão `Isc/IL` e por que a linha `<20` é a obrigatória (nota "c") |
| a base do percentual, em linguagem direta ("corrente nominal do inversor", "tensão nominal da Barra 2") | a notação `Isc`/`IL`/`I_rated` e o mapeamento entre normas (tabela acima) |
| a norma citada de forma curta (IEEE 1547-2018 §7.3; IEEE 519-2014 Tab.1) | por que `IL` foi descartado (não computável em simulação EMT) e a genealogia 519 → 1547 dos valores |
| o que a cor significa e em quais segmentos vale | os achados de verificação (isenção por segmento, resíduo dq em 60 Hz) |
| referências em forma curta, para o leitor achar a fonte | a citação bibliográfica completa (`references:` no frontmatter) |

**Why:** a legenda existe para o leitor do dashboard (banca, orientador)
decidir *se aquela célula vermelha é problema*, não para reconstituir a
derivação do limite. Despejar a justificativa na tela deixa a legenda longa
demais para ser lida e, pior, faz o critério aplicado competir por atenção
com a discussão que levou até ele.

**TDD não é usado neste projeto** — nem no código, nem em explicação. A
tabela de harmônicas do dashboard só compara **limites individuais por
ordem**, nunca um índice agregado. O índice agregado da norma efetivamente
usada aqui (IEEE 1547-2018) chama-se **TRD**, não TDD, e usa `I_rated` em
vez de `IL`. TRD é matematicamente calculável a partir dos dados já em pu —
`√(Σ Iₕ², h=2…50) / I_rated`, limite 5% na Tabela 15/§7.3 — mas **não está
implementado** no dashboard (nenhuma ocorrência de TDD/TRD/THD em `src/`);
citado aqui só para não reintroduzir "TDD" ao explicar os limites deste
projeto.
