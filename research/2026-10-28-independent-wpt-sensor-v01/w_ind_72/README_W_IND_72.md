# W-IND-72 — Descarga conmutada: la R2 permanente NO desaparece mágicamente

**31/10/2026. Robot aspirador NUEVO, VALDO sector W. Código original Python, sólo modelo matemático digital, no hardware cualificado.** No se modifica ningún esquema, equipo, CAD C, firmware, estaciones, batería/BMS, upstream o PR #79.

## Mejora material y reproducible

W70 verificó mediante netlist KiCad 9.0.2 que W21 contiene **R2=1 kΩ siempre entre TX_5V_CUT y GND**, después del segundo interruptor. W71 probó que, para DOS objetivos ficticios simultáneos (máximo 5 mW de disipación continua y descarga a 0,5 V en 250 ms), una resistencia pasiva única no sirve bajo hipótesis V0=5,5 V, C nominal=100 µF ±20 %, R ±5 %. W72 compara esa topología con agregar una nueva rama de 750 Ω que solo conduce al apagar TX.

**Hallazgo:** si se agrega la rama activa EN PARALELO sin retirar R2, el gasto continuo de R2 sigue existiendo. Un esquema futuro que la elimine podría cumplir el presupuesto matemático, pero introduce fallo abierto del switch de descarga (sin ruta), cerrado (shunt en funcionamiento) y peligro con doble corte de potencia soldado. Ninguna protección física se ha demostrado.

| Magnitud, solo simulación RC ideal | W21 R2 permanente + rama conmutada | Variante hipotética sin R2 |
|---|---:|---:|
| Pérdida ON a 5,5 V, R tolerancia 5 %, corriente electrónica ficticia total 101 µA | **32,398 mW** | **0,556 mW** |
| Tiempo de descarga máximo a 0,5 V, C=120 µF, R activa máxima=787,5 Ω + R switch=10 Ω | **130,4 ms** | **229,5 ms** |
| Cumplimiento de dos metas ficticias | **NO: consumo** | **SÍ, solo bajo hipótesis** |
| Autorización hardware/fabricación/energización | **NO** | **NO** |

Máxima corriente hipotética inicial 7,72 mA y máxima potencia instantánea en la resistencia activa 42,46 mW; energía supuesta máxima almacenada 1,815 mJ. Son cálculos de C/R ficticios, no especificaciones del transmisor. No incluyen bobinas, resonancia, retorno inverso, V del tanque, tolerancia térmica, driver real, fallos comunes, EMI ni FOD. La tolerancia de R2 se supone, no se extrae de BOM. El código siempre devuelve hardware_approved=false y may_energize=false, incluso cuando se le indican flags hipotéticos positivos.

## Criterio de aceptación y evidencia

21 pruebas adversariales Python originales: R2 sigue disipando, variante sin R2, R abierta/cerrada, doble soldadura, monitor sin alimentación, tolerancias, fugas, resistencia de conducción, datos desconocidos, NaN/Inf/bool, CLI y JSON. Ejecutar desde research/2026-10-28-independent-wpt-sensor-v01:

    python3 -m unittest discover -s w_ind_72 -p 'test_w72.py' -v
    python3 -m w_ind_72.w72_switched_discharge --report /tmp/W72_R2_RETAINED.json
    python3 -m w_ind_72.w72_switched_discharge --no-w21-r2 --report /tmp/W72_FUTURE_HYPOTHESIS.json

La opción --no-w21-r2 es SOLO matemática, NO cambia componentes. La CI de .github/workflows/w-ind-72-switched-bleed.yml ejecuta los tests y compara ambos resultados contra W72_SYNTHETIC_COMPARISON.json; archiva JSON regenerados. Hasta ver una ejecución CI concluida, no atribuir PASS de GitHub. Un PASS demuestra SOLO lógica, no ensayo FOD, temperatura, offset, EMI, desconexión independiente o descarga real.

## Matriz de decisiones

| Área | Alternativas y límites | Decisión |
|---|---|---|
| Dock de carga | WPT sencillo frente a regulado con FOD y temperatura, control térmico/EMI, offset, humedad, corte independiente, cargador/BMS litio separados | **Bloqueado: no usar batería/estación** |
| Potencia de módulos | Primer sensor *hipotético* 5 V, 0,4 W medio/1,5 W pico. WPT sencillo sin protección insuficiente; regulado con corte autónomo necesita piezas y mediciones; cable reforzado removible es control económico | **Ninguno elegido ni alimentado** |
| Bleeder R2 permanente | Barato y reparable, pero gasto continuo y tiempo RC acoplados | W71 demuestra incompatibilidad de dos metas hipotéticas |
| Descarga conmutada añadida | Puede acelerar OFF, pero no disminuye pérdida de R2 conectada | **No incorporarla en paralelo alegando ahorro** |
| Descarga conmutada en topología distinta | Separaría pérdidas ON y OFF, pero necesita control local independiente y evaluación de fallos y precio | **Solo candidato digital** |
| Datos | ESP-NOW unicast protegido u OpenThread, ACK aplicativo, CRC, secuencia, timeout, privacidad, recuperación; no son suministro | **Radio nunca es parada crítica** |
| WISP5 | RFID microsensores con lector, sin 0,4 W demostrados | **Sólo micropotencia justificada** |
| WPT motores/bombas | Picos y pérdidas reales desconocidos | **No introducir por defecto** |

## Autores, SHA HEAD/PR verificados el 31/10/2026

Comparados con pins de 19-alternativas-abiertas-para-robot-independiente.md del 28/10, **sin copiar** código/esquema ajeno:

- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0: master **7c7858c0dd7040801b6f191df1396115560218f0**, igual pin; eficiencia declarada por el autor, no nuestra.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause: master **08332bc398aa3350d351ef2aaac163f8007cffda**, igual pin.
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause: rama por defecto **640kHz**, HEAD **604eee2dffaeba3a270de61cf3dae887a33309c2**, **divergente +68/-11** de pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; [PR #40](https://github.com/wisp/wisp5/pull/40) antigua abierta.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0: master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, igual pin; #151 y #153 cerradas enero/febrero 2026.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause: main **b6d0f06db304055f5866ff6e3c67370b54c81b15**, +18 commits respecto a pin 7009584dadc20cf20c20a6062f357dd572ba6885; [PR #13821](https://github.com/openthread/openthread/pull/13821) y [#13822](https://github.com/openthread/openthread/pull/13822) recientes, no probadas aquí.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo) main f01a1b295f462da5ab8d5f021a3f741cbd2b47df. [VALDO PR #9](https://github.com/Valdi320/Valdo/pull/9) propia abierta. Repo local de VALDO en rama Codex sucia, **no tocado**; adaptación VALDO_OOMWOO y contrato WPT leídos en remoto, sin cambios.

El componente del esquema W21 TPS22918 (hoja [Texas Instruments](https://www.ti.com/product/TPS22918)) tiene QOD, pero no limitador integrado de corriente; NO se elige para esta topología sin caracterización. No hay piezas importadas de referencias GPL/BSD/Apache.

## BOM, coste, bloqueo y punto dulce

[BOM_W_IND_72.csv](BOM_W_IND_72.csv) distingue R2 dibujada, nuevo resistor 750 Ω, switch activo, monitor de tensión y corte FOD/térmico **no seleccionados**. Hardware añadido/comprado: **cero**, coste real de construirlo **desconocido**, aunque el software sea gratuito. Diotronic [Zaragoza, Av. de Valencia 5](https://diotronic.com/2-inicio) sólo auxiliar: ningún stock local exacto, precio final IVA o MOQ verificado para estos candidatos. TME, Mouser, DigiKey y fabricantes son alternativas críticas por trazabilidad; NO comprar ni sustituir por coincidencia de precio.

**Beneficio comprobado:** evitable error de arquitectura en una futura PCB: agregar descarga conmutada sin revisar la R2 permanente no logra ahorro. **Pendiente para construir:** esquemas/datasheets completos TX, inventario C/L de todos los nodos, corte autónomo, retorno/backfeed, monitoreo alimentado de manera independiente y seguridad FOD/temperatura/humedad/EMI. **Decisión:** consolidar el resultado, no seguir simulando variantes RC sin datos nuevos. Primero caracterizar documentalmente transmisor abierto candidato; solo futuro banco aislado, carga resistiva, con proceso de seguridad y autorización. **W18 ERC histórico sigue con 3 infracciones; ningún montaje/energización autorizados.**
