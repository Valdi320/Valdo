# Extrusión abierta de silicona: mecanismo, material y coste completo

Fecha: **23/10/2026**. Investigación documental, lectura parcial de CAD y revisión visual de instrucciones; cálculos propios. Sin instalar programas, modificar impresoras, imprimir, mezclar materiales o comprar. Complementa [piezas elastoméricas](JUNTAS_BOMBAS_FABRICACION_ELASTOMEROS.md) y [bioproducción de silicona](BIOPRODUCCION_SILICONA.md).

**Conclusión:** existe hardware abierto concreto para estudiar extrusión de pastas. También hay publicaciones sobre impresión de silicona y modificación de materiales comerciales. Su combinación todavía necesita validación: no se considera que una impresora con Allstruder sustituya directamente al sistema Filament2 ni que fabrique por sí sola la silicona.

## 1. Allstruder: qué está publicado

Se fija la revisión **809cda985a016ebdb54eb9294d0098ee85e7292d**, de **04/08/2026**, del repositorio `hintonthomas/Allstruder`. El README declara **CERN-OHL-P-2.0**, incluida modificación y fabricación bajo sus condiciones. No hay un archivo independiente llamado `LICENSE` en ese árbol; la declaración está en el README. No se ha realizado una auditoría jurídica de todos los archivos o dependencias. [README y declaración de licencia](https://github.com/hintonthomas/Allstruder/blob/809cda985a016ebdb54eb9294d0098ee85e7292d/README.md).

La API devuelve **138 entradas, 104 archivos**, sin truncamiento: **51 STL, 46 STEP, 5 proyectos 3MF, un PDF y un README**. Hay geometrías para piezas principales y adaptadores de jeringas e impresoras. No aparecen archivos nativos de un modelador paramétrico entre esas extensiones. Esto describe lo publicado, sin verificar que todas las combinaciones monten correctamente. [Árbol fijado](https://api.github.com/repos/hintonthomas/Allstruder/git/trees/809cda985a016ebdb54eb9294d0098ee85e7292d?recursive=1).

Se pudo leer la cabecera del STEP **Pusher Block v1.3**: formato AP214, exportación indicada desde SolidWorks 2024. No se abrió su geometría en un editor ni se midió. La existencia de STEP permite investigar edición de geometría sin exigir el programa de autoría, pero no acredita conservar el historial paramétrico original. [Archivo consultado](https://github.com/hintonthomas/Allstruder/blob/809cda985a016ebdb54eb9294d0098ee85e7292d/Building%20Allstruders/Main%20Parts%20-%20Default%20Configuration/STP/Pusher%20Block%20v1.3.STEP).

El documento de montaje contiene **24 páginas**. Se descargó y revisó visualmente mediante una hoja de contacto: muestra ensamblaje de bastidor, guía, husillo, transmisión, motor y adaptador. No se extrajo una lista de materiales valorada; las imágenes no sustituyen referencias, tolerancias o presupuesto completos. [Instrucciones de montaje de esa revisión](https://github.com/hintonthomas/Allstruder/blob/809cda985a016ebdb54eb9294d0098ee85e7292d/Assembly%20Panels.pdf).

## 2. Qué seguiríamos comprando y qué se ha ensayado

La página del laboratorio enumera guía MGN9C, husillo Tr8x8 y tuerca, rodamientos 608, correa y poleas 2GT, motor y tornillería. Publica un coste orientativo de **unos 50–51 USD**. Se mantiene como estimación del proyecto, sin precio español entregado ni conjunto instalado. Sus ejemplos incluyen colágeno, hidrogeles, precursores de aerogel y chocolate; la página consultada no contiene la palabra «silicone». Esto no prueba que nadie haya ensayado silicona con ese mecanismo. [Página técnica del laboratorio](https://shiwarskilab.com/allstruder/).

La misma fuente distingue una medida del mecanismo —deformación de hasta **20 µm bajo una carga calculada de 24 N**, con una jeringa concreta— de la calidad de impresión de una configuración completa. No se toma esa deformación como tolerancia de piezas finales ni **24 N como fuerza máxima autorizada**.

**Para nuestra autonomía:** bastidor y adaptadores imprimibles pueden facilitar reparaciones. Guía, husillo, motor, correas, jeringas y boquillas siguen siendo dependencias mientras no se demuestre su fabricación y reposición propias. Reutilizar el motor de una impresora tampoco demuestra compatibilidad eléctrica y mecánica de cualquier montaje.

## 3. Por qué importa la jeringa elegida

**Ejemplo propio, no ensayo ni recomendación de presión:** se supone una presión de 2 bar y diámetros interiores de 10 o 20 mm. Sin fricción, la fuerza ideal es `F = P × π × d² / 4`. Para dispensar 1 ml, el recorrido ideal es volumen dividido por área del émbolo.

| Diámetro interior elegido | Fuerza ideal a 2 bar | Recorrido ideal para 1 ml |
|---|---:|---:|
| 10 mm | 15,71 N | 12,73 mm |
| 20 mm | 62,83 N | 3,18 mm |

Duplicar el diámetro multiplica por cuatro el área y la fuerza requerida a igual presión; reduce a una cuarta parte el recorrido para igual volumen. **La capacidad en mililitros no basta para escoger una jeringa.** Deben comprobarse dimensiones, resistencia, fricción, deformación, boquilla, caudal y material real. Que la fuerza calculada supere la carga de un ensayo publicado no demuestra por sí solo fallo: indica que no se puede extrapolar ese ensayo sin evidencia adicional.

## 4. La silicona imprimible requiere una formulación y un proceso

El resumen de un estudio de **13/03/2026**, de la Universidad de Florencia, describe adaptación de EcoFlex 00-50 con THI-VEX para una **Lynxter S300X industrial**. Identifica una formulación de 4,0 % en masa como la mejor entre las ensayadas para sus geometrías y condiciones. La apertura del artículo devolvió **429**; no se revisaron íntegramente métodos, base exacta del porcentaje, resultados mecánicos ni suplementos. No se convierte ese dato en receta para Allstruder, otra silicona o agua potable. [Estudio, resumen indexado](https://www.mdpi.com/2076-3417/16/6/2764).

Smooth-On describe THI-VEX como espesante para ciertas siliconas propias y expresa sus adiciones respecto al componente A. Identifica incompatibilidades con Mold Max 40, Mold Max 60 y Solaris, y advierte de almacenamiento limitado. La ficha consultada no proporciona una formulación química completa abierta. [Fabricante del aditivo](https://www.smooth-on.com/products/thi-vex/).

**Inferencia:** adaptar un material comercial puede ampliar lo que fabriquemos, pero conserva compras de silicona y aditivo. Además, más consistencia no demuestra por sí sola buen curado, adhesión entre capas o duración de una junta. Para un sistema bicomponente habrá que comprobar también mezcla, tiempo disponible, limpieza y material que queda inutilizable en el circuito.

## 5. Una demostración anterior de sellos de silicona

El resumen indexado de **Open-source hybrid 3D-bioprinter for simultaneous printing of thermoplastics and hydrogels** describe un módulo de jeringa añadido a una Prusa i3 MK3. Entre sus demostraciones figura una cámara con sellos de silicona extruidos para unir ventanas de vidrio; la ficha declara GPLv3. La apertura de PMC mostró CAPTCHA y no se eludió. No se verificaron todos los archivos, el material exacto o un ensayo de presión. [Publicación y alcance descrito](https://pmc.ncbi.nlm.nih.gov/articles/PMC9123455/).

Esto aporta evidencia de una aplicación concreta previa a los anuncios recientes. No demuestra un sistema universal, aptitud sanitaria ni que cualquier cabezal doméstico produzca el mismo sello. Los datos parcialmente accesibles se conservan como pistas por completar, sin presentarlos como una réplica lista.

## 6. Costes observados y comparación que todavía falta

Bentley Advanced Materials mostraba **THI-VEX 1 oz, peso anunciado 0,03 kg, a 4,70 GBP con IVA británico**. No se calculó entrega, importación o impuestos finales españoles; no se convierte a euros ni se presupone disponibilidad de una formulación compatible. [Precio de referencia](https://www.benam.co.uk/thi-vex).

No se suman ese importe y los 51 USD del proyecto para formar una cesta: faltan impresora anfitriona, configuración exacta, jeringas, boquillas, material, preparación, limpieza y posibles rechazos. Tampoco se comparan como equivalentes con los 925 USD del cabezal Filament2 recogidos en el [anexo de juntas](JUNTAS_BOMBAS_FABRICACION_ELASTOMEROS.md).

| Ruta | Ventaja que investigar | Dependencia y comprobación pendientes |
|---|---|---|
| Molde propio y silicona comercial | Piezas sencillas sin adaptar toda la impresora | Útil, material, compatibilidad, desmoldeo y propiedades |
| Extrusor abierto de jeringa | Adaptadores modificables y estudio de pastas distintas | Impresora compatible, suministro, mezcla o soporte, curado y limpieza |
| Cabezal de dos componentes anunciado | Integración del suministro y mezcla que habría que comparar | Disponibilidad, consumibles, apertura y rendimiento equivalente |
| Biocatálisis de silicona | Investigar producción del polímero | Precursores, recuperación y formulación final, como explica el anexo biológico |

**Decisión provisional:** Allstruder merece una ficha técnica de candidato abierto, sin elegir compra ni adaptación. Para unas pocas juntas sencillas debe compararse primero el proceso completo con moldeo. El criterio será una pieza útil, repetible y mantenible, con material y trabajo contabilizados; no el coste aislado del actuador.

Próxima evidencia prioritaria: una aplicación no crítica especificada, lista de componentes por referencia, material concreto y comparación de coste y trabajo completos. La síntesis local de silicona permanece como línea separada; no se declara cerrada por poder extruir una pasta.

Datos y aritmética: [extrusion_silicona_2026-10-23.json](datos/extrusion_silicona_2026-10-23.json). Referencias 269–277 en [FUENTES.md](FUENTES.md).
