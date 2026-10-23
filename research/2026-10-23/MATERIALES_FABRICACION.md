# Materiales locales, reciclaje y fabricación reparable · 23/10/2026

**Estado:** revisión documental y modelos aritméticos; sin máquinas adquiridas, piezas fabricadas o propiedades verificadas. [D] documentado; [I] inferencia; [P] propuesta; [A] pendiente. Fuentes en FUENTES.md; parámetros en [datos](datos/materiales_fabricacion_2026-10-23.json). Se amplía el documento anterior de materiales, sin tratar sus hipótesis como resultados propios medidos.

## 1. Resultado que cambia la primera inversión

**[I/P]** Para una única vivienda, reparar piezas existentes y fabricar repuestos de geometría sencilla puede acercarnos antes a la autonomía que comprar inmediatamente una línea de reciclaje. No se decide aún qué impresora o taller comprar: faltan piezas objetivo, consumo de material, espacio y capacidades disponibles.

La cadena que hay que cerrar es **recurso disponible → materia acondicionada → pieza → verificación → uso → recuperación**, más los repuestos de las máquinas que la sostienen. Tener los planos abre información y opciones de reparación; no produce el polímero, el acero, las celdas o los chips con los que se construye el equipo. No se asigna un porcentaje global a esa cadena con datos incompletos.

## 2. Reciclaje de filamento: separar demostración y promesa

**[D]** El resumen de Woern et al., HardwareX 2018, describe RepRapable Recyclebot con 0,4 kg/h, 0,24 kWh/kg y variación de diámetro ±4,6 %. El coste menor de 700 USD pertenece a aquella publicación. [104] **No es presupuesto de 2026 ni energía de toda una vivienda/taller.**

El extracto indexado de su apartado de validación especifica PLA y una medición de producción de filamento; distingue costes eléctricos y exclusión de capital/trabajo en su estimación con residuo. El resumen es accesible; el PDF completo no pudo revisarse íntegramente: primero excedió el tamaño admitido y la descarga directa recibió 403. Se detuvo esa vía. No se acredita aquí réplica independiente ni rendimiento para cualquier residuo.

**[I]** No se debe convertir el coste de electricidad de extrusión en «precio del plástico gratis». Faltan recogida, selección, limpieza, secado, molienda, purgas, descartes, consumibles, medición y mantenimiento. No se extrapolan aquellos resultados al equipo Felfil o a un proceso con botellas PET.

**[D]** Polyformer sigue publicando CAD, lista de materiales y GPL-3.0, pero su README anuncia fin de soporte a finales de 2025 y una incompatibilidad entre una revisión de placa y el firmware antiguo. [26] **[P]** Antes de reproducirlo habría que resolver esa compatibilidad. Es candidato de desarrollo, no compra lista para asegurar suministro indefinido.

## 3. Referencia de mercado y apertura comprobada por versión

| Referencia Felfil anunciada | Precio observado | Alcance que hay que distinguir |
|---|---:|---|
| Evo Complete Kit | 699 € | Kit de extrusora; no línea completa de recuperación |
| Evo + Spooler+ | 1.399 € | Extrusión y bobinado |
| Evo + Spooler+ + Shredder+ | 2.999 € | Incluye trituradora, extrusora y bobinador |

**[D]** Precios de la página principal al consultar el 23/10/2026. [105] Las condiciones indican IVA incluido para consumidores UE y transporte separado. [109] **[A]** Falta confirmar variante, entrega en España y precio final. No se añadió nada al carrito ni se solicitó compra.

**[D]** La ficha del conjunto anuncia extrusión de 100-150 g/h, Evo de 300 °C y cuchillas reemplazables. [106] **[I]** A ese caudal, 1 kg requeriría aproximadamente 6,7-10 horas solo de extrusión, sin contar preparación y cambios. Es una conversión de lo anunciado, no medida propia ni comparación controlada con Recyclebot. La potencia máxima indicada para la trituradora no sirve para calcular el consumo total por kilogramo del conjunto.

**[D]** Felfil presenta Evo como abierto y reconoce componentes especiales caros de fabricar individualmente. [107] El README de su repositorio consultado declara actualización 18/07/2016. [108] **[A]** La carpeta de licencia no fue accesible y no se eludió el rechazo. No se da por auditada la licencia exacta de todos los archivos, ni que el conjunto comercial actual esté reproducido íntegramente en ese repositorio. El eslogan abierto y la existencia de un repositorio antiguo no bastan para demostrar equivalencia.

**[P]** No seleccionamos el conjunto comercial como superior: faltan comparación de calidad de salida, horas humanas, fallos y coste completo frente a una versión abierta reproducible. Sus referencias económicas permiten evaluar escala, no justificar automáticamente la compra.

## 4. Cuándo podría amortizarse: escenarios, no estimación personal

**[P] Supuestos elegidos:** inversión de referencia de 3.000 €, margen neto de 10 o 20 € por kg de material utilizable y demanda de 2, 10 o 30 kg/año. Los 3.000 € redondean una escala comercial; no incluyen un taller presupuestado. El margen deberá restar todos los costes incrementales reales y no está observado. No se supone que el residuo sea gratuito o que el equipo dure el plazo calculado.

**Fórmula:** años de recuperación simple = inversión / (kg utilizables al año × margen neto por kg).

| Demanda elegida | Ahorro anual con margen 10 €/kg | Recuperación simple | Ahorro anual con margen 20 €/kg | Recuperación simple |
|---|---:|---:|---:|---:|
| 2 kg/año | 20 € | 150 años | 40 € | 75 años |
| 10 kg/año | 100 € | 30 años | 200 € | 15 años |
| 30 kg/año | 300 € | 10 años | 600 € | 5 años |

**[I]** Con bajo consumo, incluso un margen favorable puede dejar una recuperación incompatible con la vida útil real. Un taller compartido podría elevar utilización, pero añade coordinación y dependencia de terceros; no se cuenta como independencia individual. Si el margen real es cero o negativo, no hay amortización por ahorro de material. Tampoco se imprime más para justificar una inversión.

## 5. Un reciclaje muy bueno tampoco demuestra un ciclo infinito

**[P] Modelo elegido:** 10 kg iniciales, sin entrada externa, rendimiento másico constante por ciclo y sin pérdida adicional de propiedades. Se usa **M(n) = 10 × rendimientoⁿ**. No es caracterización de ningún polímero o máquina.

| Rendimiento másico elegido por ciclo | Masa que quedaría tras 10 ciclos | Aporte para mantener 10 kg constantes en cada ciclo |
|---|---:|---:|
| 95 % | 5,99 kg | 0,5 kg/ciclo |
| 90 % | 3,49 kg | 1 kg/ciclo |
| 80 % | 1,07 kg | 2 kg/ciclo |

**[I]** Aunque la geometría se pueda recuperar, las pérdidas elegidas obligan a una entrada de material si se quiere mantener el mismo inventario. Este cálculo ni siquiera penaliza contaminación o degradación química: no predice diez reciclados útiles. El rendimiento de masa no es porcentaje de autonomía doméstica. Recoger residuos nuevos de fuera reduce compras, pero conserva una dependencia exterior y de su disponibilidad.

## 6. Otra máquina abierta tampoco garantiza encaje doméstico

**[D]** Precious Plastic describe su extrusora 2.0 con 35 kg, 380 V, potencia nominal mínima de 1,5 kW y máximo de funcionamiento indicado de 4 h/día. Su introducción menciona continuidad técnica, pero no debe interpretarse como permiso para 24/7 de esta versión. Da costes orientativos de materiales en Países Bajos, sin presupuesto español actualizado. [110]

**[I]** No se extrapolan los costes de una máquina básica a una línea de filamento dimensionalmente controlado. La versión, el proceso y la instalación eléctrica importan. Esta referencia exige taller y logística; no se clasifica como conjunto transportable en moto.

**[D/P]** Su documentación identifica emisiones y necesidad de extracción. [111] Eso añade infraestructura y mantenimiento a la comparación. No se adoptan como garantía sanitaria sus afirmaciones generales sobre filtros o detectores: no se ha evaluado exposición en un lugar concreto. No se propone triturar o fundir mezclas desconocidas en una habitación.

## 7. Recursos locales: qué podría sustituir compras y qué falta

| Familia | Avance propio propuesto | Dependencia o verificación que permanece |
|---|---|---|
| Madera maciza | Reparación de muebles, mangos y piezas sencillas; uniones desmontables | Procedencia permitida, secado, estabilidad, herramientas y aptitud para el uso |
| Tierra/minerales | Investigar revestimientos o componentes adecuados al suelo y al diseño | Caracterización, agua, proceso, protección y comprobación; no toda tierra sirve |
| Plástico conocido recuperado | Separación por familia/lote y piezas no críticas seleccionadas | Limpieza, secado, transformación, calidad, pérdidas y repuestos de máquinas |
| Metal reutilizado | Preferir perfiles y piezas aprovechables antes de refundir todo | Aleación, estado, mecanizado y herramientas; no se presumen aceros de herramienta o rodamientos reproducibles |
| Fibras y textiles | Reparación y reutilización, después estudiar transformación local | Hilo, preparación, desgaste, tintes/acabados cuando procedan y trabajo |
| Vidrio y cerámica | Mantener/reutilizar lo existente; estudiar un proceso por función | Horno, energía, formulación y calidad; no sustituir un vidrio técnico por material desconocido |
| Juntas y elastómeros | Diseñar acceso y sustitución con referencias normalizadas | Química, temperatura, compatibilidad y envejecimiento; la forma sola no basta |
| Electrónica, celdas y sensores | Diagnóstico, conectores y módulos reemplazables; software local | Cadena industrial de componentes todavía sin cierre doméstico demostrado en este estudio |

Las filas son una **matriz de trabajo**, no ocho procesos ya validados ni recomendaciones para piezas críticas.

**[D]** El Wood Handbook de USDA separa propiedades, uniones, adhesivos, productos compuestos, biodeterioro y protección. [112] Su capítulo de secado explica la relación entre humedad ambiental, contenido de humedad y cambios dimensionales. [113] **[I]** Un árbol disponible no equivale a un tablero industrial o pieza estable lista para mecanizar; habría que elegir especie, acondicionamiento y diseño. No se atribuye al manual una receta para el emplazamiento aún desconocido.

**[D limitado]** El extracto indexado de Auroville señala que no todos los suelos sirven para bloques y que la estabilización depende del suelo y del proyecto. [114] La apertura recibió 403; no se elude ni se presenta su documento como revisado íntegramente. No se transfieren sus proporciones o datos antiguos de India al suelo de una futura finca española.

**[D/A]** El registro Michigan Tech de un artículo de 2013 describe una impresora metálica experimental basada en soldadora comercial y movimiento abierto. [115] Otro registro del mismo título muestra aviso de retirada; no se ha aclarado si se refiere al depósito duplicado o al artículo, y no se afirma retractación científica. [116] Se deja como antecedente a verificar, sin precio vigente o selección de compra. **[I]** Automatizar la deposición no fabrica alambre, gas, metales aleados o un sistema completo de verificación.

## 8. La metrología también forma parte de la autonomía

**[D]** El catálogo Mitutoyo publica resolución y exactitud como magnitudes distintas. [117; extracto indexado] **[I]** Que una pantalla muestre centésimas no demuestra que la pieza tenga esa exactitud. Una máquina abierta o una IA no suprimen la necesidad de referencias, tolerancias y comprobación del resultado.

**[P]** Para cada repuesto candidato: identificar función y consecuencia de fallo; conservar muestra original y cotas; elegir material/proceso; medir dimensiones y funcionamiento; registrar tiempo y fallos; autorizar únicamente el uso que la evidencia sostenga. Comenzar por útiles y carcasas no críticas. No hay aquí ensayos estructurales, eléctricos, alimentarios o de presión superados.

**[P]** Registrar además lo que desgasta el taller: filos, boquillas, correas, guías, rodamientos, lubricantes, resistencias, sensores y medios de medición. Un repuesto propio acerca a la meta solo si no consume una cadena de equipos cuya renovación queda ignorada. Conservar manuales y archivos sin nube es útil, pero no conserva indefinidamente el ordenador físico.

## 9. Qué avanzar ahora y cómo decidir cuándo cambia la conclusión

**[P] Orden de trabajo:**

1. Inventariar piezas reales que se rompen o consumen; estimar cantidad anual y materiales. No comprar una máquina por una lista genérica de posibilidades.
2. Comparar reparación, pieza normalizada y fabricación propia para esas mismas funciones, incluyendo trabajo y mantenimiento.
3. Construir un expediente reproducible de un repuesto no crítico, con CAD, material, proceso, medidas y resultado de uso. Esa será una unidad medible de autonomía; todavía no hay pieza seleccionada o fabricada en esta entrega.
4. Evaluar reciclaje cuando exista corriente de material identificada y consumo suficiente. Comprobar salida útil y coste completo, no solo kilos que atraviesan la extrusora.
5. Estudiar recursos renovables locales y materiales procesados por separado. Los residuos industriales disponibles hoy no acreditan suministro independiente a largo plazo.

**[A]** No hay datos para fechar una microfábrica que reproduzca todos sus componentes, ni para afirmar que esperar un número de años lo resolverá. Una mejora relevante sería una cadena demostrada con materiales accesibles, repuestos reproducibles, calidad suficiente y mantenimiento asumible. Un anuncio o un CAD nuevo no cumplen por sí solos esos requisitos.

**Siguiente bloque independiente:** IA local, documentación y control sin nube, junto con el mantenimiento del hardware que los ejecuta. Se conservará la distinción entre software libre, modelo reutilizable y ordenador fabricable. La meta completa continúa abierta y no hay compras o instalaciones.

## 10. Elección provisional del taller, actualizada con la consulta del propietario

**[P] Arquitectura elegida para comparar, no autorización de compra:** impresión FDM de diseño abierto y componentes comunes, acompañada por moldes y reparación convencional. Primero se definirán piezas y requisitos; siguen pendientes modelo, cesta instalada y comparación de coste y mantenimiento. No se denomina fábrica autosuficiente al conjunto.

| Función | Ruta prioritaria de estudio | Dependencia que permanece |
|---|---|---|
| Carcasas, útiles y algunos repuestos rígidos | FDM con material elegido para la función | Filamento, energía, máquina, repuestos y verificación |
| Piezas flexibles seleccionadas | Molde y colada compatibles; comparar con impresión directa cuando sea útil | Elastómero, preparación, curado, defectos y vida del molde |
| Piezas grandes o con requisitos que el plástico no cubra | Madera y perfiles/metales existentes, trabajados con herramientas apropiadas | Estado/material, fijaciones, herramientas, medidas y espacio |
| Recuperación de polímeros | Selección por familia y lote antes de adquirir línea de transformación | Flujo de residuo conocido, rendimiento útil y demanda suficiente |
| Producción biológica o síntesis propia | Investigación por material y función | Insumos, acondicionamiento, propiedades, mantenimiento y reproducibilidad |

**[D/I]** La documentación de Voron recomienda ABS/ASA para sus piezas funcionales y distingue excepciones; no considera PLA o PETG sustitutos generales para ese entorno. [302] Ese ejemplo muestra por qué “imprimible” y “repuesto válido” son decisiones distintas. No se traslada automáticamente la elección de material de una impresora a todos los aparatos de una vivienda.

El [anexo de juntas](JUNTAS_BOMBAS_FABRICACION_ELASTOMEROS.md) conserva la evidencia de moldeo, las limitaciones de compatibilidad y un ejemplo geométrico no crítico. La documentación comercial de moldeo [255] no demuestra que FDM sirva para cualquier molde o precisión, ni abre la formulación de la silicona. Se comparará acabado y material por pieza antes de escoger otra máquina.

**[I]** Fabricar la forma no equivale a sintetizar el material: imprimir plástico comprado o colar silicona comprada reduce dependencia de ciertos recambios, pero conserva la del insumo. La elección se revisará si una tecnología ofrece ventaja demostrada para la misma pieza y servicio. No se recomienda ahora una línea completa de reciclaje ni un cabezal especializado sin esa comparación.
