// ── Modo apresentação: o site inteiro vira um palco branco em tela cheia ──

var PRES_CFG = { responsive: true, displaylogo: false, displayModeBar: false };

function presToggle() {
  presOn = !presOn;
  var el = document.getElementById("pres");
  el.style.display = presOn ? "" : "none";
  document.body.classList.toggle("pres-on", presOn);
  if (presOn) {
    presPasso = 0;
    var fs = document.documentElement.requestFullscreen;
    if (fs) {
      try {
        var pr = document.documentElement.requestFullscreen();
        if (pr && pr.catch) pr.catch(function() {});
      } catch (e) {}
    }
    _renderPres();
  } else {
    _fasorStop();
    _presPassoReset();
    if (document.fullscreenElement && document.exitFullscreen) {
      try { document.exitFullscreen(); } catch (e) {}
    }
    if (activeTab === "tcc") _renderTcc();
  }
}

function presGo(i, back) {
  if (i < 0 || i >= CAPS.length) return;
  _mapaEnter(i, back);
  if (i !== tccCap) {
    presPasso = (back && CAPS[i].passos_pres) ? CAPS[i].passos_pres.length - 1 : 0;
    fasorT = null;
  }
  tccCap = i;
  _renderPres();
}

function _renderPres() {
  var cap = CAPS[tccCap];
  document.getElementById("pres-count").innerHTML = (tccCap + 1) + "<span>/" + CAPS.length + "</span>";
  document.getElementById("pres-ref").textContent = cap.ref;
  document.getElementById("pres-title").textContent = cap.titulo;
  var pp = cap.passos_pres, ps = pp ? pp[Math.min(presPasso, pp.length - 1)] : null;
  if (ps) {
    var st = _tccSt(cap);
    pp.forEach(function(q) { q.ocultar.forEach(function(k) { st.on[k] = true; }); });
    ps.ocultar.forEach(function(k) { st.on[k] = false; });
  }
  document.getElementById("pres-text").innerHTML = ps ? "<span class=\"pres-msg\">" + ps.texto + "</span>" : cap.texto;
  document.getElementById("pres-passo").innerHTML = ps
    ? _passoInd(presPasso, pp.length) : "";
  document.getElementById("pres-chips").innerHTML = _tccChipsHtml(cap, false, false);
  document.getElementById("pres-dots").innerHTML = CAPS.map(function(c, i) {
    return "<button class=\"pres-dot" + (i === tccCap ? " active" : "") + "\" onclick=\"presGo("
      + i + ")\" title=\"" + c.curto + "\">" + (i + 1) + " · " + c.curto + "</button>";
  }).join("");
  var plotEl = document.getElementById("pres-plot");
  var tbl = document.getElementById("pres-table");
  var cardsEl = document.getElementById("pres-cards");
  var mapaEl = document.getElementById("pres-mapa");
  var bodyEl = document.getElementById("pres-body"), sideEl = document.getElementById("pres-side");
  _fasorStop();
  document.getElementById("fs-cursor").style.display = "none";
  sideEl.style.display = "none"; sideEl.innerHTML = ""; sideEl.className = "pres-side";
  if (cap.kind === "mapa") {
    Plotly.purge(plotEl);
    bodyEl.style.display = "none"; cardsEl.innerHTML = "";
    tbl.style.display = "none"; tbl.innerHTML = "";
    mapaEl.style.display = ""; mapaEl.innerHTML = _mapaHtml(cap, "pres");
    return;
  }
  mapaEl.style.display = "none"; mapaEl.innerHTML = "";
  if (cap.kind === "tabela") {
    Plotly.purge(plotEl);
    bodyEl.style.display = "none"; cardsEl.innerHTML = "";
    tbl.style.display = ""; tbl.innerHTML = _tccTableHtml();
    return;
  }
  tbl.style.display = "none"; tbl.innerHTML = "";
  bodyEl.style.display = "";
  var lado = _presLado();
  if (lado) { sideEl.className = "pres-side " + lado; sideEl.style.display = ""; }
  cardsEl.innerHTML = _tccCardsHtml(cap, false);
  var h = Math.max(260, plotEl.clientHeight);
  var fig = _tccFigure(cap, cap.pres, { dark: false, height: h, big: true, bg: "#ffffff" });
  // largura explícita: o react guarda a do capítulo anterior (com ou sem painel ao lado)
  fig.layout.width = plotEl.clientWidth;
  Plotly.react(plotEl, fig.data, fig.layout, PRES_CFG);
  if (lado === "fasor") _fasorInit(plotEl, cap);
  else if (lado === "minimapa") _miniMapa(cap, sideEl);
}

// painel ao lado do passo atual: o lado do passo, se houver, senão o do capítulo
function _presLado() {
  var cap = CAPS[tccCap], pp = cap.passos_pres;
  var ps = pp ? pp[Math.min(presPasso, pp.length - 1)] : null;
  return (ps && ps.lado) || cap.lado;
}

