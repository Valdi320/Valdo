# 03 — Navegación entre obstáculos, escaleras, acoplamiento y rescate

## 1. El problema exacto de la cama bloqueando la ruta tiene nombre: NAMO

**[D]** *Navigation Among Movable Obstacles* (NAMO) permite que un robot **modifique temporalmente la disposición de los objetos** para abrir una ruta. No es simplemente un planificador de rutas que evita colisiones. Ya se formalizó en [Stilman y Kuffner (2005)](https://doi.org/10.1142/S0219843605000545). Investigación de **septiembre de 2026** [Wang et al., arXiv 2609.23312](https://arxiv.org/abs/2609.23312) estudia reubicación con geometría y capacidad de empuje, incluyendo pruebas físicas; [Zhang et al., arXiv 2609.19541](https://arxiv.org/abs/2609.19541) trata el dilema de explorar caminos desconocidos frente a mover objetos y la dependencia entre varios obstáculos.

**[I]** Estos resultados son relevantes para muebles, pero **no prueban capacidad general** con colchones, objetos frágiles, cables, mascotas ni muebles de masa desconocida.

## 2. Arquitectura de planificación de cuatro niveles

1. **Topología:** regiones habitables, puertas, escaleras, pasillos, plantas; buscar alternativas de ruta sin interacción.
2. **Geometría 3D:** mapa de ocupación, alturas y suelo, envolvente actual del robot, brazos y herramientas; detectar apoyos.
3. **Propiedades y manipulabilidad:** móvil/fijo/desconocido, masa/centro de gravedad estimados, agarres, fricción, conexiones, daños potenciales y autorización humana.
4. **Plan ejecutable:** TAMP (*task and motion planning*), contactos/estabilidad, destino seguro de cada objeto, comprobaciones intermedias y retorno de muebles cuando corresponda.

**[P]** Separar el plan de alto nivel («desplazar silla»), el plan de contacto («punto de empuje») y el controlador físico en tiempo real. Un LLM puede sugerir hipótesis, pero un verificador mecánico debe vetar apoyos y fuerzas inviables.

### Máquina de estados propuesta

```text
GOAL → MAP → TRY_PATH → [PATH_OK] MOVE
                         [BLOCKED] → CLASSIFY_BLOCKER
                                     → TRY_RECONFIGURE
                                     → TRY_SAFE_RELOCATE
                                     → TRY_REMOTE_TOOL
                                     → TRY_CHECKED_BRIDGE
                                     → ASK_COMPANION
                                     → STOP_AND_REQUEST_HELP
```

En todos los estados: personas, animales, escalones, cables, agua, materiales y permiso prevalecen sobre tiempo/eficiencia.

## 3. Un objeto caído NO es solo una geometría

**[P]** Casos de prueba:
- botella de plástico vacía → puede recogerse;
- vaso de cristal roto → evitar contacto desprotegido, delimitar y utilizar herramienta apropiada;
- taburete pesado → medir/estimar masa, geometría y dónde quedará después;
- cable conectado a enchufe → no desplazar indiscriminadamente; evaluar energía y tensión;
- persona o mascota → detener movimiento y preservar distancia;
- elemento caliente o recipiente con líquido → evitar empujes y derrames.

**Criterio:** un plan que libera el pasillo pero hace caer un objeto por las escaleras **es un fallo**, aunque llegue al destino.

## 4. ¿Subir sobre la cama?

**[I]** Colchón, somier, cabecero y estructura ofrecen resistencia y rigidez completamente distintas. Identificación visual de «cama» no demuestra capacidad de carga ni contacto suficiente. En primera generación:
1. preferir camino alternativo;
2. valorar mover la cama o reconfigurar robot;
3. utilizar un minibot/cámara si basta inspeccionar;
4. tender puente solamente entre **apoyos verificados y estables**;
5. no existe plan seguro → rechazar tarea.

**Prueba negativa deliberada:** escenario en el que una IA elige «pasar por encima» pero la supervisión de estabilidad rechaza apoyar carga en un colchón sin ensayar. El éxito de la prueba es **no subir**.

## 5. Escaleras: plan físico específico

**[D]** La literatura incluye robots con módulo elevador activo para contrahuellas abiertas [Mechatronics, octubre 2026](https://www.sciencedirect.com/science/article/pii/S0957415826001297), y muchos modelos ruedas-patas. No suponer transferencia automática a cualquier escalera.

**[P]** Percepción/calibración: borde delantero/trazado del peldaño, contrahuella, altura, ancho útil, espesor/resistencia de huella, material, fricción probable, obstáculos y distancia a caída. Ensayar hacia arriba y hacia abajo como problemas diferentes. Mantener cuerpo/masa bajos, apoyar y verificar fuerza antes de transferir peso; controlar deslizamiento, IMU y gasto de energía. Cuantificar maniobras que necesitan plataforma/retención externa.

**Rampas:**
- módulo corto de paso entre pequeñas alturas y huecos pequeños;
- inclinación máxima determinada por ensayo con carga y superficie, con frenado y retención;
- no proponer rampa larga en escalera completa por defecto: a relación 1:12, 2,5 m de desnivel exigirían unos 30 m horizontales;
- verificar puentes como estructuras sometidas a flexión, no como «tablas que caben».

## 6. Docking: dos escalas de navegación + verificación energética

**[D]** [Nav2 Docking Framework](https://api.nav2.org/nav2-rolling/html/md_nav2_docking_README.html) separa aproximación a pose de **staging**, refinamiento de pose con sensores y comprobación de `isDocked` / `isCharging`. Es compatible con detección por marcadores, cámaras y plugins de carga.

**[P] Diseño FDAA:**
- guardar `dock_id`, mapa/planta y punto de preparación;
- navegar por SLAM/odometría hasta la zona próxima;
- identificar dock por **AprilTag**/IR y refinar pose relativa con estimación de incertidumbre;
- entrar lentamente guiado por topes mecánicos; validar presencia física y **corriente de carga efectiva**, tensión y temperatura;
- ante error: retroceder, reobservar, número limitado de reintentos y parada segura;
- base movida: búsqueda local limitada y revalidación antes de actualizar mapas;
- estación nunca presenta contactos de energía peligrosa expuestos; interbloqueos eléctricos independientes.

**Caso de uso nuevo:** varios docks para pisos/planta baja o áreas de taller; navegación entre plantas solo con mecanismos aprobados.

## 7. Robot inmovilizado fuera de la estación

**[P]** Cuatro modos:
1. **Recuperación local:** reduce tareas y conserva movimiento seguro si un actuador falló.
2. **Asistencia del compañero:** herramientas y módulos in situ; control del peso/cables/batería.
3. **Remolque controlado:** chasis con puntos de agarre, ruedas liberables o patines; no arrastrar patas trabadas ni baterías dañadas.
4. **Intervención humana/profesional:** suspensión segura si no existe modo de rescate verificado.

El robot compañero no debe quedar atrapado intentando ayudar: evaluar capacidad de remolque y adherencia antes de mover. Registrar incidencias de modo que ambas máquinas no repitan el mismo error de razonamiento.

## 8. Mapa de evaluación para algoritmo NAMO

| Escena | Objetivo | Qué se considera FAIL |
|---|---|---|
| Puerta parcialmente cerrada | Abrirla/pasar sin rozar | empuje excesivo o aprisionamiento |
| Silla caída | recolocar temporalmente | nueva obstrucción/silla caída sobre otro objeto |
| Dos obstáculos dependientes | establecer orden correcto de traslado | uno impide mover el otro o atrapa el robot |
| Cama ocupa ruta | encontrar alternativa o rechazar | cargar peso sobre colchón no verificado |
| Descansillo estrecho | girar sin volcar | caída o pérdida de estabilidad |
| Dock cambiado de lugar | localizar y cargar | afirmar carga sin corriente |
| Robot averiado | llevarlo a zona segura | daño al arrastrar o fallo de compañero |

**Fuentes:** [NAMO 2005](https://doi.org/10.1142/S0219843605000545), [NAMO relocación 2026](https://arxiv.org/abs/2609.23312), [NAMO exploración 2026](https://arxiv.org/abs/2609.19541), [Nav2 docking](https://api.nav2.org/nav2-rolling/html/md_nav2_docking_README.html), [Mechatronics escaleras 2026](https://www.sciencedirect.com/science/article/pii/S0957415826001297), [NIST mobile robotics](https://www.nist.gov/programs-projects/grasping-manipulation-and-contact-safety-performance-robotic-systems).
