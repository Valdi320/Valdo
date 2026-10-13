# Acoplamiento, estación-taller y reparación recíproca

> Extracto temático del [documento canónico](PROYECTO_CANONICO.md). Conserva secciones y numeración originales. Estado: diseño conceptual no validado.

## 9. Volver a una base de carga barata y fiable: inspiración Xiaomi S12

El **Xiaomi Robot Vacuum S12** usa información de navegación del entorno y **sensor de carga por infrarrojos** para alinear el aparato con su base; Xiaomi indica alcance efectivo aproximado de **4 metros** para ese sensor. Esto no significa que detecte directamente la estación desde cualquier parte de la casa: primero localiza la región mediante su mapa y odometría, luego corrige la aproximación próxima. Si la base cambia de sitio o hay obstáculos puede fallar. Ver [especificaciones Xiaomi S12](https://www.mi.com/es/product/xiaomi-robot-vacuum-s12/specs/) y [guía oficial de regreso](https://www.mi.com/global/support/faq/details/KA-124398/).

**Para nuestro robot, propuesta modular de bajo coste:**

1. **SLAM y mapa local**: sabe dónde está y dónde espera encontrar la estación.
2. **Navegación al área de aproximación**: planifica la ruta con obstáculos, puertas y condiciones energéticas.
3. **Marcador AprilTag** visible cerca del dock para estimar posición relativa; opcionalmente IR como respaldo.
4. **Guías mecánicas de acoplamiento** para absorber pequeños errores de pose; topes seguros.
5. **Contactos protegidos, BMS y supervisión de corriente/temperatura**: confirmar carga real antes de declarar éxito.
6. **Detección de dock movido**: búsqueda visual limitada, confirmación, actualización de ubicación; varias bases o base auxiliar por planta.
7. **Modo degradado offline**: el docking y la seguridad funcionan aunque la IA generalista no esté disponible.

Software existente a evaluar: [Nav2 Docking Server](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/core_servers/configuring_docking_server/) y [AprilTag](https://github.com/AprilRobotics/apriltag). El coste marginal de balizas/impresiones puede ser bajo si el robot ya tiene cámaras, navegación y ordenador, **pero batería, contactos, mecánica y protección eléctrica no son gratis**.

---

---

## 10. La base de carga debe ser un tercer robot, estacionario

### Zonas funcionales

- **A: recarga/comunicaciones**: guiado, energía, BMS, protección, gestión de temperatura y sincronización de registros.
- **B: inspección y diagnóstico**: cámara, iluminación, prueba de sensores, consumo de motores, holgura, ruido, temperatura, calibración, limpieza de contactos y ópticas.
- **C: reparación**: soporte que inmoviliza al robot, manipulador independiente, herramientas de extracción y atornillado, almacén de módulos, calibración y pruebas posreparación.

### Secuencia de mantenimiento

Regreso al dock → confirmar que carga → recopilar telemetría → inspeccionar desgaste → limpiar → ejecutar diagnósticos selectivos → identificar fallos persistentes → inmovilizar en zona de reparación → cambiar módulo **si la operación ha sido validada** → calibrar → probar en condiciones seguras → autorizar próxima salida o bloquearla.

**Ejemplo:** una pata consume más corriente que antes al producir la misma fuerza. La estación compara curvas históricas para distinguir posible rozamiento externo de fallo interno; solo tras una prueba de diagnóstico independiente inmoviliza y sustituye módulo, comprobando luego el par/posición/temperatura.

**Fallo lejos de la estación:** el segundo robot puede remolcar o asistir. **Fallos simultáneos:** acceso manual, subsistemas independientes y mecanismos de recuperación. No diseñar un sistema que dependa absolutamente de un único Wi-Fi, suministro o controlador.

---

---

## 11. Dos robots para reparación recíproca y continuidad

**Robot A:** fabricación, reparaciones domésticas y uso general. **Robot B:** inspección, soporte, rescate y mantenimiento. Ambos podrían intercambiar roles y usar la misma biblioteca de herramientas, pero conviene diversificar determinados fallos comunes.

**Reglas mecánicas:**

- Módulos sustituibles de ruedas, patas, articulaciones, motores/reductoras, brazos, cámaras, baterías, cableado y placas.
- Acceso exterior a tornillos y conectores incluso cuando el robot receptor esté **apagado o inmovilizado**.
- Conectores codificados mecánica y eléctricamente, sin poder intercambiar polaridad/tensión por error.
- Posiciones de mantenimiento estables y articulaciones externamente liberables cuando sea seguro.
- Identificación de compatibilidad, versiones, firma de repuestos y par de fijaciones conocido.
- El otro robot o el brazo del dock pueden reemplazar módulos sin necesitar que el receptor mueva sus brazos.
- Registro de piezas montadas, número de ciclos, desgaste, calibración y autorización de salida.
- Sistema de rescate para un robot inmóvil fuera de la base; acceso humano cuando no haya rescate automático.

**Prueba fundamental:** inducir avería inocua y controlada de módulo, dejar A apagado, hacer que B extraiga/sustituya módulo y verifique; repetir B apagado y A reparando. Después ensayar fallos comunes de software, fuente, batería y estación.

Referencia científica (no robot doméstico de mantenimiento total): [Columbia Engineering: Robot Metabolism, julio de 2025](https://www.engineering.columbia.edu/about/news/robots-grow-consuming-other-robots), sobre integración y reutilización modular de partes robóticas.

---
