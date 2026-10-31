# W-IND-65 — Política RF fail-closed para el primer sensor independiente

**31-10-2026 | Entrega DIGITAL original, W exclusivamente.** Robot aspirador NUEVO, abierto, reparable e imprimible. Se mantiene la decisión 28/10: **NO** trasplante de firmware, electrónica, pack, BMS, estación ni otros componentes Xiaomi X20 Pro. No se ha modificado OOMWOO, PR #79, clones de autores ni trabajo de C/otros compañeros.

## Problema, solución y medida reproducible

La telemetría previa tenía ACK aplicativo, CRC, secuencia, expiración, autenticación HMAC W61 y AES-256-GCM W64; **no había un control automático de perfil de radio** que bloquease accidentalmente un piloto ESP-NOW en claro, sin LMK, con PMK de fábrica, broadcast, o que confunda el callback de envío MAC con ACK aplicativo. Tampoco distinguía con contrato ejecutable la seguridad de enlace de OpenThread de cifrado de aplicación.

W65 introduce un validador **fail-closed** (w65_rf_policy.py) con entrada JSON de campos explícitos y tipos exactos, decisión digital y razones por código. Solo permite como **candidato experimental** ESP-NOW unicast con CCMP nativo declarado (LMK de 16 bytes y PMK personalizada), o ese mismo enlace con W64 adicional; OpenThread solo con AEAD aplicativo y MTU sin cualificar. Exige ACK de aplicación, CRC, secuencia, timeout ≤250 ms, máximo dos reintentos y **corte de seguridad independiente de la radio**. Broadcast, rol de motor/bomba/dock, PMK por defecto, falta de peer binding, callbacks de radio usados como ACK y configuraciones incompletas se rechazan. **Nunca devuelve producción aprobada.** La función examina DECLARACIONES, no lee ni configura chips ni verifica que claves y corte realmente existan; la criptografía nativa debe comprobarse físicamente antes de usarla.

Una exploración **sintética** de 512 combinaciones de nueve permisos nativos ESP-NOW acepta exactamente **1/512**, la configuración declarada completa. Las pruebas no demuestran seguridad criptográfica ni fiabilidad real: solo comportamiento del software. En el contrato existente w_link.py DATA/ACK tienen 22 bytes; W64 AEAD 54 bytes. Por tanto, intercambio DATA+ACK = **44 bytes aplicativos** con cifrado CCMP del propio enlace ESP-NOW, o **108 bytes aplicativos** con W64 añadido: diferencia 64 bytes, **59,26 % menos bytes de aplicación**, NO potencia, radio, coste, latencia ni ahorro demostrado. Una cota sintética de tres DATA y tres ACK da 132 frente a 324 bytes; no incluye cabeceras 802.11, CCMP, retransmisiones inferiores, fragmentación ni software. Las pruebas W65 comprueban ambos tamaños contra los módulos reales w_link/W64 ya publicados.

**Frontera de confidencialidad distinta:** ESP-NOW CCMP cifra/autentica el enlace unicast, no necesariamente los datos extremo a extremo frente a gateways y memoria de nodos. W64 AES-GCM aplicativo añade una frontera, pero NO está lista para producto: no existe aún una ancla antirrollback física para su nonce/época, ni aprovisionamiento seguro confirmado. No retirar W64 automáticamente ni declarar ESP-NOW protegido solo porque el JSON ponga LMK=16.

## Separar los tres subsistemas

| Sistema | Requisitos medibles y comparación | Decisión |
|---|---|---|
| Dock inductivo de carga | Potencia/eficiencia medidas; FOD con metales pequeños; temperatura y humedad en estación; offset/ángulos; EMI; doble corte independiente normalmente OFF; BMS/litio cualificados | BLOQUEADO, no batería ni estación conectada |
| Potencia de módulo | Primer sensor 5 V, 0,4 W nominal y 1,5 W pico **solo hipótesis**; WPT simple de Belbin frente a WPT regulado con FOD/temperatura/corte, y cable reemplazable como base económica W47 | Mantener cable provisional; no WPT de motores/bombas ni ensayo físico |
| Datos de módulo | ESP-NOW unicast CCMP y ACK aplicativo, CRC, seq, timeout, identidad y privacidad; alternativa OpenThread/802.15.4 con AEAD de aplicación | ESP-NOW candidato de banco, OpenThread alternativa. No radios elegidas ni medición |

WISP5 solo sería pertinente para **microsensores RFID de energía mínima** con lector apropiado, no alimentación general ni radio ESP-NOW. WPT transmite potencia y radio transmite datos: no son intercambiables ni autorizan movimiento o carga.

## Reproducción / evidencia

Desde research/2026-10-28-independent-wpt-sensor-v01 con Python 3.12; la CI instala cryptography==46.0.4 solo por regresión de W64 (licencia dual Apache-2.0/BSD-3-Clause, implementación NO copiada). Ejecutar en ese directorio:

1. python3 -m unittest discover -s w_ind_65 -p 'test_w65.py' -v
2. python3 -m unittest discover -s w_ind_64 -p 'test_w64.py' -v
3. python3 -m w_ind_65.w65_demo > W65_RF_SYNTHETIC.json

Artefacto JSON marcado SYNTHETIC_RF_POLICY_ONLY y hardware_approved=false. Ni pruebas RF, ni banco eléctrico, ni calibración, ni motores, ni batería/BMS/dock. CI específica PASS no significa seguridad física y no soluciona el ERC histórico W-IND-18 ni CI general anteriores.

## Fuentes, autorías, revisión de SHA/ramas del 31-10-2026

| Autor/proyecto propio del autor, NO copiado | Licencia indicada | SHA registrado en 19-alternativas → HEAD observado |
|---|---|---|
| mark-belbin/simple-wireless-power | GPL-3.0 | 7c7858c0 → 7c7858c0, master idéntico |
| wisp/wisp5-hw | BSD-2-Clause | 08332bc3 → 08332bc3, master idéntico |
| wisp/wisp5 | BSD-2-Clause | d978a697 → 604eee2d, rama **640kHz divergente: 68 ahead y 11 behind**, no inferir actualidad por orden de ramas |
| espressif/esp-now | Apache-2.0 | c3b5f9be → c3b5f9be, master idéntico |
| openthread/openthread | BSD-3-Clause | 7009584d → b6d0f06d, main 18 ahead/0 behind |

También se examinaron avances/comentarios de autores referenciados anteriormente: mark #1, WISP #40, ESP-NOW #151/#153 y OpenThread #13790/#13823, v2026.10.0. OpenThread contiene modificaciones recientes en radio y API, sin adoptar automáticamente su stack. El proyecto de Belbin reporta resultados propios hasta 100 W/81,3 % a ~1–2 mm, **NO son prestaciones de nuestro módulo** ni demuestran FOD, térmica o protección independiente. OOMWOO oficial makerspet/oomwoo HEAD consultado f01a1b29; no modificar modelos, adaptación CAD, firmware ni PR cleaning-jobs #79. VALDO master ajeno con trabajo local sin integrar sigue intacto; solo se escribe en rama W de PR propia #9.

Documentación de los fabricantes y fuentes, sin copia de su código:
- https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html (PMK/LMK 16 bytes, unicast cifrado CCMP; multicast nativo no cifrado; envío MAC distinto de ACK de aplicación)
- https://github.com/espressif/esp-now y https://github.com/openthread/openthread
- https://github.com/mark-belbin/simple-wireless-power
- https://github.com/wisp/wisp5-hw y https://github.com/wisp/wisp5
- https://cryptography.io/en/latest/hazmat/primitives/aead/

## BOM económica, trazabilidad y límites

Consultar BOM_W_IND_65.csv y MATRIZ_W_IND_65.csv. Software W65: **0 € adicionales de componentes por robot**, NO significa que el equipo RF cueste cero. ESP32-C3-WROOM-02-N4 **módulo SMD**, no una placa terminada: referencias orientativas TME ~3,43 €/ud IVA y DigiKey ~3,50 €/ud IVA, exclusión de portes/placa/regulación/protecciones. Mouser ≈3,13 € listado antes de IVA (precio final no confirmado). Diotronic auxiliar: **sin precio, cantidad mínima ni stock físico en Zaragoza verificados**. Solo se aceptan elementos de seguridad con datasheet y trazabilidad. Ninguna compra, soldadura, impresión, energización o flasheo.

**Siguiente puerta:** banco RF aislado autorizado, con evidencia de configuración CCMP real, captura y medición de paquetes/pérdidas, ACK de aplicación, latencia, privacidad y energía por paquete, antes de elegir si W64 AEAD adicional compensa. Para dock y WPT primero se requiere procedimiento de seguridad, corte eléctrico independiente, FOD térmico y medidas; litio siempre desconectado hasta autorización específica.
