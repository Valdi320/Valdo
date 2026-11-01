# W-IND-95 — contrato de reloj estricto para telemetría inalámbrica (01-11-2026)

**Ámbito:** robot VALDO nuevo, independiente, abierto, reparable. Código Python propio W; no reutiliza fuentes/CAD externos, no modifica Xiaomi, OOMWOO, PR #79, CAD ajeno ni estación/batería. Sin hardware, compras ni pruebas RF.

## Defecto real corregido

En el HEAD previo 05a9eec74eb8586fe397f60b586d46ad112931b9, AckTracker.retry() aceptaba sin validar el tipo de now_ms. Un NaN hace falsas las comparaciones de reloj, permitiendo **emitir una retransmisión con reloj inválido** y registrar NaN en el estado interno. None/string podían causar TypeError y cortar el bucle. start() y accept_ack() aceptaban booleanos como marcas de tiempo (bool es subclase de int en Python); commission_local() del receptor aceptaba NaN; fresh(True) podía certificar falsamente frescura.

**Cambio mínimo:** exigir el tipo exacto int en arranque, retransmisión, ACK, comisionado local y consulta de frescura. Los fallos de tiempo en retransmisión/ACK descartan la transacción pendiente y suman una incidencia, sin emisión ni ACK; comisionado inválido lanza ValueError antes de modificar el receptor. Con tiempos válidos siguen idénticos los intervalos de 60 ms, caducidad de 240 ms, tres intentos como máximo y frescura de 250 ms.

No se alteran las tramas de 22 bytes, CRC-16, HMAC/AEAD opcional ni la autenticación real del enlace. Un indicador de autenticación de prueba True no prueba identidad criptográfica. Esta barrera NO controla motores, bomba, escobillas, batería, FOD ni corte eléctrico crítico.

## Evidencia y reproducción

Ejecutar desde research/2026-10-28-independent-wpt-sensor-v01:

    python3 -m unittest -v test_w_link

Nueve pruebas nuevas TestClockBoundary cubren NaN, infinito, bool, float, strings, None y objetos; no emisión, no ACK falso, estado de comisionado intacto, frescura estricta y retransmisiones válidas conservadas. Ejecutarlas junto a las regresiones antiguas en la CI existente wpt-sensor-v01.yml; w-ind-60 y w-ind-61 reaccionan a cambios de w_link.py. Etiqueta de evidencia: **SOFTWARE_SINTETICO**, no radio ni medición física. CI, SHA y PR se verifican tras publicar, nunca se presentan conteos previstos como observados.

## Matriz técnica resumida

| Ruta | Decisión | Evidencia / límite |
|---|---|---|
| Validar reloj entero estricto | Adoptar | Defecto software reproducible, sin nuevos componentes |
| Comparaciones implícitas NaN/float/bool | Rechazar | Permiten retries o ACK falsos, excepciones |
| Energía NFC/WISP para microsensor | Investigar solo si carga real diminuta | Faltan curvas fuente RX, lector, arranque y radio |
| Potencia WPT sencilla sin control | No aprobar | Faltan FOD, térmica y corte autónomo |
| WPT regulada para módulo | Candidata | Sin medidas offset, EMI, eficiencia, mantenimiento y protección |
| Carga WPT de estación | Subsistema aparte bloqueado | No tocar litio/BMS/carga, sin proceso autorizado |
| ESP-NOW | Candidato a datos | App ACK auténtico, CRC, secuencia, timeout, recuperación y privacidad pendientes de hardware |
| OpenThread | Alternativa RF | Stack/topología/consumo a comparar, no integrar ambas por defecto |
| Cable sustituible | Base económica y segura comparativa | No retirarlo sin pruebas de coste total y fiabilidad |

## Auditoría de autores, ramas y revisiones (consultado 01-11-2026)

Pines registrados 28-10-2026 en el documento maestro local 19-alternativas-abiertas-para-robot-independiente.md; no se copia código, CAD ni licencia:

- mark-belbin/simple-wireless-power, GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0, sin cambio; curvas de gap son del autor. https://github.com/mark-belbin/simple-wireless-power
- wisp/wisp5-hw, BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda, sin cambio. https://github.com/wisp/wisp5-hw
- wisp/wisp5, BSD-2-Clause, HEAD por defecto 640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2, distinto de master fijado d978a6978ad23ccd6c44dd55430973b04a3d4a9b; divergencia, no interpretar como sustitución automática. https://github.com/wisp/wisp5
- espressif/esp-now, Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5, sin cambio; el ACK de radio no es ACK aplicativo. https://github.com/espressif/esp-now
- openthread/openthread, BSD-3-Clause, main c6872259f4194fb76c7d333bda209343e8c88e71, 21 commits posteriores al pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13800 MLE router no es pertinente a nuestro validador. https://github.com/openthread/openthread/pull/13800
- OOMWOO oficial makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df; firmware fd8689f3e3f7bcd0dcc35725be4a48cd9fcc8596 y PCB ac8ac0b52254582be3acda9d3fddfd06cbbabd4f (1 Nov); adaptación VALDO_OOMWOO no editada. https://github.com/makerspet/oomwoo

El árbol local Valdo pertenece a una rama sucia de otro compañero y no se utilizó. Única publicación objetivo: PR propia #9 rama w/independent-sensor-wpt-link-20261028. Automatización OOMWOO desactivada; tareas OEM apagadas.

## BOM, límites y siguiente actuación

**Coste eléctrico incremental: 0 EUR** en hardware, por ser corrección de software; tiempo de desarrollo/CI no valorado. Diotronic Zaragoza AUXILIAR para pasivos y prototipos, nunca proveedor obligatorio: stock, MOQ, precio final IVA y comparación TME/Mouser/DigiKey pendientes; no se compra nada. El circuito KiCad W18 sigue bloqueado: ERC físico en CI 1 etiqueta colgante + 2 pines de alimentación sin driver, 3 errores totales. No declaración de seguridad eléctrica, rendimiento RF ni fiabilidad a largo plazo.

**Punto dulce:** cerrar este fallo software verificable; el siguiente retorno relevante precisa un banco aislado seguro, autorizado, con carga resistiva, sin litio/BMS/estación/motores, midiendo potencia lector/RX, desplazamiento, calor/FOD, corte independiente y ACK real frente a cable reparable. Más escenarios sintéticos no sustituyen esos datos.
