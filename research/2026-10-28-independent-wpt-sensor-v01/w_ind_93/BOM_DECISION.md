# W-IND-93 — Decisión, seguridad y BOM (01/11/2026)

| Candidato | Potencia | Datos | FOD/corte local | Decisión |
|---|---|---|---|---|
| Cable desmontable, retención sólida | Cable | Cable o radio opcional | Protección convencional dimensionada | **BASE ECONÓMICA**; medir antes de eliminar |
| WPT simple sin control | Inductiva hipotética | No suministra datos automáticamente | Sin control/FOD demostrados | **NO APROBADO** |
| WPT regulado (sensor no crítico) | Inductiva, consumo RX desconocido | Separar radio de potencia | Temperatura, metal, offset, EMI y doble corte pendientes | **EXPERIMENTAL SIN ENERGIZACIÓN** |
| Dock de carga autónoma | Pendiente especificar | Telemetría no es autorización de carga | FOD/calor/agua/desconexión independiente imprescindible | **BLOQUEADO** (litio/BMS desconectados) |
| ESP-NOW Apache-2.0 | **Ninguna** | RF con ACK de aplicación, CRC, epoch, secuencia, timeout, privacidad y MAC/AEAD | Parada crítica sólo local | Candidato por sencillez, pendiente ensayos |
| OpenThread BSD-3-Clause | **Ninguna** | IPv6/Thread, misma capa de aplicación | Parada crítica local | Alternativa, requiere hardware 802.15.4 |
| WISP5 BSD-2-Clause | RFID ultrabajo consumo | Retrodispersión | No solución de carga/motores | Referencia secundaria |

El cambio **ACK estricto** es software stdlib y no altera la selección de hardware ni el precio de un sensor. La palabra `True` no equivale a autenticación criptográfica. La única reducción acreditada es el rechazo de falsos ACK por **tipos inválidos**. No se contabilizan ahorros de cables/placas, no se aprueba WPT.

| Elemento (cantidad) | Diotronic Zaragoza, precio IVA / stock / MOQ | Alternativa con IVA y disponibilidad | Justificación |
|---|---|---|---|
| Código propio W93, Python stdlib (1) | No aplica | 0 € de hardware añadido por el parche | Sin compra ni costes adicionales de componentes; no cubre integración |
| Cable sustituible con conector (1) | Referencia, precio, stock y MOQ **PENDIENTES** | TME/Mouser/DigiKey **sin SKU/IVA/stock cotejado** | Baseline necesaria contra WPT |
| Lector ST X-NUCLEO-NFC08A1 (1) | Stock local/precio/MOQ **PENDIENTES** | DigiKey ES ~41,08 € IVA incl. (W90, 01/11; stock a revalidar, sin portes) | Sólo banco, no producción |
| Tag ST X-NUCLEO-NFC07A1 ST25DV64KC (1) | **PENDIENTE** | DigiKey ES ~18,57 € IVA incl. (W90, sin portes) | NO extrapolar chip 04KC |
| Regulación, sensor, RF, FOD, corte dual, protección térmica e instrumentación (por definir) | **PENDIENTES** | TME/Mouser/DigiKey: precios/stock/MOQ **PENDIENTES** | Críticos sólo con hoja de datos, trazabilidad y verificación eléctrica |

Estos precios son referencias previas **sin verificación nueva de stock local**. No se presentan como oferta final en Zaragoza: transporte, IVA de conjunto, energía, componentes críticos y mantenimiento no cerrados. Diotronic sólo es apoyo a pasivos/conectores competentes.

Fuentes exactas y licencias: [Belbin GPL-3.0](https://github.com/mark-belbin/simple-wireless-power), [WISP-hw BSD-2](https://github.com/wisp/wisp5-hw), [WISP FW BSD-2](https://github.com/wisp/wisp5/tree/640kHz), [Espressif ESP-NOW Apache-2](https://github.com/espressif/esp-now), [OpenThread BSD-3](https://github.com/openthread/openthread), [ESP-NOW ACK aplicación](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html). Comparaciones 28/10→01/11, PRs y SHAs detallados en README. Ninguna fuente externa importada. VALDO mantiene los derechos propios según licencia que adopte el titular (no presumir licencia por repositorio público).
