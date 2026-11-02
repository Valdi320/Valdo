# W-IND-73 — Auditoría verificable de capacitores del transmisor ajeno (31/10/2026)

**Entrega digital y documental; no se ha seleccionado, construido, energizado ni autorizado transmisor, cargador, batería o BMS.** Robot NUEVO, independiente de Xiaomi; sector W solamente.

## Hallazgo de retorno alto
El [netlist WPT_TX.net](https://github.com/mark-belbin/simple-wireless-power/blob/7c7858c0dd7040801b6f191df1396115560218f0/hardware/WPT_TX/WPT_TX.net) de Mark Belbin contiene **37 condensadores**, cuatro de los cuales, C35–C38 = **330 µF cada uno**, están conectados entre /HD y GND. La [BOM histórica WPT_TX_bom_001.csv](https://github.com/mark-belbin/simple-wireless-power/blob/7c7858c0dd7040801b6f191df1396115560218f0/hardware/WPT_TX/WPT_TX_bom_001.csv) lista **33 condensadores** y omite exactamente C35–C38. La BOM es anterior al netlist; no se sabe cuál es el montaje real. Esto activa una **puerta de bloqueo de compra/diseño**, no una corrección del autor. El código nuevo identifica la discrepancia, exige ambos hashes Git blob, inventaría redes y falla ante cambios incompatibles.

Los C26–C29 = 100 nF cada uno son el banco resonante en paralelo entre HS_1 y Net-(C26-Pad1), NO condensadores del bus que deban descargarse con R2. Los 4 x 330 µF constituyen **1.320 µF nominales**, si están realmente montados. Aplicando E=0,5·C·V² y solo si todos se cargan a la tensión supuesta, su energía es **0,019965 J a 5,5 V, 0,095040 J a 12 V y 0,380160 J a 24 V**. No es medición; se desconocen tensión real de /HD, tolerancias, ESR, rutas de descarga, energía magnética, corrientes inversas y comportamiento tras fallos. El circuito W21/W72 propio a 5 V no es el sistema de 24 V de este autor.

El autor [documentó](https://github.com/mark-belbin/simple-wireless-power/tree/7c7858c0dd7040801b6f191df1396115560218f0) 81,3 % a 100 W y separación 1–2 mm, además de condensadores por encima de 70 °C y fallos a corrientes elevadas; son datos **del autor y de su prototipo**, no rendimientos propios. Su PWM sin realimentación RX–TX no suple regulación, FOD, protección térmica ni apagado independiente.

## Reproducibilidad y límites
**Fuente del creador, GPL-3.0**; lectura pública fijada a su commit 7c7858c0dd7040801b6f191df1396115560218f0. Hash netlist SHA Git blob d4ef7e2c2c9588abcc2f28c6a775715108f2e523; hash BOM 04f274dfa46810d655ae2d9783cb96ad1f17bc27. No se incluye su código, CAD ni copia de datos de terceros, ni se modifica su repositorio. El código y las pruebas son autoría propia.

Ejecutar en esta carpeta:
- python3 -m unittest -v test_w73.py (19 pruebas adversariales **sintéticas/offline**).
- python3 w73_source_inventory.py --fetch-pinned --out audit.json (consulta pública de GitHub, exige Internet).
- También admite --netlist WPT_TX.net --bom WPT_TX_bom_001.csv --out audit.json, **solo con bytes originales que superen ambos hashes**.

La CI dedicada repite pruebas, verifica hashes/factores y publica JSON con hardware_approved=false y measurement_performed=false. No se asegura ninguna prueba real ni aceptación de seguridad. Fallos históricos ERC eléctrico W18 y CI general anteriores siguen siendo bloqueos separados.

## Matriz de decisión (problemas separados)
| Problema | Decisión | Condiciones medibles antes de continuar |
|---|---|---|
| Dock de carga | No adoptar diseño autor 24 V/100 W; ningún BMS/cargador seleccionado | Caracterizar carga, alimentación segura, FOD, humedad, temperatura, offset, EMI y corte físico autónomo; no conectar litio |
| Potencia a módulo sensor | Priorizar evaluar un par WPT **regulado y protegido**, frente a resonancia simple no regulada | Empezar por carga resistiva aislada: V/I entrada-salida, eficiencia, pérdidas, offset, desconexión y protección térmica |
| Inventario de energía | **STOP**: 2021 netlist y 2020 BOM no coinciden; C35–C38 ausentes | Confirmar as-built, condensadores tras cada corte, tensión, energía residual, rutas inversas y descarga independiente |
| Datos | ESP-NOW vs OpenThread, ninguna transporta energía | ACK aplicativo, CRC, secuencia, timeout, cifrado y recuperación, medición real; parada crítica por circuito propio |
| WISP | Solo micro-sensores RFID de potencia mínima | Comprobar continuidad, lector, coste y necesidades del sensor; nunca motores/bombas |
| Motores/bombas | Sin WPT de serie | Exigir picos/consumo reales y retorno medido |

## Revisión de los cuatro autores y ramas, fecha 31/10/2026
Comparación HEAD contra el inventario del 28/10:
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power): master sigue en 7c7858c; última actividad del creador junio de 2021. Licencia GPL-3.0.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw): master sin cambios desde 08332bc; historial 2017. BSD-2-Clause.
- [wisp/wisp5](https://github.com/wisp/wisp5): master d978a697 sin cambios; rama *640kHz* identificada por separado como 604eee2dffaeba3a270de61cf3dae887a33309c2, commit 25/04/2022 (otras ramas no permiten suponer orden). BSD-2-Clause.
- [espressif/esp-now](https://github.com/espressif/esp-now): master c3b5f9 sin cambios desde 10/09/2026; ajustes de compatibilidad con IDF v6 y consola. Apache-2.0.
- [openthread/openthread](https://github.com/openthread/openthread): main avanzado de 7009584 a b6d0f06db304055f5866ff6e3c67370b54c81b15 el 31/10, PR #13823/#13790/#13666; no justifica cambiar arquitectura RF. BSD-3-Clause.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo): main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, 29/10, cambio bot de gráfico; #78 fusionada 27/10. No modificar OOMWOO, PR #79, geometría del compañero ni clones upstream.

## BOM y abastecimiento
[BOM_W_IND_73.csv](BOM_W_IND_73.csv) distingue componentes **referenciados por el autor** de piezas elegidas. No se ha comprado nada (0 €). Diotronic Zaragoza auxiliar, sin precios IVA, existencias ni mínimos locales confirmados; la referencia comparativa Panasonic EEEFK1V331P de TME fue solo un anuncio orientativo de 0,96 €/unidad IVA incluido en una consulta histórica, **sin compatibilidad con la huella, ESR ni rizado de C35–C38 confirmada ni stock actual certificado**. Los elementos de seguridad requieren fabricante/trazabilidad y verificación documental especializada. No cambiar diseño por catálogo.

**Siguiente paso:** conciliar netlist, esquema, PCB y BOM del candidato, sin adoptar esta plataforma de alta potencia; inventariar todos los almacenamientos en un **par WPT de bajo consumo** realmente documentado y preparar protocolo de banco con alimentación aislada/carga ficticia tras revisión y autorización. Ninguna prueba física ejecutada.
