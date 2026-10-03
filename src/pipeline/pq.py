"""
pq.py — Correção de escala de P e Q do UFV nas rodadas antigas.

Até 03/10/2026 o subsistema "Inverter Active & Reactive Power" do .slx usava
ganho 1/sqrt(3) nos dois cálculos, com Vabc e Iabc em pu de pico:
    P_modelo = (1/sqrt(3)) * sum(v*i)        ->  P_pu = (2/3) * sum(v*i)
    Q_modelo = (1/sqrt(3)) * sum(i*v_ff)     ->  Q_pu = (2/(3*sqrt(3))) * sum(i*v_ff)
Ou seja, P saía multiplicada por sqrt(3)/2 e Q por 3/2. O .slx foi corrigido;
as rodadas novas gravam os ganhos no fault_info.json (pq_ganho_p/pq_ganho_q)
e não são reescaladas. Detalhe: .claude/kb/simulation/export_workflow.md.
"""

from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd

GANHO_ANTIGO = "1/sqrt(3)"
FATOR_P = 2 / np.sqrt(3)
FATOR_Q = 2 / 3


def escala_legada(info: dict) -> bool:
    """True se a rodada saiu do .slx com o ganho antigo (sem campo = antiga)."""
    return info.get("pq_ganho_p", GANHO_ANTIGO) == GANHO_ANTIGO


def corrige_pq(df: pd.DataFrame, info: dict) -> pd.DataFrame:
    """Devolve df com P_ufv_pu e Q_ufv_pu em pu, reescalando rodada antiga."""
    if not escala_legada(info):
        return df
    df = df.copy()
    df["P_ufv_pu"] = df["P_ufv_pu"] * FATOR_P
    df["Q_ufv_pu"] = df["Q_ufv_pu"] * FATOR_Q
    return df


def le_sim_data(pasta: Path, **kw) -> pd.DataFrame:
    """pd.read_csv(pasta/sim_data.csv) com P e Q já corrigidas."""
    pasta = Path(pasta)
    df = pd.read_csv(pasta / "sim_data.csv", **kw)
    info_path = pasta / "fault_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8")) if info_path.exists() else {}
    return corrige_pq(df, info)
