---
name: stability-classification-classic
description: Classificação CLÁSSICA de estabilidade de sistemas de potência (IEEE/CIGRE Joint Task Force 2004) e seus limites diante de recursos baseados em inversor (IBR)
source: Gu & Green, "Power System Stability With a High Penetration of Inverter-Based Resources", IEEE Proceedings, vol. 111, n.7, jul/2023, DOI 10.1109/JPROC.2022.3179826, §I–II (p.832–835)
---

# Classificação Clássica de Estabilidade — IEEE/CIGRE Joint Task Force (2004)

Base para a seção 2.2 do TCC. Framework amplamente aceito, definido pelo
IEEE/CIGRE Joint Task Force em 2004, que decompõe o problema (intratável em
bloco único) em subproblemas tratáveis. Ver [[stability-classification-extended]]
para a extensão proposta para redes dominadas por IBR.

## Definição formal

> "A capacidade de um sistema elétrico de potência, para uma dada condição
> operativa inicial, retornar a um estado de equilíbrio operacional após
> ser submetido a um distúrbio físico, com a maioria das variáveis do
> sistema limitadas de forma que, na prática, o sistema inteiro permaneça
> íntegro." (IEEE/CIGRE, 2004)

Dois aspectos-chave, relacionados mas com ênfases diferentes conforme o
problema: (1) as variáveis do sistema devem **convergir** a um equilíbrio;
(2) devem permanecer **limitadas** dentro de patamares (thresholds). Ex.:
uma oscilação de frequência pode convergir a longo prazo mas ainda assim
"falhar" no critério de estabilidade se o RoCoF ou o nadir inicial excederem
os limites operativos. Já a estabilidade angular é vista de forma diferente:
a ênfase recai na convergência dentro do primeiro *swing*, independente da
excursão angular inicial.

## As três dimensões de categorização (Fig. 1 do artigo)

1. **Estado dominante** — tensão, ângulo ou frequência. Cada um mapeia um
   aspecto de desempenho: qualidade de energia (tensão), sincronização
   (ângulo), balanço carga-geração (frequência). Dinâmicas EM próximas ou
   acima da frequência síncrona (decaimento de fluxo em indutores,
   ressonância de capacitores shunt/série) são **desprezadas** no
   framework clássico.
2. **Escala de tempo** — curto prazo (segundos) vs. longo prazo (minutos).
3. **Nível de distúrbio** — pequeno sinal (small-signal) vs. grande sinal
   (large-disturbance). Matematicamente, estabilidade a grande sinal
   implica estabilidade a pequeno sinal; a categoria de pequeno sinal existe
   como compromisso prático, pela escassez de técnicas analíticas para
   dinâmicas não-lineares/variantes no tempo de grande sinal.

## Dois mecanismos de desacoplamento que viabilizam a decomposição

1. **Ativa/reativa**: em linhas de transmissão indutivas, potência ativa
   (associada a ângulo e frequência) se desacopla de potência reativa
   (associada a tensão).
2. **Longo prazo/curto prazo**: regulação de frequência primária (segundos
   a dezenas de segundos, via reguladores de velocidade) é muito mais lenta
   que o *swing* angular (10–20 s), permitindo tratar a sincronização
   angular como "instantânea" nos estudos de frequência, e representar o
   conjunto de síncronas pelo centro de inércia (CoI).

## Índices de estabilidade por categoria

| Categoria | Índice | Escopo |
|---|---|---|
| Estabilidade de frequência | **Inércia** | Global (soma de todos os geradores) |
| Ângulo, pequeno sinal | **Coeficientes de sincronização e amortecimento** | Local (gerador) ou global (matriz) — ambos devem ser positivos na frequência de *swing* |
| Ângulo, grande sinal | **Energia crítica** | Global; depende da localização da falta, geralmente estimada |
| Tensão, longo prazo (pequeno sinal) | **∂V/∂Q** | Local ou global |
| Tensão, curto prazo | **Short-Circuit Ratio (SCR)** | Originalmente local, estendido a SCR generalizado |

## GFL vs. GFM — por que o framework clássico precisa ser revisto

Um inversor tem pouca funcionalidade intrínseca da sua forma física — quase
todas as suas características vêm do algoritmo de controle. Duas
abordagens de topo:
- **Grid-Following (GFL)**: sincroniza-se à tensão local da rede (via PLL)
  e injeta um vetor de corrente — formato dominante em inversores comerciais
  hoje. É o objeto de estudo deste TCC.
- **Grid-Forming (GFM)**: controlado como fonte de tensão livre-oscilante,
  com frequência decrescente em proporção à potência drenada (droop) —
  compatível analiticamente com o modelo de gerador síncrono, mas pode se
  comportar de forma muito diferente em curto-circuito (falta de capacidade
  de sobrecorrente). Oferecer resposta a faltas em modo GFM exige
  sobredimensionamento de semicondutores/armazenamento, com custo adicional.

Como o inversor GFL não tem análogo físico direto de máquina síncrona, seu
comportamento desafia a modelagem analítica clássica — motivando a extensão
do framework (ver [[stability-classification-extended]]), que introduz
"generalized angle dynamics", "indirect voltage control", "fast frequency
dynamics" e renomeia "converter-driven stability" para **"EM stability"**:
ressonâncias eletromagnéticas (paralela/série) excitadas por amortecimento
negativo introduzido pelo controle rápido dos inversores nas malhas internas
de corrente (GFL/GFM) e de tensão (GFM) — o mesmo fenômeno de fundo
formalizado no roadmap alemão como *converter-driven stability* em
[[stability-classification-extended]].

## Relevância para o TCC

Este artigo é a ponte formal entre a taxonomia clássica (2.2) e sua extensão
(2.3): mostra que o próprio framework clássico já reconhece a necessidade de
revisão diante de IBRs, e que o inversor GFL — foco deste trabalho — é
precisamente o caso mais desafiador para a modelagem analítica clássica,
por não ter analogia física direta com a máquina síncrona. Ver também
[[srf-pll-theory]] para o mecanismo de sincronização do GFL estudado no TCC.
