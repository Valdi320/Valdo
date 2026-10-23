# Afilado y metales recuperados para mantener un taller propio

**Fecha: 23/10/2026.** Investigación documental y cálculos de cantidades. [D] documentado; [I] inferencia; [P] propuesta; [A] pendiente. No se han afilado herramientas, fundido metales, instalado programas o comprado productos. Referencias en [Fuentes](FUENTES.md); parámetros en [datos](datos/afilado_metales_2026-10-23.json).

**Resultado:** mantener filos existentes y reutilizar material identificable puede reducir compras y reparaciones externas. No cierra por sí solo el suministro de herramientas: afilar retira material, los abrasivos y las limas también requieren reposición, y una pieza de metal recuperada conserva incertidumbres sobre composición y estado. La opción más autónoma depende del trabajo y del mantenimiento completo, no solo de la vida anunciada de una máquina.

## 1. Escoger herramientas que podamos mantener

**[D]** Bahco distingue en una misma familia de serruchos el 4211, con dientes endurecidos, del 4212, que admite limado; anuncia hojas de repuesto para ambos [233]. Silky indica que sus hojas endurecidas por impulso no se pueden reafilar con una lima manual [232]. No se extiende esa limitación a todos los modelos de la marca o a cualquier método industrial de rectificado.

**[I/P]** Cuando una herramienta reafilable cumpla la función, puede reducir la dependencia de hojas nuevas. A cambio requiere aprender y conservar geometría, limas/abrasivos y tiempo de trabajo. No hay una comparación medida de velocidad, duración o coste entre esos serruchos que permita declarar un ganador universal. Cambiar una hoja comprada es reparabilidad por sustitución; restaurar el filo es otra capacidad.

| Función | Qué podemos avanzar [P] | Dependencia que permanece |
|---|---|---|
| Cuchillos y hojas sencillas | Mantener el filo y documentar geometría y desgaste | Acero, abrasivo y cantidad de material restante |
| Serrucho que admite limado | Conservar dentado y registrar mantenimiento | Lima adecuada, geometría y estado de la hoja |
| Hoja endurecida no limable | Identificar el recambio antes de elegirla | Hoja comprada o proceso de recuperación aún no demostrado |
| Brocas, fresas y herramientas complejas | Estudiar qué geometrías podemos inspeccionar y recuperar | Sujeción, rectificado, medición y, en algunos casos, recubrimiento |

Esta tabla es una propuesta de trabajo, no un procedimiento de afilado ni una afirmación de que todas esas funciones estén resueltas en casa. La [entrega de medición](MEDICION_MECANIZADO_PRECISION.md) explica por qué conseguir una forma parecida no demuestra su aptitud.

## 2. Una guía abierta que sí podemos estudiar y adaptar

**[D]** El proyecto **Whetstone guide**, de anorm, publica diseño paramétrico OpenSCAD, STL y una licencia CC BY-SA 4.0 [218–220]. Se fija la revisión **1655d779d0c1cbe2a2549eccb22e41d242b0da69**. Permite configurar dimensiones de la piedra y hasta cuatro ángulos. El código incluye la biblioteca BOSL2, cuyo repositorio declara BSD-2-Clause [221]; esta dependencia no está incorporada en el árbol de la guía.

**[I]** Es una opción concreta para fabricar parte del soporte con una impresora y material adquiridos. No fabrica la piedra ni demuestra exactitud angular o duración. Un parámetro que admite décimas de grado no garantiza ese error en el objeto impreso o durante el uso.

### Adaptación identificada sin ejecutar el diseño

**[D]** El archivo toma una piedra de 28 mm de alto por defecto y calcula una variable interna `height = stone_height - base_edge_height - rail_d*0.1`, con `base_edge_height = 10` y `rail_d = 15` [219]. **[I]** Esa variable resulta 16,5 mm con los valores originales y −2,0 mm si se cambia únicamente la altura a 9,5 mm, que es la anunciada para una placa comercial revisada [226].

**[A]** No se ha renderizado el modelo ni comprobado la geometría final. El valor negativo señala una adaptación que revisar; no demuestra por sí solo fallo del programa. No se declara compatible la placa fina por coincidir largo y ancho. Una base elevadora o un cambio de diseño son hipótesis, no soluciones verificadas.

**[P] Aportación propia útil:** adaptar el soporte a una piedra real identificada, documentar dependencias y comprobar montaje, estabilidad y ángulo efectivo. Conservar el archivo editable y las condiciones del material impreso. Cualquier distribución de una adaptación deberá respetar la licencia del diseño; no se ha copiado o relicenciado aquí el proyecto.

## 3. Un abrasivo duradero sigue teniendo condiciones de uso

**[D]** La guía de Tormek distingue muelas con diferente capacidad de desbaste y acabado [222]. Sus muelas diamantadas emplean cuerpo de acero y grano fijado mediante níquel; el fabricante advierte que demasiada presión puede dañarlas y exige ACC-150 al trabajar con agua [223–224]. Son características y condiciones de ese sistema, no reglas transferibles a todas las placas diamantadas.

En una respuesta de 02/10/2024 sobre **T-1**, Tormek anuncia miles de afilados y posible duración de por vida en muchos hogares, pero reconoce que depende del uso y que la superficie se vuelve progresivamente más fina [225]. **[I]** No se convierte esa respuesta sobre una afiladora doméstica de cuchillos en garantía de desgaste nulo, plazo fijo o vida útil de una muela para herramientas de taller.

**[D]** ACC-150 se vende en dos envases de 150 ml y el fabricante especifica 10 ml de concentrado por 250 ml de agua [224]. **[I]** Un paquete representa **30 preparaciones nuevas de esa cantidad**, antes de pérdidas. No son treinta afilados: la mezcla puede reutilizarse bajo las condiciones indicadas por el fabricante, y no conocemos su reposición real en nuestro uso.

La página del producto enumera ácido dodecanodioico y agua [224]. **[A]** Esa lista no establece formulación completa, concentración, compatibilidad o un sustituto abierto equivalente. No se deduce de ella una receta. Estudiar un equivalente exige definir la función y evaluar corrosión y materiales con resultados comparables.

## 4. Precios de referencia y consumibles

Observaciones del 23/10/2026, sin compra o cesta. No son una comparación de productos equivalentes ni el presupuesto de un sistema completo.

| Referencia comercial | Precio mostrado [D] | Condiciones y límites |
|---|---:|---|
| DMT Duo Sharp fina/extrafina, Nakatogi [226] | 124,10 €, impuestos incluidos | Vendedor anuncia 203 × 67 × 9,5 mm y granos 600/1200. Falta confirmar referencia exacta de fabricante y entrega. |
| DMT DuoSharp gruesa/fina con base, UTSET [227] | 194,50 €, impuesto incluido | Página enlazada como W8FC-WB; combinación y base diferentes de la anterior. Envío calculado al pagar. |
| Tormek ACC150, SKU TRMACC150, Gubias [228] | 44,00 €, impuestos incluidos en la última lectura | Dos envases de 150 ml. Otra lectura de la misma ficha mostró 43,00 €: no hay precio final confirmado. |

**[I]** Usando 44,00 € como referencia, el concentrado de una preparación nueva de 10 ml costaría **1,47 €**, sin agua, transporte, pérdidas o gestión del líquido usado. No se calcula coste anual o por herramienta sin medir frecuencia de renovación y reutilización. Este consumible de Tormek no se añade automáticamente al mantenimiento de las placas DMT.

No se han acreditado planos abiertos de fabricación de los abrasivos comerciales ni una ventaja suficientemente comparada para seleccionar un sistema cerrado completo. Sus precios permiten identificar dependencias. Una guía imprimible tampoco demuestra que podamos mantener cualquier fresa o recuperar un recubrimiento industrial.

## 5. Qué significa reutilizar metal de forma fiable

**[D]** Böhler publica para su acero rápido S600, EN HS6-5-2C, una composición con carbono, cromo, molibdeno, vanadio y wolframio; identifica aplicaciones de corte [229]. **[I]** Aportar carbono o dar forma a un acero recuperado no basta para demostrar equivalencia a ese acero rápido. Faltan aleación, historia térmica y propiedades verificadas. No se presenta una ruta doméstica demostrada para fabricarlo desde chatarra mezclada.

**[D]** Evident explica que el análisis XRF ayuda a separar aleaciones, pero generalmente no mide elementos ligeros como el carbono [230]. **[I]** Saber que una pieza contiene hierro o ciertos aleantes no identifica automáticamente su grado, tratamiento o aptitud para una herramienta. Comprar un analizador tampoco elimina la necesidad de referencias y un método adecuado.

**[D]** El International Aluminium Institute describe reciclaje con selección por composición, eliminación de recubrimientos/aceites y, según la ruta, refinado, desgasificación y ajuste de aleación [231]. **[I]** Fundir aluminio no restaura por sí solo la composición y las propiedades de cualquier producto original. El proceso incorpora energía, materiales auxiliares y residuos. El ahorro energético industrial anunciado frente a producción primaria no es una medición de un horno doméstico ni de su coste completo.

| Recurso disponible | Uso propio razonable para investigar [P] | Evidencia necesaria antes de exigir prestaciones |
|---|---|---|
| Perfil o chapa con procedencia y grado conservados | Reutilización directa y mecanizado mínimo | Estado, dimensiones, tratamiento y adecuación al uso |
| Herramienta conocida gastada | Restauración del filo si su diseño y estado lo permiten | Material restante, geometría y comportamiento |
| Metal mezclado sin identificación | Separar y mantener identificado el lote; evitar atribuirle propiedades de un grado conocido | Composición y estado suficientes para la función prevista |
| Virutas o material con recubrimientos | Estudiar una ruta de recuperación específica | Preparación, rendimiento, emisiones, residuos y calidad obtenida |

**[I]** Conservar una pieza aprovechable puede evitar procesos y consumibles que aparecerían al refundirla. El material recogido fuera conserva dependencia de disponibilidad y acceso; no se cuenta automáticamente como recurso propio gratuito y permanente.

## 6. El mantenimiento incluye residuos y condiciones del taller

**[D/A]** Un estudio de exposición en fabricación y mantenimiento de herramientas de metal duro, consultado mediante su resumen indexado, observó exposición a cobalto durante rectificado y recomendó cerramiento y extracción local [234]. No se ha revisado íntegramente ni se extrapolan sus concentraciones a nuestro caso.

**[I]** Recuperar una herramienta puede desplazar parte del coste a control de polvo, líquido de trabajo, limpieza y residuos. Esas necesidades forman parte del proceso que se compare. No se presupone que cualquier esmeril y una piedra resuelvan todas las herramientas del futuro taller.

## 7. Decisión provisional y continuación

**[P]** Empezar por una familia de herramientas reafilables que realmente necesitemos, documentar su mantenimiento y registrar material retirado, tiempo, consumibles y calidad conseguida. Para los metales, priorizar reutilización identificada antes de añadir fusión y tratamientos. No se compra maquinaria con esta entrega.

**[P]** La guía abierta permite un primer desarrollo delimitado; quedan por comprobar sus dependencias, adaptación a piedra fina y comportamiento físico. El estudio continúa con protección frente a corrosión, uniones desmontables y materiales auxiliares, porque condicionan la duración de las piezas y las compras de reposición.

**[A]** No se acredita fabricación doméstica completa de acero rápido, abrasivos, limas o recubrimientos, ni un plazo para cerrar esas cadenas. Avanzar en conservación y mantenimiento reduce dependencias concretas; no demuestra todavía gasto cero indefinido.
