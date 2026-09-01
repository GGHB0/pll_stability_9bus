# Charts — Gráficos de Dados Reais

Diferente de `assets/diagrams/` (esquemáticos e curvas desenhados à mão em SVG
puro), esta pasta guarda **gráficos gerados a partir dos dados reais de
simulação** (`output/results/*/sim_data*.csv`), sem o layout interativo do
Plotly usado no dashboard — destinados a figuras estáticas do TCC.

Gerados com **matplotlib** (`svg.fonttype: path`, glifos viram contorno
vetorial no SVG — texto não é mais selecionável/editável, mas renderiza
identico em qualquer visualizador; `none` foi tentado antes e quebrava o
espaçamento de rótulos com subscrito, ver seção de convenções abaixo), usando
a paleta de cores do projeto (`src/config/settings.py`, `LIGHT_COLORS`) e as
mesmas convenções de série do dashboard.
`scripts/gen_regime_waveforms.py` gera os dois cenários abaixo de uma vez.

## Cenário `regime` — PLL nominal (regime permanente, sem falta)

| Arquivo | Conteúdo | Janela |
|---|---|---|
| `regime_correntes_abc.svg` / `.png` | Correntes trifásicas do inversor (`i_a, i_b, i_c`) | 0,55–0,60 s (3 ciclos) |
| `regime_tensoes_abc.svg` / `.png` | Tensões trifásicas do inversor (`v_a, v_b, v_c`) | 0,55–0,60 s (3 ciclos) |
| `regime_potencia_pq.svg` / `.png` | Potência ativa e reativa do inversor (`P, Q`) | 0–0,6 s completo |
| `regime_corrente_dq.svg` / `.png` | Corrente dq, medida (sólido) + referência (tracejado) — `i_d, i_q` | 0–0,6 s completo |
| `regime_tensao_dq_rede.svg` / `.png` | Tensão dq do lado da Rede — `v_d, v_q` | 0–0,6 s completo |
| `regime_tensao_dq_inversor.svg` / `.png` | Tensão dq do lado do Inversor — `v_d, v_q` | 0–0,6 s completo |

Marcador de assentamento: `T_settle = 0,1 s` (constante oficial do dashboard,
`src/config/settings.py`, excluída de todo cálculo).

Fonte: `output/results/regime/sim_data.csv` (P, Q, dq) e
`output/results/regime/sim_data_abc.csv` (abc).

## Cenário `regime_bad_pll` — sintonia inadequada (Kp/Ki_pll ×0,2)

| Arquivo | Conteúdo | Janela |
|---|---|---|
| `regime_bad_pll_correntes_abc.svg` / `.png` | Correntes trifásicas do inversor | 0,95–1,00 s (3 ciclos) |
| `regime_bad_pll_tensoes_abc.svg` / `.png` | Tensões trifásicas do inversor | 0,95–1,00 s (3 ciclos) |
| `regime_bad_pll_potencia_pq.svg` / `.png` | Potência ativa e reativa (`P, Q`) | 0–1,0 s completo |
| `regime_bad_pll_corrente_dq.svg` / `.png` | Corrente dq, medida + referência | 0–1,0 s completo |
| `regime_bad_pll_tensao_dq_rede.svg` / `.png` | Tensão dq do lado da Rede | 0–1,0 s completo |
| `regime_bad_pll_tensao_dq_inversor.svg` / `.png` | Tensão dq do lado do Inversor | 0–1,0 s completo |

Com ξ = 0,316 (vs. 0,707 nominal) o transitório de energização é muito mais
lento e oscilatório — visível na P/Q e na corrente/tensão dq oscilando bem
acima do valor final por ~0,5 s antes de convergir. Marcador de assentamento
aqui é **empírico** (`≈ 0,55 s`, última vez que P/Q se afastam >0,08 pu do
valor final), não o `T_SETTLE` global do dashboard — este último foi medido
só para o caso nominal e não vale pra esta sintonia. Motivo do intervalo
completo ir a 1,0 s (não 0,6 s como o nominal): mesma convenção temporal dos
cenários com sintonia inadequada, ver `.claude/kb/simulation/cenarios_simulados.md`.

Fonte: `output/results/regime_bad_pll/sim_data.csv` e `sim_data_abc.csv`.

## Cenários de falta — Barras 6/7 e Linhas 7-8/8-9

Gerados por `scripts/gen_fault_waveforms.py` (script separado do de regime —
fonte de dados e lógica de janela são diferentes, ver docstring do módulo).
Cada cenário em `SCENARIOS` produz o mesmo conjunto de 6 arquivos, prefixo
`<pasta>_<tipo_falta>[_bad_pll]`:

| Arquivo | Conteúdo | Janela |
|---|---|---|
| `<prefixo>_correntes_abc.svg` / `.png` | Correntes trifásicas do inversor | ~2 ciclos antes da falta a 3 ciclos após a eliminação |
| `<prefixo>_tensoes_abc.svg` / `.png` | Tensões trifásicas do inversor | mesma janela |
| `<prefixo>_potencia_pq.svg` / `.png` | Potência ativa e reativa (`P, Q`) | assentamento – fim da simulação |
| `<prefixo>_corrente_dq.svg` / `.png` | Corrente dq, medida + referência | assentamento – fim |
| `<prefixo>_tensao_dq_rede.svg` / `.png` | Tensão dq do lado da Rede | assentamento – fim |
| `<prefixo>_tensao_dq_inversor.svg` / `.png` | Tensão dq do lado do Inversor | assentamento – fim |

`t_fault`/`t_clear` vêm de `fault_info.json` de cada pasta (não hardcoded —
ver `.claude/kb/simulation/cenarios_simulados.md`). Marcador de falta:
sombreado vermelho + vline tracejada vermelha (início) / verde (eliminação),
mesma convenção do dashboard (`src/pipeline/chart.py`, método `_vline`).

Diferente do cenário `regime`, os gráficos de linha do tempo completa (P/Q,
corrente/tensão dq) **cortam** o trecho antes do assentamento em vez de só
sombreá-lo — aqui o fenômeno de interesse é a falta, não o transitório de
partida do PLL. O instante de corte depende do modelo (`bad_pll` no
`fault_info.json`): T$_{settle}$ = 0,1 s (nominal, constante oficial do
dashboard) ou ≈0,55 s empírico (sintonia inadequada, xi=0,316 assenta bem
mais devagar — mesmo valor de `gen_regime_waveforms.py`).

| Prefixo | Barra | Tipo | Modelo | Falta | Fim |
|---|---|---|---|---|---|
| `bus7_3phase` | 7 | trifásica | nominal | 0,3–0,4 s | 0,6 s |
| `bus7_3phase_bad_pll` | 7 | trifásica | sintonia inadequada | 0,6–0,7 s | 1,0 s |
| `bus6_3phase` | 6 | trifásica | nominal | 0,3–0,4 s | 0,6 s |
| `bus6_3phase_bad_pll` | 6 | trifásica | sintonia inadequada | 0,6–0,7 s | 1,0 s |
| `bus7_1phase` | 7 | monofásica | nominal | 0,3–0,4 s | 0,6 s |
| `bus7_1phase_bad_pll` | 7 | monofásica | sintonia inadequada | 0,6–0,7 s | 1,0 s |
| `bus6_2phase` | 6 | bifásica | nominal | 0,3–0,4 s | 0,6 s |
| `bus6_2phase_bad_pll` | 6 | bifásica | sintonia inadequada | 0,6–0,7 s | 1,0 s |
| `line7_8_3phase` | Linha 7-8 | trifásica | nominal | 0,3–0,4 s | 0,6 s |
| `line7_8_3phase_bad_pll` | Linha 7-8 | trifásica | sintonia inadequada | 0,6–0,7 s | 1,0 s |
| `line8_9_3phase` | Linha 8-9 | trifásica | nominal | 0,3–0,4 s | 0,6 s |
| `line8_9_2phase` | Linha 8-9 | bifásica | nominal | 0,3–0,4 s | 0,6 s |

Fonte de cada linha do inventário: `output/results/bus<N>/<tipo>[_bad_pll]/`
ou `output/results/line<X>_<Y>/<tipo>[_bad_pll]/` (`sim_data.csv`,
`sim_data_abc.csv`, `fault_info.json`).

As linhas têm cobertura parcial: `line8_9` não tem variante `_bad_pll`
simulada, e nenhuma das duas linhas tem falta monofásica ainda — só `bus6`/
`bus7` cobrem os três tipos completos hoje. Ver
`.claude/kb/simulation/cenarios_simulados.md` para o levantamento completo
de lacunas.

As faltas monofásica e bifásica são **assimétricas** → sequência negativa →
oscilação visível em ~120 Hz (`2f₁`) em `P`/`Q` e em `v_d`/`v_q` durante a
falta, ausente na trifásica (equilibrada) — mais pronunciada ainda com
sintonia inadequada, que não amortece a oscilação tão bem.

Título com sufixo "(sintonia inadequada)" fica mais longo que os demais —
`set_title()` reduz a fonte automaticamente acima de 62/78 caracteres pra não
cortar na borda da figura.

## Figuras didáticas da retenção

Gerados por `scripts/gen_retencao_didatica.py`. Diferente dos demais, não são
oscilogramas de um cenário: mostram **como a métrica de retenção é construída**
sobre os dados reais, para o texto do TCC não precisar definir a razão só em
prosa. As faixas sombreadas e as linhas de média são anotação sobre o dado, não
alteração dele — os dois valores saem calculados do CSV a cada geração.

| Arquivo | Conteúdo |
|---|---|
| `retencao_construcao.svg` / `.png` | Painel único, `bus7/3phase` (nominal): janela pré-falta, 2 ciclos descartados, janela de medição e a razão fechada |
| `retencao_comparacao.svg` / `.png` | Painel duplo `bus7/3phase` × `bus7/3phase_bad_pll`, para a Seção 5.4 do TCC |

Receita (a mesma de `src/pipeline` e da KB de métricas):

```
retencao = média(v_d) em [t_fault + 2 ciclos, t_clear]
         / média(v_d) em [t_fault − 50 ms, t_fault)
```

Os 2 ciclos descartados (33,3 ms a 60 Hz) removem o transitório de comutação da
aplicação da falta, que domina o trecho inicial e não representa o afundamento.

Duas convenções que **só** valem para o painel duplo, e por isso ficam
documentadas aqui:

- **Eixo X em tempo relativo ao início da falta.** É a única figura da pasta que
  não usa tempo absoluto. Necessário porque `t_fault` difere entre os cenários
  (0,3 s no nominal, 0,6 s na sintonia inadequada) e sem o deslocamento os dois
  painéis não alinham.
- **Eixo Y compartilhado** (`sharey`), mesmo princípio do `YLIM_GROUPS` de
  `gen_fault_waveforms.py`: a diferença das bases pré-falta (0,989 contra
  0,823 pu) é justamente o que a figura precisa deixar visível.

A barra vermelha superior marca a **duração real da falta** (0,1 s), distinta da
janela de medição em laranja, que começa 2 ciclos depois.

## Plano P-Q pós-falta

Gerado por `scripts/gen_plano_pq.py` → `plano_pq_comparacao.svg` / `.png`.
Painel duplo `bus7/3phase` × `bus7/3phase_bad_pll`, mesma família didática da
retenção: mostra sobre o dado real o que a série temporal não mostra.

Em vez de P(t) e Q(t), plota a **trajetória no plano P-Q**. O ponto de operação
pré-falta vira um marcador ("antes") e a média da janela pós-falta vira outro
("depois"). No nominal os dois praticamente coincidem; na sintonia inadequada o
"depois" está **do outro lado da linha P = 0**, ou seja, o inversor passou a
absorver energia. O semiplano `P < 0` fica sombreado em vermelho.

**Métrica destacada: fração do tempo com `P < 0`** (1,1% no nominal contra 64,6%
na sintonia inadequada). Escolhida por ser adimensional e **não depender do
comprimento da janela** — é uma razão, ao contrário dos valores de pico, que
mudam com o recorte. Foi o que substituiu a enumeração de picos no texto, ver
`.claude/kb/tcc-word/revisao_fragmento_cap5_analise.md`.

Janela: `[t_clear + 50 ms, fim]`. Os 50 ms descartados removem o transitório de
comutação da **eliminação** da falta, que no nominal leva P a −3,4 pu por poucos
milissegundos e falsearia a comparação — mesmo racional do descarte de 2 ciclos
na figura da retenção. Eixos compartilhados entre os painéis, porque a diferença
de extensão da órbita é justamente o que a figura precisa mostrar.

## Convenções de série (todos os gráficos)

Corrente dq segue `src/pipeline/chart.py` (`kind="dq_combined"`): medido
sólido + referência tracejada, sobrepostos na mesma figura.

**Padrão de cor/z-order do par medido↔referência** (corrente dq): a curva
"alvo" (referência) usa um tom mais escuro/saturado da mesma cor-base
(`AZUL_REF #1d4ed8` / `VERMELHO_REF #b91c1c` em
`scripts/gen_regime_waveforms.py`), desenhada **primeiro** (zorder menor); a
curva medida é tracejada e desenhada **por cima** (zorder maior), para suas
lacunas revelarem o traço sólido por baixo. Como o medido já tem ondulação
própria visível, usar a mesma família de cor (mais clara) evita que a
sobreposição densa vire uma mancha de alto contraste.

Tensão dq **não** segue mais `kind="vdq_combined"` do dashboard (Rede +
Inversor sobrepostos): as duas séries ficam quase coincidentes o tempo todo
em regime permanente (sem falta, PCC ≈ tensão de rede), e sobrepor exigia
truques de cor/zorder que mesmo assim ficavam difíceis de ler. A pedido do
usuário, viraram **arquivos separados** (`..._tensao_dq_rede` /
`..._tensao_dq_inversor`), cada um com `v_d`/`v_q` em `AZUL`/`VERMELHO`
puro e o mesmo eixo Y nos dois arquivos do par, para comparação lado a lado.

Os dados de `sim_data.csv` vêm a 5 µs (~120 mil pontos em 0,6-1,0 s); P/Q e
corrente/tensão dq são decimados para ~4 000 pontos antes de plotar (mesmo
teto do dashboard, `_MAX_POINTS` em `src/pipeline/chart.py`), por
`decimate_envelope()` — min **e** max de cada bin, não 1 amostra a cada N.
Uma subamostragem ingênua (`iloc[::stride]`) escolhe a mesma fase de
amostragem pra toda coluna; onde a ondulação real é mais rápida que a taxa
decimada (caso do batimento em `v_q`/`v_d` durante a "barriga" de sintonia
inadequada), isso aliasa em zigue-zague artificial em vez do envelope
suave real. Manter min+max por bin preserva a forma verdadeira sem cortar
picos; em trechos suaves degrada pro mesmo efeito de 1 amostra por bin.

## Gerar / regenerar

```powershell
.venv\Scripts\pip install matplotlib   # não está no requirements.txt do pipeline principal
.venv\Scripts\python.exe scripts\gen_regime_waveforms.py   # regime / regime_bad_pll (12 arquivos)
.venv\Scripts\python.exe scripts\gen_fault_waveforms.py    # cenários de falta (6 arquivos por cenário em SCENARIOS)
.venv\Scripts\python.exe scripts\gen_retencao_didatica.py  # figuras didáticas da retenção (4 arquivos)
.venv\Scripts\python.exe scripts\gen_plano_pq.py           # plano P-Q pós-falta (2 arquivos)
```

Reproduzível sempre que os dados de simulação forem atualizados. Novos
cenários de falta entram em `SCENARIOS` no topo de
`scripts/gen_fault_waveforms.py` (72 arquivos hoje — 12 cenários × 6). Ver
inventário completo em `.claude/kb/simulation/cenarios_simulados.md`.
