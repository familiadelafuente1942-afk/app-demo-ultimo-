-- Revierte 010 · quita políticas y desactiva RLS.
-- ATENCIÓN: deja las tablas sin protección. Solo para revertir una migración fallida.
begin;
do $$
declare r record;
begin
  for r in
    select schemaname, tablename, policyname from pg_policies where schemaname = 'public'
  loop
    execute format('drop policy if exists %I on %I.%I', r.policyname, r.schemaname, r.tablename);
  end loop;
end $$;

alter table if exists sistema_config      disable row level security;
alter table if exists aprobaciones        disable row level security;
alter table if exists audit_logs          disable row level security;
alter table if exists presupuestos        disable row level security;
alter table if exists precios_ia          disable row level security;
alter table if exists costos_ia           disable row level security;
alter table if exists senales             disable row level security;
alter table if exists evidencias          disable row level security;
alter table if exists hallazgos           disable row level security;
alter table if exists misiones            disable row level security;
alter table if exists mission_type_config disable row level security;
alter table if exists estrategias         disable row level security;
alter table if exists empresa_obras       disable row level security;
alter table if exists empresa_historial   disable row level security;
alter table if exists empresa_contactos   disable row level security;
alter table if exists empresas            disable row level security;
alter table if exists denominadores       disable row level security;
alter table if exists localidades         disable row level security;
alter table if exists partidos            disable row level security;
alter table if exists provincias          disable row level security;
alter table if exists paises              disable row level security;
commit;
