# Auditoría CSV con Python — demostración sintética

Proyecto propio y reproducible para respaldar nuestros servicios de calidad de datos. **No es un encargo anterior de cliente ni una prueba de experiencia comercial remunerada.** Creado con ayuda de IA y Python 3, sin dependencias externas, publicidad ni servicios de pago.

## Ejecución

Desde esta carpeta, ejecutar `python3 audit_csv.py sample_input.csv --outdir output --id id --name name --city city --required id,name,city --numeric amount`.

Ejecutar las pruebas con `python3 -m unittest test_audit_csv.py -v`.

## Entregables

- `annotated_rows.csv`: filas originales conservadas y etiquetadas para revisión.
- `exceptions.csv`: incidencias con índice del registro y campo.
- `candidate_duplicates.csv`: **posibles** coincidencias de nombre/ciudad, jamás identidades demostradas.
- `receipt.json`: SHA-256 del original, reconciliación de filas, controles realizados y hashes de salidas.
- `report.md`: resumen, recuentos y limitaciones.

Los datos de ejemplo son inventados. El archivo CSV original no se modifica. No se borran ni fusionan registros. Las coincidencias se deben confirmar con reglas y datos del cliente. Los números usan decimal con punto y no se corrigen automáticamente. Los encabezados repetidos, las filas con columnas sobrantes/faltantes y los límites excedidos se rechazan por seguridad. No subir ni introducir datos personales sensibles.

Las entregas comerciales requieren el consentimiento de un comprador, reglas de aceptación acordadas y QA específico de sus datos autorizados.
