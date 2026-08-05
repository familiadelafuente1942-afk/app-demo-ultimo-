-- ════════════════════════════════════════════════════════════
-- 008 · AUDITORÍA Y APROBACIONES
-- audit_logs es de solo inserción: sin políticas de update ni delete.
-- ════════════════════════════════════════════════════════════

begin;

create table if not exists audit_logs (
  id            bigserial primary key,
  actor_tipo    text not null,
  actor_id      text,
  accion        text not null,
  entidad       text not null,
  entidad_id    uuid,
  valor_antes   jsonb,
  valor_despues jsonb,
  mision_id     uuid,
  aprobacion_id uuid,
  costo_usd     numeric(12,6),
  creado        timestamptz not null default now(),
  constraint audit_actor_valido check (actor_tipo in ('humano','agente','sistema'))
);

create index if not exists audit_entidad on audit_logs (entidad, entidad_id, creado desc);
create index if not exists audit_fecha on audit_logs (creado desc);
create index if not exists audit_mision on audit_logs (mision_id) where mision_id is not null;

comment on table audit_logs is
  'Solo inserción. No hay políticas de update ni delete, así que nadie puede alterar el registro.';

-- ── aprobaciones humanas ──
create table if not exists aprobaciones (
  id            uuid primary key default gen_random_uuid(),
  tipo          text not null,
  descripcion   text not null,
  carga         jsonb not null,
  entidad       text,
  entidad_id    uuid,
  estado        text not null default 'pendiente',
  solicitada    timestamptz not null default now(),
  vence         timestamptz not null default (now() + interval '48 hours'),
  resuelta      timestamptz,
  resuelta_por  uuid references auth.users(id) on delete set null,
  comentario    text,
  constraint aprobacion_tipo_valido check (
    tipo in ('fusion','estrategia','denominador','accion_externa','autonomia','contacto')
  ),
  constraint aprobacion_estado_valido check (
    estado in ('pendiente','aprobada','rechazada','vencida')
  )
);

create index if not exists aprobaciones_pendientes on aprobaciones (solicitada desc)
  where estado = 'pendiente';
create index if not exists aprobaciones_vence on aprobaciones (vence) where estado = 'pendiente';

-- ── interruptor de emergencia ──
create table if not exists sistema_config (
  clave       text primary key,
  valor       jsonb not null,
  descripcion text,
  actualizado timestamptz not null default now(),
  actualizado_por uuid references auth.users(id) on delete set null
);

insert into sistema_config (clave, valor, descripcion) values
  ('ejecucion_habilitada', 'true'::jsonb,
   'Interruptor general. En false, ningún agente ejecuta nada.'),
  ('modo_autonomia', '"supervisado"'::jsonb,
   'supervisado | nocturno. Solo pasa a nocturno cumpliendo los criterios de la sección 14.'),
  ('ventana_horaria', '{"desde":"22:00","hasta":"06:00"}'::jsonb,
   'Franja en la que puede correr el cron cuando esté en modo nocturno.'),
  ('misiones_por_corrida', '1'::jsonb,
   'Una misión por invocación. No cambiar sin revisar el timeout de las Edge Functions.')
on conflict (clave) do nothing;

commit;
