/* NEXO demo · motor de idioma (español base, inglés, portugués)
   Traduce los nodos de texto y los atributos visibles. La app se redibuja sola,
   así que un observador vuelve a traducir lo nuevo. El idioma lo manda la página
   de presentación (localStorage "idioma" o mensaje {idioma}) o ?lang=en|pt. */
(function () {
  var D = window.DEMO_DICT || {};
  var IDX = { en: 0, pt: 1 };
  var lang = 'es';
  var orig = new WeakMap();      // nodo de texto -> {es, puesto}
  var origAt = new WeakMap();    // elemento -> {attr: {es, puesto}}
  var obs = null, busy = false;

  function norm(t) { return String(t).replace(/\s+/g, ' ').trim(); }
  var MABBR = { ene: 0, feb: 1, mar: 2, abr: 3, may: 4, jun: 5, jul: 6, ago: 7, sep: 8, sept: 8, oct: 9, nov: 10, dic: 11 };
  var MEN = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var MPT = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
  var MABRE = /(\d\s*)(ene|feb|mar|abr|may|jun|jul|ago|sept|sep|oct|nov|dic)\b|\b(ene|feb|mar|abr|may|jun|jul|ago|sept|sep|oct|nov|dic)(\s*\d)/gi;
  function normAll(t) {
    var n = [], m = [];
    var k = t.replace(MABRE, function (x, a1, a2, b1, b2) {
      var ab = (a2 || b1).toLowerCase(); m.push(MABBR[ab]);
      return a2 ? a1 + 'MES' : 'MES' + b2;
    });
    k = k.replace(/\d[\d.,]*\d|\d/g, function (x) { n.push(x); return '#'; });
    return { key: k, n: n, m: m };
  }
  function fillAll(s, o) {
    var i = 0, j = 0;
    return s.replace(/MES|#/g, function (x) {
      if (x === '#') return i < o.n.length ? o.n[i++] : '#';
      if (j < o.m.length) { var mm = o.m[j++]; return lang === 'en' ? MEN[mm] : MPT[mm]; }
      return 'MES';
    });
  }
  var PRE = window.DEMO_PREFIX || [];
  var RULES = (window.DEMO_RULES || []).map(function (r) { return [new RegExp(r[0]), r[1], r[2]]; });
  var SEP = [' · ', ' — ', ' | ', ' / ', ': ', ', ', ' → ', ' - ', ' × ', '; ', ' (', ')'];
  var CACHE = {};
  function hit(e) { return e && e[IDX[lang]] ? e[IDX[lang]] : null; }
  var LET = /[A-Za-zÁÉÍÓÚáéíóúñÑüÜ]/;
  var FRASES = null;
  function frases() {
    if (FRASES) return FRASES;
    FRASES = Object.keys(D).filter(function (k) {
      return k.length >= (k.indexOf('#') >= 0 ? 6 : 8) && k !== '# de #';
    }).sort(function (a, b) { return b.length - a.length; });
    return FRASES;
  }
  // sustituye frases conocidas dentro de un texto (trabaja sobre la clave con #/MES)
  function subst(t) {
    var o = normAll(t), out = o.key, ch = false, f = frases();
    for (var i = 0; i < f.length; i++) {
      var k = f[i], from = 0, at;
      while ((at = out.indexOf(k, from)) >= 0) {
        var b = at > 0 ? out.charAt(at - 1) : ' ', a = out.charAt(at + k.length) || ' ';
        if (LET.test(b) || LET.test(a)) { from = at + 1; continue; }
        var rep = D[k][IDX[lang]] || k;
        out = out.slice(0, at) + rep + out.slice(at + k.length); from = at + rep.length; ch = true;
      }
    }
    return ch ? fillAll(out, o) : null;
  }
  var SEP = [' · ', ' — ', ' | ', ' / ', ': ', ', ', ' → ', ' - ', ' × ', '; ', ' (', ')'];
  function cap(x, up) { return x ? (up ? x.charAt(0).toUpperCase() : x.charAt(0).toLowerCase()) + x.slice(1) : x; }
  function exact(k) {
    var r = hit(D[k]); if (r != null) return r;
    var c = k.charAt(0);
    if (c !== c.toUpperCase()) { r = hit(D[cap(k, true)]); if (r != null) return cap(r, false); }
    else if (c !== c.toLowerCase()) { r = hit(D[cap(k, false)]); if (r != null) return cap(r, true); }
    return null;
  }
  function look(t, depth) {
    var r = exact(t); if (r != null) return r;
    var o = normAll(t);
    if (o.key !== t) { r = exact(o.key); if (r != null) return fillAll(r, o); }
    if (/^[#\s\/\-–:.,MES]+$/.test(o.key) && /MES|#/.test(o.key)) return fillAll(o.key, o);
    if (depth > 4) return null;
    for (var ri = 0; ri < RULES.length; ri++) {
      var mm = t.match(RULES[ri][0]);
      if (mm) { var tpl = RULES[ri][IDX[lang] + 1]; return tpl.replace(/\$(\d)/g, function (x, d) { var g = mm[+d] || ''; var tg = look(g, depth + 1); return tg != null ? tg : g; }); }
    }
    if (/[^.]\.$/.test(t)) { var rt = look(t.slice(0, -1), depth + 1); if (rt != null) return rt + '.'; }
    // oraciones
    var sents = t.split(/(?<=[.!?])\s+/);
    if (sents.length > 1) {
      var any1 = false, res = sents.map(function (x) { var q = look(x, depth + 1); if (q == null) q = subst(x); if (q != null) { any1 = true; return q; } return x; });
      if (any1) return res.join(' ');
    }
    for (var q = 0; q < PRE.length; q++) {
      var pf = PRE[q][0];
      if (t.indexOf(pf) === 0 && t.length > pf.length) {
        var rest = t.slice(pf.length), rr = look(rest, depth + 1);
        if (rr == null) rr = subst(rest);
        return PRE[q][IDX[lang] + 1] + (rr != null ? rr : rest);
      }
    }
    for (var i = 0; i < SEP.length; i++) {
      var sp = SEP[i];
      if (t.indexOf(sp) > 0) {
        var parts = t.split(sp), any = false;
        var out = parts.map(function (p) {
          if (!p) return p;
          var r2 = look(p, depth + 1); if (r2 == null) r2 = subst(p);
          if (r2 != null) { any = true; return r2; } return p;
        });
        if (any) return out.join(sp === ' y ' ? (lang === 'en' ? ' and ' : ' e ') : sp);
      }
    }
    var w = t.match(/^(["“*¿¡(]*)(.+?)(["”*?!.:;…)]*)$/);
    if (w && w[2] !== t && (w[1] || w[3])) { r = look(w[2], depth + 1); if (r != null) return w[1] + r + w[3]; }
    var sb = subst(t); if (sb != null) return sb;
    if (t.indexOf(' y ') > 0) {
      var ps = t.split(' y '), any2 = false;
      var o2 = ps.map(function (p) { if (!p) return p; var r3 = look(p, depth + 1); if (r3 == null) r3 = subst(p); if (r3 != null) { any2 = true; return r3; } return p; });
      if (any2) return o2.join(lang === 'en' ? ' and ' : ' e ');
    }
    return null;
  }
  function tr(text) {
    if (lang === 'es') return text;
    var t = norm(text);
    if (t.length < 2) return text;
    var ck = lang + '|' + t;
    if (CACHE.hasOwnProperty(ck)) return CACHE[ck];
    var r = look(t, 0);
    if (r == null) r = subst(t);
    if (r == null) r = text;
    CACHE[ck] = r;
    return r;
  }

  function doText(n) {
    var cur = n.nodeValue, reg = orig.get(n);
    var base = (reg && reg.puesto === cur) ? reg.es : cur;       // si la app lo cambió, es texto nuevo
    if (lang === 'es') { if (reg && reg.puesto === cur) { n.nodeValue = reg.es; orig.delete(n); } return; }
    var lead = base.match(/^\s*/)[0], trail = base.match(/\s*$/)[0];
    var nuevo = tr(base);
    if (nuevo === base) return;
    var puesto = lead + nuevo + trail;
    n.nodeValue = puesto; orig.set(n, { es: base, puesto: puesto });
  }
  var ATTRS = ['placeholder', 'aria-label', 'title', 'alt'];
  function doAttrs(el) {
    ATTRS.forEach(function (a) {
      var v = el.getAttribute(a); if (!v) return;
      var m = origAt.get(el) || {}, r = m[a];
      var base = (r && r.puesto === v) ? r.es : v;
      if (lang === 'es') { if (r && r.puesto === v) { el.setAttribute(a, r.es); delete m[a]; } return; }
      var nv = tr(base);
      if (nv !== base) { el.setAttribute(a, nv); m[a] = { es: base, puesto: nv }; origAt.set(el, m); }
    });
  }
  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { doText(root); return; }
    if (root.nodeType !== 1) return;
    if (root.nodeName === 'SCRIPT' || root.nodeName === 'STYLE') return;
    doAttrs(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null), n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) { if (n.parentNode && n.parentNode.nodeName !== 'SCRIPT' && n.parentNode.nodeName !== 'STYLE') doText(n); }
      else doAttrs(n);
    }
  }
  function run(root) {
    if (busy) return; busy = true;
    if (obs) obs.disconnect();
    try { walk(root || document.body); } catch (e) { console.error(e); }
    if (obs) watch();
    busy = false;
  }
  function watch() { obs.observe(document.body, { childList: true, subtree: true, characterData: true }); }
  function setLang(l) {
    if (l !== 'es' && !IDX.hasOwnProperty(l)) l = 'es';
    lang = l;
    document.documentElement.lang = l;
    try { document.title = lang === 'es' ? 'NEXO' : 'NEXO'; } catch (e) { }
    run(document.body);
  }
  window.demoIdioma = setLang;
  window.demoIdiomaActual = function () { return lang; };
  // traducción de textos sueltos (toasts, PDF, IA) por si la app los arma por JS
  window.demoTr = tr;

  function inicio() {
    obs = new MutationObserver(function (ms) {
      if (lang === 'es') return;
      obs.disconnect();
      try { ms.forEach(function (m) { m.addedNodes.forEach(function (n) { walk(n); }); if (m.type === 'characterData') doText(m.target); }); } catch (e) { }
      watch();
    });
    watch();
    var l = 'es';
    try { var q = new URLSearchParams(location.search).get('lang'); if (q) l = q; else l = localStorage.getItem('idioma') || 'es'; } catch (e) { }
    setLang(l);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inicio); else inicio();
  window.addEventListener('message', function (e) { if (e.data && e.data.idioma) setLang(e.data.idioma); });
  window.addEventListener('storage', function (e) { if (e.key === 'idioma' && e.newValue) setLang(e.newValue); });
})();
