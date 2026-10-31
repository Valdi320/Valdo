# W-IND-61 — autenticación DATA y ACK con HMAC (31/10/2026)

Ámbito: solo VALDO W, PR propia #9, robot aspirador NUEVO, local y reparable. La decisión del 28/10 cancela el trasplante OEM Xiaomi. No se ha modificado ningún repositorio externo, ninguna fuente de C/Codex/otros compañeros, ni OOMWOO, ni la PR #79 cleaning-jobs, ni ningún dispositivo.

## Defecto localizado y mejora comprobable

El contrato anterior W60 pasaba un indicador simulado authenticated_transport=True al receptor. CRC16 detecta errores accidentales, pero no autentica: cualquiera puede reconstruir una trama DATA o ACK sintácticamente válida y recalcular CRC. W61 añade autenticación de aplicación real (criptografía estándar de biblioteca Python): HMAC-SHA256 truncado a 16 bytes, con claves diferentes para DATA/ACK, derivadas por HKDF-SHA256 (RFC 5869) de clave maestra >=256 bits, epoch de 16 bytes, nodo y sesión. Se usa comparación de MAC de tiempo constante de biblioteca; las tramas anteriores de 22 bytes se transportan ahora en 38 bytes (16 bytes adicionales, 72,7% mayor). El protocolo NO cifra, por tanto **no proporciona privacidad**.

AuthenticatedSender solo admite ACK verificados criptográficamente antes de informar al AckTracker; AuthenticatedReceiver solo admite DATA verificados antes de informar al ModuleReceiver. La política existente de secuencia, plazo 240 ms, re-ACK acotado, expiración y no refresco por duplicados se conserva. La recepción comprueba caducidad incluso si recibe tráfico falsificado. No se ha alterado w_link.py ni incluido código licenciado de terceros.

## Reproducción y clasificación rigurosa

Desde research/2026-10-28-independent-wpt-sensor-v01:

    python3 -m unittest -v test_w_link
    python3 -m unittest discover -v -s w_ind_60 -p 'test_w60.py'
    python3 -m unittest discover -v -s w_ind_61 -p 'test_w61.py'
    python3 w_ind_61/w61_demo.py > W61_SYNTHETIC_AUTH_NO_RADIO.json

29 tests W61 adversariales: vector HKDF independiente RFC 5869 A.1, DATA/ACK, modificación de valor con CRC recalculado, falsificación de ACK/MAC, claves/epoch/sesiones/nodos incorrectos, replay, ACK perdido, timeout, rollback de reloj, tipos/longitudes incorrectos, falta de confidencialidad explícita. Ejecutados 29/29 en sandbox con doble local de la interfaz W60 (NO radios); la CI de GitHub con W60 REAL es imprescindible para elevar la evidencia. Archivo de demostración marcado SYNTHETIC_ONLY; no hay medición propia de potencia, radio, seguridad física ni energía.

**Bloqueador de seguridad:** el epoch debe ser NUEVO, aleatorio fuerte mediante CSPRNG y distribuido por una ceremonia de provisión local segura por cada sesión. Ni el RNG/secretos en MCU, ni la ceremonia, ni la unicidad persistente, revocación, rekey o almacenamiento seguro están implementados. Reusar (clave, epoch, sesión) tras reinicio permite replay criptográfico de capturas antiguas aunque un receptor nuevo arranque sin memoria de secuencias. Los valores de tests publicados son deliberadamente públicos y NO deben instalarse en un robot. El HMAC no sustituye cifrado del transporte, ni protege memoria de claves, ni para nada crítico; validar ambas radios con hardware queda pendiente.

## Tres sistemas que jamás confundir

1. Dock de carga: íntegramente diferido; SIN estación, litio ni BMS. No se controla la carga por radio.
2. Potencia a módulos: sensor piloto hipotético 5 V, 80 mA promedio (0,4 W), 300 mA pico (1,5 W). Comparar cable reemplazable (baseline) con WPT sencillo lazo abierto y WPT regulado; calor, FOD metálico, temperatura, desplazamiento, EMI y doble corte local normalmente-OFF quedan sin aprobar. **No WPT por defecto a motores, bombas ni turbinas.**
3. Datos: ESP-NOW (Apache-2.0) candidato simple, OpenThread (BSD-3-Clause) alternativa si la topología 802.15.4 justifica complejidad/coste; esta envolvente es independiente de ambos. ACK de aplicación, CRC, HMAC, secuencia, timeout y recuperación local separados. WISP5 RFID solo microconsumo, no alimenta por sí solo el sensor a 0,4 W.

Costo marginal del software: 0 € en piezas nuevas del robot, pero el coste de MCU, entropía, claves, RF, bobinas, protección y reparación **NO está calculado**; no afirmar que la solución física sea gratuita. Diotronic queda proveedor auxiliar de pasivos y recambios, sin stock local, MOQ o IVA final verificados; críticos electrónicos solo con documentación/seguimiento técnico. Véanse BOM y matriz de decisiones adjuntas.

## Auditoría de autores, ramas, cambios y derechos (31/10/2026)

- mark-belbin/simple-wireless-power GPL-3.0, master 7c7858c0 (pin 28/10 igual); PR #1 fusionada 2021; no copiar código GPL.
- wisp/wisp5-hw BSD-2-Clause, master 08332bc3 (igual); PR #1 fusionada 2015.
- wisp/wisp5 BSD-2-Clause, **rama por defecto 640kHz** HEAD 604eee2d, pin d978a697: 68 ahead / 11 behind **divergente**, PR #40 abierta; no interpretar fast-forward ni usar diseños RFID para 0,4 W continuo.
- espressif/esp-now Apache-2.0, master c3b5f9be (igual); PR #153 cerrada sin fusión; ACK MAC no equivale a ACK de aplicación.
- openthread/openthread BSD-3-Clause, main HEAD 4f909842, pin 7009584d: **16 ahead / 0 behind**; PR #13820 (IP6) y #13666 (DHCPv6) fusionadas 31/10, PR #13822 abierta; esos cambios no acreditan mejora para nuestro robot.
- OOMWOO oficial makerspet/oomwoo main f01a1b295f46 (29/10, star-history, PR #78 cleaning-jobs previa). VALDO PR #9 HEAD previo 49fcc297 (W60). VALDO_OOMWOO/adaptacion es carpeta y NO repositorio Git; no se ha editado. Checkout local Valdo estaba en rama Codex ajena con archivos dirty; no se ha tocado.

Fuentes públicas: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo ; https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html ; https://www.rfc-editor.org/rfc/rfc2104 ; https://www.rfc-editor.org/rfc/rfc5869 ; https://www.rfc-editor.org/rfc/rfc4231 .

Sin copias de fuente externa: solo bibliotecas estándar de Python. La licencia general del repositorio VALDO no consta expresamente adoptada aquí; no atribuir derechos ajenos.

## Siguientes puertas

Aprovisionamiento seguro, epoch único durable entre reinicios, revocación y cifrado de transporte; pruebas de pérdida/latencia y consumo real de RF con procedimiento autorizado; medir energía y coste de WPT frente a arnés reparable; FOD/temperatura/offset/EMI/cortes independientes y solucionar ERC conceptual histórico W-IND-18 (9 infracciones). No aceptar el módulo para fabricación/energización. Cero compras, cero pruebas físicas, cero batería/BMS conectados.
