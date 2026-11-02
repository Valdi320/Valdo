# W-IND-54 — Dos INA219 intercambiados: cancelar sesgo multiplicativo sin comprar otro medidor

30 de octubre de 2026. **Proyecto independiente VALDO, código original ámbito W.** No es un robot Xiaomi ni una integración de hardware OOMWOO. Este hito solo desarrolla un método digital reproducible de metrología de un enlace WPT de **muy baja potencia**; no energiza bobinas, no ejecuta I²C, no instala servicios y no toca el ordenador, clones ni el trabajo de C/Codex.

## Una mejora real frente a W-IND-53

El principal coste pendiente del banco con dos INA219 baratos es determinar si su calibración relativa basta para medir eficiencia. Si el medidor A exagera la potencia un 10 % y el B la infravalora un 10 %, una lectura convencional puede informar una eficiencia completamente equivocada. **La inversión de los dos instrumentos permite cancelar idealmente sus factores multiplicativos constantes sin un tercer vatímetro:**

Primera pasada, A en entrada y B en salida: η_AB = (g_B/g_A) × η_1.
Segunda, tras un intercambio sin energía, B en entrada y A en salida: η_BA = (g_A/g_B) × η_2.
Estimación cruzada: η_X = sqrt(η_AB × η_BA) = sqrt(η_1 × η_2).

**Límite fundamental:** si las condiciones cambiaron, el resultado es la **media geométrica de dos eficiencias distintas**, NO la eficiencia de ninguna pasada. Tampoco cancela offsets aditivos, no linealidad dependiente de corriente, cambios de ganancia/temperatura, caídas por shunt ni efectos físicos del intercambio. Por eso se imponen identidades y trazas distintas, orden temporal sin solapes, misma fijación, temperaturas, offset de bobinas, distancia y resistencia comparables; las cotas de repetibilidad son hipótesis de cribado, NO tolerancias de seguridad. Los límites de error de entrada y salida son también datos que deben obtenerse externamente; una casilla en BENCH_MEASURED no prueba nada.

### Evidencia sintética reproducible

Ejemplo con potencia REAL FICTICIA: 1000 mW de entrada y 800 mW de salida; ganancia A 1,10; ganancia B 0,90. El programa reproduce:
- Pasada AB: 720 / 1100 = **65,45 % aparente**.
- Pasada BA: 880 / 900 = **97,78 % aparente**.
- Combinación cruzada: **80 %** bajo ganancias multiplicativas fijas y condiciones idénticas.
- Con límites aditivos **SUPUESTOS** de ±2 mW por canal/pasada, intervalo condicionado conservador **79,637–80,364 %**.
- Fallos inyectados: ganancia alterada, distinta eficiencia verdadera, temperatura, carga, distancia/offset, trazas o IDs repetidos, desfase, muestras imposibles, incertidumbre inválida, ausencia de trazabilidad. El método nunca aprueba hardware.
- 12 pruebas unitarias Python con subcasos adversarios; GitHub Actions ejecuta la misma suite y archiva JSON sintético.

Reproducir con Python 3 sin paquetes externos:
    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_54 -p 'test_w54.py' -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_54/w54_crossed_meter.py --demo --out W54_SYNTHETIC.json

## Matriz técnica: separar los 3 problemas

| Problema / alternativa | Decisión provisional | Causa / qué falta |
|---|---|---|
| WPT sencillo en sensor 5 V / ~80 mA, pico hipotético 300 mA | Solo candidato experimental | Potencia nominal del módulo autor no equivale a 80 mA útiles; eficiencia, FOD, temperatura, EMI, offset, humedad y corte independiente NO probados |
| WPT regulado con FOD, doble corte autónomo, vigilancia térmica | Necesario si la inductiva se adopta; NO aprobado | Coste y complejidad pueden superar cable reemplazable; W-IND-18 ERC sigue rojo; ningún circuito seguro construido |
| Módulo cableado corto con conector bloqueable | **Referencia económica por defecto** | Cable real sustituible, no ofrece ausencia total de contactos; resistencia a ciclos aún por medir |
| Dock inductivo / carga de litio | **Otra arquitectura y expediente de seguridad** | Batería/BMS totalmente desconectados; no se extrapola ensayo de 0,8 W a estación de decenas de W |
| ESP-NOW / ESP32-C3 | Primer candidato de datos no críticos | ACK aplicación, CRC, secuencia, timeout, privacidad autenticación y recuperación por especificar/probar en RF real; radio NO para parada crítica |
| OpenThread / 802.15.4 | Alternativa futura | Hardware compatible extra, pila de red/consumo/topología a comparar; no mezclar con ESP-NOW por defecto |
| WISP5 RFID | Investigación secundaria | Solo microsensores de energía mínima; requiere lector y estudio de ciclos despierto/dormido |

No colocar WPT por defecto en motores, bombas ni sensores cuya retirada no lo justifique; WPT de potencia, docking y enlace radio son tres trabajos distintos.

## Auditoría de creadores y revisiones HEAD, verificada 30/10/2026

PIN local del documento maestro de 28/10 comparado con HEAD de la rama EXACTA, no con fechas ni orden de ramas. Ningún código/CAD ajeno copiado.

| Creador y repositorio / licencia | PIN 28/10 → HEAD 30/10 | Cambios relevantes |
|---|---|---|
| [Mark Belbin, simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, master | 7c7858c → 7c7858c | Sin cambio; la prueba de 100 W/81,3 % del autor no prueba nuestro FOD/corte/regulación |
| [WISP5 hardware](https://github.com/wisp/wisp5-hw), BSD-2-Clause, master | 08332bc → 08332bc | Sin cambio; PCB Altium y lector RFID ajenos no integrados |
| [WISP5 firmware](https://github.com/wisp/wisp5), BSD-2-Clause, **640kHz** | d978a69 → 604eee2 | **Divergió**, +68/-11 commits, no utilizar orden de ramas para inferir actualidad |
| [Espressif, esp-now](https://github.com/espressif/esp-now), Apache-2.0, master | c3b5f9b → c3b5f9b | Sin cambio; v1.0 release y ejemplos de autor no equivalen a garantías de aplicación |
| [OpenThread](https://github.com/openthread/openthread), BSD-3-Clause, main | 7009584 → e577777 | +14/-0, radio, CLI, secure transport, pruebas; PR [#13819](https://github.com/openthread/openthread/pull/13819) / [#13821](https://github.com/openthread/openthread/pull/13821) abiertos el 29/10 |

[OOMWOO oficial](https://github.com/makerspet/oomwoo), main f01a1b295f46 (última modificación observada de gráficos de stars); [VALDO propia PR #9](https://github.com/Valdi320/Valdo/pull/9), HEAD previo d1b0db28. Adaptación local VALDO_OOMWOO con contrato WPT_DATOS_V01 leído; sin edición. PR #79 OOMWOO es cleaning-jobs de otro ámbito. La automatización W es la única activa de esta familia (OOMWOO horaria detenida). La licencia global de VALDO todavía no está confirmada; el presente código es original sin copia de GPL/BSD/Apache.

## BOM y coste completo, no fingir compra

El único cambio de W54 es SOFTWARE, **0 € de partes nuevas y 0 € por robot**. Reutiliza los dos INA219 candidatos W51–W53: Satkit MCU-219 anunciados a 3,63 € c/u con IVA, pareja **7,26 € de catálogo** pero sin portes, disponibilidad conciliada ni patrón/calibración, y **NO comprado**. Una comparación de precio real puesto en Zaragoza necesita cantidades mínimas, IVA, envío y stock verificable. Diotronic es auxiliar para pasivos, hilos/conectores/prototipos si son equivalentes y baratos; sin stock local confirmado. Instrumentos críticos, protectores térmicos/FOD/corte/BMS: documentar y adquirir con trazabilidad en TME/Mouser/DigiKey/fabricante cuando corresponda. CSV BOM y matriz adjuntos.

## Estado de seguridad y siguiente paso

**12/12 pruebas sintéticas PASS local**; no se asegura CI hasta revisar ejecución GitHub. Este método es una comparación matemática, no una calibración: W52 corriente, W53 tensión, W50 tiempo y autenticidad de lecturas siguen requiriendo referencia trazable, lectura I²C real y verificación física de estabilidad entre intercambios. El DT-830B doméstico no es automáticamente un patrón calibrado. FOD, corte independiente, protección térmica, EMI, humedad y retroalimentación todavía sin cualificar; W-IND-18 ERC original sigue bloqueante.

**Siguiente paso, no realizado:** pedir revisión metrológica de W54 y, solo con autorización/procedimiento de seguridad, un futuro banco aislado de baja tensión, carga resistiva y bobinas sin batería ni dock. Cambiar físicamente los medidores únicamente con fuente apagada y aislada. **hardware_approved=false; power_on=false; lithium_dock=false.** No comprar, imprimir, soldar, conectar, ni modificar firmware/máquinas.
