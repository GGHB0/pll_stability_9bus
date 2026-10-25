// ── Fasor (cap.lado "fasor", Perda de sincronismo): ângulo do PLL de cada
// caso contra a rede, num círculo ao lado do gráfico. O instante segue o
// mouse no gráfico; o play percorre a janela do capítulo em câmera lenta
// (20 s; 8 s ficou rápido demais na defesa, pedido de 2026-10-24).
// Os ângulos vêm dos traços do erro de fase já desenhados (gd._fullData).
var fasorT = null, _fasorRaf = null, FASOR_MS = 20000;

function _fasorSeries(gd) {
  return gd._fullData.filter(function(d) { return d.yaxis === "y" && d.mode === "lines"; })
    .map(function(d) { return { x: d.x, y: d.y, cor: d.line.color }; });
}

function _fasorVal(x, y, t) {
  var lo = 0, hi = x.length - 1;
  while (hi - lo > 1) { var m = (lo + hi) >> 1; if (x[m] < t) lo = m; else hi = m; }
  return y[hi];
}

function _fasorDraw(t) {
  var gd = document.getElementById("pres-plot"), box = document.getElementById("fs-svg");
  if (!box || !gd._fullData) return;
  var cap = CAPS[tccCap], R = 150, c = 190;
  t = Math.max(cap.xrange[0], Math.min(cap.xrange[1], t));
  fasorT = t;
  var pt = function(deg, r) {
    var a = (-90 - deg) * Math.PI / 180;
    return [c + r * Math.cos(a), c + r * Math.sin(a)];
  };
  var w0 = pt(-2, R), w1 = pt(2, R), defs = "", vecs = "";
  _fasorSeries(gd).forEach(function(s, i) {
    var e = pt(_fasorVal(s.x, s.y, t), R);
    defs += '<marker id="fs-ah' + i + '" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5"'
      + ' markerHeight="5" orient="auto"><path d="M0,0L10,5L0,10z" fill="' + s.cor + '"/></marker>';
    vecs += '<line x1="' + c + '" y1="' + c + '" x2="' + e[0] + '" y2="' + e[1] + '" stroke="' + s.cor
      + '" stroke-width="5" stroke-linecap="round" marker-end="url(#fs-ah' + i + ')"/>';
  });
  box.innerHTML = '<svg viewBox="0 -20 380 400"><defs>' + defs + '</defs>'
    + '<circle cx="' + c + '" cy="' + c + '" r="' + R + '" fill="none" stroke="#cbd5e1" stroke-width="2"/>'
    + '<path d="M' + c + ',' + c + ' L' + w0[0] + ',' + w0[1] + ' A' + R + ',' + R + ' 0 0 1 ' + w1[0] + ',' + w1[1]
    + ' Z" fill="rgba(22,163,74,.35)"/>'
    + '<path d="M' + (c - 11) + ',' + (c - R - 24) + ' L' + (c + 11) + ',' + (c - R - 24) + ' L' + c + ',' + (c - R - 4)
    + ' Z" fill="#0f172a"/><text x="' + c + '" y="' + (c - R - 30) + '" text-anchor="middle"'
    + ' font-size="15" font-weight="700" fill="#0f172a">rede</text>'
    + vecs + '<circle cx="' + c + '" cy="' + c + '" r="5" fill="#0f172a"/></svg>';
  var sc = _tccVisible(cap).map(function(v) { return SCENARIOS[v.key]; })
    .filter(function(x) { return x.tFault != null; })[0];
  var falta = sc && t >= sc.tFault && t < (sc.tClear != null ? sc.tClear : sc.tFault);
  document.getElementById("fs-t").innerHTML = "t = " + t.toFixed(3).replace(".", ",") + " s";
  document.getElementById("fs-falta").style.visibility = falta ? "visible" : "hidden";
  var fl = gd._fullLayout, cur = document.getElementById("fs-cursor");
  cur.style.left = (gd.offsetLeft + fl._size.l + fl.xaxis.l2p(t)) + "px";
  cur.style.top = (gd.offsetTop + fl._size.t) + "px";
  cur.style.height = fl._size.h + "px";
  cur.style.display = "";
}

function _fasorInit(gd, cap) {
  var side = document.getElementById("pres-side");
  // nominal × inadequada: legenda pela sintonia; só nominais (Localização):
  // pelo rótulo do ponto no mapa (B7, L7-8...)
  var mixed = _tccMixed(cap), rot = {};
  CAPS.forEach(function(c) {
    (c.kind === "mapa" ? c.passos : []).forEach(function(q) { if (q.cenario) rot[q.cenario] = q.rotulo; });
  });
  var leg = _tccVisible(cap).map(function(v) {
    var nome = mixed ? "PLL " + (SCENARIOS[v.key].badPll ? "inadequada" : "nominal")
                     : (rot[v.key] || SCENARIOS[v.key].label);
    return '<span style="color:' + v.light + '">&#9644; ' + nome + '</span>';
  }).join("") + "<span>&#9660; rede</span>";
  side.innerHTML = '<p class="pres-side-h">Ângulo do PLL contra a rede</p><div id="fs-svg"></div>'
    + '<div class="fs-leg">' + leg + '</div>'
    + '<div class="fs-ctl"><button class="fs-play" id="fs-play" onclick="_fasorPlay()">&#9654; play</button>'
    + '<span class="fs-t" id="fs-t"></span><span class="fs-falta" id="fs-falta">falta</span></div>'
    + (_capDestaque(cap) && cap.destaque.lado
       ? '<div class="fs-dest"><b>' + cap.destaque.num + '</b><span>' + cap.destaque.txt + '</span></div>' : '');
  if (gd.removeAllListeners) gd.removeAllListeners("plotly_hover");
  gd.on("plotly_hover", function(e) { if (!_fasorRaf && e.points.length) _fasorDraw(e.points[0].x); });
  if (fasorT === null || fasorT < cap.xrange[0] || fasorT > cap.xrange[1]) fasorT = cap.xrange[0];
  _fasorDraw(fasorT);
}

function _fasorPlay() {
  if (_fasorRaf) { _fasorStop(); return; }
  var cap = CAPS[tccCap], x0 = cap.xrange[0], x1 = cap.xrange[1];
  // o play sempre recomeça do início da janela do capítulo
  var t0 = x0, start = performance.now();
  document.getElementById("fs-play").innerHTML = "&#10074;&#10074; pausa";
  var step = function(now) {
    var t = t0 + (now - start) / FASOR_MS * (x1 - x0);
    if (t >= x1) { _fasorDraw(x1); _fasorStop(); return; }
    _fasorDraw(t);
    _fasorRaf = requestAnimationFrame(step);
  };
  _fasorRaf = requestAnimationFrame(step);
}

function _fasorStop() {
  if (_fasorRaf) cancelAnimationFrame(_fasorRaf);
  _fasorRaf = null;
  var b = document.getElementById("fs-play");
  if (b) b.innerHTML = "&#9654; play";
}

