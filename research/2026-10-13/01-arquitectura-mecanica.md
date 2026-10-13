# 01 — Arquitectura mecánica, equilibrio y tamaño compacto

**[P]** Contrastar físicamente la hipótesis inicial FDAA: 45 cm de ancho × 70 cm de largo × 40 cm de alto plegado, ~30–45 kg, 4 ruedas-patas, 2 brazos de 7 GDL y torso elevable. **Ninguno de estos valores está comprobado como conjunto**.

## 1. La contradicción central: pequeño en puertas, estable trabajando

**[I]** Para un empuje lateral, una aproximación cuasiestática conservadora relaciona la fuerza admisible con masa, gravedad, huella de apoyo y altura del punto de empuje. Ejemplo idealizado: con base de ancho **0,45 m**, masa **35 kg**, fuerza lateral aplicada a **1,0 m**, y centro de gravedad perfectamente centrado, la fuerza que equilibra el momento gravitatorio sobre el borde lateral es aproximadamente:

```text
M_resistente ≈ m · g · (ancho/2) = 35 · 9,81 · 0,225 = 77,3 N·m
F_umbral ideal ≈ M_resistente / h = 77,3 N a h = 1 m
```

**Esto NO es un límite seguro de operación**: no incluye aceleraciones, inclinación de suelo, patas fuera de la huella, masa transportada, posibles deslizamientos ni margen normativo. Una herramienta puede necesitar pares elevados al soltar una tuerca o mover un mueble. Se necesitan sensores de carga en patas, análisis multibody y estabilidad dinámica. **No prometer 2–4 kg por brazo sin especificar alcance, aceleración, postura y dirección.**

### Tres arquitecturas rivales para ensayar

| Alternativa | Ventaja | Coste/limitación | Recomendación |
|---|---|---|---|
| A. Base omnidireccional + estabilizadores + 2 brazos | Simplifica mecánica, control y coste del prototipo | Obstáculos y escaleras difíciles | **Primera plataforma real** para ensayos de destreza/dock |
| B. 4 ruedas-patas + 2 brazos | Rodar en llano y variar apoyo/escalón | Muchas articulaciones, integración, masa, control y consumo | **Candidato a robot final; simular antes de comprar** |
| C. Orugas/flippers + 2 brazos | Tracción y escalones determinados, bajo centro de masa | Tacto/contacto, alfombras y maniobrabilidad sobre suelos delicados | Comparador para movilidad |
| D. Bípedo humanoide | Mejor adaptación teórica a utensilios/escaleras para humanos | Estabilidad y caídas, consumo, mayor complejidad | No elegir por parecer humano |

**[D]** [Open Dynamic Robot Initiative](https://open-dynamic-robot-initiative.github.io/) proporciona actuadores abiertos, control de par, herramientas mecánicas y experimentos de cuadrúpedos; sirve como referencia de BOM y torques, **no** como prueba de que cabe el robot FDAA en 45 cm.

## 2. Un enfoque modular vence al «cuerpo que lo lleva todo»

**[P]** División de funciones:
- **Unidad móvil:** locomoción, percepción inmediata, manipuladores para cargas moderadas, baterías, emergencia.
- **Estación:** IA generalista pesada, herramienta no portátil, brazo de recambio, almacén, instrumentos, energía y logs.
- **Carro autónomo de carga:** elevación de bajo perfil, correas de sujeción diseñadas, ruedas adecuadas al suelo, sensores de carga y desplazamiento.
- **Minibot/cámara articulada:** inspección por debajo de muebles; no asumir manipulación a través de cualquier hueco.
- **Kit de puentes/rampas:** usar solamente donde dos apoyos estructurales hayan sido caracterizados.

Este desacoplamiento reduce la presión de fabricar manos capaces de levantar 100 kg. La capacidad de mover una nevera se evalúa como **operación cooperativa**, no como «fuerza de brazo».

## 3. Contrato de diseño mecánico antes de comprar actuadores

Entregables ineludibles:
1. URDF + CAD paramétrico, envolvente plegada y completa, masa estimada de **cada** motor, rueda, brazo, engranaje, batería, cable, placa y carcasa.
2. Centros de masa por postura, tensor de inercia por enlace, alcance 3D real de ambas muñecas y superposición bimanual útil.
3. Par continuo/pico, curva par-velocidad, límites térmicos de reductoras y desgaste, backdrivability/compliance.
4. Energía Wh de desplazamiento, trabajo de brazos, cálculo y standby; estimación de autonomía por tarea, no «horas» sin definir ciclo.
5. Análisis de reparto de fuerzas y **margen de vuelco** en trabajos sobre encimeras, apertura de electrodomésticos y escaleras.
6. Configuración de cableado: radios mínimos de curvatura, pasos por articulación, extracción de módulos sin romper conectores.
7. Especificación de reparabilidad externa: accesibilidad de tornillos, fijación a estación, intervención sobre robot completamente apagado.
8. FMEA mecánica: caída, pellizco, empuje, atrapamiento, rotura de carcasa o separación de rueda.
9. Tolerancias, estado térmico, deformación y vibraciones; no tratar pieza impresa como material isótropo.
10. Coste y disponibilidad de repuestos; **comparar el coste completo** de prototipo A, B y C.

## 4. Peldaños y rampas: física antes de elegir

**[D]** La investigación reciente documenta ascenso de escaleras con mecanismos auxiliares incluso para escaleras sin contrahuella [Mechatronics 2026](https://www.sciencedirect.com/science/article/pii/S0957415826001297). No generalizar a escaleras domésticas irregulares, resbaladizas o con curvas.

**[P]** Ensayar de forma incremental:
- un umbral bajo;
- escalón de altura variable;
- escalera recta con retención;
- descansillo estrecho;
- contrahuella abierta y bordes expuestos;
- escalera con objeto caído;
- escalera mojada: **solo simulación** inicialmente.

Rampa a pendiente geométrica **1:12** implica 2,16 m horizontales por 0,18 m de altura. El dato es **ejemplo geométrico**, no obligación de usar esa pendiente: medir pendiente máxima real con carga y posibilidad de frenado. Ninguna escalera se resolverá automáticamente con una rampa corta.

## 5. Interfaz y diseño para reparación mutua

**[P]** Definir módulos con:
- identificador, modelo y versión, masa, centro de gravedad;
- posiciones externas accesibles para herramienta, puntos de sujeción y secuencia de retirada;
- conexión de datos y potencia distinta físicamente o codificada, fusibles y aislamiento;
- bloqueo mecánico seguro sin alimentación, y posibilidad de desenganche por otro robot;
- sensores de vida (temperatura, corriente, vibración, error de encoder), autoprueba posrecambio;
- modos degradados permitidos, o bloqueo de movimiento.

Un robot no debe depender de sus brazos para liberarse a sí mismo. **La estación debe poder fijar un robot sin energía**, de manera que el otro manipulador tenga un marco geométrico estable.

## 6. Ensayo de decisión A/B/C

**Hipótesis refutables:** A simplifica el primer prototipo; B mejora variedad de obstáculos sin exceder huella; C aporta ventajas en peldaños. Para las tres, usar **misma carga**, mismo escenario, mismos sensores y mismo método de medición.

| Prueba | Métrica |
|---|---|
| Entrar en puerta estrecha y girar | ancho efectivo, espacio de giro y golpes |
| Empujar puerta/mueble | fuerza segura sostenida y momento restante |
| Brazo a máxima extensión | desviación del TCP y oscilación de base |
| Subir escalón con carga | contactos fallidos, abortos, vuelco y energía |
| Transporte a taller | masa total, ruido, protección del suelo |
| Reparación de una pata/rueda | tiempo, herramientas y necesidad de ayuda |

**Resultado esperado:** decisión de arquitectura basada en pruebas; si la envolvente deseada no cabe, **se revisa la envolvente**, nunca se falsifican capacidades.

**Referencias:** [ODRI](https://open-dynamic-robot-initiative.github.io/), [MuJoCo/MJX](https://github.com/google-deepmind/mujoco/blob/main/doc/mjx.rst), [Drake](https://github.com/RobotLocomotion/drake), [Mechatronics 2026](https://www.sciencedirect.com/science/article/pii/S0957415826001297), [NIST mobile manipulation](https://www.nist.gov/programs-projects/grasping-manipulation-and-contact-safety-performance-robotic-systems).
