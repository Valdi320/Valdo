# Riesgos, restricciones y seguridad

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 14. Aspectos subestimados: investigación nueva de alto retorno

### 14.1. Metrología y trazabilidad

Cada componente debería poder asociarse a una cadena: **fuente/sensor → lectura calibrada → tolerancia → CAD → proceso → lote/material → pieza real → medición de aceptación**. El error de una cámara o escáner no es el error final de fabricación. El sistema deberá distinguir precisión, repetibilidad y veracidad de medición.

### 14.2. Tacto y control de fuerza como prioridad

Un brazo con visión perfecta puede romper un conector o el borde de una vitrocerámica si solo conoce posición. Priorizar medición de **fuerza, par, deslizamiento, material blando, fricción** y pruebas con útiles desechables de bajo riesgo. Los sensores táctiles como AnySkin y plataformas como Digit Plexus son vías abiertas que merecen prototipo.

### 14.3. Diseño para desmontaje robótico

Todos los objetos creados por nuestra microfábrica deberían tener, siempre que resulte práctico, **tornillos accesibles desde posiciones alcanzables, conectores únicos o codificados, carcasas reparables, instrucciones incorporadas, referencias visuales y módulos etiquetados**. Es más fácil que dos robots se reparen mutuamente si nacen diseñados para la operación, que si intentan manipular dispositivos irreparables de terceros.

### 14.4. Razonamiento y ensayo de fuerzas sobre muebles

Necesitamos saber **cuándo NO empujar, levantar o pisar**. El robot deberá estimar masas y apoyos, buscar documentación, aplicar fuerzas de prueba solo cuando el entorno sea seguro y calcular márgenes. Un colchón, una encimera de vidrio o una balda aparentemente rígida no son apoyo aceptable por defecto.

### 14.5. Redundancia y recuperación

Dos robots no resuelven el problema si ambos usan el mismo firmware con error, dependen del mismo controlador o pierden la misma fuente. Redundar selectivamente **mecanismos de diagnóstico, parada y recuperación**, preservar herramientas manuales y capacidad de rescate. El propio taller necesita diseño para reparación.

### 14.6. Energía, disipación y condiciones ambientales

Medir energía total de fabricar una pieza o efectuar una reparación, incluyendo GPUs, motores, ventilación, secado de material, carga, desperdicios y transporte. Añadir protección de incendio, polvo, vapores, humedad y ruido; si el objetivo es sostenibilidad, comparar contra comprar una pieza fabricada industrialmente.

### 14.7. Ciberseguridad y privacidad doméstica

La visión robótica puede captar dormitorios, documentos y personas. Diseño **local por defecto**, retención limitada, permisos sobre zonas de la casa, actualizaciones firmadas, control de acceso y registros de decisiones. El texto de un manual obtenido por Internet nunca podrá autorizar por sí mismo operaciones físicas peligrosas o modificar las políticas de seguridad.

### 14.8. Leyes físicas y economía real

Una pieza que se puede imprimir no es necesariamente más barata, duradera o ecológica. Decidir **fabricar, reparar, reutilizar, comprar repuesto o pedir servicio profesional** mediante mediciones, valor total, impacto, vida útil y riesgos. Los procesos caros o peligrosos deben quedarse fuera de casa cuando tenga sentido.

### 14.9. Evaluación del sistema a largo plazo

La diferencia entre un vídeo espectacular y un robot doméstico útil es la **fiabilidad bajo miles de acciones, ambientes nuevos, suciedad, desgaste y fallo de sensores**. Registrar intentos, errores, rescates, caídas, daños y tiempos de mantenimiento. No eliminar pruebas fallidas de las métricas.

---

---

## 16. Seguridad, salud, calidad y restricciones legales

El proyecto debe implementar desde el primer prototipo:

- **Parada de emergencia física** y limitaciones independientes del LLM, watchdog, estado seguro tras pérdida de energía/comunicación.
- Interbloqueos para cargar baterías, ejecutar herramientas, introducir brazos en huecos o energizar instalaciones.
- Límites estrictos de velocidad y par según entorno, colisión, proximidad humana y estado del objeto.
- Supervisión de vuelco, contacto con escaleras, deslizamiento, sobretemperatura y zonas de atrapamiento.
- Ensayos con **arnés de seguridad** en escaleras antes de cualquier demostración doméstica.
- Aislamiento verificado de aparatos antes de desmontar. Riesgos residuales de condensadores, presión, refrigerante, calor y partes móviles.
- Exclusión de tareas de red eléctrica fija, gas, circuito frigorífico sellado y otras operaciones reguladas salvo equipos y profesionales autorizados.
- Los equipos de rayos X y similares no se consideran componentes DIY domésticos; normativa y seguridad radiológica son una barrera legítima.
- Recuperación humana y no destructiva cuando los sistemas automáticos fallen.
- Registros de incidentes, análisis sistemático de riesgos y manual de parada y mantenimiento.

**Referencias:**
- [ISO 13482:2014, robots de asistencia personal](https://www.iso.org/es/contents/data/standard/05/38/53820.html). Figura publicada en 2026 y se encuentra en proceso de revisión.
- [ISO 10218-1:2025, robots industriales](https://www.iso.org/es/contents/data/standard/07/39/73933.html). **No** sustituye por sí sola la normativa de servicio doméstico.
- [Reglamento (UE) 2023/1230 sobre máquinas](https://eur-lex.europa.eu/eli/reg/2023/1230/spa), con aplicación general desde **20/01/2027**.
- [Directiva (UE) 2024/1799 sobre promoción de la reparación](https://eur-lex.europa.eu/eli/dir/2024/1799/2026-07-31); revisar transposición y ámbito concreto al construir/comercializar.

**La publicación de planos abiertos no exime a fabricantes o constructores de obligaciones legales.** Cada fase debería contar con revisión específica si se utiliza fuera de entornos de ensayo.

---

---

## 19. Riesgos principales y diseño para no quedar bloqueados

| Riesgo | Respuesta de diseño |
|---|---|
| No cabe todo en el chasis | CAD y comparación de configuraciones; aumentar tamaño o distribuir funciones |
| Baja estabilidad al empujar/tirar | apoyo extendido, sensor de par, planificador de momento de vuelco |
| Escalera peligrosa | pruebas con retención, límites de geometría, alternativa de transporte |
| Pieza nueva de material insuficiente | ensayos, biblioteca de propiedades, rechazo de uso crítico |
| Desconocimiento de cable/conector | escaneo, manual, desconexión segura, abortar |
| Error de la IA | verificador independiente, confirmación y controles de seguridad |
| Robo/filtración de vídeo doméstico | almacenamiento local y control de acceso |
| Dos robots averiados | estación separada, redundancia selectiva y acceso manual |
| Fallo del ordenador principal | control embebido y estado seguro |
| Propiedades internas no observables | informar incertidumbre y pedir laboratorio/desmontaje |
| Reciclaje caro o perjudicial | análisis ciclo de vida y opción de comprar repuesto |
| Dependencia de un fabricante | interfaces abiertas, documentación, módulos estándares |
| Coste de robot demasiado alto | hitos pequeños de mesa, escalado solo tras resultados |
| Proceso normativamente restringido | remitir a profesional/equipo certificado |

---
