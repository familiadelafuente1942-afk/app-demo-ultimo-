-- ════════════════════════════════════════════════════════════
-- 002 · GEOGRAFÍA
-- País → Provincia → Partido/Departamento → Localidad
-- Los denominadores de cobertura se guardan por fuente, sin mezclar.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists paises (
  id          uuid primary key default gen_random_uuid(),
  codigo      text not null unique,
  nombre      text not null,
  config      jsonb not null default '{}'::jsonb,
  activo      boolean not null default true,
  creado      timestamptz not null default now()
);

comment on column paises.config is
  'Nombres de los niveles, formato del identificador fiscal, idioma. Permite sumar países sin tocar código.';

create table if not exists provincias (
  id          uuid primary key default gen_random_uuid(),
  pais_id     uuid not null references paises(id) on delete restrict,
  codigo      text not null,
  nombre      text not null,
  poblacion   integer,
  centro_lat  numeric(9,6),
  centro_lng  numeric(9,6),
  creado      timestamptz not null default now(),
  unique (pais_id, codigo)
);

create table if not exists partidos (
  id            uuid primary key default gen_random_uuid(),
  provincia_id  uuid not null references provincias(id) on delete restrict,
  codigo_indec  text,
  nombre        text not null,
  tipo          text not null default 'departamento',
  poblacion     integer,
  creado        timestamptz not null default now(),
  unique (provincia_id, nombre)
);

comment on column partidos.tipo is 'partido (PBA) | departamento | comuna (CABA)';

create table if not exists localidades (
  id              uuid primary key default gen_random_uuid(),
  partido_id      uuid not null references partidos(id) on delete restrict,
  codigo_indec    text,
  nombre          text not null,
  codigo_postal   text,
  lat             numeric(9,6),
  lng             numeric(9,6),
  poblacion       integer,

  -- estado de barrido · alimenta los colores del mapa
  ultimo_barrido  timestamptz,
  tipos_barridos  text[] not null default '{}'::text[],

  creado          timestamptz not null default now(),
  unique (partido_id, nombre)
);

-- ── denominadores, uno por fuente ──
-- No se combinan padrones distintos como si fueran uno solo.
create table if not exists denominadores (
  id                  uuid primary key default gen_random_uuid(),
  localidad_id        uuid references localidades(id) on delete cascade,
  partido_id          uuid references partidos(id) on delete cascade,
  provincia_id        uuid references provincias(id) on delete cascade,

  tipo_empresa        text,                 -- null = todas
  cantidad            integer not null check (cantidad >= 0),

  fuente_nombre       text not null,        -- 'IERIC' | 'CAMARCO' | 'INDEC CNE'
  fuente_fecha        date not null,
  identificador_original text,              -- número de padrón, resolución, etc.
  cobertura_geografica text not null,       -- 'localidad' | 'partido' | 'provincia' | 'pais'
  metodo              coverage_method not null,
  metodo_detalle      text,                 -- si es extrapolación, cómo se calculó
  url                 text,

  ultima_actualizacion timestamptz not null default now(),
  creado              timestamptz not null default now(),

  -- Tiene que colgar de exactamente un nivel geográfico.
  constraint denominador_un_nivel check (
    (localidad_id is not null)::int +
    (partido_id  is not null)::int +
    (provincia_id is not null)::int = 1
  ),
  -- Una fuente no puede tener dos valores para el mismo alcance y tipo.
  unique nulls not distinct (localidad_id, partido_id, provincia_id, tipo_empresa, fuente_nombre)
);

comment on table denominadores is
  'Cada fila es el aporte de UNA fuente. Nunca se suman fuentes distintas sin declarar el método.';

create index if not exists denominadores_localidad on denominadores (localidad_id);
create index if not exists denominadores_fuente on denominadores (fuente_nombre, fuente_fecha desc);

create index if not exists provincias_pais on provincias (pais_id);
create index if not exists partidos_provincia on partidos (provincia_id);
create index if not exists localidades_partido on localidades (partido_id);
create index if not exists localidades_barrido on localidades (ultimo_barrido nulls first);
create index if not exists localidades_nombre_trgm on localidades using gin (nombre gin_trgm_ops);

commit;
