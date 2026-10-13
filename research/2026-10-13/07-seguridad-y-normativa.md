# 07 — Seguridad funcional, producto, IA, ciberseguridad y derecho a reparar

> **Fecha de comprobación: 13/10/2026.** Investigación informativa; no constituye asesoramiento jurídico, evaluación de conformidad ni permiso para trabajar con gas, refrigerantes o electricidad. Normas, calendarios y ámbitos **pueden cambiar**. El proyecto deberá consultar texto consolidado y especialistas antes de comercializar o ensayar máquinas de riesgo.

## 1. Hallazgo normativo nuevo: una norma de servicio robótico está cambiando AHORA

**[D]** [ISO 13482:2014](https://www.iso.org/standard/53820.html) sigue publicada como referencia de robots de atención personal. [ISO/FDIS 13482, edición 2](https://www.iso.org/standard/83498.html) estaba en **fase final de aprobación en septiembre/octubre 2026**, prevista para reemplazarla; la nueva descripción abarca **robots de servicio** para ámbitos personales y profesionales/comerciales y presta atención a contacto físico y seguridad funcional. **Es un borrador FDIS, no debe citarse como norma publicada en esta fecha.**

**[P]** Vigilar nueva edición; diseñar ahora por riesgos y ensayos, no elegir componentes únicamente por una norma a punto de sustituirse. Distintos subsistemas pueden exigir otras normas de máquinas, electricidad, elevación y baterías.

## 2. Reglamento de maquinaria de la UE actualizado

**[D]** [Reglamento (UE) 2023/1230, versión consolidada 27/07/2026](https://eur-lex.europa.eu/eli/reg/2023/1230/en) indica **aplicación general desde el 20 de enero de 2027** y define obligaciones sobre riesgos, diseño y comercialización/puesta en servicio. **Importante:** páginas no consolidadas de 2023 muestran fechas previas; utilizar texto vigente y modificaciones publicadas, incluida (UE) 2026/1744. Evaluar clasificación exacta del sistema antes de afirmar si procede o qué procedimiento de evaluación corresponde.

**[P]** Expediente de diseño: análisis de riesgos desde fase 0, documentación de subsistemas, resguardos, manual de instalación/mantenimiento, pruebas de seguridad, límites de uso, paradas de emergencia y evidencia de conformidad aplicable. No confundir prototipo de laboratorio con robot apto para vivienda o comercialización.

## 3. Ley de IA: no todos los LLM son automáticamente sistemas de alto riesgo

**[D]** La [Comisión Europea](https://digital-strategy.ec.europa.eu/es/policies/regulatory-framework-ai) explica el calendario tras las modificaciones de 2026: determinadas reglas de alto riesgo para sistemas integrados en productos como robótica/maquinaria se aplicarían desde **2 de agosto de 2028**. La [guía de clasificación](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems) distingue casos relacionados con producto y su necesidad de evaluación por terceros. **El proyecto deberá clasificar concretamente su diseño, no asignarle automáticamente todas las obligaciones de «alto riesgo».**

**[P]** Evitar usar LLM/VLA como componente único de seguridad; proteger el enlace entre instrucciones, control y riesgos. Conservar trazas, versiones de modelo, pruebas de sesgos peligrosos y errores fuera de distribución.

## 4. Ley de Ciberresiliencia (CRA): parte de obligaciones YA vigente

**[D]** [Reglamento (UE) 2024/2847](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847) aplica en general desde **11/12/2027**; el **artículo 14** de notificación se aplica desde **11/09/2026**. La Comisión describe obligaciones de notificación de vulnerabilidades explotadas activamente e incidentes graves para fabricantes en determinadas condiciones [guía oficial](https://digital-strategy.ec.europa.eu/es/policies/cra-reporting). Puede afectar a productos robóticos comercializados con software, pero existen particularidades para investigación/código abierto y una clasificación jurídica que no debe asumirse de forma indiscriminada.

**[P] Diseño de ciberseguridad:**
- interfaz de control sin exposición pública por defecto;
- roles y autorización granular por tipo de acción (observar, moverse, cortar, energizar, cargar);
- autenticación fuerte dispositivo-dock-ordenador, tráfico cifrado, rotación/revocación de claves;
- imágenes y telemetría domésticas **locales**, cifradas, retención mínima;
- updates firmadas, reproducibilidad de firmware, rollback, arranque confiable cuando sea viable;
- trazas inmutables de acciones sensibles y watchdog que lleva a estado seguro;
- separar redes y credenciales de robots, cámaras, taller y servicios personales;
- pruebas de prompt injection contra manuales/documentos externos: nunca convertir texto no confiable en órdenes de actuador;
- procedimiento privado de divulgación de vulnerabilidades y SBOM de dependencias.

**No confundir** una biblioteca de software que funciona offline con un dispositivo ciberseguro.

## 5. Derecho a reparar y pasaporte de producto

**[D]** La [Directiva UE 2024/1799](https://eur-lex.europa.eu/eli/dir/2024/1799/2026-07-31) establece reglas que promueven reparación, con aplicación/transposición en el marco previsto; la [Comisión informó de nuevos derechos desde el 31/07/2026](https://commission.europa.eu/news-and-media/news/right-repair-new-consumer-rights-easy-and-attractive-repairs-2026-07-31_en). El futuro portal europeo para encontrar reparadores está previsto para **2027**; **no significa que se pueda intervenir automáticamente cualquier dispositivo bajo garantía sin efectos jurídicos**.

**[D]** El Reglamento [Ecodiseño ESPR (UE) 2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng) configura **pasaportes digitales de productos** con obligaciones dependientes de legislación/actos por producto. La [Comisión registra normas armonizadas de pasaporte en 2026](https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/digital-product-passport-dpp_en).

**[P]** Diseñar ya **fichas técnicas/identificadores digitales locales** para piezas y reparaciones, compatibles conceptualmente con DPP, sin afirmar que cumplen requisitos normativos aún no definidos para ese producto.

## 6. Requisitos físicos de seguridad: contrato de autonomía

**Zonas del sistema:**
- **Zona humana:** lento, alcance y fuerza restringidos; prohibir herramientas calientes/cortantes/eléctricas automatizadas.
- **Zona de taller cerrada:** herramientas/impresora y trabajo con piezas, con enclavamientos, ventilación, sensores y autorización.
- **Zona de pruebas de locomoción:** escaleras/obstáculos bajo retención y barreras físicas.
- **Zona de intervención profesional:** sistemas de gas, red fija eléctrica, refrigerantes, alta energía o riesgo elevado; robot solo actúa como auxiliar si lo permite procedimiento experto.

**Estados de seguridad:**
- `STOP`: orden física de emergencia prioritaria;
- `SAFE_HOLD`: postura estable/soportes asegurados; no asumir que apagar motores mantiene una carga;
- `ENERGY_ISOLATED`: energías peligrosas desconectadas y comprobadas;
- `SUPERVISED`: operador competente supervisa tareas de riesgo limitado;
- `MAINTENANCE_LOCKOUT`: estación inmoviliza robot y verifica desenergización antes de cambiar módulo.

**[P]** Validar cada transición con sensórica/interbloqueos físicos. Si falla un sensor de fuerza o visión, debe aplicarse política degradada; en tareas sin percepción suficiente, detenerse.

## 7. Peligros particulares que deben figurar en FMEA

| Peligro | Mecanismo | Mitigación preliminar y ensayo |
|---|---|---|
| Volcar por brazo extendido | momento fuera del polígono de apoyo | modelar CG, fuerzas y ensayo bajo retención |
| Atropello/atrapamiento doméstico | velocidad, masa y contacto | detección independiente, velocidad limitada, stop probado |
| Caída desde escalera | contacto incorrecto o resbalamiento | ensayo con arnés, estimador de estabilidad, barrera |
| Fuga tras intervenir lavadora | junta/manguera mal instalada | ensayo estanqueidad antes de recolocar |
| Cristal fracturado en vitro | carga de ventosa/palanca mal distribuida | soportes y simulación de carga |
| Carga errónea de batería | alineación incorrecta, temperatura | BMS, contactos seguros, protección térmica |
| Retiro de tornillo equivocado | estructura en tensión/energía almacenada | secuencia verificada, inmovilización y autorización |
| Software comprometido | instrucciones remotas fraudulentas | autenticación, scope, registro y control aislado |
| Reciclado de plástico | cuchillas, calor y emisiones | máquinas protegidas, ventilación, protocolos apropiados |

## 8. Qué NO decidir solo con un sitio web

No inferir que una norma industrial cubre automáticamente un robot de servicio ni que un marcado CE de un subsistema certifica el sistema integral. Preparar matriz «función → peligro → norma y legislación aplicables → método de ensayo → responsable → evidencia». Pedir revisión de profesional cualificado para cada ámbito y jurisdicción concreta.

**Fuentes primarias:** [ISO 13482:2014](https://www.iso.org/standard/53820.html), [ISO/FDIS 13482:2026](https://www.iso.org/standard/83498.html), [UE 2023/1230 consolidado](https://eur-lex.europa.eu/eli/reg/2023/1230/en), [CRA](https://digital-strategy.ec.europa.eu/es/policies/cra-reporting), [AI Act Comisión](https://digital-strategy.ec.europa.eu/es/policies/regulatory-framework-ai), [R2R 2026](https://commission.europa.eu/news-and-media/news/right-repair-new-consumer-rights-easy-and-attractive-repairs-2026-07-31_en), [ESPR](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng).
