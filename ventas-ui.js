/* Botón claro/oscuro de la app de ventas (NEXO y Belfast, cada una recuerda el suyo). */
(function(){
  var K = /belfast/.test(location.pathname) ? "bf_ui_tema" : "nexo_ui_tema";
  function leer(){ try { return localStorage.getItem(K) === "claro" ? "claro" : "oscuro"; } catch(e){ return "oscuro"; } }
  function aplicar(t){ var r = document.documentElement; if (t === "claro") r.setAttribute("data-ui-tema", "claro"); else r.removeAttribute("data-ui-tema"); var b = document.getElementById("ui-tema"); if (b) { b.innerHTML = t === "claro" ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10z"/></svg>' : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'; b.title = t === "claro" ? "Pasar a oscuro" : "Pasar a claro"; b.setAttribute("aria-label", b.title); } }
  aplicar(leer());
  function iniciar(){
    if (!document.getElementById("ui-tema")) { var b = document.createElement("button"); b.type = "button"; b.id = "ui-tema"; document.body.appendChild(b);
      b.addEventListener("click", function(){ var t = leer() === "claro" ? "oscuro" : "claro"; try { localStorage.setItem(K, t); } catch(e){} aplicar(t); }); }
    aplicar(leer());
    var sy = document.createElement("div"); sy.id = "ui-sync"; document.body.appendChild(sy);
    setInterval(function(){ var e = window.estadoSincronizacion; if (!e) { sy.style.display = "none"; return; } sy.style.display = "";
      if (e.ultimaBajada && !e.ultimoError) { sy.className = "ok"; sy.textContent = "☁ Sincronizado" + (e.total != null ? " · " + e.total : ""); }
      else if (/Sin sesión/.test(e.ultimoError || "")) { sy.className = "mal"; sy.textContent = "Sin sesión: los contactos quedan solo en este aparato"; }
      else if (e.ultimoError) { sy.className = "mal"; sy.textContent = "No se pudo sincronizar"; sy.title = e.ultimoError; }
      else { sy.className = ""; sy.textContent = "☁ Sincronizando…"; } }, 1500);
    setInterval(function(){ var nav = document.querySelector("#root-ventas .co-nav"); var vis = !!(nav && nav.offsetParent !== null || (nav && getComputedStyle(nav).position === "fixed" && nav.getBoundingClientRect().width > 0)); document.documentElement.classList.toggle("ui-con-barra", vis); }, 700);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
