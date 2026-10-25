// ── Aba Análise TCC e modo apresentação: capítulos do Cap. 5 ──────────────
// Os dois usam _tccFigure: a aba mostra um sinal por vez (seletor), a
// apresentação empilha os sinais de cap.pres em tela cheia, em palco branco.

var TCC_EXTRA = [["#9333ea", "#c084fc"], ["#db2777", "#f472b6"],
                 ["#ca8a04", "#fbbf24"], ["#16a34a", "#4ade80"]];
var SINAIS = {
  err:  { lbl: "Erro de fase", trace: "Erro de fase", y: "Erro de fase (°)", u: "°" },
  vd:   { lbl: "v<sub>d</sub> da rede", trace: "V<sub>d</sub> Rede", y: "v<sub>d</sub> (pu)", u: " pu" },
  P:    { lbl: "Potência ativa P", trace: "P UFV", y: "P (pu)", u: " pu" },
  Q:    { lbl: "Potência reativa Q", trace: "Q UFV", y: "Q (pu)", u: " pu" },
  spec: { lbl: "Espectro de v<sub>d</sub> na falta", y: "Amplitude (pu)", u: " pu" },
};
var IND_LBL = {
  terr2: "Erro na faixa de 2°", tvd5: "v<sub>d</sub> na faixa de 5%",
  ret: "Retenção de v<sub>d</sub>", pico: "Pico do erro na falta",
  ts: "Retorno à faixa de 2°", a120: "120 Hz em v<sub>d</sub>",
  fracP: "P absorvida após a eliminação", Vmed: "Tensão no inversor",
  rampa: "Rampa ONS prevê", iqref: "i<sub>q,ref</sub> médio",
};
var tccCap = 0, tccState = {}, presOn = false;

function _tccSt(cap) {
  if (!tccState[cap.id]) {
    var on = {};
    cap.casos.forEach(function(c) { on[c[0]] = true; });
    tccState[cap.id] = { on: on, extra: [], sinal: cap.sinais[0] || null };
  }
  return tccState[cap.id];
}

function _tccCases(cap) {
  var st = _tccSt(cap);
  var list = cap.casos.filter(function(c) { return SCENARIOS[c[0]]; })
    .map(function(c) { return { key: c[0], light: c[1][0], dark: c[1][1] }; });
  st.extra.forEach(function(k, i) {
    var pal = TCC_EXTRA[i % TCC_EXTRA.length];
    list.push({ key: k, light: pal[0], dark: pal[1], extra: true });
  });
  return list;
}

function _tccVisible(cap) {
  var st = _tccSt(cap);
  return _tccCases(cap).filter(function(c) { return st.on[c.key] !== false; });
}

function _tccMixed(cap) {
  var cs = _tccCases(cap);
  return cs.some(function(c) { return SCENARIOS[c.key].badPll; })
      && cs.some(function(c) { return !SCENARIOS[c.key].badPll; });
}

function _tccLabel(k, mixed) {
  var sc = SCENARIOS[k];
  if (sc.badPll) return sc.label + " · inadequada";
  return mixed ? sc.label + " · nominal" : sc.label;
}

function _tccTrace(sc, sinal) {
  if (sinal === "spec") {
    var f = sc.specData && sc.specData.d;
    if (!f) return null;
    // 2ª linha da figura dq = tensão v_d do inversor; segmento da falta
    for (var i = 0; i < f.data.length; i++) {
      if (f.data[i].name === "Durante a falta" && f.data[i].yaxis === "y2") return f.data[i];
    }
    return null;
  }
  var d = sc.invData.data;
  for (var j = 0; j < d.length; j++) {
    if (d[j].name === SINAIS[sinal].trace) return d[j];
  }
  return null;
}

// Figura de um capítulo. sinais = um painel por sinal, empilhados com o mesmo
// eixo x (zoom junto). o = { dark, height, big, bg }.
function _tccFigure(cap, sinais, o) {
  var dark = o.dark, B = dark ? BASE_DARK : BASE_LIGHT;
  var bg = o.bg || B.paper, grid = dark ? "#2a3a55" : "#e2e8f0";
  var fs = o.big ? 15 : 12, mixed = _tccMixed(cap), visible = _tccVisible(cap);
  var col = function(c) { return dark ? c.dark : c.light; };
  var layout = {
    height: o.height, margin: { t: o.big ? 30 : 26, r: 24, b: 58, l: 80 },
    paper_bgcolor: bg, plot_bgcolor: o.bg || B.plot, showlegend: false,
    font: { family: "Inter, Segoe UI, system-ui, sans-serif", color: B.font, size: fs },
    hoverlabel: { bgcolor: dark ? "#0f172a" : "#ffffff", bordercolor: dark ? "#60a5fa" : "#2563eb",
                  font: { size: fs + 1, color: B.font }, align: "left" },
    hovermode: "x unified", shapes: [], annotations: [],
  };
  var data = [];

  if (cap.kind === "ons") return _onsFigure(cap, o, layout, visible, mixed, col, grid, fs);

  var n = sinais.length, gap = n > 1 ? 0.09 : 0, h = (1 - gap * (n - 1)) / n;
  var spec = sinais[0] === "spec";
  sinais.forEach(function(sinal, i) {
    var ax = (i === 0) ? "" : String(i + 1);
    var y1 = 1 - i * (h + gap), y0 = y1 - h;
    var S = SINAIS[sinal];
    layout["yaxis" + ax] = { domain: [y0, y1], anchor: "x", gridcolor: grid, zerolinecolor: grid,
      title: { text: S.y }, hoverformat: ".3f" };
    visible.forEach(function(c) {
      var t = _tccTrace(SCENARIOS[c.key], sinal);
      if (!t) return;
      var lbl = _tccLabel(c.key, mixed);
      data.push({ type: "scatter", mode: "lines", x: t.x, y: t.y, name: lbl,
        xaxis: "x", yaxis: "y" + ax,
        line: { color: col(c), width: o.big ? 2.6 : 2.2, dash: c.extra ? "dot" : "solid" },
        hovertemplate: lbl + ": <b>%{y:.3f}" + S.u + "</b><extra></extra>" });
    });
    if (n > 1) {
      layout.annotations.push({ xref: "paper", yref: "paper", x: 0, y: y1, xanchor: "left",
        yanchor: "bottom", showarrow: false, text: "<b>" + S.lbl + "</b>",
        font: { size: fs, color: dark ? "#93c5fd" : "#1d4ed8" } });
    }
    if (sinal === "err") {
      layout.shapes.push({ type: "rect", xref: "paper", yref: "y" + ax, layer: "below",
        x0: 0, x1: 1, y0: -2, y1: 2, line: { width: 0 },
        fillcolor: dark ? "rgba(74,222,128,.18)" : "rgba(22,163,74,.14)" });
      if (cap.id === "sinc") {   // escorregamento de ciclo: faixa inteira de ±180°
        layout["yaxis" + ax].range = [-190, 190];
        layout["yaxis" + ax].tickvals = [-180, -90, 0, 90, 180];
        layout["yaxis" + ax].ticktext = ["−180", "−90", "0", "90", "180"];
      }
    }
    if (cap.id === "energ") _marcaPartida(layout, data, visible, sinal, ax, [y0, y1], col, fs, dark);
    if (sinal === "err" && cap.faixa_err) {
      var fe = cap.faixa_err, st4 = (fe[1] - fe[0]) / 4;
      layout["yaxis" + ax].range = fe;
      layout["yaxis" + ax].tickvals = [0, 1, 2, 3, 4].map(function(k) { return fe[0] + k * st4; });
      layout["yaxis" + ax].ticktext = layout["yaxis" + ax].tickvals.map(function(v) { return String(v).replace("-", "−"); });
    }
    if (sinal === "err" && cap.metricas.indexOf("ts") !== -1) _marcaRetorno(layout, data, visible, ax, [y0, y1], col, fs, dark);
    if (sinal === "spec") {
      layout["yaxis" + ax].range = [0, 1];
      layout.shapes.push({ type: "line", xref: "x", yref: "paper", x0: 120, x1: 120, y0: y0, y1: y1,
        line: { color: B.font, width: 1, dash: "dash" }, opacity: 0.45 });
      layout.annotations.push({ xref: "x", yref: "paper", x: 120, y: y1, yanchor: "bottom",
        text: "120 Hz", showarrow: false, font: { size: fs - 1 } });
    }
  });
  if (o.big && cap.destaque && !cap.destaque.lado) _destaque(cap.destaque, sinais, layout);
  layout.xaxis = { anchor: "y" + (n > 1 ? String(n) : ""), gridcolor: grid, zerolinecolor: grid,
    title: { text: spec ? "Frequência (Hz)" : "Tempo (s)" },
    hoverformat: spec ? ".0f" : ".4f" };
  if (cap.xrange) layout.xaxis.range = cap.xrange;
  if (!spec) {
    var f0 = visible.map(function(c) { return SCENARIOS[c.key]; })
      .filter(function(sc) { return sc.tFault != null; })[0];
    if (f0) {
      var tc = (f0.tClear != null) ? f0.tClear : f0.tFault;
      layout.shapes.push({ type: "rect", xref: "x", yref: "paper", layer: "below",
        x0: f0.tFault, x1: tc, y0: 0, y1: 1, line: { width: 0 },
        fillcolor: dark ? "rgba(248,113,113,.10)" : "rgba(220,38,38,.06)" });
      layout.annotations.push({ xref: "x", yref: "paper", x: (f0.tFault + tc) / 2, y: 1,
        yanchor: "bottom", text: "falta", showarrow: false,
        font: { size: fs - 1, color: dark ? "#fca5a5" : "#b91c1c" } });
    }
  }
  return { data: data, layout: layout };
}

// Número grande sobre o gráfico (cap.destaque, só no palco). Com x/y, seta
// da caixa (ax/ay) até o alvo; sem x, a caixa fica solta em ax/ay.
function _destaque(D, sinais, layout) {
  var i = sinais.indexOf(D.sinal);
  if (i === -1) return;
  var yr = "y" + (i === 0 ? "" : String(i + 1)), red = "#b91c1c";
  var a = { xref: "x", yref: yr, align: "left", xanchor: "left", yanchor: "middle",
    text: "<b style='font-size:46px'>" + D.num + "</b><br><span style='font-size:16px'>" + D.txt + "</span>",
    font: { color: red, size: 16 }, bgcolor: "rgba(255,255,255,.92)", bordercolor: "#fecaca",
    borderwidth: 1.5, borderpad: 10 };
  if (D.x != null) {
    a.x = D.x; a.y = D.y; a.ax = D.ax; a.ay = D.ay; a.axref = "x"; a.ayref = yr;
    a.showarrow = true; a.arrowhead = 2; a.arrowwidth = 2.5; a.arrowcolor = red;
  } else {
    a.x = D.ax; a.y = D.ay; a.showarrow = false;
  }
  layout.annotations.push(a);
}

// Capítulos com falta (métrica "ts"): onde o erro volta de vez à faixa de 2°
// depois da eliminação. Tracejado e ponto no instante do retorno, e seta da
// eliminação até ele com o tempo do cartão, porque o retorno é contado de
// t_clear. Casos que não retornam ficam sem marca. Valores de tccInd.retorno.
function _marcaRetorno(layout, data, visible, ax, dom, col, fs, dark) {
  var row = 0, yref = "y" + ax;
  visible.forEach(function(c) {
    var r = SCENARIOS[c.key].tccInd && SCENARIOS[c.key].tccInd.retorno;
    if (!r) return;
    var cor = col(c), ya = dom[1] - (0.06 + row * 0.07) * (dom[1] - dom[0]);
    row++;
    layout.shapes.push({ type: "line", xref: "x", yref: "paper", x0: r.t, x1: r.t, y0: dom[0], y1: dom[1],
      line: { color: cor, width: 1.4, dash: "dash" } });
    layout.annotations.push({ xref: "x", yref: "paper", x: r.t, y: ya, ax: r.t0, ay: ya,
      axref: "x", ayref: "paper", text: "", showarrow: true, arrowhead: 2, arrowside: "end+start",
      arrowsize: 0.8, arrowwidth: 1.6, arrowcolor: cor });
    layout.annotations.push({ xref: "x", yref: "paper", x: r.t, y: ya, xanchor: "left", yanchor: "middle",
      xshift: 6, showarrow: false, text: "<b>" + Math.round(r.ms) + " ms</b>",
      font: { size: fs, color: cor }, bgcolor: dark ? "rgba(15,23,42,.85)" : "rgba(255,255,255,.9)" });
    data.push({ type: "scatter", mode: "markers", x: [r.t], y: [r.err], xaxis: "x", yaxis: yref,
      marker: { size: fs - 2, color: dark ? "#0f172a" : "#ffffff", line: { color: cor, width: 3 } },
      hoverinfo: "skip", showlegend: false });
  });
}

// Capítulo "Energização": marca onde cada curva entra de vez na faixa (erro
// em 2°, v_d em 5% do valor final). Linha tracejada na cor do caso com o
// tempo no topo e ponto na curva; o eixo do erro fica em ±20° para a faixa de
// 2° aparecer (o pico da partida sai do quadro). Valores de tccInd.partida.
function _marcaPartida(layout, data, visible, sinal, ax, dom, col, fs, dark) {
  if (sinal !== "err" && sinal !== "vd") return;
  var verde = dark ? "#4ade80" : "#15803d", yref = "y" + ax;
  var tKey = sinal === "err" ? "terr2" : "tvd5";
  if (sinal === "err") {
    layout["yaxis" + ax].range = [-20, 20];
    layout["yaxis" + ax].tickvals = [-20, -10, 0, 10, 20];
    layout["yaxis" + ax].ticktext = ["−20", "−10", "0", "10", "20"];
  }
  var fin = null;
  visible.forEach(function(c, j) {
    var p = SCENARIOS[c.key].tccInd && SCENARIOS[c.key].tccInd.partida;
    if (!p) return;
    if (fin === null) fin = p.vdfin;
    if (sinal === "vd") {   // faixa de cada caso, em volta do próprio valor final
      layout.shapes.push({ type: "rect", xref: "paper", yref: yref, layer: "below", x0: 0, x1: 1,
        y0: p.vdfin * 0.95, y1: p.vdfin * 1.05, line: { width: 0 },
        fillcolor: dark ? "rgba(74,222,128,.12)" : "rgba(22,163,74,.09)" });
    }
    var x = p[tKey], y = sinal === "err" ? p.err : p.vd, cor = col(c);
    layout.shapes.push({ type: "line", xref: "x", yref: "paper", x0: x, x1: x, y0: dom[0], y1: dom[1],
      line: { color: cor, width: 1.6, dash: "dash" } });
    layout.annotations.push({ xref: "x", yref: "paper", x: x, y: dom[1] - j * 0.045, xshift: 6,
      xanchor: "left", yanchor: "top", showarrow: false, text: "<b>" + Math.round(x * 1000) + " ms</b>",
      font: { size: fs + 1, color: cor }, bgcolor: dark ? "rgba(15,23,42,.85)" : "rgba(255,255,255,.9)" });
    data.push({ type: "scatter", mode: "markers", x: [x], y: [y], xaxis: "x", yaxis: yref,
      marker: { size: fs, color: dark ? "#0f172a" : "#ffffff", line: { color: cor, width: 3.5 } },
      hoverinfo: "skip", showlegend: false });
  });
  var yl = sinal === "err" ? 2 : (fin === null ? null : fin * 1.05);
  if (yl !== null) {
    layout.annotations.push({ xref: "paper", yref: yref, x: 1, y: yl, xanchor: "right",
      yanchor: "bottom", showarrow: false, text: sinal === "err" ? "faixa de ±2°" : "faixa de ±5%",
      font: { size: fs - 2, color: verde } });
  }
}

