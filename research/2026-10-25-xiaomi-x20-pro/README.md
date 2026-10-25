# Xiaomi X20 Pro: reparar, reforzar y conocer su mecánica

**Dossier de investigación — 25 de octubre de 2026.** Equipo de referencia: **Xiaomi Robot Vacuum X20 Pro, D102GL**, con estación europea **D102-JZEU**. Caso aplicado al proyecto [Fábrica Doméstica Autónoma Abierta](https://github.com/Valdi320/Valdo).

## Resultado principal

**Es viable rediseñar progresivamente la estructura que rodea a la electrónica original para hacerla más reparable. El primer proyecto útil es la suspensión de las ruedas; un chasis completo es una fase posterior.** La información disponible permite preparar el trabajo, comparar repuestos y definir qué medir. Todavía no permite fabricar una pieza compatible sin medir el soporte real.

La secuencia recomendada es **recuperar el uso → desarrollar un soporte pequeño y sustituible fuera del robot → ampliar sólo lo que demuestre una ventaja**. Así se evita que el aparato permanezca desmontado mientras se diseña. No hace falta iniciar ingeniería inversa de software para estas tres rutas: se conservan electrónica, firmware, motores, batería, sensores y estación, junto con sus interfaces funcionales.

El resultado es investigación documentada y una propuesta de trabajo. **No se ha fabricado ni ensayado un refuerzo, no hay CAD dimensional validado y no se conoce aún la ubicación exacta de la fractura.** Esos límites determinan qué puede comprarse o diseñarse con confianza.

## Qué se ha averiguado

- Hay recambios catalogados expresamente para Pro: módulos motrices, pasadores, muelles, placa, motores de mopas, aspiración y conjunto trasero de contactos e IR. Las fichas y precios están en [repuestos](02-repuestos-y-reparacion.md) y en el [CSV](repuestos.csv).
- El catálogo comercial consultado reúne **99 entradas**, incluidas estación y consumibles. No es un despiece OEM ni significa que se hayan identificado todos los componentes internos.
- **Pro y Max comparten determinadas piezas.** La compatibilidad de las ruedas no demuestra la del chasis. La carcasa completa Max encontrada a 19,21 € sigue sin estar verificada para Pro.
- Los vídeos de M30 y otros modelos relacionados ayudan a entender el acceso. No se ha localizado un manual oficial de servicio del D102GL con su mapa de tornillos. Las observaciones de vídeos y sus límites están en [arquitectura y desmontaje](01-arquitectura-y-desmontaje.md).
- No se encontró un CAD completo del X20 Pro ni una reparación imprimible del apoyo de rueda con encaje y funcionamiento comprobados. Es un resultado de búsqueda, no una afirmación de inexistencia.
- [OOMWOO](https://oomwoo.com/) y su [repositorio CAD](https://github.com/makerspet/oomwoo-cad) aportan piezas editables y un procedimiento de diseño. No constituyen un kit terminado ni un reemplazo dimensional del Xiaomi.

Las referencias primarias y comerciales que sostienen estas conclusiones se localizan junto a cada afirmación en los capítulos. El [registro de fuentes y límites](05-fuentes-y-limites.md) reúne la trazabilidad.

## La decisión que evita gastar en la pieza equivocada

Una «agarradera rota» puede cumplir funciones distintas:

| Daño real | Intervención que se puede estudiar | Lo que no resuelve el problema por sí solo |
|---|---|---|
| Falta el muelle, con ambos anclajes sanos | Muelle correcto y comprobación de recorrido/retorno | Un muelle parecido cuya fuerza sea desconocida |
| Gancho del muelle fracturado | Anclaje reemplazable, situado como el original y apoyado en material sano | Poner más tensión al muelle |
| Alojamiento del pasador en la carcasa móvil de rueda | Reparar esa carcasa o sustituir el módulo si incluye la zona dañada | Cambiar únicamente el pasador |
| Apoyo del pasador en el chasis fijo | Reconstruir o sustituir ese apoyo, con fijación y alineación verificadas | Comprar un módulo de rueda completo |

**Sin ver ambas caras del daño no se puede escoger entre esas intervenciones.** El primer objetivo de una apertura preparada es resolver esa identificación y tomar las medidas mínimas, no desmontar todos los módulos.

## Tres rutas

| | A. Más barata y práctica | B. Más llevadera a medio plazo | C. Control dimensional completo |
|---|---|---|---|
| Objetivo | Recuperar funcionamiento con una reparación localizada o el recambio exacto | Hacer que el apoyo averiado y el módulo se mantengan con pocas operaciones | Disponer de un chasis modular propio y de todas sus interfaces documentadas |
| Trabajo | Identificar daño, conservar piezas sanas, sustituir muelle o módulo cuando proceda; estudiar puente/anclaje si el daño está en chasis | Modelar portapivote y anclaje reemplazables; prever pasador, conector y tornillos accesibles | Medir conjuntos, crear ensamblaje paramétrico y fabricar una estructura por módulos |
| Qué se reutiliza | Prácticamente todo | Motores, reductoras, ruedas, electrónica, batería, sensores, hidráulica y sellos existentes | Esos mismos conjuntos; se rediseñan sus soportes y la estructura según necesidad |
| Coste conocido | Precios de recambios disponibles; refuerzo aún sin presupuesto | Herrajes, pruebas de ajuste y fabricación a cotizar tras definir la pieza | No hay presupuesto responsable sin volumen, piezas, iteraciones y método de fabricación |
| Cómo reducir la parada | Preparar repuestos y herramientas antes de la intervención | Diseñar en banco con la pieza dañada o repuesto mientras funciona el robot reparado | Ensamblar y comprobar plantillas/estructura antes de transferir módulos |
| Límite | Puede resolver sólo la avería actual | Exige espacio sano de fijación y acceso; aún sin diseño validado | Mayor trabajo e incertidumbre; no ofrece independencia del firmware original |

### Ruta A: restaurar la función con el mínimo gasto total

Si sólo falta un muelle y los anclajes están bien, ese es el recambio lógico. Si el plástico roto pertenece al módulo móvil y no hay una reparación local convincente, el módulo completo proporciona una referencia económica y puede reducir las iteraciones. Si pertenece al chasis, habrá que reparar o reemplazar ese soporte; una rueda nueva no lo reconstruye.

Un refuerzo viable debe conservar el eje, el recorrido y el retorno de la rueda, y conducir la carga hacia material sano. Un collar puede contener una grieta sin descargar su raíz; un puente bien anclado puede crear otro camino de carga. La diferencia está explicada en los [esquemas conceptuales](assets/refuerzos-conceptuales.svg). No indican dónde taladrar el X20 Pro.

**Ceys curado durante 48 horas no equivale a un apoyo estructural comprobado.** La ficha oficial describe un adhesivo flexible y excluye algunos plásticos. El adhesivo no sustituye la comprobación de alineación, material y cargas repetidas. Véase el análisis de su ficha en el capítulo de repuestos.

### Ruta B: convertir la avería en una pieza pequeña y reemplazable

El proyecto recomendado es un **portapivote desmontable y un anclaje de muelle sustituible**, conservando pasador y muelle metálicos adecuados. Las superficies de asiento colocarían la pieza; las fijaciones accesibles la sujetarían. Una rotura futura debería obligar a cambiar ese soporte, sin sustituir el motor ni intervenir en módulos ajenos.

La mejora de acceso debe diseñarse junto al apoyo: espacio para extraer el pasador, desenganchar el muelle y alcanzar el conector. No se propone cortar ahora una trampilla a ciegas; antes hay que localizar nervios, sellos y cables. Conviene fabricar primero un cupón pequeño del alojamiento, y después el soporte.

Para un presupuesto limitado, encargar esas pruebas o usar un taller compartido puede evitar comprar una impresora antes de conocer la necesidad. No se ha obtenido una cotización de fabricación. Debe compararse el coste total de iteraciones y herrajes con el recambio exacto, además del tiempo sin uso.

### Ruta C: chasis modular propio con interfaces medidas

El objetivo sería un ensamblaje paramétrico con: núcleo que conserva referencias, soportes de rueda independientes, bandeja de electrónica, cuna de batería, accesos a aspiración y mopas y piezas exteriores reemplazables. Se mantiene la geometría funcional original y se verifica cada unión.

Se conservarían al principio neumáticos, engranajes, muelles, pasadores, juntas, turbina equilibrada, pack de batería cerrado, placas, óptica y contactos. No tiene utilidad económica imprimir una pieza sana sólo para afirmar que todo es imprimible. Los elementos que requieren ajuste o desgaste controlado pueden ser metálicos y comerciales.

«Controlar al milímetro» significa conocer qué dimensiones importan, medirlas, definir su ajuste y poder fabricar/reemplazar la pieza. No significa que cualquier impresión reproduzca el CAD sin error. Tampoco permite cambiar distancia entre ruedas, diámetro efectivo, sensores o acoplamiento y asumir que el firmware se adaptará. El control mecánico puede ser completo mientras el software siga siendo el original.

## Referencias económicas comprobadas

Precios observados el 25/10/2026 en PC:MediaStore, con IVA indicado por el vendedor y envío aparte. Son una referencia de comparación; no una compra ni un total de checkout validado.

| Elemento | Precio |
|---|---:|
| Módulo izquierdo, SKU 12585 | 29,62 € |
| Módulo derecho, SKU 13025 | 36,79 € |
| Muelle, SKU 37935 | 1,83 €; 1,80 €/ud. desde 2 |
| Dos pasadores, SKU 12584 | 2,03 € |
| Ambos módulos | 66,41 € |

Un muelle más el paquete de pasadores suma **3,86 € en piezas**, pero sólo es suficiente si alojamientos y anclajes están sanos. Dos módulos, dos muelles y el paquete de pasadores suman **72,04 €**. Con la tarifa publicada DHL a España de 0–5 kg, el segundo escenario sería **95,83 €**, condicionado al peso, destino, impuestos y servicio aceptados en checkout. Para pedidos de hasta 50 €, la tabla publica opciones de correo de menor coste; su elegibilidad no se ha comprobado. En [repuestos](02-repuestos-y-reparacion.md) están las URLs y la aritmética completa.

No se asigna un precio ficticio al rediseño completo. El coste se calculará como **piezas compradas + material o servicio de impresión + prototipos descartados + transporte**, registrando aparte horas de trabajo y de indisponibilidad. Una investigación gratuita puede evitar compras erróneas; no elimina el trabajo de medir, fabricar y comprobar.

## Qué no demuestra la investigación

No hay base suficiente para afirmar que esta rotura sea frecuente en toda la serie, que Xiaomi la haya diseñado para fallar o que un material concreto vaya a superar automáticamente al original. Hay casos individuales y una pieza dañada por identificar. Geometría, fabricación, montaje, golpes y uso son hipótesis que requieren observación.

Tampoco se ha confirmado un depósito interno de agua en el Pro ni un chasis Max intercambiable. El dossier evita transferir esas características por parecido de nombre. Las medidas y materiales desconocidos permanecen en blanco en la [plantilla de mediciones](mediciones.csv).

## Cómo utilizar este dossier

1. Leer la tabla de daños de esta página y comparar la pieza real.
2. Consultar [01 — Arquitectura y desmontaje](01-arquitectura-y-desmontaje.md) para ubicar módulos, interfaces y vídeos.
3. Consultar [02 — Repuestos y reparación](02-repuestos-y-reparacion.md) antes de comprar.
4. Usar [03 — Ingeniería física y CAD](03-ingenieria-fisica-y-cad.md) para diseñar y fabricar el apoyo.
5. Preparar la única sesión necesaria con [04 — Plan de trabajo y mediciones](04-plan-de-trabajo-y-mediciones.md), [mediciones.csv](mediciones.csv) y [registro-intervenciones.csv](registro-intervenciones.csv).
6. Revisar [05 — Fuentes y límites](05-fuentes-y-limites.md) cuando se quiera comprobar una afirmación o ampliar el proyecto.
7. Consultar [06 — Inventario ampliado del robot](06-inventario-ampliado-del-robot.md) para sensores, óptica, cepillos, LDS, piezas de carcasa y arneses. Las alternativas de catálogo no se cuentan como componentes instalados simultáneamente.

Hay también una versión continua para leer sin conexión: **[Dossier_Xiaomi_X20_Pro.html](Dossier_Xiaomi_X20_Pro.html)**. Las figuras propias son conceptuales; las imágenes de recambios y vídeos de terceros se enlazan desde su origen.

Este caso concreta la investigación de [metrología e ingeniería inversa del 13 de octubre](https://github.com/Valdi320/Valdo/blob/master/research/2026-10-13/05-ingenieria-inversa-metrologia.md). Los diseños nuevos deberán conservar sus archivos editables, parámetros medidos y registro de pruebas. El estado de licencias del repositorio se mantiene; publicar una propuesta no autoriza a redistribuir manuales, vídeos o CAD ajeno.
