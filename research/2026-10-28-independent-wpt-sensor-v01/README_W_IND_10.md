# W-IND-10 — FOD y cota de incertidumbre (28/10/2026)

Hito de una única mejora: modelo Python original y 21 pruebas automatizadas, para el robot NUEVO abierto, reparable, imprimible y local. No es un detector físico, firmware MCU, protección certificada ni control de energía. Nada de trasplante OEM Xiaomi, batería, BMS, carga de estación, motor, compra o intervención de hardware; repositorios ajenos, PR #79 y ámbito C intactos.

## Hallazgo y reproducción

Calcula la diferencia de pérdidas de potencia DC entre una referencia y otra observación de la MISMA pareja, carga, bancada y geometría: delta=(Pin−Pout)evento−(Pin−Pout)referencia. Incertidumbre conservadora U = suma de errores absolutos de los cuatro valores + deriva, NO desviación estándar. La cota [delta−U, delta+U] puede quedar por debajo, cruzar o superar un umbral diagnóstico puramente hipotético. En ningún caso afirmar FOD libre: las pérdidas eléctricas también cambian por ferrita, acoplamiento y electrónica; no son calor de metal. El dato RX por radio no vale como medida independiente calibrada.

Demostración 100% SINTÉTICA, no medición de nuestro robot ni valor de seguridad: 2 W entrada y 1 W salida de referencia; cuatro cotas ±0,04 W y ±0,03 W de potencia y deriva ±0,05 W → U=0,19 W. Umbral diagnóstico inventado de 0,25 W:
- delta 0 W → intervalo [-0,19,+0,19] W: sin exceso resoluble; no «FOD limpio».
- delta +0,12 W → [-0,07,+0,31] W: INDETERMINADO; no autorizar.
- delta +0,50 W → [+0,31,+0,69] W: EXCESO SOSPECHADO; investigar.

Rechaza instrumentos y valores inválidos, datos de radio, diferencias de pareja/montaje/procedencia y cambios de XY >0,5 mm, gap >0,2 mm o ambiente >2°C. Esos límites son supuestos de cribado, no tolerancias aprobadas. Los tres campos de permiso físico son siempre FALSE incluso si la pérdida es grande; no confiar en radio para paro crítico, ni en este script para interrumpir la potencia.

En research/2026-10-28-independent-wpt-sensor-v01 ejecutar:
python3 -m py_compile fod_uncertainty_gate.py test_fod_uncertainty_gate.py
python3 -m unittest -v test_fod_uncertainty_gate
python3 fod_uncertainty_gate.py
La PR incorpora los tests a GitHub Actions. Solo las ejecuciones reales determinan cuántos pasan.

## Matriz y BOM

| Dominio | Decisión | Pendiente |
|---|---|---|
| Dock / carga de litio | NO energizar ni conectar | estación/BMS/seguridad separados |
| Potencia sensor WPT 5V, 0,4W medio / 1,5W pico hipotéticos | cribado de metrología digital, no aprobación física | TX normalmente OFF, FOD real, doble corte independiente, térmica, metales, agua, EMI/offset |
| RF ESP-NOW / OpenThread | alternativas para datos, no energía | ACK, CRC, seq, cifrado, hardware real |
| WISP5 | solo sensor RFID de energía mínima | consumo/lector por demostrar |
| Motores/bombas inductivos | NO adoptar por defecto | consumos/picos/pérdidas desconocidos |

BOM_W_IND_10.csv: dos mediciones de energía independientes, fuente aislada, carga artificial, termistores, FOD físico y dos cortes reales pendientes de elegir. Diotronic AUXILIAR: referencias, stock local, pedidos mínimos y precios con IVA pendientes; no compras ni componentes inventados.

## Fuentes, ramas, autoría y control de solapamiento

Se leyeron documentos maestros decisión-no-OEM y alternativas, D22, coordinación cableado C/W, VALDO_OOMWOO/LEEME_PRIMERO y contrato WPT_DATOS_V01. El master del usuario contiene cambios sin confirmar de otros: NO TOCAR. La rama propia Valdo PR #9 tenía HEAD 70e0f10cafc55b51894c9603244181a5563144af antes del hito. Codex A01–A14 está en ramas propias y no se integró ni se presenta como trabajo nuestro; OOMWOO main 1c2bd43abcf74288afcf2d8b64514cc325f9b905, PR #79 cleaning-jobs ajena.

Auditoría GitHub HEAD, pin en 19-alternativas, PR y release (28/10/2026):
- mark-belbin/simple-wireless-power GPL-3.0 master 7c7858c0dd7040801b6f191df1396115560218f0, idéntico, sin PR ni release latest.
- wisp/wisp5-hw BSD-2-Clause master 08332bc398aa3350d351ef2aaac163f8007cffda, idéntico, sin PR ni release latest.
- wisp/wisp5 BSD-2-Clause **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2, diverge del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b (+68/-11), PR #40 abierta, sin release latest.
- espressif/esp-now Apache-2.0 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5, idéntico, release v1.0 14/03/2022, sin PR abierta.
- openthread/openthread BSD-3-Clause main 42717efd5b1203eb888fb38db462253237fb077b, +6/-0 desde pin 7009584dadc20cf20c20a6062f357dd572ba6885, release v2026.10.0, PR reciente #13808. No copiar su código ni integrar de forma automática.

Fuentes físicas de terceros, solo criterios generales, sin copiar código:
TI FOD: https://www.ti.com/video/5104921249001
IEC 63563-7:2025 FOD: https://theiteh.com/catalog/standards/iec/2aebf0ed-d5ee-4986-93cb-af6beec820d2/iec-63563-7-2025

Siguiente puerta de seguridad: esquema eléctrico con FOD físico local, doble corte normalmente OFF, temperatura y protección ante alimentación inversa; documentación ERC/SPICE y pruebas con fuente aislada y carga resistiva SOLO si se aprueba procedimiento. Cero FOD medido, cero hardware aprobado.
