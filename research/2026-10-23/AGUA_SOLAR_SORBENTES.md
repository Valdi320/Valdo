# Agua del aire con calor solar: materiales, escala y fabricación · 23/10/2026

**Decisión provisional:** conservar la sorción solar como investigación complementaria; no elegir todavía una máquina doméstica ni sintetizar material. El gel de sílice merece comparación por disponibilidad, y MOF-303 por rendimiento en aire seco y síntesis publicada a escala de kilogramos. Ninguno acredita suministro anual potable, fabricación local completa o ausencia de reposición.

Convenciones: **[D]** documentado; **[I]** inferencia o cálculo propio; **[P]** propuesta; **[A]** pendiente. Fuentes 303–311 en [FUENTES.md](FUENTES.md). [Datos y límites de los cálculos](datos/agua_solar_sorbentes_2026-10-23.json). Amplía el [anexo general de agua atmosférica](AGUA_ATMOSFERICA_FABRICACION.md).

## 1. Dos materiales, dos cadenas distintas

**[D]** El resumen del experimento de Gentile y colaboradores (2022) comunica gel de sílice convencional, **1,5–3,3 L/día por m² de captación solar** y **1–3 kWh térmicos/L**, con regeneración máxima de 57 °C. Reproduce condiciones de clima seco, con ambiente de 20–35 °C y punto de rocío de 2–8 °C. El texto íntegro del editor devuelve 403: no se han auditado sus métodos ni se dispone aquí de la referencia exacta del gel. [303]

**[D]** Song y colaboradores (2023) midieron **114–210 g de agua por kg de MOF y día** en Death Valley y 285 en Berkeley. Los métodos del dispositivo incluyen MOF-303 con grafito, preparación y activación, piezas impresas y mecanizadas, aislamiento al vacío y superficies especializadas de condensación. Se revisaron visualmente sus páginas 7–8; no el suplemento completo. No se verificó licencia de hardware abierto. [304]

**[I]** Estos resultados no permiten comparar ganadores por una sola cifra: sus denominadores, condiciones y aparatos son distintos. Absorber vapor, liberarlo y recogerlo como líquido son pasos diferentes. Ganancia de masa del polvo no equivale a litros entregados ni a potabilidad.

## 2. La síntesis a escala cambia la valoración del MOF

**[D]** El protocolo de Zheng y colaboradores, publicado online en octubre de 2022, demuestra lotes de aproximadamente **3,5 kg** mediante reacción acuosa. Pero la cadena incluye un ligando específico, sales/reactivos, purificación con agua y etanol, secado y comprobación de propiedades. Recomienda al menos difracción de rayos X y describe medidas de adsorción. La pureza del ligando puede afectar al resultado. Se revisaron en texto las secciones pertinentes y visualmente las páginas 6, 12 y 13; no se ejecutó el protocolo. [305]

**[I]** Por tanto, sería incorrecto descartar esta familia multiplicando el precio de un gramo de laboratorio por decenas de kilogramos. También sería incorrecto llamar al proceso «solo agua» o «fabricación casera desde materias locales». La reacción es una parte del coste; quedan purificación, recuperación o compra de insumos, equipo, tiempo y calidad del producto. Una reacción de minutos no entrega por sí sola un captador terminado.

**[A]** Faltan presupuesto por lote instalado, recuperación efectiva de disolvente, gestión de residuos, capacidad útil del material fabricado y repetibilidad. Publicación científica accesible no equivale a licencia libre de aparato, formulación o explotación: no se ha auditado libertad de explotación ni encontrado un conjunto completo de CAD/BOM/licencia para adoptar.

## 3. Precios contrastados, sin convertirlos en coste del agua

| Referencia comercial consultada | Precio mostrado | Qué sigue sin demostrar |
|---|---:|---|
| P-LAB S 50000, sílice sin indicador, 1 kg | 17,45 EUR sin IVA; disponibilidad orientativa 03/11/2026 | Entrega española, equivalencia con el gel experimental y aptitud sanitaria |
| Thermo Fisher 131750250, ligando monohidrato 97 %, 25 g | 185 EUR, página de Alemania | Precio final en España y coste por lote de MOF utilizable |
| Ruixi R-M-5635, MOF-303, 1 g | 509 USD | Precio industrial, equivalencia de prestaciones y coste del dispositivo |

Datos comerciales, no compras ni cotizaciones vinculantes. [306,308,309] No se sustituyen masas de reactivo anhidro y monohidrato sin recalcular el protocolo. No se adopta ningún precio por kilogramo industrial a partir de estos formatos.

**[D]** P-LAB indica regeneración a **130–150 °C durante 4 h** para su versión sin indicador. Su documento enlazado como especificación es una declaración de clasificación de peligros, no una curva de adsorción ni una aprobación para agua de consumo. [306,307] **[I]** No contradice automáticamente el experimento a 57 °C: grado, condiciones y objetivo de regeneración pueden diferir. Tampoco permite intercambiar esos materiales y conservar el rendimiento publicado.

## 4. Cuánta superficie podría pedir el calor

**[I] Sensibilidad energética, no dimensionamiento:** se eligen 5 L/día, los extremos 1 y 3 kWh térmicos/L del experimento y dos rendimientos globales hipotéticos del captador y transferencia, 25 % y 50 %. Se reutiliza irradiación PVGIS sobre plano sur a 35°: diciembre **3,35** y julio **7,34 kWh/m²/día**. Se usa irradiación, no generación eléctrica fotovoltaica. [52; datos originales en el anexo energético]

`Superficie = litros/día × kWh térmicos/L ÷ (irradiación × rendimiento elegido)`

| Mes | A 1 kWh térmico/L, η 50 % | A 3 kWh térmicos/L, η 50 % | A 1 kWh térmico/L, η 25 % | A 3 kWh térmicos/L, η 25 % |
|---|---:|---:|---:|---:|
| Diciembre | 2,99 m² | 8,96 m² | 5,97 m² | 17,91 m² |
| Julio | 1,36 m² | 4,09 m² | 2,72 m² | 8,17 m² |

**No son superficies que garanticen esos litros.** Los rendimientos son supuestos, no medidas de un colector a la temperatura requerida. El consumo específico procede de otras condiciones ambientales. El balance no demuestra captura suficiente, temperatura alcanzable, condensación, pérdidas nocturnas, calidad ni continuidad. PVGIS describe medias históricas para una posición genérica, sin sombras de edificios; no representa la terraza ni una finca elegida. No se han añadido accesorios eléctricos ni almacenamiento entre días.

**[I]** El interés del calor solar directo es evitar parte de la conversión a electricidad. No evita construir y mantener captador, circuito térmico, condensador y reserva. Para comparar con lluvia debe mantenerse igual servicio útil y continuidad; el [balance previo](AGUA_CAPTACION_CALIDAD.md) tampoco garantiza autonomía pluvial.

## 5. Duración y reparabilidad

**[D]** Bohlender describe, para un caso de sílice regenerada a 150 °C, aproximadamente 20 % menos capacidad de equilibrio tras 100 ciclos y estabilización posterior hasta 500. Sorbtech advierte deterioro tras regeneraciones repetidas con su propio procedimiento. Son notas técnicas comerciales, no garantías universales ni ensayos del captador propuesto. [310,311]

**[I]** No hay base para prometer «gel de por vida» o fijar sustitución anual sin conocer grado, contaminación, temperaturas y capacidad restante. El cartucho desmontable facilita reemplazo; no fabrica el material. La posibilidad de limpiar un condensador tampoco demuestra calidad microbiológica o química del agua. Se mantienen los criterios y límites sanitarios del [anexo de captación](AGUA_CAPTACION_CALIDAD.md).

## 6. Qué podemos avanzar nosotros

**[P]** La parte más abordable es documentar módulos desmontables: soporte, aislamiento, lecho de material identificado, condensador accesible, reserva protegida y registro local. La futura evaluación deberá medir líquido recogido, calor y electricidad consumidos, condiciones ambientales, pérdidas de material y mantenimiento; la aptitud para beber se evalúa aparte. No se autoriza en esta entrega experimento, síntesis, compra ni consumo de agua de ensayo.

**[P]** Antes de elegir prototipo, obtener curva de adsorción/desorción y composición de un grado disponible, referencia de colector y condensador, licencia clara, presupuesto instalado y datos horarios de un emplazamiento. Después comparar el mismo servicio con lluvia y otras fuentes. MOF-303 permanece como opción avanzada que merece cotización real, no como material ya reproducible en casa a coste cero.

Esta investigación no modifica la prioridad del [taller](MATERIALES_FABRICACION.md): **FDM abierta, moldes y reparación convencional**, con material y proceso elegidos por función. La fabricación química especializada sigue siendo una línea distinta de investigación.
