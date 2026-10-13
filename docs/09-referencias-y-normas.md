# Fuentes, estándares y licencias

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 21. Fuentes primarias y recursos revisados

**Revisados para esta especificación el 13/10/2026.** Los proyectos y las normas evolucionan: volver a comprobar versiones, licencias, disponibilidad y límites de seguridad cuando comience cada fase.

### Navegación, robótica y control

1. [ROS 2](https://www.ros.org/) — ecosistema de componentes robóticos.
2. [ros2_control](https://control.ros.org/) — interfaz y ciclo de control.
3. [Nav2 Docking Server](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) — docking configurable.
4. [Nav2 Behavior Trees](https://docs.nav2.org/rolling/getting_started/navigation_concepts/behavior_trees/) — tareas secuenciales/recuperación.
5. [MoveIt Task Constructor](https://moveit.picknik.ai/main/doc/concepts/moveit_task_constructor/moveit_task_constructor.html) — descomposición de tareas de manipulación.
6. [Drake](https://github.com/RobotLocomotion/drake) — dinámica, optimización, IK.
7. [ANYbotics grid_map](https://github.com/ANYbotics/grid_map) — mapa de elevación y características de terreno.
8. [AprilTag](https://github.com/AprilRobotics/apriltag) — localización relativa mediante marcadores.
9. [Especificaciones oficiales Xiaomi Robot Vacuum S12](https://www.mi.com/es/product/xiaomi-robot-vacuum-s12/specs/) — sensórica y alineación IR.
10. [Guía oficial Xiaomi: retorno a la base](https://www.mi.com/global/support/faq/details/KA-124398/) — limitaciones prácticas.

### IA y robótica abierta

11. [LeRobot](https://github.com/huggingface/lerobot) — entrenamiento e integración.
12. [SO-101](https://github.com/huggingface/lerobot/blob/main/docs/source/so101.mdx) — brazo y documentación de montaje.
13. [SmolVLA 450M](https://huggingface.co/blog/smolvla) — VLA compacto.
14. [openpi](https://github.com/Physical-Intelligence/openpi) — referencia de modelos de acción y recursos GPU.
15. [Meta Digit Plexus](https://github.com/facebookresearch/digit-plexus) — plataforma modular de sensores táctiles.
16. [AnySkin](https://any-skin.github.io/) — tacto intercambiable.
17. [Robot Metabolism, Columbia Engineering, 2025](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots) — modularidad y adaptación física.

### Ingeniería inversa, CAD, electrónica y materiales

18. [OpenScan](https://github.com/OpenScan-org) — escaneado comunitario.
19. [OpenScan Mini: guía de hardware](https://github.com/OpenScan-org/OpenScan-Doc/blob/main/docs/hardware/OpenScanMini.md) — componentes de escáner económico.
20. [FreeCAD](https://github.com/FreeCAD/FreeCAD) — CAD paramétrico.
21. [CadQuery](https://cadquery.readthedocs.io/) — CAD por Python.
22. [KiCad](https://www.kicad.org/) — esquemas y PCB.
23. [openEMS](https://docs.openems.de/en/stable/intro.html) — simulación electromagnética.
24. [Ghidra](https://github.com/NationalSecurityAgency/ghidra) — análisis de código máquina.
25. [Degate](https://github.com/DegateCommunity/Degate) — análisis de imágenes de VLSI.
26. [PulseView / sigrok](https://sigrok.org/wiki/PulseView) — análisis de señales digitales.
27. [Claude's C Compiler](https://github.com/anthropics/claudes-c-compiler) — estudio de caso de agentes de programación.
28. [3dsrecomp](https://github.com/fearkov/3dsrecomp) / [Zakuro](https://github.com/fearkov/zakuro) — recompilación/emulación de arquitectura particular.
29. [Comisión Europea: biobasados, biodegradables y compostables](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en) — definiciones y criterios ambientales.
30. [Revisión de PHA a partir de residuos, 2025](https://www.sciencedirect.com/science/article/pii/S0141813025009079) — posibilidades y restricciones de biopolímeros.

### Normativa y derecho a reparar

31. [ISO 13482:2014](https://www.iso.org/es/contents/data/standard/05/38/53820.html) — robots de asistencia personal, versión bajo revisión.
32. [ISO 10218-1:2025](https://www.iso.org/es/contents/data/standard/07/39/73933.html) — robots industriales, distinto ámbito.
33. [Reglamento (UE) 2023/1230](https://eur-lex.europa.eu/eli/reg/2023/1230/spa) — marco de maquinaria.
34. [Directiva (UE) 2024/1799](https://eur-lex.europa.eu/eli/dir/2024/1799/2026-07-31) — promoción de la reparación.

**Precaución respecto a las fuentes:** que una publicación demuestre una tarea específica, una velocidad o un sensor no permite extrapolarla automáticamente a un robot capaz de repararlo todo. Especialmente las medidas **45×70×40 cm**, **30–45 kg**, **16–24 GB** y el horizonte «década de 2030» pertenecen al planteamiento del proyecto; no son características demostradas de un producto existente.

---

---

## 22. Estándares abiertos, publicación y licencias

- Priorizar **documentación reproducible**, CAD paramétrico, archivos de circuitos, BOM, calibraciones, registros de ensayos y pruebas automatizadas.
- Analizar licencias compatibles para software (**Apache-2.0, GPL** según contexto), hardware (**CERN-OHL**) y documentación (**Creative Commons**), **sin asumir que este documento otorga automáticamente una licencia formal**.
- Separar materiales propios de componentes o software ajeno, evitar publicar piezas protegidas por propiedad intelectual sin autorización.
- Definir contratos de interoperabilidad entre modelos, herramientas, sensores y robots; el proyecto no debe depender de una única empresa.
- Política de privacidad local, cifrado, firma de software y plan de mantenimiento de dependencias.
- Publicar también experimentos fallidos, incertidumbres, perfiles de material e incidentes técnicos.
- Diseñar como proyecto abierto posible de construir por etapas y con piezas adquiribles comercialmente cuando proceda.

---
