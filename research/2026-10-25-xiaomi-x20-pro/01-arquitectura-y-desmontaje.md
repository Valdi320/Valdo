# Xiaomi Robot Vacuum X20 Pro D102GL: arquitectura física y acceso para reparación

Fecha de revisión: 2026-10-25. Alcance: conservar electrónica, firmware, sensores, actuadores e interfaces originales; preparar reparaciones y soportes sustituibles con la menor indisponibilidad posible. Este documento no es un manual de servicio del fabricante ni un plano de fabricación validado.

## 1. Conclusiones que condicionan el proyecto

1. El conjunto de referencia es **robot D102GL + estación D102-JZEU**. Xiaomi publica 350 mm de diámetro, 97 mm de altura, alimentación nominal del robot de 14,4 V y carga a 19,6 V. Son dimensiones exteriores y valores de identificación, no cotas de los soportes. [F01]
2. La electrónica original impone conservar posiciones relativas y recorridos. Cambiar únicamente la estructura evita desarrollar controladores, pero obliga a mantener la geometría que relaciona ruedas, sensores, cepillos, mopas y estación. Esta es una conclusión de ingeniería, no una especificación publicada por Xiaomi. **E4**.
3. Hay recambios comercializados específicamente para el Pro: ruedas izquierda/derecha, pasador, muelle, motores de mopa, aspiración, placa principal y conjunto trasero de contactos con infrarrojos. Permiten identificar módulos; la compatibilidad declarada por una tienda no sustituye la comparación del componente recibido. [F06–F14]
4. **No se ha localizado un plano dimensional OEM, despiece oficial de servicio, mapa completo de tornillos ni procedimiento oficial de sustitución de las ruedas motrices.** El manual público describe mantenimiento ordinario. Los vídeos útiles de acceso interno son de modelos relacionados. No se deducen tornillos ocultos, diámetros de agujeros ni materiales a partir de su parecido.
5. Para intervenir una rueda, no hay evidencia que imponga extraer de antemano placa principal, aspirador y motores de mopa. La estrategia es acceso selectivo al lado afectado, retirando sólo una obstrucción comprobada. La demostración completa de extracción procede de modelos relacionados; no equivale a una secuencia exacta garantizada para cada revisión del Pro. [V01–V03]
6. Antes de encargar un módulo debe distinguirse **carcasa móvil de rueda**, **apoyo fijo del chasis**, **gancho de muelle** y **retención del pasador**. Un módulo nuevo no repara un apoyo roto perteneciente al chasis. **E4**.

## 2. Escala de evidencia

| Código | Significado | Qué permite afirmar | Qué no permite afirmar |
|---|---|---|---|
| **E1** | Fuente oficial exacta del X20 Pro: Xiaomi o manual de Xiaomi identificado | Identidad, funciones, componentes señalados y mantenimiento publicado | Geometría oculta o procedimiento de servicio no publicado |
| **E2** | Vendedor de un recambio con compatibilidad explícita X20 Pro | Existencia comercial declarada, aspecto y datos de esa ficha | Tolerancias OEM, equivalencia de revisiones, autenticidad independiente o ajuste de una pieza genérica |
| **E3a** | Observación audiovisual primaria de un modelo relacionado | Lo que se ve hacer en ese modelo, con marca temporal | Que todos los tornillos, sensores y pasos sean iguales en D102GL |
| **E4** | Inferencia o propuesta de ingeniería | Hipótesis de diseño y comprobaciones necesarias | Resultado ensayado, resistencia garantizada o cota medida |

Una observación visual más nítida no convierte E3a en E1. El mismo módulo de rueda en dos modelos tampoco demuestra que ambos chasis, placas o circuitos de agua sean idénticos.

### Hechos y límites principales

| Hecho | Evidencia | Consecuencia para el diseño |
|---|---|---|
| Dos ruedas principales, rueda libre, cepillo principal/lateral y dos alojamientos de mopa | E1, dibujo del manual [F04] | Levantar un sistema de coordenadas común para todos los apoyos |
| Sensores LDS, láser frontal, desnivel y ultrasonidos; estación con zona de señalización | E1 [F02–F04] | Preservar ventanas, orientación y campo de visión |
| Contactos traseros y sensor IR se venden juntos con soporte para Pro | E2 [F13] | Conservar el conjunto como una unidad geométrica |
| Ruedas L/R y pasadores vendidos para Pro y Max | E2 [F07–F09] | Comparar componentes, sin asumir intercambio del cuerpo completo |
| Muelle vendido para Pro, dimensiones anunciadas 6,2 × 32/45 mm | E2 [F10] | La ficha no aporta rigidez ni pretensión; no basta para elegir un muelle equivalente |
| M30 y Max permiten acceso superior a la zona de suspensión | E3a [V01–V02] | Preparar acceso por carcasas, no arrancar el gran fondo negro |
| No se ha confirmado depósito interno de agua del Pro | Evidencia insuficiente | No copiar el circuito del Max ni diseñar un puerto de llenado supuesto |

## 3. Inventario funcional del robot

La columna de conservación y las necesidades de medida son propuestas **E4**. Los códigos de tienda son SKU del vendedor; no se presentan como referencias OEM verificadas. Se omiten precios y existencias porque cambian.

| Subsistema | Identificación documental | Unidad que interesa conservar | Interfaz física que documentar |
|---|---|---|---|
| Bastidor inferior y carcasa superior | Exterior E1; organización interna análoga E3a | Bastidor sano y envolvente original durante las primeras etapas | Planos de apoyo, uniones, nervios, accesos y holguras |
| Rueda motriz izquierda | E2, SKU 12585 [F07] | Rueda, reductora, motor, placa y cable como conjunto | Pivote, topes, muelle, alojamiento y ruta del cable |
| Rueda motriz derecha | E2, SKU 13025 [F08] | Igual criterio; no confundir lateralidad | Medir cada lado; no asumir simetría perfecta |
| Pasador de suspensión | E2, SKU 12584, anunciado 4 × 38,5 mm [F09] | Pasador sano y retención original | Diámetro real, rectitud, longitud útil, apoyos y libertad axial |
| Muelle de suspensión | E2, SKU 37935 [F10] | Muelle de referencia correcto y ambos anclajes | Longitudes libre/montada, ganchos, dirección de tiro y recorrido |
| Detección de rueda extendida/levantada | E3a, microswitch observado en M30/Max [V01–V02] | Interruptor, soporte y accionamiento, si la unidad confirma esa disposición | Punto de actuación y recuperación; fijación exacta por verificar |
| Rueda libre delantera | E1 [F03–F04] | Rueda y soporte giratorio | Altura cargada, posición, libertad de orientación |
| Cepillo principal | E1 [F04]; conjunto motorizado en catálogo E2 [F06] | Rodillo, caja, transmisión, tapa y juntas | Apoyo del rodillo, contacto con suelo y conducto al depósito |
| Cepillo lateral | E1 [F03–F04]; motor en catálogo E2 [F06] | Motor/reductora y acoplamiento | Altura, radio barrido y espacio respecto a rueda/bumper |
| Aspiración del robot | E2, SKU 72817 [F12] | Turbina completa, carcasa, juntas y cableado | Sellado de entrada/salida, fijaciones y espacio de ventilación |
| Depósito y filtro | E1 [F04] | Depósito, cierres, filtro y sellos | Acoplamiento a succión y bocas de vaciado |
| Mopas giratorias | E1 [F02–F04]; motores L/R con detección de plato E2 [F11] | Motores, reductoras, platos y detección originales | Separación de ejes, altura, montaje y zona barrida |
| Elevación de mopas | E1: elevación anunciada hasta 10 mm [F02] | Mecanismo original completo | Cinemática, topes y holgura; no se ha aislado su despiece interno exacto |
| LDS superior | E1 [F04] | Sensor, montaje y cubierta con su mecanismo original | Posición, nivelación, giro y libertad de cubierta |
| Óptica frontal/lateral y bumper | E1 [F02–F04]; cableado análogo E3a [V01] | Óptica en sus soportes, ventanas y bumper completo | Campo de visión, separación, recorrido, retorno y flex |
| Sensores inferiores | E1 [F03–F04] | Módulos con sus ventanas y orientación | Altura y ángulo respecto al suelo, ausencia de obstáculos nuevos |
| Carga y acoplamiento trasero | E2, SKU 28885 [F13] | Contactos, IR y soporte original conjunto | Coordenadas, orientación, accesibilidad y presión de contacto |
| Placa principal | E2, SKU 40091 [F14] | Placa de la propia unidad y todos sus conectores | Fijación, distancias libres, aislantes y refrigeración |
| Batería | E1 [F01]; recambio específico en catálogo E2 [F06] | Pack cerrado original compatible, protección y conexión | Envolvente, sujeción sin aplastamiento y salida del cable |
| Mandos, indicadores y señal acústica | E1 [F04]; placas auxiliares/altavoz en catálogo E2 [F06] | Componentes y mazos originales | Posición de botones, pasos y radios de curvatura |

**No se dispone de pinout validado para D102GL**, mapa de conectores, revisión completa de placas, material de cada pieza ni parámetros de calibración. No se trasladan los pinouts de Xiaomi 1T, M30 o un robot ROS al Pro. Mantener conectores y mazos originales evita convertir una reparación física en un proyecto electrónico.

Algunas fichas comerciales llaman «cámara» al conjunto óptico frontal. La descripción oficial habla de luz estructurada/láser para obstáculos; este informe no lo identifica como cámara RGB ni presupone funciones de vídeo. [F02, F06]

## 4. Estación y acoplamientos que el chasis debe respetar

### 4.1 Inventario funcional

| Bloque de estación | Evidencia exacta | Decisión para este proyecto |
|---|---|---|
| Alimentación y carga | E1, D102-JZEU, salida 19,6 V / 1,2 A [F01] | Conservar estación y sistema de carga originales |
| Rampa, bandeja de lavado y apoyo | E1 [F04] | Usarlas como útiles físicos de comprobación, sin modificarlas inicialmente |
| Depósitos limpio/sucio | E1, 4 l / 3,8 l [F02] | Conservar tapas, flotadores, juntas y conexiones |
| Aspiración para vaciado y bolsa | E1 [F02–F04]; turbina en catálogo E2 [F06] | Conservar conductos y superficies de sellado |
| Lavado y evacuación de agua | E1 [F03]; bombas y tubos comercializados E2 [F06] | No deducir el circuito hidráulico completo por nombres de recambio |
| Secado de mopas | E1 [F02]; ventilador/calefactor en catálogo E2 [F06] | Mantener paso del aire, separación y materiales originales de esa zona |
| IR de guiado | E2, SKU 26830 [F15] | Preservar la zona de señalización y su pareja en el robot |
| Detección de depósitos, bandeja y bolsa; electrónica de estación | E2, catálogo específico [F06] | Conservar estos conjuntos; no requieren desmontaje para reforzar una rueda |

Los manuales describen lavado/mojado de mopas en la bandeja. Los dibujos consultados no identifican un puerto de carga de agua en el robot. Esto **no demuestra por sí solo la ausencia de cualquier depósito oculto**, pero impide presentar como hecho un depósito interno de 80 ml basándose en una ficha comercial contradictoria. El Max tiene diferencias documentadas de módulos; su circuito no se transfiere al Pro. [F04, F06]

### 4.2 Matriz de interfaces críticas — requisitos de conservación E4

| Interfaz | Geometría que mantener | Resultado que comprobar |
|---|---|---|
| Suelo → ruedas → rampa | Altura inferior, distancia entre ruedas, posiciones de apoyo, recorrido de suspensión y reparto de carga | Sube y baja sin patinar, arrastrar el fondo ni perder apoyo |
| Robot → contactos de estación | Altura, separación, orientación y posición trasera del conjunto | Carga estable al terminar el acoplamiento |
| IR robot ↔ estación | Ventanas libres y orientación del conjunto original | Aproximación y alineación repetibles |
| Vaciado → boca del robot | Posición, sección, plano y compresión de juntas | Acoplamiento sellado y evacuación normal de polvo |
| Mopas → bandeja | Separación de ejes, altura y recorrido vertical, diámetro efectivo y espacio libre | Platos giran y se lavan sin tocar elementos ajenos |
| Secado → zona de mopas | Trayecto libre del aire, huecos y separaciones | Secado sin bloquear salidas ni aproximar piezas nuevas al calentamiento |
| Bumper/contorno → estación | Envolvente, libertad del bumper y salientes | No aparece un choque artificial durante aproximación o retirada |

## 5. Desmontaje: qué se ha visto y qué sigue sin probarse

### 5.1 Registro audiovisual, modelos relacionados (E3a)

| Fuente y tiempo | Observación directa |
|---|---|
| M30, 00:20–00:28 | Retira embellecedor superior a presillas |
| M30, 00:32–01:00 | Cuatro tornillos plateados corresponden a bisagras/tapa abatible; retira tapa y depósito |
| M30, 02:25–03:15 | Acceso inferior y retirada de batería |
| M30, 03:20–04:10 | Libera retenedor de bumper y su cable flexible |
| M30, 04:15–05:10 | Tornillos inferiores unen cuerpo superior y base; levanta carcasa |
| M30, 12:20–12:55 | Expulsa pasadores desde el interior hacia el perímetro |
| M30, 13:00–13:40 | Desengancha muelles, libera microswitch a presión y extrae ruedas |
| M30, 17:50–19:05 | Reintroduce pasador desde fuera; repone interruptor, guía cables y comprueba retorno |
| X20 Max, 01:37–01:40 | Muelle e interruptor accesibles con placa/aspirador instalados; no extrae la rueda |
| Mijia 2, 02:25–02:39 | Extrae una rueda conservando placa y aspirador; fijación del interruptor distinta |

Fuentes [V01–V03]. El M30 realiza un despiece completo: sus retiradas intermedias no prueban que sean necesarias para una sola rueda. No se extrapola al Pro el número de tornillos de microswitch del Mijia 2.

### 5.2 Plan de acceso condicionado para D102GL — propuesta E4

| Nivel | Objetivo concreto | Límite de intervención |
|---|---|---|
| 0. Robot cerrado | Registrar dimensiones exteriores, alturas, movimiento de ruedas y acoplamiento | No retirar piezas internas para obtener datos que pueden medirse fuera |
| 1. Acceso de mantenimiento | Quitar consumibles que impidan inspección y limpiar la zona | El manual describe extracción de cepillo lateral, rodillo, rueda libre y platos según su sistema [F03–F04] |
| 2. Acceso eléctrico seguro | Apagar fuera de estación, abrir tapa de acceso pertinente y desconectar batería por su conector | No abrir el pack, alterar cargador o hacer funcionar el aparato abierto |
| 3. Carcasa superior | Acceder al apoyo o conector que se necesita medir/reparar | Usar el vídeo como orientación; localizar cada unión real, sin forzar porque un vídeo tenga menos tornillos |
| 4. Lado afectado | Liberar cable, retención del pivote, muelle e interruptor que realmente impidan sacar ese módulo | Una rueda cada vez; conservar el otro lado como referencia sólo cuando sea comparable |
| 5. Trasplante de bastidor | Transferir conjuntos a una estructura preparada | Reservarlo para una pieza ya fabricada y verificada; no empezar con un despiece total exploratorio |

En nivel 3, distinguir embellecedor, tapa abatible, carcasa estructural y bumper. Soltar una tapa de bisagras no demuestra que el resto del cuerpo esté libre. El cable flexible del bumper y sus retenedores deben localizarse antes de separar piezas. No se ha probado que sea imprescindible extraer el LDS para reparar la rueda; no se prescribe su retirada preventiva.

En nivel 4, **no tirar del módulo con muelle o cable aún sujetos**, ni usar el interruptor como asa. Si el pasador no sale con una maniobra controlada, identificar retención, deformación o apoyo cargado antes de insistir. No trasladar a ciegas la dirección del M30 a una revisión cuya retención aún no se ha visto. No hay instrucción de martillear, taladrar o cortar un apoyo sin identificarlo.

### 5.3 Cuándo abrir y cuándo posponer

Abrir sólo cuando exista un resultado de esa sesión: una lista breve de cotas que no pueden tomarse desde fuera, una pieza lista para comparar o una reparación preparada. Tener identificados útiles, conexiones que se tocarán, orden de montaje y posibilidad de volver al estado anterior. Si falta el recambio, la pieza impresa o el diseño del refuerzo, obtener primero lo que pueda resolverse sin dejar el robot desarmado.

No es necesario desmontar la estación para estudiar la suspensión del robot. Las interfaces se pueden medir desde sus superficies accesibles. Este alcance excluye intervenir en sus partes conectadas a la red y en el interior del pack de batería.

## 6. Levantamiento dimensional antes de fabricar — todos pendientes

**No se establecen tolerancias numéricas aún.** La precisión necesaria depende de la función, el método de fabricación y lo que se mida en piezas sanas. Una dimensión de catálogo del pasador no es la dimensión de taladro, ni una holgura apropiada para impresión.

Definir un marco reproducible: X hacia el bumper delantero, Y hacia la izquierda del robot en posición normal, Z hacia arriba. Elegir un plano A sobre apoyos estructurales sanos y un plano B de simetría; definir una tercera referencia estable sin usar una orejeta deformada. Documentar cómo se apoya el robot al medir y si las ruedas están descargadas o soportan peso.

| Grupo | Magnitudes pendientes | Cómo obtener una referencia útil | Qué se controla |
|---|---|---|---|
| Daño | Qué pieza ha roto, extensión de grieta, material restante y posible deformación | Inspección de ambas caras y comparación con zona sana | Que el refuerzo cargue sobre material competente |
| Pasador | Diámetro real, longitud, extremos, ranuras y rectitud | Medición directa fuera sólo cuando la extracción esté justificada | Ajuste y retención, sin inventar un taladro |
| Apoyos | Separación, coaxialidad, anchura de apoyo y espesor de base | Referencias rígidas y eje de comprobación adecuado | Evitar que un soporte nuevo tuerza el pivote |
| Pivote → rueda | Distancia entre ejes y orientación | Medir módulo completo, sin abrir reductora | Conservar brazo y recorrido originales |
| Ruedas | Diámetro efectivo, anchura y distancia entre planos medios | Mismo estado de carga en mediciones comparativas | Desplazamiento por vuelta, giro y entrada en estación |
| Suspensión | Posición descargada, posición apoyada y topes | Recorrido manual con batería desconectada | Ningún punto duro o contacto nuevo |
| Juego | Libertad axial y radial funcional en conjunto sano | Registrar método; no confundir flexión de carcasa con holgura | Giro libre y conservación de alineación |
| Muelles | Longitud libre, montada y en extremos; ganchos y anclajes | Muelle correcto y posiciones originales | Precarga y palanca; no elegir por longitud solamente |
| Detección de rueda | Posiciones de actuación/retorno del mecanismo | Observación mecánica; comprobación funcional posterior montado | Evitar falsos avisos o detección anulada |
| Cables móviles | Recorrido completo, anclajes y reserva de longitud | Observar en ambos extremos de suspensión | No tirar del conector ni rozar neumático/pasador |
| Tornillos existentes | Posición, longitud, cabeza, asiento y pieza de destino | Mapa propio durante desmontaje, conservando separación | No atravesar carcasa ni tocar batería/placa |
| Rueda libre | Posición y altura respecto al plano de suelo | Estado apoyado equivalente | Reparto de carga y estabilidad |
| Cepillos | Altura, radios barridos y planos del conducto | Conservar módulos montados de referencia | No degradar recogida ni sellado |
| Mopa | Coordenadas de ejes, plano de trabajo, elevación y paso libre | Platos originales y bandeja de estación | Fregado, elevación y lavado compatibles |
| Sensores | Coordenadas, orientación y contorno de ventana | Conservar soportes originales como referencias | No alterar visión del suelo/obstáculos |
| Bumper/LDS | Recorrido, retorno y espacios en todo el movimiento | Mecanismos completos de referencia | No inmovilizar detección de contacto |
| Acoplamiento | Contactos, IR, bocas y caras de sello respecto a los apoyos | Robot y estación originales como pareja | Carga, guiado y vaciado |
| Masas | Masa y ubicación de los módulos; altura cargada | Pesada y anotación de posiciones, sin usar cifras comerciales como medida real | Evitar sobrecargar un apoyo o perder tracción |
| Cubiertas | Altura final, envolvente y accesibilidad de herramientas | Plantillas y prueba de cierre antes de energizar | Ninguna colisión ni desmontaje innecesario futuro |

## 7. Tres rutas físicas compatibles con mantener la electrónica

### Ruta A: recuperar disponibilidad con intervención localizada

Identificar el apoyo dañado y restaurar su función manteniendo el módulo, posición de pivote, muelle e interruptor. Si sólo falla el módulo desmontable, sustituir esa pieza puede ser más predecible que reconstruir su alojamiento. Si falla el chasis, estudiar un refuerzo fijado a zona sana; no comprar una rueda esperando reparar una orejeta fija.

Antes de abrir: repuesto o refuerzo concreto disponible, comprobación de que no cruza una articulación y plan de remontaje. Resultado: robot utilizable y daño documentado con cotas. No constituye validación de vida útil de un arreglo provisional. **E4**.

### Ruta B: soporte reemplazable de acceso sencillo

Diseñar un portapivote o subestructura local cuya sustitución futura no requiera retirar placa, aspirador o todo el fondo. Conservar los conjuntos originales y llevar la carga a una zona amplia y sana. Preparar piezas y plantilla de posicionamiento fuera del aparato; realizar una única sesión de adaptación y comprobación.

El diseño debe permitir retirar pasador, desenganchar muelle y alcanzar el conector sin invadir el movimiento de la rueda. La independencia de mantenimiento se consigue con accesos y uniones desmontables, no aumentando arbitrariamente la rigidez de todo el robot. **E4**.

### Ruta C: bastidor modular con control dimensional

Usar las medidas validadas para definir interfaces de módulos atornillables y conservar inicialmente la envolvente, sensores, conductos, batería y conjunto trasero originales. Preparar primero el bastidor y comprobar en seco posición de módulos, articulaciones, cierre y acoplamiento. Transferir la electrónica sólo después, con posibilidad de volver al chasis anterior si sigue siendo recuperable.

Un escaneo sirve como referencia de superficies, pero los alojamientos del pasador, planos de apoyo, sellos y distancias funcionales requieren medición directa. «Modelo 3D que se parece» y «pieza dimensionalmente intercambiable» son resultados distintos. **E4**.

## 8. Riesgos mecánicos del refuerzo y criterios de aceptación

### 8.1 Qué no resolvería un soporte más rígido

- Un collar puede impedir que una grieta se abra, mientras el plástico original sigue recibiendo la carga. Un puente o casquillo puede cambiar el camino de carga hacia una base sana; necesita espacio, fijación y alineación comprobados.
- Un refuerzo corto o fijado junto al borde roto puede trasladar la rotura al chasis o al siguiente apoyo. Aumentar la sección de una orejeta sin revisar su base no garantiza una mejora del conjunto.
- Apretar el pasador o desalinear sus apoyos puede bloquear la suspensión. Los impactos y esfuerzos se transmiten entonces a otros apoyos y pueden perjudicar tracción, acoplamiento y detección.
- Una brida que una la rueda basculante al chasis actúa como un tope o amarre. Sólo puede estudiarse como contención de una pieza del mismo cuerpo, sin sustituir asiento, muelle o articulación.
- Un anclaje de muelle desplazado cambia la longitud de trabajo y su brazo de palanca. Un muelle «más fuerte» no es una mejora automática.
- Adhesivo curado no implica asiento rígido y coaxial; tampoco reconstituye por sí solo la resistencia a cargas repetidas. La compatibilidad del adhesivo depende del material aún no identificado.

Todos estos puntos son **E4**, razonamiento de diseño; no se atribuyen intenciones al fabricante ni se promete superar la vida útil original.

### 8.2 Verificación mínima proporcional a la reparación

1. **Antes de cerrar y sin batería:** pasador retenido; giro de rueda y basculación libres; retorno por muelle; mecanismo de detección libre; cables y ópticas sin interferencias. Comparar movimiento antes/después y con referencia sana cuando sea válida.
2. **Montado:** comprobar desplazamiento y giro, ausencia de avisos nuevos y recorrido por la zona de uso habitual. No cambiar varios parámetros a la vez si aparece un fallo.
3. **Con la estación original:** comprobar entrada/salida, carga, vaciado, elevación y lavado de mopas. Registrar qué funciones se han probado, no declarar «totalmente validado» por una sola vuelta.
4. **Tras uso representativo:** inspeccionar si aparecen holgura, marcas de roce, apertura de grieta, desplazamiento o aflojamiento. La duración de esa observación es un dato a registrar, no una garantía de fatiga.

## 9. Incertidumbres y exclusiones de transferencia

- **X20+ no es X20 Pro.** Un anuncio genérico de «X20» no demuestra compatibilidad.
- **X20 Max comparte algunos recambios, no todas las funciones.** Su sistema de agua, mopa extensible, carcasa o placa no se transfieren por parecido.
- La serigrafía de placa comercializada como B108EU_MB no demuestra firmware, revisión ni configuración intercambiables. Este proyecto conserva la placa de la unidad. [F14]
- La ficha de un vendedor puede contener texto genérico: por ejemplo «aspirar agua sucia del robot» no prueba un depósito de agua sucia interno. Las recomendaciones se basan en la función y las interfaces identificadas, no en esa frase.
- El manual europeo consultado indica 3,6 kg y la web española actual 3,7 kg para el robot. No se usa ninguna de ambas cifras para calcular cargas del refuerzo; se mide la unidad. [F01, F04]
- No se ha identificado con certeza el polímero de las orejetas, orientación de fibra, pretensión de muelle, tolerancias de pivote ni resistencia a fatiga. No se prescribe material de impresión, adhesivo, par de apriete o diámetro de perforación como si fueran especificaciones de fábrica.
- Los esquemas del manual son ilustrativos. No se toman medidas a escala de sus dibujos ni de fotogramas con perspectiva.
- El inventario es funcional y de interfaces, no una lista completa de cada tornillo, imán, junta o componente de placa.

## 10. Fuentes y localizadores de verificación

### E1: documentación exacta

- **F01. Xiaomi España, especificaciones X20 Pro.** https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/specs/ — modelo, alimentación, dimensiones y estación. Consulta 2026-10-25.
- **F02. Xiaomi España, página del producto.** https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/ — sensores, mopas, elevación y funciones de estación.
- **F03. Xiaomi Global, FAQ X20 Pro.** https://www.mi.com/global/support/faq/details/KA-445208/ — mantenimiento, sensores, docking y funcionamiento de estación. Versión española: https://www.mi.com/es/support/faq/details/KA-922892/ .
- **F04. Manual de usuario Xiaomi X20 Pro, edición europea, alojado por Otto.** https://d.otto.de/files/7208679f-5a7d-56d4-b534-937139397f71.pdf — documento Xiaomi, modelos D102GL y D102-JZEU verificados. PDF de 59 páginas; páginas PDF 6–7 contienen las dobles páginas impresas 04–07, con vistas del robot/estación; página PDF 10 incluye especificaciones. Descargado y revisado visualmente. SHA-256: `7e1530070d82fedd6b574ba287950db389520483b7d2ea1c1e073acaff61cbc0`. Alojamiento de tercero, autoría identificada como Xiaomi; no es manual de servicio.
- **F05. Manual JP/EN en CDN oficial Xiaomi, corroboración visual.** https://i02.appmifile.com/993_operatorx_operatorx_xm/13/05/2025/77d23ed347099a90e75ce297d1202d40.pdf — páginas PDF 11–12 con vistas equivalentes. No se utilizan sus datos regionales de alimentación de estación para la versión EU.

### E2: recambios con identificación explícita del modelo

- **F06. Catálogo PC:MediaStore filtrado por X20 Pro BHR8859EU / D102-JZEU.** https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html y https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html?page=2 . Es un catálogo comercial, no una lista OEM; las recomendaciones laterales de otros productos no constituyen compatibilidad.
- **F07. Rueda izquierda, SKU 12585.** https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html — Pro/Max explícitos; rueda, motor y reductora.
- **F08. Rueda derecha, SKU 13025.** https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html .
- **F09. Pasador, SKU 12584.** https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html — dimensiones anunciadas 4 × 38,5 mm; Pro/Max en compatibilidad. Debe medirse el componente real.
- **F10. Muelle, SKU 37935.** https://www.ep-mediastore-ab.de/xiaomi-radfeder-62x32-45mm-p-37935.html — Pro explícito; no especifica curva fuerza/elongación.
- **F11. Motores de mopa Pro, SKU 29890.** https://www.ep-mediastore-ab.de/xiaomi-wischmotoren-x20-pro-p-29890.html — izquierdo/derecho, reductoras y detección de plato según vendedor.
- **F12. Aspiración Pro, SKU 72817.** https://www.ep-mediastore-ab.de/saugmotor-hjd-ra60405-xiaomi-s20-x20pro-p-72817.html .
- **F13. Contactos e IR trasero Pro, SKU 28885.** https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html — dos contactos, cable, sensor de docking y soporte según vendedor; identificación D102_BIR en ficha.
- **F14. Placa Pro, SKU 40091.** https://www.ep-mediastore-ab.de/xiaomi-x20-pro-mainboard-b108eumb-p-40091.html — identificación comercial B108EU_MB; no confirma equivalencia de firmware entre modelos.
- **F15. IR de estación, SKU 26830.** https://www.ep-mediastore-ab.de/xiaomi-dock-ir-sensor-d102-x20m-p-26830.html — compatibilidad D102-JZEU/D109-JZEU y etiqueta D102_DOCK_IR según vendedor.

### E3a: vídeos primarios de modelos relacionados

- **V01. Mijia M30, «小米全能扫拖机器人M30拆装机教学视频».** https://www.douyin.com/video/7483728020235177231 — 36:15; autor 好杜ཻ๓ ້有度࿐. Contenido previamente descargado y observado; los tiempos de §5 corresponden al vídeo, no a un texto indexado. M30 no se declara idéntico a D102GL.
- **V02. X20 Max, «Robô Aspirador Xiaomi X20 Max - Desmontagem completa».** https://www.facebook.com/eliandro.martins.340852/videos/rob%C3%B4-aspirador-xiaomi-x20-max-desmontagem-completa/1459675169547042/ — vídeo previamente descargado y observado. Detalle de muelle/interruptor en 01:37–01:40; no muestra extracción de rueda.
- **V03. Mijia All-in-one 2, «米家全能扫拖机器人2轮子拆卸更换视频».** https://www.bilibili.com/video/BV1bG5WzYELb/ — 03:45; autor bili_32371503140. Extracción selectiva observada; disposición del interruptor distinta, no usar su número de tornillos en Pro.

### Método y trazabilidad

Revisión de fuentes oficiales, documentos descargados, compatibilidad explícita de fichas y fotogramas ya obtenidos en la investigación. No se han añadido fotografías de la unidad del usuario, información personal ni medios completos de terceros a este documento. Las URLs y marcas temporales permiten volver al original. La investigación no modifica firmware ni hardware. Sus resultados se documentan en este repositorio.

Los pasos de diseño y aceptación marcados E4 deberán convertirse en registros medidos y resultados de prueba antes de fabricar una versión definitiva. Una medida pendiente permanece pendiente; no se rellena con una estimación visual.
