# Ingeniería inversa física, software y firmware

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 2. Descompilador físico portátil: qué tiene que medir y devolver

### 2.1. Cadena de resultados

**Objeto → medidas multimodales calibradas → hipótesis contrastables → gemelo digital → CAD/BOM/esquemas → simulación → fabricación de prueba → medición de equivalencia → diseño corregido.**

| Instrumento/módulo | Información que puede aportar | Lo que NO garantiza |
|---|---|---|
| Fotogrametría, cámaras RGB y macro | Color, marcas, textura, geometría visible, desgaste | interior opaco y composición |
| Luz estructurada / escáner óptico 3D | nube de puntos, malla y dimensiones externas | fuente CAD original y tolerancias |
| Microscopía | circuitos y materiales visibles | capas ocultas y lógica completa |
| Ultrasonidos compatibles | fallos y estructuras internas de ciertos sólidos | funcionamiento universal en todo material |
| Termografía | patrones térmicos y fallos posibles | causa única |
| Raman / IR / NIR / XRF | firmas químicas o elementos en materiales apropiados | todos los aditivos o procesos de fabricación |
| Multímetro / sondas de continuidad / medidor de impedancia | redes y componentes eléctricos accesibles | esquema completo de placa multicapa |
| Osciloscopio / analizador lógico | comunicaciones y señales | significado íntegro de firmware |
| Masa, ensayos mecánicos, vibración | densidad aparente, rigidez, resonancias | receta original única |
| Tomografía industrial de terceros | partes internas de objetos compatibles | barato, portátil, universal o inocuo |

La tecnología debe **registrar resolución, calibración, unidades, fecha, error e incertidumbre**. No mezclar datos medidos con inferencias de IA sin marcarlo.

### 2.2. Hardware propuesto

- **Unidad de mano**: cámaras, lente macro, iluminación polarizada, sensor de profundidad o luz estructurada calibrada y marcadores de escala.
- **Módulos acoplables**: contacto mecánico, termografía, medición de señales y sondas de material cuando proceda.
- **Estación de procesamiento**: GPU local, CAD, análisis físico, simulación y almacenamiento; no obligar a llevar una gran GPU en la mano.
- **Servicios externos opcionales**: tomografía industrial, microscopía avanzada o ensayos destructivos. El aparato no necesita integrar fuentes de radiación ionizante.

### 2.3. Software de reconstrucción activa

1. Detectar el tipo aproximado de objeto y sus superficies.
2. Crear una geometría preliminar y segmentar componentes, juntas, tornillos y posibles funciones.
3. Mantener varias hipótesis de material/topología/comportamiento con grados de confianza.
4. Elegir **la medición siguiente por ganancia de información esperada** y riesgo/coste, en vez de escanear todo sin criterio.
5. Recuperar primitivas y operaciones CAD (revoluciones, extrusiones, agujeros, patrones, roscas) y sus cotas; conservar la malla original.
6. Estimar uniones, restricciones, conexiones y comportamiento observado.
7. Simular, medir de nuevo y revisar la hipótesis cuando falle.
8. Exportar **CAD paramétrico editable**, planos, BOM, materiales, incertidumbres, protocolo de fabricación y pruebas.

**Fuentes precursoras:** [OpenScan](https://github.com/OpenScan-org), [OpenScan Mini](https://github.com/OpenScan-org/OpenScan-Doc/blob/main/docs/hardware/OpenScanMini.md), [FreeCAD](https://github.com/FreeCAD/FreeCAD), [CadQuery](https://cadquery.readthedocs.io/), [Degate](https://github.com/DegateCommunity/Degate), [PulseView](https://sigrok.org/wiki/PulseView). La automatización de CAD desde escaneos (incluidos enfoques de Fraunhofer de reconstrucción asistida por IA) es una línea precedente; no significa que los resultados sean automáticamente fabricables y equivalentes.

### 2.4. Límite fundamental

Dos objetos de interior distinto pueden verse iguales por fuera y comportarse igual en las pruebas realizadas. **Ninguna IA puede recuperar certeza sobre propiedades que no son observables.** El sistema deberá solicitar apertura, otras mediciones, laboratorio o asistencia, y dejar explícitamente sin resolver lo que no pueda verificar.

---

---

## 3. Descompilación de software y firmware integrada con lo físico

- **Referencia inmutable** de binarios y mediciones, huellas y versiones.
- Ghidra y otras herramientas apropiadas de análisis estático/dinámico, emulación, depuración, detección de tipos, funciones y referencias.
- Recuperación incremental de lógica; renombrado, agrupación en módulos y reconstrucción de estructuras.
- **Pruebas diferenciales** de salidas, memoria, estado, temporización e interacción con hardware antes de sustituir una función.
- Relación entre diagramas eléctricos, sensores, actuadores y firmware cuando exista acceso legítimo.
- No publicar contenido protegido por derechos de terceros; revisar licencias, interoperabilidad y legislación pertinente.

La IA puede ayudar a interpretar algoritmos y proponer reconstrucciones, pero **el código pseudodescompilado no constituye por sí solo fuente completa y mantenible**. Para aplicaciones de usuario, Java y .NET ofrecen otros analizadores de bytecode; para código nativo ARM/x86, usar herramientas compatibles con arquitectura y formato.

Herramientas útiles: [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [3dsrecomp](https://github.com/fearkov/3dsrecomp), [Zakuro](https://github.com/fearkov/zakuro), [Degate](https://github.com/DegateCommunity/Degate). Estas últimas son **referencias tecnológicas de usos distintos**, no promesa de que un solo motor analice todo.

---
