# Agua del aire: fabricación abierta, energía y potabilidad · 23/10/2026

**Resultado provisional:** sí merece investigación como fuente complementaria, especialmente para beber y cocinar donde falten fuentes mejores. No hay evidencia suficiente para elegirla como suministro único de una vivienda en Zaragoza, ni para afirmar que podemos fabricar hoy un equipo potable sin compras recurrentes. Se prioriza un sistema abierto por módulos; no se ha comprado, montado, conectado ni probado ningún aparato.

Convenciones: **[D]** documentado; **[I]** inferencia o cálculo propio; **[P]** propuesta; **[A]** pendiente. Las fuentes nuevas son 278–290 en [FUENTES.md](FUENTES.md). [Registro de evidencia y cálculos](datos/agua_atmosferica_2026-10-23.json).

## 1. Qué máquina existe y qué trabajo realiza

**[D]** Un generador de agua atmosférica, AWG, extrae agua ya presente en el aire. Una ruta enfría una superficie para condensarla; otra captura vapor con un material absorbente y aplica calor para liberarlo y recogerlo. DOE distingue estas rutas y señala la importancia del clima, la energía y el uso final. [279]

**[I]** La función completa tiene tres partes: captar agua, tratarla para el uso elegido y conservarla sin recontaminación. Fabricar una superficie que gotea solo resuelve una parte. Tampoco se obtiene agua neta evaporando primero nuestra propia reserva con un humidificador. Una habitación cerrada no es una fuente ilimitada: hace falta renovación de aire y considerar sus condiciones.

| Ruta | Interés para la autonomía | Dependencia que debemos resolver |
|---|---|---|
| Compresor frigorífico | Tecnología comercial; estudiar funcionamiento con excedentes solares | Electricidad, ventilación, averías del circuito frigorífico, limpieza y calidad del circuito de agua |
| Placas Peltier | Montaje sencillo para estudiar condensación a pequeña escala | Rendimiento real y disipación; sencillez de montaje no demuestra eficiencia ni potabilidad |
| Material absorbente regenerado por calor solar | Puede aprovechar calor sin convertirlo primero en electricidad | Fabricación, regeneración, pérdida de material, contaminación y duración del absorbente |
| Rocío o niebla | Interesa investigar si el emplazamiento ofrece esas condiciones | No se ha demostrado aportación diaria suficiente en una finca concreta; humedad ambiental no equivale a niebla aprovechable |

La tabla es una comparación de diseño, no una clasificación experimental propia. No existe aún una ruta ganadora para nuestro emplazamiento futuro.

## 2. Zaragoza: humedad relativa alta no garantiza mucha agua

**[D]** AEMET, estación Zaragoza Aeropuerto 9434, normales **1981–2010**, ofrece estas medias seleccionadas: [69]

| Mes | Temperatura media | Humedad relativa media |
|---|---:|---:|
| Enero | 6,6 °C | 75 % |
| Abril | 13,8 °C | 57 % |
| Julio | 25,3 °C | 47 % |
| Octubre | 16,2 °C | 67 % |
| Diciembre | 7,0 °C | 76 % |

**[I]** El invierno es húmedo en términos relativos, pero frío. No debe equipararse al aire cálido y húmedo de una prueba comercial. Tampoco se pueden combinar medias mensuales de temperatura y humedad para predecir litros diarios: faltan su coincidencia horaria, caudal, temperatura del condensador, controles, deshielo y curva de rendimiento.

**[D]** GENNY declara **0,4 kWh/L a 26,7 °C y 60 % HR**, hasta 30 L/día, 80 kg y funcionamiento desde 18 °C y 30 % HR. Son datos del fabricante, no mediciones nuestras. [280] **[I]** El umbral de funcionamiento no significa mantener producción máxima o el mismo consumo específico en todo el intervalo. Las medias de varios meses de Zaragoza quedan por debajo de esa temperatura mínima; no se deriva de ello un número de horas operativas ni producción cero todo el mes.

**[P]** Para el campo, comparar primero climas y fuentes disponibles. Elegir una finca con agua accesible y verificable puede reducir mucho más la dependencia que añadir una máquina que necesite electricidad para cada litro. La decisión no se cierra con el porcentaje anual de humedad.

## 3. La energía cambia la escala de la propuesta

**[I] Cálculo de sensibilidad:** energía diaria = litros diarios × kWh por litro. El primer valor procede de la condición comercial anterior; **1 y 3 kWh/L son hipótesis elegidas**, no resultados medidos, límites universales ni pronóstico de Zaragoza. Los litros son escenarios de servicio, no necesidades personales prescritas.

| Servicio supuesto | A 0,4 kWh/L | A 1 kWh/L | A 3 kWh/L |
|---|---:|---:|---:|
| 5 L/día para una reserva pequeña de consumo | 2 kWh/día | 5 kWh/día | 15 kWh/día |
| 100 L/día, escenario doméstico del estudio | 40 kWh/día | 100 kWh/día | 300 kWh/día |

No se añaden consumos no incluidos en cada especificación, nuevas pérdidas de almacenamiento o el resto de la vivienda. Si el aparato no funciona con una condición ambiental, la tabla no permite forzar ese rendimiento suministrándole más energía.

**[I]** Como comparación de escala, el [modelo PVGIS previo](ENERGIA_PVGIS.md) da 2,83 kWh/día por kWp al sur en diciembre: **6 kWp → 16,98 kWh/día medios modelados**. No es un mínimo diario ni energía garantizada tras batería. En el escenario de 5 L y 3 kWh/L, solo el AWG demandaría 15 kWh/día; en el de 100 L y 0,4 kWh/L serían 40. El sistema solar no queda dimensionado para ello. No se resta una media meteorológica de un consumo hipotético para acreditar continuidad.

**[I]** La comparación con lluvia debe mantener iguales cantidad útil, calidad, continuidad y costes. La lluvia evita esta fase activa de extraer vapor, pero requiere cubierta, reserva, tratamiento y disponibilidad estacional. El [balance de agua anterior](AGUA_CAPTACION_CALIDAD.md) tampoco demuestra autonomía solo con tejado. Ninguna de las dos rutas se declara gratuita por omitir sus componentes y mantenimiento.

## 4. Qué hay abierto y qué podemos fabricar

### OpenAWG / BlueIce Alpha

**[D]** Revisión fijada en `c03ccb9fcca86f70d1dd5e32b71ea0784273ab80`, último commit de la rama por defecto consultada, **20/05/2016**. Árbol no truncado: no aparece un archivo de licencia global identificado por nombre. Esto no audita las licencias de cada dependencia ni demuestra abandono de toda actividad externa. [283]

**[D]** BlueIce publica montaje y referencias comerciales: deshumidificador, bomba, ósmosis/UV y depósito. El README mantiene pendiente la certificación de agua potable. [284] La entrada del proyecto del 22/03/2016 comunica análisis iniciales favorables y pide más pruebas; los informes enlazados no se han abierto en esta revisión. [285]

**[I]** Es antecedente útil de integración, no una máquina íntegramente fabricable desde materias primas. No se adopta como base libre sin aclarar derechos. Tampoco se transfiere un resultado antiguo de una muestra a otro deshumidificador o a servicio permanente.

### WaterOfLife-OpenAWG

**[D]** Revisión `62ecd2db624031b608f8a41ded1b2fda91173008`, **15/04/2026**. El árbol no truncado contiene seis archivos Markdown; no aparece licencia separada, CAD ni datos instrumentales de producción. El README declara alternativamente MIT o CC BY 4.0, sin desarrollar una licencia completa. La declaración requiere aclaración antes de reutilizar como proyecto abierto verificado. [286,287]

**[D]** Propone Peltier y anuncia 60–100 USD. Su documento de rendimiento presenta **expectativas**, no un registro de medidas: 0,3–0,6 L/día con un módulo a 24–30 °C y 60–80 % HR. [287,288]

**[I]** Sumando las 17 líneas de precios de su propia BOM, comprando un ejemplar de cada elemento y un Peltier: **98–206 USD**; con dos, **101–212 USD**. No incluye entrega española, impuestos, comprobación sanitaria ni instrumentación. Recuperar piezas puede reducir compras, pero hay que contabilizar cuáles existen y son adecuadas. La lista no acredita el presupuesto anunciado como máquina potable completa.

**[P]** Podemos desarrollar por separado soportes, bandeja accesible, conducciones desmontables, control local, registro de energía/agua y documentación. La pieza impresa que sirve de soporte no queda autorizada por ello para contacto con agua de boca. Faltan materiales y referencias concretos, rendimiento, vida útil, procedimiento de limpieza y validación del conjunto. No se ha demostrado ventaja de un diseño cerrado que justifique copiarlo; se estudiarán principios y documentación con acceso legítimo.

## 5. La opción solar sin compresor sigue abierta

**[D]** Un trabajo publicado el **09/06/2026** en Nature Water comunica un sistema modular de tejidos de gel celulósico: **1,3 L con dos módulos en Austin**, en torno a 62 % HR; también informa rendimiento normalizado en el desierto de Chihuahua. Solo se ha revisado el resumen indexado: la apertura redirigió a un servicio de identificación inaccesible; no se ha sorteado ni leído método o suplemento. No se conoce aquí una BOM reproducible, coste español o duración multianual. [289]

**[D]** Otro trabajo de Nature Water, **11/06/2025**, informa **57,0–161,5 mL/día** en Death Valley con un dispositivo de escala métrica y gel plegado. Es resultado del dispositivo y condiciones de ese estudio, no litros por metro cuadrado transferibles a otro equipo. Solo resumen indexado; misma limitación de apertura, sin auditoría de materiales o vida útil. [290]

**[I]** Los resultados justifican continuar esta línea: un sistema solar térmico puede cambiar la comparación frente a refrigeración eléctrica. No permiten prometer una lámina barata que suministre toda la casa. Rendimiento por masa de absorbente, por superficie, por ciclo y por aparato no son cifras intercambiables. Una publicación accesible tampoco constituye por sí sola una licencia de hardware abierta.

## 6. Agua recogida y agua apta para beber

**[D]** EPA estudió durante tres meses un GEN-350: informó resultados microbiológicos favorables para consumo en ese estudio, junto con recuentos heterótrofos elevados y necesidad de controlar crecimiento microbiano. Señala que compuestos orgánicos volátiles del aire pueden disolverse en el condensado. No valida todos los AWG ni un deshumidificador doméstico modificado. [278]

**[I]** Por tanto, agua transparente y una lectura baja de sales no demuestran potabilidad. Un filtro de carbón no constituye por sí solo una garantía microbiológica o química universal. Se deberán estudiar aire de entrada, superficies mojadas, sustancias liberadas por materiales, tratamiento y conservación, con comprobación adecuada del agua producida. No se recomienda beber el primer condensado de un montaje experimental.

**[D]** La página tecnológica de Watergen anuncia cambios de cartuchos cada seis meses. [281] **[I]** Es una dependencia comercial concreta, no un intervalo universal: deben contarse filtros, limpieza, recambios, desinfección y comprobaciones en el diseño propio. Alimentación solar no elimina esas tareas o compras. Un módulo frigorífico reemplazable puede mejorar el mantenimiento, pero no equivale a fabricar ni reparar todas sus partes en casa.

## 7. Precios y decisión de avance

| Referencia consultada 23/10/2026 | Importe observado | Alcance |
|---|---:|---|
| Dhoop Solar DW-90 | **2.995 EUR, IVA incluido** | Oferta pública de 30 L/día; no se especifica una condición única de ensayo que permita transferir esa producción al clima local. Entrega, disponibilidad y coste total no verificados. [282] |
| WaterOfLife, suma propia de BOM, un Peltier | **98–206 USD** | Aritmética de rangos publicados; no precio de compra español ni máquina potable validada. [287] |
| Prototipo de sorción solar reproducible | **Pendiente** | No se inventa precio a partir de gramos de absorbente omitiendo carcasa, captación solar, condensación, almacenamiento y control de calidad. |

**[P] Orden útil, sin gastar todavía:**

1. Comparar una demanda elegida de 5 L/día con lluvia almacenada y fuentes locales, usando la misma exigencia de continuidad y calidad.
2. Obtener o reutilizar registros horarios fiables de temperatura y humedad para cada emplazamiento candidato; no comprar sensores si ya existe información suficiente para descartar una ruta.
3. Priorizar la lectura de un método de sorción solar con materiales, geometría, rendimiento real y condiciones de reutilización verificables. Queda pendiente, no sustituido por el resumen.
4. Completar una BOM de un candidato abierto y separarla de las funciones que dependen de componentes comerciales. Evaluar litros útiles por kWh, horas de trabajo y coste de reposición.
5. Si después se decide prototipar, comenzar por recogida y medidas sin consumo humano; validar tratamiento y almacenamiento antes de considerarlo fuente de bebida. Esta investigación no ejecuta ese ensayo.

**Decisión actual:** incorporar el agua atmosférica como línea concreta del proyecto, con prioridad a sorción solar documentada y control modular abierto. Para Zaragoza se mantiene como complemento pendiente de demostrar. El suministro único, la potabilidad del equipo propio y el gasto cotidiano cero siguen sin acreditarse.
