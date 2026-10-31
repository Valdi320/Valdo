# W-IND-51 — coste COMPLETO y precisión condicional de dos INA219 montados

**30/10/2026 · SOLO frente W del robot NUEVO, abierto y económico.** Sin trasplante Xiaomi, ni modificaciones de OOMWOO, PR #79, CAD C, Codex o clones upstream. Cero pruebas físicas, compras, soldaduras o baterías energizadas.

## Mejora real y verificable

W48 comparaba 2 circuitos INA219 *desnudos* (4,3076 € con IVA) con 2 placas INA260 (21,1024 €); **no eran presupuestos equivalentes**. W49 y W50 añadieron filtros de tiempo/CNVR/OVF. Ahora W51 permite evaluar **solo pares de medidores montados y reutilizables del banco**, no sensores integrados en cada robot, y **bloquea cualquier ganadora económica** si faltan IVA, cantidad mínima, entrega a Zaragoza, cableado, montaje, calibración, trazabilidad del shunt y existencias. Separa precio de catálogo de coste final y detecta saturación o error hipotético desmesurado de la resistencia de medición. Código original Python estándar: `w51_cost_metrology_gate.py`.

**Hallazgo nuevo de ahorro:** Satkit anuncia módulo MCU-219 **3,63 €/ud IVA incluido**, stock online limitado; 2 unidades **7,26 € de precio bruto de catálogo**. El anuncio del mismo vendedor en ManoMano indica shunt 0,1 Ω, 1 %, 2 W, **sin certificación de lote ni comprobación propia**. Frente a 2 placas INA260 BerryBase a 10,95 €/ud (21,90 €), hay una diferencia **de 14,64 € solo en precio de catálogo**, no ahorro neto de compra ni equivalencia funcional demostrada. Otra opción de INA219 ensamblado Soldered/BerryBase cuesta 7,20 €/ud (14,40 € el par), con shunt nominal 0,1 Ω. **No se elige proveedor todavía**.

## Requisitos cuantitativos, simulación, límites

Piloto **sensor no crítico**, carga resistiva ficticia: 5 V, 80 mA de corriente útil mínima y 300 mA de pico supuesto. Dos canales TX/RX por separado. Contrato W49/W50: objetivo 20 lecturas/s, alineación ≤25 ms, conversión INA219 CNVR/OVF, clocks y datos frescos; futura calibración externa. Nada de ello garantiza simultaneidad real ni seguridad eléctrica.

Con shunt 0,1 Ω y valores HIPOTÉTICOS: 80 mA → **8 mV, 0,64 mW**; 300 mA → **30 mV, 9 mW**. En el rango PGA elegido de **40 mV** cabrían ambos; **1 A → 100 mV** y **satura** ese rango. Presupuesto de error de corriente a 80 mA **2,1875 %** calculado como suma conservadora de shunt 1 % supuesto, ganancia 0,5 % condicional, offset 50 µV condicional y cuantización ±5 µV (medio paso 10 µV). Límite de diseño **3 %**. Es una *criba condicional*, no precisión medida de Satkit, sin deriva térmica, ruido, sincronización, errores de tensión ni incertidumbre global de eficiencia. Un shunt de 10 mΩ **no supera** ese presupuesto hipotético. La ficha de TI distingue variantes (50/100 µV offset): **no se ha verificado físicamente** cuál lleva el módulo comercial.

**No instalar INA219 en las protecciones críticas**: mide DC promedio, no prueba FOD, temperatura, EMI, picos rápidos, corte normalmente OFF ni seguridad de batería. El objetivo es **instrumentación reutilizable**, con un cable robusto y sustituible como alternativa de producción.

## BOM / comparación por pares (IVA, stock, MOQ, destino)

| Alternativa | Precio catálogo por 2 | Referencia y procedencia | MOQ / disponibilidad observada | Diotronic Zaragoza / entrega | Decisión |
|---|---:|---|---|---|---|
| 2 módulos MCU-219 0,1 Ω anunciado | **7,26 €** | [Satkit](https://satkit.com/sensor-de-corriente-ina219-i2c-mcu-219), [shunt anunciado](https://www.manomano.es/p/mcu-219-ina219-i2c-iic-sensor-de-fuente-de-alimentacion-de-corriente-continua-bidireccional-modulo-de-interrupcion-sensor-de-monitoreo-de-energia-35334049) | Venta unitaria aparente, stock web limitado | Envío total y calibración sin verificar | Candidato de menor precio anunciado; no autorizado |
| 2 Soldered INA219 SOL-333066 | **14,40 €** | [BerryBase](https://www.berrybase.de/en/soldered-ina219-spannungs-und-stromsensor-breakout-i2c-shunt-0-1-ohm-bis-26-v-3-2-a-qwiic) | Venta unitaria, stock web, valor shunt 0,1 Ω | Envío y calibración pendientes | Comparar en banco, no afirmar equivalencia |
| 2 INA260 ADA4226 | **21,90 €** | [BerryBase](https://www.berrybase.de/en/adafruit-ina260-high-or-low-side-voltage-current-and-power-sensor/) | Venta unitaria, stock web | Envío y calibración pendientes | Referencia; arquitectura de shunt distinta |
| 2 IC INA219BIDCNR desnudos | **4,3076 €** | [DigiKey España](https://www.digikey.es/es/products/detail/texas-instruments/INA219BIDCNR/2596849) | Venta unitaria, stock catálogo | Faltan PCB, shunt, montaje, cables, calibración y portes | **No equiparar al precio de un módulo completo** |
| Equivalentes Diotronic | **Sin precio verificado** | [Diotronic](https://diotronic.com/), proveedor **auxiliar** | SKU, MOQ, stock tienda Zaragoza pendientes | Recogida local solo cuando se confirme | Priorizar pasivos/conectores si equivalentes y competitivos |
| TME / Mouser / fabricante | **Pendiente** | Alternativas especializadas para partes críticas | Consultar stock, referencias, MOQ | Transporte, IVA y trazabilidad pendientes | Revisar antes de pedir seguridad eléctrica |

*Stock web ≠ stock físico en Zaragoza; ningún precio incluye todos los gastos o demuestra trazabilidad/calibración. No se ha añadido instrumento ni coste al robot de producción. Una oferta realmente comparable necesita dos canales, electrónica y cableado de adquisición, calibración y coste final entregado, además de protección eléctrica independiente (fuera de esta BOM de medición).*

## Reproducción y evidencia digital

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_51
python3 -m unittest discover -s . -p 'test_w51.py' -v
python3 w51_cost_metrology_gate.py --demo --out W51_SYNTHETIC_NOT_HARDWARE.json
```

**32/32 pruebas Python PASS** en entorno aislado antes de publicación (IVA, cantidad mínima, gastos ocultos, calibración/stock, datos faltantes, shunt, error, disipación y saturación). El workflow CI reproduce la batería y archiva JSON con `evidence_kind=SYNTHETIC-CATALOG-NOT-HARDWARE` y `hardware_approved=false`. Es **simulación aritmética y verificación de precios de catálogo**, NO medición, aprobación eléctrica, FOD ni autonomía real. El bloqueo histórico de ERC W-IND-18 no desaparece por el PASS de esta suite.

## Autores, licencias y revisión HEAD del 30/10/2026

Comparados PIN del maestro local `19-alternativas...`, GitHub API **rama por rama**, últimos commits y PR de cada titular (sin copiar código externo):

| Proyecto / licencia / rama | PIN 28/10 | HEAD 30/10 | Cambios del autor |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 `master` | `7c7858c0dd70` | **igual** | Gap del prototipo/PR #1 histórica; sin copiar GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause `master` | `08332bc398aa` | **igual** | Tuning y PR #1 histórica |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause **`640kHz`** | `d978a6978ad2` | `604eee2dffae` | **DIVERGIDO +68/-11**, CCS11, PR #40 abierta; NO fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 `master` | `c3b5f9be245f` | **igual** | IDF v6 / PR #153 cerrada |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause `main` | `7009584dadc2` | `e577777c308f` | **+14/-0**, radio/CLI/CI, PR #13822 abierta |

[OOMWOO oficial](https://github.com/makerspet/oomwoo) `main` HEAD `f01a1b295f46` (29/10: gráfico star-history; PR #79 cleaning-jobs ajena intacta). VALDO propia [PR #9](https://github.com/Valdi320/Valdo/pull/9) estaba en `eb86561d00f7` W50 antes del hito. Maestros leídos: NO_TRASPLANTE_X20, alternativas 19, D22, coordinación C/W, LEEME_PRIMERO y WPT_DATOS_V01. Worktree local de Valdo está ocupado por cambios ajenos, **se publicó exclusivamente en rama propia remota**; sin interferir con automaciones desactivadas.

## Separación y siguiente puerta

1. **Carga dock** independiente: BMS/estación/batería SIN conectar, sin pruebas de litio.
2. **Potencia a módulos**: cable desmontable económico por defecto; WPT solo tras demostrar coste de ciclo de vida, offset, EMI, temperatura, FOD y dos cortes autónomos realmente independientes.
3. **Datos**: ESP-NOW candidato frente a OpenThread; ACK **de aplicación**, CRC, secuencia, timeout, confidencialidad y recuperación, siempre separado de paradas críticas. WISP reservado a microsensores RFID.

**Bloqueos:** no hay dos medidores calibrados ni I²C real; shipping/MOQ firmado/stock Diotronic y cota física de error no verificados; W-IND-18 ERC histórico FAIL, FOD/temperatura/corte independiente sin validación. **Siguiente paso:** protocolo de calibración contra referencia externa y cotización completa puesta en Zaragoza; no energizar ni comprar nada.
