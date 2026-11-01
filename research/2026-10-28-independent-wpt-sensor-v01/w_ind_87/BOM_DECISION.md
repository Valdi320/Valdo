# W-IND-87 — matriz de decisión, BOM y auditoría de propietarios (1 nov 2026)

## Alternativas para el robot abierto

| Ruta | Potencia / datos | Riesgos y durabilidad | Decisión |
|---|---|---|---|
| **Cable sustituible retenido** | Referencia eléctrica de menor complejidad, coste por determinar | Ciclos de desmontaje y cableado a validar por C | **BASELINE** |
| ST25DV04KC NFC harvesting | Solo puntos de autor en mW; datos ISO15693 no equivalen a ACK app | EH sin regular, débil campo, sincronía no garantizada, falta FOD/ESR/corte/lector | **Microsensor esporádico condicional** |
| WPT regulada + ESP-NOW | Potencia y datos por canales independientes; RX 1–20 mW **sin medida propia** | FOD/térmico/EMI y corte independiente no cualificados | No elegida |
| WPT regulada + OpenThread | Igual separación; consumo RF / red pendientes | Contrato aplicación ACK/seq/timeout/cifrado/recuperación por medir | No elegida |
| WISP5 RFID | Sensores de energía mínima sin batería | Lector y herramientas particulares; no motores ni funciones críticas | Secundaria |
| Simple Wireless Power | Autor declara hasta 100 W/81,3% **en otro prototipo**, irrelevante a mW | Sin FOD/cortes autónomos aprobados; GPL-3.0 si se copiara fuente | Solo referencia |
| Estación/litio/BMS/motores/bombas | Escalas distintas a datos ST | Seguridad independiente y autorización ausente | Fuera del hito |

## BOM exploratoria, NO COMPRABLE

Diotronic **solo auxiliar**; no se ha confirmado stock en tienda Zaragoza, coste final de envío ni precio en caja. IVA español calculado al 21%; el catálogo no es entrega garantizada.

| Referencia/uso | Diotronic / alternativa | Precio visible IVA, MOQ | Disponibilidad/equivalencia |
|---|---|---|---|
| **ST25DV04KC-IE8S3 SO8N**, etiqueta EH | Diotronic sin ficha/stock local confirmado; [Farnell ES 3972494](https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494) | Catálogo **0,926€ sin IVA = 1,12046€ IVA**, MOQ1 | Existencias online anunciadas, sin entrega efectiva verificada. El SO8N es más reparable que chip ultrapequeño. **No incluye lector ni antena** |
| **ST25DV04KC-IE8S3 SO8N** | Diotronic pendiente; [RS ES 248-7495](https://es.rs-online.com/web/p/modulos-rf/2487495) | **5,83€ IVA/5**, MOQ5 | Distribución externa, no stock Zaragoza; portes pendientes |
| **ST25DV04KC-IE8C3 UFDFPN**, **huella distinta** | Diotronic pendiente; [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/ST25DV04KC-IE8C3/16359660), [Mouser ES](https://www.mouser.es/es/ProductDetail/STMicroelectronics/ST25DV04KC-IE8C3?qs=QNEnbhJQKvY88dTRgPa5uw%3D%3D) | DigiKey 1,11€ sin IVA ≈**1,3431€ IVA** MOQ1; Mouser 1,02€ sin IVA ≈**1,2342€ IVA** MOQ1 | Referencias informativas; **NO intercambiable por SO8N**, stock/portes reales pendientes |
| Lector NFC ISO15693 13,56MHz y antena | Diotronic / TME / Mouser / DigiKey / fabricante | **Sin SKU**; precios/MOQ/stock pendientes | Bloqueo de energía TX, detección EH y coste instalado |
| Condensador efectivo + regulador/cold-start | Diotronic pasivos si equivalentes; especialistas para críticos | Sin SKU ni precio/stock, **C mínima ideal 1058 µF**, no C nominal | ESR, temperatura, fuga y margen sin verificar |
| Supervisor, corte normalmente OFF, térmica/FOD | Distribuidor trazable (Diotronic auxiliar si especificaciones demostradas) | Sin SKU ni coste | Requiere fichas, tiempo máximo, respuesta a alimentación caída y prueba autónoma |
| Cable/mazo reemplazable | Diotronic/TME/Mouser/DigiKey | Pines/longitud/ciclos/MOQ/precio pendientes | Baseline de mantenimiento, no inferir eliminación de cables |

No considerar 0€ el lector, bobinas, PCB, cable/mecánica, transporte, servicio, consumo del lector, protecciones, mantenimiento o pruebas. **No se han comprado piezas.**

## Revisión HEAD + rama + PR/changelog de los autores

Comparación exacta con SHAs registrados en el documento local `19-alternativas-abiertas-para-robot-independiente.md`, realizada mediante repositorio y referencias GitHub el **1/11/2026**. Todas las fuentes de autores se mantienen intactas.

| Dueño / licencia | HEAD rama | Comparación y novedades revisadas |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | `master` `7c7858c0dd7040801b6f191df1396115560218f0` | Igual a 19; último README junio2021, PR #1 cerrada |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause | `master` `08332bc398aa3350d351ef2aaac163f8007cffda` | Igual; sintonía de antena de 2017, PR #1 cerrada |
| [wisp/wisp5](https://github.com/wisp/wisp5/tree/640kHz) BSD-2-Clause | **`640kHz`** `604eee2dffaeba3a270de61cf3dae887a33309c2` | **DIVERGIDA +68/−11** frente `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`; CCS11 (2022), PR #40 abierta; no ordenar por ramas |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | `master` `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | Igual; compatibilidad IDF6/console septiembre2026, PR #151 cierre IDF5.5 |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause | `main` `c6872259f4194fb76c7d333bda209343e8c88e71` | **+21/−0** frente `7009584dadc20cf20c20a6062f357dd572ba6885`; Oct31 router LinkAccept y radio max-power; PRs recientes IPv6/CI abiertas |

**OOMWOO oficial leído, NO EDITADO:** `makerspet/oomwoo` main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` (PR upstream #79 fuera de alcance); `oomwoo-one` jazzy `a630d1c77255072d280a2a41a7a2bd1a1c98cadd`; `oomwoo-cad` main `038002ddc5586d711960545ecf76a038eec48656`; `oomwoo-install` jazzy `789ed982ac6ecef19a3c4789e43e1eeb5b021999`; firmware `fd8689f3e3f7bcd0dcc35725be4a48cd9fcc8596` (J1 **sin I²C**, 1/11); PCB `ac8ac0b52254` (esquema aligerado 1/11, avance respecto a `bfc381c10d2b...`). No asumir nuevas conexiones sin contrato.

**Gobernanza:** decisiones maestras locales 00_DECISION_NO_TRASPLANTE, 19-alternativas, D22, acuerdo W/C, VALDO_OOMWOO LEEME_PRIMERO y WPT_DATOS_V01 leídos. C posee CAD/servicio; W posee RF/WPT. Checkout compartido local **sucio** en rama de Codex, NO TOCADO; trabajo solo en rama W propia GitHub/PR #9. Otras automatizaciones de ingeniería OOMWOO/C apagadas. No se copiaron fuentes de autores, no se añadió GPL/BSD a código propio. No OEM, baterías, firmware, compras ni ensayos físicos.
