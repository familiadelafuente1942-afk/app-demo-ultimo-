-- Revierte 005.
begin;
alter table if exists empresas drop constraint if exists empresas_origen_fk;
drop table if exists evidencias;
drop table if exists hallazgos;
commit;
