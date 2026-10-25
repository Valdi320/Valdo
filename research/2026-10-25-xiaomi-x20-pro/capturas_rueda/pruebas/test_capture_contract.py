"""Pruebas independientes del contrato de captura 0.2.

Todos los números y etiquetas de este archivo son DATOS SINTÉTICOS de pruebas.
No representan medidas físicas del Xiaomi ni nominales de diseño.
Se ejecuta con Python 3 desde cualquier directorio.
El validador se copia al directorio temporal del sistema, fuera del proyecto.
No se modifica el original/CAD ni se escriben logs o bytecode en el producto.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[2]
CAPTURE = Path(__file__).resolve().parents[1]
TESTS = Path(__file__).resolve().parent
CAD = PROJECT / "cad"


def digest_tree(directory):
    return {
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


class CaptureContract(unittest.TestCase):
    # El runner de paridad activa este colector; no afecta a la ejecución normal.
    parity_cases = None

    @classmethod
    def setUpClass(cls):
        for directory in (PROJECT, CAPTURE, TESTS):
            locks = [p.name for p in directory.iterdir()
                     if p.is_file() and (p.name.lower().endswith(".lock")
                     or p.name.lower() in {"lock", "cerrojo", "bloqueo"}
                     or "cerrojo" in p.name.lower())]
            if locks:
                raise RuntimeError("Cerrojo encontrado; no se ejecutan las pruebas.")
        cls.cad_before = digest_tree(CAD)
        temporary_root = Path(tempfile.gettempdir()).resolve()
        if temporary_root == PROJECT or PROJECT in temporary_root.parents:
            raise RuntimeError("Configura el directorio temporal del sistema fuera del proyecto.")
        cls.tmp = tempfile.TemporaryDirectory(prefix="x20_capture_contract_")
        cls.tmp_path = Path(cls.tmp.name)
        cls.hashes = {}
        for name in ("validar_ficha.py", "definiciones.json"):
            body = (CAPTURE / name).read_bytes()
            cls.hashes[name] = hashlib.sha256(body).hexdigest()
            (cls.tmp_path / name).write_bytes(body)
        spec = importlib.util.spec_from_file_location(
            "capture_validator_review_snapshot", cls.tmp_path / "validar_ficha.py")
        cls.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.validator)
        print("SNAPSHOT_SHA256=" + json.dumps(cls.hashes, sort_keys=True), flush=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def blank(self):
        return self.validator.blank_capture("TEST_SOFTWARE_NO_MEDIDA_FISICA")

    def record(self, capture, field_id):
        return next(row for row in capture["mediciones"] if row["id"] == field_id)

    def pin_fixture(self, state="medido", origin="unidad_real"):
        """Simula el contrato de una ficha; incluso origin=unidad_real es ficticio."""
        data = self.blank()
        data.update({
            "origen": origin, "fecha_medicion": "2026-10-25",
            "instrumento": "INSTRUMENTO_FICTICIO: prueba de software",
            "condicion": "SIN PIEZA FISICA: valores sintéticos de prueba",
            "pieza_pasador": "TEST_PASADOR_001", "pieza_rueda": "TEST_RUEDA_001",
            "evidencia_general": "TEST_SOFTWARE: no hay medición física",
            "notas": "La prueba simula una declaración; no acredita medida real.",
        })
        data["seccion_pasador"] = {"forma": "circular", "evidencia": "HIPOTESIS SINTETICA"}
        for field_id, value in (("pasador_diametro", 3.17), ("pasador_longitud", 28.4)):
            self.record(data, field_id).update({
                "estado": state, "valor_mm": value,
                "referencias": "REFERENCIAS SINTETICAS de la misma sección/extremos",
                "nota": "Método sintético para prueba de contrato",
            })
        return data

    def validate(self, data):
        if self.parity_cases is not None:
            try:
                raw = json.dumps(data, ensure_ascii=True, allow_nan=False)
            except (TypeError, ValueError):
                # NaN/Infinity de Python no son JSON; sus literales se prueban
                # por separado mediante raw_path y parseo estricto.
                pass
            else:
                self.parity_cases.append({"test": self._testMethodName, "kind": "json_data", "raw": raw})
        return self.validator.validate(data)

    def assert_rejected(self, data):
        result = self.validate(data)
        self.assertTrue(result["errores"])
        self.assertFalse(result["puertas"]["registro"])
        self.assertFalse(result["puertas"]["pasador_local"])
        self.assertFalse(result["puertas"]["fabricacion"])
        return result

    def raw_path(self, text):
        if self.parity_cases is not None:
            self.parity_cases.append({"test": self._testMethodName, "kind": "raw_parser", "raw": text})
        path = self.tmp_path / "ficha_sintetica.json"
        path.write_text(text, encoding="utf-8")
        return path

    def test_01_pending_null_is_valid_without_geometry(self):
        data = self.blank()
        before = deepcopy(data)
        result = self.validate(data)
        self.assertEqual(result["errores"], [])
        self.assertTrue(result["puertas"]["registro"])
        self.assertEqual(result["medidas_declaradas"], 0)
        self.assertFalse(result["puertas"]["pasador_local"])
        self.assertEqual(data, before)
        self.assertTrue(all(row["valor_mm"] is None for row in data["mediciones"]))

    def test_02_pending_cannot_smuggle_zero_or_readings(self):
        for key, value in (("valor_mm", 0), ("lecturas_mm", [3.17]), ("incertidumbre_mm", 0)):
            with self.subTest(key=key):
                data = self.blank()
                self.record(data, "pasador_diametro")[key] = value
                self.assert_rejected(data)

    def test_03_unrecoverable_and_not_applicable_keep_null(self):
        for state in ("no_recuperable", "no_aplica"):
            with self.subTest(state=state):
                data = self.blank()
                row = self.record(data, "movil_ancho_pivote")
                row.update(estado=state, nota="CASO FICTICIO de geometría no disponible")
                result = self.validate(data)
                self.assertEqual(result["errores"], [])
                self.assertEqual(result["medidas_declaradas"], 0)
                self.assertIsNone(row["valor_mm"])

    def test_04_estimations_are_excluded_from_measured_geometry(self):
        result = self.validate(self.pin_fixture(state="estimado"))
        self.assertEqual(result["errores"], [])
        self.assertEqual(result["medidas_declaradas"], 0)
        self.assertFalse(result["puertas"]["pasador_local"])

    def test_05_software_origin_cannot_open_geometry(self):
        result = self.validate(self.pin_fixture(origin="prueba_software"))
        self.assertEqual(result["errores"], [])
        for key, allowed in result["puertas"].items():
            if key != "registro":
                self.assertFalse(allowed, key)

    def test_06_local_pin_does_not_invent_side_pair_or_global_pose(self):
        data = self.pin_fixture()
        before = deepcopy(data)
        result = self.validate(data)
        self.assertEqual(result["errores"], [])
        self.assertTrue(result["puertas"]["pasador_local"])
        for key in ("soporte_fabricable", "colocacion_global", "fabricacion"):
            self.assertFalse(result["puertas"][key])
        self.assertEqual(data, before)
        self.assertEqual(data["lado"]["valor"], "desconocido")
        self.assertEqual(data["pareja"]["estado"], "sin_confirmar")

    def test_07_partial_pin_does_not_open_complete_pin_gate(self):
        data = self.pin_fixture()
        data["mediciones"] = [self.record(data, "pasador_diametro")]
        result = self.validate(data)
        self.assertEqual(result["errores"], [])
        self.assertEqual(result["medidas_declaradas"], 1)
        self.assertFalse(result["puertas"]["pasador_local"])

    def test_08_identity_is_required_for_declared_physical_measure(self):
        data = self.pin_fixture()
        data["pieza_pasador"] = "   "
        self.assert_rejected(data)

    def test_09_side_and_pair_require_their_own_evidence(self):
        for key, subkey, value in (("lado", "valor", "izquierdo"), ("pareja", "estado", "confirmada")):
            with self.subTest(key=key):
                data = self.pin_fixture()
                data[key][subkey] = value
                self.assert_rejected(data)

    def test_10_wheel_and_pin_have_distinct_physical_ids(self):
        for wheel_id in ("TEST_PASADOR_001", "test_pasador_001", "  TeSt_PaSaDoR_001  "):
            with self.subTest(wheel_id=wheel_id):
                data = self.pin_fixture()
                data["pieza_rueda"] = wheel_id
                data["pareja"] = {"estado": "confirmada", "evidencia": "CASO SINTETICO"}
                self.assert_rejected(data)

    def test_11_numeric_types_are_not_coerced(self):
        for value in (None, True, False, "3.17", "3,17", "3.17 mm", 0, -1, float("nan"), float("inf")):
            with self.subTest(value=repr(value)):
                data = self.pin_fixture()
                self.record(data, "pasador_diametro")["valor_mm"] = value
                self.assert_rejected(data)

    def test_12_uncertainty_zero_is_not_default_precision(self):
        data = self.pin_fixture()
        self.record(data, "pasador_diametro")["incertidumbre_mm"] = 0
        self.assert_rejected(data)

    def test_13_repetitions_do_not_rewrite_declared_value(self):
        data = self.pin_fixture()
        row = self.record(data, "pasador_diametro")
        row["lecturas_mm"] = [3.16, 3.18]
        before = deepcopy(data)
        self.assertEqual(self.validate(data)["errores"], [])
        self.assertEqual(data, before)
        row["valor_mm"] = 3.2
        self.assert_rejected(data)

    def test_14_duplicate_measurement_ids_are_rejected(self):
        data = self.pin_fixture()
        data["mediciones"] = [deepcopy(self.record(data, "pasador_diametro")) for _ in range(2)]
        self.assert_rejected(data)

    def test_15_duplicate_json_keys_are_rejected_at_every_level(self):
        for raw in ('{"id_captura":"A","id_captura":"B"}',
                    '{"lado":{"valor":"izquierdo","valor":"derecho"}}'):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    self.validator.load_json(self.raw_path(raw))

    def test_16_malformed_json_and_nonfinite_literals_are_rejected(self):
        for raw in ('{"x":1,}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    self.validator.load_json(self.raw_path(raw))

    def test_17_finite_json_exponent_overflow_cannot_enter_geometry(self):
        raw = json.dumps(self.pin_fixture()).replace('"valor_mm": 3.17', '"valor_mm": 1e309')
        self.assert_rejected(self.validator.load_json(self.raw_path(raw)))

    def test_18_large_integer_is_a_validation_error_not_an_exception(self):
        data = self.pin_fixture()
        self.record(data, "pasador_diametro")["valor_mm"] = 10 ** 400
        loaded = self.validator.load_json(self.raw_path(json.dumps(data)))
        self.assert_rejected(loaded)

    def test_19_wrong_enum_types_return_errors_instead_of_crashing(self):
        locations = [
            ("origen",), ("lado", "valor"), ("pareja", "estado"),
            ("seccion_pasador", "forma"), ("danos", "soporte_fijo"),
            ("extraccion", "direccion"), ("mediciones", 0, "estado"),
        ]
        for path in locations:
            for value in ([], {}):
                with self.subTest(path=path, value=value):
                    data = self.pin_fixture()
                    target = data
                    for key in path[:-1]:
                        target = target[key]
                    target[path[-1]] = value
                    self.assert_rejected(json.loads(json.dumps(data)))

    def test_20_invalid_containers_and_nonobjects_are_rejected(self):
        for data in (None, [], True, "ficha", 1):
            with self.subTest(data=data):
                result = self.validate(data)
                self.assertTrue(result["errores"])
                self.assertFalse(result["puertas"]["registro"])
        for key in ("lado", "pareja", "seccion_pasador", "danos", "extraccion", "mediciones"):
            with self.subTest(key=key):
                data = self.pin_fixture()
                data[key] = None
                self.assert_rejected(data)

    def test_21_unknown_keys_invalid_dates_and_approval_are_rejected(self):
        data = self.pin_fixture()
        data["fecha_medicion"] = "2026-02-30"
        self.assert_rejected(data)
        data = self.pin_fixture()
        data["fabricacion_aprobada"] = True
        self.assert_rejected(data)
        data = self.pin_fixture()
        data["colocacion_global"] = {"x": 0, "y": 0, "z": 0}
        self.assert_rejected(data)

    def test_22_cli_returns_json_error_for_malformed_types(self):
        data = self.blank()
        data["origen"] = []
        path = self.raw_path(json.dumps(data))
        run = subprocess.run([sys.executable, "-B", str(self.tmp_path / "validar_ficha.py"), str(path)],
                             text=True, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 2, run.stderr)
        result = json.loads(run.stdout)
        self.assertTrue(result["errores"])
        self.assertFalse(result["puertas"]["registro"])
        self.assertNotIn("Traceback", run.stderr)

    def test_23_cad_original_is_unchanged(self):
        self.assertEqual(self.cad_before, digest_tree(CAD))


if __name__ == "__main__":
    unittest.main(verbosity=2)
