# W-IND-04: sesión persistente anti-replay tras corte WPT (solo laboratorio software)

**Robot NUEVO, independiente, sector W.** Reutiliza exclusivamente ideas generales de VALDO y OOMWOO. No trasplante Xiaomi X20 Pro, firmware/estación/BMS OEM, movimiento mecánico C ni PR #79 cleaning-jobs. **Sin prototipo energizado, carga, compras ni cambios en equipos.** Código original Python, sin copiar GPL/BSD/Apache de terceros.

## Mejora concreta verificada

W-IND-03 usa `VolatileEpochStore` por diseño: al reiniciarlo pierde la sesión anterior y un identificador antiguo puede volver a admitirse. `durable_epoch_store.py` sustituye ese fake por una implementación de **almacenamiento persistente en un HOST Linux/POSIX**, compatible con el contrato `EpochStore.claim(node_id, session)`. El firmware embarcado MCU/ESP32 **NO ESTÁ IMPLEMENTADO**.

* Provisionamiento explícito de la lista de IDs, protegido contra sobrescritura accidental (`O_EXCL`). Una base ausente/corrupta/no provisionada **NO se recupera automáticamente**.
* Control SQLite transaccional: `BEGIN IMMEDIATE` + `UPDATE ... WHERE last_epoch < ?` + `COMMIT`, `journal_mode=DELETE` y `synchronous=EXTRA`; tras commit, la sesión repetida se rechaza incluso después de reiniciar el proceso.
* Lecturas inválidas, lock ocupado, escritura dudosa, versiones desconocidas y ausencia del nodo: no se arma telemetría. En caso de commit efectuado pero ACK local perdido, la operación devuelve error y requiere la siguiente sesión creciente.
* Dos instancias compitiendo por la misma sesión: solo una puede obtener `True` (banco de concurrencia). No hay wrap del contador `0xffffffff`.
* Inyección de una muerte `os._exit(77)` en un proceso hijo con transacción SQLite abierta: la escritura sin `COMMIT` revierte tras reabrir el diario. **No equivale a cortar físicamente la alimentación.**

### Reproducción

```bash
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m py_compile durable_epoch_store.py test_durable_epoch_store.py
python3 -m unittest -v test_w_link test_hold_up_envelope test_power_restart_gate test_durable_epoch_store
```

Los 22 casos nuevos se suman a los **69 previos** (CI integrada pendiente de confirmar). Todos ejecutan dispositivos ficticios y archivos temporales; nunca energía de bobinas o batería.

### Límites y vulnerabilidades restantes

1. SQLite/stdlib es referencia para SBC con almacenamiento fiable. No demuestra **wear leveling, atomicidad, brownout, FRAM o eFuse** en microcontrolador. El comportamiento ante pérdida real de alimentación depende del soporte que dé el hardware a `fsync`, sistema de archivos, controlador, cachés y VFS SQLite.
2. CRC protege accidentalmente del ruido; no acredita autenticación ni cifrado. `physically_authorized=True`, `authenticated_transport=True` y `locally_authorized=True` siguen siendo **simulaciones**. En ESP-NOW serán necesarios LMK unicast, PMK no predeterminada, pareado por identidad y política de claves, con aplicación ACK/seq; OpenThread es alternativa.
3. **Ataque de rollback**: sustituir un DB válido por una copia antigua puede restaurar sesiones previas. Necesita ancla independiente antirretroceso y procedimiento de provisión/recuperación. Un DB perdido o destruido deliberadamente bloquea, no se reinicia a cero.
4. Fallos de SSD/eMMC, pérdida real de energía, ruido radio, cronometraje HW, FOD físico, corte de potencia, temperatura, metal, humedad y EMC: **SIN MEDIR**. La protección eléctrica debe ser normalmente OFF e independiente de CPU/radio. No se propone WPT para motores ni bombas.
5. Frecuencia de escritura: una transacción solo al reautorizar una sesión, no por telemetría; 5 reinicios/día ≈1825 commits/año (hipótesis). El firmware real requiere presupuesto de desgaste y estrategia de recambio/reparación.

## Contrato de tres sistemas

| Sistema | Decisión actual | Próxima condición obligatoria |
|---|---|---|
| Dock→batería | pospuesto; BMS sin conectar | cargador y BMS del robot nuevo, FOD/temperatura/corte independientes |
| Base→módulo no crítico | objetivo HIPOTÉTICO 5V, 0,4W medio y 1,5W pico; sin hold-up 150ms forzado | pareja WPT regulada, protección, desviación bobinas, coste UE, EMI y prueba con resistencia aislada |
| Datos independientes | tramas W-IND-01; brownout W-IND-03; NVM host W-IND-04 | radio cifrada/pareada real, identidad y gestión de claves; watchdog HW separado |

## Matriz de decisión y costes

| Alternativa | Ventaja | Riesgo / decisión |
|---|---|---|
| Cable con cierre positivo | coste y eficiencia probablemente mejores | control económico si WPT no se justifica; propietario C de mecánica |
| mark-belbin/simple-wireless-power GPL-3.0 | diseño abierto de bobina/potencia, aportación del autor | referencia sin FOD/térmico y realimentación integrada demostrada; NO reutilizado |
| TX/RX regulados + supervisor externo | módulo sellado desmontable sin contactos | candidato de banco, aún sin proveedor/stock/precio comprobado |
| ESP-NOW Apache-2.0 | radio unicast ESP, ACK app externo | requiere LMK/PMK, pareado; código fuente ajeno NO copiado |
| OpenThread BSD-3 | IPv6/mesh si realmente aporta | requiere IEEE 802.15.4 y más integración |
| WISP5 BSD-2 | micropotencia RFID | no alimenta sensor continuo de 0,4W |

La BOM W-IND-04 identifica todos los elementos restantes como **NO SELECCIONADOS**, sin precios inventados. El único componente software nuevo es SQLite del Python estándar. Por tanto no existe presupuesto total verificable ni compra autorizada.

## Auditoría creadores y revisiones GitHub, 28/10/2026

Se compararon los SHAs de `19-alternativas-abiertas-para-robot-independiente.md` con HEAD/ramas originales **antes de editar este hito**:
* [Mark Belbin, simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, `master 7c7858c0dd7040801b6f191df1396115560218f0`: mismo SHA; PR #1 TX board v1.1 cerrada.
* [WISP5 HW](https://github.com/wisp/wisp5-hw), BSD-2, `master 08332bc398aa3350d351ef2aaac163f8007cffda`: mismo SHA; PR #1 cerrada.
* [WISP5 firmware](https://github.com/wisp/wisp5), BSD-2, rama **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2`: **68 adelante y 11 atrás** respecto a pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`; historia divergente, no actualización lineal; PR #38 cerrada.
* [Espressif ESP-NOW](https://github.com/espressif/esp-now), Apache-2, `master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5`: mismo SHA; PR #153 cerrada.
* [OpenThread](https://github.com/openthread/openthread), BSD-3, `main 3d645eb9106cb1d5c2ff11891e84dc14e52e293a`: cinco commits delante de pin `7009584dadc20cf20c20a6062f357dd572ba6885`; cambian radio.h/SubMac/heap/CI; PR #13804 y #13802 **abiertas**, no tratadas como ya incorporadas.
* [OOMWOO oficial](https://github.com/makerspet/oomwoo), `main 1c2bd43abcf74288afcf2d8b64514cc325f9b905`, sin cambio frente a lectura anterior; PR #79 abierta de un compañero, no modificada.
* GitHub Valdi320/Valdo rama de este módulo `w/independent-sensor-wpt-link-20261028` PR #9 propia. Repo local `master` tenía cambios ajenos sin commitear: se ha trabajado SOLO en la rama GitHub propia, no en el checkout compartido.

**Fuentes independientes:** [SQLite synchronous EXTRA](https://www.sqlite.org/pragma.html#pragma_synchronous), [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html), [Python os/posix](https://docs.python.org/3/library/os.html), [ESP-NOW docs oficiales](https://documentation.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/network/esp_now.html). Referencias no implican homologación.

**Siguiente hito:** comparar al menos dos parejas comerciales de WPT de baja potencia, documentar hojas técnicas y disponibilidad/precio real UE, FOD/térmico y coste integral. Si no se alcanza una opción segura, mantener cableado sustituible. Sin batería ni BMS en pruebas iniciales.
