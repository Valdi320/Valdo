# W-IND-92 — Matriz técnica, fuentes, propiedad y BOM (01/11/2026)

## Matriz y decisiones

| Ruta | Función | Estado / motivo |
|---|---|---|
| Cable sustituible con fijación robusta | Potencia y datos en primer sensor | **REFERENCIA** económica y mantenible; coste real de conector/cable todavía por cotizar |
| WPT sencillo sin control de RX | Energía a microsensor | **NO APROBADO**: falta regulación, FOD, temperatura, desfase, límites de corriente, EMI y apagado independiente |
| WPT controlado de bajo consumo | Energía a microsensor opcional 1–20 mW | **SOLO INVESTIGACIÓN**: W84 y W92 prueban aritmética, no eficiencia física; W91 impide confundir el kit NUCLEO USB con sensor sin batería |
| Acoplamiento WPT de dock | Estación de carga | **BLOQUEADO**: FOD, offset, humedad, térmica, seguridad y corte autónomo; batería/BMS desconectados |
| ESP-NOW | Telemetría RF | **CANDIDATO DATOS**: ACK de aplicación, CRC, secuencia, timeout, autenticación/cifrado, privacidad y recuperación no sustituidos por ACK MAC |
| OpenThread | Telemetría/red IPv6/Thread | **ALTERNATIVA DATOS**, no sumar dos pilas por rutina; mayor pila/integración, comparar consumo y latencia REALES |
| WISP5 | Sensor RFID de energía ínfima | **REFERENCIA SECUNDARIA**, no alimentar motores/bombas, sin lector ni medidas propias |

W92 corrige la interpretación de una ventana con acumulación (carga y descarga). No garantiza eficiencia WPT ni reduce automáticamente materiales. Requisitos del primer módulo: definir P media y ráfagas con medidas, 1–20 mW como **rango de estudio**, rail/tensión tolerable, distancia/offset, período de ACK, estados apagado, demanda energética del lector, protección física, coste completo y durabilidad. Sin medición no se libera hardware.

## BOM: precios de referencia y abastecimiento (NO COMPRAR)

| Elemento / cantidad | Diotronic Zaragoza (precio IVA, stock local) | Alternativa y precio con IVA | Estado y decisión |
|---|---|---|---|
| ST X-NUCLEO-NFC08A1, lector x1 | PENDIENTE referencia / precio / existencia | DigiKey ES ~41,08 € (W90, observado 01/11, sin portes), TME/Mouser sin verificación | Solo evaluación, no emisor final del robot |
| ST X-NUCLEO-NFC07A1, tag ST25DV64KC x1 | PENDIENTE | DigiKey ES ~18,57 € (W90, sin portes), TME/Mouser sin verificación | Placa de evaluación, NO chip ST25DV04KC |
| NUCLEO-L476RG x0 o x1/2 según host real | PENDIENTE | DigiKey ES ~24,54 €/ud (W90, sin portes) | USB/3V3 no debe confundirse con energía NFC; cero en ensayo RF-only |
| Condensador 1000 µF (valor SOLO del modelo) | Precio/stock/referencia PENDIENTES | TME/Mouser/DigiKey: sin SKU ni precio comparables | No seleccionado: faltan ESR, tolerancia efectiva, fugas, encapsulado y tensión admisible |
| Carga ficticia, sondas calibradas, limitación y corte local normalmente OFF | Precios y stock PENDIENTES | Distribuidores especializados para seguridad: cotización PENDIENTE | Protecciones/instrumentación NO diseñadas ni presupuestadas; no energizar |
| Cable desmontable y retención | Precio/stock PENDIENTES | TME/DigiKey/Mouser: cotización PENDIENTE | Línea base económica; selección pendiente del sensor/conector concreto |

El conjunto de **dos** NUCLEO + dos placas ST se estimó en W90 en 108,73 € IVA incluido sin envío, instrumentación, seguridad ni consumo energético real. No recomendar comprarlo para demostrar sensor sin cables (W91). Diotronic solo proveedor AUXILIAR; ni precios web ni stock remoto prueban existencias locales. No se dispone de precio final puesto en Zaragoza; ninguna pieza de protección crítica se acepta sin trazabilidad, documentación y especificaciones.

## Comparación con revisiones registradas (API GitHub consultada 01/11/2026)

| Creador / repositorio | Licencia | HEAD y rama observados | Contra SHA de 19-alternativas del 28/10 | PR/changelog |
|---|---|---|---|---|
| mark-belbin/simple-wireless-power | GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | Idéntico (0 commits) | Sin PR abiertas; prototipo de autor, no FOD/control regulado probado en el nuestro |
| wisp/wisp5-hw | BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | Idéntico (0 commits) | Sin PR abiertas |
| wisp/wisp5 | BSD-2-Clause | **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2 | **Divergió**: 68 delante/11 detrás de d978a6978ad23ccd6c44dd55430973b04a3d4a9b; no equiparar orden de ramas | PR #40 abierta, actualizada 2021; último HEAD commit 2022 |
| espressif/esp-now | Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | Idéntico (0 commits) | Sin PR abiertas |
| openthread/openthread | BSD-3-Clause | main c6872259f4194fb76c7d333bda209343e8c88e71 | 21 commits por delante de 7009584dadc20cf20c20a6062f357dd572ba6885 | Correcciones MLE #13800/#13802, POSIX #13821 del 31/10; PR #13826, #13814 y #13827 abiertas |

Propiedad exclusiva de sus creadores; W92 no utiliza, altera ni copia sus fuentes/licencias. GitHub OOMWOO oficial revisado: makerspet/oomwoo f01a1b295f462da5ab8d5f021a3f741cbd2b47df (29/10); oomwoo-one jazzy a630d1c77255072d280a2a41a7a2bd1a1c98cadd; oomwoo-cad 038002ddc5586d711960545ecf76a038eec48656; **oomwoo-firmware fd8689f3e3f7bcd0dcc35725be4a48cd9fcc8596** (J1 sin I2C, 01/11) y **oomwoo-pcb ac8ac0b52254582be3acda9d3fddfd06cbbabd4f** (01/11). No se cambian clones upstream, CAD/IF14, ROS2 ni PR #79.

**Coordinación y locks**: se leyeron decisión 28/10, 19-alternativas, D22, contrato VALDO_OOMWOO y acuerdo W/C; W solo es dueño de investigación electrónica y datos, C de fijaciones/CAD. El checkout local Valdo está sucio en rama codex/instrucciones-punto-dulce-20261029 y NO se tocó. No se hallaron ficheros nominales *lock*/*owner* en dicho checkout, pero no demuestra ausencia de bloqueos externos. La automatización OOMWOO está deshabilitada; esta contribución usa exclusivamente rama GitHub propia W de PR #9. No se anunció como trabajo físico ni se editó otro repositorio.

Fuentes matemáticas: [Gamry — energía de condensador ideal y ESR](https://www.gamry.com/application-notes/battery-research/testing-electrochemical-capacitors-cyclic-voltammetry-leakage-current/), [W84](../w_ind_84/README.md), [W91](../w_ind_91/README.md), [ST25DVKC producto](https://www.st.com/en/nfc/st25dv-i2c-series-dynamic-nfc-tags.html), [ESP-NOW docs](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html). El cálculo W92 es original, solo aritmética sobre hipótesis.
