# W-IND-78 — Verificador de microcortes RX ENTRE muestras (WPT sensor de baja potencia)

31/10/2026. Diseño y código ORIGINAL del ámbito W. **Cero prototipos, compras, mediciones físicas o hardware aprobado**. Se trabaja en un robot NUEVO; la electrónica y el dock OEM Xiaomi quedan excluidos por decisión de 28/10. No se tocan fuentes ajenas, OOMWOO, CAD mecánico ni la PR #79 cleaning-jobs.

## Problema y mejora verificable
W77 detecta el mínimo RX **observado** y marca la máxima separación de muestras. Una señal puede medir 3,30 V en todos los instantes muestreados y caer entre ellos. W78 incorpora una cota MATEMÁTICA conservadora para la tensión NO observada, condicionada a un límite global de rapidez de cambio |dV/dt|<=S en toda la adquisición. En una ventana de duración efectiva D, extremos medidos A y B, e incertidumbre de voltaje ±u, la cota inferior es **(A+B-2u-S·D)/2**, suponiendo muestras temporalmente correctas y que el límite S es válido también durante el microcorte. La duración efectiva incluye +2 veces la incertidumbre de timestamp. El programa comprueba coherencia de pendiente, cobertura completa, orden temporal, tiempo, voltajes, muestras y fuentes; falla cerrado con entradas no finitas y límite de pendiente no caracterizado.

**CUIDADO:** un conjunto finito de muestras NO acredita un límite S. Ni siquiera medir a alta frecuencia garantiza ausencia de pulsos más rápidos sin límites físicos demostrados, ancho de banda/trigger adecuados y prueba real del circuito. La cadena documental de caracterización y su calibración no son verificadas por este código. El programa SIEMPRE devuelve hardware_approved=false, instantaneous_voltage_proven=false y critical_stop_authorized=false.

### Ejemplo enteramente SINTÉTICO
- Todos los puntos observados: 3,30 V; separados 10 ms.
- Hipótesis: incertidumbre 0,05 V, rapidez máxima 60 V/s.
- Cota condicional: 3,30-0,05-(60×0,010)/2 = **2,95 V**.
- Mínimo del sensor hipotético: 3,00 V → BLOCKED, aunque las muestras parezcan perfectas.
- Muestreo cada 5 ms con iguales hipótesis daría 3,10 V como cota matemática, PERO no aprueba hardware ni demuestra que S=60 V/s sea verdadero.

### Reproducción exacta
~~~sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_78
python3 -m unittest -v test_w78.py
python3 w78_inter_sample_gate.py --input TRACE_SYNTHETIC.json --output W78_REGENERATED.json
cmp W78_EVIDENCE_SYNTHETIC.json W78_REGENERATED.json
~~~
22 pruebas independientes de validación adversarial y determinista. Evidencia sintética JSON fijada en Git, regenerada en CI.

## Separación de subsistemas y límites
1. **Dock y carga**: no acoplar batería/BMS ni estación; ninguna aprobación de carga de litio.
2. **Potencia a módulos**: sólo sensor no crítico 1–20 mW; WPT vs cable sustituible se decide con eficiencia TX/RX, consumo completo, FOD, térmica, offset, EMI, descarga residual, corte autónomo, humedad, mantenimiento y costes reales. No trasladar por defecto a motores/bombas.
3. **Datos RF**: ESP-NOW/OpenThread con ACK de aplicación, CRC, seq/epoch, caducidad, cifrado/autenticación y recuperación. La radio NO alimenta el sensor ni detiene un peligro físico. WISP5 se reserva para RFID de microenergía, no potencia de motores.

Se conserva la arquitectura fail-closed de W77; se añade una condición NECESARIA, no suficiente. El resultado de laboratorio no es inferible a partir de pruebas sintéticas. Los márgenes de 3 V, 60 V/s y 0,05 V son meras hipótesis, no límites de un componente comercial.

## Fuentes y titularidad
Comparación HEAD vs registros maestros al 31/10/2026:
- mark-belbin/simple-wireless-power, GPL-3.0, master 7c7858c0... **igual**; prototipo del autor no implementa regulación/protecciones completas.
- wisp/wisp5-hw, BSD-2-Clause, master 08332bc3... **igual**.
- wisp/wisp5, BSD-2-Clause, rama **640kHz** 604eee2d... **DIVERGENTE** respecto d978a697... (+68/-11, no interpretar como simple actualización), PR #40 abierta, último commit del autor 2022.
- espressif/esp-now, Apache-2.0, master c3b5f9be... **igual**, PR #151 cerrada.
- openthread/openthread, BSD-3-Clause, main b6d0f06d... **+18/0** respecto 7009584d; PR #13824/#13825 abiertas (radio y simulación), no adoptadas.
- OOMWOO oficial makerspet/oomwoo main f01a1b29 (29/10); oomwoo-pcb main 87aa7d38 y firmware main ce05f266 (31/10); VALDO PR #9 head 968a5d76 antes de W78. Adaptación VALDO_OOMWOO y contratos leídos; repositorios originales y checkout local compartido sucio quedaron INTACTOS.

Enlaces fuente: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5/tree/640kHz ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo . Código del verificador original, sin copiar de terceros.

## BOM, decisión y próximo bloqueo
Ver BOM_W78.csv y MATRIZ_W78.csv. Coste de nueva electrónica: 0 €, no compra. Diotronic: **auxiliar** para pasivos/prototipado, sin stock Zaragoza, MOQ ni IVA verificado; TME/Mouser/DigiKey sin cotización cerrada. No elegir componentes críticos sin datasheet ni trazabilidad. ERC KiCad W18 mantiene tres infracciones y CI general anterior fallos históricos.

**Siguiente paso:** antes de hardware, exigir diseño del receptor y regulador que permita justificar una cota independiente de dV/dt (incluyendo posibles cortes abruptos) y captura real con ancho de banda/trigger apropiados. Con un corte brusco, el modelo Lipschitz puede ser inválido: bloquear, no extrapolar.
