# Fábrica Doméstica Autónoma Abierta — FDAA

> Proyecto de futuro: un ecosistema doméstico, abierto y progresivamente autónomo para **comprender, fabricar, mantener, reparar y reciclar** objetos, con ingeniería inversa, IA local y robótica cooperativa.

**Estado — 13 de octubre de 2026:** investigación y propuesta técnica; **no existe un prototipo funcional completo**. Todas las dimensiones y prestaciones de hardware son **objetivos que deben verificarse**. Este repositorio es un punto de partida documental, no un producto ni una garantía de seguridad.

### Documento canónico

- **[Especificación integral con todos los antecedentes](docs/PROYECTO_CANONICO.md)**: documento maestro completo, conservado íntegramente.
- **[Publicación original en GitHub: issue #2](https://github.com/Valdi320/Valdo/issues/2)**: hilo de visión y propuestas.
- **[Hoja de ruta](docs/08-hoja-de-ruta-y-metricas.md)**, **[seguridad](docs/07-seguridad-y-riesgos.md)** y **[decisiones abiertas](docs/10-decisiones-y-proximos-pasos.md)**.

### Autosostenimiento e investigación continua: 23 de octubre de 2026

- **[Informe de autosostenimiento, 24 casos y plan de continuidad](research/2026-10-23/README.md)**: energía, agua, alimentación, fabricación y límites de dependencia industrial.
- **[Precios consultados y exclusiones](research/2026-10-23/PRECIOS.md)** y **[290 referencias principales](research/2026-10-23/FUENTES.md)**. Sin compras ni prototipos nuevos; no se declara alcanzado un gasto cotidiano de cero euros.

### Investigación ampliada: octubre de 2026

- **[Investigación complementaria con referencias verificadas](research/2026-10-13/README.md)** — 10 informes sobre tamaño/estabilidad, destreza y mantenimiento, obstáculos NAMO, IA y simulación, metrología y CAD, materiales y reciclaje, legislación y ciberseguridad, datos técnicos, evaluación económica y fuentes.
- **[30 experimentos priorizados](research/2026-10-13/experimentos-priorizados.csv)** y **[30 riesgos adicionales](research/2026-10-13/riesgos-adicionales.csv)**, pendientes de ejecución/validación.
- **[ADR-0002](docs/ADR-0002-estrategia-de-investigacion.md)** — estrategia de simulación y pruebas modulares antes de comprar robots completos.

**Hallazgos que condicionan el diseño:** bancos NIST para montaje de conectores/tornillos, navegación con objetos movibles, necesidad de metrología calibrada, degradación de polímeros reciclados y cambios normativos en 2026. El hardware de referencia (RTX 4080 de 16 GB y 24 GB de RAM) **no cumple el mínimo de RAM de 32 GB publicado para Isaac Sim**; empezar con simulación más ligera. **No hay todavía hardware FDAA construido.**

### Arquitectura propuesta

| Sistema | Meta |
|---|---|
| Ingeniería inversa digital | Ghidra, pruebas de equivalencia, reconstrucción y firmware cuando el acceso sea legítimo |
| Descompilador físico portátil | Escáner multimodal, metrología, CAD paramétrico, hipótesis y pruebas |
| IA local | Planificador de herramientas con objetivo exploratorio 16–24 GB VRAM; control de seguridad separado |
| Microfábrica | Impresión 3D multimaterial, ensamblaje, mecanizado cuando haga falta, verificación |
| Materiales circulares | Celulosa, lignina, PHA, polímeros reciclables, metales recuperados y pasaporte de material |
| Robot A / B | Dos manipuladores móviles compactos, modulares, capaces de asistirse y reemplazar módulos |
| Estación-taller | Docking, carga, diagnóstico, mantenimiento, reparación externa y almacén |
| Movilidad | Obstáculos movibles, escaleras, ruedas-patas o alternativas, puentes/rampas y elevador de cargas |

**Envolvente candidata del robot:** **45 × 70 × 40 cm plegado**, cuatro ruedas-patas, dos brazos de siete grados de libertad y torso ajustable. **No es un diseño validado**: puede ser necesario agrandarlo o dividir funciones entre robots y plataforma auxiliar. Las reparaciones de lavadora, placa de cocción y frigorífico se plantean de extremo a extremo; las intervenciones peligrosas se excluyen de los prototipos autónomos iniciales.

### Primer experimento de alto retorno

Una pieza mecánica **no crítica** se escanea → convierte a CAD editable → fabrica → mide → instala con un brazo robótico → prueba. Después el robot **vuelve al dock, carga y ejecuta un diagnóstico**. Solo se escala a tareas más difíciles tras ensayos trazables y controles de riesgo independientes de la IA.

### Cómo usar este repositorio

- Lee primero **[la especificación canónica](docs/PROYECTO_CANONICO.md)**.
- Consulta los [módulos técnicos](docs/README.md) y [registros de decisión](docs/ADR-0001-arquitectura-preliminar.md).
- Registra cada experimento con el [formato de ensayo](tests/FORMATO_ENSAYO.md) y cada riesgo con el [registro](safety/REGISTRO_RIESGOS.csv).
- Antes de comprar componentes, completa la [plantilla de BOM](hardware/BOM_PLANTILLA.csv) y verifica dimensiones, masa, pares y estabilidad.

### Principios irrenunciables

**Medido ≠ inferido ≠ demostrado.** Privacidad local y software abierto cuando sea posible; control independiente de seguridad; diseño modular; no prometer robot universal, material milagroso ni fabricación doméstica de semiconductores avanzados. Reparar y reutilizar antes de destruir o degradar. No asumir que un diseño abierto es automáticamente seguro o legal para comercialización.

**Licencias:** pendientes de decisión informada y revisión de dependencias; no se declara ninguna licencia abierta por el mero hecho de publicar esta propuesta. Ver [CONTRIBUTING.md](CONTRIBUTING.md).