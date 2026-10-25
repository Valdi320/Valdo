# SPDX-License-Identifier: MIT
"""Importar una captura como documento nuevo; nunca modifica el maestro del robot."""
from pathlib import Path
import hashlib
import json
import re
from validar_ficha import validate, FIELDS


def make_document(data, source_text=None, ensayo_software=False):
    import FreeCAD as App
    result = validate(data)
    if not result["puertas"]["registro"]:
        raise ValueError("\n".join(result["errores"]))
    if ensayo_software and data["origen"] != "prueba_software":
        raise ValueError("El modo ensayo requiere origen prueba_software.")
    slug = re.sub(r"[^A-Za-z0-9_]", "_", data["id_captura"])
    doc = App.newDocument("Captura_" + slug)
    doc.Label = ("ENSAYO SOFTWARE · " if data["origen"] == "prueba_software" else "Captura · ") + data["id_captura"]
    doc.Comment = "Medidas declaradas; sin validación física, ubicación global o aprobación de fabricación."
    doc.CreatedBy = "Valdi320/Valdo — captura de rueda"
    group = doc.addObject("App::DocumentObjectGroup", "Ficha")
    group.Label = "01 · Datos y procedencia de la captura"
    status = doc.addObject("App::FeaturePython", "AlcanceCaptura")
    status.Label = "LEER · alcance de estos datos"
    group.addObject(status)
    source = source_text if source_text is not None else json.dumps(data,ensure_ascii=False,sort_keys=True)
    properties = {
        "IdCaptura": data["id_captura"], "OrigenDatos": data["origen"],
        "FechaMedicion": data["fecha_medicion"], "Instrumento": data["instrumento"],
        "Condicion": data["condicion"], "PiezaPasador": data["pieza_pasador"], "PiezaRueda": data["pieza_rueda"],
        "Lado": data["lado"]["valor"], "EvidenciaLado": data["lado"]["evidencia"],
        "Pareja": data["pareja"]["estado"], "EvidenciaPareja": data["pareja"]["evidencia"],
        "SeccionPasador": data["seccion_pasador"]["forma"],
        "FuenteSHA256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "OrigenGeometrico": "Local y convencional: Z sigue el pasador, origen en un extremo abstracto; sin transformación al robot",
        "Fabricacion": "NO APROBADA; sin perfil de extremos, ajustes, material, retención, soporte ni ensayos",
        "Integracion": "Documento independiente; no modifica parámetros DEMO ni el maestro de arquitectura",
        "EdicionPosterior": "Editar la geometría no cambia ni demuestra las medidas declaradas en esta captura",
        "Notas": data["notas"],
    }
    for key, value in properties.items():
        status.addProperty("App::PropertyString", key, "Captura")
        setattr(status,key,str(value))
    status.addProperty("App::PropertyBool", "ValidacionFisica", "Captura")
    status.ValidacionFisica = False
    status.addProperty("App::PropertyString", "DatosJSON", "Captura")
    status.DatosJSON = json.dumps(data,ensure_ascii=False,sort_keys=True)
    table=doc.addObject("Spreadsheet::Sheet", "MedicionesDeclaradas")
    table.Label="Tabla · valores declarados, pendientes y procedencia"
    group.addObject(table)
    for col,txt in zip("ABCDEFGHI",["Magnitud","Estado","Valor mm","Lecturas mm","Incertidumbre mm","Referencias","Evidencia","Nota","Mxx"]):table.set(col+"1",txt)
    table.setStyle("A1:I1","bold","add")
    for row,m in enumerate(data["mediciones"],2):
        definition=FIELDS[m["id"]]
        vals=[definition["nombre"],m["estado"],"" if m["valor_mm"] is None else str(m["valor_mm"]),"; ".join(map(str,m["lecturas_mm"])),"SIN EVALUAR" if m["incertidumbre_mm"] is None else str(m["incertidumbre_mm"]),m["referencias"],m["evidencia"] or data["evidencia_general"],m["nota"],definition["mediciones"]]
        for col,value in zip("ABCDEFGHI",vals):
            # Force text for descriptions: imported '=' must not become an expression.
            table.set(col+str(row), "'"+value if col not in {"C","E"} or not value or value=="SIN EVALUAR" else value)
    for col,width in [("A",300),("B",140),("C",90),("D",160),("E",140),("F",300),("G",250),("H",260),("I",220)]:table.setColumnWidth(col,width)
    measured={m["id"]:m for m in data["mediciones"] if m["estado"]=="medido"}
    can_test=ensayo_software and data["seccion_pasador"]["forma"]=="circular" and {"pasador_diametro","pasador_longitud"}<=set(measured)
    if result["puertas"]["pasador_local"] or can_test:
        pin=doc.addObject("Part::Cylinder","ReferenciaPasador")
        pin.Label=("ENSAYO FICTICIO · " if can_test else "Referencia simplificada · ")+"cuerpo y longitud declarados del pasador"
        pin.Radius=measured["pasador_diametro"]["valor_mm"]/2
        pin.Height=measured["pasador_longitud"]["valor_mm"]
        pin.addProperty("App::PropertyString","Alcance","Captura")
        pin.Alcance="Referencia cilíndrica simplificada; no reproduce cabeza, ranuras, extremos o retención. No es un repuesto fabricable."
        pin.addProperty("App::PropertyString","DatosOrigen","Captura")
        pin.DatosOrigen=data["id_captura"]+" / pasador_diametro + pasador_longitud"
        pin.addProperty("App::PropertyBool","EnsayoSoftware","Captura")
        pin.EnsayoSoftware=can_test
        if App.GuiUp:
            pin.ViewObject.ShapeColor=(0.91,0.45,0.18) if can_test else (0.10,0.52,0.58)
            pin.ViewObject.DisplayMode="Flat Lines"
    doc.recompute()
    if App.GuiUp and doc.getObject("ReferenciaPasador"):
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
    return doc,result


def save_new_document(doc,path):
    target=Path(path)
    if target.suffix.lower()!=".fcstd":raise ValueError("La salida debe terminar en .FCStd")
    if target.exists():raise FileExistsError("No se sobrescribe un archivo existente: "+str(target))
    doc.saveAs(str(target))
    return target
