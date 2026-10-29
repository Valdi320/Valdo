# W-IND-31 — Bloqueo de habilitación falsa por ALERT en alta impedancia

**29/10/2026 · sector W propio · robot aspirador NUEVO e independiente. Solo software; instalación y energización NO autorizadas.**

## Defecto específico descubierto antes de crear la desconexión

El INA301 de TI entrega una salida **ALERT de drenador abierto, activa a nivel bajo** al detectar sobrecorriente; en reposo necesita una resistencia pull-up para obtener un nivel lógico alto. El TPS25947 dispone de **EN/UVLO activo en alto**. Por tanto, **conectar ALERT + pull-up directamente a EN (o invertir su intención sin un PG independiente) no demuestra seguridad**: una línea alta por pull-up no prueba que el INA301 siga alimentado y capaz de detectar fallos. La conducta concreta con el INA301 desalimentado requiere revisar su especificación eléctrica y/o ensayarlo; el modelo introduce conservadoramente la posibilidad de ausencia de hundimiento. **No afirmamos haber medido ni caracterizado tal estado en el chip.**

Una protección eléctrica real debe exigir **una prueba positiva de suministro de vigilancia válido**, no interpretar la ausencia de alarma como autorización. La condición de permiso prevista, NO implementada, es: monitor alimentado y válido, dos supervisores/alimentaciones de corte calificados, corriente aceptable, temperaturas válidas, FOD aceptable y **rearme local nuevo**. Cada actuador debe arrancar normalmente OFF; la RF jamás rearma ni se usa para parada de emergencia.

### Contrato/diagrama funcional (NO esquema de fabricación)

    RX_5V_SOURCE ── [CUT_A con RCB, OFF por defecto] ── [CUT_B con RCB, OFF por defecto] ── SENSOR_RX
                           ▲                                ▲
                   EN_A: prueba positiva A          EN_B: prueba positiva B
                           ▲                                ▲
       PG_A válido + monitor activo + alarma sana + temperatura/FOD + latch local
                NO conectar INA301 ALERT directamente a EN
       ALERT (open drain; LOW=alarma) ───> lógica de inhibición **independiente de radio**

**Crítica importante:** el diagrama aún usa calificaciones lógicas compartidas y, por sí solo, NO demuestra independencia física de alimentación, reset o comparadores. Diseñar dos caminos físicos aislados por fallo común sigue pendiente. Cortes con RCB idealizados **no equivalen** a piezas cualificadas; dos elementos soldados o un puente pueden alimentar la carga.

## Reproducibilidad y evidencia

Ejecutar con Python >= 3.10 sin dependencias, en esta carpeta:

    python3 -m unittest -v w31_alert_power_gate
    python3 w31_alert_power_gate.py > evidence.json
    python3 -m json.tool evidence.json

**Resultado local verificado antes de publicar:** 12/12 pruebas PASS; 256 combinaciones exhaustivas de 8 señales hipotéticas; 0 estados energizados indebidos entre los casos de fallo con máximo un corte soldado, **pero 63 casos sintéticos inseguros con ambos cortes soldados** y al menos una condición de alarma. Esto NO es tasa de fallo ni eficacia física. El anti-patrón conserva EN alto con monitor desalimentado **en el modelo de pull-up y salida incapaz de hundir corriente**. El nuevo contrato, bajo supuestos ideales, bloquea y requiere flanco de rearme local.

El código tiene pruebas de: salida abierta normal; fallo de alimentación del monitor; alarma activa; encendido inhibido; FOD, térmica y pérdida de PG; un corte soldado; dos cortes soldados; RF ignorada; recuperación solo con nuevo flanco local; reinicio después de brownout. Archivo íntegramente original; ni esquemas ni bibliotecas de terceros incorporados.

## Matriz de decisión

| Arquitectura | Estado | Evidencia/ventaja | Bloqueo |
|---|---|---|---|
| ALERT open-drain con pull-up conectado directamente a EN | **RECHAZAR** | El pull-up puede marcar sano sin prueba de monitor alimentado | Validar I/O desalimentado y alimentación parásita; nunca permitir sola |
| INA301 + dos permisos positivos independientes, latch local | **CONTRATO DIGITAL** | 12 tests y 256 combinaciones, cero fallos sintéticos hasta 1 corte soldado | Falta circuito KiCad con pinout real, PG/POR y disparos autónomos; causas comunes |
| TPS3890 supervisor VDD/SENSE | Candidato por cualificar, NO elegido | TI documenta RESET activo bajo de drenador abierto y detección de undervoltage | No basta otra señal open-drain; exigir driver de permiso positivo y estado al perder suministro |
| TPS25947 con RCB | Candidato no elegido | Bloqueo inverso documentado, EN activo alto | Límite integrado mínimo 0.5 A no detecta por sí solo el caso RX 0.4 A |
| ESP-NOW / OpenThread | Separado del poder | ACK aplicación, CRC, secuencia, timeout, cifrado autenticado y recuperación pendientes de hardware | La radio NO es watchdog eléctrico ni corte |
| Dock, Li-ion/BMS, motores y bombas | **FUERA DEL PILOTO** | Evita trasladar el umbral RX a TX o motores | Seguridad y curvas de consumo independientes; no conectar |

El piloto se mantiene en requisitos **hipotéticos** 5 V, 80 mA medio, 300 mA pico; fallo supuesto 400 mA. FOD metálico, EMI, offset, humedad, pérdidas y termometría real **no están aprobados**. Dock de carga y energía distribuida a un microsensor son dos diseños distintos; radio es un tercero. WISP5 queda únicamente para microsensores RFID intermitentes de menor consumo.

## Contraste externo realizado 29/10/2026 (propietarios y licencias)

| Proyecto original | Rama y HEAD 29/10 | Respecto a SHA fijado 28/10 | PRs/documentación revisados |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master [7c7858c](https://github.com/mark-belbin/simple-wireless-power/commit/7c7858c0dd7040801b6f191df1396115560218f0) | Idéntico | PR [#1](https://github.com/mark-belbin/simple-wireless-power/pull/1), circuitos del autor sin control FOD adoptado |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master [08332bc](https://github.com/wisp/wisp5-hw/commit/08332bc398aa3350d351ef2aaac163f8007cffda) | Idéntico | PR [#1](https://github.com/wisp/wisp5-hw/pull/1) |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | **640kHz** [604eee2](https://github.com/wisp/wisp5/commit/604eee2dffaeba3a270de61cf3dae887a33309c2) | Divergencia **+68/-11** frente a d978a697 | [#40](https://github.com/wisp/wisp5/pull/40); no realizar fast-forward ni copiar firmware |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master [c3b5f9b](https://github.com/espressif/esp-now/commit/c3b5f9be245f1a80db9cb938600566aa6a8dd1e5) | Idéntico | PR [#153](https://github.com/espressif/esp-now/pull/153) (cambio de wakeup, no WPT) |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main [e577777](https://github.com/openthread/openthread/commit/e577777c308f6c87e5da3056239231a8fc147cb2) | +14/-0 vs 7009584 | PR [#13820](https://github.com/openthread/openthread/pull/13820), [#13730](https://github.com/openthread/openthread/pull/13730), desarrollo activo IP/radio; sin integración |

OOMWOO oficial makerspet/oomwoo main [f01a1b2](https://github.com/makerspet/oomwoo/commit/f01a1b295f462da5ab8d5f021a3f741cbd2b47df), cambios recientes no relacionados con el módulo W. VALDO PR #9 HEAD anterior b2110d7048be5ec09d42ef49385e224c9eca3f9e; adaptación local VALDO_OOMWOO se preserva; OOMWOO cleaning-jobs #79 no es destino. Otras automatizaciones comprobadas: solo W habilitada; OOMWOO horario pausado. Checkout VALDO local en master tenía cambios ajenos sin commitear: no se tocó. Acuerdos W/C y la decisión del 28/10 leídos antes de escribir. Todo se publica exclusivamente en la rama W propia, no en repositorios de autores ni clones upstream.

Fuentes de fabricante: [INA301 (open-drain, modo enclavado)](https://www.ti.com/product/INA301), [TPS25947 (EN activo alto, RCB, 0.5 A mínimo)](https://www.ti.com/product/TPS25947), [TPS3890 (supervisor RESET abierto)](https://www.ti.com/product/TPS3890). Las características lógicas proceden del fabricante; **las simulaciones y sus condiciones son nuestras y no son mediciones**. Los SHAs externos son lecturas de GitHub, no versiones adoptadas.

## BOM de evaluación y abastecimiento

Véase [BOM_W_IND_31.csv](BOM_W_IND_31.csv): componente exacto, cantidad, fuente Diotronic/alternativas, precio con IVA, MOQ y stock verificado o pendiente. La única oferta numérica consultada es INA301A1IDGKR en [DigiKey España](https://www.digikey.es/es/products/detail/texas-instruments/INA301A1IDGKR/6571979): corte de cinta 1 ud a **2,77 € sin IVA / 3,3517 € con 21% IVA**, sin portes, stock web comunicado y NO comprobado físicamente; Diotronic Zaragoza sin confirmación. Ninguna selección de compra ni sustitución crítica.

**Siguiente puerta única:** construir un KiCad nuevo de dos etapas normalmente apagadas con **permiso positivo real** desde alimentación supervisada, pinout y fallos comunes comprobados por ERC/netlist. Verificar apagado con INA301 sin tensión y después FOD/térmica del TX con circuitos independientes. No aprobar hardware por la prueba digital. No comprar, soldar, imprimir, alimentar ni conectar litio.
