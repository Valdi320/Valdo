# Fuentes, método y límites

**Fecha de consulta:** 25/10/2026. La investigación combina tres líneas: arquitectura/desmontaje, repuestos/reparación y metrología/CAD/materiales. Las conclusiones se han integrado y revisado para evitar transferencias indebidas entre variantes. Los precios y existencias son observaciones de esa fecha.

## Escala común de evidencia

| Código | Fuente o estado | Alcance |
|---|---|---|
| E1 | Fabricante o documentación primaria del producto citado | Prueba lo que publica ese fabricante; identificar modelo y versión |
| E2 | Ficha propia de vendedor con compatibilidad explícita | Precio, aspecto, referencia y compatibilidad declarados; sin validación independiente |
| E3a | Vídeo/observación primaria de un modelo relacionado | Útil para comprender mecanismo; no demuestra idéntico desmontaje del Pro |
| E3b | Caso individual o anuncio de particular | Acredita relato/oferta; no frecuencia de fallos ni estado real ensayado |
| E4 | Razonamiento o propuesta de ingeniería | Hipótesis, método y condiciones a verificar |
| Pendiente | No observado, medido o probado | No rellenar con una estimación presentada como hecho |

Los identificadores F01, F1, etc. son **locales a cada capítulo**. Una fuente de fabricante de filamento no prueba que ese material funcione en el robot; un catálogo de repuestos no es un plano OEM. Se distingue explícitamente entre identificación comercial y referencia original.

## Qué se buscó y cómo se filtró

- Identificación D102GL/D102-JZEU/BHR8859EU, documentación Xiaomi y manuales regionales identificados.
- Repuestos estructurales y motrices en español, inglés, alemán y referencias de la familia M30 en chino; fichas individuales y compatibilidad por componente.
- Vídeos de apertura y extracción de rueda, con modelo y marcas temporales, diferenciando desmontaje completo y acceso mínimo.
- CAD/STL, refuerzos y módulos imprimibles; se descartaron accesorios de filtros, rampas y piezas de Mop Essential como evidencia de soporte Pro.
- Proyectos de aspiradores abiertos y archivos realmente publicados; se distinguieron hardware construido, CAD, simulación y objetivos pendientes.
- Documentación primaria de metrología, impresión y uniones en polímeros; se aplicó como orientación general, no como especificación Xiaomi.

La búsqueda no establece exhaustividad absoluta de Internet. No se ha accedido a documentación interna del fabricante ni a un despiece OEM privado. El inventario funcional no incluye cada tornillo, junta o componente electrónico individual.

## Respuestas que permanecen abiertas

| Pregunta | Estado actual | Evidencia que permitiría resolverla |
|---|---|---|
| ¿Qué apoyo exacto se ha roto? | Descripción insuficiente para fijar diseño | Primeros planos de ambas caras y movimiento relativo |
| ¿Es PP, ABS, PA u otro plástico? | No identificado | Marcaje del componente o identificación material fiable |
| ¿El chasis Max encaja en Pro? | No verificado | Referencia cruzada fiable y comparación dimensional/funcional |
| ¿Qué fuerza debe tener el muelle? | Catálogo publica dimensiones, no curva | Pieza equivalente especificada o medición del original sano |
| ¿Se puede cambiar rueda sin retirar otros módulos en esta revisión? | Evidencia análoga favorable, no procedimiento exacto | Observación del acceso real y registro de obstáculos |
| ¿Hay depósito interno/puerto de agua en este Pro? | No confirmado | Observación o documentación inequívoca de esa unidad |
| ¿Es una avería habitual de la serie? | Unos relatos no establecen tasa | Datos comparables de una población y condiciones de uso |
| ¿Un refuerzo durará más que el original? | Hipótesis, sin ensayo | Comparación de carga, deformación, uso y mantenimiento |
| ¿Cuánto costará el chasis propio? | Sin diseño ni cotización | CAD, BOM, fabricación y número de iteraciones |

## Publicación y reproducibilidad

Se publican texto propio, tablas, plantillas y esquemas propios. Los documentos, fotografías de tienda, vídeos y CAD de terceros se enlazan; no se redistribuyen íntegros. Las imágenes del aparato particular y sus identificadores no se incluyen en la publicación pública.

El manual europeo Xiaomi alojado por Otto se identifica con su URL, páginas pertinentes y SHA-256 en el capítulo 01. Las observaciones de vídeos se acompañan de tiempos; proceden del contenido inspeccionado y no de un título o fragmento de buscador. Wallapop se identifica expresamente como pista indexada cuyo cuerpo no pudo abrirse.

La licencia del repositorio y la de cada dependencia deben respetarse. La existencia de un repositorio público de CAD no implica que todo el producto sea de uso libre ni que esté listo para fabricar. Esta entrega no incorpora diseños ajenos al árbol del proyecto.

## Índice de URLs citadas

Cada enlace conserva su contexto, límites y localizador en los capítulos indicados. La lista incluye fuentes, proyectos y referencias de comparación; no equivale a una afirmación de compatibilidad de cada producto.

| Nº | URL | Capítulos |
|---:|---|---|
| 1 | [https://api.github.com/repos/makerspet/oomwoo-cad/git/trees/main?recursive=1](https://api.github.com/repos/makerspet/oomwoo-cad/git/trees/main?recursive=1) | [03](03-ingenieria-fisica-y-cad.md) |
| 2 | [https://cadquery.readthedocs.io/en/latest/importexport.html](https://cadquery.readthedocs.io/en/latest/importexport.html) | [03](03-ingenieria-fisica-y-cad.md) |
| 3 | [https://cadquery.readthedocs.io/en/latest/intro.html](https://cadquery.readthedocs.io/en/latest/intro.html) | [03](03-ingenieria-fisica-y-cad.md) |
| 4 | [https://cults3d.com/en/3d-model/tool/wheel-gear-for-xiaomi-mi-vacuum-robot-32-teeth](https://cults3d.com/en/3d-model/tool/wheel-gear-for-xiaomi-mi-vacuum-robot-32-teeth) | [02](02-repuestos-y-reparacion.md) |
| 5 | [https://d.otto.de/files/7208679f-5a7d-56d4-b534-937139397f71.pdf](https://d.otto.de/files/7208679f-5a7d-56d4-b534-937139397f71.pdf) | [01](01-arquitectura-y-desmontaje.md) |
| 6 | [https://es.wallapop.com/item/averiado-xiaomi-robot-vacuum-x20-pro-1312894872](https://es.wallapop.com/item/averiado-xiaomi-robot-vacuum-x20-pro-1312894872) | [02](02-repuestos-y-reparacion.md) |
| 7 | [https://github.com/AlieksieievYurii/vacuum-cleaner](https://github.com/AlieksieievYurii/vacuum-cleaner) | [03](03-ingenieria-fisica-y-cad.md) |
| 8 | [https://github.com/FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD) | [03](03-ingenieria-fisica-y-cad.md) |
| 9 | [https://github.com/Valdi320/Valdo](https://github.com/Valdi320/Valdo) | [Resumen](README.md) |
| 10 | [https://github.com/Valdi320/Valdo/blob/master/research/2026-10-13/05-ingenieria-inversa-metrologia.md](https://github.com/Valdi320/Valdo/blob/master/research/2026-10-13/05-ingenieria-inversa-metrologia.md) | [Resumen](README.md) |
| 11 | [https://github.com/chrismawson/OpenVac-Mk1](https://github.com/chrismawson/OpenVac-Mk1) | [03](03-ingenieria-fisica-y-cad.md) |
| 12 | [https://github.com/makerspet/oomwoo-cad](https://github.com/makerspet/oomwoo-cad) | [03](03-ingenieria-fisica-y-cad.md), [Resumen](README.md) |
| 13 | [https://github.com/makerspet/oomwoo-cad/blob/main/LICENSE](https://github.com/makerspet/oomwoo-cad/blob/main/LICENSE) | [03](03-ingenieria-fisica-y-cad.md) |
| 14 | [https://github.com/makerspet/oomwoo/blob/main/docs/BUILD_INSTRUCTIONS.md](https://github.com/makerspet/oomwoo/blob/main/docs/BUILD_INSTRUCTIONS.md) | [03](03-ingenieria-fisica-y-cad.md) |
| 15 | [https://help.prusa3d.com/article/infill_42](https://help.prusa3d.com/article/infill_42) | [03](03-ingenieria-fisica-y-cad.md) |
| 16 | [https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) | [03](03-ingenieria-fisica-y-cad.md) |
| 17 | [https://help.prusa3d.com/article/watertight-prints_112324](https://help.prusa3d.com/article/watertight-prints_112324) | [03](03-ingenieria-fisica-y-cad.md) |
| 18 | [https://i02.appmifile.com/993_operatorx_operatorx_xm/13/05/2025/77d23ed347099a90e75ce297d1202d40.pdf](https://i02.appmifile.com/993_operatorx_operatorx_xm/13/05/2025/77d23ed347099a90e75ce297d1202d40.pdf) | [01](01-arquitectura-y-desmontaje.md) |
| 19 | [https://makerspet.com/blog/oomwoo-3d-design-how-its-made/](https://makerspet.com/blog/oomwoo-3d-design-how-its-made/) | [03](03-ingenieria-fisica-y-cad.md) |
| 20 | [https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/nodes/SfMTransform.html](https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/nodes/SfMTransform.html) | [03](03-ingenieria-fisica-y-cad.md) |
| 21 | [https://mundoceys.com/storage/app/media/fichas_tecnicas/507219-ft-triaction-total-tech.pdf](https://mundoceys.com/storage/app/media/fichas_tecnicas/507219-ft-triaction-total-tech.pdf) | [02](02-repuestos-y-reparacion.md) |
| 22 | [https://oomwoo.com/](https://oomwoo.com/) | [03](03-ingenieria-fisica-y-cad.md), [Resumen](README.md) |
| 23 | [https://prusament.com/materials/prusament-pa11-nylon-carbon-fiber/](https://prusament.com/materials/prusament-pa11-nylon-carbon-fiber/) | [03](03-ingenieria-fisica-y-cad.md) |
| 24 | [https://prusament.com/wp-content/uploads/2022/08/TDS_PA11CFB.pdf](https://prusament.com/wp-content/uploads/2022/08/TDS_PA11CFB.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
| 25 | [https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf](https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
| 26 | [https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557217197.pdf](https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557217197.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
| 27 | [https://storage.googleapis.com/prusa3d-content-prod-14e8-wordpress-prusament-prod/2023/10/9f8d2165-tds_prusament-petg_n_en.pdf](https://storage.googleapis.com/prusa3d-content-prod-14e8-wordpress-prusament-prod/2023/10/9f8d2165-tds_prusament-petg_n_en.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
| 28 | [https://www.bilibili.com/video/BV1bG5WzYELb/](https://www.bilibili.com/video/BV1bG5WzYELb/) | [01](01-arquitectura-y-desmontaje.md) |
| 29 | [https://www.dns-shop.kz/product/0daa56c88926541e/dvigatel-v-sbore-s-kolesom-r-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/](https://www.dns-shop.kz/product/0daa56c88926541e/dvigatel-v-sbore-s-kolesom-r-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/) | [02](02-repuestos-y-reparacion.md) |
| 30 | [https://www.dns-shop.kz/product/5a1ae0fea1a1b25e/dvigatel-v-sbore-s-kolesom-l-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/](https://www.dns-shop.kz/product/5a1ae0fea1a1b25e/dvigatel-v-sbore-s-kolesom-l-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/) | [02](02-repuestos-y-reparacion.md) |
| 31 | [https://www.douyin.com/video/7483728020235177231](https://www.douyin.com/video/7483728020235177231) | [01](01-arquitectura-y-desmontaje.md) |
| 32 | [https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-gy-p-11965.html](https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-gy-p-11965.html) | [06](06-inventario-ampliado-del-robot.md) |
| 33 | [https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-schwarz-p-56231.html](https://www.ep-mediastore-ab.de/buerstenmotor-getriebe-l10-x10-x20-schwarz-p-56231.html) | [06](06-inventario-ampliado-del-robot.md) |
| 34 | [https://www.ep-mediastore-ab.de/deebot-mini-lidar-sensor-lds-schwarz-p-13034.html](https://www.ep-mediastore-ab.de/deebot-mini-lidar-sensor-lds-schwarz-p-13034.html) | [06](06-inventario-ampliado-del-robot.md) |
| 35 | [https://www.ep-mediastore-ab.de/dreame-buerstenmodul-grau-l10-x10-x20-p-46648.html](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-grau-l10-x10-x20-p-46648.html) | [06](06-inventario-ampliado-del-robot.md) |
| 36 | [https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-refurbished-p-56222.html](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-refurbished-p-56222.html) | [06](06-inventario-ampliado-del-robot.md) |
| 37 | [https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-x20-p-73385.html](https://www.ep-mediastore-ab.de/dreame-buerstenmodul-schwarz-l10-x10-x20-p-73385.html) | [06](06-inventario-ampliado-del-robot.md) |
| 38 | [https://www.ep-mediastore-ab.de/dreame-bumper-feder-hebel-p-32363.html](https://www.ep-mediastore-ab.de/dreame-bumper-feder-hebel-p-32363.html) | [06](06-inventario-ampliado-del-robot.md) |
| 39 | [https://www.ep-mediastore-ab.de/dreame-d9-l10-frontrolle-halter-schwarz-p-42556.html](https://www.ep-mediastore-ab.de/dreame-d9-l10-frontrolle-halter-schwarz-p-42556.html) | [02](02-repuestos-y-reparacion.md) |
| 40 | [https://www.ep-mediastore-ab.de/dreame-lds-board-vpower-v204-gruen-p-66896.html](https://www.ep-mediastore-ab.de/dreame-lds-board-vpower-v204-gruen-p-66896.html) | [06](06-inventario-ampliado-del-robot.md) |
| 41 | [https://www.ep-mediastore-ab.de/dreame-lds-board-wpftb-v262-gruen-p-42267.html](https://www.ep-mediastore-ab.de/dreame-lds-board-wpftb-v262-gruen-p-42267.html) | [06](06-inventario-ampliado-del-robot.md) |
| 42 | [https://www.ep-mediastore-ab.de/dreame-lds-bracket-rahmen-l10s-ultra-gen3-l40spu-d20-p-26977.html](https://www.ep-mediastore-ab.de/dreame-lds-bracket-rahmen-l10s-ultra-gen3-l40spu-d20-p-26977.html) | [06](06-inventario-ampliado-del-robot.md) |
| 43 | [https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftb-v262-schwarz-p-77339.html](https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftb-v262-schwarz-p-77339.html) | [06](06-inventario-ampliado-del-robot.md) |
| 44 | [https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftbcd-v101-p-41867.html](https://www.ep-mediastore-ab.de/dreame-lds-einheit-wpftbcd-v101-p-41867.html) | [06](06-inventario-ampliado-del-robot.md) |
| 45 | [https://www.ep-mediastore-ab.de/dreame-lds-gehaeuse-fuer-wpftb-v262-p-50112.html](https://www.ep-mediastore-ab.de/dreame-lds-gehaeuse-fuer-wpftb-v262-p-50112.html) | [06](06-inventario-ampliado-del-robot.md) |
| 46 | [https://www.ep-mediastore-ab.de/dreame-lds-laser-board-v2-schwarz-p-40871.html](https://www.ep-mediastore-ab.de/dreame-lds-laser-board-v2-schwarz-p-40871.html) | [06](06-inventario-ampliado-del-robot.md) |
| 47 | [https://www.ep-mediastore-ab.de/dreame-lds-lidar-sensor-l10s-pro-ultra-heat-l20-x30-x40-mova-p-26720.html](https://www.ep-mediastore-ab.de/dreame-lds-lidar-sensor-l10s-pro-ultra-heat-l20-x30-x40-mova-p-26720.html) | [06](06-inventario-ampliado-del-robot.md) |
| 48 | [https://www.ep-mediastore-ab.de/dreame-lds-motor-l10s-pro-ultra-heat-l20-x30-x40-p-54774.html](https://www.ep-mediastore-ab.de/dreame-lds-motor-l10s-pro-ultra-heat-l20-x30-x40-p-54774.html) | [06](06-inventario-ampliado-del-robot.md) |
| 49 | [https://www.ep-mediastore-ab.de/dreame-lds-motor-v2-l10s-pro-ultra-heat-l20-x30-p-27165.html](https://www.ep-mediastore-ab.de/dreame-lds-motor-v2-l10s-pro-ultra-heat-l20-x30-p-27165.html) | [06](06-inventario-ampliado-del-robot.md) |
| 50 | [https://www.ep-mediastore-ab.de/dreame-lds-riemen-l10s-pro-ultra-heat-l20-x30-original-p-58751.html](https://www.ep-mediastore-ab.de/dreame-lds-riemen-l10s-pro-ultra-heat-l20-x30-original-p-58751.html) | [06](06-inventario-ampliado-del-robot.md) |
| 51 | [https://www.ep-mediastore-ab.de/dreame-lds-transfer-board-v2-schwarz-p-27164.html](https://www.ep-mediastore-ab.de/dreame-lds-transfer-board-v2-schwarz-p-27164.html) | [06](06-inventario-ampliado-del-robot.md) |
| 52 | [https://www.ep-mediastore-ab.de/dreame-seitenbuerstenmotor-schwarz-p-55856.html](https://www.ep-mediastore-ab.de/dreame-seitenbuerstenmotor-schwarz-p-55856.html) | [06](06-inventario-ampliado-del-robot.md) |
| 53 | [https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md), [06](06-inventario-ampliado-del-robot.md) |
| 54 | [https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html?page=2](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html?page=2) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md), [06](06-inventario-ampliado-del-robot.md) |
| 55 | [https://www.ep-mediastore-ab.de/images/72990/01/25/12584/rad_lager_splint_4x38.5_mm_stueck-1280x1280.jpg](https://www.ep-mediastore-ab.de/images/72990/01/25/12584/rad_lager_splint_4x38.5_mm_stueck-1280x1280.jpg) | [02](02-repuestos-y-reparacion.md) |
| 56 | [https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280.jpg](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280.jpg) | [02](02-repuestos-y-reparacion.md) |
| 57 | [https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_1.jpg](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_1.jpg) | [02](02-repuestos-y-reparacion.md) |
| 58 | [https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_2.jpg](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_2.jpg) | [02](02-repuestos-y-reparacion.md) |
| 59 | [https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585.gif](https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585.gif) | [02](02-repuestos-y-reparacion.md) |
| 60 | [https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585_1.gif](https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585_1.gif) | [02](02-repuestos-y-reparacion.md) |
| 61 | [https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html](https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 62 | [https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html](https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 63 | [https://www.ep-mediastore-ab.de/saugmotor-hjd-ra60405-xiaomi-s20-x20pro-p-72817.html](https://www.ep-mediastore-ab.de/saugmotor-hjd-ra60405-xiaomi-s20-x20pro-p-72817.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 64 | [https://www.ep-mediastore-ab.de/versand_und_zahlungsbedingungen.php](https://www.ep-mediastore-ab.de/versand_und_zahlungsbedingungen.php) | [02](02-repuestos-y-reparacion.md) |
| 65 | [https://www.ep-mediastore-ab.de/xiaomi-2x-mop-halter-teller-schwarz-x20max-pro-5pro-p-18142.html](https://www.ep-mediastore-ab.de/xiaomi-2x-mop-halter-teller-schwarz-x20max-pro-5pro-p-18142.html) | [06](06-inventario-ampliado-del-robot.md) |
| 66 | [https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-s10-etc-p-55018.html](https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-s10-etc-p-55018.html) | [06](06-inventario-ampliado-del-robot.md) |
| 67 | [https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-vorn-s10-etc-p-42075.html](https://www.ep-mediastore-ab.de/xiaomi-abgrundsensor-vorn-s10-etc-p-42075.html) | [06](06-inventario-ampliado-del-robot.md) |
| 68 | [https://www.ep-mediastore-ab.de/xiaomi-akku-5200mah-p2150-4s2p-scev-fuer-s20-x20-max-pro-original-p-56237.html](https://www.ep-mediastore-ab.de/xiaomi-akku-5200mah-p2150-4s2p-scev-fuer-s20-x20-max-pro-original-p-56237.html) | [02](02-repuestos-y-reparacion.md) |
| 69 | [https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 70 | [https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 71 | [https://www.ep-mediastore-ab.de/xiaomi-bedienboard-kabel-b108eu-p-13988.html](https://www.ep-mediastore-ab.de/xiaomi-bedienboard-kabel-b108eu-p-13988.html) | [06](06-inventario-ampliado-del-robot.md) |
| 72 | [https://www.ep-mediastore-ab.de/xiaomi-bedienknoepfe-x20pro-p-78444.html](https://www.ep-mediastore-ab.de/xiaomi-bedienknoepfe-x20pro-p-78444.html) | [06](06-inventario-ampliado-del-robot.md) |
| 73 | [https://www.ep-mediastore-ab.de/xiaomi-bumper-ir-sensor-kabel-b108eu-p-89488.html](https://www.ep-mediastore-ab.de/xiaomi-bumper-ir-sensor-kabel-b108eu-p-89488.html) | [06](06-inventario-ampliado-del-robot.md) |
| 74 | [https://www.ep-mediastore-ab.de/xiaomi-camsub-board-fuer-bumper-s20-x20max-p-53002.html](https://www.ep-mediastore-ab.de/xiaomi-camsub-board-fuer-bumper-s20-x20max-p-53002.html) | [06](06-inventario-ampliado-del-robot.md) |
| 75 | [https://www.ep-mediastore-ab.de/xiaomi-dock-ir-sensor-d102-x20m-p-26830.html](https://www.ep-mediastore-ab.de/xiaomi-dock-ir-sensor-d102-x20m-p-26830.html) | [01](01-arquitectura-y-desmontaje.md) |
| 76 | [https://www.ep-mediastore-ab.de/xiaomi-dreame-lautsprecher-36mm-p-68441.html](https://www.ep-mediastore-ab.de/xiaomi-dreame-lautsprecher-36mm-p-68441.html) | [06](06-inventario-ampliado-del-robot.md) |
| 77 | [https://www.ep-mediastore-ab.de/xiaomi-dreame-lds-kabel-9cm-p-72988.html](https://www.ep-mediastore-ab.de/xiaomi-dreame-lds-kabel-9cm-p-72988.html) | [06](06-inventario-ampliado-del-robot.md) |
| 78 | [https://www.ep-mediastore-ab.de/xiaomi-dustbin-sensor-kabel-b108eu-p-70969.html](https://www.ep-mediastore-ab.de/xiaomi-dustbin-sensor-kabel-b108eu-p-70969.html) | [06](06-inventario-ampliado-del-robot.md) |
| 79 | [https://www.ep-mediastore-ab.de/xiaomi-front-kamera-fuer-bumper-s20-x20max-p-50096.html](https://www.ep-mediastore-ab.de/xiaomi-front-kamera-fuer-bumper-s20-x20max-p-50096.html) | [06](06-inventario-ampliado-del-robot.md) |
| 80 | [https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-schwarz-s20-x20max-p-58034.html](https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-schwarz-s20-x20max-p-58034.html) | [06](06-inventario-ampliado-del-robot.md) |
| 81 | [https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-weiss-s20-x20pro-p-70759.html](https://www.ep-mediastore-ab.de/xiaomi-frontbumper-mit-kamera-weiss-s20-x20pro-p-70759.html) | [06](06-inventario-ampliado-del-robot.md) |
| 82 | [https://www.ep-mediastore-ab.de/xiaomi-gummi-tuelle-filter-x20pro-p-66031.html](https://www.ep-mediastore-ab.de/xiaomi-gummi-tuelle-filter-x20pro-p-66031.html) | [06](06-inventario-ampliado-del-robot.md) |
| 83 | [https://www.ep-mediastore-ab.de/xiaomi-ir-sensor-rechts-fuer-bumper-s20-x20max-p-52012.html](https://www.ep-mediastore-ab.de/xiaomi-ir-sensor-rechts-fuer-bumper-s20-x20max-p-52012.html) | [06](06-inventario-ampliado-del-robot.md) |
| 84 | [https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-schwarz-s20-x20max-p-26811.html](https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-schwarz-s20-x20max-p-26811.html) | [06](06-inventario-ampliado-del-robot.md) |
| 85 | [https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-weiss-s20-x20pro-p-29986.html](https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-weiss-s20-x20pro-p-29986.html) | [02](02-repuestos-y-reparacion.md) |
| 86 | [https://www.ep-mediastore-ab.de/xiaomi-lds-einheit-wpftb-v262-orange-p-42740.html](https://www.ep-mediastore-ab.de/xiaomi-lds-einheit-wpftb-v262-orange-p-42740.html) | [06](06-inventario-ampliado-del-robot.md) |
| 87 | [https://www.ep-mediastore-ab.de/xiaomi-lidar-deckel-feder-weiss-x10-s10-s20-p-88027.html](https://www.ep-mediastore-ab.de/xiaomi-lidar-deckel-feder-weiss-x10-s10-s20-p-88027.html) | [06](06-inventario-ampliado-del-robot.md) |
| 88 | [https://www.ep-mediastore-ab.de/xiaomi-radfeder-62x32-45mm-p-37935.html](https://www.ep-mediastore-ab.de/xiaomi-radfeder-62x32-45mm-p-37935.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 89 | [https://www.ep-mediastore-ab.de/xiaomi-reset-board-btn-b108eu-p-63078.html](https://www.ep-mediastore-ab.de/xiaomi-reset-board-btn-b108eu-p-63078.html) | [06](06-inventario-ampliado-del-robot.md) |
| 90 | [https://www.ep-mediastore-ab.de/xiaomi-saugmotor-kabel-4pin-42cm-p-35389.html](https://www.ep-mediastore-ab.de/xiaomi-saugmotor-kabel-4pin-42cm-p-35389.html) | [06](06-inventario-ampliado-del-robot.md) |
| 91 | [https://www.ep-mediastore-ab.de/xiaomi-staubbehaelter-x20-pro-weiss-p-50066.html](https://www.ep-mediastore-ab.de/xiaomi-staubbehaelter-x20-pro-weiss-p-50066.html) | [06](06-inventario-ampliado-del-robot.md) |
| 92 | [https://www.ep-mediastore-ab.de/xiaomi-wischmotoren-x20-pro-p-29890.html](https://www.ep-mediastore-ab.de/xiaomi-wischmotoren-x20-pro-p-29890.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 93 | [https://www.ep-mediastore-ab.de/xiaomi-x20-max-gehaeuse-komplett-p-41414.html](https://www.ep-mediastore-ab.de/xiaomi-x20-max-gehaeuse-komplett-p-41414.html) | [02](02-repuestos-y-reparacion.md) |
| 94 | [https://www.ep-mediastore-ab.de/xiaomi-x20-pro-mainboard-b108eumb-p-40091.html](https://www.ep-mediastore-ab.de/xiaomi-x20-pro-mainboard-b108eumb-p-40091.html) | [01](01-arquitectura-y-desmontaje.md), [02](02-repuestos-y-reparacion.md) |
| 95 | [https://www.facebook.com/eliandro.martins.340852/videos/rob%C3%B4-aspirador-xiaomi-x20-max-desmontagem-completa/1459675169547042/](https://www.facebook.com/eliandro.martins.340852/videos/rob%C3%B4-aspirador-xiaomi-x20-max-desmontagem-completa/1459675169547042/) | [01](01-arquitectura-y-desmontaje.md) |
| 96 | [https://www.fixshop.eu/spare-parts-vacuum-cleaner-parts-accessories-spare-parts-engine/xiaomi-robot-vacuum-x20-s10-dreame-x30-x20-x10-pro-wheel-with-motor-left-white/](https://www.fixshop.eu/spare-parts-vacuum-cleaner-parts-accessories-spare-parts-engine/xiaomi-robot-vacuum-x20-s10-dreame-x30-x20-x10-pro-wheel-with-motor-left-white/) | [02](02-repuestos-y-reparacion.md) |
| 97 | [https://www.kleinanzeigen.de/s-anzeige/xiaomi-x20-pro-saugroboter-mit-wischfunktion-defekt/3524161933-176-1857](https://www.kleinanzeigen.de/s-anzeige/xiaomi-x20-pro-saugroboter-mit-wischfunktion-defekt/3524161933-176-1857) | [02](02-repuestos-y-reparacion.md) |
| 98 | [https://www.leespring.com/learn-about-extension-springs](https://www.leespring.com/learn-about-extension-springs) | [02](02-repuestos-y-reparacion.md) |
| 99 | [https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/](https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/) | [01](01-arquitectura-y-desmontaje.md) |
| 100 | [https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/specs/](https://www.mi.com/es/product/xiaomi-robot-vacuum-x20-pro/specs/) | [01](01-arquitectura-y-desmontaje.md) |
| 101 | [https://www.mi.com/es/support/faq/details/KA-922892/](https://www.mi.com/es/support/faq/details/KA-922892/) | [01](01-arquitectura-y-desmontaje.md) |
| 102 | [https://www.mi.com/global/product/xiaomi-robot-vacuum-x20-pro/specs/](https://www.mi.com/global/product/xiaomi-robot-vacuum-x20-pro/specs/) | [02](02-repuestos-y-reparacion.md) |
| 103 | [https://www.mi.com/global/support/faq/details/KA-445208/](https://www.mi.com/global/support/faq/details/KA-445208/) | [01](01-arquitectura-y-desmontaje.md) |
| 104 | [https://www.mitutoyo.com/webfoo/wp-content/uploads/D_section.pdf](https://www.mitutoyo.com/webfoo/wp-content/uploads/D_section.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
| 105 | [https://www.mwcomponents.com/how-to-select-an-extension-spring](https://www.mwcomponents.com/how-to-select-an-extension-spring) | [02](02-repuestos-y-reparacion.md) |
| 106 | [https://www.printables.com/model/1745789-xiaomi-x20-pro-x20-max-filter-storage-holder-store](https://www.printables.com/model/1745789-xiaomi-x20-pro-x20-max-filter-storage-holder-store) | [02](02-repuestos-y-reparacion.md) |
| 107 | [https://www.printables.com/model/990525-wheel-holder-for-mi-robot-vacuum-mop-essential/user-gcodes](https://www.printables.com/model/990525-wheel-holder-for-mi-robot-vacuum-mop-essential/user-gcodes) | [02](02-repuestos-y-reparacion.md) |
| 108 | [https://www.reddit.com/r/RobotVacuums/comments/1t2604u/need_help_with_my_xiaomi_x20_pro_one_wheel_stays/](https://www.reddit.com/r/RobotVacuums/comments/1t2604u/need_help_with_my_xiaomi_x20_pro_one_wheel_stays/) | [02](02-repuestos-y-reparacion.md) |
| 109 | [https://www.spirol.com/assets/files/ins-wp-how-to-design-the-proper-hole-for-heat-ultrasonic-inserts-us.pdf](https://www.spirol.com/assets/files/ins-wp-how-to-design-the-proper-hole-for-heat-ultrasonic-inserts-us.pdf) | [03](03-ingenieria-fisica-y-cad.md) |
