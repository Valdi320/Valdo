# SPDX-License-Identifier: MIT
"""Bootstrap del CAD X20 Pro abierto. Ejecutar dentro de FreeCAD 1.1.

El FCStd guardado es el maestro editable. Este script reproduce SOLAMENTE
la revisión inicial y se niega a sobrescribir un maestro existente.
Ninguna dimensión DEMO es una medida de la unidad ni una cota de fabricación.
"""
from pathlib import Path
import csv
import json
import hashlib
import math

import FreeCAD as App
import Part


MODEL_NAME = "X20Pro_Base_Arquitectura.FCStd"
SPEC_URL = "https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/specs/"


def text_prop(obj, name, value, group="Evidencia"):
    obj.addProperty("App::PropertyString", name, group)
    setattr(obj, name, str(value))


def note(doc, group, name, label, fields):
    obj = doc.addObject("App::FeaturePython", name)
    # Sin Proxy Python ni dependencia de módulos externos: solo metadatos.
    obj.Label = label
    for k, v in fields.items():
        text_prop(obj, k, v)
    group.addObject(obj)
    return obj


def add_group(doc, name, label):
    obj = doc.addObject("App::DocumentObjectGroup", name)
    obj.Label = label
    return obj


def make_sheet(doc, name, label, rows):
    sh = doc.addObject("Spreadsheet::Sheet", name)
    sh.Label = label
    for col, title in zip("ABCDE", ["Dato", "Valor", "Estado", "Procedencia / límite", "Alias"]):
        sh.set(col + "1", title)
    sh.setStyle("A1:E1", "bold", "add")
    sh.setBackground("A1:E1", (0.10, 0.23, 0.29))
    sh.setForeground("A1:E1", (1.0, 1.0, 1.0))
    for i, row in enumerate(rows, 2):
        label_, value, status, origin, alias = row
        for col, value_ in zip("ABCDE", row):
            sh.set(col + str(i), str(value_))
        if alias:
            sh.setAlias("B" + str(i), alias)
        sh.setBackground("B" + str(i), (1.0, 0.91, 0.72) if status == "DEMO" else (0.81, 0.93, 0.91))
    for col, width in [("A", 290), ("B", 150), ("C", 150), ("D", 550), ("E", 200)]:
        sh.setColumnWidth(col, width)
    return sh


def build(cad_dir, output_dir=None, render=True):
    cad_dir = Path(cad_dir).resolve()
    output_dir = Path(output_dir).resolve() if output_dir else cad_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / MODEL_NAME
    if model_path.exists():
        raise FileExistsError("Maestro existente: abrirlo y editarlo; no regenerar encima: " + str(model_path))
    modules_path = cad_dir.parent / "electronica-modulos.csv"
    interfaces_path = cad_dir / "interfaces.json"
    modules = list(csv.DictReader(modules_path.open(encoding="utf-8-sig", newline="")))
    interfaces = json.loads(interfaces_path.read_text(encoding="utf-8"))
    doc = App.newDocument("X20ProBaseArquitectura")
    doc.Label = "X20 Pro · arquitectura v0.1 · NO FABRICAR"
    doc.Comment = "Referencia exterior + inventario + estudio independiente. Sin cotas internas medidas."
    doc.CreatedBy = "Proyecto Valdi320/Valdo"

    state = add_group(doc, "Estado", "00 · LEER: alcance y límites")
    refs = add_group(doc, "Referencias", "01 · Referencias publicadas y marco provisional")
    conserved = add_group(doc, "ModulosConservados", "02 · Módulos observados — geometría pendiente")
    functional = add_group(doc, "InterfacesFuncionales", "03 · Interfaces críticas — medidas pendientes")
    frame = add_group(doc, "Bastidor", "04 · Bastidor resistente — implantación pendiente")
    service = add_group(doc, "Accesos", "05 · Extracción, barridos y herramientas — pendientes")
    concept = add_group(doc, "DemoCartucho", "90 · DEMO independiente de cartucho · NO FABRICAR")

    note(doc, state, "Alcance", "NO ES UNA BASE FABRICABLE", {
        "Estado": "ARQUITECTURA v0.1 / SIN VALIDACION FISICA",
        "Objetivo": "Base resistente + soportes reemplazables; conservar módulos útiles; control abierto por fases",
        "CotasReales": "Solo envolvente comercial del producto; NINGUNA cota interna medida",
        "Origen": "Centro de envolvente de referencia; Z=0 es su límite inferior abstracto, NO plano del suelo",
        "Ejes": "Convención propuesta X avance, Y izquierda, Z arriba; transformación física pendiente M40",
        "Demo": "Cartucho situado fuera de envolvente. Todas sus dimensiones son ilustrativas y deliberadamente independientes del Xiaomi",
        "Fabricacion": "Bloqueada: faltan medidas, interfaces, tolerancias, materiales, retención, comprobaciones y ensayos",
        "FuenteMaestra": "Este FCStd editable; el script es bootstrap de v0.1 y no sobrescribe ediciones",
        "Licencia": "CAD propio CERN-OHL-P-2.0; script MIT; ningún derecho sobre firmware o geometría OEM",
    })
    note(doc, frame, "DecisionBastidor", "Marco híbrido: forma y espesores SIN decidir", {
        "Propuesta": "Caminos de carga metálicos donde aporten valor; adaptadores, conductos y tapas sustituibles",
        "NoModelado": "No se dibujan travesaños antes de conocer módulos, barridos, aire y ventanas",
        "Requisito": "Conservar relación ruedas/caster/sensores/limpieza/estación; controlar masa y acceso",
        "Material": "PENDIENTE de implantación, carga y proceso de fabricación",
    })

    ref_sheet = make_sheet(doc, "DatosPublicados", "Tabla · datos exteriores publicados", [
        ("Diámetro exterior del producto", "350 mm", "PUBLICADO", SPEC_URL + " — no diámetro de la base interna", "DiametroExterior"),
        ("Altura exterior del producto", "97 mm", "PUBLICADO", SPEC_URL + " — no altura de eje ni plano de suelo", "AlturaExterior"),
    ])
    refs.addObject(ref_sheet)
    envelope = doc.addObject("Part::Cylinder", "EnvolventeReferencia")
    envelope.Label = "Ø350 × 97 · envolvente EXTERIOR publicada; no volumen disponible"
    envelope.setExpression("Radius", "DatosPublicados.DiametroExterior / 2")
    envelope.setExpression("Height", "DatosPublicados.AlturaExterior")
    text_prop(envelope, "Estado", "PUBLICADO / NO FABRICAR / no representa la forma completa del robot")
    text_prop(envelope, "Fuente", SPEC_URL)
    refs.addObject(envelope)

    for module in modules:
        note(doc, conserved, module["id_modulo"], module["id_modulo"] + " · " + module["nombre_provisional"], {
            "Referencia": module["referencia_original"],
            "Revision": module["revision"],
            "Fotos": module["fotos"],
            "Observacion": module["condicion_observada"],
            "Interfaz": module["interfaces_criticas"],
            "IntegridadMecanica": module["integridad_mecanica"],
            "Funcionamiento": module["funcionamiento_electrico"],
            "Cotas": "PENDIENTE — no hay caja ni coordenadas ficticias",
            "Posicion": "PENDIENTE — no interpretar Placement por defecto como posición medida",
            "Pendientes": module["pendientes"],
        })
    for item in interfaces["interfaces"]:
        note(doc, functional, item["id"], item["id"] + " · " + item["nombre"], {
            "Modulos": item["modulos"], "Medidas": item["medidas"],
            "Estado": "PENDIENTE", "Requisito": item["requisito"],
            "DatoAusente": item["falta"], "Evidencia": item["evidencia"],
        })
    for code, label, requirement in [
        ("SERV01", "Ruedas y pasadores", "Extraer cassette, conector y pasador sin retirar placa principal; medir M43"),
        ("SERV02", "Batería y electrónica", "Acceso a desconexión y bandejas; conservar aislamiento, conectores y radio; medir M70–M89"),
        ("SERV03", "Cepillo, depósito y filtro", "Acceso de limpieza frecuente independiente del bastidor; medir M46/M52/M58"),
        ("SERV04", "Mopas, turbina y juntas", "Extracción local y juntas sustituibles; preservar plano, elevación y estanqueidad"),
        ("SERV05", "Paragolpes, sensores y estación", "No invadir movimiento, ventanas ni aproximación de estación; medir M28/M30/M54–M60"),
    ]:
        note(doc, service, code, code + " · " + label, {"Requisito": requirement, "VolumenDeExtraccion": "PENDIENTE — medir pieza, herramienta y ruta de cable"})

    demo_rows = [
        ("Separación libre entre apoyos", "26 mm", "DEMO", "Elegida para explicar el concepto; no es ancho de rueda Xiaomi", "Hueco"),
        ("Espesor de cada apoyo", "8 mm", "DEMO", "Sin material ni resistencia validados", "ApoyoEspesor"),
        ("Margen lateral de placa", "10 mm", "DEMO", "Geometría ilustrativa", "Margen"),
        ("Largo de placa", "78 mm", "DEMO", "No patrón de montaje del robot", "PlacaLargo"),
        ("Espesor de placa", "3 mm", "DEMO", "No selección de chapa para fabricar", "PlacaEspesor"),
        ("Largo de apoyo", "32 mm", "DEMO", "Geometría ilustrativa", "ApoyoLargo"),
        ("Altura de apoyo", "26 mm", "DEMO", "Geometría ilustrativa", "ApoyoAlto"),
        ("Posición longitudinal de apoyo", "12 mm", "DEMO", "Solo coordenada local de estudio", "ApoyoX"),
        ("Posición longitudinal de pivote", "28 mm", "DEMO", "Solo coordenada local de estudio", "PivoteX"),
        ("Altura de pivote sobre placa", "18 mm", "DEMO", "NO altura sobre suelo", "PivoteZ"),
        ("Diámetro de pasador ilustrativo", "5 mm", "DEMO", "NO Ø4 mm de catálogo; dimensión demo deliberadamente distinta", "PasadorD"),
        ("Diámetro exterior de casquillo", "8 mm", "DEMO", "Concepto de asiento reemplazable; ajuste pendiente", "CasquilloD"),
        ("Saliente de pasador por extremo", "4 mm", "DEMO", "Retención NO diseñada", "Saliente"),
        ("Diámetro de agujeros de fijación", "3.5 mm", "DEMO", "No selección de tornillo ni tolerancia", "FijacionD"),
        ("Altura de orejeta de muelle", "22 mm", "DEMO", "No anclaje final ni brazo de palanca conocido", "AnclajeAlto"),
        ("Espesor de orejeta de muelle", "4 mm", "DEMO", "Material y concentración de tensiones pendientes", "AnclajeEspesor"),
        ("Diámetro de ojo ilustrativo", "4 mm", "DEMO", "No corresponde al muelle de la unidad", "OjoD"),
    ]
    demo_sheet = make_sheet(doc, "ParametrosDEMO", "Tabla · TODO DEMO, no medidas del X20 Pro", demo_rows)
    concept.addObject(demo_sheet)
    note(doc, concept, "LimitesCartucho", "Cartucho DEMO: unión fija; parte móvil NO reconstruida", {
        "Estado": "ESTUDIO VISUAL / NO FABRICAR",
        "Alcance": "Explica apoyos separables, casquillos y anclaje fijo; no copia el módulo Xiaomi",
        "InterfazMovil": "PENDIENTE: identificar rotura en carcasa móvil, alojamiento o gancho; el soporte fijo no resuelve ese daño",
        "Pendientes": "Giro real, ajustes, retención del pasador, tornillos/tuercas, detector, topes, brazo de muelle y barridos",
        "Cargas": "Ningún ensayo estructural, de fatiga o de montaje ejecutado",
        "Servicio": "La retirada del pasador requiere espacio lateral medido; no pinzar la carcasa móvil al apretar",
    })
    # Native primitives, expressions and booleans; no executable custom Proxy.
    helpers = []
    finals = []
    D = "ParametrosDEMO."
    def expr(s):
        return s.replace("p.", D)
    def box(name, label, size, xyz):
        obj = doc.addObject("Part::Box", name)
        obj.Label = label
        for prop, value in zip(("Length", "Width", "Height"), size):
            obj.setExpression(prop, expr(value))
        for prop, value in zip(("Placement.Base.x", "Placement.Base.y", "Placement.Base.z"), xyz):
            obj.setExpression(prop, expr(value))
        concept.addObject(obj)
        helpers.append(obj)
        return obj
    def cyl(name, diameter, height, xyz, along_y=False):
        obj = doc.addObject("Part::Cylinder", name)
        obj.setExpression("Radius", "(" + expr(diameter) + ") / 2")
        obj.setExpression("Height", expr(height))
        if along_y:
            obj.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), App.Vector(0, 1, 0))
        for prop, value in zip(("Placement.Base.x", "Placement.Base.y", "Placement.Base.z"), xyz):
            obj.setExpression(prop, expr(value))
        concept.addObject(obj)
        helpers.append(obj)
        return obj
    def cut(name, label, base, holes):
        if len(holes) == 1:
            tool = holes[0]
        else:
            tool = doc.addObject("Part::MultiFuse", name + "Taladros")
            tool.Shapes = holes
            concept.addObject(tool)
            helpers.append(tool)
        result = doc.addObject("Part::Cut", name)
        result.Label = label
        result.Base = base
        result.Tool = tool
        concept.addObject(result)
        helpers.append(result)
        return result
    def finish(obj, color, role):
        text_prop(obj, "Estado", "DEMO / NO FABRICAR")
        text_prop(obj, "FuncionPropuesta", role)
        if App.GuiUp:
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.LineColor = (0.13, 0.18, 0.21)
            obj.ViewObject.DisplayMode = "Flat Lines"
        finals.append(obj)
        return obj

    width = "2 * p.Margen + 2 * p.ApoyoEspesor + p.Hueco"
    base = box("PlacaBruta", "DEMO · placa sin taladrar", ("p.PlacaLargo", width, "p.PlacaEspesor"), ("0 mm", "0 mm", "0 mm"))
    mounting_holes = []
    y_positions = ["p.Margen + p.ApoyoEspesor / 2", "p.Margen + p.ApoyoEspesor + p.Hueco + p.ApoyoEspesor / 2"]
    for i, y in enumerate(y_positions):
        for j, x in enumerate(["p.ApoyoX + 5 mm", "p.ApoyoX + p.ApoyoLargo - 5 mm"]):
            mounting_holes.append(cyl("PlacaTaladro%d%d" % (i,j), "p.FijacionD", "p.PlacaEspesor + 2 mm", (x,y,"-1 mm")))
    anchor_holes = []
    for j,y in enumerate(["(" + width + ") / 2 - 9 mm", "(" + width + ") / 2 + 9 mm"]):
        anchor_holes.append(cyl("PlacaAnclajeTaladro%d" % j,"p.FijacionD","p.PlacaEspesor + 2 mm",("65 mm",y,"-1 mm")))
    plate = finish(cut("PlacaCartucho", "DEMO · placa de cartucho independiente", base, mounting_holes + anchor_holes), (0.52,0.59,0.64), "Repartir carga del cartucho; fijación al futuro bastidor todavía sin diseñar")

    for i, y in enumerate(["p.Margen", "p.Margen + p.ApoyoEspesor + p.Hueco"]):
        support = box("ApoyoBruto%d" % i,"DEMO · apoyo",("p.ApoyoLargo","p.ApoyoEspesor","p.ApoyoAlto"),("p.ApoyoX",y,"p.PlacaEspesor"))
        pivot_hole = cyl("Alojamiento%d" % i,"p.CasquilloD","p.ApoyoEspesor + 2 mm",("p.PivoteX","("+y+") - 1 mm","p.PlacaEspesor + p.PivoteZ"),True)
        holes = [pivot_hole]
        for j,x in enumerate(["p.ApoyoX + 5 mm","p.ApoyoX + p.ApoyoLargo - 5 mm"]):
            holes.append(cyl("ApoyoFijacion%d%d" % (i,j),"p.FijacionD","p.ApoyoAlto + 2 mm",(x,"("+y+") + p.ApoyoEspesor / 2","p.PlacaEspesor - 1 mm")))
        finish(cut("Apoyo%d" % i,"DEMO · apoyo reemplazable %s" % ("A" if i==0 else "B"),support,holes),(0.05,0.55,0.59),"Apoyo local separable; material, apriete y asiento pendientes")
        sleeve_outer = cyl("CasquilloExterior%d" % i,"p.CasquilloD","p.ApoyoEspesor",("p.PivoteX",y,"p.PlacaEspesor + p.PivoteZ"),True)
        sleeve_inner = cyl("CasquilloVacio%d" % i,"p.PasadorD","p.ApoyoEspesor + 2 mm",("p.PivoteX","("+y+") - 1 mm","p.PlacaEspesor + p.PivoteZ"),True)
        finish(cut("Casquillo%d" % i,"DEMO · asiento/casquillo sustituible %s" % ("A" if i==0 else "B"),sleeve_outer,[sleeve_inner]),(0.83,0.64,0.26),"Ilustra interfaz de desgaste; ajustes y necesidad real sin determinar")
    pin = cyl("PasadorDEMO","p.PasadorD","p.Hueco + 2 * p.ApoyoEspesor + 2 * p.Saliente",("p.PivoteX","p.Margen - p.Saliente","p.PlacaEspesor + p.PivoteZ"),True)
    finish(pin,(0.70,0.74,0.77),"Pasador visual; no tiene retención diseñada y no es SKU12584")

    foot = box("PieAnclajeBruto","DEMO · pie de anclaje",("16 mm","28 mm","p.AnclajeEspesor"),("57 mm","("+width+") / 2 - 14 mm","p.PlacaEspesor"))
    foot_holes=[]
    for j,y in enumerate(["("+width+") / 2 - 9 mm","("+width+") / 2 + 9 mm"]):
        foot_holes.append(cyl("PieTaladro%d" % j,"p.FijacionD","p.AnclajeEspesor + 2 mm",("65 mm",y,"p.PlacaEspesor - 1 mm")))
    foot_cut=cut("PieAnclaje","DEMO · pie con fijaciones",foot,foot_holes)
    ear=box("OrejaBruta","DEMO · orejeta",("16 mm","p.AnclajeEspesor","p.AnclajeAlto"),("57 mm","("+width+") / 2 - p.AnclajeEspesor / 2","p.PlacaEspesor + p.AnclajeEspesor"))
    eye=cyl("OjoAnclaje","p.OjoD","p.AnclajeEspesor + 2 mm",("65 mm","("+width+") / 2 - p.AnclajeEspesor / 2 - 1 mm","p.PlacaEspesor + p.AnclajeEspesor + p.AnclajeAlto - 6 mm"),True)
    ear_cut=cut("OrejaMuelle","DEMO · ojo de anclaje",ear,[eye])
    anchor=doc.addObject("Part::Fuse","AnclajeMuelle")
    anchor.Label="DEMO · anclaje FIJO de muelle reemplazable"
    anchor.Base=foot_cut
    anchor.Tool=ear_cut
    concept.addObject(anchor)
    helpers.append(anchor)
    finish(anchor,(0.91,0.40,0.16),"Anclaje independiente; no fija muelle sustituto, fuerza ni geometría móvil")

    doc.recompute()
    for obj in helpers:
        if App.GuiUp:
            obj.ViewObject.Visibility = obj in finals
    # El estudio se traslada lejos de la envolvente sin atribuirle coordenadas OEM.
    # Se aplica a las primitivas (las operaciones booleanas heredan su posición).
    for obj in helpers:
        if obj.TypeId in ("Part::Box", "Part::Cylinder"):
            for prop, value in list(obj.ExpressionEngine):
                if prop.lstrip(".") == "Placement.Base.x":
                    obj.setExpression(prop,"("+value+") + 250 mm")
    warning = doc.addObject("App::Annotation", "AvisoDemo")
    warning.Label = "DEMO — NO FABRICAR"
    warning.LabelText = ["DEMO - NO FABRICAR", "Sin medidas internas del Xiaomi"]
    warning.Position = App.Vector(250, 8, 52)
    concept.addObject(warning)
    if App.GuiUp:
        warning.ViewObject.FontSize = 22
        warning.ViewObject.TextColor = (0.65, 0.16, 0.07)
    doc.recompute()
    validation={"revision":"0.1","freecad_version":".".join(App.Version()[:3]),"physical_validation":False,"manufacturing_ready":False,"measured_internal_dimensions":0,"module_records":len(modules),"interface_records":len(interfaces["interfaces"]),"checks":[]}
    for obj in finals + [envelope]:
        assert not obj.Shape.isNull(), obj.Name
        assert obj.Shape.isValid(), obj.Name
        assert len(obj.Shape.Solids)==1, (obj.Name,len(obj.Shape.Solids))
    validation["checks"].append("Sólidos finales y envolvente: no nulos, válidos y un sólido cada uno")
    assert math.isclose(envelope.Shape.BoundBox.XLength,350,abs_tol=1e-6)
    assert math.isclose(envelope.Shape.BoundBox.ZLength,97,abs_tol=1e-6)
    validation["checks"].append("Envolvente publicada: 350 × 350 × 97 mm; no es validación de base")
    assert plate.Shape.BoundBox.XMin > envelope.Shape.BoundBox.XMax
    validation["checks"].append("Estudio DEMO separado físicamente de la envolvente: X mínimo 250 mm > 175 mm")
    # Propagación nativa: cambiar el hueco desplaza apoyo B y alarga placa/pasador.
    gap_cell="B2"
    before=(doc.Apoyo1.Shape.BoundBox.YMin,doc.PlacaCartucho.Shape.BoundBox.YLength,doc.PasadorDEMO.Shape.BoundBox.YLength)
    demo_sheet.set(gap_cell,"30 mm")
    doc.recompute()
    after=(doc.Apoyo1.Shape.BoundBox.YMin,doc.PlacaCartucho.Shape.BoundBox.YLength,doc.PasadorDEMO.Shape.BoundBox.YLength)
    for b,a in zip(before,after):
        assert math.isclose(a-b,4,abs_tol=1e-6),(before,after)
    demo_sheet.set(gap_cell,"26 mm")
    doc.recompute()
    validation["checks"].append("Hueco DEMO 26→30→26 mm: apoyo B, placa y pasador responden +4 mm y vuelven")

    if App.GuiUp:
        import FreeCADGui as Gui
        envelope.ViewObject.ShapeColor=(0.25,0.48,0.63)
        envelope.ViewObject.LineColor=(0.25,0.48,0.63)
        envelope.ViewObject.Transparency=88
        envelope.ViewObject.DisplayMode="Wireframe"
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
    doc.recompute()
    doc.saveAs(str(model_path))
    expected={o.Name:o.Shape.Volume for o in finals}
    final_names=list(expected)
    App.closeDocument(doc.Name)
    reopened=App.openDocument(str(model_path))
    reopened.recompute()
    for name,volume in expected.items():
        assert reopened.getObject(name).Shape.isValid()
        assert math.isclose(reopened.getObject(name).Shape.Volume,volume,rel_tol=1e-9)
    assert len(reopened.ModulosConservados.Group)==len(modules)
    validation["checks"].append("FCStd guardado y reabierto: inventario y volúmenes coinciden")

    export_dir=output_dir/"exportacion"
    export_dir.mkdir(exist_ok=True)
    step_path=export_dir/"DEMO_cartucho_NO_FABRICAR.step"
    Part.export([reopened.getObject(n) for n in final_names],str(step_path))
    validation["export_step"]={"file":str(step_path.relative_to(output_dir)),"purpose":"Intercambio del estudio, nunca fabricación","solids":len(final_names)}

    if render and App.GuiUp:
        import FreeCADGui as Gui
        views=output_dir/"vistas"
        views.mkdir(exist_ok=True)
        reopened.EnvolventeReferencia.ViewObject.Visibility=False
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.activeDocument().activeView().saveImage(str(views/"DEMO_cartucho_NO_FABRICAR.png"),1500,1000,"White")
        reopened.EnvolventeReferencia.ViewObject.Visibility=True
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.activeDocument().activeView().saveImage(str(views/"referencias_y_estudio.png"),1500,1000,"White")
        # Guardar disposición global tras las dos capturas.
        reopened.recompute()
        reopened.save()
        validation["checks"].append("Vistas nativas generadas con FreeCADGui; inspección visual externa pendiente")
    validation["sha256_fcstd"]=hashlib.sha256(model_path.read_bytes()).hexdigest()
    validation["sha256_step"]=hashlib.sha256(step_path.read_bytes()).hexdigest()
    (output_dir/"validacion_cad.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return validation
