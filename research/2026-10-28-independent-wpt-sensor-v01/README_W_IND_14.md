# W-IND-14 — Diagnóstico en dos fases de cortes del transmisor inductivo

**29/10/2026 — Exclusivamente robot NUEVO, ámbito W y PR #9.** No Xiaomi OEM, dock, batería, placa, firmware ni OOMWOO #79. Código Python 3.10+ original. Es un modelo DC nodal, **no** esquema KiCad, SPICE, prueba de hardware o certificación.

## Mejora falsable

W-IND-13 demostró que dos cortes pueden fallar simultáneamente por un ENABLE común. Este hito propone observar individualmente dos cortes hipotéticos **sin alimentar una bobina**:

```text
VIN=5V -- R_A -- MID -- R_B -- TX -- 1kOhm -- GND
                  |
                22kOhm
                  |
                 GND
SONDA=5V -- 10kOhm -- MID (únicamente segunda fase)
```

1. **Fase pasiva:** ambos cortes solicitados OFF, la sonda ausente; se exige MID y TX bajos. Un corte A soldado sube MID y se DENIEGA antes de aplicar la sonda.
2. **Fase activa de microsonda resistiva:** tras fase 1 sin anomalías, una resistencia de 10kOhm inyecta una corriente **calculada** como máximo de 0,611mA a 5,5V/9kOhm. Se exige MID alto y TX bajo; un corte B soldado arrastra ambos nodos hacia la descarga TX.
3. **Fail-closed:** entrada ausente, monitor sin calificar, umbral ambiguo, sonda o alimentación fuera de rangos → HOLD. Ningún resultado permite habilitar una potencia real: siempre `hardware_approved=False`, `covers_esd_body_diodes=False`, `proves_real_fod=False`.

## Modelo y pruebas reproducibles

Archivos: `tx_offline_diagnostics.py` (matriz DC de conductancias 2x2; admite carga resistiva y una hipotética ruta auxiliar) y `test_tx_offline_diagnostics.py` (**18 pruebas deterministas**). Ejecutar en `research/2026-10-28-independent-wpt-sensor-v01/`:

```shell
python3 -m py_compile tx_offline_diagnostics.py test_tx_offline_diagnostics.py
python3 -m unittest -v test_tx_offline_diagnostics
python3 tx_offline_diagnostics.py
```

La matriz de esquinas recorre **192 configuraciones** (VIN 4,5/5/5,5V; sonda 4,5/5,5V; R_MID ±20%; R_TX ±10%; R_PROBE ±10%; estado OFF ficticio 1MOhm/100MOhm; precisión supuesta 0/80mV) y cuatro estados cada una = **768 decisiones sintéticas**. También comprueba leyes de Kirchhoff, ambos cortes soldados, monitor ausente, AUX, brownout, entradas inválidas, límite de corriente y degradación.

Ejemplo sintético (VIN 5V, cortes OFF 100MOhm, soldadura modelada 0,1Ohm): sano MID pasivo 0,001V, MID con sonda 3,437V, TX con sonda 0V; soldadura A MID pasivo 5V, DENY; soldadura B MID/TX con sonda 0,437V, DENY; doble soldadura MID pasivo ~5V, DENY. **Nueva observación:** R_MID=47kOhm, estado OFF supuesto 1MOhm puede dar MID pasivo ~0,228V y quedar ambiguo con monitor ±80mV. El candidato **22kOhm** evita esa ambigüedad en la cuadrícula hipotética. Esto no estima confiabilidad real ni fuga garantizada de ningún semiconductor.

## Comparaciones, ámbito y límites

| Área | Decisión provisional | Evidencia pendiente |
|---|---|---|
| Primer sensor | Hipótesis 5V/0,4W medio y 1,5W pico | Sensor real y alimentación medida |
| Potencia modular | Comparar WPT sencillo vs controlado, ambos con FOD, temperatura, offset, EMI y corte independiente | Circuito con referencias, KiCad/ERC/SPICE y medida |
| Dock de carga | Proyecto separado; batería y BMS desconectados | Análisis de cargador/litio específico |
| Datos | ESP-NOW candidato y OpenThread alternativa; ACK aplicación, CRC, secuencia, timeout, autenticación, recuperación | RF/latencia/cifrado reales; nunca parada crítica por radio |
| WISP | Solo microsensores RFID si energía/coste justifican lector | Perfil consumo y reparabilidad |
| Motores y bombas | No WPT por defecto | Corrientes/picos/eficiencia reales; mantener conector reparable |
| Mecánica C/OOMWOO | Sin cambios ni compatibilidad presumida | Validación por sus propietarios |

**Grandes ausencias:** transitorios y capacitancias, diodos corporales/ESD/GPIO, fallo de un sensor atascado, resistencias reales de apagado, deriva térmica, sonda cortocircuitada, alimentaciones auxiliares, susceptibilidad RF, FOD real, calor de metal, detección de humedad, fallos comunes y corte físico. No se ha construido ni alimentado ningún circuito. `kicad-cli` y `ngspice` no están instalados en el PC conectado, por lo que **no** se alegan pruebas ERC/SPICE.

## Fuentes oficiales revisadas y autores (29/10/2026)

| Proyecto | Licencia | HEAD verificado frente al pin 28/10 | Uso |
|---|---|---|---|
| [Simple Wireless Power](https://github.com/mark-belbin/simple-wireless-power) | GPL-3.0 | master 7c7858c, igual al pin | Referencia sin copiar |
| [WISP5 hw](https://github.com/wisp/wisp5-hw) | BSD-2-Clause | master 08332bc, igual al pin | Referencia RFID |
| [WISP5 fw](https://github.com/wisp/wisp5) | BSD-2-Clause | rama 640kHz 604eee2; divergencia **+68/-11** frente al pin d978a69 | No fast-forward |
| [ESP-NOW](https://github.com/espressif/esp-now) | Apache-2.0 | master c3b5f9b, igual al pin | Datos, no energía |
| [OpenThread](https://github.com/openthread/openthread) | BSD-3-Clause | main 51aa078; **+9/0** frente al pin 7009584 | Alternativa de datos |

Se revisaron documentos maestros locales 00_DECISION, 19-alternativas, D22, contratos W/C, VALDO_OOMWOO y las tareas de otros agentes. OOMWOO master/main (makerspet/oomwoo) HEAD 1c2bd43; su PR #79 cleaning-jobs es ajena. Ningún código ajeno copiado ni otro repositorio alterado. El fabricante [TI TPS22918](https://www.ti.com/product/TPS22918) se consulta solo como ejemplo de especificación: **este modelo NO simula el TPS22918 ni aprueba su uso**.

## BOM y abastecimiento

`BOM_W_IND_14.csv`: Diotronic auxiliar **10kOhm 1W 5%** SKU 10351, web **0,15€ IVA incluido** con mínimo cinco; y bolsa **25×1kOhm 1206 1/4W** SKU BSMD1025025, web **1,00€ IVA incluido**. Precio, mínimo, referencia y existencia de tienda física, portes, sustitutos o cotizaciones TME/Mouser/DigiKey **no comprobados**. Resistencia 22k, dos dispositivos de corte, monitores, FOD, térmica y PCB sin SKU aprobado; no compras.

**Siguiente hito**: esquemático pin a pin real con alimentación independiente de supervisores, protección de sonda ante cortos/ESD, retorno inverso y FOD local, ERC/SPICE y revisión de fallo único. Banco resistivo aislado únicamente con autorización explícita y sin batería o estación.
