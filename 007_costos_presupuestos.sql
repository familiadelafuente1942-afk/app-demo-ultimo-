-- ════════════════════════════════════════════════════════════
-- 007 · COSTOS Y PRESUPUESTOS
-- actual_cost_usd es la referencia principal cuando está disponible.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists costos_ia (
  id                      uuid primary key default gen_random_uuid(),
  mision_id               uuid references misiones(id) on delete cascade,
  hallazgo_id             uuid references hallazgos(id) on delete set null,

  proveedor               text not null,
  modelo                  text not null,

  tokens_entrada          integer not null default 0,
  tokens_salida           integer not null default 0,
  tokens_cache_lectura    integer not null default 0,
  tokens_cache_escritura  integer not null default 0,

  busquedas_web           integer not null default 0,
  herramientas_externas   jsonb not null default '{}'::jsonb,

  estimated_cost_usd      numeric(12,6) not null,
  actual_cost_usd         numeric(12,6),
  diferencia_usd          numeric(12,6) generated always as
                            (coalesce(actual_cost_usd, estimated_cost_usd) - estimated_cost_usd) stored,

  request_id              text,
  creado                  timestamptz not null default now()
);

comment on column costos_ia.actual_cost_usd is
  'Costo informado por el proveedor. Es la referencia principal; estimated_cost_usd es el respaldo.';
comment on column costos_ia.diferencia_usd is
  'Si crece de forma consistente, la tabla de precios usada para estimar quedó desactualizada.';

create index if not exists costos_mision on costos_ia (mision_id);
create index if not exists costos_fecha on costos_ia (creado desc);
create index if not exists costos_modelo on costos_ia (proveedor, modelo);

-- ── precios vigentes, para estimar antes de ejecutar ──
create table if not exists precios_ia (
  id                  uuid primary key default gen_random_uuid(),
  proveedor           text not null,
  modelo              text not null,
  precio_entrada_mtok numeric(10,4) not null,
  precio_salida_mtok  numeric(10,4) not null,
  precio_busqueda     numeric(10,6) not null default 0,
  vigente_desde       date not null default current_date,
  vigente_hasta       date,
  unique (proveedor, modelo, vigente_desde)
);

-- ── presupuestos con corte automático ──
create table if not exists presupuestos (
  id                uuid primary key default gen_random_uuid(),
  alcance           text not null default 'global',
  referencia        text,
  tope_diario_usd   numeric(10,2) not null,
  tope_mensual_usd  numeric(10,2) not null,
  aviso_pct         smallint not null default 80,
  activo            boolean not null default true,
  actualizado       timestamptz not null default now(),
  constraint alcance_valido check (alcance in ('global','mission_type','estrategia'))
);

-- ── vistas de gasto ──
create or replace view gasto_dia as
select
  (creado at time zone 'America/Argentina/Buenos_Aires')::date as dia,
  sum(coalesce(actual_cost_usd, estimated_cost_usd)) as gasto_usd,
  count(*) as llamadas,
  sum(busquedas_web) as busquedas
from costos_ia
group by 1;

create or replace view gasto_mes as
select
  date_trunc('month', creado at time zone 'America/Argentina/Buenos_Aires')::date as mes,
  sum(coalesce(actual_cost_usd, estimated_cost_usd)) as gasto_usd,
  count(*) as llamadas
from costos_ia
group by 1;

-- Costo por empresa aceptada · la métrica que decide si el sistema conviene
create or replace view costo_por_empresa as
select
  date_trunc('month', c.creado)::date as mes,
  sum(coalesce(c.actual_cost_usd, c.estimated_cost_usd)) as gasto_usd,
  count(distinct e.id) as empresas_nuevas,
  case when count(distinct e.id) > 0
    then round(sum(coalesce(c.actual_cost_usd, c.estimated_cost_usd)) / count(distinct e.id), 4)
    else null end as usd_por_empresa
from costos_ia c
left join hallazgos h on h.mision_id = c.mision_id and h.estado = 'aceptado'
left join empresas e on e.origen_hallazgo_id = h.id
group by 1;

commit;
