# W-IND-74 · La potencia en vacío puede hacer inviable un sensor WPT diminuto

**31/10/2026 — ingeniería DIGITAL verificable, NO ensayo eléctrico.** Código original, exclusivamente sector W y robot aspirador nuevo sin electrónica Xiaomi. No se selecciona ningún producto ni se autoriza compra, montaje, soldadura, impresión, carga de litio, estación o motor.

## Mejora reproducible

Antes se estudiaban eficiencia, descarga y seguridad de un transmisor, pero faltaba una **puerta cuantitativa de consumo en reposo** para evitar fabricar una bobina/transmisor por cada sensor de muy bajo consumo. Esta entrega introduce `w74_energy_gate.py`: compara la energía de una **pareja WPT energizada continuamente** con una conexión corta reemplazable a igual tensión de salida, comprueba picos y límites presupuestarios explícitos y calcula el **máximo consumo fijo admisible del TX**. Rechaza datos omitidos, no numéricos, `NaN`, eficiencias imposibles, motores/bombas, parada crítica dependiente de radio y conexión a batería/BMS. **Ningún resultado digital declara hardware aprobado.**

**Primer módulo objetivo**: indicador no crítico de presencia/llenado del depósito extraíble, solo como demostrador de un sensor pequeño a 3,3 V; el tipo exacto de sensor, encapsulado y potencia siguen por elegir. La fijación mecánica la define su dueño C en otra fase. En caso de fallo, el robot no debe tomar decisiones críticas basándose exclusivamente en este sensor. La radio sólo transportaría datos (ESP-NOW u OpenThread); no alimenta ni autoriza un corte crítico. Un microsensor WISP exigiría un lector RFID y otro balance energético; aquí no se asume equivalente.

### Caso totalmente hipotético — no es dato de un componente

| Variable | Supuesto para explorar la decisión |
|---|---:|
| Sensor activo / reposo / pico | 20 mW / 1 mW / 100 mW |
| Fracción de actividad | 10 % |
| Rail del módulo | 3,3 V ideal, regulado |
| Eficiencia DC conjunta TX → rail RX, excluyendo fijo | 50 % **inventado** |
| Potencia fija de TX siempre energizado | 100 mW **inventados** |
| Potencia máxima de entrada TX / salida RX | 400 mW / 200 mW **supuestos** |
| Par de cables de comparación | resistencia total 0,2 Ω **supuesta** |
| Criterio energético de investigación | máximo +0,5 Wh/día WPT frente a cable, **no norma** |
| Límite provisional de disipación pico | 0,25 W **no límite de seguridad** |

Resultado con ecuaciones deterministas:

- Sensor: **2,9 mW de media**. Transmisor WPT: **105,8 mW de media** y **300 mW de pico** (modelo). Pérdidas WPT medias: **102,9 mW**.
- WPT **2,5392 Wh/día** frente a cable teórico **0,069618 Wh/día**: **36,47×** consumo de la alternativa idealizada. Exceso = **2,469582 Wh/día**, por encima del límite ficticio de +0,5 Wh/día.
- A eficiencia 50 % y cargas anteriores, para cumplir el criterio de +0,5 Wh/día el **consumo fijo del transmisor debería ser como máximo 17,934 mW**; el supuesto de 100 mW lo incumple. **No sabemos qué consumo fijo tendrá un transmisor real.**
- La resistencia de cable y pérdidas de regulación también deben medirse. La comparación no considera valor económico del reemplazo sin contactos, envejecimiento ni pérdida de autonomía real de una batería aún no seleccionada.

Cálculos: `P_RX_avg = d·P_active+(1-d)·P_sleep`, `P_TX_avg = P_TX_fixed+P_RX_avg/eta`, `P_wire_avg = P_RX_avg + R·(d·(P_active/V)^2+(1-d)·(P_sleep/V)^2) + P_wire_fixed`. Criterio: `P_TX_fixed_max = limite_Wh_dia/24 + P_wire_avg - P_RX_avg/eta`.

**Decisión W74: NO-GO para ese caso sintético, NO prohibición general de WPT.** Si se identifica un transmisor con menor consumo en vacío, eficacia y protecciones demostradas, se ejecuta el mismo comparador con evidencia; no se elige hardware por resultados inventados. No se traslada el transmisor de 24 V/100 W de Mark Belbin al piloto.

## Reproducir en una copia sin repos externos

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_74
python3 -m unittest -v test_w74.py
python3 w74_energy_gate.py --input SCENARIO_HYPOTHETICAL.json --output calculado.json
cmp calculado.json W74_EVIDENCE_SYNTHETIC.json
```

33 tests digitales originales cubren física idealizada, límites, fallos de entrada, privacidad funcional, picos y separación de batería. La CI propia reproduce la evidencia JSON de forma determinista, verifica resultados clave y publica el JSON; no oculta el ERC W18 ni otras CI históricas. La unidad principal es W, Wh/día y porcentaje; no se calcula temperatura real a partir de potencia sin propiedades térmicas verificadas.

## Tres problemas que NO se confunden

| Problema | Decisión | Puerta antes de integrar |
|---|---|---|
| **Dock de carga** | Fuera de este ensayo. Ni cargador ni batería/BMS seleccionados o conectados. | Seguridades de litio, acoplamiento, agua, FOD, temperatura, EMI y corte físico independiente revisados y autorizados. |
| **Potencia del módulo extraíble** | Comparar bobinas reguladas de bajo consumo con un cable corto o un conector bloqueado. Este test rechaza WPT si el consumo fijo arruina autonomía. | Medir P_TX fijo, eta con carga mínima/pico, variación XY/gap, brownout, corrientes inversas y residual; FOD y protección térmica. |
| **Datos** | ESP-NOW o OpenThread, sin energía por radio. Preferir el más simple que pase las pruebas reales. | ACK de aplicación, CRC, identidad, secuencia, TTL/timeout, cifrado, recuperación, tasa, coexistencia; nunca parada de motor/cliff por radio. |

**WISP5** sólo bajo una puerta separada para microsensores RFID de consumo suficientemente bajo; no reemplaza un enlace de potencia contínuo. **Motores, bombas y turbina** quedan excluidos del piloto.

## Proveniencia y propiedad externa comprobadas el 31/10/2026

- Mark Belbin [simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, `master` **7c7858c0dd7040801b6f191df1396115560218f0**, idéntico a registro de 28/10; PR histórica [#1](https://github.com/mark-belbin/simple-wireless-power/pull/1). Datos del prototipo ajeno, no hardware elegido.
- WISP [hardware](https://github.com/wisp/wisp5-hw), BSD-2-Clause, `master` **08332bc398aa3350d351ef2aaac163f8007cffda**, idéntico; [firmware](https://github.com/wisp/wisp5), BSD-2-Clause, `640kHz` **604eee2dffaeba3a270de61cf3dae887a33309c2**. La referencia registrada **d978a6978ad23ccd6c44dd55430973b04a3d4a9b** pertenece a una historia DIVERGENTE (**68 ahead / 11 behind** con respecto a la rama 640kHz); no llamarla simplemente actualización lineal. [PR #38](https://github.com/wisp/wisp5/pull/38) informa compatibilidad de lector, no justifica nuestro módulo.
- Espressif [esp-now](https://github.com/espressif/esp-now), Apache-2.0, `master` **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, idéntico a registro; [PR #151](https://github.com/espressif/esp-now/pull/151) de compatibilidad esp-idf. Librería no certifica nuestro enlace ni clave.
- OpenThread [openthread](https://github.com/openthread/openthread), BSD-3-Clause, `main` **b6d0f06db304055f5866ff6e3c67370b54c81b15**, **18 commits por delante** del registrado **7009584dadc20cf20c20a6062f357dd572ba6885**; incluye cambios de radio y TCP/IPv6 y PR recientes [#13821](https://github.com/openthread/openthread/pull/13821)/[#13822](https://github.com/openthread/openthread/pull/13822), ninguno cambia el balance WPT.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo), Apache-2.0, `main` **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**; último cambio gráfico bot, PR de limpieza propia [#79](https://github.com/makerspet/oomwoo/pull/79) abierta e INTACTA. [VALDO W PR #9](https://github.com/Valdi320/Valdo/pull/9) es destino exclusivo. Se revisaron las decisiones locales del 28/10, contrato WPT_DATOS_V01 y coordinación de propietarios W/C; ni clones upstream ni fuentes C tocados.

No se copia código ni CAD de autores externos ni se redistribuyen diseños GPL incompatibles. Cálculos y pruebas W74 son independientes.

## Límites, evidencia y próximo paso

`W74_EVIDENCE_SYNTHETIC.json` conserva **source_kind=SYNTHETIC_HYPOTHESIS**, `hardware_approved=false` y `physical_tests_performed=false` incondicionalmente. Aun si alguien escribe `BENCH_UNREVIEWED`, el programa **no otorga aprobación física**. Las condiciones reales de consumo, offset, EMI, FOD, humedad, disipación, resistencia de cable, contacto y tasa de fallo siguen DESCONOCIDAS. Ninguna simulación prueba cortes eléctricos contra doble soldadura o descarga de condensadores.

**Próximo paso de mayor retorno**: fichar un par WPT regulado **real** de 5 V/centenas de mW con esquemas/datasheets trazables y comparar su consumo fijo/eficiencia a 1 mW y 20 mW con un conector desmontable. Si no supera este umbral económico/energético, priorizar unión mecánica reparable y cable corto para ese sensor. Banco aislado, resistivo y desconectado de litio solamente tras proceso de seguridad y autorización.
