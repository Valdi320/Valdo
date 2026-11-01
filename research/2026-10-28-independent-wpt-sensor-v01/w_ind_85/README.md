# W-IND-85 — NFC con potencia y datos sin contactos: primera criba con cifras de fabricante

**2026-11-01. Sector W original, robot aspirador NUEVO. No Xiaomi OEM. Sin electricidad real.**

**Mejora concreta:** un filtro matemático reproducible contrasta por primera vez un candidato comercial de captación NFC 13,56 MHz, el **ST25DV04KC-IE8S3 (SO8N)**, con dos puntos de ensayos publicados por su fabricante. Un mismo lector podría transferir energía y mensajes RFID a un microsensor de mantenimiento junto a él, pero **no está aprobado** sustituir el cable del primer sensor continuo. El chip no es un TX/RX de carga de batería, ni una radio ESP-NOW, ni un regulador.

## Evidencia del fabricante y origen

- STMicroelectronics [DS13519 Rev8 §5.5.2, p49](https://www.st.com/resource/en/datasheet/st25dv04kc.pdf#page=49): V_EH **no regulada**, alta impedancia si RF insuficiente/función desactivada; **la comunicación NO está garantizada mientras se entrega energía**.
- STMicroelectronics [AN4913 Rev2, p7 Tablas 4 y 5](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7), cuyo ámbito incluye los KC: banco propio del **autor** con antena ISO clase 1 13,6 MHz, lector específico y respuesta RFID inventory funcionando. Dos muestras con campo H=3 A/m rms:

| AM del lector | V_EH medida por ST | I_EH medida por ST | P_EH calculada/documentada por ST |
|---|---:|---:|---:|
| 100 % | 3,23 V | 0,9 mA | 2,907 mW |
| 10 % | 3,13 V | 1,3 mA | 4,069 mW |

Esos datos **no** son nuestras mediciones, ni garantías de potencia mínima, ni condiciones de montaje del robot. Una respuesta inventory no demuestra ACK de aplicación, cifrado o transmisión continua. Las fichas de ST son obra de su autor; **no se copian archivos, circuitos ni código de terceros**.

## Escenario original, NO medición ni selección de pieza

Sensor hipotético opcional: consumo **2,9 mW**, rail **3,30 V**, mínimo **3,00 V**, conversor idealizado con eficiencia **80 % inventada**, no medida. A H=3 A/m en el banco del autor:

- AM100: 2,907×80 %=**2,3256 mW**; déficit **0,5744 mW**, exigiría un 99,759 % de eficiencia ideal para llegar a 2,9 mW.
- AM10: 4,069×80 %=**3,2552 mW**, margen aritmético **0,3552 mW**, **pero** el V_EH del autor es **3,13 V**, inferior al rail objetivo 3,30 V. Harían falta conversión, regulación, prueba de data+energy concurrentes, lector/antena y caracterización real.
- Hueco RF hipotético 100 ms: energía de reserva **290 µJ**, capacitancia efectiva **ideal** mínima **306,878 µF** entre 3,30 y 3,00 V. Para 250 ms: **767,196 µF**. Un supuesto 330 µF *efectivos* pasa sólo 100 ms en el modelo: ESR, fugas, arranque, tensión de campo, edad y picos están fuera del cálculo.

Por ello, **cualquier salida** informa hardware_release = BLOCKED. Las dos potencias son datos de ST en su banco; el resto es HIPÓTESIS. El modelo no calcula consumo del lector, campo real, EMI, FOD, temperatura, desalineación, regulación, backfeed o coste instalado. Ni siquiera es simulación de radio o SPICE. **No elimina todavía ningún cable.**

## Reproducción exacta: 31 tests + JSON

Desde raíz del repositorio:

~~~sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_85 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_85/w85_nfc_eh_gate.py > /tmp/w85-evidence.json
cmp /tmp/w85-evidence.json research/2026-10-28-independent-wpt-sensor-v01/w_ind_85/expected.json
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_85/w85_nfc_eh_gate.py --outage-ms 250 --effective-cap-uf 330
~~~

Solo Python 3 biblioteca estándar; tests adversariales de valores no finitos, costes de potencia, límites de voltaje, ausencia de RF y prohibición de aprobación. GitHub CI publica el JSON como evidencia digital. Ninguna prueba física.

## Tres sistemas distintos

**Estación/dock:** carga inalámbrica regulada con batería/BMS pertenece a arquitectura separada. STOP sin seguridad/autorización. **Potencia de módulos:** ST NFC RFID EH solo candidato a microsensor **intermitente** junto a lector; primera alternativa sigue siendo cable corto sustituible, no bobina en motores ni bombas. **Datos:** NFC necesita lector; ESP-NOW y OpenThread siguen alternativas RF con consumo propio, ACK *de aplicación*, CRC, secuencias, timeouts, protección anti-replay y privacidad real cifrada. La parada eléctrica crítica es **independiente** de radio y software. WISP solo se considera para sensores RFID de consumo ultrabajo.

**Siguiente criterio medible:** obtener/medir curva de potencia RX a 1–20 mW y consumo lector completo, geometría y mínimo H de campo, RF simultánea con harvesting, fallos, temperatura, FOD, EMI, corte autónomo, costo total y mantenimiento. Nunca comprar, imprimir, soldar o energizar sin autorización previa. Referencias, titulares de licencias y BOM comparada en BOM_DECISION.md.
