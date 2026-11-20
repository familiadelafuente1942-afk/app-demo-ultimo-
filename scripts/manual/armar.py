# Arma manual-obra.html desde el contenido (c1.py, c2.py) y la plantilla.
import json, pathlib
aqui = pathlib.Path(__file__).parent
g = {}
exec((aqui / "c1.py").read_text(encoding="utf-8"), g)
exec((aqui / "c2.py").read_text(encoding="utf-8"), g)
exec((aqui / "c3.py").read_text(encoding="utf-8"), g)
REAL={"principios/reglas":"ob-01","principios/roles":"ob-05","principios/registro":"ob-07","obrador/cerco":"ob-13","obrador/acopio":"ob-11","obrador/seguridad":"ob-12","subsuelos/tabiques":"ob-02","estructura/encofrados":"ob-04","estructura/armaduras":"ob-08","fundaciones/vigasfund":"ob-09","estructura/hormigonado":"ob-06"}
for c in g["C"]:
    for s in c["s"]:
        k=c["id"]+"/"+s["id"]
        if k in REAL: s["foto"]="belfast-obra/"+REAL[k]+".jpg"; s["fr"]=1
        else: s["foto"]="manual-fotos/"+c["id"]+"-"+s["id"]+".jpg"; s["fr"]=0
t = (aqui / "plantilla.html").read_text(encoding="utf-8").replace("__DATOS__", json.dumps(g["C"], ensure_ascii=False))
(aqui.parent.parent / "manual-obra.html").write_text(t, encoding="utf-8")
print("manual-obra.html listo:", len(g["C"]), "capítulos,", sum(len(c["s"]) for c in g["C"]), "temas")
