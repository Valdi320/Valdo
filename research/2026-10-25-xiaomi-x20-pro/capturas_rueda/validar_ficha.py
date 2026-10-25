# SPDX-License-Identifier: MIT
"""Validador sin dependencias externas. No prueba medidas ni resistencia física."""
from pathlib import Path
import argparse
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parent
SPEC = json.loads((ROOT / "definiciones.json").read_text(encoding="utf-8"))
FIELDS = {x["id"]: x for x in SPEC["campos"]}
STATES = set(SPEC["estados"])
TOP_KEYS = {"version_esquema", "id_captura", "origen", "fecha_medicion", "instrumento", "condicion", "evidencia_general", "pieza_rueda", "pieza_pasador", "lado", "pareja", "seccion_pasador", "danos", "extraccion", "mediciones", "notas", "fabricacion_aprobada"}
RECORD_KEYS = {"id", "estado", "valor_mm", "lecturas_mm", "incertidumbre_mm", "referencias", "evidencia", "nota"}


def is_number(v):
    if type(v) not in (int, float):
        return False
    try:
        return math.isfinite(v)
    except OverflowError:
        return False


def nonempty(v):
    return isinstance(v, str) and bool(v.strip())


def blank_record(field_id):
    return {"id": field_id, "estado": "pendiente", "valor_mm": None, "lecturas_mm": [], "incertidumbre_mm": None, "referencias": "", "evidencia": "", "nota": ""}


def blank_capture(capture_id="RUEDA_PENDIENTE"):
    return {
        "version_esquema": "0.2", "id_captura": capture_id, "origen": "unidad_real",
        "fecha_medicion": "", "instrumento": "", "condicion": "", "evidencia_general": "",
        "pieza_rueda": "", "pieza_pasador": "",
        "lado": {"valor": "desconocido", "evidencia": ""},
        "pareja": {"estado": "sin_confirmar", "evidencia": ""},
        "seccion_pasador": {"forma": "desconocida", "evidencia": ""},
        "danos": {"soporte_fijo": "desconocido", "pivote_movil": "desconocido", "gancho_movil": "desconocido", "nota": ""},
        "extraccion": {"direccion": "pendiente", "espacio_observado": "", "obstaculos": ""},
        "mediciones": [blank_record(x) for x in FIELDS], "notas": "", "fabricacion_aprobada": False,
    }


def validate(data):
    errors, warnings = [], []
    result = {"errores": errors, "avisos": warnings, "medidas_declaradas": 0, "puertas": {"registro": False, "pasador_local": False, "soporte_fabricable": False, "colocacion_global": False, "fabricacion": False}}
    if not isinstance(data, dict):
        errors.append("La ficha debe ser un objeto JSON.")
        return result
    def err(message):
        errors.append(message)
    missing = TOP_KEYS - set(data)
    extra = set(data) - TOP_KEYS
    if missing: err("Faltan campos de ficha: " + ", ".join(sorted(missing)))
    if extra: err("Campos no reconocidos: " + ", ".join(sorted(extra)))
    if data.get("version_esquema") != "0.2": err("Versión de esquema no admitida; se requiere 0.2.")
    if not isinstance(data.get("id_captura"), str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", data.get("id_captura", "")):
        err("ID de captura: 1–64 letras ASCII, cifras, guion o guion bajo; debe empezar por letra/cifra.")
    if data.get("origen") not in ("unidad_real", "prueba_software"): err("Origen no admitido.")
    if data.get("fabricacion_aprobada") is not False: err("Esta ficha no puede aprobar fabricación.")
    for key in ["fecha_medicion", "instrumento", "condicion", "evidencia_general", "pieza_rueda", "pieza_pasador", "notas"]:
        if not isinstance(data.get(key), str): err(key + " debe ser texto.")
    nested = [
        ("lado", {"valor", "evidencia"}, "valor", {"desconocido", "izquierdo", "derecho"}, "desconocido"),
        ("pareja", {"estado", "evidencia"}, "estado", {"sin_confirmar", "confirmada", "no_corresponde"}, "sin_confirmar"),
        ("seccion_pasador", {"forma", "evidencia"}, "forma", {"desconocida", "circular", "otra"}, "desconocida"),
    ]
    for key, keys, value_key, values, unknown in nested:
        item = data.get(key)
        if not isinstance(item, dict) or set(item) != keys:
            err(key + ": estructura incompleta o no reconocida.")
            continue
        if not isinstance(item.get(value_key), str) or item.get(value_key) not in values: err(key + ": valor no admitido.")
        if not isinstance(item.get("evidencia"), str): err(key + ": evidencia debe ser texto.")
        if item.get(value_key) != unknown and not nonempty(item.get("evidencia")): err(key + ": describe cómo lo has identificado.")
    pair = data.get("pareja", {})
    if isinstance(pair, dict) and pair.get("estado") == "confirmada" and not (nonempty(data.get("pieza_rueda")) and nonempty(data.get("pieza_pasador"))):
        err("Para confirmar la pareja hay que identificar rueda y pasador.")
    if nonempty(data.get("pieza_rueda")) and nonempty(data.get("pieza_pasador")) and data["pieza_rueda"].strip().lower() == data["pieza_pasador"].strip().lower():
        err("Rueda y pasador son piezas distintas: asigna identificadores diferentes.")
    damage = data.get("danos")
    if not isinstance(damage, dict) or set(damage) != {"soporte_fijo", "pivote_movil", "gancho_movil", "nota"}:
        err("Registro de daños incompleto.")
    else:
        for key in ["soporte_fijo", "pivote_movil", "gancho_movil"]:
            if damage[key] not in ("desconocido", "presente_sin_dano_visible", "danado", "ausente"): err("Estado de daño no admitido: " + key)
        if not isinstance(damage["nota"], str): err("La nota de daños debe ser texto.")
    extraction = data.get("extraccion")
    if not isinstance(extraction, dict) or set(extraction) != {"direccion", "espacio_observado", "obstaculos"}:
        err("Registro de extracción incompleto.")
    else:
        if extraction["direccion"] not in ("pendiente", "hacia_cara_a", "hacia_cara_b", "otra"): err("Dirección de extracción no admitida.")
        if not all(isinstance(extraction[k], str) for k in extraction): err("Extracción: se requieren textos.")
    records = data.get("mediciones")
    if not isinstance(records, list):
        err("mediciones debe ser una lista.")
        return result
    if len(records) > len(FIELDS): err("Hay más registros que magnitudes definidas.")
    measured, seen = {}, set()
    for item in records:
        if not isinstance(item, dict) or set(item) != RECORD_KEYS:
            err("Registro de medida incompleto o con campos no reconocidos.")
            continue
        field_id = item.get("id")
        if not isinstance(field_id, str) or field_id not in FIELDS:
            err("Magnitud no reconocida.")
            continue
        if field_id in seen: err("Magnitud duplicada: " + field_id)
        seen.add(field_id)
        label = FIELDS[field_id]["nombre"]
        state, value, reads, uncertainty = item["estado"], item["valor_mm"], item["lecturas_mm"], item["incertidumbre_mm"]
        if not isinstance(state, str) or state not in STATES:
            err(label + ": estado no admitido.")
            continue
        for key in ["referencias", "evidencia", "nota"]:
            if not isinstance(item[key], str): err(label + ": " + key + " debe ser texto.")
        if not isinstance(reads, list) or len(reads) > 20 or any(not is_number(v) or v <= 0 for v in reads):
            err(label + ": lecturas debe ser una lista de hasta 20 longitudes positivas finitas.")
            reads = []
        if state in {"pendiente", "no_recuperable", "no_aplica"}:
            if value is not None or reads or uncertainty is not None: err(label + ": un dato pendiente/no disponible no puede llevar números.")
            if state != "pendiente" and not nonempty(item["nota"]): err(label + ": explica por qué no está disponible o no aplica.")
            continue
        if not is_number(value) or value <= 0: err(label + ": se necesita una longitud positiva en mm.")
        if uncertainty is not None and (not is_number(uncertainty) or uncertainty <= 0): err(label + ": incertidumbre positiva o vacío si no se evaluó; nunca cero por defecto.")
        if not nonempty(item["referencias"]): err(label + ": identifica los puntos, sección y orientación medidos.")
        if not (nonempty(item["evidencia"]) or nonempty(data.get("evidencia_general"))): err(label + ": falta referencia a lectura, foto o croquis.")
        if state == "estimado":
            if not nonempty(item["nota"]): err(label + ": explica el método de estimación.")
            warnings.append(label + ": estimación conservada como nota; no se usa para geometría medida.")
        elif state == "medido":
            measured[field_id] = item
            if reads and is_number(value) and not min(reads) <= value <= max(reads): err(label + ": el valor declarado queda fuera de las repeticiones; revisa si son de la misma sección/condición.")
            if uncertainty is None: warnings.append(label + ": incertidumbre sin evaluar; los decimales no la sustituyen.")
            piece_key = "pieza_pasador" if FIELDS[field_id]["grupo"] == "pasador" else "pieza_rueda"
            if not nonempty(data.get(piece_key)): err(label + ": identifica la pieza física.")
    result["medidas_declaradas"] = len(measured)
    if measured:
        if not nonempty(data.get("instrumento")): err("Indica el instrumento utilizado.")
        if not nonempty(data.get("condicion")): err("Indica la condición de medida.")
        date = data.get("fecha_medicion")
        if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            err("Indica la fecha de medición como AAAA-MM-DD.")
        else:
            try:
                from datetime import date as Date
                Date.fromisoformat(date)
            except ValueError: err("Fecha de medición no válida.")
    if data.get("origen") == "prueba_software": warnings.append("Datos de prueba: no representan el robot del propietario.")
    if isinstance(data.get("lado"), dict) and data["lado"].get("valor") == "desconocido": warnings.append("Lado pendiente: no se asigna izquierda/derecha ni posición en el robot.")
    if isinstance(data.get("pareja"), dict) and data["pareja"].get("estado") != "confirmada": warnings.append("La pertenencia del pasador a esta rueda no está confirmada.")
    warnings.append("Esta revisión no reconstruye soportes, orientaciones globales ni retención; no autoriza fabricación.")
    result["puertas"]["registro"] = not errors
    result["puertas"]["pasador_local"] = not errors and data.get("origen") == "unidad_real" and {"pasador_diametro", "pasador_longitud"} <= set(measured) and isinstance(data.get("seccion_pasador"), dict) and data["seccion_pasador"].get("forma") == "circular"
    return result


def load_json(path):
    def reject_constant(value):
        raise ValueError("Número JSON no finito: " + value)
    def reject_duplicates(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj: raise ValueError("Clave JSON duplicada: " + key)
            obj[key] = value
        return obj
    text = Path(path).read_text(encoding="utf-8-sig")
    if len(text) > 200000: raise ValueError("La ficha supera 200000 caracteres.")
    return json.loads(text, parse_constant=reject_constant, object_pairs_hook=reject_duplicates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ficha", nargs="?")
    parser.add_argument("--plantilla", action="store_true")
    args = parser.parse_args()
    if args.plantilla:
        print(json.dumps(blank_capture(), ensure_ascii=False, indent=2))
    elif args.ficha:
        try:
            result = validate(load_json(args.ficha))
        except (OSError, ValueError) as error:
            result = {"errores": [str(error)], "puertas": {"registro": False, "fabricacion": False}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["puertas"]["registro"] else 2)
    else:
        parser.error("Indica ficha.json o --plantilla")
