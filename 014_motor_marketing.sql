-- ═════════════════════════════════════════════════════════════
-- 014 · MOTOR DE MARKETING IA
-- Cola de aprobación, topes de envío, bajas, auditoría y prospectos
-- del motor de marketing del Centro de Operaciones.
-- Se corre una sola vez en Supabase (SQL Editor).
-- El acceso es solo para los mails de la tabla mkt_admins.
-- ═════════════════════════════════════════════════════════════
begin;

create table if not exists mkt_admins (
  email text primary key
);
insert into mkt_admins (email) values ('nexoentorno@gmail.com') on conflict do nothing;

create or replace function es_admin_motor() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from mkt_admins where lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));
$$;

-- Configuración y interruptor de frenado (una sola fila)
create table if not exists mkt_motor_config (
  id int primary key default 1 check (id = 1),
  activo boolean not null default false,          -- false = el motor NO envía ni publica nada
  tope_mails_dia int not null default 30,         -- tope máximo diario de mails
  rampa boolean not null default true,            -- sube de a poco (calentamiento)
  tope_posts_dia int not null default 6,
  remitente text,
  primer_envio date,
  actualizado timestamptz not null default now()
);
insert into mkt_motor_config (id) values (1) on conflict do nothing;

-- Cola de aprobación: todo lo que sale pasa por acá
create table if not exists mkt_cola (
  id uuid primary key default gen_random_uuid(),
  tipo text not null check (tipo in ('mail','post')),
  canal text not null check (canal in ('email','linkedin','instagram','facebook')),
  pais text,
  idioma text check (idioma in ('es','en','pt')),
  destino text,                                   -- mail del destinatario (solo tipo mail)
  asunto text,
  cuerpo text not null,
  meta jsonb not null default '{}'::jsonb,
  estado text not null default 'pendiente'
    check (estado in ('pendiente','aprobado','rechazado','enviado','error','cancelado')),
  programado_para timestamptz,
  enviado_en timestamptz,
  error text,
  aprobado_por text,
  creado timestamptz not null default now()
);
create index if not exists mkt_cola_estado on mkt_cola (estado, tipo, creado);

create table if not exists mkt_prospectos (
  id uuid primary key default gen_random_uuid(),
  empresa text not null,
  contacto text,
  email text,
  web text,
  pais text,
  ciudad text,
  idioma text,
  rubro text,
  puntaje int not null default 0,
  fuente text,
  estado text not null default 'nuevo',
  creado timestamptz not null default now()
);
create unique index if not exists mkt_prospectos_email on mkt_prospectos (lower(email)) where email is not null;
create unique index if not exists mkt_prospectos_web on mkt_prospectos (lower(web)) where web is not null;

create table if not exists mkt_bajas (
  email text primary key,
  creado timestamptz not null default now()
);

create table if not exists mkt_auditoria (
  id bigserial primary key,
  creado timestamptz not null default now(),
  actor text,
  accion text not null,
  detalle jsonb not null default '{}'::jsonb
);

-- Seguridad: solo los administradores del motor
alter table mkt_admins enable row level security;
alter table mkt_motor_config enable row level security;
alter table mkt_cola enable row level security;
alter table mkt_prospectos enable row level security;
alter table mkt_bajas enable row level security;
alter table mkt_auditoria enable row level security;

do $$ declare t text; begin
  foreach t in array array['mkt_admins','mkt_motor_config','mkt_cola','mkt_prospectos','mkt_bajas','mkt_auditoria'] loop
    execute format('drop policy if exists motor_admin on %I', t);
    execute format('create policy motor_admin on %I for all to authenticated using (es_admin_motor()) with check (es_admin_motor())', t);
  end loop;
end $$;

commit;
