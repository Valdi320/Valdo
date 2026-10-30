# W-IND-48 — Metrología económica y conservadora para el primer sensor (30/10/2026)

**Robot abierto e INDEPENDIENTE. Solo sector W.** Se publica un verificador original de energía en Python estándar: dos trazas de tensión/corriente (TX y RX), eficiencia con incertidumbre declarada, rechazos de muestras inválidas y SHA-256 de fuentes. **31/31 pruebas sintéticas PASS antes de publicar**. No hay medidas propias en hardware, placa, batería, WPT o estación energizada.

## Mejora medible y retorno
Evita comprar dos monitores caros **por módulo**: propone medidores de bancada reutilizables y exige datos suficientes antes de justificar sustitución de arnés por bobinas. W47 demuestra que WPT simple no sustituye por sí mismo cinco hilos, radio y protecciones; W48 añade una *puerta energética auditable* que rechaza desfase de relojes, pérdidas de filas, datos inválidos, energía de entrada cero, huecos y falsa ganancia energética. **No confundir esta herramienta con autorización eléctrica.**

### Entradas/salida
`tx.csv` y `rx.csv`, encabezado exacto `t_ms,v_volts,i_amps`, 3+ muestras por lado en el mismo número y orden; `config.json` con `mode` = `synthetic` o `measured`, dos incertidumbres relativas de **potencia** (no automáticas), `max_skew_ms`, `max_gap_ms` y `min_efficiency`. En modo `measured`, requiere declaraciones `battery_disconnected=true`, `source_kind=isolated_current_limited`, `load_kind=resistive` y `calibration_ref`; esos metadatos los aporta el operador, **no se verifican solos**.

Integración trapezoidal por lado: `E = integral(V*I dt)`, `eta=E_rx/E_tx`. Bajo hipótesis de incertidumbre de potencia relativa `u_tx,u_rx`: `eta_lower=eta*(1-u_rx)/(1+u_tx)` y `eta_upper=eta*(1+u_rx)/(1-u_tx)`. La cota incluye shunt, calibración, rango, offset, temperatura, aliasing y sincronización **solo si se han acotado en los valores que suministra el operador**. Los transitorios con acumulación de energía en el enlace requieren balance y ventana adecuada.

### Resultado de demostración, EXCLUSIVAMENTE SINTÉTICO
21 muestras a 50 ms, 1 s; entrada 5 V×0,10 A = 0,50 W, salida 5 V×0,08 A = 0,40 W. **0,500 J entrada, 0,400 J salida, η nominal 80 %, cota inferior 75,34 %, superior 84,95 %** con incertidumbre **HIPOTÉTICA** ±3 % de potencia por lado. Umbral hipotético 70 % pasa la criba energética, pero `hardware_approved=false` y `battery_or_dock_approved=false` permanentemente. No se ha demostrado eficiencia del robot.

Reproducir desde `w_ind_48/`:

```sh
python3 -m unittest -v test_w48
python3 w48_meter_gate.py --demo --out W48_SYNTHETIC_NOT_HARDWARE.json
python3 w48_meter_gate.py --tx tx.csv --rx rx.csv --config config.json --out result.json
```

El último comando requiere trazas externas y configuración reales; no se proporcionan mediciones. Workflow W48 genera artefacto JSON explícitamente sintético.

## Instrumentación y coste económico: candidatos, NO compras
- [TI INA219](https://www.ti.com/product/INA219): bus 0–26 V, I2C, ADC 12 bits, 3–5,5 V de alimentación de chip, max Iq 1 mA, variantes A/B con precisión diferente. **Dos chips** [INA219BIDCNR DigiKey España](https://www.digikey.es/es/products/detail/texas-instruments/INA219BIDCNR/2596849) 2×2,1538 € = **4,3076 € IVA**. Stock web y MOQ 1; **no** incluyen shunt, PCB, montaje, cables, calibración ni envío. Sin homologación como sistema completo.
- Comparación **no equivalente**: **dos placas completas** [Adafruit INA260 4226 DigiKey](https://www.digikey.es/es/products/detail/adafruit-industries-llc/4226/10130492), 2×10,5512 € = **21,1024 € IVA**, portes aparte. **No afirmar 16,79 € de ahorro neto** entre placa y chip desnudo.
- [Mouser INA219](https://www.mouser.es/en/c/?q=INA219): variante B 1,75 €/ud indicada; IVA/porte y referencia exacta a verificar. [TME INA219AIDR](https://www.tme.eu/en/details/ina219aidr/smd-operational-amplifiers/texas-instruments/): variante A SOIC, cotización portal EN en USD, no equivalente en grado ni formato.
- Diotronic [ACS712/20](https://diotronic.com/sensores-de-corriente/20430-m%C3%B3dulo-de-sensor-de-corriente-ca-cc-de-rango-20a-30a) **7,08 € IVA** módulo, web disponible: **rechazado** para el piloto 80 mA, porque sensibilidad 100 mV/A arroja solo 8 mV. Precio/stock físico de Zaragoza y MOQ sin confirmar. Diotronic permanece auxiliar para pasivos y conectores; sin atribuir equivalencia inexistente.
- BOM, matriz y portes/montaje no verificados están declarados como pendientes en CSV. **Nada comprado.**

Contrato futuro de puntos de medición, no KiCad físico: **fuente limitada aislada → monitor TX DC → corte TX autónomo normalmente OFF → TX bobina || RX bobina → regulador RX → monitor RX DC → carga resistiva**. Incluir todos los consumos del enlace donde corresponda. INA219 o INA260 son **instrumentos de observación**, nunca protección de sobrecorriente/FOD/térmica; no miden ripple/EMI de alta frecuencia, que requerirá instrumentación independiente. Tampoco hay pruebas sobre desplazamiento de bobinas, FOD metal, humedad, temperaturas, reconexión, radio, datos o litio. Ningún motor o bomba con WPT por defecto.

## Matriz arquitectónica
**Arnés reparable provisional** para sensores normales; **WPT DFR0362** solo posible experimento no crítico después de revisar FOD, temperatura, EMI, offset, desconexión y coste integral; **WPT regulado con FOD** sin controlador aprobado; **dock de carga** separado, batería/BMS desconectados. **ESP-NOW / OpenThread** son únicamente datos y requieren ACK de aplicación, CRC, secuencia, timeout, cifrado/autenticación y recuperación; la parada crítica siempre local. **WISP** solo microsensores RFID, no motores.

## Titularidad y revisiones auditadas el 30/10/2026
Documentos maestros locales decisión 00/alternativas 19/D22, coordinación C/W (C mecánico, W eléctrico), `VALDO_OOMWOO/LEEME_PRIMERO` y `WPT_DATOS_V01` leídos. El worktree X20 local contiene cambios ajenos: **no se edita**. Se publica solo en [VALDO PR #9](https://github.com/Valdi320/Valdo/pull/9). OOMWOO oficial PR#79, C/IF14, clones upstream y electrónica OEM intactos.
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) (GPL-3.0), `master` `7c7858c0...` = pin 28/10; sin release nuevo/PR #1 histórica.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause `master` `08332bc3...` = pin.
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause **`640kHz`** `604eee2d...` vs `d978a697...` = **68 adelante / 11 detrás**, no fast-forward. PR #40 información abierta.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 `master` `c3b5f9be...` = pin; PR #151 ya cerrada.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause `main` `e577777c...` = **14 ahead / 0 behind** pin `7009584d...`, cambios BUILD.gn/radio/UDP; release v2026.10.0 de 01/10.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) main `f01a1b29...` último 29/10 (star-history); no módulo W integrado. VALDO PR #9 HEAD anterior W47 `ce5a34d5...`. Ninguna fuente externa copiada.

**Siguiente puerta:** cotizar dos medidores montados equivalentes con materiales, portes y calibración; documentar reloj y error total. Separar carga de estación, distribución a módulos y radio. **Sin** soldar, imprimir, comprar, energizar, flashear ni conectar litio.
