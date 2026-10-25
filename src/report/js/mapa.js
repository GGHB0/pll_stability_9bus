// ── Capítulo kind "mapa" (Faltas destacadas): unifilar redesenhado do
// ieee9bus_unifilar.svg, sem R/X/B nem cargas; a Linha 8-9 em dois circuitos ──
var mapaPasso = 0;
var MAPA_RAIO = { b7: [265, 222], l78: [368, 178], l89: [568, 187], b6: [665, 392] };

function _mapaSvg(cap, on, cur) {
  var idx = {};
  cap.passos.forEach(function(p, i) { if (p.id) idx[p.id] = i; });
  var c = function(id) { return on[id] ? " on" : ""; };
  var hot = function(id) {
    return "<g class=\"mp-hot" + (cur === id ? " cur" : "") + "\" onclick=\"_mapaGo(" + idx[id] + ")\">";
  };
  var cond = function(pts) { return "<polyline class=\"mp-cond\" points=\"" + pts + "\"/>"; };
  var trafo = function(x1, y1, x2, y2, r) {
    return "<circle cx=\"" + x1 + "\" cy=\"" + y1 + "\" r=\"" + r + "\" class=\"mp-fill\" stroke=\"#1e40af\" stroke-width=\"2.2\"/>"
         + "<circle cx=\"" + x2 + "\" cy=\"" + y2 + "\" r=\"" + r + "\" class=\"mp-fill\" stroke=\"#1e40af\" stroke-width=\"2.2\"/>";
  };
  var gen = function(x, y, r) {
    return "<circle cx=\"" + x + "\" cy=\"" + y + "\" r=\"" + r + "\" class=\"mp-fill\" stroke=\"#166534\" stroke-width=\"2.5\"/>";
  };
  var s = "<svg viewBox=\"20 90 860 590\" preserveAspectRatio=\"xMidYMid meet\">"
    // usina e Barra 2
    + "<rect x=\"30\" y=\"140\" width=\"66\" height=\"78\" rx=\"5\" fill=\"#fffbeb\" stroke=\"#b45309\" stroke-width=\"2\"/>"
    + "<text x=\"63\" y=\"176\" text-anchor=\"middle\" font-size=\"13\" font-weight=\"700\" fill=\"#b45309\">UFV</text>"
    + "<text x=\"63\" y=\"191\" text-anchor=\"middle\" font-size=\"10.5\" fill=\"#78350f\">100 MW</text>"
    + "<text x=\"63\" y=\"205\" text-anchor=\"middle\" font-size=\"10.5\" fill=\"#b45309\">SRF-PLL</text>"
    + cond("96,178 265,178")
    + "<line class=\"mp-bus\" style=\"stroke:#b45309\" x1=\"109\" y1=\"152\" x2=\"109\" y2=\"204\"/>"
    + "<text x=\"109\" y=\"139\" text-anchor=\"middle\" class=\"mp-lbl\" style=\"fill:#b45309\">2</text>"
    + trafo(174, 178, 200, 178, 13)
    + "<text x=\"187\" y=\"212\" text-anchor=\"middle\" font-size=\"12.5\" font-weight=\"600\" fill=\"#1e40af\">T2</text>"
    // anel inferior, G1 e G3
    + cond("265,200 300,200 300,392") + cond("668,200 633,200 633,392")
    + cond("336,392 336,498 412,498 412,517") + cond("598,392 598,498 524,498 524,517")
    + cond("468,517 468,538") + trafo(468, 550, 468, 572, 12) + cond("468,584 468,620")
    + "<line class=\"mp-bus\" style=\"stroke:#166534\" x1=\"440\" y1=\"604\" x2=\"496\" y2=\"604\"/>"
    + gen(468, 638, 20) + "<text x=\"500\" y=\"643\" class=\"mp-lbl\" style=\"fill:#166534\">G1</text>"
    + cond("668,178 815,178") + trafo(719, 178, 745, 178, 13)
    + gen(840, 178, 22) + "<text x=\"840\" y=\"230\" text-anchor=\"middle\" class=\"mp-lbl\" style=\"fill:#166534\">G3</text>"
    // barras sem falta
    + "<line class=\"mp-bus\" x1=\"178\" y1=\"392\" x2=\"362\" y2=\"392\"/><text x=\"185\" y=\"378\" class=\"mp-lbl\">5</text>"
    + "<line class=\"mp-bus\" x1=\"352\" y1=\"517\" x2=\"584\" y2=\"517\"/><text x=\"468\" y=\"503\" text-anchor=\"middle\" class=\"mp-lbl\">4</text>"
    + "<line class=\"mp-bus\" x1=\"468\" y1=\"128\" x2=\"468\" y2=\"218\"/><text x=\"468\" y=\"113\" text-anchor=\"middle\" class=\"mp-lbl\">8</text>"
    + "<line class=\"mp-bus\" x1=\"668\" y1=\"142\" x2=\"668\" y2=\"258\"/><text x=\"668\" y=\"127\" text-anchor=\"middle\" class=\"mp-lbl\">9</text>"
    // pontos de falta (clicáveis)
    + hot("l78") + "<rect class=\"mp-hit\" x=\"272\" y=\"150\" width=\"190\" height=\"56\" rx=\"6\"/>"
    + "<line class=\"mp-cond" + c("l78") + "\" x1=\"265\" y1=\"178\" x2=\"468\" y2=\"178\"/></g>"
    + hot("l89") + "<rect class=\"mp-hit\" x=\"474\" y=\"150\" width=\"188\" height=\"56\" rx=\"6\"/>"
    + "<line class=\"mp-cond" + c("l89") + "\" x1=\"468\" y1=\"171\" x2=\"668\" y2=\"171\"/>"
    + "<line class=\"mp-cond" + c("l89") + "\" x1=\"468\" y1=\"187\" x2=\"668\" y2=\"187\"/>"
    + cond("468,171 468,187") + cond("668,171 668,187") + "</g>"
    + hot("b7") + "<rect class=\"mp-hit\" x=\"248\" y=\"118\" width=\"34\" height=\"150\" rx=\"6\"/>"
    + "<line class=\"mp-bus" + c("b7") + "\" x1=\"265\" y1=\"142\" x2=\"265\" y2=\"258\"/>"
    + "<text x=\"265\" y=\"127\" text-anchor=\"middle\" class=\"mp-lbl\">7</text></g>"
    + hot("b6") + "<rect class=\"mp-hit\" x=\"565\" y=\"364\" width=\"200\" height=\"40\" rx=\"6\"/>"
    + "<line class=\"mp-bus" + c("b6") + "\" x1=\"572\" y1=\"392\" x2=\"758\" y2=\"392\"/>"
    + "<text x=\"751\" y=\"378\" text-anchor=\"end\" class=\"mp-lbl\">6</text></g>";
  Object.keys(MAPA_RAIO).forEach(function(id) {
    if (!on[id]) return;
    var p = MAPA_RAIO[id];
    s += "<g class=\"mp-raio\" transform=\"translate(" + p[0] + "," + p[1] + ")\"><circle r=\"20\"/>"
       + "<path d=\"M3,-13 L-7,2 L-1,2 L-4,13 L7,-4 L1,-4z\"/></g>";
  });
  if (on.l89) s += "<g class=\"mp-note\"><text x=\"568\" y=\"152\" text-anchor=\"middle\" font-size=\"13\" fill=\"#6b7280\">circuito sem falta</text>"
    + "<text x=\"568\" y=\"228\" text-anchor=\"middle\" font-size=\"13\" font-weight=\"700\" fill=\"#dc2626\">circuito com falta</text></g>";
  if (on.b7) s += "<text class=\"mp-note\" x=\"200\" y=\"290\" text-anchor=\"middle\" font-size=\"14\" font-weight=\"700\" fill=\"#dc2626\">mais perto da usina</text>";
  if (on.b6) s += "<text class=\"mp-note\" x=\"665\" y=\"432\" text-anchor=\"middle\" font-size=\"14\" font-weight=\"700\" style=\"fill:var(--accent)\">mais longe da usina</text>";
  return s + "</svg>";
}

// gid: prefixo do gradiente, para a aba e o palco não repetirem o id
function _mapaHtml(cap, gid) {
  var p = cap.passos[mapaPasso], on = {};
  cap.passos.forEach(function(q) { if (q.id && (p.resumo || q.id === p.id)) on[q.id] = true; });
  var side = "<div class=\"mp-card\"><span class=\"mp-tag " + (p.tom || "") + "\">" + p.tag + "</span>"
    + "<p class=\"mp-h\">" + p.titulo + "</p>"
    + p.texto.map(function(t) { return "<p class=\"mp-p\">" + t + "</p>"; }).join("")
    + "<p class=\"mp-why\">" + p.papel + "</p>";
  if (p.faltas) {
    side += "<div class=\"mp-facts\">" + ["trifásica", "bifásica", "monofásica"].map(function(f) {
      return "<span" + (p.faltas.indexOf(f) === -1 ? " class=\"off\"" : "") + ">" + f + "</span>";
    }).join("") + "<span>sintonia nominal</span><span" + (p.inadequada ? "" : " class=\"off\"")
      + ">sintonia inadequada</span></div>";
  }
  if (p.cenario && SCENARIOS[p.cenario]) {
    side += "<button class=\"mp-open\" onclick=\"_openScenario('" + p.cenario + "')\">Abrir no painel &rarr;</button>";
  }
  side += "</div>";
  var pins = cap.passos.map(function(q, k) {
    if (!q.id) return "";
    var cx = 10 + q.pos * 360, cur = (q.id === p.id);
    return "<g class=\"mp-pin\" onclick=\"_mapaGo(" + k + ")\" opacity=\"" + (on[q.id] ? 1 : 0.3) + "\">"
      + "<circle cx=\"" + cx + "\" cy=\"30\" r=\"" + (cur ? 10 : 8) + "\"/>"
      + "<text x=\"" + cx + "\" y=\"60\" text-anchor=\"middle\">" + q.rotulo + "</text></g>";
  }).join("");
  side += "<svg class=\"mp-ruler\" viewBox=\"0 0 380 74\"><defs><linearGradient id=\"" + gid + "-gr\" x1=\"0\" x2=\"1\">"
    + "<stop offset=\"0\" stop-color=\"#dc2626\"/><stop offset=\"1\" stop-color=\"#2563eb\"/></linearGradient></defs>"
    + "<text x=\"10\" y=\"14\">afundamento mais profundo</text>"
    + "<text x=\"370\" y=\"14\" text-anchor=\"end\">mais raso</text>"
    + "<rect x=\"10\" y=\"26\" width=\"360\" height=\"8\" rx=\"4\" fill=\"url(#" + gid + "-gr)\"/>" + pins + "</svg>"
    + "<p class=\"mp-step\">" + _passoInd(mapaPasso, cap.passos.length) + "</p>";
  return "<div class=\"mapa\"><div class=\"mapa-svg\">" + _mapaSvg(cap, on, p.id)
    + "<p class=\"mapa-hint\">Clique numa barra ou linha para ver o ponto de falta</p></div>"
    + "<div class=\"mapa-side\">" + side + "</div></div>";
}

function _mapaGo(n) {
  var cap = CAPS[tccCap];
  if (cap.kind !== "mapa" || n < 0 || n >= cap.passos.length) return;
  mapaPasso = n;
  _tccRefresh();
}

// seta dentro do capítulo mapa: anda um passo; true se consumiu a tecla
function _mapaStep(d) {
  var cap = CAPS[tccCap], n = mapaPasso + d;
  if (cap.kind !== "mapa" || n < 0 || n >= cap.passos.length) return false;
  _mapaGo(n);
  return true;
}

// ao entrar num capítulo mapa: passo 1, ou o último se veio pela seta ←
function _mapaEnter(i, back) {
  if (CAPS[i].kind === "mapa" && i !== tccCap) mapaPasso = back ? CAPS[i].passos.length - 1 : 0;
}

// seta (teclado ou botões ‹ ›): passo do mapa ou capítulo vizinho
