# Visión, cronología y decisiones

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 0. Resumen ejecutivo: el sistema completo

La aspiración es que una persona pueda enseñar al sistema una pieza o máquina, describir su problema o función deseada, recibir un diseño técnico editable y ver cómo un robot obtiene o fabrica las piezas necesarias, desmonta el aparato, lo repara, verifica su funcionamiento y vuelve a dejarlo en su posición original. Cuando el robot necesite mantenimiento, una **base-taller o un segundo robot** podrán encargarse de él. Todo funcionará fundamentalmente de manera local.

**Subconjuntos que deben encajar:**

1. **Descompilador digital:** análisis de software y firmware; recuperación de lógica mediante Ghidra y herramientas complementarias, con verificación diferencial.
2. **Descompilador físico:** escaneo 3D, metrología, análisis de materiales, sensores eléctricos y funcionales, reconstrucción CAD paramétrica, esquemas y modelos físicos.
3. **IA local de 16–24 GB de VRAM como referencia inicial:** planificación, herramientas, conocimiento recuperable, modelos de visión y manipulación especializados, ejecución offline, memoria verificable.
4. **Microfábrica doméstica multimaterial:** impresión 3D, acabado, ensamblaje, ensayos y recuperación de residuos; no solo extruir plástico.
5. **Materiales abiertos y de ciclo circular:** celulosa, lignina, PHA, fibras, almidón, minerales y materiales reciclados, combinados con arquitectura geométrica; sin exigir que todos sean biodegradables.
6. **Robot reparador compacto de dos brazos:** circulación autónoma, manipulación precisa y capacidad física de realizar una reparación completa, incluidos sacar y volver a meter electrodomésticos.
7. **Movilidad todoterreno doméstica:** cuatro ruedas-patas como candidato, escaleras, muebles que bloquean, rampas o puentes desplegables, obstáculos inesperados.
8. **Segundo robot cooperativo:** rescate, mantenimiento mutuo e intercambio de herramientas y módulos.
9. **Estación de carga y mantenimiento:** localización, docking, autodiagnóstico, recambios y un pequeño manipulador de reparación independiente.
10. **Seguridad, privacidad y documentación:** verificación, diseño para desmontaje, control de riesgos, medición, registro de fallos y datos locales.

**La meta no es una máquina omnisciente ni una autorreplicación perfecta.** Seguirán haciendo falta energía, materias primas, electrónica industrial, trabajos profesionales regulados y ciertos recursos externos. El éxito será aumentar progresivamente la proporción de necesidades que se pueden resolver con seguridad de forma local.

---

---

## 1. Cronología de la conversación y decisiones que deben conservarse

### 1.1. De compilar/descompilar a comprender y reconstruir

Partimos de la diferencia entre un **compilador**, que convierte fuentes de alto nivel en código ejecutable, y un **descompilador**, que intenta recuperar una representación de alto nivel desde el ejecutable. Aunque pueden compartir análisis de control y datos, representación intermedia y herramientas, no son inversos perfectos. Compilar → descompilar → compilar reiteradamente **no garantiza idempotencia, equivalencia binaria, equivalencia semántica ni un código mejor**. Hay pérdida de nombres, tipos, intención, comentarios, estructura y optimizaciones irreversibles.

La estrategia correcta es guardar el ejecutable original como referencia inmutable, recuperar funciones y relaciones, construir código mantenible y realizar **pruebas diferenciales** entre comportamientos; no repetir transformaciones esperando recuperar información perdida.

### 1.2. Referencia práctica de Ghidra y recompilación

En un trabajo distinto sobre un ejecutable ARM de Nintendo 3DS se consiguió una recompilación estática y se desarrolló una exportación masiva con Ghidra. Un estado comprobado el 13/10/2026 indicaba **23.743 funciones detectadas por Ghidra y 18.499 exportaciones satisfactorias**, mientras otro analizador proponía más entradas (algunas resultaron falsas o no concordaban). Esto demostró que la producción automática de pseudocódigo a escala es factible, pero que **exportar sin errores no equivale a comprender correctamente cada función ni a disponer de un programa de alto nivel compilable**.

Este antecedente es metodológico. La fábrica doméstica es un proyecto separado. **No se publicarán ROMs, código de juegos, firmware propietario ni otros materiales protegidos** como parte de este proyecto.

Otro referente es [Claude's C Compiler](https://github.com/anthropics/claudes-c-compiler) de Anthropic: experimento de construcción de un compilador C en Rust mediante agentes. Ilustra el valor de una orquestación rigurosa de tareas, pruebas y verificación; no demuestra que la decompilación sea universal.

### 1.3. La analogía física

Nos preguntamos si se podría desarrollar un «Ghidra de objetos reales». Un escáner 3D recupera una **superficie**; un descompilador físico verdadero debería devolver **geometría CAD editable, materiales, conexiones, funcionamiento, tolerancias, proceso de fabricación y nivel de confianza**. El campo ya dispone de piezas de la solución —fotogrametría, tomografía, espectrometría, osciloscopios, análisis CAD—, pero **no existe un dispositivo universal y portátil que lo comprenda todo**.

### 1.4. Materiales y autosuficiencia

La aspiración fue encontrar un material barato, disponible en todas partes, biodegradable, reciclable y apto para cualquier objeto. La conclusión fue preferir una **familia pequeña y compatible de materiales** y explotar también los **metamateriales geométricos**. Una misma composición puede exhibir rigidez, flexibilidad o amortiguación distintas por su arquitectura, pero esa técnica no crea por sí sola un semiconductor, un metal conductor o una batería.

### 1.5. Robots y reparación de verdad

Se añadió un robot capaz no solo de cambiar piezas sino de **acceder al objeto físicamente**, desplazar neveras/lavadoras, sacar una placa de la encimera sin romperla, desmontar, probar, montar y colocar de nuevo. Posteriormente, un segundo robot que pueda reparar al primero —y viceversa—, además de una estación-taller independiente.

### 1.6. Navegación, rampas, acoplamiento y dimensiones

El robot debe resolver camas atravesadas, objetos caídos, escaleras y lugares sin una ruta despejada. Las **rampas plegables** se aceptan como herramientas, especialmente para huecos y pequeños desniveles, pero **subir cada escalón mediante cuatro ruedas-patas** puede ser más compacto que transportar enormes rampas. Se estudiaron las funciones de retorno de un Xiaomi Robot Vacuum S12 como ejemplo de cómo combinar mapa, odometría y alineación IR. Se propuso una estación con marcadores visuales AprilTag.

La referencia dimensional inicial quedó en **45 cm de ancho × 70 cm de largo × 40 cm de alto plegado**, con torso extensible y dos brazos. **No está verificado que quepan todos los actuadores y baterías sin sacrificar fuerza, seguridad o autonomía.**

---

---

## 20. Coste, plazos y viabilidad: distinguir evidencia de pronóstico

**Hoy existen por separado:** escáneres 3D económicos, CAD abierto, impresión, brazos asequibles, robots con escaleras, SLAM, docking, análisis de software y circuitos, modelos de IA pequeños y laboratorios de materiales.

**La integración sigue siendo investigación:** reparación generalista fiable, identificación causal de averías desconocidas, manipulación bimanual fina, escaleras con carga, reparación recíproca de fallos variados, materiales locales útiles y verificación automatizada segura.

**No demostrado y muy alejado:** un dispositivo que haga ingeniería inversa no destructiva exacta de cualquier objeto o chip; una impresora casera que fabrique todos los materiales/electrónica; autorreplicación total; eliminar toda dependencia externa.

**Horizontes conversados, altamente especulativos:** más conversión escaneo→CAD durante los próximos años; sistemas domésticos multimodales más completos posiblemente en la década de 2030; autonomía generalista sin supervisión en reparaciones complejas **sin fecha creíble**. No son compromisos ni justificación para gastar dinero hoy.

**BOM antes de comprar:** separar coste de cámaras/escáner; electrónica de control y sensores; brazos/útiles; chasis/actuadores/batería; estación-taller; carro elevador; impresión/metrología; ventilación; ensayos y seguridad; repuestos y consumibles. Comparar primero prototipos de mesa en lugar de adquirir un humanoide completo.

---
