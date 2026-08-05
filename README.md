# ETAPA A · Infraestructura y esquema

Todo lo que sigue vive en carpetas nuevas. **No se modifica ningún archivo de
las cinco aplicaciones existentes.** El único cambio que van a necesitar más
adelante es apuntar a la base nueva, y eso se hace en una etapa posterior con
tu autorización explícita.

---

## 1 · Estructura de carpetas

```
etapa-a/
├── .env.example                  plantilla de variables
├── README.md                     este archivo
├── docs/
│   └── GEOGRAFIA.md              de dónde salen los datos geográficos
├── scripts/
│   ├── cargar_geografia.mjs      ingiere el dataset oficial
│   └── migrar_indexeddb.mjs      sube tus prospectos actuales
└── supabase/
    ├── migrations/               se ejecutan en orden
    │   ├── 001_extensiones_y_tipos.sql
    │   ├── 002_geografia.sql
    │   ├── 003_empresas.sql
    │   ├── 004_misiones.sql
    │   ├── 005_hallazgos_evidencias.sql
    │   ├── 006_senales.sql
    │   ├── 007_costos_presupuestos.sql
    │   ├── 008_auditoria_aprobaciones.sql
    │   ├── 009_funciones_triggers.sql
    │   └── 010_rls.sql
    ├── seed/
    │   └── 011_semillas.sql      país, 24 provincias, configuración
    ├── rollback/
    │   └── down_001 … down_011   uno por migración
    └── tests/
        └── rls_pruebas.sql       12 pruebas de seguridad y reglas
```

---

## 2 · Crear el proyecto Supabase

**Esto lo hacés vos.** No tengo acceso a tu cuenta ni puedo crear el proyecto.

1. Entrá a `supabase.com` y creá una cuenta si no tenés
2. **New project**
   - Nombre: `construia`
   - Contraseña de la base: generala y **guardala en un gestor de contraseñas**
   - Región: **South America (São Paulo)** — la más cercana, menor latencia
   - Plan: Free alcanza para la Etapa A. Pro (USD 25/mes) hace falta para las
     copias de seguridad diarias y la recuperación a un punto en el tiempo,
     que son requisito antes de habilitar la autonomía.
3. Esperá a que termine de aprovisionar, unos dos minutos
4. **Settings → API**, copiá:
   - Project URL → `VITE_SUPABASE_URL` y `SUPABASE_URL`
   - `anon public` → `VITE_SUPABASE_ANON_KEY`
   - `service_role secret` → `SUPABASE_SERVICE_ROLE_KEY`

### Sobre la clave `service_role`

Salta toda la seguridad de RLS. Con ella se puede leer, modificar y borrar
cualquier fila de cualquier tabla.

- Va **solo** en variables de entorno del servidor
- **Nunca** en el navegador, ni en el código, ni en el repositorio
- Si alguna vez se filtra: Settings → API → **Reset service key**

### Autenticación

**Authentication → Providers → Email**: dejalo activado y desactivá
"Enable email signups". Los usuarios los creás vos a mano desde
**Authentication → Users → Add user**. Así nadie se registra por su cuenta.

---

## 3 · Orden exacto de ejecución

En **SQL Editor → New query**, pegá y ejecutá **uno por uno, en este orden**.
Cada archivo es una transacción: si algo falla, no queda a medias.

| # | Archivo | Qué crea | Si falla, revertir con |
|---|---|---|---|
| 1 | `migrations/001_extensiones_y_tipos.sql` | Extensiones y 8 tipos enum | `rollback/down_001_...` |
| 2 | `migrations/002_geografia.sql` | Jerarquía geográfica y denominadores | `down_002_...` |
| 3 | `migrations/003_empresas.sql` | Empresas, contactos, historial, obras | `down_003_...` |
| 4 | `migrations/004_misiones.sql` | Estrategias, misiones, config por tipo | `down_004_...` |
| 5 | `migrations/005_hallazgos_evidencias.sql` | Hallazgos y evidencias | `down_005_...` |
| 6 | `migrations/006_senales.sql` | Señales del Radar | `down_006_...` |
| 7 | `migrations/007_costos_presupuestos.sql` | Costos, precios, topes y vistas | `down_007_...` |
| 8 | `migrations/008_auditoria_aprobaciones.sql` | Auditoría, aprobaciones, interruptor | `down_008_...` |
| 9 | `migrations/009_funciones_triggers.sql` | Reglas, `tomar_mision`, vistas | `down_009_...` |
| 10 | `migrations/010_rls.sql` | Todas las políticas de seguridad | `down_010_...` |
| 11 | `seed/011_semillas.sql` | País, 24 provincias, configuración | `down_011_...` |

**Para revertir varias:** ejecutar los `down_` en orden **inverso**. Para
deshacer todo: `down_011` → `down_010` → … → `down_001`.

**Antes de empezar:** Database → Backups → tomá una copia manual. Con el
proyecto vacío no cuesta nada y te deja un punto de retorno limpio.

---

## 4 · Cargar la geografía

```bash
cd etapa-a
npm install @supabase/supabase-js

export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=eyJhb...

# Opción A · subconjunto verificado, para probar ya
node scripts/cargar_geografia.mjs --subconjunto

# Opción B · carga oficial completa (ver docs/GEOGRAFIA.md)
node scripts/cargar_geografia.mjs --dir ./datos-geo
```

**Empezá por la A.** Te deja el mapa funcionando en minutos con las zonas donde
más vas a operar. La B la corrés cuando bajes los archivos oficiales.

---

## 5 · Pruebas de seguridad

Ejecutar `supabase/tests/rls_pruebas.sql` completo en el SQL Editor.

Las doce pruebas verifican:

| # | Qué comprueba |
|---|---|
| 1 | RLS activada en las 21 tablas |
| 2 | `audit_logs` no admite modificación ni borrado |
| 3 | El agente no puede cambiar la configuración del sistema |
| 4 | Un hallazgo **sin evidencia no puede aceptarse** |
| 5 | Con evidencia sí se acepta |
| 6 | Una evidencia sin URL ni identificador es rechazada |
| 7 | El Radar **no puede vincular empresa sin hallazgo** |
| 8 | El CUIT verificado es único |
| 9 | Los dominios genéricos no bloquean altas legítimas |
| 10 | Sin denominador, la cobertura es `null` y no un número |
| 11 | El interruptor de emergencia frena `tomar_mision` |
| 12 | Resumen de conteos |

**Si alguna falla, no avances.** Cada una corresponde a una regla que aprobaste.

---

## 6 · Migración desde IndexedDB

### Qué se migra

Tus prospectos actuales viven en IndexedDB del navegador, en la tabla
`prospectos`, con el formato que veníamos usando.

| Campo actual | Destino |
|---|---|
| `empresa` | `empresas.nombre` |
| `nombre` | `empresa_contactos.nombre` |
| `rol` | `empresas.tipo` |
| `mail` | `empresas.email` |
| `tel` | `empresas.telefono` |
| `web` | `empresas.web` → genera `dominio` |
| `zona` | se resuelve contra `localidades` |
| `dolor` | `empresas.observaciones` |
| `estado` | `empresas.estado` (equivalencia abajo) |
| `historial[]` | `empresa_historial` |

Equivalencia de estados:

```
nuevo       → no_investigada
contactado  → investigada
reunión     → calificada
propuesta   → calificada
cerrado     → cliente
perdido     → descartada
```

### Cómo se hace

1. En la app: **Base de datos → Descargar base**. Queda un
   `construia-backup-AAAA-MM-DD.json`
2. `node scripts/migrar_indexeddb.mjs --archivo construia-backup-2026-08-05.json --simular`
3. Revisar el informe: cuántas se van a crear, cuántas no tienen zona
   reconocible, cuántas quedan sin geolocalizar
4. Si está bien, correr sin `--simular`

### Reglas de la migración

- **Nada se borra.** El archivo JSON queda intacto y la IndexedDB también
- Cada empresa migrada lleva `origen_hallazgo_id = null` y un asiento en
  `empresa_historial` que dice que vino de la migración
- Las que no tengan zona reconocible se cargan **sin localidad**, no se descartan
- Si una empresa ya existe por CUIT o dominio, **se enriquece**, no se duplica
- La IndexedDB sigue funcionando como caché local: no se apaga en esta etapa

---

## 7 · Checklist de validación

Marcá cada punto antes de dar la Etapa A por terminada.

### Infraestructura
- [ ] Proyecto Supabase creado en São Paulo
- [ ] Contraseña de la base guardada en un gestor
- [ ] `service_role` **no** aparece en ningún archivo del repositorio
- [ ] Registro por email desactivado; tu usuario creado a mano
- [ ] Copia manual tomada antes de las migraciones

### Esquema
- [ ] Las 11 migraciones ejecutadas sin error, en orden
- [ ] 21 tablas creadas
- [ ] Las 12 pruebas de seguridad pasan
- [ ] `select count(*) from provincias` devuelve **24**
- [ ] `select * from mission_type_config` devuelve **6 filas**
- [ ] `select * from presupuestos` muestra tope diario 2 y mensual 50

### Geografía
- [ ] Subconjunto o carga oficial ejecutada
- [ ] La consulta de verificación de `docs/GEOGRAFIA.md` da números razonables
- [ ] Ninguna localidad quedó sin partido

### Reglas
- [ ] Un hallazgo sin evidencia **no** se puede aceptar
- [ ] Una señal **no** puede vincular empresa sin hallazgo
- [ ] `cobertura_pct` da `null` donde no hay denominador
- [ ] El interruptor de emergencia frena `tomar_mision`
- [ ] Dos empresas con el mismo CUIT verificado son rechazadas

### Migración
- [ ] Simulación revisada antes de ejecutar
- [ ] Cantidad de empresas en Supabase coincide con la esperada
- [ ] Los historiales se migraron
- [ ] La app local sigue funcionando igual que antes

### Aplicaciones existentes
- [ ] Las cinco aplicaciones siguen funcionando sin cambios
- [ ] Ningún archivo de esas aplicaciones fue modificado

---

## 8 · Lo que NO se hace en esta etapa

Para que quede explícito:

- No se ejecuta ninguna misión
- No se llama a la IA
- No se manda ningún correo
- No se activa ningún cron
- No se modifican las cinco aplicaciones existentes
- No se apaga IndexedDB

La Etapa A deja la base lista y vacía. La primera misión se ejecuta en la
Etapa I, de a una y con vos mirando.

---

## 9 · Qué falta que definas

| Pendiente | Bloquea |
|---|---|
| Crear el proyecto Supabase y pasarme las credenciales | Todo |
| Bajar los archivos oficiales de geografía | La carga completa; el subconjunto no |
| Padrones de IERIC y cámaras | El cálculo de cobertura |
| Dominio propio | Solo el envío de correo, más adelante |
