# 11 — Base resistente y reconstrucción sin fragmentos

**Investigación del 25-10-2026.** Frente de trabajo: estructura, referencias dimensionales y CAD de la base nueva. Se revisaron las 18 fotos privadas F001–F018, el dossier previo, documentación Xiaomi, catálogos de recambios y nuevas búsquedas específicas del modelo. Las fotografías y los identificadores individuales permanecen privados. Este frente documental no instaló aplicaciones; la ejecución posterior de FreeCAD se registra en el capítulo 14.

## 1. Decisión propuesta y alcance

Propongo desarrollar **un bastidor híbrido propio, con la estructura principal metálica y alojamientos, conductos y cierres reemplazables**, conservando inicialmente los módulos Xiaomi que se comprueben aprovechables. La base plástica original deja de ser el elemento que soporta el robot. No hace falta volver a pegar las orejetas ni recuperar los fragmentos que ya no existen.

Esta es una elección de arquitectura para desarrollar, no una especificación de fabricación aprobada. No se ha elegido espesor, aleación, tornillería o material impreso porque faltan envolventes, cargas y oferta del proceso. OOMWOO sirve como referencia de organización y soluciones; no impone su distribución ni sus componentes. El primer resultado mecánico será un soporte propio verificable, no una reparación provisional de la base vieja.

El objetivo de robot abierto tiene dos capas: **CAD, planos y piezas accesibles desde esta fase**; control y software abierto en un desarrollo posterior coordinado con electrónica. Conservar el firmware Xiaomi para validar la mecánica inicial no demuestra que el producto final tenga software abierto, ni obliga a mantenerlo para siempre.

## 2. Qué documentación exacta existe y qué no se ha encontrado

Xiaomi identifica el Pro como **D102GL**, con envolvente exterior declarada **Ø350 × 97 mm**, y estación europea **D102-JZEU**. Son datos del producto completo, no cotas internas. El peso publicado no sustituye pesar los módulos y la estructura nueva. [S01]

El manual Xiaomi muestra las posiciones generales de rueda loca, ruedas motrices, cepillo, mopas, sensores y contactos; describe mantenimiento ordinario. No ofrece el plano acotado de la base, centros de pivote, material estructural, espesores ni un despiece de servicio. Se revisó el manual de autoría Xiaomi servido por su CDN como corroboración visual; sus especificaciones regionales de estación no se transfieren a la versión EU. [S02]

El catálogo filtrado por Pro contiene ruedas, pasadores, muelle, motores de mopa, turbina, placa y conjuntos periféricos. Es documentación comercial de piezas, no un plano de montaje OEM. No localicé en las fichas inspeccionadas una base estructural desnuda identificada inequívocamente como Pro. La carcasa completa SKU 41414 sigue declarando **X20 Max**; no se adopta su geometría ni se recomienda como recambio compatible. Las tapas superiores de mantenimiento tampoco son equivalentes a la base portante. [S03–S05]

Las búsquedas nuevas incluyeron D102GL y X20 Pro con términos de carcasa, base, chasis, desmontaje, reparación e imágenes internas en español, inglés, francés, alemán, polaco, ruso y chino. No apareció un CAD OEM acotado o un desmontaje completo del Pro exacto que resuelva las coordenadas ausentes. El caso de rueda rota publicado por un propietario confirma que existe ese relato individual; no aporta un plano dimensional ni datos de frecuencia de fallo. [S06]

Los vídeos M30/Max del dossier siguen siendo referencias de familias relacionadas. No sustituyen las medidas de D102GL. **La evidencia exacta más útil del interior es actualmente la unidad y sus 18 fotografías.** El límite de la búsqueda no prueba que nunca exista otro documento; identifica lo que no está disponible para fabricar hoy.

## 3. Lo que sobrevive y puede definir el diseño nuevo

La base original reúne funciones distintas: soportar cargas, colocar módulos, guiar movimiento, sujetar cableado, cerrar aire/polvo y formar superficies de contacto con el entorno. Sustituirla requiere reasignar cada función; no basta un disco con agujeros para los motores.

| Referencia física observada | Datos que pueden medirse sin fragmentos | Lo que esa referencia NO recupera por sí sola |
|---|---|---|
| Rueda con motor y reductora, F006; pasadores, F008 | Eje/pivote disponible en el módulo, diámetro y longitud del pasador, ancho de alojamientos, barrido de la rueda, salida del cable | Posición absoluta original del pivote perdido, geometría completa del enganche fijo o carrera correcta del detector |
| Mecanismos de mopa con carcasa y orejetas, F005/F009/F010 | Patrón de fijación, caras de apoyo, eje de salida, altura y recorrido del conjunto si está mecánicamente apto | Distancia global a rueda, suelo y estación sin otra referencia |
| Turbina con carcasa propia, F002 | Fijaciones, entradas/salidas, juntas, volumen y orientación del conjunto | Forma de todo el conducto integrado en la base ni pérdidas aceptables del circuito nuevo |
| Motor y caja del cepillo, F004/F013/F018 | Eje, apoyos del rodillo y transmisión conservada, bocas, cubiertas y superficies de sellado accesibles | Altura de trabajo del rodillo y distribución original si se han perdido sus referencias globales |
| Placa principal curva y cubierta, F013; placas auxiliares F007/F011 | Contorno, agujeros, alturas, apoyo inferior, ventanas de botones y volumen para conectores | Localización de la antena o una orientación de sensor inercial no identificada; no asignarlas por apariencia |
| Conjunto posterior, F012 | Geometría propia, apoyos, cara exterior y relación de sus piezas si se conserva completo | Su altura de contacto con la estación sin cotejar robot/base |
| Frontal con unidades ópticas y flex, F014–F016 | Distancias y orientación entre sensores, fijaciones, ventanas, forma del flex y apoyos del conjunto | Recorrido completo de paragolpes y su relación con ruedas/suelo sin montaje o referencias adicionales |
| Carcasa superior con LDS fijado y pieza negra tubular junto al hueco central, F014/F017/F018 | Patrón de fijación y plano del LDS; puntos de unión y geometría de la pieza negra superviviente | Altura/orientación final respecto al suelo; función de la pieza negra todavía no confirmada, sin asignarle un circuito concreto |
| Batería cerrada, F001/F018 | Envolvente, masa, apoyo y espacio para cable/conector | Una posición de centro de gravedad del robot completo |
| Estación original, todavía sin fotografías dimensionales en esta serie | Rampas, contactos, superficies de presentación, bandeja y acoplamientos reales | Coordenadas internas del robot; es una condición funcional de encaje, no un plano inverso único |

Las fotos indican qué medir, pero no contienen escala válida para sacar cotas de fabricación. No se usa el teclado, las herramientas, las cabezas de tornillo ni la capacidad de la batería como regla. Las piezas que aparecen montadas deben confirmarse todavía presentes y estables: una fotografía histórica no demuestra el estado después de nuevas roturas.

La carcasa superior no se clasifica entera como meramente estética: además del LDS conserva la pieza negra señalada. Antes de retirarla del proyecto hay que identificar sus conexiones y superficies de contacto. El circuito de aire o las interfaces del depósito podrían repartirse entre piezas superiores e inferiores; es una posibilidad a resolver por inspección, no una identificación de autovaciado basada en la forma.

## 4. Método de reconstrucción cuando faltan piezas

### 4.1 Dos problemas diferentes

**Geometría local:** la cara de un módulo sano o su patrón de agujeros puede medirse directamente y recibir una cuna nueva. No necesitamos copiar la forma del plástico que antes lo sostenía.

**Geometría global:** dónde debe quedar ese módulo respecto a ruedas, suelo, sensores y estación. Esta posición requiere una cadena de referencias. Medir perfectamente cada pieza por separado no reconstruye automáticamente su disposición original.

### 4.2 Referencias recuperables, en orden de confianza

1. **Zonas intactas todavía unidas del conjunto original.** Agujeros, caras de asiento o ejes que conserven su relación pueden servir como referencias de medida, sin poner el robot en carga ni reutilizarlos como estructura. Una zona agrietada o que flexiona no fija el sistema de coordenadas.
2. **Contrapartes sanas.** La carcasa superior, el conjunto de cepillo, un soporte periférico o el propio módulo pueden conservar superficies que encajaban entre sí. Medir ambos lados del acoplamiento ayuda a recuperar posición y orientación. No sujetar una PCB como si fuera una placa de utillaje.
3. **Referencia externa del modelo exacto.** Si una coordenada crítica se ha perdido por completo, una medición verificable de otro D102GL o de su pieza exacta puede resolverla. Una foto sin escala, la simetría aparente o un Max no completan el dato.
4. **Posición nueva deliberada.** Si no se recupera la original, la nueva posición debe declararse propuesta y tener pruebas funcionales específicas. No se etiqueta como cota OEM; puede introducir una incertidumbre de firmware que obligue a revisar el alcance.

Los fragmentos desaparecidos no se solicitan ni forman una dependencia. La macro de CAD tampoco debe deducir por simetría un alojamiento que nadie ha medido.

### 4.3 Un útil sencillo y un sistema de coordenadas reproducible

Usar un tablero o placa de referencia suficientemente estable para la tarea, apoyos y topes que no deformen las piezas. Comprobar que repetir el montaje reproduce las medidas; la superficie del banco no se supone metrológicamente perfecta. El principio de separar **localización** de **sujeción**, con apoyos y topes bien definidos, está documentado por Carr Lane. [S07]

Para el CAD, mantener X hacia el avance, Y hacia la izquierda del robot y Z hacia arriba. Un origen provisional puede pertenecer al útil, identificado por puntos físicos recuperables. Cuando se conozca la rodadura se registra la transformación al marco funcional del robot. No se redefine silenciosamente el origen para que una pieza encaje.

Cada medida debe guardar: interfaz, valor/unidad, puntos entre los que se midió, instrumento, estado de carga/movimiento, repetibilidad observada, fotografía de contexto y condición de evidencia. Distinguir dato observado, dato publicado, nominal propuesto y pendiente. Una incertidumbre pendiente no vale cero.

**Primera captura de mayor valor:** vista completa superior e inferior con frontal marcado y regla en el plano de los elementos medidos, acompañada de medidas directas entre referencias intactas. Las imágenes rectificadas pueden apoyar un trazado de contorno; las alturas, ejes y ajustes requieren medidas independientes. Para agujeros, comprobar más de una distancia entre centros y una diagonal evita confundir perspectiva o giro con geometría.

### 4.4 Datos estructurales que todavía faltan

IDs provisionales de este informe, con identificadores propios; el coordinador mantiene el registro común:

| ID | Medida o observación | Método mínimo útil | Decisión que permite |
|---|---|---|---|
| SB01 | Referencias supervivientes y estabilidad de sus relaciones | Fotos de contexto, inspección sin carga y repetición de distancias | Elegir referencias del útil y del modelo |
| SB02 | Centros globales de pivotes y apoyo delantero | Medida directa en partes estables o referencia exacta independiente | Geometría de rodadura, posiciones de cartuchos |
| SB03 | Envolventes ocupadas y barridas por rueda/mopas/paragolpes | Medidas de extremos y posiciones de movimiento mecánicamente aptas | Zonas donde no pueden pasar travesaños |
| SB04 | Planos y patrones de fijación de cada módulo | Calibre/regla según necesidad, distancias cruzadas y alturas | Soportes reemplazables y cotización |
| SB05 | Aperturas, conductos y superficies de juntas | Secciones/contornos y prueba de encaje de tapas existentes | Fondo funcional y sellos independientes |
| SB06 | Ventanas y orientación de sensores; campos libres | Montaje conservado, distancias y vistas de perfil | Soporte óptico y límites de material opaco/conductor |
| SB07 | Interfaz robot/estación en sus distintas posturas | Medidas de robot y estación; presentación pasiva sin forzar | Altura, contorno inferior/posterior y acoplamientos |
| SB08 | Masas de conjuntos y reparto del apoyo | Balanza y montaje retenido apto | Cargas y objetivo de masa, sin porcentaje inventado |
| SB09 | Acceso real de herramientas y extracción de módulos | Maniobra en maqueta/útil; registrar piezas que estorban | Partición de tapas y uniones |
| SB10 | Proceso y precisión que ofrece el fabricante | Oferta concreta y pieza/cupón representativo | Material, tolerancias, divisiones y acabado |

## 5. Arquitectura híbrida: dónde pondría metal y dónde piezas sustituibles

### Núcleo de la propuesta

Un **marco abierto con recortes y travesaños en los huecos reales**, que mantenga la posición relativa de los apoyos de rodadura y de las interfaces críticas. Las piezas planas cortadas y, donde proceda, dobladas o unidas a perfiles sencillos son candidatas a fabricar externamente. Los recortes de cepillo, ruedas y mopas impiden asumir una placa continua; la rigidez se comprueba después de introducir esas aperturas y uniones.

El número de sectores, su espesor y su orientación dependen del mapa interior. No se fija una estructura arbitraria en X que pueda cruzar el conducto o una mopa, ni una enorme placa maciza que haga el robot más pesado sin resolver las fijaciones.

| Interfaz o función | Solución candidata | Razón y comprobación necesaria |
|---|---|---|
| Reacción de ruedas y suspensión | Cartucho de rueda desmontable, con apoyos del pivote y anclaje de muelle fijados al marco | El fallo local no obliga a sustituir toda la base. Comprobar coaxialidad, recorrido, retención, detector y fuerza de rueda. |
| Pasador y zona de desgaste | Soporte con apoyo por ambos lados donde la geometría lo permita; casquillo/asiento reemplazable | Evitar que una pequeña pared impresa en voladizo sea la única reacción. No prescribir diámetro o ajuste sin medir pasador/módulo. |
| Anclaje fijo de muelle | Orejeta o puente mecánico independiente unido al cartucho/marco | La carga se distribuye; conservar brazo de palanca y carrera. Endurecer el muelle no es reforzar el chasis. |
| Apoyo delantero | Cuna desmontable con asiento localizado y retención accesible | Mantener altura y giro completo; comprobar carga y holgura sin atrapar el caster. |
| Módulos de mopa/cepillo/turbina | Adaptadores específicos atornillados y desmontables | Reutilizar carcasas funcionales sanas conserva transmisiones y geometría interna. La base nueva recoge sus esfuerzos por apoyos amplios. |
| Placas y batería | Cunas aislantes, retención y apoyos medidos; acceso sin retirar transmisión | No usar la PCB para arriostrar el marco ni sujetar batería mediante presión localizada. Conservar espacio de conectores y aislamiento. |
| Aire y polvo | Conductos/cierres independientes y juntas reemplazables | Separar estanqueidad de la función resistente; una junta no compensa una placa que se deforma en servicio. |
| Fondo exterior, ventanas y tapas | Sectores pequeños, accesibles y reemplazables | Reponer una pieza de contacto/desgaste no debe cambiar la referencia de ruedas o sensores. |
| Paragolpes y topes | Subsistema con movimiento y retorno propios | La estructura resistente no debe anular su recorrido ni transmitir golpes directamente a la óptica. |

**El objetivo es que el desgaste o un daño local sean reparables; no diseñar deliberadamente una unión que se desprenda durante uso.** Si se desea una pieza fusible, su carga de activación requerirá una especificación y prueba separadas.

### Uniones que no dependan de apretar plástico indefinidamente

En los puntos importantes se evaluarán tornillos pasantes, tuercas accesibles/cautivas, superficies de reparto y, cuando corresponda, separadores que reciban la compresión del tornillo. SPIROL documenta cómo los limitadores de compresión protegen conjuntos de plástico y mantienen la unión; exige un apoyo adecuado bajo la cabeza/arandela. Eso justifica estudiar el detalle, no copiar automáticamente sus cotas o pares a FDM. [S08]

Un inserto roscado por sí solo no resuelve la fluencia del plástico que queda comprimido entre piezas. Las nuevas uniones deben poder inspeccionarse, conservar alineación tras desmontaje y no invadir batería, cables o movimiento. El metal también necesita cantos acabados, aislamiento eléctrico y ubicación compatible con antenas y ventanas. La zona posterior/inferior estará próxima al lavado; el cierre y los materiales de unión deben considerar ese entorno.

### Material impreso

Los adaptadores impresos permiten geometrías compactas y sustitución económica, pero la orientación, los perímetros, el material y la fabricación real condicionan ajuste y comportamiento. Prusa documenta que no existe una tolerancia universal y que dividir una pieza puede mejorar su fabricación. [S09]

Se elegirán material y orientación por función. PLA puede servir para una plantilla sin carga; no queda aprobado como soporte duradero de muelle. PETG tampoco recibe una aprobación universal. Si una orejeta sigue siendo el único elemento que soporta carga cíclica elevada, el cambio de inyección a FDM exige resolver el camino de carga y ensayarlo, no solo aumentar el relleno.

## 6. Cómo reflejarlo en un CAD editable

### Modelo principal y estados de evidencia

FreeCAD ofrece modelado paramétrico, Python y exportación de sólidos/planos. Su FCStd será el documento editable principal; STEP es intercambio y STL/3MF, cuando corresponda, son salidas de fabricación. [S10]

Propuesta de grupos, cuyos nombres puede adaptar el proyecto:

| Grupo | Contenido | Estado inicial honesto |
|---|---|---|
| `Referencias` | Ejes, origen, planos de medida y envolvente exterior publicada | Datum provisional; dimensiones exteriores de fabricante, sin equipararlas a base interna |
| `Modulos_conservados` | Volúmenes simplificados de conjuntos, apoyos y conectores | Interfaces observadas; cotas pendientes hasta medir |
| `Espacios_libres` | Barridos, extracción, herramientas, cables y campos ópticos | Requisitos pendientes o comprobados, separados de sólidos fabricables |
| `Bastidor` | Partes metálicas, recortes, uniones y apoyos globales | Arquitectura propuesta; dimensionamiento pendiente |
| `Cartuchos_rodadura` | Soportes de rueda/caster, pasadores, anclajes y topes | Interfaz con estudio de suspensión; no espejo automático |
| `Adaptadores_y_conductos` | Soportes de módulos y cierres funcionales | Reutilizable por piezas, con su revisión |
| `Tapas_servicio` | Sectores de fondo y accesos | Volumen y sentido de extracción declarados |
| `Comprobaciones` | Posiciones de movimiento, interferencias y referencias de ensayos | No convertir una simulación de montaje en prueba de durabilidad |

Cada pieza debe exponer los parámetros útiles: coordenadas de referencia, patrón de apoyo, distancias entre fijaciones, espesor propuesto y holgura funcional justificada. Los sketches de piezas planas y extrusiones/cortes simples permiten modificar el modelo sin depender de una malla opaca. Conviene acotar a planos/ejes estables en vez de encadenar todo a caras generadas que cambien tras una edición.

**Datos desconocidos:** conservarlos como `pendiente` en la tabla; el generador no debe crear un agujero o soporte de fabricación con un cero o un valor ilustrativo presentado como real. Para explicar una arquitectura pueden existir piezas `DEMO`, ocultas o separadas de las piezas fabricables y rotuladas en la vista/exportación. Una envolvente Ø350 × 97 mm es una referencia exterior oficial, no la base terminada.

### Herramientas realmente disponibles

En este entorno de investigación se verificó que OCP y CadQuery están preinstalados, pero no se encontró FreeCAD, su módulo `Part`, `FreeCADCmd` ni Flatpak. Se puede generar/inspeccionar un sólido neutral con esas bibliotecas; eso no prueba que se haya producido y reabierto un FCStd paramétrico.

Para FreeCAD en el Bazzite del usuario, existe paquete publicado en Flathub y Bazzite documenta su gestión de aplicaciones gráficas [S11–S12]. Este frente investigó la vía de instalación; posteriormente el coordinador instaló FreeCAD 1.1.4 y ejecutó, guardó, reabrió y modificó una cota del CAD inicial en ese equipo. El capítulo [14](14-entrega-cad-y-siguiente-medicion.md) y `cad/validacion_cad.json` documentan esa ejecución y sus límites. No se extrapola a resistencia o encaje físico.

Si se usa CadQuery para una pieza excepcional, su script es la fuente única de esa pieza y el STEP entra al ensamblaje como derivado; no prometer que importar STEP crea automáticamente el historial paramétrico. No abrir tres fuentes de verdad paralelas para el mismo bastidor.

## 7. Fases y entregables que permiten avanzar sin los fragmentos

| Fase | Trabajo y entregable | Qué se puede dar por terminado |
|---|---|---|
| A. Definición ahora | Arquitectura, mapa de interfaces, tabla de datos pendientes y árbol de CAD con referencias verificadas | Decisión de diseño documentada y modelo conceptual identificable; no archivo de fabricación aprobado |
| B. Recuperación dimensional | Útil/referencias y medidas de módulos, posiciones críticas y estación | Modelo de implantación y primeros adaptadores acotados; dependencias perdidas explícitas |
| C. Piloto propio | Un cartucho o unión representativa unido a soporte propio; cupón del proceso elegido | Encaje, apriete, geometría y movimiento de esa interfaz; no validación del robot entero |
| D. Bastidor completo sin energía | Conjuntos retenidos, acceso, masa, reparto, barridos y presentación a estación | Integración mecánica apta para las funciones que vayan a ensayarse |
| E. Cierre y funcionamiento | Aire/polvo, sensores, movimiento, carga y servicios de estación con comandos disponibles | Funcionamiento observado por modo, condiciones y revisión; incidencias registradas |
| F. Durabilidad y publicación | Seguimiento de juego, aflojamiento, deformación y mantenimiento; CAD/BOM/planos revisados | Publicación de lo comprobado y límites restantes; no promesa de vida indefinida |

La prueba del piloto no debe saltarse el comportamiento del bastidor: dos apoyos que funcionan solos pueden desalinearse al cerrar/apretar la estructura. Para durabilidad, definir carga y condiciones relevantes después de medir; una cantidad arbitraria de ciclos no convierte un prototipo en garantía de vida útil.

## 8. Resultado de la revisión crítica

La nueva base puede diseñarse sin conservar las orejetas originales. La información que falta es recuperable en parte a través de módulos y contrapartes; algunas posiciones globales pueden requerir una referencia adicional del modelo exacto. Debe declararse ese límite antes de asignar números al CAD.

La arquitectura híbrida es una propuesta razonable porque separa caminos de carga, desgaste, sellado y acceso. Su aprobación depende de la implantación y del proceso: podría resultar preferible cambiar la partición si los travesaños no caben o si una pieza metálica compleja encarece mucho la fabricación. No se obtiene mayor robustez solo sustituyendo todos los plásticos por metal.

Las búsquedas ya no son el principal bloqueo para fabricar: lo son las medidas del ejemplar, las posiciones perdidas y las pruebas de unión/suspensión. Se puede comenzar ahora el proyecto CAD y su documentación sin confundir esa primera versión con una base lista para encargar.

## Fuentes primarias y evidencia

- **S01. Xiaomi España, especificaciones D102GL:** https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/specs/
- **S02. Manual Xiaomi desde CDN oficial, identificación D102GL y dibujos de mantenimiento:** https://i02.appmifile.com/993_operatorx_operatorx_xm/13/05/2025/77d23ed347099a90e75ce297d1202d40.pdf . Complemento exacto de funciones/sensores: https://www.mi.com/es/support/faq/details/KA-922892/ . No son planos dimensionales de servicio.
- **S03. Catálogo de recambios, declaración directa del vendedor filtrada por Pro:** https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html y segunda página `?page=2`.
- **S04. Carcasa completa que declara Max, sin equivalencia Pro comprobada:** https://www.ep-mediastore-ab.de/xiaomi-x20-max-gehaeuse-komplett-p-41414.html
- **S05. Tapas de mantenimiento declaradas Pro:** https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-weiss-s20-x20pro-p-29986.html ; la identificación ya se revisó en el dossier anterior.
- **S06. Relato de primera mano de rueda/muelle Pro, sin datos dimensionales o estadísticos:** https://www.reddit.com/r/RobotVacuums/comments/1t2604u/need_help_with_my_xiaomi_x20_pro_one_wheel_stays/
- **S07. Carr Lane, principios de localización y sujeción:** https://www.carrlane.com/engineering-resources/fixture-design-principles/locating-clamping-principles
- **S08. SPIROL, integridad de unión con limitador de compresión:** https://my.spirol.com/resources/white-papers/how-to-ensure-bolted-joint-integrity/ ; producto y concepto: https://www.spirol.com/product/compression-limiters/
- **S09. Prusa, diseño para impresión y tolerancias:** https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- **S10. FreeCAD, capacidades oficiales:** https://www.freecad.org/features.php y sitio oficial servido desde GitHub Pages https://freecad.github.io/Website/features/
- **S11. FreeCAD publicado en Flathub:** https://flathub.org/apps/org.freecad.FreeCAD
- **S12. Bazzite, gestión de aplicaciones:** https://docs.bazzite.gg/Installing_and_Managing_Software/

**Evidencia privada:** F001–F018, inspeccionadas visualmente; no se copian ni publican aquí. Las propuestas de estructura, medición y fases son razonamiento de ingeniería propio, no instrucciones OEM ni resultados de resistencia ya ensayados. La integración y el estado ejecutado del CAD se registran en el capítulo 14.


---
Documentación original de este proyecto: CERN-OHL-P-2.0. Alcance y exclusiones en [cad/LICENCIAS.md](cad/LICENCIAS.md). Las fuentes y diseños de terceros conservan sus derechos.
