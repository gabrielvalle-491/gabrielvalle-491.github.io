/*
 * Language toggle (ES / EN).
 * Text for each language lives in the HTML as elements with data-l="es" / data-l="en";
 * CSS hides the inactive language based on <html lang>. Attributes (title, meta,
 * aria-labels) are translated with data-es-* / data-en-* attributes.
 */
(function () {
  var KEY = "lang";
  var SUPPORTED = ["es", "en"];

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) { /* storage unavailable */ }
  }

  function apply(lang) {
    if (SUPPORTED.indexOf(lang) === -1) lang = "es";
    var root = document.documentElement;
    root.lang = lang;

    // Translate attributes: data-es-content / data-en-content, data-es-aria-label, ...
    var attrs = ["content", "aria-label", "title"];
    attrs.forEach(function (attr) {
      var sel = "[data-" + lang + "-" + attr + "]";
      document.querySelectorAll(sel).forEach(function (el) {
        el.setAttribute(attr, el.getAttribute("data-" + lang + "-" + attr));
      });
    });
    var t = root.getAttribute("data-" + lang + "-title");
    if (t) document.title = t;
  }

  apply(stored() || "es");

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-lang-toggle]");
    if (!btn) return;
    var next = document.documentElement.lang === "es" ? "en" : "es";
    store(next);
    apply(next);
  });

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
