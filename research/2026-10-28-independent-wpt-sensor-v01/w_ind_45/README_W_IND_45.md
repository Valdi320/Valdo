# VALDO W-IND-45 — fuga del PMOS HEALTH en el receptor WPT (SIN hardware)

Fecha: 30/10/2026. Investigación original del sector W para el robot NUEVO abierto, local, reparable e imprimible. Cero trabajo Xiaomi OEM, batería, BMS, estación, motores, pruebas eléctricas o compra. No se toca el esquema W44; este hito es una **corrección del modelo de aceptación** y una **propuesta de resistor**, no una protección eléctrica integrada.

## Mejora material

El esquema diagnóstico W44 tiene TPS3700 OUTB (drenador abierto), BSS84LT1G Q1 y resistencia R4=47 kΩ de HEALTH a masa. El verificador de netlist/ERC no estudia la tensión producida por fugas del transistor cuando debería estar apagado. La ficha del fabricante [onsemi BSS84L Rev.14, abril 2024 p.2](https://www.onsemi.com/download/data-sheet/pdf/bss84lt1-d.pdf) documenta IDSS máximas 0,1 µA a VDS=-25 V/TJ25°C, 15 µA a -50 V/25°C y 60 µA a -50 V/125°C. **Estas cifras NO garantizan fuga a VDS de ~5 V.** Solo se utilizan como INYECCIONES HIPOTÉTICAS de estrés. La propia ficha advierte que no caracteriza condiciones de ensayo diferentes.

Modelo: V_HEALTH_OFF = min(Vfuente, I_inyectada * R4_max), con tolerancia **supuesta** ±1%, Vin hipotética 4,5/5/5,5 V y nivel OFF arbitrario **<=0,4 V**. No se conoce VIL real del receptor. Potencia ON = V²/R4_min solo en el modelo de transistor idealmente conductor (no RDSon real). 4 resistencias x 3 tensiones x 3 inyecciones = **36 escenarios sintéticos**.

| R4 | OFF con 60 µA y +1% | Margen contra límite supuesto de 0,4V | Potencia ON ideal 5V, -1% | Resultado hipotético |
|---|---:|---:|---:|---|
| 47 kΩ (W44) | 2,848 V | -2,448 V | 0,537 mW | 6/9 escenarios fallan |
| 10 kΩ | 0,606 V | -0,206 V | 2,525 mW | 3/9 fallan |
| **4,7 kΩ** | **0,285 V** | **+0,115 V** | **5,373 mW** | **9/9 pasan; candidato** |
| 2,2 kΩ | 0,133 V | +0,267 V | 11,478 mW | 9/9 pasan; más consumo |

**Decisión:** 4,7 kΩ es el candidato de menor consumo entre los 4 valores que cumplen únicamente ESTE ensayo, con ~4,836 mW más de consumo ON ideal que R4 actual. No afirmar que 47 kΩ falla realmente a 5 V: el fabricante no especifica esa fuga ni el límite de entrada del receptor; se ha descubierto una laguna de verificación que exige calificación real. Todos los resultados son hipótesis/cálculos, nunca medidas.

## Reproducción

    cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_45
    python3 -m unittest -v test_w45
    python3 w45_leakage_screen.py --out evidence/W45_SYNTHETIC_NOT_HARDWARE.json --csv evidence/tabla.csv

El workflow W45 ejecuta pruebas y archiva CSV/JSON etiquetados **NOT HARDWARE**. No se ha ejecutado SPICE, KiCad para W45 ni ensayo físico. El ERC de W44 era 0, pero no verifica este margen.

## Separación y límites

**Dock:** litio/BMS/estación aislados, sin piloto. **Energía WPT distribuida:** único candidato de microsensor ficticio 5 V/0,4 W promedio/1,5 W pico; sin par inductivo aprobado, eficiencia/offset/temperatura/FOD/EMI medidos. Aquí solo diagnosticamos un nodo HEALTH, no alimentamos el sensor. **Datos:** ESP-NOW y OpenThread son alternativas RF con ACK de aplicación, CRC, secuencia, timeout, privacidad/seguridad y recuperación por definir; WISP RFID solo para sensores de potencia ínfima. Ninguna radio alimenta módulos ni detiene funciones críticas.

**Bloqueos aún abiertos:** IDSS real de BSS84 a ~5V y temperatura; VIL/VIH/impedancia de entrada del receptor, polaridad/diodo de cuerpo, backfeed, POR TPS3700 bajo VDD, cortocircuito HEALTH a +5V, transistor/gate atascado, rearme local W37 real, doble corte normalmente OFF, FOD, térmica, metal, offset, humedad, EMI. La señal HEALTH sigue separada de EN. Ninguna autorización para energizar o modificar hardware.

## BOM y abastecimiento

Ver BOM_W_IND_45.csv: Panasonic **ERJ6ENF4701V** 4,7kΩ ±1% 0805 125mW [TME](https://www.tme.eu/en/details/erj6enf4701v/smd-resistors/panasonic/), disponible como referencia comercial, precio español final/stock/MOQ y transporte pendientes; [Reichelt España](https://www.reichelt.com/es/es/shop/producto/resistencia_smd_0805_4_7_kohmios_125_mw_1_-379219) anuncia el SKU a **0,15 € IVA incluido/ud, sin envío**, compra mínima mostrada 1 ud; no equivale a oferta final. **Diotronic Zaragoza** es auxiliar: precio final, equivalencia de SKU, existencias en tienda y MOQ NO verificados. Mouser/DigiKey por comprobar, sin compras. Las piezas críticas requieren hoja de fabricante/trazabilidad.

## Propiedad, revisiones exactas y licencias comprobadas 30/10

Leídos localmente: decisión 00 sin Xiaomi, alternativas 19/pines SHA, D22, coordinación W/C (ruta correcta bajo /coordinacion/cableado_inalambrico_acuerdo_20261027), VALDO_OOMWOO/LEEME_PRIMERO y WPT_DATOS_V01. Única automatización W activa; OOMWOO hourly detenido. Repo VALDO del PC tiene cambios ajenos pendientes: **no modificado**. Este commit se publica solo en **nuestra rama W / [VALDO PR #9](https://github.com/Valdi320/Valdo/pull/9)**, NUNCA OOMWOO [PR #79](https://github.com/makerspet/oomwoo/pull/79).

- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 master 7c7858c0dd7040801b6f191df1396115560218f0 = pin; PR #1 antigua, sin release.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause master 08332bc398aa3350d351ef2aaac163f8007cffda = pin; PR #1 antigua.
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause, **640kHz** HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 **diverge +68/-11** de pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; PR #40 abierta, no asumir avance lineal.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin, PR #153/#151 compatibilidad cerradas en 2026, release v1.0 antigua.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause main e577777c308f6c87e5da3056239231a8fc147cb2, **+14/-0** contra pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13822/#13819 abiertas 30/10 y release v2026.10.0 publicada 01/10.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, último cambio gráfico star-history; no modificación propia.

**No se copia código, diseños ni CAD de creadores; permanecen las autorías y licencias.** El siguiente paso (hito separado) será estudiar modelo eléctrico real a VDS=5V y recepción lógica/medida autorizada antes de cambiar el esquema diagnóstico y, mucho después, doble corte autónomo.
