# SPDX-License-Identifier: MIT
"""Estudio comparativo nativo de suspensión; ejecutar dentro de FreeCAD.

El CAD propio se entrega bajo CERN-OHL-P-2.0. Este generador es MIT.
No instala complementos, no usa Proxy geométrico y no exporta STL.
Todas las cotas internas son hipótesis visuales salvo el nominal comercial
del pasador. El documento generado NO es una suspensión fabricable.
"""
from pathlib import Path


MODEL_NAME = "X20Pro_Suspension_Conceptual.FCStd"
PIN_SOURCE = "https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html"
H = "HipotesisVisuales."
P = "DatosPublicados."

# Valor inicial, nunca una inferencia dimensional de fotografías.
# Cada magnitud de la geometría propuesta figura en esta tabla editable.
VISUAL_ROWS = [
    ("Hueco entre apoyos", "26 mm", "DEMO HEREDADO", "ParametrosDEMO.Hueco del CAD v0.1; no ancho móvil medido ni M06 recuperado", "HuecoDemo"),
    ("Espesor axial de apoyo modelado", "3 mm", "HIPÓTESIS VISUAL", "Escenario comparativo propio; no elección resistente", "ApoyoEspesor"),
    ("Espesor axial de apoyo alternativo", "4 mm", "HIPÓTESIS VISUAL", "Sólo comparación aritmética; no pieza elegida", "ApoyoAlternativo"),
    ("Reserva axial por extremo", "4 mm", "DEMO HEREDADO", "Saliente inicial del DEMO v0.1; NO una retención diseñada", "ReservaExtremo"),
    ("Largo de núcleo visual", "124 mm", "HIPÓTESIS VISUAL", "Bloque de función estructural; no forma de base Xiaomi", "NucleoLargo"),
    ("Ancho de núcleo visual", "64 mm", "HIPÓTESIS VISUAL", "Presentación del asiento común", "NucleoAncho"),
    ("Espesor de núcleo visual", "5 mm", "HIPÓTESIS VISUAL", "No especificación de material o fabricación", "NucleoEspesor"),
    ("Largo de asiento común", "110 mm", "HIPÓTESIS VISUAL", "Interfaz de comparación idéntica en ambas variantes", "AsientoLargo"),
    ("Ancho de asiento común", "50 mm", "HIPÓTESIS VISUAL", "Posicionamiento y apriete reales pendientes", "AsientoAncho"),
    ("Espesor de asiento común", "3 mm", "HIPÓTESIS VISUAL", "Sin fijación ni tolerancias diseñadas", "AsientoEspesor"),
    ("Largo de placa de cartucho", "108 mm", "HIPÓTESIS VISUAL", "No patrón de fijación Xiaomi", "CartuchoLargo"),
    ("Ancho de placa de cartucho", "48 mm", "HIPÓTESIS VISUAL", "Independiente del ancho desconocido del módulo conservado", "CartuchoAncho"),
    ("Espesor de placa de cartucho", "4 mm", "HIPÓTESIS VISUAL", "No espesor aprobado para fabricar", "CartuchoEspesor"),
    ("Longitud longitudinal de apoyo", "18 mm", "HIPÓTESIS VISUAL", "Bloque local ilustrativo", "ApoyoLargo"),
    ("Altura de apoyo sobre placa", "34 mm", "HIPÓTESIS VISUAL", "No cota del módulo original", "ApoyoAlto"),
    ("Posición X local del pivote", "42 mm", "HIPÓTESIS VISUAL", "Marco común del estudio, sin transformación al robot", "PivoteX"),
    ("Altura de pivote sobre placa", "24 mm", "HIPÓTESIS VISUAL", "No altura sobre el suelo", "PivoteSobrePlaca"),
    ("Diámetro visual de alojamientos", "5 mm", "HIPÓTESIS VISUAL", "No ajuste calculado con pasador nominal de 4 mm", "AlojamientoD"),
    ("Largo del brazo abstracto", "48 mm", "HIPÓTESIS VISUAL", "No distancia entre ejes medida en M41/M42", "BrazoLargo"),
    ("Ancho del brazo abstracto", "14 mm", "HIPÓTESIS VISUAL", "No representa ancho móvil ni reductora Xiaomi", "BrazoAncho"),
    ("Espesor del brazo abstracto", "6 mm", "HIPÓTESIS VISUAL", "Sólo permite visualizar una pieza móvil", "BrazoEspesor"),
    ("Diámetro del ojo visual del brazo", "12 mm", "HIPÓTESIS VISUAL", "No reconstruye un alojamiento móvil roto", "OjoBrazoD"),
    ("Ángulo del segundo estado", "15 deg", "HIPÓTESIS VISUAL", "Muestra 0→ángulo; NO recorrido Xiaomi ni límite admisible", "AnguloMuestra"),
    ("Radio de marcadores de anclaje", "2 mm", "HIPÓTESIS VISUAL", "Marcadores, no ganchos o contactos fabricables", "MarcadorRadio"),
    ("Largo de reserva móvil de contacto", "12 mm", "HIPÓTESIS VISUAL", "Volumen solidario al brazo, no contacto resuelto", "ContactoLargo"),
    ("Ancho de reserva móvil de contacto", "20 mm", "HIPÓTESIS VISUAL", "Reserva gráfica independiente de la forma final", "ContactoAncho"),
    ("Alto de reserva móvil de contacto", "12 mm", "HIPÓTESIS VISUAL", "No deformación calculada del elemento elástico", "ContactoAlto"),
    ("Espesor gráfico del sector", "0.8 mm", "HIPÓTESIS VISUAL", "Visualización del barrido de un segmento; no espesor de pieza", "SectorEspesor"),
    ("Radio visual de reservas de retención", "6 mm", "HIPÓTESIS VISUAL", "Sin cierre, tope axial ni procedimiento de descarga diseñados", "RetencionRadio"),
    ("X de mordaza de lámina", "4 mm", "HIPÓTESIS VISUAL", "Posición local de una alternativa propia", "MordazaX"),
    ("Longitud de mordaza", "12 mm", "HIPÓTESIS VISUAL", "Longitud de sujeción no validada", "MordazaLargo"),
    ("Ancho de mordaza", "20 mm", "HIPÓTESIS VISUAL", "No selecciona apriete ni presión de contacto", "MordazaAncho"),
    ("Espesor de cada mordaza", "3 mm", "HIPÓTESIS VISUAL", "No material ni unión elegidos", "MordazaEspesor"),
    ("Altura inferior de lámina plana", "50 mm", "HIPÓTESIS VISUAL", "Referencia sin precarga ni contacto con el brazo resueltos", "LaminaZ"),
    ("Longitud activa de lámina visual", "74 mm", "HIPÓTESIS VISUAL", "No longitud de diseño elástico", "LaminaActiva"),
    ("Ancho de lámina visual", "14 mm", "HIPÓTESIS VISUAL", "No sección seleccionada para cargas", "LaminaAncho"),
    ("Espesor de lámina visual", "1.2 mm", "HIPÓTESIS VISUAL", "No selección de fleje, grado o condición de suministro", "LaminaEspesor"),
    ("X de anclaje fijo del alambre", "18 mm", "HIPÓTESIS VISUAL", "Anclaje conceptual inferior al pivote; sin gancho diseñado", "AlambreFijoX"),
    ("Z de anclaje fijo del alambre", "10 mm", "HIPÓTESIS VISUAL", "No cota de anclaje Xiaomi ni selección de precarga", "AlambreFijoZ"),
    ("Anclaje móvil de alambre bajo el brazo", "8 mm", "HIPÓTESIS VISUAL", "Offset en −Z del marco móvil para no atravesar el brazo; orejeta y carga local pendientes", "AlambreMovilBajo"),
    ("Margen de reserva de alambre", "6 mm", "HIPÓTESIS VISUAL", "Caja alrededor del segmento entre anclajes; no diámetro de muelle", "AlambreMargen"),
    ("Largo de reservas de topes", "8 mm", "HIPÓTESIS VISUAL", "No superficie de impacto dimensionada", "TopeLargo"),
    ("Ancho de reservas de topes", "24 mm", "HIPÓTESIS VISUAL", "Funciones independientes del detector y elemento elástico", "TopeAncho"),
    ("Alto de reservas de topes", "4 mm", "HIPÓTESIS VISUAL", "Posiciones no calculadas como límites de recorrido", "TopeAlto"),
    ("Z de reserva de tope inferior", "14 mm", "HIPÓTESIS VISUAL", "No garantiza protección al final de carrera", "TopeInferiorZ"),
    ("Z de reserva de tope superior", "48 mm", "HIPÓTESIS VISUAL", "No limita el ángulo de muestra ni define su admisibilidad", "TopeSuperiorZ"),
    ("Traslación de cartucho para servicio", "55 mm", "HIPÓTESIS VISUAL", "+Z local ilustrativo; no ruta medida en el robot", "ExtraccionCartucho"),
    ("Traslación del pasador en banco", "45 mm", "HIPÓTESIS VISUAL", "+Y local; liberación de retención y energía pendientes", "ExtraccionPasador"),
    ("Separación gráfica de variantes", "170 mm", "HIPÓTESIS VISUAL", "Composición de escenas; no coordenada de implantación", "SeparacionVariantes"),
    ("Separación gráfica de escena de servicio", "120 mm", "HIPÓTESIS VISUAL", "Presentación independiente, no posición dentro del robot", "SeparacionServicio"),
]


def _text(obj, key, value, group="Procedencia"):
    obj.addProperty("App::PropertyString", key, group)
    setattr(obj, key, str(value))


def _sheet(doc, name, label, rows):
    sheet = doc.addObject("Spreadsheet::Sheet", name)
    sheet.Label = label
    for col, value in zip("ABCDE", ("Magnitud / función", "Valor / referencia", "Estado", "Origen inicial / límite", "Alias")):
        sheet.set(col + "1", value)
    sheet.setStyle("A1:E1", "bold", "add")
    sheet.setBackground("A1:E1", (0.10, 0.23, 0.29))
    sheet.setForeground("A1:E1", (1.0, 1.0, 1.0))
    for rownum, row in enumerate(rows, 2):
        for col, value in zip("ABCDE", row):
            sheet.set(col + str(rownum), str(value))
        if len(row) > 4 and row[4]:
            sheet.setAlias("B" + str(rownum), row[4])
        sheet.setBackground("B" + str(rownum), (0.81, 0.93, 0.91) if row[2] == "PUBLICADO" else (1.0, 0.92, 0.76))
    for col, width in (("A", 315), ("B", 185), ("C", 185), ("D", 590), ("E", 220)):
        sheet.setColumnWidth(col, width)
    return sheet


def create_document():
    """Crea y devuelve un documento nuevo, sin guardar ni sobrescribir archivos."""
    import FreeCAD as App

    doc = App.newDocument("X20ProSuspensionConceptual")
    doc.Label = "X20 Pro · suspensión conceptual · HIPÓTESIS · NO FABRICAR"
    doc.Comment = "Comparación editable de lámina y alambre; interfaces, cargas, contacto y extracción sin validar."
    doc.CreatedBy = "Proyecto Valdi320/Valdo"
    finals, helpers = [], []

    def group(name, label, parent=None, part=False):
        obj = doc.addObject("App::Part" if part else "App::DocumentObjectGroup", name)
        obj.Label = label
        if parent:
            parent.addObject(obj)
        return obj

    def note(parent, name, label, values):
        obj = doc.addObject("App::FeaturePython", name)
        obj.Label = label
        for key, value in values.items():
            _text(obj, key, value)
        parent.addObject(obj)
        return obj

    def style(obj, color, transparency=0, wire=False):
        if App.GuiUp:
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.LineColor = color if wire else (0.16, 0.23, 0.27)
            obj.ViewObject.Transparency = transparency
            if obj.TypeId != "Part::Line":
                obj.ViewObject.DisplayMode = "Wireframe" if wire else "Flat Lines"

    def primitive(parent, kind, name, label, dimensions, xyz, color=None,
                  role="HIPÓTESIS VISUAL; no fabricar", rotation=None,
                  transparency=0, wire=False, final=True):
        obj = doc.addObject(kind, name)
        obj.Label = label
        parent.addObject(obj)
        if rotation:
            obj.Placement.Rotation = rotation
        for prop, expression in dimensions.items():
            obj.setExpression(prop, expression)
        for component, expression in zip("xyz", xyz):
            obj.setExpression("Placement.Base." + component, expression)
        _text(obj, "Estado", "HIPÓTESIS VISUAL / NO FABRICAR")
        _text(obj, "Funcion", role)
        if color:
            style(obj, color, transparency, wire)
        (finals if final else helpers).append(obj)
        return obj

    def box(parent, name, label, size, xyz, color, **kwargs):
        return primitive(parent, "Part::Box", name, label,
                         dict(zip(("Length", "Width", "Height"), size)), xyz, color, **kwargs)

    def cylinder(parent, name, label, radius, length, xyz, color,
                 along_y=False, **kwargs):
        rotation = App.Rotation(App.Vector(0, 0, 1), App.Vector(0, 1, 0)) if along_y else None
        return primitive(parent, "Part::Cylinder", name, label,
                         {"Radius": radius, "Height": length}, xyz, color,
                         rotation=rotation, **kwargs)

    def sphere(parent, name, label, xyz, color):
        return primitive(parent, "Part::Sphere", name, label,
                         {"Radius": H + "MarcadorRadio"}, xyz, color,
                         role="Marcador de interfaz; no es un gancho, casquillo ni superficie de contacto diseñada")

    def cut(parent, name, label, base, tool, color):
        obj = doc.addObject("Part::Cut", name)
        obj.Label = label
        obj.Base, obj.Tool = base, tool
        parent.addObject(obj)
        _text(obj, "Estado", "HIPÓTESIS VISUAL / NO FABRICAR")
        _text(obj, "Ajuste", "Alojamiento visual de 5 mm inicial; no ajuste con el nominal publicado ni tolerancia")
        style(obj, color)
        finals.append(obj)
        return obj

    def annotation(name, lines, xyz):
        obj = doc.addObject("App::Annotation", name)
        obj.Label = lines[0]
        obj.LabelText = lines
        obj.Position = App.Vector(*xyz)
        if App.GuiUp:
            obj.ViewObject.FontSize = 16
            obj.ViewObject.TextColor = (0.18, 0.28, 0.35)
        return obj

    scope = group("Alcance", "00 · LEER: estudio comparativo, no suspensión validada")
    refs = group("Referencias", "01 · Nominal publicado y procedencia")
    params = group("Parametros", "02 · Hipótesis visuales editables")
    notes = note(scope, "EstadoEstudio", "NO FABRICAR · lo abierto aquí es el estudio", {
        "Revision": "0.3 / 2026-10-25",
        "Objetivo": "Comparar cartuchos con lámina y alambre fabricables desde materia prima especificada; todavía no se dimensionan",
        "DatosReales": "Sólo Ø4 × 38,5 mm nominal comercial del pasador SKU12584; no medidas del ejemplar",
        "Convencion": "Marco local del asiento común: X longitudinal abstracto, Y eje del pasador, Z perpendicular al asiento; NO ejes o coordenadas Xiaomi",
        "MuestraAngular": "Brazo de referencia 0° y muestra inicial 15°, ambos visuales. No representan carrera permitida ni altura de rueda",
        "EstadoElastico": "Lámina plana sin deformación calculada; alambre como caja/segmento entre anclajes conceptuales, sin hélice ni tensión inicial",
        "Barrido": "Sector del segmento longitudinal central del brazo; excluye offset del anclaje móvil y otros volúmenes. NO envolvente completa del brazo, módulo, herramientas, cable o detector",
        "InterfazMovil": "Brazo abstracto; no reconstruye alojamiento o gancho roto del módulo conservado y no presupone superficies sanas",
        "Servicio": "Traslaciones gráficas de cartucho y pasador; liberación de cierres, conector y contención de energía PENDIENTES",
        "MaterialesYCargas": "No se asignan grado, módulo elástico, fuerza, resistencia, fatiga ni vida útil",
        "FuenteMaestra": "El FCStd generado es editable. Este script reproduce la revisión inicial del estudio y no debe sobrescribir ediciones",
        "Licencias": "CAD y documentación propios CERN-OHL-P-2.0; generador MIT; sin geometría externa ni licencia sobre firmware OEM",
    })
    notes.addProperty("App::PropertyBool", "FabricacionAprobada", "Estado")
    notes.FabricacionAprobada = False

    public = _sheet(doc, "DatosPublicados", "Nominal comercial · no medida de la unidad", [
        ("Diámetro nominal del pasador", "4 mm", "PUBLICADO", PIN_SOURCE + " — 25-10-2026; sin tolerancia", "DiametroPasador"),
        ("Longitud total nominal del pasador", "38.5 mm", "PUBLICADO", PIN_SOURCE + " — no longitud útil garantizada, sin cabeza/ranuras modeladas", "LongitudPasador"),
    ])
    refs.addObject(public)
    hypothesis = _sheet(doc, "HipotesisVisuales", "EDITAR · hipótesis visuales; no cotas de Xiaomi", VISUAL_ROWS)
    params.addObject(hypothesis)
    provenance = _sheet(doc, "Procedencia", "Procedencia por función · requisitos pendientes", [
        ("Asiento, núcleo y cartucho", "HipotesisVisuales", "HIPÓTESIS VISUAL", "Capítulo16 §2; posicionamiento y apriete son funciones distintas, sin fijación resuelta", ""),
        ("Apoyos y parte móvil", "M41 / M42", "PENDIENTE", "Ancho móvil, caras, giro real y daños sin reconstruir; HuecoDemo no sustituye esos datos", ""),
        ("Retención y topes", "Reservas gráficas", "PENDIENTE", "No se modela cierre ni carga de impacto; el elemento elástico no retiene la rueda", ""),
        ("Detector y cable", "IF01–IF04 / IF13", "PENDIENTE", "Sin geometría ficticia de detector; nunca usarlo como tope", ""),
        ("Función elástica", "M44 / capítulo16", "PENDIENTE", "Fuerza en rueda, precarga, rozamiento y evolución temporal sin datos; no modeladas", ""),
        ("Servicio", "M43 / capítulo16", "HIPÓTESIS VISUAL", "Ruta +Z cartucho y +Y pasador en banco; obstáculos reales y energía por resolver", ""),
        ("Barrido angular", "0° → AnguloMuestra", "HIPÓTESIS VISUAL", "Sector del segmento longitudinal central del brazo; excluye offset del anclaje y otros volúmenes", ""),
        ("Colores", "Identifican funciones", "PRESENTACIÓN", "No indican grado/material aprobado ni resultado de análisis", ""),
    ])
    refs.addObject(provenance)
    budget = _sheet(doc, "PresupuestoAxial", "Presupuesto axial · ninguna suma aprueba encaje", [
        ("Longitud nominal publicada", "=" + P + "LongitudPasador", "PUBLICADO", "No longitud útil ni tolerancia; fuente en DatosPublicados", ""),
        ("Hueco DEMO heredado", "=" + H + "HuecoDemo", "DEMO HEREDADO", "No anchura móvil ni separación medida de soportes originales", ""),
        ("Apoyo modelado, inicial 3 mm", "=" + H + "ApoyoEspesor", "HIPÓTESIS VISUAL", "Común a ambas variantes", ""),
        ("Reserva por extremo, inicial 4 mm", "=" + H + "ReservaExtremo", "DEMO HEREDADO", "No retención diseñada", ""),
        ("Demanda axial del modelo", "=B3 + 2 * B4 + 2 * B5", "CALCULADO", "Cuenta cada tramo una vez; no se reduce hueco desconocido para encajar", "DemandaActual"),
        ("Margen aritmético nominal − demanda", "=B2 - B6", "CALCULADO", "Negativo descarta esta suma; positivo NO demuestra ajuste/retención", "MargenActual"),
        ("Apoyo alternativo, inicial 4 mm", "=" + H + "ApoyoAlternativo", "HIPÓTESIS VISUAL", "Comparación; no altera la geometría de las variantes", ""),
        ("Demanda con apoyo alternativo", "=B3 + 2 * B8 + 2 * B5", "CALCULADO", "Comparación aritmética, sin decisión resistente", "DemandaAlternativa"),
        ("Margen nominal con alternativa", "=B2 - B9", "CALCULADO", "Los valores iniciales dan demandas 40/42 mm frente a nominal 38,5 mm", "MargenAlternativo"),
    ])
    params.addObject(budget)

    # Todas las variantes se construyen en el mismo marco local, sin alterar el
    # asiento o el pivote para acomodar una arquitectura elástica diferente.
    pivot_z = H + "CartuchoEspesor + " + H + "PivoteSobrePlaca"
    gray, teal, gold = (0.56, 0.64, 0.70), (0.10, 0.53, 0.59), (0.91, 0.66, 0.26)
    violet, orange = (0.55, 0.34, 0.77), (0.90, 0.39, 0.18)

    def arm_state(cart, prefix, sample, kind):
        code = "Muestra" if sample else "Referencia"
        state = group(prefix + "Brazo" + code,
                      ("MUESTRA · ángulo visual editable" if sample else "REFERENCIA · brazo abstracto a 0°"), cart, part=True)
        state.setExpression("Placement.Base.x", H + "PivoteX")
        state.setExpression("Placement.Base.z", pivot_z)
        if sample:
            # La prueba de raíz en FreeCAD1.1.4 confirma conversión directa de
            # una cantidad angular: 15deg produce Rotation.Angle=0,261799rad.
            state.Placement.Rotation = App.Rotation(App.Vector(0, -1, 0), 15)
            state.setExpression("Placement.Rotation.Angle", H + "AnguloMuestra")
        _text(state, "Estado", "HIPÓTESIS VISUAL; no límite de recorrido")
        _text(state, "Contacto", "Brazo, marcador y reserva giran solidarios. Ningún contacto con elemento elástico está resuelto")
        stem = box(state, prefix + code + "BrazoBruto", "Auxiliar · brazo", (H + "BrazoLargo", H + "BrazoAncho", H + "BrazoEspesor"),
                   ("0 mm", "-" + H + "BrazoAncho / 2", "-" + H + "BrazoEspesor / 2"), gray, final=False)
        boss = cylinder(state, prefix + code + "OjoBruto", "Auxiliar · ojo visual", H + "OjoBrazoD / 2", H + "BrazoAncho",
                        ("0 mm", "-" + H + "BrazoAncho / 2", "0 mm"), gray, along_y=True, final=False)
        fused = doc.addObject("Part::Fuse", prefix + code + "BrazoFusion")
        fused.Base, fused.Tool = stem, boss
        state.addObject(fused)
        helpers.append(fused)
        bore = cylinder(state, prefix + code + "Taladro", "Auxiliar · alojamiento visual", H + "AlojamientoD / 2", H + "BrazoAncho + 2 mm",
                        ("0 mm", "-" + H + "BrazoAncho / 2 - 1 mm", "0 mm"), gray, along_y=True, final=False)
        arm = cut(state, prefix + code + "Brazo", "Brazo abstracto · " + code + " · no módulo Xiaomi", fused, bore, teal if sample else gray)
        style(arm, teal if sample else gray, 55 if sample else 15)
        # En alambre la referencia queda bajo el brazo; no se dibuja una
        # orejeta ficticia para justificar todavía la transmisión de carga.
        offset_z = "-" + H + "AlambreMovilBajo" if kind == "alambre" else "0 mm"
        marker = sphere(state, prefix + code + "InterfazMovil", "Marcador móvil · contacto/anclaje PENDIENTE",
                        (H + "BrazoLargo", "0 mm", offset_z), violet if sample else gold)
        reserve = box(state, prefix + code + "ReservaContacto", "Reserva móvil · contacto no calculado",
                      (H + "ContactoLargo", H + "ContactoAncho", H + "ContactoAlto"),
                      (H + "BrazoLargo - " + H + "ContactoLargo / 2", "-" + H + "ContactoAncho / 2", "(" + offset_z + ") - " + H + "ContactoAlto / 2"),
                      violet, wire=True, transparency=75)
        return state, arm, marker, reserve

    def wire_reserve(cart, prefix, sample):
        code = "Muestra" if sample else "Referencia"
        angle = H + "AnguloMuestra" if sample else "0 deg"
        mx = "(" + H + "PivoteX + " + H + "BrazoLargo * cos(" + angle + ") + " + H + "AlambreMovilBajo * sin(" + angle + "))"
        mz = "(" + pivot_z + " + " + H + "BrazoLargo * sin(" + angle + ") - " + H + "AlambreMovilBajo * cos(" + angle + "))"
        fx, fz, margin = H + "AlambreFijoX", H + "AlambreFijoZ", H + "AlambreMargen"
        line = doc.addObject("Part::Line", prefix + "LineaAlambre" + code)
        line.Label = "Segmento entre anclajes · " + code + " · NO hélice"
        cart.addObject(line)
        for key, value in {"X1": fx, "Y1": "0 mm", "Z1": fz, "X2": mx, "Y2": "0 mm", "Z2": mz}.items():
            line.setExpression(key, value)
        _text(line, "Estado", "HIPÓTESIS VISUAL; no longitud libre, tensión inicial o respuesta de resorte")
        style(line, violet if sample else gold)
        if App.GuiUp:
            line.ViewObject.LineWidth = 3.0
        finals.append(line)
        reserve = box(cart, prefix + "ReservaAlambre" + code, "Reserva longitudinal · " + code + " · NO muelle fabricable",
                      ("abs(" + mx + " - " + fx + ") + 2 * " + margin, "2 * " + margin, "abs(" + mz + " - " + fz + ") + 2 * " + margin),
                      ("min(" + mx + ", " + fx + ") - " + margin, "-" + margin, "min(" + mz + ", " + fz + ") - " + margin),
                      violet if sample else gold, wire=True, transparency=85)
        _text(reserve, "Limite", "Caja alrededor del segmento; no volumen real de espiras/ganchos ni barrido completo")
        return line

    def cartridge(scene, prefix, kind, extraction=False):
        cart = group(prefix + "Cartucho", "Cartucho · " + kind + " · HIPÓTESIS VISUAL", scene, part=True)
        if extraction:
            cart.setExpression("Placement.Base.z", H + "ExtraccionCartucho")
        box(cart, prefix + "Placa", "Placa separable · sin fijaciones diseñadas",
            (H + "CartuchoLargo", H + "CartuchoAncho", H + "CartuchoEspesor"),
            ("0 mm", "-" + H + "CartuchoAncho / 2", "0 mm"), gray)
        for suffix, y in (("A", "-" + H + "HuecoDemo / 2 - " + H + "ApoyoEspesor"), ("B", H + "HuecoDemo / 2")):
            body = box(cart, prefix + "ApoyoBruto" + suffix, "Auxiliar · apoyo " + suffix,
                       (H + "ApoyoLargo", H + "ApoyoEspesor", H + "ApoyoAlto"),
                       (H + "PivoteX - " + H + "ApoyoLargo / 2", y, H + "CartuchoEspesor"), teal, final=False)
            hole = cylinder(cart, prefix + "TaladroApoyo" + suffix, "Auxiliar · taladro " + suffix,
                            H + "AlojamientoD / 2", H + "ApoyoEspesor + 2 mm",
                            (H + "PivoteX", "(" + y + ") - 1 mm", pivot_z), teal, along_y=True, final=False)
            cut(cart, prefix + "Apoyo" + suffix, "Apoyo " + suffix + " · local y sustituible · HIPÓTESIS", body, hole, teal)
        pin = cylinder(cart, prefix + "PasadorNominal", "PUBLICADO · pasador simplificado Ø4 × 38,5 mm",
                       P + "DiametroPasador / 2", P + "LongitudPasador",
                       (H + "PivoteX", "-" + P + "LongitudPasador / 2", pivot_z), (0.71, 0.74, 0.77), along_y=True)
        pin.Estado = "NOMINAL COMERCIAL; ubicación visual; no cabeza, ranura, tolerancia o longitud útil"
        _text(pin, "Fuente", PIN_SOURCE)
        for suffix, y in (("A", "-" + H + "HuecoDemo / 2 - " + H + "ApoyoEspesor - " + H + "ReservaExtremo"),
                          ("B", H + "HuecoDemo / 2 + " + H + "ApoyoEspesor")):
            cylinder(cart, prefix + "ReservaRetencion" + suffix, "Retención " + suffix + " · RESERVA, sin cierre",
                     H + "RetencionRadio", H + "ReservaExtremo", (H + "PivoteX", y, pivot_z), orange,
                     along_y=True, wire=True, transparency=80,
                     role="Retención axial independiente del elástico; no se ha diseñado el cierre ni la contención de energía")
        reference = arm_state(cart, prefix, False, kind)
        sample = arm_state(cart, prefix, True, kind)
        sector = primitive(cart, "Part::Cylinder", prefix + "SectorReferencia", "Barrido de segmento central 0→muestra · NO envolvente completa",
                           {"Radius": H + "BrazoLargo", "Height": H + "SectorEspesor", "Angle": H + "AnguloMuestra"},
                           (H + "PivoteX", H + "SectorEspesor / 2", pivot_z), violet,
                           rotation=App.Rotation(App.Vector(1, 0, 0), 90), transparency=87,
                           role="Sector del segmento longitudinal central del brazo. Excluye offset del anclaje móvil, espesor, ojo, contacto, rueda, cable, detector y herramientas")
        for suffix, z in (("Inferior", H + "TopeInferiorZ"), ("Superior", H + "TopeSuperiorZ")):
            box(cart, prefix + "ReservaTope" + suffix, "Tope " + suffix.lower() + " · RESERVA independiente",
                (H + "TopeLargo", H + "TopeAncho", H + "TopeAlto"),
                (H + "PivoteX + " + H + "BrazoLargo - " + H + "TopeLargo / 2", "-" + H + "TopeAncho / 2", z),
                orange, wire=True, transparency=80,
                role="Función de tope sin calcular; no coincide necesariamente con los estados ni protege aún el detector/cable")
        if kind == "lámina":
            box(cart, prefix + "SoporteMordaza", "Soporte de mordaza · HIPÓTESIS",
                (H + "MordazaLargo", H + "MordazaAncho", H + "LaminaZ - " + H + "MordazaEspesor - " + H + "CartuchoEspesor"),
                (H + "MordazaX", "-" + H + "MordazaAncho / 2", H + "CartuchoEspesor"), gray)
            for suffix, z in (("Inferior", H + "LaminaZ - " + H + "MordazaEspesor"), ("Superior", H + "LaminaZ + " + H + "LaminaEspesor")):
                box(cart, prefix + "Mordaza" + suffix, "Mordaza " + suffix.lower() + " · sin apriete dimensionado",
                    (H + "MordazaLargo", H + "MordazaAncho", H + "MordazaEspesor"),
                    (H + "MordazaX", "-" + H + "MordazaAncho / 2", z), teal)
            leaf = box(cart, prefix + "LaminaPlana", "Lámina PLANA de referencia · NO deformada calculada",
                       (H + "MordazaLargo + " + H + "LaminaActiva", H + "LaminaAncho", H + "LaminaEspesor"),
                       (H + "MordazaX", "-" + H + "LaminaAncho / 2", H + "LaminaZ"), gold)
            _text(leaf, "ContactoPendiente", "Puede haber separación o interferencia con reservas. No se impone contacto a ninguno de los estados")
        else:
            sphere(cart, prefix + "AnclajeFijo", "Marcador de anclaje fijo · NO gancho",
                   (H + "AlambreFijoX", "0 mm", H + "AlambreFijoZ"), gold)
            wire_reserve(cart, prefix, False)
            wire_reserve(cart, prefix, True)
            note(cart, prefix + "SentidoRetorno", "Anclajes visuales: comprobar el signo de retorno", {
                "ConfiguracionInicial": "Anclaje fijo por debajo/antes del pivote; la distancia al móvil aumenta entre 0° y 15° en estos valores visuales",
                "Limite": "Sólo relación geométrica. No demuestra precarga, fuerza, estabilidad ni que el resorte permanezca en tracción",
                "AnclajeMovil": "Marcador bajo el brazo para separar el segmento del sólido. La orejeta y la transmisión de carga siguen pendientes",
                "Edicion": "Mover anclajes o cambiar ángulo exige revisar de nuevo el signo; el generador no optimiza ni corrige para conseguir retorno",
            })
        if extraction:
            # El pasador desplazado es otro estado, no otra pieza que haya que fabricar.
            cylinder(cart, prefix + "PasadorEnBanco", "Estado de pasador retirado +Y · HIPÓTESIS",
                     P + "DiametroPasador / 2", P + "LongitudPasador",
                     (H + "PivoteX", "-" + P + "LongitudPasador / 2 + " + H + "ExtraccionPasador", pivot_z),
                     (0.34, 0.63, 0.81), along_y=True, transparency=45)
            cylinder(cart, prefix + "RutaPasador", "Reserva de traslación de pasador · sólo en banco",
                     H + "RetencionRadio", P + "LongitudPasador + " + H + "ExtraccionPasador",
                     (H + "PivoteX", "-" + P + "LongitudPasador / 2", pivot_z), violet,
                     along_y=True, wire=True, transparency=90)
        return cart

    def scene(name, prefix, label, kind, x, y="0 mm", extraction=False):
        root = group(name, label, part=True)
        root.setExpression("Placement.Base.x", x)
        root.setExpression("Placement.Base.y", y)
        box(root, prefix + "Nucleo", "Núcleo estructural · bloque de función, no chasis",
            (H + "NucleoLargo", H + "NucleoAncho", H + "NucleoEspesor"),
            ("(" + H + "CartuchoLargo - " + H + "NucleoLargo) / 2", "-" + H + "NucleoAncho / 2", "-" + H + "AsientoEspesor - " + H + "NucleoEspesor"), gray)
        box(root, prefix + "Asiento", "Asiento común · localización y apriete pendientes",
            (H + "AsientoLargo", H + "AsientoAncho", H + "AsientoEspesor"),
            ("(" + H + "CartuchoLargo - " + H + "AsientoLargo) / 2", "-" + H + "AsientoAncho / 2", "-" + H + "AsientoEspesor"), (0.72, 0.80, 0.85))
        cartridge(root, prefix, kind, extraction)
        if extraction:
            box(root, prefix + "RutaCartucho", "Corredor gráfico +Z · obstáculos/energía PENDIENTES",
                (H + "CartuchoLargo", H + "CartuchoAncho", H + "ExtraccionCartucho + " + H + "LaminaZ + " + H + "LaminaEspesor + " + H + "MordazaEspesor"),
                ("0 mm", "-" + H + "CartuchoAncho / 2", "0 mm"), violet, wire=True, transparency=92)
        return root

    leaf_scene = scene("VarianteLamina", "LAM_", "10 · Lámina plana + brazo en dos estados · HIPÓTESIS", "lámina", "0 mm")
    wire_scene = scene("VarianteAlambre", "ALM_", "20 · Reserva de alambre entre anclajes · HIPÓTESIS", "alambre", H + "SeparacionVariantes")
    service_scene = scene("EscenaExtraccion", "EXT_", "30 · Extracción ilustrativa en banco · energía PENDIENTE", "lámina", "0 mm", H + "SeparacionServicio", True)
    note(scope, "ServicioYDetector", "Servicio, detector y cableado: sin geometría ficticia", {
        "Extraccion": "EscenaExtraccion muestra estados de montaje/extracción por traslación; no resuelve cierres, agarres ni acceso a tornillos",
        "Energia": "OBJETIVO PENDIENTE: cartucho extraíble con energía contenida y descarga controlada. Ninguna pieza dibujada certifica esa función",
        "Pasador": "Su retirada se estudia fuera del robot; primero deben quedar controladas las piezas móviles y la energía",
        "Detector": "Identificación y actuación del detector original pendientes. No hay un detector inventado ni se usa de tope",
        "Cable": "Conector y radio/bucle de cable no están representados; el sector no demuestra holgura para ellos",
        "InterfazConservada": "Antes de adaptar deben resolverse las contrapartes supervivientes del módulo, sin apoyo en fragmentos inexistentes",
    })

    # Las dos anotaciones no son geometría de producto: posición y fuente son
    # composición gráfica. Sus textos evitan incorporar números que queden obsoletos.
    a = annotation("RotuloComparacion", ["HIPOTESIS VISUALES - NO FABRICAR", "Lamina plana / reserva de alambre", "Contacto, fuerza y recorrido reales pendientes"], (0, -48, 60))
    a.setExpression("Position.z", H + "LaminaZ + " + H + "MordazaEspesor + 8 mm")
    b = annotation("RotuloServicio", ["EXTRACCION ILUSTRATIVA EN BANCO", "Contencion de energia y cierres PENDIENTES"], (0, 72, 115))
    b.setExpression("Position.y", H + "SeparacionServicio - " + H + "NucleoAncho / 2")
    b.setExpression("Position.z", H + "ExtraccionCartucho + " + H + "LaminaZ + " + H + "MordazaEspesor + 8 mm")

    doc.recompute()
    if App.GuiUp:
        for obj in helpers:
            obj.ViewObject.Visibility = False
        for obj in finals:
            obj.ViewObject.Visibility = True
        doc.EXT_BrazoMuestra.ViewObject.Visibility = False
        doc.EXT_SectorReferencia.ViewObject.Visibility = False
        service_scene.ViewObject.Visibility = False
        a.ViewObject.Visibility = False
        b.ViewObject.Visibility = False
        import FreeCADGui as Gui
        # Inicializa los wrappers Coin de la GUI de FreeCAD antes de obtener
        # nodos de cámara; la importación es intencionada aunque no use coin.
        from pivy import coin
        view = Gui.activeDocument().activeView()
        view.viewAxonometric()
        view.fitAll()
        camera = view.getCameraNode()
        # SoOrthographicCamera tiene height; la perspectiva tiene heightAngle.
        if hasattr(camera, "height"):
            camera.height.setValue(camera.height.getValue() * 1.15)
        Gui.updateGui()
    doc.recompute()
    return doc


def save_new(doc, path):
    """Guarda un FCStd nuevo; nunca sobrescribe un estudio editado."""
    path = Path(path).expanduser().resolve()
    if path.suffix.lower() != ".fcstd":
        raise ValueError("La salida debe ser un .FCStd")
    if path.exists():
        raise FileExistsError("No se sobrescribe el estudio existente: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.recompute()
    doc.saveAs(str(path))
    return path


def export_views(doc, output_dir, overwrite=False):
    """Exporta vistas PNG sólo con GUI. No afirma que el OpenGL sea utilizable."""
    import FreeCAD as App
    if not App.GuiUp:
        raise RuntimeError("Las vistas requieren una sesión gráfica de FreeCAD")
    import FreeCADGui as Gui
    # Pivy/Coin pertenece al entorno gráfico de FreeCAD; no es un complemento.
    from pivy import coin
    output_dir = Path(output_dir).expanduser().resolve()
    names = ("suspension_comparativa.png", "suspension_lamina.png", "suspension_alambre.png", "extraccion_conceptual.png")
    paths = [output_dir / name for name in names]
    if not overwrite and any(p.exists() for p in paths):
        raise FileExistsError("Ya existe una vista de salida; usar otra carpeta o overwrite=True")
    output_dir.mkdir(parents=True, exist_ok=True)
    scene_objects = [doc.VarianteLamina, doc.VarianteAlambre, doc.EscenaExtraccion,
                     doc.RotuloComparacion, doc.RotuloServicio]
    original = [obj.ViewObject.Visibility for obj in scene_objects]
    active_before = App.ActiveDocument
    configurations = ((True, True, False, False, False), (True, False, False, False, False),
                      (False, True, False, False, False), (False, False, True, False, False))
    try:
        App.setActiveDocument(doc.Name)
        for path, visible in zip(paths, configurations):
            for obj, flag in zip(scene_objects, visible):
                obj.ViewObject.Visibility = flag
            view = Gui.activeDocument().activeView()
            # Propaga la visibilidad al scene graph antes de calcular el encuadre.
            # No se recalcula el documento ni se alteran sus formas.
            Gui.updateGui()
            view.redraw()
            Gui.updateGui()
            view.viewAxonometric()
            view.redraw()
            Gui.updateGui()
            view.fitAll()
            # El visor debe actualizar también sus planos de recorte antes de
            # que saveImage use la cámara en el render fuera de pantalla.
            view.redraw()
            Gui.updateGui()
            camera = view.getCameraNode()
            if hasattr(camera, "height"):
                camera.height.setValue(camera.height.getValue() * 1.15)
            view.redraw()
            Gui.updateGui()
            view.saveImage(str(path), 1600, 1050, "White")
    finally:
        for obj, flag in zip(scene_objects, original):
            obj.ViewObject.Visibility = flag
        Gui.updateGui()
        Gui.getDocument(doc.Name).activeView().redraw()
        Gui.updateGui()
        if active_before:
            App.setActiveDocument(active_before.Name)
    return dict(zip(names, map(str, paths)))


def build(output_dir, render=False):
    """API breve: crea, guarda y, opcionalmente, exporta vistas; devuelve doc."""
    output_dir = Path(output_dir).expanduser().resolve()
    target = output_dir / MODEL_NAME
    if target.exists():
        raise FileExistsError("No se sobrescribe " + str(target))
    doc = create_document()
    save_new(doc, target)
    if render:
        export_views(doc, output_dir / "vistas")
    return doc


if __name__ == "__main__":
    create_document()
