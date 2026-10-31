# W-IND-11 — Coste energético de transmisores inductivos en vacío (28/10/2026)

Hito W propio, independiente del X20 Pro OEM, del mantenimiento mecánico C, de OOMWOO y de PR #79. Mejora: una decisión reproducible que impide escalar módulos WPT sin cuantificar su pérdida en reposo. **No implementa electrónica, no habilita ni protege una bobina, no hay medidas propias.**

## Evidencia externa y cálculo
- La tienda BricoGeek publica para el kit **DFRobot DFR0362**: 5 V de entrada, **30–50 mA de consumo en reposo**, precio **9,92 € con IVA**, envío desde **3,95 €** y advertencia de cables de bobina frágiles: https://tienda.bricogeek.com/fuentes-de-alimentacion/899-cargador-inalambrico-5v-1a.html (consulta 28/10/2026). Son afirmaciones del VENDEDOR, no mediciones nuestras; verificar condiciones exactas de ensayo y cotización antes de comparar hardware.
- El fabricante DFRobot especifica 5 V / 1 A, separación nominal de 2–10 mm y eficiencia que *podría alcanzar* 90 %: https://wiki.dfrobot.com/dfr0362 . La cifra máxima NO demuestra eficiencia de carga parcial, en vacío, con offset, a largo plazo, ni FOD o apagado seguro.
- Opencircuit España también anuncia kit DFR0362 a 9,50 € con IVA, envío desde 12,50 € y almacén externo: https://opencircuit.es/producto/wireless-charging-module-5v-1a . Ejemplo de suelo anunciado 22 € en pedido unitario, no presupuesto definitivo.
- Diotronic confirma venta al detalle: https://diotronic.com/ . Referencia, stock de la sucursal próxima, pedido mínimo, precio con IVA de un módulo WPT y protector equivalente: **SIN VERIFICAR**. Diotronic es auxiliar, no dependencia.

**Fórmula verificable de potencia en vacío**: N × V_TX × I_sin_carga. Para UN transmisor DFR0362 bajo las condiciones anunciadas: 5 V × (0,030–0,050 A) = **0,15–0,25 W** SIN receptor/carga. Para OCHO transmisores hipotéticos mantenidos encendidos sin receptor: **1,20–2,00 W**, o **28,8–48 Wh por cada día de 24 h** sin receptor. OCHO no es la cantidad aprobada para VALDO.

**Hipótesis de ingeniería para evaluar un corte local:** si un interruptor independiente y realmente normalmente apagado consumiera TOTAL 5 mW por interfaz en OFF (NO MEDIDO NI ESCOGIDO), ocho interfaces sin módulos gastarían 0,04 W, una diferencia teórica de **1,16–1,96 W**, o **27,84–47,04 Wh/día** durante 24 h sin receptor. A cinco años de 365 días y 0,25 €/kWh FICTICIOS, se corresponde con 50,808–85,848 kWh o 12,70–21,46 € de coste energético evitado. NO es un ahorro observado ni una razón suficiente por sí sola para instalar WPT.

A la vez, el mínimo de lista anunciado para ocho kits DFR0362 de BricoGeek sería **8×9,92 € + 3,95 € de envío desde = 83,31 €**, sin protecciones, reguladores, FOD, radio, PCB, reparación, impuestos adicionales si aplicaran ni garantía de precio múltiple; no existe BOM final aprobada. Nunca inferir que tener ocho bobinas equivale a ocho módulos útiles.

## Decisión práctica y requisitos medibles

| Problema | Decisión W-IND-11 | Verificación pendiente |
|---|---|---|
| Dock / carga de batería | APLAZADO, sin conectar litio ni BMS | FOD, parada local, certificación aplicable, gestión térmica y carga autónoma |
| Potencia WPT del primer sensor **no crítico** | SOLO un enlace piloto hipotético 5 V / 0,4 W medio / 1,5 W pico, no ocho TX | consumo de sensor real y corriente de arranque; TX no-load por posición, tensión y temperatura; RX regulada |
| Estado sin receptor | Diseñar como requisito evaluable **TX localmente OFF**, jamás ON permanente por defecto | medida de W apagados y tiempo de descarga; dos cortes, FOD, térmica, agua, EMI y offset independientes |
| Transmisión ESP-NOW / OpenThread | Datos exclusivamente, con ACK de aplicación, CRC, secuencia, timeout, privacidad y reinicio local | ensayos RF reales; nunca paro de seguridad basado en radio |
| WISP5 RFID | Solo microsensores ultrabajos si la potencia y el lector lo justifican | corriente real, duty cycle, continuidad |
| Alternativa cableada reemplazable | Mantener como referencia económica/reparable, no declarar cables ahorrados | longitud, conectores, ciclos, precio con IVA, mantenibilidad y propietario C |
| Motores y bombas | NO WPT por defecto | potencia y pérdidas medidas |

**Criterio de rechazo temprano:** ningún marketing de «90 % de eficiencia» sustituye la medición de potencia de entrada con y sin módulo; si el equipo pretende dejar el emisor continuamente activo, contabilizar también el consumo SIN carga. El presupuesto **1 W para ocho TX en vacío** es un ejemplo de requisito, no aprobado: los 1,2–2,0 W anunciados lo incumplen. El límite de 5 mW OFF también es una hipótesis de cribado y requeriría selección eléctrica y medida propia; no hay diseño ni aprobación física de los cortes. Un circuito real debe estar normalmente deshabilitado, mantener independencia de FOD/térmica/corriente/agua y no depender de radio para desconexión crítica.

## Reproducir
Desde esta carpeta: python3 -m py_compile standby_energy_screen.py test_standby_energy_screen.py ; python3 -m unittest -v test_standby_energy_screen ; python3 standby_energy_screen.py

**Resultado previo en sandbox aislado:** 44/44 pruebas Python PASAN (aritmética, rangos de incertidumbre, escalado, entradas negativas, nulas, NaN, infinito, presupuestos e imposibilidad de aprobación física). Después del commit, GitHub Actions debe probar también la regresión total; no presumir estado de CI sin consultarlo. No se han ejecutado ensayos con bobinas, herramientas ni batería.

## Auditoría upstream, autoría y otros ámbitos
Revisión API GitHub del 28/10/2026, contrastada con los cinco SHAs de 19-alternativas-abiertas-para-robot-independiente.md, HEAD, commits, PR y releases:
- mark-belbin/simple-wireless-power — propietario mark-belbin, GPL-3.0, master **7c7858c0dd7040801b6f191df1396115560218f0**, idéntico al pin. PR #1 cerrada, última actividad 2021, sin última release publicada. No copiar firmware ni KiCad.
- wisp/wisp5-hw — propietario wisp, BSD-2-Clause, master **08332bc398aa3350d351ef2aaac163f8007cffda**, idéntico. PR #1 cerrada, sin última release. No importar hardware.
- wisp/wisp5 — propietario wisp, BSD-2-Clause, rama default **640kHz**, HEAD **604eee2dffaeba3a270de61cf3dae887a33309c2**, **diverge +68/-11** del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; PR #40 abierta, sin última release. NO fast-forward ni tratar como software de robot.
- espressif/esp-now — propietario espressif, Apache-2.0, master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, idéntico; cambios de compatibilidad IDF v6 y consola, última release v1.0 de 2022, PR #153 cerrada. No se integra código externo.
- openthread/openthread — propietario openthread, BSD-3-Clause, main **995eee810c2707cdf676f7097960ce066935b2c1**, **+8/-0** desde pin 7009584dadc20cf20c20a6062f357dd572ba6885. Cambios recientes en radio address filter, spinel/heap, API direct radio availability y neighbor parent; release v2026.10.0 (01/10/2026), PR #13804 abierta sobre reintentos de energy scan; no presumirla fusionada.
- OOMWOO oficial makerspet/oomwoo main **1c2bd43abcf74288afcf2d8b64514cc325f9b905** sin nuevos commits frente a revisión anterior; #79 cleaning-jobs se mantiene AJENA. VALDO PR #9 HEAD previo **7fc1e5068ec457d336c2196c82c47335b8143505**, trabajo anterior W-IND-10. Los repositorios/clones de autores originales, Codex A01–Axx, W de compañeros, CAD C y master local con cambios sin confirmar no se modificaron.

Fuentes maestras leídas antes de intervenir: decisión 00_DECISION_20261028_NO_TRASPLANTE_X20.md, 19-alternativas-abiertas..., D22 digital, coordinación C/W, VALDO_OOMWOO/LEEME_PRIMERO.md, WPT_DATOS_V01.md. Este modelo y pruebas son ORIGINALES; sin código/CAD de terceros. VALDO todavía no tiene licencia global seleccionada, pendiente de decisión del titular.

## Siguiente paso (NO realizado)
Escoger, mediante plano revisable, un TX con FOD física y parada local normalmente OFF, medir bajo autorización en banco RESISTIVO AISLADO **tres modos distintos** (receptor ausente, presente sin carga y carga piloto con offsets), incluyendo arranque/apagado, disfunción de corte, temperatura y humedad; seguridad independiente de ESP-NOW. No compras ni prueba física sin proceso aprobado. El primer módulo deberá justificar su cable eliminado y coste total antes de escalar.
