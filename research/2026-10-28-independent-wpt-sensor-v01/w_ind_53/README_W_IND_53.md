# W-IND-53 — Calibración digital de tensión INA219 TX/RX para robot NUEVO y barato

**30/10/2026, ámbito propio W, solo digital/sintético.** No trasplante Xiaomi OEM, no clon upstream editado, no modificación OOMWOO, PR #79, mecánica C, estaciones, baterías o BMS. El árbol de trabajo local VALDO estaba sucio por trabajo ajeno y no se tocó.

## Una mejora material sobre W50/W52

W50 verifica frescura/tiempo de muestras; W52 comprueba **corriente** con INA219 baratos. Sin calibración separada de la **tensión**, la eficiencia DC inductiva puede parecer buena por un error de escala aun si la corriente está bien. Se añade un contrato de **3 puntos**: referencias de 3,000 y 6,000 V para ajustar la relación; una comprobación independiente al nivel previsto (TX 5,000 V, RX 4,000 V) que **no participa** en el ajuste. Dos placas físicas con IDs distintos. El software rechaza tensiones invertidas, fuera de rango 0–26 V, pasos que no sean múltiplos del LSB 4 mV, errores de escala, límites de incertidumbre inexistentes o inválidos, fecha de calibración caducada, temperatura fuera de ventana, deriva no acotada e identidades faltantes.

La cota de peor caso es **aritmética de intervalos**, no porcentaje de confianza: incluye ±2 mV de cuantización en cada uno de los 3 registros, incertidumbre de cada lectura del patrón y deriva térmica declarada. Exige trazabilidad del patrón, identidad de placa, holdout independiente, temperatura real, evidencia de adquisición y reloj. Esas banderas pueden falsearse; el programa **jamás** convierte una etiqueta BENCH_MEASURED en autorización de ensayo: `hardware_approved=false` siempre.

### Caso sintético ejecutable, NUNCA medida física

- Hipótesis: patrón ±3 mV en los tres puntos, temperatura 25→27 °C, deriva teórica 200 ppm/°C y 0,5 mV/°C; tolerancia condicional máxima 2%.
- TX 5,000 V frente a referencia 5,000 V: cota condicional **0,2682%**.
- RX 4,000 V frente a referencia 4,000 V: cota condicional **0,3353%**.
- RX defectuosa simulada con 3,840 V frente a 4,000 V: **4,3383%**, rechazada.
- 33 pruebas unitarias sintéticas de aceptación y fallos inyectados. Ninguna lectura I²C real.

### Reproducir sin comprar nada

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_53
python3 -m unittest discover -s . -p 'test_w53.py' -v
python3 w53_bus_voltage_gate.py --demo --out W53_SYNTHETIC_NOT_HARDWARE.json
```

La CI propia ejecuta estas pruebas, genera JSON y comprueba que ninguna protección ni eficiencia esté aprobada. La ejecución de prueba previa a publicar fue **33/33 PASS en contenedor aislado**, no en el PC de usuario. Código, tests, BOM y matriz están en este directorio; GitHub Actions archiva JSON regenerado. No se declara simulación electromagnética ni metrología real.

## Coste, decisiones y separación de funciones

- **Coste adicional en el robot final: 0 €**: programa y medidores reutilizables en un banco, sin añadir electrónica por sensor. Los dos módulos MCU-219 Satkit anunciados anteriormente a **3,63 €/unidad IVA incluido, pareja 7,26 €** son candidatos sin compra, portes, calibración o stock entregado confirmado. La ficha alterna “stock limitado” con una FAQ “agotado”, por lo que **no se presupone disponibilidad**. El patrón calibrado/prestado y su incertidumbre/fecha tienen coste por determinar.
- Alternativa TME [MIKROE-4039 INA260](https://www.tme.eu/es/details/mikroe-4039/placas-de-expansion/mikroe/) 26,80 € IVA por placa (53,60 € pareja), más portes/calibración; no es equivalente económicamente. DigiKey/Mouser sirven de alternativa trazable, con SKU por concretar. Diotronic queda **auxiliar** para cables/terminales adecuados, no como referencia de calibración sin datos, no hay stock verificado en Zaragoza, IVA final/MOQ pendientes.
- En el robot barato **cable corto sustituible por defecto**; solo añadir WPT a módulos no críticos si un ensayo demuestra beneficios frente a precio, pérdidas, EMI y mantenimiento. Motores y bombas NO se alimentan por inducción sin presupuesto medido.
- Tres problemas distintos: (1) **dock** inductivo/recarga con BMS y cargador: no integrado ni conectado; (2) **WPT de módulos**: todavía sin FOD, temperatura, offset, humedad, EMI, protección autónoma normalmente OFF y doble corte validados; (3) **datos RF**: ESP-NOW candidato frente a OpenThread, con ACK de aplicación, CRC, secuencia, timeout, autenticación/cifrado y recuperación. La radio nunca es la parada crítica. WISP5 solo para microsensores RFID si el coste total compensa.

## Actualidad y autoría verificada el 30/10/2026

Comparado con los SHA del maestro local “19-alternativas-abiertas” (PIN 28/10); se verificaron **rama, HEAD, compare y PR de los creadores**, sin copiar código ni CAD ajeno:

| Dueño/proyecto (licencia y rama) | PIN → HEAD | Diferencia/PR |
|---|---|---|
| [Mark Belbin, Simple Wireless Power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, master | 7c7858c → 7c7858c | 0 cambios; PR #1 histórica, sin controlador/FOD certificados |
| [WISP5 hardware](https://github.com/wisp/wisp5-hw) BSD-2-Clause, master | 08332bc → 08332bc | 0 cambios, PR #1 histórica |
| [WISP5 firmware](https://github.com/wisp/wisp5) BSD-2-Clause, **640kHz** | d978a69 → 604eee2 | **DIVERGIDA** +68/-11, código CCS11, PR #40 abierta histórica |
| [Espressif ESP-NOW](https://github.com/espressif/esp-now) Apache-2.0, master | c3b5f9b → c3b5f9b | 0 cambios; IDF6, PR #153 cerrada |
| [OpenThread](https://github.com/openthread/openthread) BSD-3-Clause, main | 7009584 → e577777 | +14/-0; radio/CLI/build, PR #13800 y #13822 abiertas |

[OOMWOO oficial makerspet/oomwoo](https://github.com/makerspet/oomwoo) main HEAD f01a1b295f46, último cambio conocido gráfico de stars; PR #79 pertenece a limpieza ajena. La adaptación VALDO_OOMWOO está aislada con 10 clones oficiales y contratos no modificados. Única automatización activa para este ámbito: W. Licencia global de VALDO aún por determinar; nuestro código es original y no incorpora fuentes GPL/BSD/Apache externas.

## Bloqueos y punto dulce

Faltan patrón de tensión trazable, calibración **física** TX y RX, adquisición I²C real y reloj, corriente W52 validada, costes entregados, FOD, térmica, EMI, cortes independentes y seguridad de estación. El DT-830B no se presupone patrón válido. El ERC histórico **W-IND-18** falla debido a defectos de un esquema no cualificado: este hito no lo oculta. **0 ensayos físicos; hardware_approved=false.**

**Siguiente paso rentable:** conseguir un instrumento de tensión calibrado/prestado y mediciones supervisadas con autorización de seguridad en fuente aislada, sin batería. Otra capa de simulación de calibración tendría retorno marginal inferior a esa medición; consolidar esta especificación mientras falta hardware.

Fuentes: [TI INA219 Rev.G](https://www.ti.com/product/INA219), [Satkit MCU-219](https://satkit.com/sensor-de-corriente-ina219-i2c-mcu-219), [W52 en PR propia](https://github.com/Valdi320/Valdo/pull/9).
