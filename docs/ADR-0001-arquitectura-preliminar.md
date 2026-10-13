# ADR-0001 — Arquitectura de referencia

- Fecha: 2026-10-13.
- Estado: **PROPUESTA**, aún sin CAD de masas ni ensayos físicos.

## Contexto

El sistema debe ser compacto para viviendas, pero manipular dispositivos, superar obstáculos, cooperar en reparaciones y operar principalmente con IA local. Ello crea conflictos de estabilidad, energía, tamaño, coste y seguridad.

## Decisiones provisionales

1. IA planificadora local con herramientas y modelos especializados; **control físico de seguridad independiente** y determinista.
2. Robot candidato de **45 × 70 × 40 cm plegado**, con cuatro ruedas-patas, dos brazos con siete grados de libertad, torso ajustable y cambio automático de herramientas.
3. Externalizar grandes cargas a un transportador/elevador, y el mantenimiento complejo a una estación-taller con manipulador independiente.
4. Segundo robot con interfaces estándar que pueda asistir y reparar al primero; ambas máquinas deben aceptar intervención con energía aislada.
5. «Descompilador físico» multimodal con CAD paramétrico y mediciones verificadas; no prometer penetración universal de sensores.
6. Microfábrica multiproceso con recuperación de materiales separados, ensayos de resistencia y control de calidad.
7. Prioridad a software abierto, privacidad y operaciones offline que toleren pérdida de red o LLM.

## No decidido

- Ruedas-patas frente a ruedas omnidireccionales/orugas.
- Volumen, masas, par de actuadores, autonomía y estabilidad real.
- Distribución de computación entre robot y estación.
- Alcance del kit de rampas/puentes y herramienta elevadora.
- Familia concreta de materiales y técnicas de fabricación.

## Criterio de revisión

Modelar CAD completo con baterías/motores/reductoras/estructura, simular momentos y escaleras, medir fuerzas y calor, redactar FMEA, aprobar ensayos y presupuesto antes de fabricar. **Redimensionar si el tamaño candidato incumple la física o la seguridad.**

[Documento canónico](PROYECTO_CANONICO.md)
