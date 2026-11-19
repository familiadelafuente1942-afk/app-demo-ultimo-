/* ════════════════════════════════════════════════════════════
   SINCRONIZACIÓN CON SUPABASE
   ConstruIA · Centro de Operaciones Comercial

   Este archivo se agrega DESPUÉS de que la app define el objeto `bd`.
   No reemplaza IndexedDB: sigue siendo la base rápida de cada
   dispositivo. Esto agrega, por encima, un puente hacia Supabase
   para que los tres dispositivos vean lo mismo.

   Regla simple: al abrir la app se baja lo último de Supabase.
   Al guardar algo local, se sube en segundo plano. El último que
   guarda gana — no hay resolución de conflictos más fina que esa.
   ════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const SUPA_URL = 'https://agcmhrbxqtibrtmhwrrx.supabase.co';
  const SUPA_KEY = 'sb_publishable_kGPLp-DPPglnf6Eo3zPu6Q_OvE0MCkZ';

  let token = null;
  let sincronizando = false;
  let evitarRebote = false; // se activa mientras una bajada escribe en IndexedDB, para no volver a subir lo que se acaba de bajar

  // ── estado visible, por si la interfaz quiere mostrarlo ──
  const estadoSync = {
    conectado: false,
    ultimaSubida: null,
    ultimaBajada: null,
    ultimoError: null,
    pendientes: 0
  };
  window.estadoSincronizacion = estadoSync;

  window.addEventListener('unhandledrejection', function (ev) {
    try {
      const msg = ev && ev.reason && ev.reason.message ? ev.reason.message : String(ev && ev.reason);
      estadoSync.ultimoError = `[promesa sin atrapar] ${msg}`;
    } catch (e) {}
  });

  // ── sesión ──
  // Se guarda en sessionStorage (no localStorage): pide iniciar sesión
  // de nuevo en cada pestaña nueva, pero no dura para siempre en el
  // dispositivo. Ajustable si se prefiere otra política.
  function tokenGuardado() {
    try { return localStorage.getItem('supa_token'); } catch { return null; }
  }
  function refreshGuardado() {
    try { return localStorage.getItem('supa_refresh'); } catch { return null; }
  }
  function guardarToken(t, refresh) {
    try {
      localStorage.setItem('supa_token', (t || '').trim());
      if (refresh) localStorage.setItem('supa_refresh', (refresh || '').trim());
    } catch {}
  }

  async function iniciarSesion(email, clave) {
    const r = await fetch(`${SUPA_URL}/auth/v1/token?grant_type=password`, {
      method: 'POST',
      headers: { apikey: SUPA_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: clave })
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error_description || d.msg || 'No se pudo iniciar sesión');
    token = d.access_token;
    guardarToken(token, d.refresh_token);
    estadoSync.conectado = true;
    return token;
  }

  // Renueva la sesión sola, sin volver a pedir correo/contraseña,
  // usando el refresh_token que Supabase entrega junto al access_token.
  async function renovarSesion() {
    const refresh = refreshGuardado();
    if (!refresh) return null;
    try {
      const r = await fetch(`${SUPA_URL}/auth/v1/token?grant_type=refresh_token`, {
        method: 'POST',
        headers: { apikey: SUPA_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refresh })
      });
      const d = await r.json();
      if (!r.ok) return null;
      token = d.access_token;
      guardarToken(token, d.refresh_token);
      estadoSync.conectado = true;
      return token;
    } catch {
      return null;
    }
  }

  async function pedirSesionSiHaceFalta() {
    if (token) return token;
    const guardado = tokenGuardado();
    if (guardado) { token = guardado; estadoSync.conectado = true; return token; }

    const renovado = await renovarSesion();
    if (renovado) return renovado;

    // Pide credenciales una sola vez por pestaña. Se puede envolver
    // en una pantalla más prolija más adelante; por ahora usa prompt
    // nativo para no tocar el diseño existente de la app.
    // Modo abierto: nunca pide usuario ni contraseña. Sin sesión, la base queda en este dispositivo.
    throw new Error('Sin sesión: no se sincroniza');

  }

  // ── llamadas a la API ──
  async function supaFetch(ruta, opciones, _reintentado) {
    const t = await pedirSesionSiHaceFalta();
    try {
      const r = await fetch(`${SUPA_URL}/rest/v1/${ruta}`, {
        ...opciones,
        headers: {
          apikey: SUPA_KEY,
          Authorization: `Bearer ${t}`,
          'Content-Type': 'application/json',
          Prefer: 'return=representation',
          ...(opciones && opciones.headers)
        }
      });
      if (!r.ok) {
        const txt = await r.text();
        // token vencido: renovar una vez y reintentar el mismo pedido
        if (r.status === 401 && !_reintentado) {
          token = null;
          const renovado = await renovarSesion();
          if (renovado) return supaFetch(ruta, opciones, true);
        }
        throw new Error(`${r.status} · ${txt.slice(0, 200)}`);
      }
      // Algunos pedidos (los que llevan "return=minimal") responden
      // sin cuerpo. Leer eso como .json() directo rompe en Safari
      // con un error críptico ("The string did not match the
      // expected pattern"). Por eso se lee como texto primero.
      const cuerpo = await r.text();
      return cuerpo ? JSON.parse(cuerpo) : null;
    } catch (e) {
      throw new Error(`[${ruta}] ${e.message}`);
    }
  }

  // ── sincronización completa de la base de prospectos ──
  // Cada prospecto se guarda entero (todos sus campos) en la tabla
  // ventas_prospectos, separado por app (nexo / belfast). Al abrir, cada
  // 45 segundos y al volver a la app se mezcla lo local con la nube:
  // nada se pierde, lo nuevo de cualquier aparato aparece en los demás.
  const APP = /belfast/.test(location.pathname) ? 'belfast' : 'nexo';
  const K_META = 'sync_v2_' + APP; // { id: huella } de lo último que quedó igual en la nube
  let guardarOriginal = null, listarOriginal = null, subiendo = false, colaSubida = null;

  function huella(o) { const t = JSON.stringify(o); let h = 5381; for (let i = 0; i < t.length; i++) h = ((h << 5) + h + t.charCodeAt(i)) | 0; return String(h); }
  function leerMeta() { try { return JSON.parse(localStorage.getItem(K_META) || '{}') || {}; } catch { return {}; } }
  function guardarMeta(m) { try { localStorage.setItem(K_META, JSON.stringify(m)); } catch {} }

  async function bajarTodo() {
    const filas = [];
    for (let desde = 0; ; desde += 1000) {
      const tanda = await supaFetch(`ventas_prospectos?app=eq.${APP}&select=id,datos,t,borrado&order=id`, { headers: { Range: `${desde}-${desde + 999}`, 'Range-Unit': 'items' } });
      if (!tanda || !tanda.length) break;
      filas.push(...tanda);
      if (tanda.length < 1000) break;
    }
    return filas;
  }

  async function subirFilas(filas) {
    for (let i = 0; i < filas.length; i += 300) {
      await supaFetch('ventas_prospectos?on_conflict=app,id', {
        method: 'POST',
        headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
        body: JSON.stringify(filas.slice(i, i + 300))
      });
    }
  }

  // Sube lo que cambió en este aparato desde la última vez.
  async function subirCambios(lista) {
    const meta = leerMeta(), ahora = Date.now(), filas = [], vistos = new Set();
    for (const p of lista || []) {
      if (!p || p.id == null) continue;
      const id = String(p.id), h = huella(p); vistos.add(id);
      if (meta[id] !== h) filas.push({ app: APP, id, datos: p, t: ahora, borrado: false, _h: h });
    }
    for (const id of Object.keys(meta)) if (!vistos.has(id) && meta[id] !== 'x') filas.push({ app: APP, id, datos: {}, t: ahora, borrado: true, _h: 'x' });
    if (!filas.length) return 0;
    await subirFilas(filas.map(({ _h, ...f }) => f));
    filas.forEach(f => { if (f._h === 'x') meta[f.id] = 'x'; else meta[f.id] = f._h; });
    guardarMeta(meta);
    estadoSync.ultimaSubida = new Date().toISOString();
    return filas.length;
  }

  // Mezcla la nube con lo local y deja las dos iguales.
  async function mezclar() {
    if (sincronizando || !listarOriginal) return;
    sincronizando = true;
    try {
      const nube = await bajarTodo();
      const local = await listarOriginal('prospectos') || [];
      const meta = leerMeta();
      const porId = new Map(local.map(p => [String(p.id), p]));
      const idsNube = new Set(nube.filter(f => !f.borrado).map(f => String(f.id)));
      // La misma empresa cargada por separado en dos aparatos tiene distinto id: se queda la de la nube.
      const clave = p => { const n = String(p && (p.empresa || p.nombre) || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]/g, ''); const m = String(p && p.mail || '').trim().toLowerCase(); return [n ? 'n:' + n : '', m ? 'm:' + m : ''].filter(Boolean); };
      const localPorClave = new Map();
      for (const p of local) for (const k of clave(p)) if (!localPorClave.has(k)) localPorClave.set(k, String(p.id));
      let cambioLocal = false;
      for (const f of nube) {
        if (f.borrado || porId.has(String(f.id))) continue;
        for (const k of clave(f.datos)) { const otro = localPorClave.get(k); if (otro && otro !== String(f.id) && !idsNube.has(otro) && porId.has(otro)) { porId.delete(otro); delete meta[otro]; cambioLocal = true; } }
      }
      for (const f of nube) {
        const id = String(f.id), loc = porId.get(id);
        const locSinTocar = loc && meta[id] === huella(loc);
        if (f.borrado) {
          if (loc && locSinTocar) { porId.delete(id); cambioLocal = true; }
          if (!loc || locSinTocar) meta[id] = 'x';
          continue;
        }
        const hn = huella(f.datos);
        if (!loc) { porId.set(id, f.datos); meta[id] = hn; cambioLocal = true; }
        else if (huella(loc) === hn) meta[id] = hn;
        else if (locSinTocar) { porId.set(id, f.datos); meta[id] = hn; cambioLocal = true; }
        // si cambió en este aparato, gana lo local y se sube abajo
      }
      guardarMeta(meta);
      const final = [...porId.values()];
      if (cambioLocal) {
        evitarRebote = true;
        try { await guardarOriginal('prospectos', final); } finally { evitarRebote = false; }
        try { window.dispatchEvent(new StorageEvent('storage', { key: 'bd_ver_prospectos' })); } catch (e) {}
      }
      await subirCambios(final);
      estadoSync.ultimaBajada = new Date().toISOString();
      estadoSync.ultimoError = null;
      estadoSync.conectado = true;
      estadoSync.total = final.length;
    } catch (e) {
      estadoSync.ultimoError = e.message;
      console.warn('[sync] no se pudo sincronizar', e.message);
    } finally {
      sincronizando = false;
      if (typeof window.avisarBD === 'function') window.avisarBD();
    }
  }

  function programarSubida(filas) {
    colaSubida = filas;
    if (subiendo) return;
    subiendo = true;
    setTimeout(async () => {
      try { while (colaSubida) { const f = colaSubida; colaSubida = null; await subirCambios(f); } }
      catch (e) { estadoSync.ultimoError = e.message; console.warn('[sync] no se pudo subir', e.message); }
      finally { subiendo = false; }
    }, 1500);
  }

  // ── engancharse al objeto bd existente sin romperlo ──
  function engancharBD() {
    if (!window.bd || window.bd.__sincronizado) return false;
    guardarOriginal = window.bd.guardar.bind(window.bd);
    listarOriginal = window.bd.listar.bind(window.bd);
    window.bd.guardar = async function (tabla, filas) {
      const ok = await guardarOriginal(tabla, filas);
      if (ok && tabla === 'prospectos' && !evitarRebote) programarSubida(filas || []);
      return ok;
    };
    const actualizarOriginal = window.bd.actualizar.bind(window.bd);
    window.bd.actualizar = async function (tabla, fila) {
      const ok = await actualizarOriginal(tabla, fila);
      if (ok && tabla === 'prospectos' && !evitarRebote) listarOriginal('prospectos').then(programarSubida).catch(() => {});
      return ok;
    };
    window.bd.__sincronizado = true;
    return true;
  }

  // ── arranque ──
  function intentarArrancar() {
    if (!window.bd) { setTimeout(intentarArrancar, 200); return; }
    engancharBD();
    setTimeout(mezclar, 800);
    setInterval(mezclar, 45000);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) mezclar(); });
    window.addEventListener('focus', () => mezclar());
  }

  window.sincronizarAhora = mezclar;
  intentarArrancar();
})();
