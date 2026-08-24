---
name: tcc-revisao-fragmento-cap5-metricas
description: Definições fechadas e valores medidos das métricas de falta do Cap.5 do fragmento, após a auditoria de 2026-08-23 que reprovou vários números do texto anterior
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
| Erro de fase | `atan2(vq_rede_pu, vd_rede_pu)` em graus, no PAC |
| Pico durante a falta | `max\|erro\|` em `[t_fault + 1 ciclo, t_clear]` |
| Retenção de `v_d` | média em `[t_fault + 2 ciclos, t_clear]` ÷ média em `[t_fault − 50 ms, t_fault)` |
| t_s pós-falta | último instante com `\|erro\| > 2°`, contado a partir de `t_clear` |
| Componente de 120 Hz | FFT com janela de Hann de `vd_rede_pu` em `[t_fault + 2 ciclos, t_clear]` |
| `i_q,ref` de pico | `max\|iq_ufv_ref_pu\|` na janela de falta |
| P durante a falta | média na segunda metade da janela |

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
| Barra 7 (PAC) | 9,2% | 37,3° | 1,000 | 0,00 pu | 98 ms |
| Linha 7-8 | 11,3% | 32,5° | 1,000 | 0,01 pu | 98 ms |
| Linha 8-9 | 47,1% | 29,8° | 1,000 | 0,00 pu | 112 ms |
| Barra 6 | 58,4% | 7,3° | 0,776 | 0,34 pu | 76 ms |

Progressão monotônica confirmada em todas as colunas. O "até 100 ms" do texto
antigo era furado pela Linha 8-9 (112 ms); o texto agora diz 112 ms.

## 5.3 — pares nominal × sintonia inadequada

| Cenário | Pico (>1 ciclo) | t_s pós | 120 Hz em `v_d` |
|---|---|---|---|
| `bus7/2phase` | 180,0° | 51 ms | 0,715 |
| `bus7/2phase_bad_pll` | 180,0° | 99 ms | 0,639 |
| `bus7/1phase` | 89,7° | 46 ms | 0,590 |
| `bus7/1phase_bad_pll` | 72,2° | 98 ms | 0,546 |
| `bus6/2phase` | 96,0° | 48 ms | 0,401 |
| `bus6/2phase_bad_pll` | 34,9° | 78 ms | 0,373 |
| `bus6/1phase` | 12,0° | 39 ms | 0,294 |
| `bus6/1phase_bad_pll` | 13,2° | 47 ms | 0,300 |

Trifásicas na mesma métrica de 120 Hz: 0,0001 a 0,0013 pu. O contraste com as
assimétricas é de **mais de duas ordens de grandeza**.

### Barra 7 bifásica é caso à parte

`v_d` da rede chega a −0,154 pu: o vetor de tensão cruza para o semiplano de
eixo direto negativo e o erro satura em ±180° **nas duas sintonias**. O erro
instantâneo passa de 90° em 17,8% da janela (nominal) e 14,3% (inadequada).

Não é *cycle slipping*: é desalinhamento momentâneo imposto pela sequência
negativa, que desaparece com a eliminação da falta. Manter essa distinção no
texto, por causa da pendência do Cap. 4.

## Números do texto antigo que não se sustentaram

| Afirmação antiga | Medido | Natureza |
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
da sintonia **não** aparece (satura nos dois). Passou a:

| Fig | Arquivo | Papel |
|---|---|---|
| 5.7 | `bus7_2phase_tensao_dq_rede` | caso severo, perda de alinhamento |
| 5.8 | `bus6_2phase_tensao_dq_rede` | nominal |
| 5.9 | `bus6_2phase_bad_pll_tensao_dq_rede` | inadequada (figura nova) |
| 5.10 | `bus6_2phase_bad_pll_potencia_pq` | era a 5.9 |

5.8 e 5.9 são comparação controlada: mesma barra, mesma falta, mesma escala
vertical, variando só a sintonia.

### Escala Y compartilhada (`YLIM_GROUPS`)

`gen_fault_waveforms.py` escalava cada figura pelos próprios dados, o que
falseia leitura lado a lado. Entrou `YLIM_GROUPS`, que torna o ylim a união
dos extremos dq do grupo:

- `sim_localizacao`: `bus7/3phase` + `bus6/3phase` (Figuras 5.4 e 5.5)
- `assim_sintonia`: `bus6/2phase` + `bus6/2phase_bad_pll` (Figuras 5.8 e 5.9)

Mesmo motivo do `YLIM_DQ_REGIME` em `gen_regime_waveforms.py`. O script passou
a aceitar prefixos em `argv` para regenerar só um subconjunto.

## Efeito no texto

A tese do capítulo **não muda**: segue o compromisso entre imunidade durante a
falta e velocidade na recuperação. Muda o alcance: vale em três dos quatro
pares, com o mais brando empatado e o mais severo saturado, em vez de "nos
quatro pares avaliados".
