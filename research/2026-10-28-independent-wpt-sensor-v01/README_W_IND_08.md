# W-IND-08 — Riesgo de cortocircuito de descarga QOD al cortar el TX (28/10/2026)

**Alcance:** nuevo robot aspirador abierto y no OEM, primer módulo sensor WPT hipotético 5 V. Modelo matemático offline, sin circuito energizado, sin batería, estación, motores ni modificaciones físicas. Contribución original W exclusivamente; C posee mecánica/CAD; OOMWOO PR #79 es otro ámbito.

## Hallazgo y decisión de ingeniería

El modelo W-IND-07 suponía dos cortes normalmente apagados pero no representaba la descarga rápida de salida QOD. El TPS22918 de Texas Instruments ofrece QOD opcional: cuando se conecta a salida, permite descarga rápida. En un escenario con transistor pasante A permanentemente cortocircuitado y orden de apagado, la QOD activa de A puede crear una ruta de corriente continua desde la fuente hacia masa, aunque B corte correctamente el TX. Es un escenario **hipotético de topología**, NO defecto medido de ese chip.

**Propuesta para estudiar, NO hardware aprobado:** dos interruptores high-side TPS22918 en serie, QOD de ambos SIN CONECTAR, pulldowns ON de seguridad a validar y una resistencia pasiva de descarga posterior a B; las autorizaciones proceden de dos canales analógicos independientes, temperatura, FOD, alimentación y rearme local; jamás de radio. Real FOD, dos interrupciones con independencia física, comparadores, POR, latch, supervisor, retorno de energía y seguridad aún están pendientes. El TPS22918, 1–5,5 V y hasta 2 A según fabricante, **NO sirve para desconectar el rail de 12 V del dock**. El corte de TX no resuelve carga de litio ni distribución de energía de motores.

## Topología en evaluación (no es netlist ni esquema instalable)

Fuente aislada experimental 5 V -> protección de entrada PENDIENTE -> interruptor A normalmente OFF, QOD sin conexión -> interruptor B normalmente OFF, QOD sin conexión -> etapa TX comercial aún por evaluar. Resistencia de descarga 1 kOhm, >=0,25 W hipotética, desde salida posterior a B hasta retorno. Dos resistencias pulldown ON independientes candidatas de 100 kOhm, no dimensionadas por datasheet. FOD real no seleccionado: hasta entonces NO habilitar.

## Resultados cuantitativos reproducibles (suposiciones, no medidas)

| Simulación | Resultado | Limitación |
|---|---|---|
| 2 x 52 mOhm RON típica TI, 1 A supuesto | caída 0,104 V; pérdida 0,104 W | valor típico, no esquina peor |
| Resistencia 1 kOhm a 5 V | 5 mA, 25 mW | solo estudio de pérdidas |
| 100 uF, 1 kOhm, caída ideal 5 V a 0,5 V | 0,23026 s | no demuestra apagado del oscilador RF |
| 470 uF, mismas hipótesis | 1,0822 s | supera objetivo provisional 0,5 s |
| QOD de 200 Ohm **ficticios** con pasante soldado | corriente 25 mA; disipación 125 mW | NO equivale a R_QOD real del TPS22918 |

**Mejora:** al desconectar QOD, el modelo deja de tener la derivación interna hipotética al fallar solo el pasante de una etapa. **No** elimina fallo de dos pasantes, dos pines ON pegados activos, sobrecorriente, corto externo, interferencias ni ausencia de FOD real. Un solo interruptor en corto aún queda bloqueado por el segundo en la lógica ideal; fallos de modo común sin cubrir.

## Matriz de decisiones

| Alternativa | Beneficio | Defecto/riesgo | Decisión |
|---|---|---|---|
| Dos interruptores con QOD conectada | Descarga rápida | shunt sostenido en pasante corto, circuito hipotético | no elegir por defecto |
| Dos interruptores QOD aisladas + bleeder posterior | separación de apagado/descarga y simulación verificable | pérdidas y FOD, reversas, POR y latches pendientes | candidato SOLO para diseño |
| Un interruptor | BOM inferior | una avería activa TX | descartado como protección única |
| WPT regulado comercial con FOD y corte externo | reduce RF propio | sin validación en nuestro montaje | pendiente |
| Cable reemplazable protegido | barato y más eficiente si no hay movimiento | contactos mecánicos | alternativa sólida |

## Pruebas y método

Código original: tx_cut_power_screen.py; pruebas: test_tx_cut_power_screen.py. Python 3.10+ sin bibliotecas externas. Para reproducir, desde research/2026-10-28-independent-wpt-sensor-v01 ejecutar:

    python3 -m py_compile tx_cut_power_screen.py test_tx_cut_power_screen.py
    python3 -m unittest -v test_tx_cut_power_screen
    python3 tx_cut_power_screen.py

**25/25 nuevas pruebas offline PASS en sandbox local:** 9 entradas de permiso, 16 pares de estados de interruptores, QOD en pasante corto, dos cierres peligrosos, descarga RC, pérdida típica, rechazo explícito de 12 V y >2 A y parámetros inválidos. CI suma las pruebas previas solo cuando Github Actions las ejecute. No es certificación, SPICE, prototipo, FOD ni ensayo térmico.

## BOM y compras (ninguna realizada)

Ver BOM_W_IND_08.csv. Referencia TPS22918DBVR estimada DigiKey España 0,47 € sin IVA (0,5687 € IVA 21%) **sin existencias al consultar**. Variante de embalaje TPS22918DBVT en Mouser estimada 1,06 €/unidad, condiciones de IVA/portes y stock aún a verificar. Dos chips según precio meramente publicado DigiKey serían 1,1374 € con IVA sin portes, pero oferta sin stock, NO presupuesto completo. Resistencias genéricas, comparadores, enclavamientos, protección de retorno y FOD: pendientes de selección, precio y cualificación. Diotronic auxiliar para pasivos: SKU/stock/cantidad mínima/precio final **NO VERIFICADOS**. Compare con TME, Mouser y DigiKey antes de aprobar componentes. No comprar ni montar.

Fuentes de fabricante: https://www.ti.com/product/TPS22918 ; https://www.ti.com/lit/gpn/tps22918 ; https://www.digikey.es/en/products/detail/texas-instruments/TPS22918DBVR/7033453 ; https://www.mouser.es/es/ProductDetail/Texas-Instruments/TPS22918DBVT

## Revisión de propiedad, externos y pin Git SHA (28/10/2026)

- Mark Belbin GPL-3.0, simple-wireless-power master HEAD 7c7858c0dd7040801b6f191df1396115560218f0: igual al SHA pin.
- WISP5 hardware BSD-2-Clause, wisp/wisp5-hw master 08332bc398aa3350d351ef2aaac163f8007cffda: idéntico.
- WISP5 firmware BSD-2-Clause, rama 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 vs pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b: diverge 68 ahead y 11 behind; no hacer fast-forward. PR #40 abierta según auditoría W-IND-07.
- Espressif ESP-NOW Apache-2.0, master HEAD c3b5f9be245f1a80db9cb938600566aa6a8dd1e5: igual al pin; solo datos RF.
- OpenThread BSD-3-Clause, main HEAD 3d645eb9106cb1d5c2ff11891e84dc14e52e293a vs pin 7009584dadc20cf20c20a6062f357dd572ba6885: +5/0, cambios en MAC/API radio no aplican al QOD.
- OOMWOO oficial makerspet/oomwoo HEAD main 1c2bd43abcf74288afcf2d8b64514cc325f9b905; adaptación local y PR cleaning-jobs #79 separadas, ningún fichero modificado.

Documentos originales de decisión no Xiaomi, D22, acuerdo de propietarios W/C y VALDO_OOMWOO/LEEME_PRIMERO y WPT_DATOS_V01 fueron leídos desde el PC. VALDO master local está sucio por trabajo ajeno y no se toca. Esta aportación está en rama propia de PR #9 y no reproduce código GPL ni otro de los cuatro autores.

## Bloqueo y siguiente hito

**NO APROBADO PARA INSTALACIÓN NI ENSAYO ENERGIZADO**. Es imprescindible concretar el circuito KiCad/contrato de habilitación independiente: QOD desconectadas, pulldowns, POR, latches, comparadores, fallos comunes, protección de retorno/entrada y comportamiento de la etapa TX ante corte; FOD físico independiente con umbrales de falsos negativos, temperatura/EMI/offset. Caracterizar todo esto antes de ensayo aislado autorizado con carga resistiva; batería y BMS siempre separados inicialmente.
