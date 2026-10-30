# W-IND-52 — calibración de tres puntos de dos medidores INA219 económicos (SOLO digital)

**30/10/2026 · Ámbito W, robot aspirador NUEVO, abierto, local, barato y reparable.** Sin trasplante Xiaomi OEM. Sin cambios OOMWOO, PR #79, mecánica C, clones de autores, estación, BMS ni batería. Sin compras ni energía aplicada. Se leyeron los cinco documentos maestros y el contrato de coordinación antes de actuar; el worktree PC de VALDO contiene trabajo ajeno y permanece intacto.

## Una mejora material sobre W49–W51

Los filtros W49–50 verificaban frescura/sincronía hipotética y W51 calculaba un margen de error **por especificaciones supuestas**; faltaba detectar que una placa INA219 barata concreta pudiera tener **shunt mal identificado, offset, polaridad, deriva o ganancia** y que se le atribuyese una precisión de 3% sin un patrón externo. W52 introduce un contrato ejecutable de **cero + fondo de escala + punto independiente de comprobación a 80 mA**. No necesita nuevos sensores dentro del robot: solo dos medidores de banco reutilizables.

`w52_calibration_gate.py` recibe **microvoltios brutos** (múltiplos de 10 µV, LSB INA219), cero, 80 mA y 300 mA con dos incertidumbres declaradas del patrón. Ajusta nominalmente la pendiente usando **solo cero y 300 mA**, y reserva 80 mA como comprobación ciega: su resultado debe caber en un presupuesto conservador de error con cuantización, incertidumbre de las dos lecturas de referencia y deriva térmica por TCR de shunt, ganancia y offset del chip. Rechaza lecturas invertidas, saturadas, no cuantizadas, incertidumbre sin cifra, referencia caducada, ventana térmica excedida, IDs duplicados TX/RX y falta de procedencia. **No prueba que las banderas de procedencia sean verdaderas**, por eso exige evidencia externa y siempre marca `hardware_approved=false`.

### Resultado reproducible sintético; no es una calibración

- **Caso favorable HIPOTÉTICO:** 0 mA→20 µV, 80 mA→8 020 µV, 300 mA→30 020 µV, patrón supuesto ±0,2 mA por punto, TCR shunt hipotético 100 ppm/°C, temperatura 25→27 °C, deriva de ganancia hipotética 167 ppm/°C y offset 0,5 µV/°C. Predicción nominal 80 mA; límite conservador **0,543%** en el punto de 80 mA. **Sigue bloqueado** por `source_kind=SYNTHETIC`, referencia/celda/certificados/temperatura no verificados.
- **Fallo inyectado:** con 6 420 µV a 80 mA, el modelo predice 64 mA; incertidumbre condicional **20,56%** y rechaza la calibración. No se ha observado este fallo en hardware.
- Aun con dos canales calibrados, la **eficiencia del WPT no queda calificada**: falta calibrar también bus de tensión, sincronía del reloj/I²C y verificar un enlace real, sin confundir medición DC con FOD/EMI. El software nunca autoriza el hardware.

### Condiciones que deberán constar en una futura ficha física

IDs físicos y variantes INA219B, identificación y TCR de cada shunt, patrón externo con certificado/fecha y precisión a 80/300 mA, carga introducida por el multímetro (*burden voltage*), cero corriente comprobado, temperatura real y cota de deriva, puntos crudos de shunt, PGA, polaridad, cálculo TX/RX por separado y archivo de registro íntegro. El multímetro doméstico DT-830B **no se declara patrón apto** sin su incertidumbre vigente y análisis de burden. El resultado de estos datos siempre requiere una revisión humana previa a energizar.

## Reproducción

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_52
python3 -m unittest discover -s . -p 'test_w52.py' -v
python3 w52_calibration_gate.py --demo --out W52_SYNTHETIC_NOT_HARDWARE.json
```

**32/32 tests Python PASS en contenedor aislado, no PC de Valdi**. La CI independiente repite tests, genera JSON, exige `hardware_approved=false`, confirma rechazo del fallo inyectado y archiva evidencia. Todas las entradas son ficticias. No se ha construido un driver I²C ni un patrón físico.

## Matriz de decisión y coste

- Banco: dos módulos INA219 MCU-219 Satkit, **3,63 €/u IVA incluido; 7,26 € por pareja de catálogo** (<https://satkit.com/sensor-de-corriente-ina219-i2c-mcu-219>), shunt 0,1 Ω 1% **anunciado**, disponibilidad web limitada; envío, calibración y stock físico Zaragoza pendientes. **No comprar**. La función W52 añade **0 € de electrónica al robot final**.
- Referencia patrón: instrumento existente o prestado, coste adicional pendiente; **ninguna precisión validada**. Comprar otro instrumento sin saber la incertidumbre sería gasto inútil.
- Alternativa: módulos INA260 o INA219 de vendedores con documentación; el coste completo se evaluará con W51, no comparando chips sueltos con placas.
- Diotronic auxiliar: sin SKU equivalente INA219 ni stock confirmado en tienda. Resistencias de catálogo de otros valores/tolerancias no son automáticamente shunts equivalentes; distribuidor especializado para referencias críticas.
- Ver `BOM_W_IND_52.csv` y `MATRIZ_W_IND_52.csv` (incluyen alternativas TME/Mouser/DigiKey, disponibilidad y motivo). No hay lista cerrada para comprar.

## Autorías y cambios HEAD revisados el 30/10/2026

Confrontados contra SHA del maestro local `19-alternativas...`:

| Autor / licencia / rama | PIN → HEAD | Cambios revisados |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, `master` | `7c7858c` → idéntico | PR #1 histórica; controlador sin feedback completo; **no se ha copiado GPL** |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause, `master` | `08332bc` → idéntico | PR #1 histórica; WISP solo microsensores RFID |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause, `640kHz` | `d978a69` → `604eee2` | **divergencia +68/-11**; CCS11 y PR #40, no asumir fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0, `master` | `c3b5f9b` → idéntico | IDF6 PR #153 cerrada; ACK de aplicación no sustituido |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause, `main` | `7009584` → `e577777` | +14/0 commits, radio/CLI/build; PR #13800/#13822 recientes; alternativa, no mezcla duplicada |

OOMWOO oficial [makerspet/oomwoo](https://github.com/makerspet/oomwoo) `main` HEAD `f01a1b295f46` del 29/10: solo gráfico *star-history*, PR upstream #79 ajena de cleaning-jobs, no toca W. VALDO PR propia #9 HEAD W51 `bb64cae613a04571e6f8ebdddefb7cc38b5b4e86` antes de W52; adaptación VALDO_OOMWOO y sus upstream son de terceros y no editados. Solo nuestra automatización W estaba activa entre las revisadas.

## Arquitectura, límites y seguridad

**Tres problemas distintos:** (1) carga inductiva de dock, NO aprobado y sin litio conectado; (2) potencia inductiva para pequeños módulos, requiere FOD/temperatura/offset/EMI y **corte autónomo normalmente OFF** antes de un montaje; (3) comunicación RF ESP-NOW candidata vs OpenThread con CRC, secuencia, ACK de aplicación, privacidad y timeout, sin uso para parada crítica. WISP no alimenta bombas o motores. Un cable corto protegido y reemplazable sigue siendo el valor económico predeterminado.

Pendientes: certificado/coste real de referencia, tipo de placa, ajuste térmico, mediciones a 80/300 mA, driver I²C, bus de tensión, reloj y ruido, ensayo físico supervisado, FOD/humedad/EMI/doble corte, compatibilidad CAD, pruebas de litio y estación. La **CI histórica W-IND-18 ERC falla de forma independiente**. Todo lo aquí descrito es software, no medición de fabricante ni autorización de ensayo.

Fuentes: [TI INA219 Rev.G](https://www.ti.com/product/INA219), [Satkit MCU-219](https://satkit.com/sensor-de-corriente-ina219-i2c-mcu-219), [W51](https://github.com/Valdi320/Valdo/blob/bb64cae613a04571e6f8ebdddefb7cc38b5b4e86/research/2026-10-28-independent-wpt-sensor-v01/w_ind_51/README_W_IND_51.md), [W50](https://github.com/Valdi320/Valdo/blob/eb86561d00f7a47be555dbc4f9c07f6062a2df15/research/2026-10-28-independent-wpt-sensor-v01/w_ind_50/README_W_IND_50.md).
