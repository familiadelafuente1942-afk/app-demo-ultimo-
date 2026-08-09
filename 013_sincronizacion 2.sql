-- ════════════════════════════════════════════════════════════
-- 013 · SINCRONIZACIÓN MULTI-DISPOSITIVO
--
-- Agrega una columna para emparejar el id numérico que usa la app
-- (basado en timestamp, ej. 1785882822431) con el id real de Supabase.
-- Sin esto no se puede saber si un prospecto que llega desde un
-- dispositivo ya existe en la base o es nuevo.
-- ════════════════════════════════════════════════════════════

begin;

alter table empresas
  add column if not exists origen_local_id text;

create unique index if not exists empresas_origen_local_unico
  on empresas (origen_local_id) where origen_local_id is not null;

commit;
