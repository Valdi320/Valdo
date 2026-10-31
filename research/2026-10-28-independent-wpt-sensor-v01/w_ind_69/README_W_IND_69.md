# W-IND-69 — Descarga de nodos múltiples y fallo abierto del bleeder (31/10/2026)

**Ámbito W, código original; solo un modelo eléctrico hipotético, sin circuito ni pruebas físicas.** Robot abierto completamente nuevo: NO electrónica, batería, firmware ni estación Xiaomi. No cambios a OOMWOO o colaboradores; W18 con ERC FAIL permanece intacto. La ausencia de radio o de 5 V no prueba la ausencia de energía en condensadores situados después de los cortes.

## Mejora material respecto a W68

W68 solo evalúa un condensador con resistencia permanente ideal. Ahora se evalúa una **envolvente superior** de hasta 32 nodos aislados declarados, cada uno con C máxima, V inicial máxima y resistencia máxima de descarga. Se suman energías: E_upper(t) = suma de 0.5 Cmax_i [Vmax_i exp(-t/(Rmax_i Cmax_i))]^2. Un bleeder abierto en fallo simple deja V_upper(t)=Vmax indefinidamente. La rutina impide que una descarga rápida de TX oculte otro condensador lento, y nunca emite una autorización eléctrica. Valores imposibles, NaN, booleanos donde debe haber números, nodos repetidos o topología desconocida se rechazan o devuelven estado indeterminado.

**Contraejemplos, todos SINTÉTICOS a 5 V:**

| Caso ficticio | Salida analítica | Consecuencia |
|---|---|---|
| TX 100 µF, 1 kΩ, 500 ms | 0,03369 V; 0,05675 µJ | Por debajo de pantallas hipotéticas, NO implica seguro |
| Mismo TX con resistor abierto, tras 1 h | 5 V; 1,25 mJ | Detecta fallo oculto por descarga ideal |
| TX anterior + AUX 1 mF, 1 MΩ, 500 ms | AUX ≈4,9975 V; energía global ≈12,49 mJ | Detecta nodo con descarga lenta |
| Fuente/desacoplamiento/aislamiento sin prueba | No estima voltajes | Bloqueado, no inventa continuidad o seguridad |

Los umbrales 0,5 V/1 mJ son pantallas hipotéticas, no límites seguros, regulatorios ni valores de fabricante. Los indicadores source_cut_verified, backfeed_excluded y nodes_independent_verified expresan condiciones asumidas para la simulación: **NO están verificadas en hardware**. Sin estas premisas se niega a calcular un límite superior creíble. No trata acoplos, inductancias, resonancia, fallos concurrentes, calentamiento de resistencias, aislamiento eléctrico, tolerancia térmica, daño por descarga ni fusibles. En particular, en un circuito real varios condensadores en paralelo se modelarían como un único nodo equivalente, no sumados arbitrariamente como aislados.

## Reproducir

Desde research/2026-10-28-independent-wpt-sensor-v01 con Python 3.12 sin dependencias externas:

    python3 -m unittest discover -s w_ind_69 -p 'test_w69.py' -v
    python3 -m w_ind_69.w69_demo > W69_EVIDENCE_REPRODUCED.json

El workflow W69 ejecuta estas 15 pruebas más regresión de W68 y archiva el resultado reproducido. Tests Python no equivalen a KiCad ERC, EMI o pruebas de prototipo. No se ha instalado ni energizado nada.

## Matriz técnica y próximo bloqueo

| Sistema | Decisión y pendiente |
|---|---|
| Estación de carga | Solo conceptual. Litio, BMS, dock y electrónica OEM NO usados. Protecciones autónomas, FOD, temperatura, agua, EMI y alineación sin demostrar |
| Potencia de primer módulo | Piloto hipotético 5 V, 0,4 W y picos 1,5 W; modelo de descarga no demuestra eficiencia WPT ni cables eliminados. No usar para motores/bombas |
| Datos | ESP-NOW frente a OpenThread aparte, sin energía transmitida por RF; ACK aplicativo, CRC, secuencia, caducidad, autenticidad y privacidad necesarias; ninguna parada crítica depende de radio |
| Microsensores | WISP5 solo si consumo y lector RFID justifican electrónica adicional |

**Próxima intervención:** identificar capacidades y bleeders posteriores a ambos cortes desde esquema propio, y documentar C/V/R, rutas inversas, retorno y corriente independiente, sin enmascarar 3 errores KiCad ERC existentes (dos power_pin_not_driven, uno label_dangling). Cambios eléctricos requieren revisión física y autorización de banco aislado sin baterías. Un corte eléctrico independiente no queda sustituido por estos cálculos.

## Fuentes, licencias, propietarios y límites

- Trabajo propio W anterior: https://github.com/Valdi320/Valdo/commit/6c3356b37f81f29cf3ecc9e9a7245281bb516bf3 . W69 es código original, no contiene código externo. No editar trabajos C/Codex A01–A04.
- Revisión de autores frente a SHAs registrados el 28/10 (comprobada el 31/10): https://github.com/mark-belbin/simple-wireless-power GPL-3.0 master 7c7858c0 sin cambio; https://github.com/wisp/wisp5-hw BSD-2 master 08332bc3 sin cambio; https://github.com/wisp/wisp5 BSD-2 rama **640kHz** 604eee2d, divergente 68 ahead/11 behind de pin d978a697; https://github.com/espressif/esp-now Apache-2 master c3b5f9be sin cambio; https://github.com/openthread/openthread BSD-3 main b6d0f06d, 18 commits ahead de 7009584d.
- Revisadas PRs recientes upstream ESP-NOW #151/#153, OpenThread #13821/#13822 y WISP #38/#40, y autores oficiales OOMWOO https://github.com/makerspet/oomwoo main f01a1b29, firmware ce05f266 y PCB 87aa7d38 (J1, IMU y BOM). Nada editado allí.
- Física del condensador ideal: V(t)=V0 exp(-t/RC), E=1/2 C V²; sin tolerancias parametrizadas de pieza elegida, sin ensayos ni certificado. Referencia TI TPS22918: https://www.ti.com/product/TPS22918 . Ningún esquema de terceros copiado.
- BOM adjunta separa Diotronic auxiliar (pasivos/prototipado) de TME/Mouser/DigiKey/fabricante (críticos); precios finales IVA, mínimos y existencias de Diotronic Zaragoza no verificados, quedan pendientes. Incremento hardware de W69: **cero unidades**, no cero coste del robot.

**Estado:** solo 15 pruebas digitales W69 y regresión W68 sujeto a CI; cero ensayos físicos/compras/placas/energización/litio/BMS/estación. Eficiencia, FOD, EMI y mantenibilidad todavía sin mediciones; W18 ERC bloqueado.
