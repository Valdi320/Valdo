# W-IND-83 — energía de ráfagas RF frente a WPT para sensor reemplazable

**1 noviembre 2026. Autoría original W, exclusivamente software matemático. Robot nuevo independiente, nunca trasplante Xiaomi.**

El verificador establece dos puertas **distintas** para un sensor auxiliar de lectura, de baja potencia y datos inalámbricos: (a) que una ráfaga radio no agote su reserva de energía entre V_hi y V_floor; (b) que entre ráfagas pueda recuperar, de forma estacionaria, al menos toda la energía consumida. Un condensador más grande NO arregla un déficit de potencia promedio. La radio transporta datos, no energía; tampoco corta físicamente motores, bomba, TX WPT, dock o batería.

## Procedencia y parámetros: dato de fabricante frente a HIPÓTESIS

**Dato verificable del autor de silicio:** [Espressif ESP32-C3 datasheet v2.4, §5.6.1, Table 5-7](https://documentation.espressif.com/esp32-c3_datasheet_en.html): modo Wi-Fi TX 802.11b 1 Mbps, 21 dBm, 25 °C, 3,3 V, corriente pico 335 mA a 100 % duty; 3,3 V × 335 mA = **1.105,5 mW**. El dato NO demuestra corriente de ESP-NOW en mensajes W82 de 66 bytes, ni duración real de transmisión ni un máximo garantizado para el módulo, ni cubre RX, ACK, retries, despertar ni regulador.

**Suposiciones de escenario — NO observaciones**: RX inductivo ideal entrega constantemente **20 mW**, consumo sensor en reposo **2,9 mW**, un modo radio de 1.105,5 mW ocupa **10 ms** cada **250 ms**; capacitor **efectivo** ideal de **15 mF** entre 3,30 y 3,00 V. Sin ESR/fuga/temperatura/derating ni fallos de control, FOD, acoplamiento o tensión intermedia. Los intervalos son deliberadamente hipotéticos, no anunciados por Espressif.

## Resultado matemático reproducible

- Demanda promedio **47,004 mW** y RX entregaría 20 mW: déficit **6,751 mJ cada 250 ms**; ninguna capacidad finita sostiene indefinidamente ese ciclo.
- Un pulso requiere **10,855 mJ netos**, capacidad efectiva mínima **11,487 mF** entre 3,30 y 3,00 V. Con **10 mF** falla primera ráfaga; con **15 mF** pasa primera y falla segunda, tras recarga ideal entre ellas.
- Contraejemplo hipotético: **1 ms** y 2 mF permite las seis ráfagas sintéticas y balance medio positivo. Por tanto **no se rechaza ESP-NOW genéricamente**: se rechaza aprobarlo sin perfil de consumo real.
- W82 (secuencia, CRC, HMAC, ACK de aplicación, timeout, sesión tras brownout) es independiente. HMAC no cifra: privacidad depende de radio real; ninguna transmisión habilita un corte o rearme crítico.

## Reproducir y clasificar evidencia

Ejecutar en Python 3 estándar sin red ni hardware, desde raíz del repositorio:
1. python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_83 -p test_*.py -v
2. python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_83/w83_energy.py > /tmp/w83-evidence.json
3. cmp /tmp/w83-evidence.json research/2026-10-28-independent-wpt-sensor-v01/w_ind_83/expected.json

**27 tests** adversariales/deterministas: finitud, tensión, potencia, energía, saturación, recarga, cap límite, pérdida RX y no aprobación de hardware. CI dedicada repite prueba de identidad byte a byte y exporta JSON. Es una simulación de energía ideal, NO simulación electromagnética SPICE ni medición física.

## Matriz por problema: dock, alimentación, datos

| Área | Opción | Decisión técnica |
|---|---|---|
| Dock de carga | WPT regulado con FOD, temperatura, offset, humedad, EMI y dos cortes | BLOQUEADO. Batería y BMS completamente desconectados; carga litio fuera del alcance |
| Potencia sensor | Cable sellado y reemplazable | REFERENCIA BASE por coste, eficiencia y reparabilidad |
| Potencia sensor | WPT sencillo, sin feedback/corte independiente | NO APROBADO por ausencia de regulación/FOD/corte |
| Potencia sensor 1–20 mW | WPT regulado, RX/condensador | HIPÓTESIS; no hay pareja TX/RX con consumo cargado y standby cualificados |
| Datos | ESP-NOW cifrado a nivel enlace más W82 | Preferencia SW, ACK/CRC/seq/timeouts/HMAC en modelo; tiempos y privacidad reales NO demostrados |
| Datos | OpenThread 802.15.4 | Alternativa, consumo RAM y RF sin medir |
| Microsensores | WISP5 RFID sin batería | Pospuesto; lector y funcionamiento intermitente |
| Seguridad | FOD, térmica, UVLO y doble corte fail-OFF local | BLOQUEADO, no depender de radio ni permitir rearme remoto |
| Potencia motores/bombas | Distribución cableada protegida | Mantener hasta mediciones de consumo y eficiencia; prohibida adopción WPT por defecto |

## BOM y Diotronic auxiliar, sin orden ni selección

| Componente / función | Diotronic Zaragoza | Otra fuente / precio individual | MOQ, stock y motivo |
|---|---|---|---|
| Espressif ESP32-C3-WROOM-02-N4 | Stock en tienda, SKU exacta, precio final IVA PENDIENTES | [TME](https://www.tme.eu/es/katalog/modulos-de-iot-wifi-bluetooth_113196/p%2Cespressif_1109/) **3,43 € IVA incluido** indicado; [DigiKey](https://www.digikey.es/es/products/detail/espressif-systems/ESP32-C3-WROOM-02-N4/14553031) **3,49690 € IVA incluido** indicado; [Mouser](https://www.mouser.es/es/ProductDetail/356-ESP32C3WROOM02N4) 3,13 €, IVA por confirmar | MOQ 1 en distribuidores, stock remoto anunciado, no stock local; envío, PCB portadora y costes finales Zaragoza sin cotizar |
| Reserva efectiva 15 mF | SKU y stock PENDIENTES | TME/Mouser/DigiKey, precio sin verificar | Sin capacitor elegido; ESR, tolerancia, temperatura y capacidad efectiva desconocidos |
| Par WPT TX/RX 1–20 mW regulado | No identificado | Fabricante / distribuidores especializados sin precio | Falta documentar consumo TX cargado/standby, FOD/corte; no apto aún |
| Supervisor UVLO, termometría, FOD, doble corte | Seguridad sin SKU cualificada | Fabricante/distribuidor especializados PENDIENTES | Requiere tiempos máximos garantizados y comportamiento fail-OFF |
| Cable reemplazable y conectores retenidos | Pasivos/connectores: equivalencia y precios PENDIENTES | TME/fabricantes, PENDIENTES | Baseline de coste/servicio, sin elegir material todavía |

Precios indicativos consultados 01/11/2026, IVA y stock local no confirmados salvo los datos expresamente indicados. NO se presume que un catálogo equivale a stock de Diotronic ni que bobina/placa sean aptas. Cero compras.

## Auditoría terceros, propietarios, HEAD reales, licencias

Contraste del 01/11/2026 con el registro SHA del documento maestro 19-alternativas-abiertas-para-robot-independiente.md del 28/10. Ningún código/CAD externo copiado; propietarios respetados:

| Autor/repositorio | Rama HEAD | Comparación con base registrada | Licencia |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) | master 7c7858c0dd7040801b6f191df1396115560218f0 | idéntico | GPL-3.0 |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) | master 08332bc398aa3350d351ef2aaac163f8007cffda | idéntico | BSD-2-Clause |
| [wisp/wisp5](https://github.com/wisp/wisp5) | 640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2 | **DIVERGE** del SHA d978a697, +68/-11 commits; no confundir rama local | BSD-2-Clause |
| [espressif/esp-now](https://github.com/espressif/esp-now) | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | idéntico | Apache-2.0 |
| [openthread/openthread](https://github.com/openthread/openthread) | main c6872259f4194fb76c7d333bda209343e8c88e71 | +21 frente 7009584dadc20 | BSD-3-Clause |

OOMWOO oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df también revisado; VALDO propio PR #9 y VALDO_OOMWOO local consultados. Worktree VALDO compartido tiene cambios de otros; **no alterado**. No tocar ramas upstream ni PR #79 cleaning-jobs. Revisar releases/PR de terceros antes de adoptar, especialmente diverged WISP y nuevo OpenThread.

## Bloqueo y siguiente hito

La pareja WPT, corriente real de TX+RX+ACK+retries+despertar, mínimo de tensión, derating de condensador, EMI/offset, FOD/térmica/corte independiente **no están medidos**. Antes de comprar/energizar hardware, preparar banco aislado y protocolo de seguridad con autorización explícita; carga litio, estaciones, motores y bombas excluidos. Medir ciclo de potencia para comprobar matemáticas de W83 frente a cable reemplazable. Cero pruebas físicas, placas, compras o cambios OEM.
