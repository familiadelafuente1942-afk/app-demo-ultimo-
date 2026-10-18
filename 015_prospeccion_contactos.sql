-- Contactos completos de cada prospecto (teléfono, WhatsApp, LinkedIn, Instagram) y claves para no duplicar.
begin;
alter table mkt_prospectos add column if not exists telefono text;
alter table mkt_prospectos add column if not exists whatsapp text;
alter table mkt_prospectos add column if not exists linkedin text;
alter table mkt_prospectos add column if not exists instagram text;
alter table mkt_prospectos add column if not exists direccion text;
alter table mkt_prospectos add column if not exists wa_estado text not null default 'sin_contactar';
create unique index if not exists mkt_prospectos_whatsapp on mkt_prospectos (whatsapp) where whatsapp is not null;
create unique index if not exists mkt_prospectos_linkedin on mkt_prospectos (lower(linkedin)) where linkedin is not null;
create unique index if not exists mkt_prospectos_instagram on mkt_prospectos (lower(instagram)) where instagram is not null;
commit;
