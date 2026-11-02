# W-IND-34 — Diagnóstico de continuidad de ALERT_N por terminación remota (SOLO DIGITAL)

**29/10/2026 · VALDO sector W · Robot aspirador NUEVO independiente · NO ENERGIZAR.**

## Hallazgo y mejora

W-IND-32/W-IND-33 proponen proteger un sensor receptor HIPOTÉTICO a 5 V, 80 mA medios, 300 mA pico, fallo de 400 mA. El monitor INA301 tiene ALERT_N activa-baja de drenador abierto. **Si se parte el hilo ALERT_N, un pullup puede hacer que parezca sano:** el circuito previo no garantiza detección de continuidad. Un rearme local no corrige este problema.

**Propuesta de interfaz experimental (NO conectada a KiCad):** un resistor de fin de línea EOL de 10 kΩ situado físicamente en el extremo INA301, un único pullup de 10 kΩ en el extremo lector, y una ventana ratiométrica de 0,40–0,60 × Vrail. En condiciones IDEALES: sano≈0,5Vrail; abierto≈Vrail; cortocircuitado/alarma≈0. Requiere dos comparadores y una salida de permiso normalmente apagado, **ambos sin seleccionar ni construir**. Además necesita supervisión positiva de la alimentación del INA301 (PG), supervisor de rail, rearme físico local y cortar por hardware sin depender de RF. El modelo expresa deseos lógicos, NO la realización física.

**Defecto de composición W32/W33:** ambos tienen un pullup de 10kΩ. Con EOL=10kΩ, uno produce 2,5 V a Vrail 5 V; **dos en paralelo producen 3,333 V** y la ventana 0,40–0,60 rechaza el estado sano. Para integrar, un solo pullup efectivo o valores recalculados con ERC/netlist antes de fabricar. Este cambio no modifica W32 ni W33.

## Evidencia reproducible

Desde research/2026-10-28-independent-wpt-sensor-v01/w_ind_34 ejecutar:

    python3 -m unittest -v test_w34_eol_window.py
    python3 w34_eol_window.py

24 tests nuevos PASS en Python local aislado. **128 esquinas hipotéticas** con Vrail 4,5/5,5 V, Rpullup y REOL ±5 % de 10kΩ, hilo 0/100Ω, comparadores lower=0,38/0,42 y upper=0,58/0,62 veces Vrail, offset supuesto ±25mV. Ninguno de esos extremos procede de caracterización física de un comparador elegido. 128 × 9 = **1152 evaluaciones aritméticas**, NO pruebas reales. Sano 128/128 solicitudes correctas; alarmado, señal abierta, retorno abierto, corto, EOL abierta, EOL cortada, duplicación de pullup y PG ausente 0/128 solicitudes cada uno. Ratio sano **0,46944–0,53292**, margen matemático mínimo **0,04708 de Vrail**.

**Contraejemplo no resuelto:** si el INA301 pierde VDD y ALERT_N queda en alta impedancia, la EOL sigue pareciendo sana **128/128 veces** sin supervisión independiente del VDD del monitor; el PG de este modelo es un booleano ficticio. Una EOL degradada a 14kΩ también puede pasar nominalmente. No se garantiza detección de toda corrosión o fuga. Un circuito real puede fallar por VOL, histéresis, backfeed, fallos comunes y transitorios no simulados.

Divisor nominal 5 V/(10k+10k) = 0,25 mA y **1,25 mW** de alimentación en estado sano; NO es potencia/eficiencia real de WPT ni incluye todos los circuitos.

## Matriz de decisiones (detallada en MATRIZ_W_IND_34.csv)

| Método | Hilo abierto | Monitor sin VDD | Corte autónomo real | Decisión |
|---|---|---|---|---|
| W33 ALERT directo | Puede parecer sano | Puede parecer sano | No | Bloquear como protección única |
| EOL+umbral único | No garantizado | No | No | Rechazar |
| EOL+ventana | Rechaza en modelo ideal | **Falla** sin PG | No | Candidato digital |
| EOL+ventana+PG+rearme | Rechaza en modelo | PG ideal inhibe | **No implementado** | Futuro esquema analógico/KiCad |
| Cable protegido modular | Depende diagnóstico | Depende monitor | Depende circuito | Mantener referencia de coste/servicio |

## Arquitecturas separadas

Dock de carga WPT, batería y BMS están **fuera**; ni carga Li-ion ni estación energizada. Alimentación WPT de módulos solo para un pequeño sensor hipotético; FOD/metal, desalineación, humedad, offset, térmica, EMI, rendimiento y actuadores físicos no demostrados. Motores y bombas **no** pasan por defecto a WPT. ESP-NOW y OpenThread dan **datos RF** (ACK de aplicación, CRC, secuencias, timeout, recuperación, autenticación/cifrado propios), no alimentación, parada ni rearme. WISP5 solo referencia de microsensores RFID.

## Autores y fuentes, HEAD comparados con 19-alternativas (29/10/2026)

- [Belbin Simple Wireless Power](https://github.com/mark-belbin/simple-wireless-power), **GPL-3.0**, master HEAD 7c7858c0dd7040801b6f191df1396115560218f0 igual pin. [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) cerrada.
- [WISP5 hardware](https://github.com/wisp/wisp5-hw), **BSD-2-Clause**, master HEAD 08332bc398aa3350d351ef2aaac163f8007cffda igual pin. [PR #1](https://github.com/wisp/wisp5-hw/pull/1) cerrada.
- [WISP5 firmware](https://github.com/wisp/wisp5), **BSD-2-Clause**, rama **640kHz**, HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2, **68 ahead/11 behind** del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b. [PR #40](https://github.com/wisp/wisp5/pull/40) abierta; no fast-forward.
- [Espressif ESP-NOW](https://github.com/espressif/esp-now), **Apache-2.0**, master HEAD c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 igual pin. [PR #153](https://github.com/espressif/esp-now/pull/153) cerrada; master incluye compatibilidad IDF6 y robustez consola de septiembre de 2026.
- [OpenThread](https://github.com/openthread/openthread), **BSD-3-Clause**, main HEAD e577777c308f6c87e5da3056239231a8fc147cb2, **14 ahead/0 behind** del pin 7009584dadc20cf20c20a6062f357dd572ba6885. Cambios GN CLI y radio; [PR #13820](https://github.com/openthread/openthread/pull/13820) abierta, no se toma como integrado.

[OOMWOO oficial](https://github.com/makerspet/oomwoo) main f01a1b295f462da5ab8d5f021a3f741cbd2b47df: último cambio gráfico del 29/10 sin incidencia W; [OOMWOO PR #79](https://github.com/makerspet/oomwoo/pull/79) es cleaning-jobs, intacta. VALDO propio W PR #9 partía de SHA 3d1d278a5006eb7a41ad0aee57c386db04de4a5f. Documentos maestros, D22, acuerdo C/W, adaptación y sus propietarios revisados. No editar clones upstream, CAD C, fuentes A01-A04 ni OEM; no copiar código ajeno.

Fuente primaria de comportamiento ALERT_N: [TI INA301](https://www.ti.com/product/INA301) (salida drenador abierto activa baja). Este modelo de resistores/ventana es propio y **no** replica una solución homologada de TI.

## BOM incremental y Diotronic

[BOM_W_IND_34.csv](BOM_W_IND_34.csv) documenta Diotronic como AUXILIAR. Resistencia axial [Diotronic 10351](https://diotronic.com/resistencias-de-carbono-1w/16309-resistencia-10k-5-1w): 10kΩ ±5% 1 W, catálogo web **0,15€ con IVA/unidad**, mínimo **5**, indicada «disponible» en catálogo; **NO hay stock comprobado en tienda Zaragoza**, ni equivalencia con huella SMD. Alternativa [TME Yageo RC0805FR-0710KL](https://www.tme.eu/es/details/rc0805fr-0710k/resistencias-smd/yageo/rc0805fr-0710kl/): 10kΩ ±1% 0805, precio/MOQ/disponibilidad final sin validar. Componente crítico de comparadores y PG **SIN PART NUMBER APROBADO**, precios, IVA, stock, plazos y trazabilidad pendientes. Ninguna compra.

## Bloqueos antes de avanzar físicamente

Elegir comparadores y PG reales de arranque/corte seguro; determinar ratiometría/histéresis/offset/temp/fugas/retornos y evitar realimentación parasitaria. Integrar en KiCad W32 con habilitación de los dos eFuses, reinicio local y ERC/netlist; luego FOD térmico independiente, EMI/offset y pruebas físicas **solo si se autoriza un proceso seguro**. Batería/BMS/dock/motores/estaciones permanecen desconectados. **No fabricar ni energizar.**
