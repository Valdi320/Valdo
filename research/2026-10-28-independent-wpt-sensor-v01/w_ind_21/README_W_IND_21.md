# W-IND-21 — Fuente externa 5 V declarada explícitamente en KiCad (2026-10-29)
## Resultado propuesto y verificación reproducible
La referencia de W-IND-15 carece de fuente eléctrica explícita, por lo que el ERC real de KiCad 9.0.2 señaló 3 infracciones: VIN_5V etiquetada sin otro extremo y dos pines de alimentación sin fuente declarada. Este hito aporta un **esquema CANDIDATO NUEVO, separado del original**, que representa la frontera de una fuente **externa, aislada y regulada de laboratorio de 5 V** con dos salidas lógicas ERC (VIN_5V, GND). Es un **símbolo original de ingeniería de banco**, no una fuente eléctrica construida ni elegida, NO un PWR_FLAG arbitrario ni un conector apto para compra.

- `W_IND_21_TX_BENCH_DECLARED.kicad_sch`: conserva el bloque de dos TPS22918 y cuatro resistencias, incorpora J1 **no-BOM y no-board**; etiquetas positivas y retorno en pines explícitos.
- `VALDO.kicad_sym` y `sym-lib-table`: biblioteca de tres símbolos originales, sin reutilizar una biblioteca del fabricante sin licencia.
- `test_w_ind_21_bench_source.py`: 12 tests contra pinout, etiquetas, alteraciones y regresión. `.github/workflows/w-ind-21-bench-erc.yml`: KiCad CLI 9.0.2 real con JSON y attestation archivadas y check ROJO si encuentra una infracción.
- **Aprobación todavía prohibida** incluso si ERC nuevo informa cero. El antiguo W-IND-15 sigue aislado e intacto, y su check no se ha desactivado. No se modifican contratos originales ni se ocultan errores históricos.

## Matriz de decisión
| Opción | Beneficio | Riesgo | Decisión |
|---|---|---|---|
| Silenciar los 3 errores o añadir PWR_FLAG | ERC verde fácil | Certifica una fuente ficticia | Rechazada |
| Fuente real de banco aislada declarada como **frontera lógica** y no como PCB | Da procedencia a VIN y retorno, permite comprobar conectividad | El símbolo *no demuestra* aislamiento, corriente, polaridad ni seguridad | **Implementada como prototipo digital** |
| Comprometer ya la fuente 5 V física | Facilita banco | Sin cotización, protección, consentimiento, mediciones | Rechazada |
| Construir WPT TX y conectar Li-ion o dock | Ninguno antes de medidas | Riesgo de calor/FOD y batería | Prohibida |

## Requisitos y límites
Aún hipótesis: módulo sensor 5 V, 0,4 W promedio y 1,5 W pico; fuente externa sólo nominal a 5 V. No hay fuente, cableado, protección, bobinas, regulador ni montaje probados; corriente inicial, pérdidas, offset, FOD, sobretemperatura, protección inversa, corte independiente, humectación, EMI y envejecimiento sin evaluar. La parada crítica deberá ser autónoma y local; la radio nunca será permiso de seguridad. Un ERC verde significa solo **consistencia de pines según reglas de KiCad**, nunca fuente cualificada ni circuito aprobado. No energizar ni fabricar.

**Separación**: (1) carga de dock/batería/BMS totalmente desconectados, arquitectura por determinar; (2) piloto de potencia local solo sensor, motores y bombas excluidos; (3) datos RF ESP-NOW u OpenThread con ACK de aplicación, CRC, secuencia, caducidad, privacidad y recuperación, todavía sin hardware. WISP únicamente referencia de microsensores RFID.

## Titularidad y auditoría externa (HEAD observado 29/10/2026)
- Mark Belbin, [simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0: master `7c7858c0dd7040801b6f191df1396115560218f0`, igual que pin de 28/10; no importar el circuito del autor, 100 W/81,3% declarados solo por autor y sin regulación RX↔TX completa.
- WISP5 de wisp, [hardware](https://github.com/wisp/wisp5-hw) y [firmware](https://github.com/wisp/wisp5), BSD-2-Clause: hardware master `08332bc398aa3350d351ef2aaac163f8007cffda` igual pin; firmware default **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` contra pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` diverge 68 ahead/11 behind; no autopromoción de rama, PR #40 abierto desde 2021.
- Espressif, [esp-now](https://github.com/espressif/esp-now), Apache-2.0: master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` igual pin, cero PR abiertas; es datos, **no energía**.
- OpenThread, [openthread](https://github.com/openthread/openthread), BSD-3-Clause: main `51aa078ee4fe1ad803bc83ca7b372e7ab62120f3` contra pin `7009584dadc20cf20c20a6062f357dd572ba6885`: +9/0 commits (filtrado de direcciones, corrección heap/CSL, etc.), PR recientes #13813–#13815; no importar código.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo) main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`: actualización de gráfico [skip ci], ajena al enlace W. VALDO PR #9 W, sin tocar #79 cleaning-jobs ni fuentes originales/CodeX.
- Fuente técnica pinout y ratings [Texas Instruments TPS22918DBVR](https://www.ti.com/product/TPS22918): VIN 1, GND 2, ON 3, CT 4, QOD 5, VOUT 6; 1–5,5 V y 2 A **máximo**, no circuito de sobrecorriente ni FOD.

## BOM / Diotronic
`BOM_W_IND_21.csv` documenta **cero componentes de compra añadidos**, oferta de fuente real/alternativa aún pendiente, precio final con IVA, MOQ y stock local Diotronic NO verificados. Diotronic auxiliar para pasivos; fuentes/protecciones de seguridad deben venir con documentación y trazabilidad. Sin compra, instalación, soldadura, servicio o prueba de Li-ion.

## Próxima puerta
Revisar CI KiCad nativo del nuevo candidato y registrar exactamente ERC PASS/FAIL. Incluso con cero infracciones, diseñar fuentes físicas y rutas de corriente, anti-retorno, FOD/termometría independiente, corte real, EMI y ensayo resistivo **sólo si hay autorización de seguridad**. Conservar W-IND-15 como artefacto histórico sin modificar.

## Evidencia ERC 9.0.2 observada (29/10/2026)
- Candidato W-IND-21, commit [6db468348c9be4871ee23d3a9041b03b1453c8ca](https://github.com/Valdi320/Valdo/commit/6db468348c9be4871ee23d3a9041b03b1453c8ca): **12/12 tests Python PASS**, KiCad CLI nativo **9.0.2**, **ERC 0 errores + 0 avisos**, salida `ERC_ZERO_REPORTED_STILL_DO_NOT_BUILD`; [CI verde](https://github.com/Valdi320/Valdo/actions/runs/40850866344), [JSON y attestación originales](https://github.com/Valdi320/Valdo/actions/runs/40850866344/artifacts/12887350442), [regresión general PASS](https://github.com/Valdi320/Valdo/actions/runs/40850866370).
- **Comparación honesta:** el W-IND-15 original conservado sigue dando **3 errores ERC** (bloqueador [W-IND-18 histórico rojo](https://github.com/Valdi320/Valdo/actions/runs/40850866488)). La nueva variante alcanza cero solo tras **declarar en un símbolo lógico la fuente externa 5 V**; esto NO certifica que exista una fuente aislada físicamente, ni constituye una prueba de corte autónomo. Ambos resultados son correctos y el check histórico no se desactiva.
- Queda bloqueada fabricación, alimentación física, conexión de baterías y carga. FOD, termometría, sobrecorriente, corriente inversa, control independiente, EMC y compatibilidad de bobinas sin evidencia física. Este paquete usa **cero componentes nuevos comprados** y no altera OOMWOO #79 ni las fuentes de autores.
