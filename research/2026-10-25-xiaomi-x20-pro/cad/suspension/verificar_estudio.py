# SPDX-License-Identifier: MIT
"""Comprobación acotada del estudio en FreeCAD, sin ensayos físicos.

run(study_module, output_dir, render=True) crea un documento independiente,
comprueba relaciones, guarda y reabre. Nunca cierra documentos ajenos ni
sobrescribe un FCStd existente. Devuelve (documento_reabierto, resultado).
Las dimensiones/ángulos usados son hipótesis de prueba, no datos del Xiaomi.
"""
from pathlib import Path
import hashlib
import math


def number(value):
    import FreeCAD as App
    if hasattr(value, "Value"):
        return float(value.Value)
    if isinstance(value, (int, float)):
        return float(value)
    return float(App.Units.Quantity(str(value)).Value)


def run(study, output_dir, render=True):
    import FreeCAD as App

    output_dir = Path(output_dir).resolve()
    target = output_dir / study.MODEL_NAME
    if target.exists():
        raise FileExistsError(str(target))
    result = {
        "revision": "0.3",
        "tipo": "COMPROBACION DE SOFTWARE Y GEOMETRIA DE ESTUDIO",
        "datos": "HIPOTESIS VISUALES; no medidas del robot",
        "validacion_fisica": False,
        "checks": {},
        "version_freecad": App.Version(),
    }
    owned = None

    def check(name, condition):
        result["checks"][name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    def close_own():
        nonlocal owned
        if owned and owned.Name in App.listDocuments():
            name = owned.Name
            owned = None
            App.closeDocument(name)

    try:
        doc = study.create_document()
        owned = doc
        sheet = doc.HipotesisVisuales
        cells = {row[4]: "B" + str(i) for i, row in enumerate(study.VISUAL_ROWS, 2)}
        values = {row[4]: row[1] for row in study.VISUAL_ROWS}

        def set_value(alias, value):
            sheet.set(cells[alias], value)
            doc.recompute()

        def global_point(obj):
            return obj.getGlobalPlacement().Base

        def wire_tip():
            line = doc.ALM_LineaAlambreMuestra
            local = App.Vector(number(line.X2), number(line.Y2), number(line.Z2))
            return line.getGlobalPlacement().multVec(local)

        def wire_length(obj):
            return math.sqrt(sum((number(getattr(obj, axis + "2")) - number(getattr(obj, axis + "1"))) ** 2 for axis in "XYZ"))

        invalid = [obj.Name for obj in doc.Objects
                   if any("Invalid" in state or "Error" in state for state in obj.State)]
        result["errores_objetos"] = invalid
        check("sin_errores_de_objetos", not invalid)
        shapes = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
        bad_shapes = [obj.Name for obj in shapes if obj.Shape.isNull() or not obj.Shape.isValid()]
        result["formas_invalidas"] = bad_shapes
        check("formas_no_nulas_y_validas", bool(shapes) and not bad_shapes)
        result["objetos_con_forma_comprobados"] = len(shapes)
        result["objetos_totales"] = len(doc.Objects)
        check("fabricacion_no_aprobada", not doc.EstadoEstudio.FabricacionAprobada)
        check("pasador_nominal", abs(doc.LAM_PasadorNominal.Height.Value - 38.5) < 1e-8
              and abs(doc.LAM_PasadorNominal.Radius.Value - 2) < 1e-8)
        check("presupuesto_inicial_40", abs(number(doc.PresupuestoAxial.get("B6")) - 40) < 1e-8)
        check("margen_inicial_menos_1_5", abs(number(doc.PresupuestoAxial.get("B7")) + 1.5) < 1e-8)
        check("presupuesto_alternativo_42", abs(number(doc.PresupuestoAxial.get("B9")) - 42) < 1e-8)
        check("angulo_nativo_15", abs(doc.LAM_BrazoMuestra.Placement.Rotation.Angle - math.radians(15)) < 1e-9)
        check("extremo_alambre_coincide_con_marcador", (wire_tip() - global_point(doc.ALM_MuestraInterfazMovil)).Length < 1e-7)
        reference_length = wire_length(doc.ALM_LineaAlambreReferencia)
        sample_length = wire_length(doc.ALM_LineaAlambreMuestra)
        check("alambre_se_alarga_en_muestra", sample_length > reference_length)
        result["longitudes_ilustrativas_alambre_mm"] = {"referencia": reference_length, "muestra": sample_length}

        marker_before = global_point(doc.ALM_MuestraInterfazMovil)
        reference_before = global_point(doc.ALM_ReferenciaInterfazMovil)
        set_value("AnguloMuestra", "20 deg")
        check("angulo_editable_20", abs(doc.ALM_BrazoMuestra.Placement.Rotation.Angle - math.radians(20)) < 1e-9)
        check("marcador_movil_responde", (global_point(doc.ALM_MuestraInterfazMovil) - marker_before).Length > 1)
        check("referencia_permanece_fija", (global_point(doc.ALM_ReferenciaInterfazMovil) - reference_before).Length < 1e-8)
        check("extremo_alambre_sigue_marcador", (wire_tip() - global_point(doc.ALM_MuestraInterfazMovil)).Length < 1e-7)
        check("sector_sigue_angulo", abs(doc.ALM_SectorReferencia.Angle.Value - 20) < 1e-8)
        set_value("AnguloMuestra", values["AnguloMuestra"])

        support_before = doc.LAM_ApoyoA.Shape.BoundBox.YMin
        set_value("ApoyoEspesor", "4 mm")
        check("apoyo_responde_un_mm", abs(doc.LAM_ApoyoA.Shape.BoundBox.YMin - support_before + 1) < 1e-8)
        check("presupuesto_responde_42", abs(number(doc.PresupuestoAxial.get("B6")) - 42) < 1e-8)
        check("pasador_conserva_nominal", abs(doc.ALM_PasadorNominal.Height.Value - 38.5) < 1e-8)
        set_value("ApoyoEspesor", values["ApoyoEspesor"])

        core_before = global_point(doc.EXT_Nucleo)
        cartridge_before = global_point(doc.EXT_Cartucho)
        pin_before = global_point(doc.EXT_PasadorNominal)
        set_value("ExtraccionCartucho", "65 mm")
        check("cartucho_extraido_diez_mm", abs(global_point(doc.EXT_Cartucho).z - cartridge_before.z - 10) < 1e-8)
        check("pasador_viaja_con_cartucho", abs(global_point(doc.EXT_PasadorNominal).z - pin_before.z - 10) < 1e-8)
        check("nucleo_permanece_fijo", (global_point(doc.EXT_Nucleo) - core_before).Length < 1e-8)
        set_value("ExtraccionCartucho", values["ExtraccionCartucho"])

        study.save_new(doc, target)
        close_own()
        reopened = App.openDocument(str(target))
        owned = reopened
        reopened.recompute()
        check("reapertura_con_valores_restaurados",
              abs(reopened.LAM_BrazoMuestra.Placement.Rotation.Angle - math.radians(15)) < 1e-9
              and abs(number(reopened.PresupuestoAxial.get("B6")) - 40) < 1e-8
              and abs(reopened.EXT_Cartucho.Placement.Base.z - 55) < 1e-8)
        check("reapertura_sin_aprobacion", not reopened.EstadoEstudio.FabricacionAprobada)
        if render:
            result["vistas"] = study.export_views(reopened, output_dir / "vistas")
        result["sha256_fcstd"] = hashlib.sha256(target.read_bytes()).hexdigest()
        result["ok"] = True
        return reopened, result
    except Exception as error:
        error.x20_result = result
        close_own()
        raise
