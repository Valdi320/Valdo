# W-IND-64 · Privacidad AES-256-GCM de telemetría (31/10/2026)

**Alcance:** software W original para robot NUEVO, local, abierto, reparable e imprimible. Ningún circuito energizado, batería/BMS, litio, estación, firmware OEM Xiaomi, PR OOMWOO #79 o CAD de otro propietario tocado.

## Defecto y mejora verificable

W61 autenticaba tramas con HMAC pero **exponía el valor íntegro en texto claro**. W64 añade cifrado/autenticación **AES-256-GCM** a los 22 bytes de telemetría DATA y ACK, mediante paquete versionado de 54 bytes (W61 = 38 bytes, sobrecoste 16 bytes/paquete). Usa HKDF-SHA256 ya existente, claves separadas por sentido, nodo, sesión y época; nonce de 96 bits derivado de tipo+secuencia, AAD ligado al contexto. Una retransmisión de DATA/ACK devuelve exactamente los mismos bytes cifrados; reutilización de secuencia con otro contenido o retroceso bloquean **transmisión de esa instancia**. Un bit alterado, ACK falso o par incorrecto no supera autenticación y no actualiza frescura. Solo es una implementación Python de laboratorio: ni hardware ni radio ESP-NOW/OpenThread integrados.

**Limitaciones críticas:** el constructor puede recibir época repetida tras reinicio. W62/W63 bloquean duplicados **solo con ancla externa confiable** aún inexistente físicamente. Por tanto, **NO desplegar, NO afirmar confidencialidad de producto físico**, ni claves/entropía/provisionamiento seguros; la prueba incluye explícitamente reproducciones iguales al recrear el objeto con la misma época, para mostrar el riesgo. Python no implica memoria/latencia MCU compatibles. No usar radio para parada crítica, permisos de bombas/motores, FOD/corte o carga. AESGCM de la dependencia externa cryptography (licencia dual Apache-2.0/BSD-3-Clause); no copiamos su implementación. Revisar si ESP-NOW unicast CCMP ya proporciona privacidad sin sobrecoste de aplicación.

## Reproducción

Python 3.12 + cryptography==46.0.4 (solo en CI/entorno aislado), desde research/2026-10-28-independent-wpt-sensor-v01:

    python3 -m unittest discover -s w_ind_64 -p test_w64.py -v
    python3 -m unittest discover -s w_ind_63 -p test_w63.py -v
    python3 -m unittest discover -s w_ind_62 -p test_w62.py -v
    python3 -m unittest discover -s w_ind_61 -p test_w61.py -v
    python3 -m unittest discover -s w_ind_60 -p test_w60.py -v
    python3 -m unittest -v test_w_link
    python3 w_ind_64/w64_demo.py > W64_AESGCM_SYNTHETIC.json

26 pruebas nuevas: NIST AES-GCM vector, autocifrado, CRC interno, ACK, bit flips, suplantación, llaves/epoch/dirección, nonce, retransmisiones, antirrepetición de proceso, agotamiento, ausencia de refresco timeout. Tests locales de W64 PASS en sandbox con dobles de W61/W_link; **integración real necesita CI GitHub**. Evidencia JSON completamente sintética; no implica medición real.

## Tres problemas independientes y matriz de elección

| Problema/alternativa | Eficiencia, FOD, térmica, EMI, offset y corte | Decisión |
| --- | --- | --- |
| Dock de carga inductiva | Sin ensayo aislado de carga resistiva, FOD ni doble desconexión autónoma | **BLOQUEADO**, no batería |
| Módulo sensor 5V 0,4W típico/1,5W pico | Presupuesto HIPOTÉTICO, no consumo medido | Comparar cable bloqueado desmontable (referencia de coste) frente a WPT regulado; no elegir aún |
| WPT sencillo Mark Belbin GPL-3.0 | Autor: 100W, 81,3% y 1–2mm, NO probado en nuestro diseño, feedback/FOD insuficientes | Solo referencia, sin código/CAD copiados |
| WPT regulado | FOD, termometría, corte independiente, humedad, desalineación y EMI pendientes | Evaluar tras banco aislado; no motores/bombas |
| Datos ESP-NOW Apache-2.0 | Radio MAC no equivale ACK aplicativo; CCMP depende configuración/unicast | Primer candidato; medir si cifrado de aplicación compensa |
| Datos OpenThread BSD-3-Clause | Requiere 802.15.4, evaluación hardware/topología | Alternativa, no doble stack |
| WISP5 BSD-2-Clause | Sensores RFID de muy baja energía y lector dedicado | Posponer salvo microsensor |

**Auditoría autores 31/10 GitHub (pin 19-alternativas):** mark-belbin/simple-wireless-power master 7c7858c0 SAME (GPL-3.0); wisp/wisp5-hw master 08332bc3 SAME (BSD-2); wisp/wisp5 **640kHz 604eee2d** DIVERGE del pin d978a697 (**68 ahead/11 behind**, BSD-2); espressif/esp-now master c3b5f9be SAME (Apache-2); openthread/openthread main **b6d0f06d**, 18 ahead/0 behind del pin 7009584d (BSD-3). PR/release de autores: Mark #1 (2021), WISP firmware #40 (no incorporar como HEAD), ESP-NOW #151/#153, OpenThread #13790/#13823 y v2026.10.0. OOMWOO main f01a1b29, firmware ce05f266, PCB 87aa7d38, CAD 038002dd; solo consulta. OOMWOO automation deshabilitada, PR #79 fuera de W. Clone VALDO local sucio ajeno sin editar; rama PR #9 propia autorizada. Nada copiado bajo GPL.

Fuentes: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html ; https://cryptography.io/en/latest/hazmat/primitives/aead/ ; https://csrc.nist.gov/pubs/sp/800/38/d/final .

**Puerta siguiente:** determinar en MCU económico si el cifrado adicional compensa al CCMP nativo, con claves y antirrollback reales; medir latencia/energía/paquetes RF bajo seguridad; dock/potencia WPT aparte. No comprar, energizar ni autorizar hardware.
