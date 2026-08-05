-- ════════════════════════════════════════════════════════════
-- 005 · HALLAZGOS Y EVIDENCIAS
-- Todo lo que produce la IA entra por acá. Nada llega a empresas
-- sin al menos una evidencia verificable.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists hallazgos (
  id                uuid primary key default gen_random_uuid(),
  mision_id         uuid not null references misiones(id) on delete cascade,
  senal_id          uuid,                    -- FK se agrega en 006

  -- lo que devolvió el modelo, sin tocar
  datos_crudos      jsonb not null,
  respuesta_completa text,

  -- extraído para poder comparar
  nombre_crudo      text,
  cuit_crudo        text,
  web_cruda         text,
  dominio_norm      text,
  localidad_cruda   text,

  -- procesamiento
  estado            finding_status not null default 'crudo',
  motivo_rechazo    text,
  empresa_id        uuid references empresas(id) on delete set null,
  candidato_de      uuid references empresas(id) on delete set null,
  similitud         numeric(5,2),

  creado            timestamptz not null default now(),
  procesado         timestamptz
);

comment on table hallazgos is
  'Guardar la respuesta cruda permite reprocesar con criterios nuevos sin volver a pagarle a la IA.';

create index if not exists hallazgos_mision on hallazgos (mision_id);
create index if not exists hallazgos_pendientes on hallazgos (estado)
  where estado in ('crudo','validado','revision');
create index if not exists hallazgos_dominio on hallazgos (dominio_norm)
  where dominio_norm is not null;
create index if not exists hallazgos_cuit on hallazgos (cuit_crudo)
  where cuit_crudo is not null;
create index if not exists hallazgos_empresa on hallazgos (empresa_id);

-- ── evidencias ──
create table if not exists evidencias (
  id              uuid primary key default gen_random_uuid(),
  hallazgo_id     uuid not null references hallazgos(id) on delete cascade,
  tipo            evidence_type not null,
  url             text,
  identificador   text,
  extracto        text,
  verificada      boolean not null default false,
  verificada_por  uuid references auth.users(id) on delete set null,
  verificada_el   timestamptz,
  creada          timestamptz not null default now(),

  -- Una evidencia sin URL ni identificador no es evidencia.
  constraint evidencia_tiene_respaldo
    check (url is not null or identificador is not null)
);

create index if not exists evidencias_hallazgo on evidencias (hallazgo_id);
create index if not exists evidencias_tipo on evidencias (tipo);

-- ── la FK diferida de empresas hacia su hallazgo de origen ──
alter table empresas drop constraint if exists empresas_origen_fk;
alter table empresas
  add constraint empresas_origen_fk
  foreign key (origen_hallazgo_id) references hallazgos(id) on delete set null;

create index if not exists empresas_origen on empresas (origen_hallazgo_id);

commit;
