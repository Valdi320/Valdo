# W-IND-39 — comparador de sobrecorriente redundante en dos rutas de apagado (KiCad; experimental)

Fecha: 30/10/2026. Ámbito propio W, **robot abierto NUEVO**. No trasplante Xiaomi, no baterías/BMS/cargador/dock conectados; **NO FABRICAR / NO ENERGIZAR**.

## Mejora y criterio de aceptación

W38 enviaba exclusivamente la alarma de U1 INA301 al MR_N del supervisor U4. Si U1 quedaba mudo (pin VDD roto, componente averiado, ALERT abierto) pero el rail 3,3 V general permanecía correcto, la rama U4 no detectaba la sobrecorriente. **W39 propone** un segundo INA301A1 (U12) vigilando la misma resistencia Kelvin con su LIMIT independiente y condensador de desacoplo propio. Su ALERT_N tiene pullup 10 kOhm al rail de 5 V, y conduce **U9.MR_N**; U1 sigue conduciendo **U4.MR_N** mediante pullup a 3,3 V. Ambos PG llegan a dos AND de reset y dos AND de habilitación preexistentes. No se juntan directamente salidas push-pull de tensiones distintas.

Resultado buscado, exclusivamente lógico: **una sola avería silenciosa de monitor, un ALERT abierto o una ruta de reset averiada no deben dejar activados los dos cortes durante sobrecorriente**, suponiendo que la otra rama y los elementos compartidos funcionen. Se requieren ambos caminos para permanecer permitidos; un único disparo obliga CLR_N a bajo en ambos biestables. No depende de radio.

Es un progreso respecto a W38, no una solución completa. Simular un fallo de un chip de manera booleana NO prueba detección eléctrica real, ni consumo, ni el margen de umbral, ni la propagación hasta OUT. El código y el esquema son originales de VALDO; no hay código/CAD reutilizado de los cuatro terceros.

## Reproducir

Desde w_ind_39:
- python3 generate_w39.py; python3 generate_w39.py --verify
- python3 -m unittest -v test_w39
- python3 fault_model_w39.py --out native_out/w39_faults.json
- En CI, KiCad 9.0.2 exporta ERC JSON y netlist XML. netlist_gate_w39.py coteja todos los pines, referencias y no-conectados; las mutaciones negativas deben ser rechazadas. El esquema se guarda en el artefacto W39, sin alteración de W38.

**Sin prueba física y sin huella PCB validada.** ERC=0 solo acredita coherencia eléctrica estática de esa representación, no que un chip defectuoso apague antes de dañarse. No hay SPICE transitorio ni caracterización real. No se confirma disponibilidad del rail externo ni de las bobinas.

## Matriz de decisión y defectos no resueltos

| Candidato | Fallo silencioso único (modelo ideal) | Riesgos comunes | Coste incremental |
| --- | --- | --- | --- |
| W38, solo U1->U4 | NO cubierto | shunt, VDD, U4, cortes | 0 componente |
| W39, U1->U4 y U12->U9 | Cubierto **en modelo** si la otra rama funciona | **shunt común, VDD 3,3 V común, nodos CLR, carga, ambos cortes, tensiones transitorias** | +1 INA301, +2 resistencias / condensador (ver BOM) |
| Comparadores realmente diversos con fuente aislada | Por investigar | requiere otro proyecto y coste | No calculado |

Las 64 combinaciones del pequeño modelo representan únicamente seis entradas binarias; **no son 64 modos físicos de fallo**. Se conservan contraejemplos donde las dos alarmas quedan mudas o la resistencia Kelvin queda puenteada: el circuito aún permitiría una corriente perjudicial. La independencia no alcanza al shunt, la fuente 3,3 V, las pistas, los eFuses ni a las bobinas. La resistencia de pullup a 5 V está dentro del máximo de ALERT del INA301 (5,5 V según TI) **solo nominalmente**: fugas, condiciones sin VDD, umbrales MR_N y retardo deberán verificarse en hardware. RESET de ambos INA301 queda alto (modo latch), por lo que un disparo exige un proceso de recuperación **aún no diseñado**.

El W37 de liberación antes de rearme sigue en código, **no está implantado eléctricamente**. También faltan FOD metálico, sensor térmico, offset, EMI, humedad, UVLO de todos los raíles, latencia de apagado, tolerancia real 346 mA y la antigua CI ERC W18. No aprobar motor/bomba ni litio. Dock de carga, WPT distribuido y radio son tres sistemas **distintos**. ESP-NOW u OpenThread siguen alternativas de datos con ACK/CRC/secuencia/timeout/privacidad que no pueden controlar este corte; WISP solo microsensores intermitentes.

## Coste, mantenibilidad y fuentes

DigiKey España muestra el **INA301A1IDGKR** en cinta cortada MOQ 1 a 2,77 EUR sin IVA (aprox. 3,35 EUR con 21 % IVA), stock online 4225 al consultar el 30/10/2026, sin reservar ni añadir transporte. Ver https://www.digikey.es/es/products/detail/texas-instruments/INA301A1IDGKR/6571979 . Componentes R3/R4/C7 y montaje aún sin cotización; el precio total no está cerrado. Diotronic Zaragoza no tiene disponibilidad confirmada; para R3 existe antecedente de pasivo axial de catálogo, **no compatible sin rediseñar la PCB SMD**, y no justifica cambiar la arquitectura. Para funciones críticas, fabricante TI y distribuidores trazables antes de prototipar. Ninguna compra.

Fabricante: https://www.ti.com/product/INA301 (salida ALERT open-drain, alimentacion 2,7–5,5 V, max 700 uA). https://www.ti.com/product/TPS3840 (supervisores), https://www.ti.com/product/TPS25947 (interruptores), https://www.ti.com/product/SN74LVC1G74 . Estos son **datos declarados por fabricante**, no mediciones de VALDO.

Ramas revisadas el 30/10/2026 contra SHA del maestro 19:
- mark-belbin/simple-wireless-power, GPL-3.0 master **7c7858c0dd7040801b6f191df1396115560218f0**, sin cambio; PR #1 fusionada, referencia WPT sin realimentación.
- wisp/wisp5-hw, BSD-2-Clause master **08332bc398aa3350d351ef2aaac163f8007cffda**, sin cambio; PR #1 histórica.
- wisp/wisp5, BSD-2-Clause **640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2**, diverge de d978a6978ad23ccd6c44dd55430973b04a3d4a9b (+68/−11); PR #40 aún abierta, no usar orden de ramas para inferir actualidad.
- espressif/esp-now, Apache-2.0 master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, sin cambio; PR #153 cerrada sin fusionar.
- openthread/openthread, BSD-3-Clause main **e577777c308f6c87e5da3056239231a8fc147cb2**, +14 commits respecto 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13822 abierta y no incorporada.
- makerspet/oomwoo oficial main **f01a1b295f462da5ab8d5f021a3f741cbd2b47df**; VALDO PR #9 propia, OOMWOO PR #79 cleaning-jobs ajena al ámbito W, intacta. VALDO_OOMWOO y clones upstream intactos. Otros agentes y automatizaciones sin ámbitos de escritura superpuestos.

## Puerta siguiente: optimización y ensayos antes de más circuitos

Primero validar exclusivamente **en digital** este esquema completo y verificar que el incremento de coste y modos comunes compensa. Después, con protocolo de seguridad y autorización separada, proponer ensayo de banco con fuente aislada y carga ficticia, instrumentando ambos ALERT/MR, ambos PG/EN, corriente/temperatura y defectos simples. **No se ha realizado ese ensayo ni solicitado energizar**. Si no hay hardware ni medidas de corriente, suspender nuevas ampliaciones redundantes y conservar una alternativa por cable seguro y reparable. La redundancia no equivale a cualificación funcional.
