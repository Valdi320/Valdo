# 17 — Suspensión paramétrica, asiento desmontable y vínculos del maestro

**25-10-2026 · Entrega CAD comprobada; sin aprobación de fabricación.** El requisito de fabricar también la función elástica ya tiene un estudio FreeCAD editable. Compara lámina y alambre, muestra dos posiciones del brazo y una extracción conceptual. Se integra además el asiento desmontable preparado por Codex y se completan las relaciones documentales pendientes del maestro.

## 1. Qué se puede abrir y editar

| Archivo nativo | Para qué sirve | Estado comprobado |
|---|---|---|
| [Suspensión conceptual v0.3](cad/suspension/X20Pro_Suspension_Conceptual.FCStd) | Comparar las dos arquitecturas, cambiar ángulo, apoyos y separación de servicio | 23 comprobaciones nativas, guardado y reapertura; cuatro capturas inspeccionadas. |
| [Asiento desmontable A](cad/estudios/X20Pro_Asiento_Desmontable_DEMO.FCStd) | Separar superficies de apoyo/localización de las fijaciones y estudiar la salida de la placa | Aportación de Codex con 16 comprobaciones registradas; archivo y capturas contrastados al integrar. |
| [Presupuesto axial v0.3](cad/estudios/X20Pro_Estudio_Axial_Publicado.FCStd) | Explorar dimensiones sin modificar el nominal de catálogo conservado | Corrección de Codex con 24 comprobaciones de macro, seis del archivo entregado y control negativo en copia. |
| [Maestro de arquitectura](cad/X20Pro_Base_Arquitectura.FCStd) | Mantener módulos, interfaces y referencias del robot | Cinco propiedades documentales actualizadas; formas y otros datos conservados; reapertura nativa correcta. |

Los documentos son independientes. Sus posiciones en pantalla no forman un ensamblaje del interior del Xiaomi. La base completa, el módulo real de rueda y las contrapartes de la estación siguen sin tener geometría interna medida. Las piezas rotas descartadas no son un requisito para continuar.

![Comparación nativa de lámina y alambre; hipótesis visuales, no fabricar](cad/suspension/vistas/suspension_comparativa.png)

*Lámina arriba a la izquierda; reserva de alambre abajo a la derecha. Los colores distinguen funciones, no materiales aprobados. Las cajas y contornos representan reservas; no son mecanismos de retención terminados.*

## 2. Qué permite estudiar la suspensión

Ambas variantes usan el mismo marco local para comparar asiento, pivote y brazo. La hoja `HipotesisVisuales` contiene las dimensiones de ejemplo y su procedencia. El brazo de muestra gira alrededor del mismo eje que el brazo de referencia; el marcador y sus reservas se mueven solidariamente. La geometría y las expresiones son nativas de FreeCAD, sin un complemento de ensamblaje ni un programa externo necesario para mantener las formas.

El generador deja un ángulo de muestra de 15°, una hipótesis gráfica. Se comprobó que cambiarlo a 20° actualiza el brazo, marcador, sector y línea de alambre, y que volver al valor inicial conserva las relaciones. Ese intervalo no es un recorrido admisible del robot. El sector sólo representa el segmento longitudinal central del brazo; excluye el espesor completo y el desplazamiento del anclaje inferior.

La lámina sigue **plana**. Su contacto, longitud activa, flexión y precarga no están resueltos. En alambre se representa la relación entre anclajes y su reserva, sin dibujar una hélice que aparente estar dimensionada. La primera revisión detectó que el segmento atravesaba el brazo; se corrigió colocando el marcador bajo él y aplicando su transformación también a las expresiones. Esa corrección no diseña una orejeta resistente ni acredita el anclaje al módulo conservado.

El pasador Ø4 × 38,5 mm procede de una declaración comercial [S1]. El hueco de 26 mm continúa siendo DEMO. Con apoyos de 3 mm y reserva de 4 mm por extremo, la suma inicial es 40 mm; con apoyos de 4 mm es 42 mm. Ambas exceden el nominal. Se conserva la restricción visible: ni se alarga el pasador presentado como publicado ni se reduce una anchura real desconocida para aparentar encaje. Un presupuesto aritmético favorable tampoco demostraría tolerancia, retención o resistencia.

## 3. Qué aporta el asiento de Codex

El asiento A representa una placa apoyada en tres zonas. Un alojamiento redondo y una ranura orientan su localización; las fijaciones tienen otra función, mantener el contacto. El archivo permite apartar las fijaciones y elevar la placa. Sus números son DEMO y no determinan la orientación del cartucho dentro del robot.

Codex comprobó el barrido continuo de **esa placa**, utilizando su perfil inferior perforado y verificando que corresponde a una sección constante. El resultado no cubre rueda, suspensión, cables, herramientas ni la retirada de las fijaciones. Tampoco diseña todavía roscas, contrapieza de apriete, raíz de los localizadores o repetibilidad bajo carga. El [README del asiento](cad/estudios/README.md) explica las poses y el alcance de las 16 comprobaciones.

La revisión conjunta concreta tres uniones independientes:

1. **Cartucho–núcleo:** permite extraer el conjunto pequeño para mantenimiento.
2. **Mordaza o fijación del elemento elástico:** permanece cerrada mientras se retira el cartucho.
3. **Retén del pivote:** mantiene el conjunto móvil contenido durante esa operación.

En banco deberá existir una forma diseñada de contener la rueda y descargar el elemento elástico antes de liberarlo. Aflojar su raíz bajo carga no es una secuencia de descarga. El estudio de extracción actual muestra el objetivo y el espacio conceptual; todavía no resuelve ese mecanismo.

Para el accionamiento manual, Codex propone comparar primero pomo cautivo y palanca con seguro, manteniendo el cuarto de vuelta como alternativa. Es una investigación de funciones y accesibilidad, recogida con fuentes en su [revisión de integración](coordinacion/revision_suspension_codex.md). **No se han modelado ni validado esos cierres en el asiento entregado.** Añadir elementos cautivos exige revisar su propio barrido; no hereda automáticamente la salida de la placa con fijaciones apartadas.

## 4. Maestro actualizado sin modificar su geometría

La revisión precedente dejó dos vínculos documentales pendientes. Ya están incorporados tanto a `cad/interfaces.json` como a las propiedades nativas:

| Interfaz | Cambio | Propósito |
|---|---|---|
| IF02 | Añade M15 por lado y procedencia | Registrar el ajuste del pivote de cada conjunto, sin asumir que ambas ruedas son equivalentes. |
| IF04 | Añade M55/M60, enlace nativo a IF13 y procedencia | Relacionar rodadura y reinstalación con las condiciones de apoyo y acoplamiento de la estación. |

La modificación comprende cinco propiedades y la dependencia nativa derivada IF04→IF13. Se generaron los metadatos con FreeCAD sobre una copia, se verificó su diferencia completa y se conservaron íntegros los demás miembros del original, incluidos sus 51 archivos de formas/mapas. La copia final se abrió en FreeCAD 1.1.4 y confirmó los vínculos. El [registro de software](cad/suspension/validacion_software.json) contiene hashes, comparadores y alcance. La revisión geométrica continúa siendo 0.1; `mediciones.csv` conserva su revisión publicada en adf76aba.

El estudio axial de Codex incorpora además una mejora de trazabilidad: los nominales de fuente son propiedades conservadas y los escenarios se editan por separado. Su comprobador ahora incluye la preservación de archivos en el resultado global. Los registros del compañero se mantienen atribuidos a su ejecución y a los hashes de su checkout histórico; no se presentan como pruebas nuevas sobre nuestro maestro actualizado.

## 5. Qué se ha comprobado y qué queda abierto

La ejecución del estudio de suspensión en FreeCAD 1.1.4 verificó 223 objetos, de los que 199 exponen una `Shape` válida. Ese recuento incluye auxiliares y contenedores; no son 199 piezas físicas. Las 23 comprobaciones cubren expresiones, unidades angulares, respuesta a cambios de ángulo/apoyo/extracción, restauración, guardado y reapertura. El [registro detallado](cad/suspension/validacion_software.json) contiene cada resultado.

La copia final conserva los datos y geometría del modelo probado; sólo cambian dos visibilidades de anotaciones y la cámara. Sus 121 archivos BREP/mapa permanecen idénticos. En algunas exportaciones se observó recorte gráfico intermitente, por lo que se seleccionaron e inspeccionaron cuatro PNG completos de dos exportaciones de esa misma geometría. Se documenta esta limitación del render; que una captura se guarde sin excepción no basta para aceptarla.

No se han ensayado piezas ni calculado una vida útil. Siguen pendientes material, proceso, contacto, curva fuerza–posición, estabilidad bajo precarga, fatiga, retención, topes, detector, cables y comportamiento con la estación. Una lámina fabricable a partir de material especificado sigue siendo la primera candidata, condicionada por esas comprobaciones. El alambre se mantiene como alternativa; el muelle comercial disponible no condiciona el diseño abierto.

## 6. Próximo bloque de trabajo

El siguiente paso geométrico es adaptar el cartucho al asiento y resolver la contraparte móvil conservada, con una referencia de inserción de lámina y un mecanismo explícito de contención/descarga. Después debe incorporarse al barrido el conjunto completo, con cable y acceso manual. Las hipótesis que afecten a compatibilidad se sustituirán por evidencia dimensional identificada; no por escalado visual de fotos.

La consulta dimensional ya enviada al proveedor permanece a cargo del compañero Codex. No se duplica el contacto. La [nota de entrega coordinada](coordinacion/entrega_suspension_cad_v03.md) identifica los archivos vigentes y el reparto para continuar sin pisar trabajo.

## Referencias

- **S1:** [PC:MediaStore, pasador SKU12584, Ø4 × 38,5 mm](https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html). Fuente del nominal comercial; no aporta tolerancia ni longitud útil certificada.
- [Suspensión reproducible: criterio y fuentes](16-suspension-reproducible.md).
- [Revisión mecánica independiente del estudio](cad/suspension/REVISION_MECANICA.md).
- [Revisión de interfaces y servicio](cad/REVISION.md).
- [Aportación de Codex: asiento, uniones y cierres manuales](coordinacion/revision_suspension_codex.md).

Documentación y CAD originales bajo [CERN-OHL-P-2.0; scripts propios MIT](cad/LICENCIAS.md), con el alcance y las exclusiones de terceros allí indicados.
