# Alimentación, conservación y herramientas abiertas · 23/10/2026

**Estado:** estudio y escenarios, sin huerto productivo medido, cosechas propias ni validación de conservación. Continúa el objetivo de producir necesidades y reducir compras sin dar por alcanzada una dieta autónoma. [D] documentado; [I] inferido; [P] propuesto; [A] pendiente. Referencias en FUENTES.md.

## 1. Qué significa cubrir comida

**[P]** Medir por separado cantidad cosechada, parte que se puede comer, energía alimentaria, diversidad, conservación, insumos, agua y trabajo. Las ventas de excedentes se calcularán después de descontar necesidades propias, semilla, pérdidas, preparación y obligaciones aplicables. Un porcentaje de kilos de hortalizas no es un porcentaje de dieta.

**[I]** Una cosecha abundante puede aportar frescos y ahorro sin cubrir calorías anuales. Por otra parte, cubrir una cifra de calorías con un solo alimento no garantiza alimentación adecuada. No se propone aquí una dieta, una necesidad personal de energía ni un menú de un único cultivo.

## 2. Escenario contable: 100 m² de patata, no pronóstico de producción

**[P] Supuestos elegidos:** una cosecha anual; rendimientos de 1, 2 y 3 kg/m²; 80 % de la cosecha disponible como porción comestible tras reservar o descartar lo que corresponda. Ese 80 % no es una medición ni una tasa agronómica recomendada. La referencia contable de comparación es 2.000 kcal/día × 365 = 730.000 kcal; no es una prescripción nutricional para el propietario.

Para convertir masa comestible se usa **880 kcal/kg**: la ficha Patata alojada por MAPA muestra 88 kcal por 100 g comestibles. [79] Se consultó su extracto indexado; el PDF no estuvo accesible para lectura integral. Su composición remite a tablas de 2013. No se toman de esa ficha recomendaciones personales ni rendimientos de campo.

| Rendimiento hipotético | Cosecha en 100 m² | Disponible comestible, supuesto 80 % | kcal contables | Fracción de la referencia anual |
|---|---:|---:|---:|---:|
| 1 kg/m² | 100 kg | 80 kg | 70.400 | 9,6 % |
| 2 kg/m² | 200 kg | 160 kg | 140.800 | 19,3 % |
| 3 kg/m² | 300 kg | 240 kg | 211.200 | 28,9 % |

[Supuestos y resultados completos](datos/agua_alimentacion_escenarios_2026-10-23.json).

**[I]** Incluso el escenario más productivo elegido aporta aproximadamente 29 % de esa referencia de energía. No es 29 % de autosuficiencia personal, de nutrientes o de dinero ahorrado. Se podrían cambiar los resultados con otra cosecha o cultivo, pero habría que medir las nuevas condiciones; no se multiplican cosechas automáticamente por disponer de un invernadero.

**[P]** La planificación debe incorporar rotaciones, suelo, semillas/plantación, fertilidad, plagas, superficie realmente útil y conservación. Los caminos, zonas de trabajo, compost y almacenamiento también ocupan espacio. No se presenta una superficie mínima de finca para alimentar a una persona a partir de este ejemplo.

## 3. Qué desarrollar antes de comprar un robot agrícola

**[P]** Empezar por una unidad de cultivo manejable, registro de agua y cosecha aceptada, y un modo sencillo de operar el riego. Medir trabajo en preparar, plantar, revisar, cosechar y conservar. Solo automatizar después tareas repetitivas que demuestren utilidad. La IA puede ayudar a analizar el registro; no acredita una cosecha que no se ha obtenido.

| Herramienta o recurso | Apertura comprobada | Uso y límite para nuestro objetivo |
|---|---|---|
| farmOS | Aplicación publicada bajo GPL-2.0; admite alojamiento propio [77] | Registro y planificación; no produce comida ni elimina hardware, energía o mantenimiento |
| Mycodo | Software GPL-3.0 o posterior para monitorización y regulación [78] | Puede integrar sensores y salidas; no convierte sondas, bombas o relés en hardware fabricable desde recursos locales |
| OpenSprinkler / FarmBot, catálogo inicial | Documentación ya incluida en [13,14] | Comparar alcance real y coste completo con una alternativa más sencilla; no se añade hardware en esta campaña |
| L’Atelier Paysan, plantoir à poireaux revisado | Publica planos con CC BY-NC-SA [84] | Recurso de autoconstrucción con restricción comercial; no clasificarlo como hardware abierto estricto ni extender esa licencia a toda herramienta sin mirar la revisión |
| CAWST, manual de bioarena | Documentación revisada CC BY 3.0 [75] | Ejemplo de documentación adaptable para una función concreta de agua, con límites; no resuelve toda la cadena alimentaria |

No se instala farmOS o Mycodo en el PC ni se compran sensores. Antes de elegirlos debe justificar el registro qué función falta y si un sistema más sencillo ya la cubre.

**[P] Pendiente de comparación:** suelo y riego sencillo frente a hidroponía o acuaponía, contando entradas de materiales, agua, energía, nutrición vegetal y tareas. Una recirculación no se puntuará como ciclo cerrado sin un balance de entradas y salidas. La página FAO de acuaponía consultada rechazó el acceso completo; no se ha eludido ni se usa como evidencia de prestaciones.

## 4. Conservar también consume recursos

**[P]** Escoger método por alimento, cantidad, fecha de consumo y condiciones del lugar. La comparación debe incluir equipos, envases, agua y energía de preparación, pérdidas y mantenimiento. Reducir cosechas que no podamos conservar puede dar mejor resultado que fabricar más maquinaria.

| Ruta a estudiar | Lo que podría aportar | Dependencias y cuestión pendiente |
|---|---|---|
| Almacenamiento fresco o seco apropiado a cada producto | Pocas transformaciones y posible uso de condiciones del edificio | Temperatura, humedad, plagas y duración por cultivo; no equivale a refrigeración de todos los alimentos |
| Secado solar controlado y documentado | Aprovechar calor solar para ciertos lotes | Tiempo meteorológico, flujo de aire, materiales, limpieza y aceptación del resultado |
| Deshidratación eléctrica | Condiciones de operación más controlables | Electricidad, calentador, ventilador, control y repuestos; medir energía por kg aceptado |
| Congelación | Ruta que debe compararse para alimentos apropiados | Frío continuo, compresor, almacenamiento eléctrico y recuperación ante averías |
| Conservas con procedimiento validado | Conservación posterior sin frío para productos y procesos adecuados | Agua y calor, envases/cierres y control del proceso; no basta un tarro cerrado |

**[D]** NCHFP distingue el secado exterior de frutas en condiciones apropiadas de los casos para los que recomienda condiciones controladas; no recomienda secado al aire libre de carnes o verduras, salvo la excepción que indica para judías secadas en la planta. [81] **[I]** Un secador solar propio tiene que demostrar sus condiciones; no se acepta como sustituto universal de un deshidratador controlado.

**[D]** AESAN explica que las conservas mal elaboradas pueden causar botulismo y que la toxina no se detecta por el aspecto, olor o sabor. [80] **[P]** Para un lote concreto se utilizará un proceso validado apropiado al alimento y equipo; esta campaña no define recetas ni tiempos de tratamiento. Probar el sabor no será criterio de aceptación.

## 5. Un precio comercial para contrastar fabricación propia

**[D]** La ficha de Leroy Merlin para H.Koenig DSY900 muestra 129,90 EUR, vendido por HOME HOME, con campaña visible de 05 septiembre a 05 diciembre y anuncio de envío gratuito. [88] No se ha fijado destino, comprobado factura o probado su uniformidad, rendimiento o reparabilidad interna. No se declara superior a una alternativa abierta.

La ficha anuncia 650 W. **[P]** Como simple escala de energía, ocho horas constantes a esa potencia serían 5,2 kWh; no es una receta de secado ni consumo real medido. El ciclo del termostato, producto y carga cambian el consumo. No se infiere duración útil ni euros por kilo a partir de la potencia nominal.

**[I]** El ahorro de fabricar un secador propio no está demostrado sin presupuesto de materiales aptos, fuente editable, instrumentación, limpieza, duración y resultado equivalente. Tener madera o sol disponibles no acredita por sí solo el conjunto para alimentos.

**[D/P]** Appropedia reúne documentación y declara políticas de licencias con excepciones; su material sobre secado se conserva como referencia histórica para investigar diseño, no como validación sanitaria ni kit terminado. [82,83] Antes de reproducir un diseño se verificará la licencia de la página, planos e imágenes concretos. No se trasladan automáticamente indicaciones antiguas a un lote actual.

## 6. Trabajo y coste recurrente que debemos hacer visibles

**[P]** Registrar por lote y temporada: semilla/plantación, sustrato o suelo, entradas de nutrientes, agua, energía, horas de trabajo, mantenimiento, consumibles, merma y alimento realmente disponible. Conservar un balance de nutrientes y materiales antes de llamar cerrado al ciclo de compostaje o reciclaje. Reducir compras es un resultado valioso; ausencia completa de entradas todavía no se ha demostrado.

**[P]** Documentar carcasas, soportes, uniones, útiles y acceso de limpieza que podamos mejorar con CAD y fabricación propia. Para elementos de contacto alimentario se comprobará material y proceso, no solo geometría. El control debe permitir intervención manual y registrar fallos; no hay aquí una nueva automatización funcionando.

## 7. Decisiones que deja esta entrega

- El abastecimiento de agua para cultivar se calcula junto con el de casa; no después de comprar el huerto automatizado.
- Se medirá comida utilizable y energía/nutrición por separado del peso cosechado y del dinero de supuestas ventas.
- La primera automatización candidata será la que reduzca trabajo observado con poca dependencia nueva; no se selecciona un robot por la promesa de autosuficiencia.
- Se comparan conservación y tamaño de cultivo antes de aumentar producción; no se asume que cualquier secado o conserva sea aceptable.
- No se ha comprado nada ni demostrado una dieta autónoma. Siguen pendientes rendimientos, trabajo, superficie, entradas y condiciones reales.

**Siguiente bloque independiente:** criterios para vivienda y emplazamiento, saneamiento y gestión de materiales/residuos, cruzados con agua y energía. Continúan abiertas las líneas de fabricación, IA local y reparación; no se declara terminado el estudio general.
