# 08 — Modelo de datos, digital thread y contratos de confianza

**Descubrimiento de arquitectura:** la fábrica personal no necesita solo un «cerebro IA»; necesita **datos técnicos coherentes que sobrevivan años** y puedan transferirse entre escáner, diseño, fabricación, robot, estación, segundo robot y futuro software.

## 1. Estructura de información del proyecto

**[P]** Cinco colecciones versionadas y enlazadas:

1. **Objetos y ensamblajes**: `object_id`, revisión CAD, piezas, fijaciones, tolerancias, cargas, materiales observados/inferidos, archivos paramétricos y medidas.
2. **Materiales y lotes**: origen, clasificación, usos permitidos, ciclos térmicos, propiedades medidas, reciclabilidad/compostabilidad verificada y advertencias.
3. **Máquinas/módulos**: `module_id`, interfaz mecánica/eléctrica, firmware firmado, versión, limitaciones de carga, calibración, mantenimiento, compatibilidad y repuestos.
4. **Acciones y misiones**: pasos con precondiciones, autorizaciones, sensores y herramientas; sucesos, resultado y compensaciones.
5. **Ensayos y evidencia**: archivos inmutables de captura, fecha, instrumentos, calibración, PASS/FAIL, anomalías e identidad del modelo de IA.

**[D]** Las familias de estándares [STEP / AP242](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/step-nist) para CAD/PMI y [QIF](https://www.nist.gov/publications/end-end-quality-information-framework-qif-technology-survey) para medición e inspección forman parte del «hilo digital» industrial. **[P]** FDAA puede utilizar formatos abiertos simples inicialmente y mapear a estos estándares cuando lo requiera la complejidad, sin inventar una equivalencia automática.

## 2. Ejemplo de ficha de componente (esquema conceptual, NO estándar legal)

```json
{
  "schema_version": "fdaa-part-0.1",
  "part_id": "F-00034",
  "revision": 3,
  "source": {"type": "reverse_engineered", "original_object_id": "OBJ-12"},
  "geometry": {
    "native_cad_uri": "cad/F-00034.fcstd",
    "step_uri": "cad/F-00034.step",
    "units": "mm",
    "critical_dimensions": [
      {"name": "hole_diameter", "value": 5.01,
       "measurement_uncertainty": 0.04, "evidence_id": "M-021"}
    ]
  },
  "material": {
    "family": "polymer",
    "grade": "UNKNOWN",
    "origin": "inferred",
    "allowed_use": "non-critical prototype only",
    "lot_id": "LOT-018"
  },
  "fabrication": {"process": "FFF", "recipe_rev": 2},
  "verification": {"status": "pending", "test_plan": "T-02"},
  "repair": {"fasteners": [], "tools": [], "disassembly_plan_uri": null},
  "evidence": ["M-021"],
  "unknowns": ["actual polymer grade", "fatigue life"]
}
```

**Las rutas y números son ficticios e ilustran el contrato**, no mediciones ni archivos existentes. En producción, campos y tipado deben normalizarse; hashes y firmas deben cubrir archivos asociados.

## 3. Estados seguros de una operación física

**[P]** Máquina de estados de acción:

```text
PROPOSED → CHECKED → HUMAN_AUTHORIZED? → RESERVED
         → ENERGY_SAFE → EXECUTING → VERIFYING → ACCEPTED
                              └─[abnormal]─→ STOPPED → RECOVERY_REVIEW
```

Cada paso recibe un **identificador único de misión** y referencia a:
- modelo de entorno/version y fecha;
- descripción geométrica de objeto, robot y herramienta;
- permiso humano o política de tarea preaprobada;
- límites físicos declarados y sensores requeridos;
- criterios de aceptación y pruebas posteriores;
- estado del gemelo digital antes/después;
- resultado medido, no un simple mensaje «hecho».

**No** hacer depender autorización de otra respuesta generada por el mismo modelo sin verificación externa. El controlador de seguridad valida límites y puede rechazar cualquier acción.

## 4. Contratos de hardware entre robots y estación

**[P]** Para un módulo reemplazable:

| Campo | Motivo |
|---|---|
| ID/versión y compatibilidad | no instalar recambio erróneo |
| masa y centro de gravedad | manipulación y soporte seguro |
| envolvente CAD y espacios de herramienta | reparar con el otro robot |
| agarres y puntos de inmovilización | rescate con robot apagado |
| protocolo de potencia y señales | no dañar controladores |
| estado de energía/batería y enclavamiento | mantenimiento aislado |
| posición de calibración y autoprueba | comprobar que está reparado |
| procedimiento de sustitución reversible | auditoría y rollback |
| límites de operación y fallos observados | evitar que reincida la avería |

**Estandarizar pocas interfaces de herramientas/cables** dará más retorno que pretender imprimir todas las piezas. Siempre definir cargas, llaves mecánicas antierror y modelos de repuesto.

## 5. Contratos entre IA y herramientas científicas

Cada petición estructurada tendrá:
- **entrada verificada** (modelo, versión, unidades y límites);
- **resultado medible** (CAD, trayectoria, curva par o señal);
- **advertencias del simulador/verificador**;
- **estado PASS/FAIL/UNKNOWN**;
- **recursos consumidos** (tiempo, VRAM/RAM/energía);
- **próximo ensayo** si no puede concluirse.

**Política anti-alucinación:** si el modelo no identifica material con datos medidos, registrar `UNKNOWN`, ofrecer medidas adicionales y no autorizar fabricación crítica. Misiones de riesgo mayor requieren aprobación humana y procedimientos específicos.

## 6. Almacenamiento local, privacidad y fiabilidad

- Índice local de documentos con búsqueda sobre contenido, metadatos y procedencia; archivos originales hashados.
- Historial de mantenimiento con fotos/mediciones **mínimas necesarias** y control granular de acceso.
- Copias redundantes y restauración ensayada; backup offline de datos esenciales y credenciales de recuperación.
- Git para documentación/CAD textual/firmware, almacenamiento de objetos para imágenes y datos grandes con verificaciones de integridad.
- Versiones fijadas de software, firmware y modelos, con capacidad de volver a versión segura.
- Retención de datos por política; no registrar permanentemente vídeo de estancias sin necesidad/autorización.
- Identidad y permisos de robot A, B, estación, herramientas e IA local; credenciales distintas.

## 7. Digital Product Passport y futuros estándares

**[D]** El marco [ESPR (UE) 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng) define pasaportes digitales de producto basados en requisitos de producto que serán concretados por regulación delegada. La [Comisión publica referencias de estandarización DPP](https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/digital-product-passport-dpp_en).

**[P]** Nuestro pasaporte interno anticipa campos útiles (componentes, reparación, origen, material, manuales, desmontaje) pero **no declara automáticamente conformidad con ninguna regulación sectorial o norma de pasaporte**.

## 8. Primeros ensayos de integridad de datos

1. El CAD versión N fabrica una pieza y registra tolerancia; cambiar parámetro obliga a crear revisión N+1.
2. Un robot informa de sustitución pero falta lectura eléctrica/táctil: sistema marca **VERIFYING**, no SUCCESS.
3. Un manual propone acción contradictoria con controlador/limitaciones: **rechazo** y registro.
4. Copia del inventario incompatible de módulos en A y B: detecta incompatibilidad antes de atornillar.
5. Caída de red: registro local continúa y ninguna misión peligrosa se inicia.
6. Corrupción parcial de imagen/dataset: hashes revelan fallo y el sistema no toma decisiones basadas en pruebas corruptas.
7. Dos robots actualizan misma pieza: control de versiones/identidad evita doble consumo o sustitución contradictoria.

**Fuentes:** [NIST STEP](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/step-nist), [NIST QIF](https://www.nist.gov/publications/end-end-quality-information-framework-qif-technology-survey), [ESPR](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng), [CRA](https://digital-strategy.ec.europa.eu/es/policies/cra-reporting), [LeRobot](https://github.com/huggingface/lerobot).
