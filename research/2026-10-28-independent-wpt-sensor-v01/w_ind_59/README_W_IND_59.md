# W-IND-59 — puerta de identidad funcional de dos canales INA219 (solo software)

**30 de octubre de 2026. Robot aspirador NUEVO, independiente, abierto, local y reparable; ámbito W exclusivo.** La decisión del 28/10/2026 CANCELA el trasplante Xiaomi X20 Pro OEM. No se opera sobre firmware, batería, BMS, motores, bomba, estación, OOMWOO oficial, CAD de C, PR #79 ni fuentes de otros creadores.

## Hallazgo y mejora original verificable

En W-IND-57/W-IND-58 se leen bytes I²C y se verifican capturas temporales de 2 INA219. Sin embargo, dos direcciones lógicas diferentes (0x40 y 0x41) **NO prueban que los dos sensores físicos TX/RX sean independientes y estén bien etiquetados**. Si se duplica, intercambia o congela un canal, la eficiencia WPT inferida puede resultar ficticia, aunque cada transacción I²C y CRC funcione.

W-IND-59 publica un verificador Python, sin acceso al hardware, para evaluar tres patrones de referencia **independientes** y una matriz de respuesta 2×2. Detecta en datos sintéticos canales alias, intercambiados, bloqueados, acoplamiento indebido, ganancia incorrecta, sesgo y registros malformados. Incluye conversor de capturas W57 y regresión W57→W58→W59 con dispositivos I²C **simulados**. Se rechaza por defecto la evidencia insuficiente. No existe un ID de silicio único verificado del INA219: una respuesta correcta no demuestra identidad física, calibración ni autenticidad de la referencia.

Patrones puramente matemáticos: baseline TX/RX 2000/2000 mV; TX aislado 5000/2000 mV; RX aislado 2000/4000 mV. Los umbrales propios de screening, **hipótesis y NO valores homologados**, son: error absoluto <=60 mV, paso >=1000 mV, movimiento de referencia no excitada <=40 mV, ganancia diagonal 0,90–1,10, ganancia cruzada <=0,05, determinante >=0,80 y duración <=30 s. Un sistema fraudulento que reproduzca las tres respuestas podría pasar. No mide corriente ni temperatura, ni demuestra FOD, EMI, seguridad o eficiencia.

### Reproducibilidad

Ejecutar desde la raíz de Valdo con Python estándar 3.10+ (no instalar paquetes):

```sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_59 -p 'test_w59.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_59/w59_mapping_gate.py > W59_SYNTHETIC_NOT_HARDWARE.json
```

**24 pruebas digitales** enumeradas, incluyendo la regresión integrada con el código propio W57/W58. En entorno sin fuentes W57/W58, solo pueden ejecutarse 23/24, por lo que el PASS final debe comprobarse en GitHub Actions. La demostración sintética produce matriz identidad, determinante +1 y PASS_PATTERN_ONLY; alias, determinante 0 y REJECT_PATTERN; canales cruzados, determinante -1 y REJECT_PATTERN. En todos los casos se devuelven hardware_approved=false, meter_identity_proven=false y physical_measurements_performed_by_this_software=0. CI y JSON adjuntos deben verificarse tras publicar, sin deducir éxito de la mera existencia del workflow.

### Tres problemas independientes, decisión y límites

| Problema | Recomendación provisional | Evidencia que falta |
|---|---|---|
| Carga inductiva en estación | **Diferir** toda integración; nada conectado a batería/BMS/dock | Regulación apropiada, procedimiento seguridad litio, FOD metálico, temperatura, humedad, posición, EMI, corte eléctrico independiente normalmente OFF |
| Potencia inalámbrica a primer sensor hipotético 5 V, 0,4 W media y 1,5 W pico | Comparar cable sencillo reemplazable (referencia económica) contra WPT regulado y WPT sencillo; ningún TX/RX aprobado | Par de bobinas con datasheets, gap/offset 6D, pérdidas/eficiencia medidas, coste puesto en Zaragoza, termometría, FOD y desconexión autónoma local. **No extender a bombas/motores/turbinas** |
| Datos inalámbricos | ESP-NOW (Apache-2.0) candidato, OpenThread (BSD-3-Clause) alternativa; WISP (BSD-2-Clause) solo microsensores RFID de energía mínima | ACK de aplicación, CRC, secuencia antireplay, timeout, autenticación/cifrado, privacidad, pérdida de enlace y recuperación. Radio NO transmite potencia NI autoriza parada crítica |

La solución de este hito es **instrumentación de investigación**, no un controlador WPT. No se diseñó nueva PCB; ninguna de las condiciones de seguridad de hardware ha sido satisfecha. Las 16 comprobaciones físicas del antiguo D22 siguen 0/16; el ERC eléctrico histórico W-IND-18 permanece pendiente de resolución.

### Autoría y HEAD externos comprobados el 30/10/2026

| Creador/repo y licencia | Pin en documento maestro 19-alternativas (28/10) → HEAD de rama (30/10) | Historial / PR |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master 7c7858c0 → **idéntico** | [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) fusionada 2021; ejemplo WPT del autor sin protección suficiente. No copiar GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master 08332bc3 → **idéntico** | [PR #1](https://github.com/wisp/wisp5-hw/pull/1) fusionada 2015; RFID energy harvesting necesita lector |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | pin d978a697 frente rama **640kHz** HEAD 604eee2d → **DIVERGE 68 por delante, 11 por detrás** | [PR #40](https://github.com/wisp/wisp5/pull/40) abierta; no fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master c3b5f9be → **idéntico** | [PR #153](https://github.com/espressif/esp-now/pull/153) cerrada sin fusionar 11/02/26; commit IDF v6 10/09/26 |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main 7009584d → e577777c, **14 por delante** | CI/CLI/radio/build 29/10; [PR #13819](https://github.com/openthread/openthread/pull/13819) abierta |

[OOMWOO oficial](https://github.com/makerspet/oomwoo) main f01a1b295f46 (29/10, star-history); upstream PR #78 fusionada, [#79 cleaning-jobs](https://github.com/makerspet/oomwoo/pull/79) abierta y fuera de W. [OOMWOO firmware](https://github.com/makerspet/oomwoo-firmware) main c63a21e14e7d (30/10, Specs/pinout), [PR #3 watchdog](https://github.com/makerspet/oomwoo-firmware/pull/3) abierta; no se ha tocado. VALDO propio PR #9 rama W HEAD anterior 342da328, checkout local de otro Codex está sucio y se preservó sin edición. Otras automatizaciones revisadas: ninguna activa compitiendo con W. **No se ha copiado código ni CAD de terceros**.

Fuentes locales leídas antes de modificar: 00_DECISION_20261028_NO_TRASPLANTE_X20.md; 19-alternativas-abiertas-para-robot-independiente.md; inalambrico_auditoria_gpt6_20261027/d22/ (informe y contrato); coordinacion/cableado_inalambrico_acuerdo_20261027/ (acuerdo y relevos); VALDO_OOMWOO/LEEME_PRIMERO.md; adaptacion/contratos/WPT_DATOS_V01.md. Fuente del fabricante: [TI INA219](https://www.ti.com/product/INA219), [hoja de datos](https://www.ti.com/lit/ds/symlink/ina219.pdf).

## BOM y abastecimiento

[BOM_W_IND_59.csv](BOM_W_IND_59.csv) y [MATRIZ_W_IND_59.csv](MATRIZ_W_IND_59.csv): coste de **electrónica adicional por robot = 0€** por ser solo software, **NO** se afirma coste total del futuro banco. Dos INA219 montados a 7,26€ IVA son referencia histórica sin portes ni calibración; el catálogo ManoMano/Satkit (2,42€/pieza) y DigiKey bare IC INA219AIDCNR (2,2506€/IC con IVA, excluyendo placa) no son ofertas verificadas en Zaragoza. Diotronic solo proveedor auxiliar, con referencias, existencias de tienda, MOQ y total final con IVA **pendientes**; priorizar distribuidor especializado para controlador WPT, FOD, protección térmica, corte independiente y BMS, siempre documentado y trazable. No comprar basándose en listado de catálogo.

## Bloqueo y siguiente paso

**0 mediciones reales, 0 adquisiciones I²C físicas, 0 energía física aplicada**. La independencia de los medidores, su calibración y la referencia no se han verificado. Se exige ensayo futuro con fuente aislada y resistencias ficticias, medidor de referencia independiente trazable, procedimiento de seguridad y autorización expresa, dejando batería/BMS/dock desconectados. No autoriza energizar, imprimir, comprar, soldar, instalar servicios ni cambiar firmware/maquinaria.