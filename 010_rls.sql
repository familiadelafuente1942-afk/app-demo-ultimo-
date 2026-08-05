-- ════════════════════════════════════════════════════════════
-- 010 · SEGURIDAD A NIVEL DE FILA
-- Sin políticas, RLS bloquea todo. Lo que no está permitido, no pasa.
-- ════════════════════════════════════════════════════════════

begin;

alter table paises              enable row level security;
alter table provincias          enable row level security;
alter table partidos            enable row level security;
alter table localidades         enable row level security;
alter table denominadores       enable row level security;
alter table empresas            enable row level security;
alter table empresa_contactos   enable row level security;
alter table empresa_historial   enable row level security;
alter table empresa_obras       enable row level security;
alter table estrategias         enable row level security;
alter table mission_type_config enable row level security;
alter table misiones            enable row level security;
alter table hallazgos           enable row level security;
alter table evidencias          enable row level security;
alter table senales             enable row level security;
alter table costos_ia           enable row level security;
alter table precios_ia          enable row level security;
alter table presupuestos        enable row level security;
alter table audit_logs          enable row level security;
alter table aprobaciones        enable row level security;
alter table sistema_config      enable row level security;

-- ══ GEOGRAFÍA · lectura para todos los autenticados, escritura solo servidor ══
create policy geo_leer_paises      on paises      for select to authenticated using (true);
create policy geo_leer_provincias  on provincias  for select to authenticated using (true);
create policy geo_leer_partidos    on partidos    for select to authenticated using (true);
create policy geo_leer_localidades on localidades for select to authenticated using (true);
create policy geo_leer_denom       on denominadores for select to authenticated using (true);

create policy geo_srv_paises      on paises      for all to service_role using (true) with check (true);
create policy geo_srv_provincias  on provincias  for all to service_role using (true) with check (true);
create policy geo_srv_partidos    on partidos    for all to service_role using (true) with check (true);
create policy geo_srv_localidades on localidades for all to service_role using (true) with check (true);
create policy geo_srv_denom       on denominadores for all to service_role using (true) with check (true);

-- El humano puede cargar denominadores a mano
create policy denom_humano on denominadores for insert to authenticated with check (true);
create policy denom_humano_upd on denominadores for update to authenticated using (true);

-- ══ EMPRESAS ══
create policy emp_leer on empresas for select to authenticated using (true);
create policy emp_crear on empresas for insert to authenticated with check (true);
create policy emp_editar on empresas for update to authenticated using (true);
create policy emp_borrar on empresas for delete to authenticated using (true);
-- El agente puede escribir, pero el trigger empresa_origen_valido le exige
-- que venga de un hallazgo aceptado.
create policy emp_srv on empresas for all to service_role using (true) with check (true);

create policy cont_leer on empresa_contactos for select to authenticated using (true);
create policy cont_escribir on empresa_contactos for all to authenticated using (true) with check (true);
create policy cont_srv on empresa_contactos for all to service_role using (true) with check (true);

create policy hist_leer on empresa_historial for select to authenticated using (true);
create policy hist_srv on empresa_historial for insert to service_role with check (true);
create policy hist_humano on empresa_historial for insert to authenticated with check (true);
-- Sin update ni delete: el historial no se edita.

create policy obras_leer on empresa_obras for select to authenticated using (true);
create policy obras_srv on empresa_obras for all to service_role using (true) with check (true);

-- ══ MISIONES ══
create policy mis_leer on misiones for select to authenticated using (true);
-- El humano solo crea misiones marcadas como propias.
create policy mis_crear_humano on misiones for insert to authenticated
  with check (creada_por = 'humano');
create policy mis_editar_humano on misiones for update to authenticated using (true);
create policy mis_srv on misiones for all to service_role using (true) with check (true);

create policy estr_leer on estrategias for select to authenticated using (true);
-- Las estrategias las modifica el humano. El agente solo suma métricas.
create policy estr_editar on estrategias for update to authenticated using (true);
create policy estr_crear on estrategias for insert to authenticated with check (true);
create policy estr_srv_leer on estrategias for select to service_role using (true);
create policy estr_srv_metricas on estrategias for update to service_role using (true) with check (true);

create policy mtc_leer on mission_type_config for select to authenticated using (true);
create policy mtc_editar on mission_type_config for update to authenticated using (true);
create policy mtc_srv on mission_type_config for select to service_role using (true);

-- ══ HALLAZGOS Y EVIDENCIAS ══
create policy hall_leer on hallazgos for select to authenticated using (true);
create policy hall_editar on hallazgos for update to authenticated using (true);
create policy hall_srv on hallazgos for all to service_role using (true) with check (true);

create policy evi_leer on evidencias for select to authenticated using (true);
create policy evi_editar on evidencias for update to authenticated using (true);
create policy evi_srv on evidencias for all to service_role using (true) with check (true);

-- ══ SEÑALES ══
create policy sen_leer on senales for select to authenticated using (true);
create policy sen_editar on senales for update to authenticated using (true);
create policy sen_srv on senales for all to service_role using (true) with check (true);

-- ══ COSTOS ══
create policy cost_leer on costos_ia for select to authenticated using (true);
create policy cost_srv on costos_ia for insert to service_role with check (true);
create policy cost_srv_upd on costos_ia for update to service_role using (true) with check (true);
-- El humano no edita costos: son el registro de lo que se gastó.

create policy prec_leer on precios_ia for select to authenticated using (true);
create policy prec_editar on precios_ia for all to authenticated using (true) with check (true);
create policy prec_srv on precios_ia for select to service_role using (true);

create policy pres_leer on presupuestos for select to authenticated using (true);
create policy pres_editar on presupuestos for all to authenticated using (true) with check (true);
create policy pres_srv on presupuestos for select to service_role using (true);

-- ══ AUDITORÍA · solo se agrega ══
create policy audit_leer on audit_logs for select to authenticated using (true);
create policy audit_srv_insert on audit_logs for insert to service_role with check (true);
create policy audit_humano_insert on audit_logs for insert to authenticated with check (true);
-- Deliberadamente NO hay políticas de update ni delete.
-- Con RLS activada, eso significa que nadie puede modificar ni borrar un asiento.

-- ══ APROBACIONES · solo el humano resuelve ══
create policy apr_leer on aprobaciones for select to authenticated using (true);
create policy apr_resolver on aprobaciones for update to authenticated using (true);
create policy apr_srv_crear on aprobaciones for insert to service_role with check (true);
create policy apr_srv_leer on aprobaciones for select to service_role using (true);
-- El agente puede pedir aprobación pero no aprobarse a sí mismo.

-- ══ CONFIGURACIÓN · el interruptor de emergencia ══
create policy cfg_leer on sistema_config for select to authenticated using (true);
create policy cfg_editar on sistema_config for update to authenticated using (true);
create policy cfg_srv_leer on sistema_config for select to service_role using (true);
-- El agente lee la configuración pero no puede cambiarla:
-- no puede volver a encenderse solo después de un apagado de emergencia.

commit;
