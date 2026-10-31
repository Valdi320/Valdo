# W-IND-71 — Imposibilidad cuantificada de un bleeder pasivo barato bajo dos objetivos simultáneos

**31/10/2026. VALDO, sector W, robot aspirador NUEVO, abierto, reparable.** Mejora original: verificar *a partir del netlist KiCad real W21* que una sola resistencia de descarga pueda cumplir simultáneamente el presupuesto energético y el tiempo de bajada, **antes de elegir una pieza**. Ningún material OEM Xiaomi; no tocar CAD C/Codex, makerspet/oomwoo ni PR #79. No compras ni pruebas físicas.

## Resultado y valor práctico

W70 identificó R2=1 kΩ entre TX_5V_CUT y GND después del segundo interruptor; R1=22 kΩ está antes de él. W21 **NO representa** condensadores, bobinas, electrónica de TX ni fuente real (J1 es una declaración lógica no-BOM). W71 reutiliza la auditoría exacta W22/W70 de XML KiCad 9.0.2 para obtener el valor R2 y calcula un **intervalo de resistencias factible** para *dos* objetivos hipotéticos, con tolerancias.

**Ejemplo sintético, NO especificación de seguridad:** máxima tensión inicial supuesta 5,5 V, umbral arbitrario 0,5 V, C nominal imaginaria 100 µF ±20 %, R ±5 %, descarga ideal <=250 ms, potencia permanente máxima de descarga <=5 mW. Necesitaríamos a la vez R_nom >=6,368 kΩ para reducir pérdida y R_nom <=~0,827 kΩ para descargar a tiempo. **No existe resistencia fija que cumpla ambas condiciones.** R2=1 kΩ actual tendría hasta ~31,84 mW de pérdida a 5,5 V y ~0,302 s de descarga ideal en peor caso, incumpliendo ambos objetivos ficticios. Si se mantuvieran esos objetivos, la C nominal permitida para alguna resistencia pasiva sería <=~13 µF, pero **C física es desconocida**. Esto no demuestra que la R2 actual sea inadecuada para un dispositivo real; solo evita afirmar que aumentar R reduce pérdidas sin penalización térmica/temporal.

Formulación ideal: t=R*C*ln(V0/Vumbral); P=V0²/R. Con tolerancias dR,dC:
- R_min_nom=Vmax²/[Ppresupuesto(1-dR)]
- R_max_nom=tmax/[(1+dR)Cnom(1+dC)ln(Vmax/Vumbral)]
- Hay solución solo si R_min_nom<=R_max_nom. Este razonamiento supone **descarga RC autónoma de una sola capacidad** y una resistencia siempre conectada; no cubre resonancias, acoplamiento, alimentación inversa, cargas activas o fallo abierto de R2.

## Código, pruebas y evidencia

- `w71_bleed_feasibility.py`: auditoría matemática original con bloqueo de alteraciones del netlist, valores inválidos, falta de evidencia física y falsas aprobaciones. `test_w71.py`: 22 pruebas adversariales sintéticas, incluyendo tolerancias, factibilidad, puentes, resistencia cambiada, condensador extra, entradas inválidas y CLI.
- `.github/workflows/w-ind-71-bleed-pareto.yml`: usa el contenedor efímero **kicad/kicad:9.0.2** para exportar de verdad el esquema W21 a XML, ejecuta W22/W70/W71 y conserva XML/JSON con SHA256. Un PASS significa que se probó la lógica de **bloqueo**, jamás la descarga o FOD físicos.
- Ejecución manual: desde `research/2026-10-28-independent-wpt-sensor-v01`, `python3 -m unittest discover -s w_ind_71 -p 'test_w71.py' -v`; para XML nativo exportado `python3 -m w_ind_71.w71_bleed_feasibility w21.native.xml --report w71_review.json`. Cualquier XML no previsto se bloquea.

## Matriz de decisiones

| Solución | Retorno | Riesgo/limitación | Estado |
|---|---|---|---|
| R2=1 kΩ del W21 | Descarga pasiva nominal rápida, pieza estándar | Pérdida continua y tiempo real no medidos, fallo abierto desconocido | Solo esquemático |
| Subir R2 a 10 kΩ | Menos pérdida resistiva nominal | Mayor tiempo RC, C desconocida | **No cambiar** |
| Elegir cualquier R fija optimizada | Máxima sencillez y reparabilidad | Sin solución bajo el ejemplo conjunto de límites | **Descartada para ese ejemplo**, no para hardware aún |
| Descarga activa independiente al apagar TX + monitor real | Posible separar pérdidas ON de descarga OFF | Requiere control físico, test de fallo, FOD, temperatura, EMI, coste | Candidato sin seleccionar |
| WPT simple sin vigilancia | Barato sobre papel | No acredita FOD, calor o cortes seguros | Rechazado |
| WPT regulado y cortes independientes | Potencialmente más seguro y medible | Componentes/documentos/mediciones/coste pendientes | Estudio, no aprobado |
| Carga de dock con litio/BMS | Arquitectura distinta de módulo pequeño | Seguridad y consumo no caracterizados | Fuera de ensayo |
| ESP-NOW / OpenThread | Datos RF: ACK aplicativo, CRC, secuencias, timeout, cifrado, rearme | No alimentan ni sustituyen parada local | Alternativas digitales |
| WISP5 RFID | Micropotencia con lector | No apropiado para el sensor hipotético 0,4 W | Solo microsensores |

## Datos de procedencia: no confundir autor y simulación

W21 propio: [KiCad schematic](https://github.com/Valdi320/Valdo/tree/w/independent-sensor-wpt-link-20261028/research/2026-10-28-independent-wpt-sensor-v01/w_ind_21). Componente TI [TPS22918DBVR](https://www.ti.com/product/TPS22918), 1–5,5 V, máximo continuo 2 A, **sin limitador de corriente integrado** («Current limit type: None»), no fuente de seguridad FOD; los dos switches son solo **referencia no fabricable**. El estudio de descarga usa ninguna medida del proveedor ni de nuestro hardware; todos sus parámetros numéricos salvo R2 proceden de hipótesis. No interpretar 2 A de rating como disparo de protección.

Auditoría de HEAD/propiedad/licencias contrastada 31/10/2026 con los pins de `19-alternativas-abiertas-para-robot-independiente.md`: mark-belbin/simple-wireless-power GPL-3.0 master `7c7858c0dd7040801b6f191df1396115560218f0` igual pin (potencia sin adaptar); wisp/wisp5-hw BSD-2 master `08332bc398aa3350d351ef2aaac163f8007cffda` igual pin; wisp/wisp5 BSD-2 **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2`, diverge **+68/-11** de pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`, PR #40 antigua sin integrar; espressif/esp-now Apache-2 master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` igual pin, PR #151/#153 cerradas en enero/febrero 2026; openthread/openthread BSD-3 main `b6d0f06db304055f5866ff6e3c67370b54c81b15` **+18/0** vs pin `7009584dadc20cf20c20a6062f357dd572ba6885`, PR #13824/#13825 reciente radio/sim; no se ha copiado una línea de esos autores. OOMWOO oficial `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` en main, fuera de alcance. Bibliografía de autores y licencias preservadas.

## BOM e intervención

Archivo `BOM_W_IND_71.csv`: ningún nuevo componente físico ni cambio de valor aplicado. Diotronic auxiliar para pasivos solo con referencia, MOQ, precio con IVA, disponibilidad exacta Zaragoza y comparación TME/Mouser/DigiKey pendientes. Controladores FOD, corte y protecciones deberán tener trazabilidad y datasheet. **Gasto 0 €, batería y BMS desconectados, cero ensayos, no imprimir/soldar/energizar.**

**Siguiente paso de alto retorno:** obtener inventario eléctrico y documental de C/L del TX físico seleccionado y tolerancias con hoja del fabricante; diseñar corte autónomo por FOD/térmica/sobreintensidad, revisar y verificar la descarga activa en un banco aislado con carga resistiva **solo mediante proceso de seguridad y autorización**, antes de hablar de ensayos de batería/estación. El **W18 ERC histórico sigue FAIL** y el W21 ERC verde no habilita fabricación.
