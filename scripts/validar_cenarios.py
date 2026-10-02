"""
Valida os cenarios exportados em output/results/ antes de gerar figura.

Rodar depois de todo `git pull` com simulacao nova do Bruno:
    .venv\\Scripts\\python.exe scripts\\validar_cenarios.py

Checagens (ERRO = o cenario nao pode ir para figura; AVISO = usar com cuidado):
  ERRO  duplicado    sim_data.csv identico byte a byte ao de outra pasta: o
                     export gravou dados de outra rodada (logsout velho).
  ERRO  assinatura   o tipo de falta da pasta nao bate com as tensoes abc do
                     inversor durante a falta: trifasica tem de afundar as 3
                     fases por igual, mono/bifasica tem de desequilibrar.
  AVISO safra        sintonia inadequada com falta fora de 0,3-0,4 s (safra de
                     agosto/2026, v_d pre-falta ~0,82 pu no modelo da epoca).
  AVISO redundante   existem `1phase_bad_pll` e `1phase_ground_bad_pll` na mesma
                     barra: o export novo grava `1phase_ground`, o nome antigo
                     e `1phase` (mesmo tipo de falta).

Os geradores de figura importam `cenario_ok()` e `pasta_inadequada()` para
nunca plotar cenario com ERRO. Detalhe em
.claude/kb/simulation/cenarios_simulados.md.
"""
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "output" / "results"
DESEQ_SIM = 0.05     # trifasica: diferenca max entre fases (pu do pre-falta)
DESEQ_ASSIM = 0.15   # mono/bifasica: desequilibrio minimo esperado
T_FAULT_ATUAL = 0.3


def pastas():
    return sorted(p.parent.relative_to(RES).as_posix() for p in RES.glob("**/fault_info.json"))


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _desequilibrio(folder, fi):
    p = RES / folder / "sim_data_abc.csv"
    if not p.exists():
        return None
    d = pd.read_csv(p, usecols=["t_s", "va_ufv_pu", "vb_ufv_pu", "vc_ufv_pu"])
    tf, tc = fi["t_fault"], fi["t_clear"]
    w = d[(d.t_s > tf + 0.03) & (d.t_s < tc)]
    pre = d[(d.t_s > tf - 0.05) & (d.t_s < tf)]
    r = [np.sqrt((w[c] ** 2).mean() / (pre[c] ** 2).mean()) for c in ("va_ufv_pu", "vb_ufv_pu", "vc_ufv_pu")]
    return max(r) - min(r)


@lru_cache(maxsize=1)
def validar():
    """{pasta: [(nivel, codigo, mensagem), ...]} para todas as pastas."""
    out = {f: [] for f in pastas()}
    for f in out:
        fi = json.loads((RES / f / "fault_info.json").read_text())
        tipo = fi.get("fault_type", "")
        if tipo != "regime" and not f.startswith("regime"):
            dq = _desequilibrio(f, fi)
            if dq is not None:
                if tipo == "3phase" and dq > DESEQ_SIM:
                    out[f].append(("ERRO", "assinatura", f"trifásica desequilibrada ({dq:.2f} pu)"))
                elif tipo != "3phase" and dq < DESEQ_ASSIM:
                    out[f].append(("ERRO", "assinatura",
                                   f"{tipo} com afundamento equilibrado ({dq:.2f} pu): parece trifásica"))
        if fi.get("bad_pll") and abs(fi["t_fault"] - T_FAULT_ATUAL) > 1e-6:
            out[f].append(("AVISO", "safra", f"falta em {fi['t_fault']} s (safra antiga)"))
        if f.endswith("/1phase_bad_pll") and (RES / f.replace("1phase_bad", "1phase_ground_bad")).exists():
            out[f].append(("AVISO", "redundante", "existe também 1phase_ground_bad_pll (nome novo)"))
    # duplicata: a copia e quem tem a assinatura errada; o original (assinatura
    # coerente) fica so com aviso. Sem como decidir, todos viram ERRO.
    hashes = {}
    for f in out:
        hashes.setdefault(_md5(RES / f / "sim_data.csv"), []).append(f)
    for grupo in (g for g in hashes.values() if len(g) > 1):
        ruins = [f for f in grupo if any(k == "assinatura" for _, k, _ in out[f])]
        for f in grupo:
            outros = ", ".join(g for g in grupo if g != f)
            nivel = "AVISO" if ruins and f not in ruins else "ERRO"
            out[f].append((nivel, "duplicado", f"sim_data.csv idêntico a {outros}"))
    return out


def cenario_ok(folder):
    return (RES / folder / "fault_info.json").exists() and \
        not any(n == "ERRO" for n, _, _ in validar().get(folder, []))


def pasta_inadequada(folder):
    """Pasta de sintonia inadequada valida para o cenario nominal `folder`, ou
    None. Prefere o nome novo (`1phase_ground_bad_pll`) e a safra atual."""
    cand = [folder + "_bad_pll"]
    if folder.endswith("/1phase"):
        cand.insert(0, folder + "_ground_bad_pll")
    validos = [c for c in cand if cenario_ok(c)]
    atuais = [c for c in validos if not any(k == "safra" for _, k, _ in validar()[c])]
    return (atuais or validos or [None])[0]


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    res = validar()
    n_err = 0
    for f, probs in res.items():
        for nivel, cod, msg in probs:
            n_err += nivel == "ERRO"
            print(f"{nivel:5s} {cod:11s} {f:30s} {msg}")
    print(f"\n{len(res)} cenários · {n_err} erros · "
          f"{sum(len(p) for p in res.values()) - n_err} avisos")
    sys.exit(1 if n_err else 0)
