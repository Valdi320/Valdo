# W-IND-24 — Selección de verdadero bloqueo inverso (29/10/2026)

**Ámbito W exclusivamente. Datos de fabricante y pruebas de software. NO autoriza fabricar, energizar ni cargar.** Continúa el bloqueo W-IND-23, sin modificar su esquema ni archivos.

## Hallazgo de mayor retorno
El anterior **TPS22918DBVR** tiene diodo interno VOUT→VIN y carece de limitación de sobrecorriente. En comparación, TI declara auténtico bloqueo inverso con FET enfrentados:
- [TPS2521 Rev. A](https://www.ti.com/product/TPS2521): 2,7–5,7 V, RON típico 31 mΩ, Iq típico 411 µA, ILIM configurable **desde 0,5 A**. [Familia](https://www.ti.com/product/TPS2521).
- [TPS25947 Rev. C](https://www.ti.com/product/TPS25947): 2,7–23 V, RON típico 28,3 mΩ, Iq típico 426 µA, ILIM **desde 0,5 A**.

El primer módulo es una **hipótesis** de 5 V, 0,4 W promedio (80 mA), 1,5 W pico (300 mA). Un **fallo ejemplar supuesto de 400 mA** queda por debajo del límite mínimo ajustable de ambos eFuses: son candidatos razonables para antirretorno, pero **NO son por sí mismos la protección de corriente adecuada al sensor**. Tampoco reclamar precisión de salida ILM a 80 mA: los fabricantes especifican su precisión principal para corrientes de alrededor de 1 A o superiores. Un transistor interno en corto anula la garantía de bloqueo bajo ese fallo. Sigue siendo necesaria protección autónoma de menor corriente, FOD físico, térmica y dos órdenes locales independientes normalmente OFF.

## Evidencia reproducible y decisión
`reverse_block_qualification.py` calcula el sobreconsumo teórico a partir de Iq/RON **típicos** y comprueba rango, limitación, corto sintético y puertas de seguridad. **20 tests originales** en `test_reverse_block_qualification.py` verifican la lógica. Ejecutar:
```bash
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_24
python3 -m unittest -v test_reverse_block_qualification
python3 reverse_block_qualification.py > qualification.json
```
CI `.github/workflows/w-ind-24-efuse-screen.yml`: pruebas y JSON descargable; `hardware_approved=false` siempre. Pérdida de TPS2521 a 80 mA: **2,2534 mW típicos calculados**; no representa pérdidas del enlace WPT ni máxima disipación térmica.

| Elección | Inversión de corriente (sano) | Detectar hipotéticos 400 mA | Coste/mantenimiento | Veredicto |
|---|---|---|---|---|
| 2 TPS22918 | NO demostrado (diodos) | No (sin ILIM) | Circuito previo barato, peligro | Bloqueado |
| TPS25210ARPWR | Sí, según TI | No, ILIM mínimo 0,5 A | QFN 2×2 poco reparable a mano: cambiar placa | Candidato no aprobado |
| TPS259474ARPWR | Sí, según TI | No, ILIM mínimo 0,5 A | Igual, VIN más amplio | Alternativa no aprobada |
| Back-to-back MOSFET discretos | Teórico sin esquema/protección | No demostrado | Más piezas, quizá mejor reemplazo | Pendiente |

BOM `BOM_W_IND_24.csv`: cero compras. [DigiKey](https://www.digikey.es/en/products/detail/texas-instruments/TPS25210ARPWR/14124025) muestra **1,07 € unidad sin IVA** (1,2947 € calculados al 21%, portes excluidos), 2409 en stock en captura de catálogo, **NO en Zaragoza**; precio/cesta sujeto a confirmación. [Mouser ES](https://www.mouser.es/es/c/semiconductors/power-management-ics/voltage-regulators-voltage-controllers/hot-swap-voltage-controllers/?m=Texas+Instruments) lista `TPS25210LRPWR` alrededor de 1,05 € y existencias, **no asumir equivalencia de las variantes A/L**. Diotronic auxiliar: referencia/stock local, precios con IVA y cantidad mínima **no verificados**; TME pendiente. Documentación y trazabilidad del fabricante son obligatorias para seguridad.

## Licencias, fuentes y coordinación (HEAD del autor 29/10 frente a pins 28/10)
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, `master=7c7858c0` igual pin; no copiar fuente.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause, `master=08332bc3` igual pin; RFID microscópico.
- [wisp/wisp5](https://github.com/wisp/wisp5/tree/640kHz) BSD-2-Clause, `640kHz=604eee2d` vs `d978a697`, **68 ahead/11 behind DIVERGED**; no autopromoción.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0, `master=c3b5f9be` igual pin, 0 PR abiertas visibles; datos RF solamente.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause, `main=51aa078e` vs `7009584d`, **9 ahead**, cambios radio/CI; revisión de PR #13784 de filtrado PAN. Sin integración.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) oficial `main=f01a1b29`, +1 cambio de imágenes SVG respecto al pin `1c2bd43a`, no relacionado. PR upstream #79 cleaning-jobs pertenece a otro ámbito; intocable. Nuestra contribución propia: [Valdi320/Valdo PR #9](https://github.com/Valdi320/Valdo/pull/9).

Se leyeron decisión 28/10, D22, acuerdo W/C, `LEEME_PRIMERO` y `WPT_DATOS_V01`; los clones, CAD y otros agentes no han sido modificados. **Dock de carga y batería/BMS siguen desconectados; módulo de sensor es solo un concepto; ESP-NOW/OpenThread y ACK/CRC/seq/timeout/recovery no equivalen a seguridad eléctrica; WISP no resuelve potencia continua.** Siguiente paso: esquema KiCad separado con eFuse antirretorno y protección independiente de corriente por debajo de 0,5 A, FOD y temperatura, después ERC/Spice. Cero pruebas físicas, alimentación, soldadura, compras y firmware.
