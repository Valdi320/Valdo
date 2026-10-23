# Almacenamiento de calor y reducción de batería eléctrica

Consulta del 23/10/2026. Se compara una función térmica con distintas rutas de generación y almacenamiento para reducir reposiciones y compras externas manteniendo comodidad. [D] dato documentado; [I] inferencia; [P] escenario o propuesta; [A] pendiente. [Datos y fórmulas](datos/calor_almacenamiento_2026-10-23.json).

**Decisión provisional:** estudiar primero aislamiento y demanda; después, acumulación de agua con componentes sustituibles y producción en horas solares. Guardar calor puede reducir batería eléctrica, pero no siempre reduce energía. Un sistema compacto de cambio de fase solo justificaría la excepción a la prioridad abierta si demuestra una ventaja necesaria y un coste de dependencia aceptable. No se ha seleccionado una compra ni un diseño listo para instalar.

## Qué servicio puede sustituir el calor almacenado

**[I]** Agua caliente y calefacción necesitan energía térmica; el ordenador, luces y motores necesitan electricidad. Un acumulador térmico no sustituye directamente la batería que mantiene funcionando esos aparatos. Su aportación sería evitar que ciertos usos térmicos nocturnos consuman almacenamiento eléctrico, con generación y disponibilidad suficientes durante el día.

**[D]** IDAE destaca la importancia del aislamiento de la vivienda, acumuladores y tuberías para reducir demanda y pérdidas. [181] **[I]** El aislamiento evita parte del trabajo de generar y almacenar; el acumulador desplaza el momento de suministro. No son ahorros que puedan sumarse sin conocer la vivienda y los servicios considerados.

**[P]** Prioridades para una futura finca: demanda térmica y temperaturas de confort; recorridos cortos del agua; aislamiento; fuente de calor; almacenamiento útil; control y recuperación ante avería. Una casa que conserva el calor necesita menos infraestructura para mantener la misma temperatura, aunque sigan pendientes ventilación, humedad y verano. No se propone sustituir ventilación necesaria por cerrar indiscriminadamente las entradas de aire.

## Cuánta energía cabe en agua

**[P]** Aproximación de calor sensible: Q = m × c × ΔT / 3.600, usando densidad de agua de 1 kg/L y calor específico constante de 4,18 kJ/(kg·K). Son aproximaciones para comparar escalas; no consignas sanitarias o de presión. La energía realmente entregable depende de temperaturas, estratificación, intercambiador y pérdidas.

| Agua | Energía para un salto de 20 K | Energía para un salto de 40 K | Masa de agua aproximada |
|---|---:|---:|---:|
| 50 L | 1,161 kWh térmicos | 2,322 kWh térmicos | 50 kg |
| 100 L | 2,322 kWh térmicos | 4,644 kWh térmicos | 100 kg |
| 200 L | 4,644 kWh térmicos | 9,289 kWh térmicos | 200 kg |
| 500 L | 11,611 kWh térmicos | 23,222 kWh térmicos | 500 kg |

**[I]** Estos kWh térmicos no equivalen a capacidad de una batería eléctrica utilizable para cualquier aparato. Los litros tampoco incluyen masa del depósito, aislamiento o accesorios. Vaciar un recipiente facilita trasladarlo, pero siguen importando tamaño, peso en vacío y conexiones. Para almacenamiento doméstico de esta escala hace falta logística distinta de transportar un equipo al cuerpo o en moto.

**[P]** El escenario anterior de calefacción de 20 kWh térmicos diarios era una demanda elegida, no medida. Un depósito de 500 L con salto aprovechable de 40 K almacenaría idealmente una cantidad similar a algo más de ese día, antes de pérdidas. No resolvería por sí solo una semana invernal sin generación.

## Las pérdidas pueden cambiar la decisión

**[P]** Se modela un depósito técnico de 100 L como un solo volumen a temperatura uniforme, sin extracción, sin recalentamiento y con ambiente constante de 20 °C. Comienza a 60 °C. Su conductancia térmica total UA se elige en 0,5, 1 o 2 W/K; incluye el efecto global de pérdidas, sin atribuirla a un producto. Capacidad térmica C = 0,1161 kWh/K.

La temperatura se calcula con T(t) = Ta + (T0 − Ta) × exp(−UA × t/C), usando UA en kW/K y t en horas. Para comparar servicio se elige un umbral técnico de 40 °C: Q disponible = C × máximo(T − 40, 0). Este umbral no convierte el modelo en suministro de agua potable ni en temperatura recomendada de acumulación sanitaria.

| UA elegido | Espera | Temperatura calculada | Calor perdido desde el inicio | Calor por encima del umbral técnico de 40 °C |
|---|---:|---:|---:|---:|
| 0,5 W/K | 12 h | 57,99 °C | 0,234 kWh | 2,088 kWh |
| 1 W/K | 12 h | 56,07 °C | 0,456 kWh | 1,866 kWh |
| 2 W/K | 12 h | 52,53 °C | 0,867 kWh | 1,455 kWh |
| 0,5 W/K | 24 h | 56,07 °C | 0,456 kWh | 1,866 kWh |
| 1 W/K | 24 h | 52,53 °C | 0,867 kWh | 1,455 kWh |
| 2 W/K | 24 h | 46,46 °C | 1,573 kWh | 0,750 kWh |
| 0,5 W/K | 72 h | 49,34 °C | 1,238 kWh | 1,084 kWh |
| 1 W/K | 72 h | 41,52 °C | 2,146 kWh | 0,176 kWh |
| 2 W/K | 72 h | 31,57 °C | 3,301 kWh | 0 kWh |

**[I]** Sigue quedando calor respecto al ambiente en la última fila, pero ya no supera el umbral elegido. Por eso contar todo el calor almacenado como servicio útil exageraría la autonomía. Este modelo no representa estratificación, extracciones, clima variable, puentes térmicos individuales o un ciclo real de agua caliente. Su función es mostrar sensibilidad y qué habría que medir.

**[D]** Las recomendaciones domiciliarias de la Generalitat Valenciana sobre legionela señalan acumulación sanitaria a temperatura igual o superior a 60 °C y mantenimiento. Solo se accedió al contenido indexado; la apertura directa quedó restringida. [182] **[I]** No se adopta el enfriamiento pasivo anterior como estrategia sanitaria. Un circuito técnico y un suministro de agua de consumo necesitan diseño, separación e higiene apropiados a su función.

## Cuándo se ahorra energía además de batería

**[P]** Comparación ideal para entregar 2 kWh de calor durante la noche. Se elige rendimiento eléctrico efectivo de la ruta de batería del 90 %, incluyendo su cadena de conversión en este ejemplo. Se elige pérdida térmica de acumulación de 0,5 kWh antes de entregar el servicio. Los COP son hipótesis, no prestaciones de un equipo o garantía de que el día sea siempre mejor.

| Ruta elegida | Operación | Electricidad de entrada |
|---|---|---:|
| A | Guardar electricidad y usar resistencia ideal de noche: 2 / 0,9 | 2,222 kWh |
| B | Calentar por resistencia de día y guardar calor: 2 + 0,5 | 2,500 kWh |
| C | Guardar electricidad y usar bomba de calor nocturna con COP 2: 2 / (0,9 × 2) | 1,111 kWh |
| D | Bomba de calor diurna con COP 3 y acumular: (2 + 0,5) / 3 | 0,833 kWh |

**[I]** B evita almacenamiento eléctrico para esa función, pero aquí consume más energía que A. La ventaja de D frente a C depende, entre otras cosas, del COP elegido: no prueba que cualquier bomba de calor o depósito la consiga. No se dimensiona producción instantánea de agua sanitaria, potencia, capacidad de batería ni controles a partir de estas cuentas.

**[P]** Si las dos rutas usan la misma tecnología generadora con igual rendimiento, la acumulación térmica reduce entrada energética frente a la eléctrica cuando L < Q × (1/η − 1). Para Q = 2 kWh y η = 0,9, el umbral es **0,222 kWh de pérdida por episodio**. Se deben contabilizar también auxiliares y pérdidas no comunes. Que el calor perdido caliente una habitación solo es útil cuando coincide con demanda de calefacción; en verano puede perjudicar el confort.

**[I]** Ninguna ruta crea energía en una semana sin sol. Tampoco se traslada a estos escenarios un porcentaje de autonomía de PVGIS calculado para cargas diferentes. Un sistema real necesitaría perfiles horarios de electricidad y calor, invierno, disponibilidad de agua y condiciones de avería.

## Software abierto y límites del control

**[D]** ThermalTank es un modelo de depósito que incluye cambio de fase, con licencia BSD-3-Clause en su repositorio y registro DOE CODE 101810. [172,173] Es software científico, no un depósito fabricado ni una licencia abierta para reproducir cualquier acumulador comercial. No se instaló ni ejecutó su código; el cálculo simplificado anterior es propio y conserva sus ecuaciones y supuestos.

**[D]** PVRouter-1-phase publica firmware con licencia LGPL-2.1 y funciones de desvío hacia cargas resistivas, medida de temperatura y telemetría para Home Assistant. [174,175] **[I]** El control abierto es una aportación útil, pero no resuelve el tanque, la resistencia, el aislamiento o las protecciones. Tampoco demuestra compatibilidad con una instalación aislada: el esquema de medida de excedentes y la interacción con batería/inversor deben evaluarse para esa arquitectura.

**[P]** La mejora propia más útil sería definir una función de control con prioridades verificables: suministro esencial, disponibilidad solar, reserva eléctrica, estado térmico y recuperación manual. La IA podría ayudar a explicar y revisar datos, mientras las protecciones y límites físicos deben conservar funcionamiento independiente. No se propone puentear termostatos, limitar funciones sanitarias o adaptar directamente un firmware sin validar el sistema.

## Agua convencional y cambio de fase comercial

Referencias observadas el 23/10/2026, sin compras ni presupuesto instalado:

| Referencia | Precio mostrado | Datos relevantes | Dependencias pendientes |
|---|---:|---|---|
| EQUATION EQ2 100L, artículo 92389709 de Leroy Merlin | 209 € | La ficha declara 100 L, 1,5 kW, 24,5 kg en vacío, acero esmaltado y ánodo de magnesio; también lo llama Utilis [180] | Manual y repuestos de la referencia exacta; entrega, instalación y mantenimiento; no se acredita diseño abierto |
| Thermino 150 ePlus, Sunamp Shop / Think Renewables | 1.500 GBP sin VAT; 1.800 GBP con VAT británico anunciado | Es un acumulador de cambio de fase para agua caliente [179] | Instalación, accesorios y coste entregado/importado en España; no se convierte GBP a EUR ni se presupone identidad de MPN |

**[I]** No son productos de igual capacidad o función demostrada en condiciones idénticas. Los precios no permiten calcular un ahorro directo ni declarar vencedor. La ficha del termo anuncia disponibilidad de documentos de reparación, pero no se ha acreditado coste o plazo de cada pieza. La presencia de ánodo y resistencia obliga a estudiar mantenimiento y reposición, sin inventar un intervalo universal.

**[D]** La nota Sunamp D0089 atribuye al 150 ePlus una equivalencia de cilindro de 140 L y pérdidas de 0,67 kWh/24 h bajo su metodología. La equivalencia usa condiciones explícitas de temperaturas y utilización; no significa que contenga 150 L de agua. [176]

**[D]** El manual D0083 versión 1.8, de 13/10/2025, indica para el 150 ePlus 136 kg vacío y 140 kg lleno; “vacío” significa sin agua en el intercambiador. También declara 7 W en espera y variantes eléctricas de 2.800 o 1.800 W según prefijo de referencia. Restringe reparación por el usuario. [177]

**[I]** Compacto no equivale a ligero: ni vacío resulta un equipo portátil individual razonable. La variante de 2.800 W supera los 2.400 W continuos del inversor de referencia anterior; la de 1.800 W requeriría igualmente comprobar coincidencias y compatibilidad. No se suman automáticamente los 7 W a las pérdidas térmicas o al consumo de etiqueta sin revisar las fronteras de sus ensayos.

**[D]** Sunamp describe sus formulaciones Plentigrade como patentadas. [178] **[I]** Esto no demuestra por sí solo qué derechos siguen vigentes en España, pero tampoco aporta una licencia de reproducción abierta. Una investigación de alternativas debe estudiar formulaciones y diseños con derechos suficientes, degradación, corrosión, intercambio térmico y encapsulado; no asumir que cualquier sal reproduce el producto.

**[P]** Para aceptar este producto cerrado haría falta una limitación real de espacio, rendimiento equivalente comprobado, coste completo y una estrategia de mantenimiento compatible con la meta. Con lo revisado, su restricción de reparación es una desventaja relevante. No se ha probado una superioridad que justifique elegirlo como solución definitiva.

## Desarrollo propio con menor dependencia

**[P]** Primera comparación: conservar el mismo servicio con menos demanda, depósito de agua y piezas sustituibles, o material de cambio de fase. Para cada alternativa se documentarán función, temperatura útil, pérdidas, energía auxiliar, horas humanas, piezas consumibles y respuesta ante fallo. El diseño propio puede ser modular y publicarse con archivos editables; eso no acredita fabricar localmente el acero, aislante, sensores o elementos de protección.

**[P]** La siguiente evidencia necesaria es un inventario funcional y de materiales de una reparación doméstica o un acumulador concreto, con precios de repuestos e intervalos del fabricante. En paralelo sigue abierta la búsqueda de aislamiento local durable y herramientas de precisión: reducir demanda puede eliminar más reposiciones que añadir una máquina compleja.

**[I]** Esta comparación reduce una incertidumbre: ya no se considera que guardar calor sea universalmente más eficiente o portátil. Sigue sin haber finca, demanda medida, instalación dimensionada o gasto cero demostrado. No se han realizado modificaciones eléctricas, hidráulicas o sanitarias.
