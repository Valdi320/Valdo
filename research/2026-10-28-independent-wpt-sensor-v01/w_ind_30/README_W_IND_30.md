# W-IND-30 — Auditoría de caminos de corriente, fallos y rearme local (SOLO DIGITAL)

**29/10/2026 · VALDO ámbito W · robot independiente, abierto, reparable e imprimible.** No hay trasplante Xiaomi OEM, compras, PCB, ensayos de tensión ni estación/batería/BMS conectados.

## Problema y hito verificable

El esquema W-IND-29 es únicamente un monitor RX INA301A1 con 0,1 ohm Kelvin, umbral nominal hipotético 346,4 mA y ALERT sin desconexión. W-IND-23 demostró que los dos TPS22918 NO bloquean necesariamente corriente inversa al estar apagados. Este hito añade un **grafo original de conductividad direccional** que encuentra las rutas explícitas SOURCE→LOAD y LOAD→SOURCE. Se simulan dos cortes normalmente apagados, idealmente con bloqueo inverso (RCB), y se inyectan cortos directos, dos soldaduras, pin ENABLE pegado, caídas de alimentación, sobrecorriente, calor y FOD. Un autómata lógico exige un rearme local después de desconectarse y nunca permite que una trama RF rearme una parada.

Resultados reproducibles: **15 pruebas Python y 512 combinaciones** de nueve indicadores binarios. **375/512** producen ruta peligrosa bajo la orden de apagado, debido a fallos de bypass o combinación de actuadores; esto es un número de escenarios sintéticos NO una probabilidad ni medida. En el subconjunto ideal de máximo un fallo de actuador sin bypass hubo **0 casos de camino delantero indebidamente cerrado** cuando se requiere parada. La herramienta exhibe caminos concretos de fallo. El script nunca devuelve aprobación para energizar.

**Este resultado NO crea dos interruptores físicos:** 'rcb' es un contrato de arco ideal, no equivale a un eFuse real; el elemento 'soldado' se modela como un hilo bidireccional conservador. Se ignoran corrientes de fuga, tensión, FET body diodes exactos, retardo, fallos de alimentación de los comparadores, errores de control de los dos canales, caída sobre shunt, inductancias, FOD real, humedad, temperatura, EMI, fallos comunes, geometría 3D y fabricación. La lógica de rearme es un requisito por implementar en hardware, NO seguridad por software. **Energización bloqueada incluso si todos los tests pasan.**

## Reproducción (Python 3.10+ sin librerías)

    python3 -m unittest -v w30_cutset
    python3 w30_cutset.py --json > evidence.json

Workflow w-ind-30-cutset.yml ejecuta las 15 pruebas y archiva el JSON de 512 casos. Evidencia creada digitalmente por nuestro sector W; no se ha copiado código de creadores externos.

## Comparativa y decisión

| Objeto | Decisión técnica | Evidencia y bloqueo |
|---|---|---|
| Dos TPS22918 en serie sin RCB | No adecuados para aislar en ambos sentidos | Dos rutas inversas ideales pueden atravesar en apagado; no se modelan caídas reales de diodo |
| Dos cortes independientes RCB normalmente OFF | Arquitectura candidata por demostrar | Un soldado aislado aún deja otro corte; dos soldaduras o puente directo son inseguras; falta circuito KiCad, alimentación de seguridad y FMEA |
| TI TPS25947 con FETs opuestos | Candidato NO elegido | TI documenta bloqueo inverso; corriente mínima ajustable ~500 mA no detecta un fallo RX de 400 mA; no asumir que un eFuse sustituye al INA301 ni que RCB permanece ante soldadura |
| INA301A1 + shunt Kelvin | Monitor previo, NO parada | Umbral RX 346,4 mA solo hipotético; hace falta salida de corte, PG/undervoltage y dos rutas físicamente separadas; no copiar umbral RX a TX |
| WPT sencillo vs regulado | Medir antes de seleccionar | Piloto hipotético 5 V/0,4 W promedio, 1,5 W pico: comparar eficiencia/gap/desalineación, metal/FOD, térmica, EMI, consumo en reposo y sustitución frente a conector protegido |
| Dock de carga | Totalmente separado y desconectado | Carga de litio y BMS necesitan autorización y seguridad independientes |
| Datos ESP-NOW vs OpenThread | Alternativas, nunca dos radios por defecto | ACK de aplicación, CRC, secuencia, anti-replay, autenticación/cifrado, timeout y recuperación; radio NO alimenta ni autoriza parada/rearme |
| WISP5 RFID | Posponer para microsensores intermitentes | No demuestra alimentación continua de 1,5 W |
| Motores y bombas WPT | Rechazo por defecto | Sin curva de potencia, coste, calor y pérdidas |

## Revisión de propietarios, HEAD y cambios públicos, 29/10/2026

| Repositorio del creador, licencia | Rama HEAD consultada | SHA fijado el 28/10 y cambios |
|---|---|---|
| mark-belbin/simple-wireless-power GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | Igual; PR #1 fusionada en 2021, no copiar su fuente GPL |
| wisp/wisp5-hw BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | Igual; PR #1 del autor de 2015 |
| wisp/wisp5 BSD-2-Clause | **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2 | vs d978a6978ad23ccd6c44dd55430973b04a3d4a9b **divergió +68/-11**; NO hacer fast-forward; PR #40 abierta |
| espressif/esp-now Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | Igual; PR #153 cerrada febrero 2026 |
| openthread/openthread BSD-3-Clause | main e577777c308f6c87e5da3056239231a8fc147cb2 | vs 7009584dadc20cf20c20a6062f357dd572ba6885 **+14/-0**; cambios cipher-suite #13810, API, radio, CLI; release v2026.10.0; PR #13819 abierta |

OOMWOO oficial makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df (29/10): último cambio star-history, no relacionado. **No se editan** autores, upstream, adaptación OOMWOO, mecánica C, PR #79 cleaning-jobs ni aportación separada Codex de parada térmica cruzada A01-A04.

Documentos maestros efectivamente leídos: decisión 00 del 28/10, alternativas 19, auditoría D22 y contrato, coordinación W/C y LEEME_PRIMERO + WPT_DATOS_V01. Clasificar siempre como simulación propia, nunca ensayo eléctrico.

Fuentes primarias: https://www.ti.com/product/TPS25947 (bloqueo inverso y límite mínimo), https://www.ti.com/product/INA301 ; https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5/tree/640kHz ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo .

BOM con columna Diotronic auxiliar/alternativa/IVA/MOQ/stock en BOM_W_IND_30.csv. **Todo precio y stock local pendiente**; no confundir catálogo con disponibilidad de Zaragoza, no sustituir piezas críticas sin documentación. Matriz de decisiones en MATRIZ_W_IND_30.csv.

**Siguiente hito:** KiCad de dos cortes con fuente de seguridad normalmente OFF e inhibición independiente PG/INA/FOD/termal, variantes exactas traceables y conexiones contra backfeed, revisión ERC/netlist y SPICE de fabricante si existe. No hardware ni litio sin revisión/permiso.
