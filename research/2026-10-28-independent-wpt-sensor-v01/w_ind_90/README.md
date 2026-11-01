# W-IND-90: costo real de banco NFC vs chip aislado

Fecha: 01/11/2026. Robot NUEVO; cero Xiaomi OEM. Hito propio W documental y aritmético, sin compra, montaje, firmware, ensayo físico o batería. No se modifica upstream OOMWOO ni la PR #79. Cable extraíble = BASELINE.

## Mejora de decisión: pareja de evaluación REALMENTE identificada
- TX: ST X-NUCLEO-NFC08A1 (lector ST25R3916B, antena PCB 47x34 mm, ISO15693, activo). X-NUCLEO-NFC06A1 es OBSOLETO, no comprar por defecto. ST: https://www.st.com/en/evaluation-tools/x-nucleo-nfc08a1.html ; obsoleto: https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC06A1/10442436
- RX: ST X-NUCLEO-NFC07A1 (TAG ST25DV64KC, antena circular 54 mm, energía RF o alimentación externa, activo). ST: https://www.st.com/en/evaluation-tools/x-nucleo-nfc07a1.html ; ejemplo independiente https://www.st.com/en/embedded-software/x-cube-nfc7.html . NO contiene el ST25DV04KC estudiado en W85-89: no transferir sus 22 puntos de tensión/potencia. No equivale a validación RF, compatibilidad de firmware o carga de sensor.
- Host MCU por extremo, cuando se requieren simultáneamente aplicaciones y diagnóstico I2C en ambos extremos: NUCLEO-L476RG. Dos MCU son un escenario de desarrollo, no un mínimo obligatorio de toda función NFC.

## Costo: DigiKey España, observado 01/11, MOQ1, stock web remoto, sin envío
- Lector NFC08A1: 33,95 EUR sin IVA / 41,0795 EUR IVA incluido.
- Tarjeta/tag NFC07A1: 15,35 EUR sin IVA / 18,5735 EUR IVA incluido.
- MCU NUCLEO-L476RG: 20,28 EUR sin IVA / 24,5388 EUR IVA incluido por unidad.
- Un host solo lector (tag sin controlador de aplicación): 69,58 EUR sin IVA; **84,19 EUR IVA incluido**.
- Dos hosts de telemetría: 89,86 EUR sin IVA; **108,73 EUR IVA incluido**.
La segunda suma NO incluye fuente aislada, instrumentos V/I y calibración, carga resistiva, apagado local, FOD, protección térmica/EMI, cableado, envío o montaje; no es costo final puesto en Zaragoza ni BOM del robot. La mención de 1,7 W de salida del lector por ST NO es potencia captada/útil en RX. El chip SO8N ST25DV04KC de Farnell ~1,12 EUR IVA incluido carece de antena, PCB y regulación; no sustituye tarjeta NFC07A1.

## Reproducción
Desde raíz del repositorio:
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_90 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_90/w90_bench_bom.py > /tmp/w90.json
sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_90/expected.sha256

Son 12 pruebas CPU originales con costos, IVA, cantidades, diferencia de chip y negativa permanente a declarar hardware apto. Evidencia JSON determinista, no captura física. Matriz/sourcing/autorías/SHAs en BOM_DECISION.md.

## Próximo discriminante y límites
Para decidir si merece la pena un único microsensor no crítico WPT a 1-20 mW: presupuesto completo y autorización de seguridad primero; medir banco aislado sin litio ni BMS, TX V/I, EH V/I frente a distancia y carga, arranque frío, alimentación durante datos/ACK, pérdidas/temperatura/FOD/EMI y apagado autónomo; comparar con cable sustituible. Las tres rutas (carga dock, potencia de módulo, datos RF) siguen separadas. ESP-NOW/OpenThread son datos solamente; CRC, ACK de aplicación, seq, timeout, cifrado y recuperación; ningún paro crítico por RF, ningún WPT motor/bomba. WISP5 solo microsensores mínimos. No realizar pruebas sin autorización.

Diotronic auxiliar: 0 SKUs con stock local y precio verificados. TME y Mouser mismo conjunto sin cotización verificada; Farnell NFC08A1 34,98 EUR ex IVA (bajo pedido), MCU 16,46 EUR ex IVA (stock web), portes desconocidos. No usar stock como sustituto de requisitos. Derechos de ST y cuatro proyectos externos conservados; no se ha copiado código/CAD externo.
