"""Auditoria do deck antes da entrega. Código 1 se houver FALHA.

    python.exe check_pptx.py <deck.pptx> [--tcc <canônico.docx>] [--slides 1-16]

FALHA (bloqueia a entrega):
  - forma fora da área do slide (tolerância 0,02 in)
  - "Figura/Tabela X.Y do TCC" que não existe no DOCX (com --tcc)
AVISO (o principal decide; confirmar no render):
  - texto que provavelmente não cabe na caixa (estimativa por caracteres)
  - corpo de texto < 11 pt (ilegível projetado)
  - imagem abaixo de 150 px/in na escala exibida (borra no projetor)
  - fonte explícita fora de Arial/Calibri (design.md)
  - travessão "—" em slide ou nota; identificador de código (BAD_PLL, params.m)
  - slide sem notas
A estimativa de overflow não substitui o render: render.ps1 e ler os PNGs.
"""
import argparse
import re
import zipfile

from pptx_util import abrir, faixa, formas, notas, pol, texto_forma, tipo, utf8

utf8()
ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("--tcc")
ap.add_argument("--slides")
a = ap.parse_args()

FONTES_OK = {"Arial", "Calibri", "+mj-lt", "+mn-lt"}
CODIGO = re.compile(r"\b(BAD_PLL|FAULT_TYPE|params\.m|logsout|[A-Z]{2,}_[A-Z_]{2,})\b")
REF_TCC = re.compile(r"\b(Figura|Gráfico|Tabela|Quadro)s?\s+(\d+\.\d+)(?:\s*(?:,|e)\s*(\d+\.\d+))*")

prs = abrir(a.pptx)
W, H = pol(prs.slide_width), pol(prs.slide_height)
falhas, avisos = [], []

legendas = {}
if a.tcc:
    xml = zipfile.ZipFile(a.tcc).read("word/document.xml").decode("utf8")
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
        m = re.match(r"\s*(Figura|Gráfico|Tabela|Quadro)\s+(\d+\.\d+)\s*[–-]\s*(.*)", t)
        if m:
            legendas.setdefault(m.group(2), (m.group(1), m.group(3)[:90]))


def cabe(sh):
    """Estimativa grosseira: linhas necessárias x altura de linha vs altura da caixa.
    Só julga texto que quebra linha: caixa de uma linha é desenhada justa de
    propósito (título de cartão, número grande) e sempre cai no aviso à toa.
    Caixa com autoajuste (normAutofit) ou sem quebra (wrap=none) fica de fora."""
    tf = sh.text_frame
    body = tf._txBody.bodyPr
    if body.get("wrap") == "none" or body.find(
            "{http://schemas.openxmlformats.org/drawingml/2006/main}normAutofit") is not None:
        return True, 0
    w_pt = (pol(sh.width) - 0.2) * 72
    h_pt = (pol(sh.height) - 0.1) * 72
    if w_pt <= 0 or h_pt <= 0:
        return True, 0
    usado, quebrou = 0.0, False
    for p in tf.paragraphs:
        tam = max([r.font.size.pt for r in p.runs if r.font.size] or [18])
        chars_linha = max(1, int(w_pt / (0.44 * tam)))
        linhas = max(1, -(-len(p.text) // chars_linha))
        quebrou |= linhas > 1
        usado += linhas * tam * 1.2
    if not quebrou:
        return True, 0
    return usado <= h_pt * 1.25, usado / h_pt


slides = list(prs.slides)
for n in faixa(a.slides, len(slides)):
    s = slides[n - 1]
    if not notas(s):
        avisos.append(f"slide {n}: sem notas")
    if "—" in notas(s):
        avisos.append(f"slide {n} NOTAS: travessão")
    for c in CODIGO.findall(notas(s)):
        avisos.append(f"slide {n} NOTAS: identificador de código '{c}'")
    for sh, _ in formas(s):
        x, y, w, h = pol(sh.left), pol(sh.top), pol(sh.width), pol(sh.height)
        if round(getattr(sh, "rotation", 0) or 0) % 180 == 90:   # girada a 90/270: caixa visível troca w e h no centro
            x, y, w, h = x + (w - h) / 2, y + (h - w) / 2, h, w
        nome = f'slide {n} "{sh.name}"'
        if x < -0.02 or y < -0.02 or x + w > W + 0.02 or y + h > H + 0.02:
            falhas.append(f"{nome}: fora do slide ({x:.2f},{y:.2f}) {w:.2f}x{h:.2f}")
        txt = texto_forma(sh)
        if "—" in txt:
            avisos.append(f"{nome}: travessão")
        for c in CODIGO.findall(txt):
            avisos.append(f"{nome}: identificador de código '{c}'")
        for m in REF_TCC.finditer(txt):
            if "TCC" not in txt[m.end():m.end() + 12] and "TCC" not in txt[:m.start()]:
                continue
            for num in [g for g in m.groups()[1:] if g]:
                if a.tcc and num not in legendas:
                    falhas.append(f"{nome}: '{m.group(1)} {num}' não existe no TCC")
                elif a.tcc and legendas[num][0] != m.group(1):
                    falhas.append(f"{nome}: TCC chama de {legendas[num][0]} {num}, deck diz {m.group(1)}")
        if tipo(sh) == "imagem":
            px = sh.image.size[0] / max(w, 0.01)
            if px < 150:
                avisos.append(f"{nome}: imagem a {px:.0f} px/in")
        if sh.has_text_frame and txt.strip():
            ok, r = cabe(sh)
            if not ok:
                avisos.append(f"{nome}: texto talvez não caiba ({r:.0%} da altura): {txt[:60]}")
            for p in sh.text_frame.paragraphs:
                for run in p.runs:
                    if run.font.size and run.font.size.pt < 11 and run.text.strip():
                        avisos.append(f"{nome}: {run.font.size.pt:.0f} pt em '{run.text[:40]}'")
                        break
                    if run.font.name and run.font.name not in FONTES_OK:
                        avisos.append(f"{nome}: fonte {run.font.name}")
                        break

if a.tcc:
    print(f"TCC: {len(legendas)} legendas lidas de {a.tcc}")
for f in falhas:
    print("FALHA:", f)
for av in dict.fromkeys(avisos):
    print("AVISO:", av)
print(f"\n{len(falhas)} falha(s), {len(set(avisos))} aviso(s)")
raise SystemExit(1 if falhas else 0)
