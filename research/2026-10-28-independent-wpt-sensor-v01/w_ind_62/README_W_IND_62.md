# W-IND-62 — reserva fail-closed de epoch (31/10/2026)

**Objeto:** nuevo robot abierto y reparable, ámbito propio VALDO W, PR #9. **Cero** acciones Xiaomi OEM, OOMWOO/PR #79, hardware físico, compras, litio, motores, estación o clones upstream.

## Problema y solución verificable

W61 autentica DATA y ACK, pero después de un reinicio la misma clave + epoch permitiría replays válidos porque la secuencia del receptor se reinicia. `EpochIssuer` **no entrega el AuthCodec** hasta que una interfaz de almacén confiable valida su checkpoint y confirma **durablemente y atómicamente** una reserva única. El token HMAC-SHA256 de `epoch` es independiente de número de sesión y nodo: con la misma clave no se admite reutilizar el epoch cambiando esos campos. Cualquier fallo de lectura/escritura, estado borrado/no fiable, reserva duplicada, o resultado distinto de `True` bloquea la expedición. Después de una reserva, un crash antes de devolver el codec quema la época, evitando su reutilización.

### Límite crítico

**NO existe aún un almacén NVM real, ni antirollback físico, ni aprovisionamiento de secretos, ni generador CSPRNG validado, ni integración de esta puerta como única vía de construcción W61.** `FakeLedger` en tests y `FixtureStore` en demo son memoria ordinaria: no persisten tras apagado y un snapshot restaurado puede permitir replay. El contrato `DurableOnceStore` exige verificación contra borrado/rollback, escritura durable atómica y power-fail/cross-process; una API Python no demuestra que el hardware cumpla. Los valores de prueba son públicos, NO para desplegar. Claves expuestas, ataques de DoS, falta de cifrado, privacidad y seguridad física permanecen sin resolver. Esto es una mejora digital **condicionada**, no un dispositivo seguro aprobado.

## Reproducción

En `research/2026-10-28-independent-wpt-sensor-v01/`:

```sh
python3 -m unittest -v test_w_link
python3 -m unittest discover -v -s w_ind_60 -p 'test_w60.py'
python3 -m unittest discover -v -s w_ind_61 -p 'test_w61.py'
python3 -m unittest discover -v -s w_ind_62 -p 'test_w62.py'
python3 w_ind_62/w62_demo.py > W62_SYNTHETIC_EPOCH_REPLAY_GUARD.json
```

23 tests nuevos cubren doble uso, reinicio simulado **con memoria conservada entre objetos**, epoch nuevo, DATA viejo rechazado, ACK W61 nuevo, fallos de almacenamiento, no-booleanos, inputs inválidos y crash tras commit. Pruebas de persistencia física **0**. CI produce JSON inequívocamente `SYNTHETIC_ONLY`.

## Decisiones, BOM y límites

| Área | Estado | Condición |
|---|---|---|
| Dock de carga | Diferido | Batería/BMS desconectados. FOD, temperatura, EMI, offset y corte autónomo físico sin verificar. |
| Potencia a módulo | Primer piloto **hipotético** 5 V, 0,4 W medio, 1,5 W pico | Mantener arnés reemplazable como referencia; comparar WPT sencillo vs regulado con coste, eficiencia, mantenimiento, FOD y calentamiento medidos. No WPT por defecto en motores/bombas. |
| Datos | W60 ACK/CRC/secuencia/timeout, W61 HMAC, W62 reserva lógica | ESP-NOW o OpenThread no elegidos; no hay radio física ni privacidad cifrada. WISP solo microsensores. |

BOM y matriz adjuntas. **0 € de electrónica incremental de este algoritmo** no significa que hardware de memoria/radio/WPT sea gratuito. Diotronic es **auxiliar**; stock de tienda Zaragoza, MOQ y precio final IVA/portes **pendientes**; piezas críticas deben tener trazabilidad de fabricante y distribuidor especializado.

## Revisión de autores, ramas, HEAD y pins (GitHub, 31/10/2026)

| Autor/proyecto; licencia | Rama y HEAD | Contra pin 19-alternativas |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master [7c7858c0](https://github.com/mark-belbin/simple-wireless-power/commit/7c7858c0dd7040801b6f191df1396115560218f0) | idéntico, 0 cambios |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master [08332bc3](https://github.com/wisp/wisp5-hw/commit/08332bc398aa3350d351ef2aaac163f8007cffda) | idéntico |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | **640kHz** [604eee2d](https://github.com/wisp/wisp5/commit/604eee2dffaeba3a270de61cf3dae887a33309c2) | **divergida**: 68 ahead, 11 behind vs d978a697; no fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master [c3b5f9be](https://github.com/espressif/esp-now/commit/c3b5f9be245f1a80db9cb938600566aa6a8dd1e5) | idéntico |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main [b6d0f06d](https://github.com/openthread/openthread/commit/b6d0f06db304055f5866ff6e3c67370b54c81b15) | 18 ahead, 0 behind vs 7009584d; radio power-table #13790 y CLI #13823 no alteran selección |

Comparación GitHub commits y HEAD frente a pins maestros; ver también [OpenThread v2026.10.0](https://github.com/openthread/openthread/releases/tag/v2026.10.0). No se copia fuente ni CAD de autores; revisiones de PR abiertas no proporcionaron inventario exhaustivo, no se afirma ausencia. [makerspet/oomwoo main f01a1b29](https://github.com/makerspet/oomwoo/commit/f01a1b295f462da5ab8d5f021a3f741cbd2b47df) cambia star-history y PR #78 ya fue fusionada. VALDO W PR #9 partía del commit a3d84dc3. La adaptación local VALDO_OOMWOO se conservó sin cambios.

**Siguiente puerta:** seleccionar backend NVM realmente antirrollback y demostrar commit atómico ante brownout, además de entropía y provisión de claves. No aprobar energía ni seguridad con la prueba digital.
