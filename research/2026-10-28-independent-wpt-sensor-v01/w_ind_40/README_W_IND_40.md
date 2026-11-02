# W-IND-40 — fallos comunes y valor marginal de un tercer INA301 (SOLO DIGITAL)

**Fecha 30/10/2026 · VALDO W exclusivo · robot NUEVO independiente · NO FABRICAR / NO ENERGIZAR**

## Resultado verificable y decisión de alto retorno

En W39 hay dos INA301 con **la misma resistencia shunt y la misma alimentación 3,3 V**. Añadir un tercer INA301 alimentado también del mismo nodo y midiendo el mismo shunt **NO reduce** los dos escenarios de fallo común en este modelo: shunt puenteado y pérdida de 3,3 V. El coste incremental orientativo del tercer INA301A1IDGKR es **3,35 € IVA incluido, más pasivos, PCB, montaje, transporte**, según [DigiKey España](https://www.digikey.es/es/products/detail/texas-instruments/INA301A1IDGKR/6571979), consultada el 30/10/2026 (2,77 € antes de IVA, cantidad 1, 4.225 anunciados en web; no reservado).

**Decisión del hito:** no añadir ahora ese tercer INA redundante. Priorizar el estudio de un **supervisor de presencia real del rail 3,3 V**, alimentado desde dominio independiente, con salida local de permiso positivo normalmente OFF, y un ensayo que distinga un INA muerto de una alarma sana. Esta es una *hipótesis arquitectónica*, NO un componente elegido ni un circuito implementado.

### Ensayo cuantitativo digital (sin probabilidades)

Para cada topología, se comprueban exactamente **106 conjuntos de fallos** de orden 0, 1 y 2 entre 14 nombres de fallo, bajo la hipótesis de sobrecorriente y fuente presente. Son **424 configuraciones topología/conjunto**, con salidas ideales de los dos cortes en serie:

| Topología ideal | conjuntos mínimos inseguros de 1 fallo | conjuntos mínimos inseguros de 2 fallos | estados inseguros exactos de 2 fallos | interpretación |
| --- | ---: | ---: | ---: | --- |
| W39: 2 INA/shunt/3,3 V comunes | 2 | 10 | 35/91 | shunt y 3,3 V son fallos únicos comunes |
| 3 INA pero **todos** con shunt/rail comunes | 2 | 1 | 26/91 | reduce fallos dobles de monitores, **no** los comunes únicos |
| supervisor 3,3 V alimentado **desde ese mismo rail** | 2 | 10 | 35/91 | no se acredita protección frente a pérdida del propio rail |
| supervisor 3,3 V alimentado independientemente (**HIPOTÉTICO**) | 1 | 11 | 23/91 | elimina del modelo el fallo único de pérdida 3,3 V, **no** el shunt |

**Fallo hallado durante el desarrollo:** el primer test exigía monotonía de los fallos; falló. Al añadirse una pérdida de alimentación, un hipotético supervisor independiente puede solicitar OFF y convertir un escenario antes peligroso en uno no peligroso. Se corrigió el test y el JSON consigna explícitamente la no-monotonía. Los recuentos NO equivalen a fiabilidad ni probabilidad de fallo; no se han modelado coberturas diagnósticas reales.

**Precaución en el escenario 3,3 V perdido:** se modela una condición conservadora de peor caso: el permiso de W39 podría quedar aparentemente sano porque **no existe una supervisión 3,3 V independiente acreditada en su esquema**. No se afirma haber demostrado cómo se comportan las salidas físicas desalimentadas. Cuando el rail vuelva, los biestables, retardos y recuperaciones tienen que medirse; todavía está pendiente implementar eléctricamente el rearme W37.

## Reproducción y evidencia

Desde `research/2026-10-28-independent-wpt-sensor-v01/w_ind_40/`:

```sh
python3 -m unittest -v test_w40_common_mode
python3 w40_common_mode.py --out W40_EVIDENCE.json
```

- 17/17 tests Python 3.11 PASS en entorno de cálculo aislado el 30/10/2026.
- JSON determinista reproducible, `schema=VALDO_W40_FAULT_TREE_V1`, siempre `safe_to_energize=false` y `hardware_qualified=false`.
- Escenarios adversariales: pérdida de alimentación, shunt puenteado, alarma abierta, monitor silenciado, ruta de reset interrumpida, dos cortes soldados, supervisor alimentado por rail incorrecto o bloqueado en saludable.
- Inyección negativa: un supervisor que se alimenta de la misma línea 3,3 V averiada **no obtiene crédito** como protección independiente.
- Dependencias: solo biblioteca estándar Python; no se ejecuta diseño externo ni se copia código/circuito de terceros.

## Puertas de seguridad y trabajo que NO cubre

1. **No existe esquema KiCad para el supuesto supervisor independiente**. Elegir componentes exige ficha del fabricante, condiciones válidas con alimentación parcial y salida realmente baja durante pérdida/retorno, tolerancias, supervisión 3,3 V desde 5 V, salida hacia ambos eFuses, compatibilidad del pin MR_N/PG, test de retroalimentación, tiempo y energía residual; revisar ERC, netlist y luego simulación eléctrica real.
2. Un shunt puenteado es un fallo único aún no detectado. No atribuir redundancia física a dos o tres INA que comparten ese elemento. Debe estudiarse un mecanismo diverso de detección, sin asumir que medir la entrada TX basta para FOD.
3. El modelo presupone sobrecorriente ya por encima del umbral y disparo instantáneo sin analogía, tolerancias, cargas reactivas o energía almacenada. Un corte soldado de cada rama simultáneamente deja camino. No mide calor, humedad, metal, desplazamiento, EMI, bobinas, UART/radio, falsos positivos, envejecimiento ni un banco real.
4. Se mantienen **tres sistemas separados**: dock/carga (sin litio ni estación real), energía inductiva de módulos (primer piloto solo sensor de poca potencia y carga ficticia), y datos (ESP-NOW u OpenThread, ACK de aplicación, CRC, secuencia, timeout, privacidad y recuperación). Ningún paquete RF concede permisos de parada crítica. WISP solo micro-sensores pasivos intermitentes.
5. Sin electricidad física, compras, impresión 3D, soldadura ni maquinaria intervenida. Ninguna afirmación de protección homologada o dispositivo listo para fabricar.

## Matriz BOM: Diotronic auxiliar y alternativas

Consulte `BOM_W_IND_40.csv`. No se añade material a la arquitectura aprobada: incremento de BOM **0,00 €**, porque el hito descarta el tercer INA compartido, no porque un equipo funcional cueste cero. El hipotético supervisor requiere selección y presupuesto completo. Diotronic [resistencia axial 10351 10 kΩ 1 W](https://diotronic.com/resistencias-de-carbono-1w/16309-resistencia-10k-5-1w) anuncia **0,15 € IVA incluido, MOQ 5, stock web disponible**, pero **NO** es automáticamente sustituible por una 0805 SMD. Stock **físico en Zaragoza no confirmado**. No consta una referencia local equivalente trazable para componentes críticos. TME/Mouser/DigiKey y fabricante, sin precios inventados, seguirán como alternativa trazable y cualificada.

## Auditoría de autorías, HEAD y PR, 30/10/2026

Los cinco repositorios oficiales externos se consultaron, sin copiar código ni editar clones (la nota maestra `19-alternativas...` contiene los SHAs fijados 28/10):

| Autor/ámbito y licencia declarada | rama y HEAD verificados | comparado con SHA registrada y estado útil de PR |
| --- | --- | --- |
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, potencia WPT | master `7c7858c0dd7040801b6f191df1396115560218f0` | igual al pin; autor demuestra 81,3 % a 1–2 mm **en su prototipo** y carece de realimentación RX→TX; no se importa su CAD/GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause, RFID | master `08332bc398aa3350d351ef2aaac163f8007cffda` | igual al pin; no se adopta para sensor siempre activo |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause, RFID firmware | **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` | `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`: diverge **68 ahead, 11 behind**; PR #40 `Information update` sigue abierta, no integrar otra rama por orden de nombres |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0, datos | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | igual al pin; PR #153 cerrada **sin merge**; ACK MAC no equivale ACK aplicación |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause, datos | main `e577777c308f6c87e5da3056239231a8fc147cb2` | +14 commits respecto `7009584dadc20cf20c20a6062f357dd572ba6885`; PR #13822 abierta, no integrada; no cambio de arquitectura RF por esta PR |

OOMWOO oficial [makerspet/oomwoo](https://github.com/makerspet/oomwoo) `main=f01a1b295f462da5ab8d5f021a3f741cbd2b47df`; no se editan fuentes del creador. PR upstream #79 `cleaning-jobs` sigue **abierta pero fuera de ámbito W**. VALDO PR #9 es propiedad de Valdi320 y sólo se modifica el directorio nuevo W-IND-40 + workflow. Los archivos locales de VALDO y `VALDO_OOMWOO` se inspeccionaron **solo lectura**; el repositorio local VALDO estaba sucio con trabajo de otros autores y **no se utilizó** para modificar archivos. Automatizaciones mecánicas OEM pausadas; ninguna activa con escritura solapada. Fuente y límites: [INA301](https://www.ti.com/product/INA301), [TPS3840](https://www.ti.com/product/TPS3840), [TPS25947](https://www.ti.com/product/TPS25947), [GPL simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power/blob/master/LICENSE), documentación propia [W39](../w_ind_39/README_W_IND_39.md).

**Próximo hito solo si procede:** comparar en papel candidatos documentados de supervisor por rail diferente, calcular márgenes/tolerancias y hacer el esquema KiCad **normalmente apagado** con pruebas de alimentación parcial. Cualquier banco posterior requiere protocolo de seguridad y autorización; no conectar BMS, litio, motores o estación real.
