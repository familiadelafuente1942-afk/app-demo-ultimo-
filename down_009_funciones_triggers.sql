-- Revierte 009 · quita funciones, triggers y vistas.
begin;
drop view if exists estado_barrido;
drop view if exists cobertura_localidad;
drop trigger if exists trg_auditar_empresa on empresas;
drop trigger if exists trg_empresa_origen on empresas;
drop trigger if exists trg_hallazgo_requiere_evidencia on hallazgos;
drop trigger if exists trg_empresas_antes_guardar on empresas;
drop function if exists liberar_misiones_colgadas();
drop function if exists tomar_mision(integer);
drop function if exists auditar_empresa();
drop function if exists empresa_origen_valido();
drop function if exists validar_evidencia_hallazgo();
drop function if exists empresas_antes_guardar();
drop function if exists dominio_generico(text);
drop function if exists normalizar_dominio(text);
drop function if exists normalizar_nombre(text);
commit;
