# FDAA — investigación complementaria de viabilidad (13 de octubre de 2026)

**Estado: investigación documental, NO prototipo validado.** Esta carpeta amplía sin reemplazar la [especificación canónica](../../docs/PROYECTO_CANONICO.md) y la [issue principal](https://github.com/Valdi320/Valdo/issues/2). Las propuestas se identifican como tales, y los hechos contrastados enlazan a fuentes primarias. Las referencias de software, normas y hardware son una fotografía del **13/10/2026** y deben comprobarse al arrancar cada fase.

## Descubrimientos más importantes

1. **La destreza de montaje es un cuello de botella mayor que el lenguaje.** NIST publica tableros y protocolos para inserción de conectores, tornillos, engranajes, correas y cableado: un benchmark inmediato y reproducible. [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly).
2. **El robot no debe depender de levantar cargas con los brazos.** Toda acción lateral implica momento de vuelco, posibles anclajes, apoyo y reparto de masa. Comparar ruedas-patas con una base de ruedas más fácil antes de congelar 45×70×40 cm; [ODRI](https://open-dynamic-robot-initiative.github.io/) publica actuadores modulares para investigación.
3. **Mover obstáculos ya es un campo técnico propio:** *Navigation Among Movable Obstacles* (NAMO). En septiembre de 2026 se publicaron métodos que enlazan ruta, reubicación y capacidad real de empujar [arXiv 2609.23312](https://arxiv.org/abs/2609.23312), con limitaciones experimentales.
4. **El primer taller robótico debería probar un módulo estándar, no una lavadora real.** El ensamblaje y desmontaje requieren táctil, fuerza/par, observación de cables, gestión de piezas y reversión; ver [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/robotic-grasping-0).
5. **IA local 16 GB: plausible para inferencia especializada, NO universalidad.** NVIDIA documenta inferencia de GR00T N1.7 desde 16 GB, mientras que su ajuste fino recomendado necesita ≥40 GB; el control seguro debe funcionar sin la IA. [NVIDIA](https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md).
6. **Limitación concreta del PC de referencia:** la RTX 4080 de 16 GB alcanza la GPU mínima que documenta Isaac Sim, pero la instalación completa solicita **32 GB de RAM del sistema como mínimo**; el PC actual tiene 24 GB. No afirmar que todo Isaac Sim / Isaac Lab cabe ahí. Priorizar simulaciones pequeñas MuJoCo y Gazebo/ROS aislados. [Requisitos Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html).
7. **ROS 2 ya tiene LTS 2026:** Lyrical Luth se publicó en mayo de 2026 con soporte hasta 2031; usar Ubuntu 26.04 en contenedor/VM si se elige esa rama, y mantener Jazzy/Ubuntu 24.04 como alternativa de compatibilidad. [ROS](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021), [MoveIt](https://moveit.ai/about/distribution/).
8. **El escaneo sin calibración no da piezas fiables.** OpenScan advierte que la fotogrametría puede carecer de escala absoluta; NIST propone trazabilidad metrológica. En CAD, iniciativas como CAD-Recode ya infieren código paramétrico desde puntos, sin garantizar tolerancias ni intención. [OpenScan](https://openscan-org.github.io/OpenScan-Doc/photogrammetry/quality/), [ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Rukhovich_CAD-Recode_Reverse_Engineering_CAD_Code_from_Point_Clouds_ICCV_2025_paper.html).
9. **Reciclaje doméstico ≠ reciclaje ilimitado.** Estudios experimentales de PLA confirman degradación con ciclos y ventaja de mantener procedencia/lotes; [artículo experimental](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/). PHA tiene cuellos de botella de extracción y escala [revisión](https://www.sciencedirect.com/science/article/pii/S0959652625016075).
10. **La normativa ha cambiado en 2026:** ISO/FDIS 13482 (edición 2) está en aprobación, *no publicada aún* a 13/10/2026; el reglamento europeo de maquinaria aplica en general desde 20/01/2027, y el Cyber Resilience Act ya activa notificaciones en 09/2026. Consultar versiones consolidadas y ámbitos reales. [ISO FDIS](https://www.iso.org/standard/83498.html), [UE maquinaria](https://eur-lex.europa.eu/eli/reg/2023/1230/en), [CRA](https://digital-strategy.ec.europa.eu/es/policies/cra-reporting).
11. **El Reglamento de Ecodiseño (UE) 2024/1781 abre una vía de interoperabilidad:** pasaportes digitales y datos de reparación/materiales. El proyecto debe crear pasaportes locales desde ahora, sin presentarlos como conformidad jurídica. [Reglamento](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng).
12. **La prueba debe ser reproducible y registrar fallos.** Complementar 12 pruebas del repositorio con benchmarks de [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) y [BEHAVIOR-1K](https://behavior.stanford.edu/), con condiciones de parada y casos fuera de distribución.

## Informes de esta campaña

- [01 · Arquitectura mecánica, estabilidad y tamaño mínimo](01-arquitectura-mecanica.md)
- [02 · Manipulación, desmontaje y reparación mutua](02-manipulacion-y-reparabilidad.md)
- [03 · Navegación activa, escaleras y docking](03-navegacion-y-rescate.md)
- [04 · IA local, simulación y aprendizaje](04-ia-local-y-simulacion.md)
- [05 · Ingeniería inversa física/digital y metrología](05-ingenieria-inversa-metrologia.md)
- [06 · Materiales, reciclaje y microfábrica](06-materiales-y-fabricacion-circular.md)
- [07 · Seguridad, normativa europea y ciberseguridad](07-seguridad-y-normativa.md)
- [08 · Modelo de datos, interoperabilidad y trazabilidad](08-datos-y-contratos.md)
- [09 · Plan de pruebas y decisiones económicas](09-pruebas-y-economia.md)
- [10 · Fuentes, incertidumbres y brechas de conocimiento](10-fuentes-y-brechas.md)
- [ADR-0002 · estrategia modular y de simulación primero](../../docs/ADR-0002-estrategia-de-investigacion.md)
- [Registro ampliado de riesgos](riesgos-adicionales.csv) · [experimentos investigables](experimentos-priorizados.csv)

## Política de evidencia

| Etiqueta | Significado | Uso |
|---|---|---|
| **[D] Demostrado** | Medición, documentación oficial o experimento publicado dentro de su ámbito | Describir exactamente las condiciones de la fuente |
| **[I] Inferencia** | Consecuencia razonada, no ensayada en FDAA | Exponer supuestos y refutación |
| **[P] Propuesta** | Diseño/criterio experimental para nuestro futuro sistema | No presentarlo como producto actual |
| **[A] Abierto** | Falta medir, probar o verificar | No completar con cifras inventadas |

**Orden de inversión sugerido:** ninguna compra de robot completo sin superar simulación y control de seguridad; primera meta con hardware existente: digitalizar piezas + CAD paramétrico + ensayo dimensional. Esta investigación por sí sola **no constituye una evaluación de conformidad ni asesoramiento jurídico**.
