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

extra = r'''
__TEMA__
<script>
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
