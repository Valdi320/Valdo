# Agua: captación, almacenamiento y calidad · 23/10/2026

**Estado:** investigación documental y escenarios aritméticos. No hay captación, tratamiento ni agua analizada propios. Se conserva la meta de autonomía y desembolso cotidiano cero; esta entrega no demuestra haberla alcanzado. Se distingue [D] información documentada, [I] inferencia propia, [P] propuesta y [A] dato pendiente. Fuentes numeradas en FUENTES.md.

## 1. La primera decisión es disponer de agua, no elegir un filtro

**[P]** Evaluar por separado: fuente y derecho de uso; cantidad estacional; capacidad de almacenamiento; calidad para cada uso; distribución; tratamiento; saneamiento y destino de los residuos. Un sistema puede funcionar bien en uno de estos aspectos y seguir sin cubrir la vida cotidiana.

**[D]** La tabla pública de AEMET para Zaragoza Aeropuerto (9434), periodo **1981-2010**, indica 322 mm anuales medios. [69] No es lluvia del año 2026 ni pronóstico. Se utiliza como referencia climática de exploración, no como estimación de una finca desconocida. Un PDF de otra referencia climática rechazó el acceso: no se ha eludido ese rechazo ni se presenta su lectura como completada.

## 2. Cuánto podría captar una cubierta: cálculo auditable

**[P] Supuesto elegido:** coeficiente de captación efectivo 0,8. No es una medición: resume una pérdida elegida en la recogida. Se omiten después evaporación, rebose y pérdidas de almacenamiento. Por tanto, los litros calculados no son litros potables garantizados ni volumen necesariamente utilizable.

**Fórmula:** precipitación en mm × superficie horizontal de captación en m² × coeficiente = litros brutos recogidos. El área de un tejado inclinado no se confunde con su proyección horizontal. No se ha medido una cubierta real.

| Cubierta de referencia | Litros brutos al año con 322 mm y coeficiente 0,8 | Media aritmética diaria |
|---|---:|---:|
| 50 m² | 12.880 L | 35,3 L/día |
| 100 m² | 25.760 L | 70,6 L/día |
| 200 m² | 51.520 L | 141,2 L/día |

[Datos, supuestos y resultados del cálculo](datos/agua_alimentacion_escenarios_2026-10-23.json).

**[I]** Una demanda elegida de 100 L/día necesita 36.500 L/año. La cubierta de 100 m² solo aportaría 25.760 L brutos en este cálculo: faltan 10.740 L incluso antes del huerto y de las pérdidas posteriores. Un tanque mayor no corrige ese déficit anual.

Los 100 L/día son un escenario, no tu consumo ni un umbral universal de comodidad. Como contexto histórico, INE publicó 128 L/habitante/día de media nacional y 110 en Aragón para 2022. [89] No se afirma que sean los últimos datos publicados ni que describan una vivienda concreta.

## 3. El huerto cambia mucho el balance

**[P] Escenario independiente de riego:** 100 m² a los que se aportan 3 L/m²/día durante 90 días requieren 27.000 L de riego. La dosis y el periodo son parámetros elegidos para estudiar escala, **no necesidades agronómicas medidas ni recomendación de riego**. Hay que sustituirlos por suelo, lluvia efectiva, cultivo, evapotranspiración y manejo reales. Tampoco se supone esa agua adicional todos los días del año.

**[I]** Sumado al caso doméstico anterior: 36.500 + 27.000 = 63.500 L/año. Incluso 200 m² de cubierta, que darían 51.520 L brutos en la referencia, quedarían cortos. No se puede prometer cerrar casa y alimentación con un pequeño tejado y un depósito por considerar solo el agua bebida.

## 4. Reserva para periodos sin aportes

Escenarios de interrupción **elegidos**, no pronóstico de sequía. Suponen depósito lleno al inicio y cero aportes durante el periodo, sin pérdidas o margen adicional.

| Demanda doméstica supuesta | 30 días | 60 días | 90 días |
|---|---:|---:|---:|
| 50 L/día | 1.500 L | 3.000 L | 4.500 L |
| 100 L/día | 3.000 L | 6.000 L | 9.000 L |
| 150 L/día | 4.500 L | 9.000 L | 13.500 L |

**[I]** Si coincidieran 90 días sin aportes con el riego supuesto de 300 L/día y otros 100 L/día de casa, serían 36.000 L. No es el tamaño recomendado de un tanque: muestra por qué reducir consumo y elegir fuente/emplazamiento precede a comprar almacenamiento.

No se ha simulado una serie diaria de lluvia ni frecuencia de agotamiento. Las medias mensuales conservadas en el JSON no permiten afirmar continuidad. Antes de escoger finca se necesitan datos de estiaje y variabilidad, no solo media anual.

## 5. Calidad: separar recogida, filtración y potabilidad

**[D]** CDC señala que el agua de lluvia puede incorporar microorganismos y sustancias del aire, cubierta, tuberías o depósito, y que debe comprobarse y tratarse según el uso y los contaminantes presentes. [74] **[I]** Transparencia, buen sabor o conductividad aceptable no sustituyen una evaluación de esos peligros. No se prescribe un filtro universal.

**[D]** El manual CAWST de filtro de bioarena revisado permite adaptar su documentación bajo CC BY 3.0 y describe construcción, operación y mantenimiento. Advierte que no elimina todas las contaminaciones ni garantiza por sí solo el resultado. [75] Su marco de competencias aporta controles de fabricación, arena e instalación. [76]

**[P]** Es una línea abierta interesante para estudiar fabricación y mantenimiento con materiales sencillos; no se acepta automáticamente como única barrera de agua de consumo. Necesitamos identificar fuente, contaminación, tratamiento requerido y almacenamiento posterior. No se dan aquí instrucciones para convertir agua desconocida en potable.

**[A]** No hay BOM local cerrada para ese filtro, ni pruebas de nuestro montaje, ni plan analítico para una fuente concreta. Su precio no se inventa a partir de costes antiguos de otros países. Los materiales y consumibles deberán verificarse por lote y función, aunque el diseño sea abierto.

## 6. Derechos y condiciones que afectan a la elección del lugar

**[D]** La Ley de Aguas contempla el aprovechamiento por el propietario de lluvia dentro de la finca, con límites, y determinados usos de manantiales/aguas subterráneas hasta 7.000 m³ anuales sujetos a condiciones. Una concesión tampoco garantiza caudal disponible. [70] El reglamento añade comunicación, documentación y reglas específicas; el Registro de Aguas de CHE permite consultar títulos. [71,73]

**[I]** Tener terreno o ver un pozo no demuestra por sí solo permiso, potabilidad o disponibilidad en verano. Antes de comprar un lugar se verificarán el derecho aplicable, sus condiciones y la viabilidad física. No se ha tramitado ni obtenido ninguna autorización.

**[D]** El RD 3/2023 distingue tipos de abastecimiento y supuestos de aplicación, incluidos pequeños suministros y actividad comercial. [72] No se aplicará sin análisis toda la normativa de una red urbana a un uso doméstico, ni se supondrá exención total por ser privado. Vender alimentos puede cambiar el contexto. Falta estudiar saneamiento y reutilización para el emplazamiento elegido.

## 7. Referencias de coste: almacenamiento y comprobación

Consulta del 23/10/2026, sin carrito, pedido o ubicación de entrega fijada. Los anuncios no son presupuesto instalado. Los depósitos se cuentan como referencias de mercado; no se declara demostrada una superioridad de diseño cerrado frente a uno abierto.

| Referencia | Importe mostrado | Qué incluye o qué falta | Fuente |
|---|---:|---|---|
| GRAF agua potable 1.000 L, ref. 25136176 | 290 EUR con IVA | Depósito; disponibilidad por almacén, transporte y adaptación pendientes. La ficha indica que no lleva válvula integrada | [85](https://www.obramat.es/productos/deposito-de-agua-potable-1000-l-25136176.html) |
| Aquatonne 1.000 L | Desde 375,64 EUR con IVA | Anuncia transporte 31,46 EUR; validar destino. El vendedor lo describe apto para uso alimentario | [86](https://www.todocontenedor.com/producto/deposito-aquatonne-agua-potable-1000-litros.html) |
| Servicio Análisis Potabilidad, Agua Ecosocial | 134,31 EUR con IVA | Panel básico; proveedor indica mensajería incluida en Península. No es evaluación de todos los contaminantes posibles | [87](https://aguaecosocial.com/producto/analisis-potabilidad/) |

**[I]** Nueve depósitos GRAF al importe mostrado sumarían 2.610 EUR para 9.000 L nominales. Es solo una cesta modular aritmética para el caso doméstico de 90 días: no es la opción óptima, ni incluye obra, cubierta, filtros, conducciones, tratamiento o comprobaciones. Puede ser mejor otra solución constructiva; falta compararla y presupuestarla.

[Registro de precios y condiciones](datos/precios_agua_conservacion_2026-10-23.json).

Un depósito lleno de 1.000 L contiene aproximadamente una tonelada de agua, además del recipiente. No se ha validado una terraza ni una estructura para esas cargas; estas cantidades no son una propuesta de instalación en una vivienda urbana actual.

**[D/I]** El panel comercial de 134,31 EUR enumera parámetros básicos, entre ellos E. coli y conductividad; nitratos, metales o plaguicidas no figuran en esa lista. [87] No se presenta como comprobación suficiente para cualquier pozo o cubierta. El proveedor declara laboratorio acreditado: no se ha auditado su identidad, alcance o método. Deben verificarse para la necesidad concreta.

## 8. Mantenimiento y mejoras que podríamos hacer

**[P]** Diseñar separación de usos y conexiones, acceso para limpieza, aislamiento por módulos, registro de fugas y medición de consumo antes de automatizar. Usar piezas normalizadas y documentar repuestos. La fabricación de soportes o carcasas no acredita un material para contacto con agua de consumo.

**[I]** La energía de bombeo puede calcularse aparte de la calidad. Un ejemplo idealizado para subir 1 m³ 10 m, con rendimiento supuesto del 50 %, da unos 0,055 kWh: masa × gravedad × altura / rendimiento. No incluye rozamiento, arranques u otros consumos, ni dimensiona una bomba. Evitar bombas mediante gravedad puede simplificar mantenimiento si el lugar lo permite.

**[P]** Registrar limpieza, sustitución de componentes, pérdidas, resultados analíticos y cambios de fuente. No se fija una frecuencia universal de análisis ni se convierte una sola muestra favorable en garantía permanente. La autonomía exige resolver estos recursos y tareas, no ocultarlos como mantenimiento gratuito.

**Pendientes:** fuente y finca, derechos, serie diaria reciente, estiaje, demanda real, controles de calidad, tratamiento específico, depósito alternativo fabricable, saneamiento, agua reutilizada y coste completo. La investigación tiene rutas abiertas aunque esos datos aún no existan.
