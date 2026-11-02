# W-IND-03 — Reinicio seguro de telemetría tras microcortes de WPT (28/10/2026)

**Robótica nueva e independiente. No electrónica, batería, firmware ni estación Xiaomi.** Este hito añade solo software experimental original y un contrato de alimentación; no habilita carga de litio, TX, bobinas, motores ni parada funcional.

## Defecto concreto que corrige
W-IND-02 descartó exigir 150 ms de supercondensador para el sensor reemplazable (0,4 W medio / 1,5 W pico **HIPOTÉTICOS**). Eso permite que el receptor se reinicie con una interrupción WPT, pero exige que los datos anteriores al corte NO se acepten al volver a recibir energía. W-IND-01 `ModuleReceiver.commission_local()` limpia el estado y permite, si el integrador recicla accidentalmente una sesión, aceptar otra vez un mensaje antiguo.

**Nuevo `power_restart_gate.py`:** un adaptador externo rodea `ModuleReceiver`. Arranca bloqueado; exige alimentación/temperatura/FOD externos afirmativos con muestreo continuo, 100 ms estables, autorización local explícita y sesión monotónica aceptada por un registro transaccional; solo entonces procesa datos. Deshabilita la telemetría inmediatamente ante corte, exceso térmico, FOD, reloj reverso, lectura desconocida, pérdida de monitorización, expiración de datos o fallo del registro. Requiere **nueva sesión** para rearmar: recibir radio no restaura el permiso.

### Contrato numérico (objetivos sintéticos, NO datos eléctricos)
| Señal / criterio | Objetivo del piloto | Quién lo deberá probar |
|---|---|---|
| Módulo desmontable | 5 V, 0,4 W nominal / 1,5 W máximo | W mide consumo físico |
| Sampleo de POWER_GOOD, TEMP_OK, FOD_CLEAR | separación <=20 ms | W supervisión de baja tensión; fuente independiente |
| Estabilización continua | 100 ms tras POWER_GOOD | W mide rizado, inrush y transitorios |
| Datos aceptados tras restablecer V | **No**, hasta `commission()` local y epoch nuevo | W firmware+host |
| Expiración del último dato | 250 ms; no es temporizador de seguridad | W enlace real ESP-NOW u OpenThread |
| Nuevo epoch | entero 1..2^32-1, estrictamente creciente por nodo | W NVM duradera con claim atómico y política desgaste |
| Cortes de fuente / sobretemperatura / FOD | hardware normalmente OFF, autónomo, sin paquetes RF | W circuito FOD/temperatura + ensayos de fallo |
| TX/RX, gap/offset, EMI, agua, costes UE | no seleccionados/no medidos | W futuro banco aislado y compra únicamente autorizada |

### Matriz de decisión
| Alternativa | Decisión actual |
|---|---|
| Cable con conector de servicio | Mantener como control económico: puede ser más barato y estable |
| Pareja WPT simple en lazo abierto | Solo referencia; no se acepta para sensor conectado sin regulación y protección |
| WPT TX/RX regulados + monitor independiente | Candidato para banco aislado; FOD y corte físico pendientes |
| Radio ESP-NOW unicast cifrado | Preferencia inicial de datos; ACK de aplicación, CRC y secuencia existentes en W-IND-01; claves y privacidad reales **NO** implementadas |
| OpenThread 802.15.4 | Alternativa si red mallada/interoperabilidad justifican consumo/coste, con idéntico contrato de aplicación |
| WISP5 RFID | Solo microsensores intermitentes; no sustituye 0,4 W continuos |
| Supercondensador 150 ms | No imprescindible para este sensor no crítico; depende de nuevos perfiles de carga |
| WPT en motores/bombas | RECHAZADO por defecto sin mediciones |

### Fallos y resultados
`test_power_restart_gate.py` añade **28 tests sintéticos**: arranque denegado, tiempo de estabilización, pérdida de POWER_GOOD, alarma térmica, FOD, muestras omitidas, reloj atrasado, radio no autenticada, duplicado y paquete viejo, rearmado local, fallos del registro, reinicio de objeto y seguridad negativa de un nuevo registro volátil. Ejecución local de la nueva suite con **copia mínima de la interfaz de W-IND-01**: 28/28 PASS; la CI en GitHub ejecuta pruebas contra **w_link.py real**, además de las 41 existentes. CI debe ser la referencia de integración.

**Prueba negativa crítica:** un `VolatileEpochStore` recién creado tras un reinicio pierde la historia y ACEPTA de nuevo la misma sesión. Esta prueba confirma el **BLOQUEO**: no hay seguridad de replay tras brownout real hasta implementar NVM transaccional resistente a corte, provisión criptográfica/rotación de claves y autorización local auténtica. `locally_authorized=True` y `authenticated_transport=True` son *stubs de ensayo*, no certificaciones. `CRC16` detecta errores casuales, no autentica. El contador de 32 bits se agota y requiere política segura, no wrap.

### Tres dominios físicos que NO se mezclan
1. **Dock de carga:** pospuesto y completamente desconectado de baterías/BMS; cargador, FOD, térmica y control requieren revisión propia.
2. **Alimentación de módulos:** futuro enlace WPT independiente, con carga resistiva de banco sin baterías. El programa solo supervisa un POWER_GOOD ficticio; jamás energiza o interrumpe físicamente una bobina.
3. **Datos:** ESP-NOW o OpenThread; ninguna respuesta de radio decide el apagado térmico, FOD, corriente o motor.

### BOM incremental W-IND-03
Ver `BOM_W_IND_03.csv`. **No es BOM comprable:** ni transmisor/regulador/protección ni ESP32 concretos están cualificados, ni existe coste total o disponibilidad EU validada. No reservar volumen mecánico a C. El mayor retorno es eliminar el riesgo lógico de aceptar telemetría obsoleta cuando se deja de exigir el supercondensador.

### Fuentes y licencias verificadas (HEAD el 28/10/2026)
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, `master 7c7858c0dd7040801b6f191df1396115560218f0`, PR #1 merge 2021. Abierto sin feedback/FOD propio acreditado, no se copia código.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause, `master 08332bc398aa3350d351ef2aaac163f8007cffda`, PR #1 de 2015. WISP no da energía WPT a ESP32.
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause, `640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2`; frente a pin `d978a697...` **68 ahead/11 behind**, no lineal; PR #38 de compatibilidad R420.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0, `master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` (10/9), PR #153 cerrada sin merge; [IDF ESP-NOW](https://documentation.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/network/esp_now.html) insiste en que MAC SEND_SUCCESS no es ACK aplicación.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause, `main 3d645eb9106cb1d5c2ff11891e84dc14e52e293a` a las 09:43 UTC (28/10), 5 ahead/0 behind de pin `7009584d...`; PR #13804 (scan timeout), #13802 (vecino obsoleto) abiertas.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) HEAD `1c2bd43abcf74288afcf2d8b64514cc325f9b905`; PR #79 de cleaning-jobs de nuestro compañero, **NO TOCADA**. `Valdi320/Valdo` rama propia W `w/independent-sensor-wpt-link-20261028` PR #9, sin modificar base/master ni clones locales.
- No se importa código, CAD ni licencias de autores externos. El repositorio Valdo todavía no elige licencia general, no atribuirle la de proyectos citados.

### Reproducción
```sh
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m unittest -v test_w_link test_hold_up_envelope test_power_restart_gate
python3 -m py_compile w_link.py power_restart_gate.py test_power_restart_gate.py
```

**Siguiente bloqueo físico:** seleccionar TX/RX regulados, comprobar FOD/corte independiente con documentación del fabricante y determinar sus precios totales UE; solo después autorización de banco aislado con carga resistiva. **Batería, BMS y estación siguen sin conectar**.
