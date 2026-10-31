# W-IND-81 — No confundir retardo típico con máxima reacción garantizada

31/10/2026. Aporte ORIGINAL **solo W** al **nuevo robot abierto**; no Xiaomi OEM, no firmware ni electrónica OEM, batería/BMS/dock ni motores. No se ha tocado hardware, CAD de C, OOMWOO ni PR #79 cleaning-jobs. No hay autorización de compras ni ensayos físicos.

## Hallazgo documental real, efecto verificable

La ficha oficial [TI TPS3890, SLVSD65A, tablas 7.3/7.5/7.6](https://www.ti.com/document-viewer/TPS3890/datasheet/specifications) describe el TPS3890 **activo** y de umbral ajustable; a VDD=3,3 V, CT abierto y sobreexcitación de entrada del 5 % especifica **18 µs como retardo TÍPICO** entre SENSE decreciente y RESET, **sin valor MÁXIMO** en la columna correspondiente. La misma tabla cita 325 µs TÍPICOS para arranque, también sin máximo tabulado. La ficha garantiza rango VDD 1,5–5,5 V, especifica salida RESET de drenador abierto y exactitud de umbral del 1 %, pero no certifica por sí sola el corte ni la retención de un enclavamiento al perder VDD. Una corriente típica en reposo de 2,1 µA tampoco constituye garantía de consumo completo del enlace WPT.

**Nuevo control:** un analizador reproducible exige la *categoría* y condiciones de cada tiempo: TÍPICO, MÁXIMO de fabricante, medición o hipótesis; **nunca sustituye TÍPICO por MÁXIMO**. También estima la reserva ideal restante de un condensador tras alcanzar un umbral de desconexión y bloquea la aceptación cuando faltan máximos de respuesta y de conmutación. Ni una marca falsa 'manufacturer_max' ni una URL sin comprobar constituyen acreditación externa: estas etiquetas son datos proporcionados por el evaluador, no verificaciones de autenticidad del fabricante; **hardware_approved=false siempre**.

## Ejemplo sintético, NO especificaciones del robot ni del TPS3890

Se inventa un sensor no crítico que consume hasta **20 mW**, deja de funcionar bajo **3,00 V**, se supone desconexión a **3,08 V**, con **10 µF EFECTIVOS mínimos** disponibles en esa región (esta cifra NO ha sido ensayada y los condensadores nominales pueden perder capacidad). La caída del rail es modelada solo por el condensador ideal y una carga de potencia constante ≤20 mW:

t_ideal = C_ef,min × (V_trip,min² − V_suelo²) / (2 × P_pico).

Da **121,6 µs de reserva ideal condicionada**. Sumar erróneamente el tiempo típico de TI (18 µs) con **40 µs hipotéticos** de conmutación parece pasar (58 µs < 121,6 µs); nuestro gate lo **rechaza** por ausencia de límites máximos demostrados. Si SOLO como contrafactual se exigiesen 200 µs máximos del monitor y 40 µs máximos del corte, se necesitarían **al menos 19,736842 µF efectivos** bajo el modelo, sin margen extra. Es una cota teórica, no selección de un condensador real ni permiso de ensayo. Los 200 µs provienen de W79 como **HIPÓTESIS**, no de TI. No se conoce el retardo real máximo, por tanto aumentar capacidad *no demuestra* seguridad en este supervisor.

El modelo no cubre: dinámica del regulador RX, caída brusca sin reserva, capacitancia real bajo tensión/temperatura/envejecimiento, ESR/ESL, corriente de fuga, sobreconsumo, resistencia serie, entrada/arranque del monitor, cualificación de umbral e histéresis, señal open-drain/pullup, corrientes inversas, MOSFET soldados, alimentación independiente de monitor, latencia de enclavamiento, FOD, temperatura, agua, EMI o offset. La inferencia energética solo valdría si estas hipótesis se verificasen en un montaje concreto. El mínimo 1,5 V de alimentación del TPS3890 tampoco asegura operación cuando colapsa su propia fuente. No deriva ninguna lógica de parada crítica de ESP-NOW/OpenThread.

## Reproducción software (sin periféricos)

Desde esta carpeta, Python 3.10+ estándar, sin librerías externas: ejecutar 'python3 -m unittest -v test_w81.py'; después 'python3 w81_timing_provenance.py --input SCENARIO_SYNTHETIC.json --output /tmp/W81_REGENERATED.json'; comparar byte a byte contra W81_EVIDENCE_SYNTHETIC.json con 'cmp'. **31 pruebas deterministas/adversariales locales PASS** antes de publicar. CI propia prueba y archiva el JSON exactamente igual. No es simulación SPICE, certificación de semiconductor, medida de banco ni prueba eléctrica. El validador rechaza entradas no finitas, permisos mal tipados, procedencia ausente, batería conectada, carga crítica y ventanas sin margen.

## Decisión y tres trabajos distintos

- **Dock de carga:** NO implementado, aislado de litio y BMS. Definir y cualificar por separado FOD, temperatura, descarga, corte físico, humedad y protocolo de batería, solo tras proceso de seguridad y autorización.
- **Potencia sin contactos del primer módulo:** **BLOQUEADO para hardware**: ni TPS3890 ni red de 10 µF se aprueban; cable sustituible sigue referencia. Obtener mínimos garantizados de respuesta TX/RX/corte, tensión real mínima, cargas 1–20 mW, reserva efectiva y medir retardo con fuente aislada y carga resistiva autorizada. Comparar WPT simple vs regulado con FOD, temperatura, offset, EMI, apagado autónomo, coste total y mantenibilidad. No escalar a motores/bombas.
- **Datos por radio:** ESP-NOW (tentativo; menos red) vs OpenThread (topología IP/mesh; mayor complejidad). Ninguno alimenta ni sustituye parada local. Requiere ACK de aplicación, CRC, seq/epoch, timeout, emparejamiento/privacidad, reset seguro y pruebas de recuperación. WISP5 solo microsensores RFID discontinuos.

El supervisor de TI exige placa y unión de 1,5×1,5 mm WSON: desventaja de reparabilidad manual. Considerar comparador/supervisor físicamente reparable con tiempo MÁXIMO documentado o mantener el cable retenido.

## Autoría, licencias y estado HEAD consultados 31/10/2026

Son **fuentes de terceros, no código ni diseños copiados**. Baselines de '19-alternativas-abiertas-para-robot-independiente.md' 28 Oct:

| Propietario / licencia | HEAD actual / rama | Comparado con SHA registrado y revisión del autor |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | master '7c7858c0dd7040801b6f191df1396115560218f0' | igual; última revisión 8 junio 2021, PR #1 merged; hardware ~100 W no demuestra 20 mW. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2 | master '08332bc398aa3350d351ef2aaac163f8007cffda' | igual; 16 junio 2017, PR #1 histórica. |
| [wisp/wisp5](https://github.com/wisp/wisp5/tree/640kHz) BSD-2 | 640kHz '604eee2dffaeba3a270de61cf3dae887a33309c2' | **DIVERGE**: +68/−11 commits respecto a 'd978a6978ad23ccd6c44dd55430973b04a3d4a9b' (master); CCS11 25 abril 2022, PR #40 sin merge. |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | master 'c3b5f9be245f1a80db9cb938600566aa6a8dd1e5' | igual; 10 septiembre 2026 arreglo IDF6, PR #153 abierta. |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3 | main 'b6d0f06db304055f5866ff6e3c67370b54c81b15' | +18/0 respecto a '7009584dadc20cf20c20a6062f357dd572ba6885', PR #13790 radio y #13823 CLI merged 31 Oct; no importar. |

OOMWOO oficial 'makerspet/oomwoo' main 'f01a1b295f462da5ab8d5f021a3f741cbd2b47df' (29 Oct, gráfico; PR #78 antes), VALDO master '8a6030bda52a159493a42dc4bed245e722b876e8', propia PR #9 head previo W80 '36faa4ccd701bf2cc24a2e83d7784d4544886d11'. Adaptación local y contrato WPT_DATOS_V01 revisados. Solo propia rama GitHub W; **checkout local compartido dirty en rama Codex no tocado**. Dueño C de CAD; otras automatizaciones revisadas sin otra W concurrente. No material Codex A01–A04 reapropiado.

## Fuentes y BOM

- TI [TPS3890](https://www.ti.com/product/TPS3890), [tablas de temporización y VDD](https://www.ti.com/document-viewer/TPS3890/datasheet/specifications).
- [DigiKey España TPS389001DSER](https://www.digikey.es/es/products/detail/texas-instruments/TPS389001DSER/8567784): activo, cut tape 1ud **1,7100 EUR sin IVA / 2,06910 EUR con 21 %**, stock central mostrado ~26.283 (consulta 31 Oct; volátil), envío aparte. [DigiKey logística](https://www.digikey.es/es/): 25 EUR de porte para compras menores de 75 EUR; verificar checkout/fiscalidad antes de compra.
- 'BOM_W81.csv': Diotronic solo auxiliar; sin referencia exacta ni stock local verificado. TME/Mouser pendiente; no suponer equivalencia eléctrica ni comercial, no coste total PCB/protecciones. **CERO euros gastados**.
