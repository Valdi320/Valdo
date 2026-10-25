# Plan de trabajo: mejorar sin inmovilizar el robot durante el diseño

Fecha: 25/10/2026. Todas las acciones de esta página son **propuestas de ingeniería (E4)**. La investigación pública ha terminado; las mediciones y pruebas de la unidad real siguen pendientes.

## 1. Resolver la incógnita que bloquea el diseño

La primera entrega física no debe ser un chasis completo. Debe ser una identificación inequívoca del apoyo roto y un pequeño conjunto de medidas que permitan diseñar una solución.

Fotografías útiles, con luz lateral y una regla en el mismo plano cuando sea posible:

1. Vista de contexto que incluya rueda, pasador y ambos extremos del muelle.
2. Primer plano de la fractura por delante y por detrás.
3. Pieza fija y móvil en dos posiciones de suspensión, para distinguir a qué cuerpo pertenece el apoyo.
4. Apoyo sano equivalente, si existe; no asumir que los dos lados son simétricos.
5. Espacio detrás de la zona donde podría ir un refuerzo, mostrando cables y partes móviles.
6. Marcaje de polímero y referencias del módulo, sin necesidad de publicar números de serie.

Las fotografías se pueden mantener privadas. En el repositorio público basta documentar cotas, dibujos propios y resultados sin datos personales.

## 2. Preparar una intervención con resultado concreto

| Etapa | Trabajo fuera del robot | Trabajo que exige acceso | Condición para terminar |
|---|---|---|---|
| Identificación | Revisar fichas y las imágenes ya disponibles | Ver la fractura si aún no está accesible | Se sabe si pertenece a chasis, módulo o gancho |
| Medición mínima | Preparar tabla, referencias y herramientas | Medir apoyos, pasador, recorrido y espacio sano | Cotas críticas registradas con condición de medida |
| Restauración | Tener recambio o reparación concreta disponible | Sustituir/reparar la zona definida | Movimiento y funciones comprobados; aparato cerrado |
| Diseño de mejora | CAD, cupones y comparación en banco | Ninguno, si las medidas son suficientes | Encaje y fijación del prototipo entendidos |
| Instalación del prototipo | Preparar tornillería, orientación y montaje | Montar sólo la mejora prevista | No requiere forzar, bloquea ni altera interfaces |
| Seguimiento | Registrar uso y observaciones | Inspección accesible cuando sea necesaria | No hay evolución de grieta, juego o deformación |

Si el robot ya está averiado, el primer objetivo es restaurarlo. La estrategia de cerrar y seguir utilizándolo sólo se aplica después de comprobar que la reparación es funcional; no implica volver a usar una suspensión incompleta o bloqueada.

No se promete un tiempo exacto de desmontaje: faltan la revisión concreta y el mapa de fijaciones. El objetivo de diseño es que **cada apertura tenga las piezas preparadas y una tarea definida**, y que una sustitución futura no requiera retirar electrónica o aspiración sin necesidad.

## 3. Medidas de la primera sesión

La [plantilla CSV](mediciones.csv) deja los valores reales en blanco. Las dimensiones de catálogo están en otra columna y no sustituyen mediciones.

| Prioridad | Dato | Utilidad inmediata |
|---|---|---|
| 1 | Cuerpo al que pertenece la rotura; grieta y material sano | Decide recambio, puente, anclaje o reconstrucción |
| 1 | Pasador: diámetro, longitud, extremos y retención | Define qué debe alojar y liberar el soporte |
| 1 | Alineación y separación de los apoyos | Conserva el eje de basculación |
| 1 | Espesor útil y cara posterior de una posible fijación | Decide si existe una base para repartir carga |
| 1 | Espacio barrido por rueda, muelle y cables | Descarta interferencias antes de fabricar |
| 1 | Posición de ambos anclajes del muelle | Mantiene palanca y longitud de trabajo |
| 2 | Estado del detector de rueda levantada y topes | Conserva detección y recorrido |
| 2 | Material identificado, tornillos y acceso de herramientas | Ayuda a elegir fabricación y mantenimiento |
| 3 | Sensores, estación, masas y envolvente completa | Sólo necesario cuando se amplía a un chasis propio |

Para establecer ejes, usar X hacia delante, Y hacia la izquierda del robot en su posición normal y Z hacia arriba. Elegir superficies sanas y accesibles. Un valor debe registrar instrumento, dispersión observada y condición de carga. No asignar ±0,01 mm por el mero hecho de que el calibre muestre centésimas.

## 4. Primera pieza que merece modelarse

Un portapivote reemplazable puede descomponerse en cuatro funciones:

- **Posición:** asiento que conserve el centro y la dirección del eje.
- **Carga:** base amplia que transmita esfuerzo a material sano.
- **Desgaste:** alojamiento o casquillo que permita el giro previsto y pueda sustituirse.
- **Servicio:** fijaciones y retención accesibles sin retirar módulos ajenos.

El anclaje del muelle se trata aparte cuando sus cargas y posición lo aconsejen. La disposición concreta depende de lo medido; no se elige de antemano una broca, un tornillo M3 o un espesor de chapa.

**Regla para bridas y pegamento:** pueden ayudar a presentar o contener piezas dentro de un mismo cuerpo, pero no deben amarrar el brazo basculante al chasis ni sustituir el muelle. Una pieza pegada necesita conservar el movimiento y las cotas para cumplir su función. El apartado de Ceys describe las limitaciones de la ficha técnica, sin afirmar que todo adhesivo esté prohibido.

## 5. Entregables de CAD antes de montar

| Archivo o dato | Contenido mínimo |
|---|---|
| Modelo nativo editable | Parámetros con nombres y relaciones, sin depender únicamente de una malla |
| STEP | Geometría de intercambio; no reemplaza la historia paramétrica |
| STL o 3MF | Malla derivada de la revisión correcta |
| Dibujo | Referencias, interfaces funcionales y dimensiones aún pendientes |
| Lista de piezas | Material, herrajes comerciales y componentes originales reutilizados |
| Fabricación | Orientación, material exacto, proceso y parámetros relevantes |
| Verificación | Qué encaja, qué se mueve, qué se ensayó y con qué resultado |
| Mantenimiento | Orden de retirada, útiles y número de piezas ajenas que hubo que desmontar |

Un archivo STL sin dimensiones, material y montaje no es todavía un repuesto reproducible. Para las primeras pruebas, imprimir sólo el asiento o agujero necesario ahorra material y tiempo.

## 6. Comprobaciones proporcionadas al cambio

Antes de tocar módulos eléctricos, apagar el equipo fuera de su base y desconectar la batería por el conector cuando se abra el acceso correspondiente. Se conserva el pack cerrado y no se interviene en la alimentación de red de la estación.

Con batería desconectada: comprobar retención del pasador, giro y basculación libres, retorno por el muelle, topes, accionamiento del detector y ausencia de roce/tensión de cables. No aprobar una pieza que sólo encaje deformando el conjunto.

Una vez montado: comprobar avance/giro y ausencia de avisos, después entrada/salida de base y carga. Si se ha alterado una estructura que afecta a mopas o conductos, comprobar además lavado, elevación y vaciado. Los sensores de caída se comprueban sin exponer el aparato a un borde desde el que pueda caer.

Durante uso representativo: observar juego, grietas, desgaste, aflojamiento y pérdida de posición. No se fija una cantidad arbitraria de ciclos que garantice vida útil. Anotar horas, superficie, obstáculos y cambios observados permite comparar revisiones.

La resistencia y la reparabilidad son resultados distintos: una pieza puede aguantar y seguir siendo difícil de cambiar. Registrar **tiempo real de intervención, herramientas, fijaciones y módulos ajenos retirados** permite comprobar la mejora que más interesa en este proyecto.

## 7. Decisiones económicas antes de ampliar

Para cada revisión, registrar por separado:

1. Repuestos comprados y piezas recuperadas.
2. Fabricación propia o precio de servicio, con material y orientación definidos.
3. Herrajes y consumibles.
4. Transporte.
5. Iteraciones fallidas.
6. Horas de trabajo y horas sin robot utilizable.

El precio de una impresión no puede estimarse responsablemente a partir de una foto. Una vez exista el CAD, el laminador permite conocer masa y tiempo; un taller puede cotizar esa pieza concreta. No hay que comprar un escáner para empezar a medir dos apoyos ni una impresora para comparar alternativas.

**Condición para pasar a B:** la ruta A ha devuelto uso al equipo y hay datos suficientes para diseñar fuera de él. **Condición para pasar a C:** el primer soporte se ha fabricado, montado, usado y vuelto a desmontar con una ventaja comprobable. Una ambición mayor no justifica volver a dejarlo semanas desarmado.

La hoja [registro-intervenciones.csv](registro-intervenciones.csv) está vacía a propósito: ningún ensayo físico se presenta como ejecutado durante esta investigación.
