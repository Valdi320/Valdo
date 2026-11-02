# W-IND-90: BOM, fuente, matriz y HEAD autores 01/11/2026

Precios del catálogo electrónico del distribuidor, NO stock en Zaragoza, NO reserva, IVA 21% calculado; cada uno MOQ1 sin portes. No equivalen a costo de robot terminado. Diotronic auxiliar para pasivos y prototipado solo si equivalente y competitivo; consulta local pendiente, nunca exclusivo.

| Bloque | SKU y fabricante | Diotronic / alternativa | Precio IVA incl. | Existencias y criterio |
|---|---|---|---|---|
| Lector NFC-V ISO15693, activo | ST X-NUCLEO-NFC08A1, ST25R3916B, antena 47x34 mm | Diotronic pendiente / https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC08A1/16962233 ; Farnell https://es.farnell.com/stmicroelectronics/x-nucleo-nfc08a1/expansion-board-nfc-card-reader/dp/4458495 | 41,0795 EUR DigiKey, MOQ1 (Farnell 34,98 EUR ex IVA) | 443 stock remoto anunciado DigiKey; ST confirma activo e ISO15693 https://www.st.com/en/evaluation-tools/x-nucleo-nfc08a1.html |
| Etiqueta con antena, 64KC NO 04KC | ST X-NUCLEO-NFC07A1, ST25DV64KC, diametro 54 mm | Diotronic pendiente / https://www.digikey.es/en/products/detail/stmicroelectronics/X-NUCLEO-NFC07A1/16284297 | 18,5735 EUR, MOQ1 | 80 remoto; ST activo y posibilidad de EH https://www.st.com/en/evaluation-tools/x-nucleo-nfc07a1.html ; NO reproducen tablas W89 |
| MCU host en lector y opcional en tag | ST NUCLEO-L476RG | Diotronic pendiente / https://www.digikey.es/en/products/detail/stmicroelectronics/NUCLEO-L476RG/5347711 ; Farnell https://es.farnell.com/stmicroelectronics/nucleo-l476rg/placa-desarrollo-arduino-mbed/dp/2493816 | 24,5388 EUR/u, MOQ1; Farnell 16,46 EUR ex IVA | 2314 remoto; escenario un host o dos hosts |
| Chip de W89 solo | ST25DV04KC-IE8S3 SO8N | Diotronic pendiente / Farnell https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494 | ~1,12 EUR, MOQ1, oferta histórica W89 a reconfirmar | Falta antena, PCB, lector, regulación, medición y corte |
| Lector descatalogado | ST X-NUCLEO-NFC06A1 | Diotronic pendiente / https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC06A1/10442436 | No cotizar | OBSOLETO; preferir evaluación 08A1 no drop-in por defecto |
| Alimentación aislada, carga ficticia, sensores V/I, termometría, FOD, corte independiente, cable baseline | SIN SKU cualificado | Diotronic pasivos / TME, Mouser, DigiKey y fabricantes para críticos | DESCONOCIDO, disponibilidad pendiente | BLOQUEO de seguridad y costo, no ensayo físico |

Costes del SKU específico DigiKey sin IVA y con IVA 21%: 33,95 + 15,35 + 20,28 = 69,58 EUR => 84,1918 EUR (un MCU, función limitada). Con dos MCU: 89,86 EUR => 108,7306 EUR. Esto no es presupuesto entregado ni coste económico de producción. TME y Mouser del conjunto exacto sin precio/stock verificados; Diotronic Zaragoza sin inventario local comprobado; no adquirir nada.

## Matriz funcional
| Opción | Problemas pendientes | Dictamen |
|---|---|---|
| Cable desmontable | ruta, costo, servicio según dueño C | BASELINE |
| NFC08A1+NFC07A1, con una o dos MCU | ST25DV64KC NO ES ST25DV04KC; curva W89 no transferible; RF/energía simultáneas y offset/V/I arranque no medidos; costo incompleto | CANDIDATO DE BANCO NO APROBADO |
| ST25DV04KC SO8N sin placa | no posee antena ni RF matching, energía sin medir | NO ASUMIR chip ~1EUR = módulo |
| Dock WPT sencillo | FOD, temperatura, EMIs, humedad, corte independiente sin aprobar | BLOQUEADO |
| Dock WPT regulado | coste/eficiencia/offset y prueba aislada sin batería | CANDIDATO NO APROBADO |
| ESP-NOW u OpenThread | datos, ACK app, CRC, seq, timeout, privacidad y recuperación; no alimentación | SELECCIÓN ABIERTA, radio no para sistema crítico |
| WISP5 | extrema baja energía, lector RFID | SOLO MICRO-SENSOR |
| Motores/bombas | potencias/pérdidas no demostradas | NO WPT POR DEFECTO |

## Cuatro proyectos externos, 5 repositorios: titulares/licencias, HEAD y cambios de autores
Comparación GitHub API 01/11 contra SHAs del documento local 19-alternativas registrado el 28/10:
- mark-belbin/simple-wireless-power, GPL-3.0: master https://github.com/mark-belbin/simple-wireless-power/commit/7c7858c0dd7040801b6f191df1396115560218f0 idéntico al registrado (0/0); PR #1 antigua integrada (2021). Sin copiar PCB/código.
- wisp/wisp5-hw, BSD-2-Clause: master https://github.com/wisp/wisp5-hw/commit/08332bc398aa3350d351ef2aaac163f8007cffda idéntico (0/0); PR #1 histórica integrada (2015).
- wisp/wisp5, BSD-2-Clause: firmware rama 640kHz https://github.com/wisp/wisp5/commit/604eee2dffaeba3a270de61cf3dae887a33309c2 vs registrado d978a6978ad23ccd6c44dd55430973b04a3d4a9b, DIVERGENCIA +68/-11; PR #40 abierta histórica; no infiere actualidad por rama.
- espressif/esp-now, Apache-2.0: master https://github.com/espressif/esp-now/commit/c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = registrado (0/0); PR #151/#153 2026 cerradas, no fusionadas.
- openthread/openthread, BSD-3-Clause: main https://github.com/openthread/openthread/commit/c6872259f4194fb76c7d333bda209343e8c88e71 +21/-0 vs registrado 7009584dadc20cf20c20a6062f357dd572ba6885; 2026.10.0 https://github.com/openthread/openthread/releases, PR #13800 fusionada 31/10, #13814/#13826 abiertas 01/11; API radio/CLI cambió. Ninguna copia de terceros.

OOMWOO oficial https://github.com/makerspet/oomwoo/commit/f01a1b295f462da5ab8d5f021a3f741cbd2b47df main, 29/10 ornamental; VALDO master https://github.com/Valdi320/Valdo/commit/8a6030bda52a159493a42dc4bed245e722b876e8. Solo PR #9 ámbito W, no OOMWOO #79 ni los 10 clones upstream ni adaptación ROS2. Coordinación: W exclusivamente electrónica, C CAD y fijaciones; local checkout compartido sucio y no tocado, otra automatización OOMWOO pausada. No hardware validado, batería/BMS desconectados, compras no autorizadas. Próximo hito no es más modelos: protocolo seguridad y única curva experimental real V_EH/I_EH con carga ficticia una vez aprobado; comparar cable.
