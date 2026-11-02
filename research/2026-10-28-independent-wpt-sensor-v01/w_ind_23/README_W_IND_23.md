# W-IND-23 — Auditoría de diodos internos en los dos cortes (29/10/2026)

**Seguridad: revisión DIGITAL. BLOQUEADO PARA ALIMENTAR, FABRICAR O CARGAR.**

## Mejora material
El esquema W-IND-21 tiene dos \`TPS22918DBVR\` en serie. TI, [TPS22918 Rev. C §9.2.2.2](https://www.ti.com/product/TPS22918), documenta el diodo interno entre salida y entrada: si \`VOUT\` queda suficientemente por encima de \`VIN\`, puede conducir en sentido inverso. Aunque ambos pines ON estén a nivel bajo, existe una **ruta condicional TX_5V_CUT → U2 (pin6→1) → MID → U1 (pin6→1) → VIN_5V** por esos diodos internos. ERC-zero y el verificador de netlist W-IND-22 verifican conexiones externas; **no implican protección contra corriente inversa**.

\`reverse_path_gate.py\` exige los pines, redes, componentes y valores exactos del **XML generado por KiCad real** para W-IND-21. Modela únicamente la dirección de los diodos documentados y entrega \`REVIEW_BLOCKED_TPS22918_REVERSE_DIODE_PATH\`, \`power_on_allowed=false\`, \`hardware_approved=false\`. La CLI ordinaria devuelve exit 2 al detectar esta barrera. \`--expect-known-blocker\` permite a CI pasar exclusivamente al **demostrar que la barrera persiste**, no porque el circuito sea apto. Pruebas: **17 sintéticas PASS localmente** por \`python3 -m unittest -v test_reverse_path_gate\`; CI específica exporta XML **nativo KiCad 9.0.2** y archiva SHA-256 e informe. Mantener la variante histórica W-IND-15 y su ERC rojo sin ocultar resultados.

**Alcance limitado:** ninguna corriente, caída de diodos, energía en condensadores, temperatura, FOD o fallo real se han medido; el esquema no incorpora una fuente de retroalimentación física ni un condensador elegido. La ruta solo transportaría corriente si TX tiene energía y la diferencia de potencial basta para polarizar ambos diodos. No es un cálculo SPICE ni diseño de protección construido.

## Matriz de decisión
| Alternativa | Riesgo/consecuencia | Coste/reparación | Decisión |
|---|---|---|---|
| Afirmar que dos TPS22918 OFF cortan en ambos sentidos | La hoja del fabricante contradice el bloqueo inverso | Cero coste inmediato, alta falsa confianza | RECHAZAR |
| Preservar el esquema como dibujo no cualificado y automatizar el bloqueo | Detecta riesgo sin modificar trabajo anterior | 0 piezas nuevas y software auditable | **APLICADO** |
| Sustituir por ruta con MOSFET enfrentados y dos permisos locales autónomos | SOA/fallos comunes, polarización y EMI por cualificar | BOM, pérdidas y mantenibilidad pendientes | ESTUDIAR |
| Conmutador de carga con protección inversa documentada + FOD, temperatura y sobrecorriente autónomos | No garantiza solo por etiqueta de marketing | Datasheet, stock y pruebas independientes exigibles | ESTUDIAR |

## Separación de sistemas
1. **Dock y batería/BMS:** arquitectura nueva, desconectada y sin carga real. 2. **Potencia modular:** candidato solamente de bajo consumo, supuestos 5 V, 0,4 W promedio y 1,5 W pico, aún sin bobinas ni FOD físicos. Sin inductivo por defecto para motores ni bombas. 3. **Datos:** ESP-NOW vs OpenThread aún sin hardware; ACK de aplicación, CRC, secuencia, timeout, privacidad y recuperación, jamás parada crítica por RF. WISP se reserva a microsensores RFID si compensa un lector.

## Propietarios, licencias y revisión HEAD 29/10/2026
| Propietario y repositorio | Licencia | HEAD del autor vs SHA fijado 28/10 | Relevancia |
|---|---|---|---|
| mark-belbin/simple-wireless-power \`master\` | GPL-3.0 | \`7c7858c0dd7040801b6f191df1396115560218f0\` igual pin | Fuente conceptual, sin copiar circuitos |
| wisp/wisp5-hw \`master\` | BSD-2-Clause | \`08332bc398aa3350d351ef2aaac163f8007cffda\` igual pin | Sensores pasivos, no potencia continua |
| wisp/wisp5 \`640kHz\` | BSD-2-Clause | \`604eee2dffaeba3a270de61cf3dae887a33309c2\` frente a \`d978a6978ad23ccd6c44dd55430973b04a3d4a9b\`; **68 ahead/11 behind** | No autopromover rama ni mezclar |
| espressif/esp-now \`master\` | Apache-2.0 | \`c3b5f9be245f1a80db9cb938600566aa6a8dd1e5\` igual pin | Radio, no alimentación |
| openthread/openthread \`main\` | BSD-3-Clause | \`51aa078ee4fe1ad803bc83ca7b372e7ab62120f3\` = **9 ahead/0 behind** de \`7009584dadc20cf20c20a6062f357dd572ba6885\` | Cambios MAC/CSL/heap/radio, no se copió código |

Otros: makerspet/oomwoo oficial \`main=f01a1b295f462da5ab8d5f021a3f741cbd2b47df\`; no tocar PR #79 cleaning-jobs, adaptación C, clones oficiales ni Xiaomi OEM. Esta entrega es de \`Valdi320/Valdo\` PR #9 propia. Autoría del script original propia; no se copió código GPL/BSD/Apache.

## BOM y evidencia
Ver \`BOM_W_IND_23.csv\`: **cero nuevos componentes, cero compras**. Diotronic como proveedor auxiliar, precios finales IVA, MOQ, inventario tienda Zaragoza y alternativas TME/Mouser/DigiKey **pendientes**, no inventados. Los futuros componentes anti-retorno, FOD, sobrecorriente y térmicos exigirán documentación/trazabilidad. Se usa solo CI/software: cero PCB, ensayo físico, batería, estación, soldadura o impresiones. La batería de litio permanece desconectada.

**Siguiente trabajo:** comparar fichas técnicas de topologías de **aislamiento bidireccional real** con cortes autónomos, FOD, temperatura y sobrecorriente, y generar esquema KiCad / simulación SPICE antes de plantear un banco aislado autorizado.
