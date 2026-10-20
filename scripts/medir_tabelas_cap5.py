"""
Mede os indicadores das Tabelas 5.1, 5.2 e 5.3 do TCC (Cap. 5) a partir de
output/results/ e grava output/tabelas_cap5.csv.

Receita fechada em .claude/kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5_metricas.md
e implementada em src/pipeline/indicadores.py (desde 2026-10-20), a mesma
funcao que o dashboard usa: retencao de v_d como media em [t_fault + 2 ciclos,
t_clear] sobre a media em [t_fault - 50 ms, t_fault); pico apos o 1o ciclo;
retorno a faixa de 2 graus contado de t_clear; 120 Hz pela FFT de
gen_espectro_vd.py; demais medias em [t_fault + 1 ciclo, t_clear].

Rampa ONS (Tabela 5.2): iq = (0,85 - V)/0,35 limitada a 1, com V = |V| do
inversor filtrado (tau = 5 ms), como na entrada do bloco ONS_2_11 (ver
.claude/kb/standards/ride-through/ons_2_11.md). iq_rampa_inst aplica a rampa
instante a instante e tira a media; iq_rampa_Vmed aplica sobre a media de V.
Sinal: corrente reativa injetada sai positiva (o modelo usa iq < 0).

Uso: .venv\\Scripts\\python.exe scripts\\medir_tabelas_cap5.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validar_cenarios import pasta_inadequada  # noqa: E402
from src.pipeline.indicadores import indicadores_falta  # noqa: E402
from src.pipeline.pq import corrige_pq  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "output" / "results"
SAIDA = ROOT.parent / "tabelas_cap5.csv"
COLS = ['t_s', 'P_ufv_pu', 'Q_ufv_pu', 'iq_ufv_ref_pu', 'iq_ufv_pu',
        'vd_ufv_pu', 'vq_ufv_pu', 'vd_rede_pu', 'vq_rede_pu']
CAMPOS = ['ret', 'vdmed', 'vdmin', 'vdmax', 'a120', 'pico', 'ts', 'Vmed',
          'iq_rampa_Vmed', 'iq_rampa_inst', 'iqref', 'iqref_pico', 'iq', 'P', 'Q']


def calc(folder):
    fi = json.load(open(ROOT / folder / 'fault_info.json'))
    d = corrige_pq(pd.read_csv(ROOT / folder / 'sim_data.csv', usecols=COLS), fi)
    s = {c: d[c].to_numpy() for c in COLS[1:]}
    ind = indicadores_falta(d.t_s.to_numpy(), s, fi['t_fault'], fi['t_clear'])
    return dict(caso=folder, bad=fi.get('bad_pll'), **{k: ind[k] for k in CAMPOS},
                data=fi['timestamp'][:10])


def main():
    casos = ['bus7/3phase', 'line7_8/3phase', 'line8_9/3phase', 'bus6/3phase']
    for f in ['bus7/2phase', 'bus7/1phase', 'bus6/2phase', 'bus6/1phase']:
        casos.append(f)
        b = pasta_inadequada(f)
        if b:
            casos.append(b)
    casos += ['bus7/3phase_bad_pll', 'line7_8/3phase_bad_pll', 'bus6/3phase_bad_pll']
    df = pd.DataFrame([calc(c) for c in casos])
    pd.set_option('display.width', 250)
    pd.set_option('display.max_columns', 30)
    print(df.round(4).to_string())
    df.to_csv(SAIDA, index=False)
    print(f'-> {SAIDA}')


if __name__ == '__main__':
    main()
