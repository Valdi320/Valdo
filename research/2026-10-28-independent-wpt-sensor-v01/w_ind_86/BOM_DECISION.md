# W-IND-86 — matriz, BOM condicionada y dueños (1/11/2026)

## Matriz
| Alternativa | Potencia/coste | Seguridad y duración | Decisión |
|---|---|---|---|
| Cable desmontable y retenido | TX sin consumo, precio pendiente | Recambios y ciclos mecánicos a evaluar por C | **BASELINE** |
| ST25DV04KC NFC EH | En datos ST AM10 de **0,36 a 12,593 mW** con lector/antena específicos, **no garantías**; chip SO8N ~1,12€ IVA no incluye sistema | V_EH sin regular, inversión AM10 vs AM100 al cambiar campo, sin FOD/corte/offset ni comunicación app demostrados | **SOLO microsensor intermitente** |
| Simple Wireless Power GPL-3.0 | Hasta 100 W, 81,3% declarados por autor en otro prototipo; no aplicable a esta carga | Sin FOD/temperatura/corte independiente cualificados | Referencia, sin código GPL importado |
| WPT regulada y RF separada | Eficiencia a 1–20 mW, consumo búsqueda/reposo y coste total **desconocidos** | FOD/temperatura/EMI, desconexión autónoma, offset y agua sin prueba | No elegida |
| WISP5 RFID BSD-2-Clause | Microsensores, lector específico | Dependencia fuerte de campo y firmware en rama divergente | Secundaria |
| ESP-NOW Apache-2.0 vs OpenThread BSD-3-Clause | Datos, **no alimentación** | CRC, ACK app, secuencias, timeout, privacidad/cifrado, recuperación; parada crítica local | No escoger ambos por defecto |
| Dock/batería/BMS/motores/bombas | Extrapolación NFC inválida | Alta potencia y carga de litio NO autorizadas | Fuera del hito |

## BOM de investigación — sin compra
Diotronic es **auxiliar**, nunca único. No se confirma precio/stock físico en Zaragoza. Los portales pueden cambiar; IVA calculado no incluye portes.

| Referencia exacta | Diotronic / alternativa | Precio IVA y MOQ | Disponibilidad verificada o pendiente; razón |
|---|---|---|---|
| ST25DV04KC-IE8S3 SO8N | Diotronic: sin stock ni ref confirmados / [Farnell ES 3972494](https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494) | Catálogo 0,926€ sin IVA ≈ **1,12046€ con IVA 21%**, MOQ1, transporte pendiente | Catálogo web, entrega efectiva sin confirmar; SO8N facilita retrabajo relativo |
| ST25DV04KC-IE8S3 SO8N | Diotronic pendiente / [RS ES 248-7495](https://es.rs-online.com/web/p/modulos-rf/2487495) | **5,83€ IVA** paquete de 5, MOQ5; envío pendiente | Catálogo indica stock desde otro centro, NO Zaragoza |
| ST25DV04KC-IE6S3 SO8N (rango térmico distinto) | Diotronic pendiente / [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/ST25DV04KC-IE6S3/14645784) | Catálogo 0,71€ sin IVA ≈ **0,8591€ con 21%**, MOQ1, envío pendiente | No equivale automáticamente a IE8S3; comparar datasheet |
| Lector ISO15693, antena clase 1 | Diotronic/TME/Mouser/DigiKey/fabricante pendientes | **Sin referencia escogida, precio IVA/MOQ/stock pendientes** | Consumir del lector, campo útil, tamaño, reemplazo, coste/EMI por medir |
| Regulador mW, supervisor autónomo, corte normalmente OFF, condensador efectivo/ESR | Diotronic pasivos si equivalentes; críticos a distribuidor trazable | **Pendiente**, sin variantes certificadas | Ninguna curva de conversión o máximo de corte garantizados |
| Cable alternativo desmontable | Diotronic/TME/Mouser/DigiKey | **Pendiente**, longitud/pines/ciclos por definir | Reutilizable y reemplazable como referencia de bajo coste |

No se declara que un precio catálogo implique stock en tienda. Ningún componente de seguridad elegido solo por precio o cercanía.

## SHA de autores y revisión upstream; comparación con 19-alternativas (28/10)
| Autor y licencia | Rama HEAD real al 1/11 | Estado respecto al SHA maestro |
|---|---|---|
| [mark-belbin/simple-wireless-power GPL-3.0](https://github.com/mark-belbin/simple-wireless-power) | master **7c7858c0dd7040801b6f191df1396115560218f0** | Igual. Última actualización de código junio 2021, PR #1 cerrada |
| [wisp/wisp5-hw BSD-2-Clause](https://github.com/wisp/wisp5-hw) | master **08332bc398aa3350d351ef2aaac163f8007cffda** | Igual; último junio 2017 |
| [wisp/wisp5 BSD-2-Clause](https://github.com/wisp/wisp5/tree/640kHz) | **640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2** | **DIVERGIDA +68/−11** frente d978a6978ad23ccd6c44dd55430973b04a3d4a9b; CCS11, no inferir orden por ramas |
| [espressif/esp-now Apache-2.0](https://github.com/espressif/esp-now) | master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5** | Igual; correcciones recientes compatibilidad IDF6 y saneamiento consola sep2026 |
| [openthread/openthread BSD-3-Clause](https://github.com/openthread/openthread) | main **c6872259f4194fb76c7d333bda209343e8c88e71** | **+21** frente 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13800 router y #13821 max-power-table octubre31 |

Consultadas HEAD, comparación y PR/commits de respectivos creadores; no se copian archivos o diseños licenciados. ST es una fuente de datos de fabricante (atribuidos), no repositorio abierto.

## Coordinación y límites
Se leyeron decisiones maestras locales 00_DECISION_NO_TRASPLANTE, 19-alternativas, D22, acuerdo C/W, VALDO_OOMWOO LEEME_PRIMERO y WPT_DATOS_V01. Solo W puede escribir esta carpeta/PR propia. C lleva CAD mecánico. OOMWOO oficial [makerspet/oomwoo](https://github.com/makerspet/oomwoo) main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**; [firmware](https://github.com/makerspet/oomwoo-firmware) **fd8689f3e3f7bcd0dcc35725be4a48cd9fcc8596**, [PCB](https://github.com/makerspet/oomwoo-pcb) **bfc381c10d2bcc34bcd7ad8874575bac9a6b64ed**. Cambios del 1/11 indican J1 sin I2C, no inventar conectividad; PR #79 cleaning-jobs no se toca. No cambios en clones upstream, ficheros de compañeros, OEM, maquinaria, litio o estación.
