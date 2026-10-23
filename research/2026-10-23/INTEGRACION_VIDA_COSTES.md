# Integración de vida cotidiana y costes de ciclo de vida · 23/10/2026

**Estado:** integración de evidencia documental, precios observados y escenarios elegidos. No hay finca seleccionada, vivienda dimensionada, instalación completa o autonomía verificada. [D] documentado; [I] inferencia; [P] propuesta; [A] pendiente. Datos, fórmulas y referencias de origen en [JSON](datos/integracion_vida_costes_2026-10-23.json). La meta de gasto cero y fabricación propia se conserva; este documento no la redefine como tener ingresos para pagar facturas.

## 1. Qué demuestra la integración y qué sigue sin demostrar

**[I]** Los capítulos anteriores aportan componentes y funciones parciales. No se obtiene una vivienda autosuficiente simplemente sumando un sistema solar, depósitos, un huerto y una impresora. Los servicios tienen que coexistir durante el invierno, una avería y la conservación de una cosecha; también hay que mantener las máquinas que los permiten.

**[P]** Evaluar cuatro balances separados: energía por estación y hora, agua por uso y estación, comida utilizable y nutrición, y materiales/dinero/trabajo de mantenimiento. Un saldo anual positivo en uno no cancela un déficit en otro. Los ingresos por excedentes o el trueque, si se estudiaran, se registrarían como intercambios externos, no como cierre de esos balances.

**[D]** IDAE separa calefacción, refrigeración, agua caliente, cocina, iluminación/electrodomésticos y otros usos; su agregado residencial no incorpora sin más todo el transporte o actividad económica del hogar. [136] **[I]** Un consumo doméstico publicado tampoco acredita la energía de una microfábrica o de la movilidad rural.

## 2. Dos referencias nuevas de consumo y precio, sin recomendación de compra

| Aparato de referencia | Importe visible | Dato útil | Exclusiones y límites |
|---|---:|---|---|
| IKEA LAGAN 00572853, frigorífico integrado 126 L | 299 € | Declara 92 kWh/año; sin congelador en esta referencia | Requiere instalación en mueble; herrajes/elementos indicados aparte; entrega y precio final pendientes [134] |
| IKEA TILLREDA 80590155, una zona de inducción | 34,99 € | Declara 2.000 W | Precisa menaje compatible; no se ha medido consumo de una receta, reparación o vida útil [135] |

Consulta de páginas directas: 23/10/2026. Se recoge el importe mostrado, sin pedido o presupuesto instalado. EPREL está enlazado por la página del frigorífico, pero no mostró contenido legible con esta herramienta: los 92 kWh se atribuyen a la ficha comercial, no a comprobación independiente propia.

No se ha acreditado licencia abierta de diseño de estos aparatos ni superioridad frente a una alternativa abierta equivalente. Sirven para estudiar funciones y costes, sin aceptar por defecto la excepción a la prioridad abierta del proyecto. Acceso a un manual no equivale a tener planos completos y permiso para reproducirlo.

## 3. Un día de servicios parciales, con todas las hipótesis visibles

**[P]** Se construye un ejemplo aritmético para detectar omisiones. No es un consumo típico, mínimo de comodidad, selección de aparatos o presupuesto de vivienda. No incluye lavado, bombeo, ventilación, congelación, climatización o taller salvo donde se incorporan expresamente después.

| Uso | Base documental o supuesto elegido | Energía diaria del ejemplo |
|---|---|---:|
| Frigorífico | 92 kWh/año declarados / 365 [134] | 0,252 kWh |
| Cocina | 2.000 W de la referencia × 0,5 h constantes elegidas [135] | 1,000 kWh |
| Luz | 15 W × 6 h elegidos | 0,090 kWh |
| Teléfono | 25 Wh/día elegidos | 0,025 kWh |
| Red local | 5 W × 24 h elegidos | 0,120 kWh |
| Control | 3 W × 24 h elegidos | 0,072 kWh |
| PC | 200 W × 1 h elegidos; cero consumo restante en este modelo | 0,200 kWh |
| Consumo propio del inversor | 11 W sin carga × 24 h, referencia [54] | 0,264 kWh |
| **Total parcial A** | Sin ACS o calefacción | **2,023 kWh** |

**[I]** La media anual del frigorífico no representa cada día, estación o arranque. Añadir los 11 W como carga contable no modela toda la curva de pérdidas de conversión, ni sustituye su cálculo bajo carga. Tampoco se toma esta tabla para volver a aplicar pérdidas a una simulación existente sin revisar su frontera energética.

### Agua caliente y calefacción cambian el tamaño

**[D]** La guía IDAE/ASIT distingue demanda de calor del agua y consumo que incluye las pérdidas de la instalación. [137] **[P]** Para ilustrar la demanda, se eligen 50 L, densidad aproximada 1 kg/L, calor específico 4,18 kJ/(kg·K) y un salto de 30 K:

**50 × 1 × 4,18 × 30 / 3.600 = 1,742 kWh de calor.**

No es una necesidad personal ni una consigna de temperatura de depósito. Con resistencia ideal en el punto de uso se contabilizaría la misma energía eléctrica; almacenamiento, distribución y control añadirían pérdidas o consumos que aquí faltan. Otra tecnología requeriría un modelo diferente de rendimiento y operación.

**[P]** Se añade después una demanda de calefacción elegida de 20 kWh de calor/día y COP 2: 10 kWh eléctricos. No es dato de una vivienda o clima concreto ni COP garantizado. Finalmente se agrega un lote hipotético del secador ya estudiado: 650 W constantes durante 8 h = 5,2 kWh; no receta o ciclo medido. [88]

| Escenario elegido | Energía calculada |
|---|---:|
| A: servicios parciales sin agua caliente o calefacción | 2,023 kWh/día |
| B: A más calentamiento del agua elegido | 3,765 kWh/día |
| C: B más calefacción elegida | 13,765 kWh/día |
| D: C más lote hipotético de secado | 18,965 kWh en ese día |

**[I]** No se puede prometer vida cómoda con el sistema calculado para A si después se necesitan C o D. Estos días tampoco representan una serie anual: antes de dimensionar habrá que definir demanda térmica y horarios estacionales reales. Reducir pérdidas del edificio podría cambiar la solución más que una compra de batería; falta cuantificarlo en una vivienda.

## 4. Energía almacenada y potencia disponible son límites distintos

**[D/I]** La inducción de referencia declara 2.000 W y el secador 650 W: sumarían 2.650 W si coincidieran a esas potencias. [135,88] El inversor estudiado publica 2.400 W continuos a 25 °C. [54] La suma excede esa referencia en 250 W, antes de otras cargas. No es una prueba de disparo, estudio de transitorios o validación de conexión: muestra una incompatibilidad de ese caso elegido.

**[P]** Comparar separación de tareas, limitación de carga o arquitectura distinta antes de aceptar más aparatos. También hay que cubrir servicios que no puedan diferirse; un frigorífico no se convierte automáticamente en carga diurna desconectable.

**[D]** AESAN indica que la seguridad de alimentos tras un apagón depende de temperatura, alimento, tiempo y conservación; no se determina probando olor o sabor. [139] **[I]** No se propone apagar el frío durante noches o déficits solares sin comprobar conservación y respuesta a fallos. Aquí no se establece un protocolo alimentario propio.

### Qué nos dicen realmente los escenarios solares anteriores

| PVGIS ya conservado: 6 kWp, batería de modelo 15 kWh | f_e anual | f_e diciembre |
|---|---:|---:|
| Demanda constante 5 kWh/día, perfil predeterminado | 0,32 % | 1,02 % |
| Demanda constante 15 kWh/día, perfil predeterminado | 22,54 % | 57,89 % |

**[D/I]** Son resultados leídos de los JSON originales de esta campaña, con meteorología histórica 2005-2023, emplazamiento genérico y corte de descarga del modelo al 20 %. `f_e` describe días en que se alcanza el límite inferior del modelo: **no porcentaje de energía no servida ni días completos sin luz**. Véase [sensibilidad y límites](ENERGIA_SENSIBILIDAD.md).

Los casos C y D nuevos **no se simularon** con PVGIS; no se les asignan los porcentajes del caso de 15 kWh. El banco comercial de 14,4 kWh nominales tampoco equivale exactamente a la batería de modelo de 15 kWh. No se acredita continuidad de una vivienda real.

## 5. Agua, cultivo y conservación tienen que cerrar juntos

**[D/P]** Conservando los supuestos del [anexo de agua](AGUA_CAPTACION_CALIDAD.md): 100 L/día domésticos requieren 36.500 L/año. El riego elegido de 100 m² a 3 L/m² durante 90 días agrega 27.000 L: total 63.500 L. No es dosis agronómica recomendada ni consumo del propietario.

Con lluvia media de referencia de Zaragoza 1981-2010 y coeficiente elegido 0,8, una cubierta de 100 m² daría 25.760 L brutos y una de 200 m², 51.520 L. Los déficits aritméticos frente a esa demanda serían respectivamente **37.740 y 11.980 L/año**, antes de pérdidas posteriores o requisitos de calidad. Un depósito mayor no crea el agua que falta.

**[I]** Las normales de lluvia y la meteorología de PVGIS corresponden a periodos diferentes. No se suman como si fueran una simulación diaria conjunta o prueba de riesgo combinado. Tampoco se asigna ese riego a una cosecha concreta por compartir superficie de ejemplo.

**[D/I]** El ejercicio de 100 m² de patata no acreditó dieta completa: su caso intermedio da 140.800 kcal, un 19,3 % de la referencia contable elegida de 730.000 kcal/año. No es porcentaje de nutrientes, alimentación personal o autosuficiencia. La OMS distingue adecuación, balance, moderación y diversidad, además de inocuidad. [138] Producir kilos o calorías no basta para concluir cobertura alimentaria.

**[P]** Elegir fuente de agua y superficie productiva junto con dieta, trabajo y métodos de conservación. Automatizar el riego o imprimir un secador puede mejorar una tarea; no cierra por sí solo agua, nutrición, insumos y calidad de los lotes.

## 6. Dinero: subtotal de ejemplos y reposición, sin disfrazarlo de precio de una vida

**[P]** Para hacer visible la escala de algunas partidas, se suman referencias ya observadas. Es una selección contable **no validada como kit o diseño**, no presupuesto mínimo o suficiente de una casa. Mantiene las dudas de IVA/desglose, disponibilidad e instalación indicadas en cada anexo.

| Partida ilustrativa | Importe contado |
|---|---:|
| Cesta solar no validada: referencia 6 kWp y tres módulos, según anexo | 5.886,29 € |
| Nueve depósitos nominales de 1.000 L a 290 €, sin instalación | 2.610,00 € |
| Frigorífico de referencia | 299,00 € |
| Placa de inducción de referencia | 34,99 € |
| **Subtotal de esas partidas** | **8.830,28 €** |

**Fuentes:** [58-61,85,134,135]. No significa «por 8.830 € puedes mudarte y vivir sin gastos». Faltan suelo y vivienda, permisos, estructuras y protecciones, instalación, agua segura, saneamiento, calor, otros aparatos, herramientas, logística, consumibles, mantenimiento y contingencias. Los depósitos no tienen diseño hidráulico conjunto y el sistema solar no tiene esquema validado. Parte del equipo no cumple todavía nuestra aspiración de diseño abierto y reparación interna propia.

### Reposición en un horizonte elegido

**[P]** Ejercicio contable de 30 años, intervalo [0,30), sin reposición justo en el año 30. Se eligen, sin predecir vida útil: renovar las tres baterías en año 15; inversor en años 10 y 20; frigorífico en años 12 y 24. Se mantiene el mismo precio, sin inflación, financiación o descuento.

3.264,27 + 2 × 685 + 2 × 299 = **5.232,27 € de reposición parcial futura**.

Sumado al subtotal anterior: **14.062,55 €**, todavía solo por aquellas partidas iniciales y estas reposiciones elegidas. No es coste total de propiedad de una vivienda ni prueba de que esos aparatos duren hasta las fechas elegidas. Se omiten las restantes reparaciones y reposiciones, que no se suponen gratuitas.

**[D/I]** La guía solar térmica también contempla vigilancia, mantenimiento preventivo y sustitución de componentes. [137] Por tanto, cambiar electricidad por calor solar no acredita por sí solo ausencia de mantenimiento. Falta comparar diseños concretos, consumibles y trabajo.

**[I]** Una reserva o precompra podría evitar determinados pagos posteriores, pero consume capital y depende de precios, conservación y compatibilidad de repuestos. No se considera demostración de autosuficiencia material ni coste económico cero.

## 7. Cobertura del objetivo completo: qué no puede quedar fuera

| Necesidad | Evidencia disponible en esta campaña | Qué impide afirmar cobertura propia |
|---|---|---|
| Vivienda habitable | Opciones abiertas y marco urbanístico estudiados | Sin finca, edificio o situación administrativa comprobada |
| Electricidad y confort térmico | Simulaciones y referencias de equipos; cálculos parciales de calor | Sin cargas/estación/continuidad ni presupuesto instalado de vivienda real |
| Agua segura y saneamiento | Balances, calidad y vías de gestión documentadas | Sin fuente analizada o sistema completo autorizado y comprobado |
| Alimentación | Escenarios limitados, conservación y herramientas | Sin dieta, cosechas, fertilidad, reservas o trabajo validados |
| Ropa, calzado e higiene | Recursos abiertos parciales; fabricación por materiales descrita | Falta investigación específica de suministro, desgaste y mantenimiento cotidiano |
| Salud, atención dental y contingencias | No hay servicio propio acreditado | No se presupone sustituible por una IA, impresora o botiquín |
| Movilidad y acceso | Se identificó dependencia logística | Sin balance de transporte, energía, repuestos o acceso a servicios |
| Informática y conocimiento | Pila local documentada y hardware observado | Sin continuidad probada tras fallo, reposición de chips o soportes |
| Reparación y fabricación | Diseños y procesos parciales, referencias económicas | Sin cadena completa de materiales, herramientas y verificación |
| Obligaciones y servicios comunes | IBI, residuos e IMAR revisados en sus condiciones | Sin municipio/finca/liquidación concreta; no existe exención por asumir autosuficiencia |

**[I/A]** No se convierte esta tabla en un porcentaje de «vida resuelta»: las necesidades no tienen peso equivalente y ninguna fila acredita un sistema propio completo. El 67 % del catálogo inicial solo describía su selección de proyectos. Tampoco basta que el gasto medio sea pequeño para llamarlo cero.

## 8. Plan de avance y condiciones para cambiar la decisión

**[P]** Primero, completar inventario de necesidades y demanda: aparatos, calor del edificio, dieta, agua, desplazamientos y tareas. Después, evaluar emplazamientos con residencia legal, agua estacional y acceso; esto puede descartar una finca antes de comprar maquinaria.

La siguiente unidad práctica sería una función pequeña con resultado verificable: medir, mantener y recuperar algo que ya se use. Su expediente deberá comparar compra/reparación/fabricación, incluir materiales y horas, y documentar resultado. No se declara esa unidad ejecutada en esta entrega.

**[P]** Antes de mudanza, comprobar funcionamiento en estaciones desfavorables y recuperación ante fallos, sin comprometer servicios del lugar actual. Un ciclo anual observado aporta información que una prueba de verano no da, pero tampoco garantiza años posteriores. Los tiempos dependen de finca, capital y resultados; no se fija una fecha de independencia por esperar avances tecnológicos.

**[A]** El coste integral y el plazo para conseguir el objetivo siguen sin determinarse. La tecnología disponible permite autonomía parcial y control sobre muchos servicios; la independencia total de materiales, servicios y compras no está demostrada por esta investigación. El siguiente bloque profundizará en ropa, calzado, higiene y movilidad, necesidades que una casa solar y un huerto no resuelven automáticamente.

**Límites de fuentes nuevas:** una página NIH rechazó acceso y EUR-Lex presentó comprobación de navegador; no se eludieron ni se usan para recomendaciones de B12 o plazos legales de repuestos. La guía IDAE térmica se consultó por secciones de demanda y mantenimiento, no se presenta como lectura íntegra de sus 296 páginas. Sin gastos, compras, instalaciones o ensayos físicos.
