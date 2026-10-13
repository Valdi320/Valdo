# 02 — Manipulación: tornillos, conectores, cables, juntas y autorreparación

## Hallazgo: la primera dificultad no es diagnosticar, sino actuar sin romper

**[D]** El [National Institute of Standards and Technology (NIST)](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) ofrece diseños y protocolos públicos de **Assembly Task Boards**:
- tablero 1: pasadores, engranajes, conectores eléctricos, tuercas;
- tablero 2: correas, poleas, tensores, piezas flexibles;
- tablero 3: guía y tejido de cables, extremos de conectores;
- tablero 4: arneses, clips y organización de cableado;
- tablero 5: roscas y tornillos cerca de obstáculos.

**[P] La fase inaugural de destreza FDAA debe adoptar estos ejercicios en un banco de baja energía**, antes de prometer reparaciones de lavadoras. NIST también publica reglas para repetición y montaje/desmontaje [documentación NIST](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/robotic-grasping-0).

## 1. Habilidades elementales

| Habilidad | Por qué es difícil | Sensores y control mínimo | Criterio de PASS |
|---|---|---|---|
| Retirar tornillo | cizallamiento de cabeza, punta equivocada, pérdida | visión de punta, par, ángulo, fuerza axial | sin dañar rosca y conservar tornillo |
| Volver a roscar | rosca cruzada o apriete insuficiente | estrategia de alineación, fuerza y curva par-giro | par dentro de especificación validada |
| Soltar clip | fractura oculta y material envejecido | cámara de proximidad + fuerza limitada | clip íntegro si es reversible |
| Extraer conector | seguro oculto, dirección incorrecta | inspección + mecanismo de liberación | sin pines deformados |
| Guiar cable/manguera | se engancha y queda pellizcado | visión multicámara, detección de tensión y pinza compliant | no pellizcado tras montaje |
| Poner junta | deformación y estanqueidad | visión de asiento, fuerza de inserción | pasa test de fugas apropiado |
| Sujetar panel | pieza grande, gravitacional, sin agarre | dos brazos + apoyos + sujeciones | panel no cae ni se deforma |
| Meter módulo en dock | tolerancia, conectores rígidos | chamfer/guía, sensor de pose y esfuerzo | módulo asentado, contacto probado |

**No basta el agarre**: desatornillar requiere controlar **fuerza de empuje + par aplicado** y reaccionar ante deformación o desgaste; reconectar exige comprobar funcionamiento, no solo coincidencia visual.

## 2. Ordenar herramientas: cambiar de útil es más útil que manos antropomorfas completas

**[P] Primer conjunto de útiles:**
1. pinza paralela con dedos reemplazables y recubrimiento táctil;
2. destornillador automático con par programable y mecanismo de cambio de punta;
3. tenaza/pinza fina para conectores;
4. ventosa con **mecanismo de retención secundaria** para cristal o paneles;
5. cámara endoscópica y luz en muñeca;
6. pequeño palpador/medidor de fuerza;
7. soporte de piezas y bandejas codificadas.

**[I]** Para la mayoría de ensayos de montaje iniciales, una pinza fiable con cambio automático de herramienta puede ser más rentable que diseñar desde cero cinco dedos. Las manos complejas se estudiarían cuando una evaluación objetiva muestre cobertura insuficiente.

## 3. Sensibilidad: táctil barato y reemplazable

**[D]** [AnySkin](https://any-skin.github.io/) investiga sensores táctiles magnéticos con superficies intercambiables, útiles para contacto y detección de deslizamiento. Su artículo reporta transferencia entre superficies para determinadas tareas, **no manipulación arbitraria**. El desgaste de piel debe quedar incluido en BOM y planes de mantenimiento.

**[P]** Combinar tacto distal, sensores de fuerza/par de muñeca y medición de corriente/par de articulaciones. Usar control de impedancia/admitancia con límites verificados; cualquier aprendizaje de fuerza se somete a barreras físicas independientes. La tactilidad no sustituye la visión, y una cámara no sustituye la medición de fuerza.

## 4. Desmontaje reverso y trazabilidad exacta

**Contrato de cada paso físico:**
```text
id_paso | pieza_id | precondiciones | energia_aislada | postura_referencia
herramienta | fijaciones | par_registrado | fotos_antes | fuerzas_reales
resultado | piezas_en_bandeja | anomalías | reversibilidad | fotos_despues
```

Guardar etiqueta y coordenadas de cada tornillo, arandela o junta. La secuencia de montaje puede requerir **otro orden** o junta nueva: no invertir ciegamente los movimientos. Interrumpir si un tornillo se gripó, aparece fluido o cambia geometría respecto a lo esperado.

## 5. Reparación mutua A ↔ B

**[P]** Tres demostraciones diferenciadas:
- B sustituye un elemento **no crítico y externo** de A (carcasa/sensor).
- B reemplaza un módulo de pata/rueda de A **sin que A tenga energía**: dock lo sostiene físicamente, existen guías y conectores seguros.
- A repite sobre B; la estación efectúa reparación si ambos quedan incapacitados.

**Pruebas negativas:** módulo incorrecto; conector invertido; tornillo dañado; ausencia de recambio; fallo de luz; pérdida de conexión; estación sin energía; temperatura fuera de rango. La decisión correcta puede ser **no reparar**.

**[D]** La [Open Dynamic Robot Initiative](https://open-dynamic-robot-initiative.github.io/) aporta diseño abierto de módulos de actuador controlados por par; [Robot Metabolism (Columbia)](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots) es un antecedente de ensamblaje/reconfiguración, no de reparar autónomamente cualquier máquina.

## 6. Entrenamiento mediante teleoperación y dataset real

**[D]** La [documentación de LeRobot](https://github.com/huggingface/lerobot/blob/main/docs/source/il_robots.mdx) muestra cómo grabar demostraciones de teleoperación, visualizar, entrenar políticas y evaluar tareas. No exige comenzar con control totalmente autónomo.

**[P]** Dataset local con registros de:
- cámaras fijas, cámara en muñeca, estado de articulaciones, fuerza/tacto y audio/vibración cuando proceda;
- orden humana, estado previo, herramienta, errores, necesidad de intervención y resultados;
- episodios de fallos *y* de éxitos, pero nunca grabar para forzar un fallo peligroso;
- variaciones entre objetos, modelos, posiciones, iluminación y desgaste;
- consentimiento/anonimización en escenas domésticas.

**Separación de datos:** entrenamiento, validación en objetos conocidos y conjunto **fuera de distribución** (otros tornillos, conectores y posiciones). Evaluar repetibilidad con ensayos ciegos y criterios pre-registrados.

## 7. Escalado a electrodomésticos reales

Pruebas ordenadas: ATB NIST → carcasa imprimible desmontable → aparato de baja tensión desconectado → electrodoméstico real **solo tras revisión de seguridad y autorizaciones**. Antes de manipular una lavadora real ensayar con una **maqueta de masa y conectores simulados**, sin red eléctrica ni agua, incluyendo extracción y retorno a hueco.

**No automatizar en prototipo temprano** red eléctrica fija, refrigerantes, gas, baterías dañadas, izado inestable ni aparatos conectados a personas.

**Fuentes principales:** [NIST benchmarks](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly), [NIST RGMC](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/robotic-grasping-0), [AnySkin](https://any-skin.github.io/), [LeRobot imitation learning](https://github.com/huggingface/lerobot/blob/main/docs/source/il_robots.mdx), [NIST contact-safety performance](https://www.nist.gov/programs-projects/grasping-manipulation-and-contact-safety-performance-robotic-systems).
