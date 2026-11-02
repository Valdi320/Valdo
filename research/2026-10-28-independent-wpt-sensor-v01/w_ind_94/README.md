# W-IND-94 — cierre de regresión CI en ACK duplicados (01-11-2026)

**Alcance propio W; solo robot abierto independiente.** No modificar Xiaomi, OOMWOO, CAD de compañeros ni estación/batería. Este hito **reconcilia una prueba antigua con la semántica W60** y añade tres casos adversariales, sin tocar el protocolo en producción.

## Problema reproducible

CI general anterior [run 41294041922](https://github.com/Valdi320/Valdo/actions/runs/41294041922), job 124811037065: **428/429 PASS, 1 FAIL**. `test_power_restart_gate.GateTests.test_seq_duplicate_on_same_epoch` esperaba que una segunda trama DATA idéntica no devolviese ACK. W60 permite **dos re-ACK iguales, autenticados y limitados temporalmente** tras perderse el ACK original. No entrega dos veces el dato ni actualiza `last_ms`. El test anterior contradice `test_w_link.TestReceiver.test_replayed_and_reordered` y W60.

## Cambio verificable

- Actualizada la prueba antigua para exigir ACK original + exactamente dos re-ACK y bloquear el tercero, sin refrescar `last_ms` ni `last_seq`.
- Tres regresiones nuevas: indicador de autenticación no booleano no consume cupo; misma secuencia con carga cambiada no consigue ACK; retransmisión dentro del margen no prolonga el vencimiento de telemetría (250 ms) ni rearma tras fallo.
- **Código de producción sin cambios:** `w_link.py`, W60, W93, formato de 22 bytes, CRC y plazos permanecen idénticos. `authenticated_transport=True` es un *stub* de test; NO implementa HMAC/AEAD.
- Un duplicado re-ACKado NO autoriza actuadores ni carga; el corte crítico es físico independiente. Sin radio ni banco físico conectados.

## Reproducción y criterios

```bash
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m unittest -v test_power_restart_gate test_w_link
# Regresión completa: workflow .github/workflows/wpt-sensor-v01.yml
```

Resultado esperado de la suite general después del parche: **432/432** si el resto permanece igual (429 pruebas previas más tres nuevas). Este número es *esperado* hasta que GitHub Actions lo confirme. No clasificar como PASS ningún run que no sea `conclusion=success`.

## Matriz de decisión

| Alternativa | Resultado | Razón |
|---|---|---|
| Mantener 2 re-ACK idénticos con autenticación y ventana | **Elegida, solo en software** | Recuperación ante ACK perdido; prueba de no extender frescura |
| Desactivar re-ACK para satisfacer test desactualizado | Rechazada | Rompería la recuperación W60 |
| Aceptar re-ACK de payload cambiado o indicador truthy | Rechazada | Abre rutas de falsos positivos |
| Extender validez de lectura por paquetes duplicados | Rechazada | No demuestra muestra nueva; podría ocultar sensor parado |
| Usar radio como interbloqueo de seguridad del WPT | Prohibida | Necesario corte eléctrico autónomo |

## Auditoría de dependencias, propietarios y límites

Consulta GitHub de **01-11-2026** y comparación con `19-alternativas-abiertas-para-robot-independiente.md` (28-10):
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, `master`: `7c7858c0dd7040801b6f191df1396115560218f0`, sin cambio.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause, `master`: `08332bc398aa3350d351ef2aaac163f8007cffda`, sin cambio.
- [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause: `master` sigue `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`; rama **`640kHz`** `604eee2dffaeba3a270de61cf3dae887a33309c2`, historia divergente (68 ahead / 11 behind frente a master), **no** considerar HEAD de `640kHz` sustituto automático de master.
- [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0, `master`: `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5`, sin cambio; ACK de enlace no equivale a ACK aplicativo.
- [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause, `main`: `c6872259f4194fb76c7d333bda209343e8c88e71`, **21 commits después** de `7009584dadc20cf20c20a6062f357dd572ba6885`; [PR #13800](https://github.com/openthread/openthread/pull/13800) cambia control de estado MLE, no justifica integrar código aquí.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo), Apache-2.0, `main` actual `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` (star-history); adaptación VALDO+OOMWOO conserva clones fijados el 28-10. No editados.
- VALDO PR #9 propia, HEAD anterior `1e8ee0dd1383b0dc818955f460ee735e538af75d`. El working tree local `codex/instrucciones-punto-dulce-20261029` contiene cambios de compañeros; **no utilizado ni modificado**. Automatización OOMWOO está desactivada. No se copiaron archivos de los autores.

## Fronteras y pendientes

**Evidencia:** lógica, asserts y GitHub Actions sobre datos sintéticos; **0 mediciones físicas y 0 radios probadas**. No prueba autenticación criptográfica ni independencia de cortes eléctricos. El dock de carga, WPT distribuido y la radio real permanecen tres subsistemas distintos. Antes de conectar una batería: FOD, UVLO, temperatura, offset, EMI, aislamiento, corte físico, retardo y consumo total medidos en banco autorizado. La continuidad eléctrica y el cable sustituible siguen como línea base.

**Próximo hito potencial, NO iniciado:** banco RF+receptor aislado con carga ficticia para medir ACK/energía total y la reserva energética real.
