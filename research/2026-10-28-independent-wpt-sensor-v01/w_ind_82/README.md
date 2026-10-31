# W-IND-82 — telemetría caducable tras brownout (módulo no crítico)

**31-10-2026 · autoría original W · sin copiar fuentes ajenas.** Mejora: si un módulo sensor pierde alimentación inductiva, el controlador deja de considerar válido su dato y exige nueva sesión autenticada. Esto **no garantiza continuidad eléctrica** ni sustituye los cortes físicos FOD, temperatura, potencia y batería. Arquitectura enteramente independiente del Xiaomi X20 Pro.

## Decisión de alto retorno

Para un sensor opcional, de diagnóstico y **solo lectura**, los reinicios RX pueden ser tolerables: no obligan a sobredimensionar condensadores únicamente para mantener datos siempre disponibles. La validez del enlace es independiente de la parada local de precipicios, bumper, motor, bomba, BMS y TX WPT. La protección física nunca espera una orden por radio.

Esto NO demuestra ahorro ni viabilidad de WPT. W74 usó 2,9 mW y límite +0,5 Wh/día como **hipótesis**; HMAC/ACK/802.11 pueden excederlo. Cable protegido y reemplazable sigue como opción de referencia.

## Contrato cuantitativo, únicamente sintético

| Campo | Umbral del modelo; NO medición |
|---|---|
| Carga lógica | telemetría de diagnóstico uint16; sin interfaz de actuadores |
| Tamaño | **66 B**, inferior al máximo ESP-NOW v1 de 250 B |
| Identidad | ID de módulo 16 bits; epoch de arranque aleatorio 128 bits renovado tras brownout |
| Inicio | challenge aleatorio host 128 bits, HELLO autentificado en 500 ms |
| Validez | 250 ms desde último DATA nuevo aceptado; primer DATA tras HELLO también en 250 ms |
| Repetidos | ACK duplicado permitido, pero NUNCA refresca vigencia |
| Replays | secuencia 32 bits estricta, reject huecos/regresión/wrap/epoch anterior |
| Aplicación | ACK epoch+challenge+seq; stop-and-wait; 60 ms y máximo 2 reintentos hipotéticos |
| Integridad | CRC32 para errores + HMAC-SHA256 truncado 16 B para autenticación; clave >=32 B |
| Privacidad | encrypted_unicast=False bloquea por defecto; configurar y VERIFICAR cifrado del RF real fuera del modelo |
| Rehabilitación | pérdida de sesión obliga nuevo challenge/HELLO; nunca habilita corte crítico |

Trama: magic(4), version(1), kind(1), module(2), epoch(16), challenge(16), sequence(4), value(2), CRC(4), HMAC(16) = 66 bytes. Cuatro tipos: CHALLENGE, HELLO, DATA y ACK. CRC **no autentica**; HMAC **no cifra**. Las claves del test son deliberadamente públicas y FICTICIAS, nunca para despliegue. Entropía CSPRNG durante arranque real, emparejamiento, rotación de claves y confidencialidad del transporte permanecen sin validar.

**Limitación crítica:** recibir un paquete nuevo hace fresca la **recepción**, NO demuestra la edad de la muestra. No hay reloj sensor verificado, medición de latencia RF ni tolerancia a sincronización. El booleano de cifrado es una hipótesis del test, no demuestra ESP-NOW CCMP, Thread o robustez de la radio. Tampoco se cubren reinicio del host, pérdida de NVM, clave comprometida, ataques físicos, ni uso en sistemas de seguridad.

A 10 muestras/s, DATA+ACK generan 1320 bytes/s de payload de aplicación sin sobrecarga, retransmisiones o handshake; energía RF y CPU no medida. No hay WPT aprobado para motores o bombas.

## Auditoría de fuentes de sus creadores — 31 octubre 2026

| Titular / licencia | HEAD de rama comparado con SHAs guardados en doc 19 del 28/10 | Consecuencia |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master 7c7858c0 = registrado; PR #1 fusionada en 2021 | sólo referencia WPT; sin apropiación de circuito |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master 08332bc3 = registrado | RFID microenergía no equivale a WPT continua |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | **640kHz 604eee2d**, registrado d978a697; **divergente: ahead 68, behind 11**. HEAD 25-04-2022, PR #40 abierta de 2021 | jamás inferir rama ordenada por fecha |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master c3b5f9be = registrado; PR #153 cerrada, no fusionada feb 2026 | transporte candidato; MAC callback no implica ACK aplicación |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main **c4ebc1c1**, +20 commits sobre 7009584d; PR #13821 y #13802 fusionadas 31 oct | alternativa 802.15.4, no seleccionar ambas |

Fuente primaria de los límites radio: [Espressif ESP-IDF 5.5.1 ESP-NOW](https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32c5/api-reference/network/esp_now.html) (PMK/LMK, cifrado CCMP y confirmación MAC no end-to-end). [OpenThread](https://openthread.io/) se compara en la matriz. OOMWOO upstream main f01a1b29 del 29-10 (chart, no electrónica); PR #79 cleaning-jobs intacta. VALDO rama W propia en PR #9 desde 0fc147a7; adaptación VALDO+OOMWOO v01 sin hardware WPT integrado. No se copiaron repositorios, ejemplos, diseños ni fuentes externas.

## Reproducción determinista

~~~sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_82
python3 -m unittest discover -s . -p 'test_w82_lease.py' -v
python3 demo.py > /tmp/w82-check.json
diff -u expected.json /tmp/w82-check.json
~~~

**36 pruebas adversariales de software** comprobadas en sandbox Python 3.11: replay/brownout/epoch, retos caducados, errores CRC/HMAC, seq, perdida/duplicación ACK, reloj regresivo, privacidad por defecto y ausencia API motora. Evidencia JSON sintética y CI específica tras publicación. No es validación física. Sin compras, impresiones, energía aplicada, litio, motores ni servicios instalados.

**Próximo bloqueo discriminante:** medir de forma autorizada y aislada un par TX/RX realmente activo en 1–20 mW, potencia TX cargada, radio+ACK, caídas de tensión y FOD/offset/temperatura/EMI/corte independiente. Si excede coste energético y monetario del cable, detener WPT del sensor y consolidar la línea cableada.
