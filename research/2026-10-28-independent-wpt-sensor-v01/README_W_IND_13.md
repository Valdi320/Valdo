# W-IND-13 — Fallo de causa común en los dos cortes de potencia WPT (29/10/2026)

**Solo ámbito W del robot NUEVO** y PR #9. No trasplante OEM Xiaomi, litio, estación ni modificación OOMWOO. Código original, sin copiar fuentes ajenas.

## Mejora real y falsable

Dos interruptores en serie NO forman dos barreras independientes si comparten un ENABLE o un latch que pueda quedar alto. El modelo original `tx_common_cause_audit.py` enumera los conjuntos mínimos de fallos que permiten alimentar el TX estando ordenado OFF. Es complemento de W-IND-12 (caminos inversos/auxiliares), no un esquema eléctrico, KiCad ERC ni una demostración de seguridad física.

| Topología hipotética, VIN presente | Conjuntos mínimos *sin puente de PCB ni AUX, únicamente para comparar mandos* |
|---|---|
| Dos cortes, un ENABLE común | **1 fallo**: driver común alto; alternativamente dos cortes soldados |
| Dos ENABLE realmente independientes | **2 fallos** en el catálogo considerado, cuatro parejas posibles (controles o soldaduras) |
| Dos ENABLE pero latch común | **1 fallo**: latch único alto; o las cuatro parejas dobles |

**Contraejemplos que permanecen:** un puente conductor VIN→TX en la PCB, o una alimentación auxiliar que evite ambos cortes, reintroducen caminos con un único fallo aunque los ENABLE estén separados. Aislamiento de estos caminos, fallos comunes del componente y polaridad real son desconocidos. `hardware_approved=False` en todos los resultados.

### Contrato eléctrico pendiente de implementar

VIN_5V -> CORTE_A -> MID -> CORTE_B -> TX_5V -> BOBINA. EN_A y EN_B deben proceder de cadenas locales verdaderamente independientes y normalmente OFF; no compartir driver/latch como única defensa. FOD, temperatura y sobrecorriente deben actuar físicamente sin depender de radio, CPU, ROS2, ESP-NOW ni OpenThread. AUX/DEBUG no debe crear rutas VIN o GPIO/ESD a TX. Comprobar el estado OFF al arrancar, con brownout y pérdida de alimentación de supervisores. La alimentación de batería y dock sigue completamente separada.

## Evidencia

- `tx_common_cause_audit.py`: enumerador original de conjuntos mínimos de fallos hasta tres eventos, rutas VIN/AUX, catálogo validado.
- `test_tx_common_cause_audit.py`: **19/19 pruebas PASS en sandbox aislado**: causa común, EN separados, latch, inyección AUX/PCB, monotonicidad, entradas mal formadas y denegación permanente de aprobación.
- Reproducir: `python3 -m py_compile tx_common_cause_audit.py test_tx_common_cause_audit.py && python3 -m unittest -v test_tx_common_cause_audit && python3 tx_common_cause_audit.py` desde la carpeta W del proyecto.
- CI integra las pruebas y se verifica tras push. La simulación no equivale a medición ni prueba de seguridad.

## Matriz de decisión y límites

| Problema | Decisión | Bloqueo físico |
|---|---|---|
| Primer sensor | Hipótesis 5 V, 0,4 W media, 1,5 W pico SOLO sensor | Pérdidas y radio sin medir |
| Cortes TX | **Rechazar el ENABLE compartido como única defensa** | Requiere esquema pin a pin, datos de dispositivo, PCB, FOD y térmica |
| Dock de carga | Independiente del piloto sensor | Batería/BMS desconectados |
| Datos | ESP-NOW u OpenThread con ACK de aplicación, CRC, secuencia, timeout, autenticación y recuperación | Nunca autorizar parada crítica por radio |
| WISP | Solo microsensores justificados | Lector/energía/coste sin caracterizar |
| Motores y bombas | No WPT por defecto | Consumos/desgaste desconocidos |
| Alternativa | Conector reparable reversible | Mecánica corresponde a C; ninguna eliminación de cable afirmada |

## Fuentes y revisión de autores / HEAD / PR (29/10/2026)

- `mark-belbin/simple-wireless-power` GPL-3.0: `master` 7c7858c0dd7040801b6f191df1396115560218f0 = pin; PR #1 fusionada en 2021. Solo referencia, nada copiado.
- `wisp/wisp5-hw` BSD-2-Clause: `master` 08332bc398aa3350d351ef2aaac163f8007cffda = pin; PR #1 fusionada 2015.
- `wisp/wisp5` BSD-2-Clause: `640kHz` 604eee2dffaeba3a270de61cf3dae887a33309c2; contra pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b divergencia **68 ahead / 11 behind**; PR #40 abierta. No fast-forward.
- `espressif/esp-now` Apache-2.0: `master` c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin; PR #153 cerrada sin merge. Ningún código integrado.
- `openthread/openthread` BSD-3-Clause: `main` 51aa078ee4fe1ad803bc83ca7b372e7ab62120f3, **9 ahead / 0 behind** contra pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13812, #13811, #13810 abiertas. No se atribuyen como merged.
- OOMWOO `makerspet/oomwoo main` 1c2bd43abcf74288afcf2d8b64514cc325f9b905; PR #79 cleaning-jobs ajena, abierta. VALDO PR #9 W estaba en 755f615f2962c2858dc5f4e6e5ff985b6dfd186c; apoyo Codex W12 A29 y posteriores siguen en repo propio sin copiarse.
- Fabricante: https://www.ti.com/tool/TIDA-00514 (bloqueo inverso con elementos back-to-back, no aval de nuestro circuito). https://www.ti.com/product/TPS2080 (entradas EN independientes en dispositivo dual; no prueba separación de fallos internos).

Se leyeron antes de intervenir los dos documentos maestros de arquitectura/alternativas, D22 y su contrato, coordinación W/C de 2026-10-27, VALDO_OOMWOO/LEEME_PRIMERO.md y WPT_DATOS_V01.md. El repositorio local master está sucio por trabajo ajeno: **no se tocó**. No compras, impresión, soldadura, hardware, firmware ni nuevas licencias incorporadas.

## BOM / Diotronic

`BOM_W_IND_13.csv` separa los dos cortes, dos canales EN, FOD, sensores térmicos, protección de corriente, AUX y PCB. **Ningún SKU/prcio/stock real verificado**; seleccionar componentes tras circuito y datasheets. Diotronic auxiliar para pasivos y repuestos, nunca como dependencia. Comprobar referencia, precio IVA, MOQ, stock por sucursal y total puesto en casa frente a TME/Mouser/DigiKey antes de comprar.

**Siguiente hito:** esquema KiCad con pines, dominios de alimentación, EN/ESD y rutas inversas reales; ERC/SPICE + inspección de caminos de causa común. Después, solamente con autorización separada, prueba resistiva de baja tensión aislada con FOD/termometría independientes. **No se aprueba hardware.**
