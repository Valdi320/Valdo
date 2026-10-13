# Preguntas abiertas y próximos pasos

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 23. Preguntas de investigación pendientes, con prioridad

1. **¿Qué dimensiones/peso son mecánicamente mínimos?** ¿Cabrá la versión bimanual ruedas-patas realmente en 45×70×40 cm?
2. ¿Es mejor ruedas-patas o **robot omnidireccional + vehículo de escaleras** para viviendas comunes?
3. ¿Cómo medir de forma fiable resistencia y fricción de una cama, una rampa o una tabla **antes de cruzarla**?
4. ¿Cómo recuperar tolerancias y parámetros CAD sin inventarlos a partir de una malla ruidosa?
5. ¿Cuál es la mezcla adecuada de modelo generalista, VLA, control clásico, tacto y simulación con **16 GB reales**?
6. ¿Qué diez o veinte herramientas cubren la mayoría de reparaciones benignas en una casa?
7. ¿Cómo diseñar una operación de desmontaje general cuando no hay manual, sin dañar piezas ocultas?
8. ¿Cuándo es óptimo fabricar una pieza, comprarla o pedir un servicio profesional?
9. ¿Qué procesos de reciclaje/materiales realmente pueden mantenerse a escala doméstica con emisiones/costes aceptables?
10. ¿Cómo reparar a ambos robots si fallan simultáneamente, o si la estación queda sin energía?
11. ¿Qué tareas pueden certificarse para plena autonomía sin vigilancia? ¿Cuáles nunca deberían confiarse a un robot doméstico generalista?
12. ¿Qué significa «equivalencia» de un objeto fabricado: forma, carga, seguridad, aislamiento, fatiga, vida útil, consumo?
13. ¿Cómo evitar dependencia de proveedores en motores, baterías, sensores y semiconductores que la microfábrica no pueda construir?
14. ¿Cómo probar que el sistema funciona en **otra vivienda** diferente de donde se ha entrenado?

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
