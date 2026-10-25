function tccStep(d) { if (!_mapaStep(d)) tccGo(tccCap + d, d < 0); }
function presStep(d) { if (!_mapaStep(d) && !_presPassoStep(d)) presGo(tccCap + d, d < 0); }

// Passos do palco (cap.passos_pres): cada um troca a legenda por uma frase e
// esconde casos. presPasso vale para o capítulo atual do palco.
var presPasso = 0;
function _presPassoStep(d) {
  var pp = CAPS[tccCap].passos_pres, n = presPasso + d;
  if (!presOn || !pp || n < 0 || n >= pp.length) return false;
  presPasso = n;
  _renderPres();
  return true;
}

// indicador de passo: barra em segmentos que enche até o atual, "k de n" embaixo
function _passoInd(k, n) {
  var seg = "";
  for (var i = 0; i < n; i++) seg += "<i" + (i <= k ? " class=\"on\"" : "") + "></i>";
  return "<span class=\"passo-ind\"><span class=\"passo-seg\">" + seg + "</span>"
    + "<span class=\"passo-n\"><b>" + (k + 1) + "</b> de " + n + "</span></span>";
}

// passo atual do palco (null fora do palco ou em capítulo sem passos)
function _presPassoAtual(cap) {
  var pp = cap.passos_pres;
  return (presOn && pp) ? pp[Math.min(presPasso, pp.length - 1)] : null;
}

// número de destaque: em capítulo com passos, só nos passos com destaque
function _capDestaque(cap) {
  var ps = _presPassoAtual(cap);
  return (ps && !ps.destaque) ? null : cap.destaque;
}

// ao sair do palco, a aba volta a mostrar todos os casos dos capítulos com passos
function _presPassoReset() {
  CAPS.forEach(function(c) {
    if (!c.passos_pres || !tccState[c.id]) return;
    c.passos_pres.forEach(function(ps) { ps.ocultar.forEach(function(k) { tccState[c.id].on[k] = true; }); });
    if (c.kind === "ons") tccState[c.id].outros = false;
  });
}

function _tccRefresh() { if (presOn) _renderPres(); else _renderTcc(); }

function _tccSinal(s) { _tccSt(CAPS[tccCap]).sinal = s; _tccRefresh(); }

function _tccChip(k) {
  var st = _tccSt(CAPS[tccCap]);
  st.on[k] = (st.on[k] === false);
  _tccRefresh();
}

function _tccAdd(sel) {
  var k = sel.value;
  if (!k) return;
  var st = _tccSt(CAPS[tccCap]);
  if (st.extra.indexOf(k) === -1) st.extra.push(k);
  st.on[k] = true;
  _tccRefresh();
}

function _scrollToTabs() {
  setTimeout(function() {
    var sticky = document.querySelector(".header").offsetHeight
               + document.querySelector(".filter-bar").offsetHeight;
    var y = document.getElementById("tab-bar").getBoundingClientRect().top
          + window.scrollY - sticky - 8;
    document.scrollingElement.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
  }, 60);
}

function tccGo(i, back) {
  if (i < 0 || i >= CAPS.length) return;
  _mapaEnter(i, back);
  tccCap = i;
  if (activeTab !== "tcc") switchTab("tcc"); else _renderTcc();
  _scrollToTabs();
}

function _openScenario(k) {
  if (presOn) presToggle();
  _applyPllFilter(SCENARIOS[k].badPll ? "bad" : "nominal");
  activeTab = "inv";
  document.getElementById("scenario-picker").value = k;
  switchScenario(k);
  _scrollToTabs();
}

function _renderTcc() {
  var cap = CAPS[tccCap], st = _tccSt(cap);
  document.querySelectorAll(".tcc-pill").forEach(function(b, i) {
    b.classList.toggle("active", i === tccCap);
  });
  document.getElementById("tcc-ref").textContent = cap.ref;
  document.getElementById("tcc-title").textContent = cap.titulo;
  document.getElementById("tcc-text").innerHTML = cap.texto;   // texto nosso, com <sub>
  var sb = document.getElementById("tcc-sinais");
  sb.style.display = (cap.sinais.length > 1) ? "" : "none";
  sb.innerHTML = cap.sinais.map(function(s) {
    return "<button class=\"pll-btn" + (s === st.sinal ? " active" : "") + "\" onclick=\"_tccSinal('"
      + s + "')\">" + SINAIS[s].lbl + "</button>";
  }).join("");
  document.getElementById("tcc-chips").innerHTML = _tccChipsHtml(cap, isDark, true);

  var plotEl = gd.tcc, tbl = document.getElementById("tcc-table");
  var cardsEl = document.getElementById("tcc-cards");
  var mapaEl = document.getElementById("tcc-mapa");
  mapaEl.innerHTML = (cap.kind === "mapa") ? _mapaHtml(cap, "tcc") : "";
  if (cap.kind === "mapa") {
    plotEl.style.display = "none"; tbl.innerHTML = ""; cardsEl.innerHTML = "";
    return;
  }
  if (cap.kind === "tabela") {
    plotEl.style.display = "none"; cardsEl.innerHTML = "";
    tbl.innerHTML = _tccTableHtml();
    return;
  }
  tbl.innerHTML = "";
  plotEl.style.display = "";
  var sinais = (cap.kind === "spec") ? ["spec"] : (cap.kind === "ons" ? [] : [st.sinal]);
  var fig = _tccFigure(cap, sinais, { dark: isDark, height: cap.kind === "ons" ? 520 : 460 });
  PLOTLY_CFG.toImageButtonOptions.filename = "tcc_" + cap.id + (st.sinal ? "_" + st.sinal : "");
  Plotly.react(plotEl, fig.data, fig.layout, PLOTLY_CFG);
  cardsEl.innerHTML = _tccCardsHtml(cap, isDark);
}

