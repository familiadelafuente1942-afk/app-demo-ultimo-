-- Revierte 001 · los tipos solo se borran si ninguna tabla los usa.
begin;
drop type if exists coverage_method;
drop type if exists signal_type;
drop type if exists signal_status;
drop type if exists company_status;
drop type if exists evidence_type;
drop type if exists finding_status;
drop type if exists mission_status;
drop type if exists mission_type;
-- Las extensiones se dejan: otras cosas pueden depender de ellas.
-- drop extension if exists pg_trgm;
commit;
