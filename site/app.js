/* VapePods site renderer — data from data.js (verified 2026-09-14). */
(function () {
  "use strict";
  var D = window.PODS_DATA;
  if (!D) { document.body.innerHTML = "<p style='padding:40px'>Data not loaded.</p>"; return; }

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function money(n) { return n == null ? null : "$" + n.toFixed(2); }
  function grams(size) {
    var m = /([\d.]+)\s*g/.exec(size || "");
    return m ? parseFloat(m[1]) : null;
  }
  function perGram(e) {
    var g = grams(e.size);
    if (g && e.price) return e.price / g;
    return null;
  }
  function taxChip(tax) {
    if (tax === "included") return '<span class="taxchip tax-included">TAX INCLUDED</span>';
    if (tax === "not-included") return '<span class="taxchip tax-not-included">TAX NOT INCLUDED</span>';
    return '<span class="taxchip tax-not-stated">TAX NOT STATED</span>';
  }
  function verifChip(v) {
    if (v === "live") return '<span class="verif">verified: live fetch</span>';
    return '<span class="verif index">verified: search index — click to confirm</span>';
  }

  // dates
  ["verified-date", "verified-date-2", "verified-date-3"].forEach(function (id) {
    var el = $(id); if (el) el.textContent = D.verified_date;
  });

  // ---------------- stat bar ----------------
  var priced = D.entries.filter(function (e) { return e.price != null; });
  var pods = priced.filter(function (e) { return e.type === "pod"; });
  var bestPod = pods.slice().sort(function (a, b) { return perGram(a) - perGram(b); })[0];
  var incl = priced.filter(function (e) { return e.tax === "included"; }).length;
  var bestDist = Math.min.apply(null, D.stores.map(function (s) { return s.distance_miles; }));
  $("statbar").innerHTML = [
    "<div class='stat'><div class='n'>" + priced.length + "</div><div class='l'>verified price entries</div></div>",
    "<div class='stat'><div class='n'>" + D.stores.length + "</div><div class='l'>stores checked</div></div>",
    "<div class='stat'><div class='n green'>" + (bestPod ? money(perGram(bestPod)) : "—") + "<span style='font-size:.7rem;color:var(--muted)'>/g</span></div><div class='l'>best $ per gram (pod)</div></div>",
    "<div class='stat'><div class='n amber'>" + incl + "</div><div class='l'>entries tax-included</div></div>",
    "<div class='stat'><div class='n green'>≈" + bestDist.toFixed(1) + " mi</div><div class='l'>closest verified store</div></div>",
  ].join("");

  // ---------------- best deals ----------------
  var best = pods.filter(function (e) { return perGram(e); })
    .sort(function (a, b) { return perGram(a) - perGram(b); })
    .slice(0, 4);
  $("best-grid").innerHTML = best.map(function (e, i) {
    var was = e.price_was ? "<s>" + money(e.price_was) + "</s>" : "";
    return "<div class='best-card'>" +
      "<div class='rank'>#" + (i + 1) + " · " + esc(e.store) + " · " + e.distance_miles.toFixed(1) + " mi</div>" +
      "<div class='name'>" + esc(e.product) + " · " + esc(e.size) + "</div>" +
      "<div class='price'>" + money(e.price) + was + " " + taxChip(e.tax) + "</div>" +
      "<div class='meta'>" + (e.deal ? esc(e.deal) + " · " : "") + "<a href='" + esc(e.source_url) + "' target='_blank' rel='noopener'>verify on official page →</a></div>" +
      "</div>";
  }).join("");

  // ---------------- filters ----------------
  var storeSel = $("f-store");
  storeSel.innerHTML = "<option value=''>All stores</option>" + D.stores
    .map(function (s) { return "<option value='" + esc(s.name) + "'>" + esc(s.name) + " (" + s.distance_miles.toFixed(1) + " mi)</option>"; })
    .join("");

  function render() {
    var fs = storeSel.value, ft = $("f-type").value, fx = $("f-tax").value, so = $("f-sort").value;
    var list = D.entries.filter(function (e) {
      if (fs && e.store !== fs) return false;
      if (ft && e.type !== ft) return false;
      if (fx && e.tax !== fx) return false;
      return true;
    });
    list.sort(function (a, b) {
      if (so === "price-asc") return (a.price || 1e9) - (b.price || 1e9);
      if (so === "price-desc") return (b.price || 0) - (a.price || 0);
      if (so === "dist-asc") return a.distance_miles - b.distance_miles;
      if (so === "pergram-asc") return (perGram(a) || 1e9) - (perGram(b) || 1e9);
      return 0;
    });
    $("entry-count").textContent = "(" + list.length + " shown)";
    $("entry-list").innerHTML = list.map(function (e) {
      var was = e.price_was ? "<s>" + money(e.price_was) + "</s>" : "";
      var deal = e.deal ? "<span class='deal'>🏷 " + esc(e.deal) + "</span>" : "";
      var stock = e.stock && /out of stock/i.test(e.stock) ? "<span class='stock'>⚠ " + esc(e.stock) + "</span>" : (e.stock ? "<span class='stock' style='color:var(--muted)'>" + esc(e.stock) + "</span>" : "");
      var thc = e.thc ? "· " + esc(e.thc) : "";
      var price = e.price != null
        ? "<div class='price'>" + money(e.price) + was + "</div>"
        : "<div class='price' style='font-size:1rem;color:var(--muted)'>see page</div>";
      return "<div class='entry'>" +
        "<div class='top'>" +
          "<span class='prod'>" + esc(e.product) + "</span>" +
          "<span class='size'>" + esc(e.size) + "</span>" +
          taxChip(e.tax) + deal + stock + verifChip(e.verified) +
        "</div>" +
        "<div class='pricebox'>" + price + (thc ? "<div class='thc'>" + thc + "</div>" : "") + "</div>" +
        "<div class='bottom'>" +
          "<span><span class='store-name'>" + esc(e.store) + "</span> <span class='dist'>· " + e.distance_miles.toFixed(1) + " mi</span></span>" +
          "<span class='compat'>" + esc(e.compat) + "</span>" +
          "<span class='src'>Source: <a href='" + esc(e.source_url) + "' target='_blank' rel='noopener'>" + esc(e.source_url) + "</a></span>" +
        "</div>" +
        (e.notes ? "<div class='note'>" + esc(e.notes) + "</div>" : "") +
        "</div>";
    }).join("");
  }
  ["f-store", "f-type", "f-tax", "f-sort"].forEach(function (id) { $(id).addEventListener("change", render); });
  render();

  // ---------------- stores ----------------
  $("store-grid").innerHTML = D.stores.map(function (s) {
    var deals = s.deals.map(function (d) {
      var warn = /FLAG|DOWN|no Stiiizy/i.test(d) ? " class='warn'" : "";
      return "<li" + warn + ">" + esc(d) + "</li>";
    }).join("");
    return "<div class='store-card'>" +
      "<h3>" + esc(s.name) + " <span class='dist'>≈" + s.distance_miles.toFixed(1) + " mi</span></h3>" +
      "<div class='addr'>" + esc(s.address) + (s.phone && s.phone !== "-" ? " · " + esc(s.phone) : "") + "</div>" +
      "<div class='hrs'>" + esc(s.hours) + "</div>" +
      "<div class='taxnote'>" + esc(s.tax_note) + "</div>" +
      (deals ? "<ul>" + deals + "</ul>" : "") +
      "<div class='links'>" +
        "<a href='" + esc(s.url) + "' target='_blank' rel='noopener'>Store page (official)</a>" +
        "<a href='" + esc(s.menu_url) + "' target='_blank' rel='noopener'>Live menu</a>" +
        (s.specials_url && s.specials_url !== s.menu_url ? "<a href='" + esc(s.specials_url) + "' target='_blank' rel='noopener'>Deals</a>" : "") +
      "</div>" +
      "<div class='n' style='margin-top:8px'>" + esc(s.source_status) + "</div>" +
      "</div>";
  }).join("");

  $("loc-list").innerHTML = D.other_locations.map(function (l) {
    // l = [name, address, phone, hours, url, note]
    return "<div class='loc'><div class='l'>" + esc(l[0]) + "</div>" +
      "<div class='a'>" + esc(l[1]) + " · " + esc(l[2]) + "</div>" +
      "<div class='a'>" + esc(l[3]) + "</div>" +
      "<div class='n'><a href='" + esc(l[4]) + "' target='_blank' rel='noopener'>Official store page →</a></div>" +
      "<div class='n'>⚠ " + esc(l[5]) + "</div></div>";
  }).join("");

  // ---------------- flags ----------------
  $("flag-list").innerHTML = D.flags.map(function (f) {
    var kind = f[0] === "FLAG" ? "f-flag" : "f-info";
    var tag = f[0] === "FLAG" ? "REVIEW" : "NOTE";
    var link = f[2] ? "<a href='" + esc(f[2]) + "' target='_blank' rel='noopener'>" + esc(f[2]) + "</a>" : "";
    return "<div class='flag " + kind + "'><span class='tag'>" + tag + "</span><div><p>" + esc(f[1]) + "</p>" + link + "</div></div>";
  }).join("");
})();
