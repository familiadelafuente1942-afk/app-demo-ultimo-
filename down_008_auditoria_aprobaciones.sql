-- Revierte 008.
begin;
drop table if exists sistema_config;
drop table if exists aprobaciones;
drop table if exists audit_logs;
commit;
