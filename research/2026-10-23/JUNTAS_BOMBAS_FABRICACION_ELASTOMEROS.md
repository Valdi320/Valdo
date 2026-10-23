# Juntas, bombas y fabricación de piezas elastoméricas

Consulta: **23/10/2026**. Revisión de documentos y archivos fuente; cálculos propios ilustrativos. Sin compras, instalación de software, impresión, moldeo ni ensayos con agua. Continúa el análisis de [corrosión y desmontaje](CORROSION_UNIONES_MATERIALES_AUXILIARES.md), [agua](AGUA_CAPTACION_CALIDAD.md) y [materiales críticos](MATERIALES_CRITICOS_REPOSICION.md).

**Resultado:** fabricar la forma de una pieza flexible es una posibilidad actual, incluso mediante moldes impresos; fabricar su material, acreditar su función y mantener indefinidamente sus medios de producción siguen siendo problemas distintos. Para reducir dependencia conviene elegir recambios identificables, acceso al desmontaje y una aplicación concreta. No se demuestra aquí gasto cero ni independencia material completa.

## 1. Una junta tiene más especificaciones que sus dos medidas

El manual público de Parker distingue diseño estático y dinámico, compatibilidad con fluidos, presión, temperatura, acabado superficial, deformación remanente y almacenamiento. Advierte que los máximos de distintas variables no se combinan automáticamente. Su sección 8.14 separa almacenamiento de servicio y explica que malas condiciones pueden inutilizar las juntas antes de instalarlas. [O-Ring Handbook](https://www.parker.com/content/dam/Parker-com/Literature/Praedifa/Catalogs/Catalog_O-Ring-Handbook_PTD5705-EN.pdf).

**Inferencia para nosotros:** «EPDM», «silicona» o una dureza nominal no bastan para aceptar un recambio. Hacen falta compuesto o referencia, dimensiones, alojamiento, exposición y función. Tampoco basta imprimir un aro con buen aspecto. No se han verificado aquí tablas dimensionales mediante revisión visual: la descarga local del manual devolvió 403 y se detuvo esa vía; no se extraen de ellas tolerancias o instrucciones de montaje.

El artículo 44 del Real Decreto 3/2023 exige que los materiales en contacto con agua de consumo no comprometan la salud, características del agua, crecimiento microbiano o migración de contaminantes; contempla también materiales incorporados durante reparaciones. Es una referencia para evaluar una pieza, no una aprobación de cualquier material «alimentario» ni una determinación del régimen de una futura finca. [BOE, artículo 44 y disposiciones sobre materiales](https://www.boe.es/eli/es/rd/2023/01/10/3/con#a44).

Por tanto, un circuito experimental de agua sin uso sanitario no valida un circuito para beber. La equivalencia sanitaria requiere evidencia distinta de que una unión no gotee.

## 2. Bomba peristáltica: recambio accesible, tubo consumible

El manual del fabricante Watson-Marlow para 401U y cabezales 400D/400DM relaciona la duración del tubo con presión, velocidad, compresión, fluido, temperatura y dimensiones. Indica que debe determinarse en la aplicación y programarse su sustitución. Esto fundamenta considerar el tubo como consumible; no permite trasladar las horas orientativas de esos cabezales a una bomba impresa distinta. [Manual del fabricante, apartado Tube life and performance against pressure](https://www.wmfts.com/es-ar/resources/bibliografia/manuals/en/401u-manual-en/).

**Decisión provisional:** estudiar peristálticas para dosificación o trasvases concretos, sin asumir que sustituyen a una bomba doméstica de abastecimiento. Caudal libre, presión disponible, tiempo de trabajo, electricidad y tubo consumido se necesitan conjuntamente.

### HiPeristaltic: software verificable y documentación mecánica pendiente

El README del proyecto describe una bomba multicanal de laboratorio con piezas impresas y compradas; publica un coste aproximado de 280 USD y una prestación volumétrica anunciada de hasta 0,2 %. Son afirmaciones del proyecto, sin reproducción independiente aquí ni presupuesto actual entregado en España. El repositorio identifica archivos mecánicos y montaje mediante un depósito externo. [README fijado en revisión db9a435](https://github.com/gunakkoc/HiPeristaltic/blob/db9a43589ec3b8e9f0624caa9871cc5c3a12e66a/README.md).

Se comprobó su licencia raíz Apache-2.0. Hay licencias particulares en dependencias; por ejemplo, la del controlador HAL remite a condiciones de paquete y, en su ausencia, a BSD-3-Clause. No se atribuye una licencia uniforme a cada componente. [Licencia raíz](https://github.com/gunakkoc/HiPeristaltic/blob/db9a43589ec3b8e9f0624caa9871cc5c3a12e66a/LICENSE), [aviso del HAL](https://github.com/gunakkoc/HiPeristaltic/blob/db9a43589ec3b8e9f0624caa9871cc5c3a12e66a/firmware/STM32G0B1RET6_BIGTREETECH/STM32CubeProject/HiPeristaltic/Drivers/STM32G0xx_HAL_Driver/LICENSE.txt).

La API devolvió un árbol no truncado de 442 entradas, sin archivos sueltos con extensiones STL, STEP, STP, SCAD, FCStd o DXF. Existe un ZIP que no se abrió; esto no prueba ausencia absoluta de CAD. El enlace DOI de hardware produjo un error de resolución no recuperable y el artículo de RSC devolvió 403. Se registran como límites, sin utilizar copias alternativas para eludirlos. La reproducibilidad y licencia del conjunto mecánico quedan pendientes. [Árbol de la revisión](https://api.github.com/repos/gunakkoc/HiPeristaltic/git/trees/db9a43589ec3b8e9f0624caa9871cc5c3a12e66a?recursive=1).

### Phisik/Peristaltic-Pump: fuente paramétrica con condiciones que aclarar

El README de la revisión **8dbbafe**, de 2020, describe piezas SCAD y electrónica comercial. Atribuye unos 700 ml/min a un tubo de 7 mm exterior y 5,5 mm interior, y unos 35 USD al montaje histórico. No son precio vigente, caudal garantizado con contrapresión ni prueba de servicio prolongado. [README original](https://github.com/Phisik/Peristaltic-Pump/blob/8dbbafe1e1c8c02d33d99f95e23c47561df6de33/README.md).

La licencia raíz es **CC BY-NC-SA 4.0**, mientras `settings.scad` y `pump.scad` llevan una cabecera «Licence GPL» sin versión en esa cabecera. Puede haber alcances por archivo; no se resuelve aquí su interpretación. Por ello no se incorpora como base de permisos comerciales claros ni se redistribuye una modificación. [Licencia raíz](https://github.com/Phisik/Peristaltic-Pump/blob/8dbbafe1e1c8c02d33d99f95e23c47561df6de33/LICENSE), [parámetros](https://github.com/Phisik/Peristaltic-Pump/blob/8dbbafe1e1c8c02d33d99f95e23c47561df6de33/scad/settings.scad), [fuente del cabezal](https://github.com/Phisik/Peristaltic-Pump/blob/8dbbafe1e1c8c02d33d99f95e23c47561df6de33/scad/pump.scad).

Además, el archivo de parámetros usa **9 mm exteriores y pared de 1,5 mm**, que darían **6 mm interiores** por resta. No son las dimensiones del ejemplo del README. Es una diferencia de configuración, no prueba de un defecto. No se transfieren calibración o caudal entre ambos tubos.

**Cálculo de escala:** a un caudal supuesto constante de 0,7 L/min, mover 100 L requeriría **142,86 minutos**, sin contar presión, pérdidas o paradas. Esta división no demuestra que el montaje pueda elevar ese volumen ni abastecer los aparatos de una vivienda.

## 3. Moldear silicona con útiles impresos es una ruta existente

Formlabs distingue hacer un molde de silicona de **producir una pieza de silicona dentro de un molde impreso**. Documenta esta segunda ruta para series pequeñas y advierte que el curado del molde y su compatibilidad afectan al resultado; resina sin curar puede inhibir el curado de la silicona. Su guía cita desgaste de sus moldes tras 10–20 usos típicos, no una garantía universal transferible a FDM. [Guía técnica de Formlabs](https://formlabs.com/support/Silicone-mold-making-and-silicone-part-production/).

Esto ofrece una vía para fabricar geometrías propias sin comprar un cabezal especializado. **No demuestra que cualquier resina, filamento, desmoldeante o silicona produzca una junta potable o resistente a presión.** El proceso, material y acabado de cada pareja deben verificarse.

Como referencia de insumo, Feroca mostraba **EasyPlat ACQUA, kit de 900 g, ref. 201354301, a 29,04 € con IVA**, envío no calculado. La ficha lo presenta para moldeo y efectos especiales, con dureza Shore A25 y densidad de 1,20 g/cm³; señala posibles inhibidores del curado. No se encontró en lo leído acreditación de esa referencia para agua potable ni una formulación completa abierta. [Ficha y precio](https://feroca.com/es/siliconas-de-platino-adicion/1234-3382-easyplat-acqua.html).

### Ejemplo geométrico propio: cuánto material ocupa una pieza sencilla

Se elige una **junta plana experimental para una caja seca**, diámetro exterior 50 mm, interior 30 mm y espesor 2 mm. No tiene asignada función sanitaria, de presión, protección eléctrica o carga.

- Volumen geométrico: `π/4 × (50² − 30²) × 2 / 1000` = **2,513 cm³**.
- Con la densidad comercial publicada de 1,20 g/cm³: **3,016 g teóricos**.
- Añadiendo un 25 % arbitrario para pérdidas: **3,770 g** por pieza intentada.
- A 29,04 €/900 g: **0,122 € de material consumido**, aproximadamente.

El desembolso del kit sigue siendo **29,04 €**, además del útil, material de impresión, energía, preparación, herramientas y posibles rechazos. No se ha demostrado que resulte una pieza funcional, que el sobrante se conserve el tiempo necesario ni que todas las piezas salgan iguales. No es un coste completo por reparación.

La junta comercial KWC Home **Z.605.806**, anunciada como EPDM 20,35 × 1,78 mm, IRHD70, figuraba a **6,58 € con impuestos**. Es otra geometría y material; no se compara el ejemplo de silicona como sustituto barato equivalente. No se comprobó qué grifo concreto acepta esa referencia ni su documentación sanitaria de fabricante. [Precio del recambio](https://www.suministrossanitarios.com/es/complementos-para-grifos/146911-junta-torica-d2035x178-irhd70-epdm-marca-kwc-home.html).

## 4. Impresión directa: avance real anunciado, cadena todavía comprada

La página oficial de Prusa presenta un cabezal de dos componentes de Filament2 para la XL. En la consulta mostraba **925 USD con región Estados Unidos**, no precio final español; no se confirmó stock o plazo. El anuncio de envío en septiembre aparecía en resultados indexados y no en la apertura actual, por lo que no se toma como prueba de entrega. [Producto oficial](https://www.prusa3d.com/es/producto/original-prusa-xl-silicone-printing-toolhead/).

Filament2 describe un tubo relleno de material que se alimenta y cuya envoltura se retira durante la impresión; declara el enfoque patentado y ofrece acceso anticipado. La apertura de la impresora anfitriona no acredita que este cabezal, consumible y formulación sean abiertos. [Descripción de Filament2](https://www.filament2.com/).

**Decisión:** no recomendar comprar XL más cabezal para resolver nuestras juntas. Faltan necesidad concreta, material, disponibilidad, coste de consumibles y comparación con moldeo. Tampoco hay demostración aquí de que supere ampliamente una vía abierta equivalente. La investigación legítima de un equivalente tendría que separar principios generales, derechos aplicables y trabajo propio; no se inicia una copia ni se promete libertad de explotación.

## 5. Qué avanzar nosotros y cómo medirlo

| Paso | Trabajo concreto | Evidencia que falta antes de depender de él |
|---|---|---|
| Identificar un recambio | Relacionar aparato, despiece, junta, compuesto y alojamiento | Compatibilidad exacta y estado de las superficies |
| Probar fabricación de forma | Diseñar un útil propio para una pieza seca no crítica | Medidas, curado, defectos y repetibilidad |
| Documentar duración | Registrar ciclos, ambiente, deformación y consumo | Seguimiento; una primera pieza no predice décadas |
| Investigar material propio | Revisar formulaciones publicadas y origen de cada insumo | Síntesis o abastecimiento local, propiedades y reposición de herramientas |
| Agua de consumo | Exigir evidencia sanitaria además de estanqueidad | Aptitud del producto y del sistema completo |

La reducción verificable de una dependencia sería, por ejemplo, sustituir una pieza descatalogada mediante un útil propio y material especificado. La silicona seguiría siendo comprada si no cerramos su fabricación. No se oculta esa dependencia por ser pocos gramos.

**Próxima comparación:** una bomba de agua concreta con despiece y recambios identificados, frente a una arquitectura con menor necesidad de bombeo. Debe conservar caudal, presión y comodidad requeridos; no sustituirlos por una demostración de laboratorio más fácil. No se fija una fecha de independencia total.

Datos, fórmulas, revisiones y límites: [juntas_bombas_2026-10-23.json](datos/juntas_bombas_2026-10-23.json). Referencias 245–260 en [FUENTES.md](FUENTES.md).
