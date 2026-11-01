# W-IND-91 — BOM, decisiones y trazabilidad (01/11/2026)

**Cero compras, mediciones, montaje o aprobación.** El conjunto se propone para evaluación con alimentación externa, no como microsensor inalámbrico probado. W90 registró estos precios web de DigiKey ES el **01/11/2026**; confirmar antes de comprar. Los importes tienen **IVA del 21%**, excluyen transporte y costes adicionales. Ni inventario de tienda Diotronic Zaragoza, ni pedidos, ni cantidades económicas de producción están verificados.

| Bloque / SKU | Diotronic / alternativa documentada | Precio con IVA | MOQ / disponibilidad | Elección |
|---|---|---:|---|---|
| Lector ST X-NUCLEO-NFC08A1 | **Diotronic pendiente** / [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC08A1/16962233) | **41,08 €** | MOQ1; 443 remoto anunciado en W90, no local | Solo lector de evaluación, consumo completo pendiente |
| Tag ST X-NUCLEO-NFC07A1 (64KC) | **Diotronic pendiente** / [DigiKey ES](https://www.digikey.es/en/products/detail/stmicroelectronics/X-NUCLEO-NFC07A1/16284297) | **18,57 €** | MOQ1; 80 remoto W90, no local | ST1 selecciona alimentación del tag, no de NUCLEO |
| ST NUCLEO-L476RG, 1 o 2 | **Diotronic pendiente** / [DigiKey ES](https://www.digikey.es/en/products/detail/stmicroelectronics/NUCLEO-L476RG/5347711) | **24,54 €/u** | MOQ1; 2314 remoto W90, no local | NUCLEO por USB **invalida evidencia RF-only** |
| Cable/terminales/pasivos sustituibles | **Diotronic auxiliar** / TME, Mouser, DigiKey | **Sin SKU/precio IVA comprobado** | Stock Zaragoza y MOQ pendientes | Referencia reparable y normalmente más simple |
| Fuente aislada, carga resistiva, V/I calibrado, corte autónomo, FOD, térmica y EMI | Diotronic pasivos si equivalentes; **distribuidores especializados críticos** | **Sin selección, precio ni stock verificables** | Pendiente | Bloqueo de seguridad: no energizar |

**Subtotal parcial** lector+tag+un NUCLEO **84,19 €**; con dos NUCLEO **108,73 € IVA incluido** sin envío, instrumentación, protecciones, sensor, regulación y banco. Los precios finales, MOQ e inventario exacto para esta cesta en Diotronic, TME y Mouser **no están verificados**; no simular equivalencias ni disponibilidad de la tienda. El bare IC ST25DV04KC antes mencionado ~1,12 € NO incluye antena, lector ni circuito. No asumir que dos NUCLEO son necesarias para el primer sensor, ni que sirvan para demostrar cosecha energética.

## Matriz de decisión

| Opción | Límite medible y riesgo | Estado |
|---|---|---|
| Cable reemplazable | coste, ciclos de servicio, conductores reales | **BASELINE** |
| NFC07A1 ST1=3V3 o RX conectada a NUCLEO por USB | alimentación externa o retroalimentación no descartada | **RECHAZAR como prueba de WPT autónoma** |
| NFC07A1 ST1=EH y carga V_EH aislada | salida bajo carga, arranque, campo real, estabilidad, pérdidas y coste | **CANDIDATO DE BANCO; NO APROBADO** |
| Dock WPT simple/regulado | FOD, temperatura, offset, EMI, humedad y corte independiente | **BLOQUEADO** |
| ESP-NOW u OpenThread | ACK de aplicación, CRC, secuencia, timeout, cifrado, reconexión, energía por evento | **DATOS ÚNICAMENTE; SIN PARADA CRÍTICA RF** |
| WISP5 | lector RFID y presupuestos de microenergía | **SOLO MICRO-SENSOR** |
| Motores/bombas WPT | corrientes de pico, eficiencia y calor desconocidos | **NO PROPONER** |

## Autores externos: HEAD, rama y diferencias vs SHAs de 19-alternativas (28/10)

Consultados el **01/11/2026** con GitHub y comparación de commits:

| Autor/repositorio | Licencia | HEAD verificado (rama) | Comparación registrada |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) | GPL-3.0 | [7c7858c0](https://github.com/mark-belbin/simple-wireless-power/commit/7c7858c0dd7040801b6f191df1396115560218f0) master | idéntico 0/0 |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) | BSD-2-Clause | [08332bc3](https://github.com/wisp/wisp5-hw/commit/08332bc398aa3350d351ef2aaac163f8007cffda) master | idéntico 0/0 |
| [wisp/wisp5](https://github.com/wisp/wisp5) | BSD-2-Clause | [604eee2d](https://github.com/wisp/wisp5/commit/604eee2dffaeba3a270de61cf3dae887a33309c2) **640kHz** | **DIVERGENTE +68/−11** desde d978a697; no inferir actualidad por rama |
| [espressif/esp-now](https://github.com/espressif/esp-now) | Apache-2.0 | [c3b5f9be](https://github.com/espressif/esp-now/commit/c3b5f9be245f1a80db9cb938600566aa6a8dd1e5) master | idéntico 0/0 |
| [openthread/openthread](https://github.com/openthread/openthread) | BSD-3-Clause | [c6872259](https://github.com/openthread/openthread/commit/c6872259f4194fb76c7d333bda209343e8c88e71) main | +21/−0 desde 7009584; PR #13800 integrada 31/10, #13825-27 pendientes 01/11 |

El proyecto oficial [makerspet/oomwoo](https://github.com/makerspet/oomwoo) main HEAD **f01a1b295f462da5ab8d5f021a3f741cbd2b47df** (cambio gráfico 29/10) y Valdo master **8a6030bda52a159493a42dc4bed245e722b876e8**; W propia en PR #9 comenzó este hito en **4069c4ed485a443db6047077e6b457f45b64ae1d**. Se revisaron PR recientes OpenThread; ninguna fuente externa se copió. OOMWOO #79 cleaning-jobs y todos los clones upstream, CAD C y checkout compartido intactos. Coordinación histórica de W/C subordinada a cancelación OEM del 28/10.

## Fuentes ST (dato del autor, no medición propia)

[UM2960 Rev.2](https://www.st.com/resource/en/user_manual/um2960-getting-started-with-the-xnucleonfc07a1-nfcrfid-tag-ic-expansion-board-based-on-st25dv64kc-for-stm32-nucleo-stmicroelectronics.pdf) conexiones, ST1 y esquema; [X-NUCLEO-NFC07A1](https://www.st.com/en/evaluation-tools/x-nucleo-nfc07a1.html) tag 64KC; [DB4607](https://www.st.com.cn/resource/en/data_brief/dm00838234.pdf) EH puede high-Z; [X-NUCLEO-NFC08A1](https://www.st.com/en/evaluation-tools/x-nucleo-nfc08a1.html) lector. Lector/tag podrían compartir ISO15693 pero no constituyen sistema probado, ni garantizan potencia suficiente ni simultaneidad de lectura y alimentación.

**Próximo dato decisivo**: tras seguridad y autorización expresa, medir solamente banco aislado sin litio, RX V_EH/I_EH con carga y MCU desconectada, TX V/I de entrada, RF ON durante ACK, offset y corte térmico/FOD/EMI independiente. Hasta entonces hardware_release=BLOCKED.