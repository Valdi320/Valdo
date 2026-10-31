# W-IND-70 — Auditoría nativa del inventario de descarga después del segundo corte

**31/10/2026 · VALDO ámbito W, robot aspirador NUEVO, sin trasplante Xiaomi.** Código y pruebas originales. No editar esquemas W15/W21/W22, fuentes de autores, C/Codex, OOMWOO o PR #79. **Solo revisión digital: ninguna batería, BMS, cargador, estación, placa o motor conectado.**

## Hallazgo material y corrección

W68/W69 calculan la energía de *capacitores hipotéticos*, pero **el esquema propio W21** que realmente tenemos versionado carece de inventario explícito de condensadores y cargas TX externas. Un cálculo de un capacitor asumido no prueba que el transmisor se descargue ni que existan dos resistencias útiles tras los cortes.

El nuevo guardia ejecuta el auditor **exacto W22 sobre un netlist XML exportado por KiCad 9.0.2**, identifica las conexiones de R1/R2 y **bloquea sistemáticamente toda calificación de descarga**. Distingue:

- **R1 = 22 kΩ entre MID y GND**, nodo entre interruptores U1 y U2: NO descarga directamente el transmisor después del segundo corte.
- **R2 = 1 kΩ entre TX_5V_CUT y GND**, único bleeder representado directamente en esa red.
- **R3/R4 = 100 kΩ entre EN_A/EN_B y GND**: pull-downs de habilitación, NO descargan el TX.
- Fuente **J1 solo declarativa**. Cero capacitores/inductores dibujados, lo cual **NO SIGNIFICA cero capacitancia/energía física**. Bobinas, condensadores resonantes, PCB externa, acoplos, alimentación inversa y parásitos no tienen inventario.

Si cualquier componente o terminal cambia, la lista estricta W22 rechaza la exportación como BLOCKED_UNREVIEWED_NETLIST: no asigna automáticamente capacidades cero. Si coincide el dibujo, la salida es BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED, **no un permiso eléctrico**, independientemente del valor simulado por W69.

### Cuantificación nominal SOLO hipotética

Si R2 estuviese realmente a 5,0 V permanentes, serían **5 mA, 25 mW, 0,6 Wh por 24 h**; R1 22 kΩ en MID a 5 V sería ~1,136 mW. No se ha medido funcionamiento continuo, eficiencia ni standby del robot. Con **100 µF ficticios, 5 V iniciales y pantalla ficticia 0,5 V**: R2=1 kΩ daría 0,23026 s; sustituirla teóricamente por 10 kΩ bajaría la pérdida nominal a 2,5 mW pero aumentaría el tiempo a 2,30259 s. **No cambiar R2** sin medir C, energía, alimentación inversa, tensión de carga, temperatura y consecuencias de fallo abierto/corto. Umbral 0,5 V no es norma de seguridad. El tiempo de descarga del robot sigue DESCONOCIDO.

## Verificación reproducible

Desde el directorio research/2026-10-28-independent-wpt-sensor-v01:

- Tests sintéticos originales: python3 -m unittest discover -s w_ind_70 -p 'test_w70.py' -v (**19 casos**, con mutaciones de red, valor, capacitor extra, fuente, puente, falsos valores y CLI).
- Workflow .github/workflows/w-ind-70-storage-inventory.yml: imagen **kicad/kicad:9.0.2**, exporta **de verdad** el esquema W21 a XML, aplica nuestro W22 y W70 y archiva **XML + JSON SHA256**. El test de revisión PASS significa **detección correcta del bloqueo**, no hardware aprobado. El archivo w70_review.json informa hardware_approved=false, physical_tests=0, power_on_allowed=false, residual_discharge_qualified=false. Ante un esquema modificado inesperadamente, el workflow falla. La evidencia CI específica debe consultarse tras el push; la ejecución local con fixtures no acredita KiCad.
- Sin instalación de servicios ni piezas físicas; no hay SPICE de componentes reales, placa, metal/FOD, EMI, temperatura, humedad, offset, envejecimiento o descarga medida.

## Matriz de decisión

| Problema / opción | Retorno | Decisión |
|---|---|---|
| **Dock carga** con batería y BMS | Gran potencia y protecciones FOD/temperatura/EMI y cargador independiente | **Fuera del piloto**; litio, estación y BMS desconectados |
| Potencia sensor 5V/0,4W media, 1,5W pico (presupuesto **hipotético**): WPT simple | Barato en principio, carece de regulación/reacción autónoma demostrada | No adoptar: falta eficiencia/gap/offset/FOD/corte |
| WPT regulado con protección independiente + bleeder | Mejor control y reparación potencial | Solo estudio; faltan piezas documentadas, retorno económico, corte y medición |
| Bleeder R2 en TX vs R1 en MID | Identificar descarga físicamente representada y cuantificar pérdida nominal | **Implementada auditoría digital**; no aprobar hardware ni sustituir resistencias |
| RF datos ESP-NOW vs OpenThread | ACK aplicativo, CRC, sesión/secuencia, timeout, privacidad, recuperación | Alternativas, no potencia; nunca paro crítico sobre radio |
| WISP5 | Micropotencia RFID con lector | Solo microsensores con consumo medido que justifique su coste |
| WPT motores/bombas | Pérdidas y picos desconocidos | Excluido hasta medición |

## Fuentes, autoría y límites actualizados (consultados el 31/10/2026)

Pines registrados 28/10 en 19-alternativas, contrastados con rama HEAD/PR de sus autores: [Mark Belbin / simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0 **igual**; su 81,3 % es dato propio del autor, no del robot. [WISP hardware](https://github.com/wisp/wisp5-hw) BSD-2 master 08332bc398aa3350d351ef2aaac163f8007cffda **igual**; [WISP firmware](https://github.com/wisp/wisp5) BSD-2 rama **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2, **diverge 68 ahead/11 behind** de d978a6978ad23ccd6c44dd55430973b04a3d4a9b, PR #40 antigua abierta. [Espressif esp-now](https://github.com/espressif/esp-now) Apache-2 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 **igual**, PR #151/#153 cerradas 2026. [OpenThread](https://github.com/openthread/openthread) BSD-3 main b6d0f06db304055f5866ff6e3c67370b54c81b15, **18 ahead** del pin 7009584dadc20cf20c20a6062f357dd572ba6885, cambios octubre 31 radio/IPv6/DHCP/CLI, PR #13821/13822 abiertas. No se copia código/CAD de estos autores.

[OOMWOO oficial](https://github.com/makerspet/oomwoo) main f01a1b295f462da5ab8d5f021a3f741cbd2b47df; [oomwoo-one](https://github.com/makerspet/oomwoo-one) jazzy a630d1c77255072d280a2a41a7a2bd1a1c98cadd. VALDO PR #9 propia W abierta. Los documentos maestros del 28/10, D22, coordinación W/C, VALDO_OOMWOO/LEEME_PRIMERO y WPT_DATOS_V01 se leyeron previamente. OOMWOO #79 es trabajo cleaning-jobs ajeno a esta mejora, no se modifica.

## BOM (véase BOM_W_IND_70.csv)

**Cero componentes hardware nuevos**, no significa que el robot cueste cero. R1=22k/R2=1k/R3/R4=100k y TPS22918 aparecen SOLO en esquema W21 no cualificado. No sustituir por similares sin revisión de voltaje, corriente inversa, potencias y calores. **Diotronic proveedor auxiliar**, referencia exacta, stock Zaragoza, IVA, portes, MOQ y diferencia TME/Mouser/DigiKey **pendientes**; nada comprado. Componentes críticos de seguridad exigen trazabilidad. No declarar instalado o validado.

**Siguiente puerta:** inventariar desde esquema electrónico completo / referencias de fabricantes los C, L y todos los nodos después de U1/U2, medir el caso real solo en banco aislado autorizado con carga resistiva, caracterizar corto/abierto de bleeder, anti-retorno, doble soldadura, FOD, termometría, offset y EMI. El **ERC antiguo W18 sigue FALLANDO** y no se silencia. No hay autorización de energización, fabricación ni litio.
