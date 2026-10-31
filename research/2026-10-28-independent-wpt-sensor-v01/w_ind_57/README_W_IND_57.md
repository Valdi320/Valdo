# W-IND-57 — INA219: disparos verificables de dos canales y rechazo de muestras viejas

**30/10/2026. Ámbito W, robot NUEVO abierto y reparable; solo software, SIN hardware.** Se respeta la cancelación del trasplante Xiaomi X20 Pro del 28/10. No se modifican batería, BMS, estación, motores, firmware, CAD de C, repositorios de autores, adaptación OOMWOO ni la PR upstream #79 de cleaning-jobs.

## Una mejora respecto de W50/56

W50 aceptaba flags de frescura CNVR aportados externamente; W57 implementa una **secuencia comprobable de lectura de registros** sobre un puerto de comunicación y reloj **inyectados**. Para dos INA219 en direcciones diferentes, dispara conversiones shunt+bus single-shot, comprueba configuración y CNVR/OVF limpios tras trigger, limita desfase de disparos, sondea CNVR con timeout y reloj monotónico, rechaza overflow y palabras ilegales, valida que la configuración no cambió, lee SHUNT y BUS, y finalmente POWER exclusivamente para verificar que CNVR queda limpio.

Contrato TI INA219: CONFIG=00h, SHUNT=01h, BUS=02h, POWER=03h. Configuración **0x0663**: bus 16 V, shunt ±40 mV, ambos ADC con 16 promedios, shunt+bus triggered. BUS bits 15:3 representan 4 mV por LSB, bit 1 CNVR y bit 0 OVF; SHUNT 10 µV por LSB con signo. Conversión nominal 2 × 8,51 = **17,02 ms**, dato de fabricante, **no es máximo garantizado**. Políticas ficticias de cribado: desfase entre triggers 2 ms, timeout 50 ms y supuesto rango sensor 0–6 V y 0–300 mA, **NO** umbrales de seguridad.

No existe driver I²C real: el único puerto incluido es FakePort, un simulador determinista; FakeClock inyecta tiempo. Sin identidad física de instrumentos, controlador externo, calibración independiente, prueba de orden/integridad de bytes y validación de reloj, NO se aceptará ningún ensayo como medición física. Dentro de un INA219 tensión y corriente no se convierten simultáneamente. El software no calcula eficiencia ni autoriza alimentación.

### Evidencia reproducible digital

Ejecutar desde raíz del repositorio:

    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_57 -p test_w57.py -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_57/w57_i2c_capture.py --demo --out W57_SYNTHETIC_NOT_HARDWARE.json

**19/19 test PASS en sandbox Python**, no en robot ni PC del propietario: CNVR viejo, no-ready, stuck, overflow, reset de configuración, lectura corrupta, fallo de bus, corriente inversa, corriente/tensión fuera de supuestos, dirección duplicada, disparos desfasados y reloj retrocedido o congelado. Ejemplo sintético: TX 5,000 V, RX 4,000 V, SHUNT=8000 µV; equivaldría a 80 mA **solo si Rshunt = 0,100 Ω real** (NO medido). Conversión simulada completada a 18 ms por polling de 1 ms, triggers a 0 ns; las dos ventanas se solapan, pero no demuestra sincronía de muestras ADC reales. Datos tipados explícitamente como SYNTHETIC_OR_UNTRUSTED_ADAPTER y con physical_measurements=0, hardware_approved=false, energization_approved=false, lithium_dock_approved=false, efficiency_qualified=false. Se incluye workflow GitHub Actions para regenerar y archivar JSON sintético. No fingir CI si permanece en cola.

### Matriz de decisión

| Sistema | Decisión provisional | Bloqueos |
|---|---|---|
| Potencia sensor no crítico supuesto 5 V / 80 mA media / 300 mA pico | **Cable corto bloqueable y sustituible** por defecto; WPT sencillo solo candidato de banco. Control regulado mejor en principio pero incompleto | Pérdidas reales, desalineación, metal FOD, calor, humedad, EMI, corte local autónomo normalmente OFF y coste total |
| Dock carga | **Expediente separado**; batería, BMS, estación totalmente desconectados | Química/cargador, FOD, aislamiento, temperatura, protección y revisión de litio |
| Datos RF | ESP-NOW candidato frente a OpenThread/802.15.4 alternativa | ACK de aplicación, CRC, secuencias+epoch, deadline/timeout, autenticación y cifrado, antireplay, reingreso/privacidad; **RF nunca parada crítica** |
| WISP5 | Solo micro-sensores RFID si se justifica lector y consumo mínimo | No aporta 80 mA continuos demostrados |
| Motores, bomba, turbina | **NO WPT por defecto** | Medir consumos continuos, picos y pérdidas antes de diseñarlo |

## Auditoría de proyectos ajenos: autor, licencia, rama PIN → HEAD y PR (30/10/2026)

PINs comparados con los de 19-alternativas-abiertas-para-robot-independiente.md, verificados en la rama real del autor (no suponer actualidad por orden de ramas):

| Creador/proyecto | Rama PIN → HEAD | PR, hallazgo |
|---|---|---|
| [Mark Belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | master **7c7858c0dd7040801b6f191df1396115560218f0** → igual | [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) fusionada en 2021, no aporta FOD/corte validado para VALDO |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2 | master **08332bc398aa3350d351ef2aaac163f8007cffda** → igual | [PR #1](https://github.com/wisp/wisp5-hw/pull/1) fusionada 2015; requiere lector RFID |
| [wisp/wisp5 firmware](https://github.com/wisp/wisp5) BSD-2 | **640kHz** d978a6978ad23ccd6c44dd55430973b04a3d4a9b → **604eee2dffaeba3a270de61cf3dae887a33309c2** | **DIVERGED +68/-11**, no fast-forward; actualización CCS11 2022 y [PR #40](https://github.com/wisp/wisp5/pull/40) abierta histórica |
| [Espressif esp-now](https://github.com/espressif/esp-now) Apache-2 | master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5** → igual | [PR #153](https://github.com/espressif/esp-now/pull/153) cerrada sin merge en feb. 2026; ACK radio no equivale a aplicación |
| [OpenThread](https://github.com/openthread/openthread) BSD-3 | main 7009584dadc20cf20c20a6062f357dd572ba6885 → **e577777c308f6c87e5da3056239231a8fc147cb2** | +14/-0, cambios CLI/BUILD GN/radio, [PR #13819](https://github.com/openthread/openthread/pull/13819) abierta el 30/10 |
| [OOMWOO oficial](https://github.com/makerspet/oomwoo) Apache-2 | main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df** | Último cambio 29/10 gráfico star-history, no WPT, [PR #79](https://github.com/makerspet/oomwoo/pull/79) cleaning-jobs ajena |

No se copió código/CAD de ningún autor, se conservan licencias y autorías. Antes de preparar los archivos se leyeron decisión 28/10, alternativas 19, D22, acuerdo de coordinación W/C, VALDO_OOMWOO/LEEME_PRIMERO y contrato WPT_DATOS_V01; se revisaron automatizaciones y owners. Checkout local VALDO en rama Codex **con archivos de otros modificados**, por tanto quedó intacto. Cambios publicados solo en la rama propia de [Valdo PR #9](https://github.com/Valdi320/Valdo/pull/9).

## BOM, procedencia y pendientes

Consultar BOM_W_IND_57.csv y MATRIZ_W_IND_57.csv: el software de banco añade 0 € de piezas **a cada robot**, pero el banco sí requiere instrumental. Pareja de módulos INA219 Satkit citada previamente 7,26 € IVA total, precio **histórico W56**, no recotizado, sin envío ni calibración/stock Zaragoza comprobados. Diotronic **auxiliar** para pasivos/conectores/rápidos, sin suponer existencias; TME, Mouser, DigiKey/fabricantes para componentes de seguridad trazables, MOQ/precio final pendientes. Ninguna compra ni ensayo físico.

Siguientes bloqueos: lector I²C físico con integridad de 2 bytes/reloj/identidad, calibración W52/W53 trazable, FOD, temperatura, offset, humedad, EMI, dos cortes independientes, ERC histórico W-IND-18 FAIL y autorización formal. No fabricar/energizar electrónica, litio ni estación. Siguiente paso tras revisión: adquirir evidencia de banco segura con fuente aislada y carga resistiva **solo con procedimiento aprobado**, nunca conectado a batería.

Fuentes: [TI INA219, datasheet Rev.G](https://www.ti.com/product/INA219); [W50 previo](https://github.com/Valdi320/Valdo/commit/eb86561d00f7a47be555dbc4f9c07f6062a2df15).
