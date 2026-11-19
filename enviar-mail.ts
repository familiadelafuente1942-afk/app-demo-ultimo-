// FUNCIÓN: enviar-mail
// Recibe { to, subject, html, from?, replyTo?, adjuntoUrl?, adjuntoNombre? } y manda el correo con Resend.
// Solo manda si el pedido trae la sesión de un usuario logueado (así nadie puede usarla para mandar mails a tu nombre).
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") || "";
const SUPABASE_ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY") || "";
const REMITENTE_POR_DEFECTO = "NEXO <sebas@nexorarq.com>";
const RESPONDER_A_POR_DEFECTO = "nexoentorno@gmail.com";
const DOMINIOS_REMITENTE = ["nexorarq.com", "belfastcm.com"];

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  try {
    if (!RESEND_API_KEY) throw new Error("Falta configurar RESEND_API_KEY como secreto en Supabase.");
    const token = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
    const u = token ? await fetch(SUPABASE_URL + "/auth/v1/user", { headers: { apikey: SUPABASE_ANON_KEY, Authorization: "Bearer " + token } }) : null;
    if (!u || !u.ok) return json({ error: "Falta iniciar sesión para mandar mails." }, 401);

    const { to, subject, html, from, replyTo, adjuntoUrl, adjuntoNombre } = await req.json();
    if (!to || !subject || !html) return json({ error: "Faltan datos: hacen falta 'to', 'subject' y 'html'." }, 400);
    const remitente = from && DOMINIOS_REMITENTE.some((d) => String(from).toLowerCase().includes("@" + d)) ? from : REMITENTE_POR_DEFECTO;

    const cuerpo: any = { from: remitente, to: [to], subject, html, reply_to: replyTo || RESPONDER_A_POR_DEFECTO };
    if (adjuntoUrl) cuerpo.attachments = [{ path: adjuntoUrl, filename: adjuntoNombre || "adjunto.pdf" }];

    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify(cuerpo),
    });
    const data = await r.json();
    if (!r.ok) return json({ error: data }, r.status);
    return json({ ok: true, id: data.id });
  } catch (e) {
    return json({ error: String((e as Error).message || e) }, 500);
  }
});
