# W-IND-58 — frontera de bytes I2C INA219 para la captura de W57

**30/10/2026. Robot nuevo abierto; ámbito W exclusivo; solo software.** Se respeta la decisión de 28/10 que cancela todo trasplante Xiaomi X20 Pro OEM. No se modifica batería, BMS, motor, cargador, estación, firmware ni maquinaria. No se tocan CAD y fuentes de C/Codex, OOMWOO oficial/adaptación, ni la PR upstream #79 de cleaning-jobs.

## Mejora real y verificable

W57 (autoría propia, commit ce7f775dd7c8eef97b97cbc1c62481b37278deb9) suponía que un puerto ya entregaba palabras de 16 bits correctas. **W58 añade una frontera verificable y fail-closed de bytes** sin hardware: escritura de registro INA219 con byte de dirección seguido por MSB y LSB; lectura combinada de índice y exactamente dos bytes, interpretados MSB primero. Ejemplo CONFIG 0x0663 debe salir como bytes 00 06 63 y leer 06 63. Una API SMBus read_word_data puede dar una palabra de orden distinto y no debe conectarse sin adaptador auditado. La transacción repetida-start es un requisito del puerto raw, no una propiedad demostrada de Linux/I2C físico.

El código W58 rechaza dirección fuera de 0x40..0x4F, registro fuera de 00..03, escritura fuera de CONFIG, booleanos/números falsos, respuestas de tamaño o tipo erróneo, lecturas/escrituras fallidas y falsos recibos de escritura. Una inyección de byte-swapping en CONFIG queda rechazada por la comprobación W57. **No garantiza detectar un intercambio limitado a datos de medición que siga dando valores plausibles**, ni identifica físicamente un INA219 sin patrón/calibración independiente. No hay /dev/i2c, gpio, SMBus, radio real ni accionamiento.

## Reproducibilidad

Desde raíz del repositorio, Python estándar:

    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_58 -p test_w58.py -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_58/w58_ina219_wire.py > W58_SYNTHETIC_NOT_HARDWARE.json

**14/14 pruebas digitales locales** en sandbox aislado (transcripción de la interfaz W57 solo para el ensayo local); CI del repositorio integrará **W57 publicado original** y generará un JSON sintético de rastreo. La CI remota debe comprobarse antes de declararla PASS. Marcadores explícitos: physical_measurements=0, hardware_approved=false, energization_approved=false, lithium_dock_approved=false, physical_i2c_implemented=false, meter_identity_proven=false, calibration_proven=false y thermal_fod_emi_proven=false.

Ejemplo sintético del contrato: dos configuraciones byte a byte 000663; registro leído 00, palabra 0663; muestras ficticias TX=5000 mV y RX=4000 mV. **No son mediciones físicas** ni prueban rendimiento WPT. Cualquier futura captura real necesita instrumento de referencia, resistencias medidas, identidad/tensión/control I2C, reloj verificable, y una cadena de protección independiente.

## Matriz técnica: tres problemas distintos

1. **Carga en estación:** interfaz y proceso de seguridad independientes, SIN batería/BMS/estación conectados; ni litio ni protección de carga se derivan de este verificador.
2. **Potencia a módulos:** primer sensor hipotético no crítico 5 V, 80 mA media, 300 mA pico (0,4/1,5 W). Cable corto bloqueable y reemplazable es opción por defecto. WPT simple y regulado siguen candidatos, ninguno autorizado sin FOD metálico, termometría, gap/offset 6D, agua, EMI, corte eléctrico local normalmente OFF, coste y eficiencia verificados. No WPT por defecto en bombas/motores.
3. **Datos:** ESP-NOW candidato y OpenThread alternativa; hace falta ACK de aplicación, CRC, secuencia, caducidad, privacidad, autenticación, antireplay y recuperación. Ni RF alimenta el módulo ni se usa para parada crítica. WISP5 RFID, solo para futuros microsensores tras justificar consumo y coste lector.

## Auditoría de creadores externos y OOMWOO

Se consultaron documentos maestros de decisión, alternativas, D22, coordinación W/C, LEEME_PRIMERO y WPT_DATOS_V01 y se verificaron las otras automatizaciones y propietarios; la automatización OOMWOO está deshabilitada. El checkout VALDO del PC pertenece a rama Codex sucia, conservado intacto. Comparación GitHub de las ramas HEAD reales del **30/10/2026** contra PIN del documento 19-alternativas (28/10), con revisión de cambios/PR registrados en W57:

| Proyecto/creador | Licencia | PIN → HEAD en su rama | Implicación |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), master | GPL-3.0 | 7c7858c → igual | Potencia inductiva del autor, no diseño de seguridad nuestro; PR #1 histórica. Sin copiar GPL. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), master | BSD-2-Clause | 08332bc → igual | Requiere lector RFID, no un sensor continuo 80 mA; PR #1 histórica. |
| [wisp/wisp5](https://github.com/wisp/wisp5), **640kHz** | BSD-2-Clause | d978a69 → 604eee2 | **Diverged: +68/-11**, NO fast-forward. PR #40 histórica. |
| [espressif/esp-now](https://github.com/espressif/esp-now), master | Apache-2.0 | c3b5f9b → igual | Datos, no potencia; PR #153 cerrada sin merge en febrero 2026. |
| [openthread/openthread](https://github.com/openthread/openthread), main | BSD-3-Clause | 7009584 → e577777 | +14/-0, cambios CLI/radio/CI/build; PR #13819 registrada abierta el 30/10. |

OOMWOO oficial makerspet/oomwoo main: +1 commit sobre 1c2bd43 (solo imágenes históricas). makerspet/oomwoo-firmware main: +6 sobre 33ee70d (docs/SPEC.md y include/oomwoo_pins.h), sin importación. VALDO propio PR #9 HEAD inicial ce7f775 W57. **No se ha incorporado código, esquemas, CAD o trabajos de terceros**; se referencian fuentes y licencias sin atribuirlos como propios.

## BOM, costes y límites

BOM_W_IND_58.csv y MATRIZ_W_IND_58.csv: el nuevo software cuesta 0 € de hardware adicional por robot, pero el banco físico NO es gratis. La pareja candidata de INA219 montados a 7,26 € IVA fue precio **histórico** de W57, no recotizado, sin portes, calibración ni stock Zaragoza. Diotronic auxiliar para pasivos/cables/conectores; MOQ, referencia, stock local y precio final con IVA **pendientes**. TME/Mouser/DigiKey/fabricantes prioritarios para piezas críticas con trazabilidad; no hay controlador, bobina o FOD seleccionados.

**Bloqueos:** 0 mediciones físicas; sin I2C real ni control de reloj físico, calibración trazable, FOD, temperatura, EMI y desconexión independiente. ERC histórico W-IND-18 pendiente. Ningún circuito ni batería autorizados para energizar. Siguiente hito responsable: calibración sobre patrón independiente y futura comprobación del transporte real, solo después de procedimiento seguro y autorización.

Fuente técnica: [datasheet TI INA219 Rev.G](https://www.ti.com/lit/ds/symlink/ina219.pdf). Datos del autor no son mediciones de VALDO.
