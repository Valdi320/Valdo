# Xiaomi Robot Vacuum X20 Pro D102GL: repuestos, reparación mecánica y coste de referencia

Investigación consultada el **25 de octubre de 2026**. Ámbito: conservar electrónica, motores, batería y sensores originales; evaluar reparación localizada o donante antes de rediseñar piezas. Los precios y compatibilidades proceden de consultas públicas; no se ha realizado ninguna compra.

## Conclusiones que sí sostienen las fuentes

1. **Hay módulos motrices completos, muelle y pasadores catalogados expresamente para X20 Pro en un vendedor de la UE que publica envío a España.** Los dos módulos suman 66,41 € antes del transporte. Esta referencia permite poner un límite económico a una reparación experimental.
2. **No está identificado qué plástico concreto está roto en el robot del usuario.** Hay que distinguir la orejeta del módulo móvil de la orejeta fija del chasis y del gancho del muelle. Cambiar una rueda solo resolverá una rotura que forme parte del conjunto suministrado.
3. **No se localizó una carcasa desnuda del módulo, orejeta independiente o clip de reparación estructural con compatibilidad y resultado comprobados para D102GL.** Tampoco un CAD/STL completo del chasis exacto. Esto es el resultado de la búsqueda, no prueba de inexistencia.
4. **Existe carcasa estructural completa X20 MAX por 19,21 €, pero su compatibilidad con Pro NO está documentada.** Solo sirve como candidato para comparación geométrica y referencia económica.
5. **La compatibilidad se decide pieza por pieza.** Pro y Max comparten determinadas referencias; X20+ comparte alguna pieza de mantenimiento, pero eso no permite trasladar sus módulos motrices, chasis, batería o tutoriales.
6. Para presupuesto bajo, la primera decisión útil es fotografiar e identificar las superficies rotas. Comprar dos motores para reparar dos puntos fijos del chasis sería un gasto que no resuelve el fallo.

## Criterio de evidencia

- **E1 — fabricante:** Xiaomi, Ceys o fabricante del componente; prueba lo que publica expresamente.
- **E2 — ficha propia del vendedor:** compatibilidad, precio y disponibilidad que el vendedor declara. Es evidencia comercial directa, no una medición independiente ni una homologación del fabricante.
- **E3b — anuncio o experiencia particular:** prueba de que se anuncia o se relata ese caso; no certifica estado real ni durabilidad.
- **Sin verificar:** analogía, compatibilidad inferida o un resultado de buscador cuyo cuerpo no se pudo abrir.

Los precios son observaciones, no ofertas reservadas. En PC:MediaStore las fichas indican IVA incluido y transporte aparte; no se verificó ajuste fiscal por destino ni elegibilidad de un pedido mediante checkout. Los SKU de cinco dígitos de esa tienda **no son referencias OEM universales**. Un EAN tampoco sustituye una identificación OEM.

## Identificación y catálogo

Xiaomi identifica el robot Pro como **D102GL** y la estación como **D102-JZEU**. El catálogo europeo del vendedor agrupa el equipo comercial **BHR8859EU** bajo esos nombres. [Ficha Xiaomi](https://www.mi.com/global/product/xiaomi-robot-vacuum-x20-pro/specs/).

El [catálogo canónico PC:MediaStore para Pro](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html) mostró 99 entradas en dos páginas; incluye estación, accesorios y consumibles, por lo que no representa una lista de 99 componentes exclusivos del robot. Se inspeccionaron las fichas individuales relevantes. [Página 2](https://www.ep-mediastore-ab.de/ersatzteile-mi-robot-vacuum-x20-pro-bhr8859eu-omni-station-d102-jzeu-fm-1019.html?page=2).

## BOM de referencia: locomoción y carcasa

| Pieza | Referencia de tienda, identificación adicional | Compatibilidad explícita relevante | Precio observado | Disponibilidad publicada | Evidencia y límite |
|---|---|---|---:|---|---|
| Módulo motriz izquierdo completo | **12585**; PCB XYD-2012W; EAN 4251919454088 | X20 Pro BHR8859EU y X20 Max BHR9220EU | **29,62 €** | Más de 10 | E2. Rueda, motor, reductora y cable. No hay código OEM numérico de módulo comprobado. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-links-schwarz-x20max-pro-p-12585.html) |
| Módulo motriz derecho completo | **13025**; PCB XYD-2012W; EAN 4251919454095 | X20 Pro, X20 Max; además Vacuum 5 OV31GL en esta ficha | **36,79 €** | Más de 10 | E2. No generalizar la compatibilidad adicional de la derecha a la izquierda. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-antriebsmodul-rechts-schwarz-x20max-pro-p-13025.html) |
| Muelle de suspensión de rueda, 1 unidad | **37935**; sin PN OEM verificado | Pro y Max incluidos expresamente | **1,83 €**; desde 2 unidades, 1,80 €/ud. | Más de 10 | E2. Longitud aproximada total 45 mm, cuerpo 32 mm, diámetro exterior 6,2 mm. No publica rigidez, precarga ni carrera admisible. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-radfeder-62x32-45mm-p-37935.html) |
| Pasador metálico, paquete de 2 | **12584**; EAN 4251919454071 | Pro y Max | **2,03 € / 2 uds.** | Más de 10 | E2. Diámetro × longitud 4 × 38,5 mm. Un pasador nuevo no reconstruye un alojamiento plástico roto. [Ficha](https://www.ep-mediastore-ab.de/rad-lager-splint-4x385-mm-stueck-p-12584.html) |
| Rueda delantera giratoria con soporte | **42556** | Pro, Max, X20+ y otros, según árbol de compatibilidad | **29,98 €** | Más de 10 | E2. Incluye retención en U. No es una rueda motriz lateral. [Ficha](https://www.ep-mediastore-ab.de/dreame-d9-l10-frontrolle-halter-schwarz-p-42556.html) |
| Tapa abatible y embellecedor superior blancos | **29986**; campo de fabricante TOPCOVER.WHITE.S20+ | Pro, Max, S20+ blanco/negro | **16,12 €** | Más de 10 | E2. Dos tapas cosméticas; no sustituyen el chasis que soporta el pivote. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-klappdeckel-abdeckung-weiss-s20-x20pro-p-29986.html) |
| Carcasa completa negra, tres piezas | **41414**; campo descriptivo COMPLETE.CHASSIS | **Solo X20 MAX** en ficha | **19,21 €** | Disponible | E2 para Max; sin verificar para Pro. Incluye base, parte media y superior. No autoriza a comprarla para Pro sin cotejo. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-x20-max-gehaeuse-komplett-p-41414.html) |
| Carcasa desnuda del módulo motriz Pro | Sin referencia verificada | No establecida | — | No localizada | No confundir ofertas de otras familias con esta pieza. |
| Orejeta/gancho del muelle independiente Pro | Sin referencia verificada | No establecida | — | No localizado | Puede estar integrado en el módulo o chasis. |
| Chasis estructural completo Pro | Sin referencia verificada | No establecida | — | No localizado | La tapa 29986 y carcasa Max 41414 no prueban su disponibilidad. |

Las fichas de las ruedas no establecen con claridad que suministren muelle y pasador nuevos. Presupuestarlos separadamente evita suponer que vienen incluidos. Para izquierda/derecha debe usarse la orientación de marcha del robot y comprobar su correspondencia con las fotos, no la posición en una fotografía tomada boca abajo.

## Electrónica y conjuntos que conviene preservar

Estos precios documentan la disponibilidad y el valor de reutilizar lo existente; no son una recomendación de reemplazar piezas sanas.

| Conjunto | SKU vendedor / identificación de componente | Precio | Compatibilidad y estado de la fuente |
|---|---|---:|---|
| Placa principal del robot | **40091 / B108EU_MB** | **159,00 €** | E2, original Pro, disponible. El nombre de PCB por sí solo no prueba que el firmware de otras versiones sea intercambiable. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-x20-pro-mainboard-b108eumb-p-40091.html) |
| Batería original | **56237 / P2150-4S2P-SCEV o P2150-4S2P-PTEV** | **58,99 €** | E2, Pro/Max/S20+; más de 10. La tienda advierte expresamente que una batería Dreame L10 de apariencia semejante tiene otra polaridad de conector. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-akku-5200mah-p2150-4s2p-scev-fuer-s20-x20-max-pro-original-p-56237.html) |
| Dos accionamientos de mopas con reductoras y detección | **29890 / motor PRI-3855SV-2185** | **27,88 €** | E2, Pro; más de 5. La PN identifica el motor, no necesariamente todo el conjunto. [Ficha](https://www.ep-mediastore-ab.de/xiaomi-wischmotoren-x20-pro-p-29890.html) |
| Contactos traseros de carga, IR y soporte | **28885 / D102_BIR** | **24,57 €** | E2, Pro; disponible. Es un conjunto del robot asociado al acoplamiento a base. [Ficha](https://www.ep-mediastore-ab.de/ladekontakteinheit-ir-sensor-x20-pro-p-28885.html) |
| Turbina de aspiración | **72817 / HJD-RA60405, BL.531124.0161** | **41,99 €** | E2, Pro/S20+; más de 10. El vendedor indica extracción de equipos nuevos para repuestos. La ficha no es una curva de rendimiento verificada. [Ficha](https://www.ep-mediastore-ab.de/saugmotor-hjd-ra60405-xiaomi-s20-x20pro-p-72817.html) |

**Implicación para rediseño — criterio técnico propio:** conservar arneses, polaridad, conectores, sensores y ubicación funcional de las piezas reduce el trabajo de integración. Una carcasa nueva no debería obligar a sustituir electrónica sana por otra meramente parecida. La compatibilidad dimensional de un enchufe no garantiza compatibilidad eléctrica.

## España: transporte y escenarios económicos

La [FAQ propia de envío](https://www.ep-mediastore-ab.de/versand_und_zahlungsbedingungen.php), apartado *Spanien*, publica:

| Servicio | Condición publicada | Tarifa |
|---|---|---:|
| DHL Paket | 0–5 kg | **23,79 €** |
| DHL Paket | 5–10 kg / 10–20 kg | 28,56 € / 34,51 € |
| DPD Europa | 0–31,5 kg | 30,23 € |
| DHL Warenpost International | Hasta 0,5 kg; pedido máximo 50 €; seguimiento reducido | **9,98 €** |
| DHL Warenpost International | Hasta 1 kg; pedido máximo 50 €; seguimiento reducido | **11,00 €** |

La misma tabla indica orientación de 3–6 días laborables desde entrega a DHL. No se verificó un destino postal concreto, islas, peso embalado, elegibilidad de productos, selección del transportista ni total fiscal mediante checkout.

Cálculos de referencia con precios observados:

| Escenario | Material | Con transporte ilustrativo | Cuándo tiene sentido |
|---|---:|---:|---|
| 1 muelle + paquete de 2 pasadores | 3,86 € | 13,84 € si permite Warenpost de 9,98 € | Solo cuando alojamientos y anclajes están sanos |
| Módulo izquierdo + 1 muelle + pasadores | 33,48 € | 43,46 € bajo esa misma condición | Rotura localizada en conjunto izquierdo suministrado |
| Módulo derecho + 1 muelle + pasadores | 40,65 € | 50,63 € bajo esa misma condición | Rotura localizada en conjunto derecho suministrado |
| Dos módulos, sin accesorios | 66,41 € | 90,20 € usando tarifa DHL 0–5 kg | Solo si ambos conjuntos requieren sustitución |
| Dos módulos + 2 muelles + pasadores | 72,04 € | 95,83 € usando tarifa DHL 0–5 kg | Incluye precio por cantidad de muelles; necesidad por confirmar |

**Los totales con transporte son aritmética condicional, no presupuestos finales.** En un pedido conjunto los dos módulos ya superan el límite publicado de 50 € para Warenpost.

## Donantes: referencias reales y límites

### Alemania, anuncio abierto completo

[Anuncio Kleinanzeigen 3524161933](https://www.kleinanzeigen.de/s-anzeige/xiaomi-x20-pro-saugroboter-mit-wischfunktion-defekt/3524161933-176-1857), Hilden, publicado el 27/09/2026: **100 € negociables**, X20 Pro con estación y accesorios, vendido como averiado por error de sensor de línea. E3b. Hay cuatro fotografías, pero no se demostró el estado de orejetas, muelles, ejes o motores. El importe de envío genérico de la plataforma no prueba envío a España. No se contactó al anunciante.

### España, pista de menor certeza

[Anuncio Wallapop 1312894872](https://es.wallapop.com/item/averiado-xiaomi-robot-vacuum-x20-pro-1312894872), Vic: el buscador indexa **120 €** y error de sensor de línea. El cuerpo de la página no se pudo abrir; disponibilidad, fecha, contenidos y estado mecánico no confirmados. Es una pista de mercado, no una unidad verificada ni un precio de transacción.

### Decisión económica

Un donante tiene interés si aporta un chasis sano que no se consigue suelto, más piezas aprovechables o material para medir sin inmovilizar el robot del usuario. Con un anuncio de 100–120 € no es automáticamente más barato que reparar una sola rueda. Para que resuelva este caso hay que verificar el modelo de etiqueta y **ambos puntos de pivote y de enganche del muelle**, no solo que el robot encienda. El defecto declarado por el anunciante no excluye daños adicionales. Estos requisitos son razonamiento técnico, no constataciones sobre esos anuncios.

No se localizó una oferta española abierta de carcasa desnuda o rueda motriz Pro con referencia y precio más sólidos que las fichas alemanas. Las búsquedas de “repuestos” devolvieron principalmente cepillos, filtros y mopas.

## Compatibilidad: lo probado y lo que se debe evitar

| Relación | Evidencia útil | Límite |
|---|---|---|
| Pro ↔ Max | Misma ficha de módulos 12585/13025, muelle 37935, pasadores 12584 y tapas 29986 | No demuestra todo el chasis, distribución interior ni firmware idénticos |
| Pro ↔ S20+ | Tapas 29986, batería 56237 y turbina 72817 catalogadas comunes | No convierte todo un S20+ en donante directo |
| Pro ↔ X20+ | La rueda delantera 42556 sí figura para ambos | Sus ruedas motrices y estructura no quedan verificadas por compartir un consumible o rueda loca |
| Pro ↔ M30 D102 | Familia relacionada útil para estudiar fotos; no se obtuvo tabla primaria que iguale todos los soportes | No usar una etiqueta M30/M30 Pro o nombre “Pro” de otro fabricante como equivalencia |
| Pro ↔ Dreame L10 batería parecida | El vendedor documenta polaridad diferente del conector | Evitar sustitución por apariencia |

**Ejemplo de resultado que no supera el filtro:** [FixShop, rueda izquierda blanca VACC-XIA-334 / 1100328004](https://www.fixshop.eu/spare-parts-vacuum-cleaner-parts-accessories-spare-parts-engine/xiaomi-robot-vacuum-x20-s10-dreame-x30-x20-x10-pro-wheel-with-motor-left-white/), **29,49 €** IVA incluido en la región mostrada. Lista numerosas familias, M30 y X20+, pero no declara X20 Pro D102GL. Es aftermarket; no se incorpora como alternativa compatible. Un título que combina Xiaomi X20 y Dreame X10 Pro no significa Xiaomi X20 Pro.

## CAD, clips y reparación mecánica localizada

Búsquedas dirigidas con X20 Pro/D102GL y wheel, bracket, holder, spring, chassis, housing, Radgehäuse, reparación, STL, además de consultas a Printables, Cults y búsquedas chinas de M30, no localizaron un CAD estructural exacto verificado o un refuerzo probado de la orejeta del D102GL.

Se distinguieron estos resultados de los realmente útiles:

- [Printables: soporte para almacenar filtros Pro/Max](https://www.printables.com/model/1745789-xiaomi-x20-pro-x20-max-filter-storage-holder-store). Es accesorio de almacenamiento; no un refuerzo de rueda.
- [Printables: Wheel holder for Mi Robot Vacuum-Mop Essential, autor cab](https://www.printables.com/model/990525-wheel-holder-for-mi-robot-vacuum-mop-essential/user-gcodes). Modelo de otra familia, sin validación para Pro.
- [Cults: engranaje de rueda para Mi Robot Vacuum Mop Essential](https://cults3d.com/en/3d-model/tool/wheel-gear-for-xiaomi-mi-vacuum-robot-32-teeth). No es un soporte Pro.
- Los buscadores agregadores mezclan esas piezas con rampas Pro y modelos de láser Atomstack X20 Pro. No son prueba de compatibilidad.

[Experiencia con fotos de un X20 Pro con muelle suelto](https://www.reddit.com/r/RobotVacuums/comments/1t2604u/need_help_with_my_xiaomi_x20_pro_one_wheel_stays/): acredita un caso particular y permite observar el conjunto; no acredita una reparación validada, frecuencia de fallos ni la avería concreta del usuario.

**Recomendación de ingeniería, todavía no diseño validado:** para reducir coste y mejorar mantenibilidad conviene explorar primero una reparación local reemplazable que distribuya la carga sobre material sano, conservando eje, carrera y muelle originales. Solo tras identificar la pieza rota puede decidirse si basta una placa de respaldo/soporte mecánico o hace falta una carcasa nueva. No hay evidencia para prometer que una brida, abrazadera o pegamento por sí solos mantendrán la alineación durante servicio.

### Qué falta medir o fotografiar

1. La rotura por ambos lados, con el módulo en su posición normal y desplazado lo justo para ver el pivote.
2. Qué fragmento pertenece al cuerpo fijo y cuál se mueve con la rueda.
3. Diámetro y longitud útiles del alojamiento sano, distancias entre apoyos, espacio para refuerzo y trayectoria de cables.
4. Punto fijo y móvil del muelle; recorrido libre y comprimido, y holguras con el sensor de rueda levantada.
5. Marcaje de material del plástico, si existe.
6. Si el pasador está íntegro y si ambos extremos siguen retenidos.

Las cotas del pasador y muelle publicadas ayudan a identificar piezas, pero no aportan tolerancias del alojamiento ni cargas de diseño. Los fabricantes de muelles recuerdan que debe compararse fuerza inicial, rigidez y extensión de trabajo, no solo longitud y diámetro: [MW Components](https://www.mwcomponents.com/how-to-select-an-extension-spring), [Lee Spring](https://www.leespring.com/learn-about-extension-springs).

## Ceys Tri’Action: interpretación correcta para esta reparación

La [ficha técnica oficial TRI’ACTION TOTAL TECH, referencias 507219/507228](https://mundoceys.com/storage/app/media/fichas_tecnicas/507219-ft-triaction-total-tech.pdf), versión 2 de 2018, describe un polímero híbrido flexible: curado total 48 h, elongación 180 %, dureza Shore A 60; excluye PE, PP y PTFE. También menciona resistencia máxima a 24 h en instrucciones de aplicación. Hay que cotejar el envase exacto; espesores y condiciones afectan al curado.

**Conclusión técnica propia:** cumplir 48 h no demuestra que una orejeta de pivote recupere geometría, rigidez y resistencia cíclica originales. La ficha no valida esta aplicación estructural concreta. Conviene tratar el adhesivo como unión elástica de comportamiento aún no verificado aquí; un eventual refuerzo debería transmitir carga por una trayectoria mecánica comprobable. No afirmar “irrompible”, “listo para lo peor” ni adhesión garantizada sin identificar el plástico.

## Fuentes de fotos para comparación técnica

- [Módulo izquierdo, cara1](https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585.gif).
- [Módulo izquierdo, cara2](https://www.ep-mediastore-ab.de/images/Artikelbilder/01/25/12585_1.gif). Inspeccionada: se distingue el alojamiento cilíndrico junto al extremo del motor. La imagen no muestra el alojamiento fijo del chasis.
- [Pasadores metálicos](https://www.ep-mediastore-ab.de/images/72990/01/25/12584/rad_lager_splint_4x38.5_mm_stueck-1280x1280.jpg).
- [Carcasa Max, exterior](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280.jpg), [interior](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_1.jpg), [base](https://www.ep-mediastore-ab.de/images/72990/04/14/41414/xiaomi_x20_max_gehaeuse_komplett-1280x1280_2.jpg). Son Max, no etiquetarlas como Pro.
- [Ficha DNS Kazakhstan, rueda izquierda Pro](https://www.dns-shop.kz/product/5a1ae0fea1a1b25e/dvigatel-v-sbore-s-kolesom-l-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/), [derecha Pro](https://www.dns-shop.kz/product/0daa56c88926541e/dvigatel-v-sbore-s-kolesom-r-dla-pylesosa-robota-xiaomi-robot-vacuum-x20-pro-na/): fotos complementarias localizadas en investigación anterior; precio actual y envío UE no verificados en esta ronda.

## Datos reutilizables

El archivo compañero `repuestos.csv` conserva importes, unidades, evidencia y límites en columnas para reutilizar la tabla. No es una lista de compra.

