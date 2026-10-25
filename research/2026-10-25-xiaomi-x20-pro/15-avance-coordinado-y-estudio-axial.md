# 15. Avance coordinado: cotas públicas, servicio y estudio axial

**25-10-2026.** Esta entrega integra trabajo de ChatGPT y del compañero Codex del chat «Explora cómo avanzar Oomwoo». Se conserva el objetivo: base resistente propia, módulos útiles del Xiaomi y mantenimiento mediante piezas reemplazables. La electrónica original es una fase de transición; no se declara abierto su firmware.

## 1. Coordinación recibida y trabajo integrado

El intercambio se realizó mediante `coordinacion/` del checkout compartido. Se recibió y leyó el acuse del compañero, su aportación `f4d87c5` sobre cotas públicas y presupuesto axial, y su revisión posterior `cd882f0` sobre IF01–IF04 e IF13. No se atribuyen al compañero las pruebas de software realizadas por ChatGPT.

| Aportación | Responsable y resultado |
|---|---|
| Prioridad de fuentes públicas y análisis axial | Codex, integrado en 07, 12 y 14; cable publicado sincronizado en `repuestos.csv`. |
| Cargas, desmontaje y repetición de posición al reinstalar | Codex, ampliación de [cad/REVISION.md](cad/REVISION.md). |
| Contraste de fuentes y conversión del cálculo a CAD | ChatGPT, [estudio nativo separado](cad/estudios/README.md). |
| Captura física opcional e importación | ChatGPT y revisiones auxiliares de guía/contrato, [capturas_rueda/](capturas_rueda/README.md). |
| Pruebas en el PC y publicación integrada | ChatGPT; registros de resultados con sus límites. |

**Fuentes públicas primero.** Se ha incorporado la corrección del propietario trasladada por Codex: rellenar un formulario no es condición para avanzar el primer CAD. Se buscan cotas exactas, despieces y referencias públicas; los valores nominales publicados se distinguen de medidas de esta unidad. Una dimensión no publicada continúa pendiente o como hipótesis expresamente identificada. No se completan coordenadas con cifras inventadas.

La nueva herramienta de captura sólo facilita una comprobación física posterior. No exige volver a enviar las fotos generales ni conservar los fragmentos desaparecidos.

## 2. Resultado dimensional concreto

El vendedor publica **Ø4 × 38,5 mm** para el pasador SKU12584 y declara compatibilidad con X20 Pro [S1]. Los módulos de rueda izquierdo/derecho anuncian **115 mm de cable hasta conector** [S2–S3]; esa longitud no es recorrido disponible de suspensión.

El estudio DEMO v0.1 emplea una disposición ilustrativa de 26 mm de hueco, dos apoyos de 8 mm y salientes de 4 mm a cada extremo. El presupuesto axial desarrollado por Codex da:

| Configuración | Longitud requerida | Exceso respecto a 38,5 mm |
|---|---:|---:|
| DEMO con dos salientes | 4 + 8 + 26 + 8 + 4 = **50 mm** | **11,5 mm** |
| DEMO sin ambos salientes | 8 + 26 + 8 = **42 mm** | **3,5 mm** |
| Nominal comercial | **38,5 mm** | Referencia publicada, sin tolerancia |

![Presupuesto axial del estudio](cad/estudios/presupuesto_axial.svg)

No basta cambiar de Ø5 a Ø4 en el DEMO. Esa combinación de hueco y apoyos tampoco cabe longitudinalmente. **Se descarta esa distribución para ese nominal**, conservando pendiente el ancho móvil que deba alojarse. No se reduce artificialmente el hueco para obtener una suma favorable.

El archivo [X20Pro_Estudio_Axial_Publicado.FCStd](cad/estudios/X20Pro_Estudio_Axial_Publicado.FCStd) hace editable ese cálculo. Incluye los dos cilindros de referencia, bandas de presupuesto y una hoja con fórmulas. No es el conjunto final de rueda ni un archivo para imprimir. El maestro [X20Pro_Base_Arquitectura.FCStd](cad/X20Pro_Base_Arquitectura.FCStd) conserva su revisión anterior.

## 3. Qué cambia en la propuesta de mantenimiento

La revisión independiente concreta una arquitectura para desarrollar: **extraer el cartucho completo con la suspensión contenida** y, cuando el espacio interior no permita sacar el pasador, realizar esa operación en banco. Esto puede evitar reservar dentro del robot todo el recorrido axial de extracción, pero aún exige resolver la salida del cartucho, el conector y el acceso de herramienta. No se ha fijado una dirección de salida ni se ha comprobado el espacio real.

Cada lado debe distinguir reacción transversal, empuje axial y retención del pasador. La fijación al núcleo debe distinguir superficies de localización y función de apriete; el conjunto ha de recuperar su posición al reinstalarlo. La revisión también enlaza ese requisito con las posturas de la estación, cuyos apoyos y acoplamientos siguen pendientes. Son propuestas y condiciones de aceptación, no ensayos superados. Los principios generales de localización/apriete tienen apoyo en Carr Lane [S4], sin trasladar a este robot las cargas o tolerancias de utillajes industriales.

La secuencia debe contener la energía del muelle antes de liberar pivote o anclajes; desconectar un cable no descarga el muelle. Lee Spring describe el almacenamiento de energía y fuerza de restitución de los muelles de tracción [S5]. No se prescribe aún una maniobra concreta de descarga para la rueda dañada.

Dos vínculos se han identificado para actualizar conjuntamente en la próxima revisión del registro y del maestro: **IF02 → M15 por lado** y **IF04 → IF13 / M55 / M60**. Se conservan como pendientes explícitos: escribirlos en una revisión documental no modifica automáticamente los objetos CAD.

## 4. Comprobación física opcional, preparada

[Capturar_Rueda.html](capturas_rueda/Capturar_Rueda.html) funciona sin conexión. Permite empezar con diámetro/longitud del pasador, guardar pendientes y ampliar seis magnitudes más de la rueda. La guía muestra qué caras y ejes se están describiendo, sin afirmar que sus dibujos sean geometría Xiaomi.

El JSON separa identidad de rueda, identidad de pasador, lado, correspondencia, fuente, fecha, instrumento, condición, lecturas y daños. Un pendiente es `null`; una estimación no habilita geometría medida. Los números de catálogo continúan en el estudio público y no se presentan como lecturas físicas.

La macro valida de nuevo el archivo y crea **otro documento FreeCAD**. Con dos medidas declaradas y sección circular identificada puede crear una referencia cilíndrica local. No reconstruye extremos o retención ni modifica el maestro, el DEMO o `mediciones.csv`. La ficha no aprueba fabricación.

## 5. Verificación realmente ejecutada

| Comprobación | Resultado y límite |
|---|---|
| Contrato de datos | 23 pruebas superadas; fixtures sintéticos. |
| Paridad Python/JavaScript | 66 entradas comparadas, sin diferencias de aceptación o permisos de geometría en esos casos. |
| Revisión de identidad | Se corrigió la aceptación de un mismo ID para rueda y pasador; se comprueban también espacios y mayúsculas. |
| Importación FreeCAD 1.1.4 | Pendientes sin geometría, prueba sintética explícita, ficha inválida rechazada antes de crear, guardado/reapertura y rechazo de sobrescritura. |
| Texto de captura | Una referencia que comienza por `=` se mantiene como texto en la hoja. |
| Estudio axial | Siete sólidos válidos; valores y diferencias comprobados; cambio de hueco DEMO 26 → 30 mueve el apoyo 4 mm y longitud 50 → 54. Valores restaurados al guardar. |
| Maestro y registro | SHA-256 antes/después idénticos; no se registraron medidas físicas nuevas. |
| Guía SVG | XML, identificadores y render revisados. |
| Interacción HTML completa | No se ha ejecutado una validación automatizada de toda la interfaz de navegador; sí de sus reglas, sintaxis y construcción. |
| Montaje, resistencia y funcionamiento | No ensayados. No se aprueba fabricar ni instalar. |

El primer arnés FreeCAD se interrumpió por consultar `Name` después de cerrar un documento; se corrigió el arnés y la segunda ejecución completó las comprobaciones. El [registro de software](cad/estudios/validacion_software.json) recoge resultados y hashes. Las [pruebas portátiles](capturas_rueda/pruebas/README.md) permiten repetir el contrato; [verificar_software.FCMacro](cad/estudios/verificar_software.FCMacro) conserva el núcleo de comprobación FreeCAD con selección portátil de carpeta y salidas temporales, sin cerrar documentos ajenos. Esa adaptación de selector no ha pasado una nueva prueba interactiva.

## 6. Próximo trabajo de geometría

El siguiente avance es resolver una variante provisional de **asiento del cartucho y extracción del conjunto**, con la restricción axial publicada visible y las incógnitas de la mitad móvil separadas. Las fuentes públicas se agotan primero; el estudio puede comparar hipótesis sin declararlas medidas. No corresponde imprimir una base grande antes de resolver interfaces, retención, barridos y acoplamiento con estación.

La salida debe conservar estructura resistente en el núcleo y apoyos/anclajes reemplazables en piezas accesibles. No se ha demostrado todavía que una combinación de espesores o material concreto sea más resistente que la original.

## Fuentes de esta integración

- [S1 · Pasador SKU12584, Ø4 × 38,5 mm](https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html).
- [S2 · Módulo izquierdo SKU12585, cable 11,5 cm](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html).
- [S3 · Módulo derecho SKU13025, cable 11,5 cm](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html).
- [S4 · Carr Lane, principios de localización y apriete](https://www.carrlane.com/engineering-resources/fixture-design-principles/locating-clamping-principles/ctl).
- [S5 · Lee Spring, muelles de tracción](https://www.leespring.com/learn-about-extension-springs).

Fuentes públicas contrastadas el 25-10-2026. Los nominales del vendedor no son planos ni garantías dimensionales OEM. La autoría y alcance de cada entrega se conservan en [coordinación](coordinacion/entrega_integrada.md).
