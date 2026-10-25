# 09 — OOMWOO como base para el Xiaomi X20 Pro

Consulta: 25 de octubre de 2026. Encargo: conservar electrónica, firmware, batería y módulos útiles del Xiaomi, construir una carcasa resistente y reparable, y comprobar si partir del cuerpo OOMWOO ahorra trabajo. Investigación de fuentes oficiales y lectura de archivos públicos; no se ha modificado el ordenador del usuario ni instalado CAD.

## Dictamen provisional

**Sí merece la pena aprovechar OOMWOO como biblioteca y referencia de arquitectura. Todavía no hay evidencia suficiente para elegir su chasis completo como donante.** Mi opción inicial sería diseñar el cuerpo nuevo alrededor de las interfaces Xiaomi y reutilizar del CAD OOMWOO solamente los elementos que sobrevivan a una comparación dimensional. Es una conclusión de ingeniería, no una prueba de incompatibilidad: faltan cotas del Xiaomi y un ensamblaje stock importable y comprobado.

La diferencia importa: adaptar un soporte OOMWOO a nuestro motor puede ahorrar modelado; meter todos los módulos Xiaomi dentro de otra distribución puede obligar a rehacer el cuerpo entero. El firmware conservado y la estación Xiaomi hacen que la posición funcional de ruedas, sensores, contactos, mopas y conductos sea una restricción prioritaria.

## 1. Qué está realmente publicado

El sitio oficial sigue describiendo un proyecto en desarrollo, con simulación disponible y hardware en prototipado. El README principal y las instrucciones de construcción dicen que aún no se puede construir el conjunto completo siguiendo una guía validada. Hay trabajo físico real en subconjuntos, especialmente el cepillo principal; los vídeos de navegación y acoplamiento etiquetados como simulación no demuestran un robot físico completo. [1–3]

El repositorio CAD sí contiene archivos reales, y distingue expresamente dos líneas: `designs/one/stock` es el diseño OOMWOO One; `designs/one/agentic` conserva experimentos, no el diseño de producto. [4–5]

### Inventario comprobado del árbol público

Árbol consultado: `ea4e357b5755380ad44be9e50dc97f33fbb05348`, respuesta de GitHub con `truncated: false`. Es un identificador de árbol, no lo presento como commit. El historial de la ruta stock devuelve el commit de reorganización `b859d3e1a7f242912841ce12d2d09e5a155761fa`, de 9 de octubre de 2026. [6]

| Archivo o grupo | Tamaño del archivo | Qué permite afirmar |
|---|---:|---|
| `stock/Assembly_2.f3z` | 41.367.262 bytes | Hay un ensamblaje nativo Fusion con referencias incluidas. |
| `stock/Top_Assembly_081426a.f3z` | 3.675.255 bytes | Hay otro snapshot de ensamblaje, anterior y más pequeño. |
| `stock/C01 Top Assembly.f3d` | 6.087.750 bytes | Hay un archivo nativo de conjunto superior. |
| `stock/C01_2_base_snapshot.f3d` | 1.580.341 bytes | Hay un archivo nativo de base. |
| `stock/OOM-B03_Main_Assembly.f3d` | 29.548.693 bytes | Hay CAD del cepillo principal. |
| `stock/OOM-M02-Assembly.f3d` | 15.893.548 bytes | Hay CAD de otro subconjunto de cepillo. |
| `stock/STEP/03-01 Motor_Gearbox.step` | 9.082.971 bytes | Exportación STEP de reductora. |
| `stock/STEP/03-02 Red_Brush_Gearbox_step.step` | 2.953.386 bytes | Segunda exportación STEP de reductora. |
| `agentic/july-2026/device_full.step` | 16.375.631 bytes | Robot experimental completo, con errores conocidos; véase abajo. |

**En el árbol inspeccionado, las dos reductoras son los únicos STEP de `stock/STEP`. No aparece un STEP del chasis stock completo ni un juego STL/3MF para imprimirlo.** Esto no significa que no exista CAD del chasis: existe en Fusion. Significa que el salto a nuestro flujo FreeCAD necesita una exportación neutral del conjunto correcto o reconstrucción seleccionada; cambiar la extensión de un F3D no resuelve esa conversión. [6–7]

La biblioteca `lib/` contiene numerosos STEP de piezas compradas o reconstruidas: ruedas y batería Roborock, caster iRobot, sensores, aspiradores, mopas, filtros, cepillos, módulos Raspberry Pi y varios LiDAR. Un archivo llamado `xiaomi_lds02rr.step` no demuestra que corresponda al LiDAR concreto del X20 Pro. [6]

## 2. El STEP completo pertenece al experimento

El autor identifica `agentic/july-2026/device_full.step` como un experimento de generación de CAD con IA, sin revisión manual, **no como OOMWOO One**. Describe errores de orientación de caster y cepillo lateral, una puerta por la que no sale la batería, una batería provisional, una abertura de aspiración sin recorrido de aire funcional y ausencia de mopas. El documento informa que pasó sus comprobaciones numéricas de colisiones. [8]

Por tanto, el hecho de que ese archivo abra, tenga aspecto de robot y no presente intersecciones según sus comprobaciones no demuestra ensamblaje, aspiración, mantenimiento ni compatibilidad con una base. **No lo usaría para encargar la impresión del cuerpo.** Puede servir como ejemplo de por qué una revisión de funciones es indispensable.

El diámetro de envolvente de 355 mm que menciona ese README pertenece al experimento. No lo he tratado como dimensión del stock, ni como cota medida del Xiaomi. [8]

## 3. Qué inspeccioné dentro del Fusion stock

Descargué el contenedor `Assembly_2.f3z` y leí su manifiesto y descripción, además de extraer las miniaturas PNG incluidas. No abrí sus sólidos en Fusion ni validé restricciones o interferencias del ensamblaje.

Su `DesignDescription.json` identifica un snapshot de 7 de septiembre de 2026 e incluye referencias a `C01_2`, las dos ruedas W01, batería E01, caster iRobot, sensores de desnivel, cepillo principal B03 y mopas P01/P02/P03. La miniatura muestra una base con varios de estos elementos. El snapshot pequeño de agosto contiene menos subconjuntos. Esta inspección confirma que **hay ensamblajes mecánicos auténticos**, pero no ofrece una lista certificada de componentes funcionales, posiciones, medidas o piezas listas para imprimir. [9]

Además, el blog mecánico explica que el diseño de mopas Roborock se descartó por complejidad y se propuso emplear motores con reductora y correas; relata varias iteraciones físicas del cepillo principal y la necesidad de adaptar piezas a impresión. La evolución del proyecto obliga a comprobar qué snapshot incorpora cada decisión: no conviene mezclar automáticamente el ensamblaje de septiembre con todos los objetivos de documentos posteriores. [10]

### Geometría neutral que sí pude medir

Importé dos STEP de la biblioteca con OpenCascade ya disponible, sin instalar software. Los archivos declaran milímetros. La geometría importada pasa la comprobación BRep y se obtienen tres sólidos para W01 y uno para E01. El lector advierte sobre el formato de un campo de autorización de la cabecera; esto no equivale a una validación exhaustiva del archivo.

| Modelo de biblioteca | Envolvente de toda la geometría, en los ejes del archivo |
|---|---:|
| `OOM-W01-drive-wheel-assembly.stp` | aproximadamente 72,705 × 111,211 × 60,368 mm |
| `OOM-E01-battery.stp` | aproximadamente 44,400 × 142,839 × 43,500 mm |

Son cálculos propios sobre los modelos identificados en [11]. **No son diámetro de rueda, cotas de montaje, distancia entre ruedas ni dimensiones verificadas de nuestro robot.** No justifican todavía comprar o imprimir adaptadores. No he obtenido una cota verificable del chasis stock completo o de su separación de ruedas. [11]

## 4. Qué pretende montar OOMWOO y qué exige conservar Xiaomi

El SPEC de OOMWOO se presenta como documento de trabajo. Propone ruedas Roborock S5 Max, batería Roborock, caster iRobot, sensores de varias procedencias y Raspberry Pi CM4/CM5. Su propia placa de entradas/salidas tiene forma y dimensiones pendientes de decidir según el CAD. Esto ofrece libertad al diseñador OOMWOO que no tenemos si conservamos la placa Xiaomi ya fabricada. [12]

La revisión de las fotografías de esta unidad muestra una placa principal Xiaomi ancha y curvada, un conjunto frontal/lateral unido por un flex largo y dos motorreductores de mopas independientes con carcasa propia. No hay escala en las fotos. Estos hechos sirven para definir envolventes a medir, no para declarar que caben o que no caben.

La compatibilidad necesaria tiene varias capas:

| Interfaz conservada | Qué debe comprobarse en cualquier cuerpo donante |
|---|---|
| Ruedas y suspensión | Radio efectivo, posición de contacto, distancia entre ruedas, pivote, recorrido y reacción del muelle; acceso a pasadores y extracción. |
| Placa, cableado y batería | Envolventes, fijaciones, conectores, holguras de flexión, salida de cables y acceso sin desmontar módulos ajenos. |
| Sensores y paragolpes | Posición y orientación de ventanas, campo libre, desplazamiento del paragolpes y recorrido de flex. |
| Aspiración | Continuidad y estanqueidad del recorrido desde cepillo a depósito/filtro/turbina; mantenimiento de tapas y juntas. |
| Mopas | Centros, altura, movimiento y espacio durante elevación; relación con suelo y bandeja de lavado. |
| Base Xiaomi | Aproximación física, rampas, contactos, guía óptica y acoplamientos de vaciado/lavado que se identifiquen en nuestra unidad. |

Esta tabla es criterio de diseño propio. Un motor compatible eléctricamente no garantiza ninguna de esas relaciones. Conservar componentes completos y sus carcasas sanas reduce el número de superficies que hay que reproducir con precisión; no obliga a conservar el cuerpo roto.

## 5. Estación: referencia de estudio, no interfaz Xiaomi validada

El repositorio guarda `docs/dock_teardown_x20.pdf`, un desmontaje ilustrado de una estación con electrónica, calentadores, bombas y guiado óptico. Su existencia demuestra que el proyecto estudió una estación comercial; no prueba que el cuerpo OOMWOO acople a la estación concreta del X20 Pro. El PDF no aporta una identificación de esa equivalencia ni un plano de interfaz homologado. No traslado sus tensiones o etiquetas de componentes al equipo del usuario. [13]

El RFC oficial de docking dice que el robot físico todavía no está construido y trabaja en simulación. La geometría de la base genérica está por decidir; contempla servicios futuros cuando estén soportados. El SPEC también deja decisiones de geometría y servicios abiertas. **No encontré una estación OOMWOO terminada cuya compatibilidad de carga, vaciado y lavado con Xiaomi pueda darse por supuesta.** [12,14]

Como vamos a conservar la estación Xiaomi, sus interfaces deben medirse y convertirse en requisitos del cuerpo nuevo. No hace falta sustituirla por una estación OOMWOO para aprovechar ideas de su chasis.

## 6. Comparación de las tres rutas

Evaluación propia; esfuerzo relativo, no presupuesto ni estimación de horas.

| Ruta | Qué ahorra | Trabajo/riesgo que introduce | Decisión hoy |
|---|---|---|---|
| **A. Cuerpo stock OOMWOO entero con módulos Xiaomi** | Una estructura y distribución iniciales, si el CAD correcto se puede editar. | Conseguir exportación actual; separar referencias antiguas; acomodar placa, ruedas, sensores, conductos y mopas distintos; garantizar la base Xiaomi; rehacer todas las funciones afectadas. | Candidato para comparar; no es una base elegida ni validada para fabricar. |
| **B. Subconjuntos, patrones y biblioteca OOMWOO** | Detalles existentes, organización modular, ejemplos de soportes y orientación de fabricación; referencias de componentes si coinciden. | Comprobar pieza real, versión, licencia, cargas y fabricación; reconstruir parámetros necesarios. | Utilidad clara, selectiva. No sustituir motorreductores Xiaomi sanos por otros más complejos solo porque haya CAD. |
| **C. Cuerpo propio alrededor de interfaces Xiaomi** | Evita adaptar nuestro robot a las restricciones de una segunda plataforma; conserva funciones originales con menos cambios geométricos deliberados. | Hay que levantar medidas y diseñar estructura, accesos, uniones y fabricación. | Base provisional preferida, incorporando B cuando ahorre trabajo demostrado. |

La ruta A no es imposible. La cuestión pendiente es si su estructura reutilizable supera el trabajo que cuestan las adaptaciones. Un mayor porcentaje de piezas visualmente reutilizadas tampoco asegura menor coste si obliga a muchas pruebas e impresiones completas.

### Qué haría cambiar la conclusión

1. Obtener el ensamblaje **stock actual** en STEP, con identificación de versión y referencias de componentes; o una exportación verificable del Fusion disponible.
2. Medir las envolventes e interfaces críticas Xiaomi y colocar ambas distribuciones sobre un sistema común de referencia.
3. Comprobar que el cuerpo stock admite ruedas, placa, sensor frontal, aspiración, mopas y estación Xiaomi mediante adaptadores localizados, sin desplazar interfaces que el firmware presupone.
4. Confirmar accesibilidad y recorrido: no basta ausencia de colisión en posición nominal. Debe poder extraerse cada módulo previsto, moverse la suspensión y pasar cables sin pinzamientos.
5. Verificar que el diseño se puede fabricar con el proceso elegido y que existe evidencia física relevante o un prototipo pequeño que resuelva la principal incertidumbre.

Si esa superposición da pocas modificaciones localizadas, elegir A tendría sentido. Si exige mover casi todo y reconstruir conductos y perímetro, C+B será una base más directa. La comparación debe hacerse con envolventes simples y secciones antes de modelar todos los tornillos o imprimir toda la carcasa.

## 7. Licencias y límites del resultado

El repositorio CAD publica `LICENSE` Apache-2.0 y el experimento se remite expresamente a esa licencia. El sitio y README principal todavía describen una licencia de hardware por decidir. Registro ambas declaraciones, sin inventar que la documentación ya está armonizada. Al conservar piezas de CAD conviene guardar procedencia y versión; el presente análisis no resuelve derechos de terceros de todos los modelos de biblioteca. [1,4,8,15]

No se ha demostrado un encaje dimensional, resistencia del chasis, durabilidad de impresiones ni funcionamiento del conjunto trasplantado. Tampoco se ha demostrado incompatibilidad definitiva. El resultado útil de esta auditoría es identificar el CAD correcto, descartar el STEP experimental como atajo listo para imprimir y definir una comparación que pueda decidir objetivamente cuánto OOMWOO conviene reutilizar.

## Fuentes primarias y evidencias

1. Sitio oficial, estado y licencia declarada: https://oomwoo.com/
2. README del proyecto: https://github.com/makerspet/oomwoo
3. Estado de instrucciones: https://github.com/makerspet/oomwoo/blob/main/docs/BUILD_INSTRUCTIONS.md
4. Repositorio CAD: https://github.com/makerspet/oomwoo-cad
5. Distinción stock/agentic: https://github.com/makerspet/oomwoo-cad/blob/main/designs/README.md
6. Inventario íntegro vía API pública: https://api.github.com/repos/makerspet/oomwoo-cad/git/trees/main?recursive=1 ; historial stock: https://api.github.com/repos/makerspet/oomwoo-cad/commits?path=designs%2Fone%2Fstock&per_page=3
7. Directorio y README stock: https://github.com/makerspet/oomwoo-cad/tree/main/designs/one/stock ; https://github.com/makerspet/oomwoo-cad/blob/main/designs/one/stock/README.md
8. Limitaciones del experimento, leídas completas: https://github.com/makerspet/oomwoo-cad/blob/main/designs/one/agentic/july-2026/README.md
9. Ensamblaje nativo inspeccionado como archivo: https://github.com/makerspet/oomwoo-cad/blob/main/designs/one/stock/Assembly_2.f3z
10. Evolución mecánica y prototipos: https://makerspet.com/blog/oomwoo-3d-design-how-its-made/
11. STEP medidos: https://github.com/makerspet/oomwoo-cad/blob/main/lib/roborock/OOM-W01-drive-wheel-assembly.stp ; https://github.com/makerspet/oomwoo-cad/blob/main/lib/roborock/OOM-E01-battery.stp
12. Especificaciones de trabajo: https://github.com/makerspet/oomwoo-cad/blob/main/docs/SPEC.md
13. Referencia de desmontaje de estación: https://github.com/makerspet/oomwoo-cad/blob/main/docs/dock_teardown_x20.pdf
14. RFC docking: https://github.com/makerspet/oomwoo/blob/main/contributions/dock-cycle/README.md
15. Licencia CAD: https://github.com/makerspet/oomwoo-cad/blob/main/LICENSE

Se conservaron copias de trabajo del árbol, metadatos y medidas para la auditoría. Las miniaturas extraídas son evidencias de archivo, no planos dimensionales ni capturas de una validación de ensamblaje. El repositorio de investigación enlaza los CAD a su origen, sin redistribuir las fotografías personales.

Plan de ejecución: [07 — Chasis propio](07-plan-del-chasis-propio.md). Evidencia de esta unidad: [10 — Inventario fotográfico](10-inventario-fotografico.md).
