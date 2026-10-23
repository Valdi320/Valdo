# Baterías cauchos lubricantes y electrónica para reposición propia

Consulta del 23/10/2026. Se mantiene el objetivo de producción y reparación propias con desembolso cotidiano nulo. Este capítulo examina cadenas que todavía obligan a adquirir materiales o servicios industriales. [D] dato publicado; [I] inferencia; [P] propuesta; [A] pendiente. [Operaciones y observaciones](datos/materiales_criticos_2026-10-23.json).

**Conclusión:** la batería de flujo abierta de FBRC ofrece una vía concreta para investigación reproducible, pero sus propios documentos limitan el kit a educación y desarrollo. El níquel-hierro merece comparación por mantenimiento y duración; no elimina agua de reposición, electrolito o fabricación de electrodos. Obtener caucho de una planta, aceite de una cosecha o transistores en un garaje reduce una parte de la dependencia, sin cerrar todavía el resto de su cadena.

## Baterías duraderas y necesidades de mantenimiento

**[D]** El manual de baterías FL de níquel-hierro conservado por Bimble Solar exige revisión del nivel y reposición con agua destilada o desionizada, protección de conexiones contra corrosión y condiciones de ventilación. Contempla sustituir electrolito en determinadas circunstancias. [157] **[I]** Su larga duración potencial no equivale a ausencia de mantenimiento ni a que cualquier recipiente y electrodo produzcan una batería equivalente.

**[D]** Perma Batteries anuncia para sus elementos níquel-hierro más de 25 años de vida y rendimiento energético del 70 al 80 %. Su página también describe revisiones periódicas del nivel de electrolito y posibles reposiciones. [158] Son prestaciones y pautas del proveedor para su producto, sin una comprobación independiente aquí. No se adopta su publicidad de inversión para décadas como garantía de que todos los componentes duren indefinidamente.

**[P]** Si se elige extraer 2 kWh diarios de una batería con rendimiento de ida y vuelta del 70 u 80 %, la energía de carga sería 2,857 o 2,500 kWh diarios. La diferencia es 0,357 kWh/día, unos 130,36 kWh/año con uso constante elegido. No incluye inversor, autodescarga, temperatura ni consumo de control; tampoco dimensiona un banco real. A igualdad de servicio, duración y mantenimiento deben evaluarse junto a las pérdidas, especialmente en invierno.

**[D]** La página de prototipo de Open Source Ecology conserva tareas de selección de electrodos, lista de materiales, estimación de fabricación y construcción y ensayo de prototipos. [156] **[I]** Esa lista no demuestra que exista una línea doméstica terminada con coste, capacidad y vida verificados. El acceso a investigación histórica no resuelve el suministro local de níquel, reactivos, separadores, recipientes o utillaje.

**[P]** Antes de recomendar níquel-hierro para esta meta: exigir precio entregado del modelo, capacidad a la descarga prevista, masa, espacio, agua consumida por año, trabajo, pérdidas y condiciones de reparación. No se ha obtenido una oferta actual completa. El manual de una familia y la ficha de otro proveedor no deben combinarse como si describieran un único equipo.

## Una batería de flujo realmente abierta para investigar

**[D]** El registro OSHWA FR000028 identifica el Redox Flow Battery Development Kit versión 1.0.0, certificado el 28/08/2025, con superficie de ensayo de 2 cm² y licencias CERN-OHL-S-2.0 para hardware, software y documentación. [161] La certificación de apertura no es una certificación de seguridad eléctrica, capacidad doméstica o vida útil.

**[D]** La documentación actual del kit especifica que se destina a educación e investigación, no a aplicaciones reales de almacenamiento. [160] El informe de octubre de 2025 describe una celda de mayor formato de 175 cm² todavía en desarrollo. [163] Las actualizaciones de marzo y mayo de 2026 muestran continuidad de experimentos con distintas químicas; no anuncian allí un banco doméstico terminado. [164,165]

**[D]** La lista de materiales del kit contiene bombas peristálticas, separador, fieltro conductor, grafito, juntas, tubos, microcontrolador, fuente y piezas impresas. También necesita instrumental de ensayo. [162] **[I]** Imprimir marcos y publicar planos mejora la posibilidad de reparación, pero todavía deja componentes industriales y consumibles. La fabricación completa desde materias primas propias exigiría reproducirlos y mantener las herramientas que los producen.

**[D]** El manual del instrumento MYSTAT usado por el proyecto describe convertidores analógico-digitales, microcontrolador PIC16, programación y calibración. [170] **[I]** Fabricar una placa no equivale a fabricar sus chips, y una medida repetible necesita también una referencia de calibración. La apertura del conjunto experimental no debe atribuirse automáticamente al diseño interno de cada componente comprado.

### Qué aporta el ensayo de marzo de 2026

**[D]** El cuaderno de Kirk Pollard Smith del 26/03/2026 publica diez ciclos de una celda de 2 cm² con 11 mL, eficiencia energética superior al 70 % y una pequeña fuga o cristalización. [171] **[I]** No acredita funcionamiento doméstico duradero.

**[I]** Su cálculo integra corriente, tensión y tiempo de la celda, sin energía de bombas: no es el rendimiento del sistema instalado.

**[P]** Ejemplo para expresar el efecto, sin atribuir estos consumos al prototipo: entregar 2 kWh/día con una celda al 70 % requiere 2,857 kWh de carga. Si unas bombas consumieran además 10 W durante 24 horas, añadirían 0,240 kWh y el cociente útil/entrada bajaría aproximadamente al 64,58 %. Es una comparación contable elegida; no una medida o predicción de FBRC, y omite otras pérdidas.

### Dos observaciones que podemos aportar a su documentación

Dos discrepancias condicionadas a confirmar las masas físicas:

1. **[I] KI:** declara 3,32 g, pero calcula con la variable de ZnCl₂ de 1,40 g. Para 11 mL y 166,0028 g/mol, esas masas darían respectivamente **1,818 y 0,767 mol/L**.
2. **[I] Masa total:** omite 1,08 g de NH₄Cl; los cinco ingredientes declarados suman **14,89 g**, frente a **13,81 g** en el denominador. También debe aclararse si se expresa concentración por masa de solución o de disolvente.

**[I]** No invalidan la medida eléctrica, cuya integración no usa las masas. **[P]** Corregirlas exige confirmar preparación y unidades. No se contactó al autor ni se modificó su repositorio.

## Un artículo llamado abierto que no cumple nuestra prioridad de licencia

**[D]** La tabla indexada de “Open source all-iron battery 2.0” indica CC BY-NC-ND 4.0, costes históricos de 4,58 a 13,74 USD por celdas de 8 mL y unos 400 USD de montaje para 50 celdas. El resumen publica potencia máxima de 250 mW/L. La apertura directa del artículo devolvió 403: estos datos se limitan al contenido indexado. [159]

**[I]** La restricción NC-ND no es equivalente a permitir modificar y redistribuir libremente un diseño. No se ha comprobado una licencia distinta de sus archivos fuente, así que no se adopta como base abierta confirmada. Los dólares históricos tampoco son un precio actual por kWh de banco instalado.

**[P]** Como comprobación de escala, 250 mW/L equivalen a 0,25 W/L: alcanzar 1.000 W exigiría 4.000 L si se conservara linealmente esa densidad máxima. No es un dimensionado viable ni incluye recipientes, conexiones o conversión; muestra por qué una química barata no basta para una batería compacta. El artículo describe una batería convencional, no la plataforma de flujo de FBRC: no se transfieren entre ambas cifras o limitaciones.

## Caucho cultivable y piezas que se desgastan

**[D]** Continental documenta el uso de caucho de Taraxacum kok-saghyz y la comercialización de Urban Taraxagum, cuya banda de rodadura utiliza caucho de diente de león. Distingue ese material del neumático completo: en sus neumáticos de turismo el caucho natural supone aproximadamente el 10 al 30 % del peso, según uso. [167] No se extrapolan esos porcentajes a cualquier cubierta de bicicleta.

**[I]** Es una prueba de que una materia prima alternativa puede entrar en productos reales. No aporta una receta abierta doméstica de neumático ni permite afirmar que cultivar el diente de león común proporcione una cubierta lista. Faltan selección de planta, cultivo local, extracción, formulación y fabricación de los demás componentes.

**[D]** HSE describe mezclado de caucho y aditivos, laminado o extrusión y procesos de curado en la producción de artículos de goma. [168] **[I]** Extraer polímero de una raíz no resuelve la formulación para humedad, temperatura, desgaste o contacto con sustancias. La química adecuada para una junta tampoco es necesariamente la de una suela o cubierta.

**[P]** Empezar por una pieza estática de baja exigencia con función y material conocidos sería más verificable que intentar una cubierta de transporte. La investigación deberá registrar composición, compresión, envejecimiento, pérdidas y trabajo. No se propone usar una formulación experimental en frenos, neumáticos, sellos de presión o barreras sanitarias sin validación correspondiente.

## Lubricación desde cultivos propios

**[D]** La investigación de USDA ARS sobre lubricantes vegetales describe sus ventajas como fluidos base y las limitaciones de oxidación y comportamiento a baja temperatura. Estudia aceites de alto contenido oleico junto con aditivos para mejorar esas propiedades. [169] **[I]** Que el aceite sea renovable no significa que un aceite alimentario sirva directamente en cualquier rodamiento, motor o transmisión.

**[P]** Para una ruta propia habría que resolver cultivo y extracción, variabilidad entre lotes, formulación, almacenamiento y compatibilidad con el mecanismo. Después se compararían fricción, desgaste, corrosión y duración frente al producto especificado. Si los aditivos siguen comprándose, se registran como dependencia aunque su masa sea pequeña. Producir más aceite no compensa automáticamente una formulación inadecuada que acorta la vida de la máquina.

## Semiconductores fabricados a pequeña escala

**[D]** Sam Zeloof documentó en 2021 una matriz Z2 de cien transistores por chip, con proceso de 10 µm y varios chips en una misma pieza de silicio. Explica que compró obleas con óxido y polisilicio depositados industrialmente; describió al menos un chip completamente funcional, sin estadísticas suficientes de rendimiento de fabricación. [166]

**[I]** La demostración rebaja la barrera para fabricar dispositivos sencillos con medios pequeños. No reproduce desde arena el material de partida, ni acredita CPU, memoria, electrónica de potencia y sensores capaces de sustituir todos los equipos de una vivienda. Tampoco demuestra capacidad de producir el ordenador de IA local o mantener sus herramientas de fabricación durante décadas.

**[D]** LibreSilicon plantea abrir procesos y herramientas de fabricación y reconoce que los nodos necesitan fabricantes e infraestructura reales para resultar útiles. [24] **[P]** La ruta relevante para nosotros comienza con la función más sencilla que pueda sustituirse: un sensor, interruptor o control elemental. Solo después habría que evaluar integración, consumo, encapsulado y duración. Hacer más transistores no es por sí mismo un indicador de autonomía doméstica.

## Prioridades de desarrollo y condiciones para cambiar de decisión

| Ruta | Avance propio razonable | Qué debe demostrarse antes de depender de ella |
|---|---|---|
| FBRC | Revisión de unidades y composición; balance eléctrico con auxiliares; documentación de piezas sustituibles | Capacidad y potencia útiles, estabilidad, mantenimiento, fugas, reposición y coste de conjunto |
| Níquel-hierro | Comparación de un banco concreto con demanda y tiempo de mantenimiento | Capacidad real a su régimen, agua, pérdidas, garantía, masa y oferta completa |
| Caucho local | Identificar una pieza sencilla y una formulación reproducible | Calidad de material, envejecimiento y cadena local de aditivos y herramientas |
| Lubricantes vegetales | Estudiar una aplicación concreta y sus requisitos | Desgaste y estabilidad comparables; origen de aditivos y reposición |
| Microfabricación electrónica | Describir un dispositivo simple que falte y el proceso necesario | Rendimiento de fabricación repetible, materiales, encapsulado, instrumental y función útil |

**[I]** Estas rutas compiten por tiempo, energía y espacio. Una línea abierta útil para un laboratorio comunitario puede ser una mala primera inversión para una vivienda que busca poca intervención. Seguir una vía comunitaria no equivale a independencia de otras personas, aunque reduzca dependencia de un proveedor único.

**[P]** La primera mejora documental queda identificada en el cuaderno de batería; la siguiente comparación debe añadir una alternativa que evite consumibles difíciles, por ejemplo reducir almacenamiento eléctrico trasladando ciertos usos a horas de sol o acumulando calor. Debe evaluarse la misma función y comodidad, sin contar energía térmica como si pudiera alimentar directamente el ordenador.

**[I]** No hay un plazo demostrado para cerrar conjuntamente estas cadenas. Un calendario de laboratorio o una vida comercial anunciada no predice cuándo una persona podrá reproducirlas sin suministros externos. El avance se medirá por funciones y dependencias eliminadas con evidencia, sin declarar conseguido el gasto cero.

## Precios y alcance documental

Esta entrega no añade una cesta de compra. Conserva los costes del artículo de hierro como históricos y no asigna precio a celdas FBRC sin presupuesto completo. El banco níquel-hierro necesita oferta vigente y condiciones de entrega, impuestos y mantenimiento. No se ejecutaron compras, fabricación, instalación o ensayos físicos; la revisión de fórmulas fue documental y aritmética.
