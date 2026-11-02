# W-IND-60 — Confirmación de aplicación recuperable tras perder el ACK (31/10/2026)

**Ámbito:** SOLO VALDO W, robot aspirador NUEVO independiente, desmontable y de control local. Cancelado el trasplante Xiaomi X20 Pro OEM el 28/10. No se tocan estaciones, firmware OEM, motor, batería, BMS, CAD de compañeros, clones de terceros, OOMWOO ni PR #79 cleaning-jobs.

## Defecto real localizado y corrección

El código propio previo de `w_link.py` descartaba cualquier `seq <= last_seq`. En una entrega válida de DATA cuyo **ACK de aplicación** se perdía, el emisor `AckTracker` retransmitía el mismo DATA, pero el receptor nunca volvía a confirmar. Resultado: **falso fallo de enlace** con aplicación receptora que sí había recibido los datos. La confirmación de entrega MAC de ESP-NOW no equivale al ACK de aplicación (documentación oficial del autor Espressif).

**Cambio W-IND-60:** el receptor guarda SOLO el último datagrama DATA aceptado y permite hasta **dos re-ACKs** estrictamente idénticos dentro de **240 ms** desde la aceptación, con sesión y nodo iguales y el testigo de autenticación del transporte exigido como booleano estricto `True`. Cada duplicado devuelve el mismo ACK; **no procesa de nuevo DATA, no mueve `last_ms`, no refresca el watchdog, no avanza secuencia y no rehabilita estados latched**. Una sesión local nueva borra el cache. Se rechaza el mismo número de secuencia con distinta carga y CRC válido, un mensaje antiguo, autenticación ausente, identidad errónea, CRC corrupto, desbordamiento de tiempo, rollback del reloj, y el tercer duplicado. `authenticated_transport=True` es un **supuesto inyectado**, NO cifrado/autenticación reales: no equivale a privacidad demostrada.

### Experimento sintético y resultado esperado, nunca medición radio

| Evento (tiempo simulado) | Estado esperado |
|---|---|
| DATA seq=1 en 1 ms; ACK devuelto pero descartado | Receptor acepta **una sola** muestra |
| Reintento del emisor en 60 ms | Receptor re-ACK y emisor acepta sin falso fallo |
| Dos duplicados adicionales (120/180 ms) | El segundo re-ACK está permitido; el tercero se rechaza |
| Medición de salud al terminar | `last_ms` mantiene el instante original de 1 ms; no se prolonga la vida del dato |

La prueba incluye integración emisor-receptor `AckTracker`+`ModuleReceiver`, paquete DATA retransmitido exacto y fallos inyectados. No se ha medido latencia real, alcance, interferencia, consumo, ni radio ESP32/802.15.4.

### Reproducción, evidencia y costes

Con Python estándar 3.10+ desde `research/2026-10-28-independent-wpt-sensor-v01` (sin instalar bibliotecas):

```sh
python3 -m unittest -v test_w_link
python3 -m unittest discover -s w_ind_60 -p 'test_w60.py' -v
python3 w_ind_60/w60_ack_demo.py > W60_SYNTHETIC_ACK_NO_RADIO.json
```

La suite nueva cubre **26 pruebas adversariales** y se ejecuta además la antigua suite de telemetría. El workflow `.github/workflows/w-ind-60-ack-recovery.yml` archiva JSON sintético y falla cuando las regresiones o declaraciones de procedencia sean incorrectas. **No declarar PASS remoto hasta comprobar GitHub Actions para el SHA publicado.** El código es original y se reutiliza en nuestra rama W; sin trasplantar código ajeno.

Coste marginal de esta **corrección de software: 0 € en componentes adicionales**; NO significa que los nodos RF, bobinas, aislación, instrumentación o el robot sean gratuitos. Véanse `BOM_W_IND_60.csv` y `MATRIZ_W_IND_60.csv`. Diotronic es proveedor auxiliar de pasivos/prototipado: sin referencias, IVA final, portes, MOQ ni existencias verificadas; ningún componente comprado o seleccionado por disponibilidad.

## Tres problemas independientes, selección y seguridad

1. **Dock / carga de estación:** completamente diferido. Carga litio, BMS y cargador desconectados; falta protocolo autorizado, control térmico, FOD, EMI, offset, humedad y doble desconexión autónoma normalmente OFF. No heredar estación Xiaomi u OOMWOO.
2. **Potencia para módulo reemplazable:** piloto hipotético de sensor **5 V, 80 mA media = 0,4 W y 300 mA pico = 1,5 W**. Comparar cable protegido sustituible frente a simple WPT sin feedback y WPT regulado con FOD/termometría/corte independiente. El sencillo no satisface por defecto seguridad; el regulado es candidato sin seleccionar componentes ni demostrar pérdidas, eficiencia, gap, offset o mantenimiento. No WPT para motores/bombas/turbina por defecto. WISP5 RFID únicamente si se demuestra ventaja para microconsumo.
3. **Datos:** **ESP-NOW** (esp-now Apache-2.0) como primer candidato compatible Espressif; **OpenThread** (BSD-3-Clause) alternativa con hardware 802.15.4 y coste/topología a justificar. Contrato común de trama 22 bytes con CRC16 CCITT-FALSE, secuencia, sesión, ACK **de aplicación**, timeout, latch y recuperación local; cifrado y autenticación del peer son **requisitos futuros externos, no implementados**. Un ACK no concede permisos a motores, seguridad o carga. CRC protege integridad accidental y NO sustituye autenticación.

## Comparación obligatoria de autores/HEAD (GitHub, 31/10/2026)

| Autor y licencia | Rama: SHA previo → HEAD comprobado | Avances/estado pertinentes |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master: 7c7858c0 → **7c7858c0**, igual | [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) fusionada en 2021. Los 100 W/81,3 % y 1–2 mm son datos del autor; prototipo lazo abierto, sin protecciones propias probadas. No copiar GPL. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master: 08332bc3 → **08332bc3**, igual | [PR #1](https://github.com/wisp/wisp5-hw/pull/1) fusionada en 2015; hardware RFID no entrega potencia continua al módulo ESP32. |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | pin d978a697 → **640kHz 604eee2d**, **DIVERGENTE**, 68 commits ahead / 11 behind | [PR #40](https://github.com/wisp/wisp5/pull/40) abierta. NO hacer fast-forward ficticio del pin; firmware en 640kHz. |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master: c3b5f9be → **c3b5f9be**, igual | [PR #153](https://github.com/espressif/esp-now/pull/153) cerrada sin merge; el SDK no asegura entrega a aplicación desde callback MAC. [Contrato del fabricante](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html). |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main: 7009584d → **e577777c**, 14 ahead / 0 behind | #13810 valida cipher suite; #13811 elimina APIs wakeup legadas; #13818 UDP scope; #13812 build. [PR #13825](https://github.com/openthread/openthread/pull/13825) abierta no integrada. |

El principal OOMWOO [makerspet/oomwoo](https://github.com/makerspet/oomwoo) HEAD `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` (29/10, star-history); [firmware](https://github.com/makerspet/oomwoo-firmware) `c63a21e14e7d950be7ac8195078b6f2211a1c8a4` (30/10); [PCB](https://github.com/makerspet/oomwoo-pcb) `c6232edb03fbbd3985f4a1e1580b2179c14c65f3` (30/10). PR #79 es cleaning-jobs, no W. VALDO propio PR #9 encabezado previo `66a4325febeaab99874dee78f50e1e29e19f3e35`. Documento maestro, D22, coordinación C/W y contrato VALDO_OOMWOO leídos, otras automatizaciones y checkout ajeno sucio revisados. Sin tocar sus fuentes. Material original propio; repo VALDO aún sin licencia explícita adoptada, no inferir derecho a redistribuir terceros.

## Bloqueadores y siguiente puerta

**Cero pruebas físicas, cero radios conectadas, cero bobinas energizadas, cero baterías/BMS conectadas.** Nunca confiar en el ACK para parada crítica, FOD, temperatura o desconexión. Sigue fallando **intencionadamente** el ERC W-IND-18 por 9 infracciones del esquema conceptual; hay que corregirlas eléctricamente, no maquillar CI. Seguridad de carga, privacidad RF efectiva, calidad de servicio y eficiencia WPT sólo se pueden comprobar con hardware, proceso de seguridad y autorización posterior.

**Próxima puerta útil:** validar cifrado/identidad de pares y fallos reales de RF en un banco aislado autorizado, medir potencia/bursts del sensor y comparar coste por sustitución con cable antes de elegir WPT.
