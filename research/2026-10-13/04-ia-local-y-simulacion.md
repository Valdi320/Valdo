# 04 — IA local, robótica aprendida, simulación y adaptación a hardware doméstico

## 1. Una GPU de 16 GB sí puede orquestar — pero no resolver todo por sí sola

**[D]** [NVIDIA GR00T N1.7, guía de hardware](https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md) documenta **16 GB o más para inferencia**, y **al menos 40 GB para su ajuste fino recomendado**. Ese modelo ~3B es una política VLA de robótica, **no un técnico universal capaz de diagnosticar cualquier lavadora**. [SmolVLA de LeRobot](https://huggingface.co/blog/smolvla), más pequeño, es otra opción para tareas especializadas. LeRobot describe cómo **grabar teleoperación → entrenar → evaluar** [tutorial](https://github.com/huggingface/lerobot/blob/main/docs/source/il_robots.mdx).

**[P]** Adoptar una composición de servicios:
- **Planificador LLM local:** entiende intención, lee manual y elige próxima operación; admite latencia de segundos, no controla equilibrio.
- **Visión y estimación geométrica:** segmentación, poses, seguimiento de herramientas, OCR y diagnóstico.
- **Políticas de movimiento VLA o control clásico:** comandos de manipulación específicos; frecuencia y latencia medidas.
- **Control en MCU y barreras de seguridad:** lazo local con restricciones de par, temperatura, velocidad y colisiones.
- **Motores científicos:** FreeCAD/CadQuery, MoveIt, Nav2, MuJoCo, circuitos SPICE y métricas automáticas.
- **Memoria local recuperable:** manuales, inventario, episodios, firmas/compatibilidades de módulos y ensayos; evitar meter años de historial íntegros en contexto LLM.

### Realidad sobre el PC de referencia

**[D]** NVIDIA especifica para [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html): CPU AMD Ryzen 5 aceptable como mínimo, **32 GB de RAM del sistema**, **RTX 4080 16 GB mínimo**, 50 GB SSD. El equipo de referencia tiene **Ryzen 5 5600X, RTX 4080 16 GB y 24 GB DDR4**: GPU mínima, pero **RAM inferior a la exigida oficialmente**. El mínimo no garantiza que escenas complejas o Isaac Lab entrenen allí. Algunos assets pueden necesitar Internet inicialmente, aunque el robot final debe funcionar offline.

**[P]** No comprar inmediatamente más hardware. Comenzar con **MuJoCo/CPU** para cinemática, estabilidad y control de pocos cuerpos, y ROS 2 + Gazebo con escenas sencillas; dejar Isaac Sim/Lab como vía opcional cuando se hayan validado RAM, distribuciones y margen VRAM.

## 2. ROS 2 y simulación: no elegir una rama obsoleta

**[D]** [ROS 2 Lyrical Luth](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021) se lanzó el 22 de mayo de 2026 con mantenimiento hasta **mayo de 2031**; [MoveIt 2 Lyrical](https://moveit.ai/about/distribution/) está soportado. En binarios, [Ubuntu 26.04 para Lyrical](https://moveit.ai/documentation/faqs/) es ruta principal, mientras que Jazzy/Ubuntu 24.04 mantiene un ecosistema grande.

**[P] Recomendación:**
- Probar **Jazzy + Gazebo Harmonic** en un contenedor Ubuntu 24.04 aislado si se quiere aprovechar referencias robustas, sin modificar el sistema Fedora/Bazzite del host.
- Evaluar **Lyrical + Ubuntu 26.04** para proyecto nuevo a largo plazo si Nav2, control y simulador necesarios funcionan allí.
- No confundir que ROS distribuya paquetes Linux con que cualquier simulador funcione igual en Fedora, Bazzite o Toolbox.
- Fijar versiones de ROS, simulador, ROS-Gazebo bridge, controlador, RMW, CUDA, Python y dependencias en contenedores reproducibles.
- No activar ROS en una máquina real sin verificación de stop y límites de actuadores.

**[D]** Hay pilas de integración abierta con Gazebo/MoveIt/Nav2 para estudiar: [rbot](https://github.com/rlxai/rbot) y [MUR5e](https://github.com/Mostafasaad1/ros2-mur5e-mobile-manipulator-stack), pero su existencia **no sustituye ensayos sobre el hardware FDAA**.

## 3. MuJoCo vs Gazebo vs Isaac Sim: selección por objetivo

| Herramienta | Destino preferente | Riesgo a controlar |
|---|---|---|
| [MuJoCo](https://github.com/google-deepmind/mujoco) | control, contacto, mecánica, pruebas de estabilidad y articulaciones | modelos de fricción y contactos no perfectos; calibración sim-to-real |
| [MJX/MuJoCo Warp](https://github.com/google-deepmind/mujoco/blob/main/doc/mjx.rst) | simulación paralela para políticas/RL con GPU | VRAM, dependencias y cobertura física |
| [Gazebo](https://gazebosim.org/) + ROS 2 | sensores, nav, docking, controladores, mundo doméstico sencillo | integración de plugins y versiones |
| [Isaac Sim/Lab](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) | simulación visual/física compleja y generación de datos sintéticos | RAM mínima 32 GB, GPU y almacenamiento |
| [BEHAVIOR-1K](https://behavior.stanford.edu/) | benchmark largo de tareas domésticas | muy pesado; no tratar como simulador ligero universal |

**[D]** BEHAVIOR-1K documenta **1.000 tareas domésticas, 50 escenas y más de 10.000 objetos**. Es un benchmark extraordinario de aspiración y cobertura funcional, no promesa de ejecutar todo localmente en 16 GB. [Sitio del proyecto](https://behavior.stanford.edu/).

## 4. Arquitectura temporal propuesta (tasas iniciales hipotéticas)

| Proceso | Naturaleza | Requisito |
|---|---|---|
| servo/seguridad (MCU) | tiempo real determinista | no depender de Wi-Fi ni LLM |
| estimación de estado y contacto | rápida y constante | timestamps y watchdogs |
| navegación/cinemática | reactiva y periódica | límite de latencia en ensayo |
| política aprendida VLA | acciones de horizonte corto | inferencia con supervisión y abortos |
| LLM / consulta de manual | bajo ritmo | sin bloqueo del control físico |
| CAD / FEA / simulación | asíncrono respecto a movimiento | prohibido mover actuador si ensayo sigue pendiente |

**No fijar Hz definitivos sin hardware real.** Definir límite de edad de sensores, intervalo de watchdog, jitter máximo tolerado, gestión de saturación, stop y safe-hold en cada interfaz.

## 5. Selección de tareas y recogida de datos

**[P]** Aprender por tareas elementales: localizar pieza, tomar tornillo, insertar conector, retirar clip reversible, arrastrar herramienta con contacto, alinear dock. Diferenciar:
1. entrenamiento/ejemplos;
2. validación sobre posiciones nuevas con piezas conocidas;
3. test ciego sobre piezas y modelos no vistos;
4. recuperación ante fallos deliberadamente seguros;
5. prueba de **rechazo** cuando el mundo no permite inferencias suficientemente fiables.

**No filtrar imágenes de hogares ajenos**; registros locales cifrados, consentimiento y selección de fotogramas. Mantener datos de fallos porque son indispensables para detectar límites. En cada experimento registrar modelo/versión/cuantiación, secuencia de prompts, herramientas, VRAM pico, RAM pico, latencia, fallos y paradas.

## 6. Medición de IA local

**[P] Un benchmark mínimo útil en 16 GB (sin hardware nuevo):**
- 20 tareas de lectura de manual y localización de información crítica con respuestas trazables.
- 5 piezas en CAD: producir geometría parametrizada, verificador independiente de dimensiones y detección de cambios.
- 3 episodios de planificación NAMO sobre escenarios simulados con elección segura.
- 3 ensayos de descomposición «desmontar/apretar/alinear» representados sin movimiento real.
- 1 intervención fallida: IA debe reconocer incertidumbre, **solicitar medidas** y detener el plan.
- Perfiles de memoria y rendimiento que distingan GPU, RAM y procesos simultáneos.

Criterio esencial: **no sacrificar precisión de datos ni seguridad para que quepa una demostración llamativa en 16 GB**.

**Fuentes principales:** [NVIDIA Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), [GR00T N1.7 hardware](https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md), [ROS Lyrical](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021), [MoveIt](https://moveit.ai/about/distribution/), [MuJoCo](https://github.com/google-deepmind/mujoco), [MJX](https://github.com/google-deepmind/mujoco/blob/main/doc/mjx.rst), [LeRobot](https://github.com/huggingface/lerobot/blob/main/docs/source/il_robots.mdx), [BEHAVIOR](https://behavior.stanford.edu/).
