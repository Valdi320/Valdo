# W-IND-68 — Energía residual DESPUÉS de cortar WPT (31/10/2026)

**Una mejora W propia, digital y reproducible.** El robot es NUEVO, abierto, local, reparable e imprimible; no trasplanta ninguna pieza ni firmware Xiaomi X20 Pro. No se toca OOMWOO ni PR #79, ni clones upstream ni ficheros de C/Codex.

## Defecto material descubierto y corregido en el modelo
En W67, `evaluate(..., supply_present=False)` devuelve `supply_to_tx=False` aunque los dos interruptores estén soldados; esto significa **sin alimentación DC continua hacia TX**, NO necesariamente **TX descargado**. Un condensador físicamente ubicado *después* de los cortes puede almacenar energía aun con fuente y radio retiradas. W68 separa ambos fenómenos, incorpora clasificación explícita de fuente hacia TX, ausencia de prueba de bloqueo de corriente inversa, parámetros de almacenamiento desconocidos y decaimiento RC ideal únicamente cuando todos los supuestos se declaran. No cambia ni maquilla W67 o el ERC eléctrico W18.

Contraejemplo reproducible: **hipótesis**, C=100 µF en nodo TX, V0=5 V, resistencia de descarga 1 kΩ, sin alimentación continua ni realimentación: E(0)=1,25 mJ, V(100 ms)=1,839 V y V(500 ms)=0,03369 V. Un modelo que tratase `supply_present=False` como ausencia instantánea de energía cometería un falso negativo. Los límites de pantalla 0,5 V / 1 mJ son **supuestos de demostración**, NO umbrales seguros, de fabricante o de aprobación.

## Evaluación concreta
- Clasificaciones excluyentes: `FORWARD_SUPPLY_POSSIBLE`, `BACKFEED_NOT_EXCLUDED`, `STORAGE_OR_BLEED_UNKNOWN`, `RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN`, `BELOW_HYPOTHETICAL_SCREEN_NOT_SAFE`.
- Fallo cerrado por entradas mal tipadas, NaN, parámetros desconocidos, cortocircuito doble y falta de evidencia de bloqueo inverso. Los supuestos para evaluar RC son capacitancia única, resistencia de descarga permanente ideal, ausencia de carga y de recarga, 0–5,5 V, sin temperatura, EMI, inductancias ni tolerancias. `reverse_feed_excluded=True` es una declaración de simulación, no prueba física.
- **Nunca** devuelve `hardware_approved=True`; incluso por debajo de umbrales hipotéticos el sistema no se declara seguro. Un osciloscopio, pinza/multímetro apropiado, identificación y valor máximo de todas las capacidades, descarga física y rutas inversas requieren revisión humana en futuro banco aislado autorizado.
- W08 ya dispone de `bleeder()` para el RC ideal; W68 no elige automáticamente un bleeder ni aprueba QOD (un TPS22918 tiene diodo inverso documentado y QOD puede convertirse en shunt con pass element soldado).

## Pruebas y fuente de verdad
Desde `research/2026-10-28-independent-wpt-sensor-v01`:
```sh
python3 -m unittest discover -s w_ind_68 -p 'test_w68.py' -v
python3 -m unittest discover -s w_ind_67 -p 'test_w67.py' -v
python3 -m unittest -v test_tx_cut_power_screen
python3 -m w_ind_68.w68_demo > W68_RESIDUAL_SYNTHETIC.json
```
La CI propia `.github/workflows/w-ind-68-residual-energy.yml` ejecuta regresiones y archiva JSON con procedencia explícita. Confirmar el estado GitHub real antes de declarar PASS. Tests digitales ≠ mediciones. No energía ni hardware ensayado.

## Matriz de decisiones y límites físicos
| Problema | Elección actual y condición |
|---|---|
| Dock de carga | Bloqueado: litio/BMS/estación desconectados. FOD metálico y humedad, offset, temperatura, EMI, seguridad autónoma y proceso de carga requieren validación separada. |
| Potencia de módulo sensor | Hipótesis 5 V/0,4 W media/1,5 W pico. Preferencia conservadora por conexión cableada reparable hasta comparar con WPT sencillo y WPT regulado con FOD y corte independiente reales. W68 diagnostica *residuo*, no transfiere energía ni elimina un cable. |
| Datos | ESP-NOW unicast CCMP o OpenThread; CRC, secuencias, ACK aplicativo, expiración, privacidad y recuperación. Nunca parar motores o fuente crítica por radio. |
| WISP5 | Solo microsensores RFID compatibles, no alimentar sensor de 0,4 W ni turbinas sin evidencia. |

No incorporar WPT por defecto a motores, bombas o LiDAR. Inspeccionar posición y capacidad del condensador TX, retorno, salida de los dos cortes, descarga y bloqueo inverso antes de diseñar PCB.

## Fuentes, owners, SHAs y derechos
Lectura local previa de decisión 28/10, `19-alternativas`, W-D22, acuerdo C/W, `LEEME_PRIMERO` y `WPT_DATOS_V01`. Repo local compartido en rama Codex sucia y apoyo Codex A01–A04 propios; no tocar. Solo PR W propia #9. Auditoría oficial realizada 31/10/2026 (pin del 28/10 → HEAD por rama real):
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0: master `7c7858c0` → `7c7858c0`; es prototipo del autor, no nuestro.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause: master `08332bc3` → `08332bc3`.
- [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause: pin `d978a697` vs rama real **640kHz** `604eee2d`: 68 ahead/11 behind, divergente. PR #40 abierta.
- [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0: master `c3b5f9be` → mismo; revisar PR de compatibilidad IDF #151 y #153, sin código integrado.
- [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause: main `7009584d` → `b6d0f06d`, 18 ahead, 0 behind; PR #13823 build y #13820 IP6 fusionadas 31/10.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo) main `f01a1b29` 29/10; [firmware](https://github.com/makerspet/oomwoo-firmware) `ce05f266` y [PCB](https://github.com/makerspet/oomwoo-pcb) `87aa7d38` 31/10: últimos cambios de J1/IMU/test pads, sin intervenir ni atribuirlos a VALDO.
- [TI TPS22918 datasheet](https://www.ti.com/product/TPS22918); fuentes de componentes de terceros solo referenciadas, no copiadas.

## BOM, coste y aceptación
Código Python nuevo: **0 € en componentes adicionales**. Resistencia de descarga, condensadores del tanque, supervisión térmica, FOD y aislamiento físico **SIN valores ni piezas seleccionados**; `BOM_W_IND_68.csv` distingue Diotronic auxiliar de TME/Mouser/DigiKey/fabricante y marca precios con IVA, MOQ y stock Zaragoza **pendientes de verificación**, sin inventarlos. No se ha comprado, impreso, soldado, energizado, instalado servicio, programado equipo, alterado Li-ion/BMS, cargado batería ni ejecutado tests físicos.

**Siguiente puerta:** identificar fuente aislada y retorno real en el esquema KiCad W18 (3 errores ERC aún bloqueantes), determinar *capacidades aguas abajo y rutas inversas* por netlist/datheet antes de aprobar una resistencia de descarga. Obtener mediciones reales únicamente tras proceso de seguridad y autorización. W68 es un **modelo de fallo con hipótesis**, no un sistema seguro.
