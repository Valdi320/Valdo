# W-IND-96 — tipos estrictos en identidades y watchdog RF (01-11-2026)

**Alcance:** robot abierto nuevo, sector W exclusivo, PR propia #9. No hay trasplante ni electrónica OEM Xiaomi. No se ha intervenido en el árbol local sucio de otro colaborador, la adaptación OOMWOO, PR #79, forks externos ni hardware.

## Defecto y corrección reproducibles

Antes de W96, `Frame.encode()` admitía booleanos porque `bool` hereda de `int` en Python: `kind=True` equivalía a DATA, `session=True` a sesión 1, `seq=True` a secuencia 1 y `value_milli=True` a 1. `ModuleReceiver(7, float("inf"))` aceptaba un timeout infinito: la muestra nunca caducaría por edad matemática; `ModuleReceiver(7, True)` fijaba inadvertidamente un watchdog de 1 ms. También se admitía `max_attempts=float("nan")` y sesiones booleanas en comisionado local. Es un defecto de validación en software **experimental**, no una vulnerabilidad de un robot desplegado.

**Cambio atómico de política:** todo campo entero en la serialización, tipo de trama, identidad de nodo/sesión, número de secuencia, comisionado y parámetros de temporización/reintentos exige `type(x) is int`. Campos inválidos devuelven `ValueError` ANTES de establecer identidad, estado de comisionado o transacción pendiente. El paquete normal sigue midiendo 22 bytes; CRC-16 CCITT-FALSE, ACK de aplicación, sesión, caducidad, 60 ms retry, 240 ms expiry, hasta 3 envíos y re-ACK acotado se mantienen.

**Reproducción digital:** `cd research/2026-10-28-independent-wpt-sensor-v01 && python3 -m unittest -v test_w_link`. Los diez métodos `TestW96StrictProtocolNumbers` cubren booleanos en todos los campos, floats/NaN/Inf, watchdog, comisionado, contador de intentos, no-consumo de secuencia y recuperación ACK legítima. La CI existente `.github/workflows/wpt-sensor-v01.yml` ejecuta esta suite y regresiones. Clase de evidencia: **SOFTWARE_SINTETICO**. Un test digital que pasa no demuestra HMAC/CCMP reales, privacidad, robustez RF ni seguridad física.

## Decisión de arquitectura y límites

| Subsistema | Decisión | Falta comprobar |
|---|---|---|
| Datos RF: validación estricta de tipos | ADOPTAR para Python de laboratorio | Port a MCU y ejecución ESP-NOW/OpenThread real |
| ESP-NOW / OpenThread | Alternativas exclusivas en evaluación | ACK aplicativo autenticado, secuencia, CRC, latencia, pérdidas, cifrado, recuperación y radio real; la confirmación MAC no basta |
| Alimentación de microsensor | Cable sustituible como baseline; WPT regulado solo candidato | Voltaje/potencia bajo carga, offset, pérdidas, FOD, temperatura, EMI, corte local independiente normalmente OFF |
| WPT sencilla lazo abierto | RECHAZAR para integración sin protecciones verificadas | Control de potencia y FOD; modelo no equivale a seguridad |
| Dock de carga | BLOQUEADO | Proceso de seguridad, batería y BMS separados, FOD/humedad/corte autónomo |
| WISP5 RFID | Sólo microsensores de potencia mínima | Lector y balance de energía, sin extrapolar a 0,4 W |

Nunca depender de radio para parada de emergencia, borde, choque o motores. No asumir WPT para bombas, turbinas o tracción. No se energizan bobinas, baterías, estaciones ni dispositivos. El ERC del esquema W18 permanece bloqueado; no intervenir sin dueño de circuito y revisión técnica.

## Autores y pines comprobados (01-11-2026)

Repositorio del autor / licencia / HEAD rama / SHA registrada 28-10:

- [Simple Wireless Power, mark-belbin](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, master `7c7858c0` = pin; última PR #1 fusionada 2021. Diseño lazo abierto, resultados del autor, no copiados.
- [WISP5 hardware, wisp](https://github.com/wisp/wisp5-hw), BSD-2-Clause, master `08332bc3` = pin; PR #1 fusionada 2015.
- [WISP5 firmware, wisp](https://github.com/wisp/wisp5), BSD-2-Clause, **640kHz `604eee2d`** vs pin `d978a697`, diverge +68/−11; PR #40 abierta, no inferir rama nueva por antigüedad.
- [ESP-NOW, Espressif](https://github.com/espressif/esp-now), Apache-2.0, master `c3b5f9be` = pin; PR #153 cerrada sin fusionar. [Documentación](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html): callback MAC ≠ recepción en aplicación.
- [OpenThread](https://github.com/openthread/openthread), BSD-3-Clause, main `c6872259` vs pin `7009584d`, +21/0; PR #13554 TCP y #13828 joiner abiertas a 01-11, sin ventaja demostrada para nuestro enlace.
- OOMWOO oficial [principal](https://github.com/makerspet/oomwoo) main `f01a1b29`, [firmware](https://github.com/makerspet/oomwoo-firmware) `fd8689f3`, [PCB](https://github.com/makerspet/oomwoo-pcb) `ac8ac0b5`. Adaptación VALDO_OOMWOO no tocada. Licencias/autores conservados; ningún código/CAD tercero copiado.

## BOM, evidencia, seguridad y siguiente puerta

Se adjuntan `BOM_DECISION.csv`, `MATRIZ_DECISION.csv` y `EVIDENCIA.json` con comandos y procedencia. **Coste incremental de hardware del parche = 0 EUR**; ingeniería/CI y coste de producto no calculados. Diotronic es auxiliar (pasivos, conectores, prototipado); no hay referencia equivalente para protecciones críticas, ni stock local, MOQ ni precio final IVA comprobado; comparar TME/Mouser/DigiKey al definir cesta real, sin compras.

**Siguiente hito permitido sólo con autorización y protocolo de seguridad:** medir consumo lector/RX y comportamiento real de ACK y arranque en banco aislado con carga ficticia; sin litio/BMS/dock/motores, ensayos térmicos/FOD y desconexión autónoma. No se aprueba ningún circuito ni eliminación de cable.
