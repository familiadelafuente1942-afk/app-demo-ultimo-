-- ════════════════════════════════════════════════════════════
-- 011 · SEMILLAS
-- País, las 24 provincias, configuración por tipo de misión y presupuestos.
-- Los departamentos y localidades se cargan con scripts/cargar_geografia.mjs
-- desde el archivo oficial: NO se escriben a mano.
-- ════════════════════════════════════════════════════════════

begin;

-- ── país ──
insert into paises (codigo, nombre, config) values
('AR', 'Argentina', jsonb_build_object(
  'nivel_2', 'Provincia',
  'nivel_3', 'Partido/Departamento',
  'nivel_4', 'Localidad',
  'identificador_fiscal', 'CUIT',
  'identificador_formato', '^[0-9]{11}$',
  'idioma', 'es-AR',
  'moneda', 'ARS',
  'zona_horaria', 'America/Argentina/Buenos_Aires',
  'fuentes_denominador', jsonb_build_array('IERIC','CAMARCO','INDEC CNE','Colegios de Arquitectos')
))
on conflict (codigo) do nothing;

-- ── 24 provincias · códigos ISO 3166-2:AR ──
insert into provincias (pais_id, codigo, nombre)
select p.id, v.codigo, v.nombre
from paises p, (values
  ('C','Ciudad Autónoma de Buenos Aires'),
  ('B','Buenos Aires'),
  ('K','Catamarca'),
  ('H','Chaco'),
  ('U','Chubut'),
  ('X','Córdoba'),
  ('W','Corrientes'),
  ('E','Entre Ríos'),
  ('P','Formosa'),
  ('Y','Jujuy'),
  ('L','La Pampa'),
  ('F','La Rioja'),
  ('M','Mendoza'),
  ('N','Misiones'),
  ('Q','Neuquén'),
  ('R','Río Negro'),
  ('A','Salta'),
  ('J','San Juan'),
  ('D','San Luis'),
  ('Z','Santa Cruz'),
  ('S','Santa Fe'),
  ('G','Santiago del Estero'),
  ('V','Tierra del Fuego, Antártida e Islas del Atlántico Sur'),
  ('T','Tucumán')
) as v(codigo, nombre)
where p.codigo = 'AR'
on conflict (pais_id, codigo) do nothing;

-- ── configuración por tipo de misión ──
insert into mission_type_config
  (mission_type, costo_max_usd, timeout_ms, min_evidencias, requiere_revision, max_hallazgos, notas)
values
  ('discovery',           0.150000, 150000, 1, false, 12,
   'Busca empresas nuevas en una zona.'),
  ('enrichment',          0.050000,  90000, 1, false,  1,
   'Completa datos de una empresa ya existente.'),
  ('verification',        0.020000,  60000, 1, false,  1,
   'Confirma que la empresa sigue activa.'),
  ('contact_research',    0.060000,  90000, 1, true,   8,
   'Requiere revisión humana: toca datos de personas · Ley 25.326.'),
  ('radar',               0.100000, 120000, 1, false, 20,
   'Detecta señales. Nunca crea empresas directo.'),
  ('coverage_estimation', 0.080000, 120000, 2, true,   1,
   'Requiere revisión y dos evidencias: un denominador mal puesto distorsiona toda la cobertura.')
on conflict (mission_type) do update set
  costo_max_usd = excluded.costo_max_usd,
  timeout_ms = excluded.timeout_ms,
  min_evidencias = excluded.min_evidencias,
  requiere_revision = excluded.requiere_revision,
  max_hallazgos = excluded.max_hallazgos,
  notas = excluded.notas;

-- ── presupuesto aprobado para la etapa supervisada ──
insert into presupuestos (alcance, referencia, tope_diario_usd, tope_mensual_usd, aviso_pct, activo)
values ('global', null, 2.00, 50.00, 80, true)
on conflict do nothing;

-- ── precios de referencia para estimar ──
-- Verificar contra la lista vigente del proveedor antes de confiar en la estimación.
-- La diferencia con actual_cost_usd va a mostrar si quedaron viejos.
insert into precios_ia (proveedor, modelo, precio_entrada_mtok, precio_salida_mtok, precio_busqueda)
values
  ('anthropic', 'claude-sonnet-4-6', 3.0000, 15.0000, 0.010000),
  ('anthropic', 'claude-haiku-4-5',  0.8000,  4.0000, 0.010000)
on conflict (proveedor, modelo, vigente_desde) do nothing;

-- ── estrategias iniciales ──
insert into estrategias (nombre, mission_type, descripcion, config, prioridad_base)
values
  ('descubrimiento_web_general', 'discovery',
   'Búsqueda web abierta por zona y tipo de empresa.',
   jsonb_build_object('fuentes', jsonb_build_array('sitio_institucional','portal_publico'),
                      'max_resultados', 12), 50),
  ('descubrimiento_camaras', 'discovery',
   'Prioriza padrones de cámaras y colegios profesionales.',
   jsonb_build_object('fuentes', jsonb_build_array('camara_empresarial','ieric'),
                      'max_resultados', 12), 60),
  ('verificacion_sitio', 'verification',
   'Comprueba que el sitio siga vivo y los datos vigentes.',
   jsonb_build_object('fuentes', jsonb_build_array('sitio_institucional')), 40),
  ('radar_boletin_oficial', 'radar',
   'Revisa el Boletín Oficial buscando constituciones y cambios societarios.',
   jsonb_build_object('fuentes', jsonb_build_array('boletin_oficial'),
                      'tipos_senal', jsonb_build_array('empresa_nueva','cambio_autoridades')), 70)
on conflict (nombre) do nothing;

commit;
