// MOTOR DE MARKETING IA — una sola función del servidor (el plan gratuito de Vercel limita la cantidad).
// Todo lo que sale hacia afuera (mails, posteos) pasa por la cola de aprobación y por los topes.
// Las claves viven solo en las variables de entorno de Vercel; el navegador nunca las ve.
//
// Acciones (parámetro ?accion=):
//   públicas:      baja
//   automática:    cron           (Vercel Cron, protegida con CRON_SECRET)
//   administrador: estado, config, generar_posts, generar_mails, cazar, cola, editar, aprobar, rechazar,
//                  aprobar_todo, enviar_ahora, prospectos, auditoria
//
// Variables de entorno:
//   SUPABASE_SERVICE_ROLE_KEY  (obligatoria)    clave de servicio de Supabase
//   ANTHROPIC_API_KEY          (para generar y cazar)
//   GMAIL_USER, GMAIL_APP_PASSWORD  (para enviar mails)
//   BAJA_SECRET                (firma de los links de baja; si falta se usa CRON_SECRET)
//   CRON_SECRET                (protege el cron)
//   MOTOR_MODEL                (por defecto claude-sonnet-5-5)
//   META_PAGE_ID, META_PAGE_TOKEN        (opcional: publicar en Facebook)
//   LINKEDIN_TOKEN, LINKEDIN_ORG_URN     (opcional: publicar en LinkedIn)

const crypto = require("crypto");

const SUPA_URL = "https://agcmhrbxqtibrtmhwrrx.supabase.co";
const SUPA_ANON = "sb_publishable_kGPLp-DPPglnf6Eo3zPu6Q_OvE0MCkZ"; // clave pública, la misma que usa la app
const SITIO = "https://app-demo-ultimo.vercel.app";
const TZ_OFFSET_H = -3; // Argentina

// ───────────────────────── utilidades puras (se prueban solas) ─────────────────────────

// Hora local de Argentina (para contar "hoy").
function diaLocal(fecha) {
  const d = new Date((fecha ? new Date(fecha) : new Date()).getTime() + TZ_OFFSET_H * 3600 * 1000);
  return d.toISOString().slice(0, 10);
}

// Tope de mails de hoy. Si el calentamiento está activo, sube de a poco desde el primer envío.
function topeEfectivo(cfg, hoy) {
  const maximo = Math.max(0, Number(cfg.tope_mails_dia) || 0);
  if (!cfg.rampa || !cfg.primer_envio) return cfg.rampa ? Math.min(maximo, 20) : maximo;
  const dias = Math.floor((Date.parse(hoy) - Date.parse(cfg.primer_envio)) / 86400000);
  let r;
  if (dias < 3) r = 20;
  else if (dias < 7) r = 40;
  else if (dias < 14) r = 80;
  else if (dias < 21) r = 150;
  else r = maximo;
  return Math.min(r, maximo);
}

function firmaBaja(email, secreto) {
  return crypto.createHmac("sha256", secreto).update(String(email).toLowerCase()).digest("hex").slice(0, 32);
}
function linkBaja(email, secreto) {
  const e = Buffer.from(String(email).toLowerCase()).toString("base64url");
  return SITIO + "/api/motor?accion=baja&e=" + e + "&s=" + firmaBaja(email, secreto);
}

const TEXTO_BAJA = {
  es: "Si no querés recibir más mensajes de NEXO, podés darte de baja acá:",
  pt: "Se não quiser mais receber mensagens do NEXO, você pode cancelar aqui:",
  en: "If you do not want to receive more messages from NEXO, you can unsubscribe here:"
};

function cuerpoConBaja(cuerpo, idioma, email, secreto) {
  const t = TEXTO_BAJA[idioma] || TEXTO_BAJA.es;
  return String(cuerpo).trim() + "\n\n—\n" + t + "\n" + linkBaja(email, secreto);
}

function emailValido(e) {
  return typeof e === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length < 200;
}

// Correos genéricos de empresa (no personales). El motor solo guarda estos.
function esCorreoEmpresa(e) {
  return /^(info|contacto|contato|contact|ventas|vendas|comercial|administracion|admin|hola|oi|ola|consultas|obras|proyectos|projetos|gerencia|direccion|diretoria)@/i.test(e || "");
}

function idiomaPorPais(pais) {
  return /^br/i.test(pais || "") ? "pt" : "es";
}

function limpiarJSON(txt) {
  const t = String(txt || "").replace(/^```json\s*/i, "").replace(/```\s*$/i, "").trim();
  const i = t.search(/[\[{]/);
  if (i < 0) throw new Error("La IA no devolvió JSON");
  return JSON.parse(t.slice(i));
}

// Palabras que nunca deben salir en un texto de marketing.
function textoSeguro(t) {
  return !/\bplata\b/i.test(t || "");
}

// ───────────────────────── acceso a Supabase y APIs ─────────────────────────

function clave() { return (process.env.SUPABASE_SERVICE_ROLE_KEY || "").replace(/\s+/g, ""); }

async function db(ruta, opts) {
  opts = opts || {};
  const k = clave();
  if (!k) throw Object.assign(new Error("Falta SUPABASE_SERVICE_ROLE_KEY en Vercel."), { status: 500 });
  const r = await fetch(SUPA_URL + "/rest/v1/" + ruta, {
    method: opts.method || "GET",
    headers: Object.assign({
      apikey: k, Authorization: "Bearer " + k, "Content-Type": "application/json",
      Prefer: opts.prefer || "return=representation"
    }, opts.headers || {}),
    body: opts.body ? JSON.stringify(opts.body) : undefined
  });
  const txt = await r.text();
  let data = null;
  try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = txt; }
  if (!r.ok) throw Object.assign(new Error((data && data.message) || "Error de base de datos (" + r.status + ")"), { status: 500 });
  return data;
}

async function auditar(actor, accion, detalle) {
  try { await db("mkt_auditoria", { method: "POST", body: { actor, accion, detalle: detalle || {} }, prefer: "return=minimal" }); } catch (e) { /* no frena la acción */ }
}

async function leerConfig() {
  const f = await db("mkt_motor_config?id=eq.1&select=*");
  return (f && f[0]) || { activo: false, tope_mails_dia: 30, rampa: true, tope_posts_dia: 6 };
}

// Verifica quién llama: el token de sesión de Supabase y que su mail esté en mkt_admins.
async function exigirAdmin(req) {
  const auth = req.headers.authorization || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  if (!token) throw Object.assign(new Error("Falta iniciar sesión."), { status: 401 });
  const r = await fetch(SUPA_URL + "/auth/v1/user", { headers: { apikey: SUPA_ANON, Authorization: "Bearer " + token } });
  if (!r.ok) throw Object.assign(new Error("Sesión vencida. Volvé a ingresar."), { status: 401 });
  const u = await r.json();
  const mail = String(u.email || "").toLowerCase();
  const adm = await db("mkt_admins?select=email&email=ilike." + encodeURIComponent(mail));
  if (!adm || !adm.length) throw Object.assign(new Error("Este usuario no tiene permiso para el motor."), { status: 403 });
  return mail;
}

async function claude(prompt, opts) {
  opts = opts || {};
  const key = (process.env.ANTHROPIC_API_KEY || "").replace(/\s+/g, "");
  if (!key.startsWith("sk-ant-")) throw Object.assign(new Error("Falta ANTHROPIC_API_KEY en Vercel."), { status: 500 });
  const body = {
    model: process.env.MOTOR_MODEL || "claude-sonnet-5-5",
    max_tokens: opts.max || 3000,
    messages: [{ role: "user", content: prompt }]
  };
  if (opts.buscar) body.tools = [{ type: "web_search_20250305", name: "web_search", max_uses: opts.buscar }];
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await r.json();
  if (!r.ok) throw Object.assign(new Error((data && data.error && data.error.message) || "Error de la IA"), { status: 502 });
  return (data.content || []).filter(b => b.type === "text").map(b => b.text).join("").trim();
}

// ───────────────────────── contexto de marca ─────────────────────────

const MARCA = `NEXO es una plataforma de gestión para constructoras, estudios de arquitectura y propietarios en Latinoamérica.
Qué hace de verdad: cronograma con ruta crítica y costo del atraso; pedidos de materiales atados a la tarea que los necesita; avisos cuando una definición o un pedido crítico se está venciendo (también al cliente); avances, bitácora de obra, certificados e informes semanales; cuatro apps que comparten el mismo dato (constructora, estudio, contratista, propietario); asistente de IA que lee los datos de la obra.
Mensaje central: "El trabajo no se atrasa en la obra. Se atrasa en la gestión." Dato citable con fuente: según el Work Trend Index 2023 de Microsoft, el 57% del tiempo de trabajo se va en comunicarse (reuniones, mails y chats) y el 43% en crear.
Demo pública: https://app-demo-ultimo.vercel.app
Reglas de redacción: no inventes cifras, clientes, testimonios ni precios; no prometas ahorros; usá la palabra "dinero" y nunca "plata"; tono profesional y cercano; una sola llamada a la acción clara.`;

// ───────────────────────── acciones ─────────────────────────

async function accionEstado() {
  const cfg = await leerConfig();
  const hoy = diaLocal();
  const desde = hoy + "T00:00:00-03:00";
  const [pend, apro, env, errs, pros, bajas] = await Promise.all([
    db("mkt_cola?estado=eq.pendiente&select=id", { prefer: "count=exact,return=representation" }),
    db("mkt_cola?estado=eq.aprobado&select=id,tipo"),
    db("mkt_cola?estado=eq.enviado&tipo=eq.mail&enviado_en=gte." + encodeURIComponent(desde) + "&select=id"),
    db("mkt_cola?estado=eq.error&select=id"),
    db("mkt_prospectos?select=id,estado,pais"),
    db("mkt_bajas?select=email")
  ]);
  const porPais = {};
  (pros || []).forEach(p => { porPais[p.pais || "?"] = (porPais[p.pais || "?"] || 0) + 1; });
  return {
    config: cfg,
    tope_hoy: topeEfectivo(cfg, hoy),
    enviados_hoy: (env || []).length,
    pendientes: (pend || []).length,
    aprobados_mail: (apro || []).filter(x => x.tipo === "mail").length,
    aprobados_post: (apro || []).filter(x => x.tipo === "post").length,
    errores: (errs || []).length,
    prospectos: (pros || []).length,
    prospectos_por_pais: porPais,
    bajas: (bajas || []).length,
    claves: {
      anthropic: !!process.env.ANTHROPIC_API_KEY,
      gmail: !!(process.env.GMAIL_USER && process.env.GMAIL_APP_PASSWORD),
      supabase: !!clave(),
      facebook: !!(process.env.META_PAGE_ID && process.env.META_PAGE_TOKEN),
      linkedin: !!(process.env.LINKEDIN_TOKEN && process.env.LINKEDIN_ORG_URN)
    }
  };
}

async function accionConfig(actor, b) {
  const cambios = {};
  if (typeof b.activo === "boolean") cambios.activo = b.activo;
  if (b.tope_mails_dia != null) cambios.tope_mails_dia = Math.max(0, Math.min(500, parseInt(b.tope_mails_dia, 10) || 0));
  if (b.tope_posts_dia != null) cambios.tope_posts_dia = Math.max(0, Math.min(50, parseInt(b.tope_posts_dia, 10) || 0));
  if (typeof b.rampa === "boolean") cambios.rampa = b.rampa;
  if (typeof b.remitente === "string") cambios.remitente = b.remitente.slice(0, 120);
  cambios.actualizado = new Date().toISOString();
  const r = await db("mkt_motor_config?id=eq.1", { method: "PATCH", body: cambios });
  await auditar(actor, "config", cambios);
  return r[0];
}

async function accionGenerarPosts(actor, b) {
  const canales = (b.canales && b.canales.length ? b.canales : ["linkedin", "instagram", "facebook"]).filter(c => ["linkedin", "instagram", "facebook"].includes(c));
  const dias = Math.max(1, Math.min(14, parseInt(b.dias, 10) || 7));
  const idiomas = (b.idiomas && b.idiomas.length ? b.idiomas : ["es"]).filter(i => ["es", "pt", "en"].includes(i));
  const tema = (b.tema || "").slice(0, 300);
  const filas = [];
  for (const canal of canales) {
    const porDia = canal === "instagram" ? 2 : 1;
    const n = dias * porDia;
    const prompt = `${MARCA}\n\nEscribí ${n} posteos para ${canal}, pensados para ${dias} días (${porDia} por día), para constructoras, estudios y desarrolladoras de Argentina, Brasil, Paraguay y Chile. ${tema ? "Enfoque pedido: " + tema + "." : ""}\nVariá los formatos: dato, pregunta, caso concreto de la plataforma, consejo de gestión de obra, demo. ${canal === "instagram" ? "Incluí una descripción de la imagen o reel sugerido." : ""} ${canal === "linkedin" ? "Largo 400 a 900 caracteres, con salto de línea entre ideas." : "Largo corto, directo."} Terminá cada uno con hashtags (3 a 6) y, en algunos, el link de la demo.\nIdiomas: ${idiomas.join(", ")} (si hay más de uno, escribí cada posteo en cada idioma como piezas separadas).\nRespondé SOLO con un JSON: [{"idioma":"es","texto":"...","visual":"..."}]`;
    const txt = await claude(prompt, { max: 6000 });
    const lista = limpiarJSON(txt);
    (Array.isArray(lista) ? lista : []).forEach((p, i) => {
      if (!p || !p.texto || !textoSeguro(p.texto)) return;
      filas.push({
        tipo: "post", canal, idioma: ["es", "pt", "en"].includes(p.idioma) ? p.idioma : "es",
        cuerpo: String(p.texto).slice(0, 3000), meta: { visual: p.visual || "", orden: i }, estado: "pendiente"
      });
    });
  }
  if (!filas.length) throw Object.assign(new Error("La IA no devolvió posteos válidos."), { status: 502 });
  await db("mkt_cola", { method: "POST", body: filas, prefer: "return=minimal" });
  await auditar(actor, "generar_posts", { cantidad: filas.length, canales, dias });
  return { creados: filas.length };
}

async function accionCazar(actor, b) {
  const pais = ({ ar: "Argentina", br: "Brasil", py: "Paraguay", cl: "Chile" })[String(b.pais || "").toLowerCase()] || b.pais;
  if (!pais || !["Argentina", "Brasil", "Paraguay", "Chile"].includes(pais)) throw Object.assign(new Error("País no válido."), { status: 400 });
  const rubro = (b.rubro || "constructoras, desarrolladoras inmobiliarias y estudios de arquitectura").slice(0, 200);
  const zona = (b.zona || "").slice(0, 120);
  const idioma = idiomaPorPais(pais);
  const prompt = `Buscá en la web ${Math.min(parseInt(b.cantidad, 10) || 8, 12)} empresas reales de ${pais}${zona ? " (zona: " + zona + ")" : ""} del rubro: ${rubro}, medianas o chicas, que dirijan obras activas y podrían usar un sistema de gestión de obra.\nPara cada una necesito: nombre, sitio web, ciudad, y el correo GENÉRICO de empresa que figure públicamente en su sitio (info@, contacto@, ventas@, comercial@). No uses correos personales ni inventes ninguno: si no hay un correo genérico público, dejá email vacío. Puntuá de 1 a 10 qué tan buen cliente parece (tamaño, obras en curso, necesidad de gestión).\nRespondé SOLO con un JSON: [{"empresa":"","web":"","ciudad":"","email":"","rubro":"","puntaje":0,"fuente":"url donde lo viste"}]`;
  const txt = await claude(prompt, { max: 4000, buscar: 6 });
  const lista = limpiarJSON(txt);
  const filas = [];
  (Array.isArray(lista) ? lista : []).forEach(p => {
    if (!p || !p.empresa) return;
    const email = (p.email || "").trim().toLowerCase();
    filas.push({
      empresa: String(p.empresa).slice(0, 160), web: p.web ? String(p.web).toLowerCase().replace(/\/+$/, "").slice(0, 200) : null,
      ciudad: (p.ciudad || "").slice(0, 100), email: emailValido(email) && esCorreoEmpresa(email) ? email : null,
      pais, idioma, rubro: (p.rubro || rubro).slice(0, 120), puntaje: Math.max(0, Math.min(10, parseInt(p.puntaje, 10) || 0)),
      fuente: (p.fuente || "").slice(0, 300), estado: "nuevo"
    });
  });
  let nuevos = 0;
  for (const f of filas) {
    try { await db("mkt_prospectos", { method: "POST", body: f, prefer: "return=minimal" }); nuevos++; } catch (e) { /* ya existía */ }
  }
  await auditar(actor, "cazar", { pais, encontrados: filas.length, nuevos });
  return { encontrados: filas.length, nuevos };
}

async function accionGenerarMails(actor, b) {
  const max = Math.max(1, Math.min(40, parseInt(b.cantidad, 10) || 10));
  const bajas = new Set(((await db("mkt_bajas?select=email")) || []).map(x => x.email));
  let pros = (await db("mkt_prospectos?estado=eq.nuevo&email=not.is.null&select=*&order=puntaje.desc&limit=" + max * 2)) || [];
  pros = pros.filter(p => !bajas.has(String(p.email).toLowerCase())).slice(0, max);
  if (!pros.length) return { creados: 0, aviso: "No hay prospectos nuevos con mail. Primero usá «Buscar prospectos»." };
  let creados = 0;
  for (const p of pros) {
    const idioma = p.idioma || idiomaPorPais(p.pais);
    const prompt = `${MARCA}\n\nEscribí un mail frío corto (90 a 140 palabras) a ${p.empresa} (${p.rubro || "constructora"}, ${p.ciudad || ""}, ${p.pais}), en ${idioma === "pt" ? "portugués de Brasil" : "español neutro rioplatense"}. Es un contacto de empresa, no una persona: saludá a la empresa. Contá UNA idea concreta de cómo NEXO evita atrasos (pedidos atados a tareas y avisos de definiciones que se vencen), mencioná la demo y pedí 15 minutos o que prueben la demo. Sin exagerar, sin cifras inventadas, sin prometer ahorros. NO agregues firma con datos inventados ni link de baja (se agrega solo). Cerrá con "Equipo NEXO".\nRespondé SOLO con un JSON: {"asunto":"...","cuerpo":"..."}`;
    try {
      const j = limpiarJSON(await claude(prompt, { max: 900 }));
      if (!j.asunto || !j.cuerpo || !textoSeguro(j.asunto + " " + j.cuerpo)) continue;
      await db("mkt_cola", {
        method: "POST", prefer: "return=minimal",
        body: { tipo: "mail", canal: "email", pais: p.pais, idioma, destino: p.email, asunto: String(j.asunto).slice(0, 160), cuerpo: String(j.cuerpo).slice(0, 2500), meta: { prospecto: p.id, empresa: p.empresa }, estado: "pendiente" }
      });
      await db("mkt_prospectos?id=eq." + p.id, { method: "PATCH", body: { estado: "mail_redactado" }, prefer: "return=minimal" });
      creados++;
    } catch (e) { /* sigue con el próximo */ }
  }
  await auditar(actor, "generar_mails", { creados });
  return { creados };
}

async function accionCola(b) {
  const est = ["pendiente", "aprobado", "rechazado", "enviado", "error"].includes(b.estado) ? b.estado : "pendiente";
  const tipo = ["mail", "post"].includes(b.tipo) ? "&tipo=eq." + b.tipo : "";
  const filas = await db("mkt_cola?estado=eq." + est + tipo + "&select=*&order=creado.asc&limit=" + Math.min(parseInt(b.limite, 10) || 100, 300));
  return { items: filas || [] };
}

async function accionEditar(actor, b) {
  if (!b.id) throw Object.assign(new Error("Falta el id."), { status: 400 });
  const cambios = {};
  if (typeof b.cuerpo === "string") cambios.cuerpo = b.cuerpo.slice(0, 3000);
  if (typeof b.asunto === "string") cambios.asunto = b.asunto.slice(0, 160);
  if (cambios.cuerpo && !textoSeguro(cambios.cuerpo)) throw Object.assign(new Error("El texto no puede usar esa palabra."), { status: 400 });
  const r = await db("mkt_cola?id=eq." + encodeURIComponent(b.id) + "&estado=in.(pendiente,aprobado)", { method: "PATCH", body: cambios });
  await auditar(actor, "editar", { id: b.id });
  return r[0] || {};
}

async function accionCambiarEstado(actor, ids, estado) {
  if (!ids.length) return { cambiados: 0 };
  const lista = ids.map(encodeURIComponent).join(",");
  const cambios = { estado };
  if (estado === "aprobado") cambios.aprobado_por = actor;
  const r = await db("mkt_cola?id=in.(" + lista + ")&estado=in.(pendiente,aprobado)", { method: "PATCH", body: cambios });
  await auditar(actor, estado === "aprobado" ? "aprobar" : "rechazar", { cantidad: (r || []).length });
  return { cambiados: (r || []).length };
}

// Envía de la cola los mails aprobados, respetando frenado, tope diario y bajas.
async function enviarTanda(actor, presupuestoMs) {
  const cfg = await leerConfig();
  if (!cfg.activo) return { enviados: 0, motivo: "El motor está frenado." };
  const user = process.env.GMAIL_USER, pass = process.env.GMAIL_APP_PASSWORD;
  if (!user || !pass) return { enviados: 0, motivo: "Falta conectar Gmail (GMAIL_USER y GMAIL_APP_PASSWORD)." };
  const secreto = process.env.BAJA_SECRET || process.env.CRON_SECRET;
  if (!secreto) return { enviados: 0, motivo: "Falta BAJA_SECRET o CRON_SECRET para firmar los links de baja." };
  const hoy = diaLocal();
  const tope = topeEfectivo(cfg, hoy);
  const ya = ((await db("mkt_cola?estado=eq.enviado&tipo=eq.mail&enviado_en=gte." + encodeURIComponent(hoy + "T00:00:00-03:00") + "&select=id")) || []).length;
  let libres = tope - ya;
  if (libres <= 0) return { enviados: 0, motivo: "Se alcanzó el tope de hoy (" + tope + ")." };
  const items = (await db("mkt_cola?estado=eq.aprobado&tipo=eq.mail&select=*&order=creado.asc&limit=" + Math.min(libres, 60))) || [];
  if (!items.length) return { enviados: 0, motivo: "No hay mails aprobados para enviar." };
  const bajas = new Set(((await db("mkt_bajas?select=email")) || []).map(x => x.email));
  const nodemailer = require("nodemailer");
  const tr = nodemailer.createTransport({ host: "smtp.gmail.com", port: 465, secure: true, auth: { user, pass }, pool: true, maxConnections: 1 });
  const fin = Date.now() + (presupuestoMs || 45000);
  let enviados = 0, saltados = 0, errores = 0;
  for (const it of items) {
    if (Date.now() > fin || libres <= 0) break;
    const dest = String(it.destino || "").toLowerCase();
    if (!emailValido(dest) || bajas.has(dest)) {
      await db("mkt_cola?id=eq." + it.id, { method: "PATCH", body: { estado: "cancelado", error: "Destinatario inválido o dado de baja" }, prefer: "return=minimal" });
      saltados++; continue;
    }
    try {
      const cuerpo = cuerpoConBaja(it.cuerpo, it.idioma, dest, secreto);
      await tr.sendMail({
        from: (cfg.remitente ? cfg.remitente + " <" + user + ">" : user), to: dest, subject: it.asunto || "NEXO", text: cuerpo,
        headers: { "List-Unsubscribe": "<" + linkBaja(dest, secreto) + ">" }
      });
      await db("mkt_cola?id=eq." + it.id, { method: "PATCH", body: { estado: "enviado", enviado_en: new Date().toISOString() }, prefer: "return=minimal" });
      if (!cfg.primer_envio) { await db("mkt_motor_config?id=eq.1", { method: "PATCH", body: { primer_envio: hoy }, prefer: "return=minimal" }); cfg.primer_envio = hoy; }
      enviados++; libres--;
      await new Promise(r => setTimeout(r, 1200));
    } catch (e) {
      errores++;
      await db("mkt_cola?id=eq." + it.id, { method: "PATCH", body: { estado: "error", error: String(e.message || e).slice(0, 300) }, prefer: "return=minimal" });
      if (errores >= 3) break; // algo anda mal: frena la tanda
    }
  }
  try { tr.close(); } catch (e) { /* */ }
  await auditar(actor, "enviar_tanda", { enviados, saltados, errores, tope, antes: ya });
  return { enviados, saltados, errores, tope, antes: ya };
}

// Publica posteos aprobados en los canales que tengan conexión. Instagram queda para publicación manual.
async function publicarPosts(actor) {
  const cfg = await leerConfig();
  if (!cfg.activo) return { publicados: 0, motivo: "El motor está frenado." };
  const hoy = diaLocal();
  const hechos = ((await db("mkt_cola?estado=eq.enviado&tipo=eq.post&enviado_en=gte." + encodeURIComponent(hoy + "T00:00:00-03:00") + "&select=id")) || []).length;
  let libres = (cfg.tope_posts_dia || 0) - hechos;
  const items = (await db("mkt_cola?estado=eq.aprobado&tipo=eq.post&canal=in.(facebook,linkedin)&select=*&order=creado.asc&limit=20")) || [];
  let publicados = 0;
  for (const it of items) {
    if (libres <= 0) break;
    try {
      if (it.canal === "facebook" && process.env.META_PAGE_ID && process.env.META_PAGE_TOKEN) {
        const r = await fetch("https://graph.facebook.com/v21.0/" + process.env.META_PAGE_ID + "/feed", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: it.cuerpo, access_token: process.env.META_PAGE_TOKEN })
        });
        if (!r.ok) throw new Error("Facebook " + r.status);
      } else if (it.canal === "linkedin" && process.env.LINKEDIN_TOKEN && process.env.LINKEDIN_ORG_URN) {
        const r = await fetch("https://api.linkedin.com/v2/ugcPosts", {
          method: "POST", headers: { Authorization: "Bearer " + process.env.LINKEDIN_TOKEN, "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0" },
          body: JSON.stringify({ author: process.env.LINKEDIN_ORG_URN, lifecycleState: "PUBLISHED", specificContent: { "com.linkedin.ugc.ShareContent": { shareCommentary: { text: it.cuerpo }, shareMediaCategory: "NONE" } }, visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" } })
        });
        if (!r.ok) throw new Error("LinkedIn " + r.status);
      } else continue; // sin conexión: queda aprobado para copiar a mano
      await db("mkt_cola?id=eq." + it.id, { method: "PATCH", body: { estado: "enviado", enviado_en: new Date().toISOString() }, prefer: "return=minimal" });
      publicados++; libres--;
    } catch (e) {
      await db("mkt_cola?id=eq." + it.id, { method: "PATCH", body: { estado: "error", error: String(e.message || e).slice(0, 300) }, prefer: "return=minimal" });
    }
  }
  if (publicados) await auditar(actor, "publicar_posts", { publicados });
  return { publicados };
}

// ───────────────────────── entrada ─────────────────────────

function leerBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  try { return JSON.parse(req.body || "{}"); } catch (e) { return {}; }
}

async function handler(req, res) {
  const q = req.query || {};
  const accion = q.accion || (leerBody(req).accion);
  try {
    // Baja pública: un link firmado en cada mail. No requiere sesión.
    if (accion === "baja") {
      const secreto = process.env.BAJA_SECRET || process.env.CRON_SECRET || "";
      let email = "";
      try { email = Buffer.from(String(q.e || ""), "base64url").toString("utf8").toLowerCase(); } catch (e) { /* */ }
      const ok = secreto && emailValido(email) && String(q.s || "") === firmaBaja(email, secreto);
      if (!ok) { res.status(400).setHeader("Content-Type", "text/html; charset=utf-8"); return res.send("<p>Link de baja no válido.</p>"); }
      await db("mkt_bajas", { method: "POST", body: { email }, prefer: "resolution=ignore-duplicates,return=minimal" });
      await db("mkt_cola?destino=eq." + encodeURIComponent(email) + "&estado=in.(pendiente,aprobado)", { method: "PATCH", body: { estado: "cancelado", error: "Baja" }, prefer: "return=minimal" });
      await auditar("publico", "baja", { email });
      res.setHeader("Content-Type", "text/html; charset=utf-8");
      return res.status(200).send('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:system-ui;max-width:480px;margin:60px auto;padding:0 16px"><h2>Listo, te dimos de baja.</h2><p>No vas a recibir más mensajes de NEXO. / Você não receberá mais mensagens do NEXO.</p></body>');
    }

    // Cron automático de Vercel
    if (accion === "cron") {
      const sec = (process.env.CRON_SECRET || "").trim();
      if (!sec || req.headers.authorization !== "Bearer " + sec) return res.status(401).json({ error: "No autorizado" });
      const m = await enviarTanda("cron", 40000);
      const p = await publicarPosts("cron");
      return res.status(200).json({ mails: m, posts: p });
    }

    if (req.method === "OPTIONS") return res.status(204).end();
    const actor = await exigirAdmin(req);
    const b = Object.assign({}, q, leerBody(req));
    let out;
    switch (accion) {
      case "estado": out = await accionEstado(); break;
      case "config": out = await accionConfig(actor, b); break;
      case "generar_posts": out = await accionGenerarPosts(actor, b); break;
      case "generar_mails": out = await accionGenerarMails(actor, b); break;
      case "cazar": out = await accionCazar(actor, b); break;
      case "cola": out = await accionCola(b); break;
      case "editar": out = await accionEditar(actor, b); break;
      case "aprobar": out = await accionCambiarEstado(actor, [].concat(b.ids || []), "aprobado"); break;
      case "rechazar": out = await accionCambiarEstado(actor, [].concat(b.ids || []), "rechazado"); break;
      case "aprobar_todo": {
        const f = await db("mkt_cola?estado=eq.pendiente" + (b.tipo === "mail" || b.tipo === "post" ? "&tipo=eq." + b.tipo : "") + "&select=id&limit=300");
        out = await accionCambiarEstado(actor, (f || []).map(x => x.id), "aprobado"); break;
      }
      case "enviar_ahora": out = { mails: await enviarTanda(actor, 45000), posts: await publicarPosts(actor) }; break;
      case "prospectos": out = { items: (await db("mkt_prospectos?select=*&order=creado.desc&limit=300")) || [] }; break;
      case "auditoria": out = { items: (await db("mkt_auditoria?select=*&order=creado.desc&limit=100")) || [] }; break;
      default: return res.status(400).json({ error: "Acción desconocida" });
    }
    return res.status(200).json(out);
  } catch (e) {
    return res.status(e.status || 500).json({ error: e.message || "Error inesperado" });
  }
}

module.exports = handler;
module.exports._interno = { diaLocal, topeEfectivo, firmaBaja, linkBaja, cuerpoConBaja, emailValido, esCorreoEmpresa, idiomaPorPais, limpiarJSON, textoSeguro };
