# W-IND-67 — Separar tensión física de permiso del monitor (31/10/2026)

**Ámbito:** robot de limpieza NUEVO, abierto y reparable. Solo modelo analítico/CPU, sin baterías, BMS, estación, motores, radios energizadas ni hardware físico. Esta entrega **NO autoriza fabricar ni energizar**.

## Fallo reproducido y mejora aplicada

**Crédito del diagnóstico:** compañero Codex W-A02, `RELEVO_CODEX_W_A02_FUENTE_Y_PERMISOS_20261028.md`, commit local ajeno `9c92afa25127c99f842893ccd93243e8ec3a9f23`. Reimplementación propia sin copiar su parche ni tocar su repositorio.

En el antiguo W08, `source = interlocks.source_ok` confundía la autorización del monitor de alimentación con la presencia física de tensión. Cuando `source_ok=False` (monitor sin permiso) y ambos interruptores se soldaban cerrados, el modelo informaba **TX desenergizado**, incluso con la fuente físicamente presente. También admitía `source_ok=1` o `"false"`, interpretados mediante `all()` en lugar de rechazar entradas no booleanas.

**Ahora** la entrada independiente `supply_present: bool=True` representa una hipótesis conservadora de fuente presente, mientras `source_ok` solo participa en el permiso. El modelo reconoce que **ambos pasantes soldados permiten TX energizado sin autorización** y que QOD conectada podría crear una derivación sostenida. `supply_present=False` requiere hipótesis explícita de ausencia de fuente; **NO** prueba descarga de condensadores, bloqueo inverso ni aislamiento real. Los 9 permisos y los dos estados de interruptores se validan por tipo estricto. Las 25 regresiones W08 mantienen el contrato antiguo salvo una prueba cuyo escenario era realmente *fuente físicamente ausente* y ahora lo expresa de forma inequívoca.

## Evidencia y reproducción

Desde `research/2026-10-28-independent-wpt-sensor-v01`:

```sh
python3 -m unittest -v test_tx_cut_power_screen
python3 -m unittest discover -s w_ind_67 -p 'test_w67.py' -v
python3 -m w_ind_67.w67_demo > W67_SOURCE_PERMISSION_SYNTHETIC.json
```

La CI propia `.github/workflows/w-ind-67-physical-source.yml` debe ejecutar ambas suites y archivar JSON **SYNTHETIC_DC_TOPOLOGY_ONLY**; consultar el run real antes de anunciar PASS. 17 tests de W67 (incluida malla exhaustiva de 16 pares de fallos y 9 permisos), más 25 heredados, son **pruebas digitales**, no mediciones. El JSON incluye expresamente `physical_tests=0`, `hardware_approved=false`. Las restricciones de W66 sobre corte cruzado no sustituyen un circuito de paradas independiente.

## Matriz de decisión

| Modelo / tecnología | Beneficio | Riesgo y límite | Decisión |
|---|---|---|---|
| W08 anterior: `source_ok` = voltaje presente | Menos parámetros | Oculta energía en dos cortes soldados; valores no booleanos coercionados | **RECHAZADO** |
| W67: fuente física y permiso separados | Alerta ante corte fallido aun con monitor sin permiso | Ideal DC, no almacena capacitancia o backfeed | **IMPLEMENTADO DIGITAL** |
| Dos cortes con control autónomo, normalmente OFF y cadena FOD/térmica | Potencial barrera de fallo único | Sin esquema/circuito probado; dos soldaduras siguen peligrosas | **BLOQUEADO** |
| WPT sencillo para primer sensor | Pocas piezas inicialmente | Sin FOD, temperatura, offset/EMI/corte regulado demostrados | **NO ELEGIDO** |
| WPT regulado comercial con FOD documentado + corte externo | Mejor punto de partida para banco aislado | Coste/eficiencia/temperatura y capacidades específicas sin medir | **CANDIDATO, SIN ENERGIZAR** |
| Cable reforzado desmontable | Menor coste y pérdidas potenciales, repuesto fácil | Requiere conector en mantenimiento | **FALLBACK ECONÓMICO** |
| ESP-NOW unicast cifrado / OpenThread | Datos con ACK aplicativo, CRC, secuencia, timeout, privacidad, recuperación | Radio nunca corta TX ni transporta energía | **ESTUDIO INDEPENDIENTE** |
| WISP5 RFID | Microconsumo sin batería | Necesita lector, no 0.4 W continuos demostrado | **SOLO MICROSENSORES** |

**Tres subsistemas separables:** dock/carga de litio íntegramente bloqueados; potencia distribuida para sensor **hipotético** 5 V, 0,4 W media, 1,5 W pico, sin medición ni WPT seleccionado; datos RF: evaluar ESP-NOW/OpenThread con ACK aplicativo + CRC + secuencias + caducidad + protección de privacidad y recuperación, nunca parar un motor por radio. No WPT en motores ni bombas sin consumos/pérdidas medidas.

## Propiedad, licencias y consulta de HEAD al 31/10/2026

| Autor y licencia de su repositorio | SHA fijado 28/10 → HEAD oficial, actividad |
|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | `7c7858c0` → master `7c7858c0`, sin cambio, sin PR abiertas; resultados inductivos del autor NO nuestros |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | `08332bc3` → master `08332bc3`, sin cambio |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | `d978a697` → **640kHz `604eee2d`**; divergente 68 ahead / 11 behind; PR #40 abierta. No fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | `c3b5f9be` → master `c3b5f9be`; mejoras IDF v6 y consola del 10/09/2026 ya incorporadas |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | `7009584d` → main `b6d0f06d`, +18/-0; mejoras de radio SPINEL #13790 y build #13823 de 31/10, sin integración propia |

[OOMWOO oficial](https://github.com/makerspet/oomwoo) main `f01a1b29` (29/10, solo star-history reciente), firmware main `ce05f266` (31/10) y PCB main `87aa7d38` (31/10), revisados **sin tocar sus fuentes**. El repo local compartido VALDO está sucio en rama Codex ajena, por tanto W67 se desarrolla **solo en rama remota propia W de PR #9**. OOMWOO PR #79 cleaning-jobs no pertenece al módulo W. Dueños de CAD mecánico (C), Codex A02 y licencias externos respetados.

## Límites, criterios medibles y abastecimiento

La corrección es **software con coste incremental de piezas 0 €**; no convierte componentes de protección en gratuitos. Dos TPS22918 candidatos, termistores, comparadores, MOSFET/cortes, detección FOD y alimentación aislada **no están cualificados**. Validez física requeriría selección con datasheet, rail presente medido, corriente y tiempos de apertura en fallos, bajo protección térmica/FOD/offset/EMI/humedad, backfeed y doble cortocircuito, supervisión autónoma y presupuesto final puesto en Zaragoza. **ERC W18 mantiene 3 errores reales** (VIN_5V colgante y dos pines no alimentados); no se silencian. Ninguna prueba eléctrica, de baterías o de estación autorizada.

`BOM_W_IND_67.csv` señala Diotronic **solo auxiliar** (pasivos/prototipos rápidos) y alternativas TME/Mouser/DigiKey/fabricantes; precio con IVA, MOQ, transporte y **stock Zaragoza no comprobados**; componentes críticos requieren trazabilidad, no selección por comodidad. `MATRIZ_W_IND_67.csv` ofrece aceptación y límites. No compras, impresiones, soldaduras, despliegues de firmware ni instalaciones.

**Siguiente puerta técnica** (no ejecutada aquí): corregir el esquema ERC mediante un origen de 5 V/retorno físicamente definido en un proyecto KiCad propio, después concretar la cadena autónoma de corte y ensayar por simulación fallo de rail parcial y energía almacenada. No emplear PWR_FLAG ficticio para aparentar aprobación.
