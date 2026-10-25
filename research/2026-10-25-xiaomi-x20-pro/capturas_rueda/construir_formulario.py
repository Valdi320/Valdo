# SPDX-License-Identifier: MIT
"""Build an offline HTML artifact from the reviewed local sources; no dependencies."""
from pathlib import Path
import json


def build():
    root = Path(__file__).resolve().parent
    html = (root / "formulario.template.html").read_text(encoding="utf-8")
    spec = json.loads((root / "definiciones.json").read_text(encoding="utf-8"))
    parts = {
        "SPEC": json.dumps(spec, ensure_ascii=False).replace("<", "\\u003c"),
        "GUIDE": (root / "guia_rueda.svg").read_text(encoding="utf-8"),
        "VALIDATOR": (root / "validacion.js").read_text(encoding="utf-8").replace("</script", "<\\/script"),
        "APP": (root / "formulario.js").read_text(encoding="utf-8").replace("</script", "<\\/script"),
    }
    for key, value in parts.items():
        html = html.replace("@@" + key + "@@", value)
    if "@@" in html:
        raise RuntimeError("Unresolved placeholder in form")
    target = root / "Capturar_Rueda.html"
    target.write_text(html, encoding="utf-8")
    print(json.dumps({"archivo": str(target), "bytes": target.stat().st_size}))


if __name__ == "__main__":
    build()
