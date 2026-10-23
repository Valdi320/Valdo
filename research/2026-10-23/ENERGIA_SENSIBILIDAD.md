# Energía: sensibilidad a paneles, batería y horarios · 23/10/2026

**Avance respecto de ENERGIA_PVGIS.md:** seis consultas adicionales a SHScalc, sumadas a los dos escenarios aislados anteriores. Son ocho escenarios comparativos, no ocho viviendas diseñadas. [D] significa resultado devuelto por el modelo; [I] es interpretación propia; [P] es propuesta pendiente. No son mediciones del propietario ni certificados de disponibilidad.

## 1. Condiciones conservadas

Referencia climática general de Zaragoza: 41,65 / -0,89, base PVGIS-SARAH3 con datos 2005-2023, paneles al sur a 35 grados, horizonte del terreno y límite de descarga al 20 %. Se cambian únicamente potencia, batería, demanda diaria o distribución horaria indicadas. Se conserva el modelo propio de SHScalc; no se le aplica por nuestra cuenta el 14 % de otro cálculo.

**[D]** El servicio admite perfil horario de consumo y devuelve el porcentaje de días en que la batería se vació, `f_e`. En las consultas personalizadas, sus metadatos confirman `user-defined`; en las demás, `default`. [52] Se conserva la URL de cada consulta y su respuesta original en los archivos de datos. No se ha seleccionado una batería comercial en el modelo.

## 2. Resultados comparables

La segunda capacidad de cada fila es batería **nominal**. El porcentaje indica días en que se llega al límite inferior de carga, no porcentaje de horas sin suministro, energía no atendida ni días completos a oscuras.

| Potencia / batería / demanda | Perfil | Días con límite inferior, serie histórica | Diciembre |
|---|---|---:|---:|
| 3 kWp / 5 kWh / 5 kWh diarios | Por defecto | 13.98 % | 43.80 % |
| 6 kWp / 5 kWh / 5 kWh diarios | Por defecto | 4.89 % | 19.52 % |
| 3 kWp / 15 kWh / 5 kWh diarios | Por defecto | 2.09 % | 11.38 % |
| 6 kWp / 15 kWh / 5 kWh diarios | Por defecto | 0.32 % | 1.02 % |
| 6 kWp / 15 kWh / 15 kWh diarios | Por defecto, demanda elevada | 22.54 % | 57.89 % |
| 3 kWp / 5 kWh / 5 kWh diarios | Diurno propuesto | 7.19 % | 27.33 % |
| 3 kWp / 5 kWh / 5 kWh diarios | Nocturno propuesto | 53.98 % | 100.00 % |
| 3 kWp / 5 kWh / 2 kWh diarios | Por defecto, menor demanda | 0.23 % | 0.51 % |

**[I]** A demanda y perfil constantes, duplicar paneles manteniendo 5 kWh de batería mejora el indicador de 13,98 % a 4,89 %. Mantener paneles y triplicar la batería lo mejora a 2,09 %. Hacer ambas cosas da 0,32 %, todavía distinto de cero. La comparación identifica sensibilidad, no una inversión óptima: faltan costes completos y consumo real.

**[I]** Al elevar la demanda de 5 a 15 kWh/día, incluso el caso de 6 kWp y 15 kWh de batería vuelve a 22,54 %. Esta demanda se mantiene constante todo el año en el escenario: no es una simulación térmica estacional ni una estimación de una vivienda. Solo muestra cómo cambia el resultado al cambiar la necesidad que queremos cubrir.

## 3. Dos perfiles sintéticos, a igual energía diaria

**Diurno propuesto:** 1 % del consumo en cada hora como base; se añaden 10 puntos porcentuales por hora entre las 10 y las 15, y 4 puntos a las horas 9, 16, 17 y 18. Resultado: 66 % entre 10 y 15, 20 % en las otras cuatro horas y 14 % en el resto.

**Nocturno propuesto:** la misma distribución trasladada ocho horas: 66 % entre 18 y 23, 20 % a las horas 17, 0, 1 y 2, y 14 % en el resto. Ambos vectores suman 100 %. Se especifican como hora local estándar en el sentido de la documentación del servicio, sin cambiar con el horario de verano. No son registros de una familia real.

**[I]** Con 3 kWp, batería nominal de 5 kWh y demanda de 5 kWh/día, estos perfiles producen 7,19 % y 53,98 % respectivamente. No demuestra que el propietario pueda mover todos esos consumos; sí justifica investigar el desplazamiento de bombeo, taller, cargas informáticas y calentamiento hacia producción solar. La comida, frío y comodidad no se posponen arbitrariamente para mejorar un indicador.

**[I]** El caso de demanda de 2 kWh/día reduce el indicador a 0,23 %. No se presenta como un nivel de confort suficiente ni como electricidad ilimitada; antes de aceptar esa demanda hay que comprobar qué necesidades quedarían fuera.

## 4. Qué no permite afirmar

- No garantiza continuidad futura: solo estudia el modelo con la meteorología histórica disponible.
- No incluye sombras cercanas, estado real de batería, envejecimiento medido, consumos propios de equipos concretos ni averías.
- No representa potencia instantánea, arranque de motores o compatibilidad entre inversor, controladores y batería.
- No convierte la frecuencia `f_e` en cobertura energética ni en duración del corte. No se usa `E_miss` para calcular un coste o una cobertura sin aclarar antes su agregación.
- No compara el coste total de una instalación de 3 o 6 kWp. El presupuesto parcial adjunto es una cesta de referencias, no el sistema que ha ejecutado PVGIS.

**Decisión [P]:** medir consumo y separar cargas esenciales de flexibles antes de comprar almacenamiento. Comparar conjuntamente demanda, horarios, paneles y batería. No seleccionar únicamente por producción media anual ni por una cifra de capacidad.

## 5. Datos reproducibles

- [3 kWp / 5 kWh / 5 kWh diarios, perfil por defecto](datos/pvgis_aislada_3kw_5000wh.json).
- [6 kWp / 5 kWh / 5 kWh diarios, perfil por defecto](datos/pvgis_sensibilidad_6kw_5kwh_5diario.json).
- [3 kWp / 15 kWh / 5 kWh diarios, perfil por defecto](datos/pvgis_aislada_3kw_15000wh.json).
- [6 kWp / 15 kWh / 5 kWh diarios, perfil por defecto](datos/pvgis_sensibilidad_6kw_15kwh_5diario.json).
- [6 kWp / 15 kWh / 15 kWh diarios, perfil por defecto, demanda elevada](datos/pvgis_sensibilidad_6kw_15kwh_15diario.json).
- [3 kWp / 5 kWh / 5 kWh diarios, perfil diurno propuesto](datos/pvgis_sensibilidad_3kw_5kwh_5diurno.json).
- [3 kWp / 5 kWh / 5 kWh diarios, perfil nocturno propuesto](datos/pvgis_sensibilidad_3kw_5kwh_5nocturno.json).
- [3 kWp / 5 kWh / 2 kWh diarios, perfil por defecto, menor demanda](datos/pvgis_sensibilidad_3kw_5kwh_2diario.json).

Fuente metodológica: [JRC, API PVGIS](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/using-pvgis-5/api-non-interactive-service_en). [52] No se han instalado herramientas ni realizado ensayos de hardware para estas consultas.
