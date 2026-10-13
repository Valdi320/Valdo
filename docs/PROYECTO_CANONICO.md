# PROYECTO FUTURO — Fábrica Doméstica Autónoma Abierta (FDAA)

> **Documento canónico de visión, investigación y hoja de ruta — v0.1, 13 de octubre de 2026.**
>
> **Estado real:** idea investigada, sin prototipo integral construido ni presupuesto aprobado. Las medidas y prestaciones propuestas son **hipótesis de diseño** que deben someterse a ingeniería, simulación y pruebas. Este texto está preparado para publicarse como una *issue* de GitHub y convertirse después en un repositorio técnico independiente.
>
> **Principio rector:** descentralizar la capacidad de comprender, inventar, fabricar, mantener, reparar y reciclar objetos mediante una combinación de herramientas abiertas, IA local y robótica, reduciendo dependencia de la nube, de fabricantes y de piezas descatalogadas.

## 0. Resumen ejecutivo: el sistema completo

La aspiración es que una persona pueda enseñar al sistema una pieza o máquina, describir su problema o función deseada, recibir un diseño técnico editable y ver cómo un robot obtiene o fabrica las piezas necesarias, desmonta el aparato, lo repara, verifica su funcionamiento y vuelve a dejarlo en su posición original. Cuando el robot necesite mantenimiento, una **base-taller o un segundo robot** podrán encargarse de él. Todo funcionará fundamentalmente de manera local.

**Subconjuntos que deben encajar:**

1. **Descompilador digital:** análisis de software y firmware; recuperación de lógica mediante Ghidra y herramientas complementarias, con verificación diferencial.
2. **Descompilador físico:** escaneo 3D, metrología, análisis de materiales, sensores eléctricos y funcionales, reconstrucción CAD paramétrica, esquemas y modelos físicos.
3. **IA local de 16–24 GB de VRAM como referencia inicial:** planificación, herramientas, conocimiento recuperable, modelos de visión y manipulación especializados, ejecución offline, memoria verificable.
4. **Microfábrica doméstica multimaterial:** impresión 3D, acabado, ensamblaje, ensayos y recuperación de residuos; no solo extruir plástico.
5. **Materiales abiertos y de ciclo circular:** celulosa, lignina, PHA, fibras, almidón, minerales y materiales reciclados, combinados con arquitectura geométrica; sin exigir que todos sean biodegradables.
6. **Robot reparador compacto de dos brazos:** circulación autónoma, manipulación precisa y capacidad física de realizar una reparación completa, incluidos sacar y volver a meter electrodomésticos.
7. **Movilidad todoterreno doméstica:** cuatro ruedas-patas como candidato, escaleras, muebles que bloquean, rampas o puentes desplegables, obstáculos inesperados.
8. **Segundo robot cooperativo:** rescate, mantenimiento mutuo e intercambio de herramientas y módulos.
9. **Estación de carga y mantenimiento:** localización, docking, autodiagnóstico, recambios y un pequeño manipulador de reparación independiente.
10. **Seguridad, privacidad y documentación:** verificación, diseño para desmontaje, control de riesgos, medición, registro de fallos y datos locales.

**La meta no es una máquina omnisciente ni una autorreplicación perfecta.** Seguirán haciendo falta energía, materias primas, electrónica industrial, trabajos profesionales regulados y ciertos recursos externos. El éxito será aumentar progresivamente la proporción de necesidades que se pueden resolver con seguridad de forma local.

---

## 1. Cronología de la conversación y decisiones que deben conservarse

### 1.1. De compilar/descompilar a comprender y reconstruir

Partimos de la diferencia entre un **compilador**, que convierte fuentes de alto nivel en código ejecutable, y un **descompilador**, que intenta recuperar una representación de alto nivel desde el ejecutable. Aunque pueden compartir análisis de control y datos, representación intermedia y herramientas, no son inversos perfectos. Compilar → descompilar → compilar reiteradamente **no garantiza idempotencia, equivalencia binaria, equivalencia semántica ni un código mejor**. Hay pérdida de nombres, tipos, intención, comentarios, estructura y optimizaciones irreversibles.

La estrategia correcta es guardar el ejecutable original como referencia inmutable, recuperar funciones y relaciones, construir código mantenible y realizar **pruebas diferenciales** entre comportamientos; no repetir transformaciones esperando recuperar información perdida.

### 1.2. Referencia práctica de Ghidra y recompilación

En un trabajo distinto sobre un ejecutable ARM de Nintendo 3DS se consiguió una recompilación estática y se desarrolló una exportación masiva con Ghidra. Un estado comprobado el 13/10/2026 indicaba **23.743 funciones detectadas por Ghidra y 18.499 exportaciones satisfactorias**, mientras otro analizador proponía más entradas (algunas resultaron falsas o no concordaban). Esto demostró que la producción automática de pseudocódigo a escala es factible, pero que **exportar sin errores no equivale a comprender correctamente cada función ni a disponer de un programa de alto nivel compilable**.

Este antecedente es metodológico. La fábrica doméstica es un proyecto separado. **No se publicarán ROMs, código de juegos, firmware propietario ni otros materiales protegidos** como parte de este proyecto.

Otro referente es [Claude's C Compiler](https://github.com/anthropics/claudes-c-compiler) de Anthropic: experimento de construcción de un compilador C en Rust mediante agentes. Ilustra el valor de una orquestación rigurosa de tareas, pruebas y verificación; no demuestra que la decompilación sea universal.

### 1.3. La analogía física

Nos preguntamos si se podría desarrollar un «Ghidra de objetos reales». Un escáner 3D recupera una **superficie**; un descompilador físico verdadero debería devolver **geometría CAD editable, materiales, conexiones, funcionamiento, tolerancias, proceso de fabricación y nivel de confianza**. El campo ya dispone de piezas de la solución —fotogrametría, tomografía, espectrometría, osciloscopios, análisis CAD—, pero **no existe un dispositivo universal y portátil que lo comprenda todo**.

### 1.4. Materiales y autosuficiencia

La aspiración fue encontrar un material barato, disponible en todas partes, biodegradable, reciclable y apto para cualquier objeto. La conclusión fue preferir una **familia pequeña y compatible de materiales** y explotar también los **metamateriales geométricos**. Una misma composición puede exhibir rigidez, flexibilidad o amortiguación distintas por su arquitectura, pero esa técnica no crea por sí sola un semiconductor, un metal conductor o una batería.

### 1.5. Robots y reparación de verdad

Se añadió un robot capaz no solo de cambiar piezas sino de **acceder al objeto físicamente**, desplazar neveras/lavadoras, sacar una placa de la encimera sin romperla, desmontar, probar, montar y colocar de nuevo. Posteriormente, un segundo robot que pueda reparar al primero —y viceversa—, además de una estación-taller independiente.

### 1.6. Navegación, rampas, acoplamiento y dimensiones

El robot debe resolver camas atravesadas, objetos caídos, escaleras y lugares sin una ruta despejada. Las **rampas plegables** se aceptan como herramientas, especialmente para huecos y pequeños desniveles, pero **subir cada escalón mediante cuatro ruedas-patas** puede ser más compacto que transportar enormes rampas. Se estudiaron las funciones de retorno de un Xiaomi Robot Vacuum S12 como ejemplo de cómo combinar mapa, odometría y alineación IR. Se propuso una estación con marcadores visuales AprilTag.

La referencia dimensional inicial quedó en **45 cm de ancho × 70 cm de largo × 40 cm de alto plegado**, con torso extensible y dos brazos. **No está verificado que quepan todos los actuadores y baterías sin sacrificar fuerza, seguridad o autonomía.**

---

## 2. Descompilador físico portátil: qué tiene que medir y devolver

### 2.1. Cadena de resultados

**Objeto → medidas multimodales calibradas → hipótesis contrastables → gemelo digital → CAD/BOM/esquemas → simulación → fabricación de prueba → medición de equivalencia → diseño corregido.**

| Instrumento/módulo | Información que puede aportar | Lo que NO garantiza |
|---|---|---|
| Fotogrametría, cámaras RGB y macro | Color, marcas, textura, geometría visible, desgaste | interior opaco y composición |
| Luz estructurada / escáner óptico 3D | nube de puntos, malla y dimensiones externas | fuente CAD original y tolerancias |
| Microscopía | circuitos y materiales visibles | capas ocultas y lógica completa |
| Ultrasonidos compatibles | fallos y estructuras internas de ciertos sólidos | funcionamiento universal en todo material |
| Termografía | patrones térmicos y fallos posibles | causa única |
| Raman / IR / NIR / XRF | firmas químicas o elementos en materiales apropiados | todos los aditivos o procesos de fabricación |
| Multímetro / sondas de continuidad / medidor de impedancia | redes y componentes eléctricos accesibles | esquema completo de placa multicapa |
| Osciloscopio / analizador lógico | comunicaciones y señales | significado íntegro de firmware |
| Masa, ensayos mecánicos, vibración | densidad aparente, rigidez, resonancias | receta original única |
| Tomografía industrial de terceros | partes internas de objetos compatibles | barato, portátil, universal o inocuo |

La tecnología debe **registrar resolución, calibración, unidades, fecha, error e incertidumbre**. No mezclar datos medidos con inferencias de IA sin marcarlo.

### 2.2. Hardware propuesto

- **Unidad de mano**: cámaras, lente macro, iluminación polarizada, sensor de profundidad o luz estructurada calibrada y marcadores de escala.
- **Módulos acoplables**: contacto mecánico, termografía, medición de señales y sondas de material cuando proceda.
- **Estación de procesamiento**: GPU local, CAD, análisis físico, simulación y almacenamiento; no obligar a llevar una gran GPU en la mano.
- **Servicios externos opcionales**: tomografía industrial, microscopía avanzada o ensayos destructivos. El aparato no necesita integrar fuentes de radiación ionizante.

### 2.3. Software de reconstrucción activa

1. Detectar el tipo aproximado de objeto y sus superficies.
2. Crear una geometría preliminar y segmentar componentes, juntas, tornillos y posibles funciones.
3. Mantener varias hipótesis de material/topología/comportamiento con grados de confianza.
4. Elegir **la medición siguiente por ganancia de información esperada** y riesgo/coste, en vez de escanear todo sin criterio.
5. Recuperar primitivas y operaciones CAD (revoluciones, extrusiones, agujeros, patrones, roscas) y sus cotas; conservar la malla original.
6. Estimar uniones, restricciones, conexiones y comportamiento observado.
7. Simular, medir de nuevo y revisar la hipótesis cuando falle.
8. Exportar **CAD paramétrico editable**, planos, BOM, materiales, incertidumbres, protocolo de fabricación y pruebas.

**Fuentes precursoras:** [OpenScan](https://github.com/OpenScan-org), [OpenScan Mini](https://github.com/OpenScan-org/OpenScan-Doc/blob/main/docs/hardware/OpenScanMini.md), [FreeCAD](https://github.com/FreeCAD/FreeCAD), [CadQuery](https://cadquery.readthedocs.io/), [Degate](https://github.com/DegateCommunity/Degate), [PulseView](https://sigrok.org/wiki/PulseView). La automatización de CAD desde escaneos (incluidos enfoques de Fraunhofer de reconstrucción asistida por IA) es una línea precedente; no significa que los resultados sean automáticamente fabricables y equivalentes.

### 2.4. Límite fundamental

Dos objetos de interior distinto pueden verse iguales por fuera y comportarse igual en las pruebas realizadas. **Ninguna IA puede recuperar certeza sobre propiedades que no son observables.** El sistema deberá solicitar apertura, otras mediciones, laboratorio o asistencia, y dejar explícitamente sin resolver lo que no pueda verificar.

---

## 3. Descompilación de software y firmware integrada con lo físico

- **Referencia inmutable** de binarios y mediciones, huellas y versiones.
- Ghidra y otras herramientas apropiadas de análisis estático/dinámico, emulación, depuración, detección de tipos, funciones y referencias.
- Recuperación incremental de lógica; renombrado, agrupación en módulos y reconstrucción de estructuras.
- **Pruebas diferenciales** de salidas, memoria, estado, temporización e interacción con hardware antes de sustituir una función.
- Relación entre diagramas eléctricos, sensores, actuadores y firmware cuando exista acceso legítimo.
- No publicar contenido protegido por derechos de terceros; revisar licencias, interoperabilidad y legislación pertinente.

La IA puede ayudar a interpretar algoritmos y proponer reconstrucciones, pero **el código pseudodescompilado no constituye por sí solo fuente completa y mantenible**. Para aplicaciones de usuario, Java y .NET ofrecen otros analizadores de bytecode; para código nativo ARM/x86, usar herramientas compatibles con arquitectura y formato.

Herramientas útiles: [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [3dsrecomp](https://github.com/fearkov/3dsrecomp), [Zakuro](https://github.com/fearkov/zakuro), [Degate](https://github.com/DegateCommunity/Degate). Estas últimas son **referencias tecnológicas de usos distintos**, no promesa de que un solo motor analice todo.

---

## 4. Materiales locales, sostenibles y versátiles

**No perseguir un material mágico** con todas las propiedades. Buscar una **paleta de materiales** compatible con una biblioteca abierta de formulaciones, estructuras geométricas, fabricación y reciclaje.

| Familia | Funciones potenciales | Problemas pendientes |
|---|---|---|
| Celulosa / nanocelulosa | refuerzo, ligereza, piezas estructurales | humedad, anisotropía, procesado |
| Lignina | cargas y formulaciones protectoras/estructurales | variabilidad, compatibilidad |
| PHA producido por microorganismos | polímeros moldeables; biodegradación según formulación y ambiente | coste, separación, temperatura |
| Almidón | formulaciones biodegradables y cargas | envejecimiento, humedad |
| Fibras vegetales | rigidez y resistencia direccional | adhesión y calidad del lote |
| Minerales/cerámica | rigidez, aislantes, resistencia térmica en casos adecuados | fragilidad y energía de proceso |
| Metales reciclados | conductividad, rodamientos, tornillos y cargas elevadas | separación/aleaciones, no biodegradables |
| Tintas conductoras/carbono | sensores y circuitos modestos | no producen microchips modernos |
| Elastómeros durables | juntas, neumáticos, amortiguación | recuperación al final de vida |

**Conceptos separados:** «biobasado», «biodegradable», «compostable», «reciclable» y «no tóxico» **no son sinónimos**. Biodegradable significa bajo determinadas condiciones; no equivale a descomponerse de forma segura en cualquier entorno. [Comisión Europea: marco de bioplásticos](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en).

**Metamateriales mecánicos:** celosías, celdas auxéticas, estructuras tipo giróide y elementos flexibles permiten programar propiedades mecánicas por geometría. Esto puede reducir referencias de material, pero **no reemplaza los requisitos químicos** para conducción, magnetismo, semiconductores, aislamiento o almacenamiento electroquímico.

**Regla de fin de vida:** durabilidad adecuada → reparación → reutilización → desmontaje → reciclaje separado; reservar biodegradación para casos concretos. Diseñar juntas, fijaciones y adhesivos **desmontables** y documentar la composición como un pasaporte digital de materiales.

Producción local de PHA, celulosa procesada y formulaciones nuevas exige evaluar agua, energía, fermentación, productos auxiliares, ventilación, emisiones, coste, calidad, toxicidad y recuperación; que una materia prima sea abundante **no demuestra** que fabricarla en una vivienda sea sencillo o barato. [Revisión de PHA a partir de residuos (2025)](https://www.sciencedirect.com/science/article/pii/S0141813025009079).

---

## 5. Impresora 3D multimaterial → microfábrica doméstica

La impresión FFF/FDM será el núcleo accesible, pero un taller universal necesita otros procesos y logística:

- Cabezal o cambiador de herramientas para familias de materiales compatibles, perfiles de impresión calibrados, control de temperatura y humedad.
- Operaciones auxiliares: roscado, perforación, inserción de fijaciones, acabados y mecanizado cuando tolerancias o composición lo requieran.
- Montaje robotizado con tornillos, conectores, juntas, rodamientos y piezas electrónicas comerciales.
- Posibilidad de fabricar PCB sencillas con procesos apropiados; **no inventar una impresora de chips avanzados**.
- Metrología dimensional, probetas de resistencia/fatiga, comparación CAD vs objeto real y trazabilidad del lote.
- Separación de desechos por materiales, máquinas de recuperación compatibles, ensayos de degradación tras varios ciclos.
- Inventario de materia prima, consumibles, herramientas, repuestos y componentes críticos; decisión comprar vs fabricar vs reparar.

**Protocolo de fabricación:** especificación y material → simulación → proceso compatible → fabricación → acabado → inspección/ensayo → liberación o rechazo. La IA **no puede declarar que una pieza soportará una carga solo porque encaje geométricamente**.

---

## 6. Robot principal: forma óptima, tamaño y mecanismos

### 6.1. Preferencia de arquitectura

Un robot humanoide de tamaño adulto no parece la opción mínima para un reparador doméstico. Propusimos una **plataforma compacta de cuatro ruedas-patas, torso retráctil y dos brazos de manipulación**, con estabilizadores y herramientas externas. No está probado que supere en todos los casos a una base de ruedas omnidireccionales, orugas articuladas o dos piernas; debe compararse experimentalmente.

**Objetivos dimensionales exploratorios, no especificaciones de un producto existente:**

| Magnitud | Propuesta inicial | Estado |
|---|---:|---|
| Ancho plegado | 42–45 cm | aspiración |
| Largo plegado | 65–75 cm | aspiración |
| Alto plegado | 35–45 cm | aspiración |
| Referencia nominal de diseño | **45 × 70 × 40 cm** | por validar |
| Altura del cuerpo desplegado | 130–145 cm | por validar |
| Alcance vertical herramienta | 1,9–2,1 m | con cargas bajas, por validar |
| Peso total | 30–45 kg | muy exigente, por validar |
| Dos brazos | 7 grados de libertad por brazo | candidato |
| Alcance de cada brazo | 65–80 cm | cinemática pendiente |
| Carga útil por brazo | 2–4 kg bajo condiciones definidas | aspiración, no garantía |
| Tracción | 4 patas articuladas, ruedas en los extremos | candidato |

Es posible que varias de estas metas resulten físicamente **incompatibles entre sí**. Una combinación de cuatro patas potentes, batería, reductoras, dos brazos, sensores y torso retráctil podría exceder peso y volumen. **Priorizar capacidad y seguridad ante forzar unas medidas arbitrarias.** Determinar volumen de motores/actuadores, longitudes de barras, radio de giro, masas y pares antes de aprobar el chasis.

### 6.2. Modos de configuración

1. **Plegado/almacenamiento:** centro de gravedad bajo; brazos y piernas recogidos dentro de la anchura máxima, sin sobresalientes al cruzar puertas.
2. **Rodadura:** desplazamiento eficiente por suelo liso, control de movimiento y percepción de obstáculos.
3. **Escaleras/terreno:** cada rueda-pata puede convertirse en punto de apoyo y subir/bajar peldaños de forma secuenciada.
4. **Trabajo al suelo:** altura baja, brazo orientado lateral o frontalmente, instrumentos de visión y tacto cercanos.
5. **Trabajo a encimera:** patas estabilizadas y torso elevado; supervisión del momento de vuelco.
6. **Alcance alto:** extensión máxima con **límites inferiores de fuerza/carga**; preferir herramienta elevada o una plataforma alternativa si el equilibrio no lo permite.
7. **Mantenimiento:** articulaciones accesibles desde el exterior, postura bloqueada y conectores seguros para intervención del compañero o de la estación.

### 6.3. Manipulación fina y fuerza útil

- Brazos bimanuales para sujetar una cubierta mientras se quitan tornillos o manipular juntas y conectores con una segunda herramienta.
- Sensores de **fuerza/par en muñecas**, tacto en dedos, cámaras en muñecas, iluminación, IMU y visión externa.
- Herramientas intercambiables con identificación y calibración automática: pinzas delicadas y robustas, destornillador de par, llave, mini cámara, palpador, extractor, ventosa con **retención secundaria**, útiles para clips/conectores y guías de cableado.
- Enfoque en **control de fuerza**, no solo de posición: no romper plástico frágil, vidrio, contactos, roscas o cables.
- Al efectuar esfuerzos laterales, desplegar huella de apoyo y comparar el par aplicado con el margen de estabilidad dinámico.
- **No exigir brazos capaces de levantar 100 kg.** Transportador autónomo/elevador de perfil bajo para aparatos pesados. Minimiza tamaño, masa y coste del cuerpo principal.

### 6.4. Alternativas por comparar en CAD y banco

- Base omnidireccional baja + torso y estabilizadores: muy buena para interiores planos, peor escaleras.
- Cuadrúpedo ruedas-patas: movilidad híbrida potencialmente excelente, más complejidad/mantenimiento.
- Orugas articuladas: útiles para escombros y desniveles, riesgo de marcar suelos, maniobrabilidad fina desigual.
- Bipedo humanoide compacto: acceso a entornos humanos, pero coste energético, estabilidad y complejidad.
- Plataforma especializada + segundo robot ligero: posiblemente más robusta/compacta que un «todo en uno».

**Selección final por evidencia**: coste/Wh por tarea, tiempo de reparación, puertas, escaleras, manipulabilidad, fallos, mantenimiento, precio y seguridad. Referencias reales: [Unitree](https://www.unitree.com/), [Rainbow Robotics](https://www.rainbow-robotics.com/) y trabajos académicos de locomoción ruedas-patas. Estos productos no constituyen un prototipo ya validado de esta propuesta.

---

## 7. Navegación autónoma: rodear, retirar o superar obstáculos

### 7.1. Un planificador de alternativas físicas

La navegación ordinaria suele planear trayectorias para **evitar** obstáculos. Nuestro robot deberá considerar **cambios autorizados del entorno**. El proceso propuesto:

1. Reconocer obstáculos, estimar propiedades y su incertidumbre.
2. Comprobar si existe ruta alternativa (otra puerta/pasillo/acceso).
3. Comprobar si puede plegar el cuerpo y pasar por debajo o por un hueco estrecho.
4. Considerar mover o retirar el objeto, evaluando cables, líquidos, fragilidad, ocupantes, peso y suelo.
5. Considerar intervención remota por brazo extensible/cámara/minibot sin desplazar todo el cuerpo.
6. Evaluar sobrepasar por arriba **solo si hay apoyos con resistencia y fricción suficientemente verificadas**.
7. Considerar instalar una rampa/puente o pedir ayuda a otro robot.
8. Si no hay maniobra dentro de límites, solicitar ayuda humana y preservar estado seguro.

Esto corresponde a enfoques de **planificación integrada de tareas y movimientos (TAMP)**, percepción activa y navegación entre obstáculos móviles. Se usarán mapas 3D o de elevación, no solo mapas 2D de una aspiradora.

### 7.2. Ejemplo: la cama ocupa todo el paso

La IA puede pensar en escalarla, pero **la cama y especialmente su colchón no son una superficie portante validada para el robot**. La respuesta podría ser rodearla, moverla, extender una cámara, usar herramientas por encima o montar un puente temporal cuyo peso recaiga en apoyos firmes a ambos lados. Un puente de ancho/longitud suficiente podría ser voluminoso o pesado; el plan debe comparar su coste con otras opciones, no asumir que es viable.

### 7.3. Ejemplo: cae un objeto y bloquea el pasillo

Detenerse, inspeccionar si hay cables, filos, líquidos, vidrio, mascotas o carga inestable; apartarlo **de modo autorizado** a una zona segura, comprobar que no se empeora el entorno y, si procede, devolver el objeto a su lugar. No empujar ciegamente hacia escaleras o puertas.

### 7.4. Escaleras

- Detectar contrahuellas, huellas, anchuras, descansillos, peldaños abiertos, bordes, alfombras, inclinación y fricción.
- Planificar apoyos individuales de las ruedas-patas, bajar centro de masa y controlar transferencia de cargas.
- Sensores de contacto/IMU/fuerza y estimación de suelo, monitorización de deslizamiento en cada paso.
- Ensayos primero en escalera de laboratorio **con arnés de retención**, protección de caída y supervisión externa.
- Especial cuidado con escalera de caracol, peldaños estrechos, alfombras, personas y tránsito en sentido contrario.
- Si no está validada la escalera: transportar el robot con sistema externo o instalar una base por planta; nunca improvisar una subida peligrosa.

### 7.5. Rampas y puentes desplegables

La propuesta de que el robot **lleve o fabrique sus propias rampas** es útil para salvar huecos, umbrales y pequeños desniveles. No debe convertirse en único sistema para cualquier escalera.

**Ejemplo geométrico:** con una pendiente relativamente suave de 1:12, salvar **18 cm** de altura demanda **2,16 m de longitud horizontal**. Subir **2,5 m** de altura demanda **30 m** de desarrollo horizontal. Un robot puede estar diseñado para pendientes mayores, pero habrá compromisos en tracción, estabilidad, peso de rampa y espacio.

Diseñar módulos plegables de longitud acotada, con ensayos de flexión, apoyos, bloqueo, detección de contacto y límite de carga. No descargar peso sobre colchones, cristales o mobiliario sin validación estructural.

### 7.6. Herramientas auxiliares de movilidad

- Pequeña **plataforma robótica baja** que entre bajo objetos, los eleve ligeramente y los desplace sobre suelo.
- Pasarelas modulares, calzos, estabilizadores, cuñas y plataformas de trabajo autorizadas.
- Minibot o sonda flexible para huecos donde el robot principal no cabe.
- Segundo robot para transporte asistido, sujeción y rescate.

---

## 8. Reparación integral de electrodomésticos: casos de aceptación

### 8.1. Lavadora encastrada bajo la encimera

1. Entender fallo, manual, modelo y acceso; clasificar riesgos.
2. Aislar suministro de electricidad y agua mediante procedimiento verificado; medir estado seguro cuando proceda.
3. Inspeccionar espacio, recorrido de mangueras, enchufes, fijaciones y suelo.
4. Preparar plataforma elevadora/transporte de perfil bajo; confirmar masa, estabilidad y protección de suelo.
5. Extraer la lavadora sin arrastrar mangueras, pellizcar cables ni volcarla.
6. Desmontar paneles y conservar **foto/posición/orden/par** de tornillos, clips, conectores y juntas.
7. Medir/diagnosticar la pieza problemática; decidir entre recambio, fabricación local **si cumple tolerancias y propiedades**, o asistencia profesional.
8. Colocar repuesto; remontar y realizar ensayos de estanqueidad, ruido, vibración y funciones dentro de procedimiento seguro.
9. Reinsertar en el hueco, nivelar patas, comprobar ventilación/holguras y que cables/mangueras no estén aplastados.
10. Entregar informe y mediciones de antes y después.

El hito final NO es «cambiar un rodamiento» sino **dejar la lavadora accesible, reparada, montada, probada y físicamente en su sitio**.

### 8.2. Vitrocerámica o inducción

Examinar fijaciones y juntas desde el mueble inferior; aislar y verificar energía; aflojar elementos; retirar sellos de manera compatible; utilizar **ventosas y retención mecánica** para distribuir carga y no romper el vidrio; intervenir solo en módulos permitidos y seguros, volver a sellar, fijar y verificar asentamiento y aislamiento. **Conexiones eléctricas fijas y otras tareas reguladas deberán realizarse con profesionales habilitados**; no asumir competencia autónoma universal.

### 8.3. Nevera

Retirar contenidos sensibles según el trabajo, despejar accesos, emplear plataforma de carga que minimice inclinación y vuelco, extraer protegiendo el suelo, comprobar ventilación; revisar juntas, ventiladores o sensores accesibles cuando sea apropiado; reinstalar y verificar temperatura/puertas/ventilación. **Circuitos sellados de refrigerante quedan fuera del modo autónomo inicial**, salvo laboratorio y personal/equipos debidamente habilitados.

### 8.4. Biblioteca de otras tareas

Puertas y bisagras, cajones, estanterías, persianas, aspiradoras, herramientas, impresora 3D, muebles desmontables, grifos de baja complejidad en entorno controlado, pequeños electrodomésticos no peligrosos, elevadores, cámaras, ruedas y el propio segundo robot. La tarea de desmontaje debe registrar conectores y fijaciones **para poder reconstruir el estado original**.

---

## 9. Volver a una base de carga barata y fiable: inspiración Xiaomi S12

El **Xiaomi Robot Vacuum S12** usa información de navegación del entorno y **sensor de carga por infrarrojos** para alinear el aparato con su base; Xiaomi indica alcance efectivo aproximado de **4 metros** para ese sensor. Esto no significa que detecte directamente la estación desde cualquier parte de la casa: primero localiza la región mediante su mapa y odometría, luego corrige la aproximación próxima. Si la base cambia de sitio o hay obstáculos puede fallar. Ver [especificaciones Xiaomi S12](https://www.mi.com/es/product/xiaomi-robot-vacuum-s12/specs/) y [guía oficial de regreso](https://www.mi.com/global/support/faq/details/KA-124398/).

**Para nuestro robot, propuesta modular de bajo coste:**

1. **SLAM y mapa local**: sabe dónde está y dónde espera encontrar la estación.
2. **Navegación al área de aproximación**: planifica la ruta con obstáculos, puertas y condiciones energéticas.
3. **Marcador AprilTag** visible cerca del dock para estimar posición relativa; opcionalmente IR como respaldo.
4. **Guías mecánicas de acoplamiento** para absorber pequeños errores de pose; topes seguros.
5. **Contactos protegidos, BMS y supervisión de corriente/temperatura**: confirmar carga real antes de declarar éxito.
6. **Detección de dock movido**: búsqueda visual limitada, confirmación, actualización de ubicación; varias bases o base auxiliar por planta.
7. **Modo degradado offline**: el docking y la seguridad funcionan aunque la IA generalista no esté disponible.

Software existente a evaluar: [Nav2 Docking Server](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) y [AprilTag](https://github.com/AprilRobotics/apriltag). El coste marginal de balizas/impresiones puede ser bajo si el robot ya tiene cámaras, navegación y ordenador, **pero batería, contactos, mecánica y protección eléctrica no son gratis**.

---

## 10. La base de carga debe ser un tercer robot, estacionario

### Zonas funcionales

- **A: recarga/comunicaciones**: guiado, energía, BMS, protección, gestión de temperatura y sincronización de registros.
- **B: inspección y diagnóstico**: cámara, iluminación, prueba de sensores, consumo de motores, holgura, ruido, temperatura, calibración, limpieza de contactos y ópticas.
- **C: reparación**: soporte que inmoviliza al robot, manipulador independiente, herramientas de extracción y atornillado, almacén de módulos, calibración y pruebas posreparación.

### Secuencia de mantenimiento

Regreso al dock → confirmar que carga → recopilar telemetría → inspeccionar desgaste → limpiar → ejecutar diagnósticos selectivos → identificar fallos persistentes → inmovilizar en zona de reparación → cambiar módulo **si la operación ha sido validada** → calibrar → probar en condiciones seguras → autorizar próxima salida o bloquearla.

**Ejemplo:** una pata consume más corriente que antes al producir la misma fuerza. La estación compara curvas históricas para distinguir posible rozamiento externo de fallo interno; solo tras una prueba de diagnóstico independiente inmoviliza y sustituye módulo, comprobando luego el par/posición/temperatura.

**Fallo lejos de la estación:** el segundo robot puede remolcar o asistir. **Fallos simultáneos:** acceso manual, subsistemas independientes y mecanismos de recuperación. No diseñar un sistema que dependa absolutamente de un único Wi-Fi, suministro o controlador.

---

## 11. Dos robots para reparación recíproca y continuidad

**Robot A:** fabricación, reparaciones domésticas y uso general. **Robot B:** inspección, soporte, rescate y mantenimiento. Ambos podrían intercambiar roles y usar la misma biblioteca de herramientas, pero conviene diversificar determinados fallos comunes.

**Reglas mecánicas:**

- Módulos sustituibles de ruedas, patas, articulaciones, motores/reductoras, brazos, cámaras, baterías, cableado y placas.
- Acceso exterior a tornillos y conectores incluso cuando el robot receptor esté **apagado o inmovilizado**.
- Conectores codificados mecánica y eléctricamente, sin poder intercambiar polaridad/tensión por error.
- Posiciones de mantenimiento estables y articulaciones externamente liberables cuando sea seguro.
- Identificación de compatibilidad, versiones, firma de repuestos y par de fijaciones conocido.
- El otro robot o el brazo del dock pueden reemplazar módulos sin necesitar que el receptor mueva sus brazos.
- Registro de piezas montadas, número de ciclos, desgaste, calibración y autorización de salida.
- Sistema de rescate para un robot inmóvil fuera de la base; acceso humano cuando no haya rescate automático.

**Prueba fundamental:** inducir avería inocua y controlada de módulo, dejar A apagado, hacer que B extraiga/sustituya módulo y verifique; repetir B apagado y A reparando. Después ensayar fallos comunes de software, fuente, batería y estación.

Referencia científica (no robot doméstico de mantenimiento total): [Columbia Engineering: Robot Metabolism, julio de 2025](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots), sobre integración y reutilización modular de partes robóticas.

---

## 12. IA local y arquitectura de software: 16–24 GB como objetivo

**No requerimos que un único modelo tenga todos los conocimientos científicos en sus pesos.** La IA generalista debe saber planificar, consultar documentación, delegar, verificar y detenerse; los cálculos exigentes los resolverán instrumentos, simuladores y controladores especializados.

### Descomposición de funciones

1. **LLM local**: interpretar necesidades, leer manuales, planificar y explicar; cuantización/servicio de inferencia compatible con 16 GB cuando sea posible.
2. **Percepción y estimación del estado**: cámaras, LiDAR/3D, SLAM, objetos, humanos, superficies, fuerza y contacto.
3. **Políticas de manipulación VLA**: habilidades entrenadas/demostradas de alcance, agarre, cambio de herramienta, manipulación, con supervisión.
4. **Planificación de tareas y movimiento**: secuencias, colisiones, cinemática bimanual, obstáculos movibles, estabilidad y punto de apoyo.
5. **Herramientas de ingeniería**: FreeCAD, CadQuery, KiCad/SPICE, simulación multibody/FEA y materiales.
6. **Memoria local y RAG**: manuales, piezas, recetas, histórico de operaciones, fallos, marcas de verificación y versiones.
7. **Controladores críticos**: microcontroladores o lazos de tiempo real; límites de par/velocidad, sensores de seguridad, E-stop, protecciones de hardware.

### Modelos y precedente verificable

- [SmolVLA 450M](https://huggingface.co/blog/smolvla) es un ejemplo de modelo visión-lenguaje-acción compacto entrenable/ejecutable en equipamiento asequible para **tareas delimitadas**.
- [LeRobot](https://github.com/huggingface/lerobot) ofrece herramientas abiertas para integración de robots, teleoperación, datos y entrenamiento.
- [openpi](https://github.com/Physical-Intelligence/openpi) documenta configuraciones de inferencia con **más de 8 GB de GPU** y necesidades de ajuste fino muy superiores. Que el modelo pueda entrar en memoria no equivale a que domine reparaciones generalistas.
- Un LLM local puede orquestar múltiples herramientas; evaluar VRAM **pico**, KV cache, visión concurrente, latencia de percepción/control, energía y fiabilidad.

### Diseño para desconexión y privacidad

- La GPU central podría residir en casa (estación/servidor), mientras el robot lleva cómputo básico y control de seguridad local.
- Red local cifrada y autenticada; no se depende de Internet para seguridad, navegación básica, postura y recarga.
- No guardar vídeos de dormitorios/salas más tiempo del necesario; telemetría y modelos compartidos bajo permisos explícitos.
- Modelos y herramientas versionados con rollback; protección contra instrucciones maliciosas en manuales o documentos externos (*prompt injection*).
- No permitir que el LLM desactive límites de fuerza, enclavamientos o señales de parada.
- Priorizar operación secuencial de modelos o descargas parciales para no desbordar una GPU de 16 GB.

---

## 13. Herramientas y plataformas de código abierto (investigación complementaria)

Los proyectos existentes reducen la necesidad de inventar toda la infraestructura. **Evaluar mantenimiento, licencia, versión de ROS 2, capacidad real y requisitos GPU antes de adoptarlos**; esta tabla no es una afirmación de integración ya realizada.

| Área | Proyecto | Uso potencial |
|---|---|---|
| Middleware robótico | [ROS 2](https://www.ros.org/) | comunicaciones y componentes |
| Lazos y dispositivos | [ros2_control](https://control.ros.org/) | interfaz de actuadores y ciclo de control |
| Navegación y carga | [Nav2](https://docs.nav2.org/) | planificación, recuperación, docking |
| Tareas jerárquicas | [Nav2 Behavior Trees](https://docs.nav2.org/rolling/getting_started/navigation_concepts/behavior_trees/) | acciones secuenciales y condiciones |
| Docking autónomo | [opennav_docking](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) | aproximación y confirmación de carga |
| Manipulación | [MoveIt 2](https://moveit.picknik.ai/main/) | IK, colisiones y planes de brazo |
| Tareas multi-etapa | [MoveIt Task Constructor](https://moveit.picknik.ai/main/doc/concepts/moveit_task_constructor/moveit_task_constructor.html) | agarre, desmontaje, colocación |
| Física multibody | [Drake](https://github.com/RobotLocomotion/drake) | restricciones, dinámica, control |
| Mapa del terreno | [ANYbotics grid_map](https://github.com/ANYbotics/grid_map) | elevación, superficie y transitabilidad |
| Pose visual del dock | [AprilTag](https://github.com/AprilRobotics/apriltag) | marcadores y estimación de posición |
| Hardware robótico económico | [SO-101 en LeRobot](https://github.com/huggingface/lerobot/blob/main/docs/source/so101.mdx) | brazo imprimible, BOM, montaje |
| Entrenamiento de robot | [LeRobot](https://github.com/huggingface/lerobot) | demostraciones, políticas y datos |
| Modelo robótico compacto | [SmolVLA](https://huggingface.co/blog/smolvla) | visión y acción para tareas acotadas |
| VLA de investigación | [openpi](https://github.com/Physical-Intelligence/openpi) | comparar modelos y requisitos |
| Sensores de tacto | [Meta Digit Plexus](https://github.com/facebookresearch/digit-plexus) | integración modular de tacto |
| Tacto reemplazable | [AnySkin](https://any-skin.github.io/) | estimar contacto y agarre |
| CAD paramétrico | [FreeCAD](https://github.com/FreeCAD/FreeCAD) | modelo editable, planos y Python |
| CAD programático | [CadQuery](https://cadquery.readthedocs.io/) | piezas paramétricas a partir de scripts |
| Escaneo económico | [OpenScan](https://github.com/OpenScan-org) | fotogrametría y proyectos de hardware |
| Electrónica | [KiCad](https://www.kicad.org/) | esquemas y PCB |
| Simulación EM | [openEMS](https://docs.openems.de/en/stable/intro.html) | electromagnetismo avanzado cuando corresponda |
| Firmware/ejecutables | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | análisis y pseudocódigo |
| Microchips | [Degate](https://github.com/DegateCommunity/Degate) | análisis semiautomático de imágenes de IC |
| Señales eléctricas | [sigrok/PulseView](https://sigrok.org/wiki/PulseView) | protocolos y capturas |

**Punto nuevo importante:** en robótica hay una distinción entre aprender a manipular objetos conocidos y ejecutar una tarea compleja en un entorno nunca visto. Los modelos VLA son prometedores, pero la fiabilidad de un desmontaje delicado requerirá probablemente **teleoperación de enseñanza, pruebas, sensores táctiles, reglas duras y simulación**. Un modelo de 450 millones de parámetros y uno mucho mayor no deben compararse solo por «tokens por segundo».

---

## 14. Aspectos subestimados: investigación nueva de alto retorno

### 14.1. Metrología y trazabilidad

Cada componente debería poder asociarse a una cadena: **fuente/sensor → lectura calibrada → tolerancia → CAD → proceso → lote/material → pieza real → medición de aceptación**. El error de una cámara o escáner no es el error final de fabricación. El sistema deberá distinguir precisión, repetibilidad y veracidad de medición.

### 14.2. Tacto y control de fuerza como prioridad

Un brazo con visión perfecta puede romper un conector o el borde de una vitrocerámica si solo conoce posición. Priorizar medición de **fuerza, par, deslizamiento, material blando, fricción** y pruebas con útiles desechables de bajo riesgo. Los sensores táctiles como AnySkin y plataformas como Digit Plexus son vías abiertas que merecen prototipo.

### 14.3. Diseño para desmontaje robótico

Todos los objetos creados por nuestra microfábrica deberían tener, siempre que resulte práctico, **tornillos accesibles desde posiciones alcanzables, conectores únicos o codificados, carcasas reparables, instrucciones incorporadas, referencias visuales y módulos etiquetados**. Es más fácil que dos robots se reparen mutuamente si nacen diseñados para la operación, que si intentan manipular dispositivos irreparables de terceros.

### 14.4. Razonamiento y ensayo de fuerzas sobre muebles

Necesitamos saber **cuándo NO empujar, levantar o pisar**. El robot deberá estimar masas y apoyos, buscar documentación, aplicar fuerzas de prueba solo cuando el entorno sea seguro y calcular márgenes. Un colchón, una encimera de vidrio o una balda aparentemente rígida no son apoyo aceptable por defecto.

### 14.5. Redundancia y recuperación

Dos robots no resuelven el problema si ambos usan el mismo firmware con error, dependen del mismo controlador o pierden la misma fuente. Redundar selectivamente **mecanismos de diagnóstico, parada y recuperación**, preservar herramientas manuales y capacidad de rescate. El propio taller necesita diseño para reparación.

### 14.6. Energía, disipación y condiciones ambientales

Medir energía total de fabricar una pieza o efectuar una reparación, incluyendo GPUs, motores, ventilación, secado de material, carga, desperdicios y transporte. Añadir protección de incendio, polvo, vapores, humedad y ruido; si el objetivo es sostenibilidad, comparar contra comprar una pieza fabricada industrialmente.

### 14.7. Ciberseguridad y privacidad doméstica

La visión robótica puede captar dormitorios, documentos y personas. Diseño **local por defecto**, retención limitada, permisos sobre zonas de la casa, actualizaciones firmadas, control de acceso y registros de decisiones. El texto de un manual obtenido por Internet nunca podrá autorizar por sí mismo operaciones físicas peligrosas o modificar las políticas de seguridad.

### 14.8. Leyes físicas y economía real

Una pieza que se puede imprimir no es necesariamente más barata, duradera o ecológica. Decidir **fabricar, reparar, reutilizar, comprar repuesto o pedir servicio profesional** mediante mediciones, valor total, impacto, vida útil y riesgos. Los procesos caros o peligrosos deben quedarse fuera de casa cuando tenga sentido.

### 14.9. Evaluación del sistema a largo plazo

La diferencia entre un vídeo espectacular y un robot doméstico útil es la **fiabilidad bajo miles de acciones, ambientes nuevos, suciedad, desgaste y fallo de sensores**. Registrar intentos, errores, rescates, caídas, daños y tiempos de mantenimiento. No eliminar pruebas fallidas de las métricas.

---

## 15. Modelo de datos y contratos de confianza

El sistema debería guardar un **expediente verificable por objeto** con estos grupos de campos (estructura conceptual, no esquema API definitivo):

- **Identidad:** nombre interno, imágenes, modelo/marca si consta, geometría base, huellas.
- **Mediciones:** sensor, fecha, unidad, calibración, valor, incertidumbre y archivo bruto.
- **Hipótesis:** composición/materiales probables, geometrías ocultas, funciones, nivel de confianza y alternativas.
- **CAD y fabricación:** archivo paramétrico, material, tolerancias, orientación, proceso, herramientas, temperatura, energía, lote.
- **Conexiones:** esquema, puertos, señales permitidas, interfaces y pruebas eléctricas autorizadas.
- **Desmontaje:** secuencia, fuerzas/par, fijaciones, fotos previas, clips y sellos, condiciones de reversión.
- **Diagnóstico:** síntomas observados, hipótesis causal, pruebas discriminantes, resultado de cada prueba.
- **Reparación:** módulo antiguo/nuevo, procedencia, intervención, incidencias, pruebas de aceptación y resultado.
- **Riesgos:** peligros, clase de intervención, permisos, límites de energía/par/fuerza, requisitos de profesional.
- **Proveniencia:** modelo IA y versión, herramienta, código, autor/aprobador, registros de sensores.

**Estados de evidencia:** NO_MEDIDO, HIPÓTESIS, MEDIDO, VALIDADO_EN_SIMULACIÓN, VALIDADO_EN_ENSAYO, INVALIDADO. Evitar que una hipótesis de CAD termine convertida silenciosamente en «tolerancia garantizada» durante la fabricación.

---

## 16. Seguridad, salud, calidad y restricciones legales

El proyecto debe implementar desde el primer prototipo:

- **Parada de emergencia física** y limitaciones independientes del LLM, watchdog, estado seguro tras pérdida de energía/comunicación.
- Interbloqueos para cargar baterías, ejecutar herramientas, introducir brazos en huecos o energizar instalaciones.
- Límites estrictos de velocidad y par según entorno, colisión, proximidad humana y estado del objeto.
- Supervisión de vuelco, contacto con escaleras, deslizamiento, sobretemperatura y zonas de atrapamiento.
- Ensayos con **arnés de seguridad** en escaleras antes de cualquier demostración doméstica.
- Aislamiento verificado de aparatos antes de desmontar. Riesgos residuales de condensadores, presión, refrigerante, calor y partes móviles.
- Exclusión de tareas de red eléctrica fija, gas, circuito frigorífico sellado y otras operaciones reguladas salvo equipos y profesionales autorizados.
- Los equipos de rayos X y similares no se consideran componentes DIY domésticos; normativa y seguridad radiológica son una barrera legítima.
- Recuperación humana y no destructiva cuando los sistemas automáticos fallen.
- Registros de incidentes, análisis sistemático de riesgos y manual de parada y mantenimiento.

**Referencias:**
- [ISO 13482:2014, robots de asistencia personal](https://www.iso.org/es/contents/data/standard/05/38/53820.html). Figura publicada en 2026 y se encuentra en proceso de revisión.
- [ISO 10218-1:2025, robots industriales](https://www.iso.org/es/contents/data/standard/07/39/73933.html). **No** sustituye por sí sola la normativa de servicio doméstico.
- [Reglamento (UE) 2023/1230 sobre máquinas](https://eur-lex.europa.eu/eli/reg/2023/1230/spa), con aplicación general desde **20/01/2027**.
- [Directiva (UE) 2024/1799 sobre promoción de la reparación](https://eur-lex.europa.eu/eli/dir/2024/1799/2026-07-31); revisar transposición y ámbito concreto al construir/comercializar.

**La publicación de planos abiertos no exime a fabricantes o constructores de obligaciones legales.** Cada fase debería contar con revisión específica si se utiliza fuera de entornos de ensayo.

---

## 17. Hoja de ruta de implementación (etapas con puertas de aceptación)

### F0. Diseño y pruebas de escritorio — primero, sin comprar un robot caro

- [ ] Crear una **lista priorizada de 30–50 tareas** domésticas, riesgos, beneficios, herramientas y entornos.
- [ ] Identificar 10 tareas de primer alto retorno: p. ej., desmontar una carcasa inocua, cambiar un tornillo, abrir un cajón, cambiar una pieza impresa, detectar un obstáculo, acoplarse, etc.
- [ ] Dibujar diagrama mecánico/software/seguridad, documentar protocolos y contratos de datos.
- [ ] Simular brazo y chasis con CAD/Drake; comprobar volumen interno real, pares, estabilidad y centro de gravedad.
- [ ] Comparar ruedas-patas, omnidireccional y orugas con los mismos escenarios y criterios.
- [ ] Definir plan de ensayos reproducibles, calibración y FMEA.

**Cierre:** arquitectura revisada, BOM preliminar con supuestos, simulaciones y lista de riesgos sin tareas físicas de alto peligro.

### F1. Primer «descompilador físico» útil: escanear y fabricar una pieza

- [ ] Capturar **5 piezas mecánicas pequeñas no críticas**, con patrones de escala/calibración.
- [ ] Obtener malla y **CAD paramétrico real**, cotas, incertidumbres y enlace a medición original.
- [ ] Fabricar la réplica, medir y comprobar que encaja.
- [ ] Iterar automáticamente una modificación de geometría tras un fallo de ajuste.
- [ ] Utilizar una IA local que coordine escaneo, FreeCAD/CadQuery e informe, con supervisión.

**Cierre:** pieza reconstruida, fabricada, medida y corregida con resultados reproducibles (no solo foto).

### F2. Primer sistema de manipulación + docking autónomo

- [ ] Brazos de prototipo accesibles como **SO-101**, cámara, sensores sencillos y soporte fijo.
- [ ] Plataforma móvil segura de primer ensayo, mapa y retorno a dock con AprilTag.
- [ ] Validar contactos y corriente, temperatura y desconexión segura.
- [ ] **100 acoplamientos** bajo condiciones documentadas, con fallos contabilizados; ampliar gradualmente a base movida y obstáculos.
- [ ] Cambio automático de herramienta, con calibración y validación por visión/tacto.

**Cierre:** navegación → docking → confirmación de carga repetible y cambio de herramienta seguro.

### F3. Estación de inspección y cambio automático de un módulo

- [ ] Diseñar pieza o articulación de baja energía con **fallo inyectable** y tornillería accesible.
- [ ] Base inmoviliza, inspecciona, diagnostica y sustituye módulo mediante brazo externo.
- [ ] Ejecutar autoensayo y comparar antes/después.
- [ ] Fallo de Wi-Fi/GPU durante el proceso: sistema conserva seguridad y posibilidad de recuperación.

**Cierre:** una reparación real de un módulo de ensayo sin intervención manual, con expediente completo.

### F4. Dos robots: reparar al que no puede ayudarse

- [ ] Dos manipuladores/plataformas de módulos compatibles.
- [ ] Robot A sustituye un módulo de B **apagado**; ejecutar prueba funcional.
- [ ] Repetir B reparando A.
- [ ] Añadir escenarios de rescate desde otra habitación y estación inaccesible.
- [ ] Documentar un modo de fallo común y su mitigación.

**Cierre:** reparación recíproca con roles intercambiables, incluidos receptores inmovilizados.

### F5. Locomoción para vivienda real

- [ ] Construir prototipo móvil seleccionado por ensayos previos.
- [ ] Validar paso por puertas y posturas bajo muebles.
- [ ] Esquivar, apartar y luego devolver un obstáculo sin dañar nada.
- [ ] Superar un escalón y una escalera de ensayo **con protección de caída**.
- [ ] Demostrar rechazo explícito de una superficie portante incierta (colchón).
- [ ] Desplegar un puente sobre soportes medidos y cruzar con margen.
- [ ] Cooperación con carretilla elevadora baja para objeto pesado.

**Cierre:** movilidad robusta en escenarios declarados, con abortos seguros, fallos registrados y sin prometer universalidad.

### F6. Reparación integral de aparato benigno

- [ ] Manual/diseño conocido de aparato seguro y desmontable.
- [ ] Diagnóstico verificable de un fallo controlado.
- [ ] Desmontaje, cambio, reensamblaje, pruebas y colocación original.
- [ ] Operación de extracción/recolocación en una **maqueta de electrodoméstico** sobre plataforma de carga.
- [ ] Después de ensayos de seguridad, ampliar a aparatos reales permitidos y con supervisión.

**Cierre:** ciclo completo documentado desde el acceso al aparato hasta su devolución funcional.

### F7. Materiales circulares y fabricación ampliada

- [ ] Seleccionar pocas familias seguras y fácilmente separables.
- [ ] Ensayar reciclado en varios ciclos y propiedades resultantes.
- [ ] Evaluar celulosa/lignina/PHA como posibles líneas de mejora; estudiar proveedores, procesos y sostenibilidad real.
- [ ] Diseñar piezas para desensamblaje por robots y archivo CAD/BOM abierto.
- [ ] Incorporar metrología, ensayos y costes de ciclo de vida.

**Cierre:** materiales reprocesados con trazabilidad y propiedades medidas para usos concretos.

### F8. Integración abierta y verificada

- [ ] IA local, fabricación, percepción, robot A/B, base-taller y gemelos digitales integrados.
- [ ] Demostración **sin cortes ni edición de fallos** de reparación segura de principio a fin.
- [ ] Revisión de riesgos/conformidad, privacidad y consumibles.
- [ ] Repositorio abierto de hardware, software, documentación y experimentos; publicación de métricas incluso cuando no se alcanza el objetivo.

---

## 18. Métricas e indicadores que impedirán autoengañarnos

| Indicador | Cómo medirlo |
|---|---|
| Precisión de escaneo | diferencia vs piezas patrón calibradas, por tamaño/material |
| Calidad del CAD | editabilidad paramétrica, restricciones y fidelidad, no solo malla |
| Equivalencia del repuesto | cotas, encaje y ensayos mecánicos pertinentes |
| Manipulación | tasa de éxito, daño al objeto, fuerzas máximas, tiempo y recuperación |
| Docking | 100+ intentos, éxito/tiempo, corriente confirmada, fallo y repetición |
| Movilidad | caída, deslizamiento, abortos, tiempo, energía, rescates y daños |
| Reparación integral | desmontar + cambiar + probar + montar + recolocar |
| Reparación mutua | éxito A→B y B→A, receptor apagado, pruebas posteriores |
| Fallos comunes | capacidad de parar, recuperación y rescate sin LLM/conexión |
| Uso offline | funciones disponibles sin Internet y seguridad ante pérdida de red |
| IA local | VRAM pico, latencia end-to-end, fallos y replanificaciones |
| Economía | coste BOM, energía Wh/tarea, consumibles, mantenimiento y repuestos |
| Circularidad | pureza de separación, calidad tras N ciclos, huella y vida útil |
| Seguridad | respuesta E-stop, control fuerzas, distancia personas, auditoría |

**Banco de escenarios**: pasillo libre; puerta estrecha; silla caída; objeto conectado a cable; suelo mojado; gato/persona cerca; cama bloqueando el único camino; hueco bajo mueble; escalón; escalera con descansillo; tramo de caracol; rampa modular; lavadora encastrada simulada; vidrio frágil de placa; nevera pesada de ensayo; dock movido; batería baja; sensores sucios; cámara desconectada; un brazo averiado; ambos robots averiados; estación apagada; fallo de fabricación de una pieza; modelo de IA que propone una acción insegura.

**Criterio universal de aceptación:** repetir ensayos con un entorno distinto al entrenado y **contabilizar todos los intentos y abortos**. Una demo que solo muestra aciertos no valida un producto generalista.

---

## 19. Riesgos principales y diseño para no quedar bloqueados

| Riesgo | Respuesta de diseño |
|---|---|
| No cabe todo en el chasis | CAD y comparación de configuraciones; aumentar tamaño o distribuir funciones |
| Baja estabilidad al empujar/tirar | apoyo extendido, sensor de par, planificador de momento de vuelco |
| Escalera peligrosa | pruebas con retención, límites de geometría, alternativa de transporte |
| Pieza nueva de material insuficiente | ensayos, biblioteca de propiedades, rechazo de uso crítico |
| Desconocimiento de cable/conector | escaneo, manual, desconexión segura, abortar |
| Error de la IA | verificador independiente, confirmación y controles de seguridad |
| Robo/filtración de vídeo doméstico | almacenamiento local y control de acceso |
| Dos robots averiados | estación separada, redundancia selectiva y acceso manual |
| Fallo del ordenador principal | control embebido y estado seguro |
| Propiedades internas no observables | informar incertidumbre y pedir laboratorio/desmontaje |
| Reciclaje caro o perjudicial | análisis ciclo de vida y opción de comprar repuesto |
| Dependencia de un fabricante | interfaces abiertas, documentación, módulos estándares |
| Coste de robot demasiado alto | hitos pequeños de mesa, escalado solo tras resultados |
| Proceso normativamente restringido | remitir a profesional/equipo certificado |

---

## 20. Coste, plazos y viabilidad: distinguir evidencia de pronóstico

**Hoy existen por separado:** escáneres 3D económicos, CAD abierto, impresión, brazos asequibles, robots con escaleras, SLAM, docking, análisis de software y circuitos, modelos de IA pequeños y laboratorios de materiales.

**La integración sigue siendo investigación:** reparación generalista fiable, identificación causal de averías desconocidas, manipulación bimanual fina, escaleras con carga, reparación recíproca de fallos variados, materiales locales útiles y verificación automatizada segura.

**No demostrado y muy alejado:** un dispositivo que haga ingeniería inversa no destructiva exacta de cualquier objeto o chip; una impresora casera que fabrique todos los materiales/electrónica; autorreplicación total; eliminar toda dependencia externa.

**Horizontes conversados, altamente especulativos:** más conversión escaneo→CAD durante los próximos años; sistemas domésticos multimodales más completos posiblemente en la década de 2030; autonomía generalista sin supervisión en reparaciones complejas **sin fecha creíble**. No son compromisos ni justificación para gastar dinero hoy.

**BOM antes de comprar:** separar coste de cámaras/escáner; electrónica de control y sensores; brazos/útiles; chasis/actuadores/batería; estación-taller; carro elevador; impresión/metrología; ventilación; ensayos y seguridad; repuestos y consumibles. Comparar primero prototipos de mesa en lugar de adquirir un humanoide completo.

---

## 21. Fuentes primarias y recursos revisados

**Revisados para esta especificación el 13/10/2026.** Los proyectos y las normas evolucionan: volver a comprobar versiones, licencias, disponibilidad y límites de seguridad cuando comience cada fase.

### Navegación, robótica y control

1. [ROS 2](https://www.ros.org/) — ecosistema de componentes robóticos.
2. [ros2_control](https://control.ros.org/) — interfaz y ciclo de control.
3. [Nav2 Docking Server](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) — docking configurable.
4. [Nav2 Behavior Trees](https://docs.nav2.org/rolling/getting_started/navigation_concepts/behavior_trees/) — tareas secuenciales/recuperación.
5. [MoveIt Task Constructor](https://moveit.picknik.ai/main/doc/concepts/moveit_task_constructor/moveit_task_constructor.html) — descomposición de tareas de manipulación.
6. [Drake](https://github.com/RobotLocomotion/drake) — dinámica, optimización, IK.
7. [ANYbotics grid_map](https://github.com/ANYbotics/grid_map) — mapa de elevación y características de terreno.
8. [AprilTag](https://github.com/AprilRobotics/apriltag) — localización relativa mediante marcadores.
9. [Especificaciones oficiales Xiaomi Robot Vacuum S12](https://www.mi.com/es/product/xiaomi-robot-vacuum-s12/specs/) — sensórica y alineación IR.
10. [Guía oficial Xiaomi: retorno a la base](https://www.mi.com/global/support/faq/details/KA-124398/) — limitaciones prácticas.

### IA y robótica abierta

11. [LeRobot](https://github.com/huggingface/lerobot) — entrenamiento e integración.
12. [SO-101](https://github.com/huggingface/lerobot/blob/main/docs/source/so101.mdx) — brazo y documentación de montaje.
13. [SmolVLA 450M](https://huggingface.co/blog/smolvla) — VLA compacto.
14. [openpi](https://github.com/Physical-Intelligence/openpi) — referencia de modelos de acción y recursos GPU.
15. [Meta Digit Plexus](https://github.com/facebookresearch/digit-plexus) — plataforma modular de sensores táctiles.
16. [AnySkin](https://any-skin.github.io/) — tacto intercambiable.
17. [Robot Metabolism, Columbia Engineering, 2025](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots) — modularidad y adaptación física.

### Ingeniería inversa, CAD, electrónica y materiales

18. [OpenScan](https://github.com/OpenScan-org) — escaneado comunitario.
19. [OpenScan Mini: guía de hardware](https://github.com/OpenScan-org/OpenScan-Doc/blob/main/docs/hardware/OpenScanMini.md) — componentes de escáner económico.
20. [FreeCAD](https://github.com/FreeCAD/FreeCAD) — CAD paramétrico.
21. [CadQuery](https://cadquery.readthedocs.io/) — CAD por Python.
22. [KiCad](https://www.kicad.org/) — esquemas y PCB.
23. [openEMS](https://docs.openems.de/en/stable/intro.html) — simulación electromagnética.
24. [Ghidra](https://github.com/NationalSecurityAgency/ghidra) — análisis de código máquina.
25. [Degate](https://github.com/DegateCommunity/Degate) — análisis de imágenes de VLSI.
26. [PulseView / sigrok](https://sigrok.org/wiki/PulseView) — análisis de señales digitales.
27. [Claude's C Compiler](https://github.com/anthropics/claudes-c-compiler) — estudio de caso de agentes de programación.
28. [3dsrecomp](https://github.com/fearkov/3dsrecomp) / [Zakuro](https://github.com/fearkov/zakuro) — recompilación/emulación de arquitectura particular.
29. [Comisión Europea: biobasados, biodegradables y compostables](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en) — definiciones y criterios ambientales.
30. [Revisión de PHA a partir de residuos, 2025](https://www.sciencedirect.com/science/article/pii/S0141813025009079) — posibilidades y restricciones de biopolímeros.

### Normativa y derecho a reparar

31. [ISO 13482:2014](https://www.iso.org/es/contents/data/standard/05/38/53820.html) — robots de asistencia personal, versión bajo revisión.
32. [ISO 10218-1:2025](https://www.iso.org/es/contents/data/standard/07/39/73933.html) — robots industriales, distinto ámbito.
33. [Reglamento (UE) 2023/1230](https://eur-lex.europa.eu/eli/reg/2023/1230/spa) — marco de maquinaria.
34. [Directiva (UE) 2024/1799](https://eur-lex.europa.eu/eli/dir/2024/1799/2026-07-31) — promoción de la reparación.

**Precaución respecto a las fuentes:** que una publicación demuestre una tarea específica, una velocidad o un sensor no permite extrapolarla automáticamente a un robot capaz de repararlo todo. Especialmente las medidas **45×70×40 cm**, **30–45 kg**, **16–24 GB** y el horizonte «década de 2030» pertenecen al planteamiento del proyecto; no son características demostradas de un producto existente.

---

## 22. Estándares abiertos, publicación y licencias

- Priorizar **documentación reproducible**, CAD paramétrico, archivos de circuitos, BOM, calibraciones, registros de ensayos y pruebas automatizadas.
- Analizar licencias compatibles para software (**Apache-2.0, GPL** según contexto), hardware (**CERN-OHL**) y documentación (**Creative Commons**), **sin asumir que este documento otorga automáticamente una licencia formal**.
- Separar materiales propios de componentes o software ajeno, evitar publicar piezas protegidas por propiedad intelectual sin autorización.
- Definir contratos de interoperabilidad entre modelos, herramientas, sensores y robots; el proyecto no debe depender de una única empresa.
- Política de privacidad local, cifrado, firma de software y plan de mantenimiento de dependencias.
- Publicar también experimentos fallidos, incertidumbres, perfiles de material e incidentes técnicos.
- Diseñar como proyecto abierto posible de construir por etapas y con piezas adquiribles comercialmente cuando proceda.

---

## 23. Preguntas de investigación pendientes, con prioridad

1. **¿Qué dimensiones/peso son mecánicamente mínimos?** ¿Cabrá la versión bimanual ruedas-patas realmente en 45×70×40 cm?
2. ¿Es mejor ruedas-patas o **robot omnidireccional + vehículo de escaleras** para viviendas comunes?
3. ¿Cómo medir de forma fiable resistencia y fricción de una cama, una rampa o una tabla **antes de cruzarla**?
4. ¿Cómo recuperar tolerancias y parámetros CAD sin inventarlos a partir de una malla ruidosa?
5. ¿Cuál es la mezcla adecuada de modelo generalista, VLA, control clásico, tacto y simulación con **16 GB reales**?
6. ¿Qué diez o veinte herramientas cubren la mayoría de reparaciones benignas en una casa?
7. ¿Cómo diseñar una operación de desmontaje general cuando no hay manual, sin dañar piezas ocultas?
8. ¿Cuándo es óptimo fabricar una pieza, comprarla o pedir un servicio profesional?
9. ¿Qué procesos de reciclaje/materiales realmente pueden mantenerse a escala doméstica con emisiones/costes aceptables?
10. ¿Cómo reparar a ambos robots si fallan simultáneamente, o si la estación queda sin energía?
11. ¿Qué tareas pueden certificarse para plena autonomía sin vigilancia? ¿Cuáles nunca deberían confiarse a un robot doméstico generalista?
12. ¿Qué significa «equivalencia» de un objeto fabricado: forma, carga, seguridad, aislamiento, fatiga, vida útil, consumo?
13. ¿Cómo evitar dependencia de proveedores en motores, baterías, sensores y semiconductores que la microfábrica no pueda construir?
14. ¿Cómo probar que el sistema funciona en **otra vivienda** diferente de donde se ha entrenado?

---

## 24. Próximo paso de máximo retorno cuando se decida empezar

**NO construir inmediatamente un humanoide completo.** Demostrar una cadena autosuficiente, económica y verificable:

1. Tomar una pequeña pieza mecánica sin riesgo.
2. Escanearla con cámara/escáner calibrado.
3. Generar CAD **paramétrico editable** con una IA local que utilice herramientas CAD reales.
4. Imprimirla o fabricarla, comprobar medidas y corregir el diseño.
5. Utilizar un brazo sencillo y una cámara táctil/visual para sustituirla en un módulo de ensayo de baja energía.
6. Utilizar un robot móvil sencillo que **vuelva a un dock con AprilTag**, valide carga y ejecute autodiagnóstico.
7. Introducir un fallo conocido y demostrar que un segundo brazo o la estación puede reparar el módulo.
8. Publicar el expediente completo: costes, errores, tiempo, energía, tasas de éxito, componentes y código.

Este prototipo compacto contiene **todos los principios de la fábrica autónoma** sin exigir resolver desde el principio locomoción en escaleras, reparaciones de alto riesgo, materiales experimentales o una cadena industrial de chips.

> **Síntesis final:** una IA local que sabe usar herramientas de ingeniería, dos robots compactos que pueden asistirse y repararse, una base-taller de carga/diagnóstico, un descompilador digital y físico, y una microfábrica multimaterial cada vez más circular. La universalidad no se proclama: **se alcanza por iteraciones medibles, verificación y diseño seguro.**
