# W-IND-36 — Supervisión de 3,3 V y 5 V con rearme físico local en KiCad (INCOMPLETO)

30/10/2026 · VALDO, autoría original propia sector W · **ROBOT NUEVO**, nunca electrónica, batería, estación ni firmware Xiaomi X20. **NO CONECTAR, FABRICAR NI ENERGIZAR**.

## Mejora material

Sobre el **generador propio W-IND-32** se introduce en un esquema KiCad 9 editable una ruta de permisos positiva para cada uno de dos TPS259470L en serie, con **dos supervisores TPS3840** (3,3V/2,8V y 5V/4,2V), **dos SN74LVC1G74** de rearme por flanco local, **cuatro SN74LVC1G08** (dos para EN y dos independientes para despejar /CLR), dos pulsadores y resistencias pull-down. Se **eliminan** J3/J4, las entradas externas no cualificadas de EN de W32. La radio no tiene ruta de rearme. La alarma INA301 **sigue siendo sólo informativa**: la sobrecorriente hipotética de 400mA no produce todavía un corte autónomo.

Ambos caminos deben perder el latch cuando se pierde *cualquiera* de las dos tensiones; esto evita que la pérdida de sólo 5V deje un Q persistente, y que la pérdida de sólo 3V3 deje Q indefinido tras reinicio. **Se implementa el requisito de topología en el netlist, NO un sistema de seguridad probado**. Dos compuertas CLR separadas reducen un punto de fallo lógico compartido, pero no establecen independencia de alimentación, semiconductor, entorno, fallo soldado ni FOD.

### Hallazgo cuantitativo nuevo

Con tensión mínima **hipotética** de 4,5V en una fuente nominal de 5V y tolerancia máxima ±1,5% de umbral, un supervisor de 4,4V (PL44) deja sólo **34mV** entre ese mínimo y el umbral alto de disparo: 4,5 − 4,466 = 0,034V. La variante real **TPS3840PL42DBVR** deja **237mV**: 4,5 − (4,2×1,015) = 0,237V. Esto es un criba **aritmética** de falso corte, no prueba la regulación de WPT ni valida la protección de 5V. Los tiempos de detección y rearme tampoco se extrapolan del modelo.

## Comprobación reproducible

Desde `research/2026-10-28-independent-wpt-sensor-v01/w_ind_36/`:

```sh
python3 generate_w36.py
python3 generate_w36.py --verify
python3 -m unittest -v test_w36.py
# En GitHub Actions se ejecuta KiCad CLI 9.0.2, ERC JSON y XML nativo.
python3 netlist_gate_w36.py native_out/w36_native.xml --out native_out/w36_gate.json
```

Las pruebas Python incluyen tabla de verdad, caída de cada rail, pulsador sostenido y necesidad de flanco local, sustitución de referencia PL44->PL42, exactitud de pines TI, regresión de topología, pin duplicado, cambios de variantes, puente entre cortes y fuentes no declaradas. Los XML de unittest son **sintéticos**; sólo el exportado por KiCad CLI es nativo. El generador produce esquema, biblioteca, tabla local y proyecto editable; GitHub Actions archiva ERC/netlist y decisión. **No atribuir PASS hasta que la ejecución concreta CI lo demuestre.**

## Riesgos críticos aún abiertos — veto de energización

- Los símbolos de pulsador son **abstractos, sin huellas, antirrebote ni ensayos**. Los pulsos espurios, rebotes de alimentación y cortocircuitos todavía pueden permitir un rearme no autorizado.
- No se ha diseñado **la fuente real 3,3V**, ni su secuenciación o supervisión por debajo de VPOR, ni aislamiento de retornos. El monitor INA301 puede aparentar ALERT sano sin VDD; el PG evalúa alimentación, pero **no se ha enlazado físicamente con corriente/fallo de ALERT**.
- La conexión de los dos supervisores comparte fallos comunes y no está validada eléctricamente; valores 100k, 100nF y temporización **TBD**, ausencia de pruebas SPICE/transitorios, ESD/EMI, fugas, sobretensión, FOD/NTC/térmica, offset, humedad y metal.
- Persisten **ILIM/ITIMER/OVLO/DVDT** de W32 sin dimensionar; los TPS259470L limitan a partir de ~500mA según variante y no resuelven el evento hipotético de **400mA**.
- Modelo digital NO cubre latch metastable, doble puente, dos salidas soldadas, carga de bobina/condensadores al cortar ni seguridad física. El esquema sigue siendo experimental sin footprints ni PCB/DRC.

Separación de problemas: **dock de carga**, **energía distribuida a sensor de baja potencia** y **datos RF**. La batería/BMS y dock se mantienen desconectados; motores/bombas no son candidatos WPT por defecto. ESP-NOW y OpenThread transmiten datos, con ACK de aplicación/CRC/secuencia/timeout y cifrado por probar; no alimentación ni parada crítica. WISP5 sólo es útil para microsensores RFID intermitentes.

## Abastecimiento: proveedor auxiliar Diotronic

Ver `BOM_W_IND_36.csv`: Diotronic se contrasta **sólo** para pasivos, conectores y reemplazos de prototipado; no se declara stock en la tienda de Zaragoza. El **TPS3840PL42DBVR** tiene [ficha fabricante TI](https://www.ti.com/product/TPS3840), [referencia DigiKey España](https://www.digikey.es/es/products/detail/texas-instruments/TPS3840PL42DBVR/15857048) (catálogo consultado: **0,70 € + IVA 21% = 0,847 €**, MOQ 1 y stock web ~2900; cifra no reservada, sin transporte). La resistencia axial [Diotronic 10351](https://diotronic.com/resistencias-de-carbono-1w/16309-resistencia-10k-5-1w), catálogo histórico 0,15€ IVA MOQ5, **no** encaja con la huella 0805; [TME Yageo 0805](https://www.tme.eu/es/details/rc0805fr-0710k/resistencias-smd/yageo/rc0805fr-0710kl/) precio web 0,07€ IVA MOQ1 y stock general visto; el coste final puesto en Zaragoza sigue desconocido. Protección crítica TI siempre con documentación, identidad y trazabilidad verificables antes de comprar. Nada comprado.

## Autorías, licencias y HEAD verificados frente al maestro 19-alternativas el 30/10

- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, rama master **7c7858c0dd7040801b6f191df1396115560218f0**, igual al pin, PR#1 cerrada. **No se copia** circuito GPL.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2, master **08332bc398aa3350d351ef2aaac163f8007cffda** igual pin, PR#1 cerrada.
- [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2, **640kHz** HEAD **604eee2dffaeba3a270de61cf3dae887a33309c2**, diverge **68 ahead/11 behind** del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b, PR#40 abierta, NO fast-forward.
- [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2, master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5** igual pin, PR#153 cerrada.
- [openthread/openthread](https://github.com/openthread/openthread), BSD-3, main **e577777c308f6c87e5da3056239231a8fc147cb2**, **+14/0** del pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR#13820 pendiente, no integrada.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**; cleaning-jobs PR#79 **no se modifica**. Adaptación VALDO+OOMWOO, D22, acuerdo W/C, owners y otras automatizaciones revisados. Nada de Codex A67/A68, CAD ajeno ni clones upstream copiado.

Pinouts contrastados con hojas **TI TPS3840 SNVSB03E**, **SN74LVC1G08 SCES217AA (2026)** y **SN74LVC1G74 SCES794G**, DBV/DCU, y TI TPS25947. Las fuentes son referencias y sus creadores retienen autoría. Estos archivos Python/esquema/CSV son originales propios de VALDO.

## Siguiente paso técnico

Auditar y cualificar ELÉCTRICAMENTE el POR/CLR y los EN bajo retorno parásito, pulsadores rebotando y fallos de carga (SPICE/hojas TI), conectar la alarma **INA301** a una acción autónoma de corte sin radio y separar protección térmica/FOD TX. Tras ello definir huellas, DRC y eventual banco resistivo aislado sólo con seguridad y autorización específica. Sin litio/motores/estación.

### Incidencia ERC W36-01 resuelta dentro del hito

El primer CI nativo de 30/10 señaló **un error real de ERC**: dos fuentes ficticias J1/J5 compartían el retorno y ambos pines se declararon erróneamente `power_out`. Se corrigió **sólo** J5.RETURN a `passive`, manteniendo las dos fuentes de 5V y 3,3V separadas por etiqueta y el retorno común. Test de regresión añadido; no se ha suprimido ninguna regla ERC. La ejecución final y netlist nativo mandan sobre el test sintético.
