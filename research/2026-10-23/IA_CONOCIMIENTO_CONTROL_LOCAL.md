# IA local, conocimiento y control sin nube · 23/10/2026

**Estado:** revisión documental, observación local de solo lectura y escenarios elegidos. Sin instalación, nuevo servicio, cambio de modelos o ensayo de inferencia. [D] documentado; [O] observado; [I] inferencia; [P] propuesta; [A] pendiente. Fuentes numeradas en FUENTES.md y [parámetros guardados](datos/ia_control_local_2026-10-23.json).

## 1. Decisión provisional: separar control cotidiano y asesoramiento

**[P]** La vivienda propuesta tendría tres niveles, con funciones distintas:

| Nivel | Función | Dependencia que se pretende evitar |
|---|---|---|
| Mandos y protecciones del equipo | Operación básica, límites físicos y posibilidad de intervención | No depender del lenguaje, internet o servidor central para una función esencial |
| Control y registro local | Reglas acotadas, sensores, estados y consulta doméstica | No exigir una GPU encendida para cada lectura o acción |
| IA bajo demanda | Consultar manuales, explicar datos, comparar hipótesis y ayudar con diseño | No convertir respuestas plausibles en órdenes o medidas verificadas |

Es una arquitectura de estudio, no un sistema instalado. Las protecciones y la intervención manual dependen del aparato real; no se demuestra seguridad de ningún equipo por esta tabla. No se propone sustituir sus protecciones certificadas por software propio.

**[I]** La ventaja práctica del software local puede llegar antes que la fabricación doméstica de chips: conservar datos, elegir programas y eliminar una API obligatoria. Eso reduce dependencia comercial, pero aún requiere electricidad, almacenamiento y repuestos industriales.

## 2. Reutilizar lo existente antes de comprar otro ordenador

**[O]** La consulta local confirmó una GPU de clase 16 GB, memoria de sistema de clase 24 GB y un proceso denominado llama-server. También se leyó el llamador existente de IA para distinguir configuración actual de documentos históricos. No se lanza una consulta ni se altera ese flujo; observar el nombre de un proceso no demuestra el modelo cargado, su rendimiento o que una reparación técnica vaya a ser correcta.

**[A]** No hay en esta entrega una medida nueva de consumo en enchufe, latencia, tasa de respuestas aceptadas, memoria máxima o tiempo de revisión humana. El límite de potencia anunciado por la GPU no es la potencia del PC completo ni su consumo efectivo. Los detalles del ordenador, rutas y configuración privada no se copian al repositorio público.

**[P]** Antes de recomendar RAM, GPU u otro servidor, comparar el equipo actual en tareas delimitadas cuando la máquina compartida lo permita: localizar datos en un manual, explicar una medición, detectar un dato ausente y generar un diseño no crítico comprobable. Medir trabajo útil, errores y revisión, no únicamente palabras por segundo. Las reglas de máquina siguen vigentes; esta entrega no ejecuta tests o bancos.

## 3. Qué partes del software son abiertas y cuáles no prueban cierre de la cadena

| Pieza documental | Licencia o evidencia consultada | Límite de la conclusión |
|---|---|---|
| llama.cpp | MIT [5] | Abre el motor, no el ordenador ni todos los modelos compatibles |
| Qwen3-8B y GGUF oficial | Apache-2.0 en las fichas [6,118] | Pesos reutilizables no equivalen por sí solos a poder reproducir todo el entrenamiento |
| Home Assistant Core | Apache-2.0 [119] | La licencia de Core no abre automáticamente cada aparato o servicio integrado |
| ESPHome | Runtime C++ GPLv3; Python y otras partes MIT [123] | Revisar dependencias y placa elegida; no atribuir MIT a todo el firmware |
| Kiwix tools | GPL-3.0 [127] | El lector y el contenido que se consulta tienen derechos distintos |
| restic | BSD 2-Clause [129] | Un programa de copias no conserva físicamente los soportes o sus claves |

**[D]** Qwen3-8B declara 8,2 mil millones de parámetros. [6] Su distribución oficial GGUF muestra el archivo Q4_K_M de **5,03 GB**. [118] **[I]** Esa cifra es tamaño de archivo, no memoria completa en ejecución: contexto, cachés y otros procesos también cuentan. No se descargó ni cargó el modelo aquí. Se usa como referencia verificable, no como ganador actual o sustitución de los modelos del flujo vigente.

**[P]** Elegir modelos por fidelidad al manual, claridad sobre incertidumbre y capacidad de pedir la medición que falta. Conservar la revisión exacta, licencia, motor, parámetros, instrucciones y documentación utilizada. Cuantizar o ampliar contexto puede cambiar los resultados; no se presume calidad equivalente porque el archivo quepa.

## 4. «Local» puede esconder dependencias de internet

**[D]** ESPHome documenta que su interfaz web usa recursos externos y permite incluir JavaScript local mediante la opción correspondiente, que en la documentación estable consultada no está activada por defecto. [121] Su API también contempla reinicio si no se conecta un cliente autenticado durante el intervalo configurado. [122]

**[I/P]** No basta con comprobar que responde dentro de la Wi-Fi cuando internet funciona. Habría que verificar la interfaz desde un navegador sin caché, con conexión exterior ausente, y revisar qué ocurre cuando falta Home Assistant. El comportamiento de reinicio y el estado de las salidas deben comprobarse por dispositivo; no se cambia aquí ninguna configuración ni se recomienda desactivar mecanismos sin evaluar su función.

**[D]** Home Assistant presenta la integración Ollama como conversación con un servidor local, pero mantiene el control de dispositivos como experimental. Permite limitar las entidades expuestas y exige soporte de herramientas del modelo. [124] **[P]** Empezar por consulta y explicación; habilitar acciones únicamente cuando la tarea y sus consecuencias estén acotadas y comprobadas. Una respuesta o una herramienta emitida no acredita que el mundo físico haya quedado en el estado esperado.

**[A]** No se ha comprobado compatibilidad directa entre el servidor instalado y esa integración. Tener una API de conversación no garantiza que implemente el protocolo que espera cada cliente. No se añade otra plataforma, trabajador o bucle para sustituir el flujo existente.

## 5. Consumo: cuánto cambia dejar la IA funcionando todo el día

**[D]** Como referencia de control doméstico, Home Assistant Green anuncia consumo de unos **1,7 W en reposo y 3 W con carga a 12 V**. [120] Es información del fabricante, no medida propia en enchufe; no incorpora necesariamente los demás equipos y pérdidas de la instalación.

**[P] Escenarios elegidos:** potencia constante y horas indicadas. Los 5, 80 y 200 W son parámetros para explorar escala, no consumo de una red o PC medidos. Fórmula: **kWh/día = W × horas / 1.000**. No se dimensiona de nuevo el sistema solar a partir de ellos.

| Escenario | Potencia elegida | Horas diarias | Energía diaria | Energía anual, 365 días |
|---|---:|---:|---:|---:|
| Control de referencia | 3 W | 24 | 0,072 kWh | 26,28 kWh |
| Red local de referencia | 5 W | 24 | 0,120 kWh | 43,8 kWh |
| PC de referencia continuo | 80 W | 24 | 1,920 kWh | 700,8 kWh |
| PC de referencia en carga continua | 200 W | 24 | 4,800 kWh | 1.752 kWh |
| PC de referencia una hora | 200 W | 1 | 0,200 kWh | 73 kWh |
| PC de referencia dos horas | 200 W | 2 | 0,400 kWh | 146 kWh |

**[I]** Con control y red de esos escenarios, el caso de PC a 200 W una hora sumaría **0,392 kWh/día**; el de 24 horas, **4,992 kWh/día**. El primer caso supone PC sin consumo durante las horas restantes: no describe reposo, espera de red o arranque reales. Tampoco se supone que el mismo trabajo pueda comprimirse de 24 a una hora.

**[P]** Medir antes de elegir entre un único PC o un controlador separado: potencia en enchufe, horas efectivas, cargas simultáneas, consumo durante espera y fiabilidad. Eliminar cuotas no hace gratuita la energía; generación, acumulación y reposición siguen en el balance. No se ha demostrado suministro solar continuo de ninguno de estos casos.

## 6. Referencias de hardware: apertura, utilidad y precio son preguntas distintas

**[D]** Green muestra **179 € de precio recomendado europeo con impuestos aplicables**, no oferta entregada. Requiere internet para la configuración inicial según su página, tiene 4 GB de RAM y 32 GB eMMC. [120] **[I/A]** Es una referencia de controlador de bajo consumo, no elección para un LLM de 8B ni evidencia de que podamos fabricar toda su placa. La documentación de recursos revisada no permitió acreditar aquí una licencia del diseño completo para reproducir Green. [133] No se deduce que sea cerrado solo por esa ausencia de verificación.

**[D]** Olimex ofrece TERES-A64-WHITE como kit modular con 2 GB RAM y 16 GB eMMC, anunciado a **240 €**. [131] El importe final con impuestos y envío a destino queda pendiente; no se pasó por compra. [132] La carpeta de hardware enlazada rechazó el acceso: no se eludió y no se acredita auditoría completa de archivos/licencia por versión.

**[I]** Ese kit puede interesar por documentación y montaje, pero 2 GB no justifican elegirlo para el modelo de referencia cuyo archivo ocupa 5,03 GB, además del sistema. No se afirma que no pueda ejecutar ningún modelo pequeño: esa sería otra selección y evaluación. Una carcasa reparable o una placa documentada no fabrican el procesador, pantalla, memoria o batería.

**[D]** MNT publica documentación de hardware y ejemplos de modificación, con diseño orientado a reparación y componentes reemplazables. [130] **[A]** Se deja como familia candidata: quedan sin cerrar configuración, precio final, licencias por archivo y rendimiento de modelos en esta entrega. Sus declaraciones no acreditan que cada componente industrial pueda reproducirse en un hogar.

**[P]** Mantener el PC existente como primera referencia de asesoramiento y evaluar controlador aparte solo si ahorra energía o mejora continuidad de forma medida. Ninguno de estos aparatos se compra ahora ni se considera inversión que elimine repuestos para siempre.

## 7. Biblioteca y recuperación: autonomía después de un fallo

**[D]** Kiwix tools ofrece búsqueda y servicio local de archivos ZIM. [127] **[P]** Una biblioteca propia debería incluir manuales de los equipos elegidos, planos, despieces, fichas de material, documentación de configuración y registros de reparación. Documentos y archivos deben estar descargados lícitamente y en formatos legibles; el permiso del lector no autoriza publicar manuales de terceros en GitHub.

**[I]** Recuperación de información no es garantía de verdad: una IA puede citar un apartado incorrecto o mezclar versiones. La interfaz propuesta deberá enseñar fuente, revisión, unidad y fragmento pertinente; una medida propia y una afirmación del manual se registrarán por separado. Mantener búsqueda textual y lectura directa permite consultar aunque el modelo no esté disponible.

**[D]** Home Assistant documenta copias y migración, pero una copia cifrada necesita su clave; el kit de emergencia debe conservarse fuera de la propia instancia. Una clave nueva no abre las copias de la antigua. [125,126] restic documenta copias en almacenamiento local y opciones de integridad/restauración. [128] **[P]** No confiar en que «se hizo backup»: comprobar que se recuperan archivos y configuración en un soporte sustituto, incluyendo dependencias necesarias para reinstalar sin internet.

**[P]** Guardar por separado medios de recuperación, claves, binarios/versiones y fuentes necesarias; documentar licencias y compatibilidad. No se presupone que una copia de Home Assistant contenga todos los paquetes o imágenes necesarios para una reinstalación completamente desconectada. Las credenciales y claves no se incorporarán a la parte pública del estudio.

**[A]** No se ha creado una biblioteca completa, descargado modelos, configurado copias o probado restauración en este avance. La capacidad, número de soportes y precio quedarán ligados al inventario real; no se ofrece una cifra total inventada. Un disco también envejece y requiere reposición o migración.

## 8. Qué podemos mejorar y qué evidencia falta

| Mejora propuesta | Evidencia que permitiría aceptarla | Estado |
|---|---|---|
| Manuales consultables sin nube | Búsqueda y lectura tras arranque sin conexión exterior | No ensayado |
| Asesoramiento local con fuentes | Respuestas correctas y trazables en tareas no vistas, errores registrados | No ensayado en esta entrega |
| Control local sin servidor de IA | Función prevista conservada al apagar IA, con intervención manual disponible | No instalado |
| Tolerancia a falta de red/servidor | Estados y recuperación comprobados por dispositivo | No ensayado |
| Recuperación del almacenamiento | Restauración completa y archivos utilizables en soporte sustituto | No ensayado |
| Ventaja energética | Trabajo útil y consumo total medidos frente a alternativa | Solo escenarios |
| Reparabilidad del hardware | Diagnóstico, acceso y sustitución compatibles, documentación y repuestos | Parcial documental |

**[P]** Priorizar estas mejoras antes de ampliar autonomía de acciones o comprar más cómputo. El modelo debe poder expresar qué dato falta; la IA no aprobará por sí sola la potabilidad, capacidad de una batería o resistencia de una pieza porque su explicación resulte convincente.

**[I/A]** Podemos reducir ya dependencia de suscripciones y de una nube para funciones seleccionadas. No hay evidencia aquí de ordenador moderno reproducible íntegramente con materias primas locales, ni plazo defendible para lograrlo. Conservar software y diseños permite continuar si cambia un proveedor, pero no crea un suministro físico de componentes.

**Siguiente bloque:** integrar los subsistemas estudiados en escenarios de vivienda y costes de ciclo de vida, identificando entradas materiales, mantenimiento y gastos que impedirían el cero real. La meta completa sigue abierta; los escenarios documentales no sustituyen una instalación o funcionamiento comprobados.
