# Pruebas del contrato de captura

Estas comprobaciones verifican el formato de la ficha, sus puertas de uso y la coherencia entre los validadores Python y JavaScript. **Todos los fixtures son sintéticos, incluidos los que simulan `origen: "unidad_real"`.** Ningún número de las pruebas es una medida física del Xiaomi, un nominal de diseño ni una autorización de fabricación.

La ficha de mediciones es opcional. Estas pruebas no exigen al propietario medir piezas para continuar el CAD ni sustituyen el trabajo con fuentes públicas y referencias documentadas.

## Ejecutar

Se necesitan Python 3 y, para la paridad, Node.js disponible en `PATH`. No se requiere FreeCAD ni paquetes adicionales; los scripts no instalan dependencias ni acceden a red.

Desde el directorio del proyecto:

```bash
python3 -B capturas_rueda/pruebas/run_capture_parity.py
```

Este comando ejecuta las **23 pruebas** y compara en ambos lenguajes las **66 entradas sintéticas** derivadas de esos mismos casos. Compara aceptación/rechazo y puertas de uso; para datos aceptados también compara el recuento declarado. No exige mensajes idénticos ni rechazar en la misma etapa: por ejemplo, un desbordamiento numérico puede rechazarse al analizar JSON o al validar la ficha.

Para ejecutar únicamente las 23 pruebas de Python:

```bash
python3 -B capturas_rueda/pruebas/test_capture_contract.py
```

Las rutas de datos se resuelven respecto a los propios scripts, por lo que también pueden invocarse desde otro directorio indicando su ruta. No dependen de una carpeta de trabajo externa ni de rutas absolutas predefinidas.

## Archivos y resultados

El validador y las fichas sintéticas se copian a una carpeta temporal del sistema, que se elimina al terminar. El directorio temporal debe estar fuera del proyecto. Las comprobaciones no escriben logs ni bytecode en el producto, no cambian el CAD y no ejecutan operaciones Git.

Los resultados salen por consola: detalle de pruebas en `stderr`; resumen y hashes SHA-256 en `stdout`. La salida **0** indica que pasan las pruebas, coincide la paridad y se conservan los archivos comprobados. La salida distinta de cero indica un fallo o una dependencia no disponible. Un cerrojo reconocido en el proyecto, la carpeta de capturas o la de pruebas detiene la ejecución.

Los hashes comparan la revisión de los validadores y la conservación del CAD durante esta ejecución. No prueban resistencia, funcionamiento del robot ni compatibilidad de un diseño fabricado.
