# W-IND-76 — Integrar el ciclo de energía, no solo una lectura favorable

**31 octubre 2026. Hito original del ámbito W para robot aspirador NUEVO y abierto.** Solo cálculo sintético; cero ensayos físicos, batería/BMS, cargador, estación energizada, motores, soldadura, impresiones o compras. El Xiaomi X20 Pro OEM queda expresamente excluido.

## Mejora reproducible frente a W74/W75

W75 impide presentar un consumo *standby sin RX* como consumo del transmisor alimentando realmente al sensor. W76 añade un segundo control independiente: **el promedio de todas las fases de un ciclo**, incluidos picos breves que una lectura estable podría omitir. La herramienta valida datos finitos, cobertura matemática de duración declarada, incertidumbres, origen de evidencia y potencia entregada promedio por fase; jamás autoriza hardware. Un período de potencia RX *promedio* no garantiza continuidad instantánea: harían falta adquisiciones instrumentadas de voltaje/corriente y análisis de mínimos temporales.

Escenario ABSOLUTAMENTE FICTICIO, **no atribuible a fabricante**: sensor = 2,9 mW, TX a 20 mW durante 29,5 s y TX a 800 mW durante 0,5 s, ciclo = 30 s, RX = 2,9 mW medio en las dos fases. Frente a una distribución por cable IDEAL (sin resistencia):

| Comparación matemática | Solo fase de 20 mW | Ciclo ficticio completo |
|---|---:|---:|
| TX medio | 20 mW | **33 mW** |
| Exceso diario sobre cable ideal | 0,4104 Wh | **0,7224 Wh** |
| Cumple objetivo ilustrativo de máximo +0,5 Wh/día | Sí | **No** |
| Hardware validado | Nunca | Nunca |

Fórmula de energía: \`P_medio = Σ(t_i × P_i)/Σt_i\`; \`ΔWh_día = (P_TX_medio − 2,9 mW)×24/1000\`; techo TX para este presupuesto: **23,733333333 mW**. Por fase se puede proporcionar incertidumbre relativa y obtener una cota alta de TX y baja del **promedio por fase de RX**. 800 mW es un *valor adversarial inventado*, no un pulso de ningún ST, Renesas ni otro producto. Los datos proporcionados como "bench_measured" son solo etiquetas: el programa no verifica instrumentos ni autoría. El indicador \`hardware_approved\` es siempre false.

## Tres contratos independientes

1. **Dock/carga**: totalmente fuera del alcance; no se usa WPT de sensor para cargar batería de litio; BMS, estación y batería aislados.
2. **Potencia distribuida**: primer módulo sensor desmontable, no crítico, comparado contra cable reemplazable de bajo coste. Exigir medición global TX con RX presente 1–20 mW incluyendo ping/handshake, offsets, temperatura, arranques, FOD, EMI, humedad, energía residual, corrientes inversas y corte independiente antes de elegir hardware. No WPT por defecto en bombas/motores.
3. **Datos RF**: evaluar ESP-NOW vs OpenThread con ACK aplicativo, CRC, secuencia, timeout, privacidad, recuperación; WISP solo microsensores RFID. Ni radio alimenta ni detiene físicamente un riesgo crítico.

## Reproducir exactamente sin equipos físicos

\`\`\`sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_76
python3 -m unittest -v test_w76.py
python3 w76_cycle_gate.py --input SCENARIO_SYNTHETIC.json --output regenerado.json
cmp regenerado.json W76_EVIDENCE_SYNTHETIC.json
\`\`\`

**20 pruebas digitales originales** cubren inclusión del pico, error de modelar solo fase estable, ausencia de evidencia de banco, secuencia de fases mal sumada, potencia insuficiente RX, márgenes de incertidumbre, datos malformados/no finitos/overflow, etiquetas falsas, umbral exacto y prohibición de certificación física. El JSON de evidencia documenta \`BLOCKED\` por energía excedida, ciclo no acreditado y datos sintéticos.

## BOM y proveedores

Ver \`BOM_W_IND_76.csv\`, \`MATRIZ_DECISION_W76.csv\`. Ningún componente nuevo es necesario para este cálculo (0 € de compra). ST [STWBC86JR](https://www.st.com/en/power-management/stwbc86jr.html) (TX) y [STWLC38JRM](https://www.st.com/en/power-management/stwlc38jrm.html) (RX) son únicamente pares **documentales activos**, no elegidos: encapsulados de paso fino poco reparables en casa, y falta medición publicada del consumo *global* del enlace TX/RX a 1–20 mW en todas sus fases. Referencia histórica Renesas [P9235A-R](https://www.renesas.com/en/products/p9235a-r) y [P9027LP-R](https://www.renesas.com/en/products/p9027lp-r) obsoletos. Existencias verificadas de la tienda Diotronic próxima, MOQ y precios finales con IVA+envío comparables a TME/Mouser/DigiKey **PENDIENTES**; Diotronic solo proveedor auxiliar, especialmente pasivos/prototipos. No asumir stock por ficha web. La selección de controladores y cortes críticos requiere fabricante, datasheet y trazabilidad.

## Derechos, HEAD 31/10/2026 y coordinación

Contraste contra SHAs registrados en \`19-alternativas-abiertas-para-robot-independiente.md\` el 28/10, revisados en repositorios oficiales y sus PR:

| Proyecto original / licencia | HEAD y rama (31/10) | Estado vs SHA registrada |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | \`master 7c7858c0\` | Igual; PR #1 histórica, no copiar CAD/firmware GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause | \`master 08332bc3\` | Igual; PR #1 histórica |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause | \`640kHz 604eee2d\` | **Divergente** respecto a \`d978a697\`: +68/−11; no es actualización lineal, último commit 2022 |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | \`master c3b5f9be\` | Igual; PR #151 cerrada |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause | \`main b6d0f06d\` | +18 commits; cambios radio y build; PR #13821/#13822 abiertas; release 2026.10.0 |

OOMWOO oficial [makerspet/oomwoo](https://github.com/makerspet/oomwoo) \`main f01a1b29\` (+1 cambio gráfico); [oomwoo-pcb](https://github.com/makerspet/oomwoo-pcb) \`main 87aa7d38\` (+10, docking IR y sensores cliff) y [oomwoo-firmware](https://github.com/makerspet/oomwoo-firmware) \`main ce05f266\` (+7, contratos MCU/pines). No se importó ni modificó código CAD ajeno. Se leyeron decisión NO-TRASPLANTE, D22, coordinación W/C, LEEME_PRIMERO, contrato WPT_DATOS y revisaron otras automatizaciones; repo local compartido tiene cambios de otros compañeros, no se tocó. El desarrollo ocurre solo en rama W de Valdi320/Valdo, PR propia #9, no en OOMWOO PR #79 cleaning-jobs.

## Límites y siguiente paso

**Hipótesis/simulación**: todos los números del escenario y los umbrales; **dato fabricante**: solamente estado de ciclo de vida y funcionalidad general del ST/Renesas, no su consumo aquí; **medición propia**: ninguna. La suma de duraciones se supone secuencial y no demuestra que una captura real no omita eventos; tampoco potencia RX instantánea. Cualquier caso incluso \`DIGITAL_BUDGET_SCREEN_ONLY\` está bloqueado para hardware hasta análisis de fallos físicos. Hay que obtener curvas/documentación de par WPT activo con potencia TX global al transmitir unos 2,9 mW e incluir pulsos de búsqueda/desalineación; si no existe, conservar el cable reparable y solicitar protocolo de banco aislado resistivo con autorización posterior. Quedan sin aprobar FOD, térmica, EMI, corte autónomo, reverse current, descarga, protección RF y seguridad física.
