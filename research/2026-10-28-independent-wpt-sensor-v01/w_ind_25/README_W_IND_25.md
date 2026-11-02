# W-IND-25 — Disparo analógico sub-500 mA: ventana condicional (29/10/2026)

**ORIGINAL W-only, simulación aritmética, no esquema aprobado ni prueba física. Ningún hardware puede energizarse.** El diseño es para un NUEVO robot abierto, no un trasplante Xiaomi. Se conserva intacto W-IND-24.

## Hallazgo y mejora

Dos eFuses candidatos con bloqueo inverso sano, TPS2521/TPS25947, tienen límite mínimo ajustable de 500 mA, por lo que pueden no detectar el ejemplo de fallo a 400 mA. Este hito estudia una **protección independiente**, NO la implementa. Se toma hipotéticamente una resistencia shunt 0.100 ohm +/-1% y un amplificador/comparador TI INA301A1 (ganancia nominal 20 V/V) para distinguir el pico normal supuesto de 300 mA del fallo supuesto de 400 mA, a una tensión de 5 V.

- Señal nominal calculada: **0.600 V a 300 mA** y **0.800 V a 400 mA**.
- Se exploran 8 esquinas por nivel (shunt 1%, ganancia 0.1% + deriva 10 ppm/C x 60C, offset 35uV + deriva 0.5uV/C x 60C); se usan hechos de la ficha TI sobre ganancia y offset, pero no se calibra un chip.
- **Los supuestos NO verificados** de un umbral efectivo de salida de 0.700 V, tolerancia de umbral +/-1% y +/-10 mV extra son exploratorios y NO características certificadas de INA301.
- Resultado de aritmética bajo esas hipótesis: máxima señal sana **0.60827168 V**, mínima señal de fallo **0.78943488 V**, umbral [0.683, 0.717] V; márgenes **74.72832 mV** antes de falso disparo y **72.43488 mV** para detección de fallo.
- Pérdidas ideales de shunt calculadas: **9 mW** a 300mA y **16 mW** a 400mA. No incluye pérdidas WPT ni calentamiento real.
- Con incertidumbre mucho mayor o corrientes más cercanas, la ventana desaparece: casos negativos incluidos. El tiempo de alerta anunciado por TI de ~1us no implica desconexión de alimentación en 1us. **LIMIT, su resistencia, la precisión real de comparación, fallos internos y el latch NO se han calificado**.

## Diseño futuro y límites

Ruta hipotética: fuente aislada 5 V -> corte A normalmente OFF con bloqueo inverso -> corte B independiente normalmente OFF -> shunt Kelvin -> TX de sensor con carga ficticia. INA301 requiere polarización verificada, configuración LIMIT por ecuaciones reales, alerta/latch de desconexión **autónoma**, y señal hardware de monitor-power-good. ALERT puede quedar alta impedancia sin VCC y NO basta como protección autónoma. Dos soldaduras de corte a la vez siguen peligrosas. No existe todavía esa etapa KiCad ni ERC/SPICE; FOD, térmica, sobrecorriente real, transitorios/EMI/agua/offset y fiabilidad quedan sin demostrar.

La interrupción **no depende de radio ni de firmware**. Dock de carga y batería/BMS fuera del alcance, completamente desconectados. ESP-NOW frente a OpenThread afecta únicamente a datos: ACK aplicación, CRC, secuencia, timeout, privacidad, recuperación (pendientes de integración). WISP solo justificaría microsensores RFID; no alimentación continua, motores, bombas ni turbina. Conservar cables/conectores de retención positiva como alternativa cuando resulten más baratos, simples y reparables.

## Reproducibilidad

Desde la raíz del repositorio:

    cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_25
    python3 -m unittest -v test_sub500_trip_window
    python3 sub500_trip_window.py > results.json

**33 tests originales PASS localmente**: 8 esquinas por extremo, casos negativos de límites, NaN/Inf, pérdidas ideales, seis condiciones lógicas con 64 combinaciones (solo una habilita), power-good fallido, térmica, FOD, dos cortes soldados. El flujo CI .github/workflows/w-ind-25-sub500.yml realiza los mismos tests y publica resultados JSON. Todas las salidas indican hardware_approved=false y power_on_allowed=false; PASS solo califica el modelo sintético, NO el circuito real. No hay prototipo alimentado.

## Matriz de decisiones

| Variante | RCB sano | Supuesto 400 mA | Protección autónoma real | Resultado |
|---|---|---|---|---|
| TPS22918 anterior | No demostrado, diodo reverso | Sin ILIM | No | Rechazar |
| TPS2521 solo | TI declara sí | ILIM mínimo 500 mA: hueco | No | Candidato antirretorno |
| TPS2521 + INA301A1 + shunt | TI declara sí para eFuse sano | Ventana solo bajo hipótesis de 0.7V y errores asumidos | **No diseñada** | Investigar KiCad |
| MOSFET enfrentados discretos | Posible con topología correcta | No cuantificado | No | Investigación |
| Cable protegido y sustituible | No aplica | Requiere protecciones del módulo | No evaluada | Mantener alternativa |

## BOM y proveedores

Archivo BOM_W_IND_25.csv. INA301A1IDGKR: referencia de catálogo DigiKey ES **2.77 EUR sin IVA / 3.3517 EUR IVA 21% calculado**, 4225 stock catálogo durante consulta, una unidad en cinta cortada; **no es stock local ni precio final puesto en Zaragoza**. El resto de MPN, precio total/IVA/envío/cantidad mínima, así como equivalencias y existencias Diotronic Zaragoza, TME/Mouser/DigiKey permanecen pendientes. Diotronic solo proveedor auxiliar. No hay compra ni fabricación. Para seguridad se requiere trazabilidad del distribuidor/fabricante, no equivalencias improvisadas.

## Fuentes, propiedad y rama de referencia revisadas el 29/10/2026

- Texas Instruments: INA301 https://www.ti.com/product/INA301 ; TPS2521 https://www.ti.com/product/TPS2521 ; catálogo INA301A1IDGKR https://www.digikey.es/es/products/detail/texas-instruments/INA301A1IDGKR/6571979 .
- Mark Belbin GPL-3.0 https://github.com/mark-belbin/simple-wireless-power , master 7c7858c0dd7040801b6f191df1396115560218f0 **igual pin**, resultados físicos del autor NO nuestros.
- WISP5 hardware BSD-2-Clause https://github.com/wisp/wisp5-hw , master 08332bc398aa3350d351ef2aaac163f8007cffda **igual pin**. WISP5 firmware BSD-2-Clause https://github.com/wisp/wisp5 , default 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 **divergido 68 ahead/11 behind** respecto a pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; no actualizar ciegamente.
- Espressif ESP-NOW Apache-2.0 https://github.com/espressif/esp-now , master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 **igual pin**. OpenThread BSD-3-Clause https://github.com/openthread/openthread , main 51aa078ee4fe1ad803bc83ca7b372e7ab62120f3, **9 commits ahead** de pin 7009584dadc20cf20c20a6062f357dd572ba6885; radio/CI, no integrados.
- OOMWOO oficial https://github.com/makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df. Nuestra PR VALDO #9 WPT distinta de makerspet/oomwoo #79 cleaning-jobs. C mecánica y Codex apoyo, ajenos. No se copió código ni CAD de terceros. Se revisaron decisión 28/10, D22, coordinación W/C, VALDO_OOMWOO/LEEME_PRIMERO y contrato WPT_DATOS_V01.

**Pendiente crítico:** leer ecuaciones y dispersión de LIMIT/alerta INA301 y diseñar circuitos realmente independientes de FOD/térmica/sobrecorriente/corte, incluso bajo pérdidas de alimentación y fallos comunes; ejecutar KiCad/ERC/netlist y simulación. Requerirá proceso de seguridad y autorización antes de un banco real de baja tensión. Sin batería, BMS, estación, OEM, compras, soldadura ni hardware probado.
