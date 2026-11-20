# Protocolos de control por etapa: lo que Dirección de obra revisa y aprueba antes de pasar a la etapa siguiente.
# Cada grupo: (título, [chequeos]). "ver" enlaza al tema del manual.
def E(id, t, d, ver, grupos):
    return dict(id=id, t=t, d=d, ver=ver, g=[dict(t=a, i=b) for a, b in grupos])

PROT = [
E("inicio", "Inicio de obra y replanteo", "Antes de excavar.", "replanteo/ejes", [
 ("Documentación", ["Planos aprobados y última revisión en obra (arquitectura, estructura e instalaciones)", "Estudio de suelos en obra", "Seguro, ART y programa de seguridad firmados", "Planos de cada rubro guardados y rotulados en el obrador"]),
 ("Replanteo", ["Punto fijo y nivel 0,00 materializados y protegidos", "Ejes replanteados y verificados por Dirección de obra (diagonales)", "Retiros y FOS/FOT verificados contra el plano municipal y el reglamento del barrio", "Ejes y niveles fotografiados y cargados en NEXO"]),
]),
E("excavacion", "Excavación y rellenos", "Antes de hormigonar fundaciones.", "suelos/rellenos", [
 ("Excavación", ["Cota de fondo según plano (nivel verificado en varios puntos)", "Fondo limpio, sin agua ni suelo removido", "Taludes estables o apuntalados", "Suelo del fondo coincide con el estudio de suelos (si no, consultar al geotécnico)"]),
 ("Rellenos", ["Capas de espesor indicado (≤ 20 cm)", "Ensayo de compactación aprobado por capa", "Material de relleno aprobado (sin escombro ni materia orgánica)"]),
]),
E("fundaciones", "Fundaciones y platea", "Antes de cada hormigonado.", "fundaciones/platea", [
 ("Base", ["Film de polietileno 200 µ continuo, con solapes de 20 cm y sin roturas", "Hormigón de limpieza ejecutado donde corresponde"]),
 ("Armaduras", ["Diámetros, separaciones y cantidades según plano de estructura", "Recubrimientos con separadores (no piedras ni ladrillos)", "Pelos de columnas y tabiques en posición y con su largo de empalme", "Armadura limpia, atada y firme (se puede caminar sin que se mueva)"]),
 ("Instalaciones embutidas", ["Desagües, pases y cañerías bajo platea en posición según plano y probados", "Pases para gas, agua y electricidad dejados con camisa", "Pozo de bombeo y rejillas en su lugar (subsuelos)"]),
 ("Hormigonado", ["2 vibradores en obra y probados (uno de uso y uno de emergencia)", "Pedido de hormigón con resistencia y asentamiento del plano", "Probetas tomadas y rotuladas", "Curado iniciado y registrado"]),
]),
E("subsuelo", "Subsuelo e impermeabilización enterrada", "Antes de rellenar contra los tabiques.", "subsuelos/impermeab", [
 ("Hormigón", ["Tabiques colados en capas y vibrados, con 2 vibradores en obra", "Juntas platea-tabique con Hidro-Swell P o waterstop colocado (foto)", "Pasadores de encofrado sellados", "Nidos reparados con Concretex"]),
 ("Impermeabilización", ["Media caña en encuentro tabique-platea", "Protex Seal 77: 3 manos con fecha y foto de cada una", "Consumo real ≈ 3 kg/m² verificado", "Remate por encima del terreno terminado"]),
 ("Drenaje y relleno", ["Placa drenante colocada antes de rellenar", "Caño de drenaje con geotextil y pendiente verificada", "Bombas probadas (arranque, corte y alarma)"]),
]),
E("estructura", "Estructura de hormigón", "Antes de cada colado de columnas, vigas y losas.", "estructura/encofrados", [
 ("Encofrados", ["Medidas, niveles y plomos según plano", "Puntales y arriostramientos firmes, sobre base resistente", "Desmoldante aplicado; encofrado limpio y estanco", "Contraflechas donde lo indica el calculista"]),
 ("Armaduras", ["Armadura según planilla de doblado y aprobada por el calculista o Dirección de obra", "Separadores de recubrimiento colocados", "Pases de instalaciones en vigas y losas según plano (nunca perforar después)"]),
 ("Antes de colar", ["2 vibradores en obra y probados (uno de uso y uno de emergencia)", "Cañerías eléctricas y cajas en losa atadas a la armadura y tapadas", "Insertos, anclajes y placas para carpinterías y barandas colocados", "Pronóstico del día revisado (calor, lluvia, frío)"]),
 ("Colado y curado", ["Temperatura del hormigón medida en cada camión", "Probetas tomadas", "Curado húmedo 7 días registrado", "Desencofrado en los plazos indicados"]),
]),
E("mamposteria", "Mampostería", "Antes de revocar.", "mamposteria/muros", [
 ("Muros", ["Ubicación y espesores según plano de arquitectura", "Plomo ± 5 mm por piso y planeidad 5 mm en 2 m", "Juntas llenas y trabadas; anclajes a columnas cada 2–3 hiladas", "Capa aisladora continua y unida al contrapiso"]),
 ("Vanos", ["Medidas de vanos según planilla de carpinterías (ancho, alto y altura de antepecho)", "Dinteles con apoyo ≥ 20 cm", "Vanos a plomo y en escuadra"]),
]),
E("electrica", "Instalación eléctrica (antes de revocar)", "Revisión de cajas y cañerías contra el plano de arquitectura y de equipamiento.", "electrica/canerias", [
 ("Posición de cajas según arquitectura", ["Cada caja ubicada según plano eléctrico y de arquitectura (medida desde ejes o vanos, no a ojo)", "Alturas según planilla: tomas, llaves, tomas de mesada, TV, aire acondicionado, termostatos", "Llaves del lado de apertura de la puerta, a 10–15 cm del marco", "Tomas de mesada coordinados con el plano de cocina (fuera de anafe y bacha)", "Tomas y llaves de baño fuera del volumen de ducha y bañera", "Bocas de iluminación según plano de iluminación y de cielorraso (coordinadas con la grilla de placas)", "Cajas de corrientes débiles (datos, TV, alarma, portero) separadas de las de energía"]),
 ("Nivelación y terminación de cajas", ["Cajas a nivel y a plomo (verificar con nivel cada una)", "Cajas a la altura del revoque o la placa terminada (ni hundidas ni salidas)", "Cajas de un mismo grupo alineadas entre sí a la misma altura", "Cajas firmes, sin moverse, con tapa o papel para que no entre revoque"]),
 ("Cañerías", ["Capa aisladora y cajón hidrófugo sin picar (si se cortó, rehecho y registrado)", "Canaletas rectas hacia el techo; ninguna cañería cruzando la pared en horizontal", "Fajas y revoques hidrófugos sin picar", "Recorridos verticales y horizontales, sin diagonales", "Diámetros según proyecto; sin cañerías aplastadas", "Canaletas tapadas con malla en encuentros y sobre la cañería", "Foto de cada pared antes de revocar (con cinta métrica)"]),
 ("Tableros", ["Tablero principal y seccionales en la ubicación y altura del plano de arquitectura", "Tablero del modelo y tamaño especificado (con reserva de espacio)", "Caja del tablero a plomo, al ras del revoque terminado y protegida", "Cañerías de todos los circuitos llegando al tablero"]),
 ("Puesta a tierra", ["Jabalina instalada y medida (valor registrado)", "Conductor de tierra en todos los circuitos"]),
]),
E("sanitaria", "Instalación sanitaria y gas (antes de tapar)", "Pruebas y posiciones contra el plano de arquitectura.", "sanitaria/agua", [
 ("Posiciones según arquitectura", ["Bocas de agua y desagüe de cada artefacto según plano de baños y cocina (inodoro a eje, bidet, bacha, ducha)", "Alturas de llaves y grifería según la ficha del modelo elegido", "Desagües de pileta de cocina, lavarropas y lavavajillas según plano de equipamiento", "Embutidos de grifería (monocomando, termostáticas) a la profundidad del fabricante"]),
 ("Pruebas", ["Prueba hidráulica de agua aprobada (manómetro, 2 h)", "Prueba de desagües con agua aprobada", "Prueba de gas aprobada por el gasista matriculado"]),
 ("Cañerías", ["Agua caliente aislada", "Desagües con pendiente verificada", "Foto de todas las cañerías antes de tapar"]),
]),
E("clima", "Climatización", "Antes de llenar el radiante y de cerrar cielorrasos.", "clima/radiante", [
 ("Losa radiante", ["Altura del paquete y nivel de piso terminado verificados", "Banda perimetral continua", "Circuitos según plano y rotulados en el colector", "Prueba hidráulica 1 aprobada y tubos con presión durante el llenado", "Mortero ≥ 3,5 cm sobre el tubo"]),
 ("Aire acondicionado", ["Posición de unidades interiores y exteriores según plano", "Caños de cobre con puntas tapadas", "Desagües de condensado probados con agua", "Prueba de hermeticidad con nitrógeno"]),
]),
E("seco", "Construcción en seco y cielorrasos Durlock", "Antes de colocar placas y antes de masillar.", "seco/cielorraso", [
 ("Estructura", ["Montantes de tabiques cada 40 cm; de cielorraso cada 40 cm", "Vigas maestras ≤ 1,20 m y velas rígidas ≤ 1,00 m fijadas a losa (nunca alambre)", "Nivel del cielorraso verificado con láser en todo el perímetro", "Cielorraso por debajo de todas las instalaciones colgadas"]),
 ("Cajones de cortineros", ["Ubicación y medidas del cajón según plano (ancho y profundidad para el sistema elegido: riel, roller o motorizado)", "Largo del cajón excediendo el vano lo indicado en plano a cada lado", "Cajón a nivel y paralelo a la carpintería", "Refuerzo de madera o perfil en el fondo para atornillar el riel o el motor", "Alimentación eléctrica en el cajón si la cortina es motorizada"]),
 ("Refuerzos y huecos", ["Refuerzos para TV, muebles colgantes, sanitarios suspendidos, barrales y luminarias pesadas según plano", "Huecos de spots y luminarias según plano de iluminación (centrados y alineados)", "Cajones o bajadas para aire acondicionado y rejillas de retorno según plano", "Tapas de inspección en llaves, cajas de paso, unidades de aire y colectores"]),
 ("Placas", ["Placa verde en baños y cocinas; placa roja donde se pida", "Juntas trabadas y siempre sobre perfil", "Tornillos a la distancia del fabricante y rehundidos sin romper el papel", "Instalaciones probadas antes de cerrar la segunda cara (foto)"]),
]),
E("impermeab", "Impermeabilizaciones y cubiertas", "Antes de taparlas con piso o carpeta.", "protex/protexguia", [
 ("Baños y balcones", ["Pendientes verificadas con agua", "Seal 77 Flex con bandas en encuentros y rejillas", "Altura en ducha ≥ 2,00 m", "Prueba de estanqueidad 48 h aprobada"]),
 ("Azoteas y terrazas", ["Pendiente hacia embudos verificada", "Medias cañas y babetas ≥ 20 cm", "Consumo del producto Protex según ficha (kg usados ÷ m²)", "Prueba de estanqueidad 48–72 h aprobada"]),
]),
E("revoques", "Revoques y contrapisos", "Antes de pisos, revestimientos y pintura.", "revoques/exterior", [
 ("Revoques", ["Malla soldada en todos los encuentros hormigón-ladrillo y canaletas, con solape ≥ 15 cm", "Salpicado parejo (con promotor de adherencia sobre hormigón)", "Fajas a plomo cada 1–1,5 m hechas después de las instalaciones", "Azotado hidrófugo continuo hasta la capa aisladora", "Mallas en encuentros de materiales", "Plomo y planeidad 3 mm en 2 m; aristas rectas", "Cajas eléctricas al ras del revoque"]),
 ("Contrapisos y carpetas", ["Relleno entre vigas invertidas con el material aprobado por el calculista (Isocret o cascote) y pases de desagote en cada cajón", "Niveles de piso terminado de cada local según plano (incluye diferencias por tipo de piso y umbrales)", "Pendientes en locales húmedos y exteriores", "Juntas perimetrales y de contracción", "Planeidad 2 mm en 2 m; sin sonido hueco"]),
]),
E("terminaciones", "Pisos, revestimientos y carpinterías", "Antes de pintura final.", "pisos/porcelanato", [
 ("Pisos y revestimientos", ["Despiece aprobado por arquitectura antes de colocar (arranques, cortes, juntas)", "Material del lote único y verificado (tono, calibre)", "Adhesivo correcto para cada uso (radiante, exterior, gran formato)", "Juntas alineadas y del ancho especificado", "Sin piezas huecas (golpear)"]),
 ("Carpinterías", ["Premarcos a plomo, nivel y escuadra", "Medidas y sentido de apertura según planilla", "Sellado perimetral continuo", "Carpinterías protegidas con film hasta el final"]),
]),
E("entrega", "Entrega final", "Antes de entregar al cliente.", "entrega/final", [
 ("Funcionamiento", ["Todas las instalaciones probadas en uso (agua, desagües, eléctrica, gas, climatización)", "Diferenciales probados", "Puertas, ventanas y cortinas abren y cierran bien"]),
 ("Documentación", ["Planos conforme a obra entregados", "Manual de uso y mantenimiento entregado y firmado", "Garantías y fichas de equipos entregadas"]),
 ("Limpieza", ["Obra limpia, sin restos de materiales", "Lista de observaciones del cliente cerrada"]),
]),
]
