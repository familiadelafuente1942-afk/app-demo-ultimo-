// Fotos de obra del Manual Belfast: se guardan en Supabase Storage (bucket público "manual-obra").
// Lista:  GET  /api/manual-fotos?accion=lista
// Subir:  POST /api/manual-fotos  {accion:"subir", k:"capitulo/tema", img:"data:image/jpeg;base64,...", nota}
// Borrar: POST /api/manual-fotos  {accion:"borrar", k, path}
// Escritura: solo desde la propia app (mismo criterio "modo abierto" del motor).
const SUPA_URL = "https://agcmhrbxqtibrtmhwrrx.supabase.co";
const BUCKET = "manual-obra";

function clave() { return (process.env.SUPABASE_SERVICE_ROLE_KEY || "").replace(/\s+/g, ""); }
function cab(extra) {
  const k = clave();
  if (!k) throw Object.assign(new Error("Falta SUPABASE_SERVICE_ROLE_KEY en Vercel."), { status: 500 });
  const h = Object.assign({ apikey: k }, extra || {});
  if (!/^sb_/.test(k)) h.Authorization = "Bearer " + k;
  return h;
}
function vieneDeLaApp(req) { return /^https:\/\/app-demo-ultimo(-[a-z0-9-]+)?\.vercel\.app/.test(String(req.headers.origin || req.headers.referer || "")); }
function leerBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  try { return JSON.parse(req.body || "{}"); } catch (e) { return {}; }
}

async function asegurarBucket() {
  const r = await fetch(SUPA_URL + "/storage/v1/bucket/" + BUCKET, { headers: cab() });
  if (r.ok) return;
  const c = await fetch(SUPA_URL + "/storage/v1/bucket", { method: "POST", headers: cab({ "Content-Type": "application/json" }), body: JSON.stringify({ id: BUCKET, name: BUCKET, public: true, file_size_limit: 8 * 1024 * 1024 }) });
  if (!c.ok && c.status !== 409) throw new Error("No se pudo crear el bucket: " + (await c.text()).slice(0, 200));
}
async function leerIndice() {
  const r = await fetch(SUPA_URL + "/storage/v1/object/" + BUCKET + "/index.json?t=" + Date.now(), { headers: cab() });
  if (!r.ok) return {};
  try { return JSON.parse(await r.text()) || {}; } catch (e) { return {}; }
}
async function subirObjeto(path, buf, tipo) {
  const r = await fetch(SUPA_URL + "/storage/v1/object/" + BUCKET + "/" + path, { method: "POST", headers: cab({ "Content-Type": tipo, "x-upsert": "true", "cache-control": "max-age=31536000" }), body: buf });
  if (!r.ok) throw new Error("No se pudo guardar: " + (await r.text()).slice(0, 200));
}
async function guardarIndice(ind) {
  const r = await fetch(SUPA_URL + "/storage/v1/object/" + BUCKET + "/index.json", { method: "POST", headers: cab({ "Content-Type": "application/json", "x-upsert": "true", "cache-control": "no-cache" }), body: JSON.stringify(ind) });
  if (!r.ok) throw new Error("No se pudo actualizar el índice: " + (await r.text()).slice(0, 200));
}
const claveOk = k => /^[a-z0-9]+\/[a-z0-9]+$/.test(String(k || ""));

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  try {
    const b = req.method === "POST" ? leerBody(req) : {};
    const accion = (req.query && req.query.accion) || b.accion || "lista";
    if (accion === "lista") {
      const ind = await leerIndice();
      return res.status(200).json({ fotos: ind });
    }
    if (req.method !== "POST") return res.status(405).json({ error: "Usá POST" });
    if (!vieneDeLaApp(req)) return res.status(403).json({ error: "Solo desde la app del manual." });
    if (!claveOk(b.k)) return res.status(400).json({ error: "Tema no válido." });
    await asegurarBucket();
    if (accion === "subir") {
      const m = /^data:(image\/(jpeg|png|webp));base64,(.+)$/.exec(String(b.img || ""));
      if (!m) return res.status(400).json({ error: "Imagen no válida." });
      const buf = Buffer.from(m[3], "base64");
      if (buf.length > 6 * 1024 * 1024) return res.status(413).json({ error: "La foto es muy pesada." });
      const ext = m[2] === "jpeg" ? "jpg" : m[2];
      const path = b.k + "/" + Date.now() + "-" + Math.random().toString(36).slice(2, 7) + "." + ext;
      await subirObjeto(path, buf, m[1]);
      const ind = await leerIndice();
      (ind[b.k] = ind[b.k] || []).unshift({ path, u: SUPA_URL + "/storage/v1/object/public/" + BUCKET + "/" + path, t: Date.now(), nota: String(b.nota || "").slice(0, 200) });
      await guardarIndice(ind);
      return res.status(200).json({ ok: true, fotos: ind[b.k] });
    }
    if (accion === "borrar") {
      const ind = await leerIndice();
      const lista = ind[b.k] || [];
      if (!lista.some(f => f.path === b.path)) return res.status(404).json({ error: "No existe." });
      await fetch(SUPA_URL + "/storage/v1/object/" + BUCKET, { method: "DELETE", headers: cab({ "Content-Type": "application/json" }), body: JSON.stringify({ prefixes: [b.path] }) });
      ind[b.k] = lista.filter(f => f.path !== b.path);
      if (!ind[b.k].length) delete ind[b.k];
      await guardarIndice(ind);
      return res.status(200).json({ ok: true, fotos: ind[b.k] || [] });
    }
    return res.status(400).json({ error: "Acción desconocida." });
  } catch (e) {
    return res.status(e.status || 500).json({ error: String(e.message || e) });
  }
};
