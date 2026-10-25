# 08 — Refutaciones, decisiones y cierre de la planificación

**25 de octubre de 2026.** Registro de la revisión del proyecto de chasis propio para el X20 Pro. Se trabajó con tres revisiones especializadas en paralelo —electrónica y pruebas; CAD y fabricación; mecánica e integración— y una síntesis coordinada. La revisión documental se ha cerrado provisionalmente después de **cuatro rondas**, sin nuevas objeciones materiales en la última.

Este resultado permite avanzar con inventario, medición y CAD preliminar. No significa que el futuro robot esté validado, que todas las piezas sean reutilizables o que una evidencia posterior no pueda cambiar una decisión.

## 1. Qué se consideró una refutación útil

Una objeción debía identificar una premisa falsa, una interfaz omitida, un gasto innecesario, una prueba imposible de ejecutar con los controles disponibles o una condición de aceptación insuficiente. Cada objeción material debía producir un cambio concreto o una medida/prueba que la resolviera.

Se distinguió entre lo que limita **inventariar**, **fabricar** y **usar**. No conocer aún el diámetro del pasador no impide organizar las fotos o dibujar un volumen preliminar. Sí impide aprobar su alojamiento final. Que el robot esté abierto no justifica alimentarlo con motores y placas sin sujeción.

El criterio de cierre fue una nueva revisión sin cambios esenciales, con cada incertidumbre restante asignada a una medida, prueba o decisión. Ningún número de vueltas argumentales puede sustituir esas comprobaciones físicas.

## 2. Rondas realmente realizadas

| Ronda | Material revisado | Resultado | Cambios incorporados |
|---|---|---|---|
| **1. Brainstorming y objeciones independientes** | Objetivo del propietario, fuentes técnicas y alternativas de herramientas/fabricación | Se descartaron una reconstrucción electrónica completa como requisito inicial, un catálogo excesivo de software y el aumento indiscriminado de material | Flujo mínimo; conservar conjuntos aprovechables; geometría funcional; piezas y accesos separables; herramientas opcionales justificadas por necesidad |
| **2. Crítica de la propuesta V0 integrada** | Primer plan común de chasis, suspensión y ensayos | Aparecieron errores que sí podían arruinar el montaje aunque cada pieza pareciera correcta por separado | Verificación del bastidor completo; procesos de fabricación comparables; masa/apoyos; pivotes y fuerza-recorrido; comandos acoplados; observación térmica temprana; aislamiento y uniones conductoras |
| **3. Revisión V1 con fotografías y alternativa OOMWOO** | 18 fotos únicas, plan V1, auditoría de CAD real | La arquitectura seguía siendo adecuada; había que añadir una decisión explícita sobre el origen del CAD y actualizar el estado de identificación de la unidad | Stock OOMWOO como candidato condicionado a edición y superposición; experimento separado; módulos y conexiones observados; funcionamiento aún pendiente |
| **4. Cierre dirigido sobre V2 y capítulos 09/10** | Plan actualizado, comparación OOMWOO e inventario fotográfico | **Los tres revisores no encontraron nuevas objeciones materiales** | Sin cambios esenciales. Se cierran búsquedas generales y se asigna el siguiente avance a medidas, comparación geométrica y piloto |

La revisión de ronda 4 fue dirigida a las correcciones nuevas y a su coherencia con lo ya resuelto. No repitió artificialmente toda la investigación ni declaró resueltos datos físicos que siguen desconocidos.

## 3. Objeciones decisivas y cómo quedó el plan

| Propuesta o supuesto refutado | Motivo | Decisión resultante |
|---|---|---|
| «Más espesor o más metal siempre será más resistente» | Aumenta masa; puede desplazar cargas, crear concentraciones de esfuerzo y afectar apoyos, radio o aislamiento | Diseñar caminos de carga y uniones; pesar y verificar el conjunto; metal localizado cuando se justifique |
| «Basta medir un agujero y comprobar que entra el pasador» | Dos apoyos pueden no ser coaxiales, pinzarse tras apretar o perder alineación al unir el bastidor | Controlar ajuste local y posiciones relativas en el montaje completo bajo la condición pertinente |
| «El muelle mayor resolverá la suspensión» | Longitud no determina fuerza; cambia la palanca durante el recorrido y el rozamiento puede ocultar el comportamiento real | Caracterizar el candidato y comprobar fuerza frente a desplazamiento de rueda, ida/retorno, topes y detector |
| «Un motor que funciona implica un módulo reutilizable» | Puede haber daño en reductora, cojinete, carcasa o apoyo óptico | Separar integridad mecánica y funcionamiento eléctrico; revisar reconstrucciones de precisión antes de comprometer gasto grande |
| «Hacemos una prueba separada de cada motor desde la app» | No se ha identificado un modo de servicio que lo permita; una orden puede accionar varios conjuntos | Tabla de comandos realmente disponibles y módulos implicados; preparar el montaje completo necesario para cada acción |
| «Sin error en la app y sin calentarse al tacto, la prueba es válida» | No acredita temperatura admisible, aislamiento ni durabilidad | Observación desde las primeras cargas; medición y límites pertinentes cuando hagan falta; no inventar temperaturas universales |
| «Conservar electrónica permite cambiar libremente la distribución» | Rodadura, sensores, óptica, limpieza y estación dependen de relaciones físicas que el firmware puede presuponer | Mantener o comprobar esas interfaces; no exigir firmware nuevo salvo obstáculo concreto |
| «WIFI_LED localiza la antena; CamSub demuestra una cámara RGB» | El texto de una placa no acredita todas esas funciones | Registrar la lectura literal y mantener radio, funciones y pinouts pendientes |
| «Un STEP de robot sin colisiones es un diseño funcional» | El experimento OOMWOO documenta errores de orientación, acceso a batería y recorrido de aire pese a sus comprobaciones | Separar stock/experimento y comprobar funciones, movimiento y mantenimiento además de encaje |
| «La base OOMWOO debe servir, o debe descartarse por ser otro modelo» | Ambas conclusiones carecen de superposición dimensional con nuestra unidad | Mantenerla como candidata; elegirla sólo si conserva suficientes interfaces y ahorra trabajo real |
| «Fabricar toda la carcasa será la forma más rápida de aprender» | Una incompatibilidad local puede obligar a desechar una impresión grande | Volúmenes simplificados, cupones y piloto antes del bastidor completo |
| «Debemos reparar el robot viejo para poder empezar el nuevo» | Contradice la decisión actual del propietario y puede depender de plástico deteriorado | Soporte o útil propio; la carcasa antigua sirve como referencia recuperable, no como requisito de uso |

Estas son conclusiones de planificación. Las fuentes técnicas que fundamentan sus principios están junto a cada tema en [07](07-plan-del-chasis-propio.md), y las fuentes específicas OOMWOO en [09](09-oomwoo-comparacion.md).

## 4. Resultado depurado

**Arquitectura provisional:** estructura nueva que conserve las referencias funcionales del Xiaomi, soportes de suspensión extraíbles, montaje accesible de batería/electrónica y conjuntos de limpieza, y perímetro de sensores/paragolpes con su movimiento necesario. Aprovechar OOMWOO de forma selectiva. Su base completa permanece abierta a comparación.

**Herramientas iniciales:** documentación y Git; FreeCAD como fuente paramétrica principal; Python integrado cuando ahorre operaciones; un laminador bajo el proceso de fabricación real. KiCad, WireViz, análisis de señales, mallas, fotogrametría y simulación entran sólo si resuelven una cuestión concreta. No se ha instalado software por hacer esta planificación.

**Unidad de reutilización:** conjunto funcional comprobable, no sólo placa o motor desnudos. Esto reduce interfaces de precisión que habría que reproducir; no obliga a reutilizar una carcasa dañada.

**Primer gasto de fabricación propuesto:** cupón o piloto pequeño de una interfaz definida, tras cotizar el proceso. No se ha aprobado un material universal, comprado una impresora ni prometido un precio de chasis completo.

## 5. Lo que sigue abierto y qué lo cerrará

| Dato pendiente | Evidencia que lo resolverá | Decisión afectada |
|---|---|---|
| Revisiones y parejas de conectores que deban separarse | Lectura dirigida y trazado físico | Traslado y reconexión de esos conjuntos |
| Estado mecánico/eléctrico de módulos | Inspección y prueba apta según montaje | Qué se reutiliza completo y qué se reconstruye |
| Cotas Xiaomi y origen geométrico común | Medición directa con condición documentada | Interfaces de fabricación y comparación de bases |
| Ensamblaje stock OOMWOO utilizable | Apertura/exportación de revisión identificada y comprobación de unidades | Cuánto CAD se reutiliza realmente |
| Compatibilidad de la base candidata | Superposición de volúmenes, barridos, accesos y estación | Adaptación localizada frente a cuerpo propio |
| Muelle y apoyo de rueda | Datos de trabajo admisible y prueba fuerza-recorrido | Aprobación del piloto de suspensión |
| Fabricación, masa y coste | Proceso real, cotización, piezas medidas | Selección de material, divisiones y gasto por iteración |
| Navegación, limpieza, estación, temperatura y mantenimiento | Ensayos proporcionados del prototipo sujeto y protegido | Uso del robot y aceptación de revisiones |

Se reabrirá una decisión cuando una medida, avería o prueba la contradiga. Se revisará la parte afectada; no se reiniciará por sistema todo el proyecto.

## 6. Límite del cierre

**El plan ha convergido documentalmente; el diseño físico aún tiene que ganarse su validación.** El resultado de las cuatro rondas es una forma de trabajar con menos supuestos ocultos y menos gasto prematuro. La resistencia y la facilidad de reparar se demostrarán mediante piezas fabricadas, medidas, usadas y desmontadas, con revisiones trazables.


## Revisión adicional — base nueva y CAD ejecutado, 25-10-2026

El propietario amplió el objetivo a robot abierto y decidió comenzar por sustituir la base. Las cuatro rondas anteriores se conservan como historial; no congelan un alcance que el propietario ha cambiado. Se asignaron tres frentes: estructura/reconstrucción, geometría funcional y electrónica/control. Los resultados se integran en 11–13.

| Objeción nueva | Cambio o resolución | Límite restante |
|---|---|---|
| Los fragmentos ya no existen | Diseñar desde caras, agujeros, ejes y contrapartes supervivientes | Algunas posiciones globales pueden requerir referencia adicional exacta |
| Una base monolítica puede volver a invalidarse por un pequeño anclaje | Núcleo resistente separado de cartuchos, apoyos y tapas | Partición, coste y rigidez con uniones por comprobar |
| Dos apoyos fijos no reparan el gancho o alojamiento móvil roto | Interfaz móvil explícita en IF01/IF03 y LimitesCartucho | Inspección y medición M41–M44 |
| Un CAD atractivo podría inventar un interior preciso | No hay cajas ficticias de módulos; solo metadatos pendientes, envolvente publicada y DEMO separado | Implantación real pendiente de medidas |
| Una macro no demuestra que exista un archivo editable | Se ejecutó FreeCAD 1.1.4, guardó/reabrió el FCStd y probó cambio paramétrico | Solo validación de cadena CAD |
| La captura podía aparentar posición de montaje | Se detectó y corrigió ruta nativa .Placement.Base.x; DEMO situado fuera y comprobado | No asignar esa posición al robot |
| Conservar firmware se confundía con robot abierto final | Etapas A–D; bandeja de electrónica reemplazable y dependencias cerradas inventariadas | No hay driver Pro listo ni root soportado demostrado |

La revisión independiente del código y las interfaces no encontró un bloqueo mecánico adicional para entregar v0.1 como estudio, y rechazó añadir rueda, muelle, retenes o sensores ficticios para completar su aspecto. El criterio de avance es aportar medidas útiles; repetir objeciones generales sin datos nuevos no sustituye ese paso.
