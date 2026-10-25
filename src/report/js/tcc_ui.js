function _tccChipsHtml(cap, dark, withAdd) {
  var st = _tccSt(cap), mixed = _tccMixed(cap), grupo = null;
  // casos com grupo (a barra) ganham o rótulo do grupo antes do 1º chip e
  // perdem o prefixo "Barra N — " no chip; o traço do chip segue o da curva
  var html = _tccCases(cap).map(function(c) {
    var lbl = _tccLabel(c.key, mixed), pre = "";
    if (c.grupo) {
      if (c.grupo !== grupo) pre = "<span class=\"tcc-grupo\">" + c.grupo + "</span>";
      lbl = lbl.replace(c.grupo + " — ", "");
    }
    grupo = c.grupo || null;
    var sw = "tcc-sw" + (c.dash ? " tracejado" : "") + (c.larg ? " grosso" : "");
    return pre + "<button class=\"tcc-chip" + (st.on[c.key] !== false ? " on" : "") + "\" style=\"--c:"
      + (dark ? c.dark : c.light) + "\" onclick=\"_tccChip('" + c.key + "')\"><span class=\"" + sw + "\"></span>"
      + lbl + (cap.kind === "ons" ? _onsBadge(c.key) : "") + "</button>";
  }).join("");
  if (cap.kind === "ons") html += _onsCtrlHtml(cap);
  if (withAdd && (cap.kind === "time" || cap.kind === "spec")) {
    var inList = _tccCases(cap).map(function(c) { return c.key; });
    var opts = Object.keys(SCENARIOS).filter(function(k) {
      return inList.indexOf(k) === -1 && (cap.kind === "time"
        ? (cap.id === "energ") === (SCENARIOS[k].tFault == null)
        : SCENARIOS[k].tFault != null);
    }).map(function(k) {
      return "<option value=\"" + k + "\">" + _tccLabel(k, true) + "</option>";
    }).join("");
    html += "<select class=\"tcc-add\" onchange=\"_tccAdd(this)\">"
      + "<option value=\"\">+ comparar com…</option>" + opts + "</select>";
  }
  return html;
}

function _tccCardsHtml(cap, dark) {
  if (cap.matriz) return _tccMatrizHtml(cap, dark);
  var mixed = _tccMixed(cap), grupo = null;
  return _tccVisible(cap).map(function(c) {
    var novo = c.grupo && grupo && c.grupo !== grupo;   // respiro entre grupos
    grupo = c.grupo || null;
    var ind = SCENARIOS[c.key].tccInd || {};
    var rows = cap.metricas.map(function(m) {
      return "<p class=\"tcc-row\"><span>" + IND_LBL[m] + "</span><b>"
        + (ind[m] != null ? ind[m] : "—") + "</b></p>";
    }).join("");
    return "<div class=\"tcc-card" + (novo ? " tcc-card-grupo" : "") + "\" style=\"--c:" + (dark ? c.dark : c.light) + "\""
      + " title=\"Abrir este cenário nas abas\" onclick=\"_openScenario('" + c.key + "')\">"
      + "<p class=\"tcc-card-h\">" + _tccLabel(c.key, mixed)
      + (cap.kind === "ons" ? _onsBadge(c.key, true) : "") + "</p>" + rows + "</div>";
  }).join("");
}

// Matriz no lugar dos cartões (cap.matriz): linhas × colunas de cenário
// (chave = prefixo da linha + "/" + sufixo da coluna). 1ª métrica em
// destaque, as outras pequenas ao lado. Caso fora de cap.casos entra só na
// matriz, sem amostra de traço; caso desligado no chip fica esmaecido.
function _tccMatrizHtml(cap, dark) {
  var M = cap.matriz, st = _tccSt(cap), rot = M.rotulos || {};
  var cs = {}; _tccCases(cap).forEach(function(c) { cs[c.key] = c; });
  var cls = function(i) { return i === M.realce ? " class=\"realce\"" : ""; };
  var h = "<table class=\"tcc-mat\"><tr><th></th>" + M.colunas.map(function(c, i) {
    return "<th" + cls(i) + ">" + c[0] + "</th>"; }).join("") + "</tr>";
  M.linhas.forEach(function(l) {
    h += "<tr><th class=\"tcc-mat-l\">" + l[0] + "</th>";
    M.colunas.forEach(function(col, i) {
      var k = l[1] + "/" + col[1], sc = SCENARIOS[k], c = cs[k];
      if (!sc) { h += "<td" + cls(i) + ">—</td>"; return; }
      var ind = sc.tccInd || {}, m0 = cap.metricas[0];
      var sw = c ? "<span class=\"tcc-sw" + (c.dash ? " tracejado" : "") + (c.larg ? " grosso" : "")
        + "\" style=\"--c:" + (dark ? c.dark : c.light) + "\"></span>" : "<span class=\"tcc-sw vazio\"></span>";
      var resto = cap.metricas.slice(1).map(function(m) {
        return "<span class=\"tcc-mat-s\">" + (rot[m] || IND_LBL[m]) + " <b>"
          + (ind[m] != null ? ind[m] : "—") + "</b></span>"; }).join("");
      var off = c && st.on[k] === false ? " off" : "";
      h += "<td" + (i === M.realce ? " class=\"realce" + off + "\"" : (off ? " class=\"off\"" : ""))
        + " title=\"Abrir este cenário nas abas\" onclick=\"_openScenario('" + k + "')\">"
        + sw + "<b class=\"tcc-mat-v\">" + (ind[m0] != null ? ind[m0] : "—") + "</b>" + resto + "</td>";
    });
    h += "</tr>";
  });
  return "<div class=\"tcc-mat-wrap\">" + h + "</table>"
    + (M.nota ? "<p class=\"tcc-mat-nota\">" + M.nota + "</p>" : "") + "</div>";
}

function _tccTableHtml() {
  var keys = Object.keys(SCENARIOS).filter(function(k) { return SCENARIOS[k].tcc; })
    .sort(function(a, b) { return SCENARIOS[a].tccOrd - SCENARIOS[b].tccOrd; });
  var head = "<th>Cenário</th>" + CMP_HEAD.map(function(h) { return "<th>" + h + "</th>"; }).join("");
  var rows = keys.map(function(k) {
    var sc = SCENARIOS[k], r = sc.metricsRow;
    var bad = sc.badPll ? "<span class=\"tcc-bad-tag\">inadequada</span>" : "";
    return "<tr class=\"cmp-row\" onclick=\"_openScenario('" + k + "')\">"
      + "<td class=\"cmp-label\">" + sc.label + bad
      + "<span class=\"tcc-tag\">§" + sc.tcc + "</span></td>"
      + CMP_COLS.map(function(c) {
          // vírgula decimal, como no resto do palco (a tabela comparativa das abas segue com ponto)
          return _cmpCell({ cls: r[c].cls, val: String(r[c].val).replace(".", ",") });
        }).join("") + "</tr>";
  }).join("");
  return "<div class=\"table-wrap\"><table class=\"cmp-table tcc-cmp\"><thead><tr>"
    + head + "</tr></thead><tbody>" + rows + "</tbody></table></div>";
}

