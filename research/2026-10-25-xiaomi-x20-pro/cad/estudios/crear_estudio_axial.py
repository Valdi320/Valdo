# SPDX-License-Identifier: MIT
"""Estudio nativo de presupuesto axial; no crea una pieza para fabricar."""
from pathlib import Path

SOURCE = "https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html"


def create_document():
    import FreeCAD as App
    doc = App.newDocument("EstudioAxialX20")
    doc.Label = "X20 Pro · presupuesto axial · fuente y escenarios · NO FABRICAR"
    doc.Comment = "Comparación documental, no medidas de la unidad, ajuste, retención o resistencia validados."
    info = doc.addObject("App::FeaturePython", "Alcance")
    info.Label = "LEER · procedencia y límites"
    for key,value in {
        "Revision":"0.3 / 2026-10-25",
        "FuenteNominal":SOURCE,
        "EstadoNominal":"PUBLICADO por vendedor SKU12584; diámetro y longitud total nominales. Tolerancia y longitud útil desconocidas.",
        "FuenteDEMO":"X20Pro_Base_Arquitectura.FCStd v0.1 / ParametrosDEMO. No representa geometría Xiaomi medida.",
        "Aporte":"Presupuesto axial revisado por Codex, commit f4d87c5626eefc67dadca1b4dc682d857b7a0d21; convertido a estudio CAD por ChatGPT.",
        "Convencion":"X sigue el eje abstracto de comparación. Separaciones Y y altura de bandas son sólo presentación; sin posición global del robot.",
        "LimiteModelo":"Los cilindros simplifican cuerpo y longitud. No modelan cabeza, ranuras, extremos, juego, retención ni geometría de módulo.",
        "LimiteTramos":"Las bandas son un diagrama longitudinal; no son apoyos diseñados ni sólidos candidatos a imprimir.",
        "Decision":"Descartar la disposición DEMO de 50 mm si se pretende usar un pasador nominal de 38,5 mm. No reducir hueco real desconocido para forzar encaje.",
        "Pendiente":"Ancho móvil, longitud útil, retención, tolerancias, cargas, materiales y acceso de extracción.",
        "Edicion":"B2/B3 son escenarios inicialmente vinculados a DiametroFuente/LongitudFuente. Editarlos explora hipótesis y no cambia esos nominales conservados en Alcance. B4–B7 parten del DEMO; ninguna edición acredita una medida.",
    }.items():
        info.addProperty("App::PropertyString",key,"Estudio")
        setattr(info,key,value)
    for name,value in [("DiametroFuente",4.0),("LongitudFuente",38.5)]:
        info.addProperty("App::PropertyLength",name,"Nominales de fuente")
        setattr(info,name,value)
        info.setEditorMode(name,1)
    info.addProperty("App::PropertyBool","FabricacionAprobada","Estudio")
    info.FabricacionAprobada=False
    sheet=doc.addObject("Spreadsheet::Sheet","Presupuesto")
    sheet.Label="Presupuesto axial · valores y fórmulas editables"
    rows=[
        ("Concepto","Valor mm","Estado","Procedencia / alcance"),
        ("Diámetro del pasador de escenario","=Alcance.DiametroFuente","ESCENARIO","Parte del nominal de fuente; editar explora hipótesis"),
        ("Longitud total del pasador de escenario","=Alcance.LongitudFuente","ESCENARIO","Parte del nominal de fuente; no garantiza longitud útil"),
        ("Hueco del DEMO","26 mm","DEMO","Ilustración v0.1; no ancho medido de rueda"),
        ("Espesor de cada apoyo del DEMO","8 mm","DEMO","Ilustración; no elección resistente"),
        ("Saliente en cada extremo del DEMO","4 mm","DEMO","Ilustración; no retención definida"),
        ("Diámetro del pasador DEMO","5 mm","DEMO","Ilustración v0.1"),
        ("Longitud que necesita esa disposición","=B4 + 2 * B5 + 2 * B6","CALCULADO","Sólo disposición indicada"),
        ("Exceso respecto al pasador de escenario","=B8 - B3","CALCULADO","Positivo: esa disposición no cabe"),
        ("Longitud DEMO sin ambos salientes","=B4 + 2 * B5","CALCULADO","No afirma una retención factible"),
        ("Exceso incluso sin salientes","=B10 - B3","CALCULADO","Positivo: tampoco cabe esa disposición"),
    ]
    for row,values in enumerate(rows,1):
        for col,value in zip("ABCD",values):sheet.set(col+str(row),value)
    sheet.setStyle("A1:D1","bold","add")
    for col,width in [("A",360),("B",170),("C",145),("D",420)]:sheet.setColumnWidth(col,width)
    for cell,alias in [("B2","DiametroEscenario"),("B3","LongitudEscenario"),("B4","HuecoDemo"),("B5","ApoyoDemo"),("B6","SalienteDemo"),("B7","DiametroDemo"),("B8","LongitudDemo"),("B9","ExcesoDemo"),("B10","SinSalientes"),("B11","ExcesoSinSalientes")]:sheet.setAlias(cell,alias)
    for name,label,radius,height,y,color in [
        ("NominalPublicado","Pasador de escenario · dimensiones en Presupuesto","Presupuesto.DiametroEscenario / 2","Presupuesto.LongitudEscenario",0,(0.80,0.57,0.20)),
        ("PasadorDemo","Pasador DEMO · dimensiones calculadas en Presupuesto","Presupuesto.DiametroDemo / 2","Presupuesto.LongitudDemo",14,(0.65,0.25,0.29)),
    ]:
        obj=doc.addObject("Part::Cylinder",name);obj.Label=label
        obj.setExpression("Radius",radius);obj.setExpression("Height",height)
        obj.Placement=App.Placement(App.Vector(0,y,0),App.Rotation(App.Vector(0,1,0),90))
        if App.GuiUp:obj.ViewObject.ShapeColor=color
    group=doc.addObject("App::DocumentObjectGroup","Bandas")
    group.Label="Diagrama de tramos DEMO · no representa apoyos fabricables"
    bands=[
        ("SalienteA","Saliente A · DEMO","Presupuesto.SalienteDemo","0 mm",(0.90,0.72,0.32)),
        ("ApoyoA","Espesor axial apoyo A · DEMO","Presupuesto.ApoyoDemo","Presupuesto.SalienteDemo",(0.18,0.48,0.57)),
        ("Hueco","Hueco libre · DEMO","Presupuesto.HuecoDemo","Presupuesto.SalienteDemo + Presupuesto.ApoyoDemo",(0.62,0.76,0.77)),
        ("ApoyoB","Espesor axial apoyo B · DEMO","Presupuesto.ApoyoDemo","Presupuesto.SalienteDemo + Presupuesto.ApoyoDemo + Presupuesto.HuecoDemo",(0.18,0.48,0.57)),
        ("SalienteB","Saliente B · DEMO","Presupuesto.SalienteDemo","Presupuesto.SalienteDemo + 2 * Presupuesto.ApoyoDemo + Presupuesto.HuecoDemo",(0.90,0.72,0.32)),
    ]
    for name,label,length,x,color in bands:
        obj=doc.addObject("Part::Box",name);obj.Label=label
        obj.setExpression("Length",length);obj.Width=4;obj.Height=1
        obj.Placement.Base=App.Vector(0,27,-.5)
        obj.setExpression("Placement.Base.x",x)
        group.addObject(obj)
        if App.GuiUp:obj.ViewObject.ShapeColor=color
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
    return doc


def save_new(doc,path):
    path=Path(path)
    if path.suffix.lower()!=".fcstd":raise ValueError("Salida .FCStd requerida")
    if path.exists():raise FileExistsError("No se sobrescribe "+str(path))
    doc.saveAs(str(path))


if __name__=="__main__":
    create_document()
