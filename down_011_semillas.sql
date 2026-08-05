-- Revierte 011 · borra solo las semillas, no las tablas.
begin;
delete from estrategias where nombre in
  ('descubrimiento_web_general','descubrimiento_camaras','verificacion_sitio','radar_boletin_oficial');
delete from precios_ia where proveedor = 'anthropic';
delete from presupuestos where alcance = 'global';
delete from mission_type_config;
delete from provincias where pais_id = (select id from paises where codigo = 'AR');
delete from paises where codigo = 'AR';
commit;
