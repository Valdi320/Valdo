# 13 — Electrónica, montajes y control abierto

**Fecha de consulta: 25 de octubre de 2026. Modelo: Xiaomi Robot Vacuum X20 Pro D102GL.**

Este informe estudia la sustitución de la base plástica portante, conservando los conjuntos útiles y construyendo soportes reemplazables. El destino del proyecto es un robot reparable con control abierto. **Conservar ahora la electrónica y el firmware originales es una etapa para reducir variables, no el objetivo final.** Los fragmentos desaparecidos no se consideran disponibles para reconstruir soportes.

Se revisaron los documentos 07, 09 y 10 del dossier, el inventario CSV y las fotografías privadas F001–F018. En esta ronda se volvieron a inspeccionar F013, F014 y F017 para estudiar los montajes. No se ha alimentado la unidad, medido circuitos, instalado software en ella ni modificado firmware. Esta nota no contiene fotografías privadas, identificadores individuales ni credenciales.

## 1. Conclusiones que condicionan el diseño

1. **La nueva base debe referenciar más conjuntos que la placa principal.** En las fotos hay electrónica en el cuerpo inferior, en el cascarón superior y en el paragolpes. La placa B108EU_MB es ancha y curva; los mandos están sobre ella; el LDS conserva su apoyo en la carcasa superior; dos conjuntos ópticos del paragolpes están unidos por un flex largo. Esas relaciones son observables y deben entrar al ensamblaje CAD. [P: F013–F018]
2. **No hace falta reconstruir la forma exacta de cada tetón roto.** Se pueden crear portamódulos nuevos a partir de agujeros, planos y superficies funcionales sanos de los componentes conservados. Lo que falta recuperar es su posición relativa, orientación y condiciones de apoyo; la foto sin escala no da cotas de fabricación. Esta es una propuesta de ingeniería, no un plano Xiaomi.
3. **Una estructura más rígida no debe sujetar rígidamente todo lo que antes se movía.** Suspensión, paragolpes, cubierta móvil del LDS si la unidad la incorpora, salidas de mopas y arneses necesitan sus recorridos. La rigidez del bastidor debe transmitir cargas por sus apoyos; no mediante una PCB, una lente, un conector o un cable.
4. **Valetudo no ofrece hoy soporte oficial del X20 Pro.** Su lista se declara exhaustiva y no contiene X20 Pro/D102GL. Además, el proyecto conserva el firmware del fabricante: sustituye la dependencia de nube, no todos los algoritmos y controladores. [S01–S02]
5. **Sí existe trabajo abierto específico para órdenes de alto nivel del D102GL.** El código actual de `hass-xiaomi-miot` contiene su modelo y acciones de limpieza, pausa, lavado, secado y retorno. Es una posible herramienta posterior de supervisión, no un controlador abierto de motores ni evidencia de funcionamiento en esta unidad. [S04–S06]
6. **El diseño mecánico debe permitir sustituir la electrónica de control.** Una bandeja provisional para B108EU_MB, uniones documentadas y acceso a conectores evitan convertir la placa cerrada en parte inseparable de la estructura definitiva. No se ha elegido una controladora nueva ni se ha demostrado que pueda conservarse toda la electrónica original al abrir el control.

## 2. Qué significa cada evidencia

| Etiqueta | Significado | Límite |
|---|---|---|
| **P** | Observación directa en las fotografías privadas de esta unidad | Identifica forma y texto legibles; no demuestra continuidad, integridad interna o funcionamiento |
| **E1** | Fuente oficial exacta Xiaomi del X20 Pro | Identidad, funciones y mantenimiento; no proporciona esquema o plano interno dimensionado |
| **E2** | Ficha del vendedor del recambio exacto | Declara compatibilidad comercial y referencias; no certifica revisión ni pinout de esta unidad |
| **E3** | Evidencia primaria de un modelo relacionado | Sólo acredita lo observado en aquel modelo |
| **E4** | Inferencia o propuesta de ingeniería | Debe convertirse en medida, prueba o decisión antes de fabricar |
| **SW** | Documentación o código del propio proyecto de software | Acredita su alcance declarado; no implica soporte de hardware Xiaomi no identificado |

Se mantienen dos estados por conjunto: **integridad mecánica** y **funcionamiento eléctrico**. Ninguna fotografía acredita ambos. La clasificación mecánica distingue conjunto reutilizable completo, soporte exterior que rehacer, carcasa de precisión afectada y estado desconocido. No se da por sana una reductora porque gire el motor ni por averiada una pieza por su aspecto sin inspección pertinente.

## 3. Inventario real que debe entrar al CAD

Los MOD siguientes corresponden al CSV existente. Se conservan sus nombres provisionales y sus incertidumbres.

| ID / conjunto | Referencia y evidencia | Interfaz que debe modelarse | Qué sigue pendiente |
|---|---|---|---|
| **MOD001, batería cerrada** | SCUD **P2150-4S2P-SCEV**; F001. Etiqueta: 14,4 V nominales, 5200 mAh nominales, 4800 mAh rated, límite de carga 16,6 V y 69,12 Wh rated | Cuna, superficies de apoyo, retención, salida del cable, acceso a conector y trayectoria de extracción | Dimensiones y masa reales, posición original precisa, integridad exterior, pareja del conector y estado funcional. No se conocen las funciones de cada conductor |
| **MOD002, placa principal** | **B108EU_MB**, F013; ficha Pro [S10] | Contorno real, puntos de apoyo, alturas bajo/sobre PCB, cubierta, conectores y su extracción, orientación respecto al robot | Revisión, patrón completo, cara inferior, CPU/radio/antena/IMU y esquema. La revisión VB2 de las auxiliares no pertenece automáticamente a esta placa |
| **MOD003, mandos** | **B108EU_SWITCH**, **VB2**, F011/F013; dos pulsadores y LEDs | Soporte a su altura, alineación con botones, reacción de pulsación, arnés corto a MOD002 | Cotas y pila de montaje. No transferir fuerza de pulsación a una zona de PCB sin apoyo |
| **MOD004, auxiliar de pulsador/LED** | **B108EU_WIFI_LED**, **VB2**, F007 | Apoyos, acceso al pulsador/indicador y dos salidas de arnés | Posición de conjunto y destinos de los dos ramales. El nombre no identifica transceptor Wi-Fi ni antena |
| **MOD005, aspiración** | **HJD-RA60405 V1.5 / BL.531124.0161**, KELI, DC14.4V, F002; [S11] | Soporte del conjunto completo, electrónica local, entrada/salida de aire, juntas y cable | Cotas, integridad de carcasa/soportes, conexión exacta y comportamiento térmico. Mantener rotor, voluta y electrónica como conjunto mientras sean aptos |
| **MOD006, motor asociado provisionalmente al cepillo principal** | **PRI-390SV-24100**, F004/F013 | Conjunto motor/transmisión, apoyos y salida de cable; su interfaz mecánica la desarrolla la nota de mecanismos | Confirmar asociación, transmisión, referencia eléctrica y estado. Dos terminales visibles no bastan para especificar tensión de control o corriente de arranque |
| **MOD007–008, conjuntos de mopa A/B** | Lectura provisional **PRI-385SV-2185** en una vista, F005/F009/F010 | Conjunto motor/reductora, cableado adicional, movimiento y conectores | Asignación de lado, referencia individual, función de los hilos adicionales y carcasa de precisión. No inferir encoder/Hall sólo por el número de hilos |
| **MOD009 y segunda rueda por inventariar** | F006/F008/F018; módulos y pasadores observados | Soporte de pivote, detector/actuador que exista, camino de arnés con suspensión en ambos extremos, conector accesible | Detalle de ambos detectores, correspondencia lado/conector, recorrido y estado. La mecánica detallada corresponde a la nota de ruedas |
| **MOD010–011, frontal y unidad lateral** | **B108EU_CamSub VC1**, **CN1500**, F014–F016; dos unidades unidas por flex | Planos, posiciones y orientaciones relativas, ventanas, fijaciones, radio/recorrido del flex y movimiento del paragolpes | Cotas y conexión a principal. CamSub no demuestra una cámara RGB ni capacidad de vídeo convencional |
| **MOD012, placa perimetral** | Sólo **D102…** es legible en F012. Asociación a contactos/IR posterior provisional; vendedor ofrece ese conjunto Pro [S12] | Conservar unidad y su relación con contactos/ventana exterior; montar en soporte reemplazable | Completar relación física exterior, función y cableado. **D102_BIR** de la ficha comercial no se presenta como serigrafía leída en la foto |
| **MOD013, LDS superior** | F014/F017/F018; PCB, motor y soporte fijados a carcasa superior | Puente o soporte referido a la base, plano de montaje, posición angular, altura, apertura de escaneo y espacio de cubierta/motor | Referencia exacta, cotas, pareja externa y estado. No sustituir su apoyo por una tapa flexible sin comprobar rigidez y geometría |
| **Otro elemento de la carcasa superior, sin asignación funcional** | F018 muestra una pieza negra con forma de conducto junto al hueco central | Registrar su volumen y sus superficies de unión antes de eliminar la carcasa como soporte | Función y recorrido pendientes; no se identifica como autovaciado ni se supone prescindible |
| **Sensores inferiores y elementos aún sin ID individual** | Xiaomi enumera sensores de desnivel y ultrasonidos; la óptica frontal/lateral también está documentada [S09] | Ventanas, orientación y altura respecto al suelo; evitar que nervios o herrajes invadan sus aperturas | Inventario visual de cada módulo de esta unidad y recorrido de cables; no inventar número total ni puertos |
| **Presencia de depósito/platos, detección de bumper, altavoz y motor lateral** | Funciones y/o recambios exactos en fuentes previas; fotos no cierran su mapa completo | Alojamientos y accionadores físicos además de la electrónica | Confirmación localizada al medir el sector correspondiente; no crear un esquema completo a partir del catálogo |

**Tensiones distintas no se mezclan:** el límite 16,6 V impreso en el pack no es la salida de la estación. La especificación oficial del conjunto de carga es independiente. Ningún dato de etiqueta autoriza alimentar directamente una entrada desconocida o abrir el pack. Un vendedor advierte además que baterías exteriormente parecidas de otra familia pueden tener polaridad diferente [S13].

## 4. Mapa de conexiones: lo confirmado y lo no confirmado

| Relación física | Evidencia | Estado a registrar |
|---|---|---|
| MOD003 SWITCH ↔ MOD002 principal | Ambos extremos y arnés corto visibles en F011/F013 | Pareja de módulos observada; asignación de pines desconocida |
| MOD010 ↔ MOD011 | Flex continuo visible en F014 y extremos en F015/F016 | Recorrido físico observado; no se ha medido continuidad |
| Motor del LDS ↔ PCB local del LDS | F017 | Conexión interna observada; no equivale a la interfaz externa de MOD013 |
| WIFI_LED ↔ dos ramales | F007 | Destinos pendientes |
| Principal ↔ ramal libre hacia zona central | F013 | Un extremo observado; no emparejar con LDS por parecido |
| Perimetral D102… ↔ arnés | F012 | Destino pendiente |

En F017 se leen textos como `TX`, `PWM/RX`, `SCL`, `SDA`, `GND` y `VCC` junto a puntos de prueba. **No constituyen el pinout del receptáculo.** Faltan relación pin-pad, niveles, función y protocolo. Tampoco se deduce el negativo de potencia por color, el paso de un conector por apariencia ni una referencia comercial de serie a partir de una foto general.

Para el traslado intacto basta conservar las parejas originales y documentar los ramales que se separan. Un esquema de bloques describe módulos y conexiones; un pinout añade correspondencias y función de cada contacto; un esquema eléctrico describe circuitos. **Hoy disponemos del inicio del primero, no de los otros dos.**

## 5. Arquitectura de montaje propuesta

Sistema común ya acordado: **X hacia delante, Y hacia la izquierda del robot, Z hacia arriba**, referido a datums recuperables del conjunto. El origen concreto debe documentarse con la geometría mecánica; no asignarlo a un fragmento desaparecido.

La propuesta separa cinco soportes de electrónica y sus interfaces, sin decidir todavía material o espesor:

| Pieza CAD propuesta | Función y dependencia | Condición de reemplazo |
|---|---|---|
| `bandeja_electronica_original` | Sujeta MOD002 y mantiene su pila de apoyos/cubierta; referencia MOD003 cuando proceda | Extraíble con tornillería accesible y espacio de desconexión. No debe servir de travesaño portante imprescindible del robot |
| `soporte_mandos_auxiliares` | Recibe esfuerzos de botones y sitúa indicadores; conserva ramales cortos | Sustituible sin rehacer el bastidor; fijaciones fuera de componentes y pistas |
| `cuna_bateria` | Apoya y retiene el pack cerrado, evita movimiento y permite retirarlo | Sujeción sin aplastamiento; salida de cable protegida y acceso al conector antes de extracción |
| `puente_lds` | Recupera relación de la torreta con la base aunque se sustituya el cascarón superior | Interfaz mecánica propia, orientación repetible y espacio para giro/cubierta; los detalles del LDS se conservan si están sanos |
| `portasensores_frontal_y_posterior` | Conserva posición de óptica y contactos; el frontal sigue el movimiento previsto del bumper | Soportes localizados, ventanas despejadas, flex guiado y mantenimiento posible; no fijar el bumper al bastidor anulando su recorrido |

Los clips de arnés y soportes de detectores de rueda forman interfaces con las otras notas mecánicas. Deben poder cambiarse sin retirar la placa si el acceso y la envolvente permiten diseñarlo así. No se promete esa extracción hasta comprobar trayectorias reales.

### Reconstrucción sin fragmentos

1. **Recuperar interfaces en el módulo sano.** Los agujeros de una PCB, la cara de apoyo de una carcasa o la brida de un sensor son datos mejores que imaginar la forma del poste desaparecido. Comprobar que la propia interfaz siga íntegra.
2. **Separar posición funcional y forma de soporte.** La función puede exigir un plano y un eje, pero no el mismo tetón del molde. Un portamódulo atornillable puede establecerlos con otra forma y una base más amplia.
3. **Cruzar referencias.** Los montajes conservados en carcasa superior y paragolpes son evidencia geométrica útil, siempre que no estén deformados. No usar una sola superficie deteriorada como patrón de todo el robot ni completar lados por simetría supuesta.
4. **Crear primero envolventes con incertidumbres explícitas.** Contorno, altura, conectores, servicio y movimientos pueden modelarse antes que todos los detalles. Los parámetros no medidos quedan vacíos o marcados como provisionales; no ocultar un valor supuesto como cota exacta.
5. **Validar plantillas y apoyos antes del traslado completo.** Una plantilla de agujeros o portamódulo permite resolver encaje y acceso sin fabricar toda la base ni cargar plástico roto. No hace falta reparar primero la carcasa vieja.

### Aislamiento, radio y calor

La cubierta translúcida, espumas, arandelas y material blanco observado se conservan y documentan hasta identificar su papel. No está demostrado que toda superficie transparente sea un aislante de especificación conocida. No conectar estructura metálica nueva al negativo de batería o a una supuesta masa por intuición.

El apoyo de las placas no debe flexionarlas al apretar ni durante la pulsación de botones. Si existe un sensor inercial en ellas, ubicación y orientación también pueden influir en navegación; **no se ha identificado una IMU concreta**. Las guías de ST respaldan la sensibilidad de MEMS a esfuerzos de montaje, pero no identifican el componente del Xiaomi [S16].

Tampoco se ha localizado la antena. Hasta resolver la zona que vaya a cambiar, no se puede aprobar encerrar toda la electrónica entre chapas o colocar un travesaño conductor junto a ella. La documentación de Espressif explica el efecto del entorno mecánico en radio, pero **no prueba que haya un ESP32 ni aporta una separación aplicable a este robot** [S17].

El diseño preserva entradas/salidas y elementos térmicos que se identifiquen. Las primeras cargas relevantes requieren observar anomalías térmicas; una base más gruesa o una tapa cerrada puede cambiar el enfriamiento. No se dispone de disipaciones ni temperaturas límite de todos los componentes, por lo que no se propone una tolerancia térmica numérica.

## 6. Medidas pendientes para CAD: propuesta M70–M89

Esta tabla reserva identificadores para coordinar con M40–M69 de mecanismos; **no declara ninguna medida realizada; sus identificadores se han integrado en el CSV del proyecto**. Son grupos de medidas, no veinte cotas ficticias.

| ID propuesto | Medida/observación requerida | Fuente recuperable / utilidad |
|---|---|---|
| M70 | Transformación de MOD002 respecto a datums del robot: posición y orientación | Cuerpo y montajes todavía reconocibles; preservar orientación inicial |
| M71 | Contorno y envolvente superior/inferior de MOD002 con su cubierta | Placa completa; reservar volumen y evitar contacto con componentes |
| M72 | Patrón real de apoyos y alturas de MOD002, con elementos interpuestos | Apoyos sanos y agujeros de PCB; no basta medir centros desde foto |
| M73 | Posición y envolvente de conectores de MOD002, enclavamiento y extracción | Conectores que se vayan a mover; espacio de dedos/herramienta y salida de cable |
| M74 | Pila y patrón de montaje MOD003; alineación y recorrido de botones | F011/F013 y piezas de botón; no cargar la placa a flexión |
| M75 | Posición, apoyos y rutas de los dos ramales MOD004 | F007 y seguimiento físico sin desconectar todo |
| M76 | Envolvente, masa, apoyos y retención de batería | Pack cerrado; cuna dimensionada y reparto de carga |
| M77 | Extracción de batería y recorrido hasta el conector desconectable | Comprobación en seco; no confundir hueco ocupado con espacio de mantenimiento |
| M78 | Plano, patrón, orientación y altura de MOD013 respecto al bastidor | LDS y carcasa superior; soporte nuevo sin reconstruir óptica interna |
| M79 | Envolvente de giro, cubierta, motor y salida de arnés LDS | Conjunto completo y movimiento observado sin forzar |
| M80 | Transformaciones entre MOD010, MOD011 y ventanas frontales/laterales | Paragolpes existente; conservar geometría óptica de conjunto |
| M81 | Ruta del flex frontal, fijaciones, curvaturas y holgura durante movimiento | F014–F016 y posiciones extrema/central del bumper |
| M82 | Montaje posterior de MOD012 y relación con contactos/ventana exterior | F012 más vista exterior; coordinar con medidas de estación de la nota mecánica |
| M83 | Montaje y orientación de cada sensor inferior que se identifique | Ventanas y soportes reales; campo libre respecto al suelo y al nuevo material |
| M84 | Soporte, actuador y salida de arnés de cada detector de rueda | Detalles de ambos lados; coordinar con recorrido y topes de suspensión |
| M85 | Longitudes útiles de arneses y reservas de movimiento por sector | Medición de rutas existentes, sin tensar ni asignar pines por colores |
| M86 | Apoyos térmicos, cubiertas, espumas y uniones conductoras existentes | Registrar función conocida/desconocida; no inventar masas ni retirar elementos |
| M87 | Zona real de radio/antena y elementos nuevos que alterarían su entorno | Lectura no destructiva cuando sea posible; si no, conservar entorno provisional y reservar resolución antes del cierre conductor |
| M88 | Envolvente de soporte y espacio de cable/aire de electrónica local de turbina y motores | Subconjuntos conservados; complementar medidas de conductos, no duplicarlas |
| M89 | Interfaz de bandeja intercambiable y recorrido de servicio desde el bastidor | Decisión CAD tras medir espacio; permite otra controladora sin rediseñar estructura |

**Primera captura adicional útil:** una vista cenital completa del cuerpo inferior con el frontal marcado, detalles laterales de los conectores que queden ocultos y vistas de ambos detectores de rueda. Añadir escala y medidas directas de las interfaces elegidas. No repetir la etiqueta de batería ya legible, ni abrir batería, ópticas, reductoras o blindajes sólo para completar campos.

## 7. Estado real del control abierto

### 7.1 Resultados comprobados

| Proyecto / nivel | Evidencia primaria consultada | Qué ofrece para este objetivo | Qué no queda demostrado |
|---|---|---|---|
| **Valetudo** | Lista oficial exhaustiva sin X20 Pro/D102GL; README y panorama de implementaciones [S01–S03] | Referencia de control local e integración; útil para distinguir nube de control interno | Soporte oficial del Pro, root de esta revisión o sustitución de sus algoritmos. Tener código para otra familia Xiaomi no acredita compatibilidad |
| **hass-xiaomi-miot** | Bloque actual `xiaomi.vacuum.d102gl`; commit específico `76bc9c0…`; incidencia del modelo [S04–S06] | Código abierto de supervisión/órdenes de alto nivel. Puede evitar desarrollar desde cero cierta integración externa si luego funciona en nuestra configuración | Acceso directo a motores, calibración libre, firmware abierto, funcionamiento íntegro sin nube o en esta unidad. Hay testimonios de éxito y de problemas según versión/configuración |
| **Xiaomi Home para Home Assistant** | Repositorio oficial describe MIoT, nube y modos locales condicionados [S07] | Referencia oficial de mensajería de alto nivel y modelo de servicios | No es firmware del robot. El modo local de una integración no equivale a control de bajo nivel abierto ni valida todas las funciones exactas del Pro |
| **Tasshack/dreame-vacuum** | Petición exacta #862 cerrada por el mantenedor, que identifica D102GL como no Dreame [S08] | Evidencia para descartar la transferencia automática del soporte del X20+ | No autoriza aplicar controladores, adaptadores o procedimientos de root Dreame al Pro. No se usa este comentario como identificación completa del fabricante de todas sus piezas |
| **VacuumTiger / SangamIO** | Estado del proyecto: controlador CRL-200S verificado, GD32 y Delta-2D; otras plataformas previstas [S14] | Arquitectura reutilizable de separación entre hardware, datos y navegación; existe código real | Driver X20 Pro, equivalencia de su LDS, acceso al firmware de la placa o compatibilidad directa |
| **ROS2 bridge de remakeai** | README actual exige SangamIO y describe parámetros publicados por drivers CRL-200S y Roborock S5 Max [S15] | Integración ROS2 de plataformas para las que ya existe la capa de hardware; convención útil para separar geometría del controlador | Driver X20 Pro o conversión automática de sus motores/sensores desconocidos en dispositivos ROS por instalar el puente |

La lectura directa del archivo actual de `hass-xiaomi-miot` confirmó acciones como inicio de barrido/fregado, pausa, lavado de mopas, vaciado, secado y vuelta a carga. Son **operaciones coordinadas del aparato**: no se deben tratar como ensayos independientes de un motor. No se ha ejecutado ninguna.

La página de Valetudo distingue además entre una implementación presente en código y un robot con procedimiento realmente disponible. No basta hallar una clase genérica, una batería P2150 o un nombre Xiaomi similar. **P2150 en una lista de robots y P2150 en el nombre de un pack no demuestran identidad de plataforma.** [S03; P: F001]

### 7.2 Límites de la búsqueda

En las fuentes consultadas no se ha localizado un esquema completo de B108EU_MB, un pinout validado de todos sus conectores, una liberación reproducible del firmware completo del D102GL ni un controlador abierto listo para sus módulos. Esto describe el resultado de la investigación; no demuestra que su desarrollo sea imposible.

La base del investigador enlazada por Valetudo, `robotinfo.dev`, no pudo verificarse: devolvió timeout en el buscador y HTTP 503 en una petición pública directa. No se usa esa indisponibilidad para afirmar ausencia de root. Tampoco se trasladan al Xiaomi resultados del **Dreame X20 Pro**, que es un nombre comercial distinto.

## 8. Transición propuesta: abrir sin perder la base construida

### Etapa A — Base y montajes abiertos, control original provisional

Construir referencias mecánicas, soporte de rueda piloto, bandejas y alojamientos con el inventario real. Mantener módulos y conexiones intactos siempre que su estado lo permita. Esto permite separar errores de geometría de una futura reescritura de control. El resultado publicable son CAD editable, parámetros medidos, interfaces, montaje y evidencias; **no se etiqueta todavía como robot de control abierto**.

### Etapa B — Supervisión externa y mapa de dependencias

Después de recuperar un montaje apto, evaluar únicamente las órdenes y estados que aporten una utilidad concreta para ensayos y operación. El soporte exacto `hass-xiaomi-miot` es un candidato documental, no una instalación ya aprobada o probada. Registrar por función: interfaz, versión, dependencia de nube, datos accesibles y limitaciones.

Esta etapa tampoco debe convertirse en un callejón sin salida: enviar órdenes a firmware cerrado no satisface por sí solo el objetivo final. El acceso root, si llegara a verificarse, daría permisos de administración; **no otorgaría automáticamente código fuente, documentación de circuitos ni licencias abiertas**.

### Etapa C — Control principal abierto y sustituciones localizadas

Elegir con datos entre dos rutas:

- **Reutilizar la placa principal con software propio**, sólo si se demuestra un arranque/desarrollo reproducible, acceso al hardware necesario, posibilidad de recuperación y un coste razonable. Hoy faltan esos datos para el Pro.
- **Sustituir la controladora principal y, donde haga falta, la electrónica de interfaz**, conservando los módulos cuyo control se pueda documentar. Esta ruta evita depender de un root futuro, pero exige caracterización de sensores, actuadores, carga, protecciones y sincronización. No implica abrir el pack ni improvisar un cargador.

La selección no exige conocer hoy cada pin. Sí exige reservar en CAD una bandeja sustituible, acceso a conectores y pasos de arnés. La ingeniería eléctrica posterior debe resolver por módulo alimentación, polaridad, corriente pertinente, referencia, interfaz, comportamiento ante fallo y prueba mínima. Se documenta antes de conectar un adaptador.

El software propio debe abarcar no sólo navegación sino parada y límites de movimiento, reacción a sensores y estados, control de accionamientos, carga y coordinación de limpieza. Se puede reutilizar software abierto ya existente donde haya interfaces compatibles; no se declara que ROS, SLAM o VacuumTiger resuelvan automáticamente la electrónica desconocida.

### Etapa D — Cerrar dependencias todavía opacas

Mantener una lista separada de firmware de módulos, control de carga, sensores inteligentes y estación que sigan cerrados. Para cada dependencia, registrar si basta una interfaz documentada para repararla/sustituirla o si se necesita otro componente. **Conservar la estación al principio no la convierte en abierta.** La apertura del control del robot y la del sistema completo con estación son hitos distintos y deben quedar visibles en el objetivo del proyecto.

No se impone rediseñar ahora la electrónica conectada a red de la estación. La primera base tiene que mantener sus interfaces físicas; abrir la coordinación de servicios será una investigación posterior, con función y alcance concretos.

## 9. Pruebas y coste: puertas de paso

- **Antes del traslado:** correspondencia de montajes y conectores afectados, estado mecánico del módulo, apoyos, aislamiento observado, arnés sin tracción y trayectoria de mantenimiento. No es necesario llenar todos los pines para modelar una cuna.
- **Antes de alimentar:** montaje retenido y apto para todos los conjuntos que el comando pueda activar; parejas de conectores comprobadas; sin cables/placas colgando. El robot viejo roto no se usa como requisito de línea base si no puede sostenerse.
- **Con la primera función:** registrar comando, componentes implicados, condiciones, resultado y anomalías. No convertir ausencia de error en la app en validación de temperatura, navegación, anticaída o durabilidad.
- **Antes de un cambio de control:** una interfaz concreta ya comprendida, equipo adecuado a los niveles conocidos y posibilidad de detener/recuperar el ensayo. KiCad o PulseView sólo entran cuando resuelven esa pregunta; no descubren un pinout desde una foto.
- **Antes de fabricar una base completa:** plantillas o portamódulos críticos comprobados, presupuesto y proceso. No comprar SBC, controladora, escáner o instrumentos avanzados por anticipado.

El inventario y CAD preliminar pueden avanzar ya. Las incertidumbres sobre firmware y pines no justifican detenerlos, pero tampoco se ocultan prometiendo compatibilidad eléctrica futura. La estructura debe permitir corregir o reemplazar un soporte y una controladora sin semanas de despiece del resto.

## 10. Cambios necesarios respecto a 07 / 09 / 10

1. **07:** mantener su secuencia y controles de montaje; actualizar el objetivo de firmware original como provisional e incorporar la ruta de control abierto. La frase que deja ROS/firmware nuevo fuera de la primera versión sigue siendo válida si se explicita la siguiente etapa.
2. **09:** OOMWOO queda referencia de piezas y arquitectura, no carcasa donante seleccionada. Su controladora y sensores previstos no prueban compatibilidad eléctrica con Pro. El hecho de poder cambiar después la placa no elimina hoy las interfaces de ruedas, óptica, limpieza y estación.
3. **10 y CSV:** conservar observaciones ya correctas y estados no comprobados. Añadir sólo medidas/relaciones realmente obtenidas. No ascender la inferencia D102…→D102_BIR, ni WIFI_LED→antena, ni CamSub→RGB.
4. **GitHub:** publicar documentación y CAD propios con procedencia y revisiones. Las fotos privadas se referencian por ID y permanecen fuera. No guardar logs con tokens o identificadores personales si se investiga integración en una fase posterior.

## Fuentes consultadas y alcance

Todas las fuentes web siguientes se consultaron o se revisaron junto con la auditoría previa el **2026-10-25**. Los enlaces de código en rama son cambiantes; el commit indicado permite recuperar un antecedente fijo. Las fotografías son evidencia privada de la unidad y no se redistribuyen aquí.

- **S01 — Valetudo, lista oficial de robots soportados.** https://valetudo.cloud/pages/general/supported-robots/ — lista declarada exhaustiva; X20 Pro no aparece.
- **S02 — Valetudo, README del proyecto.** https://github.com/Hypfer/Valetudo — sustitución de nube, no firmware propio.
- **S03 — Valetudo, panorama de implementaciones.** https://valetudo.cloud/pages/usage/implementation-overview/ — distingue implementación de soporte instalable.
- **S04 — hass-xiaomi-miot, código actual de configuración por modelo.** https://github.com/al-one/hass-xiaomi-miot/blob/master/custom_components/xiaomi_miot/core/device_customizes.py — lectura pública directa del archivo bruto, bloque `xiaomi.vacuum.d102gl`, líneas 2639–2656 de la versión leída. La vista indexada no mostró el bloque; se verificó la respuesta raw de 172.644 bytes.
- **S05 — Commit específico D102GL.** https://github.com/al-one/hass-xiaomi-miot/commit/76bc9c0edc27a1405b89969ad56852f3b919db36 — cambios específicos de consultas del modelo.
- **S06 — Incidencia exacta de soporte y testimonios.** https://github.com/al-one/hass-xiaomi-miot/issues/2612 — éxito y problemas reportados según versión/configuración.
- **S07 — Xiaomi, integración oficial Home Assistant.** https://github.com/XiaoMi/ha_xiaomi_home — arquitectura MIoT/nube y condiciones del control local; no firmware del robot.
- **S08 — Tasshack, petición exacta X20 Pro.** https://github.com/Tasshack/dreame-vacuum/issues/862 — respuesta del mantenedor sobre D102GL y cierre.
- **S09 — Xiaomi, FAQ exacta del X20 Pro.** https://www.mi.com/global/support/faq/details/KA-445208/ — LDS, óptica frontal/lateral, desnivel, ultrasonidos, mandos, modos y automatismos. Manual europeo Xiaomi: https://d.otto.de/files/7208679f-5a7d-56d4-b534-937139397f71.pdf ; es manual de usuario, no de servicio.
- **S10 — Recambio de placa principal Pro.** https://www.ep-mediastore-ab.de/xiaomi-x20-pro-mainboard-b108eumb-p-40091.html — vendedor identifica B108EU_MB; la foto F013 confirma el texto en la unidad. La página advierte que la imagen puede diferir; no se obtuvo de ella un plano de apoyos.
- **S11 — Recambio de turbina.** https://www.ep-mediastore-ab.de/saugmotor-hjd-ra60405-xiaomi-s20-x20pro-p-72817.html — referencia comercial corroborada por F002.
- **S12 — Contactos e IR posterior Pro.** https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html — conjunto y compatibilidad declarados por vendedor; no lectura completa en F012.
- **S13 — Pack compatible y advertencia de conectores.** https://www.ep-mediastore-ab.de/xiaomi-akku-5200mah-p2150-4s2p-scev-fuer-s20-x20-max-pro-original-p-56237.html — no sustituye comprobación de pareja y polaridad. F001 identifica el pack real.
- **S14 — VacuumTiger.** https://github.com/codetiger/VacuumTiger — CRL-200S/GD32/Delta-2D y capas de software; no driver Pro acreditado.
- **S15 — Puente ROS2.** https://github.com/remakeai/vacuum_ros2_bridge — README actual leído; exige SangamIO y explica parámetros de CRL-200S y S5 Max, sin acreditar soporte Pro.
- **S16 — ST, TN1383.** https://www.st.com/resource/en/technical_note/tn1383-pcb-design-guidelines-for-mems-sensors-stmicroelectronics.pdf — principio de esfuerzos de montaje sobre MEMS; no identifica una IMU Xiaomi.
- **S17 — Espressif, entorno de placa/antena.** https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/pcb-layout-design.html — principio general de integración; no prueba chip ni separaciones del Pro.

**Resultado entregado:** mapa de montaje y medidas pendientes, evidencia exacta frente a inferencias y ruta a control abierto. No es un esquema eléctrico, un diseño dimensionado listo para fabricar ni una validación física del trasplante.


---
Documentación original de este proyecto: CERN-OHL-P-2.0. Alcance y exclusiones en [cad/LICENCIAS.md](cad/LICENCIAS.md). Las fuentes y diseños de terceros conservan sus derechos.
