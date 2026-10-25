# SPDX-License-Identifier: MIT
"""Añadir dos vínculos documentales al maestro, únicamente sobre una COPIA.

Ejecutar apply(document) dentro de FreeCAD con una copia ya abierta. No guarda,
no recalcula ni modifica geometría. No cambia la revisión geométrica 0.1.

Secuencia para el coordinador (rutas elegidas explícitamente por quien ejecuta):
    before = metadata(ruta_de_la_copia)  # copia del FCStd todavía sin modificar
    changed = apply(document)           # mismo archivo abierto en FreeCAD
    finalized = finalize(document, before)  # solo marcas de esos registros
    document.save()                     # guardar la copia, nunca el original
    after = metadata(ruta_de_la_copia)
    report = verify(before, after)

metadata() solo lee el ZIP nativo. verify() compara propiedades persistidas,
IDs/tipos, expresiones, hojas/alias y formas BREP serializadas. No es una prueba
física ni una comparación binaria del contenedor o del estado de la vista GUI.
La fecha automática LastModifiedDate se excluye expresamente de la comparación.
No llamar a recompute(), ni siquiera selectivo, entre estos pasos. Usar una
copia fresca si una ejecución anterior ha recalculado o ensuciado otros objetos.

Si guardar en FreeCAD reserializa BREP ajenos, conservative_copy() puede generar
una salida nueva: toma Document.xml literalmente de la copia nativa validada y
todos los demás miembros del maestro original. No inventa ni reescribe XML.
La salida debe superar verify() y abrirse después en FreeCAD sin recalcular ni
guardar; esa reapertura no es validación física.
"""
from copy import copy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


CAD_DIR = Path(__file__).resolve().parents[1]
MASTER = CAD_DIR / "X20Pro_Base_Arquitectura.FCStd"
CANONICAL_SHA256 = "1aa0a2d4a6c3b89c4475ee857c19d5b38912199f60006ce2265fcc41d411f6aa"
GROUP = "VinculosDocumentales"
SOURCE = (
    "cad/REVISION.md · Dos vínculos por incorporar al actualizar conjuntamente "
    "registro y CAD · 2026-10-25: "
)
# Claves con nombres internos, nunca Label ni alias de hoja.
CHANGES = {
    "IF02.Medidas": ("App::PropertyString", "M04–M09 por lado; M42; M43",
                     "M04–M09 por lado; M15 por lado; M42; M43"),
    "IF02.ProcedenciaVinculos": (
        "App::PropertyString", None,
        SOURCE + "IF02 → M15 por lado; comprobación independiente, pendiente."),
    "IF04.Medidas": ("App::PropertyString", "M25–M27; M40–M45; M59",
                     "M25–M27; M40–M45; M55; M59; M60"),
    "IF04.Relaciones": ("App::PropertyLinkList", None, ["IF13"]),
    "IF04.ProcedenciaVinculos": (
        "App::PropertyString", None,
        SOURCE + "IF04 → IF13 / M55 / M60; requisitos vinculados, sin nueva medida ni validación."),
}
JSON_FIELDS = {
    "Medidas": "medidas", "Relaciones": "relaciones",
    "ProcedenciaVinculos": "procedencia_vinculos",
}


def _check_registry():
    registry = json.loads((CAD_DIR / "interfaces.json").read_text(encoding="utf-8"))
    items = registry["interfaces"]
    by_id = {item["id"]: item for item in items}
    if len(by_id) != len(items) or "IF13" not in by_id:
        raise ValueError("Registro con IDs duplicados o sin IF13")
    for key, (_, _, expected) in CHANGES.items():
        name, prop = key.split(".")
        if by_id.get(name, {}).get(JSON_FIELDS[prop]) != expected:
            raise ValueError("El registro no coincide con esta migración: " + key)


def _copy_path(document):
    filename = getattr(document, "FileName", "")
    path = Path(filename).resolve() if filename else None
    if path is None or not path.is_file():
        raise ValueError("Abrir primero una copia existente y guardada del FCStd")
    if path == MASTER.resolve() or (MASTER.exists() and path.samefile(MASTER)):
        raise ValueError("No modificar el maestro original: abrir una copia independiente")
    return path


def apply(document):
    """Actualizar las cinco propiedades autorizadas; devolver sus claves.

    Idempotente. Rechaza ruta original, objetos/tipos ausentes o contenido ajeno
    antes de editar. Un error durante la transacción revierte sus cambios.
    No añade cotas, resultados de ensayo, alias, objetos ni geometría.
    """
    _copy_path(document)
    _check_registry()
    objects = {name: document.getObject(name) for name in ("IF02", "IF04", "IF13")}
    for name, obj in objects.items():
        if obj is None or obj.TypeId != "App::FeaturePython":
            raise ValueError("Objeto ausente o tipo incompatible: " + name)
        if obj.Proxy is not None:
            raise ValueError("Proxy ejecutable ajeno a la migración: " + name)
    if objects["IF04"] in objects["IF13"].OutListRecursive:
        raise ValueError("IF04 → IF13 produciría un ciclo de dependencias")
    plan = []
    for key, (type_id, old, expected) in CHANGES.items():
        name, prop = key.split(".")
        obj = objects[name]
        exists = prop in obj.PropertiesList
        if exists:
            if obj.getTypeIdOfProperty(prop) != type_id:
                raise ValueError("Tipo de propiedad incompatible: " + key)
            current = getattr(obj, prop)
            if type_id == "App::PropertyLinkList":
                if any(target.Document != document for target in current):
                    raise ValueError("Relación hacia otro documento: " + key)
                current = [target.Name for target in current]
            if current != expected and (old is None or current != old):
                raise ValueError("Contenido ajeno: no se sobrescribe " + key)
            if any(entry[0] == prop for entry in obj.ExpressionEngine):
                raise ValueError("Expresión ajena sobre la propiedad: " + key)
        elif old is not None:
            raise ValueError("Falta una propiedad original requerida: " + key)
        else:
            current = None
        if not exists or current != expected:
            plan.append((key, obj, prop, type_id, exists, expected))
    if not plan:
        return []
    document.openTransaction("Vinculos IF02-M15 e IF04-IF13-M55-M60")
    try:
        for _, obj, prop, type_id, exists, expected in plan:
            if not exists:
                obj.addProperty(type_id, prop, GROUP)
            value = [objects[name] for name in expected] if type_id == "App::PropertyLinkList" else expected
            setattr(obj, prop, value)
        document.commitTransaction()
    except Exception:
        document.abortTransaction()
        raise
    return [entry[0] for entry in plan]


def finalize(document, before):
    """Limpiar solo las marcas Touched de los dos registros ya actualizados.

    Usar inmediatamente después de apply(), con metadata() de la copia previa.
    No recalcula, no guarda y no limpia ningún otro objeto. La ausencia de
    cálculo solo se admite para estos registros y su grupo documental conocido;
    no es una función general para ocultar errores ni trabajo geométrico pendiente.
    Devuelve los nombres cuya marca se ha limpiado; repetirla devuelve [].
    """
    _copy_path(document)
    _check_registry()
    names = ("IF02", "IF04")
    objects = {name: document.getObject(name) for name in names}
    # Todas las condiciones se comprueban antes de llamar a purgeTouched().
    for name, obj in objects.items():
        prior = before["objects"].get(name)
        if (prior is None or prior.get("type") != "App::FeaturePython"
                or prior.get("Touched", "0") != "0"
                or prior.get("Invalid", "0") != "0"):
            raise ValueError("El registro previo no estaba limpio: " + name)
        if obj is None or obj.TypeId != "App::FeaturePython":
            raise ValueError("Registro ausente o tipo incompatible: " + name)
        if obj.Proxy is not None or "Shape" in obj.PropertiesList or obj.ExpressionEngine:
            raise ValueError("El registro tiene cálculo o geometría: " + name)
        if set(obj.State) - {"Touched", "Up-to-date"}:
            raise ValueError("Estado no admisible para finalización: " + name)
        for dependent in obj.InListRecursive:
            if (dependent.Name != "InterfacesFuncionales"
                    or dependent.TypeId != "App::DocumentObjectGroup"
                    or "Shape" in dependent.PropertiesList
                    or getattr(dependent, "Proxy", None) is not None
                    or dependent.ExpressionEngine
                    or obj not in dependent.Group):
                raise ValueError("Dependiente ajeno al registro documental: " + dependent.Name)
    for obj in document.Objects:
        if obj.Name not in names and "Touched" in obj.State:
            raise ValueError("Otro objeto requiere revisión; no se limpia: " + obj.Name)
    for key, (type_id, _, expected) in CHANGES.items():
        name, prop = key.split(".")
        obj = objects[name]
        if prop not in obj.PropertiesList or obj.getTypeIdOfProperty(prop) != type_id:
            raise ValueError("Migración incompleta o tipo incompatible: " + key)
        value = getattr(obj, prop)
        if type_id == "App::PropertyLinkList":
            if any(target.Document != document for target in value):
                raise ValueError("Relación hacia otro documento: " + key)
            value = [target.Name for target in value]
        if value != expected:
            raise ValueError("Migración incompleta o contenido ajeno: " + key)
    purged = [name for name, obj in objects.items() if "Touched" in obj.State]
    for name in purged:
        objects[name].purgeTouched()
    if any("Touched" in obj.State for obj in objects.values()):
        raise RuntimeError("FreeCAD no limpió las marcas documentales; no guardar")
    return purged


def _xml(node):
    """Contenido persistido sin indentación ni indicador transitorio status."""
    return {
        "tag": node.tag,
        "attributes": {k: v for k, v in sorted(node.attrib.items()) if k != "status"},
        "text": (node.text or "").strip(),
        "children": [_xml(child) for child in node],
    }


def metadata(path):
    """Leer los datos guardados; no abrir ni escribir el FCStd en FreeCAD."""
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("Document.xml"))
        objects = {obj.get("name"): dict(obj.attrib) for obj in root.findall("./Objects/Object")}
        properties = {}
        extras = {}
        for obj in root.findall("./ObjectData/Object"):
            name = obj.get("name")
            for prop in obj.findall("./Properties/Property"):
                properties[name + "." + prop.get("name")] = _xml(prop)
            extras[name] = [_xml(child) for child in obj if child.tag != "Properties"]
        geometry = {
            name: sha256(archive.read(name)).hexdigest()
            for name in archive.namelist()
            if name.endswith((".brp", ".Shape.Map.txt")) or name == "StringHasher.Table.txt"
        }
        document_props = {
            prop.get("name"): _xml(prop) for prop in root.findall("./Properties/Property")
            if prop.get("name") != "LastModifiedDate"
        }
    return {"document": document_props, "objects": objects, "properties": properties,
            "object_extras": extras, "geometry": geometry}


def _saved_value(prop):
    if prop is None:
        return None
    type_id = prop["attributes"]["type"]
    content = prop["children"][0]
    if type_id == "App::PropertyString":
        return content["attributes"]["value"]
    if type_id == "App::PropertyLinkList":
        return [link["attributes"]["value"] for link in content["children"]]
    raise ValueError("Tipo no autorizado en un vínculo de esta migración: " + type_id)


def verify(before, after):
    """Comparar dos resultados de metadata(); fallar ante cambios ajenos."""
    changed = []
    for key, (type_id, old, expected) in CHANGES.items():
        previous = before["properties"].get(key)
        result = after["properties"].get(key)
        if result is None or result["attributes"].get("type") != type_id or _saved_value(result) != expected:
            raise ValueError("Resultado ausente o incorrecto: " + key)
        if previous is not None:
            if previous["attributes"].get("type") != type_id:
                raise ValueError("Tipo previo incompatible: " + key)
            previous_value = _saved_value(previous)
            if previous_value != expected and (old is None or previous_value != old):
                raise ValueError("Contenido previo ajeno: " + key)
            if previous["attributes"] != result["attributes"]:
                raise ValueError("Metadatos de propiedad alterados: " + key)
        elif old is not None:
            raise ValueError("Faltaba una propiedad original requerida: " + key)
        if previous != result:
            changed.append(key)
    for section in ("document", "objects", "object_extras", "geometry"):
        if before[section] != after[section]:
            raise ValueError("Cambio ajeno a los vínculos en: " + section)
    protected_before = {k: v for k, v in before["properties"].items() if k not in CHANGES}
    protected_after = {k: v for k, v in after["properties"].items() if k not in CHANGES}
    if protected_before != protected_after:
        keys = sorted(k for k in protected_before.keys() | protected_after.keys()
                      if protected_before.get(k) != protected_after.get(k))
        raise ValueError("Propiedades ajenas alteradas: " + ", ".join(keys))
    return {"changed": changed, "protected_properties_equal": True,
            "object_ids_and_types_equal": True, "serialized_geometry_equal": True,
            "physical_validation": False}


def _check_native_document_xml(original_xml, native_xml):
    """Verificar el XML completo; las normalizaciones son solo para comparar."""
    roots = [ET.fromstring(content) for content in (original_xml, native_xml)]
    for root in roots:
        if root.tag != "Document":
            raise ValueError("Document.xml no contiene un documento FreeCAD")
        for props in root.iter("Properties"):
            names = [prop.get("name") for prop in props.findall("Property")]
            if len(names) != len(set(names)) or int(props.get("Count", "-1")) != len(names):
                raise ValueError("Propiedades duplicadas o contador incoherente en el XML")
        for container_path in ("Objects", "ObjectData"):
            container = root.find(container_path)
            nodes = container.findall("Object") if container is not None else []
            names = [node.get("name") for node in nodes]
            if (container is None or len(names) != len(set(names))
                    or int(container.get("Count", "-1")) != len(nodes)):
                raise ValueError("Inventario de objetos incoherente en el XML")
        for deps in root.findall("./Objects/ObjectDeps"):
            if int(deps.get("Count", "-1")) != len(deps.findall("Dep")):
                raise ValueError("Contador de dependencias incoherente en el XML")
    for key, (type_id, old, expected) in CHANGES.items():
        name, prop_name = key.split(".")
        selector = "./ObjectData/Object[@name='%s']/Properties/Property[@name='%s']" % (name, prop_name)
        previous, result = [root.find(selector) for root in roots]
        if result is None or result.get("type") != type_id or _saved_value(_xml(result)) != expected:
            raise ValueError("Propiedad nativa final ausente o incorrecta: " + key)
        if old is None:
            if previous is not None:
                raise ValueError("El original contiene ya una propiedad nueva: " + key)
        elif (previous is None or previous.get("type") != type_id
              or _saved_value(_xml(previous)) != old
              or _xml(previous)["attributes"] != _xml(result)["attributes"]):
            raise ValueError("Propiedad original o sus metadatos no coinciden: " + key)
    # El enlace nativo tiene también una entrada de dependencia serializada.
    # Se admite exactamente esa arista; ningún cambio de dependencias ajenas.
    for index, root in enumerate(roots):
        deps = root.findall("./Objects/ObjectDeps[@Name='IF04']")
        expected_deps = [] if index == 0 else [{"Name": "IF13"}]
        if len(deps) != 1 or [dict(child.attrib) for child in deps[0]] != expected_deps:
            raise ValueError("La dependencia nativa IF04 → IF13 no es la prevista")
        for child in list(deps[0]):
            deps[0].remove(child)
        deps[0].set("Count", "0")
        for key in CHANGES:
            name, prop_name = key.split(".")
            props = root.find("./ObjectData/Object[@name='%s']/Properties" % name)
            prop = props.find("Property[@name='%s']" % prop_name)
            if prop is not None:
                props.remove(prop)
                props.set("Count", str(int(props.get("Count")) - 1))
        # Mismas exclusiones que el comparador existente: fecha automática y
        # status transitorio (_xml). Touched de los objetos NO se excluye.
        props = root.find("Properties")
        date = props.find("Property[@name='LastModifiedDate']")
        if date is not None:
            props.remove(date)
            props.set("Count", str(int(props.get("Count")) - 1))
        # Estos inventarios son mapas por nombre; el orden XML no altera los IDs.
        for path in ("Objects", "ObjectData"):
            container = root.find(path)
            container[:] = sorted(container, key=lambda n: (n.tag, n.get("name", n.get("Name", ""))))
    if _xml(roots[0]) != _xml(roots[1]):
        raise ValueError("Document.xml contiene diferencias estructurales o datos ajenos a los cinco vínculos")


def conservative_copy(original_path, native_metadata_path, output_path):
    """Crear una copia documental nueva conservando todos los demás miembros.

    original_path: maestro canónico con SHA256 fijado en este módulo.
    native_metadata_path: copia guardada por FreeCAD tras apply + finalize.
    output_path: archivo inexistente, diferente de ambas entradas.

    Solo Document.xml procede de la copia nativa; se copia literalmente, sin
    construir ni modificar nodos. Todos los restantes miembros, incluidos BREP,
    mapas y GuiDocument.xml, conservan exactamente sus bytes descomprimidos del
    original. Se conserva ZipInfo y comentario del archivo; el contenedor ZIP se
    vuelve a empaquetar y no se promete identidad de los flujos comprimidos.

    Antes de escribir se validan los cinco valores y todo el XML protegido,
    incluida la única arista derivada IF04 → IF13 y sus contadores. Después se
    comprueba cada miembro y se ejecuta verify() sin modificarlo. Si falla, se
    elimina exclusivamente la salida recién creada; las entradas no se escriben.
    """
    _check_registry()
    original = Path(original_path).resolve()
    native = Path(native_metadata_path).resolve()
    output = Path(output_path).resolve()
    if original == native or original.samefile(native):
        raise ValueError("Original y fuente nativa de metadatos deben ser archivos distintos")
    if output.exists() or output in (original, native, MASTER.resolve()):
        raise FileExistsError("La salida debe ser nueva y no puede sustituir ninguna entrada")
    if not output.parent.is_dir():
        raise FileNotFoundError("La carpeta de salida debe existir: " + str(output.parent))
    original_bytes = original.read_bytes()
    if sha256(original_bytes).hexdigest() != CANONICAL_SHA256:
        raise ValueError("El original no coincide con el SHA256 canónico de esta migración")
    native_bytes = native.read_bytes()
    before = metadata(BytesIO(original_bytes))
    created = False
    try:
        with ZipFile(BytesIO(original_bytes)) as source, ZipFile(BytesIO(native_bytes)) as donor:
            original_names, native_names = source.namelist(), donor.namelist()
            if (len(original_names) != len(set(original_names))
                    or len(native_names) != len(set(native_names))
                    or set(original_names) != set(native_names)):
                raise ValueError("Miembros ZIP duplicados o inventarios de archivo diferentes")
            original_xml, native_xml = source.read("Document.xml"), donor.read("Document.xml")
            _check_native_document_xml(original_xml, native_xml)
            with output.open("xb") as handle:
                created = True
                with ZipFile(handle, "w") as result:
                    result.comment = source.comment
                    for entry in source.infolist():
                        content = native_xml if entry.filename == "Document.xml" else source.read(entry.filename)
                        result.writestr(copy(entry), content)
            with ZipFile(output) as result:
                if result.namelist() != original_names or result.comment != source.comment:
                    raise ValueError("El archivo resultante cambió el inventario, orden o comentario")
                for name in original_names:
                    expected = native_xml if name == "Document.xml" else source.read(name)
                    if result.read(name) != expected:
                        raise ValueError("Contenido de miembro no conservado: " + name)
        report = verify(before, metadata(output))
    except Exception:
        if created:
            output.unlink()
        raise
    return {"output": str(output), "sha256": sha256(output.read_bytes()).hexdigest(),
            "original_sha256": CANONICAL_SHA256,
            "native_metadata_sha256": sha256(native_bytes).hexdigest(),
            "preserved_members": len(original_names) - 1,
            "document_xml_copied_verbatim": True, "verification": report,
            "freecad_reopen_pending": True}
