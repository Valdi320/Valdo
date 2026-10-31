# W-IND-32 — esquema KiCad del receptor con dos bloqueos inversos (INCOMPLETO)

**29/10/2026 · VALDO propio, sector W · Robot NUEVO, independiente. NO FABRICAR NI ENERGIZAR.**

## Resultado técnico y reproducción

Se añade un generador **original** de esquema KiCad 9 editable con dos dispositivos **TI TPS259470LRPWR**, variedad **L con enclavamiento** (no la A de reintento automático), colocados en serie tras una resistencia Kelvin de cuatro terminales de 0,1 Ω **hipotética**. La fuente y carga de 5 V son símbolos declarativos, no hardware. El INA301A1 supervisa la corriente del RECEPTOR; su salida ALERT_N activa-baja se conecta **solo** a telemetría y **jamás** directamente al pin EN de los eFuses.

Cada pin EN dispone de su propia entrada J3/J4 (PERMIT_A/B) con resistencia pulldown de 10 kΩ. Esas entradas son **interfaces externas sin controladores positivos diseñados**. Por eso, **esta mejora solamente valida topología/ausencia de bypass en software; NO es todavía un corte autónomo**. No conectar físicamente J3/J4.

Ejecutar Python >= 3.10 desde la carpeta:
- `python3 generate_w32.py` (produce `W32_RX_DUAL_RCB_INCOMPLETE.kicad_sch`, `W32.kicad_sym`, `sym-lib-table`)
- `python3 generate_w32.py --verify`
- `python3 -m unittest -v test_w32` (**38 pruebas sintéticas PASS en Python 3.13.5 local**, 29 octubre)
- En GitHub Actions, KiCad 9.0.2 ejecuta ERC nativo, exporta netlist XML y ejecuta `python3 netlist_gate_w32.py native_out/w32_native.xml --out native_out/gate.json`; **solo acreditarlo cuando CI termine**.

Las 38 pruebas cubren mutaciones de cortocircuito directo, bypass de U2/U3, EN inadvertidamente alto, unión de habilitaciones, ALERT controlando EN, falta de pulldown, intercambio de K+/K−, variantes TI equivocadas, NC, netlist incompleto/duplicado e integridad de generación. El guard marca permanentemente `hardware_power_authorized=false` aun con topología correcta. Generador, biblioteca, auditor y pruebas son propios; sin código GPL/BSD/Apache copiado.

## Por qué estas piezas y por qué sigue bloqueado

**Fuente de fabricante:** [TPS25947 TI](https://www.ti.com/product/TPS25947) acredita bloqueo de corriente inversa verdadero por MOSFET enfrentados, **RON típico 28,3 mΩ** por dispositivo, límite mínimo de corriente **0,5 A**, RPW QFN 10 pines de 2×2 mm. TI distingue **xL latch-off** de **xA auto-retry**. El L evita reintento automático *para los eventos en que el dispositivo efectivamente entra en estado latched*, pero **no sustituye el rearme seguro de todo el sistema ni detecta por sí mismo el fallo hipotético de 400 mA**. El modelo digital anterior W31 solo establecía el contrato de permiso positivo.

Con 0,3 A y valores TIPICOS, las dos etapas tendrían disipación resistiva calculada `2 × 0.3² × 0.0283 = 5.094 mW` y la derivación 0,1 Ω `0.3² × 0.1 = 9 mW`. No es potencia completa (excluye consumo quiescente, temperatura, conductor, bobinas, inrush) ni una eficiencia WPT medida. Paquete QFN no se repara fácilmente a mano: estudiar **cartucho PCB sustituible** y comparar con conector/cable protegido.

**Bloqueadores físicos explícitos:**
- **J3/J4 son permisos externos no diseñados**, sin supervisor de tensión/PG/POR, corte autónomo del INA301, enclavamiento de rearme local ni independencia de fallos comunes.
- `RILM_A/B_TBD` y `CIT_A/B_TBD` dejan límite de corriente y temporización SIN dimensionar; DVDT sin componente deja rampa sin controlar. **OVLO a GND** en esta topología es una opción provisional SIN corte OVP externo: NO homologar. FLT/AUXOFF sin usar.
- FOD de metales, temperatura, humedad, offset bobinas, EMI, microcortes de energía, energía almacenada, disipación de PCB, backfeed y comportamiento real del corte siguen sin medición ni simulación analógica cualificada.
- **TI limita ILIM mínimo a 500 mA**: un fallo receptor supuesto de 400 mA necesita comparador/actuador independiente del radio.
- La entrada RX puede tener 80 mA promedio, 300 mA pico; valores **supuestos** de piloto, no caracterización de producto.
- Estación dock/litio/BMS, motores y bombas están fuera. No instalar ni conectar nada.

## Decisión comparativa (véase MATRIZ_W_IND_32.csv)

- **Potencia dock:** independiente; WPT simple de [Belbin](https://github.com/mark-belbin/simple-wireless-power) es referencia experimental GPL-3 sin FOD adoptado. Carga de litio y su regulación/BMS prohibidas en el piloto.
- **Potencia de módulo:** investigar WPT **regulado, supervisado y con cortes físicos autónomos** antes de sustituir cables. Enlace cableado modular reparable permanece como referencia de costes; no hay eficiencia ni coste entregado a módulo medido.
- **Datos:** ESP-NOW y OpenThread son **RF, NO alimentación**; ambos exigirán ACK de aplicación, CRC, secuencia, timeout, autenticación/cifrado y recuperación local sin control de parada crítica. WISP5 se limita a microsensores RFID intermitentes, no potencia continua.

## Titulares externos auditados (29/10/2026, frente a SHAs de 19-alternativas...)

| Proyecto del creador y licencia | Rama HEAD confirmada | Cambio / PR revisada |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3 | master `7c7858c0dd7040801b6f191df1396115560218f0` | Igual; PR #1 |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2 | master `08332bc398aa3350d351ef2aaac163f8007cffda` | Igual; PR #1 |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2 | **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` | Diverge de pin `d978a697...` **+68/-11**; PR #40, no fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2 | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | Igual; PR #153 |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3 | main `e577777c308f6c87e5da3056239231a8fc147cb2` | +14/0 vs `7009584...`; PR #13820 |

OOMWOO oficial main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` sin cambios W relevantes. La rama W previa era `2b52bfcfb7a9c862eb55d7afc1b121a908641e77`. Repositorio local VALDO en master con modificaciones C ajenas SIN tocar; fuentes W de Codex en otros repos preservadas. PR OOMWOO #79 ajena, intacta. Otras automatizaciones comprobadas: solo W habilitada.

## BOM y aprovisionamiento

[BOM_W_IND_32.csv](BOM_W_IND_32.csv): identificación exacta, función, Diotronic auxiliar/alternativas, precio final IVA y MOQ **PENDIENTES** salvo precio histórico de INA301 de W31, no revalidado. Ni stock de Diotronic Zaragoza ni de los distribuidores ha sido confirmado para compra; **no calcular coste total inventado**. Para piezas de protección exigir trazabilidad y ficha TI. No comprar nada.

**Siguiente hito propuesto:** sustituir las entradas externas no calificadas por dos verdaderos permisos positivos derivados de rail supervisado, con inhibición independiente desde INA301 y FOD/térmica, latch local sin radio; KiCad ERC/netlist, simulación eléctrica y pruebas de pérdida de alimentación antes de ninguna evaluación física autorizada. Batería desconectada siempre.
