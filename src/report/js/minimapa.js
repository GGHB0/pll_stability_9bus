// ── Mini-mapa (cap.lado "minimapa", Localização): o unifilar do capítulo
// "Faltas destacadas" com cada ponto na cor da curva e a retenção de v_d.
// MINI_ROT: deslocamento x, borda de referência (t topo, b base) e y.
var MINI_ROT = { b7: [-30, "b", 64], l78: [0, "t", -4], l89: [0, "t", -4], b6: [0, "b", 70] };

function _miniMapa(cap, side) {
  var fal = CAPS.filter(function(c) { return c.kind === "mapa"; })[0];
  if (!fal) return;
  // clicar num ponto liga/desliga o caso no gráfico, como o chip; o caso
  // desligado fica esmaecido e continua clicável
  var cor = {}, on = {}, st = _tccSt(cap);
  _tccCases(cap).forEach(function(v) { cor[v.key] = v.light; });
  fal.passos.forEach(function(q) { if (q.id && cor[q.cenario]) on[q.id] = true; });
  side.innerHTML = '<p class="pres-side-h">Onde foi a falta · retenção de v<sub>d</sub></p>'
    + '<div class="mapa-svg">' + _mapaSvg(fal, on, null) + '</div>';
  var svg = side.querySelector("svg"), ns = "http://www.w3.org/2000/svg";
  svg.querySelectorAll(".mp-hot").forEach(function(g) {
    var q = fal.passos[+(/_mapaGo\((\d+)\)/.exec(g.getAttribute("onclick"))[1])];
    g.removeAttribute("onclick");
    g.style.cursor = "default";
    if (!on[q.id]) return;
    var vis = st.on[q.cenario] !== false;
    g.style.cursor = "pointer";
    g.setAttribute("onclick", "_tccChip('" + q.cenario + "')");
    if (!vis) g.style.opacity = "0.3";
    var col = cor[q.cenario], ind = SCENARIOS[q.cenario].tccInd, r = MINI_ROT[q.id];
    g.querySelectorAll("line").forEach(function(el) { el.style.stroke = col; el.style.strokeWidth = "7"; });
    if (!ind || !ind.ret || !r) return;
    var bb = g.getBBox(), tx = document.createElementNS(ns, "text");
    tx.setAttribute("x", bb.x + bb.width / 2 + r[0]);
    tx.setAttribute("y", (r[1] === "b" ? bb.y + bb.height : bb.y) + r[2]);
    tx.setAttribute("text-anchor", "middle");
    tx.setAttribute("font-size", "34");
    tx.setAttribute("font-weight", "800");
    tx.setAttribute("fill", col);
    tx.textContent = ind.ret;
    tx.style.cursor = "pointer";
    tx.setAttribute("onclick", "_tccChip('" + q.cenario + "')");
    if (!vis) tx.setAttribute("opacity", "0.3");
    svg.appendChild(tx);
  });
}

