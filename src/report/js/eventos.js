var _presResizeT = null;
window.addEventListener("resize", function() {
  if (!presOn) return;
  clearTimeout(_presResizeT);
  _presResizeT = setTimeout(_renderPres, 150);
});

// Esc com tela cheia: o navegador sai da tela cheia e não entrega a tecla;
// fullscreenchange fecha o modo junto
document.addEventListener("fullscreenchange", function() {
  if (!document.fullscreenElement && presOn) presToggle();
});

document.addEventListener("keydown", function(e) {
  var tg = e.target && e.target.tagName;
  if (tg === "SELECT" || tg === "INPUT" || tg === "TEXTAREA") return;
  var next = (e.key === "ArrowRight" || e.key === "PageDown");
  var prev = (e.key === "ArrowLeft" || e.key === "PageUp");
  // no capítulo mapa, a seta anda os passos antes de trocar de capítulo
  if (presOn) {
    if (next) { e.preventDefault(); presStep(1); }
    else if (prev) { e.preventDefault(); presStep(-1); }
    else if (e.key === "Escape") { presToggle(); }
  }
});
