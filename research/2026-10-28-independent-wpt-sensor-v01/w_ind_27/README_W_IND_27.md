# W-IND-27 — selección económica del shunt y límite de error de terminales (29/10/2026)

**Ámbito exclusivo W — módulo nuevo de 5 V y muy bajo consumo.** No es un circuito KiCad listo para fabricación, ni prueba eléctrica de conformidad. El objetivo es resolver una laguna de W-IND-26: su shunt de 0,1 Ω estaba sin MPN, con TCR hipotético de 200 ppm/°C y sin error de soldadura/pistas. Se conserva W-IND-26 sin editar. No se utiliza electrónica Xiaomi ni se copia código de terceros.

## Mejora real y falsable

Se han identificado dos referencias comerciales **reales** de 100 mΩ: Vishay **WSL2512R1000FEA** (2 terminales, 1 W, ±1 %, ±75 ppm/°C) y VPG **Y44880R10000F9R** (4 terminales, 1 W, ±1 %, ±5 ppm/°C). El coste unitario mostrado por TME España para la primera es **0,53 € sin IVA, 0,64 € con IVA** (mínimo 1, existencias TME indicadas en catálogo, no verificadas en Zaragoza); para la segunda Farnell España muestra **16,12 € sin IVA, 19,51 € calculados con IVA** (mínimo 1; disponibilidad cambiante). Razón 30,4×, excluidos portes. La prioridad de precio sigue siendo la primera, **solo como candidata de evaluación**, nunca elegida definitivamente.

El INA301A1 utiliza una resistencia LIMIT de 8,66 kΩ (W-IND-26) y un shunt de 0,1 Ω. El programa `shunt_kelvin_screen.py` conserva las hipótesis transparentes: 300 mA de pico normal / 400 mA de fallo, excursión térmica de 100 °C, límite interno 79,2–80,8 µA, ganancia 20 V/V y sus errores TI, **otros 10 mV de comparador añadidos como reserva hipotética, no especificación garantizada**. En 2 terminales añade una resistencia de sensado extra supuesta de 0–5 mΩ (pistas, pads y soldadura; **no medida**). En 4 terminales supone 0–0,05 mΩ (**no garantizado por el fabricante**).

**Resultados aritméticos reproducibles:**

| Caso | Margen sin falso disparo a 300 mA | Margen para detectar 400 mA | Evaluación de la caja de hipótesis |
|---|---:|---:|---|
| WSL2512, R extra 0–5 mΩ, TCR 75ppm | **13,36656 mV** | **53,71244 mV** | ventana estática positiva, NO validación física |
| WSL2512, R extra 0–8 mΩ (fallo inyectado) | **−4,66944 mV** | 53,71244 mV | **falla** criterio de no disparo espurio |
| VPG 4-terminal, R extra 0–0,05 mΩ, TCR 5ppm | 47,33436 mV | 59,30124 mV | ventana estática positiva, NO validación física |

En el modelo, el límite exacto del parásito máximo para el WSL sin disparo espurio a 300mA es **7,2233 mΩ**; esto no es tolerancia admisible de PCB certificada ni límite medido. Un mal trazado puede anular la aparente ventaja del resistor económico. A 0,4 A nominales, el shunt pierde **40 mV** y disipa **16 mW**; no se han ensayado picos, pulsos, térmica del PCB ni EMI. El componente de 4 terminales también falla si su instalación induce 10mΩ de error (prueba negativa).

La diferencia principal entre 2 y 4 terminales es aislar la ruta de medición de parte de los cambios de resistencia de pistas/uniones. Pistas Kelvin hacia un encapsulado **de dos terminales** no equivalen automáticamente a 4 terminales Kelvin físicos. En ningún caso se conoce la resistencia/parasitaje efectivo del montaje. No se declara un costo-optimizado homologado por mera simulación.

## Reproducción

```bash
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_27
python3 -m unittest -v test_shunt_kelvin_screen
python3 shunt_kelvin_screen.py > RESULTS_REGENERATED.json
```

Fuente propia Python 3.10+, 20 pruebas deterministas con corrupción de supuestos, márgenes, 2/4 terminales, errores, precios y no-autorización. CI GitHub W-IND-27 ejecuta el mismo comando y archiva JSON. La validación de cada MPN y sus fechas de disponibilidad son **datos de catálogo de tercero**; todos los voltajes/márgenes son **simulación aritmética propia**; los parásitos térmicos y de pista son **hipótesis**; mediciones propias **cero**.

## BOM y decisión

Ver `BOM_W_IND_27.csv` (proveedor Diotronic auxiliar / alternativa TME, Mouser, DigiKey o Farnell, existencias reales locales pendientes) y `MATRIZ_W_IND_27.csv`. Como controles, la alimentación de comparador, el supervisor de arranque normalmente-OFF, el eFuse y el aislamiento inverso, dos cortes independientes, FOD, temperatura y EMI **siguen pendientes**. El bloqueo de corriente inversa solo puede atribuirse a referencias trazables, no al shunt. El dock de carga de litio, batería y BMS permanecen separados de este circuito hipotético. Los motores y bombas no pasan a WPT. RF ESP-NOW/OpenThread no participan en el corte crítico.

## Fuentes, licencias y ownership contrastados (29/10/2026)

- [TI INA301, SBOS713A](https://www.ti.com/lit/ds/symlink/ina301.pdf): A1 offset ±125 µV (no A3 ±35µV), LIMIT y ganancia; alimentación y ALERT no sustituyen supervisor autónomo.
- [TME España WSL2512R1000FEA](https://www.tme.eu/es/details/wsl2512r1000fea/resistencias-smd/vishay/) y [Mouser España](https://www.mouser.es/ProductDetail/Vishay-Dale/WSL2512R1000FEA): 100mΩ, dos terminales, ±1%, 1W, 75ppm; precio TME 0,53€ neto, catálogo indicaba >3000 unidades remotamente (NO stock local).
- [Farnell España Y44880R10000F9R](https://es.farnell.com/vpg-foil-resistors/y44880r10000f9r/current-sense-res-0r1-1-1w-2512/dp/4266769): 100mΩ, 4 terminales, 1W, ±1%, 5ppm, 16,12€ neto; stock web del momento **no reservado**.
- [Simple Wireless Power](https://github.com/mark-belbin/simple-wireless-power) autor mark-belbin **GPL-3.0**, `master` HEAD `7c7858c` = SHA local; PR #1 TX Board v1.1, referencia de potencia no usada en código.
- [WISP5 HW](https://github.com/wisp/wisp5-hw) **BSD-2-Clause**, `master` HEAD `08332bc` = SHA local; PR #1 de breakout/tuning. [WISP5 firmware](https://github.com/wisp/wisp5) **BSD-2-Clause**, rama default **`640kHz`** HEAD `604eee2` vs SHA local `d978a697` **divergencia 68 adelante/11 detrás**; PR #38 lector R420. No es alimentación continua de sensores de 0,4W y no se usa.
- [ESP-NOW](https://github.com/espressif/esp-now) **Apache-2.0**, `master` HEAD `c3b5f9b` = SHA local; PR #153 wakeup, datos RF. [OpenThread](https://github.com/openthread/openthread) **BSD-3-Clause**, `main` HEAD `e577777` **14 commits por delante** del SHA local `7009584`, cambios de API/radio/CLI/CI; PR #13819 de rx-on-when-idle, alternativa RF. Ninguno alimenta bobinas.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) HEAD `f01a1b2` (no editado); VALDO propia [PR #9](https://github.com/Valdi320/Valdo/pull/9), ajena a OOMWOO [PR #79 cleaning-jobs](https://github.com/makerspet/oomwoo/pull/79). Contratos VALDO_OOMWOO y reparto W/C conservados.

## Puerta siguiente

**No autorizar montaje.** Medir o demostrar por modelo de PCB validado el error efectivo de pads/pistas con trazado Kelvin y elegir finalmente shunt; después diseñar KiCad con alimentación protegida, ALERT y power-good, dos cortes normalmente apagados, bloqueo inverso, FOD y térmica. El escenario 400mA puede resultar inadecuado al medir carga real. Antes de cualquier banco con tensión se necesita procedimiento formal, aprobación y carga resistiva aislada. No compras, impresiones ni soldaduras.
