# Carga de geografía argentina

## Por qué no está escrita en el código

Las 24 provincias sí están en `seed/011_semillas.sql`: son pocas y las puedo
afirmar con certeza, con sus códigos ISO.

Los ~530 departamentos y ~2.300 localidades **no**. Escribirlos de memoria
produciría nombres mal escritos, localidades inexistentes y localidades
faltantes, y después esos errores se propagan a cada misión y a cada
cálculo de cobertura.

## De dónde bajar los datos oficiales

Fuente: **Servicio de Normalización de Datos Geográficos de Argentina**,
publicado en datos.gob.ar bajo licencia abierta.

Buscar el conjunto de datos de unidades territoriales, que incluye:

- `departamentos.csv` — departamentos y partidos
- `localidades.csv` — localidades con centroide

Guardarlos en una carpeta, por ejemplo `./datos-geo`.

## Cómo cargarlos

```bash
export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=eyJhb...

npm install @supabase/supabase-js
node scripts/cargar_geografia.mjs --dir ./datos-geo
```

## Para probar sin descargar nada

```bash
node scripts/cargar_geografia.mjs --subconjunto
```

Carga un subconjunto verificado: unas 25 unidades y 60 localidades de las
zonas donde más vas a operar (CABA, GBA Norte, La Plata, Mar del Plata,
Córdoba, Rosario, Mendoza, Neuquén, Bariloche).

Sirve para probar el mapa y las misiones. **No sirve para calcular
cobertura nacional**, porque el denominador quedaría incompleto.

## Verificación

```sql
select pr.nombre as provincia,
       count(distinct p.id) as departamentos,
       count(l.id) as localidades
from provincias pr
left join partidos p on p.provincia_id = pr.id
left join localidades l on l.partido_id = p.id
group by pr.nombre order by 3 desc;
```

Con la carga oficial completa el total debería rondar los 530 departamentos
y 2.300 localidades. Si da mucho menos, faltó procesar algún archivo.
