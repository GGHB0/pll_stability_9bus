// ── Capítulo "Código de rede" (kind "ons"): dois painéis na mesma figura.
// Esquerda: tensão da fase mais afundada contra a curva de suportabilidade
// (Figura 2.1, tccInd.lvrt). Direita: i_q contra a rampa (Figura 2.2), com
// anel vermelho nos casos fora da região. st.outros acende os demais
// cenários sem destaque; onsFiltro (mouse num rótulo-resumo) mostra só os
// casos fora ou dentro no painel da esquerda.
var onsFiltro = null;

function _onsCls(k) {
  var l = SCENARIOS[k].tccInd && SCENARIOS[k].tccInd.lvrt;
  return l ? (l.fora ? "fora" : "dentro") : null;
}

function _onsOutros(cap) {
  var mine = _tccCases(cap).map(function(c) { return c.key; });
  return Object.keys(SCENARIOS).filter(function(k) {
    return mine.indexOf(k) === -1 && _onsCls(k);
  });
}

function _onsNome(k) {
  return SCENARIOS[k].label.replace(" — ", " · ") + (SCENARIOS[k].badPll ? " (inadequada)" : "");
}

function _onsFigure(cap, o, layout, visible, mixed, col, grid, fs) {
  var dark = o.dark, st = _tccSt(cap), data = [];
  var T = dark
    ? { ink: "#cbd5e1", mut: "#94a3b8", ok: "#4ade80", bad: "#fca5a5", amb: "#fbbf24", blu: "#93c5fd",
        note: "rgba(15,23,42,0.85)", grey: "rgba(148,163,184,0.35)", redf: "rgba(248,113,113,0.40)" }
    : { ink: "#334155", mut: "#64748b", ok: "#15803d", bad: "#b91c1c", amb: "#a16207", blu: "#1d4ed8",
        note: "rgba(255,255,255,0.85)", grey: "rgba(100,116,139,0.38)", redf: "rgba(220,38,38,0.40)" };
  var big = o.big, lw = big ? 3.5 : 2.5;
  // passo do palco: realce = casos em cena (os outros esmaecem); destaque
  // aponta o ponto de um caso no painel da rampa
  var ps = big ? _presPassoAtual(cap) : null, dest = big ? _capDestaque(cap) : null;
  var esm = function(k) { return !!(ps && ps.realce && ps.realce.indexOf(k) === -1); };
  var ax = function(title, dom, anchor) {
    return { title: { text: title, standoff: 8 }, domain: dom, anchor: anchor, gridcolor: grid,
             zeroline: false, showline: true, linecolor: T.mut, ticks: "outside", tickcolor: T.mut,
             tickfont: { size: fs - 1, color: T.mut } };
  };
  layout.hovermode = "closest";
  layout.separators = ",.";
  layout.margin = { t: big ? 66 : 58, r: 16, b: 58, l: 66 };
  layout.xaxis = ax("Tempo desde o início da falta (s)", [0, 0.45], "y");
  layout.yaxis = ax("Tensão (pu)", [0, 1], "x");
  layout.xaxis2 = ax("Tensão média no inversor (pu)", [0.55, 1], "y2");
  layout.yaxis2 = ax("Corrente reativa i<sub>q</sub> (pu)", [0, 1], "x2");
  var sc0 = visible.length ? SCENARIOS[visible[0].key] : null;
  var dur = (sc0 && sc0.tClear != null) ? sc0.tClear - sc0.tFault : 0.1;
  var lv0 = sc0 && sc0.tccInd.lvrt;
  var tFim = lv0 ? lv0.t[lv0.t.length - 1] : 0.3, XMAX = 0.6;
  layout.xaxis.range = [-0.04, XMAX]; layout.xaxis.dtick = 0.1;
  layout.yaxis.range = [0, 1.3]; layout.yaxis.dtick = 0.2;
  layout.xaxis2.range = [0, 1.0]; layout.xaxis2.dtick = 0.1;
  layout.yaxis2.range = [-0.04, 1.16]; layout.yaxis2.dtick = 0.2;

  function faixa(a, x0, x1, cor, rot, corRot) {
    layout.shapes.push({ type: "rect", xref: "x" + a, yref: "y" + a + " domain", x0: x0, x1: x1, y0: 0, y1: 1,
      fillcolor: cor, line: { width: 0 }, layer: "below" });
    if (rot) layout.annotations.push({ x: (x0 + x1) / 2, y: 1, xref: "x" + a, yref: "y" + a + " domain",
      yanchor: "bottom", yshift: 3, showarrow: false, text: rot, font: { size: fs - 2, color: corRot || T.mut } });
  }
  function nota(a, x, y, txt, cor, extra) {
    var n = { x: x, y: y, xref: "x" + a, yref: "y" + a, text: txt, showarrow: false, bgcolor: T.note, borderpad: 3,
              font: { size: fs - 1, color: cor } };
    for (var k in extra) n[k] = extra[k];
    layout.annotations.push(n);
  }
  function titulo(a, txt, dir) {
    layout.annotations.push({ x: 0, y: 1, xref: "x" + a + " domain", yref: "y" + a + " domain", xanchor: "left",
      yanchor: "bottom", yshift: big ? 26 : 22, showarrow: false, text: txt, font: { size: fs + 2, color: T.ink } });
    if (dir) layout.annotations.push({ x: 1, y: 1, xref: "x" + a + " domain", yref: "y" + a + " domain",
      xanchor: "right", yanchor: "bottom", yshift: big ? 27 : 23, showarrow: false, text: dir,
      font: { size: fs - 2, color: T.mut } });
  }

  // ── Esquerda: região de permanência (ONS Subm. 2.10 §5.7, Figura 13) ──
  var bx = [0, 0.5, 1.0, 2];
  data.push({ type: "scatter", mode: "lines", x: bx.concat([2, 0]), y: [0.2, 0.2, 0.85, 0.85, 1.2, 1.2],
    fill: "toself", fillcolor: "rgba(22,163,74,0.08)", line: { width: 0 }, hoverinfo: "skip" });
  data.push({ type: "scatter", mode: "lines", x: bx.concat([2, 0]), y: [0.2, 0.2, 0.85, 0.85, 0, 0],
    fill: "toself", fillcolor: "rgba(220,38,38,0.07)", line: { width: 0 }, hoverinfo: "skip" });
  data.push({ type: "scatter", mode: "lines", x: bx, y: [0.2, 0.2, 0.85, 0.85],
    line: { color: T.ink, width: 3 }, hoverinfo: "skip" });
  data.push({ type: "scatter", mode: "lines", x: [0, 2], y: [1.2, 1.2],
    line: { color: T.ink, width: 2, dash: "dot" }, hoverinfo: "skip" });
  var outros = (st.outros || onsFiltro) ? _onsOutros(cap) : [];
  outros.forEach(function(k) {
    var l = SCENARIOS[k].tccInd.lvrt, cls = l.fora ? "fora" : "dentro";
    if (onsFiltro && cls !== onsFiltro) return;
    var cor = onsFiltro ? (l.fora ? "rgba(220,38,38,0.75)" : (dark ? "rgba(203,213,225,0.6)" : "rgba(51,65,85,0.6)"))
                        : (l.fora ? T.redf : T.grey);
    data.push({ type: "scatter", mode: "lines", x: l.t, y: l.v, name: _onsNome(k),
      line: { color: cor, width: onsFiltro ? 1.8 : 1.3 },
      hovertemplate: "<b>" + _onsNome(k) + "</b><br>t = %{x:.3f} s · %{y:.2f} pu<br>"
        + (l.fora ? "fora da região" : "dentro da região") + "<extra></extra>" });
  });
  visible.forEach(function(c) {
    var l = SCENARIOS[c.key].tccInd.lvrt;
    if (!l) return;
    var lbl = _tccLabel(c.key, mixed);
    data.push({ type: "scatter", mode: "lines", x: l.t, y: l.v, name: lbl,
      line: { color: col(c), width: lw },
      opacity: ((onsFiltro && _onsCls(c.key) !== onsFiltro) || esm(c.key)) ? 0.15 : 1,
      hovertemplate: "<b>" + lbl + "</b><br>t = %{x:.3f} s · %{y:.2f} pu<br>"
        + (l.fora ? "fora da região" : "dentro da região") + "<extra></extra>" });
  });
  faixa("", 0, dur, dark ? "rgba(226,232,240,0.06)" : "rgba(15,23,42,0.05)", "<b>falta</b>", T.ink);
  faixa("", dur, tFim, "rgba(0,0,0,0)", "pós-falta");
  faixa("", tFim, XMAX, "rgba(148,163,184,0.16)", "além da janela simulada");
  nota("", 0.45, 1.05, "região de permanência obrigatória", T.ok);
  nota("", 0.45, 0.1, "abaixo da borda: desconexão permitida", T.bad);
  nota("", XMAX, 0.5, "a borda sobe até 0,85 pu em 1 s", T.mut, { xanchor: "right" });
  nota("", 0.4, 0.2, "0,2 pu", T.ink, { yanchor: "bottom", yshift: 2 });
  titulo("", "<b>Suportabilidade a subtensões</b>  · Figura 2.1", "tensão da fase mais afundada no inversor");

  // ── Direita: rampa de corrente reativa (§5.8, Figura 14) ──
  data.push({ type: "scatter", mode: "lines", x: [0, 0.5, 0.85, 1.0], y: [1, 1, 0, 0], xaxis: "x2", yaxis: "y2",
    line: { color: T.ink, width: big ? 3.5 : 3 }, hoverinfo: "skip" });
  if (st.outros) outros.forEach(function(k) {
    var r = SCENARIOS[k].tccInd.raw;
    if (!r) return;
    data.push({ type: "scatter", mode: "markers", x: [r.Vmed], y: [r.iqref], xaxis: "x2", yaxis: "y2",
      name: _onsNome(k), marker: { size: big ? 10 : 8, color: _onsCls(k) === "fora" ? T.redf : T.grey },
      hovertemplate: "<b>" + _onsNome(k) + "</b><br>V = %{x:.2f} pu · i<sub>q,ref</sub> = %{y:.2f} pu<extra></extra>" });
  });
  // rótulos fora da rampa: B7 e L7-8 quase no mesmo ponto, um em cima e
  // outro embaixo; B6 fica abaixo da rampa, rótulo à esquerda
  var POS = ["top center", "bottom center", "bottom left", "bottom left"];
  visible.forEach(function(c, i) {
    var r = SCENARIOS[c.key].tccInd.raw;
    if (!r) return;
    var lbl = _tccLabel(c.key, mixed), fora = _onsCls(c.key) === "fora";
    // esmaecido no passo com realce: sem rótulo, para a seta do destaque não cruzá-lo
    data.push({ type: "scatter", mode: esm(c.key) ? "markers" : "markers+text", name: lbl, xaxis: "x2", yaxis: "y2",
      x: [r.Vmed], y: [r.iqref], text: ["<b>" + SCENARIOS[c.key].label.replace(" — Trifásica", "") + "</b>"],
      textposition: POS[i] || "top center", textfont: { size: fs + 1, color: col(c) },
      opacity: esm(c.key) ? 0.2 : 1,
      marker: { size: big ? 20 : 15, color: col(c),
                line: { width: fora ? 4 : 2, color: fora ? "#dc2626" : (o.bg || layout.paper_bgcolor) } },
      hovertemplate: "<b>" + lbl + "</b><br>tensão no inversor: %{x:.2f} pu"
        + "<br>i<sub>q,ref</sub> médio: %{y:.2f} pu<br>rampa prevê: " + r.rampa.toFixed(2)
        + " pu<br>" + (fora ? "fora da região" : "dentro da região") + "<extra></extra>" });
  });
  faixa("2", 0, 0.5, "rgba(234,179,8,0.10)", "<b>corrente máxima</b>", T.amb);
  faixa("2", 0.5, 0.85, "rgba(37,99,235,0.07)", "<b>proporcional ao afundamento</b>", T.blu);
  faixa("2", 0.85, 1.0, "rgba(148,163,184,0.16)", "<b>banda morta</b>", T.ink);
  if (!dest) nota("2", 0.25, 0.55, "abaixo de 0,5 pu,<br>i<sub>q</sub> = 1 pu", T.amb);
  var rd = dest && dest.key && SCENARIOS[dest.key] && SCENARIOS[dest.key].tccInd.raw;
  if (rd) layout.annotations.push({ xref: "x2", yref: "y2", x: rd.Vmed, y: rd.iqref,
    axref: "x2", ayref: "y2", ax: 0.17, ay: 0.72, showarrow: true, arrowhead: 2, arrowwidth: 2.5,
    arrowcolor: "#b91c1c", standoff: 14, align: "left", xanchor: "left", yanchor: "middle",
    text: "<b style='font-size:46px'>" + dest.num + "</b><br><span style='font-size:16px'>" + dest.txt + "</span>",
    font: { color: "#b91c1c", size: 16 }, bgcolor: "rgba(255,255,255,.92)", bordercolor: "#fecaca",
    borderwidth: 1.5, borderpad: 10 });
  nota("2", 0.64, 0.36, "i<sub>q</sub> = (0,85 − V) / 0,35", T.blu, { xanchor: "right" });
  nota("2", 0.925, 0.55, "sem injeção<br>adicional", T.ink);
  titulo("2", "<b>Corrente reativa contra a rampa</b>  · Figura 2.2",
         "<span style=\"color:#dc2626\">◯</span> fora da região de suportabilidade");
  return { data: data, layout: layout };
}

// rótulos-resumo e botão dos outros curtos, ao lado dos chips
function _onsCtrlHtml(cap) {
  var st = _tccSt(cap);
  var todos = _tccCases(cap).map(function(c) { return c.key; }).filter(_onsCls).concat(_onsOutros(cap));
  var html = ["fora", "dentro"].map(function(cls) {
    var ks = todos.filter(function(k) { return _onsCls(k) === cls; });
    var mine = _tccCases(cap).map(function(c) { return c.key; });
    var lista = ks.map(function(k) {
      return "<div" + (mine.indexOf(k) >= 0 ? " class=\"mine\"" : "") + ">" + _onsNome(k) + "</div>";
    }).join("");
    return "<span class=\"ons-sum " + cls + "\" onmouseenter=\"_onsFiltrar('" + cls + "')\""
      + " onmouseleave=\"_onsFiltrar(null)\">" + (cls === "fora" ? "Fora da região" : "Dentro da região")
      + " · " + ks.length + " casos<span class=\"ons-pop\"><b>"
      + (cls === "fora" ? "A fase mais afundada cai abaixo de 0,2 pu" : "Acima da borda em toda a janela simulada")
      + "</b>" + lista + "</span></span>";
  }).join("");
  return "<span class=\"ons-ctrl\">" + html + "<button class=\"ons-outros" + (st.outros ? " on" : "")
    + "\" onclick=\"_onsToggleOutros()\">" + (st.outros ? "Ocultar os outros curtos" : "+ Mostrar os outros curtos")
    + "</button></span>";
}

function _onsBadge(k, curto) {
  var cls = _onsCls(k);
  return cls ? "<span class=\"ons-badge " + cls + "\">" + (cls === "fora" && !curto ? "fora da região" : cls)
    + "</span>" : "";
}

function _onsToggleOutros() {
  var st = _tccSt(CAPS[tccCap]);
  st.outros = !st.outros;
  _tccRefresh();
}

// só redesenha a figura: refazer os chips trocaria o elemento sob o mouse
function _onsFiltrar(cls) {
  onsFiltro = cls;
  var cap = CAPS[tccCap], el = presOn ? document.getElementById("pres-plot") : gd.tcc;
  if (!el || !el.layout) return;
  var fig = _tccFigure(cap, [], presOn
    ? { dark: false, height: el.layout.height, big: true, bg: "#ffffff" }
    : { dark: isDark, height: el.layout.height });
  Plotly.react(el, fig.data, fig.layout, presOn ? PRES_CFG : PLOTLY_CFG);
}

