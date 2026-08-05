-- ════════════════════════════════════════════════════════════
-- 009 · FUNCIONES Y TRIGGERS
-- Las reglas que no pueden violarse viven acá, no en la aplicación.
-- ════════════════════════════════════════════════════════════

begin;

-- ── normalización de nombre ──
create or replace function normalizar_nombre(txt text)
returns text language sql immutable as $$
  select trim(regexp_replace(
    regexp_replace(
      lower(coalesce(txt,'')),
      '\y(s\.?a\.?s?|s\.?r\.?l\.?|sociedad anonima|sociedad de responsabilidad limitada|ltda|inc|corp|el|la|los|las|de|del)\y',
      ' ', 'g'),
    '[^a-z0-9ñ ]', ' ', 'g'))
$$;

-- ── normalización de dominio ──
create or replace function normalizar_dominio(url text)
returns text language sql immutable as $$
  select nullif(split_part(
    regexp_replace(
      regexp_replace(lower(coalesce(url,'')), '^https?://', ''),
      '^www\.', ''),
    '/', 1), '')
$$;

-- ── dominios que NO sirven para fusionar ──
create or replace function dominio_generico(dom text)
returns boolean language sql immutable as $$
  select coalesce(dom,'') = any (array[
    'gmail.com','hotmail.com','yahoo.com','yahoo.com.ar','outlook.com','live.com',
    'wix.com','wixsite.com','wordpress.com','blogspot.com','blogspot.com.ar',
    'facebook.com','instagram.com','linkedin.com','twitter.com','x.com',
    'google.com','sites.google.com','mercadolibre.com.ar','wa.me'
  ])
$$;

comment on function dominio_generico is
  'Dos empresas distintas pueden compartir estos dominios. Nunca fusionan por dominio.';

-- ── mantener nombre_normalizado y dominio al día ──
create or replace function empresas_antes_guardar()
returns trigger language plpgsql as $$
begin
  new.nombre_normalizado := normalizar_nombre(new.nombre);
  new.dominio := normalizar_dominio(new.web);
  if dominio_generico(new.dominio) then
    new.dominio := null;   -- no sirve como identificador fuerte
  end if;
  new.actualizado := now();
  return new;
end $$;

drop trigger if exists trg_empresas_antes_guardar on empresas;
create trigger trg_empresas_antes_guardar
  before insert or update on empresas
  for each row execute function empresas_antes_guardar();

-- ── REGLA CENTRAL · un hallazgo no se acepta sin evidencia ──
create or replace function validar_evidencia_hallazgo()
returns trigger language plpgsql as $$
declare
  minimo smallint;
  cuantas integer;
begin
  if new.estado = 'aceptado' and (tg_op = 'INSERT' or old.estado is distinct from 'aceptado') then
    select coalesce(c.min_evidencias, 1) into minimo
    from misiones m
    left join mission_type_config c on c.mission_type = m.mission_type
    where m.id = new.mision_id;

    select count(*) into cuantas from evidencias where hallazgo_id = new.id;

    if cuantas < coalesce(minimo,1) then
      raise exception
        'Hallazgo % no puede aceptarse: tiene % evidencia(s) y necesita %.',
        new.id, cuantas, coalesce(minimo,1);
    end if;
  end if;
  return new;
end $$;

drop trigger if exists trg_hallazgo_requiere_evidencia on hallazgos;
create trigger trg_hallazgo_requiere_evidencia
  before insert or update on hallazgos
  for each row execute function validar_evidencia_hallazgo();

-- ── los agentes no escriben en empresas ──
-- Solo se permite si viene de un hallazgo aceptado o de un humano.
create or replace function empresa_origen_valido()
returns trigger language plpgsql as $$
declare
  rol text := nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role';
begin
  if rol = 'service_role' then
    if new.origen_hallazgo_id is null then
      raise exception
        'Un agente no puede crear una empresa sin origen_hallazgo_id. Debe pasar por el circuito de hallazgos.';
    end if;
    if not exists (
      select 1 from hallazgos
      where id = new.origen_hallazgo_id and estado in ('aceptado','duplicado')
    ) then
      raise exception
        'El hallazgo % no está aceptado. No puede promoverse a empresa.', new.origen_hallazgo_id;
    end if;
  end if;
  return new;
end $$;

drop trigger if exists trg_empresa_origen on empresas;
create trigger trg_empresa_origen
  before insert on empresas
  for each row execute function empresa_origen_valido();

-- ── auditoría automática de cambios en empresas ──
create or replace function auditar_empresa()
returns trigger language plpgsql as $$
declare
  rol text := coalesce(nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role', 'sistema');
  actor text := case when rol = 'service_role' then 'agente'
                     when rol = 'authenticated' then 'humano'
                     else 'sistema' end;
begin
  insert into audit_logs (actor_tipo, actor_id, accion, entidad, entidad_id, valor_antes, valor_despues)
  values (
    actor,
    nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub',
    lower(tg_op),
    'empresas',
    coalesce(new.id, old.id),
    case when tg_op in ('UPDATE','DELETE') then to_jsonb(old) end,
    case when tg_op in ('INSERT','UPDATE') then to_jsonb(new) end
  );
  return coalesce(new, old);
end $$;

drop trigger if exists trg_auditar_empresa on empresas;
create trigger trg_auditar_empresa
  after insert or update or delete on empresas
  for each row execute function auditar_empresa();

-- ── tomar una misión de la cola, sin colisiones ──
create or replace function tomar_mision(minutos_lease integer default 10)
returns misiones language plpgsql security definer as $$
declare
  m misiones;
  habilitado boolean;
begin
  select (valor)::text::boolean into habilitado
  from sistema_config where clave = 'ejecucion_habilitada';

  if not coalesce(habilitado, false) then
    return null;   -- interruptor de emergencia activado
  end if;

  update misiones set
    estado = 'en_ejecucion',
    inicio = now(),
    lease_hasta = now() + make_interval(mins => minutos_lease),
    intentos = intentos + 1
  where id = (
    select id from misiones
    where estado = 'pendiente' and programada <= now()
    order by urgente desc, prioridad desc, creada asc
    limit 1
    for update skip locked
  )
  returning * into m;

  return m;
end $$;

comment on function tomar_mision is
  'FOR UPDATE SKIP LOCKED impide que dos ejecutores tomen la misma misión.';

-- ── liberar misiones con arriendo vencido ──
create or replace function liberar_misiones_colgadas()
returns integer language plpgsql security definer as $$
declare liberadas integer;
begin
  with vencidas as (
    update misiones set
      estado = case when intentos >= max_intentos then 'fallida' else 'pendiente' end,
      lease_hasta = null,
      error = coalesce(error,'') || ' | El ejecutor no terminó antes del vencimiento del arriendo'
    where estado = 'en_ejecucion' and lease_hasta < now()
    returning 1
  )
  select count(*) into liberadas from vencidas;
  return liberadas;
end $$;

-- ── cobertura por localidad, solo con denominador verificado ──
create or replace view cobertura_localidad as
select
  l.id as localidad_id,
  l.nombre as localidad,
  p.nombre as partido,
  pr.nombre as provincia,
  l.ultimo_barrido,
  l.tipos_barridos,
  d.cantidad     as estimadas,
  d.fuente_nombre,
  d.fuente_fecha,
  d.metodo,
  count(e.id) filter (where e.activa) as encontradas,
  count(e.id) filter (where e.activa and e.estado <> 'no_investigada') as verificadas,
  -- Sin denominador verificado no hay porcentaje. Se aplica acá, no en la app.
  case
    when d.cantidad is null or d.cantidad = 0 or d.metodo = 'sin_datos' then null
    else round((count(e.id) filter (where e.activa))::numeric * 100 / d.cantidad, 2)
  end as cobertura_pct,
  case
    when d.cantidad is null then null
    else greatest(d.cantidad - count(e.id) filter (where e.activa), 0)
  end as pendientes
from localidades l
join partidos p on p.id = l.partido_id
join provincias pr on pr.id = p.provincia_id
left join denominadores d on d.localidad_id = l.id and d.tipo_empresa is null
left join empresas e on e.localidad_id = l.id
group by l.id, l.nombre, p.nombre, pr.nombre, l.ultimo_barrido, l.tipos_barridos,
         d.cantidad, d.fuente_nombre, d.fuente_fecha, d.metodo;

comment on view cobertura_localidad is
  'cobertura_pct es null cuando no hay denominador verificado. Nunca se inventa un porcentaje.';

-- ── estado de barrido para el mapa ──
create or replace view estado_barrido as
select
  l.id as localidad_id,
  l.nombre,
  p.provincia_id,
  case
    when exists (select 1 from misiones m where m.localidad_id = l.id and m.estado = 'en_ejecucion')
      then 'en_ejecucion'
    when l.ultimo_barrido is null then 'nunca'
    when l.ultimo_barrido < now() - interval '90 days' then 'vencido'
    when array_length(l.tipos_barridos, 1) >= 5 then 'completo'
    else 'parcial'
  end as estado_mapa
from localidades l
join partidos p on p.id = l.partido_id;

commit;
