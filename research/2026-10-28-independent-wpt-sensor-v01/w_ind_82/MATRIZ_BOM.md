# W-IND-82 — matriz y BOM de evaluación, NO compra

| Área | Alternativas | Decisión |
|---|---|---|
| Dock de carga | separado de datos y módulos | **NO APROBADO**, batería/BMS desconectados. Regulación, FOD y parada propia obligatorias |
| Potencia sensor | cable sellado, conector de retención y recambio | **BASELINE** para comparar precio, fatiga y energía |
| Potencia sensor | WPT sencillo sin feedback | **RECHAZADO** sin FOD/offset/temperatura/EMI y desconexión segura |
| Potencia sensor | WPT regulado 1–20 mW | **CANDIDATO SIN DATOS** de consumo TX con RX cargado, picos o calor |
| Datos | ESP-NOW unicast cifrado + W82 | **PRIMERA OPCIÓN SW** pendiente de consumo y RF real |
| Datos | OpenThread 802.15.4 + W82 | **ALTERNATIVA**, memoria, topología, coste y energía desconocidos |
| RFID | WISP5 | pospuesto: lector extra, microenergía intermitente |
| Seguridad | supervisor y 2 cortes físicos fail-off | obligatorio para transmisor futuro, independiente de radio; W81 no cualificó máximo temporal |

## BOM con abastecimiento auxiliar Diotronic

| Referencia funcional | Diotronic local | Alternativa trazable | IVA/precio final, MOQ, stock local | Motivo |
|---|---|---|---|---|
| Sensor diagnóstico 1–20 mW, sin modelo final | pendiente SKU y existencias | fabricante + TME/Mouser/DigiKey | **pendiente** | primero tensión mínima/corriente real |
| MCU ESP-NOW + radio cifrada, sin modelo final | pendiente | módulo Espressif de fabricante + distribuidor | **pendiente** | consumo de 66 B/ACK no medido |
| MCU OpenThread/802.15.4, sin modelo final | pendiente | fabricante certificado, TME/Mouser/DigiKey | **pendiente** | comparar, no integrar doble stack |
| TX/RX WPT regulado baja potencia | pendiente; bobina suelta NO válida | fabricante con datasheet P_TX/P_RX y FOD | **pendiente** | no aprobar sin curvas bajo carga |
| Supervisor, FOD, temperatura y corte autónomo | pendiente documentación seguridad | fabricante + distribuidor especializado | **pendiente** | exige máximos eléctricos, trazabilidad |
| Cable premontado, pasivos, conectores | pendiente stock Zaragoza | Diotronic si equivale y mejora coste, o TME/Mouser/DigiKey | **pendiente** | sustitución simple y rápida |

Sin cotización puesta en Zaragoza, sin cifra inventada de stock/MOQ y sin órdenes. **0 euros gastados**; no equivale a coste del robot. Pruebas de protocolo no aprueban hardware.
