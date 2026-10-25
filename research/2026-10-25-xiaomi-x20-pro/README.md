# Xiaomi X20 Pro: base propia, reparación modular y control abierto por fases

**Investigación actualizada el 25 de octubre de 2026.** Equipo: Xiaomi Robot Vacuum X20 Pro, D102GL, con estación europea D102-JZEU. Caso del proyecto [Fábrica Doméstica Autónoma Abierta](https://github.com/Valdi320/Valdo).

## Objetivo vigente

El propietario ha decidido **abandonar la reparación de la carcasa original**, ya desmontada, debido a las roturas que observa. El trabajo actual consiste en recuperar los conjuntos aprovechables y diseñar una estructura nueva, resistente y fácil de mantener, con presupuesto limitado. Se conservan inicialmente electrónica, firmware, batería cerrada, arneses y estación originales. El objetivo final incluye control abierto; la etapa con firmware Xiaomi es provisional. Los fragmentos rotos ya no están y no son una dependencia del diseño nuevo.

El plan de «reparar primero y ampliar después» pertenece a una fase anterior y **ya no es un requisito**. Los capítulos de repuestos y reparación siguen siendo referencias útiles para piezas concretas; la ejecución vigente está en [07 — Plan del chasis propio](07-plan-del-chasis-propio.md).

**Arquitectura elegida para desarrollar:** núcleo resistente propio y soportes funcionales reemplazables, evaluando caminos de carga metálicos y adaptadores pequeños. Se diseña alrededor de las interfaces del Xiaomi y se aprovechan las piezas o soluciones de OOMWOO que reduzcan trabajo. No hay evidencia suficiente para afirmar que sustituir la electrónica dentro de un chasis OOMWOO completo sea actualmente la opción más sencilla. La comparación detallada, archivos comprobados y condiciones que cambiarían esta decisión están en [09 — OOMWOO](09-oomwoo-comparacion.md).

## Qué ya está documentado

- Arquitectura funcional, acceso, repuestos específicos y límites de compatibilidad del Pro. Un catálogo comercial no se trata como despiece oficial.
- Herramientas mínimas: documentación y Git, FreeCAD como CAD principal y un laminador cuando exista una pieza para fabricar. Las herramientas electrónicas, escáneres y simulación avanzada se incorporan solo para una necesidad concreta.
- Plan de geometría, suspensión, módulos extraíbles, estación, fabricación y pruebas. La primera pieza piloto pertenece al chasis nuevo; no depende de que el plástico antiguo vuelva a sostener cargas.
- Revisión crítica documentada en [08 — Refutaciones y decisiones](08-refutaciones-y-decisiones.md), con separación entre decisiones estables e incógnitas físicas.
- Inspección de **18 fotografías únicas** de esta unidad. Las fotos confirman referencias y distribución de varios conjuntos; no su funcionamiento, materiales ni medidas. [10 — Inventario observado](10-inventario-fotografico.md).
- Auditoría de archivos reales de OOMWOO, distinguiendo el diseño principal de su experimento de CAD automático. Su estado se comprueba en fuentes originales, no en imágenes promocionales.

**Ya existe un [proyecto FreeCAD nativo](cad/README.md), generado y reabierto con FreeCAD 1.1.4 en el PC.** Contiene la envolvente publicada, 13 registros de módulos, 14 interfaces y un estudio paramétrico independiente de cartucho. No contiene una base fabricable ni cotas internas medidas. No se ha fabricado un bastidor, ensayado una suspensión o validado un pinout. [Entrega y verificación](14-entrega-cad-y-siguiente-medicion.md).

**Último avance coordinado:** se han integrado las aportaciones de Codex sobre cotas públicas, espacio axial y mantenimiento. El [estudio FreeCAD de presupuesto axial](cad/estudios/README.md) contrasta el pasador comercial de 38,5 mm con los 50 mm que necesita la disposición DEMO, y descarta esa combinación. La [revisión de servicio](cad/REVISION.md) concreta la extracción del cartucho con suspensión contenida. [Entrega conjunta y pruebas](15-avance-coordinado-y-estudio-axial.md).

La investigación pública precede a pedir medidas al propietario. La [captura con guía visual](capturas_rueda/README.md) es opcional para comprobar piezas posteriormente; no bloquea el CAD provisional.

## Tres formas de aprovechar OOMWOO

| Ruta | Aplicación al Xiaomi | Decisión actual |
|---|---|---|
| Aprovechar conocimientos y piezas independientes | Soluciones de acceso, división de piezas, sujeción y fabricación, adaptadas a las medidas Xiaomi | Favorable. Se evalúa cada pieza por el trabajo que ahorra. |
| Derivar parte del bastidor principal | Importar una revisión identificada, superponer volúmenes Xiaomi y conservar las zonas que sirvan | Abierta. Antes hay que comprobar edición, unidades y compatibilidad geométrica. |
| Trasplantar todos los conjuntos al chasis completo | Cambiar soportes, frontal, suspensión, limpieza y acoplamiento según lo que realmente no coincida | No es el atajo recomendado con la evidencia actual. Podría acabar exigiendo rehacer casi toda la base. |

La comparación se decide por **interfaces conservadas, piezas que hay que rehacer y coste de fabricación**, no por el número de archivos descargables. No se presupone que ambos robots compartan geometría por ser circulares.

## Qué se conserva y qué se puede cambiar

La unidad muestra una placa principal curva, conjuntos de aspiración y mopas, módulos de rueda y un frontal óptico distribuido con cable flexible. Se tratarán como conjuntos con volumen, fijaciones, movimiento y espacio de acceso. Su integridad mecánica y su funcionamiento eléctrico se registran por separado.

Los apoyos dañados pueden reconstruirse. Las carcasas que sitúan engranajes, cojinetes u óptica necesitan una evaluación distinta de una tapa exterior. Conservar un motor no obliga a conservar plástico roto, pero tampoco convierte una reductora de precisión en una pieza trivial de imprimir.

El nuevo chasis debe mantener o verificar geometría de rodadura, orientación de sensores, movimiento del paragolpes, alturas de limpieza y acoplamiento con la estación. La electrónica original no garantiza que el firmware se adapte a cualquier distribución nueva.

## CAD entregado y siguiente avance físico

El maestro es [cad/X20Pro_Base_Arquitectura.FCStd](cad/X20Pro_Base_Arquitectura.FCStd). La propuesta estructural está en 11, la geometría funcional en 12 y la transición de control en 13. La [guía 14](14-entrega-cad-y-siguiente-medicion.md) delimita qué se ha ejecutado y qué requiere medir.

1. **Ensamblaje de volúmenes simplificados:** medidas exteriores y fijaciones de placa con cubierta, batería, turbina, ruedas y mopas, en un sistema de coordenadas común.
2. **Comparación geométrica con el diseño principal de OOMWOO:** identificar qué base o piezas se pueden conservar y qué hay que reconstruir. No imprimir una carcasa grande para descubrirlo.
3. **Piloto de suspensión en soporte propio:** conservar eje y movimiento, caracterizar el muelle disponible y comprobar fuerza frente a desplazamiento, retorno y retención.
4. **Bastidor de presentación:** comprobar el conjunto completo sin energía antes de las pruebas funcionales definidas en el capítulo 07.

Las fotos recibidas no incluyen escala metrológica suficiente ni documentan las interfaces de la estación. Se buscan primero cotas y referencias públicas para avanzar con parámetros provisionales. La comprobación física posterior será dirigida a las incógnitas restantes; no exige volver a fotografiar indiscriminadamente todo el robot. El [inventario fotográfico](10-inventario-fotografico.md) especifica los huecos de evidencia.

## Guía de archivos

| Archivo | Contenido y estado |
|---|---|
| [01 — Arquitectura y desmontaje](01-arquitectura-y-desmontaje.md) | Investigación de modelo, funciones, acceso y referencias. Las rutas iniciales de reparación son contexto histórico. |
| [02 — Repuestos y reparación](02-repuestos-y-reparacion.md) | Piezas, fuentes, precios observados y alternativas locales. No orden de compra. |
| [03 — Ingeniería física y CAD](03-ingenieria-fisica-y-cad.md) | Metrología, materiales, uniones y fuentes técnicas. |
| [04 — Plan anterior](04-plan-de-trabajo-y-mediciones.md) | Secuencia histórica de reparación localizada; sustituida por 07. |
| [05 — Fuentes y límites](05-fuentes-y-limites.md) | Fuentes de la investigación inicial; los capítulos nuevos añaden sus propias referencias. |
| [06 — Inventario de catálogo](06-inventario-ampliado-del-robot.md) | Recambios y variantes comercializadas, separados de lo instalado realmente. |
| [07 — Chasis propio](07-plan-del-chasis-propio.md) | Plan vigente de herramientas, diseño, fabricación y pruebas. |
| [08 — Refutaciones](08-refutaciones-y-decisiones.md) | Objeciones, cambios y criterio de cierre de la planificación. |
| [09 — OOMWOO](09-oomwoo-comparacion.md) | Auditoría de archivos y comparación para el trasplante. |
| [10 — Fotos de la unidad](10-inventario-fotografico.md) | Observaciones verificables por identificador, sin publicar fotos ni seriales. |
| [11 — Base resistente](11-base-resistente-y-reconstruccion.md) | Reconstrucción sin fragmentos, estructura e interfaces reemplazables. |
| [12 — Mecanismos y estación](12-interfaces-mecanicas-y-estacion.md) | Rodadura, suspensión, limpieza, acoplamiento y medidas M40–M60. |
| [13 — Electrónica y control abierto](13-electronica-y-control-abierto.md) | Montajes, medidas M70–M89, software comprobado y apertura por fases. |
| [14 — Entrega CAD](14-entrega-cad-y-siguiente-medicion.md) | Ejecución real, verificación, siguiente captura y coordinación de checkout. |
| [15 — Avance coordinado](15-avance-coordinado-y-estudio-axial.md) | Aportaciones de ambos compañeros, presupuesto axial, servicio y comprobaciones de software. |
| [cad/](cad/README.md) | FCStd editable, macro, interfaces, STEP DEMO, vistas, licencia y validación. |
| [cad/estudios/](cad/estudios/README.md) | Estudio nativo del pasador publicado y comparación con el DEMO; sin aprobación de fabricación. |
| [capturas_rueda/](capturas_rueda/README.md) | Formulario opcional sin conexión, dibujos, JSON, validador y macro de documento independiente. |

Datos reutilizables: [repuestos](repuestos.csv), [mediciones](mediciones.csv), [intervenciones](registro-intervenciones.csv), [módulos observados](electronica-modulos.csv), [conexiones](electronica-conexiones.csv) y [comandos/pruebas](comandos-pruebas.csv). Los campos desconocidos permanecen explícitos; ningún ensayo se registra como realizado por una revisión documental.

Versión continua para leer sin conexión: **[Dossier_Xiaomi_X20_Pro.html](Dossier_Xiaomi_X20_Pro.html)**.

## Límites que siguen abiertos

No se ha determinado la composición o causa de fragilidad de los plásticos de esta unidad, ni la frecuencia del problema en toda la serie. Las roturas comunicadas justifican el objetivo del propietario, pero no permiten atribuir una causa material concreta a partir de las fotografías.

El coste de fabricación se cotizará cuando haya piezas, proceso y revisiones definidos. El software gratuito no elimina material, herrajes, portes ni iteraciones. No hace falta comprar impresora, escáner o una controladora para completar la primera comparación CAD.

Control dimensional significa disponer de geometría editable, medidas, ajustes y piezas reproducibles. No equivale a independencia del firmware ni a durabilidad probada. El control abierto es un objetivo posterior explícito: la bandeja de electrónica debe permitir una sustitución localizada si no se puede abrir la placa original. Valetudo no incluye oficialmente D102GL; las integraciones de alto nivel no son un controlador de motores abierto. Véanse fuentes y límites en 13. Las fotos originales se conservan aparte del repositorio público; el dossier cita sus identificadores. Los archivos ajenos se enlazan a sus fuentes y revisiones.
