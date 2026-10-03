"""
Mede os indicadores das Tabelas 5.1, 5.2 e 5.3 do TCC (Cap. 5) a partir de
output/results/ e grava output/tabelas_cap5.csv.

Receita fechada em .claude/kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5_metricas.md:
pico e t_s pela funcao metrics() de gen_erro_fase.py; retencao de v_d como
media em [t_fault + 2 ciclos, t_clear] sobre a media em [t_fault - 50 ms,
t_fault); 120 Hz pela mesma FFT de gen_espectro_vd.py; demais medias em
[t_fault + 1 ciclo, t_clear].

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

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gen_erro_fase import metrics  # noqa: E402
from validar_cenarios import pasta_inadequada  # noqa: E402
from src.pipeline.spectrum import _amplitude_spectrum  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "output" / "results"
SAIDA = ROOT.parent / "tabelas_cap5.csv"
C = 1 / 60
TAU_V = 0.005
COLS = ['t_s', 'P_ufv_pu', 'Q_ufv_pu', 'id_ufv_pu', 'iq_ufv_ref_pu', 'iq_ufv_pu',
        'vd_ufv_pu', 'vq_ufv_pu', 'vd_rede_pu', 'vq_rede_pu']


def rampa(v):
    return np.clip((0.85 - v) / 0.35, 0, 1) * (v < 0.85)


def filtra(t, x, tau):
    dt = np.diff(t, prepend=t[0])
    y = np.empty_like(x)
    y[0] = x[0]
    for k in range(1, len(x)):
        al = dt[k] / (tau + dt[k])
        y[k] = y[k - 1] + al * (x[k] - y[k - 1])
    return y


def calc(folder):
    fi = json.load(open(ROOT / folder / 'fault_info.json'))
    d = pd.read_csv(ROOT / folder / 'sim_data.csv', usecols=COLS)
    t = d.t_s.to_numpy()
    tf, tc = fi['t_fault'], fi['t_clear']
    e = np.degrees(np.arctan2(d.vq_rede_pu.to_numpy(), d.vd_rede_pu.to_numpy()))
    pico, ts = metrics(fi, t, e)
    pre = (t >= tf - 0.05) & (t < tf)
    w2 = (t >= tf + 2 * C) & (t <= tc)
    w1 = (t >= tf + C) & (t <= tc)
    vd = d.vd_rede_pu.to_numpy()
    f, a, _ = _amplitude_spectrum(t[w2], vd[w2], window='hann')
    V = np.hypot(d.vd_ufv_pu.to_numpy(), d.vq_ufv_pu.to_numpy())
    Vf = filtra(t, V, TAU_V)
    iq_ref = d.iq_ufv_ref_pu.to_numpy()
    return dict(
        caso=folder, bad=fi.get('bad_pll'),
        ret=vd[w2].mean() / vd[pre].mean() * 100,
        vdmed=vd[w1].mean(), vdmin=vd[w1].min(), vdmax=vd[w1].max(),
        a120=float(a[np.argmin(np.abs(f - 120))]), pico=pico, ts=ts,
        Vmed=V[w1].mean(), iq_rampa_Vmed=float(rampa(V[w1].mean())),
        iq_rampa_inst=float(rampa(Vf[w1]).mean()),
        iqref=-iq_ref[w1].mean(), iqref_pico=np.abs(iq_ref[w1]).max(),
        iq=-d.iq_ufv_pu.to_numpy()[w1].mean(),
        P=d.P_ufv_pu.to_numpy()[w1].mean(), Q=d.Q_ufv_pu.to_numpy()[w1].mean(),
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
