# Revisión del CAD inicial de implantación

25-10-2026. Revisión de la propuesta comunicada por el coordinador; no se ha abierto ni modificado el CAD. Dato actualizado: el coordinador ha comprobado FreeCAD 1.1.4 en el PC y el checkout real del proyecto. La ausencia de FreeCAD en el entorno de investigación, indicada en el informe anterior, no describe ese PC.

## Dictamen

**La entrega propuesta es útil y honesta:** FCStd nativo con envolvente exterior oficial, catálogo de módulos/interfaces pendientes y estudio paramétrico de cartucho separado. No hace falta dibujar un bastidor completo con posiciones ficticias para comenzar el proyecto.

El modelo debe permitir contestar qué se conserva, qué se medirá, qué condición determina cada soporte y qué parte es solo una demostración. Un árbol de nombres vacío sería insuficiente; una tabla de interfaces vinculada a los objetos lo vuelve operativo.

## Objetos y datos mínimos

| Elemento | Contenido mínimo útil |
|---|---|
| Control del documento | Revisión, fecha, unidades, propósito, estado conceptual y lista de comprobaciones realmente realizadas. |
| Envolvente publicada | Referencia Ø350 × 97 mm, fuente Xiaomi y etiqueta de envolvente exterior del producto completo. No interpretar 97 mm como espesor de la base o altura libre interior. |
| Referencias geométricas | Convención X avance/Y izquierda/Z arriba y origen del documento explícito. Todavía no es un eje de rodadura ni un plano de suelo recuperado de la unidad. Registrar después la transformación al marco funcional medido. |
| Módulos conservados | Objeto por conjunto real, ID, función, fotos de referencia por ID, estado mecánico y estado funcional separados. Las posiciones desconocidas quedan pendientes, sin cajas de tamaño inventado colocadas en el origen. |
| Registro de interfaces | Para cada pareja: plano/eje/agujeros de montaje, movimiento permitido, espacio de cable/herramienta, dato pendiente y método de obtenerlo. Por ejemplo, rueda–cartucho y cartucho–bastidor son interfaces diferentes. |
| Parámetros y mediciones | Separar valor publicado, medido y propuesto; unidad, fuente, condición de medida y estado. Una celda pendiente no vale cero. Las expresiones de piezas reales no deben tomar datos DEMO como sustitutos. |
| Estudio independiente | Grupo propio y rótulo visible `DEMO — NO FABRICAR`, con todas las dimensiones de ejemplo identificadas y sistema de coordenadas local. Su desplazamiento fuera de la envolvente es de presentación, no una ubicación propuesta en el robot. |

La función de cada grupo puede registrarse en propiedades y en una hoja del documento. No hace falta modelar placas, tornillos ni chips con detalle antes de medir sus interfaces. Para publicar, bastan referencias F001–F018; no incluir fotos privadas, códigos individuales ni rutas personales incrustadas.

## Cuatro objeciones que debe superar el cartucho

1. **Doble apoyo no identifica el mecanismo real.** Falta confirmar si el pasador queda fijo en el chasis, gira en el módulo o se retiene de otro modo. El estudio debe mostrar una articulación conceptual, sin afirmar ajustes o casquillos originales. No sujetar el pasador rígidamente en todos los elementos ni convertir el apriete del puente en una mordaza sobre la carcasa móvil.
2. **El ancho ocupado importa tanto como el diámetro.** Los dos apoyos, la retención y cualquier casquillo consumen longitud del pasador y espacio lateral. Vincular ambos centros a un eje común en el DEMO, pero mantener explícitos ancho entre caras, apoyo axial, acceso de extracción y espacio de movimiento. Que los agujeros coincidan en CAD no demuestra coaxialidad tras fabricar/apretar.
3. **El anclaje fijo no repara una rotura móvil.** Dos soportes más puente y enganche de muelle resuelven una arquitectura del lado fijo. Si el gancho o alojamiento perdido pertenece a la carcasa móvil de la rueda, necesita otra interfaz/pieza. Dejarla registrada como pendiente; no presentar el estudio como reparación integral de ambas averías.
4. **El muelle, los topes y el detector forman parte del conjunto.** El punto del anclaje cambia brazo de palanca, fuerza y recorrido. El DEMO puede hacer visible esa dependencia, pero no fijar una posición como compatible. Reservar en el registro el barrido de rueda, paso de cable, acción del detector que se identifique y función de los topes. No transformar un detector en tope mecánico ni asumir que una geometría más rígida preserva el comportamiento.

El puente deberá transferir carga hacia el bastidor futuro; todavía falta esa unión. Un soporte muy rígido que termine en una fijación débil solo traslada el fallo. No se deduce resistencia superior o vida útil del aspecto del estudio.

## Validación proporcionada de esta entrega

Guardar y reabrir el FCStd; cambiar una dimensión DEMO significativa y comprobar que los dos apoyos, el puente y las relaciones previstas se actualizan sin perder su eje conceptual. Verificar unidades, árbol, propiedades y ausencia de errores geométricos relevantes. Esto demuestra editabilidad del estudio, no compatibilidad o resistencia del diseño final.

El archivo debe abrir mostrando claramente la distinción entre referencia oficial, objetos pendientes y estudio ilustrativo. Si se produce una captura o exportación del DEMO, conservar esa identificación en el acompañamiento; el nombre del grupo por sí solo se pierde fácilmente en STEP o en una imagen.

## Próximo paso que desbloquea geometría real

Medir contrapartes supervivientes: módulo de rueda y caras que debe alojar, pasador y retención, relación entre pivote y rueda, anclaje móvil conservado o zona que lo perdió, y referencias estables de los conjuntos vecinos. En paralelo, elegir un sistema de medida reproducible para recuperar la implantación global. No pedir fragmentos desaparecidos ni derivar coordenadas de fotos sin escala.

Con esos datos se sustituye una interfaz pendiente por geometría medida. El DEMO puede permanecer como estudio separado; no tiene que convertirse automáticamente en la solución adoptada.


Implementación: los límites figuran en los objetos Alcance/LimitesCartucho y en interfaces.json. La validación de archivo se registra en validacion_cad.json; no incluye ensayos físicos.


## Revisión del código y del registro implementado

El frente de mecánica revisó `scripts/crear_modelo.py` e `interfaces.json`. Confirmó que los riesgos de mitad móvil rota, posición ficticia, giro/retención, pinzamiento, espacio de extracción, muelle mayor y validación física quedan explícitos. No encontró una objeción adicional que impidiese entregar v0.1 como estudio. No recomendó añadir rueda, retenes, muelle, detector o topes inventados para completar el aspecto.

La inspección de las primeras vistas detectó que el desplazamiento fuera de la envolvente no se aplicaba porque FreeCAD devuelve `.Placement.Base.x` con punto inicial. El coordinador corrigió el generador y el documento; la reapertura y la reimportación STEP confirmaron X mínimo 250 mm. Se sustituyó asimismo el render inicial sin contexto OpenGL por capturas del escritorio y se inspeccionaron. El cambio corrige representación y editabilidad, no valida resistencia.
