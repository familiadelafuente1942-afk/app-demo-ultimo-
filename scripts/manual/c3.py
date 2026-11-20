# Capítulo Protex: sistema de impermeabilización Belfast con productos Protex.
# Valores tomados de las fichas técnicas Protex; ante cualquier duda manda el Departamento Técnico Protex (+54 11 5263-7770).
REF_P = "Fichas técnicas Protex (protexargentina.com). Ante dudas o casos especiales, consultar al Departamento Técnico Protex: +54 11 5263-7770."

def _sec(cid, sid):
    for c in C:
        if c["id"] == cid:
            for s in c["s"]:
                if s["id"] == sid:
                    return s
    raise KeyError(cid + "/" + sid)

def _parche(cid, sid, **kw):
    s = _sec(cid, sid)
    for k, v in kw.items():
        if k == "mat_pre":
            s["mat"] = v + s["mat"]
        elif k == "tags_mas":
            s["tags"] += " " + v
        else:
            s[k] = v

# ---------- Capítulo nuevo ----------
PROTEX = dict(id="protex", t="Impermeabilización con Protex", ico="gota",
 d="El sistema Belfast: qué producto Protex va en cada lugar, con dosis, manos y tiempos.", s=[
S("protexguia","¿Qué producto Protex uso? (tabla rápida)","protex tabla elegir producto impermeabilizante cual uso",
 "En Belfast impermeabilizamos con Protex. Esta tabla dice qué producto va en cada lugar. Si el caso no está acá, se consulta a Dirección de obra antes de comprar.",
 ["Hormigón de subsuelos, tanques y cisternas → Xypex Admix C-1000 (cristalizante en la mezcla) o Protex Hidro (hidrófugo de masa)",
  "Juntas de hormigonado (platea-tabique, losa-tabique) → Protex Hidro-Swell P o Junta PVC (waterstop)",
  "Tabiques de subsuelo desde adentro o afuera, cisternas, tanques de hormigón → Protex Seal 77 (aguanta presión positiva y negativa)",
  "Baños, duchas, balcones, Durlock en zonas húmedas, tanques que pueden moverse → Protex Seal 77 Flex",
  "Tanques, piletas y terrazas sin presión negativa → Protex Flex",
  "Capa aisladora, azotados y carpetas hidrófugas → Protex 1 (1:10 en el agua de amasado)",
  "Humedad que sube por muros existentes → Protex Fin (barrera química inyectada)",
  "Azoteas no transitables o de tránsito liviano → Protex Techos 5000 PU (con Geomanta en zonas críticas)",
  "Terrazas transitables, cocheras, jardineras → Protex Poliurea F + Protex Top Alifático",
  "Filtraciones con agua corriendo → Protex Tap (tapón hidráulico)",
  "Nidos, fisuras y reparación de hormigón → Concretex / Protex Rep; inyecciones: Protex Hydrofoam",
  "Juntas con movimiento → Protex PU 40 C sobre fondo de junta Protex Pol",
  "Pegado de revoque sobre Seal 77 → Protex Látex o Superligante; cerámicos → Pegatex Impermeable o Flexible"],
 ["Elegir el producto con esta tabla y registrar la elección en la app general de Belfast (obra, lugar, producto, lote).",
  "Pedir la ficha técnica vigente del lote y dejarla en la carpeta de obra.",
  "Verificar el vencimiento: los cementicios bicomponentes duran 6 meses en envase cerrado; Protex 1, 3 años.",
  "Nunca mezclar productos de marcas distintas en un mismo sistema sin consultar."],
 ["Producto correcto para el lugar","Ficha técnica en obra","Lote y vencimiento registrados"],
 ["Usar pintura asfáltica \"porque había\"","Agregar agua a un bicomponente","Comprar otro producto sin consultar"],
 REF_P),
S("seal77","Protex Seal 77: cementicio rígido (presión positiva y negativa)","seal 77 protex cementicio bicomponente tanque cisterna subsuelo sotano presion negativa",
 "Impermeabilizante cementicio de dos componentes. Es el que usamos cuando el agua puede empujar desde atrás (presión negativa): subsuelos impermeabilizados desde adentro, cisternas, tanques de hormigón, fosos de ascensor.",
 ["Protex Seal 77: kit predosificado (polvo + líquido Seal N° 2); se usa el kit completo, sin fraccionar","Pinceleta de cerda dura o llana","Concretex o Protex Tap para reparar antes","Protex Látex o Superligante si después va revoque"],
 ["Superficie firme, limpia, porosa y húmeda (saturada sin agua superficial). Picar lechadas, desmoldantes y partes flojas.",
  "Reparar antes: nidos y fisuras con Concretex; filtraciones activas con Protex Tap; pasadores de encofrado sellados.",
  "Media caña en los encuentros piso-pared con mortero de reparación.",
  "Mezclar volcando el polvo sobre el líquido de a poco, con mezclador a bajas revoluciones, hasta que no queden grumos. NUNCA agregar agua.",
  "Usar la mezcla dentro de las 2 horas (a 25 °C).",
  "Aplicar 3 manos cruzadas (una horizontal, otra vertical), con pinceleta o llana. Consumo ≈ 1 kg/m² por mano (≈ 3 kg/m² en total).",
  "Esperar mínimo 6 horas entre manos; humedecer levemente antes de cada mano.",
  "Proteger de lluvia y alta humedad 4 horas. Curar con agua pulverizada.",
  "Habilitar al servicio a las 72 horas (tanques: lavar antes de llenar).",
  "Si va revoque encima: puente de adherencia con Protex Látex o Superligante. Si va cerámico: adhesivo de baja absorción y alta adherencia (Pegatex)."],
 ["3 manos aplicadas (foto de cada mano con fecha)","Consumo real ≈ 3 kg/m² (bolsas usadas ÷ m²)","Sin fisuras ni zonas sin cubrir","Curado registrado"],
 ["Agregar agua para \"estirar\" la mezcla","Aplicar sobre superficie seca o con lechada","Dar 2 manos en vez de 3","Pintar encima con pintura a solvente"],
 REF_P),
S("seal77flex","Protex Seal 77 Flex: baños, duchas y balcones","seal 77 flex protex flexible baño ducha balcon durlock bañera ceramico",
 "Versión flexible del Seal 77: acompaña pequeños movimientos del soporte. Es el estándar Belfast para baños, duchas, balcones, lavaderos y placas de yeso en zonas húmedas, debajo del revestimiento.",
 ["Protex Seal 77 Flex: kit de 25 kg","Venda o banda de refuerzo en esquinas, rejillas y caños","Pegatex Flexible o Impermeable para el cerámico"],
 ["Contrapiso con pendiente y carpeta terminados, firmes, limpios y humedecidos.",
  "Media caña o banda de refuerzo en todos los encuentros piso-pared y alrededor de rejillas, caños y bridas.",
  "Mezclar el kit completo sin agregar agua.",
  "3 manos cruzadas, ≈ 1 kg/m² por mano, mínimo 6 h entre manos.",
  "Cubrir todo el piso del baño subiendo 20 cm en las paredes; dentro de la ducha subir hasta 2,00 m (o hasta el techo si hay vapor).",
  "Sobre Durlock: placa verde (resistente a la humedad), juntas tomadas y masilladas antes de impermeabilizar.",
  "Prueba de estanqueidad de 48 h antes de revestir.",
  "Revestir con adhesivo de baja absorción y alta adherencia (Pegatex Flexible o Impermeable)."],
 ["Bandas en encuentros y rejillas (foto)","Altura en ducha ≥ 2,00 m","Prueba de 48 h aprobada y registrada"],
 ["Impermeabilizar solo el piso de la ducha","Saltear la banda alrededor de la rejilla","Pegar el cerámico con adhesivo común"],
 REF_P),
S("protexflex","Protex Flex: tanques, piletas y terrazas (sin presión negativa)","protex flex tanque pileta piscina terraza sobre ceramica medianera",
 "Cementicio muy flexible para agua que empuja desde el frente (presión positiva). Apto para agua potable. Se puede aplicar sobre cerámica de terrazas sin levantarla.",
 ["Protex Flex: kit de 35 kg (25 kg de polvo + 10 kg de Protex Flex N° 2)","Concretex o Protex Tap para reparar fisuras antes"],
 ["Superficie firme, sin restos de cal, pintura, aceite o grasa; rugosidad al menos de lija mediana (lavado ácido, neutralizar y enjuagar).",
  "Reparar fisuras, juntas y roturas con Concretex o Protex Tap.",
  "Humedecer levemente. Si hace falta imprimar: una mano de Flex N° 2 solo, hasta que quede pegajoso (máx. 24 h).",
  "Mezclar volcando el polvo sobre el líquido; usar en 30–40 minutos. Sin agua.",
  "3 manos cruzadas, ≈ 1 kg/m² por mano, mínimo 6 h entre manos.",
  "Curar rociando con agua 3–4 veces cada 8 h.",
  "Tanques: esperar 48 h de curado como mínimo antes de llenar."],
 ["3 manos","Curado registrado","48 h antes de llenar"],
 ["Usarlo en subsuelos con agua desde atrás (no aguanta presión negativa)","Aplicar a menos de 5 °C o con amenaza de lluvia"],
 REF_P),
S("protex1","Protex 1: capa aisladora, azotado y carpetas hidrófugas","protex 1 hidrofugo inorganico capa aisladora azotado carpeta hidrofuga 1:10",
 "Hidrófugo químico inorgánico que se agrega al agua de amasado de los morteros. Es el que va en todas las capas aisladoras, azotados exteriores y carpetas bajo piso de Belfast.",
 ["Protex 1 (bidón)","Cemento portland y arena fina a mediana","Agua limpia"],
 ["Dilución: 1 parte de Protex 1 en 10 partes de agua (1:10). Con esa agua se amasa el mortero. Descontar la humedad de la arena.",
  "Mortero: cemento y arena 1:3 para azotados, carpetas y capas aisladoras.",
  "Capa aisladora horizontal: espesor mínimo 2,5 cm (≈ 0,45 kg/m² de Protex 1), continua, formando cajón.",
  "Azotado vertical y carpeta hidrófuga: 1 cm de espesor (≈ 0,25 kg/m²).",
  "Tanques y cisternas con mortero: primera capa 1:2 de 4–6 mm, luego mortero 1:3 de hasta 15 mm.",
  "Humedecer el soporte antes. Sobre el azotado, salpicado con la mezcla del grueso para que agarre.",
  "Curar con agua pulverizada 2–3 días. Trabajar entre 5 y 30 °C, sin lluvia ni viento fuerte.",
  "No pasarse de dosis: el exceso altera el fragüe."],
 ["Dilución 1:10 medida con recipiente (no \"a ojo\")","Espesores según uso","Curado 2–3 días"],
 ["Echar el hidrófugo directo en la mezcla sin diluir","Doble dosis \"para que impermeabilice más\"","Azotado sin curar"],
 REF_P),
S("cristalizante","Cristalizantes y juntas: hormigón impermeable de origen","xypex admix c-1000 concentrado protex hidro hidro-swell junta pvc waterstop cristalizante hormigon",
 "La mejor impermeabilización de un subsuelo es un hormigón que no deja pasar el agua. Con Xypex el hormigón cierra sus poros con cristales; las juntas se resuelven con Hidro-Swell P o Junta PVC.",
 ["Xypex Admix C-1000: cristalizante que se agrega al hormigón en planta (dosis según Protex y la hormigonera)","Xypex Concentrado: cristalizante en superficie (pinceleta) para hormigón existente","Protex Hidro: hidrófugo de masa para hormigón","Protex Hidro-Swell P: perfil hidroexpansivo 2 × 1 cm, rollos de 8 m (1 m por metro de junta)","Junta PVC O-15/25/32 o V-20 (waterstop) para juntas con más exigencia"],
 ["Definir con Dirección de obra y la hormigonera si el hormigón de subsuelo lleva Xypex Admix o Protex Hidro, y pedirlo en el remito.",
  "Hidro-Swell P: colocar sobre hormigón de primera etapa seco y limpio, en el centro de la sección.",
  "Recubrimiento mínimo del perfil: hormigón armado ≥ 10 cm de espesor con 4 cm a cada cara; sin armar ≥ 15 cm con 7 cm.",
  "Pegarlo con cemento de contacto o Protex PU 40 C para que el segundo hormigonado no lo mueva. Empalmes a tope, sin huecos.",
  "Si puede mojarse antes de hormigonar (lluvia), pintarlo con lechada de cemento para que no se hinche antes de tiempo.",
  "Hidro-Swell P NO va en juntas de dilatación ni con movimiento: ahí va Junta PVC o sellador.",
  "Hormigón existente: Xypex Concentrado sobre superficie saturada, según ficha."],
 ["Remito de hormigón con aditivo","Perfil centrado, pegado y continuo (foto antes de hormigonar)","Empalmes a tope"],
 ["Colocar el perfil al borde de la pieza","Dejarlo mojarse días antes del colado","Usarlo en juntas de dilatación"],
 REF_P),
S("protexfin","Protex Fin: humedad de cimientos en muros existentes","protex fin humedad ascendente cimientos barrera quimica inyeccion muro existente refaccion",
 "En refacciones, cuando el muro no tiene capa aisladora y la humedad sube del suelo, se hace una barrera química inyectando Protex Fin.",
 ["Protex Fin (lata de 5 l)","Taladro con mecha widia de 13 a 16 mm","Protex 1 o Protex Seal 77 para el revoque nuevo"],
 ["Picar el revoque hasta 40 cm desde el piso, de los dos lados si se puede.",
  "Agujeros a 45° hacia abajo, a 10 cm del piso, separados 20 cm, de profundidad 2/3 del espesor del muro. Segunda hilera 10 cm más arriba, intercalada.",
  "Llenar los agujeros con Protex Fin hasta saturar; repetir varias veces por día durante un par de días.",
  "Consumo: muro de 15 cm ≈ 2 l por metro lineal; 30 cm ≈ 4 l/ml; 45 cm ≈ 6 l/ml.",
  "Dejar el muro sin revocar unos 10 días para que seque.",
  "Revocar con azotado de Protex 1 (5–6 mm) o 3 manos de Seal 77 hasta 40 cm, y después el grueso.",
  "No aplicar por debajo de 5 °C."],
 ["Agujeros según esquema (foto con cinta métrica)","Litros usados ≈ consumo previsto","10 días de secado antes de revocar"],
 ["Inyectar una sola vez","Revocar enseguida con revoque común","Agujeros en una sola hilera"],
 REF_P),
S("techospu","Protex Techos 5000 PU: azoteas","techos 5000 pu protex membrana liquida poliuretano azotea geomanta techo",
 "Membrana líquida poliuretánica de alto tránsito (8–10 años). Es el sistema Belfast para azoteas no transitables o de tránsito liviano y para reparar terrazas.",
 ["Protex Techos 5000 PU","Protex Geomanta (refuerzo) en embudos, babetas, fisuras o en todo el paño si se pide máxima duración","Rodillo de lana o pinceleta","Protex PU 40 C para sellar juntas antes"],
 ["Carpeta con pendiente, sana, curada 28 días y seca (humedad ≤ 5%). Sin polvo, grasa ni partes flojas.",
  "Sellar fisuras y juntas con PU 40 C sobre fondo de junta Protex Pol.",
  "Imprimación: una mano del producto diluido 10% con agua; dejar secar 3 h.",
  "Puntos singulares primero (embudos, babetas, ventilaciones): con Geomanta.",
  "Sin refuerzo: 1,3–1,5 kg/m² en manos cruzadas, 3–6 h entre manos.",
  "Con Geomanta: 0,5–1 kg/m², colocar la manta con solapes de 5 cm, otra mano de 0,5–1 kg/m² encima; a las 24 h, manos de terminación hasta 2–2,5 kg/m² en total (2,5–3 en zonas exigidas).",
  "Subir la membrana en babetas al menos 20 cm.",
  "Aplicar entre 8 y 35 °C, humedad relativa ≤ 75%, sin lluvia prevista. Tránsito a las 72 h.",
  "No sirve para inmersión permanente ni sobre membranas con terminación de polietileno."],
 ["Humedad de carpeta medida ≤ 5%","kg usados ÷ m² ≥ consumo especificado","Geomanta en puntos singulares (foto)","Prueba de estanqueidad 48 h"],
 ["Aplicar sobre carpeta húmeda o recién hecha","Una sola mano gruesa","Terrazas sin pendiente con agua estancada"],
 REF_P),
S("poliurea","Protex Poliurea F: terrazas transitables y cocheras","poliurea f protex transitable cochera estacionamiento jardinera antiraiz top alifatico",
 "Bicomponente en frío de alta resistencia, para terrazas que se pisan, cocheras sobre losa y jardineras (antiraíz). Se protege con Protex Top Alifático.",
 ["Protex Poliurea F","Protex Top Alifático (terminación resistente al sol)"],
 ["Soporte preparado como para Techos PU: curado, seco, limpio, fisuras selladas.",
  "Tránsito medio: 1,8 kg/m²; tránsito pesado (vehículos): 2,5 kg/m².",
  "Manos cruzadas con 2–4 h entre manos.",
  "Terminación: Protex Top Alifático 0,2–0,3 kg/m².",
  "Jardineras: subir por las paredes hasta por encima del nivel de tierra."],
 ["Consumo según tránsito","Top Alifático aplicado","Prueba de estanqueidad"],
 ["Dejar la poliurea expuesta al sol sin Top","Consumo de tránsito medio en cocheras"],
 REF_P),
S("reparaciones","Filtraciones activas y reparaciones","protex tap tapon hidraulico filtracion concretex rep hydrofoam inyeccion fisura",
 "Antes de impermeabilizar hay que cortar el agua que corre y reparar el hormigón. Si no, ningún impermeabilizante adhiere.",
 ["Protex Tap: tapón hidráulico de fragüe ultrarrápido","Concretex / Protex Rep: morteros de reparación","Protex Hydrofoam: inyección de poliuretano para fisuras con agua","Protex 270: inyección epoxi para fisuras estructurales (con aprobación del calculista)"],
 ["Abrir la vía de agua en cola de milano (más ancha adentro), mínimo 2 cm.",
  "Amasar Protex Tap en poca cantidad, formar un tapón y apretarlo con la mano hasta que fragüe (segundos).",
  "Fisuras con agua: inyectar Hydrofoam con inyectores (packers) según ficha.",
  "Nidos de abeja y bordes rotos: picar hasta hormigón sano y reparar con Concretex.",
  "Recién con todo seco de agua corriente, aplicar el sistema (Seal 77, Xypex, etc.)."],
 ["Sin agua corriendo antes de impermeabilizar","Reparaciones registradas con foto"],
 ["Impermeabilizar encima de una filtración activa","Tapar fisuras estructurales sin consultar"],
 REF_P),
])

# Ubicar el capítulo después de "cubiertas"
idx = [c["id"] for c in C].index("cubiertas") + 1
C.insert(idx, PROTEX)

# ---------- Parches a temas existentes ----------
_parche("subsuelos", "tabiques",
 mat=["Hormigón H-30 de baja relación agua/cemento con Xypex Admix C-1000 o Protex Hidro (definir con Dirección de obra)",
      "Protex Hidro-Swell P en juntas de hormigonado, o Junta PVC (waterstop) donde haya más exigencia",
      "Concretex / Protex Rep para nidos y pasadores; Protex Tap si hay agua corriendo"],
 pasos=["Junta platea-tabique: pegar Protex Hidro-Swell P centrado sobre la platea (con PU 40 C o cemento de contacto), con recubrimiento ≥ 4 cm a cada cara, antes de hormigonar el tabique. Ver capítulo Protex.",
  "Hormigonar en capas de 40–50 cm, vibrando cada capa; sin caídas libres de más de 1,5 m (usar tubo).",
  "Tapar los agujeros de pasadores de ambos lados con Concretex.",
  "Reparar nidos de abeja picando hasta hormigón sano y rellenando con Concretex.",
  "Pases de caños con camisa y Hidro-Swell P alrededor."],
 ref=REF_P, tags_mas="protex xypex hidro-swell")

_parche("subsuelos", "impermeab",
 que="Todo tabique que después se tapa con tierra se impermeabiliza antes de rellenar. Una vez enterrado no se repara: se hace bien una sola vez. Sistema Belfast: Protex Seal 77 (3 manos) del lado de la tierra, más protección con placa drenante.",
 mat=["Protex Seal 77 (≈ 3 kg/m² en 3 manos) — sistema principal Belfast",
      "Alternativa: Xypex Concentrado (cristalizante) si el hormigón lleva o no Admix, según Dirección de obra",
      "Concretex y Protex Tap para reparar antes",
      "Placa drenante de polietileno nodulado (con geotextil) como protección mecánica",
      "Geotextil y piedra partida para el drenaje"],
 pasos=["Hormigón limpio, sin rebabas ni desmoldante; pasadores sellados y nidos reparados con Concretex.",
  "Media caña con mortero de reparación en el encuentro tabique-platea (radio ≥ 5 cm).",
  "Humedecer el tabique hasta saturar (sin agua superficial).",
  "Aplicar Protex Seal 77: 3 manos cruzadas, ≈ 1 kg/m² por mano, 6 h mínimo entre manos. Ver capítulo Protex.",
  "Subir la impermeabilización al menos 15–20 cm por encima del nivel de terreno terminado.",
  "Curar y esperar 72 h antes de colocar la protección.",
  "Proteger con placa drenante nodulada (nódulos contra el tabique, geotextil hacia la tierra), fijada solo en el borde superior.",
  "Recién entonces rellenar en capas, compactando con equipo liviano y sin golpear la protección.",
  "Si el tabique no se puede trabajar desde afuera (pantallas, medianeras): Seal 77 del lado interior, que aguanta presión negativa."],
 ctrl=["Media caña ejecutada","3 manos de Seal 77 con foto y fecha de cada una","Consumo ≈ 3 kg/m²","Remate por arriba del terreno","Placa drenante colocada antes de rellenar"],
 err=["Rellenar sin protección mecánica","Dar 1 o 2 manos","Aplicar Seal 77 sobre hormigón seco","Pintar solo con asfalto y dar por impermeabilizado"],
 ref=REF_P, tags_mas="protex seal 77")

_parche("subsuelos", "pisosubsuelo", tags_mas="protex")

_parche("mamposteria", "capaaisladora",
 mat=["Mortero de cemento y arena 1:3 amasado con agua con Protex 1 (1 parte en 10 de agua)"],
 pasos=["Dos capas horizontales: una a 5 cm sobre el nivel del terreno exterior y otra a nivel del contrapiso interior, unidas por dos verticales (cajón).",
  "Agua de amasado: 1 parte de Protex 1 + 10 partes de agua, medida con recipiente.",
  "Espesor mínimo 2,5 cm (la ficha Protex dice 25 mm en consumo y 2,5 mm en aplicación: Belfast toma 2,5 cm del lado seguro), continua, sin interrupciones en esquinas, vanos de puertas ni encuentros.",
  "La vertical del cajón se une al azotado hidrófugo con Protex 1 del revoque exterior y al del interior hasta el piso.",
  "Fratasar, curar húmedo 2–3 días y dejar fraguar antes de seguir levantando."],
 ctrl=["Continua en todo el perímetro (foto)","Unida a contrapiso y revoques","Espesor ≥ 2,5 cm","Dilución 1:10 controlada"],
 ref=REF_P, tags_mas="protex 1")

_parche("revoques", "exterior",
 mat_pre=[], tags_mas="protex 1")
_sec("revoques","exterior")["mat"][0] = "Azotado: cemento y arena 1:3 amasado con agua con Protex 1 (1:10)"
_sec("revoques","exterior")["pasos"][2] = "Azotado hidrófugo con Protex 1, continuo, de 1 cm, unido a la capa aisladora horizontal; salpicado con la mezcla del grueso y no dejar que seque del todo antes del grueso."
_sec("revoques","exterior")["ref"] = REF_P

_sec("contrapisos","carpetas")["mat"][0] = "Mortero de cemento y arena 1:3 (en locales húmedos y bajo piso sobre terreno, amasado con Protex 1 1:10)"
_parche("contrapisos", "carpetas", tags_mas="protex 1")

_parche("cubiertas", "azotea",
 mat=["Barrera de vapor (pintura asfáltica o film)","Aislación térmica (poliestireno extruido o expandido de alta densidad, espesor según proyecto)","Contrapiso con pendiente (alivianado o común)","Carpeta","Impermeabilización Protex: Techos 5000 PU (no transitable o tránsito liviano) o Poliurea F + Top Alifático (transitable)","Bajo piso transitable: Protex Seal 77 Flex bajo carpeta de protección o adhesivo"],
 tags_mas="protex techos 5000 poliurea")

_parche("cubiertas", "membrana",
 que="Sistema Belfast: en azoteas usamos membrana líquida Protex (Techos 5000 PU o Poliurea F). La membrana asfáltica queda solo cuando el proyecto la pide expresamente; en ese caso se coloca así.",
 tags_mas="protex")

_parche("cubiertas", "banos",
 que="La ducha es el punto más exigido de la casa. Se impermeabiliza todo el piso del baño y las paredes de la ducha con Protex Seal 77 Flex antes de revestir.",
 mat=["Protex Seal 77 Flex (3 manos, ≈ 3 kg/m²)","Banda de refuerzo para esquinas, encuentros, rejillas y caños","Rejilla lineal o central con brida para membrana","Pegatex Flexible o Impermeable para el revestimiento"],
 pasos=["Contrapiso con pendiente y carpeta firmes, limpios y humedecidos (ver Pendientes).",
  "Banda de refuerzo en encuentros piso-pared y alrededor de rejillas y caños.",
  "Protex Seal 77 Flex en 3 manos cruzadas, 6 h entre manos, subiendo 20 cm en todo el baño y hasta 2,00 m dentro de la ducha.",
  "Prueba de estanqueidad de 48 h antes de colocar el revestimiento.",
  "Colocar revestimiento con Pegatex Flexible o Impermeable (baja absorción, alta adherencia)."],
 ref=REF_P, tags_mas="protex seal 77 flex")
