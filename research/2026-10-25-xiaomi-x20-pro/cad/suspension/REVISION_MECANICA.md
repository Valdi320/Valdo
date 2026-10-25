# Revisión mecánica del estudio comparativo de suspensión

25-10-2026. Alcance: arquitectura y coherencia geométrica del estudio editable de lámina/alambre. Referencias: [capítulo 16](../../16-suspension-reproducible.md), [revisión de interfaces](../REVISION.md) y [estudio axial](../estudios/README.md). No es un dimensionamiento resistente ni una aprobación para fabricar.

## Criterios de revisión

| ID | Estado | Condición concreta para el estudio |
|---|---|---|
| R01 | Propuesta | Las dos variantes comparten un marco local explícito, un asiento al núcleo y un eje de pivote comparables. Las separaciones usadas para presentarlas no son posiciones del Xiaomi. Diferenciar superficies que localizan de fijaciones que mantienen el asiento. |
| R02 | Propuesta | Mostrar eje y apoyos sin bloquear el giro del brazo. Separar ancho móvil, apoyo axial, holguras y retención del pasador. El presupuesto anterior de 50 mm no cabe en el nominal comercial de 38,5 mm; tampoco cabe su variante de 42 mm sin salientes. Ninguno de esos números define el espacio real de la rueda. |
| R03 | Pendiente | La unión a la mitad móvil de la rueda necesita una interfaz propia. Un brazo ilustrativo no acredita una zona sana de la carcasa, ni reconstruye un alojamiento de engranajes. Marcar expresamente qué parte es un sustituto geométrico y qué contraparte falta identificar. |
| R04 | Propuesta | En lámina: distinguir tramo sujeto, longitud activa y contacto/unión móvil. En alambre: distinguir anclaje fijo, anclaje móvil y línea de acción. Comparar ambas con el mismo sentido de giro del brazo; no identificar igual apariencia con igual fuerza de retorno. |
| R05 | Propuesta | Mostrar al menos dos estados o permitir cambiar un ángulo común a ambas variantes. Los estados ilustran recorrido; no constituyen una simulación de deformación, fuerza, impacto o contacto. El posible barrido debe incluir el brazo, elemento elástico y salida del cable cuando sus envolventes se conozcan. |
| R06 | Propuesta | Representar por separado la función de los topes y la reserva del detector/cableado. Un volumen reservado no acredita que el detector se accione ni que el cable llegue. Los topes no deben confundirse con una placa, conector o contacto de la lámina. |
| R07 | Pendiente | La extracción del cartucho debe conservar pivote, retención y elemento elástico dentro de un conjunto controlado. Mostrar ruta o volumen de extracción conceptual y reservar el servicio axial del pasador en banco. Una vista desplazada o explosionada no demuestra contención de energía; el mecanismo y la secuencia siguen por diseñar. |
| R08 | Pendiente | Recuperar la posición al reinstalar exige localizar el cartucho y mantener esas referencias bajo apriete. La imagen de un asiento, dos tornillos o un material más grueso no acredita repetibilidad, carga admisible ni vida útil. |

## Qué se puede aprobar en esta entrega

- Coherencia de referencias, giro, transmisión conceptual y separación de funciones.
- Editabilidad de relaciones y procedencia visible de parámetros de ejemplo.
- Ausencia de una colisión conceptual evidente en los estados efectivamente representados.

Siguen pendientes material, dimensiones funcionales, ajustes, precarga, curva de fuerza, deformación de contacto, resistencia, fatiga, contención de energía y compatibilidad con los módulos y la estación. Esos pendientes no impiden desarrollar el estudio provisional.

## Registro de revisión

- Documentación precedente y presupuesto axial: leídos.
- Criterios R01–R08: comunicados al autor del generador antes de terminar el modelo.
- Generador `crear_estudio_suspension.py` y su README: **revisados estáticamente**, incluida la corrección del anclaje móvil de alambre.
- Representación ejecutada: **inspeccionadas las cuatro vistas** de comparación, lámina, alambre y extracción de `vistas/`. La integración comprueba generación, reapertura y persistencia por separado; esta inspección no repite esas pruebas.
- Ensayos físicos y pruebas en el PC: **no realizados en esta revisión**.

### Resultado de la revisión estática

**Sin otra objeción mecánica material para el alcance conceptual, después de corregir una interferencia.**

Se observa en el código que asiento, apoyos y pivote usan las mismas relaciones en ambas variantes; el brazo gira alrededor de ese pivote y sus marcadores siguen el mismo contenedor. Las dos posiciones no se presentan como carrera admisible. El sector sólo representa el barrido del segmento longitudinal central del brazo: excluye el desplazamiento del anclaje bajo el brazo, sus reservas y el volumen barrido de todo el conjunto. El presupuesto inicial de 40/42 mm frente a 38,5 mm sigue mostrando incompatibilidad de esas sumas, sin alterar el nominal para disimularla.

La primera versión situaba el marcador de alambre en el centro del extremo del brazo: el segmento de tracción atravesaba parte del sólido ilustrativo. Se comunicó al autor y se corrigió con `AlambreMovilBajo`, un desplazamiento visual bajo el brazo. Marcador, reserva y fórmulas del segmento aplican la misma transformación. En los dos estados iniciales el segmento queda bajo el brazo y su longitud aumenta al elevarlo, coherente con un retorno por tracción si el resorte se mantiene tensionado. No se ha diseñado una orejeta ni acreditado la carga local.

La lámina permanece plana y su contacto sigue pendiente. Las reservas de topes y retención no se presentan como mecanismos terminados. La escena de extracción mantiene el objetivo de contener energía expresamente pendiente; mover sólidos en pantalla no lo resuelve. El asiento, el detector, el cableado y la mitad móvil dañada conservan sus límites documentados.

### Resultado de la inspección visual

**Sin nueva objeción mecánica visible para el estudio conceptual.** Las cuatro capturas muestran el asiento y pivote comunes, los dos estados del brazo y la separación entre piezas y reservas. La lámina está plana por encima del brazo, sin fingir que el contacto o su deformación estén resueltos. En alambre se distingue el marcador móvil bajo el brazo, coherente con la corrección revisada. La escena de servicio separa el cartucho del asiento y muestra otro estado del pasador sobre su eje; representa una propuesta de acceso, no una maniobra de desmontaje ya validada.

La perspectiva y las transparencias no permiten certificar holguras ni ausencia de interferencias en todo el recorrido. La inspección no cambia los estados pendientes R03, R07 y R08 ni adjudica resistencia o capacidad de fabricación. El ajuste de encuadre y la retirada de anotaciones superpuestas se gestionan como presentación, sin cambio geométrico.
