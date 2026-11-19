#!/usr/bin/env python3
"""Genera belfast-ventas.html (Motor de Ventas de Belfast) a partir de index.html.
Misma app y mismas funciones de ventas, pero: base de datos propia (no se mezcla con NEXO),
solo el área Comercial, logo de Belfast, y búsqueda/mails pensados para el cliente de Belfast:
estudios de arquitectura y desarrolladoras inmobiliarias.
Correr de nuevo cada vez que cambie index.html:  python3 scripts/build-belfast.py"""
import pathlib, re, sys
raiz = pathlib.Path(__file__).resolve().parent.parent
s = (raiz / "index.html").read_text(encoding="utf-8")

def cambiar(viejo, nuevo, veces=1):
    global s
    n = s.count(viejo)
    if n < 1 or (veces and n != veces):
        sys.exit(f"No encontré (o hay {n}): {viejo[:80]}")
    s = s.replace(viejo, nuevo)

# Web de Belfast (versión de prueba de Deploy Studio; cuando esté en belfastcm.com, cambiar solo esta línea)
WEB_BELFAST = "https://belfastcm.contact-deploystudio.workers.dev"
cambiar('const LINK_APP = "https://app-demo-ultimo.vercel.app/";', 'const LINK_APP = "' + WEB_BELFAST + '/obras";')
cambiar('const linkP = LINK_APP + "?c=" + encodeURIComponent(p.id);', 'const linkP = LINK_APP;')
cambiar('"Mirá cómo funciona la app: " + LINK_APP', '"Pueden ver nuestras obras en " + LINK_APP')
cambiar('"Agrega al final del mail el link a la presentación de NEXO."', '"Agrega al final del mail el link a las obras en la web de Belfast."')
cambiar('const [adjuntarFolleto, setAdjuntarFolleto] = useState(true);', 'const [adjuntarFolleto, setAdjuntarFolleto] = useState(false);')
cambiar('React.createElement("input", { type: "checkbox", checked: adjuntarFolleto, onChange: e => setAdjuntarFolleto(e.target.checked) }),\n          "Adjuntar el folleto de NEXO en PDF"),', 'null, null),')
cambiar("placeholder: 'Ej: \"Mandales un mail de bienvenida presentando NEXO\"',", "placeholder: 'Ej: \"Presentá Belfast a los estudios de Nordelta para su próxima obra\"',")
cambiar('const BD_NOMBRE = "nexo";', 'const BD_NOMBRE = "belfast_ventas";')
cambiar('];\nfunction paisPorId(id) {',
        '].filter(p => p.id === "ar" || p.id === "uy").map(p => ({ ...p, perfiles: p.perfiles.filter(x => x.id === "estudios" || x.id === "desarrolladores") }));\nfunction paisPorId(id) {')
cambiar('PAISES.filter(pp => pp.id === "ar" || pp.id === "br" ||', 'PAISES.filter(pp => pp.id === "ar" || pp.id === "uy" ||')
cambiar('const [area, setArea] = useState("ceo");', 'const [area, setArea] = useState("comercial");')
cambiar('  activa: true\n}];\nfunction AreaMotor() {', '  activa: true\n}].filter(a => a.id === "comercial" || a.id === "motor");\nfunction AreaMotor() {')
cambiar('src: "motor.html", title: "Motor de marketing"', 'src: "belfast-motor.html", title: "Motor de Belfast"')
cambiar('objetivo: "Conseguir, calificar y acompañar constructoras, estudios de arquitectura, desarrolladoras y gerenciadoras hasta convertirlas en clientes de la plataforma."',
        'objetivo: "Conseguir, calificar y acompañar estudios de arquitectura y desarrolladoras inmobiliarias hasta convertirlos en clientes de Belfast."')
redactor_viejo = "Sos el redactor de NEXO, un sistema de gestión de obra para constructoras y estudios de arquitectura en "
redactor_nuevo = ("Sos el redactor comercial de Belfast Construction Management (@belfast_cm), constructora de alta gama con obras en Buenos Aires y Uruguay. "
                  "Belfast construye los proyectos que diseñan los estudios de arquitectura y que desarrollan las desarrolladoras inmobiliarias: ejecuta la obra con trabajo ordenado, "
                  "cuidado de la materialidad y respeto por la intención del proyecto. El mail va dirigido a un estudio o a una desarrolladora, para ofrecerle a Belfast como constructora de su próxima obra. "
                  "El tono es sobrio y elegante, nunca de oferta ni de descuento. No inventes obras, cifras ni clientes. Si invitás a ver obras, usá {link_app}, que lleva al Instagram de Belfast. El destinatario está en ")
cambiar(redactor_viejo, redactor_nuevo, veces=0)
s = re.sub(r"<title>.*?</title>", "<title>Belfast Construction Management</title>", s, count=1, flags=re.S)


# Asistente por prospecto: vende Belfast (la constructora), no el software NEXO.
ini = s.index("  const PRODUCTO = `"); fin = s.index("`.trim();", ini)
s = s[:ini] + """  const PRODUCTO = `
EMPRESA: Belfast Construction Management (@belfast_cm). Constructora de alta gama con obras en Buenos Aires y Uruguay.
QUÉ HACE: construye los proyectos que diseñan los estudios de arquitectura y que llevan adelante las desarrolladoras inmobiliarias.
Acompaña la obra completa en tres etapas: planificación, proceso y ejecución, y terminación.
CÓMO TRABAJA: trabajo ordenado en obra, cuidado de la materialidad (hormigón, mampostería, terminaciones) y respeto por la
intención de cada proyecto. Lema: "Cada proyecto tiene su propia intención. Nuestro trabajo es cuidarla en cada decisión de obra."
OBRAS PARA MOSTRAR: las publica en su Instagram @belfast_cm (por ejemplo Casa Cielo en obra, piletas, estructuras de hormigón y terminaciones).
A QUIÉN LE VENDE: estudios de arquitectura (que necesitan una constructora que respete su proyecto) y desarrolladoras (que necesitan cumplir plazos y calidad).
""" + s[fin:]
s = s.replace("Sos el asistente comercial de una empresa argentina que vende este sistema.", "Sos el asistente comercial de Belfast, una constructora que ofrece construir la próxima obra de estudios y desarrolladoras.")
s = s.replace("- NUNCA prometas funciones que no estén en la descripción de arriba.", "- NUNCA inventes obras, clientes, plazos ni cifras que no estén en la descripción de arriba.")
s = s.replace("Cerrá pidiendo 20 minutos para mostrarle la demo.", "Cerrá pidiendo 20 minutos para mostrarle obras de Belfast.")
s = s.replace("EN QUÉ ORDEN MOSTRAR LA DEMO (4 pasos con funciones reales)", "QUÉ OBRAS Y QUÉ ETAPAS MOSTRARLE (4 puntos)")
s = s.replace("qué apps le corresponden por su rol", "cómo Belfast acompañaría su obra en cada etapa")
s = s.replace('"Ej: \\"Mandales un mail de bienvenida presentando NEXO, corto y cordial\\""', '"Ej: \\"Presentá Belfast como constructora para su próxima obra, corto y cordial\\""')
s = s.replace("'Ej: \"Mandales un mail de bienvenida presentando NEXO, corto y cordial\"'", "'Ej: \"Presentá Belfast como constructora para su próxima obra, corto y cordial\"'")
s = s.replace('"🔗 Insertar link de la app"', '"🔗 Insertar link a las obras"')
s = s.replace('"Respuesta de NEXO"', '"Respuesta de Belfast"')
s = s.replace('desc: "Precio, tiempo, \\"ya tengo Excel\\""', 'desc: "Precio, plazos, \\"ya tenemos constructora\\""')

# Sin la ficha grande de "Director Comercial IA" arriba: se entra directo a las herramientas.
cambiar('  }))), contenido, /*#__PURE__*/React.createElement("div", {', '  }))), /*#__PURE__*/React.createElement("div", { className: "ficha-contenido" }, contenido), /*#__PURE__*/React.createElement("div", {')
cambiar('''  const pendiente = estado === "pendiente";
  return /*#__PURE__*/React.createElement("div", null, ''', '''  const pendiente = estado === "pendiente";
  return /*#__PURE__*/React.createElement("div", { className: "ficha-agente" }, ''')
# Traer de la base de NEXO (mismo navegador) los estudios y las desarrolladoras.
ini = s.index("  async function cargarEncontrados() {"); fin = s.index("  }", s.index('setAviso("No pude leer el archivo de contactos encontrados.")'))
s = s[:ini] + """  async function cargarEncontrados() {
    try {
      const lista = await new Promise((ok, mal) => {
        const rq = indexedDB.open("nexo");
        rq.onerror = () => mal(rq.error);
        rq.onsuccess = () => { const db = rq.result; if (!db.objectStoreNames.contains("prospectos")) { db.close(); ok([]); return; }
          const g = db.transaction("prospectos", "readonly").objectStore("prospectos").getAll(); g.onsuccess = () => { ok(g.result || []); db.close(); }; g.onerror = () => mal(g.error); };
      });
      let base = [];
      try { base = await (await fetch("belfast-base.json?v=" + Date.now())).json(); } catch (e) {}
      const sirve = lista.concat(base).filter(x => /^(estud|desarr)/i.test(String(x.rol || "")));
      let n = 0;
      setProspectos(prev => {
        const ya = new Set(prev.map(p => nombreClave(p.empresa))), mails = new Set(prev.map(p => String(p.mail || "").toLowerCase()).filter(Boolean));
        const nuevos = sirve.filter(x => !ya.has(nombreClave(x.empresa)) && !(x.mail && mails.has(String(x.mail).toLowerCase()))).map((x, i) => ({ ...x, id: Date.now() + i, estado: "nuevo", historial: [] }));
        n = nuevos.length; return [...nuevos, ...prev];
      });
      setTimeout(() => setAviso(n ? `Traje ${n} estudios y desarrolladoras de la base de NEXO` : "Ya estaban todos los estudios y desarrolladoras de NEXO."), 80);
    } catch { setAviso("No pude leer la base de NEXO en este navegador."); }
""" + s[fin:]
cambiar('  async function cargarEncontrados() {', '  React.useEffect(() => { if (prospectosAll.length === 0) { const t = setTimeout(() => { try { if (!localStorage.getItem("bf_base_cargada")) { localStorage.setItem("bf_base_cargada", "1"); cargarEncontrados(); } } catch (e) {} }, 1500); return () => clearTimeout(t); } }, []);\n  async function cargarEncontrados() {')
cambiar('}, "Cargar contactos encontrados por Claude"),', '}, "Traer estudios y desarrolladoras de NEXO"),')

cambiar('  const [perfs, setPerfs] = useState(["estudios", "constructoras"]);', '  const [perfs, setPerfs] = useState(["estudios", "desarrolladores"]);')

# Belfast no sincroniza con la nube de NEXO (son bases separadas).
cambiar('<script src="supabase-sync.js"></script>', '')

s = s.replace('"Las métricas de correos, respuestas y reuniones necesitan el motor de agentes y el envío de correo. Lo que ves abajo son las herramientas que ya funcionan."', '""')

extra = r'''
__TEMA__
<script>
// Hasta que Belfast tenga su propia casilla configurada, no se manda nada desde la cuenta de NEXO.
(function(){ var f0 = window.fetch; window.fetch = function(u, o){ if (/\/functions\/v1\/enviar-mail|accion=enviar_mail/.test(String(u && u.url || u))) return Promise.resolve(new Response(JSON.stringify({ error: "El mail de Belfast todavía no está configurado. No se mandó nada." }), { status: 409, headers: { "Content-Type": "application/json" } })); return f0.apply(this, arguments); }; })();
window.ROLES_VENTAS = [["todos","Todos"],["estudio","Estudios de arquitectura"],["desarrollador","Desarrolladoras inmobiliarias"]];
(function(){
  // Solo el área Comercial
  function marca(){
    document.querySelectorAll('img[alt="NEXO"]').forEach(function(im){ if(im.dataset.bf) return; im.dataset.bf="1"; im.src="belfast-logo.png"; im.alt="Belfast"; im.classList.add("logo-belfast"); });
    document.querySelectorAll("button,span,div").forEach(function(el){
      if(el.children.length===0){ var t=el.textContent;
        if(t==="Centro de Operaciones IA") el.textContent="Belfast · Motor de Ventas";
        else if(t==="Demo del sistema") el.textContent="Belfast Construction Management";
        else if(/\d+ de \d+ áreas conectadas/.test(t)) el.textContent="Estudios de arquitectura y desarrolladoras";
      }
    });
  }
  function abrir(){ try { if (typeof abrirVentas==="function") abrirVentas(); } catch(e){} marca(); }
  // Tocar el logo abre / cierra el panel de ventas (como en NEXO).
  document.addEventListener("click", function(e){ var t = e.target && e.target.closest && e.target.closest("#bf-logo"); if (!t) return; e.preventDefault(); document.body.classList.toggle("bf-panel"); try { window.scrollTo(0, 0); } catch(x){} });
  // Espera: después de un rato sin tocar nada en la presentación, pasan las fotos del Instagram.
  (function(){
    var fotos = ["06","09","04","02","05","07","03","10","11","08","12","01"].map(function(n){ return "belfast-ig/ig-" + n + ".jpg"; });
    var ov, img, fondo, i = 0, reloj = null, pase = null, ESPERA = 25000;
    function mostrar(){ img.classList.remove("vis"); setTimeout(function(){ var f = fotos[i++ % fotos.length]; img.onload = function(){ img.classList.add("vis"); }; img.src = f; fondo.style.backgroundImage = "url(" + f + ")"; }, 450); }
    function entrar(){ if (document.body.classList.contains("bf-panel")) { armar(); return; } ov.classList.add("on"); mostrar(); pase = setInterval(mostrar, 6000); }
    function salir(){ if (pase) { clearInterval(pase); pase = null; } if (ov) ov.classList.remove("on"); armar(); }
    function armar(){ clearTimeout(reloj); reloj = setTimeout(entrar, ESPERA); }
    function iniciar(){ ov = document.getElementById("bf-espera"); if (!ov) return; img = ov.querySelector(".bf-esp-foto"); fondo = ov.querySelector(".bf-esp-fondo");
      ["pointerdown","keydown","wheel","touchstart","scroll"].forEach(function(ev){ window.addEventListener(ev, function(){ if (ov.classList.contains("on")) salir(); else armar(); }, { passive: true, capture: true }); });
      armar(); }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
  })();
  if (document.readyState==="complete") setTimeout(abrir, 300); else window.addEventListener("load", function(){ setTimeout(abrir, 300); });
  new MutationObserver(function(){ marca(); }).observe(document.documentElement, {childList:true, subtree:true});
})();
</script>
'''
extra = extra.replace("__TEMA__", "")
TEMA = (raiz / "scripts" / "belfast-tema.html").read_text(encoding="utf-8")
# Textos propios de Belfast para el selector de idiomas (se suman al diccionario de NEXO).
TEMA += "<script>window.DICC_N3=Object.assign(window.DICC_N3||{}," + (raiz / "scripts" / "belfast-dicc.json").read_text(encoding="utf-8") + ");</script>"
cambiar('<div id="vista-ventas"><div id="root-ventas"></div></div>', '<div id="vista-ventas">' + (raiz / "scripts" / "belfast-portada.html").read_text(encoding="utf-8") + '<div id="root-ventas"></div></div>')
cambiar("</head>", '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">' + TEMA + '<style>body.en-ventas #barra-volver{display:none!important} html,body{background:#282627}</style></head>')
# Guía de ventas propia de Belfast (constructora), en lugar de la de NEXO (software).
import re as _re, json as _json
_g = _json.loads((raiz / "scripts" / "belfast-guia.json").read_text(encoding="utf-8"))
_m = _re.search(r"function GuiaVentas\(\) \{\n  const bloques = \[.*?\];\n  return", s, _re.S)
assert _m, "no encontré la guía de ventas"
_gm = _json.loads((raiz / "scripts" / "belfast-guia-motor.json").read_text(encoding="utf-8"))
s = s[:_m.start()] + "const GUIA_MOTOR = " + _json.dumps(_gm, ensure_ascii=False) + ";\nfunction GuiaVentas(props) {\n  const bloques = (props && props.bloques) || " + _json.dumps(_g, ensure_ascii=False) + ";\n  return" + s[_m.end():]
# Pestaña nueva al final: Guía del motor
_t = '["guia", "Guía de ventas"]].map('
assert _t in s
s = s.replace(_t, '["guia", "Guía de ventas"], ["guiamotor", "Guía del motor"]].map(', 1)
_v = 'vista === "guia" && /*#__PURE__*/React.createElement(GuiaVentas, null)'
assert _v in s
s = s.replace(_v, _v + ', vista === "guiamotor" && /*#__PURE__*/React.createElement(GuiaVentas, { bloques: GUIA_MOTOR })', 1)
# Que el primer pantallazo ya sea Belfast (sin mostrar la portada de NEXO mientras carga).
cambiar('<body class="no-js">', '<body class="no-js en-ventas con-motor">')
i = s.rfind("</body>")
s = s[:i] + extra + s[i:]
cambiar('href="apple-touch-icon.png"', 'href="belfast-icon-192.png"', veces=0) if 'href="apple-touch-icon.png"' in s else None
for a, b in [("#B0894F", "#9C8700"), ("#E3BE78", "#D4B800"), ("#9A6B1E", "#6F6100"), ("#EBDCC0", "#ECE6BF"), ("#FBF2E3", "#F7F4E2"), ("#FBF6EE", "#F8F6EC")]:
    s = s.replace(a, b).replace(a.lower(), b)
s = s.replace('"#0E1520"', '"#1C1B1B"').replace("background:#0E1520", "background:#1C1B1B")
(raiz / "belfast-ventas.html").write_text(s, encoding="utf-8")

# Motor de Belfast: el mismo motor de NEXO, con sus datos aparte (marca=belfast) y sin envíos hasta tener su casilla.
m = (raiz / "motor.html").read_text(encoding="utf-8")
def mrep(a, b):
    global m
    if a not in m: sys.exit("motor: no encontré " + a[:60])
    m = m.replace(a, b)
mrep('"/api/motor?accion="+a', '"/api/motor?marca=belfast&accion="+a')
mrep("<title>Motor de marketing</title>", "<title>Motor de Belfast</title>")
mrep("--bg:#0e1116;--card:#171c24;--bd:#2a3340;--tx:#e8edf3;--mu:#97a3b3;--br:#c9a35a;", "--bg:#1C1B1B;--card:#282627;--bd:#3a3738;--tx:#f2f1ef;--mu:#a9a6a3;--br:#D4B800;")
mrep('<select id="pais"><option value="ar">Argentina</option><option value="br">Brasil</option><option value="py">Paraguay</option><option value="cl">Chile</option></select>', '<select id="pais"><option value="ar">Argentina</option><option value="uy">Uruguay</option></select><select id="rubro"><option value="estudios de arquitectura">Estudios de arquitectura</option><option value="desarrolladoras inmobiliarias">Desarrolladoras inmobiliarias</option></select>')
mrep('<select id="idi"><option value="es">Español</option><option value="pt">Portugués</option><option value="en">Inglés</option></select>', '<select id="idi"><option value="es">Español</option></select>')
mrep('<button id="btnAct" class="stop" onclick="alternar()">…</button>', '<button id="btnAct" class="stop" style="display:none">…</button><span class="mu">Los envíos quedan frenados hasta configurar info@belfastcm.com. Podés buscar, redactar y aprobar.</span>')
mrep('<h2 style="margin:0">Estado del motor: <span id="est" class="off">FRENADO</span></h2><div class="mu" id="ayuda"></div>', '<h2 style="margin:0">Motor de Belfast <span id="est" style="display:none"></span></h2><div class="mu" id="ayuda" style="display:none"></div>')
mrep('<div class="card"><h2>Topes</h2>', '<div class="card" style="display:none"><h2>Topes</h2>')
mrep('<div class="card"><h2>4 · Videos para Reels</h2>', '<div class="card" style="display:none"><h2>4 · Videos para Reels</h2>')
mrep('{pais:$("pais").value,zona:$("zona").value}', '{pais:$("pais").value,zona:$("zona").value,rubro:$("rubro").value}')
m = m.replace(";reels()}", "}")
mrep('["Gmail",k.gmail]', '["Mail de Belfast (info@belfastcm.com, falta configurar)",false]')
(raiz / "belfast-motor.html").write_text(m, encoding="utf-8")
print("belfast-motor.html listo")
print("belfast-ventas.html listo,", len(s), "bytes")
