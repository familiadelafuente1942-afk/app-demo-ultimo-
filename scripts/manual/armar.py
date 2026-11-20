# Arma manual-obra.html desde el contenido (c1.py, c2.py) y la plantilla.
import json, pathlib
aqui = pathlib.Path(__file__).parent
g = {}
exec((aqui / "c1.py").read_text(encoding="utf-8"), g)
exec((aqui / "c2.py").read_text(encoding="utf-8"), g)
exec((aqui / "c3.py").read_text(encoding="utf-8"), g)
t = (aqui / "plantilla.html").read_text(encoding="utf-8").replace("__DATOS__", json.dumps(g["C"], ensure_ascii=False))
(aqui.parent.parent / "manual-obra.html").write_text(t, encoding="utf-8")
print("manual-obra.html listo:", len(g["C"]), "capítulos,", sum(len(c["s"]) for c in g["C"]), "temas")
