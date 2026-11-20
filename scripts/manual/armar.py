# Arma manual-obra.html desde el contenido (c1.py, c2.py) y la plantilla.
import json, pathlib
aqui = pathlib.Path(__file__).parent
g = {}
exec((aqui / "c1.py").read_text(encoding="utf-8"), g)
exec((aqui / "c2.py").read_text(encoding="utf-8"), g)
exec((aqui / "c3.py").read_text(encoding="utf-8"), g)
exec((aqui / "c4.py").read_text(encoding="utf-8"), g)
exec((aqui / "c5.py").read_text(encoding="utf-8"), g)
REAL={"principios/reglas":"ob-01","principios/roles":"ob-05","principios/registro":"ob-07","obrador/cerco":"ob-13","obrador/acopio":"ob-11","obrador/seguridad":"ob-12","subsuelos/tabiques":"ob-02","estructura/encofrados":"ob-04","estructura/armaduras":"ob-08","fundaciones/vigasfund":"ob-09","estructura/hormigonado":"ob-06"}
URLS=json.loads((aqui.parent.parent/"manual-fotos/urls.json").read_text())
# Fotos reales de obras Belfast enviadas por Sebastián (manual-reales/)
MALAS={"mamposteria/canaletas":["mal-cajon-picado-1","mal-cajon-picado-2","mal-sanitaria-faja","mal-canaleta-diagonal","mal-canaleta-cruza-1","mal-canaleta-cruza-2","mal-picado-revoque","mal-tablero-canaletas","mal-canos-sobre-revoque","mal-bajada-exterior"],"mamposteria/capaaisladora":["mal-cajon-picado-1","mal-cajon-picado-2"],"revoques/salpicado":["mal-sanitaria-faja","mal-picado-revoque"],"electrica/canerias":["mal-canaleta-diagonal","mal-canaleta-cruza-1"]}
REALES={"estructura/hormigonado":["hormigonado-losa","probetas"],"subsuelos/impermeab":["revoque-subsuelo"],"obrador/cerco":["obrador-aire"],"principios/registro":["planos-obrador"],"mamposteria/capaaisladora":["cajon-hidrofugo-1","cajon-hidrofugo-2","cajon-hidrofugo-3","capa-aisladora-muros","arranque-columnas"],"revoques/exterior":["malla-encuentro"],"mamposteria/muros":["obra-belfast-equipo","capa-aisladora-muros"],"revoques/malla":["malla-columna-1","malla-columna-2","malla-columna-3","malla-encuentro","canaleta-malla"],"revoques/salpicado":["fajas-1","fajas-2","canaleta-malla"],"revoques/interior":["revoque-terminado","fajas-1"],"subsuelos/contrapisosub":["contrapiso-subsuelo-1","contrapiso-subsuelo-2"],"contrapisos/carpetas":["contrapiso-subsuelo-1"],
 "seco/colgadas":["colgadas-pasillo","colgadas-planta"],"electrica/canerias":["canaleta-malla","canos-piso"],"electrica/tablero":["tablero"],
 "protex/cristalizante":["junta-hidroexpansiva"],"subsuelos/tabiques":["junta-hidroexpansiva","tabique-armadura"],"estructura/armaduras":["tabique-armadura"],
 "cubiertas/azotea":["terraza-parapeto","terraza-contrapiso"],"contrapisos/pendientes":["terraza-contrapiso"],"contrapisos/invertidas":["terraza-contrapiso","terraza-parapeto"],"clima/radiante":["losa-radiante"]}
OTRA={"mamposteria/canaletas":"manual-reales/mal-cajon-picado-1.jpg","revoques/malla":"manual-fotos/revoques-exterior.jpg","revoques/salpicado":"manual-fotos/revoques-exterior.jpg","contrapisos/invertidas":"manual-fotos/contrapisos-alivianado.jpg","seco/cielorraso":"manual-fotos/seco-placas.jpg","estructura/calor":"manual-fotos/estructura-curado.jpg"}
for c in g["C"]:
    for s in c["s"]:
        k=c["id"]+"/"+s["id"]
        s["reales"]=["manual-reales/"+x+".jpg" for x in REALES.get(k,[])]
        s["malas"]=["manual-reales/"+x+".jpg" for x in MALAS.get(k,[])]
        if k in REAL: s["foto"]="belfast-obra/"+REAL[k]+".jpg"; s["fr"]=1
        elif k in OTRA: s["foto"]=OTRA[k]; s["fr"]=0
        else: s["foto"]="manual-fotos/"+c["id"]+"-"+s["id"]+".jpg"; s["fr"]=0
        if s["fr"]==0 and s["reales"] and not (aqui.parent.parent/s["foto"]).exists() and c["id"]+"-"+s["id"] not in URLS: s["foto"]=s["reales"][0]; s["fr"]=1
t = (aqui / "plantilla.html").read_text(encoding="utf-8").replace("__DATOS__", json.dumps(g["C"], ensure_ascii=False)).replace("__PROT__", json.dumps(g["PROT"], ensure_ascii=False))
(aqui.parent.parent / "manual-obra.html").write_text(t, encoding="utf-8")
print("manual-obra.html listo:", len(g["C"]), "capítulos,", sum(len(c["s"]) for c in g["C"]), "temas")
