# 09 — Hoja de experimentación, coste real, priorización y puertas de aceptación

## 1. Evitar el error de intentar «terminar el robot» antes de poder comprobar una sola destreza

**[D]** [NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) proporciona benchmarks con tableros de montaje/desmontaje. [BEHAVIOR-1K](https://behavior.stanford.edu/) establece una referencia ambiciosa de tareas domésticas largas. **[P]** Utilizar ambos niveles: *destrezas elementales verificables* antes de *misiones domésticas de muchas etapas*.

### El recorrido más corto hacia evidencia útil

| Gate | Producto demostrable | Qué descarta | Avance solo si... |
|---|---|---|---|
| G0 | CAD/cálculos de tres cuerpos candidatos | tamaño mínimo imposible | masas, volúmenes, estabilidad y riesgos razonados |
| G1 | imagen de pieza → CAD paramétrico → pieza | «escáner = plano» | cotas verificadas + ajuste a pieza |
| G2 | robot de banco toma/coloca/conecta módulos | falta de destreza | fuerza/tacto, FAIL documentados |
| G3 | navegación y carga en dock | regreso impreciso | carga real verificada, reintentos controlados |
| G4 | dock cambia módulo averiado | «autorreparación» meramente nominal | máquina restaurada y ensayo posrecambio |
| G5 | A arregla B y B arregla A | fallo único y roles rígidos | ambos pueden intervenir con otro apagado |
| G6 | robot supera/despeja obstáculo controlado | navegación 2D insuficiente | soporte y contacto seguros, abortos |
| G7 | maqueta de electrodoméstico: extracción/reparación/retorno | demo de solo «cambiar una pieza» | misión completa sin daño |
| G8 | materiales recuperados y calidad verificada | reciclaje ilusorio | trazabilidad, ensayos, energía por ciclo |
| G9 | integración con revisión externa | ensamblaje de demos aisladas | estabilidad, registros y seguridad integral |

**Cada gate tiene PASS / FAIL / INVALID / UNKNOWN**. Si la medición falta, el resultado es UNKNOWN, no PASS.

## 2. Primer paquete que puede investigarse sin comprar grandes equipos

**[P] Tareas digitales de máximo retorno:**
- Crear tres diseños CAD de robot en contenedores virtuales y comprobar si 45×70×40 cm es plausible sin ignorar masa de motores/baterías.
- Ejecutar en MuJoCo un modelo simple de base y brazo, y medir vuelco por fuerza lateral y velocidad; **no extrapolar directamente a hardware real**.
- Construir en software una plantilla CAD paramétrica de una pieza simple, exportar STEP, comparar contra cotas conocidas.
- Prototipar ruta ROS 2/Nav2 docking en simulador ligero, con pérdida de observación y señal de carga simulada.
- Preparar dataset y contratos de información desde manuales y ejemplos públicos; **no recopilar fotos privadas sin consentimiento**.
- Establecer lista de 30–50 escenarios seguros de la vivienda y evaluación de riesgos.

**Criterios de inicio:** entornos aislados del resto del PC, sin interferir en proyectos activos, logs reproducibles, sin cambiar hardware ni prometer intervención física.

## 3. Plan reproducible de 12 ensayos mínimos

| ID | Experimento | Registro obligatorio | Fallo a provocar con seguridad |
|---|---|---|---|
| EX-01 | Escaneo de pieza con patrón de escala | sensor, escala, incertidumbre | quitar patrón y demostrar que se detecta escala desconocida |
| EX-02 | CAD paramétrico vs malla | bocetos/param, STEP, residuo | cambiar una cota y validar redibujado |
| EX-03 | 100 docks simulados/posibles | poses, contactos, tensión/corriente | mover o tapar marcador |
| EX-04 | Tornillos y tuercas tipo NIST | par-giro, daños, tiempo | rosca no alineada |
| EX-05 | Conectores y cableado | fuerza, retención, imágenes | conector incompatible |
| EX-06 | Módulo de robot defectuoso | diagnóstico+part_id+retest | desconectar sensor de estado |
| EX-07 | Rescate del robot apagado | soporte y contactos, tiempos | A no colabora porque está apagado |
| EX-08 | NAMO retirar silla | ruta antes/después, entorno | no hay lugar seguro donde dejar objeto |
| EX-09 | Escalón con arnés | contactos, fuerzas, fallos | deslizamiento controlado que obliga a abortar |
| EX-10 | Puente sobre apoyos reales | carga/deformación/apoyos | apoyo demasiado blando (rechazar) |
| EX-11 | Material reextrusionado | lote, propiedades, calor, humedad | mezcla sin trazabilidad (rechazar uso crítico) |
| EX-12 | Desconectar LLM/red | watchdog, energía, modos degradados | interrupción durante orden no crítica |

**Objetivos medibles por definir** según sensor y plataforma: porcentajes de éxito, rangos de par, tolerancias, distancias de seguridad y número de repeticiones; no inventar números para dar apariencia científica.

## 4. Presupuesto basado en BOM, no en precios elegidos de memoria

**[P]** Para cada etapa mantener cuatro sumandos separados:

```text
Coste_total_real =
  piezas_y_subsistemas
+ herramientas_de_fabricación_y_medición
+ consumibles_electricidad_y_repuestos
+ ensayos_de_seguridad_y_fallos
```

**Coste por reparación** requiere además:
- horas efectivas de diagnóstico, operación y limpieza;
- energía total (ordenador+robots+taller+clima/ventilación);
- porcentaje de impresiones o reparaciones fallidas;
- agotamiento de material/lotes y repuestos especializados;
- depreciación de motores, baterías, herramientas y sensores;
- garantías, seguros y profesionales cuando corresponda;
- transporte y compra externa frente a fabricar localmente;
- mantenimiento de la estación (tercer robot) y del compañero (robot B).

**Alternativas para comparar:** servicio humano local; reparación manual con pieza impresa; robot de brazo estacionario; robot móvil + dock; dos robots + fábrica. El sistema completo no será siempre más económico: demostrar en qué tareas se amortiza.

### No presupuestar antes de validar
- No asegurar que un robot compacto con 14 GDL de brazos + cuatro patas articuladas cabe en «cientos de euros».
- No comparar precio de kit pequeño SO-101 con el coste de dos robots de servicio seguros.
- No ocultar herramientas de precisión, baterías certificadas, ensayos físicos o mantenimiento.
- No tratar IA local como «gratis»: energía, hardware, horas de desarrollo y actualización cuentan.
- No atribuir a impresión 3D ahorro ambiental sin análisis de ciclo de vida y fallos.

## 5. Priorización por información ganada

**[P]** Definir para cada experimento: coste estimado, riesgo, dependencia de hardware, incertidumbre crítica que resuelve, entregable y posibilidad de reutilización. Usar una matriz de selección **cualitativa, no puntuación inventada**.

| Acción | Retorno potencial | Dependencias | Prioridad sugerida |
|---|---|---|---|
| Medir robot virtual y centro de masa | evita arquitectura imposible | CAD/sim | **P0** |
| Test de escala y CAD de pieza | fundamento descompilador físico | cámara+patrón | **P0** |
| NIST task board con pinza | fundamento reparación física | brazo real | **P1** |
| Dock AprilTag + carga real | autonomía básica económica | chasis básico y dock | **P1** |
| Cambio modular con brazo fijo | viabilidad autorreparación | útil y fijaciones | **P1** |
| Doble robot completo con escalera | hito costoso y arriesgado | G0–G4 | **P3** |
| Cultivo de PHA en casa | incertidumbre bioeconómica alta | laboratorio especializado | **I+D separado** |
| Tomografía de piezas cerradas | alto coste/seguridad | laboratorio externo | **según caso** |

## 6. Benchmark que impida «sobreajuste al salón»

**[P]** Separar:
- 10 escenarios de entrenamiento/configuración conocidos;
- 10 escenarios de validación sobre la misma familia con posiciones distintas;
- 10 escenarios no vistos donde cambian obstáculos, material, iluminación, herramienta o geometría;
- al menos cinco **pruebas de rechazo** con información insuficiente o riesgo;
- fallos físicos y degradaciones (sensor tapado, batería baja, dock movido, robot apagado).

Los conjuntos nunca deben mezclarse sin registrar la contaminación. Evaluar tanto tasa de éxito como daños, tiempo y recuperación; «llegar a destino» con objetos rotos se puntúa como fracaso.

## 7. Métricas de largo plazo (especialmente autorreparación)

- MTBF/MTTR **con contexto y suficientes horas**, no obtenidos de una única demo.
- Tiempo desde diagnóstico a suministro de repuesto, a intervención y a recalibración.
- Proporción de fallos que **no** se pueden reparar sin ayuda externa.
- Horas de inactividad acumuladas y número de fallos comunes entre robots A, B y base.
- Grado de dependencia industrial residual: motores, reductoras, chips, baterías, materiales, herramientas.
- Proporción de tareas domésticas realmente completadas, con definición explícita de denominador.
- Residuos y carbono por ciclo de vida, no solo masa de plástico recuperado.

**[D]** Las tareas domésticas reales combinan secuencias largas y objetos muy variados; [BEHAVIOR-1K](https://behavior.stanford.edu/) ofrece 1.000 actividades y un marco útil de evaluación. Es un benchmark de investigación, no evidencia de que un robot comercial las complete.

## 8. Próxima decisión ejecutiva

No elegir motor, impresora, material universal ni estructura final antes de G0/G1. Crear en GitHub **issues por cada experimento**, con criterio de PASS/FAIL y bloqueo de riesgo. El primer prototipo integral de interés combina **un brazo sencillo + CAD verificable + base de docking**, sin ruedas-patas caras ni electrodomésticos energizados.

**Fuentes:** [NIST tareas montaje](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly), [BEHAVIOR-1K](https://behavior.stanford.edu/), [ODRI actuadores](https://open-dynamic-robot-initiative.github.io/), [MuJoCo](https://github.com/google-deepmind/mujoco), [Nav2 docking](https://api.nav2.org/nav2-rolling/html/md_nav2_docking_README.html), [Reciclado de PLA](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/).
