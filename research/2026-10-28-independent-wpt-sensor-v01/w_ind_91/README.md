# W-IND-91 — Procedencia energética del piloto NFC (01/11/2026)

**Robot NUEVO y abierto, solo ingeniería digital.** No reutilizar batería, electrónica, firmware o estación OEM Xiaomi. Hito W exclusivo; sin compras, pruebas físicas, litio/BMS, impresión, soldadura ni cambios en OOMWOO o PR #79.

## Mejora original y verificable

**No confundir una placa de demostración alimentada por USB con un sensor alimentado sin cables.** Según el manual de ST [UM2960 Rev.2](https://www.st.com/resource/en/user_manual/um2960-getting-started-with-the-xnucleonfc07a1-nfcrfid-tag-ic-expansion-board-based-on-st25dv64kc-for-stm32-nucleo-stmicroelectronics.pdf) para la [X-NUCLEO-NFC07A1](https://www.st.com/en/evaluation-tools/x-nucleo-nfc07a1.html), el jumper **ST1 selecciona VCC 3V3 externo o EH para el integrado de etiqueta ST25DV64KC**. No hay evidencia en el esquema de que ST1 alimente desde EH el MCU de una NUCLEO ni un sensor externo completo. La demostración ST conecta placa/MCU por USB y señales I2C/GPO. Estas señales podrían ofrecer retroalimentación: **riesgo por descartar, no fallo demostrado**. La salida EH puede pasar a alta impedancia con campo insuficiente ([ST DB4607 Rev.1](https://www.st.com.cn/resource/en/data_brief/dm00838234.pdf)). La detección de tarjetas de bajo consumo del [lector NFC08A1](https://www.st.com/en/evaluation-tools/x-nucleo-nfc08a1.html) no equivale a campo RF continuo.

En el hito W90 se tasó un conjunto comercial de dos NUCLEO, lector NFC08A1 y tag NFC07A1 en **108,73 € IVA incluido, sin envío ni banco**. Es válido como coste parcial de *evaluación externa*, **no** como prueba de autosuficiencia WPT: dos NUCLEO energizadas por USB no prueban que el sensor reciba potencia inductiva. El tag **64KC** de la placa no es el chip **04KC** de las 22 curvas ST usadas en W85-W89; no trasladar curvas ni rendimientos.

## Verificador del hito (Python original)

El archivo w91_nfc_source_gate.py genera seis casos **sintéticos**, clasifica jumper ST1 (EH, 3V3, retirado, desconocido), EH desactivada, lector sin campo, NUCLEO por USB/3V3, I2C/GPO no aislados, identidad incorrecta de IC, ausencia de canal V_EH al sensor y afirmación falsa de que EH alimenta directamente toda la NUCLEO. Se ha comprobado la salida con **27 pruebas unitarias adversariales propias**, JSON determinista y SHA256. El indicador topology_candidate_only señala únicamente una topología candidata; **hardware_release=BLOCKED SIEMPRE** incluso si alguien marca eh_load_iv_measured=True. Declaraciones del software no acreditan medidas reales o protección eléctrica.

Para reproducir desde la raíz del repositorio:

    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_91 -p 'test_*.py' -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_91/w91_nfc_source_gate.py > /tmp/w91.json
    sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_91/expected.sha256

CI reutiliza el flujo dedicado W88-W90, ejecuta regresiones y publica el JSON (origen **modelo sintético**). El hash demuestra reproducibilidad, no autenticidad física.

## Próxima puerta: una sola prueba física, únicamente previa autorización

Primero documentar cableado de V_EH a una **carga ficticia**, ST1/EH, exclusión efectiva de USB/3V3 y rutas I2C/GPO, con placa RX sin NUCLEO alimentada. Aprobar seguridad con fuente aislada, limitación y corte independiente normalmente OFF, FOD, temperatura, offset, humedad y EMI **ANTES DE ENERGIZAR**. Después registrar V/I RX bajo carga y arranque frío, V/I de entrada del lector, campo y coexistencia con ACK/datos, tasa de intentos, costes totales y comparación con cable desmontable. No comprobar sobre batería, BMS o estación real.

**Tres dominios no intercambiables:** dock de carga (FOD, térmica, humedad, EMI y corte autónomo sin litio), potencia inductiva opcional solo para microsensor no crítico, y datos ESP-NOW/OpenThread con ACK de aplicación, CRC, secuencias, timeout, cifrado, recuperación; jamás RF para parada crítica. WISP5 solo microsensores mínimos. No proponer WPT para motores/bombas sin mediciones. Cable reparable = referencia económica.

Fuentes/owners/SHAs, matriz y BOM Diotronic: [BOM_DECISION.md](BOM_DECISION.md). Sin copiar código ni CAD ajenos. No editamos upstream OOMWOO, clones de autores ni archivos mecánicos de C. **Resultado: bloqueo digital de una falsa demostración de alimentación autónoma, no validación WPT física.**
