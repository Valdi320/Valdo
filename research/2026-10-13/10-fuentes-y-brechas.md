# 10 — Matriz de fuentes, niveles de evidencia y huecos pendientes

**Corte:** 13/10/2026. **Propósito:** documentación trazable para reabrir la investigación dentro de meses o años, sin depender de respuestas de chat. Los enlaces externos requieren reevaluación de versiones, licencias, datos y normativa cuando se empiece a implementar.

## A. Fuentes de máximo retorno — procedencia y uso legítimo

| Área | Fuente original | Qué permite afirmar | Qué NO permite afirmar |
|---|---|---|---|
| Montaje | [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) | Existen bancos de prueba y CAD para tornillos, correas, cables, conectores | FDAA podrá reparar lavadoras |
| Evaluación robótica | [NIST Grasping/Manipulation](https://www.nist.gov/programs-projects/grasping-manipulation-and-contact-safety-performance-robotic-systems) | Técnicas y métricas de evaluación | Seguridad garantizada al cumplir una sola prueba |
| Casa generalista | [BEHAVIOR-1K](https://behavior.stanford.edu/) | Benchmark de 1000 actividades y 50 escenas | 1000 tareas resueltas por robot doméstico |
| NAMO histórico | [Stilman/Kuffner 2005](https://doi.org/10.1142/S0219843605000545) | Razonamiento de navegación entre obstáculos movibles | Universalidad para muebles desconocidos |
| NAMO 2026 | [Wang et al., 2609.23312](https://arxiv.org/abs/2609.23312) | Reubicación y empuje con restricciones y pruebas | Manipulación segura en cualquier vivienda |
| NAMO exploración | [Zhang et al., 2609.19541](https://arxiv.org/abs/2609.19541) | Planificación de mover vs explorar | Algoritmo completamente validado en viviendas |
| Escaleras | [Mechatronics 2026](https://www.sciencedirect.com/science/article/pii/S0957415826001297) | Mecanismo de elevación activa en un caso | Subida universal de escaleras sin arnés |
| Docking | [Nav2 Dock Framework](https://api.nav2.org/nav2-rolling/html/md_nav2_docking_README.html) | Acciones/plugin para staging/pose/refinamiento/carga | Dock real seguro sin hardware de protección |
| Actuador abierto | [ODRI](https://open-dynamic-robot-initiative.github.io/) | Diseños reproducibles de actuadores controlados por par | Robot FDAA 45×70×40 demostrado |
| Autorreconfiguración | [Columbia Robot Metabolism](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots) | Investigación de módulos robóticos reconfigurables | Reparación autónoma general de electrodomésticos |
| Tacto | [AnySkin](https://any-skin.github.io/) | Sensores reemplazables experimentales | Sensibilidad universal que resuelve todas las conexiones |
| Dataset | [LeRobot real-world imitation](https://github.com/huggingface/lerobot/blob/main/docs/source/il_robots.mdx) | Método documentado de teleoperar/grabar/entrenar/evaluar | Política robusta sin nuevas demostraciones |
| VLA compacto | [SmolVLA](https://huggingface.co/blog/smolvla) | Investigación de VLA de tamaño reducido | Reparador omnisciente |
| VLA 16 GB | [GR00T N1.7 requisitos](https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md) | Umbral de referencia 16 GB para inferencia y 40 GB+ para fine-tuning | Entrenamiento completo/rapidez útil en RTX4080 ya medidos |
| Simulación pesada | [Isaac Sim requisitos](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) | Mínimo 32 GB RAM + RTX4080 16 GB | Viabilidad completa en host de 24 GB |
| Sim ligera | [MuJoCo](https://github.com/google-deepmind/mujoco) | Simulador abierto y bibliotecas físicas | Equivalencia física perfecta |
| Sim CUDA | [MuJoCo MJX/Warp](https://github.com/google-deepmind/mujoco/blob/main/doc/mjx.rst) | Caminos acelerados hardware para investigación | Que no consumirá GPU/RAM en escena real |
| ROS LTS 2026 | [ROS 2 Lyrical](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021) | LTS mayo 2026–mayo 2031 | Soporte nativo de toda herramienta en Fedora |
| Planificación | [MoveIt 2](https://moveit.ai/about/distribution/) | Distribuciones y planificación manipulador | Manipulación autónoma semántica |
| Fotogrametría | [OpenScan Quality](https://openscan-org.github.io/OpenScan-Doc/photogrammetry/quality/) | Necesidad de escala y limitaciones | Tolerancias recuperadas sin medir |
| CAD por IA | [CAD-Recode ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Rukhovich_CAD-Recode_Reverse_Engineering_CAD_Code_from_Point_Clouds_ICCV_2025_paper.html) | Código paramétrico generado desde puntos | Identificación de material y función original |
| CAD 2026 | [RenCAD](https://www.sciencedirect.com/science/article/abs/pii/S0952197625031380) | Investigación de reconstrucción CAD editable | Universalidad industrial inmediata |
| CAD intercambio | [NIST STEP/AP242](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/step-nist) | Estándar de interoperabilidad CAD/PMI | Modelo físico correcto por exportar STEP |
| Inspección | [NIST QIF](https://www.nist.gov/publications/end-end-quality-information-framework-qif-technology-survey) | Estándar de intercambio de metrología | Inspecciones automáticamente fiables |
| Elect. firmware | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Herramienta de ingeniería inversa digital | Código fuente original recuperado |
| Electrónica física | [Degate](https://github.com/DegateCommunity/Degate) | Análisis semiautomático de imágenes IC | Chips avanzados reproducidos |
| Impresión | [ISO/ASTM 52900](https://www.iso.org/standard/74514.html) | Terminología de fabricación aditiva | Calidad certificada por imprimir |
| Reciclaje abierto | [Precious Plastic](https://www.preciousplastic.com/machines/basic) | Diseños y flujo de reciclado local | Recuperación sin consumo/seguridad/mermas |
| PLA | [Reextrusión PLA y origen](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/) | Propiedades dependen de historial y pureza | PLA se recicla indefinidamente |
| PHA | [Revisión 2025](https://www.sciencedirect.com/science/article/pii/S0959652625016075) | Costes de separación/proceso y escala | PHA doméstico barato |
| Biopolímeros | [Comisión UE](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en) | Distinción biobasado/biodegradable/compostable | Todos los bioplásticos son compostables |
| Servicio robótico | [ISO 13482:2014](https://www.iso.org/standard/53820.html) | Versión publicada para robots de cuidado personal | Cubre todo robot doméstico futuro |
| ISO nueva | [ISO/FDIS 13482](https://www.iso.org/standard/83498.html) | Edición 2 en aprobación octubre 2026 | Norma ya publicada y aplicable |
| Máquinas | [UE 2023/1230 consolidado](https://eur-lex.europa.eu/eli/reg/2023/1230/en) | Aplicación general desde 20/01/2027 en versión 2026 | Cualquier prototipo es CE automáticamente |
| IA | [Comisión EU AI Act](https://digital-strategy.ec.europa.eu/es/policies/regulatory-framework-ai) | Calendario revisado 2026, ámbitos de alto riesgo | Todo LLM embebido es high-risk |
| Ciberseguridad | [CRA y notificación](https://digital-strategy.ec.europa.eu/es/policies/cra-reporting) | Reglas de reporte desde 11/09/2026 | Toda pieza open source tiene igual obligación |
| Reparar | [Right to repair UE](https://commission.europa.eu/news-and-media/news/right-repair-new-consumer-rights-easy-and-attractive-repairs-2026-07-31_en) | Nuevos derechos para determinados bienes 2026 | Derecho ilimitado a modificar aparatos de alto riesgo |
| DPP | [ESPR 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng) | Marco de pasaportes y ecodiseño | Cualquier pieza casera exige DPP completo hoy |

## B. Qué falta medir en nuestro proyecto (no sustituir por predicción)

**Robótica:** par y estabilidad de cuatro ruedas-patas con dos brazos; maniobra con cable/junta/clip realmente deteriorados; probabilidad de fallo de rescate; energía por trabajo; escalones abiertos y apoyo sobre objetos no verificables.

**IA:** VRAM/RAM/latencia real del conjunto LLM + visión + VLA; necesidad de dataset específico para electrodomésticos; generalización a conectores no vistos; sensibilidad de clasificación de riesgo; robustez sin red.

**Ingeniería inversa:** error de escala en piezas concretas, tipos de superficies reflectantes/transparentes, material inferido vs medido, tiempo de reconstrucción paramétrica por forma, precisión tolerancias, ensayo físico de piezas de reemplazo.

**Fabricación:** compatibilidad multimaterial real, desgaste por reciclaje, controles de contaminación, seguridad de trituración/extrusión, balance LCA local vs compra externa, coste de piezas fallidas, durabilidad.

**Sistema/legislación:** ámbito legal exacto al fabricar y comercializar; formación y certificaciones; capacidad de responsabilidades e indemnización; permisos y conservación de datos; necesidad de evaluación de terceros.

## C. Calidad de evidencia y qué debe hacer un próximo investigador

- **A — documentación oficial/estándar/medida:** fuente institucional con versión y ámbito. No extrapolar fuera de ese ámbito.
- **B — resultado publicado en investigación:** evaluar si solo simulación, cuántos objetos, cantidad de pruebas y acceso a código.
- **C — demo/marketing/proyecto comunitario:** sirve como inspiración, no como garantía.
- **P — propuesta FDAA:** requiere prueba reproducible propia.

Para cada afirmación futura guardar `afirmacion_id`, fuente, URL, fecha de consulta, versión o commit, tipo A/B/C/P, ámbito probado, refutación posible y estado de verificación. **No mezclar resultados propios con publicaciones de terceros.**

## D. Controles de caducidad y revisión

Revisar por lo menos antes de cada compra y cada fase física:
- seguridad y regulación española/europea (ISO/FDIS 13482, máquinas, IA, CRA, refrigerantes);
- ROS/MoveIt/Isaac/Gazebo y herramientas Python (compatibilidad exacta);
- licencias de CAD, modelos VLA, firmware y placas abiertas;
- disponibilidad local de recambios/motores/baterías y precio documentado;
- publicaciones de CAD inverso, NAMO, tacto y fabricación con nuevas validaciones;
- límites de energía, RAM/VRAM y controles de privacidad.

## E. Próximos cinco huecos de mayor impacto

1. **Física/coste de la arquitectura:** simular A/B/C con masas, cargas y consumo; no escoger solo por apariencia.
2. **Destreza replicable:** montar los tableros NIST y demostrar tornillería, clip/cable y conectores.
3. **Datos de seguridad:** FMEA, estados seguros, controles independientes, personas/pets y modo de rechazo.
4. **CAD paramétrico medido:** escala y tolerancias con captura calibrada, no solo AI-mesh.
5. **Dock/servicio:** medición real de carga y cambio de módulo, para probar autorreparación limitada desde el principio.

**Resultado del análisis:** ahora existe una ruta defendible para obtener una primera fábrica/reparador útil por partes. **No existe evidencia de una máquina universal comercial y autónoma que reúna todos los objetivos FDAA** a octubre de 2026.
