# 07 — Chasis propio: herramientas, ingeniería y ejecución

**25 de octubre de 2026 · Plan V3, ampliado tras el encargo de base nueva y robot abierto; CAD inicial ejecutado.** Alcance: Xiaomi Robot Vacuum X20 Pro D102GL y su estación original. Este plan sustituye la prioridad anterior de reparar primero la carcasa existente. El objetivo actual es **recuperar los conjuntos aprovechables y diseñar una estructura nueva, resistente y mantenible**, sin exigir reutilizar soportes deteriorados.

La propuesta define trabajo y condiciones de aceptación. Las fotografías permiten identificar componentes y conexiones concretas, pero no constituyen pruebas eléctricas. Existe un CAD inicial nativo cuya editabilidad y cadena de guardado/exportación se han comprobado; todavía no hay dimensiones internas medidas, base de fabricación ni resistencia validada. El estado ejecutado está en [14 — Entrega CAD](14-entrega-cad-y-siguiente-medicion.md). Las fuentes describen herramientas y principios; las elecciones de arquitectura y pruebas son propuestas de ingeniería.

## 1. Decisión principal

Adoptar un flujo pequeño: **inventario y medidas → FreeCAD → pieza piloto → bastidor → integración funcional**. Conservar inicialmente firmware, placas, arneses, batería cerrada y módulos que se comprueben aprovechables. El objetivo final es control abierto: esta conservación no obliga a mantener siempre la placa principal cerrada. La arquitectura reserva una bandeja intercambiable separada del bastidor; las etapas y vías comprobadas están en [13](13-electronica-y-control-abierto.md). El esquema electrónico completo, los protocolos internos y una controladora nueva no son dependencias iniciales.

La primera versión busca conservar navegación, aspiración, cepillos, suspensión, detección, mopas y las funciones de estación presentes en este Pro. Xiaomi documenta un sistema que combina esos modos y automatismos [S01]. No se supone que exista un modo de servicio capaz de accionar cada motor por separado. Controlar nuestro diseño mecánico no equivale a controlar el firmware original.

La arquitectura elegida para desarrollar separa un núcleo resistente propio de cartuchos de rueda, bandejas, conductos y tapas sustituibles. Se evalúa una estructura híbrida con metal donde aporte valor; no se fija aleación o espesor antes de la implantación. Los fragmentos descartados no son necesarios: se miden interfaces y contrapartes supervivientes.

La robustez se perseguirá con caminos de carga adecuados, geometría, uniones y proceso de fabricación comprobados. La reparabilidad se comprobará retirando y reponiendo módulos: el objetivo propuesto es poder acceder a ruedas, batería y electrónica sin desmontar conjuntos ajenos cuando el espacio real lo permita. No se promete un número de minutos antes de diseñar el acceso.

### Alternativa OOMWOO y origen del CAD

La base de diseño se definirá provisionalmente por las interfaces del Xiaomi, aprovechando piezas y soluciones OOMWOO cuando reduzcan trabajo. El diseño principal de OOMWOO sigue siendo una candidatura: antes de descartarlo o adoptarlo, comprobar una revisión concreta, su edición/exportación y la superposición de envolventes Xiaomi. El STEP experimental conocido como `agentic/july-2026` no es el diseño principal ni una base validada. La auditoría y fuentes están en [09 — Comparación OOMWOO](09-oomwoo-comparacion.md).

La comparación produce una lista de piezas conservables, soportes a adaptar, interfaces nuevas e interferencias. Si bastan adaptaciones locales, derivar la base puede ahorrar trabajo. Si hay que rehacer rodadura, frontal, fondo de limpieza, mopas y acoplamiento, resulta más razonable una base propia que reutilice únicamente lo útil. Esta decisión condiciona el chasis completo, pero no bloquea inventario, modelos simplificados ni piloto de suspensión.

## 2. Inventario antes de diseñar alrededor de piezas supuestamente sanas

Cada módulo necesita **dos evaluaciones distintas**:

- Integridad mecánica: reutilizable completo; soporte exterior a reconstruir; carcasa de precisión afectada; estado desconocido.
- Funcionamiento eléctrico: observado en condiciones registradas; fallo conocido; no comprobado.

Un motor que gira puede tener un alojamiento de engranajes dañado. Una placa que enciende no demuestra que su conjunto óptico conserve alineación. No abrir reductoras u óptica sanas solo para completar el inventario. Si aparecen daños en alojamientos de cojinetes, centros de engranajes o monturas ópticas, tratarlos como una tarea de precisión separada y revisar su coste antes de comprometer el chasis completo.

Identificadores propios: MOD001 para módulo, CAB001 para arnés, CON001 para conector y F001 para foto. Los M01… del CSV de mediciones anterior siguen siendo medidas, no módulos. Mantener la referencia y revisión originales en otro campo.

Conservar las fotos originales y anotaciones aparte. Cada dato debe indicar si se observó en esta unidad, proviene del fabricante, lo declara un vendedor, es una inferencia o sigue pendiente. Para cotas: instrumento, unidad, condición de carga y referencia geométrica. No rellenar una incertidumbre con el número de decimales que muestra un calibre.

Las tablas de [módulos](electronica-modulos.csv) y [conexiones](electronica-conexiones.csv) incorporan observaciones de las 18 fotografías únicas recibidas, descritas en [10 — Inventario fotográfico](10-inventario-fotografico.md). Se ha leído B108EU_MB en la placa principal; su revisión y funcionamiento siguen pendientes. Las revisiones de placas auxiliares no se atribuyen a la principal. La plantilla de [comandos de prueba](comandos-pruebas.csv) sigue vacía: no se ha realizado ningún ensayo. Las [mediciones existentes](mediciones.csv) se amplían cuando una pieza o prueba necesita más datos.

## 3. Software mínimo y elección de cada herramienta

| Herramienta | Uso concreto | Momento y límite |
|---|---|---|
| Editor y visor de imágenes disponibles; Markdown/CSV | Fotos identificadas, piezas, cables, medidas, decisiones y resultados | Desde ahora. Ninguna foto convierte por sí sola un color de cable en un pinout. |
| Git y repositorio de investigación | Historial de documentos y relación entre revisión CAD, parámetros y ensayos | Desde ahora para resultados revisados. No sustituye copia de fotos ni medición física. |
| **FreeCAD estable** | Modelo paramétrico, conjuntos, posiciones, planos y exportación | CAD principal. El documento nativo FCStd es la definición editable del diseño. |
| Python integrado en FreeCAD | Importar parámetros y automatizar piezas o exportaciones repetidas | Cuando ahorre trabajo. No exigir otro entorno de programación antes del primer modelo. |
| **PrusaSlicer** | Revisar orientación, capas, soportes y estimaciones bajo un perfil real | Cuando haya una pieza para fabricar. OrcaSlicer puede sustituirlo si encaja mejor con el proveedor. |

FreeCAD documenta parámetros, ensamblajes, Python y formatos FCStd/STEP/STL [S02]. PrusaSlicer es gratuito, se ejecuta localmente y está disponible para Linux [S03]. Son suficientes como base de diseño y fabricación; no constituyen por sí solos una verificación de resistencia.

### Instalación y automatización en Bazzite

La primera vía a comprobar es el paquete gráfico estable de FreeCAD en Flathub, siguiendo la preferencia de Bazzite por Flatpak para aplicaciones gráficas [S04–S05]. No hace falta cambiar de sistema operativo ni alterar su imagen base.

Antes de depender de esa instalación: crear una pieza sencilla, cambiar una cota, guardar, reabrir, exportar STEP y reabrir la exportación; contrastar unidades y una dimensión. Probar una macro mínima solo si se va a usar automatización. Registrar versión y distribución utilizadas. La ejecución se completó con FreeCAD 1.1.4 de Flathub: se creó y reabrió el FCStd, se modificó una cota DEMO comprobando dependencias y se exportó/reimportó STEP. Se inspeccionaron vistas generadas con el contexto gráfico del escritorio. Registro en `cad/validacion_cad.json`. Esto verifica archivos y editabilidad; no encaje, resistencia ni geometría del ejemplar.

La automatización inicial se ejecutará mediante las macros y Python de FreeCAD. No suponer que un paquete pip instala FreeCAD ni que el Python del sistema puede importar automáticamente los módulos de su Flatpak. Si aparece una limitación concreta, resolver acceso al directorio del proyecto o evaluar una distribución oficial alternativa. No ampliar permisos o cambiar de empaquetado por anticipado.

## 4. Brainstorming de herramientas adicionales y resultado de la criba

| Candidata | Cuándo merece entrar | Decisión actual |
|---|---|---|
| Inkscape o diagrama SVG sencillo | Ilustrar el mapa de módulos o interfaces | Usar una representación simple cuando mejore la lectura; sin instalar varios editores. |
| **WireViz** | Documentar un arnés concreto con correspondencia de posiciones conocida | Opcional. Genera diagramas desde YAML y usa Graphviz; su proyecto advierte que no está pensado para representar todo el sistema [S06]. |
| **KiCad** | Documentar una interfaz modificada o un adaptador con datos eléctricos comprobados | Condicional. El ERC revisa el esquema declarado; no identifica la electrónica real [S07]. |
| **sigrok/PulseView** | Investigar una señal digital concreta con niveles, referencia y equipo compatibles | Condicional. Necesita hardware de adquisición; no es una prueba automática del robot [S08]. |
| CadQuery u OpenSCAD | Generar una familia sencilla de piezas por código o reutilizar un diseño útil | Sin añadirlos al flujo principal. Una pieza excepcional tendría una única fuente editable y entraría al ensamblaje como tal. |
| Blender, MeshLab o CloudCompare | Tratar una malla real o estudiar una forma exterior difícil | Auxiliares; no duplicar agujeros y ajustes editándolos a la vez en malla y CAD. |
| COLMAP/fotogrametría u OpenCV | Resolver una geometría que no sea práctico medir directamente | Opcionales. Escala, oclusiones y reflejos deben verificarse contra cotas independientes. Comprobar la distribución y aceleración disponibles antes de depender de ellas. |
| FEM/CalculiX | Comparar dos decisiones estructurales con cargas y materiales suficientemente conocidos | Después de definir el problema. Un resultado numérico con material genérico no demuestra fatiga o fluencia de una impresión. |
| Escáner 3D, osciloscopio o cámara térmica | Una incertidumbre concreta que el instrumental sencillo no pueda resolver | Sin compra inicial. Buscar préstamo o servicio puntual si llega a justificarse. |
| ROS, simulador robótico completo, firmware propio o PCB nueva | Objetivo explícito posterior de control abierto | Fuera de la primera base mecánica; preparar interfaces y bandeja sustituible ahora. Elegir herramientas cuando se caracterice la electrónica, sin depender de un root no demostrado. |

Las herramientas opcionales representan alternativas de trabajo, no una lista de instalación. Su criterio de entrada es una pregunta y una comprobación que justifiquen tiempo y coste. Los proyectos oficiales de CadQuery, OpenSCAD, Blender, MeshLab, CloudCompare, COLMAP y OpenCV se incluyen en las fuentes [S14].

## 5. Lo que se modelará: referencias, interfaces y acceso

Establecer un sistema de coordenadas común: X hacia el avance, Y a la izquierda del robot y Z hacia arriba, con un origen físicamente recuperable y documentado. Evitar usar como referencia única una tapa flexible o una fractura. Si una dimensión original ya no se puede recuperar con fiabilidad, registrarla como pendiente y buscar otra referencia; no completarla por simetría supuesta.

Cada módulo se representará mediante **volumen ocupado**, **interfaces de montaje necesarias** y **espacio de movimiento/servicio**. No hace falta dibujar todos los chips; sí los conectores, los apoyos, el espacio bajo la placa y las zonas que no deben tocar piezas nuevas.

| Conjunto | Interfaces que controlan el diseño |
|---|---|
| Tracción y apoyo | Diámetro efectivo, separación de ruedas, pivotes, rueda loca, topes, despeje del suelo y retención de ejes. |
| Suspensión | Anclajes, curva del muelle, recorrido, rozamiento y accionamiento del detector que realmente exista. |
| Sensores y placa | Posición, orientación, campo libre, ventanas, apoyos sin flexión y elementos de aislamiento o disipación identificados. |
| Paragolpes | Movimiento, retorno, detectores y topes; no convertirlo en una pared rígida. |
| Limpieza | Ejes y alturas de cepillos/mopas, elevación, bocas, depósito, juntas, extracción y camino de aire. |
| Estación | Rampa, contactos, señales ópticas, postura durante cada fase, acoplamiento de vaciado y posición de mopas en lavado. |
| Electricidad y radio | Parejas originales de conectores, cableado sin tracción/abrasión, batería retenida, antena y uniones conductoras observadas. |

No se ha confirmado un depósito interno ni una toma de rellenado de agua en este Pro. Si aparece una interfaz hidráulica real, se documenta; no se añade por analogía con Max o M30.

**Masa/peso, retorno eléctrico y blindaje son conceptos distintos.** Registrar y conservar las uniones conductoras y aislantes observados. No conectar una pieza estructural nueva al negativo de batería ni a una supuesta masa por intuición. Una montura nueva tampoco debe flexionar la PCB. Las guías de ST y Espressif respaldan la importancia de montaje y entorno de antena, pero no identifican chips dentro de este robot ni proporcionan sus cotas [S09–S10].

### Datos públicos para avanzar el primer CAD

La reconstrucción inicial busca primero cotas del modelo exacto en documentación, recambios, despieces y CAD público. Las cotas publicadas pueden alimentar parámetros provisionales con fuente, unidad y estado PUBLICADO, sin esperar que el propietario mida la unidad. La columna nominal_catalogo conserva esos datos; valor_medido solo recibe una comprobación física real. Una estimación de imagen lleva método y límite propios, y no se convierte en medida directa cambiando su etiqueta.

El registro único sigue siendo M01–M32, M40–M60 y M70–M89. Cada pregunta de grupo se desglosa en registros identificados cuando haya datos; no se abren series paralelas para el mismo pivote o fijación. Si una dimensión de catálogo no describe toda la pregunta, se documenta su alcance en lugar de rellenar una coordenada con ella. Por ejemplo, los 115 mm de cable publicados para las ruedas no son su recorrido libre de suspensión.

El análisis axial del [capítulo 12](12-interfaces-mecanicas-y-estacion.md) aplica una cota pública al primer cartucho: el pasador de 38,5 mm no cubre los 50 mm de la disposición DEMO. El hueco del módulo y la retención se mantienen como incógnitas de diseño; no se reducen hasta conseguir que una suma encaje. La comprobación física de montaje, función y resistencia continúa siendo necesaria antes de aprobar una pieza para uso.

### Precisión suficiente sin falsa exactitud

Por interfaz crítica, separar medida observada, nominal elegido y margen admisible por función. Considerar incertidumbre de medición, variación de fabricación y acumulación al ensamblar. Las piezas impresas no tienen una holgura universal: influyen geometría, orientación, material y proceso [S11].

Comprobar tanto el cupón local como las posiciones relativas en el bastidor completo y bajo la condición de carga pertinente. Un agujero que admite el pasador no demuestra que dos apoyos sean coaxiales ni que sigan girando después del apriete.

## 6. Arquitectura candidata del nuevo chasis

Propuesta por comparar con espacio y fabricación reales:

1. Núcleo estructural que conserva las referencias de ruedas, sensores y estación.
2. Dos soportes de suspensión extraíbles, con pivote, anclaje y acceso a su conector.
3. Cuna de batería y soporte de electrónica accesibles.
4. Conjuntos de aspiración, cepillos y mopas montables de forma independiente cuando resulte viable.
5. Perímetro de sensores y paragolpes con movimiento propio.
6. Tapas de servicio que permitan llegar a lo anterior sin actuar como único apoyo de una carga importante.

Comparar dos construcciones: piezas impresas con metal localizado en carga/desgaste, o estructura híbrida con elementos planos y soportes impresos. Ninguna se declara más barata o resistente sin geometría y presupuesto. No fijar todavía aleación, espesor, tornillos o porcentaje de relleno.

Preferir asientos que repitan posición y fijaciones que sujeten, con pasadores, casquillos, tuercas o piezas de desgaste reemplazables cuando se justifique. Diseñar extracción y herramienta junto al soporte. Dividir el chasis solo donde se pueda mantener alineación y transmitir cargas: más módulos también añaden uniones y holgura.

Pesar conjuntos y piezas fabricadas. Estudiar el reparto de apoyo con mopas levantadas y bajadas, la altura del chasis y la entrada a la estación. Si el original dañado no admite una referencia de carga fiable, declarar ese límite. No inventar un porcentaje de sobrepeso permitido.

## 7. Muelle más grande y primera pieza piloto

El muelle disponible es un candidato, no una pieza ya validada. Registrar longitud libre entre interiores de ojales, longitud exterior por separado, cuerpo, diámetro exterior, alambre y ganchos. Lee Spring distingue tensión inicial, constante, carga máxima y extensión admisible; dentro del intervalo elástico aplicable, la fuerza depende de la tensión inicial y del alargamiento [S12].

Obtener fuerza a varias longitudes de trabajo mediante especificación o instrumento adecuado. No estirar hasta deformarlo para descubrir su límite. Si carece de especificación, una comparación de fuerzas no demuestra vida a fatiga ni extensión máxima segura: esa incertidumbre debe resolverse antes de aprobar su uso.

La prueba decisiva del conjunto compara fuerza y desplazamiento de la rueda, porque el anclaje cambia el brazo de palanca. Comprobar antes el movimiento sin muelle, cuando sea practicable, y después ida/retorno con el muelle: así se distingue elasticidad de un pivote pinzado. Verificar holguras radial/axial, coaxialidad, retención y efecto del apriete; registrar detector y topes sin asumir su tipo.

Se puede sustituir solo un muelle si el comportamiento funcional resulta compatible; no se impone cambiar ambos. La primera pieza piloto será un soporte o útil propio que permita comprobar estos puntos **sin cargar el plástico roto**. Eso forma parte del chasis nuevo y no exige restaurar primero la carcasa vieja.

## 8. Herramientas físicas y fabricación de bajo coste

**Ahora:** móvil, buena luz, etiquetas, bandejas/bolsas, regla, destornilladores adecuados y calibre disponible con comportamiento conocido. No comprar por anticipado una mesa de laboratorio.

**Al comprobar cada subsistema:** balanza para masa/reparto; dinamómetro o montaje de medida con rango y resolución adecuados para la suspensión; multímetro solo para una pregunta eléctrica definida; medición térmica pertinente si el nuevo cierre cambia refrigeración o disipación. No se requiere una cámara térmica como primer recurso. La continuidad de un arnés se mide aislado de alimentación y electrónica; no se definen aquí puntos de medida energizados desconocidos.

**Fabricación:** si no hay impresora, cotizar servicio externo o taller accesible. Acordar antes el proceso y tamaño de piezas; no diseñar un chasis monolítico para una impresora hipotética. Primero cupones y pieza piloto, luego estructura. No hace falta comprar una impresora para comprobar la viabilidad inicial.

El encargo incluirá revisión, modelo, material concreto, orientación acordada, superficies y cotas críticas. Conservar los parámetros relevantes realmente usados. Si cambia una variable que afecte a ajuste o carga, repetir solo la comprobación afectada. Enviar al fabricante modelo y requisitos, no G-code de otra máquina.

PLA puede servir de plantilla sin carga; PETG es candidato para ciertas piezas, no selección universal. Los materiales especializados se justifican por función y capacidad del proceso. La orientación FDM afecta la resistencia y el ajuste [S11]. La fluencia y la relajación obligan a considerar carga sostenida, tiempo y temperatura; datos de plásticos moldeados no validan una impresión concreta [S13]. Mantener, si están sanos, componentes como juntas, ventanas y turbina equilibrada evita añadir variables de precisión innecesarias.

## 9. Pruebas: aprovechar los controles que realmente existen

Antes de alimentar, completar una tabla **comando disponible → conjuntos que puede activar → condiciones necesarias → observación esperada**. Una orden de limpieza puede activar varios motores, y la estación tiene automatismos. Preparar todos los conjuntos implicados; no asumir control independiente ni anular sensores para compensar un módulo excluido.

| Etapa | Resultado y condición para continuar |
|---|---|
| Inventario y geometría | Datos suficientes de la interfaz siguiente; lo desconocido permanece marcado. No es preciso separar un arnés intacto para completar toda la tabla. |
| CAD preliminar | Volúmenes, referencias, movimientos, paso de cables y acceso sin interferencias conocidas. Cotización y proceso antes de grandes piezas. |
| Piloto mecánico | Encaje, apriete, movimiento, fuerza-recorrido y detector comprobados en soporte propio. |
| Bastidor sin energía | Conjuntos retenidos y mecánicamente aptos; batería protegida; conexiones, aislamiento, apoyos, recorridos y alineación comprobados. |
| Primeras funciones en seco | Comandos documentados, entorno contenido, movimiento/detección y elevación de mopas según esos comandos; vigilar anomalías térmicas desde las primeras cargas relevantes. |
| Estación y limpieza | Presentación/acoplamiento sin forzar; luego carga y aspiración/vaciado mediante modos disponibles. Comprobar cierres y estanqueidad funcional de conductos modificados. |
| Lavado y secado | Solo tras las comprobaciones mecánicas y eléctricas previas; verificar la postura de cada fase, humedad y entorno térmico de las piezas nuevas. |
| Uso y mantenimiento | Registrar juego, desgaste, aflojamiento, grietas, deformación, temperatura pertinente, errores y retirada/reposición de un módulo. |

La tabla describe dependencias; el orden concreto se adapta a los comandos reales y sus automatismos. No todas las interfaces de estación tienen que estar acopladas simultáneamente si el ciclo original cambia de postura.

Las pruebas se realizan con módulos sujetos, protegidos y aptos para la acción prevista, nunca como un conjunto de placas y motores sueltos. No forzar pruebas del robot viejo si ya no puede sostenerse. Una función sin referencia previa se acepta provisionalmente bajo condiciones registradas; no se inventa una comparación antes/después.

Una ausencia de error en la app no valida temperatura ni durabilidad. Las primeras pruebas detectan anomalías y deciden si prolongar; si hace falta aceptación térmica cuantitativa, medir en puntos pertinentes y obtener límites de los componentes identificados. No utilizar el tacto como prueba cuantitativa. Anticaída se comprueba con un método contenido, sin riesgo de caída desde una escalera.

Repetir pruebas únicamente por un cambio o incertidumbre concreta. No imponer una cantidad arbitraria de ciclos como garantía de vida útil ni reabrir toda la investigación por una corrección de una cota.

## 10. Archivos, coste y reparto del trabajo

La fuente editable principal es el FCStd, con parámetros trazables a medidas. STEP y archivos de fabricación son derivados identificados por revisión. Si una pieza excepcional se genera con un script, ese script es su única fuente y no se mantiene otro maestro contradictorio. Conservar también requisitos de fabricación, fotos de referencia, lista de piezas y resultados.

Las fotos personales permanecen fuera del repositorio público salvo decisión expresa; se pueden citar por ID. Los documentos públicos contienen dibujos propios, medidas, estados y fuentes sin seriales, direcciones o credenciales. Para reproducir el proyecto se necesitan datos y versiones, no una interfaz web nueva ni una base de datos compleja.

Coste por iteración = fabricación + herrajes + transporte + recambios + piezas descartadas. Horas de trabajo y tiempo sin servicio se registran aparte. El laminador estima consumo/tiempo bajo un perfil; no cotiza preparación, fallos y envío. Software gratuito no significa fabricación gratuita.

Antes de contratar cada etapa, fijar techo de gasto y obtener presupuesto concreto. No se obliga a comprar GPU, impresora, escáner o instrumentos avanzados. Si una carcasa de precisión interna no se puede recuperar de forma razonable, revisar ese subconjunto y su coste antes de fabricar toda la estructura; el CAD preliminar y el inventario pueden continuar.

La IA puede organizar evidencia, buscar documentación, preparar tablas, modelos/macros y revisar coherencia. La captura, medidas, estado material, montaje y pruebas físicas requieren la unidad y una persona que los ejecute. No se presenta una foto ni una simulación como sustituto de esas comprobaciones.

## 11. Incógnitas que el debate no puede resolver

| Incógnita | Cómo se resuelve | Qué limita |
|---|---|---|
| Revisiones, cableado y estado funcional | Fotos y observaciones de esta unidad | Traslado de los conjuntos afectados. |
| Estado de carcasas de precisión | Inspección localizada; sin desarmar innecesariamente | Prueba o reutilización de ese conjunto. |
| Cotas y referencias originales | Medidas directas o referencias alternativas comprobadas | Fabricación de interfaces críticas. |
| Fuerza y recorrido admisible del muelle nuevo | Especificación y comprobación adecuada | Aprobación de suspensión. |
| Procesos y herramientas disponibles | Inventario del usuario y oferta concreta del taller | Material, divisiones y coste. |
| Comandos y funciones acopladas | App/manual y comportamiento observado en montaje apto | Diseño del ensayo, no inventario inicial. |
| Tolerancias, calor, radio, sellos y navegación final | Comprobaciones proporcionadas en prototipo | Aprobación para uso. |

La revisión documental termina cuando una nueva pasada independiente no modifica decisiones esenciales y cada incertidumbre material tiene una medida, prueba o decisión asignada. Esto significa estabilidad provisional del plan, no que ninguna evidencia futura pueda refutar el diseño. El historial de revisiones está en [08 — Refutaciones](08-refutaciones-y-decisiones.md).

## Fuentes y alcance

Consultadas el **25-10-2026**. Las fuentes de herramientas acreditan capacidades; las guías de materiales/componentes aportan principios generales, no resultados de ensayo del X20 Pro.

- **S01. Xiaomi, FAQ X20 Pro:** https://www.mi.com/global/support/faq/details/KA-445208/ — modos, sensores, estación y automatismos.
- **S02. FreeCAD, características:** https://www.freecad.org/features.php — modelado, ensamblaje, Python y formatos.
- **S03. PrusaSlicer:** https://www.prusa3d.com/p/prusaslicer/ — disponibilidad, ejecución local y formatos de uso.
- **S04. Bazzite, documentación:** https://docs.bazzite.gg/ — preferencia de instalación para aplicaciones gráficas.
- **S05. FreeCAD en Flathub:** https://flathub.org/apps/org.freecad.FreeCAD — paquete Linux publicado; no es una prueba de ejecución local.
- **S06. WireViz:** https://github.com/wireviz/WireViz — arneses individuales, YAML, Graphviz y límites declarados.
- **S07. KiCad, editor de esquemas:** https://docs.kicad.org/10.0/en/eeschema/eeschema.html — alcance y límites del ERC.
- **S08. sigrok/PulseView:** https://sigrok.org/wiki/PulseView y https://sigrok.org/wiki/Supported_hardware — análisis y soporte dependiente del hardware/versión.
- **S09. ST, TN1383:** https://www.st.com/resource/en/technical_note/tn1383-pcb-design-guidelines-for-mems-sensors-stmicroelectronics.pdf — efectos de montaje y esfuerzos en MEMS; no identifica una IMU del robot.
- **S10. Espressif, diseño de placa:** https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/pcb-layout-design.html — entorno de antena y comprobación final; no identifica un ESP32 en el robot.
- **S11. Prusa, diseño para impresión:** https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 — orientación, ajuste y pruebas de impresión.
- **S12. Lee Spring:** https://www.leespring.es/en/learn-about-extension-springs y https://www.leespring.fr/download/Extension_Springs_LeeSpring_US_Eng.pdf — geometría, fuerza, tensión inicial y límites de trabajo.
- **S13. Covestro, Part and Mold Design:** https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557222937.pdf — diseño, fluencia y fatiga; no proporciona propiedades de nuestra impresión. Complemento de uniones: https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557217197.pdf.
- **S14. Proyectos auxiliares oficiales:** https://cadquery.readthedocs.io/ ; https://openscad.org/ ; https://www.blender.org/ ; https://www.meshlab.net/ ; https://www.cloudcompare.org/ ; https://colmap.github.io/ ; https://docs.opencv.org/ . No son dependencias instaladas ni probadas en este proyecto.

