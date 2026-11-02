# W-IND-49 — adquisición energética económica sin falsa sincronía (30/10/2026)

**Solo sector W del robot NUEVO independiente, cero ensayos físicos.** Sin cambios Xiaomi OEM, mecánica C, OOMWOO, estación, batería o BMS. Se revisaron documentos maestros locales decisión 00/alternativas 19/D22, coordinación C/W, VALDO_OOMWOO/LEEME_PRIMERO y contrato WPT_DATOS_V01; el worktree X20 tiene cambios ajenos que no se tocan.

## Una mejora real sobre W-IND-48

W48 acepta sellos t_ms TX/RX con diferencia inferior a 25 ms, pero **no** comprueba la separación temporal entre las conversiones internas de tensión de shunt y bus. Texas Instruments INA219 Rev.G Table 5 explica tiempos de conversión independientes: 12 bits, 1 muestra **0,532 ms**, promedio 16 **8,51 ms** y promedio 128 **68,10 ms** por ADC. Para medir V e I hacen falta las dos conversiones. Un par de medidores que reporten sellos PC idénticos puede entregar potencia con muestras V/I temporalmente distintas, más aún con 128 promedios.

W49 incorpora una puerta de selección de hardware y régimen de adquisición que suma conservadoramente **2 × tiempo por ADC + skew TX/RX declarado**, exige periodo de registro no inferior a las dos conversiones y confronta caída de shunt frente a offset del chip a 80 mA. El modelo da **candidatos, nunca una garantía de sincronización física**: faltan reloj real, ready/trigger, fase de lectura, jitter, offset, shunt medido, temperatura, ganancia, rizado y EMI. El filtro no permite afirmar una precisión total; no decide FOD.

### Ejemplos estrictamente sintéticos (no mediciones)

Hipótesis: bus 5V, corriente mínima 80mA, pico 300mA, periodo 50ms, skew de host *supuesto* 5ms, límite temporal supuesto 25ms, INA219B con offset máximo **supuesto por variante** 50µV, contribución máxima de offset propuesta 2%. Rango de shunt utilizado 40mV.

| Opción | 2 conversiones | Presupuesto con 5ms de skew | Caída a 80mA | Error relativo por offset | Criba |
|---|---:|---:|---:|---:|---|
| 100mΩ/16 promedios | 17,02ms | 22,02ms | 8mV | 0,625% | Candidato digital |
| 10mΩ/16 promedios | 17,02ms | 22,02ms | 0,8mV | 6,25% | Rechazar para 80mA sin calibración |
| 100mΩ/128 promedios | 136,20ms | 141,20ms | 8mV | 0,625% | Rechazar a 20Hz |
| 100mΩ/1 promedio | 1,064ms | 6,064ms | 8mV | 0,625% | Temporalmente candidato; ruido pendiente |

*No son errores globales medidos del módulo DFRobot ni garantías de seguridad.* La variante real del chip y resistencia, compensación y referencia de reloj se deben identificar.

### Reproducción

cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_49
python3 -m unittest -v test_w49
python3 w49_ina219_acquisition_gate.py --demo --out W49_SYNTHETIC_NOT_HARDWARE.json

Pre-publicación: **34/34 pruebas Python PASS**. El workflow independiente CI W49 repetirá pruebas y archivará JSON explícitamente sintético, que no demuestra funcionamiento físico. W-IND-18 ERC histórica permanece fallando por separado.

### BOM y decisiones

Véanse BOM_W_IND_49.csv y MATRIZ_W_IND_49.csv. No comprar: precio web de la pareja montada Berrybase 0,1Ω 7,40 € con IVA **más envío** (origen/calibración chip por confirmar); frente a dos placas Soldered ~15 € catálogo (IVA aplicable a España por verificar), dos placas DFRobot SEN0291 0,01Ω 14,3022 € IVA DigiKey, o dos chips INA219B sueltos 4,3076 € IVA DigiKey **sin PCB ni shunt ni soldadura**. Diotronic ACS712/20A no es equiparable a la instrumentación de 80mA; stock físico Zaragoza y portes finales no confirmados. La medición se queda en banco reutilizable, nunca se añade un registrador caro por sensor final.

**Tres problemas separados:** dock de carga inductivo con FOD/temperatura y corte independiente (SIN litio); alimentación WPT de pequeños módulos solo si gana económicamente a cable desmontable; datos ESP-NOW/OpenThread con ACK de aplicación, CRC, secuencia, timeout y autenticación, nunca para parada crítica. WISP5 solo microsensores RFID. Simple WPT no aprobado para carga regulada; no proponer WPT para bombas ni motores.

### Auditoría upstream, propietarios, PIN y cambios (GitHub, 30/10/2026)

- mark-belbin/simple-wireless-power GPL-3.0, master 7c7858c0dd70 = PIN; PR #1 histórica, sin release reciente. No copiar código.
- wisp/wisp5-hw BSD-2-Clause, master 08332bc398aa = PIN; PR #1 histórica.
- wisp/wisp5 BSD-2-Clause, **640kHz** 604eee2dffae frente a PIN d978a6978ad2: **68 ahead/11 behind, divergido**; PR #40 abierta 2021. NO fast-forward.
- espressif/esp-now Apache-2.0, master c3b5f9be245f = PIN; PR #153 cerrada 2026-02, release v1.0 (2022).
- openthread/openthread BSD-3-Clause, main e577777c308f vs PIN 7009584dadc2: **14 ahead/0 behind**, radio/CLI/build/test; release v2026.10.0 publicada 01/10, PR #13666 abierta 30/10.
- makerspet/oomwoo main f01a1b295f46 del 29/10: actualización gráfica [skip ci], sin novedad de W. VALDO PR #9 HEAD previo W48 29074fb3438d. No se tocan upstream, CAD C, PR#79 cleaning-jobs ni autorías de terceros.

### Bloqueo / siguiente prueba

*Una puerta digital PASS no aprueba electricidad.* Faltan verificación de tiempos internos con conversion-ready, calibración de dos monitores, medición real de shunt y coste puesto en Zaragoza. Independientes y sin aprobar: corte normalmente apagado, FOD metálico real, humedad, offsets bobinas, temperaturas, EMI, BMS/cargador y litio. Próxima mejora útil solo con estas evidencias (banco aislado con carga resistiva y aprobación expresa). No compras, instalaciones, soldadura, impresiones ni energizaciones.

**Fuentes:** https://www.ti.com/lit/ds/symlink/ina219.pdf ; https://www.ti.com/product/INA219 ; https://wiki.dfrobot.com/sen0291/ ; https://www.berry-base.com/es/ina219-stromsensor-mit-breakoutboard ; https://soldered.com/collections/sensors-modules/products/voltage-current-sensor-ina219-breakout ; https://www.digikey.es/es/products/detail/dfrobot/SEN0291/10279750 ; https://www.digikey.es/es/products/detail/texas-instruments/INA219BIDCNR/2596849 ; https://diotronic.com/sensores-de-corriente/15224-sensor-de-corriente-acs712-20a ; https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread
