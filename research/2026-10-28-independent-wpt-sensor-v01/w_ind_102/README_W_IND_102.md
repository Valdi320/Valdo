# W-IND-102 — ST25DV64KC: energía EH realista y frontera de primer microsensor

Fecha: 2026-11-01. Ámbito: W propio de VALDO. Este hito corrige una conclusión de alcance de W-IND-90 y añade un cálculo reproducible; no cambia hardware ni firmware.

## Hallazgo de alto retorno

La nota oficial ST AN4913 Rev. 2, tabla 1, incluye expresamente ST25DV64KC (además de ST25DV04KC/16KC y sus variantes KC). Por tanto, las curvas de las tablas 4 y 5 no deben descartarse como si solo aplicasen al 04KC. La limitación que sí permanece es distinta: AN4913 mide sobre antena ISO/IEC clase 1, sintonizada a 13,6 MHz, con 10 nF en V_EH; eso no demuestra el comportamiento de la antena circular de 54 mm de la placa X-NUCLEO-NFC07A1. W-IND-102 corrige la parte del número de componente y conserva la incertidumbre de la placa/antena.

La mayor potencia de la tabla AM=10 % es **12,593 mW a 5,5 A/m RMS**; con AM=100 % es **8,640 mW**. Frente al objetivo piloto heredado de 0,4 W medios / 1,5 W pico (hipótesis de W-IND-06, no medición), incluso el mejor punto AN4913 representa solo **3,148 %** de la potencia media y **0,840 %** del pico: faltan factores **31,76×** y **119,11×** respectivamente. Decisión: **ST25DV64KC EH no sirve para alimentar el módulo activo de 0,4 W**. No es un receptor Qi ni un sustituto de una etapa WPT de potencia.

## Requisito propuesto del primer módulo de bajo consumo

Primer candidato: sensor ambiental/no crítico, no sensor de parada ni protección del robot.

- Consumo medio objetivo: **≤0,25 mW**.
- Pico de diseño ilustrativo: **≤5 mW durante ≤10 ms**, cubierto por almacenamiento local.
- Campo de referencia mínimo: **≥1 A/m RMS en la antena real**; debe medirse, no inferirse del lector.
- Ventana de cálculo del buffer: 3,3 V → 2,0 V, eficiencia 80 %, capacitancia retenida 50 %. Para 50 µJ resulta C efectiva ≥18,14 µF y nominal ≥36,28 µF; 47 µF es solo valor candidato. ESR, fuga, tolerancia, corriente de arranque, tensión V_EH y tiempo de recarga no están medidos.
- La tabla AN4913 tiene 20 puntos con H≥1 A/m; el menor es 1,035 mW. El objetivo 0,25 mW deja 4,14× de margen en ese conjunto de referencia. **No es una garantía de la placa ni del robot**.

El V_EH del ST25DV64KC es analógico/no regulado y pasa a alta impedancia si el campo es insuficiente o EH está deshabilitado. La comunicación RF puede funcionar dentro de la región verde caracterizada por AN4913, pero no está garantizada en todo el dominio; cargas altas reducen la región útil y pueden hacer perder comunicación. El buffer y la secuenciación de lecturas son obligatorios; una lectura RF no puede ser permiso de seguridad.

## Decisión de arquitectura

| Necesidad | Decisión |
|---|---|
| Microsensor no crítico ≤0,25 mW medio | ST25DV64KC EH o WISP5 solo como candidatos pasivos; validar antena/campo, cold-start, buffer y datos en la placa real |
| Módulo activo 0,4 W medio / 1,5 W pico | Rechazar EH NFC; usar WPT dedicado regulado con FOD, temperatura, offset, EMI y corte independiente, o conservar conector bloqueable reparable |
| WPT sencillo en lazo abierto | Rechazado para robot autónomo: no demuestra regulación, FOD, termometría, tolerancia al offset ni corte independiente |
| Carga de dock | Sistema separado; batería/BMS/estación no forman parte de este hito |
| Datos de módulos activos | ESP-NOW primero para una red local pequeña de un salto si los nodos son Espressif; OpenThread solo si hacen falta IPv6/mesh/multi-hop |
| Microsensores pasivos | WISP5 puede estudiarse si el lector y el coste total justifican RFID; no es alimentación de motores, bombas ni un módulo de 0,4 W |

ESP-NOW y OpenThread son **transporte de datos, no alimentación**. En cualquiera: ACK de aplicación, CRC, número de secuencia, timeout, reintentos acotados, autenticación/cifrado y recuperación local. La parada crítica debe ser cableada/local y fail-safe; jamás depender de radio.

## Verificación CI (commit 33d912670892)

- [CI general WPT PASS](https://github.com/Valdi320/Valdo/actions/runs/41335129954) y [CI de PR PASS](https://github.com/Valdi320/Valdo/actions/runs/41335125190): los 15 tests nuevos y las regresiones del workflow terminan correctamente.
- [JSON reproducible generado por CI](https://github.com/Valdi320/Valdo/actions/runs/41335129954/artifacts/13094249814).
- El gate nativo W18 sigue separado: [ERC FAIL](https://github.com/Valdi320/Valdo/actions/runs/41335125189), 3 violaciones históricas del esquema W-IND-15 no cualificado. No se ha desactivado ni convertido en aprobación de hardware.

## Evidencia y reproducibilidad

- Datos transcritos de ST AN4913 Rev. 2, tablas 4–5; la tabla 1 enumera ST25DV64KC. La validación recalcula P_EH = V_EH × I_EH, exige 22 puntos únicos, 11 por modulación y la malla H=0,5…5,5 A/m.
- Código sin dependencias externas: python3 -m unittest -v w_ind_102.test_w_ind_102 y python3 w_ind_102/w_ind_102.py --out w_ind_102/RESULTADO_CI.json.
- La CI general ejecuta ambos y sube el JSON como artefacto. El SHA-256 de la tabla y del modelo queda dentro del resultado.
- Clasificación de toda salida: dato de fabricante / cálculo analítico / hipótesis. **Mediciones propias: cero. Simulaciones electromagnéticas: cero. Aprobación de hardware: falsa.**

## BOM y abastecimiento auxiliar

No se compra ni se selecciona un circuito en este hito. El BOM adjunto separa el chip, la placa de antena y el kit con MCU; no son equivalentes. Diotronic Zaragoza (Av. de Valencia, 5; teléfono publicado 976 353 258) es proveedor auxiliar. La búsqueda pública no encontró una referencia exacta ST25DV64KC o X-NUCLEO-NFC07A1 en su catálogo; stock local, precio final con IVA y MOQ siguen **sin verificar**.

Referencias online consultadas:
- RS X-NUCLEO-NFC07A1: 15,47 € + IVA = **18,56 € IVA incl.**, MOQ 1, 21 unidades mostradas en otro centro de distribución; no es stock de Diotronic.
- DigiKey ST25DV64KC-IE8T3: 1,56 € + IVA = **1,8876 € IVA incl.**, 2.081 unidades indicadas, compra desde 1; chip suelto, no placa/antena.
- TME ST25DV64KC-DISCO: **92,10 € IVA incl.**, 1 unidad indicada; kit con MCU/display/USB, no equivalente a la placa tag.
- Mouser muestra referencias ST25DV64KC, pero la base de IVA/envío no quedó confirmada en esta consulta; no se usa para un total.
- El condensador de buffer y el WPT regulado/FOD/corte no se seleccionan: faltan ESR, fuga, límites eléctricos y trazabilidad.

## Auditoría de propietarios/licencias (HEAD observado 2026-11-01)

- mark-belbin/simple-wireless-power — owner mark-belbin, GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0 igual al SHA registrado; PR #1 cerrada. No se copia código/CAD.
- wisp/wisp5-hw — owner wisp, BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda igual al SHA registrado; PR #1 cerrada.
- wisp/wisp5 — owner wisp, BSD-2-Clause, rama por defecto 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2; contra pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b diverge +68/−11; PR #40 abierta pero antigua. No asumir que otra rama es más nueva ni hacer fast-forward.
- espressif/esp-now — owner espressif, Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 igual al SHA registrado; no se copia código.
- openthread/openthread — owner openthread, BSD-3-Clause, main c6872259f4194fb76c7d333bda209343e8c88e71, +21 commits frente al pin; PR #13800 y #13821 integradas el 2026-10-31. No se copia código.
- OOMWOO oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df (29-10-2026); PR #79 cleaning-jobs abierta y desbloqueada, sin cambios desde W. Adaptación propia sigue aislada en VALDO_OOMWOO, sin instalar WPT.
- VALDO: PR propia #9, rama w/independent-sensor-wpt-link-20261028, head previo da8660e32d9322baa2b8ac6abd65ab3b74109074; se actualiza solo ese ámbito. El checkout compartido local con cambios ajenos no se toca.

## Límites y siguiente puerta

No hay prueba física de V_EH, lector, antena 54 mm, campo en carcasa, offset, eficiencia, FOD, EMI, temperatura, ESR, fuga, buffer ni corte. No se conecta batería/BMS, dock, motor o bomba; no se compra, imprime, suelda ni energiza nada. Próxima puerta solo tras procedimiento de seguridad y autorización: medir H, V_EH/I_EH, energía de entrada del lector, arranque en frío, caída de tensión, pérdida/recuperación RF y temperatura con carga resistiva aislada.
