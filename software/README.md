# Software local de FDAA

Arquitectura: **usuario y permisos → IA planificadora local → percepción/memoria con evidencia → navegación/manipulación/CAD → supervisor de seguridad independiente → controladores deterministas**.

Herramientas candidatas por evaluar: [ROS 2](https://www.ros.org/), [ros2_control](https://control.ros.org/), [Nav2](https://docs.nav2.org/), [MoveIt 2](https://moveit.picknik.ai/main/), [Drake](https://github.com/RobotLocomotion/drake), [LeRobot](https://github.com/huggingface/lerobot), [SmolVLA](https://huggingface.co/blog/smolvla), [AprilTag](https://github.com/AprilRobotics/apriltag), [FreeCAD](https://github.com/FreeCAD/FreeCAD), [CadQuery](https://cadquery.readthedocs.io/), [KiCad](https://www.kicad.org/), [Ghidra](https://github.com/NationalSecurityAgency/ghidra) y [PulseView](https://sigrok.org/wiki/PulseView).

**Prueba inicial:** usar LLM local objetivo ≤16 GB VRAM para orquestar visión → escaneo → CAD paramétrico → fabricación → inspección de 5 piezas. Medir VRAM pico y latencia; compartir cómputo con estación cuando convenga. **No asumir** que modelos robóticos VLA actuales reparen cualquier objeto desconocido.

Seguridad, parada de emergencia y control de par deben funcionar aun sin Wi-Fi, sin modelo general y sin ordenador principal.
