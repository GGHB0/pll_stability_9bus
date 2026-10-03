---
name: tcc-revisao-fragmento-cap5-metricas
aliases: [tcc-revisao-fragmento-cap5-metricas]
description: Definições fechadas e valores medidos das métricas de falta do Cap.5 (auditoria de 2026-08-23, valores atualizados em 2026-10-03 com as Tabelas 5.1-5.3)
metadata:
  type: project
---

# Cap. 5 do Fragmento — Métricas de Falta Auditadas (2026-08-23)

Auditoria pedida pelo usuário: *"verifique as análises de falta, verifique se
está utilizando os dados reais ou algum que você tentou corrigir"*.
Complementa [[tcc-revisao-fragmento-cap5]].

## Veredito

As **figuras** sempre foram dado real: as imagens do fragmento batem por MD5
com `assets/charts/`, e `scripts/gen_fault_waveforms.py` lê os CSVs de
`output/results/` sem truncar nada (só recorta o eixo x a partir do
assentamento). O que não sobreviveu à conferência foram **números do texto**,
herdados de uma sessão anterior que os registrou no KB sem a receita de
cálculo.

## Definições fechadas

Toda métrica do Cap. 5 passa a usar estas definições. A ausência delas foi a
causa direta da divergência: sem receita, o número não é reprodutível.

| Métrica | Definição |
|---|---|
| Erro de fase | `atan2(vq_rede_pu, vd_rede_pu)` em graus, no PCC |
| Pico durante a falta | `max\|erro\|` em `[t_fault + 1 ciclo, t_clear]` |
| Retenção de `v_d` | média em `[t_fault + 2 ciclos, t_clear]` ÷ média em `[t_fault − 50 ms, t_fault)` |
| t_s pós-falta | último instante com `\|erro\| > 2°`, contado a partir de `t_clear` |
| Componente de 120 Hz | FFT com janela de Hann de `vd_rede_pu` em `[t_fault + 2 ciclos, t_clear]`; na prática **3 ciclos** (df = 20 Hz), ver abaixo |
| `i_q,ref` de pico | `max\|iq_ufv_ref_pu\|` na janela de falta |
| P durante a falta | média na segunda metade da janela |
| `v_d` médio, mín. e máx. | `vd_rede_pu` em `[t_fault + 1 ciclo, t_clear]` (Tabela 5.3) |
| Rampa ONS × `i_q,ref` | rampa `(0,85 − V)/0,35` limitada a 1, com V = \|V\| do inversor filtrado (τ = 5 ms), média em `[t_fault + 1 ciclo, t_clear]`, contra a média de `−iq_ufv_ref_pu` (Tabela 5.2; ver [[ons-2-11]]) |

**Script:** `scripts/medir_tabelas_cap5.py` aplica todas as definições e grava
`output/tabelas_cap5.csv`; reproduz as Tabelas 5.1-5.3 do TCC (conferido em
2026-10-03, diferença zero). Número novo do Cap. 5 sai dele, não de conta solta.

**Janela do 120 Hz:** `[t_fault + 2 ciclos, t_clear]` tem ~67 ms, mas o 1º
instante cai uma amostra depois de `t_fault + 2 ciclos`, então
`_amplitude_spectrum` trunca para **3 ciclos inteiros**: df = 20 Hz, 120 Hz
cai num bin exato, e os bins abaixo de 60 Hz são a variação lenta de `v_d`
durante a falta, não harmônica (explicado em `gen_espectro_vd.py`).

**Por que descartar o primeiro ciclo:** o transitório de comutação da
aplicação domina o pico. Em `bus6/3phase` o máximo por ciclo cai
40,1° → 7,3° → 5,7° → 4,3° → 2,7° → 1,1°. Incluir o primeiro ciclo mede o
chaveamento, não o rastreamento. É a mesma armadilha do pico de energização
já registrada em [[tcc-revisao-fragmento-cap5]].

Nas assimétricas o comportamento é oposto: o erro **cresce** ao longo da
janela (`bus6/2phase` vai de 15,8° no 1º ciclo a 96,0° no 6º), então o pico
cai no fim e o recorte inicial pouco importa.

## 5.2 — gradiente de localização (trifásica, sintonia nominal)

| Local | Retenção `v_d` | Pico (>1 ciclo) | `i_q,ref` | P durante | t_s pós |
|---|---|---|---|---|---|
| Barra 7 (PCC) | 9,2% | 37,3° | 1,000 | 0,00 pu | 98 ms |
| Linha 7-8 | 11,3% | 32,5° | 1,000 | 0,01 pu | 98 ms |
| Linha 8-9 | 47,1% | 29,8° | 1,000 | 0,00 pu | 112 ms |
| Barra 6 | 58,4% | 7,3° | 0,776 | 0,34 pu | 76 ms |

Progressão monotônica confirmada em todas as colunas. O "até 100 ms" do texto
antigo era furado pela Linha 8-9 (112 ms); o texto agora diz 112 ms.

## 5.3 — pares nominal × sintonia inadequada

Valores de 2026-10-03 (Tabela 5.3 do TCC). A sintonia inadequada foi
re-simulada em 01/10 com a janela de falta do nominal; os números de 08-23
(t_s 99 / 78 / 47 ms) eram da safra antiga, com falta em 0,6-0,7 s.
`bus7/1phase_bad_pll` não existe na safra nova (sai da tabela).

| Cenário | Pico (>1 ciclo) | t_s pós | 120 Hz em `v_d` |
|---|---|---|---|
| `bus7/2phase` | 180,0° | 51 ms | 0,719 |
| `bus7/2phase_bad_pll` | 179,9° | 96 ms | 0,636 |
| `bus7/1phase` | 89,7° | 46 ms | 0,591 |
| `bus6/2phase` | 96,0° | 48 ms | 0,394 |
| `bus6/2phase_bad_pll` | 34,5° | 30 ms | 0,375 |
| `bus6/1phase` | 12,0° | 39 ms | 0,294 |
| `bus6/1phase_ground_bad_pll` | 12,8° | 31 ms | 0,300 |

Trifásicas nominais na mesma métrica de 120 Hz: 0,0002 a 0,0011 pu. O contraste com as
assimétricas é de **mais de duas ordens de grandeza**.

### Barra 7 bifásica é caso à parte

`v_d` da rede chega a −0,154 pu: o vetor de tensão cruza para o semiplano de
eixo direto negativo e o erro satura em ±180° **nas duas sintonias**. O erro
instantâneo passa de 90° em 17,8% da janela (nominal) e 14,3% (inadequada).

Não é *cycle slipping*: é desalinhamento momentâneo imposto pela sequência
negativa, que desaparece com a eliminação da falta. Manter essa distinção no
texto, por causa da pendência do Cap. 4.

## Números do texto antigo que não se sustentaram

| Afirmação antiga | Medido (08-23) | Natureza |
|---|---|---|
| Picos 5.2: 53,9 / 44,3 / 23,5 / 21,0° | 37,3 / 32,5 / 29,8 / 7,3° | receita desconhecida |
| `bus7/2phase`: 40,1° → 34,2° | 180° → 180° (satura) | contradiz a figura ao lado |
| `bus6/1phase`: 15,0° → 9,2° | 12,0° → 13,2° | **sentido invertido** |
| t_s inadequado: 187 / 103 / 95 ms | 99 / 78 / 47 ms | ~2× altos |
| `bus7/1phase` nominal: ~190 ms | 46 ms | ~4× alto |
| 120 Hz trifásicas: 0,008–0,014 pu | 0,0001–0,0013 pu | ~20× alto |
| `i_q,ref` 0,97 / 0,67 pu | 1,000 / 0,776 pu | arredondamento errado |
| "erro estático 0,81° → 1,48°" | rms 0,442° → 0,444° | **não há diferença** |

Varredura de ~1680 combinações (15 pastas × 2 lados × 8 recortes × 7
estatísticas): nenhuma combinação coerente reproduz o conjunto antigo nas
pastas certas. Os poucos acertos numéricos caem em pastas erradas, ou seja,
são coincidência. O valor 15,0° existe, mas na pasta `_bad_pll`, e 9,1°
existe na nominal — pares trocados de lado.

**Conferem e ficaram como estavam:** ondulação de Q 4,8 → 11,7 pu na Barra 6
bifásica, e a faixa de 0,29 a 0,71 pu das assimétricas.

## Reorganização das figuras de 5.3

Antes, as Figuras 5.7 e 5.8 eram o par `bus7/2phase`, justamente onde o efeito
da sintonia **não** aparece (satura nos dois). Passou a (coluna "Fig" com a
numeração de 08-23; "Hoje" após as inserções até 2026-10-03):

| Fig | Hoje | Arquivo | Papel |
|---|---|---|---|
| 5.7 | 5.11 | `bus7_2phase_tensao_dq_rede` | caso severo, perda de alinhamento |
| 5.8 | 5.12 | `bus6_2phase_tensao_dq_rede` | nominal |
| 5.9 | 5.13 | `bus6_2phase_bad_pll_tensao_dq_rede` | inadequada (figura nova) |
| 5.10 | 5.15 | `bus6_2phase_bad_pll_potencia_pq` | era a 5.9 |

As Figuras 5.12 e 5.13 (numeração atual) são comparação controlada: mesma barra, mesma falta, mesma escala
vertical, variando só a sintonia.

### Escala Y compartilhada (`YLIM_GROUPS`)

`gen_fault_waveforms.py` escalava cada figura pelos próprios dados, o que
falseia leitura lado a lado. Entrou `YLIM_GROUPS`, que torna o ylim a união
dos extremos dq do grupo:

- `sim_localizacao`: `bus7/3phase` + `bus6/3phase` + `bus7/3phase_bad_pll`
  (hoje Figuras 5.5, 5.6 e 5.17)
- `assim_sintonia`: `bus6/2phase` + `bus6/2phase_bad_pll` (hoje 5.12 e 5.13)

Mesmo motivo do `YLIM_DQ_REGIME` em `gen_regime_waveforms.py`. O script passou
a aceitar prefixos em `argv` para regenerar só um subconjunto.

## 5.4 — perda de sincronismo (`bus7/3phase_bad_pll`)

Movido para [[tcc-revisao-fragmento-cap5-metricas-54]] em 2026-08-25 (limite de
200 linhas): métricas próprias da seção, tabela de retenção com os valores
brutos de numerador/denominador, argumento 2×2, ressalvas e escala Y. As
definições fechadas acima continuam valendo lá.

## Efeito no texto

A tese do capítulo **não muda**: segue o compromisso entre imunidade durante a
falta e velocidade na recuperação. Muda o alcance: vale em três dos quatro
pares, com o mais brando empatado e o mais severo saturado, em vez de "nos
quatro pares avaliados".
