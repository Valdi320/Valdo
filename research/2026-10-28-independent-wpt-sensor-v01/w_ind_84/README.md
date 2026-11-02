# W-IND-84 — verificador reproducible de trazas WPT/RF, **sin aprobación física**

**1 de noviembre de 2026 · diseño y pruebas de software ORIGINALES del sector W.** Robot aspirador **NUEVO**, independiente del Xiaomi X20 Pro (decisión del 28/10). Hito abierto para evaluación; no es un controlador de carga o motor, ni equipo de seguridad certificado. No modificar firmware, BMS, batería, motores, estación real ni repositorios de otros.

## Mejora material

Los hitos W74–W83 mostraron que un consumo de transmisión en reposo, las muestras espaciadas de tensión y los presupuestos promedio pueden ocultar un sistema energéticamente inviable. **W84 añade un contrato de traza importable**, para no interpretar cifras sintéticas ni hojas de datos como medidas propias de energía.

**Entrada**: CSV UTF-8 de muestras alineadas con cabecera exacta
`t_us,tx_mv,tx_ua,rx_mv,rx_ua,rail_mv,phase`.
Tiempo de cada muestra en microsegundos desde cero, tensiones en mV, corrientes en µA positivas y fase de radio `sleep|wake|tx|rx|ack|retry|idle`. La entrada TX se mide **antes** del transmisor inductivo, la RX **después** de regulación al nivel elegido. La RX debe incluir el consumo de radio, cuando exista; no hay ningún canal separado de RF por ahora. Potencia = mV·µA / 10⁹ W. Energía en µJ durante un intervalo = (P₀+P₁)·Δt/(2·10⁹), usando los valores de mV, µA y µs del fichero (integración trapezoidal de valores muestrales).

**Manifiesto** JSON obligatorio para trazas externas: `case_id`, `provenance` (`synthetic`, `manufacturer_data`, `bench_measured`), `trace_sha256` SHA-256 hexadecimal de los **bytes originales** del CSV, `max_gap_us` positivo, `required_rail_min_mv`, `rail_uncertainty_mv`. Si se marca `bench_measured`: además `instrument_id`, `calibration_reference`, `fixture_id`, `operator_record`, `steady_state_cycle: true`. Esos campos **no prueban autenticidad**; una persona debe revisar el registro y la calibración. El hash protege de alteraciones inadvertidas, **no es firma digital**. Las muestras de banco deberían incluir 10 contratos de datos de 250 ms (2,5 s) como mínimo, al menos cinco fases RF y un paso máximo declarado de 1 ms; estos límites son **hipótesis de muestreo**, insuficientes para certificar transitorios de cientos de µs.

**Salida**: JSON determinista, potencias integradas de TX y RX, eficiencia aparente, mínimo de tensión observado con incertidumbre, observación de las fases de radio, causas de rechazo y `hardware_release: BLOCKED` **siempre**. La aceptación de la traza significa solo **admisibilidad formal digital** para un análisis posterior, nunca idoneidad de un par WPT.

**Rechaza**: CSV defectuoso, sin UTF8, fecha no monótona o fraccional, registros incompletos, valores negativos/NaN/inf, fase desconocida, SHA distinto o ausente, intervalo excesivo, tensión muestreada por debajo del umbral incluyendo incertidumbre, energía TX cero, energía RX mayor a energía TX sin contabilidad de almacenamiento, ausencia de fases sleep/wake/tx/rx/ack, ausencia de datos identificativos de instrumento para medida propia. Un parámetro de fuga de energía a través de almacenamiento o una etapa no monitorizada puede producir aparente >100% aun con mediciones correctas: el resultado ordena **revisar**, no prueba fraude.

## Evidencia reproducible (ninguna medida real)

```sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_84 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_84/w84_trace_gate.py > /tmp/w84.json
cmp /tmp/w84.json research/2026-10-28-independent-wpt-sensor-v01/w_ind_84/expected.json
# Más adelante, solo tras autorización de banco: 
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_84/w84_trace_gate.py --manifest /ruta/registro.json --trace /ruta/registro.csv
```

**Demo puramente inventada**: 5 ms, TX 5 V × 4 mA = 20 mW, RX 3,3 V × 1 mA = 3,3 mW; integración 100 µJ frente a 16,5 µJ, eficiencia **aparente** de 16,5 %. El JSON queda `evidence_eligible: false` porque `provenance=synthetic`, `hardware_release: BLOCKED`. Esa eficiencia **no** pertenece a ningún producto ni mide un robot. Python 3.12, biblioteca estándar. Pruebas adversariales originales incluidas en la CI dedicada; el JSON generado se compara byte a byte y se publica como artefacto.

## Principales límites de inferencia

- El cálculo usa integraciones de **muestras**, no capturas analógicas continuas; no detecta brownouts entre muestras, EMI, FOD, desalineación o sobrecalentamiento. El mínimo muestreado **no es un mínimo garantizado**. La capacidad, ESR, energía almacenada, recarga y estado final no se deducen del CSV; `steady_state_cycle` es declaración externa pendiente de validar.
- Si las fases RF tienen corriente propia no contenida en `rx_ua`, el análisis infravalora energía; hay que medir todos los canales activos. CRC, ACK de aplicación, HMAC, secuencias, timeout y privacidad se validan con mecanismos independientes: fase `ack` no demuestra que la aplicación haya confirmado.
- `tx_ua` es consumo de **TX inductivo**, no radio; el RF pasa por el consumo RX si está en esa misma alimentación. El uso de 1 ms de muestreo no verifica los picos de 1–200 µs. La duración de 2,5 s no prueba ciclos largos, temperatura de estacionario ni envejecimiento.
- El corte de potencia física debe ser **local e independiente de radio y software**. Ni FOD ni el supervisor, doble corte, temperatura o bobinas se seleccionan como aprobados. Sin batería ni BMS conectados en el primer banco, y **ninguna prueba física** hasta proceso de seguridad y autorización.
- La **estación de carga** (alineación/bobinas/carga de batería), la **alimentación de módulos** de bajo consumo y los **datos RF** son tres problemas separados. No se propone WPT para motores o bombas.

## Control de ámbito y autoría

Se leyeron decisiones, 19-alternativas, D22, coordinación W/C y contratos VALDO_OOMWOO. Exclusiva W: análisis eléctrico y telemetría. C conserva CAD y fijaciones; OOMWOO oficial y PR #79 cleaning-jobs permanecen fuera. Sin copiar códigos, CAD ni esquemas externos. Los SHAs de los cinco repositorios de cuatro familias externas y los cambios oficiales de OOMWOO están contrastados en `BOM_DECISION.md`. Las licencias son las declaradas por autores, no se trasplantan. Todo el código W84 es independiente.

**Próxima puerta útil:** obtener, para **un par TX/RX activo en catálogo**, medidas completas del consumo a 1–20 mW y espectro RF por ciclo, incluyendo búsqueda, reposo, offset, pérdidas, reinicio, ACK y reintentos, con instrumentación y límites documentados; comparar con cable desmontable. Mientras tanto no se elige dispositivo, tensión física, condensador ni placa.
