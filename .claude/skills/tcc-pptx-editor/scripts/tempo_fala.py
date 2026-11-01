"""Tempo de fala estimado pelas notas: por slide, por orador e total do corpo.

    python.exe tempo_fala.py <deck.pptx> [--ppm 130] [--limite 30] [--ate N]

--ppm     palavras por minuto (130 = fala técnica pausada em português)
--limite  minutos da defesa (30, combinado com o Victor em 2026-10-16)
--ate     último slide do corpo; padrão: o slide antes do 1º layout DIVIDER
          (o "Apêndice" não entra na conta: é material para perguntas)

Avisa: slide do corpo sem notas, trecho sem marcador [Bruno]/[Victor],
desequilíbrio entre os oradores acima de 60/40. Código 1 se passar do limite.
"""
import argparse

from pptx_util import abrir, falas, notas, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("--ppm", type=float, default=130)
ap.add_argument("--limite", type=float, default=30)
ap.add_argument("--ate", type=int)
a = ap.parse_args()

slides = list(abrir(a.pptx).slides)
ate = a.ate
if not ate:
    div = [i for i, s in enumerate(slides, 1) if s.slide_layout.name.upper() == "DIVIDER"]
    ate = div[0] - 1 if div else len(slides)

tot = {"Bruno": 0, "Victor": 0, "?": 0}
avisos = []
print(f"{'slide':>5} {'Bruno':>6} {'Victor':>6} {'min':>5}  acumulado")
acum = 0.0
for n, s in enumerate(slides[:ate], 1):
    por = {"Bruno": 0, "Victor": 0, "?": 0}
    partes = falas(notas(s))
    if not partes:
        avisos.append(f"slide {n}: sem notas")
    for quem, trecho in partes:
        por[quem] += len(trecho.split())
    if por["?"]:
        avisos.append(f"slide {n}: {por['?']} palavras sem marcador [Bruno]/[Victor]")
    m = sum(por.values()) / a.ppm
    acum += m
    for k in tot:
        tot[k] += por[k]
    print(f"{n:>5} {por['Bruno']:>6} {por['Victor']:>6} {m:>5.1f}  {acum:5.1f}")

palavras = sum(tot.values())
minutos = palavras / a.ppm
print(f"\ncorpo: slides 1-{ate}, {palavras} palavras, {minutos:.1f} min a {a.ppm:.0f} ppm"
      f" (limite {a.limite:.0f} min)")
fal = tot["Bruno"] + tot["Victor"]
if fal:
    pb = 100 * tot["Bruno"] / fal
    print(f"Bruno {tot['Bruno']} palavras ({pb:.0f}%), Victor {tot['Victor']} ({100 - pb:.0f}%)")
    if not 40 <= pb <= 60:
        avisos.append(f"divisão desequilibrada: Bruno {pb:.0f}% / Victor {100 - pb:.0f}%")
for av in avisos:
    print("AVISO:", av)
if minutos > a.limite:
    print(f"ACIMA DO LIMITE em {minutos - a.limite:.1f} min")
    raise SystemExit(1)
