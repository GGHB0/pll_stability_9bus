// ── Sequências (cap.lado "seq", Sequência negativa): animação didática,
// sem dado simulado. Em cima, vista da rede: a positiva gira num sentido, a
// negativa no outro, e a soma (a tensão) percorre uma elipse; o eixo d do
// PLL acompanha a positiva. Embaixo, vista do PLL: a positiva fica parada
// em d e a negativa gira a 2ω (120 Hz), fazendo v_d e v_q oscilarem.
// Amplitudes ilustrativas, sem número na tela.
var _seqRaf = null, SEQ_MS = 6000, SEQ_NEG = 0.35;
var SEQ_COR = { pos: "#2563eb", neg: "#be123c", v: "#0f172a", ax: "#94a3b8" };

function _seqVec(x0, y0, x1, y1, cor, w, id) {
  return '<line x1="' + x0 + '" y1="' + y0 + '" x2="' + x1 + '" y2="' + y1 + '" stroke="' + cor
    + '" stroke-width="' + w + '" stroke-linecap="round" marker-end="url(#sq-' + id + ')"/>';
}

function _seqDraw(now) {
  var box = document.getElementById("sq-svg");
  if (!box) return;
  var th = 2 * Math.PI * (now % SEQ_MS) / SEQ_MS, n = SEQ_NEG, C = SEQ_COR;
  var defs = ["pos", "neg", "v"].map(function(k) {
    return '<marker id="sq-' + k + '" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5"'
      + ' markerHeight="4.5" orient="auto"><path d="M0,0L10,5L0,10z" fill="' + C[k] + '"/></marker>';
  }).join("");
  // vista da rede: origem (190, 175), 1 pu = 95 px
  var cx = 190, cy = 175, K = 95, el = "";
  for (var i = 0; i <= 72; i++) {
    var a = 2 * Math.PI * i / 72;
    el += (i ? "L" : "M") + (cx + K * (1 + n) * Math.cos(a)).toFixed(1) + ","
      + (cy - K * (1 - n) * Math.sin(a)).toFixed(1);
  }
  var px = cx + K * Math.cos(th), py = cy - K * Math.sin(th);
  var sx = px + K * n * Math.cos(-th), sy = py - K * n * Math.sin(-th);
  var dx = cx + 125 * Math.cos(th), dy = cy - 125 * Math.sin(th);
  var top = '<text x="190" y="20" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">'
    + 'Vista da rede</text>'
    + '<path d="' + el + '" fill="none" stroke="' + C.ax + '" stroke-width="1.5" stroke-dasharray="5 5"/>'
    + '<line x1="' + cx + '" y1="' + cy + '" x2="' + dx + '" y2="' + dy + '" stroke="' + C.ax
    + '" stroke-width="1.5" stroke-dasharray="3 4"/>'
    + '<text x="' + (cx + 138 * Math.cos(th)) + '" y="' + (cy - 138 * Math.sin(th) + 5)
    + '" text-anchor="middle" font-size="14" font-weight="700" fill="#64748b">d</text>'
    + _seqVec(cx, cy, px, py, C.pos, 4.5, "pos") + _seqVec(px, py, sx, sy, C.neg, 4, "neg")
    + _seqVec(cx, cy, sx, sy, C.v, 2.2, "v") + '<circle cx="' + cx + '" cy="' + cy + '" r="4" fill="#0f172a"/>';
  // vista do PLL: d na horizontal, positiva parada, negativa a −2θ (120 Hz)
  var ox = 50, oy = 470, Kd = 200, fi = -2 * th;
  var tx = ox + Kd, ux = tx + Kd * n * Math.cos(fi), uy = oy - Kd * n * Math.sin(fi);
  var bot = '<text x="190" y="345" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">'
    + 'Vista do PLL (eixos dq)</text>'
    + '<line x1="' + (ox - 10) + '" y1="' + oy + '" x2="350" y2="' + oy + '" stroke="' + C.ax + '" stroke-width="1.5"/>'
    + '<line x1="' + ox + '" y1="' + (oy + 90) + '" x2="' + ox + '" y2="' + (oy - 100) + '" stroke="' + C.ax + '" stroke-width="1.5"/>'
    + '<text x="360" y="' + (oy + 5) + '" font-size="14" font-weight="700" fill="#64748b">d</text>'
    + '<text x="' + ox + '" y="' + (oy - 106) + '" text-anchor="middle" font-size="14" font-weight="700" fill="#64748b">q</text>'
    + '<circle cx="' + tx + '" cy="' + oy + '" r="' + (Kd * n) + '" fill="none" stroke="' + C.neg
    + '" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="5 5"/>'
    + '<line x1="' + ux + '" y1="' + uy + '" x2="' + ux + '" y2="' + oy + '" stroke="#64748b" stroke-dasharray="3 3"/>'
    + '<line x1="' + ux + '" y1="' + uy + '" x2="' + ox + '" y2="' + uy + '" stroke="#64748b" stroke-dasharray="3 3"/>'
    + '<circle cx="' + ux + '" cy="' + oy + '" r="6" fill="#0f172a"/>'
    + '<circle cx="' + ox + '" cy="' + uy + '" r="6" fill="#0f172a"/>'
    + '<text x="' + ux + '" y="' + (oy + 26) + '" text-anchor="middle" font-size="15" font-weight="700"'
    + ' fill="#0f172a">v<tspan font-size="11" dy="4">d</tspan></text>'
    + '<text x="' + (ox - 10) + '" y="' + (uy + 5) + '" text-anchor="end" font-size="15" font-weight="700"'
    + ' fill="#0f172a">v<tspan font-size="11" dy="4">q</tspan></text>'
    + _seqVec(ox, oy, tx, oy, C.pos, 4.5, "pos") + _seqVec(tx, oy, ux, uy, C.neg, 4, "neg")
    + _seqVec(ox, oy, ux, uy, C.v, 2.2, "v");
  box.innerHTML = '<svg viewBox="0 0 380 590" preserveAspectRatio="xMidYMid meet"><defs>' + defs + '</defs>'
    + top + '<line x1="20" y1="318" x2="360" y2="318" stroke="#e2e8f0" stroke-width="1.5"/>' + bot + '</svg>';
}

function _seqInit(side) {
  var C = SEQ_COR;
  side.innerHTML = '<p class="pres-side-h">Sequência positiva e negativa</p><div id="sq-svg"></div>'
    + '<div class="fs-leg"><span style="color:' + C.pos + '">&#9644; positiva</span>'
    + '<span style="color:' + C.neg + '">&#9644; negativa</span>'
    + '<span style="color:' + C.v + '">&#9644; tensão</span></div>'
    + '<p class="sq-nota">Uma volta da rede, duas voltas da negativa no PLL</p>';
  var step = function(now) { _seqDraw(now); _seqRaf = requestAnimationFrame(step); };
  _seqRaf = requestAnimationFrame(step);
}

function _seqStop() {
  if (_seqRaf) cancelAnimationFrame(_seqRaf);
  _seqRaf = null;
}
