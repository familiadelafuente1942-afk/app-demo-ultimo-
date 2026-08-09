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

  // ── sesión ──
  // Se guarda en sessionStorage (no localStorage): pide iniciar sesión
  // de nuevo en cada pestaña nueva, pero no dura para siempre en el
  // dispositivo. Ajustable si se prefiere otra política.
  function tokenGuardado() {
    try { return sessionStorage.getItem('supa_token'); } catch { return null; }
  }
  function guardarToken(t) {
    try { sessionStorage.setItem('supa_token', t); } catch {}
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
    guardarToken(token);
    estadoSync.conectado = true;
    return token;
  }

  async function pedirSesionSiHaceFalta() {
    if (token) return token;
    const guardado = tokenGuardado();
    if (guardado) { token = guardado; estadoSync.conectado = true; return token; }

    // Pide credenciales una sola vez por pestaña. Se puede envolver
    // en una pantalla más prolija más adelante; por ahora usa prompt
    // nativo para no tocar el diseño existente de la app.
    const email = window.prompt('Correo para sincronizar (Supabase):');
    if (!email) throw new Error('Sin correo, no se puede sincronizar');
    const clave = window.prompt('Contraseña:');
    if (!clave) throw new Error('Sin contraseña, no se puede sincronizar');
    return iniciarSesion(email, clave);
  }

  // ── llamadas a la API ──
  async function supaFetch(ruta, opciones) {
    const t = await pedirSesionSiHaceFalta();
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
      throw new Error(`${r.status} · ${txt.slice(0, 200)}`);
    }
    return r.json();
  }

  // ── mapeo de campos ──
  // El prospecto local y la fila de Supabase no tienen la misma forma.
  // Estas dos funciones traducen en cada sentido.
  function normalizarZona(z) {
    if (!z) return null;
    return String(z).split(',')[0].trim();
  }

  function prospectoASupabase(p) {
    return {
      origen_local_id: String(p.id),
      nombre: p.empresa || p.nombre || 'Sin nombre',
      tipo: p.rol || null,
      email: p.mail || null,
      telefono: p.tel || null,
      web: p.web || null,
      obras_estimadas: p.obras ? (parseInt(p.obras, 10) || null) : null,
      observaciones: p.dolor || null,
      estado: mapearEstado(p.estado),
      pais_id: null // se completa del lado del servidor si falta; ver nota abajo
    };
  }

  const MAPA_ESTADO = {
    nuevo: 'no_investigada',
    contactado: 'investigada',
    'reunión': 'calificada',
    reunion: 'calificada',
    propuesta: 'calificada',
    cerrado: 'cliente',
    perdido: 'descartada'
  };
  function mapearEstado(e) {
    return MAPA_ESTADO[String(e || '').toLowerCase()] || 'no_investigada';
  }
  const MAPA_ESTADO_INVERSO = {
    no_investigada: 'nuevo',
    investigada: 'contactado',
    calificada: 'propuesta',
    cliente: 'cerrado',
    descartada: 'perdido'
  };

  function supabaseAProspecto(e) {
    return {
      id: e.origen_local_id ? Number(e.origen_local_id) || e.origen_local_id : e.id,
      empresa: e.nombre,
      rol: e.tipo || '',
      mail: e.email || '',
      tel: e.telefono || '',
      web: e.web || '',
      obras: e.obras_estimadas != null ? String(e.obras_estimadas) : '',
      dolor: e.observaciones || '',
      estado: MAPA_ESTADO_INVERSO[e.estado] || 'nuevo',
      alta: e.fecha_alta ? new Date(e.fecha_alta).toLocaleDateString('es-AR') : '',
      notas: [],
      _supabase_id: e.id // se conserva para referencia; no lo usa el resto de la app
    };
  }

  // ── subir ──
  async function subirProspecto(p) {
    if (evitarRebote) return;
    try {
      estadoSync.pendientes++;
      const fila = prospectoASupabase(p);

      // pais_id: se asume Argentina. Se resuelve una vez y se cachea.
      fila.pais_id = await paisArgentinaId();

      await supaFetch(`empresas?on_conflict=origen_local_id`, {
        method: 'POST',
        headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
        body: JSON.stringify(fila)
      });
      estadoSync.ultimaSubida = new Date().toISOString();
      estadoSync.ultimoError = null;
    } catch (e) {
      estadoSync.ultimoError = e.message;
      console.warn('[sync] no se pudo subir', p && p.id, e.message);
    } finally {
      estadoSync.pendientes = Math.max(0, estadoSync.pendientes - 1);
    }
  }

  let _paisArgentinaId = null;
  async function paisArgentinaId() {
    if (_paisArgentinaId) return _paisArgentinaId;
    const filas = await supaFetch('paises?codigo=eq.AR&select=id');
    _paisArgentinaId = filas && filas[0] && filas[0].id;
    return _paisArgentinaId;
  }

  async function subirTodos(prospectos) {
    for (const p of prospectos) {
      if (p && p.id != null) await subirProspecto(p);
    }
  }

  // ── bajar y mezclar ──
  async function bajarYMezclar() {
    if (sincronizando) return;
    sincronizando = true;
    try {
      const filas = await supaFetch('empresas?select=*&order=fecha_alta.desc&limit=500');
      const prospectos = filas
        .filter(e => e.origen_local_id) // solo lo que vino de un dispositivo, no lo que cargue un agente
        .map(supabaseAProspecto);

      evitarRebote = true;
      await bd.guardar('prospectos', prospectos);
      evitarRebote = false;

      estadoSync.ultimaBajada = new Date().toISOString();
      estadoSync.ultimoError = null;
      if (typeof avisarBD === 'function') avisarBD();
    } catch (e) {
      estadoSync.ultimoError = e.message;
      console.warn('[sync] no se pudo bajar', e.message);
    } finally {
      sincronizando = false;
    }
  }

  // ── engancharse al objeto bd existente sin romperlo ──
  // `bd` es una variable de nivel superior definida en index.html
  // (const bd = {...}), no una propiedad de window. Un script clásico
  // cargado después comparte ese mismo ámbito, así que se referencia
  // directo por su nombre, sin el prefijo window.
  function engancharBD() {
    if (typeof bd === 'undefined' || bd.__sincronizado) return false;

    const guardarOriginal = bd.guardar.bind(bd);
    bd.guardar = async function (tabla, filas) {
      const ok = await guardarOriginal(tabla, filas);
      if (ok && tabla === 'prospectos' && !evitarRebote) {
        subirTodos(filas).catch(() => {});
      }
      return ok;
    };

    const actualizarOriginal = bd.actualizar.bind(bd);
    bd.actualizar = async function (tabla, fila) {
      const ok = await actualizarOriginal(tabla, fila);
      if (ok && tabla === 'prospectos' && !evitarRebote) {
        subirProspecto(fila).catch(() => {});
      }
      return ok;
    };

    bd.__sincronizado = true;
    return true;
  }

  // ── arranque ──
  let intentos = 0;
  function intentarArrancar() {
    if (typeof bd === 'undefined') {
      intentos++;
      if (intentos > 50) {
        console.error('[sync] no se encontró el objeto bd después de 10s. ¿Se movió el <script src="supabase-sync.js"> a otro lugar del archivo?');
        return;
      }
      // el objeto bd todavía no existe en este punto de la carga; reintenta
      setTimeout(intentarArrancar, 200);
      return;
    }
    engancharBD();
    bajarYMezclar();
  }

  // API manual, por si se quiere forzar una sincronización desde la interfaz
  window.sincronizarAhora = bajarYMezclar;

  intentarArrancar();
})();
