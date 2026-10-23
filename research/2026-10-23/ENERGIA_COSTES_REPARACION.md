# Energía: coste, invierno y reparabilidad · 23/10/2026

**Estado:** comparación documental y aritmética con precios consultados; no es presupuesto final ni recomendación de compra. Complementa las simulaciones de energía, manteniendo la meta de pocas compras externas sin dar por alcanzado el coste cero. Los números entre corchetes remiten a FUENTES.md.

## 1. El tamaño de la necesidad puede dominar la compra

**[D]** IDAE explica que el rendimiento de la bomba de calor depende de condiciones y temperaturas de operación, entre otros factores. No se puede trasladar el COP de un catálogo a todas las horas de invierno. [62]

**[P] Ejemplo aritmético, sin vivienda real:** si en un día hacen falta 20 kWh de calor y suponemos un COP de 2, la calefacción requeriría 10 kWh eléctricos. Sumados a otros 5 kWh, resultarían 15 kWh eléctricos ese día. Los valores son hipótesis, no demanda medida ni rendimiento garantizado. Con resistencia ideal, esos 20 kWh de calor requerirían aproximadamente 20 kWh eléctricos en el punto de uso; no se incluyen pérdidas del sistema.

**[I]** Antes de triplicar generación o batería interesa comparar reducción de demanda térmica, temperatura de trabajo, estrategia de acumulación y mantenimiento. Un consumo constante de 5 kWh/día del estudio anterior no cubre automáticamente calefacción, agua caliente, cocina, taller e IA. La simulación de 15 kWh/día es una exploración constante, no un modelo de calefacción estacional.

**[P] Informática y fabricación:** un ordenador que consumiese 200 W durante 24 horas gastaría 4,8 kWh/día; durante ocho horas, 1,6 kWh. Es un ejemplo, no una medida del PC del propietario ni de una IA concreta. Deberíamos registrar energía por tarea aceptada y estudiar trabajo en horas solares; no asumir que inferencia local es electricidad gratuita.

## 2. Precios de referencia comprobados en páginas directas

Consulta: 23/10/2026. Precios públicos anunciados, sin pedido, sin fijar destino y sin confirmar disponibilidad o coste entregado. No se usa una fecha antigua de entrega de un buscador como prueba de stock.

| Referencia | Precio visible | Condiciones y límites | Fuente |
|---|---:|---|---|
| Pylontech US5000, 4,8 kWh nominales | 1.088,09 EUR | Página muestra 899,25 EUR sin IVA; el primero es el precio con impuesto mostrado. Transporte y versión entregada pendientes | [58](https://autosolar.es/baterias-litio-48v/bateria-litio-48kwh-pylontech-us5000-48v) |
| MultiPlus-II 48 V 3000 VA 35+32 A | 685 EUR | Precio anunciado por Leroy Merlin; página anuncia envío gratis. No aparece desglose de IVA en la lectura consultada: confirmar fiscalidad y destino | [59](https://www.leroymerlin.es/productos/inversor-victron-multiplus-ii-48v-3000va-35-32a-90106970.html) |
| SmartSolar MPPT 150/35 | 161,76 EUR | GeneraSolar indica IVA incluido; envío calculado en carrito y plazo anunciado de una a dos semanas | [60](https://generasolar.es/product/regulador-victron-smartsolar-mppt-150-35/) |
| Lote de siete Tensite 500 W Full Black N-Type | 644,99 EUR | Página directa muestra 533,05 EUR sin IVA; confirmar transporte y condiciones. El lote suma 3,5 kWp, sin estructura ni electrónica | [61](https://autosolar.es/panel-solar-24-voltios/pack-7-unidades-placas-solares-500w-tensite-full-black-topcon-n-type) |

Un resultado de buscador mostraba 654,31 EUR para el último lote, pero la página directa consultada mostraba 644,99 EUR. La cuenta siguiente usa esta última observación; no una oferta garantizada.

## 3. Cestas aritméticas: orden de magnitud, no kits validados

Para hacer visible qué se está sumando se propone **solo como referencia de compra** un lote de siete paneles por cada seis que se usarían, dejando uno de repuesto; dos controladores 150/35 por cada 3 kWp; un inversor 48/3000 y uno o tres módulos US5000. El número de controladores se usa para contar coste y potencia nominal agregada, no para prescribir distribución, conexión o protecciones.

**No hay esquema validado.** Faltan comprobación de cadenas con temperatura mínima, intensidad, compatibilidad, comunicaciones, configuración, mínimo de módulos admitido para cada equipo y todos los elementos de instalación. No conectar estos componentes siguiendo esta tabla.

Un límite concreto: la ficha US5000 recomienda 75 A por módulo. [56] Cuatro reguladores de 35 A pueden sumar más corriente que esa referencia; una variante de 6 kWp con un solo módulo podría requerir limitar carga, recortar captación o aumentar batería. Falta comprobar el control conjunto. El modelo SHScalc no representa por sí solo ese límite del equipo comercial.

| Referencia aproximada | Paneles comprados / considerados en uso | Batería nominal comercial | Suma de precios anunciados |
|---|---|---:|---:|
| 3 kWp con un módulo | 7 / 6 | 4,8 kWh | 2.741,60 EUR |
| 6 kWp con un módulo | 14 / 12 | 4,8 kWh | 3.710,11 EUR |
| 3 kWp con tres módulos | 7 / 6 | 14,4 kWh | 4.917,78 EUR |
| 6 kWp con tres módulos | 14 / 12 | 14,4 kWh | 5.886,29 EUR |

**[I]** Son sumas de importes publicados antes de cerrar fiscalidad y partidas. No son precios «de vivir con energía gratis», ni límites superiores de inversión. Excluyen soportes, obra, cableado, distribución, protecciones, armario/rack, interfaces, transporte aplicable, mano de obra, documentación, comprobaciones y respaldo si se requiere.

Tampoco son las baterías de 5 y 15 kWh de PVGIS. La ficha US5000 publica 4,8 kWh nominales y 4,56 kWh utilizables por módulo; tres suman 14,4 y 13,68 kWh según esas condiciones, antes de considerar nuestra reserva y conversión. [56] No trasladamos a esta cesta los porcentajes exactos de la simulación.

**[I]** En estas cantidades, pasar de 3 a 6 kWp incrementa la suma en 968,51 EUR, mientras pasar de uno a tres módulos añade 2.176,18 EUR. Esto justifica comparar las dos estrategias; no demuestra que paneles adicionales sustituyan siempre a batería ni que una instalación mayor no necesite más coste auxiliar.

## 4. Límites físicos y de funcionamiento

**[D]** El inversor de referencia entrega 2.400 W continuos a 25 °C y 2.200 W a 40 °C, aunque su denominación sea 3.000 VA; su consumo sin carga a 48 V es 11 W según la ficha. [54] **[I]** Encendido 24 horas, serían aproximadamente 0,264 kWh/día sin alimentar cargas, sin contar otros consumos. No se impone ese valor al modelo PVGIS. Cocinar y usar máquinas a la vez exige revisar picos, no solo kWh diarios.

**[D]** El MPPT 150/35 tiene potencia FV nominal de 2.000 W a 48 V, con límites adicionales de tensión e intensidad. [55] No se pueden tratar sus 150 V como margen garantizado para cualquier serie: hay que comprobar el circuito en condiciones frías. La suma de controladores no valida las conexiones.

**[D/I]** Cada US5000 de la ficha pesa 38 kg; tres son 114 kg solo en baterías. [56] La ficha comercial de los paneles considerados indica 22,5 kg y 1,909 × 1,134 m por unidad: seis sumarían 135 kg y unos 13 m² de superficie de módulo, sin estructura o separaciones. [61] Este sistema doméstico sería trasladable con logística, no un equipo para llevar al cuerpo o en la moto.

## 5. Reposición: la inversión única no lo resuelve automáticamente

**[D]** Pylontech publica vida de diseño y ciclos bajo condiciones indicadas en su ficha. Es una especificación de diseño, no prueba de duración indefinida, garantía de calendario o posibilidad de reparar cada celda. [56]

**[P] Reserva contable ilustrativa:** tres módulos al precio observado suman 3.264,27 EUR. Si se planificase volver a comprarlos al mismo precio dentro de 10, 15 o 20 años, la reserva lineal sería aproximadamente 27,20, 18,13 o 13,60 EUR/mes respectivamente. Son horizontes elegidos para comparar, **no predicciones de vida útil**; se omiten inflación, descuento, impuestos futuros y precios de sustitución. No representan todo el mantenimiento de la instalación.

**[I]** Precomprar repuestos o reservar dinero puede evitar una compra imprevista, pero no transforma la reposición en coste económico cero. No se presupone que almacenar una batería sin usar congele su envejecimiento. La investigación debe buscar sustitución de celdas, documentación y alternativas de suministro; no anunciar un equipo «para siempre».

## 6. Reparabilidad y apertura comprobadas por capa

| Caso | Qué está documentado | Qué significa para FDAA |
|---|---|---|
| MultiPlus-II / Pylontech US5000 | Los manuales restringen la intervención interna a personal cualificado o autorizado, según el producto [49,57] | Modular por fuera no equivale a reparable internamente por el propietario; no son nuestra solución abierta definitiva |
| Libre Solar MPPT 2420 HC | Fuentes y desarrollo de prototipo; salida de batería entre 10 y 32 V, para sistemas 12/24 V [21] | No es sustitución directa del regulador de un banco de 48 V; estudiar una variante distinta requeriría ingeniería y validación |
| Libre Solar BMS C1 | Fuentes de gestión de batería y cuestiones de desarrollo pendientes [22] | Línea de investigación; no resuelve fabricar celdas ni certifica una batería doméstica terminada |
| diyBMS v4, hardware revisado | Diseños KiCad publicados con CC BY-NC-SA 2.0 UK y advertencias de uso [65] | Documentación accesible con restricción comercial; no cumple la definición estricta de hardware abierto adoptada por el proyecto. No mezclar con licencia del firmware |
| foxBMS 2 | Plataforma de desarrollo: software BSD-3-Clause, hardware/documentación CC BY 4.0 [66,67] | Candidato abierto para estudiar arquitectura y diagnósticos; no es por ello batería lista, coste mínimo ni protección ya validada en nuestra vivienda |
| OpenEnergyMonitor | Hardware y software para registrar energía y temperaturas localmente [63,64] | Buena línea para medir antes de dimensionar. No hace abierto el aparato que mide ni elimina comprar sensores y componentes |

**[I]** Esta revisión no demuestra que un producto cerrado sea «muchísimo mejor» en todos los criterios. Sirve como referencia comercial y de madurez; faltaría una comparación funcional en condiciones equivalentes antes de aceptar la excepción a la prioridad abierta. No se ha hecho ingeniería inversa ni copiado firmware propietario.

## 7. Mejoras propias con mayor retorno probable

**[P]** Investigar primero una ficha por aparato con consumos, versión, manual, repuestos y modo local de funcionamiento; medir tareas útiles de ordenador y taller; registrar temperatura y demanda; estudiar ejecución diurna de cargas flexibles. No añadir automatización a un servicio esencial antes de poder operarlo y recuperarlo manualmente.

**[D]** OpenEnergyMonitor distingue medir electricidad de medir también calor para obtener rendimiento de una bomba de calor. [64] HeatpumpMonitor.org describe límites de medición y fronteras de cada instalación; sus casos reales no son automáticamente extrapolables a Zaragoza o a otra vivienda. [68]

**[P]** En almacenamiento abierto, comparar disponibilidad de componentes, posibilidad de sustituir módulos de medida y herramientas de diagnóstico antes de elegir una placa. La licencia importa si se pretende compartir mejoras, vender equipos o incorporar el diseño a otro producto. No se instala ni se construye ninguna de estas alternativas en esta campaña.

## 8. Decisión y pendientes

Se avanza desde «más batería» hacia comparar conjuntamente demanda, horario, generación, almacenamiento y reparación. La cesta comercial da una referencia parcial verificable; no cierra presupuesto ni selección de equipo. La prioridad sigue siendo arquitectura abierta, y la elección de componentes de potencia permanece sin resolver.

Pendientes energéticos: demanda real y térmica, perfiles por estación, sombreado de un emplazamiento concreto, duración de déficits y respaldo, equipos abiertos que cumplan requisitos, presupuesto instalado completo y plan de repuestos. Hay trabajo independiente posible en agua, alimentación y conservación sin esperar a conocer ya la finca; ese será el siguiente bloque documental.
