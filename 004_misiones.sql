-- ════════════════════════════════════════════════════════════
-- 004 · ESTRATEGIAS Y MISIONES
-- La cola vive acá. Se toma con FOR UPDATE SKIP LOCKED.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists estrategias (
  id                  uuid primary key default gen_random_uuid(),
  nombre              text not null unique,
  mission_type        mission_type not null,
  descripcion         text,
  config              jsonb not null default '{}'::jsonb,
  activa              boolean not null default true,
  prioridad_base      smallint not null default 50,

  -- métricas acumuladas · alimentan el aprendizaje supervisado
  misiones_ejecutadas integer not null default 0,
  nuevas_totales      integer not null default 0,
  duplicados_totales  integer not null default 0,
  descartes_totales   integer not null default 0,
  costo_total_usd     numeric(12,6) not null default 0,

  creada              timestamptz not null default now(),
  actualizada         timestamptz not null default now()
);

comment on column estrategias.config is
  'Fuentes a consultar, forma de la consulta, herramientas. Los cambios los aprueba un humano.';

-- ── configuración por tipo de misión ──
create table if not exists mission_type_config (
  mission_type      mission_type primary key,
  costo_max_usd     numeric(8,6) not null,
  timeout_ms        integer not null,
  min_evidencias    smallint not null default 1,
  requiere_revision boolean not null default false,
  max_hallazgos     smallint not null,
  activa            boolean not null default true,
  notas             text
);

-- ── misiones ──
create table if not exists misiones (
  id                uuid primary key default gen_random_uuid(),
  mission_type      mission_type not null,
  estrategia_id     uuid references estrategias(id) on delete set null,

  -- destino
  pais_id           uuid not null references paises(id) on delete restrict,
  provincia_id      uuid references provincias(id) on delete set null,
  partido_id        uuid references partidos(id) on delete set null,
  localidad_id      uuid references localidades(id) on delete set null,
  tipo_empresa      text,
  empresa_id        uuid references empresas(id) on delete cascade,

  -- gestión
  prioridad         smallint not null default 50 check (prioridad between 0 and 100),
  estado            mission_status not null default 'pendiente',
  intentos          smallint not null default 0,
  max_intentos      smallint not null default 3,
  lease_hasta       timestamptz,
  urgente           boolean not null default false,

  -- tiempos
  creada            timestamptz not null default now(),
  programada        timestamptz not null default now(),
  inicio            timestamptz,
  fin               timestamptz,
  duracion_ms       integer,

  -- resultado
  encontradas       integer not null default 0,
  nuevas            integer not null default 0,
  duplicadas        integer not null default 0,
  descartadas       integer not null default 0,
  verificadas       integer not null default 0,
  senales           integer not null default 0,

  -- cobertura
  estimadas_zona    integer,
  cobertura_antes   numeric(5,2),
  cobertura_despues numeric(5,2),

  -- observabilidad
  consulta_ejecutada text,
  fuentes_usadas    jsonb,
  error             text,
  notas             text,
  creada_por        text not null default 'planificador',

  constraint creada_por_valido check (creada_por in ('planificador','humano')),
  -- enrichment y verification operan sobre una empresa concreta
  constraint mision_con_empresa check (
    mission_type not in ('enrichment','verification') or empresa_id is not null
  )
);

-- ── índices ──
-- El más importante del sistema: sostiene la selección de la cola.
create index if not exists misiones_cola
  on misiones (urgente desc, prioridad desc, creada asc)
  where estado = 'pendiente';

create index if not exists misiones_programada
  on misiones (programada) where estado = 'pendiente';

create index if not exists misiones_lease
  on misiones (lease_hasta) where estado = 'en_ejecucion';

create index if not exists misiones_zona
  on misiones (localidad_id, mission_type, estado);

create index if not exists misiones_fin
  on misiones (fin desc) where estado = 'completada';

create index if not exists misiones_estrategia on misiones (estrategia_id);

commit;
