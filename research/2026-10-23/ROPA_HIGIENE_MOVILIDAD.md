# Ropa higiene y movilidad para una vivienda autónoma

Fecha de consulta: 23/10/2026. Ampliación del estudio de autosostenimiento con prioridad por diseños abiertos, comodidad y poca intervención. Se distinguen datos documentados [D], inferencias [I], propuestas [P] y pendientes [A]. [Datos y operaciones](datos/ropa_higiene_movilidad_2026-10-23.json).

**Conclusión:** hoy podemos recuperar parte del control sobre patrones, reparaciones y electrónica de algunas máquinas. Eso no resuelve todavía la producción continuada de tejidos, calzado, productos de higiene o componentes de transporte a partir de recursos propios. La opción compatible con poca intervención es conservar funciones automáticas útiles y reducir sus dependencias pieza por pieza. La fabricación íntegra doméstica sigue siendo una línea de investigación, sin fecha de disponibilidad defendible.

## Ropa desde patrones abiertos hasta fibra propia

| Proyecto | Aportación comprobada | Alcance que debemos conservar |
|---|---|---|
| FreeSewing | Generación de patrones personalizados [140] | Su antiguo repositorio GitHub está archivado y remite a Codeberg [141]. La consulta del nuevo alojamiento quedó bloqueada por robots; licencia y reproducción de la versión actual pendientes |
| Seamly2D | Patronaje paramétrico, GPLv3+, Windows, macOS y Linux [142] | Su licencia no fabrica tejido, hilo, agujas o una máquina de coser. Hay dependencias con licencias propias |
| AYAB | Control abierto para determinadas máquinas de punto Brother; hardware documentado por generación [17] | El procedimiento básico incluye mover el carro, enhebrar y rematar [143]. Ese procedimiento no equivale a una fábrica de prendas desatendida |

**[P]** Empezar por reparar, ajustar y reutilizar ropa existente permite trabajar sobre una necesidad concreta sin crear de entrada una explotación textil. Cada intervención tendría que registrar material añadido, minutos de trabajo, resultado después de uso y lavados, y compras evitadas. Una prenda aprovechada es una reducción de compras; no acredita suministro renovable de hilo o tejidos.

**[I]** El material recuperado puede servir durante un tiempo, pero un almacén finito de ropa no produce fibra nueva. Para cerrar la cadena habrá que contabilizar también roturas, prendas que ya no admiten reparación, limpieza, merma y herramientas. Los patrones abiertos resuelven una parte del conocimiento de diseño; los trabajos de corte, costura, ajuste y control de calidad siguen presentes.

### El lino como hipótesis de materia prima local

**[D]** La extensión agraria de Wisconsin describe una cadena de cosecha, enriado, separación de partes leñosas, peinado, hilado y tejido. El enriado usa actividad microbiana para liberar las fibras; acertar su final requiere juicio y las condiciones ambientales importan. Distingue la cosecha para fibra fina de la destinada a semilla y señala necesidades de equipo a distintas escalas. [155]

**[I]** Tener una planta con fibra aprovechable no equivale a disponer de tejido. Los resultados agrarios de Wisconsin no establecen rendimiento, riego, calendario o calidad en una futura finca española. Tampoco prueban que podamos obtener de una misma cosecha el máximo de semilla comestible y fibra fina.

**[P]** Una investigación posterior debería comparar una muestra de fibra local, tejido recuperado e hilo adquirido para una misma pieza útil. Se medirían masa inicial, masa utilizable, agua, energía, trabajo activo y resistencia de la pieza. Automatizar el hilado sin resolver la preparación de fibra trasladaría el trabajo a otra etapa. La lana es otra candidata, pero una cadena con animales exige estudiar alimentación, esquila, sanidad, agua y trabajo antes de atribuirle autonomía.

## Lavado automático y fabricación de su control

**[D]** MyGenWashy publica un controlador genérico de lavadora. El relato del hackatón de junio de 2025 describe un lavado en frío con electrónica provisional y ESPHome; después se trasladó el diseño a KiCad para continuar las pruebas y el software. El repositorio contiene listas de materiales y una licencia GPL-3.0. [144,145]

**[I]** Es una base relevante para reemplazar un control que impida reparar una máquina. El resultado documentado no valida todos los programas, temperaturas, motores, interbloqueos o comportamientos ante fallos. Tampoco reproduce tambor, motor, cuba, retenes, rodamientos y mangueras. No se propone instalarlo en un electrodoméstico doméstico como sustituto ya validado.

**[P]** La mejora útil sería documentar una combinación concreta de máquina y placa: versión de archivos, esquema, piezas sustituibles, secuencia de control y comportamiento ante puerta abierta, fuga, falta de agua, sensor averiado y desequilibrio. Haría falta comparar limpieza, consumo y mantenimiento con el control original. La validación eléctrica y mecánica no se obtiene simulando únicamente el programa.

### Referencia de recursos para conservar la comodidad

**[D]** La ficha española de UDDARP 705.254.67, 8 kg, muestra 499 €, 63 kWh por 100 ciclos y 48 L por ciclo como valores ponderados. Declara 67 kg de peso. [148] Es una referencia comercial de recursos, sin licencia de diseño abierta acreditada ni selección de compra. Entrega, instalación y condiciones finales pendientes.

**[P]** Si se eligen 2 ciclos semanales durante 52 semanas, son 104 ciclos: aplicar aquellos valores ponderados da **65,52 kWh y 4.992 L al año**. Es una proyección de etiqueta, no medida de una casa ni garantía para cualquier carga o programa. En promedio aritmético son 0,180 kWh y 13,68 L diarios; la lavadora concentra consumos en horas concretas.

**[I]** Estos litros solo deben sumarse al estudio de agua si su demanda doméstica anterior excluía lavado. Añadirlos sin revisar esa frontera podría contarlos dos veces. El consumo anual tampoco dimensiona la potencia instantánea, el arranque o las necesidades de tratamiento del agua residual.

**[D]** Umweltbundesamt relaciona la dosificación con suciedad y dureza del agua y explica que sobredosificar no mejora el resultado de lavado. [150] **[I]** El detergente y el tratamiento de aguas forman parte del sistema, aunque la electricidad proceda de paneles propios.

**[P]** Para hacer visible el coste humano, se comparan dos tiempos elegidos, sin atribuirlos a máquinas: 20 frente a 45 minutos activos por cada una de 104 coladas darían 34,67 frente a 78 horas anuales. La diferencia es 43,33 horas; no es un ahorro medido. Habría que incluir clasificar, cargar, tender, recoger y limpiar, y separar trabajo activo de duración del programa. Lavar a mano no gana esta comparación por consumir menos electricidad solamente.

## Costura y calzado reparables

**[D]** Alfa anuncia Style 40 como máquina mecánica a 250 €. [149] El precio y su clasificación no demuestran apertura del diseño o reparabilidad de cada conjunto. Antes de valorar una compra frente a un equipo abierto, usado o ya disponible hacen falta despiece, repuestos, manual y coste de averías equivalentes.

**[D]** Last Shoe ofrece un diseño modular de calzado para ciclismo y caminar, con archivos de varios conjuntos y una talla europea 45. Su README indica CC BY-SA 4.0 mientras LICENSE contiene CC0: se conserva esa discrepancia sin resolverla por la etiqueta automática de GitHub. [146,147]

**[I]** El proyecto permite investigar uniones y piezas sustituibles, pero los archivos no acreditan duración, ajuste o prestaciones de un zapato fabricado con cualquier material o impresora. Tampoco equivalen a calzado de protección. Para cubrir la necesidad diaria faltan suela, textiles, cierres y validación de desgaste, flexión, humedad y reparación repetida.

**[P]** Priorizar un zapato existente que admita reparación puede evitar fabricar toda la cadena de una vez. Un ensayo posterior de pieza intercambiable debería empezar fuera de usos de protección, con material identificado y criterios de desgaste definidos. No se considera cualquier polímero reciclado equivalente a una suela comercial.

## Higiene y productos que se consumen

**[I]** Fabricar jabón, detergente y dentífrico son problemas distintos. Un inventario útil debe identificar función, dosis, composición requerida y estabilidad; después, origen y control de cada ingrediente. Disponer de una receta pública no acredita pureza, eficacia o reposición local del material.

**[D]** El Consejo General de Dentistas advierte de que alternativas naturales como bicarbonato, arcilla o aceite de coco no sustituyen la prevención de caries con flúor. [151] **[I]** Por tanto, no se contabiliza un dentífrico casero genérico como sustitución sanitaria ya resuelta ni se considera la higiene bucal independiente de productos y atención profesional.

**[P]** Para investigar limpieza producida localmente habría que definir primero el resultado: retirar grasa, lavar tejido, higiene personal o tratar una contaminación concreta. Después se compararían estabilidad y composición de materias primas, agua usada, residuos, energía, trabajo y resultado frente a una referencia. Una fuente aparentemente gratuita que varía de composición puede exigir más análisis y preparación. Se mantiene abierta esta vía sin ofrecer una receta doméstica como garantía sanitaria.

**[I]** La autonomía material completa también tendría que cubrir medicamentos, diagnóstico y cuidados que aparezcan en el futuro. La incertidumbre de esas necesidades impide prometer que una inversión inicial elimine para siempre compras o servicios sanitarios. Una biblioteca y una IA local pueden ayudar a organizar conocimiento; no sustituyen esas capacidades materiales.

## Movilidad con menos energía y componentes externos

**[D]** VESC publica firmware GPL-3.0 para control de motores. [152] **[I]** Poder mantener ese código mejora el control sobre una pieza del vehículo; no fabrica motor, celdas, neumáticos, cadena, rodamientos o electrónica. El esquema y licencia de una placa concreta deben comprobarse aparte de los del firmware.

**[D]** El Reglamento General de Vehículos diferencia el ciclo de pedaleo asistido: motor auxiliar de potencia nominal continua máxima de 250 W, asistencia que disminuye y se interrumpe antes de alcanzar 25 km/h o al dejar de pedalear. [153] **[I]** Montar un controlador programable no demuestra por sí solo que un vehículo cumpla su categoría o todos sus requisitos de circulación.

**[D]** Como referencia comercial, E-ACTV 100 de cuadro bajo 8893262 figura a 999,99 €, con batería extraíble nominal de 356 Wh. La ficha anuncia hasta 70 km en ECO bajo las condiciones que describe y un peso de 22,9 kg en L/XL. [154] No se adopta ese alcance como resultado de una ruta rural ni se acredita apertura del conjunto. Precio final, talla, disponibilidad y entrega pendientes.

**[P]** Para comparar movilidad con generación se eligen 1.000 y 3.000 km anuales, consumos de batería de 10 y 20 Wh/km y rendimiento de carga del 85 %. Las cuatro combinaciones exigirían, respectivamente, **11,76; 23,53; 35,29 y 70,59 kWh anuales en el cargador**, sin consumos de espera. Son escenarios, no datos de la bicicleta anterior. Distancia, desnivel, carga, clima y esfuerzo humano decidirán su utilidad.

**[I]** En una ruta hipotética de 20 km a 20 Wh/km se pedirían 400 Wh de batería, por encima de aquellos 356 Wh nominales incluso antes de descontar reserva o degradación. Una autonomía publicitaria no permite dar por cubierto ese desplazamiento. Ni la carga solar elimina desgaste y sustituciones de batería, cubiertas, transmisión y frenos.

**[P]** Antes de elegir vehículo, comparar emplazamientos por distancia a servicios, caminos transitables y carga que habría que mover. La bicicleta convencional evita la cadena eléctrica pero exige más trabajo humano; la asistida reduce parte del esfuerzo y añade componentes. La elección depende de trayectos y comodidad, no solo de kWh. La movilidad de emergencia y los traslados de equipos pesados necesitan una solución separada.

## Porcentaje útil y plazos

**[I]** Estos proyectos no sostienen un porcentaje único de vida autosuficiente. El 67 % del catálogo inicial describe la clasificación de 24 casos elegidos; no mide la fracción de nuestras necesidades cubierta. Tampoco sería informativo pesar las piezas fabricadas: un chip ligero puede detener una máquina pesada hecha localmente.

**[P]** Para medir progreso, cada función tendrá una demanda anual y una lista de dependencias críticas. Se registrarán por separado la fracción de servicio producido localmente, la fracción de averías reparables con medios disponibles, las compras/reposiciones externas y las horas de intervención. Los cocientes solo se calcularán cuando existan denominadores y resultados, con especial atención a invierno y fallos. No se promedian ropa, salud y agua como servicios intercambiables.

| Nivel de autonomía | Qué podemos avanzar | Condición para darlo por logrado |
|---|---|---|
| Diseño y documentación | Patrones, archivos de piezas, control local y manuales disponibles | Versión, licencia, dependencias y reproducción comprobadas |
| Reparación con materiales industriales | Costura, piezas sustituibles y algunas placas | Reparación útil y repetible con coste, trabajo y repuestos registrados |
| Producción desde recursos locales | Investigar fibra y procesos de limpieza definidos | Calidad suficiente, rendimiento y balances de agua, energía y trabajo |
| Reproducción completa del sistema | Investigar también herramientas, materiales críticos y reposición | Todas las dependencias críticas reproducibles y validadas durante un periodo significativo |

**[I]** Los dos primeros niveles permiten actuaciones con tecnología existente. Los dos últimos no tienen un plazo doméstico acreditado para todo lo importante. No hay base para prometer que esperar cinco, diez o veinte años los resolverá: también importan recursos geológicos, escala, consumibles y trabajo, además del avance de diseños abiertos.

**[P]** El siguiente avance será examinar los materiales que bloquean la reposición: baterías, elastómeros, lubricación, componentes electrónicos y herramientas de precisión. Para cada cadena se buscará una ruta abierta a escala pequeña y se distinguirá proceso demostrado, prototipo y propuesta. Solo después se podrá priorizar qué merece desarrollar nosotros frente a reducir o sustituir su función.

## Registro económico y acceso a fuentes

Los tres precios nuevos son referencias de catálogo del 23/10/2026: lavadora 499 €, máquina de coser 250 € y bicicleta eléctrica 999,99 €. No forman una cesta recomendada ni un presupuesto de autosuficiencia. No se ha probado una ventaja equivalente que justifique preferirlos a equipos abiertos; ayudan a fijar funciones, magnitudes y costes que una alternativa debería comparar.

Codeberg bloqueó la lectura automatizada del repositorio actual de FreeSewing; no se buscó otra vía para acceder al mismo contenido. La página de Wisconsin se consultó mediante contenido indexado; la apertura directa agotó el tiempo. EPREL enlazado por IKEA no devolvió contenido legible, por lo que los datos de lavado se atribuyen a la ficha del fabricante/vendedor. No se han comprado, instalado, fabricado ni ensayado estos equipos.
