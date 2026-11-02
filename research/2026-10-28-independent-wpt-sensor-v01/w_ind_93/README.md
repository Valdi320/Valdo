# W-IND-93 — Blindar el ACK de aplicación contra flags de autenticación no booleanos (01/11/2026)

**ÚNICA mejora:** se ha localizado un defecto reproducible en `w_link.AckTracker.accept_ack()`: comprobaba `if not authenticated_transport`, lo que permitía confirmar una trama ACK con CRC válido usando `authenticated_transport="false"`, `1`, un objeto o cualquier otro valor *truthy*. El resultado era un falso éxito de entrega de telemetría. El receptor `ModuleReceiver` ya exigía `is True`: ahora el emisor aplica exactamente la misma puerta estricta `authenticated_transport is True`.

**Antes:** `ack_tracker.accept_ack(valid_ack,105,authenticated_transport="false") → True` y `acked += 1`. **Después:** devuelve `False`, `acked == 0` y preserva la trama pendiente para nueva evaluación válida. También evita ejecutar el método `__bool__` de objetos suministrados accidentalmente. No cambia el formato de trama de 22 bytes ni el plazo de 240 ms.

Este flag es exclusivamente un **contrato de API software**; escribir `True` a mano NO autentica nada. Un integrador debe verificar criptográficamente un paquete (HMAC W61 o AEAD W64, con secretos/epochs bien aprovisionados) ANTES de pasar el único valor aceptado. El CRC16 sigue detectando errores accidentales pero no certifica identidad ni privacidad. Se conserva ACK aplicativo, secuencia, timeout, latcheo y rechazo de duplicados. **Nunca autoriza el corte de seguridad, motores, carga o potencia WPT.**

## Evidencia y reproducción

```sh
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m unittest -v test_w_link
python3 -m unittest discover -v -s w_ind_60 -p 'test_w60.py'
python3 -m unittest discover -v -s w_ind_61 -p 'test_w61.py'
python3 -m unittest discover -v -s w_ind_93 -p 'test_w93*.py'
python3 w_ind_93/w93_demo.py > W93_SYNTHETIC_STRICT_ACK.json
sha256sum W93_SYNTHETIC_STRICT_ACK.json
```

14 tests adversariales nuevos: casos truthy/falsy no booleanos, `__bool__` hostil, ACK con CRC válido pero no autenticado, reintento posterior válido, CRC alterado, sesión incorrecta, caducidad, duplicado y receptor. La CI existente W61 se amplía para ejecutar regresiones W-IND-01/W60/W61 y W93; prueba de laboratorio **exclusivamente CPU**, sin ESP32/802.15.4, radios, red, ni hardware. El JSON del demo es INVENTADO y verificable por CI, no captura ni medición física. Si fallan regresiones/CI, no declarar hito cerrado.

## Tres problemas separados y límites

- **Dock inductivo de carga:** permanece bloqueado; batería y BMS desconectados; requiere FOD metálico, térmica, humedad, desalineación, EMI, watchdog y corte autónomo normalmente OFF. No se toca estación ni hardware Xiaomi.
- **Alimentación sin contacto de módulos:** se mantiene como estudio en un solo sensor de consumo demostrado, con cable reemplazable como referencia; ninguna potencia WPT se habilita por ACK. No WPT a motores, bombas o turbina sin balance/mediciones.
- **Datos RF:** ESP-NOW (Apache-2.0) frente a OpenThread (BSD-3-Clause) sólo como transportes alternativos, pendientes consumo, autenticación real, latencia y ensayos de fallos. WISP5 (BSD-2-Clause) sólo sirve de precedente de microsensores RFID de energía ínfima.

El endurecimiento **no implementa criptografía, privacidad, almacenamiento de claves, par radio, fiabilidad RF ni seguridad funcional**. W61/W64 son software; no hay ensayos físicos nuevos. No se compró ni modificó nada. El WPT abierto Simple Wireless Power (GPL-3.0) sigue referencia de autor, no se ha copiado.

## Revisión y procedencia

Comparación realizada el 01/11/2026 frente a los SHA maestros del 28/10: mark-belbin/simple-wireless-power master `7c7858c0` sin cambios; wisp/wisp5-hw master `08332bc3` igual; wisp/wisp5 **640kHz** `604eee2d`, **divergencia +68/-11** frente a master registrado `d978a697`; espressif/esp-now master `c3b5f9be` igual; openthread/openthread main `c6872259`, **21 commits por delante** de `7009584d`. OpenThread PR #13828 abierta el 01/11, afecta joiner y no cambia nuestra política. Simple Wireless Power PR #1 fusionada 2021, WISP-hw PR #1 fusionada 2015, WISP FW PR #40 abierta desde 2021 y ESP-NOW PR #153 cerrada sin fusionar. Fuente y derechos permanecen de sus creadores; **cero código externo copiado**.

OOMWOO oficial main `f01a1b29`, firmware `fd8689f3` y PCB `ac8ac0b5` (01/11); VALDO master `8a6030bd`, PR #9 propia W. Adaptación local VALDO_OOMWOO sin cambio; checkout Codex ajeno sucio y sin intervención. OOMWOO PR #79 cleaning-jobs no se modifica. Ver [matriz y BOM](BOM_DECISION.md).

**Siguiente discriminante físico (pendiente de autorización):** registro de verificación criptográfica + ACK y consumo completo por ráfaga sobre radio real y enlace de alimentación independiente, en banco aislado con carga ficticia, sin batería/estación y con seguridad analizada.
