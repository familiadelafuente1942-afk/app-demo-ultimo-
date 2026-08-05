#!/usr/bin/env node
/**
 * ════════════════════════════════════════════════════════════
 * MIGRACIÓN DESDE INDEXEDDB A SUPABASE
 *
 * Lee el archivo que exporta la aplicación (construia-commercial-backup)
 * y carga las empresas en Supabase.
 *
 * NADA SE BORRA. El archivo queda intacto y la IndexedDB también.
 *
 * USO
 *   node scripts/migrar_indexeddb.mjs --archivo copia.json --simular
 *   node scripts/migrar_indexeddb.mjs --archivo copia.json
 * ════════════════════════════════════════════════════════════
 */

import { readFileSync } from "node:fs";
import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.SUPABASE_URL;
const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error("Faltan SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}

const arg = (n) => { const i = process.argv.indexOf(n); return i >= 0 ? process.argv[i + 1] : null; };
const ARCHIVO = arg("--archivo");
const SIMULAR = process.argv.includes("--simular");
if (!ARCHIVO) { console.error("Falta --archivo"); process.exit(1); }

const db = createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false } });

const ESTADOS = {
  nuevo: "no_investigada",
  contactado: "investigada",
  "reunión": "calificada",
  reunion: "calificada",
  propuesta: "calificada",
  cerrado: "cliente",
  perdido: "descartada",
};

const norm = (s) => String(s || "").toLowerCase()
  .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();

const dominioDe = (web) => {
  const d = String(web || "").toLowerCase()
    .replace(/^https?:\/\//, "").replace(/^www\./, "").split("/")[0];
  return d || null;
};

function leerArchivo(ruta) {
  const j = JSON.parse(readFileSync(ruta, "utf8"));
  if (j.format === "construia-commercial-backup" && j.data) return j.data;
  if (j.formato === "construia-base") return { prospectos: j.prospectos || [] };
  throw new Error("El archivo no tiene un formato reconocido de ConstruIA.");
}

async function main() {
  const data = leerArchivo(ARCHIVO);
  const pros = data.prospectos || [];
  console.log(`\nArchivo: ${ARCHIVO}`);
  console.log(`Empresas en el archivo: ${pros.length}`);
  console.log(SIMULAR ? "MODO SIMULACIÓN · no se escribe nada\n" : "MODO REAL · se va a escribir\n");

  const { data: pais } = await db.from("paises").select("id").eq("codigo", "AR").single();
  if (!pais) { console.error("No está cargada Argentina. Ejecutá seed/011_semillas.sql"); process.exit(1); }

  const { data: locs } = await db.from("localidades").select("id, nombre, partido_id");
  const { data: parts } = await db.from("partidos").select("id, provincia_id");
  const mapaPart = new Map((parts || []).map((p) => [p.id, p.provincia_id]));
  const mapaLoc = new Map((locs || []).map((l) => [norm(l.nombre), l]));

  const { data: existentes } = await db.from("empresas").select("id, nombre_normalizado, dominio, cuit");
  const porDominio = new Map((existentes || []).filter((e) => e.dominio).map((e) => [e.dominio, e.id]));
  const porNombre = new Map((existentes || []).map((e) => [e.nombre_normalizado, e.id]));

  const informe = { crear: 0, enriquecer: 0, sinZona: 0, sinNombre: 0, historiales: 0, contactos: 0 };
  const aCrear = [];
  const aEnriquecer = [];

  for (const p of pros) {
    const nombre = (p.empresa || p.nombre || "").trim();
    if (!nombre) { informe.sinNombre++; continue; }

    const dom = dominioDe(p.web);
    const yaId = (dom && porDominio.get(dom)) || porNombre.get(norm(nombre));

    // resolver zona: "Palermo, CABA" → busca "Palermo"
    let localidad_id = null, partido_id = null, provincia_id = null;
    if (p.zona) {
      const primera = String(p.zona).split(",")[0].trim();
      const l = mapaLoc.get(norm(primera));
      if (l) {
        localidad_id = l.id;
        partido_id = l.partido_id;
        provincia_id = mapaPart.get(l.partido_id) || null;
      } else informe.sinZona++;
    } else informe.sinZona++;

    const fila = {
      nombre,
      pais_id: pais.id,
      provincia_id, partido_id, localidad_id,
      web: p.web || null,
      email: p.mail || null,
      telefono: p.tel || null,
      tipo: p.rol || null,
      obras_estimadas: p.obras ? parseInt(p.obras, 10) || null : null,
      observaciones: p.dolor || null,
      estado: ESTADOS[p.estado] || "no_investigada",
      geo_precision: localidad_id ? "localidad" : "sin_geo",
      origen_hallazgo_id: null,
      fecha_alta: p.altaIso || new Date().toISOString(),
    };

    if (yaId) { aEnriquecer.push({ id: yaId, fila, origen: p }); informe.enriquecer++; }
    else { aCrear.push({ fila, origen: p }); informe.crear++; }

    informe.historiales += (p.historial || []).length;
    if (p.nombre && p.empresa) informe.contactos++;
  }

  console.log("RESUMEN");
  console.log(`  Se van a crear:        ${informe.crear}`);
  console.log(`  Ya existen (enriquecer): ${informe.enriquecer}`);
  console.log(`  Sin zona reconocible:  ${informe.sinZona}  (se cargan igual, sin localidad)`);
  console.log(`  Sin nombre (se omiten): ${informe.sinNombre}`);
  console.log(`  Historiales a migrar:  ${informe.historiales}`);
  console.log(`  Contactos a migrar:    ${informe.contactos}`);

  if (SIMULAR) {
    console.log("\nSimulación terminada. Nada se escribió.");
    console.log("Si el resumen te cierra, volvé a correr sin --simular.\n");
    return;
  }

  console.log("\nEscribiendo…");
  let creadas = 0;
  for (let i = 0; i < aCrear.length; i += 100) {
    const tanda = aCrear.slice(i, i + 100);
    const { data: nuevas, error } = await db.from("empresas")
      .insert(tanda.map((x) => x.fila)).select("id, nombre_normalizado");
    if (error) { console.error("  error:", error.message); break; }
    creadas += nuevas.length;

    // historiales y contactos
    for (let k = 0; k < tanda.length; k++) {
      const emp = nuevas[k];
      const org = tanda[k].origen;
      if (!emp) continue;

      const hist = (org.historial || []).map((h) => ({
        empresa_id: emp.id, tipo: h.tipo || "nota", texto: h.texto,
        actor_tipo: "humano", creado: h.iso || new Date().toISOString(),
      }));
      hist.push({
        empresa_id: emp.id, tipo: "nota",
        texto: "Migrada desde la base local del navegador",
        actor_tipo: "sistema",
      });
      if (hist.length) await db.from("empresa_historial").insert(hist);

      if (org.nombre && org.empresa) {
        await db.from("empresa_contactos").insert({
          empresa_id: emp.id, nombre: org.nombre,
          email: org.mail || null, telefono: org.tel || null,
          institucional: true, fuente: "migración local",
        });
      }
    }
    process.stdout.write(`\r  creadas: ${creadas}/${aCrear.length}`);
  }
  console.log("");

  // enriquecer: solo campos vacíos, nunca pisar
  let enriquecidas = 0;
  for (const e of aEnriquecer) {
    const limpio = {};
    for (const [k, v] of Object.entries(e.fila)) {
      if (v !== null && v !== undefined && v !== "") limpio[k] = v;
    }
    delete limpio.nombre; delete limpio.pais_id; delete limpio.fecha_alta;
    const { error } = await db.from("empresas").update(limpio).eq("id", e.id);
    if (!error) enriquecidas++;
  }

  console.log(`\nListo · ${creadas} creadas · ${enriquecidas} enriquecidas`);
  console.log("El archivo original y la base local quedaron intactos.\n");
}

main().catch((e) => { console.error(e); process.exit(1); });
