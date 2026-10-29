# W-IND-35 — Puerta de evidencia contra INA301 sin VDD y ALERT aparentemente sano

29/10/2026 · Trabajo original VALDO sector W · ROBOT NUEVO independiente · SOLO DIGITAL · NO ENERGIZAR.

## Hallazgo y mejora concreta

La resistencia de fin de línea (EOL) de 10 kΩ de W-IND-34 detecta hilos rotos, pero NO demuestra alimentación del INA301. Si VDD_MONITOR desaparece, la salida ALERT_N de drenador abierto puede quedar en alta impedancia, sostener el mismo divisor de tensión y aparentar un monitor sano. Es imposible distinguir estos estados observando únicamente ALERT.

**W-IND-35 introduce un contrato de medida falsable y un validador CSV reproducible** que exige la observación independiente del VDD del INA301 y del supervisor PG, las dos habilitaciones separadas del corte y la tensión real en la carga resistiva artificial. El analizador rechaza registros en los que el monitor no se desalimentó realmente, PG no se desactivó o persistió energía detrás de los cortes. No existe todavía hardware PG validado: es una puerta de evidencia, NO protección eléctrica real ni autorización de alimentación.

## Señales, criterios provisionales y escenarios

CSV, columnas obligatorias en orden: scenario,t_ms,v_logic,v_monitor,v_alert,v_pg,v_enable_a,v_enable_b,v_load,rearm_origin.
- Control v_logic entre 4,5 y 5,5 V hipotéticos, no valores garantizados por datasheet.
- Fallo monitor_vdd_lost: VDD del INA301 en sus pines <=0,5 V; PG independiente <=0,4 V; ALERT aparentemente sano entre 0,40 y 0,60 veces Vlogic. Es la prueba de discriminación fundamental.
- Fallos: ambos EN de cortes normalmente apagados <=0,4 V y Vload <=0,5 V. Solo rearme de procedencia local permite EN >=2,5 V y Vload >=4,0 V en el ensayo sintético.
- Obligatorio registrar t=0 y al menos dos muestras entre 100 y 200 ms con separación <=50 ms. El requisito temporal es una HIPÓTESIS para evitar falsos PASS; no demuestra tiempos eléctricos de corte.
- Escenarios: idle, local_rearm, monitor_vdd_lost, alert_open, alert_short, monitor_pg_lost, restore_no_rearm, rf_rearm_attempt. Sin órdenes RF de rearme físico. Sin ARRANQUE AUTOMÁTICO.
- Valores NaN, negativos, >6 V en el banco hipotético, >10 s, duplicados temporales, escenario ausente o estímulo incompatible: RECHAZO. Un CSV sintético puede cumplir el contrato sin demostrar electricidad.

No se acepta un GPIO que dependa del mismo INA301 ni la propia ALERT como prueba independiente de PG. Quedan pendientes selección de supervisor físico, fuente y comportamiento en arranque/brownout, fugas y retornos parásitos, salidas sin VDD, compatibilidad de niveles EN, dos cortes soldados, FOD y supervisión térmica. El código no prueba el origen ni la calibración de instrumentos.

## Ejecución digital reproducible

En esta carpeta ejecutar:
- python3 -m unittest -v test_w35_bench_contract.py
- python3 w35_bench_contract.py --demo
- Para un futuro banco EXCLUSIVAMENTE AUTORIZADO: python3 w35_bench_contract.py --csv registro_autorizado.csv

**22/22 tests PASS en entorno local aislado**; 32 filas totalmente sintéticas (8 escenarios × 4 tiempos). La demostración declara contract_pass=true, pero TAMBIÉN hardware_validated=false, energization_authorized=false, origin=synthetic y DIGITAL_FIXTURE_DEMONSTRATION_ONLY. Una tabla presentada como measured_unverified sigue en estado HUMAN_INSTRUMENT_AND_SAFETY_REVIEW_REQUIRED. No se midió ni energizó nada. Ensayos negativos incluyen EN A/B pegado, Vload residual, PG incorrecto, fallo no inyectado, rearmado por radio, secuencia temporal defectuosa y datos NaN.

## Matriz de decisiones

| Candidato | Detecta monitor apagado y ALERT sano aparente | Corte eléctrico comprobado | Decisión |
|---|---|---|---|
| EOL sola W34 | NO | NO | Rechazar como protección única |
| EOL + PG booleano ideal | Por supuesto del programa | NO | Insuficiente |
| EOL + PG independiente real + doble EN | Pendiente de KiCad/ensayos | NO | Futuro diseño prioritario |
| W35 CSV VDD/ALERT/PG/EN A/EN B/Vload | **Exige evidencia discriminante** | NO | Aprobar solo como herramienta de análisis |
| Cable corto protegido desmontable | Evita bobinas en sensor fijo | No evaluado | Mantener control económico y de fiabilidad |

Punto dulce: una prueba discriminante reutilizable y pequeña aporta más que añadir más modelos ideales del divisor. Falta construir y verificar el circuito real antes de ninguna prueba física; no se ha ganado fiabilidad eléctrica demostrada.

## BOM, Diotronic y coste

Consultar BOM_W_IND_35.csv. Diotronic 10351 resistencia axial 10 kΩ ±5% 1 W: 0,15 €/unidad con IVA, MOQ 5, disponible en catálogo web, **existencia en Zaragoza pendiente**. No intercambiar huella axial con SMD. Alternativa TME Yageo RC0805FR-0710KL 10 kΩ ±1% 0805, web 0,10 €/unidad con IVA, MOQ 1 y stock general publicado; transporte y entrega reales pendientes. No están elegidos/validados comparator ventana, PG, controlador de rearme ni cortes. Solo fabricantes y distribuidores especializados con trazabilidad para elementos críticos. Cero compras y sin precio final puesto en Zaragoza.
Fuentes: https://diotronic.com/resistencias-de-carbono-1w/16309-resistencia-10k-5-1w ; https://www.tme.eu/es/details/rc0805fr-0710k/resistencias-smd/yageo/rc0805fr-0710kl/ ; https://www.ti.com/product/INA301 ; https://www.ti.com/product/TPS25947 .

## Propiedad, licencias y HEAD revisados el 29/10/2026

Comparación de HEAD originales con pines en 19-alternativas (28/10), sin copiar fuente externa:
- mark-belbin/simple-wireless-power, GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0 = pin. Solo referencia WPT.
- wisp/wisp5-hw, BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda = pin.
- wisp/wisp5, BSD-2-Clause, rama 640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2, diverge 68 ahead/11 behind del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b (auditoría previa); PR #40 abierta, no se asume fast-forward.
- espressif/esp-now, Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin; solo datos RF.
- openthread/openthread, BSD-3-Clause, main e577777c308f6c87e5da3056239231a8fc147cb2 = 14 commits posteriores al pin 7009584dadc20cf20c20a6062f357dd572ba6885; cambios GN/CLI y radio, PR #13820 abierta NO adoptada.
- makerspet/oomwoo oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, actualización del gráfico de estrellas 29/10, sin integración W. PR #79 cleaning-jobs intacta; VALDO PR #9 es solo W.

Fuentes upstream: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo .

Antes de escribir: leídos decisión NO TRASPLANTE X20 del 28/10, 19-alternativas, D22, coordinación C/W y ratificación W, LEEME_PRIMERO, WPT_DATOS_V01, instrucciones de punto dulce AGENTS 18–24 y CONTRIBUTING. Equipo PC compartido ocupado en rama Codex, no editado. Autores, clones upstream, materiales de otro compañero, CAD y OOMWOO intactos.

## Tres subsistemas separados y siguiente paso

Dock de carga: batería/BMS/litio, FOD metal, humedad, térmica y corte TX FUERA del hito, desconectados. Distribución inductiva: primer sensor hipotético 5 V, 80 mA medios, 300 mA pico, fallo de 400 mA; no adoptar WPT para motores/bombas sin medición. Comunicación de datos: comparar ESP-NOW/OpenThread con ACK de aplicación, CRC, secuencia, timeout, privacidad y recuperación, sin confiar en RF para parada crítica. WISP reservado a microsensores de consumo ínfimo.

**Siguiente paso**: calificar supervisor real de VDD/PG y ventana EOL, integrar con doble corte W32/33 en KiCad, comprobar ERC/netlist y transitorios/fallos, FOD/térmica, y SOLO tras aprobación de seguridad medir banco aislado con carga resistiva. Nunca conectar litio, estación, motores ni batería.
