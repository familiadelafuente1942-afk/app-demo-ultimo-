#!/usr/bin/env node
/**
 * ════════════════════════════════════════════════════════════
 * CARGA DE GEOGRAFÍA OFICIAL ARGENTINA
 *
 * Los departamentos (~530) y localidades (~2.300) NO están escritos
 * a mano en ningún archivo de este proyecto. Se cargan desde el
 * dataset oficial del Servicio de Normalización de Datos Geográficos
 * (datos.gob.ar), porque escribirlos de memoria garantiza errores.
 *
 * USO
 *   1. Descargar los archivos oficiales (ver docs/GEOGRAFIA.md)
 *   2. node scripts/cargar_geografia.mjs --dir ./datos-geo
 *
 * Espera encontrar en esa carpeta:
 *   departamentos.csv   (id, nombre, provincia_id, provincia_nombre)
 *   localidades.csv     (id, nombre, departamento_id, provincia_id,
 *                        centroide_lat, centroide_lon, categoria)
 * ════════════════════════════════════════════════════════════
 */

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.SUPABASE_URL;
const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error("Faltan SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en el entorno.");
  process.exit(1);
}

const dirIdx = process.argv.indexOf("--dir");
const DIR = dirIdx >= 0 ? process.argv[dirIdx + 1] : "./datos-geo";
const SOLO_PRUEBA = process.argv.includes("--subconjunto");

const db = createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false } });

// ── lectura de CSV, tolerante a comillas ──
function leerCSV(ruta) {
  const texto = readFileSync(ruta, "utf8").replace(/^\uFEFF/, "");
  const lineas = texto.split(/\r?\n/).filter((l) => l.trim());
  const cab = partir(lineas[0]);
  return lineas.slice(1).map((l) => {
    const celdas = partir(l);
    const o = {};
    cab.forEach((h, i) => { o[h.trim()] = (celdas[i] ?? "").trim(); });
    return o;
  });
}

function partir(linea) {
  const out = [];
  let actual = "", dentro = false;
  for (let i = 0; i < linea.length; i++) {
    const c = linea[i];
    if (c === '"') {
      if (dentro && linea[i + 1] === '"') { actual += '"'; i++; }
      else dentro = !dentro;
    } else if (c === "," && !dentro) { out.push(actual); actual = ""; }
    else actual += c;
  }
  out.push(actual);
  return out;
}

// ── subconjunto verificado, para probar sin descargar nada ──
// No pretende ser completo: son localidades que puedo afirmar con certeza.
const SUBCONJUNTO = {
  "Ciudad Autónoma de Buenos Aires": {
    "Comuna 14": ["Palermo"],
    "Comuna 13": ["Belgrano", "Núñez", "Colegiales"],
    "Comuna 2": ["Recoleta"],
    "Comuna 6": ["Caballito"],
    "Comuna 12": ["Villa Urquiza", "Saavedra", "Coghlan"],
  },
  "Buenos Aires": {
    "San Isidro": ["San Isidro", "Martínez", "Beccar", "Acassuso", "Boulogne"],
    "Vicente López": ["Vicente López", "Olivos", "Florida", "Munro"],
    "Tigre": ["Tigre", "Don Torcuato", "General Pacheco", "Benavídez", "Rincón de Milberg"],
    "Pilar": ["Pilar", "Del Viso", "Manzanares", "Villa Rosa"],
    "La Plata": ["La Plata", "City Bell", "Gonnet", "Tolosa"],
    "General Pueyrredón": ["Mar del Plata", "Batán"],
    "Quilmes": ["Quilmes", "Bernal", "Don Bosco", "Ezpeleta"],
    "Morón": ["Morón", "Castelar", "Haedo", "El Palomar"],
  },
  "Córdoba": {
    "Capital": ["Córdoba"],
    "Punilla": ["Villa Carlos Paz", "Cosquín", "La Falda"],
    "Colón": ["Villa Allende", "Unquillo", "Río Ceballos"],
    "Río Cuarto": ["Río Cuarto"],
  },
  "Santa Fe": {
    "Rosario": ["Rosario", "Funes", "Roldán", "Villa Gobernador Gálvez"],
    "La Capital": ["Santa Fe", "Santo Tomé", "Recreo"],
    "Castellanos": ["Rafaela"],
  },
  "Mendoza": {
    "Capital": ["Mendoza"],
    "Godoy Cruz": ["Godoy Cruz"],
    "Luján de Cuyo": ["Luján de Cuyo", "Chacras de Coria"],
    "Maipú": ["Maipú"],
  },
  "Neuquén": {
    "Confluencia": ["Neuquén", "Plottier", "Centenario"],
    "Lácar": ["San Martín de los Andes"],
    "Los Lagos": ["Villa La Angostura"],
  },
  "Río Negro": {
    "Bariloche": ["San Carlos de Bariloche"],
    "General Roca": ["General Roca", "Cipolletti", "Allen"],
  },
};

async function main() {
  console.log("Cargando geografía argentina\n");

  const { data: provincias, error: e1 } = await db
    .from("provincias").select("id, nombre, codigo");
  if (e1) { console.error("No se pudieron leer las provincias:", e1.message); process.exit(1); }
  if (!provincias?.length) {
    console.error("No hay provincias cargadas. Ejecutá primero seed/011_semillas.sql");
    process.exit(1);
  }
  console.log(`  ${provincias.length} provincias encontradas`);

  const porNombre = new Map(provincias.map((p) => [normalizar(p.nombre), p.id]));

  const rutaDep = join(DIR, "departamentos.csv");
  const rutaLoc = join(DIR, "localidades.csv");
  const hayArchivos = existsSync(rutaDep) && existsSync(rutaLoc);

  if (SOLO_PRUEBA || !hayArchivos) {
    if (!hayArchivos && !SOLO_PRUEBA) {
      console.log("\n  No encontré los archivos oficiales en " + DIR);
      console.log("  Cargo el subconjunto verificado para que puedas probar.");
      console.log("  Para la carga completa, ver docs/GEOGRAFIA.md\n");
    }
    await cargarSubconjunto(porNombre);
  } else {
    await cargarOficial(rutaDep, rutaLoc, porNombre);
  }

  const [{ count: nP }, { count: nL }] = await Promise.all([
    db.from("partidos").select("*", { count: "exact", head: true }),
    db.from("localidades").select("*", { count: "exact", head: true }),
  ]);
  console.log(`\nListo · ${nP} partidos/departamentos · ${nL} localidades`);
}

function normalizar(s) {
  return String(s || "").toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
}

async function cargarSubconjunto(porNombre) {
  let partidos = 0, locs = 0;
  for (const [prov, deps] of Object.entries(SUBCONJUNTO)) {
    const provId = porNombre.get(normalizar(prov));
    if (!provId) { console.warn(`  provincia no encontrada: ${prov}`); continue; }

    for (const [dep, localidades] of Object.entries(deps)) {
      const { data: p, error } = await db.from("partidos")
        .upsert({ provincia_id: provId, nombre: dep,
                  tipo: prov === "Buenos Aires" ? "partido"
                      : prov.includes("Autónoma") ? "comuna" : "departamento" },
                { onConflict: "provincia_id,nombre" })
        .select("id").single();
      if (error) { console.warn(`  ${dep}: ${error.message}`); continue; }
      partidos++;

      const filas = localidades.map((n) => ({ partido_id: p.id, nombre: n }));
      const { error: e2 } = await db.from("localidades")
        .upsert(filas, { onConflict: "partido_id,nombre" });
      if (e2) console.warn(`  localidades de ${dep}: ${e2.message}`);
      else locs += filas.length;
    }
  }
  console.log(`  subconjunto cargado · ${partidos} departamentos · ${locs} localidades`);
}

async function cargarOficial(rutaDep, rutaLoc, porNombre) {
  const deps = leerCSV(rutaDep);
  console.log(`  ${deps.length} departamentos en el archivo oficial`);

  const mapaDep = new Map();
  const lotes = [];
  for (const d of deps) {
    const provId = porNombre.get(normalizar(d.provincia_nombre || d.provincia));
    if (!provId) continue;
    lotes.push({
      provincia_id: provId,
      codigo_indec: d.id || d.codigo || null,
      nombre: d.nombre,
      tipo: normalizar(d.provincia_nombre || "") === "buenos aires" ? "partido" : "departamento",
    });
  }
  for (let i = 0; i < lotes.length; i += 500) {
    const { data, error } = await db.from("partidos")
      .upsert(lotes.slice(i, i + 500), { onConflict: "provincia_id,nombre" })
      .select("id, codigo_indec, nombre");
    if (error) { console.error("  error cargando departamentos:", error.message); break; }
    data.forEach((p) => { if (p.codigo_indec) mapaDep.set(p.codigo_indec, p.id); });
    process.stdout.write(`\r  departamentos: ${Math.min(i + 500, lotes.length)}/${lotes.length}`);
  }
  console.log("");

  const locs = leerCSV(rutaLoc);
  console.log(`  ${locs.length} localidades en el archivo oficial`);
  const filas = [];
  for (const l of locs) {
    const depId = mapaDep.get(l.departamento_id || l.departamento || "");
    if (!depId) continue;
    filas.push({
      partido_id: depId,
      codigo_indec: l.id || null,
      nombre: l.nombre,
      lat: l.centroide_lat ? Number(l.centroide_lat) : null,
      lng: l.centroide_lon ? Number(l.centroide_lon) : null,
    });
  }
  for (let i = 0; i < filas.length; i += 500) {
    const { error } = await db.from("localidades")
      .upsert(filas.slice(i, i + 500), { onConflict: "partido_id,nombre" });
    if (error) { console.error("\n  error cargando localidades:", error.message); break; }
    process.stdout.write(`\r  localidades: ${Math.min(i + 500, filas.length)}/${filas.length}`);
  }
  console.log("");
}

main().catch((e) => { console.error(e); process.exit(1); });
