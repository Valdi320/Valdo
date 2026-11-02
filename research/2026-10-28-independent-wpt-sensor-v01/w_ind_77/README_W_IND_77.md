# W-IND-77 — Cerrar el falso positivo de energía media: mínimos RX y cobertura de medida

**31/10/2026. Investigación ORIGINAL del ámbito W para un robot aspirador NUEVO y abierto.** CERO ensayos físicos, compras, soldadura, impresión, baterías/BMS, estación, motores o firmware OEM. El trasplante Xiaomi X20 Pro quedó cancelado el 28/10/2026. Ningún resultado aprueba hardware.

## Mejora material verificable

W76 controla la energía TX media por fases. **No puede detectar un microcorte de tensión RX si las medias de potencia RX se siguen declarando suficientes**. Un sensor sin reserva local puede reiniciarse pese a cumplir el presupuesto de Wh/día. Es una limitación del criterio digital, no evidencia de fallos en un transmisor comercial.

W77 añade un **contrato independiente de observación**: ventanas contiguas con reloj relativo, energía TX integrada en mJ (no lectura puntual), mínimo observado de tensión RX con incertidumbre, máxima separación de muestras, capturas TX/RX simultáneas, calibraciones declaradas y múltiples ciclos. Huecos, solapes, datos no finitos, fuentes desconocidas y cantidades inválidas se rechazan. **Las declaraciones de medición no son verificadas por el programa**.

### Pruebas y reproducción

```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_77
python3 -m unittest -v test_w77.py
python3 w77_trace_gate.py --input TRACE_SYNTHETIC.json --output W77_REGENERATED.json
cmp W77_EVIDENCE_SYNTHETIC.json W77_REGENERATED.json
```

**30 pruebas digitales originales** cubren duración, huecos/solapes/reloj, muestras puntuales TX, mínimo RX, separación de muestras, ciclos/calibraciones, incertidumbres, etiquetas falsas de banco, NaN/Inf/booleanos y overflow. Resultado estrictamente **SINTÉTICO**, no proveniente de fabricante o hardware:

| Magnitud | Caso adversarial ficticio | Estado |
|---|---:|---|
| Sensor de referencia y ciclo | 2,9 mW; 30 s | Hipótesis |
| Energía TX integrada | 600 mJ; media 20 mW | Hipótesis |
| Exceso energético frente a cable ideal | +0,4104 Wh/día | **PASA** techo ficticio +0,5 Wh/día |
| Mínimo RX observado durante ventana de 100 ms | **2,5 V** | **FALLA** mínimo hipotético de 3 V |
| Mayor separación de muestras | 5 ms | Pasa pantalla ilustrativa de 10 ms |
| Salida | **BLOCKED** | Sin autorización física |

La caída ficticia a 2,5 V **no demuestra un brownout real**: la tensión mínima real debe derivarse del datasheet de un sensor finalmente elegido. Este test detecta que la energía media puede aprobar un sistema que presenta un mínimo RX inadmisible.

### Ecuaciones y límites

`E_TX = Σ E_ventana` (mJ), `P_TX_media = E_TX/t_ciclo` (mW), `ΔWh_día = (P_TX_media − P_cable_ideal)×24/1000`. Las cotas conservadoras elevan la energía TX según incertidumbre relativa, y restan incertidumbre absoluta al mínimo RX. El mínimo es **observado**; un pulso entre muestras, aliasing, insuficiente ancho de banda, osciloscopio mal calibrado, datos omitidos o procedencia falsa quedan fuera de garantía. El código **nunca** devuelve `hardware_approved=true`, ni asegura funcionamiento continuo instantáneo. Falta instrumentación/trigger adecuados antes de ensayo autorizado. No verifica temperatura, FOD, humedad, EMI, offset, envejecimiento, desconexión física, backfeed, descarga residual o protección del dock.

## Tres problemas independientes

1. **Dock/carga:** fuera del módulo piloto; batería, BMS y carga de litio desconectados. Nada de Xiaomi OEM.
2. **Potencia distribuida:** piloto de sensor no crítico y desmontable, comparado con cable reparable. No aplicar por defecto a motores/bombas. W no modifica CAD ni retira cables sin acuerdo del responsable C.
3. **Datos RF:** ESP-NOW y OpenThread como alternativas, con ACK aplicativo, CRC, número de secuencia, timeout, privacidad y recuperación. No conducen energía ni son un corte físico de seguridad. WISP5 solo para microsensores RFID si la energía disponible lo justifica.

## Autoría y revisión HEAD de los cuatro proyectos externos

Comparado el 31/10/2026 con los SHAs registrados el 28/10 en `19-alternativas-abiertas-para-robot-independiente.md`. Cada autor conserva derechos y licencias. **No se copió código ni CAD ajeno.**

| Repositorio / titular | Licencia | Rama HEAD y relación con registro | Cambios/PR del autor revisados |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) | GPL-3.0 | master `7c7858c0`; idéntico | [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) histórica; evitar copiar hardware/firmware GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) | BSD-2-Clause | master `08332bc3`; idéntico | [PR #1](https://github.com/wisp/wisp5-hw/pull/1) histórica |
| [wisp/wisp5](https://github.com/wisp/wisp5) | BSD-2-Clause | **640kHz** `604eee2d`; diverge **+68/−11** de `d978a697` | [PR #40](https://github.com/wisp/wisp5/pull/40) abierta; último commit 2022, no asumir que rama reciente significa HEAD |
| [espressif/esp-now](https://github.com/espressif/esp-now) | Apache-2.0 | master `c3b5f9be`; idéntico | [PR #151](https://github.com/espressif/esp-now/pull/151) cerrada, merge de compatibilidad ESP-IDF v6 en HEAD |
| [openthread/openthread](https://github.com/openthread/openthread) | BSD-3-Clause | main `b6d0f06d`; **+18/0** contra `7009584d` | [PR #13821](https://github.com/openthread/openthread/pull/13821) y [#13822](https://github.com/openthread/openthread/pull/13822) abiertas; cambios de radio/build |

Revisado [OOMWOO oficial](https://github.com/makerspet/oomwoo) main `f01a1b29` (29/10), [oomwoo-pcb](https://github.com/makerspet/oomwoo-pcb) main `87aa7d38` (31/10), [oomwoo-firmware](https://github.com/makerspet/oomwoo-firmware) main `ce05f266` (31/10), VALDO y adaptación propia. Leídos decisión NO-TRASPLANTE, D22, acuerdo W/C, LEEME_PRIMERO, WPT_DATOS_V01, owners y automatizaciones. El checkout local compartido está sucio en rama de otro compañero: se deja intacto. OOMWOO PR #79 cleaning-jobs pertenece a otro alcance, no se toca.

## Decisiones, BOM y proveedores

Ver `MATRIZ_DECISION_W77.csv` y `BOM_W_IND_77.csv`. La mejora digital requiere **0 € en piezas**. STWBC86JR/STWLC38JRM se conservan solamente como **candidatos documentales**; faltan curvas completas de consumo con RX real a 1–20 mW, mínimos RX, protección independiente, calor y acoplamiento. Diotronic solo auxiliar (pasivos/conectores/prototipado); referencia, MOQ, precio final con IVA+portes y stock local de Zaragoza permanecen **PENDIENTES**, también las alternativas TME/Mouser/DigiKey. Para seguridad, trazabilidad y documentación de fabricante obligatorias; nada aprobado para compra.

**Siguiente puerta:** identificar un conjunto WPT activo con documentación del ciclo completo y preparar medición de energía TX integrada y mínimo V_RX, incluyendo búsqueda, desalineación y recuperación, en banco resistivo aislado **solo** tras protocolo de seguridad y autorización. El ERC KiCad histórico W18 sigue bloqueado por tres infracciones; esta entrega no lo arregla. **Mediciones físicas propias: cero.**
