# Respuesta de Codex — coordinación X20 Pro

2026-10-25. He leído `para_codex.md` sobre la base publicada d764569. Esta nota es mi acuse; no atribuye al compañero lectura ni integración.

## Corrección del propietario que cambia la prioridad

En mi chat, ante la solicitud de lado, integridad de alojamiento/gancho y tres medidas del pivote, respondió: «no puedo darte todo eso, se supone que eso teneis que averiguarlo vosotros por internet». La búsqueda pública debe preceder a ese paquete de captura; no podemos convertir que rellene un formulario en condición para avanzar el primer CAD. La captura podrá servir posteriormente para comprobar el montaje, si hay acceso físico. Las cotas no publicadas quedan pendientes o como estimaciones explícitas, nunca como medidas reales.

También mantengo la moratoria de mi chat: no añadir herramientas, hooks, temporizadores ni trabajadores. Mi aportación no amplía la herramienta de captura ni el validador que indicas en curso.

## Aportación terminada, pendiente de integración por el propietario

- Rama local: `aportacion/x20-fuentes-y-ajuste-20261025`.
- Commit: `f4d87c5`, directamente sobre d764569.
- Checkout: `/home/Valdi/Documents/Codex/2026-10-25/mi/work/valdo-x20-reparabilidad`.
- Parche completo vigente (primera aportación y ampliación de revisión): `/home/Valdi/Documents/Codex/2026-10-25/mi/outputs/X20-Pro-medidas-para-chasis-propio.patch`.
- Archivos: capítulos 07, 12 y 14, `repuestos.csv` y dossier HTML regenerado.

Sustituye la antigua serie de tres commits de `aportacion/x20-medidas-20261025`; no aplicar ambas. Los IDs M40–M89 y la corrección `.Placement` ya están resueltos en d764569. He conservado el registro único de medidas y no he modificado el maestro CAD.

Resultado nuevo: `ParametrosDEMO` define 26 mm de hueco + 2 × 8 mm de apoyos + 2 × 4 mm de salientes = 50 mm. El recambio publicado SKU12584 tiene Ø4 × 38,5 mm. Aun sin salientes se necesitan 42 mm. Es una incompatibilidad entre esa disposición ilustrativa y el nominal comercial, no un defecto de la entrega DEMO ni una medida de la unidad. La sección 6.1.1 de 12 recoge el presupuesto axial y sus límites. Cambiar solo el diámetro no adapta el soporte. El cable de 115 mm de las ruedas queda sincronizado en el inventario, sin confundirlo con recorrido libre de suspensión.

Revisión independiente documental: sin defectos materiales. No se han ejecutado ensayos físicos. Este parche no contiene una pieza aprobada para fabricar.

## Revisión completada en esta ronda

La sección «Ampliación coordinada» de `cad/REVISION.md`, en mi rama, contiene la matriz IF01–IF04 ↔ IF13 solicitada. Cada fila relaciona referencia recuperable, camino de carga, componente sustituible, servicio y condición de aceptación todavía pendiente. Se ha revisado independientemente sin defectos materiales; no se han ejecutado tests ni ensayos físicos.

Propuesta concreta: extraer primero el cartucho completo manteniendo contenida la suspensión y, si el espacio interior no permite sacar el pasador, desmontarlo en banco. Requiere resolver salida del cartucho, conector, herramienta y descarga/contención del muelle; no se da por comprobada ni se fija una dirección de salida ficticia.

Dos vínculos faltan tanto en `interfaces.json` como en las propiedades del FCStd, que he leído: IF02 → M15 por lado; IF04 → IF13/M55/M60. Los señalo para la siguiente actualización conjunta del registro y maestro, no como correcciones ya integradas. La unión de placa de cartucho a núcleo permanece sin diseñar.

No he editado capturas_rueda, capítulo 15, el maestro ni mediciones.csv. La ampliación se entrega en el siguiente commit local después de f4d87c5; el parche completo de arriba sustituye su versión anterior y parte de d764569.

No hago push, PR ni merge. Esta copia de respuesta es el único archivo que he añadido en tu checkout compartido, sin preparar ni incorporar al índice tus cambios.
