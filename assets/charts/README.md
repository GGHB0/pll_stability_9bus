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

## Cenário `bus7_3phase` — falta trifásica na Barra 7

Gerado por `scripts/gen_fault_waveforms.py` (script separado do de regime —
fonte de dados e lógica de janela são diferentes, ver docstring do módulo).

| Arquivo | Conteúdo | Janela |
|---|---|---|
| `bus7_3phase_correntes_abc.svg` / `.png` | Correntes trifásicas do inversor | ~0,267–0,45 s (2 ciclos antes da falta a 3 ciclos após a eliminação) |
| `bus7_3phase_tensoes_abc.svg` / `.png` | Tensões trifásicas do inversor | mesma janela |
| `bus7_3phase_potencia_pq.svg` / `.png` | Potência ativa e reativa (`P, Q`) | T$_{settle}$ (0,1 s) – 0,6 s |
| `bus7_3phase_corrente_dq.svg` / `.png` | Corrente dq, medida + referência | T$_{settle}$ – 0,6 s |
| `bus7_3phase_tensao_dq_rede.svg` / `.png` | Tensão dq do lado da Rede | T$_{settle}$ – 0,6 s |
| `bus7_3phase_tensao_dq_inversor.svg` / `.png` | Tensão dq do lado do Inversor | T$_{settle}$ – 0,6 s |

Falta aplicada em `t = 0,3 s`, eliminada em `t = 0,4 s` (lido de
`fault_info.json`, não hardcoded — ver
`.claude/kb/simulation/cenarios_simulados.md`). Marcador de falta: sombreado
vermelho + vline tracejada vermelha (início) / verde (eliminação), mesma
convenção do dashboard (`src/pipeline/chart.py`, método `_vline`).

Diferente do cenário `regime`, os gráficos de linha do tempo completa (P/Q,
corrente/tensão dq) **cortam** o trecho antes de T$_{settle}$ em vez de só
sombreá-lo — aqui o fenômeno de interesse é a falta (que já ocorre depois de
T$_{settle}$), não o transitório de partida do PLL.

Fonte: `output/results/bus7/3phase/sim_data.csv`, `sim_data_abc.csv` e
`fault_info.json`.

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
```

Reproduzível sempre que os dados de simulação forem atualizados. Novos
cenários de falta entram em `SCENARIOS` no topo de
`scripts/gen_fault_waveforms.py` (ver inventário completo em
`.claude/kb/simulation/cenarios_simulados.md`).
