# CAD editable — X20 Pro abierto, base propia

**Geometría del maestro: revisión 0.1; vínculos documentales actualizados el 25-10-2026.** Abrir **[X20Pro_Base_Arquitectura.FCStd](X20Pro_Base_Arquitectura.FCStd)** en FreeCAD. Es el maestro editable del proyecto. FreeCAD **1.1.4** se ha instalado y ejecutado en el equipo del propietario mediante el paquete de usuario de Flathub.

Esta revisión contiene referencias e interfaces para empezar el diseño y un estudio independiente de cartucho. **Todavía no contiene una base adaptada a las medidas del robot ni piezas aprobadas para fabricar.** No se ha modelado un robot interior ficticio a partir de fotografías sin escala.

La [actualización de coordinación](../coordinacion/revision_suspension_codex.md) comunica la preferencia posterior del propietario: las operaciones automatizadas nuevas de FreeCAD en el PC se ejecutarán sin interfaz gráfica. Las pruebas y capturas gráficas descritas en esta entrega son anteriores a recibir esa actualización; se conservan como evidencia de lo que se ejecutó.

## Documentos de estudio actuales

El [estudio comparativo de suspensión v0.3](suspension/README.md) es otro FCStd: compara lámina y alambre, dos estados del brazo y una extracción conceptual. Tiene 23 comprobaciones nativas de software superadas y geometría propia sin cotas físicas validadas. Los [estudios de implantación](estudios/README.md) recogen la restricción axial y la aportación del asiento desmontable. Mantener estos documentos separados evita interpretar sus coordenadas gráficas como posiciones internas del Xiaomi.

El maestro incorpora **IF02→M15 por lado** y **IF04→IF13/M55/M60** tanto en [interfaces.json](interfaces.json) como en sus registros nativos. Se verificaron las cinco propiedades modificadas, la arista IF04→IF13 y la conservación íntegra de formas, mapas y demás datos ajenos al cambio. La reapertura nativa confirmó los vínculos. [Resultado y procedimiento](suspension/validacion_software.json). La comprobación original de v0.1 que se cita más abajo es histórica y conserva su hash original.

## Qué contiene

| Grupo de FreeCAD | Contenido real |
|---|---|
| `00 · LEER` | Objetivo, estado, convención de ejes, límites y licencia |
| `01 · Referencias` | Envolvente exterior publicada Ø350 × 97 mm y tabla nativa de esos dos datos |
| `02 · Módulos observados` | 13 registros de conjuntos identificados, con referencias y fotografías; geometría pendiente |
| `03 · Interfaces críticas` | 14 relaciones de montaje/función, medidas necesarias y evidencia |
| `04 · Bastidor resistente` | Decisión de arquitectura; forma, espesores y recortes pendientes de implantación |
| `05 · Extracción y barridos` | Requisitos de acceso para ruedas, batería, electrónica, limpieza y sensores |
| `90 · DEMO` | Estudio paramétrico independiente: placa, dos apoyos, dos casquillos, pasador y anclaje fijo de muelle |

La envolvente representa el límite exterior publicado del producto completo, **no la base interna ni todo el espacio utilizable**. Su plano inferior abstracto no es una medida del suelo. X/avance, Y/izquierda y Z/arriba son una convención propuesta; la transformación al ejemplar físico depende de M40.

Los módulos sin medida son registros sin sólidos ni posiciones simuladas. En el árbol se pueden seleccionar para consultar sus propiedades. Una ausencia geométrica tiene aquí significado: falta una medida. No equivale a una pieza de tamaño cero.

## Estudio de cartucho

![Estudio de cartucho — dimensiones ilustrativas, no fabricar](vistas/DEMO_cartucho_NO_FABRICAR.png)

Gris: placa del cartucho y pasador. Turquesa: dos apoyos independientes. Dorado: asientos/casquillos reemplazables ilustrativos. Naranja: anclaje fijo de muelle desmontable. Los colores identifican funciones, no materiales aprobados.

Todas sus dimensiones son **DEMO**, incluida la placa de 3 mm y el pasador de 5 mm. El pasador se eligió deliberadamente distinto de la referencia comercial Ø4 × 38,5 mm; no se deben intercambiar esos valores para intentar fabricar esta pieza. No están resueltos la retención, la tornillería, los ajustes, la fuerza del muelle, el detector, los topes ni la fijación al bastidor. La geometría de la rueda móvil no está representada.

La pieza ilustra cómo separar los soportes pequeños de la estructura grande. **No repara por sí sola un alojamiento o un gancho roto de la carcasa móvil.** Esa mitad de la interfaz se debe identificar y medir por separado.

El conjunto DEMO se encuentra fuera de la envolvente del robot, a partir de X=250 mm, para impedir que su posición se interprete como un montaje Xiaomi.

## Cómo trabajar con el archivo

1. Abrir el FCStd. Expandir primero `00`, `02` y `03` para consultar el alcance y los datos pendientes.
2. Para ver el estudio grande, ocultar `EnvolventeReferencia` seleccionándola y pulsando Espacio. Ajustar la vista con **V, F** o el comando de ajustar todo de FreeCAD.
3. Abrir la hoja `ParametrosDEMO`. La celda B2, alias `Hueco`, controla la distancia entre apoyos. Cambiar 26 a 30 mm actualiza el apoyo B, la placa y el pasador. Todos estos valores siguen siendo ilustrativos.
4. Para incorporar medidas reales, crear un grupo/pieza específico vinculado al registro de interfaz y a su evidencia. Mantener el estudio DEMO como referencia separada; no convertir sus números en cotas medidas cambiando una etiqueta.
5. Guardar el maestro y actualizar la documentación y el registro de medidas en la misma revisión Git. Usar STEP como derivado, nunca editarlo a la vez como otra definición del bastidor.

No hay complementos externos, mallas opacas ni un `Proxy` Python ejecutable del que dependan las piezas. La geometría utiliza primitivas, operaciones booleanas y expresiones nativas de FreeCAD. Los registros sin geometría almacenan propiedades de texto.

## Reproducir la revisión inicial

`scripts/crear_modelo.py` construye **la geometría v0.1**, leyendo el registro de interfaces vigente. La revisión actual del script añade también sus vínculos y procedencia documental. `crear_proyecto.FCMacro` permite escoger una carpeta nueva y ejecutarlo desde FreeCAD. La estructura de `cad/` y el CSV `../electronica-modulos.csv` deben conservarse juntos.

El generador se niega a sobrescribir un FCStd existente. Para continuar el proyecto se edita el maestro. Regenerar v0.1 no sustituye las modificaciones posteriores del CAD. El render requiere el contexto gráfico de escritorio; un proceso sin OpenGL puede construir sólidos y producir una captura en blanco.

El script puede crear el documento en otra carpeta, comprobarlo y exportar el estudio. No se conecta al robot, no instala complementos y no modifica firmware.

## Comprobaciones hechas y límites

Registro reproducible del resultado: [validacion_cad.json](validacion_cad.json). Se comprobaron los sólidos, la envolvente publicada, la dependencia paramétrica de `Hueco`, el guardado y la reapertura del FCStd. El STEP se volvió a importar para contrastar siete sólidos y sus dimensiones de estudio. Las capturas se inspeccionaron visualmente después de generarlas con el contexto gráfico de escritorio.

No se ha medido el ejemplar, realizado análisis estructural, probado ajustes, fabricado componentes ni validado resistencia, fatiga, estanqueidad o estación. La ausencia de error geométrico en FreeCAD no demuestra esas propiedades.

La revisión independiente está en [REVISION.md](REVISION.md). [interfaces.json](interfaces.json) mantiene los requisitos y vínculos Mxx, con `null` o texto pendiente en lugar de cotas inventadas. [LICENCIAS.md](LICENCIAS.md) delimita el diseño abierto propio y las dependencias de terceros.

## Siguiente entregable

**Primer cartucho adaptado a una rueda real, con una referencia global recuperable y ruta de extracción comprobable.** Necesita identificar qué está roto en la parte fija y móvil, recuperar eje/contracaras y medir M41–M43. La fuerza y geometría de suspensión M44 deben resolverse antes de aprobar uso, aunque se puede comenzar el soporte local antes.

No depende de recuperar fragmentos descartados ni de comprar una impresora. El capítulo [14](../14-entrega-cad-y-siguiente-medicion.md) da el paquete de captura y la coordinación del checkout.
