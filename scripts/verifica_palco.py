"""
verifica_palco.py — Percorre o modo apresentação do dashboard no Edge headless.

Abre output/pll_metrics.html, entra no palco no 1º capítulo e anda com a
seta → até o fim, como na defesa. Em cada tela (capítulo ou passo) tira um
PNG e confere:
  - erro de JavaScript na página;
  - se a tela cabe na janela (sem rolagem no palco);
  - se o gráfico não invade o painel ao lado (cap.lado).
Depois confere a navegação de volta (← entra no último passo), o fasor
(o instante segue o mouse e o play anda) e se a aba recupera os casos
escondidos pelos passos ao sair do palco.

Uso:
    .venv\\Scripts\\python.exe scripts\\verifica_palco.py
    .venv\\Scripts\\python.exe scripts\\verifica_palco.py --largura 1366 --altura 768

Saída: PNGs e relatorio.txt em output/verifica_palco/ (gitignored). Código
de saída 1 se alguma conferência falhar. Precisa do Playwright
(requirements.txt) e do Microsoft Edge instalado; não baixa navegador.
Os PNGs são para leitura humana ou do agente palco-validator: texto
cortado, sobreposição e número errado não saem destas conferências.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ESTADO_JS = """() => ({
  n: tccCap + 1, total: CAPS.length, id: CAPS[tccCap].id, passo: presPasso,
  passos: (CAPS[tccCap].passos_pres || []).length,
  mapaPasso: mapaPasso, mapaPassos: (CAPS[tccCap].passos || []).length,
  scroll: document.getElementById('pres').scrollHeight,
  janela: window.innerHeight,
  invade: (function() {
    var s = document.getElementById('pres-side'), g = document.getElementById('pres-plot');
    if (!s || s.style.display === 'none' || !g._fullLayout) return false;
    return g.getBoundingClientRect().left + g._fullLayout.width > s.getBoundingClientRect().left + 1;
  })()
})"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--html", default=str(ROOT / "output" / "pll_metrics.html"))
    ap.add_argument("--out", default=str(ROOT / "output" / "verifica_palco"))
    ap.add_argument("--largura", type=int, default=1920)
    ap.add_argument("--altura", type=int, default=1080)
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright não instalado: .venv\\Scripts\\pip install -r requirements.txt")
        return 2

    html = Path(a.html).resolve()
    if not html.exists():
        print(f"HTML não encontrado: {html} (rode app.py antes)")
        return 2
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()

    falhas: list[str] = []
    linhas: list[str] = []

    with sync_playwright() as p:
        nav = p.chromium.launch(channel="msedge")
        pg = nav.new_page(viewport={"width": a.largura, "height": a.altura})
        erros: list[str] = []
        pg.on("pageerror", lambda e: erros.append(str(e)))
        pg.goto(html.as_uri(), timeout=180_000)
        pg.wait_for_function("typeof presToggle === 'function'", timeout=180_000)
        pg.evaluate("() => { tccCap = 0; mapaPasso = 0; presToggle(); }")
        pg.wait_for_timeout(900)

        vistos = 0
        while True:
            e = pg.evaluate(ESTADO_JS)
            sub = (f"p{e['passo'] + 1}" if e["passos"] else
                   f"m{e['mapaPasso'] + 1}" if e["mapaPassos"] else "")
            nome = f"{e['n']:02d}_{e['id']}{'_' + sub if sub else ''}"
            pg.screenshot(path=str(out / f"{nome}.png"))
            ok = []
            if e["scroll"] > e["janela"]:
                falhas.append(f"{nome}: não cabe na tela ({e['scroll']} > {e['janela']} px)")
                ok.append("ROLA")
            if e["invade"]:
                falhas.append(f"{nome}: gráfico invade o painel ao lado")
                ok.append("INVADE")
            linhas.append(f"{nome:28s} {'ok' if not ok else ' '.join(ok)}")
            vistos += 1

            if pg.evaluate("() => CAPS[tccCap].lado === 'fasor'"):
                falhas += _confere_fasor(pg, out, nome)

            antes = (e["n"], e["passo"], e["mapaPasso"])
            pg.keyboard.press("ArrowRight")
            pg.wait_for_timeout(700)
            d = pg.evaluate(ESTADO_JS)
            if (d["n"], d["passo"], d["mapaPasso"]) == antes:
                break
            if vistos > 60:
                falhas.append("a seta → não chegou ao fim do palco em 60 telas")
                break

        # volta: do capítulo seguinte, ← deve cair no último passo do capítulo
        # com passos (i é o índice 0-based; o último capítulo não tem seguinte)
        com_passos = pg.evaluate("() => CAPS.map(function(c, i) { return c.passos_pres ? i : -1; })"
                                 ".filter(function(i) { return i >= 0 && i < CAPS.length - 1; })")
        for i in com_passos:
            seguinte = i + 1
            pg.evaluate(f"() => presGo({seguinte})")
            pg.wait_for_timeout(500)
            pg.keyboard.press("ArrowLeft")
            pg.wait_for_timeout(600)
            d = pg.evaluate(ESTADO_JS)
            if d["n"] != i + 1 or d["passo"] != d["passos"] - 1:
                falhas.append(f"voltar com ← para o capítulo {i + 1} não caiu no último passo "
                              f"(foi para {d['n']}, passo {d['passo'] + 1})")

        # sair do palco: casos escondidos pelos passos voltam à aba
        pg.evaluate("() => { if (presOn) presToggle(); }")
        pg.wait_for_timeout(400)
        presos = pg.evaluate("""() => CAPS.filter(function(c) { return c.passos_pres && tccState[c.id]; })
          .map(function(c) { return Object.keys(tccState[c.id].on)
            .filter(function(k) { return tccState[c.id].on[k] === false; }); })
          .reduce(function(a, b) { return a.concat(b); }, [])""")
        if presos:
            falhas.append(f"casos ainda escondidos na aba depois de sair do palco: {presos}")

        for er in erros:
            falhas.append(f"erro de JS: {er}")
        nav.close()

    rel = [f"Palco em {a.largura}×{a.altura}: {vistos} telas", *linhas, ""]
    rel += ["FALHAS:", *[f"  - {f}" for f in falhas]] if falhas else ["Sem falhas."]
    (out / "relatorio.txt").write_text("\n".join(rel) + "\n", encoding="utf-8")
    print("\n".join(rel))
    print(f"\nPNGs em {out}")
    return 1 if falhas else 0


def _confere_fasor(pg, out: Path, nome: str) -> list[str]:
    """O instante do fasor segue o mouse no gráfico e o play anda."""
    f: list[str] = []
    box = pg.eval_on_selector("#pres-plot", "e => { var r = e.getBoundingClientRect(); "
                                            "return [r.x, r.y, r.width, r.height]; }")
    t0 = pg.evaluate("() => fasorT")
    pg.mouse.move(box[0] + box[2] * 0.6, box[1] + box[3] * 0.3)
    pg.wait_for_timeout(400)
    t1 = pg.evaluate("() => fasorT")
    if t1 == t0:
        f.append(f"{nome}: o fasor não seguiu o mouse")
    pg.screenshot(path=str(out / f"{nome}_fasor_mouse.png"))
    pg.mouse.move(2, 2)
    pg.click("#fs-play")
    pg.wait_for_timeout(1500)
    t2, anda = pg.evaluate("() => [fasorT, !!_fasorRaf]")
    if not anda or t2 == t1:
        f.append(f"{nome}: o play do fasor não andou")
    pg.screenshot(path=str(out / f"{nome}_fasor_play.png"))
    pg.evaluate("() => _fasorStop()")
    return f


if __name__ == "__main__":
    sys.exit(main())
