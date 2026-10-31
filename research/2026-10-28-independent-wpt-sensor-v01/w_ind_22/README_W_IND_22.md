# W-IND-22 — Auditoría independiente de topología mediante netlist KiCad nativa

**29/10/2026 · Proyecto VALDO del robot NUEVO abierto. Solo diseño digital, NO apto para fabricar ni energizar.**

## Mejora y justificación
La variante W-IND-21 declara una fuente de banco externa de 5 V y obtuvo ERC KiCad 9.0.2 sin avisos. Sin embargo, ERC comprueba reglas eléctricas, no la intención de seguridad: un conductor que puentease VIN y TX podría eludir simultáneamente los dos interruptores de corte aunque ERC fuera verde. El auditor geométrico W-IND-16 comprueba elementos conocidos, pero no sustituye el netlist extraído del motor EDA.

Añadimos un guardián propio que lee la exportación **real** XML de KiCad 9.0.2 y exige un mapa exacto, revisado, de pares referencia.pin en redes; cualquier componente, red o pin nuevo obliga a revisión, sin aceptar automáticamente modificaciones porque ERC permita conectarlas. El workflow independiente exporta el netlist del esquema **sin modificar** W-IND-21, ejecuta el análisis y almacena exportación original y JSON de evidencia. Conserva intactos el esquema histórico W-IND-15 y su comprobación ERC deliberadamente roja.

Contrato del guardián:
- VIN_5V: J1.1, U1.1.
- MID: U1.6, U2.1, R1.1.
- TX_5V_CUT: U2.6, R2.1.
- EN_A: U1.3, R3.1.
- EN_B: U2.3, R4.1.
- GND: J1.2, U1.2, U2.2, R1.2, R2.2, R3.2, R4.2.

El software compara también el valor de J1 como símbolo de **declaración** externa, no pieza de BOM, dos TPS22918 U1/U2 y resistencias R1=22k, R2=1k, R3/R4=100k; detecta cortocircuitos nominales, nets fusionadas o extras, pines duplicados, valores alterados y borrados. **Un PASS no autoriza alimentación:** el JSON mantiene siempre physical_approval=false, power_on_allowed=false, battery_charging_allowed=false.

## Evidencia y reproducción
- Fuente original: [w_ind_22_netlist_guard.py](https://github.com/Valdi320/Valdo/blob/w/independent-sensor-wpt-link-20261028/research/2026-10-28-independent-wpt-sensor-v01/w_ind_22/w_ind_22_netlist_guard.py).
- 29 regresiones sintéticas: [test_w_ind_22_netlist_guard.py](https://github.com/Valdi320/Valdo/blob/w/independent-sensor-wpt-link-20261028/research/2026-10-28-independent-wpt-sensor-v01/w_ind_22/test_w_ind_22_netlist_guard.py). Ejecutadas con Python estándar de forma independiente: **29/29 PASS local**; el XML sintético NO es una exportación nativa de KiCad, ni prueba física.
- [Workflow KiCad nativo](https://github.com/Valdi320/Valdo/blob/w/independent-sensor-wpt-link-20261028/.github/workflows/w-ind-22-native-netlist.yml) usa la imagen kicad/kicad:9.0.2, registra temporalmente la biblioteca VALDO, exporta el esquema W-IND-21 mediante 'kicad-cli sch export netlist --format kicadxml', compara sin modificar orígenes y guarda artefactos también ante fallo. **La CI nativa solamente puede darse por validada tras observar su ejecución correspondiente.**

Reproducir software: desde 'research/2026-10-28-independent-wpt-sensor-v01/w_ind_22', ejecutar 'python3 -m unittest -v test_w_ind_22_netlist_guard'. Para exportación real, utilizar KiCad 9.0.2 y el registro de biblioteca y comandos exactos en el workflow; inspeccionar 'native_out/w21.native.xml' y 'native_out/attestation.json'.

## Matriz de decisiones
| Alternativa | Beneficio | Riesgo o falta | Decisión |
| --- | --- | --- | --- |
| ERC cero únicamente | Verificación formal básica de pines | Puentes con tipos eléctricos válidos pueden ser invisibles | Insuficiente |
| Solo geometría W-IND-16 | Posiciones, conectividad declarada | No valida exportación nativa tras cambios | Complementario |
| Auditoría exacta del netlist real + rechazo por defecto | Detecta vías y conexiones inesperadas en este candidato | No demuestra topología PCB física ni función interna de switches | **Implementado como puerta digital** |
| Autorizar fabricación tras PASS | Ningún beneficio defendible | Carece de protección autónoma y ensayos | Rechazado |

## Separación de arquitectura y límites
1. Carga de estación: no hay cargador, BMS, batería ni estación aprobados ni conectados; nada OEM Xiaomi.
2. Potencia sin contacto entre módulos: primer piloto de sensor **hipotético** 5 V, 0,4 W media y 1,5 W pico. No hay fuente real, bobinas, consumos medidos, eficiencia, desalineación, FOD/metal, temperaturas, protección inversa, EMI ni ambiente húmedo validados. No introducir WPT en bombas o motores.
3. Datos RF: ESP-NOW u OpenThread son alternativas y **no transportan potencia**; requieren ACK de aplicación, CRC, secuencias, timeout, privacidad, credenciales y recuperación antes de uso. Prohibido usar radio para parada crítica. WISP5 solo micropotencia RFID.

El modelo no cubre cortocircuitos de PCB, soldadura, fugas, MOSFET pegado, doble fallo, compatibilidad de encapsulado, disyunción de dominios EN, temperatura, secado ni límites de fuente. **No se ha hecho ninguna prueba física ni de litio.** El siguiente hito deberá especificar circuitería independiente de corte por temperatura/FOD, antirretorno y sobrecorriente; revisar datasheets/ERC/SPICE y ensayar más adelante en banco aislado con autorización.

## Proyectos de terceros y revisión de HEAD (29/10/2026)
Se leyeron antes de modificar: decisión NO TRASPLANTE 28/10, 19-alternativas..., D22, acuerdo de coordinación W/C, VALDO_OOMWOO LEEME_PRIMERO y contrato WPT_DATOS_V01. GitHub comparado con los SHAs guardados; no se copió código ni CAD externo:
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), autor Mark Belbin, GPL-3.0: master 7c7858c0dd7040801b6f191df1396115560218f0, idéntico al pin. Sus datos experimentales no validan nuestro circuito.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), propietarios WISP, BSD-2-Clause: master 08332bc398aa3350d351ef2aaac163f8007cffda, idéntico.
- [wisp/wisp5](https://github.com/wisp/wisp5), propietarios WISP, BSD-2-Clause: rama por defecto **640kHz** HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 frente a d978a6978ad23ccd6c44dd55430973b04a3d4a9b, **divergido +68/-11**, no fast-forward.
- [espressif/esp-now](https://github.com/espressif/esp-now), propietario Espressif, Apache-2.0: master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5, idéntico, sin PR abiertas.
- [openthread/openthread](https://github.com/openthread/openthread), OpenThread, BSD-3-Clause: main 51aa078ee4fe1ad803bc83ca7b372e7ab62120f3, +9/0 contra 7009584dadc20cf20c20a6062f357dd572ba6885; cambios radio/IPv6 en curso.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo) main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, igual última revisión. La adaptación y los clones upstream son de lectura; trabajo apoyo Codex A67/A68, áreas mecánicas C, otra automatización OOMWOO y PR #79 cleaning-jobs no se han modificado.
- [Referencia de formato](https://docs.kicad.org/9.0/en/cli/cli.html): documentación oficial KiCad CLI, exportación de netlists XML.

## BOM/Diotronic
[BOM_W_IND_22.csv](https://github.com/Valdi320/Valdo/blob/w/independent-sensor-wpt-link-20261028/research/2026-10-28-independent-wpt-sensor-v01/w_ind_22/BOM_W_IND_22.csv): **0 componentes nuevos, 0 € gastados**. Diotronic auxiliar con referencia, IVA, stock local Zaragoza, mínimos y comparación TME/Mouser/DigiKey **pendientes**; para FOD y seguridad exigir fabricante, características y trazabilidad. Sin compras ni instalaciones, sin PCB, sin motores/baterías ni estación energizados.

## Corrección de formato de exportación nativa (29/10/2026)

La primera CI nativa del [commit 8608cc9](https://github.com/Valdi320/Valdo/commit/8608cc9f59f35bb973af9a87c594ed88b631ac4d) **FALLÓ correctamente**, sin bloquear la exportación de KiCad. [Run push #40852849923](https://github.com/Valdi320/Valdo/actions/runs/40852849923) aporta [XML original y reporte de discrepancia](https://github.com/Valdi320/Valdo/actions/runs/40852849923/artifacts/12887648596). Hallazgo: KiCad 9.0.2 exporta nombres de redes de etiqueta local como '/VIN_5V', '/MID', '/EN_A', etc., y crea explícitamente cuatro redes singleton 'unconnected-(U1-CT-Pad4)', 'unconnected-(U1-QOD-Pad5)', 'unconnected-(U2-CT-Pad4)', 'unconnected-(U2-QOD-Pad5)'. El guardián original esperaba los seis nombres sin '/' e ignoraba esas cuatro redes. **No era fallo eléctrico demostrado**: era una divergencia de serialización que la nueva puerta detectó al confrontar por primera vez un netlist real.

Se corrige el contrato **estrictamente** para seis etiquetas locales con barra inicial y las cuatro redes de no-conexión *exactas* con pin asociado, sin ignorar por comodín redes desconocidas ni nuevos componentes. Se incorporan cuatro pruebas adicionales de mutación de las redes NC, completando **29/29 pruebas sintéticas locales PASS**. Mantener bloqueo ante cualquier otro nombre de red, pin, conexión o netlist inválido. El resultado de la nueva CI se anotará sólo cuando sea observable para el commit corregido. Esta revisión sigue siendo software; ningún circuito está certificado ni aprobado.
