# W-IND-94 — BOM y abastecimiento (sin compras)

Este hito es exclusivamente una **corrección de pruebas automáticas**; no añade hardware, dependencias, servicios ni cuotas de licencia. **Coste incremental de BOM de robot = 0,00 €; no equivale al precio de un módulo inalámbrico completo.**

| Elemento | Cantidad nueva | Diotronic / alternativa | Precio final IVA | Stock en Zaragoza | Decisión y motivo |
|---|---:|---|---|---|---|
| Componentes físicos añadidos | 0 | Diotronic: no aplica; TME/Mouser/DigiKey: no aplica | 0,00 € (ninguna compra) | No aplica | Solo tests; evita coste y riesgo |
| Placas WPT, bobinas, lector, condensador, protecciones | 0 | Diotronic auxiliar / distribuidores trazables | Pendiente; no presupuestado para W94 | **Sin verificar** | No seleccionar sin ensayo y seguridad |
| Transceptor ESP-NOW u OpenThread | 0 | Según hardware y trazabilidad futuros | Pendiente | **Sin verificar** | La prueba es transporte-neutral, no exige radio |

**Límites:** no reutilizar precios anteriores como cotización actual ni inferir disponibilidad local. Para el futuro BOM físico se exigirán referencia exacta, hoja de datos, IVA, mínimos, envío, stock de tienda, FOD/temperatura y corte autónomo. No comparar ahorro físico contra cable sin mediciones.

Matriz de coste/beneficio: corrección de test y CI, coste de componentes cero; riesgo de regresión cubierto por tres casos nuevos y regresión general; **fiabilidad RF y ventajas económicas físicas indeterminadas**.
