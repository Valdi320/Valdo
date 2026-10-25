# 12 — Interfaces mecánicas, limpieza y estación

**Nota de ingeniería privada · 25 de octubre de 2026 · Xiaomi Robot Vacuum X20 Pro D102GL.**

Objeto: sustituir la base plástica portante, conservar los conjuntos aprovechables y permitir sustituir apoyos o módulos sin inutilizar de nuevo toda la base. Los fragmentos rotos ya no están disponibles. Este documento no exige recuperarlos, pegar la carcasa ni restaurar el robot antes de comenzar el CAD. No contiene dimensiones de fabricación validadas.

Se han revisado las fotografías privadas F001–F018, el registro M01–M32 y las notas previas. Para esta ronda se han vuelto a inspeccionar F006, F010 y F018 y las fichas exactas de las piezas indicadas. No se han publicado fotos ni modificado CAD, repositorios o el CSV compartido. Las propuestas M40–M60 son una ampliación para integrar, no valores ya medidos.

## 1. Conclusión y decisión de arquitectura

**Podemos diseñar una base nueva sin reproducir las orejetas originales desaparecidas.** Hay que recuperar las interfaces funcionales: ejes, posiciones de apoyo, movimiento, sellos, fijaciones de conjuntos y postura frente a la estación. La forma exterior de un gancho roto no es una condición del proyecto; su posición, dirección de carga y relación con el recorrido de suspensión sí lo son.

La arquitectura propuesta es un núcleo que conserve las referencias principales, con dos cassettes de suspensión reemplazables, soportes independientes para los conjuntos de limpieza y una interfaz posterior de estación cuya posición se pueda repetir. Las superficies de localización de los cassettes deben transmitir la posición; las fijaciones deben sujetarlos sin deformar los mecanismos. **Es una elección de ingeniería por contrastar con medidas y fabricación, no un recambio demostrado para Xiaomi.**

Conviene mantener completas las reductoras, carcasas funcionales, acoplamientos y juntas que estén sanos. Sustituir una base portante no obliga a rediseñar el interior de cada transmisión. Si una carcasa de precisión del módulo está rota, su reparación o reconstrucción se registra aparte: no basta con fijar mejor el conjunto al bastidor.

## 2. Evidencia y reglas de lectura

| Código | Significado en esta nota | Alcance |
|---|---|---|
| E1 | Fuente del fabricante del robot o del componente técnico | Confirma lo que dice esa fuente; una ficha externa no es un plano interno. |
| E2 | Ficha propia de un vendedor de la pieza, con Pro expresamente declarado | Confirma una oferta y compatibilidad declarada; no demuestra una tolerancia OEM ni identidad entre chasis. |
| E3 | Observación de la unidad en las fotografías privadas | Forma, presencia y relaciones visibles; no medida física ni prueba de funcionamiento. |
| E4 | Deducción o propuesta de ingeniería | Necesita cotas, inspección o prueba antes de fabricar o aprobar. |
| Pendiente | Dato no recuperado con suficiente fiabilidad | Se deja vacío; no se completa por simetría, por píxeles ni por diámetro exterior del robot. |

Las referencias 12584, 37935, 12585, etc. son **SKU del vendedor**. No se convierten en códigos OEM porque aparezcan en una ficha de recambio original. Las páginas comerciales advierten que la imagen puede diferir; sus fotos ayudan a reconocer formas, pero no son planos de mecanizado. La compatibilidad se registra por pieza: por ejemplo, que un cepillo o una rueda loca se declare para X20+ y Pro no demuestra que sus bases sean intercambiables.

## 3. Qué cotas públicas tenemos realmente

| Interfaz o conjunto | Dato documentado | Fuente / evidencia | Lo que no se obtiene de ese dato |
|---|---|---|---|
| Robot completo | D102GL; envolvente nominal **Ø350 × 97 mm**, masa neta **3,7 kg** | Xiaomi, S01; E1 | Diámetro de la base negra, plano del suelo, ancho de vía, masa de esta unidad modificada ni tolerancias. |
| Estación | D102-JZEU; tamaño exterior **340 × 420 × 563 mm** | Xiaomi, S01; E1 | Pendiente de rampa, huellas, posición de bocas/contactos o postura del robot. |
| Pasador del módulo de rueda | **Ø4 × 38,5 mm**, nominal comercial | SKU12584, S04; E2; dos pasadores separados visibles en F008 | Diámetro real, ajuste del alojamiento, forma de retención, longitud útil entre apoyos ni dureza. |
| Muelle de rueda | Aproximadamente **45 mm con ojales / 32 mm sin ojales**, **Ø exterior 6,2 mm** | SKU37935, S05; E2 | Diámetro de alambre, longitud entre interiores de ojales, constante, tensión inicial, extensión admisible y fatiga. |
| Ruedas izquierda/derecha | Conjuntos rueda–motor–reductora; cable hasta conector **11,5 cm** declarado; placa XYD-2012W | SKU12585 / 13025, S06–S07; E2 | Diámetro de rueda, eje de pivote, huella, ángulo de trabajo o libertad útil de cable. La longitud comercial no es una autorización para tensarlo. |
| Plato de mopa | Soporte original con retención magnética, fijación de paño por velcro; diámetro anunciado **aprox. 13 cm** | SKU18142, S09; E2 | Separación de ejes, diámetro barrido real del paño húmedo, perfil de acoplamiento ni altura respecto al suelo. |
| Elevación de mopas | Elevación anunciada **hasta 10 mm** | Xiaomi, S02; E1 | Carrera exacta de esta unidad, cotas de montaje de la reductora, margen real con paño instalado o fuerzas de apoyo. |

No he localizado en las fuentes revisadas un plano dimensionado OEM de la base Pro, de los apoyos de pivote o de los patrones de montaje. Esa ausencia de información pública no significa que no exista documentación de servicio. Las cotas anteriores sirven para identificar y comprobar piezas, no para generar automáticamente taladros de fabricación.

## 4. Registro de interfaces que debe gobernar el CAD

### 4.1 Rodadura y suspensión

| Interfaz | Qué se conserva o reconstruye | Fuente / evidencia | Medida o comprobación que falta | Consecuencia para el diseño |
|---|---|---|---|---|
| Módulo de rueda izquierdo | Rueda, reductora, motor y carcasa móvil aprovechable como conjunto | S06; F006 y F018 muestran un conjunto, sin lateralidad inequívoca en esas vistas; E2/E3 | Identificar lado físicamente; relación tridimensional entre pivote, eje de rueda y caras de apoyo; envolvente durante el giro | No usar solo un cilindro del diámetro de rueda como sustituto del módulo. |
| Módulo derecho | Su propia geometría, cable y lado de extracción | S07; E2 | Medirlo por separado, aunque parezca reflejado | Un parámetro común solo se comparte después de comprobarlo; no crear un espejo CAD como dato original. |
| Pivote y retención | Eje recuperado y superficies de giro; apoyo fijo nuevo si ha desaparecido | S04; F008; E2/E3 | M04–M09 y M15; extremos, retención, anchura de apoyo y qué superficie gira respecto a cuál | Proponer apoyos o casquillos reemplazables, con fijación que no pince el brazo al apretar. Ø4 nominal no prescribe broca ni ajuste. |
| Anclaje del muelle | Coordenadas y dirección de tiro; gancho o soporte fijo reemplazable | S05 y S17; E2/E1; forma real pendiente | M16–M21; punto móvil, punto fijo, longitudes y fuerza durante el recorrido | El anclaje nuevo puede tener otra forma robusta, pero moverlo cambia el par sobre la rueda. |
| Topes y detección de rueda levantada | Límites mecánicos y actuación del detector realmente presente | F006 no documenta el conjunto completo; E3 limitada | M12–M14 y M22; posición de actuación, retorno, mecanismo de contacto y orden frente al tope | No usar el detector o su placa como tope de carga; no inventar tipo de sensor ni omitirlo. |
| Apoyo delantero | Conjunto de rueda loca y asiento en la base | SKU42556, S10, Pro explícito; E2 | M27 y nuevo M45; caras de apoyo, retención, altura, giro y espacio barrido | Conservar movilidad de rueda y horquilla; trasladar su asiento como interfaz separada. |
| Relación entre apoyos | Ancho de vía, radio efectivo, posición de rueda loca, altura del cuerpo | M25–M27 pendientes; S01 solo global; E4 | Medidas en estado definido de carga/suspensión | Conservar primero geometría funcional; el firmware original no ha demostrado ser reconfigurable para otros parámetros. |

### 4.2 Limpieza y circulación de aire

| Interfaz | Qué está documentado | Fuente / evidencia | Medida o identificación que falta | Consecuencia para la base |
|---|---|---|---|---|
| Caja de cepillo principal | Módulo comercial con motor y junta, sin rodillo ni tapa; Pro declarado | SKU73385, S11; F004/F013/F018; E2/E3 | Puntos de montaje, boca, junta, posibles grados de libertad originales y plano inferior | Conservar la caja completa sana; no rigidizar una unión que originalmente permita movimiento. |
| Rodillo y tapa inferior | Xiaomi describe extracción de la tapa por clips y apoyos en extremos del cepillo | S03; E1; rodillo visible en fotos iniciales y F006 | Eje del rodillo, acoplamientos, apoyos, holguras de tapa y contacto con suelo | El acceso de limpieza debe seguir disponible. La tapa no se convierte en una unión estructural permanente. |
| Cepillo lateral | Motor/reductora aparte, declarado compatible con Pro | SKU55856, S12; E2 | Eje, altura, fijación y barrido de las cerdas instaladas | Reservar barrido bajo el perímetro y permitir sustitución, sin interferir con rueda, faldón o frontal. |
| Mecanismos de mopa L/R | Pareja de motores/reductoras con cable y sensor de presencia de plato según ficha | SKU29890, S08; F005/F009/F010/F018; E2/E3 | Patrones de fijación de cada lado, plano de asiento, eje de salida, carrera y barrido completos | Mantener cada mecanismo sano; no identificar el sensor como encoder o sensor de elevación sin evidencia. |
| Platos/paños de mopa | Platos magnéticos disponibles y elevación oficial | S09/S02; E2/E1 | Alturas con plato y paño, separación de ejes, envolvente seca/húmeda y extracción | Una abertura de 130 mm nominal no define el hueco necesario ni el espacio libre real. |
| Depósito de polvo | Recambio exacto Pro blanco, apto para estación de vaciado, suministrado sin filtro | SKU50066, S13; E2 | Caras localizadoras, cierre, extracción, bocas, juntas y relación con detector de presencia | Preferir reutilizar depósito/filtro y reconstruir su cuna. No convertir toda su silueta en un encaje rígido sin reconocer apoyos y sellos. |
| Turbina y conexión flexible | Turbina blanca completa visible; recambio de goma y espuma declarado para Pro | F002/F018 y SKU66031, S14; E3/E2 | Bocas, orientación, fijaciones, compresión de sellos y ruta real de aire | Mantener turbina como conjunto. La ficha de la goma usa terminología ambigua de prefiltro/salida: trazar físicamente antes de asignar sentido. |
| Pieza negra junto al hueco de la tapa superior | F018 muestra una pieza de aspecto tubular fijada al cascarón blanco retirado | F018; E3 | Identidad, función, contracaras y relación con depósito/circuito de aire | No dar por hecho que todo lo unido a la tapa blanca es cosmético; inventariarlo antes de descartarla. No se afirma que sea el conducto de autovaciado. |

El nuevo bastidor puede soportar una cuna del depósito, una caja de cepillo y las unidades de mopa por separado. **El circuito de aire sigue siendo continuo:** separar piezas de mantenimiento exige juntas accesibles y localización repetible, no dejar aperturas entre módulos. La forma exacta del conducto nuevo es una decisión posterior a identificar entradas, salidas, sellos y espacio disponible.

### 4.3 Acoplamiento a la estación

| Interfaz | Fuente / evidencia | Qué se puede recuperar de la pareja real | Qué aún no se sabe |
|---|---|---|---|
| Contactos e IR posteriores | SKU28885, S15: dos contactos, cable, D102_BIR y soporte, situado atrás; E2. Xiaomi confirma contactos traseros y ventanas sin obstrucciones, S03; E1 | Caras de asiento del soporte completo, ventana y posición relativa de contactos, sin separar óptica sana | Coordenadas respecto al marco del robot, carrera de contactos y márgenes reales. Detalle electrónico en nota paralela. |
| Rampa y apoyos de acceso | Xiaomi advierte que el extensor mal instalado o el agua pueden impedir la subida, S03; E1 | Perfil y planos reales de estación; zonas de paso y apoyo de las ruedas; despeje bajo robot | No se deduce la pendiente de las dimensiones externas de estación. |
| Bocas de autovaciado y juntas | Función e interfaces de ventilación de vaciado confirmadas por Xiaomi, S02–S03; E1 | Contracaras, boca, sello, postura del robot y posibles obstrucciones | Sección, posición, presión de junta y ruta completa dentro del robot. |
| Lavado de mopas | SKU50064, S16: placa de lavado Pro que se inserta en la cubeta; Xiaomi documenta lavado/secado, S02; E2/E1 | Bandeja y platos originales como contrapartes para medir centros, alturas y superficies de contacto | Fuerzas durante lavado, postura efectiva, holguras, drenaje y si coinciden con la postura de carga. |
| Secado | Función documentada por Xiaomi, S02; E1 | Mantener libres las rutas reales del aire y el entorno de mopas | Temperaturas en nueva estructura y variaciones por material/cierre; no diseñar usando una temperatura no medida. |

La estación existente ofrece contracaras útiles, pero **no es un calibre que determine por sí solo todas las cotas originales del robot**. Varias geometrías pueden tocar sus contactos y aun así apoyar mal las ruedas, bloquear una mopa o perder el sello de polvo. No se presupone una única postura común para carga, lavado y vaciado. Tampoco se añade un depósito de agua interno o toma de rellenado del robot por analogía con otros modelos: no se ha confirmado en esta unidad.

## 5. Reconstrucción cuando faltan los fragmentos

### 5.1 Recuperar relaciones, no repetir el daño

1. **Documentar lo que queda fijo y lo que se mueve.** Identificar cada módulo por lado y estado. Los dos pasadores, la carcasa móvil, el gancho móvil superviviente y los puntos de asiento proporcionan información aunque la orejeta fija se haya perdido. Si también falta la zona de pivote del cuerpo móvil, se registra como reconstrucción de ese módulo, no como un mero soporte de base.
2. **Elegir referencias supervivientes independientes.** Usar caras de asiento y centros de fijaciones sanos de varios conjuntos, o un útil que los inmovilice sin flexionarlos. Tres puntos no colineales permiten definir un marco local; hay que documentar además su orientación respecto al avance y al suelo. La circunferencia de una tapa flexible o un borde roto no se utiliza como única referencia.
3. **Medir los módulos fuera del conjunto cuando convenga.** La posición del eje de rueda respecto a su pivote puede recuperarse del módulo. Esto no determina automáticamente dónde estaba el pivote respecto al cepillo, la rueda loca o la estación. Esa relación global se recupera de restos sanos, referencias cruzadas y restricciones funcionales.
4. **Usar la pieza que encaja como referencia de su contracara.** Un pasador permite reconocer un alojamiento; el depósito identifica sus apoyos y sellos; el módulo de mopa proporciona caras y taladros; la bandeja de estación ayuda a contrastar la postura de lavado. Se miden esas superficies, sin forzar piezas ni suponer que toda la forma exterior participa en el apoyo.
5. **Crear soporte nuevo donde el original no se puede recuperar.** Separar en el registro «cota original observada», «cota original desconocida» y «nominal nuevo elegido». Una posición nueva puede resolverse por ajuste y prueba, pero no se etiqueta como copia exacta del original.
6. **Medir ambos lados.** Cableados, topes, ganchos y sensores pueden ser distintos. La simetría queda como hipótesis comprobable, nunca como sustituto de una medida que falta.

Las fotografías comerciales aportan vistas adicionales para reconocer un alojamiento o una pieza ausente. Un vídeo de Max/M30 o una carcasa declarada solo para Max puede orientar la búsqueda, pero no fija cotas Pro. La compatibilidad de ruedas Pro/Max ya está declarada; no se extiende por ello a la carcasa portante entera.

### 5.2 Qué hacer con las mediciones antiguas de fractura

M01–M03 y M10–M11 se redactaron para estudiar una reparación local. Si ya no hay fragmento o apoyo sano utilizable, registrar esa circunstancia. **No bloquean el chasis propio por quedar irrecuperables.** La clasificación de los módulos aprovechables sí sigue siendo necesaria: carcasa sana, soporte exterior roto, precisión interna afectada o estado desconocido.

Si el chasis antiguo ya no mantiene una posición bajo carga fiable, M13, M26 o M31 no se rellenan a partir de un montaje que se deforma. Se conserva lo recuperable, se declara la referencia perdida y se valida la nueva posición en el útil/bastidor diseñado. No se calcula precisión original a partir de una foto sin escala.

## 6. Soportes reemplazables y camino de carga

### 6.1 Cassette de suspensión por lado

Propuesta E4: cada cassette puede contener los apoyos fijos del pivote, la retención accesible del pasador, el anclaje fijo del muelle, los topes y la montura del detector que se confirme. El brazo y la rueda originales entran como conjunto. La extracción debe prever el conector y el recorrido del pasador; no basta con que los tornillos sean visibles si otra pieza impide sacar el eje.

El camino de carga deseado es **rueda → carcasa móvil/pivote → apoyos del cassette → asientos amplios del núcleo**. La tracción del muelle cierra su carga entre módulo y cassette/núcleo. La ubicación de los apoyos debe evitar que el apriete de fijaciones comprima la pieza móvil. Separadores, superficies de tope, casquillos o apoyos metálicos son candidatos, con su ajuste definido después de medir.

El apoyo de desgaste y el anclaje del muelle deben poder reemplazarse sin sustituir todo el núcleo. No se diseña un gancho fino integrado en la pieza grande por comodidad de impresión. Un inserto metálico aislado en plástico débil tampoco garantiza mejora: hay que transmitir la carga a suficiente superficie y comprobar su dirección, el apriete y la deformación.

No se propone todavía un tornillo métrico concreto, espesor, aleación, material impreso ni número de nervios. Tampoco se llama al anclaje «fusible» sin conocer las cargas y el daño que causaría su fallo. La separación modular pretende facilitar reparación, no introducir una rotura deliberada.

### 6.1.1 Longitud disponible del pasador: primera restricción calculable

Se puede aplicar el nominal comercial **Ø4 × 38,5 mm** [S04] sin pedir una medida nueva. En el maestro CAD v0.1, la hoja `ParametrosDEMO` y la expresión `PasadorDEMO.Height` definen esta disposición ilustrativa:

| Tramo axial del DEMO | Longitud |
|---|---:|
| Hueco entre apoyos | 26 mm |
| Dos apoyos atravesados, 8 mm cada uno | 16 mm |
| Dos salientes, 4 mm por extremo | 8 mm |
| **Longitud total del pasador DEMO** | **50 mm** |
| Pasador comercial publicado | 38,5 mm |
| **Diferencia con esa disposición** | **11,5 mm** |

La longitud 50 mm también está guardada en el objeto nativo del FCStd. Es una consecuencia de parámetros DEMO explícitos, no una medición del robot ni un fallo de la demostración. Incluso quitando ambos salientes, 26 + 16 = **42 mm**, todavía 3,5 mm por encima del nominal comercial. Por eso cambiar solamente el diámetro de 5 a 4 mm no adapta el cartucho.

Para una disposición en la que el pasador atraviese por completo ambos apoyos, la condición axial necesaria es:

`hueco libre + espesor atravesado del apoyo A + espesor atravesado del apoyo B + salientes reservados ≤ longitud disponible del pasador`

Cada tramo se cuenta una sola vez. El hueco libre debe contener el ancho de la parte móvil y el juego axial que se diseñe. Arandelas o pestañas de casquillo que ocupen ese hueco se incluyen en su presupuesto. La longitud útil y la tolerancia del pasador no están publicadas; 38,5 mm es una referencia nominal de partida, no un límite de ajuste garantizado.

Esta relación descarta combinaciones imposibles y permite comparar apoyos locales más estrechos con un respaldo ancho, o una retención que no necesite largos salientes. No prescribe adelgazar los apoyos: longitud de apoyo, presión de contacto, flexión y unión al respaldo se comprueban con las cargas y el material elegidos. Una tapa de retención externa ocupa espacio de servicio aunque no consuma longitud del pasador. Ninguna alternativa permite pinzar la carcasa móvil mediante el apriete.

Se registran en M41/M42 el ancho y los apoyos, en M43 la extracción, y en M04/M05/M15 los datos y ajustes del pasador. Quedan sin resolver el ancho del módulo, la retención real y las tolerancias; no se inventa un hueco de rueda para cerrar la suma.

### 6.2 Limpieza y estación

| Soporte nuevo propuesto | Qué debe localizar | Qué debe quedar accesible |
|---|---|---|
| Cuna de la caja de cepillo | Caja, asiento/sello de aire y libertad original si existe | Tapa, rodillo, motor y conector, sin desmontar placa principal por rutina. |
| Soportes de mopa independientes sobre referencias comunes | Ejes, alturas y patrón de cada mecanismo | Tornillos y cable, extracción de platos, movimiento de elevación. No separar innecesariamente una reductora sana. |
| Cuna de depósito y sellos | Asientos reales, cierre, bocas y relación con detector | Sacar el depósito y limpiar/reponer filtro sin desmontar bastidor. |
| Soporte de turbina | Caras de fijación, bocas y cierre de junta | Turbina y junta como repuestos; ruta de aire libre. |
| Interfaz posterior de estación | Soporte original de contactos/IR y boca/sello real en un marco común | Ajuste documentado durante prototipo y fijación repetible después; acceso a limpieza de contactos. |
| Soporte de rueda loca | Asiento, retención, altura y giro | Limpieza y sustitución de rueda o conjunto sin desmontar limpieza posterior. |

Más piezas desmontables no siempre mejoran el resultado: cada unión añade error de posición y posibilidad de aflojamiento. Dividir en límites donde existan superficies de referencia y acceso, manteniendo las relaciones críticas en un mismo conjunto cuando resulte más preciso y sencillo.

## 7. Rigidez, masa y suspensión: condiciones funcionales

**Rigidez.** El núcleo debe conservar las posiciones relativas bajo las cargas de uso. Lo relevante es cuánto se desplazan y giran los pivotes, ejes de mopa, rueda loca, sensores y sellos, no que una placa parezca gruesa. El margen admisible debe salir de holguras funcionales y medición de ensamblaje; no se asigna una flecha máxima universal sin datos. Revisar la acumulación de error entre módulo, cassette y base, además del agujero individual.

**Masa y apoyo.** Los 3,7 kg de catálogo son una referencia del producto, no un presupuesto autorizado de aumento. Pesar conjuntos y piezas nuevas y observar reparto entre ruedas motrices, rueda loca y mopas según estado. Un cambio de masa o centro de gravedad altera cargas, posición de suspensión, despeje y entrada a estación. Si no existe un original sano para comparación, se explicita esa limitación. No aumentar la rigidez de muelle para compensar automáticamente una base más pesada.

**Muelle sustituto.** Lee Spring distingue tensión inicial, constante, longitud libre entre interiores de ojales y extensión admisible. Dentro del rango de funcionamiento aplicable, la carga se expresa como `F = Fi + k·ΔL` [S17]. La longitud comercial de 45 mm no define por sí sola esas variables. A igual resorte, mover el anclaje cambia longitud y brazo de palanca durante el recorrido; en general el par de suspensión es `τ(q) = F(L(q))·d_perpendicular(q)`. La fuerza vertical efectiva en la rueda depende además de su geometría. Estas relaciones son razonamiento mecánico, no parámetros conocidos del Pro.

Por tanto, comparar ida/retorno de fuerza frente a posición de rueda, además del muelle aislado. Comprobar antes que el pivote no esté pinzado. Puede resultar válido cambiar solo un muelle, pero no se da por equivalente por ser más largo, por caber o por mantener la rueda abajo. Tampoco se alarga o acorta un gancho para igualar longitud sin revisar toda la respuesta y límites del resorte.

**Fabricación.** Un cupón de alojamiento sirve para estudiar encaje local. No demuestra la coaxialidad de dos apoyos montados ni la rigidez del bastidor cargado. Prusa explica que orientación y tolerancias dependen de geometría y proceso [S18]. No se usan valores isotrópicos genéricos para prometer vida de una impresión. La primera geometría útil es el apoyo/cassette que resuelve una interfaz comprobable; el laminado o cotización de esa pieza permite comparar fabricación sin comprar una impresora de antemano.

## 8. Propuesta de medidas M40–M60

Los M01–M32 existentes siguen conservando sus identificadores. Las nuevas filas concretan interfaces insuficientemente desglosadas, y remiten a las anteriores para no volver a medir lo mismo. La numeración se propone para integrar con los otros frentes; M61–M69 quedan libres.

Registrar por cada fila: módulo/lado, referencia geométrica, instrumento, valor, incertidumbre o rango observado, condición, foto/esquema propio y estado. Usar sufijos o filas hijas para distintas coordenadas, sin comprimir un patrón tridimensional en un solo número. Las cotas elegidas para el CAD van separadas de las medidas físicas.

| ID | Medida / dato nuevo | Cómo obtenerlo y condición | Para qué desbloquea | Prioridad |
|---|---|---|---|---|
| M40 | Referencias supervivientes: caras/puntos A–B–C y orientación del marco común | Identificar al menos tres referencias no colineales estables; registrar estado y relaciones al avance/suelo. Útil si la base ya no fija posiciones | Colocar todos los módulos en un marco reproducible | Ahora |
| M41 | Geometría local del módulo izquierdo: eje de pivote ↔ eje de rueda ↔ caras de apoyo | Medir fuera o en útil, lado confirmado; completar M04–M09/M15 | Soporte piloto y colocación de rueda izquierda | Ahora |
| M42 | Mismo registro independiente del módulo derecho | No rellenar por espejo; identificar diferencias y ruta de cable | Segundo soporte y parámetros realmente compartibles | Ahora |
| M43 | Extracción de cada cassette/pasador/conector | Direcciones, espacio mínimo ocupado por pieza y útil; relación con M23/M24 | Mantenimiento real sin retirar módulos ajenos | Ahora |
| M44 | Correspondencia posición de rueda ↔ longitud/dirección del muelle y fuerza de rueda | Relacionar M12–M22 en estados definidos; original/sustituto diferenciados; no forzar límites desconocidos | Definir anclaje funcional y validar muelle candidato | Piloto |
| M45 | Asiento y retención de la rueda loca | Perfil de apoyo, caras, fijaciones/retén y giro; M27 conserva posición global | Soporte delantero sustituible | Bastidor |
| M46 | Interfaz de caja de cepillo | Patrón de fijación, caras, boca/sello y movimientos permitidos | Cuna y corte de la base, conservando función del conjunto | Ahora, modelo simplificado |
| M47 | Relación rodillo–tapa–suelo | Eje, apoyos y plano inferior con tapa/rodillo montados, sin deducir de cerdas deformadas | Altura de limpieza y acceso inferior | Antes de fabricar cuna |
| M48 | Eje y barrido del cepillo lateral | Ubicación, altura, fijación y barrido instalado | Evitar choque con perímetro/rueda | Antes de cerrar perímetro |
| M49 | Montaje de mecanismo de mopa izquierdo | Caras y centros de fijaciones respecto a eje de salida; volumen y salida de cables | Soporte local sin abrir reductora | Ahora, modelo simplificado |
| M50 | Montaje de mecanismo de mopa derecho | Medición propia, sin asumir espejo de M49 | Posición y soporte del segundo mecanismo | Ahora, modelo simplificado |
| M51 | Platos, paños y posiciones de elevación | Completar M29: perfil de acoplamiento si se modifica, planos, diámetro barrido y extracción; identificar paño/estado | Huecos, altura de trabajo y ausencia de interferencias | Antes de fabricar fondo |
| M52 | Depósito: asientos, cierre, bocas y extracción | Medir depósito sano y contracaras supervivientes; relación al detector coordinada con electrónica | Cuna y envolvente de acceso | Ahora, modelo simplificado |
| M53 | Turbina, juntas y continuidad de aire | Caras/bocas/juntas de conjuntos reales; identificar pieza tubular de F018; no deducir sentido del nombre comercial | Conducto y soporte que puedan desmontarse y sellar de nuevo | Antes de fabricar conductos |
| M54 | Boca/sello de autovaciado del robot respecto al marco | Identificar y medir apertura, plano, contracara y postura en estación; completar M30 | Interfaz posterior y altura funcional | Ahora, inventario y medidas |
| M55 | Perfil de acceso de estación y zonas de apoyo | Rampa/extensor montados; alturas y distancias sobre referencias de estación; no abrir alimentación | Despeje, paso de ruedas y postura de acoplamiento | Ahora, modelo simplificado |
| M56 | Bandeja de lavado ↔ platos de mopa | Centros, alturas, zonas de contacto y espacios libres; contrastar en postura real/útil sin forzar | Cierre de geometría de mopas con estación | Antes de congelar bastidor |
| M57 | Relaciones de soportes/contactos/ventana IR de estación | Completar M30 con nota electrónica; conservar conjunto original y relacionarlo al marco | Repetibilidad de acoplamiento; no duplicar pinouts | Compartida con electrónica |
| M58 | Envolventes de servicio de limpieza | Depósito, filtro, caja/rodillo, mopa y turbina; dirección de salida y espacio de herramienta | Accesos del diseño y orden de retirada | Durante CAD |
| M59 | Masa de cada módulo y posición sobre marco | Desglose de M31; condiciones con platos/paños/batería; añadir masa real de soporte fabricado | Estimar y comprobar reparto, sin prometer tolerancia de sobrepeso | Durante bastidor |
| M60 | Estados de contacto robot–estación | Registrar por carga/vaciado/lavado/secado qué apoya, qué se mueve y qué interfaz se utiliza realmente | No diseñar todas las funciones sobre una postura supuesta | Integración por fases |

**Paquete inmediato razonable:** M40–M43, M46, M49–M50, M52 y primeras referencias M54–M55, aprovechando M04–M09, M25–M30. Da para un modelo de disposición y un piloto de apoyo. No exige medir a la vez cada carcasa, ni declarar terminada la fuerza de suspensión antes de dibujar sus interfaces. M44 y los estados de trabajo deben resolverse antes de aprobar el cassette para uso, y M51/M56 antes de congelar mopas y fondo.

## 9. Cómo entra en el CAD y qué se comprueba primero

La primera entrega puede contener el marco común y representaciones simples de los conjuntos: volumen ocupado, puntos de montaje conocidos y volúmenes de movimiento/extracción. Cada parámetro pendiente debe conservar ese estado; un valor de conveniencia para visualizar no se exporta como plano de fabricación. La envolvente global de Ø350 × 97 mm es una referencia exterior, no una plantilla para escalar todas las fotos.

Para el primer soporte: asiento repetible, eje recuperado/medido, libertad de giro después del apriete, retención y acceso. Después, colocar ambos apoyos, rueda loca y conjuntos de limpieza en el bastidor para evaluar posiciones relativas, reparto de carga y claros. El núcleo y las interfaces se validan conjuntamente; comprobar una pieza aislada no basta para aprobar el robot.

El orden funcional ya acordado se mantiene: inspección y movimiento sin energía; montaje seguro de conjuntos y pruebas secas de movilidad/detección; acoplamiento y funciones de carga/aire disponibles; finalmente lavado/secado cuando las anteriores y la estanqueidad pertinente estén resueltas. Las órdenes reales pueden agrupar funciones: no se supone un modo de servicio para accionar cada motor por separado. No se añade aquí una campaña nueva de ciclos ni una garantía de vida.

El resultado que merece publicarse después de revisión será el CAD propio, parámetros con procedencia, lista de interfaces y resultados reales. Las fotos privadas sirven de evidencia de trabajo; no tienen que subirse para que el diseño sea abierto.

## 10. Fuentes verificadas y límites de transferencia

Consulta: 25-10-2026. URLs de fuentes originales; no se requieren los identificadores internos del buscador para reutilizar esta nota.

| Ref. | Fuente | Qué respalda |
|---|---|---|
| S01 | https://www.mi.com/sa-en/product/xiaomi-robot-vacuum-x20-pro/specs/ | Modelo D102GL y D102-JZEU, envolventes nominales y masa del producto. |
| S02 | https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/ | Elevación hasta 10 mm, lavado/secado/vaciado y funciones del modelo. |
| S03 | https://www.mi.com/es/support/faq/details/KA-922892/ | Mantenimiento de cepillo/depósito/rueda loca, contactos traseros, ventanas ópticas, acoplamiento y extensor de estación. |
| S04 | https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html | Pasador nominal 4 × 38,5 mm, Pro explícito. |
| S05 | https://www.ep-mediastore-ab.de/xiaomi-radfeder-62x32-45mm-p-37935.html | Dimensiones aproximadas del muelle; Pro explícito. No curva de fuerza. |
| S06 | https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html | Módulo izquierdo, Pro/Max y características de ficha. |
| S07 | https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html | Módulo derecho, Pro/Max y cable de 11,5 cm declarado. |
| S08 | https://www.ep-mediastore-ab.de/xiaomi-wischmotoren-x20-pro-p-29890.html | Pareja de mecanismos de mopa Pro; sensor de presencia de platos según ficha. |
| S09 | https://www.ep-mediastore-ab.de/xiaomi-2x-mop-halter-teller-schwarz-x20max-pro-5pro-p-18142.html | Platos con retención magnética, diámetro aproximado 13 cm y Pro explícito. |
| S10 | https://www.ep-mediastore-ab.de/dreame-d9-l10-frontrolle-halter-schwarz-p-42556.html | Conjunto de rueda loca/soporte, Pro en lista propia de compatibilidad. |
| S11 | https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-x20-p-73385.html | Caja de cepillo con motor/junta; sin rodillo/tapa; Pro en ficha. |
| S12 | https://www.ep-mediastore-ab.de/dreame-seitenbuerstenmotor-schwarz-p-55856.html | Motor/reductora lateral ofrecido para Pro, revisado en inventario anterior. |
| S13 | https://www.ep-mediastore-ab.de/xiaomi-staubbehaelter-x20-pro-weiss-p-50066.html | Depósito exacto Pro, sin filtro, admite estación de vaciado. |
| S14 | https://www.ep-mediastore-ab.de/xiaomi-gummi-tuelle-filter-x20pro-p-66031.html | Pieza de goma/espuma de conexión a turbina Pro; función precisa a contrastar físicamente. |
| S15 | https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html | Conjunto posterior contactos/IR/soporte exacto Pro. |
| S16 | https://www.ep-mediastore-ab.de/xiaomi-x20pro-mop-tray-weiss-p-50064.html | Placa/bandeja de lavado exacta Pro y relación con cubeta de estación. |
| S17 | https://www.leespring.fr/download/Extension_Springs_LeeSpring_US_Eng.pdf | Definiciones de muelle de tracción, tensión inicial, constante, longitud entre ojales y límites del catálogo Lee. No especifica el muelle Xiaomi. |
| S18 | https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 | Consideraciones de diseño, orientación y tolerancias de impresión. No valida una pieza concreta de este proyecto. |

Referencias internas: [inventario fotográfico](10-inventario-fotografico.md), [inventario de catálogo](06-inventario-ampliado-del-robot.md), [mediciones](mediciones.csv) y [plan vigente](07-plan-del-chasis-propio.md). Los apartados antiguos sobre volver a pegar/reparar antes de avanzar no gobiernan este encargo.

**Estado al cerrar esta nota:** hay componentes identificados y una arquitectura candidata, con cotas comerciales limitadas y un plan de recuperación de interfaces. No se han ejecutado medidas físicas, fabricado soportes, probado muelles o validado la geometría de estación. Las decisiones de material, espesor, fijaciones y tolerancias siguen ligadas a esos datos.


---
Documentación original de este proyecto: CERN-OHL-P-2.0. Alcance y exclusiones en [cad/LICENCIAS.md](cad/LICENCIAS.md). Las fuentes y diseños de terceros conservan sus derechos.
