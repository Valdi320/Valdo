# W-IND-100 — La consulta de vigencia enclava el timeout del sensor

Fecha: 2026-11-01. Alcance: robot abierto nuevo, **solo telemetría experimental** de la rama W propia, sin hardware. Baseline: `7dbb4bf4678a5fcc9664950e32823f8c6307c79e`. Esta corrección no modifica dock, motores, batería, BMS ni estación Xiaomi.

## Defecto e impacto
`ModuleReceiver.fresh(now_ms)` devolvía `False` una vez vencido `timeout_ms`, pero no activaba `latched_fault`. El estado del enlace dependía de que otro consumidor invocase `tick()` o `receive()`. El contrato del receptor exige que una observación de caducidad obligue a un rearme local: no basta un booleano temporalmente falso. Un monitor de solo lectura podía mostrar **datos caducados y, simultáneamente, ausencia de fallo enclavado**.

Secuencia sintética anterior: `commission_local(123,0)`, recepción válida `seq=1` en 10 ms y `fresh(261)`: resultado `False` pero `latched_fault=False`. La nueva versión conserva `False` y además enclava `latched_fault=True`. El límite es **estricto**: 260 ms es válido para `timeout_ms=250`; 261 ms es caducado. Ni un mensaje posterior ni un ACK duplicado recuperan la sesión; requiere `commission_local(124,...)` autorizado con época nueva. No cambian CRC, trama de 22 bytes, cifrado, secuencias ni parámetros temporales.

## Pruebas reproducibles
Desde `research/2026-10-28-independent-wpt-sensor-v01`:
```sh
python3 -B -m unittest -v test_w_link.TestReceiverDeadlineLatchW100
python3 -B -m unittest -v test_w_link
```
8 regresiones nuevas: frontera temporal, primer timeout sin tick, nueva lectura, intento de rearme con la misma sesión, rearme local válido, duplicados, tiempos inválidos y ausencia inicial de lectura. Los casos son digitales/deterministas; consultar GitHub Actions de la PR #9 para el resultado ejecutado del commit. Una revisión de código por sí sola no cuenta como prueba PASS.

## Tres problemas separados y decisión
| Problema | Alternativas / criterio | Decisión |
|---|---|---|
| Estación de carga | Dock de contactos reparable vs WPT regulada con FOD, corte térmico autónomo, offset, humedad y EMI | **Sin selección:** BMS y batería desconectados, 0 pruebas físicas |
| Módulos desmontables | Cable retenido reparable vs acoplamiento WPT abierto vs regulado | Pilotar solo sensor ficticio 5 V, 0,4 W promedio / 1,5 W pico; WPT **no aprobada** hasta medir consumo real y pérdidas |
| Datos | Cable vs ESP-NOW cifrado con ACK de aplicación, CRC, secuencia y timeout vs OpenThread 802.15.4 | Corrección de timeout aplicable a lógica de datos independiente del medio; sin autenticación criptográfica real ni radio instalada |

WISP5 queda limitado a referencia de microsensores RFID con su propio balance de energía: no sustituye el suministro continuo de motores/bombas.

## Procedencia y límites
No se incorpora código externo. Revisados repositorios propios de mark-belbin (GPL-3.0, master `7c7858c0`), WISP hardware (BSD-2-Clause, master `08332bc3`), WISP firmware (BSD-2-Clause, rama **640kHz** `604eee2d`; divergencia +68/-11 del pin `d978a697`), Espressif ESP-NOW (Apache-2.0, master `c3b5f9be`) y OpenThread (BSD-3-Clause, main `c6872259`, +21 frente `7009584d`). Revisadas sus PR/changelog de creadores. OOMWOO oficial `f01a1b29` y PR #79 cleaning-jobs quedan intactos. Esta rama es propiedad de VALDO/W, no del upstream ni de C.

Fuentes: [proyecto Belbin](https://github.com/mark-belbin/simple-wireless-power), [WISP5 HW](https://github.com/wisp/wisp5-hw), [WISP5 FW](https://github.com/wisp/wisp5), [ESP-NOW](https://github.com/espressif/esp-now), [OpenThread](https://github.com/openthread/openthread). Documento base: `19-alternativas-abiertas-para-robot-independiente.md` y contratos D22 y WPT_DATOS_V01. Contrato local de rearme verdadero requiere NVM duradera, autenticación de transporte y monotonicidad de reloj fiable: aquí **solo se emula**.

Coste incremental físico: **0 €**. No se instala módulo, no se compra, no se suelda ni se energiza. Diotronic es proveedor auxiliar: precio IVA, stock local y cantidades mínimas de cualquier hardware de futura BOM **pendientes de verificar** frente a TME/Mouser/DigiKey. `W18` ERC conserva tres infracciones conocidas; no se aprueba ningún circuito para fabricar o alimentar.

Siguiente paso: autorización separada y protocolo de seguridad antes de caracterizar alimentación NFC/WPT con carga resistiva aislada; medir entrada TX, energía útil, temperatura, separación/desalineación, FOD y corte independiente. No extrapolar pruebas lógicas a la seguridad de litio.
