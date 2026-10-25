# SPDX-License-Identifier: MIT
"""Copiar únicamente dos visibilidades y la cámara, preservando el modelo probado.

La fuente geométrica ya ha superado la comprobación nativa. FreeCAD puede
normalizar BREP y propiedades al volver a guardar; este paso no los sustituye.
Toma esos tres datos de una copia guardada por FreeCAD y mantiene todos los
demás miembros del FCStd original. La apertura nativa posterior es obligatoria.
"""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

EXPECTED_SOURCE = "a076ffde6d0e540bfefc971d9126db0dbe4a83004f054ba9ff330d10f3c43965"
ANNOTATIONS = ("RotuloComparacion", "RotuloServicio")


def copy_presentation(source, native_view_copy, target):
    source, native_view_copy, target = map(Path, (source, native_view_copy, target))
    if target.exists() or target.resolve() in (source.resolve(), native_view_copy.resolve()):
        raise ValueError("La salida debe ser una copia nueva")
    raw = source.read_bytes()
    if sha256(raw).hexdigest() != EXPECTED_SOURCE:
        raise ValueError("La fuente no es el modelo probado de esta revisión")
    with ZipFile(BytesIO(raw)) as original, ZipFile(native_view_copy) as native:
        if len(original.namelist()) != len(set(original.namelist())):
            raise ValueError("Miembros duplicados en la fuente")
        old_gui = ET.fromstring(original.read("GuiDocument.xml"))
        new_gui = ET.fromstring(native.read("GuiDocument.xml"))
        old_names = [n.get("name") for n in old_gui.findall("./ViewProviderData/ViewProvider")]
        new_names = [n.get("name") for n in new_gui.findall("./ViewProviderData/ViewProvider")]
        if set(old_names) != set(new_names) or len(old_names) != len(new_names):
            raise ValueError("La copia gráfica tiene otro inventario de objetos")
        for name in ANNOTATIONS:
            xpath = "./ViewProviderData/ViewProvider[@name='" + name + "']/Properties/Property[@name='Visibility']"
            a, b = old_gui.find(xpath), new_gui.find(xpath)
            if a is None or b is None or b.get("type") != "App::PropertyBool":
                raise ValueError("Visibilidad nativa ausente")
            state = b.find("Bool")
            if state is None or state.get("value") != "false":
                raise ValueError("La anotación debe estar oculta en la copia nativa")
            parent = old_gui.find("./ViewProviderData/ViewProvider[@name='" + name + "']/Properties")
            index = list(parent).index(a)
            parent.remove(a)
            parent.insert(index, deepcopy(b))
        a, b = old_gui.find("Camera"), new_gui.find("Camera")
        if a is None or b is None or not b.get("settings", "").startswith("OrthographicCamera"):
            raise ValueError("Cámara ortográfica nativa ausente")
        index = list(old_gui).index(a)
        old_gui.remove(a)
        old_gui.insert(index, deepcopy(b))
        gui_data = ET.tostring(old_gui, encoding="utf-8", xml_declaration=True)
        stream = BytesIO()
        with ZipFile(stream, "w") as out:
            out.comment = original.comment
            for info in original.infolist():
                out.writestr(deepcopy(info), gui_data if info.filename == "GuiDocument.xml" else original.read(info.filename))
        result = stream.getvalue()
        with ZipFile(BytesIO(result)) as out:
            if original.namelist() != out.namelist():
                raise ValueError("Cambió el inventario del archivo")
            changed = [name for name in original.namelist() if original.read(name) != out.read(name)]
            if changed != ["GuiDocument.xml"]:
                raise ValueError("Cambios ajenos a la presentación")
            preserved = len(original.namelist()) - 1
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as output:
        output.write(result)
    return {"ok": True, "sha256_fuente": sha256(raw).hexdigest(),
            "sha256_final": sha256(result).hexdigest(), "miembros_cambiados": changed,
            "miembros_identicos": preserved, "apertura_nativa_pendiente": True}
