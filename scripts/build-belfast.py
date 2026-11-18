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

cambiar('const BD_NOMBRE = "nexo";', 'const BD_NOMBRE = "belfast_ventas";')
cambiar("// Dónde buscar además de la web general.",
        'PERFILES_BUSQUEDA.splice(0, PERFILES_BUSQUEDA.length, ...PERFILES_BUSQUEDA.filter(p => p.id === "estudios" || p.id === "desarrolladores"));\n// Dónde buscar además de la web general.')
cambiar('const [area, setArea] = useState("ceo");', 'const [area, setArea] = useState("comercial");')
cambiar('  activa: true\n}];\nfunction AreaMotor() {', '  activa: true\n}].filter(a => a.id === "comercial");\nfunction AreaMotor() {')
cambiar('objetivo: "Conseguir, calificar y acompañar constructoras, estudios de arquitectura, desarrolladoras y gerenciadoras hasta convertirlas en clientes de la plataforma."',
        'objetivo: "Conseguir, calificar y acompañar estudios de arquitectura y desarrolladoras inmobiliarias hasta convertirlos en clientes de Belfast."')
redactor_viejo = "Sos el redactor de NEXO, un sistema de gestión de obra para constructoras y estudios de arquitectura en "
redactor_nuevo = ("Sos el redactor comercial de Belfast Construction Management, empresa constructora y gerenciadora que construye "
                  "casas y edificios para estudios de arquitectura y desarrolladoras inmobiliarias (obra gris, llave en mano y gerenciamiento), en ")
cambiar(redactor_viejo, redactor_nuevo, veces=0)
s = re.sub(r"<title>.*?</title>", "<title>Belfast · Motor de Ventas</title>", s, count=1, flags=re.S)

extra = r'''
<style id="belfast-marca">
  #barra-volver .vb{display:none!important}
  img.logo-belfast{background:#000;border-radius:50%}
</style>
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
i = s.rfind("</body>")
s = s[:i] + extra + s[i:]
cambiar('href="apple-touch-icon.png"', 'href="belfast-icon-192.png"', veces=0) if 'href="apple-touch-icon.png"' in s else None
(raiz / "belfast-ventas.html").write_text(s, encoding="utf-8")
print("belfast-ventas.html listo,", len(s), "bytes")
