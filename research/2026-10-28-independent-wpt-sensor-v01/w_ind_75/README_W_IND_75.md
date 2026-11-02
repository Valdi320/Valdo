# W-IND-75 — Estado en reposo no es consumo con receptor activo

**31/10/2026. Hito W propio para un robot de limpieza NUEVO, NO Xiaomi.** Dato de fabricante + modelo matemático, pruebas digitales originales. CERO ensayos físicos, compra, batería conectada, soldadura, impresión o equipo energizado.

## Mejora comprobable

La investigación de W74 fijó para el supuesto de sensor continuo de 2,9 mW y un exceso permitido de 0,5 Wh/día un límite de **23,733333 mW en la entrada TX con el sensor PRESENTE**, idealizando la alimentación por cable. El límite anterior 17,934 mW se refería a potencia fija interna bajo un supuesto de eficiencia del 50 % y **no debe confundirse con corriente de reposo sin receptor**.

Renesas documenta que su TX [P9235A-R](https://www.renesas.com/en/products/p9235a-r) consume aproximadamente **1 mA en standby** a 5 V (5 mW calculados), trabaja hasta 3 W y está **OBSOLETE**. Su RX [P9027LP-R](https://www.renesas.com/en/products/p9027lp-r) también está **OBSOLETE**. La cifra de 5 mW NO es una medición de TX alimentando el sensor de 2,9 mW: no puede emplearse para afirmar que pasa el límite de 23,733 mW, ni se elige esa pareja para compras.

El nuevo auditor `w75_vendor_state_gate.py` obliga a distinguir reposo sin RX de operación bajo carga: sin potencia TX/RX medida en la carga real, con separación y offset conocidos, protección térmica, FOD, EMI, humedad, retorno inverso, energía residual, corte autónomo y radio apropiada, bloquea la selección. También bloquea expresamente componentes obsoletos, batería/BMS, motores/bombas y parada crítica dependiente de radio. **Incluso un resultado de comparación digital favorable no otorga aprobación física.**

### Caso documentado y evidencia

- Fuente del autor: standby del transmisor = 1 mA × 5 V = **5 mW**, solo sin receptor (manufacturer_claim).
- Carga de sensor: **2,9 mW hipotéticos**; baseline cable ideal = **0,0696 Wh/día**; umbral TX con receptor presente = **23,733333 mW** para +0,5 Wh/día.
- Resultado de auditoría: **BLOCKED** (`LIFECYCLE_NOT_ACTIVE`, `LOADED_POWER_UNKNOWN`, `RADIO_APP_GATES_UNVERIFIED`, `SAFETY_GATES_UNVERIFIED`). No se estima eficiencia ni autonomía sin datos.
- Escenario adversarial sintético de 20 mW de entrada TX y 2,9 mW RX da exceso de **0,4104 Wh/día**, pero NO equivale a componente o medición real.

## Reproducción

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_75
python3 -m unittest -v test_w75.py
python3 w75_vendor_state_gate.py --input SCENARIO_VENDOR_DOCUMENT_ONLY.json --output generado.json
cmp generado.json W75_EVIDENCE_SYNTHETIC.json
```

**20 pruebas Python** de hipótesis y condiciones de bloqueo, en un entorno sin hardware. El workflow dedicado verifica pruebas y regeneración exacta de JSON. Valores sintéticos están diferenciados de la única afirmación del fabricante. `source_kind=bench_measured` es una etiqueta de datos aportados, NO autentica instrumentos ni valida hardware; la revisión humana y pruebas independientes son obligatorias.

## Las tres interfaces y licencias

- Dock de carga: **excluido**. No hay litio, BMS, cargador o estación modificados. Un TX de sensor no sirve como cargador de batería automáticamente.
- Potencia al módulo: WPT regulada solo cuando el balance a carga real, offset/gap, temperatura y FOD lo permitan; cable corto y conector sustituible siguen siendo alternativa válida.
- Datos: comparar [ESP-NOW](https://github.com/espressif/esp-now) (Apache-2.0) frente a [OpenThread](https://github.com/openthread/openthread) (BSD-3-Clause) con ACK aplicativo, CRC, secuencia, timeout, privacidad y fail-safe local. La radio no entrega energía, y el corte crítico es autónomo.

Se respetan licencias de [Mark Belbin](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 (solo referencia externa) y [WISP5](https://github.com/wisp/wisp5) BSD-2-Clause (microsensores RFID, no motor). No se incorporan archivos de terceros.

### HEAD y procedencia revisados 31/10/2026

| Externo | HEAD oficial / rama | Diferencia con registro 28/10 |
|---|---|---|
| mark-belbin/simple-wireless-power | `7c7858c0dd7040801b6f191df1396115560218f0` / master | idéntico; PR #1 histórica |
| wisp/wisp5-hw | `08332bc398aa3350d351ef2aaac163f8007cffda` / master | idéntico |
| wisp/wisp5 | `604eee2dffaeba3a270de61cf3dae887a33309c2` / 640kHz | historia divergente: 68 adelante y 11 detrás respecto a `d978a697...`, NO actualización lineal; PR #38 histórica |
| espressif/esp-now | `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` / master | idéntico; PR #151 cerrada |
| openthread/openthread | `b6d0f06db304055f5866ff6e3c67370b54c81b15` / main | 18 commits por delante; PR #13821/#13822 abiertas |

OOMWOO oficial `makerspet/oomwoo` main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`, PR #79 de cleaning-jobs intacta. Relevo local VALDO_OOMWOO y acuerdos W/C leídos. Única automatización activa en la parcela es I+D W; no se edita el árbol local sucio de compañeros ni upstream. Esta entrega se añade exclusivamente a PR W propia #9. Otras actualizaciones locales de adaptación no se atribuyen a W.

## Matriz / BOM y bloqueos

Ver `MATRIZ_DECISION_W75.csv` y `BOM_W_IND_75.csv`. Diotronic es proveedor **auxiliar**, con precios IVA, MOQ y stock de tienda *PENDIENTES*, nunca se sustituye un IC crítico por semejanza de catálogo. Se compararán TME/Mouser/DigiKey si se identifica pareja ACTIVA y se recibe presupuesto verificable; de momento NO hay pieza aprobada. No se dan valores de eficacia a 2,9 mW, temperatura, EMI ni tolerancia a offset basados en datos de un fabricante que no los ha publicado en esta revisión.

**Próximo paso:** seleccionar candidato comercial activo con fabricante y esquemas trazables, exigir curva de consumo *con RX presente* a 1–20 mW y protección FOD/temperatura. Sin esos datos: no comprar; preparar solo plan de medición en banco aislado resistivo tras autorización, sin litio.
