# Medición y mecanizado para fabricar repuestos propios

**Fecha: 23/10/2026.** Comparación documental, lectura de una lista de componentes y ejemplos aritméticos. No se han comprado herramientas, mecanizado piezas o ejecutado ensayos. [D] documentado; [I] inferencia; [P] propuesta; [A] pendiente. Referencias numeradas en [Fuentes](FUENTES.md); parámetros y procedencia en [datos](datos/medicion_mecanizado_2026-10-23.json).

**Conclusión:** podemos avanzar en diseño, fabricación de piezas seleccionadas e inspección con herramientas abiertas. La autonomía exige además saber si la pieza resultante sirve para su función. Una máquina con movimientos pequeños, un escáner o un microscopio no demuestran por sí solos exactitud, material adecuado o duración. La primera inversión depende de las piezas que necesitemos reponer, no de reunir todas las máquinas posibles.

## 1. Qué hay que medir antes de decir que una pieza está bien

**[D]** NIST distingue la trazabilidad del resultado de medida de la mera posesión de un instrumento calibrado. La cadena debe documentar referencias e incertidumbres. Incluso un resultado trazable puede ser insuficiente para una aplicación si su incertidumbre es demasiado grande [199].

| Concepto | Consecuencia práctica para un taller doméstico [I] |
|---|---|
| Resolución | El incremento de una escala o pantalla no es una garantía de error igual de pequeño. |
| Repetibilidad | Obtener lecturas parecidas no descarta un sesgo común. |
| Error máximo permitido del instrumento | Es una especificación bajo condiciones determinadas; no equivale automáticamente a la incertidumbre total de nuestra medición. |
| Calibración | Relaciona indicaciones con referencias y sus incertidumbres. Poner a cero no comprueba toda la escala. |
| Verificación de la pieza | Compara la propiedad necesaria con un requisito definido y una regla de decisión. |
| Aptitud funcional | Además de dimensiones puede depender de material, acabado, temperatura, carga, contacto con agua u otros requisitos. |

**[I]** Medir una carcasa no crítica o ajustar una unión de madera puede requerir menos que verificar una superficie de sellado. No se exige un laboratorio industrial para cualquier reparación; tampoco se rebaja la exigencia de una pieza crítica para hacerla encajar en nuestras herramientas.

El CEM publica el procedimiento DI-008 para calibres de pie de rey, edición de 2024 [200]. Su enlace al PDF alternó entre contenido indexado y una página de mantenimiento durante esta consulta. Aquí se conserva como referencia de procedimiento, sin atribuirle reglas o tablas que no se pudieron revisar de forma estable.

## 2. Un ejemplo que evita aceptar piezas por una sola cifra

**[P] Hipótesis didáctica:** una dimensión debe estar entre 19,90 y 20,10 mm. Se supone un intervalo total de medida de lectura ±0,04 mm. Este margen se elige para ilustrar la decisión; no procede de un instrumento real, no tiene aquí nivel de confianza asignado y no es una incertidumbre evaluada.

| Lectura elegida | Intervalo supuesto | Resultado de la regla conservadora elegida |
|---:|---:|---|
| 20,01 mm | 19,97–20,05 mm | Todo el intervalo queda dentro del requisito. |
| 20,09 mm | 20,05–20,13 mm | Se solapa con el límite: no basta para decidir. |
| 20,20 mm | 20,16–20,24 mm | Todo el intervalo queda fuera del requisito. |

**[I]** La segunda lectura cae dentro de la tolerancia nominal, pero el intervalo supuesto no. El ejemplo muestra por qué hace falta considerar el proceso de medida. No acredita conformidad de ninguna pieza ni sustituye una regla específica aplicable a su uso. Cambiar el margen cambia el resultado.

## 3. Medición manual y óptica abierta

### Instrumento mecánico como referencia de mercado

**[D]** Mitutoyo describe el 530-104 como un pie de rey mecánico de 0–150 mm, graduación de 0,05 mm y exactitud anunciada ±0,05 mm [201]. **[I]** Evitar batería y electrónica elimina esas dos reposiciones, pero no desgaste, golpes, corrosión o comprobaciones. No se acredita una licencia abierta del diseño ni se elige este modelo como superior a una alternativa abierta equivalente.

**[P]** Un instrumento manual puede encajar en un flujo de trabajo abierto: guardar lecturas y referencias en formatos legibles, usar diseños propios de soportes no críticos y conservar criterios de aceptación. Eso abre la documentación de trabajo; no convierte el instrumento comercial en hardware abierto. Su escala no basta para todas las tolerancias.

### OpenFlexure como herramienta de observación e inspección

**[D]** El proyecto recomienda la versión 7, todavía beta [212]. Se ha fijado como referencia la documentación **v7.0.0-beta5**, que ofrece configuraciones manuales y motorizadas, archivos e instrucciones [213]. Su página de licencia publica CERN-OHL-S-2.0 [217]. Esa declaración no abre automáticamente los componentes comerciales incorporados.

La lista de la configuración de alta resolución incluye 400 g de PLA, óptica, Raspberry Pi 4, cámara v2, controladora Sangaboard v0.5, motores y juntas tóricas de Viton [214]. **[I]** Podemos imprimir y sustituir parte de la mecánica con material comprado. No se demuestra que podamos fabricar localmente cámaras, lentes, chips o elastómeros equivalentes.

**[D]** La documentación de MICAT limita su función actual a calibrar el tamaño de píxel de micrografías mediante patrones USAF [215]. **[I]** Tamaño de píxel, resolución óptica y exactitud dimensional son magnitudes distintas. La inspección visual puede ayudar a detectar ciertos defectos; no valida por sí sola dureza, resistencia, estanqueidad o potabilidad. Tampoco se ha validado aquí como sistema de medición de piezas grandes mediante imágenes unidas.

**[A]** Falta un presupuesto español de la configuración elegida, incluida la referencia de calibración. No se presenta un coste histórico del microscopio como precio actual ni se afirma que todas sus variantes de hardware y software sean intercambiables.

## 4. Fresadoras abiertas y archivos realmente disponibles

| Proyecto o equipo | Evidencia de apertura y versión [D] | Decisión para esta investigación [I/P] |
|---|---|---|
| PrintNC V4 | La wiki declara CC BY 4.0; su página de archivos identifica V4.0.30 y enlaza modelos actuales mediante Discord [205–206]. El repositorio GitHub anterior está archivado desde 19/10/2024 y se identifica como V2.1 obsoleto [207–208]. | No usar el repositorio antiguo como prueba de que tenemos el conjunto actual. Obtener y comprobar los archivos de una revisión exacta antes de presupuestar. |
| OLSK Small CNC V3 | Repositorio con CAD, electrónica, firmware, montaje y lista de componentes [209]. Los metadatos distinguen CERN-OHL-W-2.0 para CAD/BOM, AGPL-3.0-or-later para firmware/configuración y licencias de documentación/recursos [210]. | Candidata para estudiar fabricación y reparación. No hay reproducción local, exactitud de mecanizado o coste total comprobados. |
| Rat Rig StrongHold ONE | Ficha comercial con guía, modelo CAD y piezas imprimibles enlazados [216]. | Referencia de mercado; esos enlaces no bastan para acreditar una licencia abierta de todos sus componentes o una superioridad técnica. |

Las páginas actuales de PrintNC no entregaron cuerpo de texto al abrirlas; los detalles de V4 proceden del contenido indexado del propio sitio. No se accedió a Discord ni se descargaron esos CAD. La licencia CC BY 4.0 se leyó en el archivo del repositorio antiguo; su existencia no demuestra por sí sola la licencia de cada archivo actual.

### Lo que enseña la lista de OLSK

**[D]** Se inspeccionó el XLSX de V3 en el commit **cae066fa5b78b596743e1f2e432b93539cba8c24**. La hoja `sheet1` contiene datos en A1:B267, con descripciones y cantidades, sin fórmulas ni columna de precios [211]. **267 filas no son 267 piezas distintas**: hay cabeceras, grupos y componentes repetidos.

Tres ejemplos verificables son dos husillos SFU1605 de 800 mm en A14:B14, dos guías MGN12 de 370 mm en A99:B99 y un soporte de husillo marcado como mecanizado CNC en A111:B111. También aparecen piezas impresas en resina. **[I]** Disponer de impresora de filamento no permite dar por resueltas esas piezas o procesos.

La descripción de V3 anuncia un cambiador de diez herramientas [209]; la fila A123 de la lista se llama «12 Tool Magazine» [211]. **[A]** Puede referirse a capacidad física o a una diferencia de revisión: no se resolvió. No se declara que la máquina esté mal diseñada; se evita construir una configuración suponiendo equivalencia documental.

**[D]** Los metadatos de licencia delimitan V3 y dejan pendiente el mapeo de V1/V2 [210]. **[A]** No se han abierto los archivos CAD o los ZIP de firmware para comprobar su integridad, compatibilidad o todas sus dependencias. La declaración de licencia es un avance concreto, no una auditoría de cada componente.

## 5. Costes observados y lo que no incluyen

Referencias consultadas el 23/10/2026, sin cesta, solicitud de presupuesto o compra. Se mantiene la fiscalidad tal como aparece en cada página; no son importes finales entregados en España.

| Referencia | Precio mostrado | Condición que cambia su interpretación |
|---|---:|---|
| Mitutoyo 530-104, TN-Tools [202] | 38,00 € sin IVA | Misma referencia comercial; transporte e importe final pendientes. |
| Mitutoyo 530-104, HBM [203] | 52,99 €, IVA incluido | Precio observado, sin certificado de calibración individual acreditado en esta consulta. |
| Juego HBM de 47 bloques, anunciado grado 1 [204] | 219,99 €, IVA incluido | No se verificaron certificado individual, incertidumbres o relación de tamaños. El nombre de grado no demuestra trazabilidad de nuestro resultado. |
| Rat Rig StrongHold ONE, cabecera del configurador [216] | 1.259,00 €, impuestos incluidos en la región mostrada | El total configurado aparece sin resolver. La ficha separa máquina mecánica y electrónica; no es presupuesto de una fresadora lista ni de un taller. |

**[I]** Calibre HBM + juego de bloques suman **272,98 €** a esos precios. Es solo una suma parcial, no una recomendación de comprar ambos ni una garantía de poder calibrar todas las mediciones. Un juego completo puede ser innecesario para las primeras piezas; faltan requisitos y comprobación de los patrones.

Rat Rig publica una distancia por paso completo de 0,04 mm [216]. **[I]** No se utiliza como tolerancia de mecanizado. La exactitud de una pieza depende también de holguras, flexión, herramienta, montaje y medición. El campo de trabajo o la promesa de cortar un metal no permiten dar por fabricable cualquier pieza de ese material.

Para presupuestar un taller quedan por identificar herramientas de corte y su afilado/reposición, sujeción, medición, extracción, acondicionamiento del espacio, suministros eléctricos y mantenimiento. No se asigna coste cero a esos elementos ni una duración indefinida. La CNC y sus servicios se tratarán como infraestructura de taller, sin suponer transporte corporal o en moto.

## 6. Qué podemos mejorar nosotros

**[P] Primero, definir una pieza necesaria y no crítica.** La ficha debe recoger función, geometría que importa, material, condiciones de trabajo, tolerancias justificadas y cómo se decidirá si sirve. Un soporte de un sensor o una pieza de mobiliario puede ser un comienzo; no se extrapola a frenos, recipientes a presión o protecciones eléctricas.

**[P] Después, cerrar su cadena de fabricación y comprobación.** Conservar modelo editable, versión, orientación/proceso, lote de material y medidas de la pieza obtenida. Separar lo que podemos fabricar, lo que podemos sustituir con componentes normalizados y lo que todavía compramos sin equivalente propio. Si falta un patrón o criterio, registrar el resultado como pendiente, en vez de deducir exactitud del aspecto visual.

**[P] Para las máquinas abiertas, aportar documentación que elimine incertidumbres.** Vincular CAD, lista de componentes, firmware y configuración de una misma revisión; explicar cada sustitución y publicar su efecto en coste y prestaciones. Un inventario de proveedores alternativos ayuda mientras estén disponibles, pero no se cuenta como fabricación doméstica de sus piezas.

**[I] Prioridad:** un taller pequeño orientado a repuestos realmente necesarios puede reducir compras y reparaciones externas antes que una colección de máquinas sin uso definido. Abrir los planos aporta control técnico; la independencia material requiere además reponer herramientas, patrones y componentes con calidad suficiente.

**[A]** Esta entrega no acredita una cadena doméstica completa de precisión, ahorro económico del taller o plazo para fabricar todos los aparatos de una vivienda. Continúa el estudio de herramientas de corte, afilado y metales recuperados, incluyendo los procesos que condicionan su calidad.
