# IA local, herramientas y modelos de datos

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 12. IA local y arquitectura de software: 16–24 GB como objetivo

**No requerimos que un único modelo tenga todos los conocimientos científicos en sus pesos.** La IA generalista debe saber planificar, consultar documentación, delegar, verificar y detenerse; los cálculos exigentes los resolverán instrumentos, simuladores y controladores especializados.

### Descomposición de funciones

1. **LLM local**: interpretar necesidades, leer manuales, planificar y explicar; cuantización/servicio de inferencia compatible con 16 GB cuando sea posible.
2. **Percepción y estimación del estado**: cámaras, LiDAR/3D, SLAM, objetos, humanos, superficies, fuerza y contacto.
3. **Políticas de manipulación VLA**: habilidades entrenadas/demostradas de alcance, agarre, cambio de herramienta, manipulación, con supervisión.
4. **Planificación de tareas y movimiento**: secuencias, colisiones, cinemática bimanual, obstáculos movibles, estabilidad y punto de apoyo.
5. **Herramientas de ingeniería**: FreeCAD, CadQuery, KiCad/SPICE, simulación multibody/FEA y materiales.
6. **Memoria local y RAG**: manuales, piezas, recetas, histórico de operaciones, fallos, marcas de verificación y versiones.
7. **Controladores críticos**: microcontroladores o lazos de tiempo real; límites de par/velocidad, sensores de seguridad, E-stop, protecciones de hardware.

### Modelos y precedente verificable

- [SmolVLA 450M](https://huggingface.co/blog/smolvla) es un ejemplo de modelo visión-lenguaje-acción compacto entrenable/ejecutable en equipamiento asequible para **tareas delimitadas**.
- [LeRobot](https://github.com/huggingface/lerobot) ofrece herramientas abiertas para integración de robots, teleoperación, datos y entrenamiento.
- [openpi](https://github.com/Physical-Intelligence/openpi) documenta configuraciones de inferencia con **más de 8 GB de GPU** y necesidades de ajuste fino muy superiores. Que el modelo pueda entrar en memoria no equivale a que domine reparaciones generalistas.
- Un LLM local puede orquestar múltiples herramientas; evaluar VRAM **pico**, KV cache, visión concurrente, latencia de percepción/control, energía y fiabilidad.

### Diseño para desconexión y privacidad

- La GPU central podría residir en casa (estación/servidor), mientras el robot lleva cómputo básico y control de seguridad local.
- Red local cifrada y autenticada; no se depende de Internet para seguridad, navegación básica, postura y recarga.
- No guardar vídeos de dormitorios/salas más tiempo del necesario; telemetría y modelos compartidos bajo permisos explícitos.
- Modelos y herramientas versionados con rollback; protección contra instrucciones maliciosas en manuales o documentos externos (*prompt injection*).
- No permitir que el LLM desactive límites de fuerza, enclavamientos o señales de parada.
- Priorizar operación secuencial de modelos o descargas parciales para no desbordar una GPU de 16 GB.

---

---

## 13. Herramientas y plataformas de código abierto (investigación complementaria)

Los proyectos existentes reducen la necesidad de inventar toda la infraestructura. **Evaluar mantenimiento, licencia, versión de ROS 2, capacidad real y requisitos GPU antes de adoptarlos**; esta tabla no es una afirmación de integración ya realizada.

| Área | Proyecto | Uso potencial |
|---|---|---|
| Middleware robótico | [ROS 2](https://www.ros.org/) | comunicaciones y componentes |
| Lazos y dispositivos | [ros2_control](https://control.ros.org/) | interfaz de actuadores y ciclo de control |
| Navegación y carga | [Nav2](https://docs.nav2.org/) | planificación, recuperación, docking |
| Tareas jerárquicas | [Nav2 Behavior Trees](https://docs.nav2.org/rolling/getting_started/navigation_concepts/behavior_trees/) | acciones secuenciales y condiciones |
| Docking autónomo | [opennav_docking](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) | aproximación y confirmación de carga |
| Manipulación | [MoveIt 2](https://moveit.picknik.ai/main/) | IK, colisiones y planes de brazo |
| Tareas multi-etapa | [MoveIt Task Constructor](https://moveit.picknik.ai/main/doc/concepts/moveit_task_constructor/moveit_task_constructor.html) | agarre, desmontaje, colocación |
| Física multibody | [Drake](https://github.com/RobotLocomotion/drake) | restricciones, dinámica, control |
| Mapa del terreno | [ANYbotics grid_map](https://github.com/ANYbotics/grid_map) | elevación, superficie y transitabilidad |
| Pose visual del dock | [AprilTag](https://github.com/AprilRobotics/apriltag) | marcadores y estimación de posición |
| Hardware robótico económico | [SO-101 en LeRobot](https://github.com/huggingface/lerobot/blob/main/docs/source/so101.mdx) | brazo imprimible, BOM, montaje |
| Entrenamiento de robot | [LeRobot](https://github.com/huggingface/lerobot) | demostraciones, políticas y datos |
| Modelo robótico compacto | [SmolVLA](https://huggingface.co/blog/smolvla) | visión y acción para tareas acotadas |
| VLA de investigación | [openpi](https://github.com/Physical-Intelligence/openpi) | comparar modelos y requisitos |
| Sensores de tacto | [Meta Digit Plexus](https://github.com/facebookresearch/digit-plexus) | integración modular de tacto |
| Tacto reemplazable | [AnySkin](https://any-skin.github.io/) | estimar contacto y agarre |
| CAD paramétrico | [FreeCAD](https://github.com/FreeCAD/FreeCAD) | modelo editable, planos y Python |
| CAD programático | [CadQuery](https://cadquery.readthedocs.io/) | piezas paramétricas a partir de scripts |
| Escaneo económico | [OpenScan](https://github.com/OpenScan-org) | fotogrametría y proyectos de hardware |
| Electrónica | [KiCad](https://www.kicad.org/) | esquemas y PCB |
| Simulación EM | [openEMS](https://docs.openems.de/en/stable/intro.html) | electromagnetismo avanzado cuando corresponda |
| Firmware/ejecutables | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | análisis y pseudocódigo |
| Microchips | [Degate](https://github.com/DegateCommunity/Degate) | análisis semiautomático de imágenes de IC |
| Señales eléctricas | [sigrok/PulseView](https://sigrok.org/wiki/PulseView) | protocolos y capturas |

**Punto nuevo importante:** en robótica hay una distinción entre aprender a manipular objetos conocidos y ejecutar una tarea compleja en un entorno nunca visto. Los modelos VLA son prometedores, pero la fiabilidad de un desmontaje delicado requerirá probablemente **teleoperación de enseñanza, pruebas, sensores táctiles, reglas duras y simulación**. Un modelo de 450 millones de parámetros y uno mucho mayor no deben compararse solo por «tokens por segundo».

---

---

## 15. Modelo de datos y contratos de confianza

El sistema debería guardar un **expediente verificable por objeto** con estos grupos de campos (estructura conceptual, no esquema API definitivo):

- **Identidad:** nombre interno, imágenes, modelo/marca si consta, geometría base, huellas.
- **Mediciones:** sensor, fecha, unidad, calibración, valor, incertidumbre y archivo bruto.
- **Hipótesis:** composición/materiales probables, geometrías ocultas, funciones, nivel de confianza y alternativas.
- **CAD y fabricación:** archivo paramétrico, material, tolerancias, orientación, proceso, herramientas, temperatura, energía, lote.
- **Conexiones:** esquema, puertos, señales permitidas, interfaces y pruebas eléctricas autorizadas.
- **Desmontaje:** secuencia, fuerzas/par, fijaciones, fotos previas, clips y sellos, condiciones de reversión.
- **Diagnóstico:** síntomas observados, hipótesis causal, pruebas discriminantes, resultado de cada prueba.
- **Reparación:** módulo antiguo/nuevo, procedencia, intervención, incidencias, pruebas de aceptación y resultado.
- **Riesgos:** peligros, clase de intervención, permisos, límites de energía/par/fuerza, requisitos de profesional.
- **Proveniencia:** modelo IA y versión, herramienta, código, autor/aprobador, registros de sensores.

**Estados de evidencia:** NO_MEDIDO, HIPÓTESIS, MEDIDO, VALIDADO_EN_SIMULACIÓN, VALIDADO_EN_ENSAYO, INVALIDADO. Evitar que una hipótesis de CAD termine convertida silenciosamente en «tolerancia garantizada» durante la fabricación.

---
