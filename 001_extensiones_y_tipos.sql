-- ════════════════════════════════════════════════════════════
-- 001 · EXTENSIONES Y TIPOS
-- Reversible con: rollback/down_001_extensiones_y_tipos.sql
-- ════════════════════════════════════════════════════════════

begin;

-- pg_trgm da la similitud de texto que usa la deduplicación.
create extension if not exists pg_trgm;
create extension if not exists pgcrypto;   -- gen_random_uuid()

-- ── tipos de misión ──
do $$ begin
  create type mission_type as enum (
    'discovery',
    'enrichment',
    'verification',
    'contact_research',
    'radar',
    'coverage_estimation'
  );
exception when duplicate_object then null; end $$;

do $$ begin
  create type mission_status as enum (
    'pendiente', 'en_ejecucion', 'completada', 'revision', 'cancelada', 'fallida'
  );
exception when duplicate_object then null; end $$;

-- ── hallazgos ──
do $$ begin
  create type finding_status as enum (
    'crudo', 'validado', 'aceptado', 'rechazado', 'duplicado', 'revision'
  );
exception when duplicate_object then null; end $$;

-- ── evidencias · lista cerrada aprobada ──
do $$ begin
  create type evidence_type as enum (
    'cuit',
    'identificador_oficial',
    'ieric',
    'boletin_oficial',
    'camara_empresarial',
    'portal_publico',
    'sitio_institucional',
    'perfil_institucional',
    'documento_oficial'
  );
exception when duplicate_object then null; end $$;

-- ── empresas ──
do $$ begin
  create type company_status as enum (
    'no_investigada', 'investigada', 'calificada', 'cliente', 'descartada'
  );
exception when duplicate_object then null; end $$;

-- ── radar ──
do $$ begin
  create type signal_status as enum (
    'detectada', 'verificada', 'procesada', 'descartada', 'vencida'
  );
exception when duplicate_object then null; end $$;

do $$ begin
  create type signal_type as enum (
    'licitacion_ganada', 'desarrollo_anunciado', 'empresa_nueva',
    'busquedas_laborales', 'sucursal_nueva', 'permiso_obra', 'cambio_autoridades'
  );
exception when duplicate_object then null; end $$;

-- ── cobertura ──
do $$ begin
  create type coverage_method as enum (
    'padron_oficial', 'extrapolacion', 'sin_datos'
  );
exception when duplicate_object then null; end $$;

commit;
