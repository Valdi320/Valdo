# Xiaomi X20 Pro: ingeniería física, CAD y fabricación para facilitar reparaciones

Capítulo de ingeniería física del dossier X20 Pro. Consulta de fuentes: 25 de octubre de 2026. Alcance: conservar electrónica, firmware, batería, motores, sensores y estación originales; reducir gasto y tiempo sin robot. Las propuestas siguientes son diseños por desarrollar y verificar, no piezas ya dimensionadas ni soluciones probadas en esta unidad.

## 1. Decisión técnica principal

Es viable rediseñar progresivamente sus soportes, fijaciones, tapas y, finalmente, el chasis para que las piezas de desgaste o rotura sean sustituibles. El mejor primer proyecto es el soporte averiado de la suspensión: permite aprender cómo se transmite la carga, medir las interfaces y comprobar un procedimiento de reparación sin comprometer todo el aparato.

La meta no exige imprimir engranajes, pasadores, muelles, neumáticos, juntas, batería o sensores. Conviene conservar las piezas comerciales que ya hacen bien su función y diseñar alrededor de ellas alojamientos desmontables. Una pieza nueva puede resultar más resistente en su punto débil si distribuye mejor la carga; eso no demuestra que todo el robot sea más resistente ni elimina la necesidad de comprobar fatiga, desgaste, temperatura y deformación con el tiempo.

**Falta una observación decisiva:** determinar si la rotura afecta al soporte fijo del chasis, a la carcasa móvil del módulo de rueda o a ambos. La fotografía general del fondo no permite dimensionar esa reparación. Tampoco sabemos la composición del plástico original, la fuerza del muelle, la geometría intacta del alojamiento ni el espacio disponible para una fijación alternativa. No corresponde inventar espesor, diámetro de tornillo, holgura o material final antes de obtener esos datos.

## 2. Tres rutas compatibles con mantener el uso

| Ruta | Trabajo físico propuesto | Qué se conserva | Qué resuelve y qué queda pendiente |
|---|---|---|---|
| A. Barata y práctica | Reparar el apoyo concreto con un puente, abrazadera o pequeña base desmontable que descargue el esfuerzo en material sano; mantener el pasador y el muelle adecuados. | Chasis, rueda, motor, engranajes, sensores y cableado. | Puede resolver la avería actual. No convierte por sí sola el robot completo en modular. Hace falta ver el daño para decidir si existe una superficie de anclaje válida. |
| B. Mejoras por etapas | Crear apoyos de suspensión reemplazables y, donde la estructura lo permita, acceso de mantenimiento independiente a cada módulo. Documentar piezas y fijaciones. | Gran parte del chasis y todas las funciones originales. | Reduce el desmontaje futuro. Una tapa de acceso solo es viable si no elimina una sección estructural o un sellado necesarios. |
| C. Rediseño dimensional completo | Crear un chasis paramétrico dividido en un núcleo de referencia y módulos desmontables, manteniendo las posiciones funcionales del conjunto original. Fabricar y comprobar el conjunto de prueba antes del trasplante. | Componentes funcionales originales, firmware y estación. | Permite controlar la geometría editable y fabricar repuestos propios. Requiere muchas más mediciones, iteraciones y comprobaciones; no garantiza la misma navegación si se alteran interfaces que el firmware presupone. |

### Ruta A: cómo mejorar el soporte sin copiar su fragilidad

Propuesta de ingeniería: sustituir la pequeña zona que concentra la carga por una pieza que la reparta sobre una superficie mayor y sana. Si el pasador pivota dentro de plástico, puede estudiarse un casquillo comercial o un apoyo metálico reemplazable, sujeto por un cuerpo impreso. El gancho del muelle puede apoyarse en metal sin cambiar su posición, su dirección de tracción ni el recorrido de la suspensión.

La diferencia entre un refuerzo útil y uno aparente es el camino que sigue el esfuerzo. Un aro alrededor de una orejeta rota puede mantener unidos los fragmentos mientras la raíz dañada sigue soportando toda la fuerza. Un puente que alcanza apoyos sanos puede crear un camino alternativo. No debe sujetarse a una tapa delgada solo porque esté cerca, ni atravesar a ciegas un área con cables, motor o conductos.

La elección entre abrazadera, puente, placa de respaldo o pieza nueva depende de las imágenes y medidas. Evitar tornillos avellanados directamente contra plástico si su cabeza produce un efecto de cuña. La guía de uniones de Covestro explica el reparto de carga mediante cabezas de apoyo plano y arandelas, así como la relajación de tensiones y el daño por exceso de apriete. Es orientación general sobre plásticos, no una dimensionación automática de esta reparación. [F8]

Las bridas pueden servir para presentar una pieza o como retención auxiliar si no rozan ni limitan el movimiento. No permiten afirmar que una suspensión será estable a largo plazo: la geometría de contacto, el material de la brida y la tensión real no están definidos. El adhesivo aplicado tampoco acredita por sí mismo una resistencia estructural concreta.

### Ruta B: hacer sustituible lo que se rompe

Diseñar la pieza de apoyo como repuesto independiente: cuerpo pequeño, pasador extraíble, elemento de desgaste accesible y fijaciones que puedan abrirse repetidamente. Conservar completo el módulo motorizado mientras motor, reductora, encoder y neumático funcionen. Dar acceso al conector original y a la retención del pasador sin desmontar módulos ajenos, cuando el espacio lo permita.

La arquitectura deseable tiene superficies que **posicionan** y tornillos que **sujetan**. Esto permite desmontar y volver a colocar el módulo con la misma alineación. Las tuercas cautivas y los tornillos pasantes con apoyo amplio son opciones económicas. Los insertos roscados pueden ser útiles donde haya suficiente plástico, pero exigen el alojamiento especificado para el inserto elegido: SPIROL documenta que un agujero demasiado pequeño introduce tensiones y uno demasiado grande reduce la retención. [F9]

No fijar todavía una familia o tamaño de tornillo. Primero comprobar diámetro, pared disponible, profundidad y distancia a las zonas móviles. La mejora no consiste en añadir una rosca metálica dentro de una pared que sigue siendo insuficiente.

### Ruta C: chasis propio manteniendo las interfaces originales

Arquitectura propuesta para el CAD:

| Subconjunto | Función del rediseño | Interfaz original que debe preservarse |
|---|---|---|
| Núcleo estructural de referencia | Mantener las posiciones relativas y servir de base de ensamblaje. Puede dividirse para imprimir, con uniones accesibles y superficies de localización. | Distancia entre ruedas, altura de funcionamiento, referencias de sensores y de la estación. |
| Soporte de cada rueda | Permitir retirar una rueda y su suspensión de forma independiente; apoyo y anclaje del muelle reemplazables. | Eje de giro, recorrido, topes, posición del muelle y actuación del detector de rueda levantada si lo incorpora. |
| Bandeja de electrónica | Sujetar placa y cableado, con acceso ordenado a conectores. | Patrón de montaje, ventilación, recorrido de cables y orientación de componentes. |
| Cuna de batería | Permitir extraer el paquete original sin desmontar otras funciones. | Conector, fijación firme sin comprimir las celdas y espacio térmico original. |
| Aspiración y depósito | Acceso al ventilador, cepillo y conductos. | Sellado, geometría de entrada/salida, acoplamiento de vaciado y separación de residuos. |
| Módulos de mopa | Acceso independiente a conjuntos completos. | Alturas, ejes, elevación y acoplamiento con la estación. |
| Paragolpes y sensores | Piezas exteriores reemplazables. | Recorrido libre del paragolpes, actuación de interruptores, ventanas ópticas, ángulos y alturas. |

Es una propuesta, no una afirmación sobre la distribución interna exacta del X20 Pro. Conviene evitar una única impresión grande de cuya integridad dependan todas las orejetas: una rotura local debería obligar a reemplazar un soporte pequeño. A la vez, dividir demasiado el chasis añade uniones, holguras y acumulación de errores; el núcleo que mantiene la alineación debe ser estable.

La estrategia inicial de documentar y cerrar el robot para seguir usándolo queda sustituida por la decisión del propietario de abandonar la carcasa dañada. Los prototipos se comprobarán en un soporte propio o útil de presentación; no es necesario restaurar antes el chasis original. El trasplante se prepara con el bastidor de prueba y los conjuntos retenidos. No hace falta comprar una impresora para decidir la viabilidad: un primer soporte puede encargarse con el material y la orientación especificados. El plan vigente está en [07 — Chasis propio](07-plan-del-chasis-propio.md).

## 3. Medición económica: qué se necesita realmente

Un calibre adecuado, regla, fotografías nítidas y una forma repetible de apoyar la pieza permiten empezar. La resolución que muestra un calibre no es la exactitud de la medición; Mitutoyo distingue ambas y describe errores por alineación, deformación del instrumento y fuerza de medida. No significa que haya que comprar esa marca: importa conocer la incertidumbre real del instrumento disponible. [F1]

Procedimiento propuesto:

1. Elegir superficies intactas y rígidas como referencias. No usar el borde fracturado ni la goma deformable de la rueda como origen dimensional principal.
2. Limpiar las superficies de medición, comprobar el cero y contrastar el calibre con una dimensión conocida si existe una referencia fiable. Repetir la medida desde distintas posiciones, sin apretar el plástico.
3. Fotografiar cada cara con escala en el mismo plano de interés. La fotografía ayuda a reconstruir forma y posición; no sustituye una medición directa de agujeros o alojamientos.
4. Guardar valor, rango observado y estado: pieza descargada, montada, comprimida o con el peso del robot. Una única cifra sin esa condición puede inducir un diseño incorrecto.
5. Crear una tabla de parámetros y fabricar primero cupones de ajuste: solo el agujero, el asiento o la sección de unión necesarios. No imprimir un chasis completo para descubrir que un pasador no entra.

### Mediciones mínimas para el soporte de rueda

| Medición | Método práctico | Qué permite decidir |
|---|---|---|
| Localización exacta de la rotura y material sano disponible | Fotografías con varios ángulos; identificación de qué pertenece al chasis y qué se mueve con la rueda. | Si se puede reforzar, qué pieza debe reemplazarse y dónde no fijar. |
| Pasador existente: diámetro, longitud, extremos y retención | Calibre en varias posiciones; observar si gira el pasador o gira la pieza sobre él. | Alojamiento y sistema de desmontaje; una medida nominal de una tienda no define el ajuste. |
| Centros y alineación de apoyos | Medición desde las mismas superficies de referencia; plantilla de comprobación que una ambos apoyos. | Evitar un eje torcido o un movimiento forzado. |
| Espesor y extensión del material sano | Medición directa y visión de la cara posterior. | Superficie de reparto y posibilidad de usar respaldo o fijación pasante. |
| Recorrido completo y espacio barrido por la rueda | Moverla suavemente entre topes, documentar posiciones y comprobar espacios con el resto del robot inmóvil. | Que el refuerzo, tornillos y cables no invadan la trayectoria. |
| Anclajes del muelle y longitudes de trabajo | Medir posiciones y longitud en estados conocidos; comparar con un lado intacto solo cuando la geometría sea equivalente. | Reproducir la función sin cambiar dirección de carga o precarga accidentalmente. |
| Fuerza de suspensión | Si se necesita, medir con dinamómetro a desplazamientos definidos o mediante un montaje de carga conocido. No deducirla solo de longitud y diámetro exteriores del muelle. | Elegir un recambio equivalente o detectar que el nuevo anclaje altera el comportamiento. |
| Topes y detección de rueda levantada | Observar puntos de contacto y el cambio de estado del sensor mediante el procedimiento accesible del equipo. | Mantener recorrido útil y detección original. |
| Tornillos, cabezas, longitudes y espacio detrás | Inventario y medición; comprobar el interior antes de proponer un agujero. | Fijaciones desmontables sin contacto con otros componentes. |

Para un chasis completo se añaden: centros y altura de ruedas bajo el peso normal, posición de LiDAR y sensores de borde, altura de cepillo y mopas, ventanas del paragolpes, contactos de carga, zonas de apoyo en la rampa y bocas de vaciado; cualquier conexión de agua adicional, sólo si se confirma en esta unidad. Registrar también masa y reparto aproximado de peso para comparar el prototipo con el original. La lista expresa interfaces que deben verificarse; no afirma que todas tengan el mismo diseño en cada variante comercial.

### Fotogrametría y escáner

Meshroom permite reconstrucción por fotografías y su herramienta SfMTransform permite establecer escala usando referencias. Es una ayuda para superficies generales y empaquetado. Una malla sin escala verificada no proporciona dimensiones fiables; incluso escalada, los ajustes críticos requieren medidas directas. [F2]

El equipo de OOMWOO documenta que escanea componentes comerciales y reconstruye modelos editables; también explica dificultades con piezas oscuras, transparentes y zonas profundas. Su experiencia confirma que obtener una malla no elimina el trabajo de interpretación. [F14] Para empezar con dos apoyos pequeños, comprar un escáner no está justificado por la información actual.

## 4. CAD paramétrico y tolerancias: dónde está el control dimensional

Conservar el proyecto editable es más útil que reunir STL. FreeCAD ofrece modelado paramétrico; CadQuery permite definir las piezas mediante parámetros en Python y exportar formatos de fabricación e intercambio. En CadQuery, el archivo Python mantiene la definición paramétrica; STEP exporta geometría, no toda esa historia de construcción. [F3, F4]

Paquete de diseño propuesto: archivo nativo editable; tabla de parámetros con su procedencia; STEP; STL o 3MF; plano con referencias y cotas funcionales; lista de tornillería y piezas conservadas; orientación de impresión; perfil de fabricación y registro de comprobaciones. Identificar revisiones para no mezclar un soporte nuevo con una tapa de una versión anterior.

**No existe una holgura universal de impresión.** Prusa relaciona el ajuste con geometría, orientación, material, calibración y condiciones de fabricación, y recomienda comprobaciones iterativas. [F5] Por ello no se prescribe aquí añadir automáticamente una cifra fija a todos los agujeros.

Para una articulación, el juego mínimo depende de la dimensión real del alojamiento más pequeño y del pasador más grande. La diferencia entre ambos diámetros no basta si los dos apoyos están desalineados, el agujero es ovalado o el cuerpo se deforma al apretar. Un cupón impreso con el mismo material, orientación y proceso debe comprobar tanto la entrada del pasador como el giro sin agarrotamiento y sin juego excesivo. La holgura aceptable se deriva de la función observada, no del número de decimales del CAD.

Propuesta: usar superficies de asiento y elementos de localización para repetir la posición del módulo; reservar a los tornillos la función principal de apretar. Si se necesita una superficie de desgaste precisa, estudiar un casquillo comercial o acabado posterior controlado. No indicar una broca concreta a partir del diámetro nominal de un anuncio.

### Lo que significa —y no significa— controlar cada milímetro

Se puede controlar el modelo, medir lo fabricado y verificar que queda dentro de un ajuste definido. No significa que una impresora reproduzca automáticamente todas las cotas con la exactitud deseada. Tampoco permite cambiar libremente distancia entre ruedas, radio efectivo del neumático, posición del LiDAR o geometría de entrada en la estación y suponer que el firmware se adaptará.

Con electrónica y firmware originales, la estrategia es preservar las interfaces que esos sistemas esperan. Si se cambia una magnitud que participa en odometría, detección o acoplamiento, hay que verificar la consecuencia; un CAD exacto no revela por sí solo constantes internas o posibilidades de calibración. Esta es una limitación de integración, no una razón para desistir del rediseño de soportes y accesos.

## 5. Materiales: escoger por función y proceso

Una pieza inyectada y otra FDM de forma parecida no son equivalentes. Las capas introducen direcciones mecánicas distintas; copiar la orejeta delgada original sin adaptar su orientación, raíz y reparto de esfuerzos puede producir una pieza peor. Prusa explica esta dependencia de la orientación. [F5] Su documentación también indica que aumentar relleno no sustituye el papel de los perímetros para la resistencia de muchas piezas. [F6]

| Material o elemento | Uso propuesto en este proyecto | Condición para aceptarlo |
|---|---|---|
| PLA | Plantillas, pruebas de encaje, comprobación de volúmenes y acceso de herramientas. | No tomar un buen encaje como aprobación de una pieza final bajo tensión permanente o calor. |
| PETG | Candidato económico para soportes o tapas, con geometría y orientación adecuadas. | Comprobar rigidez, deformación bajo carga, temperatura real y estabilidad del ajuste. |
| ASA o PC/blend | Alternativas cuando la necesidad térmica o mecánica lo justifique. | Fabricación adecuada al material; no elegirlos solo por su nombre. No se ha acreditado que sean necesarios para este soporte. |
| PA/PA con fibra | Alternativas técnicas para un diseño concreto y un proceso controlado. | Considerar humedad, impresión, dirección de capas y coste; fibra de carbono no equivale a mejora universal. |
| TPU | Amortiguadores o protectores auxiliares donde se necesite elasticidad. | No sustituir sin ensayo una junta calibrada, un apoyo de eje rígido o un neumático que afecta a la odometría. |
| Metal comercial conservado o equivalente | Pasadores, muelles, casquillos y roscas sometidas a mantenimiento. | Ajuste, desgaste, corrosión y fijación compatibles con el conjunto. |

Los papeles de materiales de esta tabla son recomendaciones de ingeniería para seleccionar candidatos, no una homologación del soporte.

### Qué dicen los datos de ensayo y qué no prueban

Las fichas de Prusament ilustran por qué no hay que resumir un material en “aguanta X grados” o “es más fuerte”:

| Material concreto de la ficha | Temperatura de deflexión bajo carga declarada, ISO 75 | Observación útil |
|---|---|---|
| Prusament PLA | 55 °C a 0,45 MPa y a 1,80 MPa. | No es una temperatura garantizada de uso continuo de cualquier pieza PLA. |
| Prusament PETG | 68 °C a 0,45 MPa y a 1,80 MPa. | Su ficha también separa propiedades del filamento, probetas impresas y adhesión entre capas. |
| Prusament PA11-CF | 192 °C a 0,45 MPa; 152 °C a 1,80 MPa. | La carga del ensayo modifica la cifra; no autoriza afirmar que un soporte funcionará indefinidamente a esas temperaturas. |

Son valores de formulaciones, probetas y condiciones específicas, no del robot. Las fichas advierten que los resultados dependen del proceso de impresión. [F10, F11, F12] Además, la propia página de PA11-CF declara menor adhesión entre capas que PA sin fibra y exige condiciones de fabricación particulares: es un motivo concreto para no recomendar “nylon con carbono” como mejora automática. [F13]

En la geometría propuesta, ensayar primero la orientación que evite abrir las capas en la raíz cargada. Añadir material donde pasa la fuerza, suavizar cambios de sección y dejar sitio a la herramienta. El número final de perímetros, espesor y orientación se define con el soporte real y sus pruebas; no corresponde anunciar una mejora porcentual de resistencia sin comparar piezas ensayadas.

Preservar inicialmente depósitos, conductos y juntas originales. La documentación de Prusa muestra que una impresión puede presentar poros o uniones que impiden la estanqueidad. [F7] Un conducto aparentemente sólido no queda validado para aspiración o agua solo por inspección visual.

## 6. Verificación mínima antes de ampliar el rediseño

Propuesta de validación escalonada:

1. **Geometría en banco:** comparar interfaces con la pieza original; comprobar asiento, alineación, espacio de herramienta y retención de tornillos y pasador. Rechazar si exige deformar el conjunto para montarlo.
2. **Movimiento:** comprobar recorrido completo sin interferencias; incorporar después el muelle equivalente y verificar retorno, topes y detección de elevación. No usar un muelle más fuerte como sustituto de un apoyo mejor diseñado.
3. **Carga y estabilidad:** observar el soporte con el peso y las posiciones habituales del robot. Registrar desplazamiento, aflojamiento o cambio de alineación. Repetir la medición tras uso y reposo para detectar deformación progresiva.
4. **Prueba funcional controlada:** recorrer una superficie despejada, comparar giro y avance, y comprobar entrada/salida de estación. Supervisar sin exponerlo a una caída para comprobar sensores de borde.
5. **Seguimiento:** revisar grietas, polvo de desgaste, marcas de roce, desplazamiento del pasador y pérdida de apriete. Aumentar gradualmente el intervalo entre revisiones si no aparece evolución.
6. **Servicio:** desmontar y volver a montar el módulo; registrar herramientas, fijaciones y piezas ajenas que hubo que retirar. Esa es la comprobación real de que el mantenimiento se ha simplificado.

No se fija aquí una cifra arbitraria de ciclos o días que convierta un prototipo en “definitivo”. La prueba debe representar el recorrido, obstáculos y horas de funcionamiento reales y documentar las condiciones. Si la pieza se deforma, mover el tornillo o aumentar relleno a ciegas no identifica la causa: revisar carga, orientación, temperatura y geometría.

## 7. Qué aporta OOMWOO y qué archivos existen realmente

**Actualización:** la auditoría detallada del diseño principal y del experimento de CAD automático, con las implicaciones para esta unidad Xiaomi, está en [09 — Comparación OOMWOO](09-oomwoo-comparacion.md). Las conclusiones de ese capítulo prevalecen sobre esta primera revisión.

OOMWOO es útil como ejemplo de proceso y organización: adquirir componentes comerciales, documentarlos, reconstruir CAD y diseñar alojamientos imprimibles. Su artículo de diseño muestra piezas físicas y explica cambios realizados después de prototipos; no equivale a un conjunto terminado compatible con este Xiaomi. [F14]

En la consulta actual, su web indica que aún no está listo para construir y distingue tareas de navegación/acoplamiento simuladas de prototipos mecánicos. Las instrucciones de montaje del repositorio siguen identificadas como provisionales. [F15, F16]

El repositorio `makerspet/oomwoo-cad` contiene CAD nativo Fusion del chasis principal, STEP de subconjuntos y modelos de componentes comerciales, incluido `lib/roborock/OOM-W01-drive-wheel-assembly.stp`. El STEP del robot completo pertenece a un experimento distinto con errores reconocidos; no es una exportación validada del chasis principal. La inspección del árbol público no encontró STL. No hay evidencia de que ese módulo Roborock coincida dimensionalmente con el X20 Pro. [F17] La existencia de CAD es útil para estudiar cómo organizar subconjuntos, no para imprimir directamente un recambio Xiaomi.

Otros proyectos comprobados durante esta investigación:

| Proyecto primario | Evidencia disponible | Límite para este encargo |
|---|---|---|
| `AlieksieievYurii/vacuum-cleaner` | Documenta un robot físico con piezas impresas y componentes comerciales. | El árbol público consultado no contiene STEP, STL, Fusion, OpenSCAD ni FreeCAD. No se presenta como paquete CAD descargable. [F18] |
| `chrismawson/OpenVac-Mk1` | Describe una arquitectura modular y objetivos de publicación. | En la versión consultada solo aparecen README y licencia; CAD está pendiente. No es una solución lista para fabricar. [F19] |

No se ha verificado un repositorio público con todo el X20 Pro modelado, dimensionalmente validado y adaptado a FDM. Esta búsqueda no demuestra que no exista algún archivo aislado; significa que no hay base comprobada para prometer una reconstrucción inmediata por descarga.

## 8. Presupuesto y decisión siguiente

El presupuesto real se obtiene después de definir la pieza. Para fabricación propia, calcular masa prevista por el laminador multiplicada por el precio real por unidad de masa, añadir tornillería/casquillos, pruebas fallidas y consumibles. Para encargo, pedir cotización de la pieza con material, orientación y acabado definidos. El coste dominante de un chasis completo puede ser el tiempo de diseño y ajuste, aunque su plástico sea barato. Son criterios de estimación, no precios de mercado observados.

La siguiente entrega concreta debería ser un modelo paramétrico del apoyo averiado con un dibujo de su montaje y una pequeña prueba de ajuste. Para producirlo hacen falta fotografías de ambas caras de la rotura, del pasador y del anclaje del muelle, junto con las medidas de la tabla. El robot completo se rediseña solo después de demostrar que esa primera mejora se monta, funciona y se repara con menos trabajo.

## Fuentes primarias y referencias para el dossier

- **F1. Mitutoyo, Calipers / Quick Guide**, especialmente apartado sobre errores de medida. https://www.mitutoyo.com/webfoo/wp-content/uploads/D_section.pdf.
- **F2. Meshroom, SfMTransform**, escala y orientación de reconstrucciones. https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/nodes/SfMTransform.html.
- **F3. FreeCAD, repositorio oficial**, descripción del modelador paramétrico. https://github.com/FreeCAD/FreeCAD.
- **F4. CadQuery, introducción y formatos**, https://cadquery.readthedocs.io/en/latest/intro.html y https://cadquery.readthedocs.io/en/latest/importexport.html.
- **F5. Prusa, Modeling with 3D printing in mind**, https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135.
- **F6. Prusa, Infill**, https://help.prusa3d.com/article/infill_42.
- **F7. Prusa, Watertight prints**, https://help.prusa3d.com/article/watertight-prints_112324.
- **F8. Covestro, Joining Techniques: Engineering Polymers**, apartado de uniones atornilladas. https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557217197.pdf.
- **F9. SPIROL, How to Design the Proper Hole for Heat / Ultrasonic Inserts**, https://www.spirol.com/assets/files/ins-wp-how-to-design-the-proper-hole-for-heat-ultrasonic-inserts-us.pdf.
- **F10. Prusament PLA, ficha técnica v1.1**, https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf.
- **F11. Prusament PETG, ficha técnica v1.1**, https://storage.googleapis.com/prusa3d-content-prod-14e8-wordpress-prusament-prod/2023/10/9f8d2165-tds_prusament-petg_n_en.pdf.
- **F12. Prusament PA11-CF, ficha técnica v1.0**, https://prusament.com/wp-content/uploads/2022/08/TDS_PA11CFB.pdf.
- **F13. Prusament, PA11 Carbon Fiber**, https://prusament.com/materials/prusament-pa11-nylon-carbon-fiber/.
- **F14. Makerspet, OOMWOO 3D Design: How It’s Made**, https://makerspet.com/blog/oomwoo-3d-design-how-its-made/.
- **F15. OOMWOO, web del proyecto**, https://oomwoo.com/.
- **F16. OOMWOO, instrucciones de montaje provisionales**, https://github.com/makerspet/oomwoo/blob/main/docs/BUILD_INSTRUCTIONS.md.
- **F17. OOMWOO CAD**, https://github.com/makerspet/oomwoo-cad. Inspección de archivos mediante lectura del árbol público: https://api.github.com/repos/makerspet/oomwoo-cad/git/trees/main?recursive=1. La licencia del repositorio CAD y la declaración general del proyecto no deben presumirse equivalentes sin revisión: https://github.com/makerspet/oomwoo-cad/blob/main/LICENSE.
- **F18. AlieksieievYurii, vacuum-cleaner**, https://github.com/AlieksieievYurii/vacuum-cleaner. Árbol público consultado en modo de lectura; no se modificó el repositorio.
- **F19. OpenVac Mk1**, https://github.com/chrismawson/OpenVac-Mk1.

Las afirmaciones sobre compatibilidad dimensional, duración y resistencia de las propuestas permanecen sin verificar hasta medir y probar la unidad real. Los repositorios de terceros se consultaron únicamente en modo de lectura. Las propuestas propias se documentan en este dossier.
