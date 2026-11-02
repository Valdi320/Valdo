# W-IND-06 — eFuse de bajo umbral para receptor inductivo (28/10/2026)

Solo W, robot NUEVO sin OEM Xiaomi, cero intervención física. Selección de un candidato de protección para la **salida DC del receptor WPT** del sensor no crítico; **NO es protección FOD ni desconecta por sí mismo el transmisor**.

## Hallazgo material / por qué mejora W-IND-05
En el sensor hipotético 5 V, 0,4 W medios y 1,5 W pico, I_media=0,08 A e I_pico=0,30 A. TI TPS2663x tiene umbral mínimo configurable de 0,6 A y TPS25947xx de 0,5 A; por tanto no permiten el límite nominal de 0,4 A que buscamos. **TPS259630** (2,7–19 V, 0,125–2 A, SOIC8, ENABLE activo alto, OTP y FLT) sí permite ese orden de magnitud. **TPS259630 tiene TSD de tipo latch-off; TPS259631 auto-retry**, no intercambiables. Fuentes: https://www.ti.com/product/TPS2596 ; https://www.ti.com/document-viewer/TPS2596/datasheet/device-comparison-table-x7984 ; https://www.ti.com/product/TPS2663 ; https://www.ti.com/product/TPS25947

Con I_lim nominal 0,4 A y precisión fabricante ±10,4 % MAX, límites teóricos 0,3584–0,4416 A. A tensión de receptor mínima **supuestamente 4,5 V** y pico 1,5 W la corriente sería 0,3333 A (holgura 25,1 mA). Una avería **hipotética** de 0,5 A rebasa umbral alto por 58,4 mA. **ESTO NO GARANTIZA DESCONEXIÓN**: el chip puede limitar corriente, demora y transitorios no simulados; tampoco garantiza que el RX entregue 4,5 V. A 4,0 V el pico necesita 0,375 A y el caso ya no pasa cribado. R_ILM, dV/dt y UVLO se dimensionarán con datasheet/herramienta TI tras medir el RX; no atribuir valores calculados al circuito.

**Coste observado 28/10/2026**: https://www.digikey.es/es/products/detail/texas-instruments/TPS259630DDAT/10445038 muestra 0,91 € sin IVA / 1,1011 € con IVA (1 unidad), 40.543 en stock durante consulta, sin portes. No es BOM final ni precio garantizado.

## Topología de referencia, NO ENERGIZAR
Fuente SELV de futuro banco → **TX: apagado por hardware normalmente OFF, sensor de metal, termometría bobina y desconexión independiente (TODO PENDIENTE)** → TX DFR0362 (solo candidato de W-IND-05) ~aire~ RX DFR0362 → TPS259630 y componentes DC sin valores aprobados → resistencia ficticia / sensor futuro. El eFuse RX no evita que el TX caliente metal cuando el receptor está ausente. **No usar su límite a 0,4 A en entrada TX:** con carga RX1,5 W, eficiencia supuesta 55 % y control TX0,05 W, corriente TX≈0,555 A y pérdidas totales≈1,277 W; son hipótesis, no calor medido ni FOD.

## Matriz de decisión
| Ámbito | Decisión | Puerta de seguridad no superada |
|---|---|---|
| Dock de carga | Pospuesto; sin batería/BMS | control de carga, seguridad térmica, metal, desconexión independiente, EMI |
| WPT módulo sensor | TPS259630 RX **candidato**, TX DFR0362 sin aprobación | FOD TX, 2 termistores, corriente TX, UVLO, prueba fallos, tensión de salida/offset, cortacircuitos y EMC |
| Datos radio | ESP-NOW candidato, OpenThread alternativa, WISP sólo microsensores RFID | cifrado autenticado real, ACK de aplicación y recuperación en MCU; no gobierna emergencia |

**BOM exhaustiva de bloques todavía incompletos** en BOM_W_IND_06.csv. Resistencias, condensadores, fuente, FOD, comparadores y PCB todavía sin precio ni valor aprobados. Cable robusto sustituible conserva preferencia cuando WPT no justifique coste. No instalar WPT en motores ni bombas con esta demostración.

## Reproducción
En el mismo directorio: python3 -m py_compile rx_efuse_screen.py test_rx_efuse_screen.py; python3 -m unittest -v test_rx_efuse_screen; python3 rx_efuse_screen.py. Código original, sin dependencias, 30 tests deterministas (cambios de tensión, umbrales, corriente y datos inválidos); verificaciones matemáticas solamente. paper_feasible **nunca** implica instalación. Cero pruebas de FOD, temperatura real, rizado, offset, radio o litio. La validación CI de GitHub se verificará después de push.

## Revisión HEAD, ramas y autorías antes de publicar (GitHub API 28/10/2026)
- mark-belbin/simple-wireless-power GPL-3.0 master 7c7858c0dd7040801b6f191df1396115560218f0: igual al pin; 0 PR abiertas, ningún código copiado.
- wisp/wisp5-hw BSD-2-Clause master 08332bc398aa3350d351ef2aaac163f8007cffda: igual al pin; 0 PR.
- wisp/wisp5 BSD-2-Clause **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2: diverge 68 ahead /11 behind respecto d978a6978ad23ccd6c44dd55430973b04a3d4a9b; PR #40 abierta, NO fast-forward.
- espressif/esp-now Apache-2.0 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5: igual al pin; 0 PR.
- openthread/openthread BSD-3-Clause main 3d645eb9106cb1d5c2ff11891e84dc14e52e293a: +5 ahead /0 behind vs 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13805/#13804/#13802 abiertas; ninguna confundida con fusionada.
- makerspet/oomwoo main 1c2bd43abcf74288afcf2d8b64514cc325f9b905, firmware main 575c49abcdc115233f4f3ee8fa512d2939ac3bc5: sin cambios frente a pins. PR #79 cleaning-jobs y #3 firmware son OTRO ámbito. No tocados.
- Contrato OOMWOO: adaptacion/contratos/WPT_DATOS_V01.md leído; mecánica C y clones intactos. Valdo checkout master local está sucio por terceros, por eso se publica en PR W #9 vía API sin tocar checkout.

**Siguiente paso:** diseñar y verificar **corte del transmisor normalmente deshabilitado e independiente del MCU y radio**, control térmico externo y detección de metal incluso sin receptor, seguido de ensayos seguros autorizados SELV/resistencia. Ninguna conexión a batería.
