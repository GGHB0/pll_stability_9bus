---
name: harmonic-significance-criteria
description: Critérios da literatura para o que conta como harmônico de tensão/corrente "significativo" em pu — normas de conformidade (IEEE 519/1547) vs. rejeição a distúrbio (TeseAGP) vs. criério funcional de PLL (Yazdani)
source: TeseAGP p.31-39,58-60,135-138,189-193; Yazdani & Iravani §4.2.4,4.3.3,12.5.1-12.5.7 (p.103-113,376-393); IEEE 1547.2-2023 §7.3 (p.144-147); IEEE 519-2014 §5 (p.17-21)
references:
  - "ALVES, André Gustavo Pereira. Metodologia para Auto-Ajuste de Controladores de Corrente em Conversores Fonte de Tensão Conectados a Redes Sujeitas a Distúrbios Harmônicos. Tese (Doutorado em Engenharia Elétrica) — COPPE/UFRJ, Rio de Janeiro, 2022."
  - "YAZDANI, Amirnaser; IRAVANI, Reza. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. Hoboken: John Wiley & Sons / IEEE Press, 2010. ISBN 978-0-470-52156-4."
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
  - "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems. IEEE Std 519-2014, 2014."
---

# Critérios de Harmônico Significativo — Normas vs. Literatura

Não existe um único número universal. Três noções diferentes de "significativo"
aparecem na literatura consultada, cada uma útil para um propósito distinto.

## 1. Conformidade normativa (limite máximo aceitável)

TeseAGP (p.58, §2.5) cita explicitamente: "normas como a **IEEE 519-2014**[14]
e **IEEE 1547-2018**[15] estabelecem limites para as componentes harmônicas de
corrente em **unidades geradoras**". Como o inversor deste TCC é uma unidade
geradora conectada ao SIN (Barra 2), essas duas normas são as aplicáveis — **não
o PRODIST Módulo 8** (ANEEL), que rege apenas conexões de distribuição (BT/MT).
Correção registrada em 2026-07-28 (usuário).

**IEEE 519-2014 §5** (extraído de `553147549-IEE-Std-519-2014.pdf`, págs.
impressas 5-10 = PDF 17-22). **Mapa completo das cinco tabelas, notas de
rodapé e anexos em [ieee519_structure.md](ieee519_structure.md)**; aqui ficam
só as linhas que se aplicam à Barra 2:

- *Tabela 1* (tensão), classe **1 kV < V ≤ 69 kV**: **3,0% individual /
  5,0% THD**, em % da tensão nominal no PCC. Limite **flat por ordem** — a
  norma não escalona tensão por ordem harmônica.
- *Tabela 2* (corrente 120 V-69 kV), linha **`Isc/IL < 20`**: **4,0%**
  (3≤h<11), **2,0%** (11≤h<17), 1,5% / 0,6% / 0,3% nas faixas seguintes,
  **TDD 5,0%** — tudo em % de `IL`. Pares a 25% do ímpar correspondente
  (nota "a").

**Nota "c" da Tabela 2 (crítica para este TCC):** *"All power generation
equipment is limited to these values of current distortion, regardless of
actual Isc/IL"* — todo equipamento de geração fica obrigado à linha **<20**
(a mais restritiva), independente da relação Isc/IL real na Barra 2.

**Aplicação à Barra 2 (20 kV, base 100 MVA):** cai na faixa "1 kV < V ≤
69 kV" → tensão: **3,0% individual / 5,0% THD**. Corrente (unidade
geradora, linha <20 obrigatória): **4,0%** em h<11, TDD **5,0%**, pares
≤25% do ímpar correspondente. Com `Irated ≈ 1,0 pu` na base do inversor,
isso traduz direto para pu de corrente do dashboard: **0,04 pu** (h<11
ímpar), **0,01 pu** (h<11 par), **0,05 pu** (TDD/TRD) — comparável com
`id_ufv_pu`/`iq_ufv_pu`/`iabc_inverter`.

**IEEE 1547-2018 §7.3 "Limitation of current distortion"** (extraído de
IEEE 1547.2-2023, Application Guide, págs. impressas 144-146 = PDF 145-147 —
arquivo `805035543-Ieee-Standard-1547-2018.pdf`; cláusula distinta da de
ride-through já documentada em
[ieee1547_ride_through.md](ieee1547_ride_through.md)). **Mapa da Cláusula 7
inteira — §7.1 a §7.5, Tabelas 15/16, notas de rodapé 118/119 e a
condicionante do transformador — em
[ieee1547_power_quality_clause7.md](ieee1547_power_quality_clause7.md)**: com
a DER servindo carga linear balanceada, a injeção de corrente harmônica no
PCC não pode exceder **4%** em harmônicos ímpares individuais, **1% / 2% /
3% / 4%** nos harmônicos pares de 2ª / 4ª / 6ª / 8ª ordem, e **5% TRD**
(Total Rated Distortion — em % da corrente nominal `Irated`, e não da
demanda máxima como no índice TDD clássico do IEEE 519; mudança de índice
registrada na Tabela 15 do guia). Aplica-se a tensões de 120 V a 69 kV,
adaptado do IEEE 519-2014, e **exclui** explicitamente qualquer harmônico já
presente na tensão da Area EPS antes da conexão da DER (§7.3.1) — ou seja, é
um limite de contribuição da DER, não de distorção total do sistema.

**Nota de consistência:** os 4,0%/TDD 5,0% batem entre as duas normas (o
1547-2018 herda a linha <20 do 519-2014 justamente porque geração cai
sempre nela). Mas os **pares divergem**: 519-2014 usa regra fixa de 25% do
ímpar (1,0% para todo h par <11); 1547-2018 usa escala progressiva
1/2/3/4% para 2ª/4ª/6ª/8ª — o próprio guia rotula isso de "Relaxed Evens"
(Tabela 15), uma flexibilização proposital para unidades geradoras.

**Lacuna confirmada em 2026-08-04 — Tabelas 17/18 do guia 1547.2-2023 (as
tabelas de verdade, com faixas por ordem tipo `11≤h<17`) existem só como
**imagem** no PDF `805035543-Ieee-Standard-1547-2018.pdf`.** A extração de
texto (pypdf) pegou o título de cada tabela e "Source: Table 26/27 of IEEE
Std 1547-2018", mas nenhum número de dentro delas — confirmado em duas
tentativas de extração (`ieee1547_73_power_quality.txt` e
`skim_ieee1547_05.txt`, ambos com o mesmo buraco). O único texto corrido com
números reais é o já citado acima (4%/1%/2%/3%/4%, todos para `h<11` — o
guia chama isso de "low-order harmonic range" explicitamente), que não cobre
`h≥11`.

**Decisão interina (2026-08-04, usuário):** para a faixa `11≤h<17` (ordens
11ª/13ª, usadas no dashboard para o bin dq de 720 Hz), usar o valor da
**IEEE 519-2014 Tabela 2, linha `<20`: 2,0%** — confirmado por extração de
texto real (`ieee519_5_limits.txt`), não por imagem. Isso é uma **inferência
por herança**, não o número lido direto da Tabela 17 do guia 1547-2018: o
próprio texto da 1547.2-2023 diz que a exigência do 1547-2018 "is based on
the most restrictive harmonic current limits from IEEE Std 519-2014" e os
valores de `h<11` batem exatamente entre as duas normas, o que torna
plausível que a faixa `11≤h<17` também bata — mas isso não foi confirmado
lendo a Tabela 17 em si. Marcado como **`CURR_ODD_LIMIT_11_16_PU` (a
confirmar)** no código e com tooltip equivalente na tela do dashboard. Se a
Tabela 17/18 for extraída depois (ex.: OCR ou fonte com texto real), este
valor deve ser conferido e o rótulo "a confirmar" removido.

**As Tabelas 17/18 são legíveis na tela** (pág. impressa 144 = PDF 145) — o
que falta é extração por texto, não acesso. Se alguém abrir o PDF nessa
página e transcrever a faixa `11≤h<17`, o valor interino acima deixa de ser
inferência.

**Condições e ressalvas do limite do 1547** (detalhe e citações literais em
[ieee1547_power_quality_clause7.md](ieee1547_power_quality_clause7.md)):

- O requisito vale sob **carga equilibrada e linear** e mede só a
  **contribuição da DER** (exclui harmônico já presente na tensão da Area EPS).
- **Nota 118:** os limites são valores de projeto para **regime normal com
  duração > 1 h**; em **partida ou condição inusual** admite-se excedê-los em
  **50%**. É a base normativa do `T_SETTLE` e do tratamento do segmento de
  falta — ver [harmonic_measurement_conditions.md](harmonic_measurement_conditions.md).
- **§7.3.1:** o requisito é definido em condição que a norma admite ser
  irrealizável em campo, servindo de base para **ensaio de tipo em
  laboratório**. É o que torna o 1547 metodologicamente compatível com uma
  simulação EMT de inversor único, ao contrário do 519 (estatístico, de campo).
- **§7.3.3:** os limites das Tab. 17/18 só são permitidos se o **transformador
  de conexão não vir mais de 5%** da corrente nominal em harmônico
  (IEEE C57.12.00; metodologia de avaliação no IEEE C57.110).
- **Nota 119** fala em "TDD… 15-min or 30-min demand", contradizendo a Tabela
  15 e os títulos das Tab. 17/18. É resíduo editorial herdado do 519 —
  prevalece **TRD sobre `Irated`**.

**Também confirmado por texto (não é inferência):** o 8º harmônico par tem
limite de **4%** — está na mesma frase corrida citada acima ("4% at 8th
order harmonic"), então entra no dashboard como dado direto, sem ressalva.
Já os pares de ordem 10ª e 12ª (que aparecem se a tabela do dashboard for
estendida até o bin de 720 Hz) não têm valor confirmado em lugar nenhum —
ficam sem limite aplicado (célula sem destaque de violação), não um valor
inventado.

## 2. Rejeição a distúrbio (significância funcional/empírica)

TeseAGP §5.2.2 "Susceptibilidade a harmônicos de ordem elevada" (p.135):
um **distúrbio de tensão de 3% (0,03 pu)** na frequência de ressonância do
filtro LCL, sem compensação, amplifica para **7,02% (0,07 pu)** de harmônico
de corrente em regime permanente — chamado explicitamente de "indesejado".
Com controlador ressonante ajustado nessa frequência, cai para 2,92%.

TeseAGP p.59 cita um estudo (inversor PV monofásico, refs [56,57]) que reduziu,
via controladores ressonantes, os harmônicos de 3ª/5ª/7ª ordem de
**8,53% / 3,44% / 1,65% → 0,613% / 0,474% / 0,388%**. Padrão implícito na
literatura: acima de ~2-3% já é tratado como problema a mitigar; resultado
"bom" pós-mitigação fica na faixa de 0,4-0,6%.

## 3. Critério funcional de PLL (primeiros princípios, sem limiar fixo)

Yazdani & Iravani não definem um valor fixo — mostram que a magnitude do
distúrbio de 2ω₀ no PLL e do harmônico de 3ª ordem gerado é **proporcional**
à fração de sequência negativa `b` (adimensional, 0 a 1 pu de V̂s), não um
degrau discreto. Ver desenvolvimento completo em
[pll_asymmetric_fault_formal_analysis.md](../pll/pll_asymmetric_fault_formal_analysis.md).

Exemplo extremo (falta linha-terra no próprio PCC, Yazdani Example 12.2):
`a=2/3, b=1/3` → ripple de potência ativa de **até ±50% do valor médio**
(±8 MW em torno de 16 MW) e sobretensão no barramento CC de **1,7-2,6%**.
Ou seja: o "quanto importa" depende inteiramente de quão severo é o
desequilíbrio visto nos terminais do inversor (que depende da localização/tipo
de falta), não de uma tabela de limites.

## Como isso se conecta ao dashboard deste projeto

**Implementado em 2026-07-29** (antes era só descritivo): a tabela de
harmônicas do dashboard agora compara célula a célula com os limites reais
descritos acima, em vez do destaque puramente estético que existia antes
(`_HARM_HI_PU`/`_HARM_LO_PU` só sobrevive como fallback de "valor quase-zero
apagado", sem mais o `harm-top` genérico). Detalhes de implementação
(constantes, classes CSS, JS) em
[espectro-fourier.md](../dashboard/graficos/espectro-fourier.md); domínio
abc vs dq, achado sobre a isenção por segmento e a notação normalizada das
variáveis de corrente (Isc/IL/I_rated — por que TDD não é usado neste
projeto) em
[harmonic_norm_application.md](harmonic_norm_application.md).
