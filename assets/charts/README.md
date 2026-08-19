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
| `regime_tensao_dq.svg` / `.png` | Tensão dq, Rede (sólido) + Inversor (pontilhado) — `v_d, v_q` | 0–0,6 s completo |

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
| `regime_bad_pll_tensao_dq.svg` / `.png` | Tensão dq, Rede + Inversor | 0–1,0 s completo |

Com ξ = 0,316 (vs. 0,707 nominal) o transitório de energização é muito mais
lento e oscilatório — visível na P/Q e na corrente/tensão dq oscilando bem
acima do valor final por ~0,5 s antes de convergir. Marcador de assentamento
aqui é **empírico** (`≈ 0,55 s`, última vez que P/Q se afastam >0,08 pu do
valor final), não o `T_SETTLE` global do dashboard — este último foi medido
só para o caso nominal e não vale pra esta sintonia. Motivo do intervalo
completo ir a 1,0 s (não 0,6 s como o nominal): mesma convenção temporal dos
cenários com sintonia inadequada, ver `.claude/kb/simulation/cenarios_simulados.md`.

Fonte: `output/results/regime_bad_pll/sim_data.csv` e `sim_data_abc.csv`.

## Convenções de série (todos os gráficos)

Seguem `src/pipeline/chart.py` (`kind="dq_combined"`/`"vdq_combined"`):
corrente dq = medido sólido + referência tracejada; tensão dq = Rede sólido +
Inversor pontilhado (praticamente sobrepostos em regime permanente — não há
falta, PCC ≈ tensão de rede).

**Padrão de cor/z-order do par medido↔alvo** (corrente dq e tensão dq): a
curva "alvo" de cada par (referência em corrente dq; Rede em tensão dq) usa
um tom mais escuro/saturado da mesma cor-base (`AZUL_REF #1d4ed8` /
`VERMELHO_REF #b91c1c` em `scripts/gen_regime_waveforms.py`), desenhada
**primeiro** (zorder menor); a curva secundária (medido/Inversor) é
tracejada/pontilhada e desenhada **por cima** (zorder maior), para suas
lacunas revelarem o traço sólido por baixo.

A cor da curva secundária depende de quanto ela já se distingue por forma:
- **Mesma cor-base, mais clara** (`AZUL`/`VERMELHO`) quando a curva já tem
  ondulação própria visível (corrente dq inteira; `v_q` em tensão dq) — o
  traço/pontilhado sozinho já separa as duas, e usar a mesma família de cor
  evita que a sobreposição densa vire uma mancha de alto contraste.
- **Cinza-ardósia neutro** (`CINZA_MEDIDO #334155`) só onde as curvas ficam
  quase idênticas o tempo todo, sem ondulação própria que as separe (`v_d`
  em tensão dq, que fica colado em ~1,0 pu) — aí duas tonalidades da mesma
  cor não bastam, é preciso um tom de família diferente para o olho pegar o
  traço por cima.

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
.venv\Scripts\python.exe scripts\gen_regime_waveforms.py
```

Reproduzível sempre que os dados de simulação forem atualizados (regera os
10 arquivos dos dois cenários de uma vez).
