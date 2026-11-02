# W-IND-19 — Evitar activación térmica peligrosa por salida open-drain sin energía (29/10/2026)

## Hallazgo y retorno práctico

El borrador W-IND-15 usa **dos interruptores TPS22918 con EN activo alto**, pero todavía no tiene protección térmica autónoma ni monitor de alimentación. Una opción económica de termostato es el **Texas Instruments TMP390A3DRLR** (hot trip OUTA open-drain activo bajo, 1.62–5.5 V, 0.5 µA de consumo típico a 25 °C, ±2 °C máx. en 0–70 °C para A3). **El error que evitamos en diseño:** conectar OUTA con una simple resistencia de pull-up al EN activo alto. Si el sensor pierde alimentación o se rompe la señal, su salida puede quedar sin conducción y el pull-up puede activar el transmisor: una alarma que pierde energía puede producir el resultado opuesto al deseado. **Esto es una posibilidad topológica, no una avería ni una tensión medida.**

Se publica un **modelo ejecutable original** de dos canales cuya aceptación exige: monitor de tensión de cada canal **independiente del sensor**; salida coherente; demostración sintética previa LOW→RELEASED con transmisor desarmado; prueba no caducada; dos cortes y permisos locales FOD, sobrecorriente y humedad. Todas las entradas desconocidas inhiben. Un radio ACK NO puede autorizar el transmisor. El límite de frescura de **1000 ms** es HIPÓTESIS; no demuestra que la prueba sea realizable físicamente ni que exista un camino hardware de apagado.

**Reproducir sin hardware** desde este directorio:

```sh
python3 -m py_compile w_ind_19_thermal_rail_gate.py test_w_ind_19_thermal_rail_gate.py
python3 -m unittest -v test_w_ind_19_thermal_rail_gate
python3 w_ind_19_thermal_rail_gate.py
```

**31/31 casos PASS** en Python local aislado: rail perdido/desconocido, salida abierta/cortocircuitada lógica, desafío ausente/vencido/futuro, corrupción de tipos, fallos FOD/corriente/agua, combinaciones cruzadas 3×3 y caso residual de sensor atascado alto no detectable entre pruebas. CI en GitHub verifica este mismo módulo; **no se ha ejecutado SPICE ni ERC nuevo sobre circuito físico**, y el esquema W15 sigue bloqueado con **3 errores ERC + 6 avisos**. Esta aportación de W19 NO corrige esos 9 defectos.

## Matriz de decisiones

| Alternativa | Riesgo/beneficio | Decisión |
| --- | --- | --- |
| TMP390 OUTA con pull-up directamente a EN alto | Bajo coste, pero puede habilitar ante pérdida de alimentación/rotura de OUTA | **RECHAZADA** |
| Dos TMP390 con alimentación supervisada y prueba de estado, más dos cortes | Mejora diagnosticabilidad lógica; requiere cableado/circuito verdaderamente independiente y pruebas de cronología | **SOLO CANDIDATO DIGITAL** |
| NTC + comparadores de ventana locales | Permite diagnosticar abierto/corto; requiere referencias, tolerancias y corte documentados | Seguir comparando |
| MCU / ESP-NOW / OpenThread para decisión de parada | Pérdidas RF, resets, latencia y backpower | **NO ACEPTADO para parada crítica** |
| Alimentar motores, bombas o batería por este enlace | Potencia y pérdidas no caracterizadas | NO introducido |

El modelo **NO garantiza** detectar un TMP390 atascado en RELEASED entre dos diagnósticos; tampoco modela corriente de fuga, POR, propagación, monitor de rail fallado, cortos comunes, disipación, calor de bobina frente al lugar de sensor, envejecimiento, FOD metálico real, EMI, desalineación o circuitos de habilitación y corte independientes. No se afirma que haya un esquema realizable de la prueba LOW→RELEASED; el datasheet anuncia función de test, **su temporización, resistor y transitorios requieren ingeniería específica**. Nunca probar con energía real sin revisión/autorización. Cero pruebas físicas.

**Hipótesis térmica solo explicativa:** hot setpoint nominal 50 °C, precisión A3 ±2 °C en 0–70 °C; entre 48 y 52 °C el resultado estático es incierto. Por encima de 52 °C solo se modela potencial trip del sensor alimentado; no se deduce temperatura de superficie, seguridad de polímeros ni tiempo hasta desconexión. Histéresis de 5/10/20 °C no está modelada y ningún valor de RSET se seleccionó.

## Comparación BOM / proveedores (sin compras)

[BOM parcial W19](BOM_W_IND_19.csv). TMP390A3DRLR es **candidato de análisis, NO componente homologado**: DigiKey informa **0,55000 € sin IVA y 0,66550 € con 21 % IVA** por unidad, cantidad mínima 1 en cut tape (precio visto en catálogo, no oferta formal ni existencias locales). Dos unidades tendrían subtotal indicativo **1,331 € IVA incluido**, sin otros componentes, montaje, transporte ni garantías de coste final. **Diotronic Zaragoza**: SKU equivalente, precio final, MOQ y stock en tienda **pendientes**; lo mismo para disponibilidad contrastada TME/Mouser. Diotronic solo pasivos/equivalentes trazables cuando compense. Bloques críticos exigen datasheets y suministro trazable. Ningún componente de batería, BMS o dock ha sido elegido.

**Fuente del autor:** [TI TMP390 producto y datasheet](https://www.ti.com/product/TMP390), [TI TPS22918](https://www.ti.com/product/TPS22918), [DigiKey TMP390A3DRLR](https://www.digikey.es/en/products/detail/texas-instruments/TMP390A3DRLR/10435095). El circuito original W15 es de VALDO y permanece sin aprobación; no se copia código, CAD ni firmware de otros creadores.

## Límites de alcance, autoría y referencias HEAD verificadas el 29/10/2026

Se leyeron NO_TRASPLANTE, 19-alternativas, D22, pacto W/C, LEEME_PRIMERO y WPT_DATOS_V01. Se revisaron owner/locks, ayuda Codex A57 (su biblioteca KiCad **NO** se integra ni atribuye), otras automatizaciones y la PR propia #9. El checkout local master tiene trabajo de terceros sin editar. La actualización OOMWOO oficial es independiente de W y no tocamos #79.

- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power): autor mark-belbin, GPL-3.0, rama master **7c7858c0dd7040801b6f191df1396115560218f0**, igual al pin; PR #1 antigua.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw): WISP BSD-2-Clause, master **08332bc398aa3350d351ef2aaac163f8007cffda**, igual al pin; [wisp/wisp5](https://github.com/wisp/wisp5): BSD-2-Clause, default **640kHz** HEAD **604eee2dffaeba3a270de61cf3dae887a33309c2**, frente a pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b **68 ahead y 11 behind**, NO fast-forward. WISP solo para microsensores RFID de energía mínima.
- [espressif/esp-now](https://github.com/espressif/esp-now): Espressif Apache-2.0 master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, igual a pin; PR #153/#151/#148 observadas. Datos RF únicamente, necesitan ACK aplicación, CRC, secuencia, timeout y privacidad.
- [openthread/openthread](https://github.com/openthread/openthread): OpenThread BSD-3-Clause main **51aa078ee4fe1ad803bc83ca7b372e7ab62120f3**, +9 commits desde pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13814/#13805/#13804 observadas. No integrar ambos stacks sin necesidad.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo): autor makerspet Apache-2.0 main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**, +1 sobre referencia anterior (solo SVG star history), sin cambio técnico W; VALDO propia PR #9 permanece ámbito único.

**Tres problemas distintos:** 1) dock/carga: fuera de este estudio y batería/BMS desconectados; 2) potencia distribuida WPT de un sensor hipotético 5 V/0,4 W media/1,5 W pico: sin bobinas, calor, offset, eficiencia ni FOD medidos; 3) datos ESP-NOW u OpenThread: transporte no seleccionado físicamente, seguridad local independiente.

**Próxima puerta:** completar primero el ERC nativo sin ocultar errores, revisar topología real de aislamiento de monitor/trip-test y añadir sobrecorriente, FOD/temperatura, inversión y cortes independientes en KiCad, con revisión de datasheets/errores/ensayo resistivo autorizado ANTES de cualquier PCB o litio.
