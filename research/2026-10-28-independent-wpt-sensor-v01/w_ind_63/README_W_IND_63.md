# W-IND-63 — Diario SQLite con ancla antirrollback **EXTERNA** (31/10/2026)

**Ámbito:** solo diseño propio VALDO W para un robot aspirador NUEVO, local, abierto, reparable e imprimible. No usa la electrónica, firmware, batería ni estación Xiaomi. No edita OOMWOO, PR #79, CAD C ni trabajo de terceros. **Sin autorización para energizar circuitos, cargar litio ni instalarlo en un robot.**

## Mejora concreta y problema

W62 bloqueaba épocas criptográficas repetidas **solo con almacenamiento simulado en RAM**. W63 implementa la **parte realmente persistente en un archivo SQLite**, con reserva transaccional de tokens HMAC de W62, cadena SHA-256 de eventos y confrontación contra un ancla externa inmutable por el atacante. Se reabre la base en un objeto nuevo y el token permanece usado. Una restauración de un snapshot viejo de SQLite produce discrepancia y **bloquea**, siempre que el ancla siga intacta y sea verdaderamente confiable.

### Modelo de seguridad; prohibición de despliegue

No hemos implementado ni elegido una **ancla antirrollback física**, ni probada su resistencia a cortes de alimentación o manipulación. `TrustedAnchor` es un protocolo que **debe aportar hardware externo**: `read_checkpoint()` y `advance_from(old,new)` como CAS monotónico, persistente, atómico y no reversible. El `FakeAnchor` publicado bajo `test_w63.py` es **RAM ordinaria**, sirve únicamente para tests y **se puede restaurar/falsear**. No es protección desplegable. Ninguna instancia SQLite por sí sola es un antirollback confiable. No se aporta aprovisionamiento seguro, secreto físicamente protegido, entropía calificada ni cifrado de radio. No hay pruebas reales de caída de alimentación ni ataque físico.

**Orden conservador de transacción:** adquirir exclusión SQLite `BEGIN IMMEDIATE`; reconstruir toda la cadena de tokens y comparar `(contador, hash)` con el ancla; insertar y actualizar en transacción; **avanzar primero el ancla** mediante CAS; confirmar SQLite después. Una caída entre el avance externo y el COMMIT bloquea la siguiente emisión: se sacrifica disponibilidad para evitar replay. No hay recuperación automática de estados divergentes ni creación implícita si falta la base. Solo el aprovisionamiento explícito en un par virgen `(0,GENESIS)` crea SQLite. Colisiones SHA-256, robo de ancla/secretos, pérdida conjunta de ancla + base, integridad física y ataques DoS no quedan probados.

**SQLite:** `journal_mode=DELETE`, `synchronous=EXTRA` (no solo FULL) y modo apertura `rw`, archivo creado `0600` en POSIX, `quick_check`, verificación de cadena en cada reserva. La documentación de SQLite aclara que `EXTRA` sincroniza también el directorio al eliminar journal en DELETE y que la garantía depende del VFS/dispositivo/`fsync`, no solo de SQL: [PRAGMA synchronous](https://www.sqlite.org/pragma.html), [atomic commit](https://www.sqlite.org/atomiccommit.html), [fallos flash](https://www.sqlite.org/howtocorrupt.html). Los tests no simulan electricidad ni prueban las hipótesis de un SSD/eMMC. Inicialización no es a prueba de un corte físico medido. La implementación **no es tiempo real** y la reserva ocurre únicamente durante alta local, nunca en el lazo de seguridad ni en un callback radio.

## Reproducción y evidencia

```bash
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m unittest discover -v -s w_ind_63 -p 'test_w63.py'
python3 -m unittest discover -v -s w_ind_62 -p 'test_w62.py'
python3 -m unittest discover -v -s w_ind_61 -p 'test_w61.py'
python3 -m unittest discover -v -s w_ind_60 -p 'test_w60.py'
python3 -m unittest -v test_w_link
python3 w_ind_63/w63_demo.py > W63_SQLITE_SYNTHETIC_ANCHOR.json
```

19 pruebas W63: reabrir SQLite, duplicados, hilos concurrentes, snapshot viejo, borrado, corrupción, ancla alterada, pérdida entre CAS y COMMIT, errores de token, permisos y puerta de W62. **Una prueba de integración W62 se omite en carpeta aislada sin el checkout completo**; debe ejecutarse con todos los módulos del repositorio en CI. Evidencia JSON usa SQLite temporal real **y ancla sintética en memoria**. Cero pruebas de corte real, radio, WPT, motores, BMS o batería.

## Decisión por subsistema

| Problema | Estado comprobado | Siguiente puerta |
|---|---|---|
| Dock de carga | **Diferido**; sin batería/BMS ni carga de litio | Banco resistivo aislado con límites de energía, FOD, temperatura, humedad, offset, EMI y dos cortes autónomos; revisión de seguridad |
| Potencia distribuida a módulo | Piloto de sensor **hipotético** 5 V/0,4 W medio, 1,5 W pico; eficiencia aún sin medir | Elegir bobina y regulación tras comparar WPT simple/regulated y cable desmontable económico; no aplicar a motores/bombas |
| Datos inalámbricos | W60 ACK+CRC+secuencia+timeout, W61 HMAC, W62 epoch, **W63 SQLite condicionada al ancla** | Evaluar ESP-NOW/OpenThread con radio real, privacidad (HMAC NO cifra), claves y antirrollback reales; radio nunca para parada crítica |
| WISP | Secundario | Solo microsensores de presupuesto sub-mW si lector, coste y continuidad compensan |

### WPT simple frente a regulado (candidatos, no mediciones)

| Alternativa | Eficiencia/temperatura/offset/EMI/FOD y corte | Reparabilidad/coste |
|---|---|---|
| Cable desmontable bloqueado | Sin pérdida inductiva; aun debe cumplir protección mecánica | Referencia económica obligatoria |
| Inductivo simple, referencia [Mark Belbin](https://github.com/mark-belbin/simple-wireless-power) | Referencia autor hasta 100 W / 81,3 % a 1–2 mm; **NO** probado para nuestro sensor ni protege por sí solo FOD, offset, EMI, calor o corte | GPL-3.0; no se ha copiado fuente; nueva protección/control exigiría coste adicional |
| Inductivo regulado de bajo consumo | Potencia/electricidad real desconocidas; exige medir pérdidas, FOD y corte independiente ANTES de elección | Mejor candidato de control solo si coste BOM+servicio+consumo supera al cable; sin pieza aprobada |

## BOM incremental y abastecimiento

`BOM_W_IND_63.csv`: cero piezas nuevas **solo de este algoritmo**; almacenamiento antirrollback hardware sigue sin seleccionar, y su coste NO puede considerarse 0 €. No se ha confirmado el stock físico de Diotronic Zaragoza, MOQ ni precios puestos en Zaragoza (con IVA/portes), y no se inventan. Diotronic auxiliar para pasivos/conectores; hardware de seguridad exige fabricante identificable + documentación y distribuidor especializado (TME/Mouser/DigiKey según pieza concreta). No comprar.

## Auditoría de autoría, HEAD, ramas, PR y versiones (consulta GitHub 31/10/2026)

Los SHAs base proceden de `19-alternativas-abiertas-para-robot-independiente.md` (28/10):

| Autor y licencia | Rama HEAD del autor | Comparación con pin base; PR/release inspeccionadas |
|---|---|---|
| [Mark Belbin, simple-wireless-power GPL-3.0](https://github.com/mark-belbin/simple-wireless-power) | master [`7c7858c0`](https://github.com/mark-belbin/simple-wireless-power/commit/7c7858c0dd7040801b6f191df1396115560218f0) | igual que pin; PR [#1 TX Board v1.1](https://github.com/mark-belbin/simple-wireless-power/pull/1) antigua |
| [WISP5-hw BSD-2-Clause](https://github.com/wisp/wisp5-hw) | master [`08332bc3`](https://github.com/wisp/wisp5-hw/commit/08332bc398aa3350d351ef2aaac163f8007cffda) | igual; PR [#1 breakout](https://github.com/wisp/wisp5-hw/pull/1) histórica |
| [WISP5 firmware BSD-2-Clause](https://github.com/wisp/wisp5) | **640kHz** [`604eee2d`](https://github.com/wisp/wisp5/commit/604eee2dffaeba3a270de61cf3dae887a33309c2) | frente al pin `d978a697`: **68 ahead, 11 behind**, divergente; commit final CCS11 2022; PR [#38](https://github.com/wisp/wisp5/pull/38) variante 436kHz, NO HEAD adoptable automáticamente |
| [Espressif ESP-NOW Apache-2.0](https://github.com/espressif/esp-now) | master [`c3b5f9be`](https://github.com/espressif/esp-now/commit/c3b5f9be245f1a80db9cb938600566aa6a8dd1e5) | igual al pin; PR [#151 compatibilidad IDF 5.5](https://github.com/espressif/esp-now/pull/151) y [#153 wakeup](https://github.com/espressif/esp-now/pull/153); última release encontrada [v1.0](https://github.com/espressif/esp-now/releases/tag/v1.0) (2022) |
| [OpenThread BSD-3-Clause](https://github.com/openthread/openthread) | main [`b6d0f06d`](https://github.com/openthread/openthread/commit/b6d0f06db304055f5866ff6e3c67370b54c81b15) | **18 ahead, 0 behind** vs pin `7009584d`; cambios radio power-table [#13790](https://github.com/openthread/openthread/pull/13790) y CLI [#13823](https://github.com/openthread/openthread/pull/13823); release [v2026.10.0](https://github.com/openthread/openthread/releases/tag/v2026.10.0) |

[makerspet/oomwoo oficial](https://github.com/makerspet/oomwoo) main [`f01a1b29`](https://github.com/makerspet/oomwoo/commit/f01a1b295f462da5ab8d5f021a3f741cbd2b47df) cambia gráfico de estrellas, PR #78 cleaning-jobs fusionada y #79 de otro ámbito; no editados. VALDO W PR #9 propia, último HEAD consultado **`74a96c3f`** antes del hito; adaptación local VALDO_OOMWOO archivada y sin edición. Se revisaron owners/locks y la tarea OOMWOO deshabilitada; ningún otro trabajo W concurrente se ha sobrescrito. **No se ha copiado código ni CAD externo.**

## Puerta siguiente

Seleccionar dispositivo real con **contador+digest protegidos y CAS atómico** verificable, y pruebas de brownout/fallo de memoria. Si tal dispositivo es inviable/caro, preferir una solución convencional con cable robusto o autenticación remota sin afirmar antirrollback físico; nunca prometer cero conectores a costa de seguridad.
