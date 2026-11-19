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
    sy.addEventListener("click", function(){ if (sy.className !== "mal") return; abrirIngreso(); });
    function abrirIngreso(){
      if (document.getElementById("ui-ingreso")) return;
      var m = document.createElement("div"); m.id = "ui-ingreso";
      m.innerHTML = '<form><b>Conectar este aparato</b><p>Con tu cuenta de administrador los contactos quedan iguales en la PC, el iPad y el iPhone.</p><input type="email" name="e" placeholder="Mail" autocomplete="username" required><input type="password" name="c" placeholder="Contraseña" autocomplete="current-password" required><div class="ui-ing-err"></div><div class="ui-ing-bt"><button type="button" class="ui-ing-no">Cancelar</button><button type="submit" class="ui-ing-si">Conectar</button></div></form>';
      document.body.appendChild(m);
      var f = m.querySelector("form"), err = m.querySelector(".ui-ing-err");
      m.querySelector(".ui-ing-no").onclick = function(){ m.remove(); };
      f.onsubmit = function(ev){ ev.preventDefault(); err.textContent = "Conectando…";
        Promise.resolve(window.iniciarSesionSync ? window.iniciarSesionSync(f.e.value.trim(), f.c.value) : Promise.reject(new Error("No cargó la sincronización")))
          .then(function(){ m.remove(); }).catch(function(x){ err.textContent = "No se pudo: " + (x && x.message || x); }); };
      setTimeout(function(){ try { f.e.focus(); } catch(e){} }, 50);
    }
    setInterval(function(){ var e = window.estadoSincronizacion; if (!e) { sy.style.display = "none"; return; } sy.style.display = "";
      if (e.ultimaBajada && !e.ultimoError) { sy.className = "ok"; sy.textContent = "☁ Sincronizado" + (e.total != null ? " · " + e.total : ""); }
      else if (/Sin sesión/.test(e.ultimoError || "")) { sy.className = "mal"; sy.textContent = "Sin sesión · tocá acá para conectar este aparato"; }
      else if (e.ultimoError) { sy.className = "mal"; sy.textContent = "No se pudo sincronizar"; sy.title = e.ultimoError; }
      else { sy.className = ""; sy.textContent = "☁ Sincronizando…"; } }, 1500);
    setInterval(function(){ var nav = document.querySelector("#root-ventas .co-nav"); var vis = !!(nav && nav.offsetParent !== null || (nav && getComputedStyle(nav).position === "fixed" && nav.getBoundingClientRect().width > 0)); document.documentElement.classList.toggle("ui-con-barra", vis); }, 700);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
