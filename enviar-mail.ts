// ════════════════════════════════════════════════════════════
// FUNCIÓN: enviar-mail
// Recibe { to, subject, html, from?, adjuntoUrl?, adjuntoNombre? }
// y manda el correo con Resend. El adjunto es opcional: si se
// manda una URL pública (ej. un PDF en Supabase Storage), Resend
// lo descarga solo y lo adjunta — no hace falta subir el archivo
// a esta función.
// La clave de API vive como secreto en Supabase — nunca en el
// código del frontend, así nadie puede verla mirando la app.
// ════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.190.0/http/server.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");
const REMITENTE_POR_DEFECTO = "NEXO <sebas@nexorarq.com>";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  // Preflight de CORS
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    if (!RESEND_API_KEY) {
      throw new Error("Falta configurar RESEND_API_KEY como secreto en Supabase.");
    }

    const { to, subject, html, from, adjuntoUrl, adjuntoNombre } = await req.json();

    if (!to || !subject || !html) {
      return new Response(
        JSON.stringify({ error: "Faltan datos: hacen falta 'to', 'subject' y 'html'." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const cuerpo = {
      from: from || REMITENTE_POR_DEFECTO,
      to: [to],
      subject,
      html,
    };

    if (adjuntoUrl) {
      cuerpo.attachments = [
        { path: adjuntoUrl, filename: adjuntoNombre || "adjunto.pdf" },
      ];
    }

    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(cuerpo),
    });

    const data = await r.json();

    if (!r.ok) {
      return new Response(JSON.stringify({ error: data }), {
        status: r.status,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ ok: true, id: data.id }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
