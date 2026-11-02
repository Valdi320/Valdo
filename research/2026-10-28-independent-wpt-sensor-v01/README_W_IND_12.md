# W-IND-12 — Auditoría de retroalimentación y bypass del apagado WPT (28/10/2026)

**Alcance:** robot aspirador NUEVO, abierto y reparable; ámbito propio W de `Valdi320/Valdo`, PR #9. **No** trasplante Xiaomi, carga de litio, batería/BMS, estación, motores, bomba, OOMWOO/PR #79 ni CAD del compañero C. No se copió código de ningún proyecto externo.

## Una mejora concreta

Los dos interruptores en serie del estudio W-IND-08 no garantizan que todo el circuito permanezca eléctricamente aislado si existe alimentación alternativa o conducción inversa. Texas Instruments documenta el bloqueo inverso como una característica específica; los esquemas con interruptores back-to-back pueden bloquear corriente inversa cuando están deshabilitados, pero no basta asumir que dos interruptores arbitrarios cumplen ese contrato. Véase [TIDA-00514 (TI)](https://www.ti.com/tool/TIDA-00514) y [familia load switch (TI)](https://www.ti.com/product-category/power-management/load-switches/overview.html). El [TPS22918 (TI)](https://www.ti.com/product/TPS22918) es un candidato de **conmutación** de las notas W08; no se ha demostrado que por sí mismo aporte protección inversa contractual. No se selecciona como circuito definitivo.

Modelo original `tx_backfeed_screen.py`: grafo de **continuidad DC ideal**, sin valores de tensión/corriente ni fugas. En modo normalmente apagado contempla VIN→A→MID→B→TX, inyección desde conector auxiliar/depuración hacia TX, fuente externa ficticia inyectada en TX, reversa TX→MID→VIN y retorno TX→LOGIC por ESD/GPIO. Los caminos alternativos son **hipótesis de auditoría**, NO un diagrama de un prototipo real ni prueba de que exista conexión galvánica entre receptor y transmisor inductivo. `None` significa dato desconocido y se computa como *posible* para la segunda pasada; nunca como cortado.

```
            SWITCH_A       SWITCH_B
 VIN  ────[ ON/OFF ]─── MID ───[ ON/OFF ]──── TX   (bobina/control hipotéticos)
    ↑                      ↑                  ↑  │
    └──────── REVERSE ? ───┴──── REVERSE ? ────┘  └── GPIO/ESD ? ── LOGIC
                                               ↑
 AUX/DEBUG ───────────── bypass no verificado ──┘
 EXT_TX_source ───────── inyección ficticia ────┘
```

`PathState` distingue `CONFIRMED_IN_MODEL`, `POSSIBLE_UNVERIFIED` y `NO_PATH_IN_MODEL`. Este último **no** significa corriente cero, FOD real, diseño seguro ni autorización. Conmutación correcta y ausencia de caminos alternativos son **requisitos diferentes**. Un único corte soldado no alimenta TX desde VIN en el modelo si el segundo permanece abierto; dos soldaduras sí. Una ruta auxiliar puede puentear ambas. Inyección externa con reversa de los dos cortes puede retroalimentar VIN, y una conexión GPIO podría retroalimentar una línea lógica aunque VIN no reciba energía. Los casos de tensión inversa, capacidad de corriente y daño térmico necesitan esquemático/medición independiente.

### Resultados deterministas (software sintético)

| Escenario hipotético, orden OFF | Trayectoria | Resultado | Decisión |
|---|---|---|---|
| Cortes sanos, sin fuente auxiliar | VIN→TX | `NO_PATH_IN_MODEL` | No aprobar; diseñar y medir |
| A soldado, B abierto | VIN→MID, pero no VIN→TX | `NO_PATH_IN_MODEL` hasta TX | Vigilancia del nodo MID |
| A y B soldados | VIN→TX | `CONFIRMED_IN_MODEL` | Bloquear |
| AUX alimentado, bypass desconocido | AUX→TX | `POSSIBLE_UNVERIFIED` | Bloquear hasta caracterizar |
| AUX alimentado, bypass conductor | AUX→TX | `CONFIRMED_IN_MODEL` | Bloquear |
| Fuente externa ficticia en TX, bloqueo inverso desconocido | EXT_TX→VIN | `POSSIBLE_UNVERIFIED` | Bloquear hasta caracterizar |
| Fuente en TX, ambos caminos inversos conductores | EXT_TX→VIN | `CONFIRMED_IN_MODEL` | Bloquear |
| Fuente en TX, ambos cortes inversos bloqueados, ESD/GPIO conectado | EXT_TX→LOGIC | `CONFIRMED_IN_MODEL` | Bloquear |

**Requisito medible de siguiente fase:** demostrar eléctricamente (no inferir de esta simulación) el OFF a la entrada, nodo intermedio, etapa TX, rail de control y puerto de servicio; repetir con fallo simple, fuente auxiliar presente y fuente externa *de banco* ficticia, usando tensión/corriente limitadas y sin batería. Respetar la parada local independiente de radio/FOD, sondas térmicas y desconexión efectiva. Cualquier ruta desconocida es un bloqueo, no una aprobación por defecto. No conectar fuentes sin un procedimiento de seguridad autorizado por el propietario.

## Evidencia reproducible

Python 3.10+ estándar, sin instalaciones ni hardware. Desde la carpeta de este informe:

```bash
python3 -m py_compile tx_backfeed_screen.py test_tx_backfeed_screen.py
python3 -m unittest -v test_tx_backfeed_screen
python3 tx_backfeed_screen.py
```

**Medición propia:** 23/23 pruebas Python sintéticas PASS en entorno aislado de desarrollo (no en el robot). En una batería de 3×3 estados de dos cortes y cuatro combinaciones de presencia de alimentaciones, todos los resultados siguen `hardware_approved=False`. Pruebas negativas inyectan soldaduras, bypass confirmados o desconocidos, ausencia de fuente, reversa y retroalimentación GPIO; la clasificación marca los caminos. **No** se midió ningún miliamperio, eficiencia, temperatura, frecuencia, perturbación EMI, metal, offset, voltaje ni potencia. CI de GitHub debe revisarse tras publicar: sin afirmación adelantada de PASS remota.

## Decisión de arquitectura y BOM

| Problema | Decisión provisional | Limitación |
|---|---|---|
| Apagado TX | Dos interrupciones locales, normalmente OFF, y auditar todas las fuentes paralelas y reversas | Sin esquemático ERC ni selección eléctrica |
| RX sensor bajo consumo | Piloto hipotético 5 V, 0,4 W medio, 1,5 W pico **solo sensor** | Radio, picos, regulación y pérdidas reales desconocidos |
| Carga de estación | Fuera del alcance; batería y BMS desconectados | No hay controlador de carga ni FOD certificados |
| Datos RF | ESP-NOW u OpenThread, con ACK de aplicación, CRC, secuencia, timeout, autenticación y recuperación | Ninguna radio energizada; paquetes no actúan como parada crítica |
| WISP RFID | Solo microsensores si justificado | Lector/coste/energía no validados |
| Motor/bomba | No aplicar WPT por defecto | Consumo y pérdidas no medidos |
| Alternativa cableada | Conector desmontable como comparación | Dueño C valida mecánica; no atribuir cables ahorrados |

[BOM_W_IND_12.csv](BOM_W_IND_12.csv) contiene el desglose pendiente. Diotronic es **auxiliar**, nunca compra automática ni dependencia: referencias, precio final con IVA, existencia local y cantidades mínimas sin verificar; cotejar con TME/Mouser/DigiKey. TI TIDA-00514 demuestra un **precedente de fabricante**, no una licencia de copiar placa ni una cualificación de nuestro diseño. No se asume que TPS22918, eFuse y reverse block sean equivalentes.

## Revisión externa y aislamiento de compañeros

Se leyeron antes de trabajar `00_DECISION_20261028_NO_TRASPLANTE_X20.md`, `19-alternativas-abiertas-para-robot-independiente.md`, D22/contrato, coordinación W/C, `VALDO_OOMWOO/LEEME_PRIMERO.md` y `adaptacion/contratos/WPT_DATOS_V01.md`. Última revisión API GitHub de ramas/commits/PR del 28/10/2026:

- **mark-belbin/simple-wireless-power**, autor mark-belbin, GPL-3.0, `master` `7c7858c0dd7040801b6f191df1396115560218f0` = pin; PR #1 cerrada. Solo referencia conceptual, sin firmware/PCB GPL reutilizado.
- **wisp/wisp5-hw**, autoría wisp, BSD-2-Clause, `master` `08332bc398aa3350d351ef2aaac163f8007cffda` = pin; PR #1 cerrada.
- **wisp/wisp5**, autoría wisp, BSD-2-Clause, rama `640kHz` `604eee2dffaeba3a270de61cf3dae887a33309c2`, diverge del pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` (+68/-11); PR #40 abierta. No fast-forward.
- **espressif/esp-now**, autoría espressif, Apache-2.0, `master` `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` = pin; PR #153 cerrada. No código integrado.
- **openthread/openthread**, autoría openthread, BSD-3-Clause, `main` `995eee810c2707cdf676f7097960ce066935b2c1` (+8/-0 respecto a pin `7009584dadc20cf20c20a6062f357dd572ba6885`); PR #13812, #13811 y #13810 abiertas, no asumir merge. No código integrado.
- **OOMWOO** oficial `makerspet/oomwoo main` `1c2bd43abcf74288afcf2d8b64514cc325f9b905`, PR #79 **cleaning-jobs** ajena y abierta; VALDO PR #9 propia HEAD previo `bce0d1188a6920a771df4405ef1996b1fbdc57db` (W-IND-11). Codex mantiene parches y ramas de apoyo A01–A23, incluidas A20 cuentas de reposo y A21 validación de journal, que **NO** se copiaron ni atribuyeron. `master` local del usuario tiene cambios ajenos sin confirmar y no se toca.

**Siguiente paso, no ejecutado:** esquema KiCad original y revisión ERC de carriles VIN/MID/TX/LOGIC/servicio con componentes reales y cortes normalmente OFF, ensayos pasivos de rutas y especificación de fuga; solamente después, banco aislado resistivo con autorización expresa y protección FOD/térmica independientes. Ninguna compra, impresión, soldadura, batería, firmware o maquinaria intervenida.
