# Anexo 06 — Inventario ampliado de repuestos del robot Xiaomi X20 Pro D102GL

**Fecha de consulta: 25 de octubre de 2026.**

Ampliación del inventario de repuestos del robot. Excluye la estación, los consumibles y los elementos ya recogidos en la tabla principal, salvo referencias alternativas necesarias para explicar una misma función.

## Alcance y evidencia

Este anexo identifica **repuestos comerciales y alternativas**, no una BOM de fabricación ni una lista de componentes comprobados físicamente en la unidad del usuario. Por ejemplo, las diferentes unidades LDS son opciones alternativas; no significa que el robot lleve varios LiDAR.

- **E2 — ficha propia:** se abrió la ficha individual del vendedor y su descripción o árbol de compatibilidad declara X20 Pro. Es evidencia comercial directa, no una prueba independiente de montaje o rendimiento.
- **E2 — solo catálogo:** la referencia aparece en el catálogo filtrado para X20 Pro BHR8859EU, pero en esta ampliación no se confirmó Pro en el contenido de su ficha individual. Se conserva ese límite expresamente.
- Los números de cinco dígitos son **SKU de PC:MediaStore**, no referencias OEM universales. Las identificaciones impresas de motores, placas o flex se separan del SKU.
- Las menciones a “cámara” reproducen la denominación del vendedor. **No demuestran que la óptica frontal sea una cámara RGB**, ni que permita obtener vídeo.
- Los precios son observaciones orientativas; las fichas indican IVA incluido y transporte aparte. No se realizó checkout ni se validó el total para un destino concreto.

Fuentes del inventario:

- [Catálogo Pro, página 1](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html).
- [Catálogo Pro, página 2](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html?page=2).

## 1. Actuadores, sensores y placas

| Elemento | SKU y fuente | Evidencia | Qué confirma y límites |
|---|---|---|---|
| Motor y reductora del cepillo principal | [11965](https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-gy-p-11965.html) | **E2 — ficha propia** | Incluye Pro. Motor **PRI-390SV-24100**, reductora y cable; 53,99 €. La PN es del motor y no necesariamente del conjunto completo. |
| Variante negra del motor/reductora principal | [56231](https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-schwarz-p-56231.html) | **E2 — solo catálogo** | Misma PN de motor indicada por el catálogo. Descatalogada. Alternativa de la función anterior, no otro motor adicional instalado. |
| Caja del cepillo principal con motor, negra | [73385](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-x20-p-73385.html) | **E2 — ficha propia** | Incluye Pro. Caja y motor, sin rodillo ni tapa; 39,99 €. Es un conjunto que se solapa con el motor/reductora individual. |
| Caja del cepillo principal, gris | [46648](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-grau-l10-x10-x20-p-46648.html) | **E2 — solo catálogo** | Conjunto alternativo, 51,99 €. Comparar qué elementos se suministran y su geometría con el original. |
| Caja del cepillo principal reacondicionada | [56222](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-refurbished-p-56222.html) | **E2 — solo catálogo** | 25,99 €; la descripción incluye rodillo y tapa. Su estado es reacondicionado, no nuevo. |
| Motor del cepillo lateral | [55856](https://www.ep-mediastore-ab.de/dreame-seitenbuerstenmotor-schwarz-p-55856.html) | **E2 — ficha propia** | Incluye Pro. **PR-500EV-14440**, reductora, cable de dos conductores y conector de tres posiciones; 19,98 €. El título Dreame no excluye la compatibilidad Pro declarada en el árbol. |
| LiDAR completo, naranja | [42740](https://www.ep-mediastore-ab.de/xiaomi-lds-einheit-wpftb-v262-orange-p-42740.html) | **E2 — ficha propia** | Incluye Pro. Unidad con motor, correa y placa **X-WPFTB-V2.6.2**; 71,99 €. No identifica necesariamente la revisión montada de fábrica en el robot del usuario. |
| Sensor inferior delantero | [42075](https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-vorn-s10-etc-p-42075.html) | **E2 — ficha propia** | Incluye Pro. Un sensor anticaída delantero para posición derecha o izquierda; cable aproximado de 6 cm y cuatro polos; 9,20 €/ud. No es el juego completo de sensores. |
| Sensor inferior lateral | [55018](https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-s10-etc-p-55018.html) | **E2 — ficha propia** | Incluye Pro. Un sensor anticaída lateral para derecha o izquierda; cable aproximado de 13 cm y cuatro polos; 8,99 €/ud. Distinguir del delantero por ubicación y arnés. |
| Paragolpes completo blanco con óptica | [70759](https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-weiss-s20-x20pro-p-70759.html) | **E2 — ficha propia** | Incluye Pro. Paragolpes, módulo óptico frontal, IR lateral, moldura inferior y tornillos; 77,99 €. El término comercial “cámara” no acredita un sensor RGB. |
| Paragolpes completo negro con óptica | [58034](https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-schwarz-s20-x20max-p-58034.html) | **E2 — solo catálogo** | Alternativa del conjunto anterior, 95,99 €. El catálogo Pro lo incluye; no es otro paragolpes instalado simultáneamente. |
| Bloque óptico frontal central | [50096](https://www.ep-mediastore-ab.de/xiaomi-front-kamera-fuer-bumper-s20-x20max-p-50096.html) | **E2 — ficha propia** | Incluye Pro. **ALF02-S-TB_V1.0**, flex **B108EU_FPC CAM VC1**, situado en el centro del paragolpes. **Descatalogado individualmente**. No inferir prestaciones de imagen por el nombre. |
| Sensor óptico/IR derecho del paragolpes | [52012](https://www.ep-mediastore-ab.de/xiaomi-ir-sensor-rechts-fuer-bumper-s20-x20max-p-52012.html) | **E2 — ficha propia** | Incluye Pro. Posición derecha, flex **B108EU_FPC PSD VC1**. **Descatalogado individualmente**. Distinto del sensor IR central 89488. |
| Placa de interconexión de la óptica frontal | [53002](https://www.ep-mediastore-ab.de/xiaomi-camsub-board-fuer-bumper-s20-x20max-p-53002.html) | **E2 — ficha propia** | Incluye Pro. **B108_CamSub**, flex **B108EU_FPC MAIN VB1**; conecta la óptica central y el sensor derecho. **Descatalogada individualmente**. |
| IR central detrás del paragolpes | [89488](https://www.ep-mediastore-ab.de/xiaomi-bumper-ir-sensor-kabel-b108eu-p-89488.html) | **E2 — ficha propia** | Descripción y compatibilidad incluyen Pro. **B108EU_IR**, con cable; 3,58 €. Componente distinto de 50096 y 52012. |
| Sensor de presencia del depósito de polvo | [70969](https://www.ep-mediastore-ab.de/xiaomi-dustbin-sensor-kabel-b108eu-p-70969.html) | **E2 — ficha propia** | Incluye Pro. Hall **B108EU_HALL** con cable; 9,51 €. Es del depósito del robot, no de los tanques de agua de la estación. |
| Placa de los dos botones superiores | [13988](https://www.ep-mediastore-ab.de/xiaomi-bedienboard-kabel-b108eu-p-13988.html) | **E2 — ficha propia** | Incluye Pro. **B108EU_SWITCH**, placa de dos pulsadores con cable; 10,99 €. Separada de las piezas plásticas de los botones. |
| Placa de reset/Wi-Fi y conmutador LDS | [63078](https://www.ep-mediastore-ab.de/xiaomi-reset-board-btn-b108eu-p-63078.html) | **E2 — ficha propia** | Incluye Pro. **B108EU_WIFI_LED** y **B108EU_LDS_SW**, con cable; 15,99 €. El nombre no aporta esquema ni función eléctrica detallada del conmutador LDS. |
| Altavoz | [68441](https://www.ep-mediastore-ab.de/xiaomi-dreame-lautsprecher-36mm-p-68441.html) | **E2 — solo catálogo** | Asociado a Pro; 36 mm, 8 Ω, cable y conector de dos polos; 0,94 €. No hace falta sustituirlo para rediseñar sus soportes. |

## 2. Piezas mecánicas y arneses

| Elemento | SKU y fuente | Evidencia | Qué confirma y límites |
|---|---|---|---|
| Palancas y muelles del paragolpes | [32363](https://www.ep-mediastore-ab.de/dreame-bumper-feder-hebel-p-32363.html) | **E2 — ficha propia** | Incluye Pro. Palancas izquierda/derecha con muelles y tornillos. **Son del paragolpes, no ganchos de suspensión de las ruedas.** |
| Cubierta de la torre LDS y sus muelles | [88027](https://www.ep-mediastore-ab.de/xiaomi-lidar-deckel-feder-weiss-x10-s10-s20-p-88027.html) | **E2 — ficha propia** | Incluye Pro. Tapa protectora con tornillos y muelles; 10,11 €. |
| Bastidor/soporte LDS | [26977](https://www.ep-mediastore-ab.de/dreame-lds-bracket-rahmen-l10s-ultra-gen3-l40spu-d20-p-26977.html) | **E2 — solo catálogo** | Soporte de la unidad de navegación, **no el chasis general**. Cotejar la revisión y geometría instaladas. |
| Platos portamopas | [18142](https://www.ep-mediastore-ab.de/xiaomi-2x-mop-halter-teller-schwarz-x20max-pro-5pro-p-18142.html) | **E2 — ficha propia** | La ficha identifica Pro/Max. Dos soportes rígidos de mopa con sujeción magnética; distintos de los paños consumibles. |
| Depósito de polvo del robot | [50066](https://www.ep-mediastore-ab.de/xiaomi-staubbehaelter-x20-pro-weiss-p-50066.html) | **E2 — ficha propia** | Identificado expresamente como Pro, sin filtro; 59 €. Útil para conservar conductos y sellado al rediseñar. |
| Manguito de la turbina | [66031](https://www.ep-mediastore-ab.de/xiaomi-gummi-tuelle-filter-x20pro-p-66031.html) | **E2 — ficha propia** | Identificado como Pro. Manguito de goma con espuma de prefiltro; 4,64 €. Conjunto de sellado y conducción de aire. |
| Botones de plástico superiores | [78444](https://www.ep-mediastore-ab.de/xiaomi-bedienknoepfe-x20pro-p-78444.html) | **E2 — ficha propia** | Identificados como Pro; 4,64 €. Piezas de accionamiento, distintas de la PCB 13988. |
| Tapas superiores negras | [26811](https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-schwarz-s20-x20max-p-26811.html) | **E2 — ficha propia** | Pro incluido en compatibilidad. Alternativa de color a 29986, ya recogida en el inventario principal. **No es una nueva pieza estructural.** |
| Arnés de la turbina | [35389](https://www.ep-mediastore-ab.de/xiaomi-saugmotor-kabel-4pin-42cm-p-35389.html) | **E2 — solo catálogo** | Catálogo Pro: cuatro polos y longitud aproximada de 42 cm. No deducir pinout por colores. |
| Arnés LDS | [72988](https://www.ep-mediastore-ab.de/xiaomi-dreame-lds-kabel-9cm-p-72988.html) | **E2 — solo catálogo** | Catálogo Pro: longitud aproximada de 9 cm; tres conductores y conectores de cuatro posiciones según descripción. Cotejar con el arnés real. |

## 3. Alternativas y despiece LDS por revisión

**Estas referencias no deben sumarse como varios sensores instalados.** La tienda presenta varias unidades completas y componentes internos asociados al modelo Pro. Su compatibilidad comercial no identifica la referencia original de cada robot ni demuestra que las placas internas de diferentes unidades LDS puedan mezclarse.

| Referencia | Fuente | Evidencia para Pro | Interpretación |
|---|---|---|---|
| **77339**, unidad completa X-WPFTB-V2.6.2 negra | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftb-v262-schwarz-p-77339.html) | **E2 — solo catálogo** | Alternativa a la unidad naranja 42740. |
| **26720**, unidad completa negra | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-lidar-sensor-l10s-pro-ultra-heat-l20-x30-x40-mova-p-26720.html) | **E2 — ficha propia** | Pro incluido en el árbol de compatibilidad. No equivale a identificar la unidad de fábrica. |
| **41867**, unidad completa D-WPFTBCD-V1.0.1 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftbcd-v101-p-41867.html) | **E2 — ficha propia** | Pro incluido. Otra opción comercial de conjunto completo. |
| **13034**, unidad denominada Deebot Mini LDS | [Ficha](https://www.ep-mediastore-ab.de/deebot-mini-lidar-sensor-lds-schwarz-p-13034.html) | **E2 — ficha propia** | Aunque el título sea de otra marca/modelo, el árbol incluye Pro. No demuestra revisión original ni equivalencia de piezas internas. |
| **27165**, motor LDS V2 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-motor-v2-l10s-pro-ultra-heat-l20-x30-p-27165.html) | **E2 — ficha propia** | Pro incluido; seleccionar según la torre conservada. |
| **54774**, motor LDS | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-motor-l10s-pro-ultra-heat-l20-x30-x40-p-54774.html) | **E2 — ficha propia** | Pro incluido; alternativa por versión, no segundo motor de navegación instalado. |
| **58751**, correa LDS | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-riemen-l10s-pro-ultra-heat-l20-x30-original-p-58751.html) | **E2 — ficha propia** | Pro incluido; cotejar con la unidad LDS concreta. |
| **27164**, Transfer-Board V2 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-transfer-board-v2-schwarz-p-27164.html) | **E2 — solo catálogo** | Placa interna de una revisión LDS; no elegir solo por modelo de robot. |
| **40871**, Laser-Board V2 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-laser-board-v2-schwarz-p-40871.html) | **E2 — solo catálogo** | Placa interna; verificar revisión y conectores. |
| **42267**, placa X-WPFTB-V2.6.2 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-board-wpftb-v262-gruen-p-42267.html) | **E2 — solo catálogo** | Identificación de placa; no trasladar a cualquier torre alternativa. |
| **66896**, placa D-VPower-V.2.0.4 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-board-vpower-v204-gruen-p-66896.html) | **E2 — solo catálogo** | Otra referencia de placa LDS. No prueba intercambiabilidad interna con 42267. |
| **50112**, carcasa para X-WPFTB-V2.6.2 | [Ficha](https://www.ep-mediastore-ab.de/dreame-lds-gehaeuse-fuer-wpftb-v262-p-50112.html) | **E2 — solo catálogo** | Carcasa interna de la torre LiDAR, no del robot. |
| **27166**, carcasa para unidad 26720 | [Catálogo página 1](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html) | **E2 — solo catálogo** | La apertura de su ficha individual dio error. Solo se conserva la asociación publicada por el catálogo. |

## 4. Implicaciones para el inventario físico y el rediseño

1. **No se identificó una “placa única de sensores inferiores”.** Lo que estas páginas venden son bloques anticaída individuales delanteros y laterales. No inventar una PCB conjunta a partir de esa lista.
2. **Conservar la óptica y los flex sanos tiene valor práctico:** 50096, 52012 y 53002 están descatalogados individualmente, mientras el paragolpes completo 70759 sigue disponible. Esto describe disponibilidad comercial observada; no pronostica su evolución.
3. **Mantener conjuntos funcionales completos reduce ambigüedad:** conservar la torre LDS original con su motor, placas, correa y arnés evita tener que validar combinaciones internas de distintas revisiones.
4. **Los muelles 32363 no resuelven el anclaje de rueda:** pertenecen a las palancas del paragolpes.
5. **El soporte 26977 y las carcasas 50112/27166 no son chasis generales.** No aportan evidencia de una carcasa estructural Pro completa disponible.
6. Esta documentación permite identificar interfaces para medir y preservar, pero **no suministra cotas, tolerancias, pinouts, cargas ni geometría CAD verificadas**. Esos datos requieren inspección del robot real.

