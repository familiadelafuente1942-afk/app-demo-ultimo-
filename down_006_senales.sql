-- Revierte 006.
begin;
alter table if exists hallazgos drop constraint if exists hallazgos_senal_fk;
drop table if exists senales;
commit;
