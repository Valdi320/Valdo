# W-IND-89 — puerta de precarga y margen de tensión NFC (solo digital)

**01/11/2026, robot NUEVO; prohibido trasplante OEM Xiaomi X20 Pro.** Mejora original del sector W, sin compra, carga, batería/BMS, estación, impresión, soldadura ni intervención física. Sin fuentes externas copiadas. Esta revisión evita confundir la comprobación matemática de W88 (condensador supuestamente precargado) con una precarga obtenible desde la tensión de salida EH real.

## Hallazgo y mejora

W88 calculó una reserva IDEAL de 1,134 mJ en 1200 µF EFECTIVOS de 3,30 a 3,00 V. Con 1 mJ por intento y 0,01 mJ de reposo en un apagón RF hipotético de 100 ms, un solo intento sobrevive en cálculo (margen +0,124 mJ). **Pero no demostró que el captador NFC pudiera alcanzar 3,30 V para precargar esa reserva.**

ST AN4913 Rev 2 tabla 4 p.7 mide **V_EH=3,30 V y P_EH=2,310 mW** a H=0,5 A/m y AM=100 % en el montaje del fabricante. V_EH es **NO REGULADA**. Si se supone un camino DC sin elevador con una caída de **0,20 V HIPOTÉTICA**, su salida condicional sería 3,10 V; la reserva por encima de 3,00 V solo **0,366 mJ** con 1200 µF efectivos. Para el evento de 1,010 mJ faltarían **0,644 mJ** y además no se alcanza el objetivo de carga 3,30 V. No es medida propia ni valor de dropout certificado; **la tensión de ST es un punto BAJO CARGA, no un máximo de la fuente ni una curva I–V**. Otra carga, topología elevadora o regulador pueden cambiar el resultado.

W89 calcula para CADA una de las **22 muestras originales** de ST, reutilizadas directamente desde el módulo propio W86: margen de tensión de carga con dropout inyectado, potencia media durante una ventana RF y reserva inmediata ante ráfaga/reintentos. Rechaza la candidatura cuando cualquiera de las tres restricciones falla. Una topología elevadora se declara **pendiente de cualificar**, nunca aprobada ni descartada de manera universal. La salida contiene siempre hardware_release=BLOCKED; un PASS condicional solo valida una operación matemática.

| Experimento — supuestos, NO mediciones | Resultado |
|---|---|
| 11 muestras AM100, caída fija hipotética 0,20 V, objetivo 3,30 V | **0/11** satisfacen conjuntamente margen, media y ráfaga |
| 11 muestras AM10, mismos supuestos | **0/11**; solo 1/11 satisface margen de precarga, pero falla potencia |
| Contrafactual ideal sin caída, AM100 a H=1 A/m | Una muestra supera el filtro **solo en el modelo ideal** |
| Aumentar C sin elevar tensión | No permite alcanzar 3,30 V; evita optimización engañosa |

**No inferir** que esos 22 puntos cubran la desalineación real, temperatura, corrientes de arranque o todos los valores de campo intermedios. La energía RF+NFC durante comunicación, ESR, fuga, regulación, cold start y lector total permanecen desconocidos. ST advierte posible pérdida de comunicación al captar energía. Este hito corrige la interpretación del modelo anterior; no especifica un cargador ni certifica un módulo.

## Reproducción y alcance

Python estándar. Desde raíz de Valdo:

~~~sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_89 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_89/w89_source_headroom_gate.py > /tmp/w89.json
sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_89/expected.sha256
~~~

**12 tests adversariales originales** más regresión de W88 desde la CI ya existente reutilizada (NO añadir nuevo workflow). Evidencia determinista SHA256 y JSON CI; pruebas exclusivamente DIGITALES, no instrumentación ni SPICE.

**Tres circuitos y decisiones separados:** (1) carga de dock: WPT regulado exige detección de metal FOD, temperatura, EMI, humedad, offset y corte físico independiente normalmente OFF; bateria/BMS desconectados, no autorizado. (2) Alimentación de módulo: cable desmontable continúa BASELINE; NFC energía para **microsensor intermitente no crítico** solo candidato condicionado por I–V real y coste completo. Sin motores, bombas ni electroválvulas WPT por defecto. (3) Datos: ESP-NOW vs OpenThread sin selección; ambos RF, no alimentación. Exigir ACK de aplicación, CRC, secuencias/epoch, timeout, recuperación, cifrado para privacidad. Nunca usar RF para una parada crítica. WISP5 solo referencia para microenergía.

**Punto dulce / siguiente paso:** un único banco aislado autorizado con carga ficticia, **después de protocolo y permiso**, que capture curva V_EH/I_EH versus carga y posición real, tiempo de precarga, Vmínimo al comunicar, consumo del lector, máxima caída/eficiencia del regulador, FOD/temperatura/EMI y desconexión independiente. Reutilizar importador de trazas W84. Sin mediciones no ampliar indefinidamente idealizaciones. Sin ensayo físico ni compra en este hito.

**Fuente primaria:** https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7 ; datasheet https://www.st.com/resource/en/datasheet/st25dv04kc.pdf . Titular W: potencia/datos electrónica; C posee CAD/canales/fijaciones; OOMWOO, 10 upstream, ROS2 adaptación, PR #79 cleaning-jobs y checkout Codex compartido **intactos**. Auditoría detallada de cinco repositorios externos y BOM en BOM_DECISION.md.
