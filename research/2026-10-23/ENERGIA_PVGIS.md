# Energía: primera comparación reproducible · 23/10/2026

**Estado:** cálculo con el servicio público PVGIS del Joint Research Centre de la Comisión Europea, sin medidas propias de una instalación, compras ni simulación de una vivienda real. Se guardan respuestas originales, fecha y URL exacta de cada consulta. Este anexo avanza la siguiente unidad de trabajo descrita en el informe; la investigación sigue abierta.

## 1. Referencia geográfica y alcance

Se usan coordenadas redondeadas de Zaragoza, **41,65 / -0,89**, como referencia climática urbana general. No son el emplazamiento de una finca elegida ni identifican una vivienda. Las respuestas declaran datos meteorológicos de 2005-2023, radiación PVGIS-SARAH3 y horizonte del terreno calculado por el servicio.

Se comparan dos orientaciones para **1 kWp**: sur a 35 grados de inclinación y noroeste a 299 grados de brújula en montaje vertical. En PVGIS los azimuts se expresan respecto al sur: 0 y 119 grados respectivamente. Ambos casos usan módulo de silicio cristalino, montaje libre y parámetro de pérdidas del sistema del 14 %. El modelo aplica también sus otros efectos; no se interpreta el 14 % como única pérdida total.

**No se han modelado** muros, voladizos, barandillas, sombras de edificios, vegetación, suciedad real ni posición concreta del panel. La comparación cambia orientación e inclinación a la vez; no aísla solo el efecto del azimut. El segundo caso no predice la producción real de un balcón. Son resultados de potencial de generación de PVcalc, no electricidad garantizada para consumos después de almacenamiento.

## 2. Variación por estación

| Mes | Sur 35°, kWh/día por 1 kWp | Noroeste vertical, kWh/día por 1 kWp |
|---|---:|---:|
| Enero | 3.24 | 0.48 |
| Febrero | 4.25 | 0.85 |
| Marzo | 4.63 | 1.29 |
| Abril | 4.91 | 1.82 |
| Mayo | 5.16 | 2.21 |
| Junio | 5.16 | 2.28 |
| Julio | 5.43 | 2.43 |
| Agosto | 5.36 | 2.08 |
| Septiembre | 4.86 | 1.50 |
| Octubre | 4.10 | 0.95 |
| Noviembre | 3.37 | 0.57 |
| Diciembre | 2.83 | 0.40 |

Producción anual modelada: **1621.24 kWh** en sur 35° y **513.95 kWh** en noroeste vertical, por 1 kWp. Son medias históricas modeladas, no mínimos diarios.

**[I] Consecuencia:** antes de buscar un panel más caro hay que resolver ubicación y orientación. Por escalado de potencia, 100 Wp darían en diciembre unos **283 Wh/día** en el primer escenario y **40 Wh/día** en el segundo, antes de añadir almacenamiento y sin las sombras cercanas omitidas. No es una medida de un panel plegable, no garantiza carga continua USB y no sirve para escoger una estación de energía de vivienda.

## 3. Por qué la media anual no basta

Se consultó también el modelo separado **SHScalc** con dos escenarios de exploración: 3.000 Wp al sur a 35°, consumo de 5.000 Wh/día y perfil horario por defecto del servicio, batería nominal de 5.000 o 15.000 Wh y límite de descarga al 20 %. El consumo de 5 kWh/día es una hipótesis, **no una estimación de las necesidades del propietario ni garantía de confort**. No se ha construido un perfil de cocina, calefacción, agua caliente, taller o IA.

SHScalc utiliza su propio modelo de sistema aislado; no se extrapola sin más el parámetro del 14 % de PVcalc ni se presupone que reproduce una batería comercial concreta.

| Escenario | Días en que la batería alcanza el límite inferior de carga, según modelo | Diciembre |
|---|---:|---:|
| 3 kWp + batería nominal 5 kWh | 13.98 % | 43.80 % |
| 3 kWp + batería nominal 15 kWh | 2.09 % | 11.38 % |

Se usa la variable **f_e** y su definición de los metadatos conservados. Llegar al límite de carga no equivale a un día entero sin suministro ni indica por sí solo duración o gravedad del déficit. La simulación con más almacenamiento mejora este indicador, pero ninguno de los dos escenarios demuestra suministro ininterrumpido. No se selecciona con ello capacidad de batería, inversor, cableado o protecciones.

**[I] Resultado que cambia la decisión:** aunque el balance energético medio parezca abundante, puede haber periodos con reserva agotada. Para buscar autonomía real hace falta estudiar las secuencias de días desfavorables, la demanda horaria y la recuperación, además de medias anuales. Los datos históricos no garantizan el futuro.

## 4. Reposición y comodidad

**[P]** El siguiente presupuesto energético deberá incluir generación, estructura, cableado, regulación, almacenamiento, inversor si hace falta, consumos propios, protección, mantenimiento y reposición. Se compararán demandas reducidas mediante aislamiento y hábitos con aumentos de panel o batería; no se equiparará menos demanda con perder confort sin analizarlo.

**[A]** Todavía no hay precio completo: faltan la vivienda, demanda térmica, perfil real, autonomía deseada ante meteorología adversa, capacidades y piezas concretas. Los precios de kits de impresión o un controlador no resuelven este presupuesto. Tampoco se supone reparabilidad interna por poder cambiar un módulo completo.

**Pendiente:** perfiles horarios explícitos para varios niveles de uso; comparación de estrategias con y sin almacenamiento; fichas de mantenimiento y repuestos de equipos concretos; precios completos por escenario; comparación de tecnologías térmicas para invierno y agua caliente. No se recomienda compra a partir de estas cuatro consultas.

## 5. Fuentes y datos originales

- [52 · JRC: API, parámetros y unidades de PVGIS](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/using-pvgis-5/api-non-interactive-service_en).
- [53 · JRC: PVcalc, alcance de generación y salidas](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/using-pvgis-5/pvgis-5-tools/grid-connected-pv_en).
- Datos propios de esta consulta al servicio público, sin alteración de la respuesta dentro del campo `respuesta`:
  - [Sur 35°](datos/pvgis_sur35.json)
  - [Noroeste vertical](datos/pvgis_noroeste_vertical.json)
  - [Aislada, batería 5 kWh](datos/pvgis_aislada_3kw_5000wh.json)
  - [Aislada, batería 15 kWh](datos/pvgis_aislada_3kw_15000wh.json)

En cada archivo se conserva la URL reproducible. La publicación de estos resultados no implica que se haya instalado PVGIS en el PC, ni que JRC valide nuestro diseño futuro.
