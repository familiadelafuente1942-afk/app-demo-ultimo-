# Capítulos nuevos: climatización (losa radiante, sala de máquinas, aire acondicionado),
# instalaciones colgadas y cielorraso Durlock, parrillas y hogares.
REF_RAD = "Manual de instalación del fabricante del sistema radiante (p. ej. Tubotherm/Grupo Dema; REHAU según DIN/UNE-EN 1264). Manda siempre el instalador matriculado y el proyecto térmico."
REF_DUR = "Durlock: construcción del sistema Cielorraso Junta Tomada y detalles técnicos (durlock.com). Ante cargas especiales consultar al Departamento Técnico Durlock."

CLIMA = dict(id="clima", t="Climatización y calefacción", ico="clima",
 d="Losa radiante, sala de máquinas, aire acondicionado: niveles, espesores y pruebas.", s=[
S("radiante","Losa radiante: capas, espesores y niveles de piso","losa radiante piso radiante calefaccion tubo pert pex aislante malla mortero espesor nivel piso terminado",
 "La losa radiante se decide en el proyecto, no en obra: suma entre 8 y 10 cm sobre la losa estructural. Si no se reserva esa altura desde el principio, los niveles de piso, umbrales y desagües no cierran.",
 ["Aislante: manta o placa de poliestireno de alta densidad (manta de 10 mm en Tubotherm; placas de 20–30 mm en planta baja o sobre locales no calefaccionados)",
  "Film de polietileno ≥ 60 µ (en planta baja, bajo el aislante contra la humedad; en planta alta, entre aislante y malla)",
  "Banda perimetral aislante en todos los muros, columnas y marcos (piso flotante)",
  "Malla tipo Cima 15×15 (o 15×25) para fijar los tubos con precintos",
  "Tubo PERT o PEX de 16 o 20 mm, de una sola pieza por circuito (sin uniones bajo el piso)",
  "Mortero de cubrición: 1 cemento : 3 arena (< 4 mm) : 3 canto rodado chico, con el aditivo fluidificante del fabricante",
  "Colector con caudalímetros, purgadores y llaves por circuito"],
 ["Definir en plano, antes de hormigonar la losa, la altura total del paquete: losa estructural → aislante → film → malla y tubo → mortero → piso. Referencia Belfast: 8 a 10 cm sobre losa hasta piso terminado (confirmar con el instalador según aislante y piso).",
  "Espesor de mortero sobre el lomo del tubo: mínimo 3,5 a 4 cm (en total ≈ 3 veces el diámetro del tubo). Con más espesor la losa tarda más en calentar; con menos se fisura.",
  "Losa estructural limpia y nivelada (± 5 mm). Si no, carpeta de regularización antes del aislante.",
  "Colocar banda perimetral subiendo hasta el nivel de piso terminado; se recorta recién al colocar el zócalo.",
  "Aislante a tope, sin huecos; film con solapes de 10 cm; malla sobre el film.",
  "Tubos según plano del instalador: separación 10 a 30 cm (más juntos junto a ventanales y en baños), fijados a la malla cada 50 cm, curvas sin aplastar.",
  "Juntas de dilatación en paños de más de 40 m² o de lado mayor a 8 m, en puertas y cambios de forma. Ningún circuito cruza una junta; las conexiones que la cruzan llevan vaina de 20 cm a cada lado.",
  "Primera prueba hidráulica antes de llenar: llenar y purgar, 3 bar; a la hora subir a 3,5 bar; a las 24 h verificar 3 bar durante 1 hora sin pérdidas. Dejar los tubos con agua a 3 bar durante el llenado del mortero.",
  "Llenar con el mortero del fabricante, sin pisar los tubos (tablones), vibrando o compactando bien alrededor del tubo.",
  "No pisar 3 días; no encender antes de 21 días; no colocar el piso antes de 30 días.",
  "Primer encendido gradual: 3 días a 25 °C y después 4 días a la temperatura de diseño. Registrar en NEXO.",
  "Segunda prueba hidráulica antes de colocar el revestimiento.",
  "Piso: cerámico, porcelanato o piedra son los mejores. Madera solo apta para radiante, encolada, con humedad de carpeta medida. Temperatura de superficie máx. 27–29 °C en estar, 33 °C en baños."],
 ["Altura del paquete en plano y en replanteo (nivel 0,00 y nivel de piso terminado marcados en obra)","Banda perimetral continua","Foto de cada circuito con su número antes de llenar","Prueba hidráulica 1 aprobada (manómetro + foto)","Mortero ≥ 3,5 cm sobre el tubo (medir en 3 puntos por local)","21 días antes de encender; protocolo de encendido registrado","Prueba hidráulica 2 antes del piso"],
 ["Uniones de tubo bajo el piso","Tubos cruzando juntas sin vaina","Contrapiso alivianado sobre los tubos","Encender en seguida para \"secar\" el mortero","Colocar el piso sin medir humedad","Clavar o perforar el piso radiante (siempre con plano de tubos a mano)"],
 REF_RAD),
S("salamaquinas","Sala de máquinas, caldera y colector","sala de maquinas caldera colector radiante termotanque tanque intermediario ventilacion gas equipo",
 "La caldera y los colectores son el corazón de la calefacción. Se ubican en un lugar accesible, ventilado y con desagüe, nunca encerrados sin acceso.",
 ["Caldera (preferentemente de condensación) según cálculo térmico","Colector por planta, en nicho con tapa a 30–50 cm del piso y centrado respecto de los locales","Vaso de expansión, válvula de seguridad, purgadores y llaves de corte","Desagüe de condensado y de válvula de seguridad"],
 ["Ubicación aprobada en plano: espacio de servicio alrededor del equipo según fabricante (habitual 50 cm al frente).",
  "Caldera a gas: instalación y ventilaciones solo por gasista matriculado y según la distribuidora (ver capítulo Gas). Conducto de evacuación del fabricante, con su pendiente.",
  "Nicho del colector con espacio para todos los circuitos, rotulados (local y largo de cada uno).",
  "Desagüe con sifón para condensado y válvula de seguridad; pileta de patio o boca de desagüe en la sala.",
  "Cañerías de ida y retorno aisladas en todo su recorrido no calefaccionado.",
  "Tablero o circuito eléctrico exclusivo con protección propia; termostatos por zona cableados antes de cerrar.",
  "Puesta en marcha por el instalador con planilla de presiones, caudales y temperaturas."],
 ["Accesos libres al equipo y al colector","Circuitos rotulados","Ventilaciones aprobadas por gasista","Planilla de puesta en marcha en NEXO"],
 ["Caldera en placard sin ventilación","Colectores tapados sin acceso","Válvula de seguridad sin desagüe"],
 REF_RAD),
S("aire","Aire acondicionado: preinstalación y equipos","aire acondicionado split cañeria cobre preinstalacion desague condensado vacio nitrogeno unidad exterior soporte",
 "La preinstalación (caños, desagüe y eléctrico) se hace con la obra gruesa, antes de revocar o cerrar cielorrasos. El equipo se coloca al final, con la obra limpia.",
 ["Caño de cobre de refrigeración (diámetros del fabricante del equipo) con aislación de espuma elastomérica en ambos caños","Desagüe de condensado de PVC o PP ≥ 20 mm con pendiente hacia pileta, embudo o pluvial, con sifón si va a cloaca","Línea eléctrica exclusiva con su protección (termomagnética y diferencial) y cable de comando","Ménsulas o base antivibratoria para la unidad exterior; caja de preinstalación en muro"],
 ["Definir en plano posición de unidades interiores (lejos de camas y sillones, sin obstáculos al aire) y exteriores (ventiladas, accesibles para service, sin dar al vecino).",
  "Pasar caños de cobre con curvas suaves, sin aplastar, con las puntas tapadas (cinta o tapón) para que no entre polvo ni humedad.",
  "Desagüe de condensado con pendiente continua ≥ 1% (nunca contrapendiente); probar con agua antes de cerrar.",
  "Cañerías fijadas cada 1 m en recorridos horizontales sobre cielorraso (ver Instalaciones colgadas).",
  "Prueba de hermeticidad con nitrógeno (presión indicada por el fabricante) y foto del manómetro.",
  "Al colocar el equipo: vacío con bomba (no \"purgar con el gas del equipo\"), abrir válvulas, verificar carga y presiones.",
  "Unidad exterior nivelada, con 30 cm libres detrás y a los lados (o lo que pida el manual), fijada con tacos químicos o bulones.",
  "Registrar marca, modelo, número de serie y ubicación de cada equipo en NEXO."],
 ["Puntas tapadas hasta la conexión","Desagüe probado con agua","Prueba con nitrógeno registrada","Vacío realizado (foto del vacuómetro)","Equipos registrados en NEXO"],
 ["Desagüe con contrapendiente o sin sifón a cloaca","Caños sin aislación o con aislación rota","Unidad exterior encerrada sin ventilación","Conectar sin hacer vacío"],
 "Manuales de instalación del fabricante de cada equipo; Reglamento AEA 90364 para la parte eléctrica."),
])

SECO_MAS = [
S("cielorraso","Cielorraso Durlock junta tomada: armado según fabricante","cielorraso durlock junta tomada montantes 40 cm vigas maestras velas rigidas soleras tornillos refuerzos",
 "El cielorraso de placa se arma con la estructura y separaciones que fija Durlock. Si se estira la separación, aparecen ondulaciones y fisuras en las juntas.",
 ["Soleras de 35 mm y montantes de 34 mm galvanizados (chapa ≥ 0,50 mm)","Placa estándar 9,5 o 12,5 mm; verde en baños y cocinas; roja donde se pida resistencia al fuego","Tornillos T1 (perfil-perfil) y T2 (placa-perfil); tarugos N° 8 con tornillo 6×40 mm o brocas metálicas para fijar a losa y muros","Cinta de papel microperforada de 50 mm, masilla, cantoneras y buña Z perimetral si el diseño la pide","Banda aislante entre perfiles y obra gruesa; sellador perimetral"],
 ["Marcar el nivel del cielorraso con láser en todo el perímetro (verificar que quede por debajo de todas las instalaciones colgadas).",
  "Soleras perimetrales de 35 mm fijadas al muro cada 60 cm como máximo, con banda aislante.",
  "Montantes (34 mm) separados como máximo 40 cm entre ejes, apoyados en las soleras.",
  "Vigas maestras (montantes de 34 mm) perpendiculares a los montantes, cada 1,20 m como máximo.",
  "Velas rígidas (montantes de 34 mm) colgando de la losa cada 1,00 m como máximo sobre cada viga maestra, fijadas a la losa con un tramo de solera en T y dos tarugos N° 8, o brocas. Nunca alambre.",
  "Placas transversales a los montantes y trabadas; las juntas de los extremos caen siempre sobre un montante.",
  "Tornillos T2 cada 25–30 cm en el centro de la placa y cada 15 cm en los bordes, a 1 cm del borde, rehundidos sin romper el papel.",
  "Refuerzos: luminarias, ventiladores, proyectores, rieles de cortina o cualquier carga se cuelgan de la losa con su propia fijación o con perfiles de refuerzo atornillados a la estructura; nunca de la placa sola.",
  "Tapas de inspección en llaves, cajas de paso, unidades de aire y colectores (registrar su ubicación).",
  "Juntas: masilla, cinta, 2 manos más con secado entre capas (24 h con masilla lista para usar); tornillos y cantoneras con 2 manos. Con luz rasante o pintura satinada, enduido total en 2 manos cruzadas.",
  "Juntas de control donde lo pida el fabricante (grandes superficies, encuentros con juntas del edificio)."],
 ["Montantes ≤ 40 cm (medir con cinta, foto)","Vigas maestras ≤ 1,20 m y velas ≤ 1,00 m","Refuerzos colocados según plano de iluminación","Tapas de inspección ubicadas","Nivel ± 3 mm en 2 m con luz rasante"],
 ["Velas de alambre","Colgar luminarias de la placa","Juntas de placa sin perfil detrás","Cerrar el cielorraso con instalaciones sin probar"],
 REF_DUR),
S("colgadas","Instalaciones colgadas bajo losa (plomería, electricidad y aire)","fijaciones cañerias cielorraso colgadas losa varilla roscada perfil c grampa soporte plomeria electricidad bandeja",
 "Todo lo que corre sobre el cielorraso se cuelga de la losa con soportes propios, ordenado y con pendiente donde corresponda. El cielorraso no sostiene ninguna cañería.",
 ["Varilla roscada galvanizada 1/4\" o 3/8\" con brocas o tacos metálicos a la losa","Perfil C galvanizado (riel) como travesaño, o grampas tipo omega con tornillo","Abrazaderas con goma para caños de agua y desagüe","Bandeja portacables para recorridos eléctricos largos o con muchos circuitos"],
 ["Coordinar en plano el recorrido de cada instalación antes de colgar: desagües (con pendiente) primero, después agua, aire acondicionado y por último electricidad.",
  "Soportes de referencia (confirmar con el fabricante del caño): desagües de PVC/PP horizontales cada 10 veces el diámetro (Ø 110 → cada 1,10 m) y siempre junto a cada accesorio; agua en PP-R cada 0,60–1,00 m según diámetro (agua caliente más seguido).",
  "Desagües colgados con pendiente continua 1–2% sostenida por la regulación de las varillas; nunca apoyados en la estructura del cielorraso.",
  "Caños eléctricos fijados cada 1 m como máximo y a 30 cm de cada caja o curva; cajas de paso fijadas a la losa, accesibles.",
  "Separar agua y desagües de electricidad (agua siempre por debajo de lo eléctrico, nunca encima de un tablero).",
  "Agua caliente y cañerías de aire con aislación continua, sin aplastarla en las abrazaderas.",
  "Fotografiar todo el plenum por local antes de cerrar el cielorraso y subirlo a NEXO (sirve para reparar sin romper)."],
 ["Ningún caño apoyado en el cielorraso","Pendientes de desagües verificadas con nivel","Soportes a la distancia indicada","Foto del plenum antes de cerrar"],
 ["Cañerías atadas con alambre a los perfiles del cielorraso","Desagüe con panza (sin soporte intermedio)","Agua sobre tableros o cajas eléctricas"],
 "Manuales de instalación de los fabricantes de cañerías (PVC/PP, PP-R) y Reglamento AEA 90364 para canalizaciones."),
]

FUEGO = dict(id="fuego", t="Parrillas y hogares", ico="llama",
 d="Parrilla de obra y hogar a leña: proporciones, tiraje, refractario y distancias.", s=[
S("parrilla","Parrilla de obra","parrilla quincho asador campana conducto tiraje refractario fogonero mesada brasero",
 "Una parrilla que no tira llena de humo el quincho. El tiraje lo dan la campana, la sección y la altura del conducto, no el tamaño de la parrilla.",
 ["Ladrillo refractario y mortero refractario en el fondo, laterales y piso del fogón","Ladrillo común o block para la estructura","Campana de chapa o de mampostería con su conducto","Conducto de chapa galvanizada o de acero, o de mampostería revocada lisa por dentro","Sombrerete en la salida","Losa o base de hormigón armado bajo el piso del fogón"],
 ["Definir con Dirección de obra el modelo: ancho útil de la parrilla, brasero o fogonero, horno, mesada y bacha.",
  "Base: losa de hormigón armado sobre la estructura de apoyo; piso del fogón a 80–90 cm del piso (altura de trabajo).",
  "Fogón revestido con refractario con junta fina de mortero refractario; dejar junta de dilatación entre el refractario y la mampostería común.",
  "Campana que cubra todo el frente de la parrilla y sobresalga hacia adelante; la boca de la campana a una altura cómoda de trabajo (no menor a 1,60 m del piso de pie).",
  "Conducto sin quiebres; si hace falta, solo curvas suaves (máx. 45°). Sección constante, sin achicarse, según el ancho de la parrilla (definir con el fabricante de la campana o el proyectista; como referencia, no menos de 25 × 25 cm o Ø 25 cm en parrillas domésticas).",
  "Salida del conducto al menos 60 cm por encima del techo y de cualquier parte de la cubierta a menos de 3 m, con sombrerete.",
  "Separar el conducto de cualquier madera o material combustible (mín. 5 cm con aislación) y sellar el pase por el techo con babeta y sellador apto para temperatura.",
  "Primer fuego chico para secar morteros antes del uso normal."],
 ["Refractario en todo el fogón","Conducto continuo y sin achicarse","Salida ≥ 60 cm sobre la cubierta, con sombrerete","Pase de techo estanco"],
 ["Conducto de caño fino o con codos a 90°","Revestir el fogón con ladrillo común","Madera de techo en contacto con el conducto"],
 "Valores de referencia de buena práctica; prevalecen el proyecto, el fabricante de la campana/conducto y las reglas del barrio o municipio."),
S("hogar","Hogar a leña","hogar a leña chimenea tiraje garganta regulador refractario cámara de humo conducto sombrerete distancias combustibles",
 "El hogar funciona por proporciones: boca, profundidad, garganta y conducto se calculan juntos. Lo más seguro es usar un hogar prearmado o un diseño de un fabricante, y en obra respetar sus medidas.",
 ["Hogar prearmado de fabricante, o cámara de fuego de ladrillo refractario con mortero refractario","Regulador de tiraje (damper) operable desde el ambiente","Conducto aislado o de mampostería con sección constante","Sombrerete y babeta de techo","Base (hearth) de material no combustible: piedra, porcelanato o cemento"],
 ["Si es prearmado: seguir el manual del fabricante en conducto, toma de aire exterior, distancias y aislación. Es la opción recomendada por Belfast.",
  "Si es de mampostería: paredes de la cámara de fuego de 20 cm con revestimiento refractario de 5 cm (juntas finas de mortero refractario), profundidad mínima de la cámara 50 cm.",
  "Garganta y regulador al menos 20 cm por encima de la boca; el paso por garganta y cámara de humo nunca menor que la sección del conducto.",
  "Base incombustible de 10 cm de espesor que avance al menos 40 cm al frente y 20 cm a cada lado de la boca (50 y 30 cm si la boca es grande).",
  "Madera u otros combustibles separados al menos 5 cm del frente y laterales y 10 cm de la parte trasera del hogar; el espacio no se rellena con nada combustible.",
  "Conducto recto o con desvíos suaves, aislado al pasar por cielorrasos y techos.",
  "Salida 60 cm por encima de cualquier parte del techo a menos de 3 m (90 cm si sale en la cumbrera), con sombrerete.",
  "Toma de aire exterior si la casa es muy hermética (aberturas de alta prestación).",
  "Primer encendido con fuego chico durante varios días para curar morteros."],
 ["Medidas del fabricante o del proyecto verificadas antes de cerrar","Base incombustible con su extensión","Distancias a combustibles","Salida y sombrerete según regla 60 cm / 3 m"],
 ["Hogar de ladrillo común sin refractario","Conducto más chico que el pedido","Revestimiento de madera pegado al hogar","Salida del conducto por debajo de la cumbrera cercana"],
 "Medidas tomadas del Código Residencial de EE. UU. (IRC/CRC R1001) como buena práctica, convertidas a cm; prevalecen el fabricante del hogar y el proyecto."),
])

# Insertar capítulos
ids = [c["id"] for c in C]
C.insert(ids.index("gas") + 1, CLIMA)
for c in C:
    if c["id"] == "seco":
        c["s"].extend(SECO_MAS)
        c["d"] = "Tabiques, cielorrasos Durlock e instalaciones colgadas."
ids = [c["id"] for c in C]
C.insert(ids.index("carpinterias") + 1, FUEGO)

# Tablero: más detalle
for c in C:
    if c["id"] == "electrica":
        for s in c["s"]:
            if s["id"] == "tablero":
                s["pasos"] += [
                  "Tablero principal y seccionales por planta según proyecto; circuitos de aire acondicionado, caldera, bomba y portón con protección propia.",
                  "Durante la obra, el tablero se protege con nylon y cinta (polvo y revoque) y queda señalizado.",
                  "Cables peinados, con terminales y borneras; nada de empalmes dentro del tablero.",
                  "Esquema unifilar actualizado pegado en la puerta y cargado en NEXO."]
                s["ctrl"] += ["Unifilar en la puerta", "Tablero protegido durante la obra"]

# Hormigonado con calor (y frío)
CALOR = S("calor","Hormigonado con calor (y con frío)","hormigon calor tiempo caluroso temperatura verano evaporacion fisuras plasticas retardador hielo curado frio helada",
 "Con calor, sol y viento el hormigón pierde agua antes de fraguar: se fisura en la superficie, pierde resistencia y es difícil de terminar. Se planifica el colado para que el hormigón llegue y se coloque fresco, y se cura enseguida.",
 ["Hormigón pedido a planta con aditivo retardador de fraguado (indicar en el pedido que es para clima caluroso)","Agua fría o hielo en planta si hace falta (lo resuelve la hormigonera)","Fibras plásticas antifisura en losas y contrapisos expuestos, si lo aprueba el calculista","Antisol (compuesto de curado blanco), arpillera, film de polietileno, aspersores o niebla","Termómetro de punzón para medir el hormigón del camión"],
 ["Se considera tiempo caluroso cuando hay más de 25–30 °C, sol fuerte, viento o baja humedad. Con pronóstico de 32 °C o más, se reprograma o se cuela de madrugada.",
  "Horario: empezar a primera hora (6–7 h) o colar de noche con iluminación. Nunca al mediodía.",
  "Temperatura del hormigón al llegar: medirla en cada camión; máximo 30–32 °C. Si llega más caliente, avisar a planta y a Dirección de obra antes de colocar.",
  "Tiempo desde la carga en planta hasta terminar la descarga: máximo 90 minutos (con calor, apuntar a 60 minutos). Coordinar los camiones para que no esperen al sol.",
  "Nunca agregar agua en obra para \"ablandar\" el hormigón. Si falta trabajabilidad, la corrige la planta con aditivo.",
  "Mojar encofrados, armaduras y base con agua fría antes de colar, sin dejar charcos.",
  "Cuadrilla y equipos completos (vibradores de reserva) para colocar, vibrar y terminar sin demoras. Pantallas contra el viento si sopla fuerte.",
  "Entre el enrasado y el fratasado, rociar con niebla fina o cubrir con film si se ve que la superficie se seca (que se pone mate).",
  "Curado inmediato apenas terminada la superficie: Antisol en una mano pareja, o arpillera mojada y film. Mantener húmedo como mínimo 7 días (losas y tabiques), sin dejar que se seque entre riegos.",
  "El agua de curado no debe estar mucho más fría que el hormigón (no más de 11 °C de diferencia).",
  "Con frío: no colar si se esperan menos de 5 °C en las 48 h siguientes sin protección; cubrir con film y mantas, no usar acelerantes con cloruros y alargar los plazos de desencofrado.",
  "Registrar en NEXO: hora de cada camión, temperatura del hormigón, temperatura ambiente, probetas y curado aplicado."],
 ["Pronóstico revisado el día anterior","Temperatura del hormigón medida en cada camión (≤ 32 °C)","Descarga dentro de los 90 min","Curado aplicado dentro de la primera hora","7 días de curado húmedo registrados"],
 ["Agregar agua en obra","Colar al mediodía con 35 °C","Dejar la losa al sol sin curar","Camiones esperando al sol"],
 "CIRSOC 201 (referencias de hormigonado en tiempo caluroso y frío) y bibliografía técnica de la cátedra de Tecnología del Hormigón (UNC, adaptado de Kosmatka et al.). Prevalecen las indicaciones de la hormigonera y del calculista.")
for c in C:
    if c["id"] == "estructura":
        i = [s["id"] for s in c["s"]].index("curado")
        c["s"].insert(i, CALOR)

# Relleno entre vigas invertidas (azoteas y losas sobre planta baja)
INVERTIDAS = S("invertidas","Relleno entre vigas invertidas (azotea y losa sobre PB)","vigas invertidas relleno cascote isocret perlas eps contrapiso alivianado azotea losa planta baja 20 28 cm peso",
 "Con vigas invertidas la losa queda abajo y las vigas sobresalen: entre viga y viga quedan cajones de 20 a 28 cm que hay que rellenar hasta el nivel del contrapiso. Ese relleno pesa mucho si se hace mal, así que el material lo aprueba el calculista antes de empezar.",
 ["Isocret (perlas de EPS aditivadas): bolsa de 170 l, rinde 0,20 m³ (5 bolsas por m³) — sistema preferido Belfast",
  "Cemento portland (para Isocret: 60 kg por bolsa de 170 l para densidad 300 kg/m³)",
  "Cascote limpio de ladrillo u hormigón, sin yeso, madera, plástico ni tierra (solo si el calculista lo aprueba)",
  "Mortero para carpeta cementicia sobre el relleno",
  "Caño camisa para pases a través de las vigas (dejados al hormigonar)"],
 ["Antes de hormigonar las vigas: definir con el calculista el material de relleno y dejar los pases (caño camisa) en el punto más bajo de cada cajón, para que el agua que entre al relleno pueda salir y no quede atrapada, y para el paso de desagües.",
  "Peso de referencia por cada cm de relleno: cascote ≈ 16–19 kg/m²; Isocret a 300 kg/m³ ≈ 3 kg/m². Un relleno de 25 cm pesa ≈ 400–470 kg/m² con cascote y ≈ 75 kg/m² con Isocret (más la carpeta: ≈ 20 kg/m² por cm). El cascote se usa solo con aprobación escrita del calculista.",
  "Instalaciones dentro del relleno (desagües de azotea, cañerías): colocadas, fijadas y probadas antes de rellenar, con su pendiente.",
  "Losa limpia y humedecida (sin charcos). En azoteas, barrera de vapor si el proyecto la pide.",
  "Fajas de nivel (o de pendiente en azoteas) con mortero, cada 1,5–2 m, para dar la altura final.",
  "Isocret — dosificación por bolsa de 170 l: 60 kg de cemento y ≈ 30 l de agua (densidad ≈ 300 kg/m³). Para más liviano: 50 kg y 25 l (250 kg/m³); para más firme: 70 kg y 35 l (350 kg/m³). Sin arena. Seguir siempre lo impreso en la bolsa.",
  "Mezclar en hormigonera: primero agua y cemento, después las perlas, hasta que estén todas cubiertas. Se puede bombear.",
  "Volcar entre las fajas y nivelar con regla sin apisonar (se aplastan las perlas). Admite grandes espesores en una sola colada; espesor mínimo 5 cm por encima de cualquier caño.",
  "No colocar con lluvia, con menos de 5 °C, riesgo de helada ni más de 35 °C.",
  "Cascote (si está aprobado): en capas de 10–15 cm, regado y trabado con mortero pobre, compactado, sin huecos ni piezas grandes sueltas; terminar con contrapiso de nivelación.",
  "Dejar secar (fragüe total ≈ 48 h; más tiempo antes de la carpeta si el espesor es grande) y no transitar con carretillas directo sobre el Isocret: usar tablones.",
  "Carpeta cementicia encima de mínimo 3 cm (el Isocret no tiene resistencia superficial). En azoteas la carpeta lleva la pendiente final hacia los embudos y después la impermeabilización Protex.",
  "Junta perimetral contra vigas, muros y parapetos.",
  "Cómputo de ejemplo: 100 m² × 0,25 m = 25 m³ → 125 bolsas de Isocret y 7.500 kg de cemento (150 bolsas de 50 kg) a 300 kg/m³."],
 ["Material de relleno aprobado por escrito por el calculista","Pases de desagote en el punto bajo de cada cajón","Instalaciones probadas antes de rellenar","Dosificación de Isocret según bolsa (cemento pesado, no a ojo)","Carpeta ≥ 3 cm sobre el relleno","Nivel o pendiente verificada antes de la carpeta"],
 ["Rellenar con cascote sin aprobación del calculista","Cajones sin salida para el agua","Escombro con yeso, madera o tierra","Porcelanato o membrana directo sobre el Isocret","Agregar arena o agua de más al Isocret"],
 "Ficha técnica Isocret (Tecnisec): dosificaciones por densidad, rendimiento y condiciones de aplicación. Pesos de referencia para cómputo de cargas; manda siempre el cálculo estructural.")
for c in C:
    if c["id"] == "contrapisos":
        i = [s["id"] for s in c["s"]].index("alivianado")
        c["s"].insert(i + 1, INVERTIDAS)
        for s in c["s"]:
            if s["id"] == "alivianado":
                s["mat"][0] = "Isocret (perlas de EPS aditivadas, bolsa de 170 l = 0,20 m³) y cemento — producto Belfast"
                s["pasos"][0] = "Dosificación Isocret por bolsa de 170 l: 60 kg de cemento y ≈ 30 l de agua (≈ 300 kg/m³), sin arena; seguir lo impreso en la bolsa. Ver también Relleno entre vigas invertidas."

# Revoques: malla en encuentros y salpicado + fajas
MALLA = S("malla","Malla soldada en encuentros de mampostería con columnas y vigas","malla soldada encuentro mamposteria columna viga fisura revoque canaleta",
 "Donde el ladrillo se encuentra con el hormigón (columnas, vigas, tabiques) o sobre canaletas de instalaciones, el revoque se fisura si no lleva malla. La malla se coloca antes del salpicado y queda dentro del revoque grueso.",
 ["Malla soldada galvanizada de alambre fino (cuadrícula de ≈ 12–25 mm) en rollos o tiras","Clavos de acero con arandela o tacos con tornillo para fijarla","Salpicado cementicio (con promotor de adherencia sobre hormigón liso)"],
 ["Colocar después de terminar y probar las instalaciones de esa pared.",
  "Cortar tiras que cubran el encuentro y pasen al menos 15–20 cm sobre cada material (ladrillo y hormigón). Sobre canaletas, 15 cm a cada lado de la canaleta.",
  "Fijar la malla separada 3–5 mm del muro (que quede dentro del revoque, no pegada al ladrillo), con fijaciones cada 30–40 cm.",
  "Tiras continuas en toda la altura del encuentro, de piso a viga; empalmes solapados 10 cm.",
  "En esquinas de vanos (puertas y ventanas), tira de malla a 45° en cada esquina.",
  "Sobre la malla, salpicado y después grueso, embebiendo completamente la malla."],
 ["Malla en todos los encuentros hormigón-ladrillo y sobre canaletas (foto de cada pared)","Solape ≥ 15 cm a cada lado","Malla fija y separada del muro","Esquinas de vanos reforzadas a 45°"],
 ["Revocar encuentros sin malla","Malla suelta que se mueve al revocar","Malla pegada al ladrillo sin revoque detrás"],
 "Buena práctica de obra Belfast; prevalecen las indicaciones del proyecto y del fabricante del mortero.")
SALP = S("salpicado","Salpicado (cervecita) y fajas","salpicado cervecita chicoteo puente de adherencia fajas plomo revoque grueso subsuelo hormigon",
 "El salpicado (la \"cervecita\") es la capa de agarre: un mortero cementicio bien fluido que se tira con fuerza para dejar la superficie rugosa. Sin salpicado el revoque se despega, sobre todo en hormigón. Las fajas son las guías a plomo que fijan el espesor y la planeidad del revoque.",
 ["Salpicado: cemento y arena gruesa 1:2 o 1:3, muy fluido (sobre hormigón, con promotor de adherencia tipo Protex Látex en el agua)","Fajas: mortero del grueso con regla y plomada o láser","Reglas de aluminio de 2–3 m"],
 ["Superficie limpia, sin polvo, desmoldante ni partes flojas; humedecer antes.",
  "Tirar el salpicado con cuchara o máquina, cubriendo toda la superficie de forma pareja y rugosa (no se alisa).",
  "En hormigón liso (columnas, vigas, tabiques de subsuelo), salpicado siempre con promotor de adherencia.",
  "En subsuelos, el salpicado se hace sobre la impermeabilización solo si el sistema lo admite (Seal 77: puente con Protex Látex o Superligante).",
  "Mantener húmedo y dejar que endurezca (mínimo 24 h) antes del grueso.",
  "Fajas: hacerlas después de colocar las instalaciones eléctricas y sanitarias y las mallas, para que el espesor cubra todo.",
  "Fajas verticales a plomo cada 1–1,5 m y en todas las aristas, con el espesor final del grueso (1,5–2 cm).",
  "Verificar las fajas con regla y plomada o láser antes de cargar el grueso entre ellas."],
 ["Salpicado parejo en toda la superficie","Promotor de adherencia en hormigón","Fajas a plomo verificadas","Cajas eléctricas a la altura del revoque terminado según las fajas"],
 ["Revocar sobre hormigón liso sin salpicado","Salpicado seco o muy espeso que no agarra","Fajas a ojo o separadas más de 1,5 m"],
 "Buena práctica de obra Belfast; prevalecen las fichas del fabricante del mortero y del promotor de adherencia.")
for c in C:
    if c["id"] == "revoques":
        c["s"][0:0] = [MALLA, SALP]
        c["d"] = "Malla en encuentros, salpicado, fajas, azotado hidrófugo, grueso, fino y yeso."
