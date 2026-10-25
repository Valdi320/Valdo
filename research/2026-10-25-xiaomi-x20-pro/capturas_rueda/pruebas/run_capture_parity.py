"""Repite las 23 pruebas y coteja sus mismas fichas sintéticas en JS/Python.

No modifica productos, CAD ni Git. Todos los fixtures son ficticios.
El resultado de rechazo se compara sin exigir mensaje o etapa idénticos.
Escribe resultados sólo en consola; usa temporales del sistema fuera del proyecto.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[2]
CAPTURE = Path(__file__).resolve().parents[1]
TESTS = Path(__file__).resolve().parent
GATES = ("registro", "pasador_local", "soporte_fabricable", "colocacion_global", "fabricacion")
FALSE_GATES = dict.fromkeys(GATES, False)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def normalize(result):
    gates = {key: result.get("puertas", {}).get(key, False) for key in GATES}
    return {"accepted": not bool(result.get("errores")) and gates["registro"],
            "gates": gates, "declared": result.get("medidas_declaradas"), "stage": "validate"}


NODE_RUNNER = r"""
const fs=require('fs'),vm=require('vm');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const sandbox={module:{exports:{}}};
vm.runInNewContext(input.source,sandbox,{timeout:5000});
const api=sandbox.module.exports;
const keys=['registro','pasador_local','soporte_fabricable','colocacion_global','fabricacion'];
const closed=()=>Object.fromEntries(keys.map(k=>[k,false]));
const out=input.cases.map(c=>{
 let data;
 try { data=api.parseStrict(c.raw); }
 catch(e){return {accepted:false,gates:closed(),declared:null,stage:'parse_rejected'};}
 try{
  const r=api.validate(data,input.spec);
  return {accepted:r.errores.length===0&&r.puertas.registro,
    gates:Object.fromEntries(keys.map(k=>[k,r.puertas[k]===true])),
    declared:r.medidas_declaradas,stage:'validate'};
 }catch(e){return {crash:e.name+': '+e.message};}
});
process.stdout.write(JSON.stringify(out));
"""


def main():
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node no disponible; no se instala software.")
    test_spec = importlib.util.spec_from_file_location("capture_contract_review", TESTS / "test_capture_contract.py")
    tests = importlib.util.module_from_spec(test_spec)
    test_spec.loader.exec_module(tests)

    class RecordedContract(tests.CaptureContract):
        parity_cases = []

        @classmethod
        def tearDownClass(cls):
            # Se conserva la copia temporal hasta terminar la paridad.
            pass

    js_body = (CAPTURE / "validacion.js").read_bytes()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(RecordedContract)
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    print(output.getvalue(), file=sys.stderr, end="")
    if not hasattr(RecordedContract, "validator"):
        if hasattr(RecordedContract, "tmp"):
            RecordedContract.tmp.cleanup()
        return 1

    try:
        cases = RecordedContract.parity_cases
        py_results = []
        path = RecordedContract.tmp_path / "parity_synthetic.json"
        for case in cases:
            path.write_text(case["raw"], encoding="utf-8")
            try:
                data = RecordedContract.validator.load_json(path)
            except ValueError:
                py_results.append({"accepted": False, "gates": FALSE_GATES.copy(),
                                   "declared": None, "stage": "parse_rejected"})
                continue
            try:
                py_results.append(normalize(RecordedContract.validator.validate(data)))
            except Exception as exc:
                py_results.append({"crash": type(exc).__name__ + ": " + str(exc)})

        payload = {"source": js_body.decode("utf-8"), "spec": RecordedContract.validator.SPEC, "cases": cases}
        run = subprocess.run([node, "-e", NODE_RUNNER], input=json.dumps(payload, ensure_ascii=True),
                             text=True, capture_output=True, timeout=20)
        if run.returncode:
            raise RuntimeError("Runner Node falló: " + run.stderr)
        js_results = json.loads(run.stdout)
        if len(js_results) != len(cases):
            raise RuntimeError("Número de resultados JS inesperado.")

        rows, mismatches = [], []
        for index, (case, py, js) in enumerate(zip(cases, py_results, js_results), 1):
            same = "crash" not in py and "crash" not in js and py["accepted"] == js["accepted"]
            if same:
                same = py["gates"] == js["gates"]
                if py["accepted"]:
                    same = same and py["declared"] == js["declared"]
                else:
                    same = same and py["gates"] == FALSE_GATES
            row = {"case": index, "test": case["test"], "kind": case["kind"],
                   "raw_sha256": sha(case["raw"].encode()), "python": py, "javascript": js, "same_contract": same}
            rows.append(row)
            if not same:
                mismatches.append(row)

        cad_unchanged = RecordedContract.cad_before == tests.digest_tree(tests.CAD)
        hashes = dict(RecordedContract.hashes, **{"validacion.js": sha(js_body)})
        current_hashes = {name: sha((CAPTURE / name).read_bytes()) for name in hashes}
        hashes["X20Pro_Base_Arquitectura.FCStd"] = RecordedContract.cad_before["X20Pro_Base_Arquitectura.FCStd"]
        summary = {"physical_measurements": False, "fixtures": "SINTETICOS",
                   "unit_tests": result.testsRun, "unit_failures": len(result.failures), "unit_errors": len(result.errors),
                   "parity_cases": len(cases), "parity_mismatches": len(mismatches),
                   "cad_unchanged": cad_unchanged,
                   "product_sources_unchanged": all(current_hashes[k] == v for k, v in hashes.items() if k in current_hashes),
                   "sha256": hashes}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if mismatches:
            print("MISMATCHES=" + json.dumps(mismatches, ensure_ascii=False))
        return 0 if result.wasSuccessful() and not mismatches and cad_unchanged and summary["product_sources_unchanged"] else 1
    finally:
        RecordedContract.tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
