# Materiales imprimibles y elección de taller · 23/10/2026

**Resultado:** no se ha identificado un único material doméstico que sustituya todas las funciones de plásticos rígidos, gomas, metales, vidrio y cerámica. Sí se puede ampliar mucho la variedad de piezas combinando unas pocas familias y procesos. La silicona es una candidata para determinadas piezas elásticas; no se adopta como materia universal. Sigue elegida como arquitectura de estudio **FDM abierta + moldes + reparación convencional**. No se compra máquina ni se acredita una fábrica autosuficiente.

Convenciones: **[D]** documentado; **[I]** inferencia; **[P]** propuesta; **[A]** pendiente. Fuentes enlazadas directamente y recogidas en [FUENTES.md](FUENTES.md). [Registro de revisión y cálculo](datos/materiales_imprimibles_taller_2026-10-23.json). La producción doméstica de la materia se estudia por separado en [el anexo específico](MATERIAL_DOMESTICO_AJUSTABLE.md).

## 1. Qué se puede imprimir hoy

**[D]** La guía de filamentos de Prusa distingue PLA, PETG, ABS/ASA, PC, PA, flexibles y materiales con cargas, con requisitos diferentes de secado, boquilla y cámara. **[I/P]** La tabla traduce esas familias a una primera selección de usos, sin validar piezas concretas. No significa que cualquier impresora admita todos los materiales. [Guía del fabricante](https://help.prusa3d.com/filament-material-guide).

| Lo que necesitamos | Familias o proceso que comparar | Límite que cambia la elección |
|---|---|---|
| Rígido, fácil para modelos y útiles sencillos | PLA, FDM | La facilidad de impresión no acredita resistencia térmica o duración exterior |
| Carcasas y piezas funcionales de uso general | PETG, FDM | Verificar carga sostenida y temperatura |
| Piezas expuestas o que requieren otras prestaciones térmicas | ASA/ABS, FDM con condiciones apropiadas | Seleccionar el grado y acondicionar el espacio |
| Goma flexible y amortiguación | TPU/TPE, FDM compatible | Dureza, alimentación del filamento y comportamiento con carga |
| Piezas técnicas con exigencias específicas | PA, PC y formulaciones reforzadas | Secado, temperatura, desgaste y propiedades por orientación |
| Juntas y piezas elásticas de silicona | Moldeo o impresión especializada de silicona | Curado, formulación y compatibilidad; no es un filamento FDM corriente |
| Piezas cerámicas | Extrusión de pasta cerámica y proceso posterior | Preparación, secado y cocción, según producto |
| Piezas metálicas | Procesos metálicos o mecanizado | No se obtienen las propiedades del metal solo por añadir polvo a un plástico |

**[D]** WASP documenta extrusión de arcilla, gres y porcelana y describe el proceso cerámico posterior en sus demostraciones. Es otra cadena, con cabezal y servicios distintos de FDM. No se adopta su equipo comercial como abierto o superior. [Equipo y materiales](https://www.3dwasp.com/en/clay-3d-printer-delta-wasp-2040-clay/), [ejemplo de secado, cocción y esmaltado](https://www.3dwasp.com/en/londra-il-primo-ristorante-al-mondo-a-stampare-il-cibo-wasp-stampa-in-3d-piatti-e-bicchieri-in-porcellana/).

**[D]** La guía de Ultrafuse metálico separa impresión de pieza con aglutinante, eliminación de ese aglutinante y sinterizado; contempla servicio externo. La página aparece titulada «Discontinued»: se conserva como explicación de proceso, no como suministro vigente asegurado. [Guía de Forward AM](https://forward-am.com/gain-knowledge/ultrafuse-metal-solution-quick-start-guide/).

## 2. Una bobina puede variar su tacto, pero no sustituir cualquier materia

**[D]** colorFabb explica que varioShore TPU modifica densidad y suavidad mediante espumado al imprimir; publica posibilidad de llegar aproximadamente a Shore 55A. Es filamento formulado comercialmente, no materia prima doméstica ni composición completa abierta verificada. [Documentación técnica](https://support.colorfabb.com/hc/en-150/articles/360003021858-VarioShore-TPU).

**[I]** Es un ejemplo real cercano a la idea de una materia adaptable: algunas zonas o piezas pueden sentirse más blandas que otras. No demuestra que la misma bobina produzca también cuchillas, cables conductores, ventanas o componentes para alta temperatura. Cambiar paredes, huecos y forma cambia la respuesta de la pieza, pero no convierte su composición en acero, vidrio o silicona.

**[D]** Avient distingue dureza superficial y resistencia a flexión, además de efectos de tiempo y condiciones de medida. [Explicación del fabricante](https://www.avient.com/resources/knowledge-base/article/understanding-hardness). **[I]** Para nuestro estudio, «duro», «rígido», «resistente», «elástico» y «duradero» no serán sinónimos. Una pieza que casi no se dobla puede romperse con poca deformación; una pieza flexible puede soportar muchos ciclos sin ser apropiada para sostener una carga permanente.

**[P]** El objetivo razonable es una **familia de materiales y geometrías ajustables**, con un pequeño inventario de entradas y propiedades conocidas por función. No se asigna un porcentaje de objetos domésticos cubiertos: faltan inventario de usos, exigencias y validación.

## 3. Qué cambia la silicona

**[D]** Formlabs ofrece Silicone 40A Resin como silicona real para equipos SLA compatibles, con depósito/plataforma dedicados, lavado y poscurado. No la recomienda para exposición UV prolongada. Es un ejemplo comercial especializado; esta documentación no abre su formulación ni la vuelve compatible con una Voron de filamento. [Flujo del fabricante](https://formlabs.com/support/Using-Silicone-40A-Resin/).

**[I]** Que una formulación sea silicona no permite trasladar sus propiedades o límites a todas las siliconas. Tampoco una impresora que cura un material comprado resuelve producirlo. Se conservan separadas cuatro capacidades: **obtener materia → formular → dar forma → verificar la pieza**.

Los [antecedentes de extrusión abierta](EXTRUSION_ABIERTA_SILICONA.md) incluyen Allstruder como mecanismo investigable, con integración y aplicación por verificar. Los [estudios biológicos](BIOPRODUCCION_SILICONA.md) no demuestran un cultivo doméstico que entregue goma de silicona a partir de recursos locales. La investigación dedicada de esta entrega compara alternativas sin atribuirles esa capacidad.

## 4. Qué impresora encaja mejor en la prioridad abierta

**[D]** OSHWA incluye en su definición la posibilidad de fabricar, modificar, distribuir y vender diseños y hardware, con archivos fuente apropiados. [Definición](https://oshwa.org/definition/). **[I]** Aquí distinguimos esa apertura de tener planos visibles con restricciones comerciales. No es una auditoría jurídica de cada dependencia o patente.

| Candidato consultado | Evidencia | Decisión para el estudio |
|---|---|---|
| Voron Trident | Repositorio con GPLv3, archivos nativos F3D, STEP, STL y configuraciones | Primera referencia para cerrar una configuración abierta; todavía sin seleccionar kit o compra |
| Rat Rig V-Core 4.1 | La ficha declara CC BY-NC-SA 4.0; precio de cabecera 908,10 EUR con impuestos en región Portugal, electrónica opcional y paneles excluidos | Planos accesibles con restricción NC; no se cuenta como equivalente libre ni como kit instalado a ese precio |
| Prusa CORE One+, ficha denominada Gen 2 | CAD bajo OCL según documentación del fabricante; hay permisos de reparación y uso interno, con restricciones de reproducción comercial | Comparador de reparabilidad, sin superioridad medida que justifique abandonar la prioridad libre |

Fuentes: [Trident README](https://github.com/VoronDesign/Voron-Trident/blob/7fcb3257a3063225934d9608f82037aa6587d844/README.md), [licencia Trident](https://github.com/VoronDesign/Voron-Trident/blob/7fcb3257a3063225934d9608f82037aa6587d844/LICENSE), [Rat Rig](https://ratrig.com/products/rat-rig-v-core-4-1), [Prusa](https://www.prusa3d.com/product/prusa-core-one-kit/), [OCL v1.1](https://github.com/OpenCommunityLicence/OpenCommunityLicence/blob/7469fcd602cc10c3e1c372e233743800b9c7b4fc/LICENSE).

**[D]** Trident se fijó en **7fcb3257a3063225934d9608f82037aa6587d844**: árbol no truncado, 247 entradas y 210 archivos. Se comprobó presencia de formatos y se leyó README/licencia; no se abrieron todas las geometrías ni el manual de 86 MB. El cabezal Stealthburner se mantiene aparte; su repositorio también contiene GPLv3, revisión **8bcb9c246fac19d8ac03931ef97fa07c5e5f0f2b**. [Árbol fijado](https://api.github.com/repos/VoronDesign/Voron-Trident/git/trees/7fcb3257a3063225934d9608f82037aa6587d844?recursive=1), [licencia del cabezal](https://github.com/VoronDesign/Voron-Stealthburner/blob/8bcb9c246fac19d8ac03931ef97fa07c5e5f0f2b/LICENSE).

**[D]** Prusa declara que no publica todos los diseños de fabricación de PCB de algunos productos y distingue firmware y cargador de arranque. Su licencia OCL v1.1 permite uso empresarial interno pero limita replicación comercial sin acuerdo; cada archivo debe comprobarse por versión y condiciones. No se aplica automáticamente v1.1 a archivos descargados anteriormente bajo v1.0. [Alcance de publicación](https://www.prusa3d.com/en/page/open-source-at-prusa-research_236812/), [explicación de versiones](https://blog.prusa3d.com/open-community-license-v1-1-the-new-plugin-system-more-examples-and-your-questions-answered_137202/).

**[I]** GPL y CAD no fabrican motores, guías, calentadores o chips. Los F3D conservan datos nativos de un programa propietario; STEP permite trabajar geometría en otros programas sin asegurar el mismo historial paramétrico. Tampoco archivos completos prueban montaje correcto, exactitud o vida útil.

## 5. Coste comprobado de una variante, sin compra

**[D]** En el navegador se seleccionó únicamente para consulta **«Mit Raspberry / Mit Druckteilen»**, Meltbro **1009167-100916704**: **1.099,99 EUR con IVA alemán del 19 %**, sin transporte. El precio base es 879,99 EUR; la diferencia es **220 EUR**. La disponibilidad mostrada pasó a una unidad para esa variante. [Ficha](https://meltbro.de/voron-trident-300mm-dreizack-komplettes-3d-drucker-kit-dragon-hotend-ptfe-kabel.html).

[Captura de la variante consultada](datos/precio_trident_configurado_2026-10-23.png). No se añadió al carrito ni se envió dirección. El peso de transporte mostrado no se usa como masa real. Faltan impuesto final de destino, portes, configuración exacta, espacio, ventilación, filamento de uso y herramientas/recambios no incluidos. No es coste completo de taller.

**[D]** Print It Forward muestra 110 USD/EUR más envío para el conjunto funcional de Trident, con precios fechados en enero de 2023 y exclusiones de algunas piezas auxiliares. Es alternativa histórica de arranque, no suplemento que se sume a un kit que ya incorpora piezas impresas ni cotización española actual. [Programa](https://pif.voron.dev/).

**[I] Sensibilidad económica:** para recuperar solo esos 1.099,99 EUR de referencia harían falta **550, 220 o 110 piezas** si cada pieza evitara respectivamente 2, 5 o 10 EUR netos. Son ahorros elegidos y cálculo redondeado al entero superior; no precios de piezas observados, demanda demostrada ni amortización del taller. El ahorro neto debe descontar material, energía, fallos y reposición; añadir inversión y trabajo cambia el resultado. No basta con que el material de una pieza cueste céntimos.

## 6. Tamaño, mantenimiento y primera aplicación

**[P]** Antes de aumentar tamaño o añadir multicolor se compararán tres aplicaciones propuestas: soporte de sensor, mando o tirador no crítico y molde para una pieza flexible sencilla. No son averías detectadas en la vivienda. Definir dimensiones, carga, temperatura, humedad, ajuste y criterio de aceptación determinará máquina y material. No se da por validado el ejemplo de junta del anexo anterior.

**[D]** El README de Trident ofrece tamaños recomendados 250/300/350 mm en X/Y, con 250 mm en Z; el configurador genera la BOM específica. La FAQ señala que esa BOM manda sobre la guía genérica. [README](https://github.com/VoronDesign/Voron-Trident/blob/7fcb3257a3063225934d9608f82037aa6587d844/README.md), [aprovisionamiento](https://docs.vorondesign.com/sourcing_faq.html). **[I]** No hay piezas definidas que justifiquen todavía el tamaño mayor. Un kit comercial puede modificar la configuración: no se mezclan automáticamente su lista y los archivos de la revisión oficial.

**[D]** Voron pide revisar fijaciones y grietas, y documenta lubricación y aprovisionamiento. Sus piezas funcionales usan materiales apropiados para el ambiente de la máquina; PLA/PETG no son sustitutos generales de ABS/ASA. [Mantenimiento](https://docs.vorondesign.com/maintenance.html), [materiales](https://docs.vorondesign.com/materials.html). **[I]** Reparabilidad reduce algunas dependencias, pero no mantenimiento o consumo.

**[D/I]** NIOSH recomienda controlar emisiones mediante selección de materiales y controles de ventilación/captación; no se considera suficiente que una carcasa esté cerrada o que haya un filtro genérico. El acondicionamiento se presupuesta como parte del taller, sin validar una habitación concreta. [Guía, secciones indexadas](https://www.cdc.gov/niosh/docs/2024-103/pdfs/2024-103.pdf).

**[I]** Rat Rig anuncia 35 kg para su kit de 300 mm; Prusa publica 22,5 kg para su equipo. No son masas equivalentes de embalaje ni prueba de que todas las configuraciones pesen eso. Sirven para descartar la expectativa de transporte corporal frecuente: se estudia un taller trasladable, no un equipo cotidiano para fijar al cuerpo en moto.

**Continuación:** escoger una pieza de utilidad real y cerrar su cadena de material, fabricación y verificación; comparar suministro doméstico del material con compra y reutilización. La apertura de archivos queda mejor identificada, pero siguen pendientes coste instalado, uso suficiente y reparación propia comprobada.
