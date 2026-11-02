# W-IND-86 — inversión del beneficio de modulación al bajar el campo RF

**Solo digital, 1 nov 2026. Robot aspirador nuevo independiente, no Xiaomi OEM. Hardware BLOCKED.**

## Un avance verificable
W85 cribó solamente dos muestras del fabricante ST a **3 A/m rms**. W86 compara **22 puntos de datos originales** de **ST AN4913 Rev. 2, página 7, tablas 4 y 5**: AM100 y AM10 en el mismo campo.
En el ensayo ST con antena clase 1, a **0,5 A/m** AM10 proporciona **0,360 mW** contra **2,310 mW** con AM100, mientras a **3 A/m** AM10 proporciona **4,069 mW** contra **2,907 mW** con AM100. **La ventaja se invierte**, por lo que la modulación no se debe seleccionar por un único punto bien alineado. Son datos medidos por ST, no por nosotros, sin valor de mínimo garantizado de producto.

Para un sensor **hipotético** de 2,9 mW, conversor de eficiencia **hipotética 80%** y mínimo **hipotético VIN 3,3 V**, ningún punto muestreado entre 0,5 y 3 A/m con ninguna modulación satisface simultáneamente la tensión y potencia exigidas. En AM10 a 0,5 A/m V_EH=3,6V pero P útil hipotética=0,288mW; AM10 a 3 A/m potencia hipotética 3,2552mW pero V_EH=3,13V. **No prueba imposibilidad:** la elección de sensor/convertidor podría cambiar las condiciones.

El software verifica P=V*I de las 22 observaciones, rechaza interpolación/extrapolación, NaN y supuestos fuera de límites, calcula escenarios por campo y ventana y marca todo como **hardware_release=BLOCKED**. Se prohíbe interpretar un mínimo observado de la muestra como una garantía sobre el rango continuo; el acoplamiento real y la incertidumbre espacial/temporal son desconocidos.

## Reproducibilidad
Ejecutar desde el repositorio con Python 3 estándar:
    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_86 -p 'test_*.py' -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_86/w86_field_sweep.py > /tmp/w86.json
    cmp /tmp/w86.json research/2026-10-28-independent-wpt-sensor-v01/w_ind_86/expected.json

Hay **34 tests digitales adversariales**, no mediciones nuestras. El flujo de CI prueba el mismo árbol y sube el JSON para reproducibilidad.

## Separar lo que no es equivalente
**Dock de carga:** circuito propio de seguridad, FOD, protección térmica, humedad, aislamiento, corte independiente y BMS; este NFC de mW **NO** se extrapola a la estación ni a litio ni motores/bombas.
**Alimentación de módulo:** una etiqueta NFC de harvesting + lector podría soportar un **microsensor intermitente no crítico** si se demuestra potencia bajo desalineación, VIN, rizado, reserva, energía del lector y coste total frente a cable desmontable; no sustituye la seguridad eléctrica.
**Datos:** inventario RF de la prueba ST **no prueba** ACK de aplicación, CRC, números de secuencia, timeout, privacidad, autenticación, cifrado y recuperación. ESP-NOW vs OpenThread se decidirán tras consumo RF medido; radio no transporta alimentación. WISP5 queda de referencia de microsensor, y no se debe usar radio para parada crítica.

## Próxima puerta realmente medible
Medir campo y offset (XYZ y ángulos), potencia TX/lector completa, P_RX y V_EH bajo carga, pérdida/recuperación RF con ACK de aplicación, tiempo entre lecturas, humedad, metal pequeño/FOD, temperatura, EMI, desconexión normal-OFF independiente, durabilidad y coste total instalado. Obtener primero proceso de seguridad y autorización para banco resistivo **separado de baterías/BMS**. No hay ensayo físico ni compra ahora.

## Procedencia y licencia
Fuente [ST AN4913 Rev. 2 (junio 2021), p. 7, tablas 4 y 5](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7). ST confirma que el campo, el acoplamiento y la antena afectan energía y comunicación; no hay garantía de comunicación durante harvesting. [ST25DV04KC datasheet](https://www.st.com/resource/en/datasheet/st25dv04kc.pdf) V_EH no regulada/Hi-Z. Python, prueba y especificación son originales; únicamente se citan/transcriben datos numéricos del autor, conservando atribución. No se copia código, PCB ni esquemáticos de terceros. Autorías/licencias/SHAs en BOM_DECISION.md.
