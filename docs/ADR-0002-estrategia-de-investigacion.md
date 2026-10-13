# ADR-0002 — Investigación incremental y simulación primero

**Fecha:** 2026-10-13. **Estado:** PROPUESTA ADOPTADA PARA PLANIFICACIÓN; no constituye una validación de hardware.

## Contexto

La visión FDAA combina un descompilador físico/digital, materiales circulares, fabricación, dos robots compactos, locomoción por escaleras y una estación de reparación. Un prototipo integral desde el principio concentraría costes, fallos y riesgos. El tamaño objetivo 45×70×40 cm es aún **hipotético**.

La [investigación complementaria de octubre de 2026](../research/2026-10-13/README.md) confirma:
- NIST ofrece tableros reproducibles para montaje y desmontaje.
- ROS Lyrical es LTS nuevo en 2026; Jazzy/Gazebo tiene ejemplos maduros.
- Isaac Sim requiere actualmente mínimo 32 GB de RAM de sistema, más de los 24 GB del PC de referencia, aunque la RTX 4080 16 GB satisface su mínimo de GPU.
- La manipulación segura de cables/engranajes/conectores y el control de estabilidad necesitan sensores y ensayos, no solo modelos de lenguaje.

## Decisión

**Fijar un programa experimental de módulos y puertas G0–G9**:

1. **Simular antes de comprar:** CAD + MuJoCo/Drake para estabilidad, patas, brazos, límite de tamaño y fuerza; Gazebo/ROS 2 para sensores, navegación/dock. Isaac Sim solo tras comprobar requisitos.
2. **Comenzar por la destreza y la metrología:** escaneo calibrado → CAD paramétrico → pieza → medida; banco NIST de tornillos/conectores/arneses de baja energía.
3. **Probar retorno a base y mantenimiento básico:** Nav2 docking, AprilTag/carga verificada y sustitución de un módulo sencillo mediante estación.
4. **Construir después la reparación cruzada A ↔ B** en banco, con un robot receptor apagado; probar fallos comunes.
5. **Decidir arquitectura de locomoción por datos:** comparar base omnidireccional estabilizada, ruedas-patas y orugas en simulación y ensayos con retención.
6. **Separar tareas críticas de IA:** controlador físico independiente, autorización, sensores y posibilidad de rechazar un plan sin información suficiente.
7. **Ampliar a electrodomésticos completos solamente con escenarios seguros** y personal competente donde se exija.
8. **Gestionar circularidad por ensayos:** materiales y lotes, reextrusión con medición, separación y fin de vida verificable.

## Alternativas rechazadas por ahora

- Comprar directamente dos robots multipropósito de alto coste sin pruebas de manipulación.
- Elegir forma humanoide o cuadrúpeda únicamente por apariencia.
- Suponer que una impresora única fabricará metales, bioplásticos, chips y baterías.
- Instalar Isaac Lab/Sim completo en el PC actual sin resolver requisitos RAM/entorno.
- Autorizar desmontaje o conexión eléctrica peligrosos a un agente sin supervisión física.
- Aceptar éxito por una sola demostración filmada.

## Consecuencias

**Positivas:** menores costes irreversibles, benchmarks comparables, trazabilidad, interfaces reutilizables y rutas de recuperación. **Negativas:** avances modulares menos espectaculares; tareas de integración adicional; un brazo fijo inicial no demuestra movilidad doméstica.

## Criterio de abandono/revisión

Revisar ADR si datos de CAD/ensayo indican que una arquitectura alternativa es superior o si requisitos legales/materiales/cómputo cambian. Ninguna preferencia de la conversación prevalece sobre seguridad, física y evidencias.

**Enlaces:** [research/index](../research/2026-10-13/README.md), [plan de ensayos](../research/2026-10-13/09-pruebas-y-economia.md), [mecánica](../research/2026-10-13/01-arquitectura-mecanica.md), [IA y simulación](../research/2026-10-13/04-ia-local-y-simulacion.md), [seguridad](../research/2026-10-13/07-seguridad-y-normativa.md).
