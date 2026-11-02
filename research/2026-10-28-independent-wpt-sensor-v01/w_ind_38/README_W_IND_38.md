# W-IND-38 — ruta de alarma INA301 al doble corte del receptor WPT (KiCad experimental)

30/10/2026. VALDO, ámbito propio W, robot NUEVO e independiente de Xiaomi. NO FABRICAR, NO ENERGIZAR NI CONECTAR BATERIA, BMS O ESTACION.

## Hito material

W-IND-36 tiene INA301 U1 con salida ALERT_N exclusivamente informativa; una sobrecorriente de su receptor no ordenaba ninguna desconexión. W38 añade en el esquema KiCad reproducible la ruta **U1 pin 6 ALERT_N → U4 pin 4 MR_N TPS3840PL28 → U4 pin 1 RESET_N → U10/U11 → U7/U8 CLR_N → Q bajos → U2/U3 EN/UVLO bajos**. Alarma activa-baja, reset asincrónico, enclavamiento local. Sin radio en este camino.

La resistencia existente R2 (10 kohm, pull-up del ALERT_N) pasa de 5V RX5_SOURCE a 3V3 MON_3V3_EXTERNAL, compartido por INA301 y el supervisor. U4.MR_N se retira de los no-conectados. U9.MR_N permanece sin conectar; NO se cortocircuitan dos salidas push-pull de 5V y 3V3. Se reutilizan los componentes existentes sin IC añadido, pero la cadena de corte conserva fallo común en U4.

Toda la modificación es nueva en W38; el generador histórico W32 y W36 permanece intacto. La CI genera los esquemas, netlist KiCad 9 nativo, ERC y auditoría por identidad de pines. Hay 14 pruebas deterministas originales + 32 combinaciones lógicas sintéticas; NO son medidas, no representan tiempo ni exactitud de silicio. Si la CI falla, no se afirma ERC PASS.

Reproducir en el directorio W38:
  python3 generate_w38.py
  python3 generate_w38.py --verify
  python3 -m unittest -v test_w38
  python3 netlist_gate_w38.py native_out/w38_native.xml --out native_out/w38_gate.json

## Por qué todavía NO es seguro

- La pérdida selectiva de VDD o fallo interno del INA301 deja su salida drenador-abierto flotante y la resistencia de pull-up puede simular ausencia de fallo. U4 supervisa el rail, no el estado interno del INA301. Faltan ventana EOL de W34 y medición independiente de salud de la alimentación.
- El rearme seguro W37 de liberar botones tras arranque, pulsar de nuevo y antirrebote sigue SOLO DIGITAL, no conectado en KiCad. Picos y transitorios no están modelados. El INA301 RESET está unido al 3V3 sin secuenciación física validada.
- Umbral receptor INA301 ~346,4mA bajo hipótesis W26; ni esa cifra, ni el fallo 400mA, ni el tiempo MR_N son medidas propias. Los eFuses TPS259470L comienzan límite ajustable alrededor de 500mA y no dan por sí solos discriminación sub-500mA.
- ILIM, ITIMER, OVLO, DVDT, FOD, temperatura y corte TX, offset de bobinas, metal, humedad, EMI, aislamiento real y doble fallo de los interruptores: pendientes. No PCB/DRC ni pruebas físicas.
- La fuente dibujada 3V3 no es regulador seleccionado. El aumento de temperatura y disponibilidad de potencia no están medidos. Litio y estación siempre desconectados.

## Tres sistemas independientes

(A) Dock carga/Li-ion: NO se trabaja ni conecta. (B) Alimentación inductiva distribuida del sensor: piloto hipotético 5V, ~0,4W promedio, ~1,5W pico; no extrapolar a motores ni bombas. (C) RF ESP-NOW vs OpenThread: solo datos; ACK de aplicación, CRC, número de secuencia, timeout, privacidad y recuperación están fuera de esta mejora y no sustituyen paradas físicas. WISP5 solo microsensores RFID intermitentes. Conservamos como alternativa arnés cableado reparable si WPT sale más caro o menos fiable.

## Auditoría de procedencia GitHub de 30/10/2026

- mark-belbin/simple-wireless-power (GPL-3.0), master 7c7858c0dd7040801b6f191df1396115560218f0 igual SHA maestro; PR #1 fusionada. https://github.com/mark-belbin/simple-wireless-power
- wisp/wisp5-hw (BSD-2-Clause), master 08332bc398aa3350d351ef2aaac163f8007cffda igual pin, PR #1 histórica. https://github.com/wisp/wisp5-hw
- wisp/wisp5 (BSD-2-Clause), rama 640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2 distinta del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b (68 ahead/11 behind según última auditoría); PR #40 abierta. https://github.com/wisp/wisp5
- espressif/esp-now (Apache-2.0), master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 igual pin; último commit 10/09/2026 de compatibilidad IDF6; PR #153 cerrada. https://github.com/espressif/esp-now
- openthread/openthread (BSD-3-Clause), main e577777c308f6c87e5da3056239231a8fc147cb2 distinto del pin 7009584dadc20cf20c20a6062f357dd572ba6885 (+14/0 en auditoría anterior). El HEAD de 29/10 añadió ajuste de BUILD.gn CLI; PR #13822 abierta 30/10, sin fusionar. https://github.com/openthread/openthread
- makerspet/oomwoo oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df; PR #79 cleaning-jobs de otro ámbito sin tocar. https://github.com/makerspet/oomwoo/pull/79

La decisión 00 de 28/10, maestro 19, D22, acuerdo W/C, VALDO_OOMWOO/LEEME_PRIMERO.md y WPT_DATOS_V01.md se leyeron antes de editar. Otras automatizaciones relevantes no estaban habilitadas. Sin reutilizar ni atribuir código/CAD de autores externos; referencias de TI solo documentación: https://www.ti.com/product/INA301 ; https://www.ti.com/product/TPS3840 ; https://www.ti.com/product/TPS25947 ; https://www.ti.com/product/SN74LVC1G74 .

## BOM, coste, siguiente puerta

BOM_W_IND_38.csv y MATRIZ_W_IND_38.csv: cero compra, cero nuevo IC, R2 ya presente. Diotronic solo auxiliar. SKU axial 10351 de catálogo histórico 0,15 EUR IVA MOQ5 incompatible con huella SMD sin PCB rediseñada. Alternativa Yageo TME 0805 ~0,07 EUR IVA históricamente; no es presupuesto final. Disponibilidad en Zaragoza de todos los componentes PENDIENTE; no se asume stock web local. Partes críticas TI necesitan verificación documental y trazabilidad de distribuidor.

Siguiente: supervisar salud propia del INA301 y detección de ALERT roto aun con VDD parcial; después implementar W37 en hardware, y estudiar FOD/temperatura independiente en TX. No aprobar energizar por un ERC verde.
