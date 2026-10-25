# 10 — Inventario observado en las fotografías de esta unidad

Fecha: **2026-10-25**. Fuente: fotografías privadas identificadas como **F001–F018**. Inspección visual; no se han realizado mediciones eléctricas ni pruebas de funcionamiento. Este inventario público cita fotografías por identificador y omite imágenes e identificadores individuales. Los códigos transcritos son referencias de diseño o de componente.

## 1. Resultado principal

Las fotos permiten comenzar el inventario real de la unidad y confirmar varias referencias que antes procedían sólo de recambios comerciales. **La placa principal muestra B108EU_MB; no se ha leído su revisión.** Las revisiones VB2 visibles corresponden a dos placas auxiliares, no deben atribuirse a la principal.

La electrónica sigue distribuida entre cuerpo inferior, carcasa superior y paragolpes desmontados. Trasladar sólo la placa principal dejaría fuera conjuntos necesarios. El plan debe conservar esos conjuntos, sus apoyos y sus arneses antes de cualquier prueba alimentada.

## 2. Referencias y observaciones

Estados: **O** = observado directamente; **I** = interpretación apoyada por forma/posición y documentación previa; **P** = pendiente. Una referencia legible identifica lo marcado, no certifica el estado funcional.

| Conjunto / foto | Observación o lectura | Estado y límite |
|---|---|---|
| Batería, F001 | SCUD; modelo **P2150-4S2P-SCEV**. Etiqueta: 14,4 V nominales; 5200 mAh nominales y 4800 mAh rated; límite de carga indicado 16,6 V; energía rated 69,12 Wh | **O.** Confirma el pack fotografiado. No define la función de sus conductores ni autoriza una fuente externa. No se transcribe su identificación individual |
| Placa principal, F013 | **B108EU_MB**, visible bajo una cubierta protectora translúcida; contorno ancho y curvo, con varios grupos de conectores | **O.** Revisión, procesador, radio, antena e IMU: **P**. No se ha desmontado la cubierta ni identificado sus propiedades eléctricas |
| Placa de mandos, F011 y F013 | **B108EU_SWITCH**, **VB2**, fecha serigrafiada **2023/12/5**; dos pulsadores, LEDs y conexión corta a la placa principal | **O.** La fecha serigrafiada no se presenta como fecha de fabricación del robot. Se distinguen SW1300 y SW1301; el mapa de pines del conector sigue pendiente |
| Placa auxiliar, F007 | **B108EU_WIFI_LED**, **VB2**, **2023/12/5**; pulsador, LED y dos conectores con arneses diferentes | **O.** El nombre no demuestra que sea el transceptor Wi-Fi ni que contenga la antena. La función detallada de sus dos conexiones queda **P** |
| Turbina, F002 | **HJD-RA60405**, **V1.5**, **BL.531124.0161**, marca KELI y etiqueta DC14.4V; carcasa blanca, soporte metálico y electrónica propia | **O** de las marcas y del montaje. Función de cada terminal y características eléctricas completas: **P**. Conservar el conjunto y su carcasa/flujo de aire |
| Motor cilíndrico, F004 y F013 | **PRI-390SV-24100**; dos terminales y cables visibles | **O** de referencia y conexiones visibles. Su asociación al accionamiento del cepillo principal es **I** por ubicación; no se deducen tensión, corriente ni velocidad a partir del código |
| Motores y reductoras, F005, F009 y F010 | La lectura visual del marcado es **PRI-385SV-2185**; se observa motor unido a carcasa negra y cableado adicional que entra en la tapa del conjunto | Referencia transcrita de la foto; comprobarla de nuevo antes de buscar un recambio. La asociación a los conjuntos de mopa es **I** por forma/posición. No se identifica la función del cableado adicional sólo por su número de hilos |
| Placa perimetral, F012 | Logotipo Xiaomi y comienzo de referencia **D102…**; varios pads TP170x, conector y fijaciones visibles | **O** de lo legible. El resto del nombre queda oculto. La asociación a contactos/IR posterior es **I**, coherente con el conjunto investigado; no completar la serigrafía desde un catálogo |
| Conjunto frontal, F014–F016 | Placa con texto **B108EU_CamSub**, revisión **VC1** y conector **CN1500**; cubiertas, soporte y cinta flexible que recorre el paragolpes hasta otra unidad | **O** de etiquetas y relación física. No deducir una cámara RGB ni funciones de vídeo por el nombre CamSub. Asignación del conector y protocolo: **P** |
| Conjunto bajo la torreta, F017 y contexto F014/F018 | PCB y motor pequeño siguen fijados a la carcasa superior. El motor conserva su conexión de dos hilos; hay otro receptáculo sin pareja conectada en la foto | **O** del montaje; identificación funcional como conjunto LDS por contexto: **I**. No se transcribe la etiqueta individual. Fabricante/referencia completa: **P** |

En F017 aparecen serigrafías como TX, PWM/RX, SCL, SDA, GND y VCC junto a puntos de prueba. **Son textos observados, no un pinout del receptáculo ni una invitación a conectarle USB, UART o una alimentación.** No se ha establecido su relación con las posiciones del conector, niveles, protocolo o función en funcionamiento.

## 3. Relaciones de cableado que sí pueden registrarse

| Relación | Evidencia | Alcance |
|---|---|---|
| B108EU_SWITCH ↔ placa principal | F011/F013 muestran ambos extremos y el arnés corto con funda | Conexión entre conjuntos confirmada visualmente. Número de vías y funciones de pin pendientes de lectura precisa |
| Dos unidades del paragolpes ↔ cinta flexible | F014 muestra el recorrido; F015/F016 sus extremos y montajes | Relación física confirmada. Conservar cinta, radios de curvatura y soportes; no hay prueba de continuidad eléctrica |
| Motor pequeño ↔ PCB bajo torreta | F017 muestra el recorrido de dos conductores y su conector local | Relación interna observable. No equivale al pinout de la conexión externa del LDS |
| B108EU_WIFI_LED ↔ dos ramales | F007 muestra los dos conectores y parte de los cables | Los destinos no quedan trazados completamente. Registrar ambos como pendientes; no asignarlos por color |
| Placa principal ↔ ramal libre en zona central | F013 muestra un ramal que acaba en conector sin pareja | Extremo libre observado. El emparejamiento con el receptáculo de F017 u otro módulo no se declara confirmado por parecido |
| Placa perimetral D102… ↔ arnés | F012 muestra un extremo | Destino y correspondencia de posiciones pendientes |

La vista general F018 está recortada en una parte del cuerpo inferior. No permite cerrar el mapa completo de ramales. Muchos conectores de la placa principal están detrás de la cubierta o de cables. **No se ha observado un mapa exacto de todos sus puertos y no debe inventarse.**

Hay material blanco alrededor de varios conectores/pulsadores. La foto no establece su composición, origen o función. No se propone retirarlo para completar etiquetas. Lo mismo ocurre con las espumas, cubiertas y soportes: se registran como elementos del montaje a conservar hasta comprender su papel.

## 4. Qué cambia en el plan del chasis

1. **La bandeja electrónica ya tiene una referencia real de forma y distribución.** Se puede construir su volumen preliminar y reservar acceso alrededor de conectores. Las fotos carecen de escala dimensional adecuada; no sirven todavía para fijar cotas de fabricación.
2. **La torreta/LDS no está en el mismo soporte que la placa principal.** Su montaje en la carcasa superior es una interfaz propia; hay que trasladar soporte, orientación, motor y conexión externa como conjunto. No se gana una prueba funcional dejando esa carcasa separada con su módulo colgando.
3. **El paragolpes contiene conjuntos electrónicos unidos por flex.** Su forma, movimiento, ventanas y la distancia entre unidades condicionan el diseño. El flex existente no permite presuponer que podrán recolocarse libremente en un chasis de otro proyecto.
4. **La placa WIFI_LED no localiza la radio.** La zona de antena continúa pendiente; ningún nuevo refuerzo conductor debe aprobarse basándose en esa etiqueta. No se necesita identificar el chip para comenzar el inventario, pero sí resolver el entorno de radio que vaya a cambiar.
5. **Hay electrónica protegida por cubiertas y conjuntos con su propia carcasa.** Conservar el montaje completo es el punto de partida. La ausencia de daño evidente en estas fotos no prueba aislamiento, resistencia mecánica o funcionamiento.
6. **La compatibilidad con un chasis abierto de referencia sigue siendo geométrica por demostrar.** Estas fotos no validan una implantación OOMWOO ni una tolerancia de sus soportes para los módulos Pro; sí proporcionan datos para comparar volúmenes e interfaces.

Mantener dos estados por módulo: **integridad mecánica para montar/accionar** y **funcionamiento eléctrico observado**. Un motor reconocible por su etiqueta puede tener una reductora que requiera atención; una placa aparentemente completa puede no haber sido probada. Ninguna de estas fotos es una prueba funcional.

## 5. Datos adicionales realmente necesarios

**Para continuar el inventario no es necesario desmontar más.** Ya se pueden registrar batería, placas auxiliares, turbina, módulos, referencias y conexiones observadas.

Antes de separar más arneses o cerrar la disposición de la bandeja electrónica:

- **Una vista cenital completa del cuerpo inferior**, sin recortarlo, con el frontal marcado. Resuelve la posición relativa de las fotos de detalle y los recorridos periféricos.
- **Detalles de las zonas de conectores de la placa principal**, tomados desde los lados que permitan verlos sin retirar material blanco o cubiertas por fuerza. Sólo hay que resolver los ramales que se vayan a mover; un conjunto que permanezca montado puede conservar conexiones internas pendientes.
- **Detalle de cada conjunto de rueda y su microinterruptor/arnés**, incluyendo la pieza que lo acciona. La foto F006 muestra sólo una vista parcial; no acredita el montaje de ambos detectores ni sus recorridos de cable. Una misma serie de detalles puede resolver las referencias mecánicas y el paso del arnés.

Antes de la primera alimentación será necesario identificar y comprobar físicamente las parejas de los conectores que ahora están separados. Las fotografías orientan, pero no sustituyen la revisión de pareja, orientación, fijación y aislamiento en el montaje.

No pedir otra foto de la etiqueta de batería: la referencia ya es legible. No abrir la batería, reductoras, óptica o blindajes para obtener marcas adicionales sin una pregunta concreta que lo justifique. La revisión de la placa principal y la identificación de radio/IMU permanecen pendientes si no pueden leerse manteniendo el montaje.

## 6. Refutación actualizada

- **Premisa corregida:** ya no dependemos sólo de una referencia comercial para B108EU_MB; existe lectura en la unidad. **No se ha confirmado su revisión ni su esquema.**
- **Premisa descartada:** ver WIFI_LED no localiza la antena, y ver CamSub no demuestra una cámara de vídeo convencional.
- **Límite nuevo concreto:** el traslado afecta también a conjuntos fijados al paragolpes y a la carcasa superior, con conexiones actualmente separadas. Una prueba de la placa principal aislada no validaría el robot.
- **Sin cambio esencial de herramientas:** las imágenes no justifican KiCad, PulseView, otra controladora o firmware nuevo. El siguiente trabajo sigue siendo inventario, correspondencia de montajes y geometría medida.

Esta inspección no diagnostica fragilización de todos los plásticos, no atribuye la causa a un adhesivo y no confirma que todos los conjuntos sean reutilizables. Las fuentes de las observaciones son los IDs de foto citados; no se han publicado ni consultado en servicios web las imágenes privadas.


## 7. Consecuencias mecánicas y comparación con OOMWOO

Se han revisado **18 imágenes únicas**. El JPEG enviado por separado coincide con F014; los originales permanecen fuera del repositorio público. El inventario no implica que se haya comprobado el funcionamiento de cada módulo.

| Evidencia | Consecuencia para el diseño | Dato todavía necesario |
|---|---|---|
| F001/F018: pack alargado con conector propio | Cuna y acceso definidos para el paquete completo | Volumen, masa, apoyos y espacio de extracción |
| F002/F018: turbina con carcasa, bocas y fijaciones | Reutilizar el conjunto si es apto; montar sólo el motor no reproduce el ventilador | Bocas, juntas, orientación, volumen y acceso |
| F005/F009/F010: mecanismos de mopas con motor y carcasa | Adaptar soportes conservando transmisión y elevación aprovechables | Centros, fijaciones, barrido completo, plano de mopa y postura en estación |
| F006/F008: rueda extraída y pasadores separados | Diseñar soporte del pivote, retención y recorrido, además de hueco para la rueda | Ambos apoyos, diámetro/longitud del pasador, daño y detector |
| F013: placa ancha y curva con cubierta | Modelar el arco y conectores; una bandeja rectangular genérica puede no servir | Patrón de fijación, altura y hueco de servicio |
| F014–F016: unidades ópticas y flex sobre el paragolpes | Tratar frontal, ventanas y flex como interfaz conjunta | Posiciones relativas, ángulos, movimiento y retorno |
| F017/F018: navegación fijada a carcasa superior | Darle soporte propio con posición y campo libre definidos | Plano, altura y referencia respecto a la rodadura |
| F018: varios resortes distintos | Separar original y candidato de sustitución | Identificación, dimensiones y fuerza frente a longitud |

La carcasa de un mecanismo puede estar deteriorada aunque su motor sea recuperable. Se inspeccionará la zona afectada antes de decidir si se conserva el conjunto completo. Una carcasa con asientos de engranajes, ejes u óptica requiere controlar esas referencias al reconstruirla; no se equipara a una tapa exterior.

Las fotografías no permiten localizar inequívocamente todas las fracturas. El relato del propietario sobre roturas se registra como observación de uso; no se atribuye una composición o causa de fragilidad a partir del aspecto. Hace falta un detalle de cada apoyo del pasador y cada gancho del muelle, por dos lados, que muestre qué pertenece al cuerpo fijo y qué bascula. No se necesita pegar de nuevo la carcasa para documentarla.

La estación y sus superficies de acoplamiento no aparecen documentadas. Su referencia sigue siendo necesaria para conservar carga, vaciado, lavado y secado. No se deduce una toma de relleno ni un depósito interno en este Pro por analogía con otro modelo.

## 8. Siguiente paquete mínimo de medidas

Para comparar una base propia con la base principal de OOMWOO basta inicialmente un ensamblaje de volúmenes simplificados; no hace falta reconstruir todos los nervios del plástico original.

1. **Referencia de conjunto:** vista completa cenital y de la base, indicando delante, con regla en el plano medido. Registrar qué piezas faltan y la posición de la suspensión; las cotas de fabricación se tomarán directamente.
2. **Geometría funcional:** centros y alturas de ruedas/pivotes, rueda loca, cepillo y mopas; coordenadas de sensores y montaje superior respecto a la misma referencia.
3. **Volúmenes de módulos:** largo, ancho, alto y puntos de montaje de placa con cubierta, batería, turbina, mecanismos de mopa y ruedas. Incluir espacio para cables, herramienta y extracción.
4. **Estación:** rampa/bandeja, contactos, señal y boca de vaciado, y su relación con el robot en cada postura necesaria. Empezar por observación y medición sin energía si el robot no puede sostenerse.
5. **Suspensión:** detalle del daño y dimensiones de pasadores/muelles; después, caracterización de fuerza y recorrido dentro de límites conocidos. Un resorte visualmente mayor no aporta esa información.

El inventario y CAD preliminar pueden avanzar con lo recibido. Los detalles adicionales se piden por interfaz que vaya a diseñarse o moverse, evitando desmontar por sistema conjuntos sanos. Las plantillas [módulos](electronica-modulos.csv) y [conexiones](electronica-conexiones.csv) contienen los primeros datos observados; sus campos pendientes no son mediciones inferidas.

**Relación con el plan:** [07 — Chasis propio](07-plan-del-chasis-propio.md); [09 — Comparación con OOMWOO](09-oomwoo-comparacion.md). Las observaciones de este capítulo proceden de fotografías del propietario; las consecuencias de diseño se presentan como razonamiento técnico, no como resultados de ensayo.
