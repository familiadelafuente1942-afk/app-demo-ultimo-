-- ════════════════════════════════════════════════════════════
-- PRUEBAS DE SEGURIDAD
-- Ejecutar en el SQL Editor de Supabase DESPUÉS de las migraciones.
-- Cada bloque debe dar el resultado indicado. Si alguno falla, no avanzar.
-- ════════════════════════════════════════════════════════════

-- ── 1 · RLS activada en todas las tablas ──
-- ESPERADO: 0 filas
select tablename as "TABLAS SIN RLS · deben ser cero"
from pg_tables t
where schemaname = 'public'
  and tablename in ('paises','provincias','partidos','localidades','denominadores',
                    'empresas','empresa_contactos','empresa_historial','empresa_obras',
                    'estrategias','mission_type_config','misiones','hallazgos','evidencias',
                    'senales','costos_ia','precios_ia','presupuestos','audit_logs',
                    'aprobaciones','sistema_config')
  and not exists (
    select 1 from pg_class c
    join pg_namespace n on n.oid = c.relnamespace
    where c.relname = t.tablename and n.nspname = 'public' and c.relrowsecurity
  );

-- ── 2 · audit_logs no puede modificarse ni borrarse ──
-- ESPERADO: 0 filas
select policyname, cmd as "POLÍTICAS PELIGROSAS EN AUDIT · deben ser cero"
from pg_policies
where schemaname = 'public' and tablename = 'audit_logs' and cmd in ('UPDATE','DELETE');

-- ── 3 · el agente no puede cambiar la configuración del sistema ──
-- ESPERADO: 0 filas · si aparece algo, el agente podría reencenderse tras un apagado
select policyname, cmd as "SERVICE_ROLE ESCRIBIENDO CONFIG · debe ser cero"
from pg_policies
where schemaname = 'public' and tablename = 'sistema_config'
  and cmd in ('UPDATE','INSERT','ALL')
  and 'service_role' = any (roles);

-- ── 4 · un hallazgo sin evidencia no puede aceptarse ──
-- ESPERADO: error 'no puede aceptarse'
do $$
declare m uuid; h uuid; p uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into misiones (mission_type, pais_id, creada_por)
    values ('discovery', p, 'humano') returning id into m;
  insert into hallazgos (mision_id, datos_crudos, nombre_crudo)
    values (m, '{"empresa":"Prueba"}'::jsonb, 'Prueba') returning id into h;

  begin
    update hallazgos set estado = 'aceptado' where id = h;
    raise exception 'FALLA · se aceptó un hallazgo sin evidencia';
  exception when others then
    if sqlerrm like '%no puede aceptarse%' then
      raise notice 'OK · el trigger bloqueó la aceptación sin evidencia';
    else
      raise;
    end if;
  end;

  delete from hallazgos where id = h;
  delete from misiones where id = m;
end $$;

-- ── 5 · con evidencia sí se acepta ──
-- ESPERADO: notice 'OK'
do $$
declare m uuid; h uuid; p uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into misiones (mission_type, pais_id, creada_por)
    values ('discovery', p, 'humano') returning id into m;
  insert into hallazgos (mision_id, datos_crudos, nombre_crudo)
    values (m, '{"empresa":"Prueba"}'::jsonb, 'Prueba') returning id into h;
  insert into evidencias (hallazgo_id, tipo, url)
    values (h, 'sitio_institucional', 'https://ejemplo.com.ar');

  update hallazgos set estado = 'aceptado' where id = h;
  raise notice 'OK · con evidencia el hallazgo se acepta';

  delete from evidencias where hallazgo_id = h;
  delete from hallazgos where id = h;
  delete from misiones where id = m;
end $$;

-- ── 6 · una evidencia sin URL ni identificador es inválida ──
-- ESPERADO: error de restricción
do $$
declare m uuid; h uuid; p uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into misiones (mission_type, pais_id, creada_por)
    values ('discovery', p, 'humano') returning id into m;
  insert into hallazgos (mision_id, datos_crudos) values (m, '{}'::jsonb) returning id into h;
  begin
    insert into evidencias (hallazgo_id, tipo) values (h, 'sitio_institucional');
    raise exception 'FALLA · se aceptó una evidencia sin respaldo';
  exception when check_violation then
    raise notice 'OK · la evidencia sin URL ni identificador fue rechazada';
  end;
  delete from hallazgos where id = h;
  delete from misiones where id = m;
end $$;

-- ── 7 · el Radar no puede vincular empresa sin hallazgo ──
-- ESPERADO: error de restricción
do $$
declare e uuid; p uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into empresas (nombre, pais_id) values ('Empresa de prueba radar', p) returning id into e;
  begin
    insert into senales (tipo, empresa_id, titulo, fecha_evento, fuente, url, ventana_dias)
    values ('empresa_nueva', e, 'Prueba', current_date, 'boletin', 'https://x.com', 30);
    raise exception 'FALLA · una señal vinculó una empresa sin pasar por hallazgo';
  exception when check_violation then
    raise notice 'OK · el Radar no puede crear vínculos sin hallazgo';
  end;
  delete from empresas where id = e;
end $$;

-- ── 8 · el CUIT verificado es único ──
-- ESPERADO: error de unicidad
do $$
declare p uuid; a uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into empresas (nombre, pais_id, cuit, cuit_verificado)
    values ('Empresa A', p, '30123456789', true) returning id into a;
  begin
    insert into empresas (nombre, pais_id, cuit, cuit_verificado)
      values ('Empresa B', p, '30123456789', true);
    raise exception 'FALLA · se permitieron dos empresas con el mismo CUIT verificado';
  exception when unique_violation then
    raise notice 'OK · el CUIT verificado no admite duplicados';
  end;
  delete from empresas where cuit = '30123456789';
end $$;

-- ── 9 · los dominios genéricos no bloquean ──
-- ESPERADO: notice 'OK' · dos empresas pueden compartir gmail.com
do $$
declare p uuid;
begin
  select id into p from paises where codigo = 'AR';
  insert into empresas (nombre, pais_id, web) values ('Genérica A', p, 'https://gmail.com');
  insert into empresas (nombre, pais_id, web) values ('Genérica B', p, 'https://gmail.com');
  raise notice 'OK · los dominios genéricos no se usan para fusionar';
  delete from empresas where nombre in ('Genérica A','Genérica B');
end $$;

-- ── 10 · la cobertura sin denominador da null, no un número ──
-- ESPERADO: cobertura_pct en null
select localidad, estimadas, encontradas, cobertura_pct as "DEBE SER NULL SIN DENOMINADOR"
from cobertura_localidad
where estimadas is null
limit 5;

-- ── 11 · el interruptor de emergencia frena tomar_mision ──
-- ESPERADO: notice 'OK'
do $$
declare m misiones;
begin
  update sistema_config set valor = 'false'::jsonb where clave = 'ejecucion_habilitada';
  select * into m from tomar_mision(10);
  if m.id is null then
    raise notice 'OK · con la ejecución deshabilitada no se toman misiones';
  else
    raise exception 'FALLA · se tomó una misión con el sistema apagado';
  end if;
  update sistema_config set valor = 'true'::jsonb where clave = 'ejecucion_habilitada';
end $$;

-- ── 12 · resumen ──
select
  (select count(*) from pg_policies where schemaname='public') as politicas,
  (select count(*) from paises) as paises,
  (select count(*) from provincias) as provincias,
  (select count(*) from mission_type_config) as tipos_mision,
  (select count(*) from presupuestos where activo) as presupuestos_activos;
