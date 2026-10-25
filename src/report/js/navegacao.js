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

// ao sair do palco, os capítulos com passos voltam a mostrar todos os casos
function _presPassoReset() {
  CAPS.forEach(function(c) {
    if (!c.passos_pres || !tccState[c.id]) return;
    c.passos_pres.forEach(function(ps) { ps.ocultar.forEach(function(k) { tccState[c.id].on[k] = true; }); });
    if (c.kind === "ons") tccState[c.id].outros = false;
  });
}

function _tccRefresh() { if (presOn) _renderPres(); }

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

function _openScenario(k) {
  if (presOn) presToggle();
  _applyPllFilter(SCENARIOS[k].badPll ? "bad" : "nominal");
  activeTab = "inv";
  document.getElementById("scenario-picker").value = k;
  switchScenario(k);
  _scrollToTabs();
}
