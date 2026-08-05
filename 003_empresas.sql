-- ════════════════════════════════════════════════════════════
-- 003 · EMPRESAS
-- La IA nunca escribe acá directamente. Solo el promotor de hallazgos.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists empresas (
  id                    uuid primary key default gen_random_uuid(),

  -- identificación
  nombre                text not null,
  nombre_normalizado    text not null default '',
  razon_social          text,
  cuit                  text,
  cuit_verificado       boolean not null default false,
  identificador_oficial text,

  -- ubicación
  pais_id               uuid not null references paises(id) on delete restrict,
  provincia_id          uuid references provincias(id) on delete set null,
  partido_id            uuid references partidos(id) on delete set null,
  localidad_id          uuid references localidades(id) on delete set null,
  direccion             text,
  codigo_postal         text,
  lat                   numeric(9,6),
  lng                   numeric(9,6),
  geo_precision         text default 'sin_geo',

  -- contacto
  web                   text,
  dominio               text,
  email                 text,
  telefono              text,
  whatsapp              text,
  redes                 jsonb not null default '{}'::jsonb,

  -- perfil
  tipo                  text,
  especialidad          text,
  empleados_estimados   integer,
  obras_estimadas       integer,
  facturacion_estimada  numeric(14,2),
  nivel_digitalizacion  text,
  herramientas_actuales text[],

  -- comercial
  estado                company_status not null default 'no_investigada',
  puntaje_ia            smallint check (puntaje_ia between 0 and 100),
  puntaje_detalle       jsonb,
  probabilidad_cierre   smallint check (probabilidad_cierre between 0 and 100),
  responsable           uuid references auth.users(id) on delete set null,
  proxima_accion        text,
  proxima_fecha         date,

  -- trazabilidad
  origen_hallazgo_id    uuid,               -- FK se agrega en 005
  veces_encontrada      integer not null default 1,
  fecha_alta            timestamptz not null default now(),
  fecha_ultimo_analisis timestamptz,
  fecha_ultimo_contacto timestamptz,
  activa                boolean not null default true,
  motivo_baja           text,
  observaciones         text,
  actualizado           timestamptz not null default now(),

  constraint cuit_formato check (cuit is null or cuit ~ '^[0-9]{11}$'),
  constraint geo_precision_valida check (geo_precision in ('exacta','localidad','sin_geo'))
);

-- ── unicidad sobre identificadores fuertes ──
-- La base rechaza el duplicado aunque falle la lógica de la aplicación.
create unique index if not exists empresas_cuit_unico
  on empresas (cuit) where cuit is not null and cuit_verificado;

create unique index if not exists empresas_dominio_unico
  on empresas (dominio) where dominio is not null and dominio <> '';

create unique index if not exists empresas_identificador_unico
  on empresas (identificador_oficial) where identificador_oficial is not null;

create index if not exists empresas_localidad on empresas (localidad_id);
create index if not exists empresas_provincia on empresas (provincia_id);
create index if not exists empresas_estado on empresas (estado);
create index if not exists empresas_tipo on empresas (tipo);
create index if not exists empresas_nombre_trgm on empresas using gin (nombre_normalizado gin_trgm_ops);
create index if not exists empresas_alta on empresas (fecha_alta desc);

-- ── contactos · solo institucionales por defecto ──
create table if not exists empresa_contactos (
  id            uuid primary key default gen_random_uuid(),
  empresa_id    uuid not null references empresas(id) on delete cascade,
  nombre        text,
  cargo         text,
  email         text,
  telefono      text,
  es_decisor    boolean not null default false,
  institucional boolean not null default true,
  fuente        text,
  creado        timestamptz not null default now()
);

comment on column empresa_contactos.institucional is
  'true = dato de la empresa (info@, contacto@). Los datos personales requieren base legal: Ley 25.326.';

create index if not exists contactos_empresa on empresa_contactos (empresa_id);

-- ── historial · permite revertir enriquecimientos y fusiones ──
create table if not exists empresa_historial (
  id            uuid primary key default gen_random_uuid(),
  empresa_id    uuid not null references empresas(id) on delete cascade,
  tipo          text not null,
  texto         text,
  campo         text,
  valor_antes   jsonb,
  valor_despues jsonb,
  actor_tipo    text not null default 'sistema',
  actor_id      text,
  mision_id     uuid,
  creado        timestamptz not null default now(),
  constraint actor_valido check (actor_tipo in ('humano','agente','sistema'))
);

create index if not exists historial_empresa on empresa_historial (empresa_id, creado desc);

-- ── obras detectadas ──
create table if not exists empresa_obras (
  id              uuid primary key default gen_random_uuid(),
  empresa_id      uuid not null references empresas(id) on delete cascade,
  nombre          text,
  localidad_id    uuid references localidades(id) on delete set null,
  monto_estimado  numeric(14,2),
  estado          text,
  fuente_url      text,
  detectada       timestamptz not null default now()
);

create index if not exists obras_empresa on empresa_obras (empresa_id);

commit;
