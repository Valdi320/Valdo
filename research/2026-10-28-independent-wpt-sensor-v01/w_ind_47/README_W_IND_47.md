# VALDO W-IND-47 — Puerta de coste y consumo del primer sensor (30/10/2026)

**Mejora:** herramienta original con 24 escenarios reproducibles y 20 tests para impedir que el robot abierto y barato adopte inductiva indiscriminadamente. Los precios proceden de catálogos de 30/10/2026, y las energías son **cálculos**, no medidas. Ninguna instalación, batería, estación ni prueba física aprobada.

## Matriz y resultados

Primer sensor hipotético: 5 V, 0,4 W medio, 1,5 W pico, no crítico. DFRobot DFR0362 (pareja TX/RX **solo energía**) a 9,92 € IVA incluido y portes **desde** 3,95 €, en [BricoGeek](https://tienda.bricogeek.com/fuentes-de-alimentacion/899-cargador-inalambrico-5v-1a.html). Alternativa: Adafruit 5089 (par de arneses montados 5 hilos, compatibles JST-PH) a 4,50 € IVA incluido, portes **desde** 12,50 € y almacén externo, en [Opencircuit](https://opencircuit.es/producto/2.0mm-pitch-5-pin-cable-matching-pair-jst-ph).

| Número hipotético de enlaces | DFR0362 y envío mínimo | Arnés 5 hilos y envío mínimo | Diferencia | Energía de TX sin receptor, si 24 h/día |
|---:|---:|---:|---:|---:|
| 1 | 13,87 € | 17,00 € | −3,13 € | 3,6–6 Wh/día |
| 2 | 23,79 € | 21,50 € | +2,29 € | 7,2–12 Wh/día |
| 4 | 43,63 € | 30,50 € | +13,13 € | 14,4–24 Wh/día |
| 8 | 83,31 € | 48,50 € | +34,81 € | 28,8–48 Wh/día |

**Interpretación:** los precios NO comparan sistemas funcionalmente equivalentes. El cable transporta cinco conductores; DFR0362 solo energía y requiere radio, protocolos y protección eléctrica adicional NO presupuestados. El caso de una sola pareja favorece artificialmente al kit WPT por **diferentes costes mínimos de envío**; no se puede concluir que el sistema inalámbrico sea más barato. Los ocho enlaces NO son una arquitectura elegida. La corriente de no carga de 30–50 mA a 5 V es referencia de fabricante/prestaciones archivadas [DFRobot](https://wiki.dfrobot.com/dfr0362), no medición propia y no implica 24 horas reales sin receptor.

## BOM barato y Diotronic
En Diotronic, [JST PHR2 solo carcasa](https://diotronic.com/serie-ph/13930-conector-hembra-ph-p-2-00-2v) cuesta 0,18 € IVA incluido y [cabecera B2BPHKS 2 pines](https://diotronic.com/1290-serie-ph) 0,36 €. **0,54 € es un subconjunto incompleto**, faltan contactos, cable, montaje, fijación y evaluación; su catálogo web dice disponible, pero existencia en la tienda de Zaragoza, MOQ, precio final y equivalencia no se han verificado. Otras opciones TME/Mouser/DigiKey pendientes para referencias exactas. No se compra nada.

## Decisión y seguridad
Para el sensor barato, **arnés corto retenido, reemplazable y fijado al bastidor** como referencia. Reservar **una** pareja inductiva experimental si una interfaz expuesta/húmeda o móvil demuestra realmente ventaja. FOD, temperatura, offset, humedad, EMI, desconexión por hardware independiente y recuperación son requisitos bloqueantes. No usar paquetes RF para parada crítica. **Dock** y carga de litio/BMS separados y desconectados; **WPT distribuido** sin aprobación; **datos** por ESP-NOW (primera opción de bajo coste) u OpenThread, con ACK aplicación, CRC, secuencia, timeout, privacidad y recuperación. WISP RFID solo para microsensores de potencia ínfima. Nunca WPT por defecto para bombas o motores.

## Reproducibilidad
Desde la carpeta w_ind_47:
```
python3 -m unittest -v test_w47
python3 w47_cost_gate.py --out W47_SYNTHETIC_NOT_HARDWARE.json
```
Aritmética Decimal, 4 tamaños × 3 períodos sin receptor × 2 corrientes = 24 casos; todos mantienen cost_complete=false, physical_measurement=false y wpt_production_authorized=false. Los 20 tests han pasado localmente antes de publicación; verificar Actions de esta revisión por separado. Sin pruebas RF reales, ni bobinas energizadas, ni FOD, ni medidas de temperatura, ni estaciones. BOM y matriz CSV acompañan.

## Fuentes, autores, roles y SHAs
Leídos los maestros 00/19/D22 y coordinación W/C (dueño W eléctrico, C mecánico), LEEME_PRIMERO y WPT_DATOS_V01. No tocar la rama local VALDO con archivos ajenos pendientes, ni los 10 upstream OOMWOO, ni la PR #79 de cleaning-jobs. Esta publicación es solo del sector W en PR propia #9.

* mark-belbin/simple-wireless-power GPL-3.0 master 7c7858c0dd7040801b6f191df1396115560218f0 = pin del 28/10.
* wisp/wisp5-hw BSD-2-Clause master 08332bc398aa3350d351ef2aaac163f8007cffda = pin.
* wisp/wisp5 BSD-2-Clause rama **640kHz** HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2: **68 por delante / 11 por detrás** de pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b.
* espressif/esp-now Apache-2.0 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin; PR #151 de compatibilidad consultada.
* openthread/openthread BSD-3-Clause main e577777c308f6c87e5da3056239231a8fc147cb2: **14 por delante / 0 detrás** del pin 7009584dadc20cf20c20a6062f357dd572ba6885, cambios de API radio/CI.
* makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df sin cambios de W.

Nada de código ni CAD de terceros se ha copiado. Las licencias y autorías originales permanecen intactas. Próximo paso: completar BOM por función con precio final de proveedores y ensayos de vida/reparación antes de sustituir cables por bobinas; experimentos físicos solo con autorización y protocolo de seguridad.
