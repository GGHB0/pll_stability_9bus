---
name: ieee519-structure
description: Mapa de cláusulas e das cinco tabelas do IEEE 519-2014 — valores, páginas (PDF vs impressa), notas de rodapé e o que se aplica ou não à Barra 2
source: IEEE 519-2014, Cl.3-5 e Anexos A-D (págs. impressas 3-11 = PDF 15-23)
references:
  - "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems. IEEE Std 519-2014, 2014."
metadata:
  type: reference
---

# IEEE 519-2014 — mapa de cláusulas e tabelas

Complementa [harmonic_significance_criteria.md](harmonic_significance_criteria.md)
(de onde vem cada limite aplicado) e
[harmonic_measurement_conditions.md](harmonic_measurement_conditions.md)
(Cláusula 4 — como medir, e como a FFT do projeto se compara). Este arquivo é o
mapa de navegação da norma: onde está cada coisa e o que **não** usamos.

## Localização no PDF

Arquivo `553147549-IEE-Std-519-2014.pdf` (29 págs.):
**página do PDF = página impressa + 12**.

O PDF não está mais em `Downloads` (só o atalho em `Recent`). Extração de
texto das Cl.4-5 em `~/pdfext/ieee519_5_limits.txt`; TOC em
`~/pdfext/toc_ieee519.txt`.

| Cláusula | Pág. impressa | Pág. PDF |
|---|---|---|
| 1 Overview / 1.1 Scope / 1.2 Purpose | 1-2 | 13-14 |
| 2 Normative references / 3 Definitions | 3-4 | 15-16 |
| **4 Harmonic measurements** (4.1-4.4) | **4-5** | **16-17** |
| **5 Recommended harmonic limits** | **5-10** | **17-22** |
| 5.1 + Tabela 1 (tensão) | 6 | 18 |
| 5.2 + Tabela 2 (corrente 120 V-69 kV) | 6-7 | 18-19 |
| 5.3 + Tabela 3 (69-161 kV) | 7-8 | 19-20 |
| 5.4 + Tabela 4 (>161 kV) | 8-9 | 20-21 |
| 5.5 + Tabela 5 + Eq.(3) | 9-10 | 21-22 |
| Anexo A (inter-harmônico/flicker) | 11 | 23 |
| Anexo B (TIF) / C (notches) / D (bibl.) | 13/15/17 | 25/27/29 |

## Filosofia da norma — responsabilidade conjunta

Abertura da Cl.5 (pág. impressa 5): *"harmonic limits are recommended for both
voltages and currents"*. A premissa é que o **usuário limita a corrente
injetada** e o **dono do sistema limita a tensão resultante** — se todos
respeitarem a corrente, a distorção de tensão fica aceitável sozinha. Tabela 1
(tensão) e Tabelas 2/3/4 (corrente) são os dois lados do mesmo contrato, não
alternativas.

Dois avisos de escopo, mesma página, válidos para todas as tabelas:

- Os limites valem **só no PCC** — *"should not be applied to either individual
  pieces of equipment or at locations within a user's facility"*. Dentro da
  instalação os valores são legitimamente maiores (falta diversidade e
  cancelamento entre fontes).
- Todas as tabelas valem só para **múltiplos inteiros da fundamental**.
  Inter-harmônico sai para o Anexo A, caso a caso.

## Cláusula 3 — definições que mudam a leitura das tabelas

| Termo | Definição (pág. impressa 3-4) |
|---|---|
| **PCC** | ponto da rede pública eletricamente mais próximo de uma carga, onde outras cargas estão ou poderiam ser conectadas; fica **a montante** da instalação. Aqui: Barra 2 |
| **TDD** | RMS do conteúdo harmônico até a **50ª ordem**, excluindo inter-harmônicos, em % da **corrente de demanda máxima** |
| **THD** | idem, mas em % da **fundamental** |
| **short-circuit ratio** | razão corrente de curto / corrente de carga — é o `Isc/IL` que escolhe a linha da tabela |

TDD e THD têm **o mesmo numerador e denominadores diferentes**. O THD explode
sob carga leve (denominador pequeno) mesmo com harmônico absoluto irrelevante;
o TDD evita esse falso positivo usando uma demanda de referência fixa. É a
mesma motivação que leva o IEEE 1547-2018 a trocar `IL` por `I_rated` e chamar
o índice de TRD — ver
[ieee1547_power_quality_clause7.md](ieee1547_power_quality_clause7.md).

## Tabela 1 — distorção de TENSÃO (§5.1, pág. impressa 6)

| Tensão V no PCC | Individual (%) | THD (%) |
|---|---|---|
| V ≤ 1,0 kV | 5,0 | 8,0 |
| **1 kV < V ≤ 69 kV** | **3,0** | **5,0** |
| 69 kV < V ≤ 161 kV | 1,5 | 2,5 |
| 161 kV < V | 1,0 | 1,5 ᵃ |

ᵃ pode ir a 2,0% se a causa for terminal HVDC cujo efeito atenua onde futuros
usuários se conectariam.

Critérios de aplicação (**dois**, não três): 99º percentil diário *very short*
(3 s) < **1,5×** a tabela; 95º percentil semanal *short* (10 min) < a tabela.
Base: **% da tensão nominal de frequência fundamental no PCC**, não da tensão
medida no instante.

**É a nossa linha** (Barra 2 = 20 kV) → `VOLT_INDIVIDUAL_LIMIT_PU = 0,03`. O
limite de tensão é **flat por ordem**: a norma não escalona tensão por ordem
harmônica, só corrente. E é a **única** fonte possível para esse limite — o
IEEE 1547-2018 não define limite de distorção de tensão (ver Tabela 15 do guia).

## Tabela 2 — corrente, 120 V a 69 kV (§5.2, pág. impressa 7)

| Isc/IL | 3≤h<11 | 11≤h<17 | 17≤h<23 | 23≤h<35 | 35≤h≤50 | TDD |
|---|---|---|---|---|---|---|
| **< 20** ᶜ | **4,0** | **2,0** | 1,5 | 0,6 | 0,3 | **5,0** |
| 20 < 50 | 7,0 | 3,5 | 2,5 | 1,0 | 0,5 | 8,0 |
| 50 < 100 | 10,0 | 4,5 | 4,0 | 1,5 | 0,7 | 12,0 |
| 100 < 1000 | 12,0 | 5,5 | 5,0 | 2,0 | 1,0 | 15,0 |
| > 1000 | 15,0 | 7,0 | 6,0 | 2,5 | 1,4 | 20,0 |

Notas de rodapé:

- **a** — pares limitados a **25% do ímpar** correspondente.
- **b** — distorções que resultem em **offset CC** (ex.: conversor de meia-onda)
  **não são permitidas**. Não é limite numérico, é proibição.
- **c** — *"All power generation equipment is limited to these values of current
  distortion, regardless of actual Isc/IL."* **É a nota que decide o caso
  deste TCC**: geração cai obrigatoriamente na linha `<20`, a mais restritiva,
  sem calcular Isc/IL.

Critérios de aplicação — **três**, mais rígidos que os de tensão: 99º percentil
diário *very short* < **2,0×**; 99º percentil semanal *short* < **1,5×**; 95º
percentil semanal *short* < a tabela.

Base: **% de `IL`**, definido logo abaixo da tabela como a soma das demandas
máximas dos **12 meses anteriores dividida por 12** — é essa definição que torna
`IL` incomputável numa simulação EMT de segundos.

**É a nossa linha** → `CURR_ODD_LIMIT_PU = 0,04` e o
`CURR_ODD_LIMIT_11_16_PU = 0,02` (interino). A nota "a" (pares a 25%) **não**
é aplicada: fica sobrescrita pela escala "Relaxed Evens" do IEEE 1547-2018.

## Tabelas 3 e 4 — corrente em alta tensão (§5.3/§5.4) — NÃO usadas

**Tabela 3** (69 kV < V ≤ 161 kV, pág. impressa 8) é a Tabela 2 com os valores
**pela metade**: linha `<20` = 2,0 / 1,0 / 0,75 / 0,3 / 0,15, TDD 2,5. Mesmas
notas a/b/c, mesmos três critérios de percentil.

**Tabela 4** (V > 161 kV, pág. impressa 9) tem só **três** faixas de Isc/IL (não
cinco) e o corte da linha restritiva muda de `<20` para **`<25`**: 1,0 / 0,5 /
0,38 / 0,15 / 0,1, TDD 1,5.

Padrão das três tabelas de corrente: **quanto maior a tensão do PCC, mais
apertado o limite** — em transmissão a impedância é menor, a mesma corrente
harmônica gera distorção de tensão que se propaga para muito mais gente.
Nenhuma das duas se aplica à Barra 2 (20 kV).

## Tabela 5 — multiplicadores de aumento (§5.5, págs. impressas 9-10) — NÃO usada

A única tabela que **afrouxa** limites, como recompensa por mitigação:

| Ordens mantidas ≤ 25% dos valores das Tab. 2/3/4 | Multiplicador |
|---|---|
| 5, 7 | 1,4 |
| 5, 7, 11, 13 | 1,7 |
| 5, 7, 11, 13, 17, 19 | 2,0 |
| 5, 7, 11, 13, 17, 19, 23, 25 | 2,2 |

A Equação (3) revela a origem: **Multiplicador = √(p/6)**, com `p` o número de
pulsos de um retificador trifásico (6, 12, 18, 24…), que produz harmônicos
característicos em ordens `p(n±1)`. Ir para 12 pulsos elimina 5ª/7ª e "ganha"
√2 ≈ 1,4 de folga. Condição de uso: **todas** as não-características,
**incluindo as pares**, abaixo de 25% dos valores da tabela.

Não aplicável a inversor PWM de dois níveis. Vale citar no TCC como evidência de
que o 519 foi escrito com **conversores comutados pela rede** em mente — o que
explica por que o IEEE 1547 precisou de uma cláusula própria para DER.

## Anexos (informativos) — NÃO usados

| Anexo | Tema | Relevância |
|---|---|---|
| A | limites de **inter-harmônico de tensão** por **flicker** de lâmpada (IEEE 1453 / IEC 61000-4-15) | é a resposta ao "e o que não é múltiplo inteiro?" |
| B | **TIF** — Telephone Influence Factor | legado (telefonia analógica) |
| C | limites de **entalhes de comutação** | fenômeno de tiristor comutado pela rede |
| D | bibliografia | — |

O Anexo A merece uma linha no TCC: a ressonância do filtro LCL
(`ω_res = 9068,99 rad/s ≈ 1443 Hz ≈ 24,05·f₁`) **não é múltiplo inteiro** de
60 Hz — formalmente é inter-harmônico, e o 519 manda tratar caso a caso. É por
isso que ela aparece no espectro como marcador (`SPEC_MARKERS`) mas **não** na
tabela de harmônicas.

## Resumo — o que do 519 é nosso

| Elemento | Pág. impressa | Usamos? |
|---|---|---|
| Cláusula 4 (medição) | 4-5 | Parcialmente — ver [harmonic_measurement_conditions.md](harmonic_measurement_conditions.md) |
| Tabela 1, linha 1-69 kV | 6 | **Sim** → 3,0% |
| Tabela 2, linha `<20` + nota "c" | 7 | **Sim** → 4,0% / 2,0% |
| Nota "a" (pares a 25%) | 7 | Não — sobrescrita pelo 1547 |
| Tabelas 3 e 4 | 8-9 | Não (classe de tensão errada) |
| Tabela 5 (multiplicadores) | 9-10 | Não (é para multipulso) |
| Anexos A-C | 11+ | Não |
