# Hoja de ruta, aceptación e hitos

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 17. Hoja de ruta de implementación (etapas con puertas de aceptación)

### F0. Diseño y pruebas de escritorio — primero, sin comprar un robot caro

- [ ] Crear una **lista priorizada de 30–50 tareas** domésticas, riesgos, beneficios, herramientas y entornos.
- [ ] Identificar 10 tareas de primer alto retorno: p. ej., desmontar una carcasa inocua, cambiar un tornillo, abrir un cajón, cambiar una pieza impresa, detectar un obstáculo, acoplarse, etc.
- [ ] Dibujar diagrama mecánico/software/seguridad, documentar protocolos y contratos de datos.
- [ ] Simular brazo y chasis con CAD/Drake; comprobar volumen interno real, pares, estabilidad y centro de gravedad.
- [ ] Comparar ruedas-patas, omnidireccional y orugas con los mismos escenarios y criterios.
- [ ] Definir plan de ensayos reproducibles, calibración y FMEA.

**Cierre:** arquitectura revisada, BOM preliminar con supuestos, simulaciones y lista de riesgos sin tareas físicas de alto peligro.

### F1. Primer «descompilador físico» útil: escanear y fabricar una pieza

- [ ] Capturar **5 piezas mecánicas pequeñas no críticas**, con patrones de escala/calibración.
- [ ] Obtener malla y **CAD paramétrico real**, cotas, incertidumbres y enlace a medición original.
- [ ] Fabricar la réplica, medir y comprobar que encaja.
- [ ] Iterar automáticamente una modificación de geometría tras un fallo de ajuste.
- [ ] Utilizar una IA local que coordine escaneo, FreeCAD/CadQuery e informe, con supervisión.

**Cierre:** pieza reconstruida, fabricada, medida y corregida con resultados reproducibles (no solo foto).

### F2. Primer sistema de manipulación + docking autónomo

- [ ] Brazos de prototipo accesibles como **SO-101**, cámara, sensores sencillos y soporte fijo.
- [ ] Plataforma móvil segura de primer ensayo, mapa y retorno a dock con AprilTag.
- [ ] Validar contactos y corriente, temperatura y desconexión segura.
- [ ] **100 acoplamientos** bajo condiciones documentadas, con fallos contabilizados; ampliar gradualmente a base movida y obstáculos.
- [ ] Cambio automático de herramienta, con calibración y validación por visión/tacto.

**Cierre:** navegación → docking → confirmación de carga repetible y cambio de herramienta seguro.

### F3. Estación de inspección y cambio automático de un módulo

- [ ] Diseñar pieza o articulación de baja energía con **fallo inyectable** y tornillería accesible.
- [ ] Base inmoviliza, inspecciona, diagnostica y sustituye módulo mediante brazo externo.
- [ ] Ejecutar autoensayo y comparar antes/después.
- [ ] Fallo de Wi-Fi/GPU durante el proceso: sistema conserva seguridad y posibilidad de recuperación.

**Cierre:** una reparación real de un módulo de ensayo sin intervención manual, con expediente completo.

### F4. Dos robots: reparar al que no puede ayudarse

- [ ] Dos manipuladores/plataformas de módulos compatibles.
- [ ] Robot A sustituye un módulo de B **apagado**; ejecutar prueba funcional.
- [ ] Repetir B reparando A.
- [ ] Añadir escenarios de rescate desde otra habitación y estación inaccesible.
- [ ] Documentar un modo de fallo común y su mitigación.

**Cierre:** reparación recíproca con roles intercambiables, incluidos receptores inmovilizados.

### F5. Locomoción para vivienda real

- [ ] Construir prototipo móvil seleccionado por ensayos previos.
- [ ] Validar paso por puertas y posturas bajo muebles.
- [ ] Esquivar, apartar y luego devolver un obstáculo sin dañar nada.
- [ ] Superar un escalón y una escalera de ensayo **con protección de caída**.
- [ ] Demostrar rechazo explícito de una superficie portante incierta (colchón).
- [ ] Desplegar un puente sobre soportes medidos y cruzar con margen.
- [ ] Cooperación con carretilla elevadora baja para objeto pesado.

**Cierre:** movilidad robusta en escenarios declarados, con abortos seguros, fallos registrados y sin prometer universalidad.

### F6. Reparación integral de aparato benigno

- [ ] Manual/diseño conocido de aparato seguro y desmontable.
- [ ] Diagnóstico verificable de un fallo controlado.
- [ ] Desmontaje, cambio, reensamblaje, pruebas y colocación original.
- [ ] Operación de extracción/recolocación en una **maqueta de electrodoméstico** sobre plataforma de carga.
- [ ] Después de ensayos de seguridad, ampliar a aparatos reales permitidos y con supervisión.

**Cierre:** ciclo completo documentado desde el acceso al aparato hasta su devolución funcional.

### F7. Materiales circulares y fabricación ampliada

- [ ] Seleccionar pocas familias seguras y fácilmente separables.
- [ ] Ensayar reciclado en varios ciclos y propiedades resultantes.
- [ ] Evaluar celulosa/lignina/PHA como posibles líneas de mejora; estudiar proveedores, procesos y sostenibilidad real.
- [ ] Diseñar piezas para desensamblaje por robots y archivo CAD/BOM abierto.
- [ ] Incorporar metrología, ensayos y costes de ciclo de vida.

**Cierre:** materiales reprocesados con trazabilidad y propiedades medidas para usos concretos.

### F8. Integración abierta y verificada

- [ ] IA local, fabricación, percepción, robot A/B, base-taller y gemelos digitales integrados.
- [ ] Demostración **sin cortes ni edición de fallos** de reparación segura de principio a fin.
- [ ] Revisión de riesgos/conformidad, privacidad y consumibles.
- [ ] Repositorio abierto de hardware, software, documentación y experimentos; publicación de métricas incluso cuando no se alcanza el objetivo.

---

---

## 18. Métricas e indicadores que impedirán autoengañarnos

| Indicador | Cómo medirlo |
|---|---|
| Precisión de escaneo | diferencia vs piezas patrón calibradas, por tamaño/material |
| Calidad del CAD | editabilidad paramétrica, restricciones y fidelidad, no solo malla |
| Equivalencia del repuesto | cotas, encaje y ensayos mecánicos pertinentes |
| Manipulación | tasa de éxito, daño al objeto, fuerzas máximas, tiempo y recuperación |
| Docking | 100+ intentos, éxito/tiempo, corriente confirmada, fallo y repetición |
| Movilidad | caída, deslizamiento, abortos, tiempo, energía, rescates y daños |
| Reparación integral | desmontar + cambiar + probar + montar + recolocar |
| Reparación mutua | éxito A→B y B→A, receptor apagado, pruebas posteriores |
| Fallos comunes | capacidad de parar, recuperación y rescate sin LLM/conexión |
| Uso offline | funciones disponibles sin Internet y seguridad ante pérdida de red |
| IA local | VRAM pico, latencia end-to-end, fallos y replanificaciones |
| Economía | coste BOM, energía Wh/tarea, consumibles, mantenimiento y repuestos |
| Circularidad | pureza de separación, calidad tras N ciclos, huella y vida útil |
| Seguridad | respuesta E-stop, control fuerzas, distancia personas, auditoría |

**Banco de escenarios**: pasillo libre; puerta estrecha; silla caída; objeto conectado a cable; suelo mojado; gato/persona cerca; cama bloqueando el único camino; hueco bajo mueble; escalón; escalera con descansillo; tramo de caracol; rampa modular; lavadora encastrada simulada; vidrio frágil de placa; nevera pesada de ensayo; dock movido; batería baja; sensores sucios; cámara desconectada; un brazo averiado; ambos robots averiados; estación apagada; fallo de fabricación de una pieza; modelo de IA que propone una acción insegura.

**Criterio universal de aceptación:** repetir ensayos con un entorno distinto al entrenado y **contabilizar todos los intentos y abortos**. Una demo que solo muestra aciertos no valida un producto generalista.

---

---

## 24. Próximo paso de máximo retorno cuando se decida empezar

**NO construir inmediatamente un humanoide completo.** Demostrar una cadena autosuficiente, económica y verificable:

1. Tomar una pequeña pieza mecánica sin riesgo.
2. Escanearla con cámara/escáner calibrado.
3. Generar CAD **paramétrico editable** con una IA local que utilice herramientas CAD reales.
4. Imprimirla o fabricarla, comprobar medidas y corregir el diseño.
5. Utilizar un brazo sencillo y una cámara táctil/visual para sustituirla en un módulo de ensayo de baja energía.
6. Utilizar un robot móvil sencillo que **vuelva a un dock con AprilTag**, valide carga y ejecute autodiagnóstico.
7. Introducir un fallo conocido y demostrar que un segundo brazo o la estación puede reparar el módulo.
8. Publicar el expediente completo: costes, errores, tiempo, energía, tasas de éxito, componentes y código.

Este prototipo compacto contiene **todos los principios de la fábrica autónoma** sin exigir resolver desde el principio locomoción en escaleras, reparaciones de alto riesgo, materiales experimentales o una cadena industrial de chips.

> **Síntesis final:** una IA local que sabe usar herramientas de ingeniería, dos robots compactos que pueden asistirse y repararse, una base-taller de carga/diagnóstico, un descompilador digital y físico, y una microfábrica multimaterial cada vez más circular. La universalidad no se proclama: **se alcanza por iteraciones medibles, verificación y diseño seguro.**
