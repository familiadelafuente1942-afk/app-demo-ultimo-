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

cambiar('const LINK_APP = "https://app-demo-ultimo.vercel.app/";', 'const LINK_APP = "https://www.instagram.com/belfast_cm/";')
cambiar('const linkP = LINK_APP + "?c=" + encodeURIComponent(p.id);', 'const linkP = LINK_APP;')
cambiar('"Mirá cómo funciona la app: {link_app}"', '"Pueden ver nuestras obras en {link_app}"')
cambiar('"{link_app} se reemplaza en cada mail por el link a la presentación de NEXO."', '"{link_app} se reemplaza en cada mail por el Instagram de Belfast."')
cambiar('const [adjuntarFolleto, setAdjuntarFolleto] = useState(true);', 'const [adjuntarFolleto, setAdjuntarFolleto] = useState(false);')
cambiar('React.createElement("input", { type: "checkbox", checked: adjuntarFolleto, onChange: e => setAdjuntarFolleto(e.target.checked) }),\n          "Adjuntar el folleto de NEXO en PDF"),', 'null, null),')
cambiar("placeholder: 'Ej: \"Mandales un mail de bienvenida presentando NEXO\"',", "placeholder: 'Ej: \"Presentá Belfast a los estudios de Nordelta para su próxima obra\"',")
cambiar('const BD_NOMBRE = "nexo";', 'const BD_NOMBRE = "belfast_ventas";')
cambiar('];\nfunction paisPorId(id) {',
        '].filter(p => p.id === "ar" || p.id === "uy").map(p => ({ ...p, perfiles: p.perfiles.filter(x => x.id === "estudios" || x.id === "desarrolladores") }));\nfunction paisPorId(id) {')
cambiar('PAISES.filter(pp => pp.id === "ar" || pp.id === "br" ||', 'PAISES.filter(pp => pp.id === "ar" || pp.id === "uy" ||')
cambiar('const [area, setArea] = useState("ceo");', 'const [area, setArea] = useState("comercial");')
cambiar('  activa: true\n}];\nfunction AreaMotor() {', '  activa: true\n}].filter(a => a.id === "comercial");\nfunction AreaMotor() {')
cambiar('objetivo: "Conseguir, calificar y acompañar constructoras, estudios de arquitectura, desarrolladoras y gerenciadoras hasta convertirlas en clientes de la plataforma."',
        'objetivo: "Conseguir, calificar y acompañar estudios de arquitectura y desarrolladoras inmobiliarias hasta convertirlos en clientes de Belfast."')
redactor_viejo = "Sos el redactor de NEXO, un sistema de gestión de obra para constructoras y estudios de arquitectura en "
redactor_nuevo = ("Sos el redactor comercial de Belfast Construction Management (@belfast_cm), constructora de alta gama con obras en Buenos Aires y Uruguay. "
                  "Belfast construye los proyectos que diseñan los estudios de arquitectura y que desarrollan las desarrolladoras inmobiliarias: ejecuta la obra con trabajo ordenado, "
                  "cuidado de la materialidad y respeto por la intención del proyecto. El mail va dirigido a un estudio o a una desarrolladora, para ofrecerle a Belfast como constructora de su próxima obra. "
                  "El tono es sobrio y elegante, nunca de oferta ni de descuento. No inventes obras, cifras ni clientes. Si invitás a ver obras, usá {link_app}, que lleva al Instagram de Belfast. El destinatario está en ")
cambiar(redactor_viejo, redactor_nuevo, veces=0)
s = re.sub(r"<title>.*?</title>", "<title>Belfast · Motor de Ventas</title>", s, count=1, flags=re.S)


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
s = s.replace('"🔗 Insertar link de la app"', '"🔗 Insertar link al Instagram"')
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
  if (document.readyState==="complete") setTimeout(abrir, 300); else window.addEventListener("load", function(){ setTimeout(abrir, 300); });
  new MutationObserver(function(){ marca(); }).observe(document.documentElement, {childList:true, subtree:true});
})();
</script>
'''
extra = extra.replace("__TEMA__", (raiz / "scripts" / "belfast-tema.html").read_text(encoding="utf-8"))
cambiar('<div id="vista-ventas"><div id="root-ventas"></div></div>', '<div id="vista-ventas">' + (raiz / "scripts" / "belfast-portada.html").read_text(encoding="utf-8") + '<div id="root-ventas"></div></div>')
cambiar("</head>", '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></head>')
i = s.rfind("</body>")
s = s[:i] + extra + s[i:]
cambiar('href="apple-touch-icon.png"', 'href="belfast-icon-192.png"', veces=0) if 'href="apple-touch-icon.png"' in s else None
for a, b in [("#B0894F", "#9C8700"), ("#E3BE78", "#D4B800"), ("#9A6B1E", "#6F6100"), ("#EBDCC0", "#ECE6BF"), ("#FBF2E3", "#F7F4E2"), ("#FBF6EE", "#F8F6EC")]:
    s = s.replace(a, b).replace(a.lower(), b)
s = s.replace('"#0E1520"', '"#1C1B1B"').replace("background:#0E1520", "background:#1C1B1B")
(raiz / "belfast-ventas.html").write_text(s, encoding="utf-8")
print("belfast-ventas.html listo,", len(s), "bytes")
