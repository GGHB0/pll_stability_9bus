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
`assets/charts/README.md` (seção "Figuras didáticas da retenção"): eixo Y sempre
compartilhado, e eixo X em tempo relativo ao evento quando o instante do evento
difere entre os cenários.

**Anotar não é manipular.** Faixas e linhas de média sobre o traço real não
ferem a regra de `assets/` (*"são os dados reais, nada de manipulações"*), que
proíbe cenário sintético ou série truncada, não anotação.
