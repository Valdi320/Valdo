# W-IND-84 · matriz técnica/BOM sin adquisiciones, 2026-11-01

## Decisión para el primer módulo: sensor diagnóstico NO crítico, siempre sustituible

| Dominio | Opción | Evidencia actual | Decisión |
|---|---|---|---|
| Estación de carga | WPT regulada con TX/RX, FOD térmica, offset, corte local | Sin acoplador ni batería autorizados, ninguna prueba física; distinta del piloto | **NO APROBADA**; diseño de dock independiente |
| Alimentación del sensor | **Cable corto sustituible** con retención mecánica | Referencia simple, reparable, sin consumo del TX | **BASE ACTUAL**; medir precio, ciclos y daño si el conjunto cambia |
| Alimentación del sensor | WPT sencilla abierta, proyecto mark-belbin | Prototipo autor hasta 100 W con 81,3 % en su configuración; no controla RX/TX de forma cerrada y documenta calentamiento | Referencia de aprendizaje, sin copiar GPL-3.0 |
| Alimentación del sensor | WPT regulada y cortes independientes | FOD, temperatura, humedad, offset, EMI y dinámica sin medir | **PENDIENTE**; usar W84 para traza, no autorizar físico |
| Micro-sensores | WISP5 RFID sin batería | Energía extremadamente pequeña y lector especializado | Investigación secundaria; no presuponer sensor continuo |
| Datos de un sensor | ESP-NOW | Poco stack, API Espressif; RF no es alimentación, confirmación MAC no es ACK de app | Primer candidato, sujeto a corriente real por fase, cifrado y recuperación |
| Datos de un sensor | OpenThread | Red Thread más compleja; 21 commits nuevos de autor | Alternativa si hay razón de topología y coste; no duplicar dos stacks |
| Parada crítica | Radio + ACK/CRC/HMAC | No garantiza tiempo real ni corte al perder TX/RX | **PROHIBIDO**; doble corte eléctrico local y watchdog independiente |

Para datos se exige mensaje identificador de sesión, secuencia, CRC para corrupción, ACK **de aplicación**, timeout, replay/rollback y privacidad con cifrado adecuado. HMAC sola no cifra. Ninguna radio reinicia automáticamente actuadores críticos. El primer módulo no dirige motor, bomba, suspensión ni seguridad de colisión.

## BOM de referencia de *instrumentación futura*, no lista de compra

| Referencia | Diotronic / alternativa | Precio de una unidad | Stock/MOQ/IVA/portes en Zaragoza | Motivo y puerta de aceptación |
|---|---|---|---|---|
| Resistencia 1,5 kΩ, ≥0,25 W, ±5 % | Diotronic equivalente **pendiente**; TME CF1/4W-1K5 SR PASSIVES | Diotronic y TME **sin total verificado** | TME catálogo visto con MOQ 100; inventario **en tienda Zaragoza no confirmado**; IVA y portes pendientes | A 5 V ideal: 16,7 mW; solo candidata a carga artificial pequeña, recalcular disipación y tolerancia |
| Resistencia HS25/1R 1 Ω 25 W | Diotronic HS25/1R, ficha comercial en web | 3,75 € IVA incluido **publicado online**, no en tienda | Disponibilidad en tienda de Zaragoza **pendiente**; envío no incluido | **DESCARTADA** para piloto: a 5 V demandaría 25 W, no 1–20 mW |
| Pareja inductiva TX/RX activa y regulada | Diotronic (no se ha confirmado equivalencia) / TME / Mouser / DigiKey / fabricante | **Pendiente**, ninguna combinación cualificada | MOQ, precio con IVA, trazabilidad y stock por verificar | Curvas 1–20 mW con RX presente, regulación, desalineación, pérdidas y función de corte; no confundir standby sin receptor |
| Supervisor independiente y elemento de corte | Diotronic auxiliar si cualificado / distribuidores con hoja oficial | **Pendiente** | Trazabilidad, máx. propagación, reposo, backfeed, seguridad y existencias **pendientes** | No seleccionar con tiempo típico como máximo; revisar histéresis y retención de bloqueo |
| Sensor/monitor de corriente de dos canales + logger temporal | Diotronic auxiliar / fabricante especializado | **Pendiente** | Resolución sub-mA, sincronización, muestreo, incertidumbre y calibración pendientes | Instrumentación independiente necesaria para trazas reales; W84 solo consume CSV |
| Opción RF ESP32-C3 devkit (solo referencia) | DigiKey ESP32-C3-DEVKITM-1-N4X / Diotronic sujeto a equivalencia | ~6,85 € indicado en DigiKey; **IVA final no verificado** | Puesto en casa, cantidad y existencia en Zaragoza pendientes | Solo evaluación digital, nunca seleccionada ni comprada |
| Condensador hold-up, FOD sensor, termometría | Diotronic auxiliar / distribuidores especializados | **Pendiente** | ESR, derating, temperatura, FOD, precios/IVA/stock pendientes | No utilizar capacidad nominal sin peor caso ni dar por ensayada ninguna protección |

Precios publicados son instantáneas orientativas, no ofertas totales ni disponibilidad local. Diotronic es **auxiliar**, jamás arquitectura obligatoria. Fuentes: https://www.diotronic.com/2-inicio ; https://www.diotronic.com/ ; https://www.tme.eu/es/details/cf1_4w-1k5/resistencias-tht/sr-passives/ ; https://www.digikey.es/ ; hojas oficiales correspondientes. **Compras, fabricación, impresión, soldadura y energización: cero.**

## Auditoría externa de propietarios y HEAD (consulta GitHub 2026-11-01)

Los commits referidos se contrastaron por rama HEAD y **comparación de historial**, no por orden lexicográfico ni cronológico aparente. Los cinco repositorios pertenecen a **cuatro proyectos independientes**.

| Autores / proyecto | Licencia | SHA maestro 28/10 | Rama HEAD actual | Relación comprobada |
|---|---|---|---|---|
| mark-belbin/simple-wireless-power | GPL-3.0 | `7c7858c0dd7040801b6f191df1396115560218f0` | master: **idéntico** | 0 nuevos; PR #1 merged 2021-05-25 |
| wisp/wisp5-hw | BSD-2-Clause | `08332bc398aa3350d351ef2aaac163f8007cffda` | master: **idéntico** | 0 nuevos; PR #1 merged 2015 |
| wisp/wisp5 | BSD-2-Clause | `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` | **640kHz**: `604eee2dffaeba3a270de61cf3dae887a33309c2` | **DIVERGENTE**, +68/−11 commits; NO asumir que registro está incluido |
| espressif/esp-now | Apache-2.0 | `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | master: **idéntico** | 0 nuevos; PR #151/#153 cerradas en 2026 |
| openthread/openthread | BSD-3-Clause | `7009584dadc20cf20c20a6062f357dd572ba6885` | main: `c6872259f4194fb76c7d333bda209343e8c88e71` | **+21 commits**, PR #13800 merged 2026-10-31 |

Fuentes originales:
https://github.com/mark-belbin/simple-wireless-power ;
https://github.com/wisp/wisp5-hw ;
https://github.com/wisp/wisp5/tree/640kHz ;
https://github.com/espressif/esp-now ;
https://github.com/openthread/openthread .
Solo se leyeron metadatos y cambios de autor; no se copió código ni hardware.

## Estado reciente OOMWOO y propiedad

| Upstream autor | Rama y HEAD al 01/11 | Diferencia frente snapshot local de VALDO_OOMWOO |
|---|---|---|
| makerspet/oomwoo | main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` | +1 commit, gráfico estrellas |
| makerspet/oomwoo-firmware | main `ce05f2660f899c3f78c8df2b6391d0f3442e3bff` | +7 commits, SPEC y mapeo pines |
| makerspet/oomwoo-pcb | main `87aa7d386af2cef9fd083141b3a733598b3d3f5a` | +10 commits, incluyendo estación y BOM, NO integrar |
| makerspet/oomwoo-one | jazzy `a630d1c77255072d280a2a41a7a2bd1a1c98cadd` | idéntico |
| makerspet/oomwoo-cad | main `038002ddc5586d711960545ecf76a038eec48656` | idéntico |

El checkout local VALDO antiguo estaba en rama **de Codex**, con muchos ficheros modificados/no seguidos de compañeros; **NO fue tocado**. El trabajo W84 se publica exclusivamente mediante GitHub sobre rama y PR W propios; OOMWOO #79 cleaning-jobs queda intacta. Se verificó que la tarea OOMWOO de otro frente está desactivada. Permisos GitHub de `Valdi320/Valdo` comprobados. Ningún origen de datos es ensayado como fabricante en el robot, ni licencia ajena se hereda como autoría nuestra.

**Decisión**: mantener cable reemplazable como referencia ganadora provisional; esperar datos de TX/RX activos y RF real, FOD, EMI, descarga residual, autonomía de desconexión, humedad, temperatura, coste instalado con IVA, reparación y montaje. W84 facilita **rechazar** traces incompletas, no certifica ninguna protección.
