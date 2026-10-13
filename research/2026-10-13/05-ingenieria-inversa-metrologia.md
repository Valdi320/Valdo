# 05 — Descompilador físico + digital: metrología, CAD paramétrico e interfaces

## Hallazgo central: geometría escaneada ≠ plano apto para fabricar

**[D]** [OpenScan](https://openscan-org.github.io/OpenScan-Doc/photogrammetry/quality/) advierte que sus mallas fotogramétricas pueden **carecer de escala absoluta** y requerir una dimensión de referencia o marcadores calibrados. [NIST](https://www.nist.gov/publications/performance-evaluation-terrestrial-laser-scanners-review) estudia trazabilidad, fuentes de error y pruebas en captura tridimensional. Sin incertidumbre/calibración un «gemelo digital» puede ser visualmente perfecto e impedir encajar una pieza.

**[P]** El producto no debe anunciar «recuperamos un diseño» hasta contener:
- cotas y referencia física del sistema de coordenadas;
- incertidumbre por medición importante, no solo media de error de malla;
- CAD paramétrico con operaciones editables y geometría comprobable;
- definición de material observada/inferida y lotes, tolerancias reales y superficie crítica;
- contexto funcional, montaje y pruebas; documentación de incógnitas.

## 1. Modos de investigación con el menor instrumental posible

| Nivel | Entrada | Capacidad | Riesgo de interpretación |
|---|---|---|---|
| Escaneo fotográfico | cámara + soporte+ marcadores | geometría exterior y textura | escala, reflexión, zonas ocultas |
| Metrología dimensional | patrón/calibre calibrado | diámetros, distancias, planitud aproximada | apilamiento de errores |
| Captura estructurada | cámara/proyector/escáner dedicado | geometría exterior más directa | calibraje y materiales reflectantes |
| Microscopía | lupa y macro | marcas, pistas y tornillos | no ve multicapa |
| Inspección térmica | cámara térmica | temperaturas indicativas | emisividad y causas múltiples |
| Ensayo táctil controlado | palpador/medidor fuerza | rigidez, holgura, fricción | puede modificar pieza |
| Electrónica en baja energía | multímetro/lógico/osciloscopio | conectividad y señales accesibles | conexiones internas y energía peligrosa |
| Ultrasonido/CT industrial | instrumental especializado | regiones ocultas compatibles | cobertura, resolución, seguridad/coste |
| Análisis químico | XRF/Raman/FTIR/NIR según muestra | identificación parcial de composición | tratamiento/aleación exacta y forma interna |

**No habilitar inspección activa energizada de aparatos domésticos sin diagnóstico eléctrico competente y protecciones.** Los sensores físicos producen observaciones distintas; ninguna combinación descubre automáticamente secretos no observables.

## 2. Algoritmo de ingeniería inversa activa

```text
inspección visual → registro de hipótesis y zonas ocluidas
             ↓
captura calibrada → malla/nube → segmentación de superficies
             ↓
reconstrucción de primitivas + programa paramétrico candidato
             ↓
error residual y propagación de incertidumbres
             ↓
¿qué nueva medida reduce incertidumbre más importante?
             ├── medición adicional y refinamiento
             ├── inspección accesible / desmontaje aprobado
             └── límite físico ⇒ valor DESCONOCIDO
             ↓
CAD B-rep paramétrico + propiedades + BOM + ensamblaje
             ↓
simulación y pieza no crítica → comparación dimensional/funcional
```

**[D]** Nuevos precedentes de 2025–2026 para *puntos → instrucciones CAD*: [CAD-Recode (ICCV 2025)](https://openaccess.thecvf.com/content/ICCV2025/html/Rukhovich_CAD-Recode_Reverse_Engineering_CAD_Code_from_Point_Clouds_ICCV_2025_paper.html), que traduce puntos a código Python de operaciones de CAD, y [RenCAD (Engineering Applications of AI 2026)](https://www.sciencedirect.com/science/article/abs/pii/S0952197625031380), que investiga generar secuencias CAD editables. **Son investigación sobre modelos geométricos; no recuperan sin más tolerancias funcionales, material o procesos originales.**

**[P]** Primera vía sin modelo grande: detectar planos/cilindros/agujeros mediante métodos clásicos como RANSAC y ajustar bocetos/operaciones de FreeCAD/CadQuery; después evaluar CAD-Recode. Es preferible una construcción sencilla y medible a un generador de mallas bonitas opacas.

## 3. Formatos y estándares que deberían preservarse

**[D]** [ISO 10303 STEP](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/step-nist) es uno de los estándares fundamentales de intercambio de información de producto y CAD; NIST señala adopción de **AP242** para modelo/PMI por grandes proveedores. [QIF](https://www.nist.gov/publications/end-end-quality-information-framework-qif-technology-survey) ofrece modelos de intercambio de **inspección y resultados de metrología**.

**[P] Datos que conservar juntos, no confundir:**
- nubes y mallas originales (entrada observada);
- CAD editable nativo y fuente procedural parametrizada;
- STEP como intercambio B-rep cuando corresponda;
- archivo de inspección QIF/CSV trazable, medidas/errores/condiciones;
- estructura ensamblaje y relaciones componentes;
- ficha de material/receta/almacén;
- firmware y documentación vinculados **solo si acceso legal y verificación**.

No exportar solo STL: STL pierde unidades confiables, historial de features y tolerancias como fuente de ingeniería.

## 4. Conexión del descompilador físico con el firmware

**[P]** Crear un grafo:

```text
pieza física → componente → pin/conexión → señal medida
                                      └── función de firmware detectada
                                      └── comportamiento esperado y prueba
```

Ghidra puede analizar firmware accesible/compatible, pero **el pseudocódigo no significa código fuente original**. Recompilación ciega repetida no asegura idempotencia ni funcionalidad. La ingeniería inversa digital se usará para interoperabilidad y conocimiento **en los límites permitidos**, con emulación y pruebas diferenciales cuando proceda.

**[D]** Para desmontaje electrónico, [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) aporta pruebas de conectores y cableado; [Degate](https://github.com/DegateCommunity/Degate) es un precedente de análisis semiautomático de lógica IC por imágenes, no un mecanismo automático de clonación de semiconductores modernos.

## 5. Primer experimento de calibración propuesto

**[P]** Elegir cinco piezas **no críticas** con distintas geometrías (prisma con agujeros, tapa de rosca sin exigencia de estanqueidad, soporte con radio, pieza compuesta, engranaje de demostración). Para cada una:

1. Definir escala y patrón calibrado, capturar malla y repetir tres veces con cambios de ángulo.
2. Medir cotas críticas con segundo método; registrar resolución y desviación.
3. Reconstruir programa CAD editable: operaciones de sketch/extrude/hole/fillet, parámetros y grados de libertad.
4. Generar STEP y verificar que un lector independiente reproduce la geometría.
5. Imprimir versión de prueba, medirla, encajarla y registrar éxito/fallo.
6. Separar errores de escaneo, ajuste CAD, slicing, material y postproceso (nunca atribuir todo a «la IA»).

**Métricas:** error dimensional por cota, repetibilidad, porcentaje de operaciones editables, número de incertidumbres resueltas con medición adicional, tiempo de edición humana, coste y tasa de ajuste funcional.

## 6. Límites y salvaguardas

- Un modelo fiel de exterior no prueba composición interna, dureza, adhesivos, tratamientos térmicos, envejecimiento o fatiga.
- Inspección no destructiva y rayos X no son equivalentes a visión universal; usar laboratorios habilitados y requisitos radiológicos.
- Evitar pruebas destructivas o energizadas sobre aparatos ajenos sin autorización.
- Resultado honesto: **posible función, confianza, pruebas requeridas y zonas desconocidas**.

**Fuentes:** [OpenScan calidad](https://openscan-org.github.io/OpenScan-Doc/photogrammetry/quality/), [OpenScan3](https://github.com/OpenScan-org/OpenScan3), [NIST metrología](https://www.nist.gov/publications/performance-evaluation-terrestrial-laser-scanners-review), [CAD-Recode](https://openaccess.thecvf.com/content/ICCV2025/html/Rukhovich_CAD-Recode_Reverse_Engineering_CAD_Code_from_Point_Clouds_ICCV_2025_paper.html), [RenCAD](https://www.sciencedirect.com/science/article/abs/pii/S0952197625031380), [STEP](https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/step-nist), [QIF](https://www.nist.gov/publications/end-end-quality-information-framework-qif-technology-survey), [FreeCAD](https://github.com/FreeCAD/FreeCAD), [CadQuery](https://github.com/CadQuery/cadquery).
