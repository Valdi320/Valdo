# W-IND-85 — decisión/BOM con trazabilidad y licencias, 2026-11-01

## Matriz técnica para un solo módulo opcional no crítico

| Diseño | Ganancia posible | Problema que impide aprobarlo | Estado |
|---|---|---|---|
| **Cable desmontable** | Sin consumo permanente de TX; bajo coste/recambio fácil | Falta cuantificar ciclos en CAD C, pero sin nueva electrónica | **BASELINE** |
| **ST25DV04KC NFC EH/RFID** | Alimentación+datos a microsensor cerca de lector, sin contactos de módulo | V_EH no regulada/Hi-Z, RF no garantizada durante EH, lector/antena/energía sin datos locales | **SOLO MICROSENSOR INTERMITENTE / CRIBA** |
| WPT sencilla mark-belbin GPL-3.0 | Diseño abierto aprendizaje | No integra las protecciones FOD/temperatura/corte cualificadas | No seleccionada; sin copiar GPL |
| WPT regulada + radio RF separada | Potencia controlable | TX/RX a 1–20 mW cargado y RF real sin validar, coste/FOD/EMI/humedad | Bloqueada |
| WISP5 RFID | Referencia histórica microsensores | Lector especializado, rama firmware divergente, potencia escasa | Secundaria |
| ESP-NOW / OpenThread | RF sin conexión de señal | No lleva electricidad, exige privacidad/ACK de app/recovery/watchdog local | Candidatos por separado |
| Carga dock / BMS / motores / bombas | Ninguna extrapolación lícita del NFC | Seguridad/batería/corte/coste no demostrados | **FUERA DE ÁMBITO** |

## BOM verificable, **sin compra**

**El chip solo NO constituye una solución**: costo conjunto requiere lector, antena, regulador, almacenamiento energético, protecciones, integración, IVA, MOQ, envío a Zaragoza y consumo de vida útil. Diotronic se considera **auxiliar**, nunca condicionante de diseño.

| Exacta referencia y función | Diotronic / alternativa | Precio con IVA, MOQ, portes | Existencia comprobada / pendiente |
|---|---|---|---|
| **ST25DV04KC-IE8S3** SO8N, NFC EH/I2C | Diotronic **sin referencia/stock Zaragoza confirmado** / [Farnell España 3972494](https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494) | **0,926 € sin IVA**, **1,12046 € con IVA 21 % calculado**, MOQ1 cinta cortada; porte pendiente | Farnell web mostró 735 uds, fotografía de catálogo que puede estar anticuada; **NO stock local confirmado**. SO8N favorece reparación |
| **Misma ST25DV04KC-IE8S3** SO8N | Diotronic pendiente / [RS España 248-7495](https://es.rs-online.com/web/p/modulos-rf/2487495) | **5,83 € con IVA por paquete de 5**, MOQ5; portes pendientes | Catálogo RS mostraba stock desde otra delegación, no Zaragoza |
| **ST25DV04KC-IE8C3** UFDFPN8, diferente encapsulado | [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/ST25DV04KC-IE8C3/16359660) / Diotronic pendiente | **1,34310 € IVA incluido**, MOQ1, envío pendiente | Online 2400 a la consulta; **descartada provisionalmente** por mayor dificultad de reparación/footprint no equivalente |
| **ST25DV04KC-IE6S3** SO8N rango térmico distinto | [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/ST25DV04KC-IE6S3/14645784) / TME/Mouser/Diotronic pendiente | **Precio/IVA/portes exactos pendiente** | Variante NO intercambiable sin comparar rango; no confundir con ST25DV04K-IER6S3 anterior |
| Lector ISO15693 13,56 MHz, antena ISO clase1 | Diotronic/TME/Mouser/DigiKey y fabricante, pendiente | **Total pendiente**, MOQ/IVA/portes desconocidos | Consumo, intensidad campo, distancia, offset, estado de catálogo no verificados |
| DC/DC para V_EH, condensador efectivo, monitor y corte local | Diotronic para pasivos; especializados para funciones críticas | **Pendiente**, no seleccionados | Hace falta eficiencia trazable en mW, ESR, envejecimiento y protección independiente |
| Cable corto reparable baseline | Diotronic para conectores/pasivos; alternativas TME, Mouser, DigiKey | **Pendiente** | Comparación de mantenimiento y coste total aún sin datos físicos |

No inventar stock de Diotronic; precios web no son presupuesto puesto en casa. Ninguna elección crítica sin fabricante y ensayos. Documentos de autor: [ST DS13519 Rev8 §5.5.2 p49](https://www.st.com/resource/en/datasheet/st25dv04kc.pdf#page=49), [ST AN4913 Rev2 p7](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7). Dos puntos **del fabricante**; no nuestros. Hipótesis: carga2,9mW, eficiencia80%, rail3,3V, outage100ms, condensador330uF efectivos. Garantía de funcionamiento: **NINGUNA**.

## Dueños externos, HEAD y comparación con documento local 19-alternativas (28/10)

Consultas de rama y comparación git, 1/11/2026; **no** deducidas del orden aparente de ramas. Los autores conservan todos sus derechos:

| Autor/repo | Licencia | HEAD de rama original | Frente a SHA documentado |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) | GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | Idéntico |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) | BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | Idéntico |
| [wisp/wisp5](https://github.com/wisp/wisp5/tree/640kHz) | BSD-2-Clause | **640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2** | **DIVERGE +68/−11** contra d978a6978ad23ccd6c44dd55430973b04a3d4a9b |
| [espressif/esp-now](https://github.com/espressif/esp-now) | Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | Idéntico |
| [openthread/openthread](https://github.com/openthread/openthread) | BSD-3-Clause | main c6872259f4194fb76c7d333bda209343e8c88e71 | +21 contra 7009584dadc20cf20c20a6062f357dd572ba6885 |

Se revisaron además PR/changelog recientes de los autores: [Simple WPT](https://github.com/mark-belbin/simple-wireless-power/pulls), [WISP5](https://github.com/wisp/wisp5/pulls), [ESP-NOW](https://github.com/espressif/esp-now/pulls), [OpenThread](https://github.com/openthread/openthread/pulls). **No se incorpora ni atribuye contenido de terceros**.

OOMWOO oficial: makerspet/oomwoo main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**; [firmware](https://github.com/makerspet/oomwoo-firmware) main **ce05f2660f899c3f78c8df2b6391d0f3442e3bff**; [PCB](https://github.com/makerspet/oomwoo-pcb) main **87aa7d386af2cef9fd083141b3a733598b3d3f5a**. Se respetaron los archivos maestros local VALDO, VALDO_OOMWOO, contrato WPT_DATOS_V01 y lock de coordinación W/C; checkout compartido sucio y clones ajenos **sin tocar**. La automatización paralela OOMWOO estaba desactivada. La PR makerspet/oomwoo **#79 cleaning-jobs NO recibe WPT**.

**Conclusión:** el ST SO8N ~1,12 € en catálogo *no* permite declarar inalámbrico barato. Sin lector y energía RF continua, protección/EMI/FOD/humedad, y datagramas válidos, el cable sustituible continúa siendo referencia.
