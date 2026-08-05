-- Revierte 007.
begin;
drop view if exists costo_por_empresa;
drop view if exists gasto_mes;
drop view if exists gasto_dia;
drop table if exists presupuestos;
drop table if exists precios_ia;
drop table if exists costos_ia;
commit;
