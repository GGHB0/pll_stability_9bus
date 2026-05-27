---
name: reuniao-2026-05-inercia-pll
description: Texto de apoio para reuniao sobre novos testes de inercia, reatancia de curto, colapso do PLL e tentativas de filtragem notch
source: Testes Simulink do projeto, semana de 2026-05
---

# Texto de Apoio para Reuniao - Inercia, Curto e PLL

Nesta semana nos concentramos em entender por que o sistema colapsa em alguns casos
mesmo depois da eliminacao da contingencia. O foco dos testes foi a inercia das
maquinas sincronas dos geradores G1 e G3, porque elas definem quanto o sistema
consegue resistir a uma aceleracao angular brusca durante e logo apos o curto.

Fizemos uma varredura com diferentes valores de segundos de inercia nas maquinas e
tambem variamos a reatancia do curto-circuito. A reatancia foi testada entre 2% e
20% do valor base de 529 ohms, o que corresponde aproximadamente a uma faixa de
10,58 ohms ate 105,8 ohms. A ideia foi observar como a severidade eletrica da falta
interage com a inercia mecanica disponivel no sistema.

O principal achado foi que, para o modelo atual, qualquer valor acima de
aproximadamente 0,1 segundos de inercia nas maquinas testadas fez com que o sistema
nao entrasse em colapso total. Isso nao deve ser apresentado como uma regra geral
para qualquer sistema eletrico, mas como um limite empirico observado dentro da
parametrizacao atual do IEEE 9 barras, do inversor, do PLL e dos curtos simulados.

Quando a inercia fica muito baixa, o problema aparece principalmente na recuperacao
pos-contingencia. Durante o curto, os rotores aceleram e o angulo eletrico se desloca
muito rapidamente. Quando a falta e eliminada, a rede tenta voltar a uma condicao
normal, mas o PLL ja esta em uma regiao ruim de operacao. Ele tenta reencontrar a
fase correta, mas entra em um comportamento repetitivo de erro, com caracteristica
de loop no erro derivativo, e deixa de cumprir sua funcao de referencia angular.

Esse ponto e importante porque o colapso nao e simplesmente uma queda de tensao. O
que observamos e que a referencia usada pelo controle do inversor se perde. Depois
disso, as componentes `Id` e `Iq` deixam de seguir uma trajetoria coerente. Como
elas dependem diretamente do angulo estimado pelo PLL, qualquer erro grande em
`theta_hat` faz o controle dq interpretar as correntes em eixos errados. Em colapsos
muito grandes, com pouca inercia proxima, `Id` e `Iq` se desorganizam e a injecao de
potencia deixa de representar uma acao controlada.

Tambem investigamos filtros notch para os casos de curto assimetrico. A motivacao
foi a presenca de componentes de 120 Hz, que aparecem no referencial dq quando existe
sequencia negativa. A tentativa foi ajustar ou introduzir um novo filtro para impedir
que essas variaveis de 120 Hz atrapalhassem a leitura do PLL e contaminassem as
correntes `Id` e `Iq`.

As tentativas de filtragem nao foram bem sucedidas nos casos de colapso mais severo.
Isso mostra uma diferenca importante: o notch pode ser uma ferramenta valida para
reduzir ripple de 120 Hz em curtos assimetricos moderados, mas ele nao resolve a
perda de sincronismo causada por baixa inercia e alta variacao angular pos-falta.
Nesses casos, a limitacao dominante nao e apenas a segunda harmonica; e o fato de o
PLL sair da sua regiao de captura.

Para a apresentacao, a conclusao mais forte e que o projeto esta revelando uma
fronteira de estabilidade do inversor grid-following. Com inercia suficiente, o PLL
consegue atravessar a contingencia e recuperar a referencia. Com inercia muito baixa,
principalmente abaixo do limiar observado de 0,1 s no modelo atual, a recuperacao da
rede nao garante a recuperacao do controle, porque o PLL pode permanecer perdido e
levar `Id`, `Iq` e a injecao de potencia a um estado incoerente.

Como proximos passos tecnicos, o Capitulo 4 deve organizar esses resultados em
tres blocos: primeiro, a varredura de inercia e reatancia de curto; segundo, a
analise do mecanismo de colapso do PLL e das correntes dq; terceiro, a discussao
das tentativas de notch, explicando por que elas ajudam no problema de 120 Hz mas
nao resolvem o colapso estrutural por baixa inercia.
