# Figuras Orientadas a Dado

Os três casos em que a figura **não** é SVG escrito à mão, porque o conteúdo
vem do repositório e muda a cada re-simulação. Referenciado por `SKILL.md`.

Para diagrama conceitual estável (circuito, laço de controle), nada disto se
aplica: continua sendo SVG escrito à mão, ver `SKILL.md`.

## 1. Gráficos de Dados Reais (não desenhados à mão)

Para gráfico plotando **dados reais de simulação** (correntes/tensões abc,
dq, P/Q, séries temporais de `output/results/*/sim_data*.csv`) — não desenhar
o SVG à mão. Usar **matplotlib** direto do CSV (`svg.fonttype: "path"`, que
converte os glifos em contorno vetorial; `"none"` mantém o texto editável mas
quebra o espaçamento de rótulos com subscrito — já foi tentado e revertido,
ver `assets/charts/README.md`), com a paleta de `src/config/settings.py`
(`LIGHT_COLORS`) e as convenções de série do dashboard (`src/pipeline/chart.py`:
medido sólido + ref tracejado; Rede sólido + Inversor pontilhado). `savefig`
gera SVG **e** PNG direto — dispensa o workflow de rasterização via browser
do `SKILL.md`, que é só para SVG desenhado à mão.

Destino: `assets/charts/` (não `assets/diagrams/`), um SVG por gráfico
(não empacotar vários painéis numa figura só, a menos que pedido). Script
gerador versionado em `scripts/gen_<nome>.py`, reproduzível a cada
re-simulação. Ver `assets/charts/README.md` e `scripts/gen_regime_waveforms.py`
como referência de estilo (legenda com fundo branco fora das curvas,
`T_SETTLE` sombreado, título com `pad` quando a legenda fica acima do eixo).

## 2. Figura Desenhada à Mão, Conteúdo Lido do Disco

Caso intermediário: o **layout** é desenhado (uma matriz, um quadro-síntese,
um inventário), mas o **conteúdo** vem do repositório e muda a cada
re-simulação. Aí não se escreve o SVG à mão nem se usa matplotlib: escreve-se
um gerador que lê a fonte e emite o SVG.

Referência: `scripts/gen_matriz_cenarios.py`, que varre `output/results/` e
gera `assets/diagrams/matriz_cenarios.svg` (a Figura 4.4 do TCC). Ganho real:
a figura não pode divergir do que foi simulado, e a contagem impressa no
rodapé é contada, não digitada — foi assim que se descobriu que a KB dizia 32
cenários onde havia 30.

Vale a pena quando o conteúdo é volátil ou quando errar o número tem custo.

## 3. Gráfico Didático de Métrica

O gráfico plota dado real, mas o objetivo não é mostrar o fenômeno e sim
**mostrar de onde sai um número** que o texto cita fechado. Surgiu quando o
usuário perguntou como a retenção de 8,2%/9,2% era calculada: *"apenas lendo o
texto não consigo identificar"*.

Referência: `scripts/gen_retencao_didatica.py`, que gera
`assets/charts/retencao_construcao` e `retencao_comparacao`.

Receita do desenho:

- Sombrear **cada janela** que entra na conta, com uma cor por papel (verde
  para a referência/base, laranja para a medição, cinza para o trecho
  descartado) e legenda única identificando as faixas.
- Traçar uma linha tracejada horizontal sobre cada janela, na altura da
  estatística que ela produz, anotada com o valor.
- Fechar a conta dentro da própria figura, em caixa (`retenção = 0,091 / 0,989
  = 9,2 %`). O leitor não precisa sair da figura para completar o raciocínio.
- **Os números saem calculados do CSV na hora**, nunca digitados no script —
  senão a figura e o texto divergem na próxima re-simulação.
- Distinguir visualmente o **evento** da **janela de medição** quando não
  coincidem. No primeiro rascunho o rótulo "falta" ficava sobre a faixa da
  janela de medição, que começa 2 ciclos depois, e sugeria que a falta começava
  ali. Virou uma barra própria marcando a duração real do evento.

Para comparar dois cenários lado a lado, ver as regras de eixo compartilhado em
`assets/charts/figuras_didaticas.md` (seção "Figuras didáticas da retenção"): eixo Y sempre
compartilhado, e eixo X em tempo relativo ao evento quando o instante do evento
difere entre os cenários.

### Validar a legibilidade no tamanho da página, sempre

Toda figura didática acumula rótulo, caixa e anotação — e é exatamente esse
texto que morre quando a figura encolhe para a largura útil do DOCX. **O PNG em
tamanho natural nunca revela o problema.**

Fonte efetiva = `font_pt × largura_na_pagina / largura_figsize`. Largura útil do
fragmento: 6,5 in. O padrão do Cap. 5 é escala ~0,79 (~7,9 pt efetivos).

Procedimento, antes de dar a figura por pronta:

1. Conferir a largura útil no próprio DOCX
   (`section.page_width − left_margin − right_margin`).
2. Escolher `figsize` para que `largura_na_pagina / figsize ≈ 0,79`.
   **Encolher o `figsize`, nunca subir a fonte** — subir fonte deixa o PNG
   isolado desproporcional e não muda a razão texto/figura na página.
3. Garantir que nenhuma anotação seja menor que a fonte-base (`font.size`).
4. Reescalar o PNG para `6,5 in × 150 dpi = 975 px` e olhar **ao lado de uma
   linha em 12 pt**, que é o corpo do TCC.

Em 2026-09-01 as duas figuras novas nasceram com `figsize` 10,2 e 10,4 in: a
6,5 in na página davam escala 0,64, com anotações de 8,8 pt caindo para 6,9 pt.
Corrigidas para 8,3 in com anotações em 9,5 pt. Foi o usuário que levantou
("vale validar se o texto pode estar ficando ruim de enxergar"), não a
conferência visual do PNG.

### Variante: anotar um oscilograma que já existe

Quando o gráfico já está no documento e o problema é que o texto ao lado
precisa enumerar valores para explicá-lo, não faça gráfico novo: **anote o que
já existe**. `scripts/gen_potencia_didatica.py` (2026-09-01) sobrepõe quatro
camadas ao traço bruto — área preenchida, patamar de referência, média
resultante e fração do tempo em caixa.

Regras que essa variante acrescenta:

- **Preencher os dois lados de uma fronteira, não só o lado "ruim".** A primeira
  versão sombreava só `P < 0` ("absorve"): dizia metade da história e deixava o
  "entrega" implícito. Regra geral: se o **sinal** de uma grandeza é o resultado,
  mostre os dois sinais.
- **Mas preencher com cor NEUTRA, não com verde/vermelho.** Foi a correção
  seguinte do usuário: *"não precisa sombrear nem vermelho e nem verde, pois dá
  indício que um tem efeito positivo e o outro negativo; a ideia é justamente
  mostrar que está entregando e absorvendo de forma desordenada"*. O par
  verde/vermelho é lido como bom/mau, e aqui os dois sentidos são igualmente
  sintomáticos — os picos positivos pós-falta não são "o inversor funcionando",
  são a mesma oscilação descontrolada. Usar **a cor do próprio traço** em alpha
  baixo, dos dois lados, e deixar a separação por conta da **linha do zero
  reforçada** mais rótulos de direção neutros (`▲ entrega` / `▼ absorve`) fora
  da borda do eixo.
  - Vale para as linhas de referência também: "antes" e "depois" passaram de
    verde/vermelho para NAVY nos dois, diferenciadas por **padrão de traço**
    (tracejado longo × pontilhado) e pelo próprio rótulo.
  - **Exceção mantida:** os marcadores de evento (`falta aplicada` vermelho /
    `falta eliminada` verde) continuam coloridos — são convenção de todo o
    capítulo (`gen_fault_waveforms.py`) e marcam *instantes*, não valores, então
    não carregam juízo sobre a grandeza.
- **Dar as duas frações**, não só a que interessa ao argumento (entrega 36,2% ·
  absorve 63,8%). Somam 100% e o leitor confere sozinho.
- **Contraste temporal dispensa painel de comparação.** Como o "antes" e o
  "depois" estão na mesma série, uma figura só basta: não precisa do painel do
  cenário sadio ao lado.
- **Substituir ou acrescentar é decisão do autor, não da técnica.** A intuição
  era substituir o oscilograma cru (custo zero de renumeração). O usuário pediu
  o contrário: *"sem retirar o que já temos, porém complementando"*. Funcionou
  porque **as duas escalas dizem coisas diferentes** — a crua mantém o recorte
  cheio e mostra o transitório do evento; a anotada fecha a escala e por isso
  consegue expor o fenômeno, que na crua fica comprimido contra o eixo. Se as
  duas tivessem a mesma escala, seriam a mesma figura duas vezes e aí substituir
  seria o certo. Antes de propor a troca, olhar se o recorte mudou.
- **Caixa de anotação nunca em cima do traço.** Reservar folga no `ylim`
  (assimétrica, se preciso) e ancorar a caixa nela, em vez de deixá-la cobrir
  dados com fundo branco.

### Variante: trocar o eixo do tempo por um plano de estado

> Técnica válida, mas **rejeitada no TCC em 2026-09-01**: *"não quero o plano
> P-Q, vai ser um tipo de análise nova que não precisamos"*. O custo não é
> desenhar, é obrigar a banca a aprender um gráfico novo no meio do capítulo.
> Só proponha quando a série temporal realmente não der conta — se um
> oscilograma anotado entrega a mesma conclusão, ele ganha.

Quando o que se quer mostrar é **mudança de regime**, e não a construção de uma
conta, às vezes a série temporal é o gráfico errado. `scripts/gen_plano_pq.py`
(2026-09-01) abandona o eixo do tempo e plota a trajetória no **plano P-Q**: o
ponto de operação pré-falta vira um marcador ("antes"), a média da janela
pós-falta vira outro ("depois"), e o semiplano `P < 0` fica sombreado. No caso
sadio os dois marcadores coincidem; no caso com perda de sincronismo o "depois"
está do outro lado da linha de potência nula. Nenhuma série temporal comunica
isso tão rápido.

Regras que essa variante acrescenta:

- **Par "antes / depois" em vez de valores de pico.** Dois marcadores fazem o
  trabalho que dez números em prosa faziam mal.
- **Sombrear a região que carrega o significado** (aqui, `P < 0` = o inversor
  absorve), com uma linha forte na fronteira. É a fronteira que conta a
  história, não os extremos.
- **Preferir métrica adimensional que não dependa da janela.** A caixa da
  figura mostra *fração do tempo* com `P < 0` (1,1% × 64,6%), não valores de
  pico — razão sobrevive a mudança de recorte, pico não. Ver
  [[tcc-revisao-fragmento-cap5-analise]] para por que isso importa no TCC.
- **Descartar o transitório do evento também aqui.** A janela começa 50 ms após
  a eliminação da falta; sem isso o pico de comutação (P a −3,4 pu no nominal)
  domina a escala e falseia a comparação. Mesmo racional dos 2 ciclos da
  retenção.

**Anotar não é manipular.** Faixas e linhas de média sobre o traço real não
ferem a regra de `assets/` (*"são os dados reais, nada de manipulações"*), que
proíbe cenário sintético ou série truncada, não anotação.
