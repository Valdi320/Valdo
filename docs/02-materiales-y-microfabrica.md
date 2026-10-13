# Materiales y microfábrica circular

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 4. Materiales locales, sostenibles y versátiles

**No perseguir un material mágico** con todas las propiedades. Buscar una **paleta de materiales** compatible con una biblioteca abierta de formulaciones, estructuras geométricas, fabricación y reciclaje.

| Familia | Funciones potenciales | Problemas pendientes |
|---|---|---|
| Celulosa / nanocelulosa | refuerzo, ligereza, piezas estructurales | humedad, anisotropía, procesado |
| Lignina | cargas y formulaciones protectoras/estructurales | variabilidad, compatibilidad |
| PHA producido por microorganismos | polímeros moldeables; biodegradación según formulación y ambiente | coste, separación, temperatura |
| Almidón | formulaciones biodegradables y cargas | envejecimiento, humedad |
| Fibras vegetales | rigidez y resistencia direccional | adhesión y calidad del lote |
| Minerales/cerámica | rigidez, aislantes, resistencia térmica en casos adecuados | fragilidad y energía de proceso |
| Metales reciclados | conductividad, rodamientos, tornillos y cargas elevadas | separación/aleaciones, no biodegradables |
| Tintas conductoras/carbono | sensores y circuitos modestos | no producen microchips modernos |
| Elastómeros durables | juntas, neumáticos, amortiguación | recuperación al final de vida |

**Conceptos separados:** «biobasado», «biodegradable», «compostable», «reciclable» y «no tóxico» **no son sinónimos**. Biodegradable significa bajo determinadas condiciones; no equivale a descomponerse de forma segura en cualquier entorno. [Comisión Europea: marco de bioplásticos](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en).

**Metamateriales mecánicos:** celosías, celdas auxéticas, estructuras tipo giróide y elementos flexibles permiten programar propiedades mecánicas por geometría. Esto puede reducir referencias de material, pero **no reemplaza los requisitos químicos** para conducción, magnetismo, semiconductores, aislamiento o almacenamiento electroquímico.

**Regla de fin de vida:** durabilidad adecuada → reparación → reutilización → desmontaje → reciclaje separado; reservar biodegradación para casos concretos. Diseñar juntas, fijaciones y adhesivos **desmontables** y documentar la composición como un pasaporte digital de materiales.

Producción local de PHA, celulosa procesada y formulaciones nuevas exige evaluar agua, energía, fermentación, productos auxiliares, ventilación, emisiones, coste, calidad, toxicidad y recuperación; que una materia prima sea abundante **no demuestra** que fabricarla en una vivienda sea sencillo o barato. [Revisión de PHA a partir de residuos (2025)](https://www.sciencedirect.com/science/article/pii/S0141813025009079).

---

---

## 5. Impresora 3D multimaterial → microfábrica doméstica

La impresión FFF/FDM será el núcleo accesible, pero un taller universal necesita otros procesos y logística:

- Cabezal o cambiador de herramientas para familias de materiales compatibles, perfiles de impresión calibrados, control de temperatura y humedad.
- Operaciones auxiliares: roscado, perforación, inserción de fijaciones, acabados y mecanizado cuando tolerancias o composición lo requieran.
- Montaje robotizado con tornillos, conectores, juntas, rodamientos y piezas electrónicas comerciales.
- Posibilidad de fabricar PCB sencillas con procesos apropiados; **no inventar una impresora de chips avanzados**.
- Metrología dimensional, probetas de resistencia/fatiga, comparación CAD vs objeto real y trazabilidad del lote.
- Separación de desechos por materiales, máquinas de recuperación compatibles, ensayos de degradación tras varios ciclos.
- Inventario de materia prima, consumibles, herramientas, repuestos y componentes críticos; decisión comprar vs fabricar vs reparar.

**Protocolo de fabricación:** especificación y material → simulación → proceso compatible → fabricación → acabado → inspección/ensayo → liberación o rechazo. La IA **no puede declarar que una pieza soportará una carga solo porque encaje geométricamente**.

---
