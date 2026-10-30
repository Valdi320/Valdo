# W-IND-43 — Corregir histéresis de TPS3700 y generar HEALTH activo sin asumir que OUTA es push-pull

**2026-10-30 · VALDO · solo sector W · robot aspirador NUEVO e independiente.** Especificación eléctrica original + comprobador Python estándar. **SIN esquema KiCad implementado, SIN simulación SPICE, SIN hardware, NO FABRICAR NI ENERGIZAR.** El robot, batería, BMS, dock y motores permanecen desconectados. No se trasplanta ni se reutiliza electrónica Xiaomi.

## Mejora de alto retorno: error real detectado en el criterio anterior

W-IND-41 calificaba un divisor de **62 kΩ/10 kΩ** a partir del umbral **ascendente** garantizado de TPS3700 (396–404 mV). Para garantizar que una rama **se desactive al caer la alimentación**, el cálculo debe abarcar su umbral **descendente** (387–400 mV), además de la historia de histéresis. Bajo los **mismos supuestos de ingeniería** que W41 (dos resistencias 1 %, perturbación de entrada ±1 µA *ficticia*; sensor sano ≥3,135 V, sensor defectuoso ≤2,700 V):

| Divisor superior / inferior | Peor umbral ascendente máximo | Peor umbral descendente mínimo | Margen a sano 3,135 V | Margen a fallo 2,700 V | Resultado **solo matemático** |
|---|---:|---:|---:|---:|---|
| 62,0 kΩ / 10 kΩ (W41 antiguo) | 3,022 V | **2,678 V** | +113 mV | **−22 mV** | **NO APTO**: salida puede seguir autorizando con rail a 2,700 V |
| **63,4 kΩ / 10 kΩ (E96 candidato)** | **3,081 V** | **2,729 V** | **+54 mV** | **+29 mV** | PASS condicionado a hipótesis ±1 µA, 1 %, voltajes de ensayo |
| 64,9 kΩ / 10 kΩ | 3,144 V | 2,785 V | **−9 mV** | +85 mV | **NO APTO**: posible rechazo de rail sano |

La protección es **sensible a hipótesis no medidas**: con perturbación ±1,5 µA el candidato 63,4 kΩ pierde ~2,2 mV de margen en rail defectuoso. No equivalen ni a incertidumbres instrumentadas ni a las garantías térmicas/fugas de un PCB; la selección de resistor no está cualificada. Los valores se obtienen de `Vrail=Vref*(1+Rtop/Rbottom)+Iinput*Rtop`, barriendo Vref garantizado, tolerancia de ambas resistencias e Iinput. Contrastar con la ficha vigente del fabricante antes de aprobar: [TI TPS3700](https://www.ti.com/product/TPS3700), [Electrical characteristics](https://www.ti.com/document-viewer/TPS3700/datasheet/electrical-characteristics-slvsci76498).

## Alternativa reparable al supuesto de W42: convertir **OUTB** en HEALTH positivo

En vez de asumir que **OUTA** de TPS3700 (drenador abierto que denuncia fallo) puede emitir HIGH activo, proponer estudiar **OUTB**: esta salida de drenador abierto puede **hundir a LOW** cuando INB− excede el umbral; el drenador abierto gobierna la **puerta de un P-MOS discreto**, no el permiso de carga directamente. Así, se utiliza una señal activa cuando el supervisor detecta la tensión adecuada, sin introducir necesariamente un segundo supervisor push-pull:

```text
Rail 3V3 a observar ── 63k4 ──┬── INB− TPS3700 (propuesta)
                               │
                              10k
                               │
                              GND

5V_PRE_CUT (alimentación candidata del TPS3700) ── S [P-MOS] D ── HEALTH_OUT ── cable ── HEALTH_IN
           │                                     G                           │
           └──────────────── 22k ────────────────┘                        47k a GND
                                                │
                                           OUTB TPS3700
                              (drenador abierto: LOW cuando INB− sano)

HEALTH_IN => interfaz de autorización por calificar y DOS EN normalmente OFF;
            nunca conectar HEALTH_IN directamente a los eFuses sin lógica.
```

**Fallos resueltos únicamente por el MODELO IDEAL:** OUTB desconectado, HEALTH roto, rail observado por debajo del límite garantizado, pérdida del 5 V que alimenta la puerta; la señal en receptor queda LOW por resistencia local. **Fallos NO resueltos:** TPS3700 con VDD por debajo del POR (la ficha indica OUTB *indeterminado*), circuito de puerta atascado a GND, HEALTH en corto a +5 V, 5V no supervisado o con backfeed, transistor con fugas, resistencia del shunt compartida o dos eFuse soldados/cerrados; ninguna autorización sin W37 rearme local real e interlocks FOD/temperatura/sobrecorriente independientes. El esquema ASCII es un **contrato de pines**, no CAD eléctrico validado; se necesita prototipo KiCad + ERC/netlist + análisis de transitorios y alimentación parcial antes de intentar una prueba de banco.

## Pruebas reproducibles y límites

Desde `research/2026-10-28-independent-wpt-sensor-v01/w_ind_43/`:

```sh
python3 -m unittest -v test_w43
python3 w43_por_gate.py --out W43_EVIDENCE.json
```

**40/40 tests locales PASS** con Python 3.11; el generador barre **1.536 casos lógicos adversariales** (3 niveles de rail × 4 estados VDD × 2 estados fuente × 6 conmutadores binarios); **52** casos pueden solicitar indebidamente ON, y 768 combinaciones producen salidas indeterminadas. Son casos sintéticos **no tasas de avería, no fallos físicos independientes ni garantía de seguridad**. La CI reproducirá el resultado y archivará JSON con nombre inequívoco `W43-POR-HYSTERESIS-1536-SYNTHETIC-NOT-HARDWARE`. La validación local mediante `unittest` no sustituye KiCad, SPICE ni pruebas de laboratorio. La falla histórica W-IND-18 (ERC) continúa como bloqueo separado.

## Decisión de sistema, sin confundir tres tareas

1. **Dock de carga:** no diseñado, sin batería/BMS; certificación de carga, FOD, térmica, agua y desconexión pendiente. No aplicar este modelo a litio.
2. **WPT distribuido a microsensor:** único piloto **hipotético** de 5 V, 0,4 W medio, 1,5 W pico con carga ficticia y fuente aislada solo tras autorización. Comparar acoplamiento/regulación/FOD/offset/EMI y alternativa por cable retenido; no extrapolar a motor, bomba o turbina. TPS3700/PMOS forman solo una **señal de permiso**, no un controlador WPT completo.
3. **Datos sin contacto:** ESP-NOW (Apache-2.0, ESP) vs OpenThread (BSD-3) siguen alternativas; ambas necesitan ACK de aplicación, CRC, sesión/secuencia, caducidad, privacidad, tiempo límite y recuperación. El radio **no alimenta un módulo** ni ejecuta parada crítica. WISP5 (BSD-2) solo para sensores RFID de potencia ínfima e intermitente.

## Matriz/BOM/procedencia

Ver `MATRIZ_W_IND_43.csv` y `BOM_W_IND_43.csv`. Diotronic es auxiliar y **NO** consta stock confirmado en Zaragoza, MOQ/precio final verificado ni equivalentes trazables de componentes críticos. Costes listados son capturas orientativas de distribuidor *IVA incluido, excluidos portes*, nunca presupuesto cerrado. P-MOS BSS84 es **solo candidato**: VGS/RDS(on), encapsulado, pinout, fugas, SOA, curva temperatura y suministro aún sin validar para esta función, así como el `5V_PRE_CUT` real y la salida de OUTB. No comprar ni modificar arquitectura por stock.

### Autores externos y control de revisiones, 30/10/2026

| Repositorio, propietario, licencia | Rama y HEAD vs pin del documento maestro 19 | Revisión de PR relevante |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | `master` `7c7858c0dd7040801b6f191df1396115560218f0` **idéntico** | PR #1 fusionada; su ensayo ~100W / 81,3% / 1–2mm es del **autor**. No copiar su CAD GPL. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | `master` `08332bc398aa3350d351ef2aaac163f8007cffda` **idéntico** | PR #1 histórica fusionada. |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | **`640kHz`** `604eee2dffaeba3a270de61cf3dae887a33309c2` **DIVERGIÓ +68/−11** frente a `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` | PR #40 abierta (rama `436kHz`, NO confundir con `640kHz`). No hacer fast-forward ciego. |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | `master` `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` **idéntico** | PR #153 cerrada sin fusionar. |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | `main` `e577777c308f6c87e5da3056239231a8fc147cb2` **+14** frente a `7009584dadc20cf20c20a6062f357dd572ba6885` | PR #13822 abierta, no fusionada; cambio de entrega IPv6 para MTD. |

OOMWOO makerspet/oomwoo (`main`, `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`), VALDO #9 propio, integración local y PR #79 cleaning-jobs revisadas, no editadas. Se consultaron maestros locales 00, 19, D22, contrato W/C, `VALDO_OOMWOO/LEEME_PRIMERO.md`, `WPT_DATOS_V01.md`, propietarios y automatizaciones antes de trabajar. Clones upstream y trabajos Codex/C permanecen intactos; código, modelo y especificación W43 son propios, sin material GPL/BSD/Apache copiado.

**Siguiente puerta:** pasar el contrato OUTB+P-MOS a esquema KiCad **nuevo** en ámbito W sin modificar el esquema existente de compañeros, verificar ERC/netlist y transitorios con estímulos POR/brownout; elegir componente exacto solo con ficha y abastecimiento comprobados. El modelo encuentra explícitamente fallos que impiden cualquier autorización de ensayos energizados.
