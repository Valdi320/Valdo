# Entrega integrada ChatGPT–Codex

25-10-2026. Integra sobre d764569 las aportaciones locales de Codex `f4d87c5` y `cd882f0`. La coordinación efectiva consta en `respuesta_codex.md`; las notas anteriores describen el inicio del intercambio y no sustituyen este estado.

## Trabajo incorporado

- 07, 12, 14 y `repuestos.csv`: búsqueda pública primero, presupuesto axial y cable publicado.
- `cad/REVISION.md`: matriz IF01–IF04 ↔ IF13, caminos de carga, extracción del cartucho y repetición de posición al reinstalar.
- `cad/estudios/X20Pro_Estudio_Axial_Publicado.FCStd`: conversión del presupuesto axial a FreeCAD nativo, documento independiente del maestro.
- `capturas_rueda/`: captura física **opcional** con guía, JSON y macro. No condiciona el avance CAD con fuentes públicas.
- Capítulo 15 y dossier regenerado con ambas aportaciones. No se ha aplicado el HTML derivado del parche ni la antigua serie sustituida.

El compañero Codex no ha hecho push, PR o merge. La integración/publicación la realiza ChatGPT según autorización vigente del propietario en este chat. Su checkout y rama permanecen independientes.

## Verificación y límites

El nuevo estudio y el importador se ejecutaron en FreeCAD 1.1.4 en un proceso independiente, tras comprobar cerrojos. Se guardaron y reabrieron; el cambio de parámetro de 26 a 30 produjo los cambios esperados y se restauró antes de guardar. El primer arnés se corrigió porque consultaba un nombre después de cerrar su documento; la segunda ejecución completó las comprobaciones.

23 pruebas de contrato y 66 casos de paridad pasaron. Todos sus números son sintéticos. Maestro CAD y `mediciones.csv` conservan los hashes publicados. No se ejecutó ningún ensayo físico, no se midió la unidad y no existe una pieza aprobada para fabricar en esta entrega.

## Rutas vigentes

- Checkout de integración: `/var/home/Valdi/Documentos/X20ProAbierto/Valdo`.
- Proyecto: `research/2026-10-25-xiaomi-x20-pro`.
- Maestro: `cad/X20Pro_Base_Arquitectura.FCStd` (v0.1 conservado).
- Estudio nuevo: `cad/estudios/X20Pro_Estudio_Axial_Publicado.FCStd`.
- Captura opcional: `capturas_rueda/Capturar_Rueda.html`.
- Checkout del compañero: `/home/Valdi/Documents/Codex/2026-10-25/mi/work/valdo-x20-reparabilidad`.

## Próximo entregable donde sirve apoyo

Variantes provisionales del asiento desmontable del cartucho y del recorrido de extracción, con presupuesto axial explícito, suspensión contenida y medio móvil separado del fijo. Buscar primero referencias públicas; no convertir falta de cotas en dimensiones reales inventadas. La salida axial del pasador en banco es una propuesta que falta comprobar con implantación y geometría.

Al actualizar el maestro, incorporar conjuntamente los vínculos IF02 → M15 por lado e IF04 → IF13/M55/M60 en JSON y propiedades nativas. Permanecen pendientes en esta entrega, tal como los identificó el compañero. La captura no abre un segundo registro de cotas ni modifica las existentes.
