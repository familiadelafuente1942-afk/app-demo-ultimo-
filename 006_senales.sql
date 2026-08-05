-- ════════════════════════════════════════════════════════════
-- 006 · SEÑALES · RADAR COMERCIAL
-- El Radar NO crea empresas. Toda señal que menciona una empresa
-- pasa obligatoriamente por hallazgo → evidencia → validación → dedup.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists senales (
  id                uuid primary key default gen_random_uuid(),
  tipo              signal_type not null,
  mision_id         uuid references misiones(id) on delete set null,

  -- vinculación
  empresa_id        uuid references empresas(id) on delete set null,
  empresa_nombre_crudo text,
  provincia_id      uuid references provincias(id) on delete set null,
  localidad_id      uuid references localidades(id) on delete set null,

  -- contenido
  titulo            text not null,
  descripcion       text,
  fecha_evento      date not null,
  fecha_deteccion   timestamptz not null default now(),
  monto_estimado    numeric(14,2),

  -- origen · sin URL no hay señal
  fuente            text not null,
  url               text not null,
  confianza         smallint check (confianza between 0 and 100),
  verificada_humano boolean not null default false,

  -- comercial
  puntaje           smallint check (puntaje between 0 and 100),
  ventana_dias      smallint not null,
  vence             date generated always as (fecha_evento + ventana_dias::integer) stored,
  estado            signal_status not null default 'detectada',
  accion_tomada     text,

  -- el hallazgo por el que pasó
  hallazgo_id       uuid references hallazgos(id) on delete set null,

  creada            timestamptz not null default now(),

  -- REGLA CENTRAL: una señal solo puede apuntar a una empresa
  -- si pasó por un hallazgo. El Radar nunca crea empresas directo.
  constraint senal_no_crea_empresa
    check (empresa_id is null or hallazgo_id is not null)
);

comment on constraint senal_no_crea_empresa on senales is
  'El Radar no puede vincular una empresa sin haber pasado por el circuito de hallazgo y evidencia.';

create index if not exists senales_vigentes on senales (puntaje desc, fecha_evento desc)
  where estado in ('detectada','verificada');
create index if not exists senales_vence on senales (vence) where estado <> 'vencida';
create index if not exists senales_empresa on senales (empresa_id);
create index if not exists senales_tipo on senales (tipo, fecha_evento desc);

-- la FK diferida de hallazgos hacia la señal que lo originó
alter table hallazgos drop constraint if exists hallazgos_senal_fk;
alter table hallazgos
  add constraint hallazgos_senal_fk
  foreign key (senal_id) references senales(id) on delete set null;

create index if not exists hallazgos_senal on hallazgos (senal_id) where senal_id is not null;

commit;
