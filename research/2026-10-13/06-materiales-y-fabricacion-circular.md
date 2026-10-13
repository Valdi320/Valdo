# 06 — Materiales locales, reciclaje real y microfábrica de múltiples procesos

## 1. Hallazgo que corrige un optimismo peligroso: el material reciclado pierde propiedades

**[D]** Un trabajo experimental sobre PLA reciclado identifica diferencias importantes según su **procedencia**: PLA de una fuente conocida soportó más ciclos de reextrusión sin degradación significativa que residuos mezclados [estudio de 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/). Otros estudios muestran escisión de cadenas por temperatura/oxidación y degradación por envejecimiento [PLA y múltiples ciclos](https://www.mdpi.com/2073-4360/14/12/2407); [durabilidad de PLA reciclado](https://www.sciencedirect.com/science/article/pii/S014294182500296X).

**Consecuencia [P]:** nada de un bucle de reciclado «infinito» que devuelva material idéntico. Identificar polímero/lote, registrar historia térmica, ensayar después de cada ciclo y limitar usos estructurales según resultados.

## 2. No buscar un único material universal: conservar funciones químicas separadas

| Material/arquitectura | Usos candidatos | Límites que ensayar |
|---|---|---|
| Celulosa y fibras | refuerzo, carcasas ligeras | humedad, creep, variabilidad |
| Lignina | formulaciones de refuerzo/relleno, propiedades térmicas específicas | dispersión, estabilidad, olor |
| PHA | piezas moldeables en formulaciones seleccionadas | coste, secado, degradación ambiental real |
| Almidón | mezclas no críticas | absorción de agua, envejecimiento |
| PLA reciclable | prototipos y piezas no críticas con ensayo | resistencia al calor, envejecimiento y recircularidad |
| PETG/otros polímeros durables | carcasas/utillajes apropiados | propiedades y reciclaje por familia |
| Acero/aluminio recuperado | cargas, tornillos, conductividad | mecanizado, disponibilidad, clasificación |
| Elastómeros | juntas, agarres y aislamiento vibratorio | adherencia, envejecimiento, reciclaje separado |
| Celosías/auxéticos/giroides | rigidez/flexión/amortiguación por geometría | anisotropía, fatiga, puntos de rotura |
| Cerámicos/minerales | aislamiento y cargas particulares | fragilidad, hornos y energía |

**Biobasado NO implica biodegradable, compostable o reutilizable.** Referencia de definiciones y orientación: [Comisión Europea](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en).

## 3. Fermentar polímeros no es una impresora doméstica barata

**[D]** La revisión de 2025 sobre PHA destaca el peso económico y ambiental del **procesamiento posterior de extracción/purificación**, el efecto de escala y la valorización de residuos [Journal of Cleaner Production](https://www.sciencedirect.com/science/article/pii/S0959652625016075). Aunque microorganismos pueden producir PHA, **no hay evidencia de que hogares puedan producirlo desde desechos sin equipamiento, seguridad y energía considerables**.

**[P]** Empezar con granulados/filamentos comerciales de procedencia conocida y experimentar con formulaciones de origen local **en entorno adecuado**; aplazar bioprocesos a colaboración especializada, no a la primera estación doméstica.

## 4. Microfábrica más útil que impresora «que haga todo»

**[D]** [Precious Plastic](https://www.preciousplastic.com/machines/basic) ofrece diseños replicables de trituradora y otras máquinas para reciclaje local; su documentación muestra que **triturar, clasificar y preparar el material** son procesos industriales a pequeña escala, no pasos sin riesgo [Shredder](https://www.preciousplastic.com/our-solutions/shredder).

**[P]** Arquitectura de estaciones separadas:
1. **Recepción y trazabilidad:** identificación de polímero, lote, origen, contenido de humedad y contaminación.
2. **Clasificación, limpieza y secado:** evitar mezclas de familias incompatibles.
3. **Recuperación/transformación:** triturado/extrusión/inyección en entorno controlado, con protección de cuchillas/calor/emisiones.
4. **Fabricación aditiva:** FFF/FDM multimaterial **cuando los materiales sean compatibles**; no asumir que una boquilla sirve para metales, cerámicas, PHA y conductores.
5. **Mecanizado/montaje:** inserts, taladros/roscas, conectores, fijaciones y mecanizado limitado.
6. **Metrología y ensayo:** muestras de lote, cotas, resistencia/fatiga cuando proceda, inspección de montaje.
7. **Inventario y fin de vida:** recuperar/limpiar/reprocesar o derivar a reciclaje externo especializado.

**Ventaja de usar granulado directo:** puede evitar una etapa de reprocesado como la fabricación de filamento, aunque exige maquinaria diferente y control del caudal; investigaciones de impresión con granulado de PLA reciclado exploran precisamente esa alternativa [estudio](https://www.sciencedirect.com/science/article/pii/S2589234723003238).

## 5. Pasaporte de material y ensamblaje

**[P]** Cada pieza fabricada debería incluir:
- ID y revisión de geometría;
- archivos CAD y receta de fabricación, material/resina, lote, fecha y proveedor;
- número de ciclos de procesado y condiciones (temperatura, humedad);
- dirección de capas/infills si es impresa, orientación y ensayos;
- uso autorizado (prototipo, funcional no crítico, estructural solo ensayado);
- fijaciones que permiten desmontaje, incompatibilidades y piezas comerciales;
- fin de vida: reutilizar/reparar/reciclar/gestionar externamente;
- registros de inspecciones, roturas y reparaciones.

**[D]** El [Reglamento UE 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng) crea el marco europeo de pasaporte digital de producto y requisitos de ecodiseño mediante actos delegados por grupos de producto; **no obliga sin más a que una pieza doméstica imprimida tenga en 2026 un DPP legalmente conforme**. Adoptaremos un «pasaporte FDAA» abierto interno, útil incluso antes de los estándares definitivos.

## 6. Auditoría ambiental real: medir ciclo de vida y alternativas

**[P]** Para cada pieza funcional compararemos **tres decisiones**:
1. reparar pieza original sin imprimir;
2. comprar repuesto duradero estandarizado;
3. fabricar repuesto local con material virgen o recuperado.

Registrar al menos: electricidad de escaneo+IA+fabricación+posprocesado, cantidad de material, agua/químicos, transporte evitado, tasa de fallos, tiempo de uso estimado y reciclaje final. Si fabricar local produce más residuos por fallos o demanda tratamiento peligroso, la opción más ecológica podría ser **comprar un repuesto**.

**Estándar de terminología:** [ISO/ASTM 52900:2021](https://www.iso.org/standard/74514.html) para procesos de fabricación aditiva; consultar además métodos de caracterización/ensayo específicos antes de afirmar calidad.

## 7. Experimentos prioritarios con bajo riesgo

**M-01:** separar residuos PLA conocidos, fabricar probetas de al menos dos historiales de reextrusión con medidas y comparar deformación/resistencia; *usar instalaciones y ventilación adecuadas*, no trituradora improvisada.

**M-02:** medir cómo cambian dimensiones, rigidez, humedad y fatiga de piezas impresas con diferentes orientaciones/celosías de **un mismo lote**; así separaremos efecto geométrico de químico.

**M-03:** diseñar una carcasa de módulo robótico que pueda abrirse repetidas veces sin perder tornillos/roscas; registrar número de ciclos de reparación.

**M-04:** usar el mismo CAD y tres rutas (compra, impresión local, reparación del original), y documentar coste/energía/esperanza de vida bajo hipótesis explícitas, sin declarar ganador anticipado.

**M-05:** simular una receta circular de material con reciclado y trazabilidad; **no empezar con fermentadores**.

**Fuentes:** [Comisión Europea](https://environment.ec.europa.eu/topics/plastics/biobased-biodegradable-and-compostable-plastics_en), [Precious Plastic](https://www.preciousplastic.com/machines/basic), [PLA conocido vs mixto](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/), [degradación del PLA](https://www.mdpi.com/2073-4360/14/12/2407), [PLA y envejecimiento](https://www.sciencedirect.com/science/article/pii/S014294182500296X), [PHA downstream](https://www.sciencedirect.com/science/article/pii/S0959652625016075), [reciclaje de granulado](https://www.sciencedirect.com/science/article/pii/S2589234723003238), [ESPR](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng), [ISO/ASTM](https://www.iso.org/standard/74514.html).
