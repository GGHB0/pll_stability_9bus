---
name: chile-2025-ibr-protections
description: Comportamento real de proteção de PFV/eólicas/hídricas no apagão chileno de 25/fev/2025 — baixa frequência, salto de vetor, sobretensão por efeito Ferranti, conformidade com NTSyCS Art. 3-10
source: Coordinador Eléctrico Nacional (Chile), EAF 089/2025 — Estudio para análisis de falla (18/mar/2025, 399 p.), §7 e §9 (análise de atuação de proteções)
---

# Apagão Chile 2025 — Proteções em Recursos Inversorizados

Achados do relatório técnico completo (EAF-089) que não aparecem no resumo
executivo nem na apresentação ao Congresso — ver contexto geral em
[[chile-2025-overview]]. Foco: como PFV, eólica e hídrica reagiram ao colapso
das duas ilhas elétricas.

## Amostra de proteções acionadas (§9, tabela de eventos)

| Unidade | Potência | Proteção acionada | Avaliação (Art. 3-10 NTSyCS) |
|---|---|---|---|
| PFV El Águila | 1,7 MW | Nenhuma — perda de tensão no PoC | N/A |
| PFV Pampa Camarones | 5,1 MW | Baixa frequência (48 Hz, 100 ms) | **Incorreta** — não cumpre Art. 3-10 |
| PFV Tamaya Solar | 8,4 MW | Baixa tensão (sem abertura de disjuntor) | Sem informação |
| PFV Teno Solar | 5,8 MW | Baixa frequência (47 Hz) | **Correta** |
| TER Trapén | 19,0 MW | Nenhuma — perda de tensão no PoC | N/A |
| HP Alto Renaico | 1,1 MW | **Salto de vetor** | Correta |
| HP Renaico | 5,1 MW | **Salto de vetor** | Correta |
| HP Sauzalito | 8,0 MW | Baixa impedância (distância zona 2) | Presume correta (sem oscilografia) |
| PE Canela | 0,0 MW | Baixa tensão | Correta |
| TER Huasco TG3 | — | Potência inversa (função 32R) | Correta |
| TER Nueva Renca / TER CMPC Pacífico | — | Ajuste de baixa frequência | **Não cumpre** Art. 3-10 |

**Salto de vetor (vector shift)** é a técnica de anti-ilhamento por detecção de
salto abrupto no ângulo de fase da tensão — conceitualmente próxima da detecção
de perda de sincronismo de um PLL (mudança brusca do ângulo estimado). O
relatório confirma sua operação correta em pelo menos duas hidrelétricas durante
o colapso da ilha sul.

## Norma de referência: NTSyCS Art. 3-10

Curva de ride-through de frequência exigida a geradores no Chile — equivalente
funcional ao LVRT/[[lvrt-standards]] (IEEE 1547-2018) já documentado no KB, mas
para frequência. Vários casos no relatório (Pampa Camarones, Nueva Renca, CMPC
Pacífico) tiveram ajuste de proteção **mais permissivo do que a curva exige**,
desconectando cedo demais (48 Hz/100 ms) ou com parametrização não conforme —
padrão de erro comparável ao que o TCC busca capturar com o cenário BAD_PLL
(sintonia inadequada, [[iberia-2025-oscillations]]).

## Física da sobretensão: efeito Ferranti em linha aberta

Após a abertura assimétrica dos disjuntores (um lado abre antes do outro), o
circuito 500 kV permaneceu **energizado a vazio** a partir de Nueva Maitencillo,
gerando sobretensão no extremo oposto (Nueva Pan de Azúcar) — efeito Ferranti
clássico de linha longa sem carga. Proteção de sobretensão de 2º escalão:
limiar 1,17 pu (base 220 kV, 257,4 kV primário), atuação em 100 ms; oscilografia
confirmou picos de até 212 kV fase-terra (260 kV fase-fase RMS). A lógica de
proteção emite ordem de disparo transferido direto (TDD) ao extremo remoto com
atraso de 150 ms. Padrão similar em S/E Lagunas/Encuentro: 2 estágios (115%/60 s
e 120%/1 s), também com TDD.

## Déficit de resposta de EDAC e clientes livres

Na ilha sul, clientes livres entregaram só 62,4% do comprometido em EDAC
(déficit de 343,6 MW, 37,6% do total) — reduzindo os recursos disponíveis para
controle de contingência e contribuindo à propagação até o blackout total.
Em zonas com alta penetração de PMGD, alguns esquemas de corte de carga
regulada tiveram efeito **contrário** ao esperado (redução de geração
distribuída em vez de corte de consumo, −83,5 MW líquidos).

## Lacunas de documentação (relevantes para o TCC)

O relatório **não detalha comportamento de PLL/sincronismo** de nenhum
inversor — apenas resultado binário de proteção (operou/não operou,
correto/incorreto). Vários casos ficaram "sem informação" por falta de
registro oscilográfico ou de Informe de Falla de 5 dias das empresas. Isso é um
argumento a favor da relevância do TCC: **não existe hoje, nem em relatórios
pós-mortem oficiais, um registro sistemático do comportamento interno do PLL**
durante grandes perturbações — só o efeito final (disparo de proteção).

## Uso no TCC

- Salto de vetor como proxy de campo para o que o SRF-PLL simulado deveria
  detectar como perda de sincronismo — comparar tempo de resposta.
- Casos de não conformidade com Art. 3-10 são exemplos reais de proteção mal
  ajustada, paralelos ao cenário BAD_PLL (kp_pll×0,2) do TCC.
- A lacuna de dados de PLL em relatórios reais reforça a contribuição do
  trabalho: simulação EMT detalhada do que os relatórios pós-mortem não captam.
