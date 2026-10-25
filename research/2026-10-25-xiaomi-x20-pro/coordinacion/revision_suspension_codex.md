# Aportación Codex: asiento y suspensión reproducible

25-10-2026. Revisados `requisito_suspension_reproducible.md`, capítulo 16, esquema y entrega en el checkout de integración `adf76ab`. La lámina metálica se trata como candidata, no como decisión validada. No se han editado capítulo 16, README principal, 07 ni 12.

## Resultado de la revisión y próximo paso geométrico

El capítulo 16 ya recoge la contraparte móvil, desgaste del contacto, mordaza reemplazable, fuerza en rueda y límites de la fatiga. No se devuelven como carencias. La brecha pendiente es convertir la contención y descarga en geometría y secuencia verificables, tal como reconoce el propio esquema.

1. **Tres fijaciones independientes:** cartucho→núcleo, mordaza de lámina y retén de pivote. Los dos tornillos del asiento A liberan solo la primera. La mordaza y el retén permanecen cerrados al extraer el cartucho. En banco: contener rueda, descargar el elemento elástico de forma controlada y solo entonces liberar el consumible. Aflojar la raíz bajo carga no es un procedimiento de descarga. La contención y los topes necesitan piezas propias; cable y detector no cumplen esa función.
2. **Referencia concreta para la mordaza.** Al dimensionar la longitud activa ya prevista en 16, representar el tope de inserción y el borde de salida de la mordaza. Así la misma lámina vuelve a la misma referencia sin colocarla a ojo. La mordaza sustituible debe permanecer independiente de los tornillos que extraen el cartucho.
3. **Comprobación de la próxima variante.** Con los tornillos del asiento retirados, comprobar en el CAD que siguen presentes los retenes de pivote, lámina y rueda, y dibujar la pieza que permite descargar antes de abrir la mordaza. Añadir el módulo, contacto móvil y cable al volumen de extracción; la comprobación de la placa que aporta Codex no cubre esos elementos. Comparar entonces lámina y alambre sobre el mismo asiento y con la misma secuencia de servicio.

Estos son puntos de diseño y revisión, no nuevas cotas de Xiaomi ni resultados físicos.

## Trabajo propio preparado

- Commit local `8f751b4`: el estudio axial 0.3 conserva los nominales de fuente y distingue escenarios; corrige el resultado global de verificación para que un fallo de preservación no pueda dar éxito. Macro, archivo nativo y control negativo sobre copia comprobados; registro junto al estudio.
- `cad/estudios/X20Pro_Asiento_Desmontable_DEMO.FCStd`: propuesta geométrica A con tres apoyos, redondo R y ranura D, fijaciones independientes y elevación normal. Todas las cotas son ilustrativas. El núcleo lleva resaltes integrales en el esquema; la unión hembra de las fijaciones aún no está diseñada. No contiene rueda ni suspensión y no valida la salida de un cartucho completo.

**Estado del asiento:** completada la comprobación final tras resultado LIBRE del cerrojo. Dieciséis comprobaciones correctas en FreeCAD 1.1.4, capturas revisadas y registro `cad/estudios/validacion_asiento.json`. Se verificó el barrido continuo de la placa, no el cartucho completo. La entrega local incluye su FCStd editable, vistas y documentación. La corrección axial `8f751b4` está terminada y disponible por separado; las series f4d87c5/cd882f0 ya están integradas y no deben volver a aplicarse.

Entrega para el integrador: primero `outputs/X20-Pro-corregir-estudio-axial.patch` (8f751b4) y después `outputs/X20-Pro-asiento-desmontable.patch`, ambos en `/home/Valdi/Documents/Codex/2026-10-25/mi`. El segundo contiene solo la aportación del asiento y esta investigación de cierres; no repite la corrección axial.

Esta aportación no modifica el maestro, `mediciones.csv` ni interfaces. Se reconoce la ampliación de metadatos de M44 que ya hizo ChatGPT en su integración; los hashes de nuestras comprobaciones se refieren a nuestra base d8a6b0b. Los vínculos IF02→M15 e IF04→IF13/M55/M60 siguen pendientes de actualización conjunta. No se ha hecho push, PR ni merge.

## Petición nueva del propietario: mantenimiento sin herramientas

El propietario pide investigar una solución que aporte la función de los tornillos sin necesitar herramientas, simplificando el uso sin perder funcionalidad. Se incorpora como criterio de diseño de los cierres de servicio. La nota `avance_suspension_cad_v03.md` reserva a ChatGPT el cartucho comparativo y la corrección conjunta de interfaces; esta aportación no invade esos archivos.

| Candidato | Qué aporta | Qué falta resolver en nuestro cartucho |
|---|---|---|
| Tornillo cautivo con pomo o ala | Accionamiento a mano y pieza que no se pierde; conserva una unión roscada. Es la adaptación inicial más directa del asiento A. | Apriete manual suficiente y repetible, protección frente a aflojamiento y espacio real para dedos. Un retenedor cautivo no bloquea el giro. |
| Palanca sobrecentro con seguro separado | Cierre y apertura rápidos con una palanca; el seguro exige una acción deliberada adicional. Candidato para simplificar el mantenimiento frecuente. | Fuerza dirigida hacia los apoyos, tope final, compensación de holgura, protección de palanca/seguro contra golpes, acceso y fabricación reproducible de ejes y enlaces. |
| Cuarto de vuelta con mando manual | Giro corto; puede permanecer cautivo y adoptar anilla abatible. | Leva y receptor emparejados, espesor acumulado, apriete y retención de posición. La retención antivibración no equivale a un seguro independiente. |

Referencias primarias consultadas 25-10-2026:

- [Southco 52, tornillos cautivos miniatura](https://southco.com/en_us_int/fasteners/captive-screws/captive-screws/52-miniature-captive-screws): variantes accionables a mano. Referencia de función, no elección de esa pieza ni prueba de apriete suficiente en el robot.
- [Ganter GN 464.2](https://www.ganternorm.com/en/products/2.2-Tensioning-clamping-withknobs/Knurled-screws-Knurled-nuts/GN-464.2-Knurled-Screws-Steel-Stainless-Steel-with-Thin-Shank-for-Loss-Prevention-Flat-Type): vástago reducido y segunda rosca para evitar pérdida del tornillo. Es una referencia concreta de cautividad, no de bloqueo contra aflojamiento.
- [Ganter GN 851.3](https://live-katalog.ganternorm.com/pdf/ganter/DE/851_3.pdf?dispositiontype=attachment): cierre de palanca con gancho de bloqueo positivo y desbloqueo manual; referencia del mecanismo de seguro. Sus dimensiones y cargas comerciales no se trasladan a nuestro diseño.
- [Southco D2 Rapier](https://media.southco.com/media/static/Literature/d2.en.pdf): leva espiral, receptor, tope y retención de posición resistente a vibraciones; retenedor opcional y variantes de accionamiento manual. Catálogo técnico histórico, sin afirmación de existencias actuales.
- [EMKA 1000-U790](https://www.emka.com/products/1000-u790): ejemplo de cierre manual de compresión; el fabricante exige comprobación según montaje y condiciones. Su declaración de vibración no certifica nuestra aplicación.

**Decisión de estudio:** comparar primero un pomo cautivo como adaptación sencilla y una palanca con seguro como candidato de apertura rápida. El cuarto de vuelta queda como alternativa de implantación. Se diseñará geometría propia; no se han importado planos/CAD comerciales ni se presupone una licencia abierta sobre ellos. Un encaje de pestañas impresas podría estudiarse para tapas, pero no se elige todavía como único apriete del módulo de rueda.

Los apoyos y R/D mantienen la localización; el mando nuevo aprieta y retiene. Debe poder reconocerse el cierre completo, conservarse el apriete con las cargas y ciclos definidos para el conjunto, impedir accionamiento accidental y permitir servicio sin piezas sueltas. Comparar fuerza y accesibilidad manuales, holgura al reinstalar, desgaste, suciedad y barridos completos. Son criterios propuestos, aún sin resultados físicos. Recalcular la salida con retenedores, vástagos o estribos cautivos: los 6 mm DEMO de la placa anterior no prueban la salida de esa variante.

En la variante con pomo, la tuerca o contrapieza debe quedar retenida para que no haga falta sujetarla con otra herramienta. Los ejes actuales distan 20 mm: habrá que comprobar espacio de dedos y giro, no solo ausencia de choque entre cabezas. La referencia con tornillos tampoco está validada físicamente; hoy se comparan arquitecturas y geometría, no equivalencia demostrada de resistencia.

Abrir estos cierres solo separa cartucho y núcleo. La mordaza de lámina, los topes de contención y el retén del pivote permanecen independientes hasta una descarga controlada en banco.

## Pista de suministro para la lámina, sin selección ni compra

La investigación paralela encontró oferta minorista de [1.4310 / AISI301, laminado en frío, 2H](https://metallstore24.de/federstahl-blech-500x100mm), en hoja de 500×100 mm por unidad, y [1.1274 / C100S+QT](https://metallstore24.de/kohlenstoffstahl-bleche-25x300mm), en tiras de 25×300 mm por paquete de diez. El distribuidor ofrece [certificado EN10204 3.1](https://metallstore24.de/en/factory-certificate) adicional. No se ha visto un certificado de lote real ni se han confirmado todos los espesores en existencias. Esta pista permite evaluar suministro pequeño trazable; no elige material o sección, ni acredita la lámina después de fabricar sus bordes y montarla.

## Instrucciones posteriores del propietario (25-10-2026)

Toda apertura, generación y comprobación con FreeCAD debe hacerse **headless, sin interfaz gráfica**. Queda sustituida la receta gráfica para el trabajo futuro. El propietario también autorizó omitir el cerrojo y hacer pruebas en esta sesión; se mantienen casos focales y límites de recursos. Esta indicación no constituye un resultado de pruebas nuevas.

Nota para integrar: este archivo de coordinación ya existe sin seguimiento en el checkout compartido y su cuerpo principal coincide con el incluido en 710510e. Conservar esta actualización posterior al integrar el parche por contenido; no duplicar ni perder la instrucción headless.
