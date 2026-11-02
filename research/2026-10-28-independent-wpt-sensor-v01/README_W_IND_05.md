# W-IND-05 — comparación verificable de dos parejas WPT, sin energizar (28/10/2026)

**Solo nuevo robot abierto, ámbito eléctrico W.** Cancelado el trasplante Xiaomi. Sin compras, baterías/BMS conectados, CAD mecánico, soldaduras, firmware OEM, instalaciones, ensayos eléctricos o cambios en OOMWOO/PR #79. Autores externos y licencias respetados; código de cribado Python escrito originalmente aquí (no copia de fuentes externas).

## Mejora material

W-IND-04 dejó sin seleccionar transmisor/receptor inductivo para un módulo sensor **hipotético** de 5 V, 0,4 W medio y 1,5 W pico. Ahora se han identificado y comparado **dos parejas con referencias verificables, precio IVA incluido en España, abastecimiento y ausencia de protección demostrada**. El programa `wpt_pair_screen.py` calcula costes de conjunto, margen **solo nominal**, rendimiento de catálogo frente a gap **sin desalineación** y genera diez puertas físicas pendientes. AUNQUE dé papel-fit positivo, la aprobación de montaje y ensayo es siempre falsa.

| Candidato | Salida anunciada (NO propia) | Fuente/precio **con IVA** | Estado y riesgos |
|--|--|--|--|
| **DFRobot DFR0362 (TX+RX)** | 5 V/1 A continuos, 1,2 A max, 2–10 mm publicado | [Opencircuit ES](https://opencircuit.es/producto/wireless-charging-module-5v-1a) €9,50, 106 en almacén externo, envío España *desde* €12,50 → **al menos €22/pieza comprada individualmente** | No documentado apagado autónomo TX por FOD/temperatura; [BricoGeek](https://tienda.bricogeek.com/fuentes-de-alimentacion/899-cargador-inalambrico-5v-1a.html) advierte cables de bobina **frágiles** y marca sin stock. Fabricante [DFRobot](https://wiki.dfrobot.com/dfr0362/). |
| **Adafruit TX2162 + RX1901 (BQ51013B)** | TX 5 W máximo, gap TX 2–8 mm; receptor 5 V/500 mA, compatibilidad Qi anunciada, **pareja no probada** | [TX2162](https://opencircuit.es/producto/universal-qi-wireless-charging-transmitter) cotizado en páginas discordantes €28,75/€39,25; [RX1901](https://opencircuit.es/producto/universal-qi-wireless-receiver-module) €23,25 → kit **€52–62,50 + envío desde €12,50 = mínimo €64,50–75** | RX [BQ51013B de Texas Instruments](https://www.ti.com/product/BQ51013B) comunica datos de FOD y posee shutdown térmico de IC. **No prueba** que el TX montado desconecte ante metal, temperatura o fallo. Almacenes/proveedor externos, tarifas/tiempo no garantizados. |
| **Cable robusto de servicio** | no WPT, alternativa real para sensores | presupuesto pendiente de C | mantener hasta demostrar beneficio económico y reparabilidad de WPT |

**Coste cuantitativo:** una pareja desde €22 versus Qi desde €64,50–75. Para cinco parejas de una misma opción, simulando el mismo carrito y política de envío gratis del proveedor a partir de €150: DFR €60; Qi €260–312,50 **como pisos publicitarios**. No son cotizaciones de compra ni incluyen fuente, sensores de metal, temperatura, protección independiente, PCB, cableado local, coste eléctrico, instrumentos, impuestos adicionales o entregas fuera de política comercial. Un precio discordante se conserva como intervalo, no se corrige inventando uno. El 90% máximo publicitado en ficha DFR no es eficiencia **medida** bajo XY offset; el 93% pico AC-DC del IC TI tampoco es eficiencia del sistema TX-RX.

**BOM por bloque:** `BOM_W_IND_05.csv`, con referencias solo donde existen, resto TBD explícito. **No se ha seleccionado ningún conjunto seguro ni firmware libre de TX certificado.** El sensor, radio, fuente y baterías futuros no están caracterizados. Es un avance de decisión documentada y software reproducible, no de hardware ni homologación.

## Seguridad / decisión

1. **FOD de transmisor y metal:** pendiente sensor y apagado independiente medidos, no inferir protección TX de funciones del chip receptor TI.
2. **Térmica, corriente y corte:** pendiente hardware normalmente OFF independiente de CPU/radio, fallo por contacto soldado, retorno de alimentación, cortocircuito/rechazo de carga.
3. **Fiabilidad:** falta ensayo de tensión/rizado con carga 1,5 W, gap XY/Z bajo temperatura, polvo/agua/metal, ruido EMI y coexistencia ESP-NOW/Thread, rendimientos completos y recambio de bobinas/cables frágiles.
4. **Dato versus potencia versus dock:** estos kits son candidatos solo para alimentación de un sensor no crítico. La carga de batería desde estación queda DIFERIDA, desconectada del BMS. ESP-NOW (Apache-2.0; cifrado, ACK de aplicación, CRC, secuencia y timeout pendientes en radio real) u OpenThread (BSD-3-Clause, radios IEEE802.15.4) son solo datos; radio jamás autoriza seguridad ni parada crítica. WISP5 (BSD-2) solo micromódulos RFID, no fuente continua de 0,4 W.
5. **Control cableado económico:** si mejora WPT no compensa pérdidas/precio/ciclos/fragilidad, conservar conector mecánico desmontable; diseño reservado al compañero C, fuera de este PR.

## Auditoría previa de propietarios y cambios (HEAD oficial, 28/10/2026)

- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, `master 7c7858c0dd7040801b6f191df1396115560218f0`, idéntico al pin; PR #1; ningún circuito copiado.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2, `master 08332bc398aa3350d351ef2aaac163f8007cffda`, idéntico; PR #1.
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2, rama **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2`, **divergido 68 ahead /11 behind** del pin d978a697...; PR #38/#40, no fast-forward.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2, `master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5`, idéntico; PR #153/#151.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3, `main 3d645eb9106cb1d5c2ff11891e84dc14e52e293a`, 5 ahead /0 behind respecto pin7009584d; cambios sub_mac/radio/CI; PR #13805/#13804/#13802, no confundir PR abierta con código fusionado.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo) `main 1c2bd43abcf74288afcf2d8b64514cc325f9b905` sin diferencia del pin; [oomwoo-firmware](https://github.com/makerspet/oomwoo-firmware) `main 575c49abcdc115233f4f3ee8fa512d2939ac3bc5` 2 commits de documentación `docs/SPEC.md` por delante. Compañero gestiona PR #79, NO tocada.
- VALDO propio PR #9 W, base `master` y rama W; checkout local `master` tiene cambios ajenos, no editado.

## Reproducibilidad

Sin dependencias nuevas ni red en las pruebas, Python >=3.10:

```sh
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m py_compile wpt_pair_screen.py test_wpt_pair_screen.py
python3 -m unittest -v test_wpt_pair_screen
python3 wpt_pair_screen.py
python3 -m unittest -v test_w_link test_hold_up_envelope test_power_restart_gate test_durable_epoch_store test_wpt_pair_screen
```

**Pruebas W-IND-05: 26/26 en sandbox Python (no es simulación de acoplamiento electromagnético).** CI de GitHub debe acreditar integración total con W-IND-01..04 (91 previas +26=117). Los flags `tx_fod_physical_verified=false` son declaraciones sobre **falta de evidencia examinada**, no una prueba de que el producto carezca de esa función. `installation_approved=false` y `physical_bench_approved=false` por diseño hasta expediente independiente autorizado.

**Siguiente paso:** localizar/controlar TX con corte de potencia normalmente OFF y termometría/FOD propio, diseño electrónico documentado y BOM completa coste total España; únicamente después proponer ensayo autorizado de 5 V aislados y **resistencia de carga**, sin conectar batería ni estación. No congelar geometría C por una pareja sin cualificar.
