# Robot compacto y navegación 3D

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 6. Robot principal: forma óptima, tamaño y mecanismos

### 6.1. Preferencia de arquitectura

Un robot humanoide de tamaño adulto no parece la opción mínima para un reparador doméstico. Propusimos una **plataforma compacta de cuatro ruedas-patas, torso retráctil y dos brazos de manipulación**, con estabilizadores y herramientas externas. No está probado que supere en todos los casos a una base de ruedas omnidireccionales, orugas articuladas o dos piernas; debe compararse experimentalmente.

**Objetivos dimensionales exploratorios, no especificaciones de un producto existente:**

| Magnitud | Propuesta inicial | Estado |
|---|---:|---|
| Ancho plegado | 42–45 cm | aspiración |
| Largo plegado | 65–75 cm | aspiración |
| Alto plegado | 35–45 cm | aspiración |
| Referencia nominal de diseño | **45 × 70 × 40 cm** | por validar |
| Altura del cuerpo desplegado | 130–145 cm | por validar |
| Alcance vertical herramienta | 1,9–2,1 m | con cargas bajas, por validar |
| Peso total | 30–45 kg | muy exigente, por validar |
| Dos brazos | 7 grados de libertad por brazo | candidato |
| Alcance de cada brazo | 65–80 cm | cinemática pendiente |
| Carga útil por brazo | 2–4 kg bajo condiciones definidas | aspiración, no garantía |
| Tracción | 4 patas articuladas, ruedas en los extremos | candidato |

Es posible que varias de estas metas resulten físicamente **incompatibles entre sí**. Una combinación de cuatro patas potentes, batería, reductoras, dos brazos, sensores y torso retráctil podría exceder peso y volumen. **Priorizar capacidad y seguridad ante forzar unas medidas arbitrarias.** Determinar volumen de motores/actuadores, longitudes de barras, radio de giro, masas y pares antes de aprobar el chasis.

### 6.2. Modos de configuración

1. **Plegado/almacenamiento:** centro de gravedad bajo; brazos y piernas recogidos dentro de la anchura máxima, sin sobresalientes al cruzar puertas.
2. **Rodadura:** desplazamiento eficiente por suelo liso, control de movimiento y percepción de obstáculos.
3. **Escaleras/terreno:** cada rueda-pata puede convertirse en punto de apoyo y subir/bajar peldaños de forma secuenciada.
4. **Trabajo al suelo:** altura baja, brazo orientado lateral o frontalmente, instrumentos de visión y tacto cercanos.
5. **Trabajo a encimera:** patas estabilizadas y torso elevado; supervisión del momento de vuelco.
6. **Alcance alto:** extensión máxima con **límites inferiores de fuerza/carga**; preferir herramienta elevada o una plataforma alternativa si el equilibrio no lo permite.
7. **Mantenimiento:** articulaciones accesibles desde el exterior, postura bloqueada y conectores seguros para intervención del compañero o de la estación.

### 6.3. Manipulación fina y fuerza útil

- Brazos bimanuales para sujetar una cubierta mientras se quitan tornillos o manipular juntas y conectores con una segunda herramienta.
- Sensores de **fuerza/par en muñecas**, tacto en dedos, cámaras en muñecas, iluminación, IMU y visión externa.
- Herramientas intercambiables con identificación y calibración automática: pinzas delicadas y robustas, destornillador de par, llave, mini cámara, palpador, extractor, ventosa con **retención secundaria**, útiles para clips/conectores y guías de cableado.
- Enfoque en **control de fuerza**, no solo de posición: no romper plástico frágil, vidrio, contactos, roscas o cables.
- Al efectuar esfuerzos laterales, desplegar huella de apoyo y comparar el par aplicado con el margen de estabilidad dinámico.
- **No exigir brazos capaces de levantar 100 kg.** Transportador autónomo/elevador de perfil bajo para aparatos pesados. Minimiza tamaño, masa y coste del cuerpo principal.

### 6.4. Alternativas por comparar en CAD y banco

- Base omnidireccional baja + torso y estabilizadores: muy buena para interiores planos, peor escaleras.
- Cuadrúpedo ruedas-patas: movilidad híbrida potencialmente excelente, más complejidad/mantenimiento.
- Orugas articuladas: útiles para escombros y desniveles, riesgo de marcar suelos, maniobrabilidad fina desigual.
- Bipedo humanoide compacto: acceso a entornos humanos, pero coste energético, estabilidad y complejidad.
- Plataforma especializada + segundo robot ligero: posiblemente más robusta/compacta que un «todo en uno».

**Selección final por evidencia**: coste/Wh por tarea, tiempo de reparación, puertas, escaleras, manipulabilidad, fallos, mantenimiento, precio y seguridad. Referencias reales: [Unitree](https://www.unitree.com/), [Rainbow Robotics](https://www.rainbow-robotics.com/) y trabajos académicos de locomoción ruedas-patas. Estos productos no constituyen un prototipo ya validado de esta propuesta.

---

---

## 7. Navegación autónoma: rodear, retirar o superar obstáculos

### 7.1. Un planificador de alternativas físicas

La navegación ordinaria suele planear trayectorias para **evitar** obstáculos. Nuestro robot deberá considerar **cambios autorizados del entorno**. El proceso propuesto:

1. Reconocer obstáculos, estimar propiedades y su incertidumbre.
2. Comprobar si existe ruta alternativa (otra puerta/pasillo/acceso).
3. Comprobar si puede plegar el cuerpo y pasar por debajo o por un hueco estrecho.
4. Considerar mover o retirar el objeto, evaluando cables, líquidos, fragilidad, ocupantes, peso y suelo.
5. Considerar intervención remota por brazo extensible/cámara/minibot sin desplazar todo el cuerpo.
6. Evaluar sobrepasar por arriba **solo si hay apoyos con resistencia y fricción suficientemente verificadas**.
7. Considerar instalar una rampa/puente o pedir ayuda a otro robot.
8. Si no hay maniobra dentro de límites, solicitar ayuda humana y preservar estado seguro.

Esto corresponde a enfoques de **planificación integrada de tareas y movimientos (TAMP)**, percepción activa y navegación entre obstáculos móviles. Se usarán mapas 3D o de elevación, no solo mapas 2D de una aspiradora.

### 7.2. Ejemplo: la cama ocupa todo el paso

La IA puede pensar en escalarla, pero **la cama y especialmente su colchón no son una superficie portante validada para el robot**. La respuesta podría ser rodearla, moverla, extender una cámara, usar herramientas por encima o montar un puente temporal cuyo peso recaiga en apoyos firmes a ambos lados. Un puente de ancho/longitud suficiente podría ser voluminoso o pesado; el plan debe comparar su coste con otras opciones, no asumir que es viable.

### 7.3. Ejemplo: cae un objeto y bloquea el pasillo

Detenerse, inspeccionar si hay cables, filos, líquidos, vidrio, mascotas o carga inestable; apartarlo **de modo autorizado** a una zona segura, comprobar que no se empeora el entorno y, si procede, devolver el objeto a su lugar. No empujar ciegamente hacia escaleras o puertas.

### 7.4. Escaleras

- Detectar contrahuellas, huellas, anchuras, descansillos, peldaños abiertos, bordes, alfombras, inclinación y fricción.
- Planificar apoyos individuales de las ruedas-patas, bajar centro de masa y controlar transferencia de cargas.
- Sensores de contacto/IMU/fuerza y estimación de suelo, monitorización de deslizamiento en cada paso.
- Ensayos primero en escalera de laboratorio **con arnés de retención**, protección de caída y supervisión externa.
- Especial cuidado con escalera de caracol, peldaños estrechos, alfombras, personas y tránsito en sentido contrario.
- Si no está validada la escalera: transportar el robot con sistema externo o instalar una base por planta; nunca improvisar una subida peligrosa.

### 7.5. Rampas y puentes desplegables

La propuesta de que el robot **lleve o fabrique sus propias rampas** es útil para salvar huecos, umbrales y pequeños desniveles. No debe convertirse en único sistema para cualquier escalera.

**Ejemplo geométrico:** con una pendiente relativamente suave de 1:12, salvar **18 cm** de altura demanda **2,16 m de longitud horizontal**. Subir **2,5 m** de altura demanda **30 m** de desarrollo horizontal. Un robot puede estar diseñado para pendientes mayores, pero habrá compromisos en tracción, estabilidad, peso de rampa y espacio.

Diseñar módulos plegables de longitud acotada, con ensayos de flexión, apoyos, bloqueo, detección de contacto y límite de carga. No descargar peso sobre colchones, cristales o mobiliario sin validación estructural.

### 7.6. Herramientas auxiliares de movilidad

- Pequeña **plataforma robótica baja** que entre bajo objetos, los eleve ligeramente y los desplace sobre suelo.
- Pasarelas modulares, calzos, estabilizadores, cuñas y plataformas de trabajo autorizadas.
- Minibot o sonda flexible para huecos donde el robot principal no cabe.
- Segundo robot para transporte asistido, sujeción y rescate.

---
