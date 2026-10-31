# W-IND-55 — Tres pasadas ABA: detectar deriva entre medidas sin tercer medidor

**30/10/2026. VALDO ámbito W original. Solo cálculos y pruebas sintéticas; NO montaje físico ni permiso para energizar.** Proyecto de robot aspirador NUEVO, abierto, económico, local, reparable e imprimible. El maestro \`00_DECISION_20261028_NO_TRASPLANTE_X20.md\` CANCELA por completo el trasplante OEM Xiaomi: conservar únicamente principios genéricos. Se leyeron antes de desarrollar los maestros locales, \`19-alternativas...\`, D22, acuerdo W/C, \`VALDO_OOMWOO/LEEME_PRIMERO.md\` y \`adaptacion/contratos/WPT_DATOS_V01.md\`. No se alteraron clones upstream, adaptación, CAD C, firmware ni PR #79 de cleaning-jobs. Única PR destino: propia [Valdo #9](https://github.com/Valdi320/Valdo/pull/9).

## Una mejora real sobre W-IND-54

W54 cancelaba la razón de ganancia multiplicativa entre DOS INA219 mediante pasadas AB y BA. Sin embargo, si cambia la eficiencia del enlace mientras se intercambian medidores, ese valor es la media geométrica de dos condiciones y NO una medida de una condición. **W55 incorpora una tercera pasada AB final** para detectar deriva entre extremos sin comprar un tercer vatímetro.

Con \(R_0=P_{out,B}/P_{in,A}\) en AB0, \(R_1=P_{out,A}/P_{in,B}\) en BA1, \(R_2=P_{out,B}/P_{in,A}\) en AB2:

\[
\eta_{ABA}=(R_0R_2)^{1/4}R_1^{1/2},\qquad
D_{end}=100|R_2/R_0-1|.
\]

Las ganancias multiplicativas fijas de los dos instrumentos se cancelan algebraicamente. Si los centros de medida son equiespaciados y \(\ln(\eta)\) deriva linealmente, estima la eficiencia en el centro; NO garantiza estabilidad del montaje. Al comparar ambos extremos AB, la ganancia relativa fija también se cancela para medir deriva neta. Una perturbación que suceda SOLAMENTE durante la medición intermedia BA puede pasar inadvertida: el código la documenta y la prueba. Tampoco elimina offset aditivo, calibración inestable, sesgo dependiente de carga, reconexiones, deriva común ni errores de reloj.

Cada \`Pin,Pout\` incluye cota de error absoluto hipotética \`u\`: el ratio verdadero se acota entre \`(Pout-uout)/(Pin+uin)\` y \`(Pout+uout)/(Pin-uin)\`. Se aplican intervalos conservadores al estimador y a \`R2/R0\`. Si el ratio máximo de cualquier pasada resulta ≥1, se rechaza como medición no cualificada. NO interpretar este rechazo como prueba de seguridad.

**Condiciones de cribado, todas HIPÓTESIS y NO umbrales seguros:** tres IDs de corrida y traza distintos; mismo fixture; papeles AB/BA/AB; relojes enteros, no solapados; asimetría de intervalos entre centros ≤5%; dispersión temperatura ≤1 °C, separación bobina ≤0,1 mm, offset ≤0,1 mm, carga ≤0,5%, deriva máxima incluyendo incertidumbre ≤2%. Se exige indicación de origen SYNTHETIC/BENCH_MEASURED, trazabilidad externa y flags booleanos exactos. Los flags son **autodeclarados y no acreditan calibración ni procedencia**. \`candidate_for_external_metrology_review\` solo filtra expedientes; \`hardware_approved\`, \`energization_approved\`, \`lithium_dock_approved\` y \`local_cutoff_qualified\` son siempre falsos.

**Ejemplo íntegramente FICTICIO:** potencia verdadera 1000 mW entrada, 800 mW salida; ganancias A=1,10, B=0,90. Por pasada: 65,4545%, 97,7778%, 65,4545%; estimador ABA = **80,0000%**; error ±2 mW por canal/pasada SUPUESTO → intervalo condicionado 79,6371–80,3644%; deriva extremos nominal 0%, peor caso condicionado 0,9234%. Se rechaza una deriva inyectada de 8% y se muestra que una anomalía del centro no se detecta por comparación de extremos. **Cero mediciones físicas**.

## Tres problemas separados

| Arquitectura | Selección económica provisional | Riesgos y puertas abiertas |
|---|---|---|
| Potencia de módulo sensor (supuesto 5 V × 80 mA promedio, pico 300 mA) | **Cable corto bloqueable y sustituible por defecto.** WPT simple solo candidato en un banco aislado; WPT regulada con FOD/corte independiente no seleccionada. | No medidos eficiencia, calor, alineación, FOD TX, humedad, EMI, temperatura, reversa, cortacircuitos normalmente-OFF ni coste total. No instalar WPT por defecto en motores/bombas. |
| Dock y carga | **Expediente separado**, batería/BMS/estación totalmente desconectados. | Química, BMS, cargador, corrientes, FOD, agua, protector térmico, corte autónomo y revisión de seguridad. No extrapolar ensayo de 0,4 W a 20–50 W. |
| Datos RF | **ESP-NOW** primer candidato de telemetría no crítica; OpenThread/802.15.4 alternativa con otro hardware; WISP5 solo microsensores RFID de energía mínima. | ACK **de aplicación**, CRC, secuencia/sesión antirreplay, timeout, identidad/privacidad, autenticación/cifrado y recuperación en RF real. La radio NO aporta energía ni puede autorizar parada crítica. |

## Autores, licencias y SHA verificadas en GitHub (30/10/2026)

PINs exactos de \`19-alternativas...\` comparados con HEAD de la **rama correcta**, con revisión de PRs del autor. No se ha copiado código ni CAD externo.

| Proyecto del creador / licencia | PIN 28/10 → HEAD 30/10 | Cambios / PR |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 \`master\` | \`7c7858c0\` → igual | Sin novedad; PR #1 fusionada 2021. Su prototipo no demuestra seguridad de nuestro robot. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause \`master\` | \`08332bc3\` → igual | PR #1 fusionada 2015. PCB Altium y lector no integrados. |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause **\`640kHz\`** | \`d978a697\` → \`604eee2d\` | **Divergió +68/-11**. No fast-forward; HEAD con CCS11 de abril 2022, PR #38 actividad 2024. |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 \`master\` | \`c3b5f9be\` → igual | Sin cambio de HEAD; PR #153 cerrada febrero 2026. ACK del radio no confirma aplicación. |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause \`main\` | \`7009584d\` → \`e577777c\` | **+14/-0**; cambios radio, secure-transport y BUILD GN, [PR #13819](https://github.com/openthread/openthread/pull/13819) abierta. |
| [makerspet/oomwoo](https://github.com/makerspet/oomwoo), Apache-2.0 \`main\` | HEAD \`f01a1b29\` | Último commit 29/10 actualiza gráfica de estrellas, NO WPT. [PR #79](https://github.com/makerspet/oomwoo/pull/79) de otro módulo, intacta. |
| [Valdi320/Valdo](https://github.com/Valdi320/Valdo/pull/9) | W54 \`2262982b\` | Propio W; no cambios en trabajo local paralelo (checkout personal está en rama Codex con archivos sucios). |

## BOM/abastecimiento y costes

Ver \`BOM_W_IND_55.csv\` y \`MATRIZ_W_IND_55.csv\`. Esta mejora es software original Python stdlib: **0 € por robot y 0 medidores adicionales**, reutilizaría dos INA219 SOLO en banco. Satkit MCU-219 anunciados a **3,63 € c/u con IVA**, pareja 7,26 €, **sin portes/calibración** y con información de existencias contradictoria, así que **no stock confirmado**. [DFRobot DFR0362 en DigiKey España](https://www.digikey.es/en/products/detail/dfrobot/DFR0362/7597155) ~7,42 € con IVA, sin envío, es candidato experimental NO cualificado. **Diotronic Zaragoza** auxiliar para pasivos y conectores equivalentes: referencia exacta, existencias en tienda, cantidad mínima, precio final IVA y portes NO comprobados, no asumir stock. Cualquier FOD, regulador, BMS o corte requiere datasheet, trazabilidad y evaluación de seguridad con TME/Mouser/DigiKey/fabricante.

## Código, pruebas y límites

Reproducir sin dependencias externas:

\`\`\`bash
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_55 -p 'test_w55.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_55/w55_aba_drift_gate.py --demo --out W55_SYNTHETIC.json
\`\`\`

**20/20 pruebas locales digitales PASS en copia aislada.** La CI W55 debe verificar remotamente y archivar JSON sintético; no se afirmará CI hasta comprobar su conclusión. Toda evidencia es simulación, no calibración. \`physical_measurements=0\`; ninguna adquisición I²C, FOD, temperatura física, EMI, RF ni corte ensayados. ERC histórico W-IND-18 sigue bloqueante: ninguna PCB aprobada para energizar. Si algún día se autoriza banco aislado, tres pasadas requieren dos intercambios físicos **con fuente apagada y aislada**; batería, BMS y dock siempre fuera. Ninguna compra, impresión, soldadura, cambio de firmware o conexión real.

**Siguiente mejora de retorno:** lector I²C real/calibración y contrato de evidencia trazable **primero como simulación**, antes de cualquier banco autorizado; cotejar coste de ciclo de reparación de cable contra WPT completo puesto en Zaragoza.
