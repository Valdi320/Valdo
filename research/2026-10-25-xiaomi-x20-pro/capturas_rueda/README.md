# Captura opcional de una rueda y su pasador

Versión 0.2, 25-10-2026. Esta herramienta conserva una comprobación física cuando sea posible hacerla. **No es un requisito para avanzar el CAD provisional:** primero se investigan cotas públicas, como las del [estudio axial](../cad/estudios/README.md).

## Abrir sin instalar programas

Abre [Capturar_Rueda.html](Capturar_Rueda.html) con el navegador. El formulario, sus reglas y sus dibujos están incluidos en ese archivo; no hace peticiones de red. El borrador se guarda en el almacenamiento local del navegador si está permitido. Descarga también el JSON: un borrador del navegador no sustituye un archivo conservado.

La [guía SVG completa](guia_rueda.svg) puede abrirse o imprimirse por separado. Es conceptual, sin escala ni dimensiones Xiaomi. El formulario amplía la figura de la magnitud seleccionada para facilitar su lectura.

## Una captura mínima, cuando haya acceso

1. Identificar el pasador con una etiqueta propia. La rueda, si se identifica, recibe otra etiqueta. El lado y la pertenencia del pasador a esa rueda pueden seguir sin confirmar.
2. Anotar **diámetro del cuerpo** y **longitud total**, en milímetros, con estado «Medido». Identificar sección o extremos, instrumento, condición, fecha y referencia a la lectura, foto o croquis. Si la sección se confirma circular, indicar la evidencia.
3. Dejar vacías las medidas no disponibles. Se admite exportar una ficha enteramente pendiente o parcialmente cumplimentada.
4. Descargar el JSON. Las fotos no se incorporan al archivo; se guarda su referencia textual.

No se solicita repetir las fotografías generales del robot. Los IDs de magnitud enlazan con el registro existente M04/M05/M07/M41/M42. La ficha no sustituye ni rellena automáticamente `mediciones.csv`.

## Interpretación de los datos

| Dato | Comportamiento |
|---|---|
| Pendiente, no recuperable o no aplicable | Valor `null`, sin lecturas numéricas. Los dos últimos estados requieren explicación. |
| Medido | Declaración física con identidad de pieza y procedencia. No acredita por sí misma exactitud ni ajuste. |
| Estimado | Se conserva el método en una nota y se excluye de la referencia geométrica medida. |
| Publicado por un proveedor | Se registra en documentación/CAD de catálogo; no se introduce como «medido» en esta ficha. |
| Repeticiones | Lecturas de la misma sección y condición. No se promedian ni reemplazan el valor declarado. |
| Incertidumbre no evaluada | `null`; nunca cero por defecto. La resolución del instrumento no equivale por sí sola a incertidumbre. |
| Origen de prueba de software | Se conserva marcado como sintético; la macro normal no crea geometría con esos datos. |

El formulario acepta coma o punto decimal. Para varias lecturas se utiliza punto y coma: no se confunde la coma decimal con un separador. Los campos desconocidos y las claves o magnitudes duplicadas se rechazan al importar un JSON. La corrección descubierta en revisión impide reutilizar el mismo identificador para rueda y pasador, incluso cambiando mayúsculas o espacios exteriores.

**Distinciones geométricas:** ancho del cuerpo móvil ≠ separación entre soportes fijos; diámetro exterior de rueda sin carga ≠ diámetro efectivo de rodadura; distancia pivote–eje ≠ orientación o posición global; longitud total del pasador ≠ longitud útil garantizada. Alojamiento A y alojamiento B se documentan independientemente.

## Abrir en FreeCAD

En FreeCAD, abrir y ejecutar [importar_ficha.FCMacro](importar_ficha.FCMacro), seleccionar la ficha JSON y un nombre **nuevo** `.FCStd`. Si la macro no encuentra su carpeta, solicita la carpeta `capturas_rueda` del proyecto.

Se crea un documento independiente con procedencia, datos originales y tabla. Cuando diámetro y longitud del pasador están declarados como medidos, la sección está identificada como circular y la ficha es válida, se añade un **cilindro de referencia simplificado**. No reproduce cabezas, ranuras, extremos ni retención. El documento no modifica el maestro del robot y no asigna el módulo a un lado o a una posición global.

No se sobrescriben archivos existentes. Ninguna ficha de esta revisión aprueba fabricación, resistencia o montaje. Para probar el código se dispone de un modo sintético explícito en la API Python; no es una opción de la macro normal.

## Archivos editables y comprobaciones

| Archivo | Papel |
|---|---|
| `definiciones.json` | Ocho magnitudes, sus referentes y relación con Mxx. |
| `plantilla_rueda.json` | Ficha inicial con todos los valores desconocidos. |
| `schema_ficha.json` | Esquema estructural JSON Schema 2020-12; requiere además validación semántica. |
| `validar_ficha.py` / `validacion.js` | Reglas de datos, evidencia y alcance; Python vuelve a validar al importar. |
| `importar_freecad.py` / macro | Creación y guardado de un documento independiente. |
| `formulario.template.html`, `formulario.js`, `construir_formulario.py` | Fuentes del HTML autónomo, sin dependencias externas. |
| [pruebas/](pruebas/README.md) | 23 comprobaciones y 66 casos de paridad, todos sintéticos. |

Desde esta carpeta:

```bash
python -B construir_formulario.py
python -B validar_ficha.py plantilla_rueda.json
python -B pruebas/run_capture_parity.py
```

Se verificó el importador en FreeCAD 1.1.4: ausencia de geometría en pendientes, modo sintético explícito, rechazo previo de ficha inválida, guardado, rechazo de sobrescritura y reapertura. Se comprobó también que un texto con `=` se conserva como texto. [Resultado de la ejecución](../cad/estudios/validacion_software.json). Estas pruebas no equivalen a ensayo físico. La interacción completa del formulario en un navegador de escritorio no se ha validado automáticamente; se han comprobado reglas, sintaxis, fuentes y guía SVG.

Licencias: código y fuentes del formulario MIT; guía conceptual, definiciones y documentación propia CERN-OHL-P-2.0. Los textos de licencia y límites de procedencia están en [cad/LICENCIAS.md](../cad/LICENCIAS.md). No se incorporan fotos privadas ni planos OEM.
