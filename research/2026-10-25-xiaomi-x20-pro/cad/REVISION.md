# Revisión del CAD inicial de implantación

25-10-2026. Revisión de la propuesta comunicada por el coordinador; no se ha abierto ni modificado el CAD. Dato actualizado: el coordinador ha comprobado FreeCAD 1.1.4 en el PC y el checkout real del proyecto. La ausencia de FreeCAD en el entorno de investigación, indicada en el informe anterior, no describe ese PC.

## Dictamen

**La entrega propuesta es útil y honesta:** FCStd nativo con envolvente exterior oficial, catálogo de módulos/interfaces pendientes y estudio paramétrico de cartucho separado. No hace falta dibujar un bastidor completo con posiciones ficticias para comenzar el proyecto.

El modelo debe permitir contestar qué se conserva, qué se medirá, qué condición determina cada soporte y qué parte es solo una demostración. Un árbol de nombres vacío sería insuficiente; una tabla de interfaces vinculada a los objetos lo vuelve operativo.

## Objetos y datos mínimos

| Elemento | Contenido mínimo útil |
|---|---|
| Control del documento | Revisión, fecha, unidades, propósito, estado conceptual y lista de comprobaciones realmente realizadas. |
| Envolvente publicada | Referencia Ø350 × 97 mm, fuente Xiaomi y etiqueta de envolvente exterior del producto completo. No interpretar 97 mm como espesor de la base o altura libre interior. |
| Referencias geométricas | Convención X avance/Y izquierda/Z arriba y origen del documento explícito. Todavía no es un eje de rodadura ni un plano de suelo recuperado de la unidad. Registrar después la transformación al marco funcional medido. |
| Módulos conservados | Objeto por conjunto real, ID, función, fotos de referencia por ID, estado mecánico y estado funcional separados. Las posiciones desconocidas quedan pendientes, sin cajas de tamaño inventado colocadas en el origen. |
| Registro de interfaces | Para cada pareja: plano/eje/agujeros de montaje, movimiento permitido, espacio de cable/herramienta, dato pendiente y método de obtenerlo. Por ejemplo, rueda–cartucho y cartucho–bastidor son interfaces diferentes. |
| Parámetros y mediciones | Separar valor publicado, medido y propuesto; unidad, fuente, condición de medida y estado. Una celda pendiente no vale cero. Las expresiones de piezas reales no deben tomar datos DEMO como sustitutos. |
| Estudio independiente | Grupo propio y rótulo visible `DEMO — NO FABRICAR`, con todas las dimensiones de ejemplo identificadas y sistema de coordenadas local. Su desplazamiento fuera de la envolvente es de presentación, no una ubicación propuesta en el robot. |

La función de cada grupo puede registrarse en propiedades y en una hoja del documento. No hace falta modelar placas, tornillos ni chips con detalle antes de medir sus interfaces. Para publicar, bastan referencias F001–F018; no incluir fotos privadas, códigos individuales ni rutas personales incrustadas.

## Cuatro objeciones que debe superar el cartucho

1. **Doble apoyo no identifica el mecanismo real.** Falta confirmar si el pasador queda fijo en el chasis, gira en el módulo o se retiene de otro modo. El estudio debe mostrar una articulación conceptual, sin afirmar ajustes o casquillos originales. No sujetar el pasador rígidamente en todos los elementos ni convertir el apriete del puente en una mordaza sobre la carcasa móvil.
2. **El ancho ocupado importa tanto como el diámetro.** Los dos apoyos, la retención y cualquier casquillo consumen longitud del pasador y espacio lateral. Vincular ambos centros a un eje común en el DEMO, pero mantener explícitos ancho entre caras, apoyo axial, acceso de extracción y espacio de movimiento. Que los agujeros coincidan en CAD no demuestra coaxialidad tras fabricar/apretar.
3. **El anclaje fijo no repara una rotura móvil.** Dos soportes más puente y enganche de muelle resuelven una arquitectura del lado fijo. Si el gancho o alojamiento perdido pertenece a la carcasa móvil de la rueda, necesita otra interfaz/pieza. Dejarla registrada como pendiente; no presentar el estudio como reparación integral de ambas averías.
4. **El muelle, los topes y el detector forman parte del conjunto.** El punto del anclaje cambia brazo de palanca, fuerza y recorrido. El DEMO puede hacer visible esa dependencia, pero no fijar una posición como compatible. Reservar en el registro el barrido de rueda, paso de cable, acción del detector que se identifique y función de los topes. No transformar un detector en tope mecánico ni asumir que una geometría más rígida preserva el comportamiento.

El puente deberá transferir carga hacia el bastidor futuro; todavía falta esa unión. Un soporte muy rígido que termine en una fijación débil solo traslada el fallo. No se deduce resistencia superior o vida útil del aspecto del estudio.

## Validación proporcionada de esta entrega

Guardar y reabrir el FCStd; cambiar una dimensión DEMO significativa y comprobar que los dos apoyos, el puente y las relaciones previstas se actualizan sin perder su eje conceptual. Verificar unidades, árbol, propiedades y ausencia de errores geométricos relevantes. Esto demuestra editabilidad del estudio, no compatibilidad o resistencia del diseño final.

El archivo debe abrir mostrando claramente la distinción entre referencia oficial, objetos pendientes y estudio ilustrativo. Si se produce una captura o exportación del DEMO, conservar esa identificación en el acompañamiento; el nombre del grupo por sí solo se pierde fácilmente en STEP o en una imagen.

## Próximo paso que desbloquea geometría real

Medir contrapartes supervivientes: módulo de rueda y caras que debe alojar, pasador y retención, relación entre pivote y rueda, anclaje móvil conservado o zona que lo perdió, y referencias estables de los conjuntos vecinos. En paralelo, elegir un sistema de medida reproducible para recuperar la implantación global. No pedir fragmentos desaparecidos ni derivar coordenadas de fotos sin escala.

Con esos datos se sustituye una interfaz pendiente por geometría medida. El DEMO puede permanecer como estudio separado; no tiene que convertirse automáticamente en la solución adoptada.


Implementación: los límites figuran en los objetos Alcance/LimitesCartucho y en interfaces.json. La validación de archivo se registra en validacion_cad.json; no incluye ensayos físicos.


## Revisión del código y del registro implementado

El frente de mecánica revisó `scripts/crear_modelo.py` e `interfaces.json`. Confirmó que los riesgos de mitad móvil rota, posición ficticia, giro/retención, pinzamiento, espacio de extracción, muelle mayor y validación física quedan explícitos. No encontró una objeción adicional que impidiese entregar v0.1 como estudio. No recomendó añadir rueda, retenes, muelle, detector o topes inventados para completar el aspecto.

La inspección de las primeras vistas detectó que el desplazamiento fuera de la envolvente no se aplicaba porque FreeCAD devuelve `.Placement.Base.x` con punto inicial. El coordinador corrigió el generador y el documento; la reapertura y la reimportación STEP confirmaron X mínimo 250 mm. Se sustituyó asimismo el render inicial sin contexto OpenGL por capturas del escritorio y se inspeccionaron. El cambio corrige representación y editabilidad, no valida resistencia.

## Ampliación coordinada: carga y servicio de IF01–IF04 frente a IF13

25-10-2026, después de d764569 y de la aportación f4d87c5. Revisión documental del registro, del generador y de las propiedades guardadas del CAD; no es un ensayo ni una nueva geometría. Atiende el reparto del compañero recogido en `coordinacion/para_codex.md`. La investigación pública es la primera vía acordada con el propietario; el paquete de medidas físicas anterior no es condición para continuar el diseño provisional.

El capítulo 12 ya cubre giro, mitad móvil rota, barridos, muelle y presupuesto axial. Esta ampliación concreta **qué superficie toma cada carga y en qué orden se repara**, sin añadir otra lista de cotas.

| Interfaz | Referencia recuperable o pendiente | Camino de carga propuesto y pieza sustituible | Ruta de servicio que debe resolver el CAD | Condición de aceptación pendiente de comprobar |
|---|---|---|---|---|
| IF01 / IF02, cada lado independiente | Eje y contracaras sanas del módulo; Ø4 × 38,5 mm publicado como referencia provisional, no ajuste | Rueda/carcasa → articulación → apoyos → placa. Distinguir reacción transversal al pasador, empuje axial y retención contra escape; asignar a cada una su superficie. El retén no se da por apto para recoger todo el empuje lateral. Apoyo o casquillo reemplazable si esa interfaz lo justifica | Dos operaciones: retirar cartucho completo del robot; después retirar pasador del cartucho. Si solo cabe hacerlo fuera, documentar servicio en banco y reservar la salida del cartucho completo | Tras apretar, conservar el giro previsto y el juego funcional acordado por lado. La retención sigue operativa durante el mantenimiento de elementos ajenos a la rueda |
| IF03 | Eje del pivote y enganche móvil conservado, o reparación móvil todavía pendiente; anclaje fijo por diseñar | Muelle → enganche móvil/carcasa y anclaje fijo → pie y fijaciones del cartucho. Revisar tanto tracción como momento sobre el pie. Anclaje fijo sustituible; la mitad móvil necesita su solución propia | Mantener contenido el conjunto rueda–muelle al sacar el cartucho. Antes de liberar el pivote o un anclaje, definir una posición descargada o una retención mecánica temporal accesible; desconectar el cable no descarga el muelle | La secuencia no libera la rueda impulsada por el muelle. En funcionamiento, cable y detector no reciben la carga del tope ni limitan el recorrido |
| IF04 | Asientos del cartucho y de la cuna del caster respecto a M40; posición nueva declarada cuando la original no sea recuperable | Apoyos y anclaje → placa del cartucho → unión al núcleo. Especificar superficies de localización, reacción al deslizamiento/giro y función de apriete. Sustituir cartucho o cuna sin sustituir el núcleo | Identificar fijaciones accesibles y referencias que permanecen en el núcleo. Tras retirar el conjunto, no depender de volver a alinear ruedas a ojo ni de mover la bandeja electrónica | Tras desmontar, reinstalar y apretar, recuperar posición/orientación dentro de tolerancias funcionales previamente definidas; comprobar que el apriete del núcleo tampoco las altera |
| IF04 ↔ IF13 | Rampa, contactos, boca y bandeja originales; estados M55/M60 aún pendientes | Identificar apoyos efectivos y reacciones para suelo, aproximación y cada postura funcional de estación. No suponer el mismo reparto ni asignar función estructural a contacto, óptica o sello sin identificarla | La reinstalación de un cartucho debe recuperar también la postura de estación, sin reajustes ocultos de contactos, sellos o mopas | Comparar antes/después del servicio: aproximación y funciones disponibles sin nuevo choque, pérdida del apoyo previsto ni pérdida de contacto o sello. Registrar cada función realmente probada |

### Decisión para la próxima geometría

Desarrollar primero la **extracción del cartucho completo, con la suspensión contenida**, y tratar la salida axial del pasador como una operación de banco cuando el espacio dentro del robot no la permita. Es una propuesta de arquitectura, no una ruta ya comprobada. Reduce la necesidad de reservar dentro del robot todo el recorrido lateral del pasador; todavía requiere volumen de salida del cartucho, acceso al conector y herramienta. La dirección de salida queda por determinar con la implantación, no se fija como inferior sin evidencia.

El DEMO incorpora taladros de los apoyos y del anclaje, pero su placa declara expresamente pendiente la unión al bastidor. Esos taladros no prueban por sí solos la localización del cartucho, la retención ni la accesibilidad. En la próxima geometría debe quedar visible el recorrido completo de la carga hasta el núcleo y el camino de la herramienta hasta cada fijación utilizada en esa extracción.

Para el asiento desmontable, separar en el dibujo las superficies que localizan de las fijaciones que mantienen el contacto. Estudiar también las fuerzas que intentan separar el asiento o hacerlo deslizar; no suponer que cualquier tornillo absorbe esas funciones por estar presente. Es una aplicación propuesta de los principios de [localización y apriete de Carr Lane](https://www.carrlane.com/engineering-resources/fixture-design-principles/locating-clamping-principles/ctl), cuya fuente trata utillajes de mecanizado: no aporta cargas ni tolerancias del X20 Pro.

La necesidad de contener la suspensión durante el servicio deriva de que el muelle de tracción almacena energía y ejerce fuerza entre sus extremos ([Lee Spring](https://www.leespring.com/learn-about-extension-springs)). No se especifica todavía una maniobra de descarga para esta rueda, cuya geometría e integridad no están confirmadas.

### Dos vínculos por incorporar al actualizar conjuntamente registro y CAD

- **IF02 → M15 por lado.** IF01 incluye juego axial/radial y IF02 lo omite. La revisión del lado derecho necesita el mismo tipo de comprobación, con resultado independiente.
- **IF04 → IF13 / M55 / M60.** El reparto de cargas y la repetición del montaje dependen también de las posturas de estación. Es un vínculo entre requisitos, no una nueva medida duplicada.

El registro v0.1 y sus propiedades nativas conservan su estado publicado. Estos dos vínculos quedan señalados para incorporarlos juntos en la siguiente revisión del maestro; no se consideran corregidos por figurar en esta nota.

Las tolerancias, cargas, deformaciones admisibles y vida objetivo siguen sin definir. Las condiciones de la tabla son compromisos verificables del diseño futuro; ninguna figura como superada. Para evaluar reparabilidad se registrarán las piezas y fijaciones realmente retiradas, los reajustes necesarios y el resultado tras reinstalar. Esa evidencia podrá mostrar si el cartucho evita desmontar conjuntos ajenos; una imagen de despiece no lo demuestra.
