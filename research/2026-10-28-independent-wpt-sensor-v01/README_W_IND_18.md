# W-IND-18 — ERC REAL BLOQUEA LA PR, NO SOLO GENERA UN INFORME (29/10/2026)

## Mejora concreta y amenaza corregida
El hito W-IND-17 ejecutó KiCad 9.0.2 real, archivó las infracciones y terminó GitHub Actions en **verde** a pesar de **9 infracciones eléctricas**. Un lector podía confundir «auditoría ejecutada correctamente» con «circuito aprobado». W-IND-18 introduce un **gate CI bloqueante** después de guardar los artefactos originales. El check de KiCad falla expresamente mientras haya cualquier infracción, incluida advertencia de biblioteca. Sin resultados válidos y consistentes también falla cerrado. La suite Python de este mismo módulo sigue ejecutándose antes de KiCad, para separar calidad del verificador de calidad del circuito.

El informe original W-IND-17 prueba: **3 errores** (VIN_5V etiquetado sin conexión y dos pines de alimentación no excitados) y **6 avisos** (biblioteca VALDO no registrada). [Ejecutado de verdad en W-IND-17](https://github.com/Valdi320/Valdo/actions/runs/40824443976) con JSON y attestation preservados. El nuevo check se diseñó para que esas 9 infracciones produzcan un check **rojo por motivos eléctricos, intencionadamente**, no una falla de herramienta. Nunca sustituir por `continue-on-error`, ignorar avisos o simular un ERC limpio.

## Archivos y reproducción
- `w_ind_18_erc_policy.py`: coteja el JSON de ERC nativo con la attestation W17, el SHA256 exacto del esquema, su ruta, la versión real KiCad 9.0.2, el SHA de CI, la procedencia y las declaraciones físicas en falso. Código de salida **1** con violaciones, **2** si las pruebas son inválidas/incompletas, **0** únicamente con ERC nativo sin infracciones (aun así NO_APTO_PARA_FABRICAR).
- `test_w_ind_18_erc_policy.py`: 15 pruebas deterministas; 9 errores replicados a partir de categorías *observadas* en el JSON real, cero, modificación del esquema, falseo de atestación, omisión de JSON, cambio de SHA/versión, etc.
- `.github/workflows/w-ind-17-kicad-erc.yml`: genera artefactos con `if: always()` **antes** del paso de bloqueo. Ejecuta `python3 -m unittest -v test_w_ind_17_erc_gate test_w_ind_18_erc_policy`. Se puede reproducir la lógica offline; el ERC real exige KiCad 9.0.2 según flujo CI.
- Ensayo local aislado de la nueva política: **15/15 PASS**. Se leyó además el **JSON real de 9 infracciones** descargado del artefacto W17: resultado esperado `(False, 9)` con fuente de prueba sustituta; no equivale a repetir KiCad. El resultado de GitHub Actions de ESTE commit confirma la integración real y debe consultarse separadamente.

## Matriz de decisión
| Opción | Ventaja | Riesgo | Decisión |
|---|---|---|---|
| CI verde y archivo JSON (W17) | Diagnóstico disponible | Check verde mal interpretable con 9 infracciones | **Rechazado** |
| Descartar avisos o PWR_FLAG artificial para maquillar ERC | Check verde fácil | Oculta conexiones sin diseñar y bibliotecas incompletas | **Prohibido** |
| CI rojo mientras ERC real tenga >0 violaciones, con informe preservado | Hace visible el bloqueo técnico y exige corrección genuina | PR permanece bloqueada hasta corregir el diseño | **Implementado** |
| Considerar ERC cero como aprobación eléctrica | Ninguna garantía real | No detecta FOD, calor, reverse-feed, EMI, fallos dobles | **Prohibido** |

## Separación de problemas y límites
*Potencia de dock*: batería y BMS completamente desconectados, sin cargas de litio ni diseño de estación fabricable. *Potencia local*: exclusivamente esquema de TX 5V conceptual para sensor hipotético 0,4W medio / 1,5W pico; motores y bombas excluidos. *Datos*: contrato de secuencia, CRC, ACK y timeout de W-IND-01, sin integrarse radios ni confundir radio con potencia. ESP-NOW y OpenThread siguen alternativas; WISP sólo es relevante para microsensores. FOD, temperatura, sobrecorriente, offset, humedad, eficiencia, EMI y dos cortes realmente independientes **sin pruebas físicas**.

## Titularidad, licencias y revisión exacta de 29/10/2026
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power): **GPL-3.0**, master **7c7858c0dd7040801b6f191df1396115560218f0**, sin cambio desde pin de 28/10; último PR #1 fusionado en 2021. No se copia software ni CAD.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw): **BSD-2-Clause**, master **08332bc398aa3350d351ef2aaac163f8007cffda**, coincide con pin; PR #1 de 2015. [wisp/wisp5](https://github.com/wisp/wisp5): **BSD-2-Clause**, default **640kHz**, HEAD **604eee2dffaeba3a270de61cf3dae887a33309c2** frente a pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; ramas divergentes **68 ahead / 11 behind**, no fast-forward.
- [espressif/esp-now](https://github.com/espressif/esp-now): **Apache-2.0**, master **c3b5f9be245f1a80db9cb938600566aa6a8dd1e5**, igual al pin; cambios de compatibilidad IDF en commits/PR anteriores, no se integra firmware.
- [openthread/openthread](https://github.com/openthread/openthread): **BSD-3-Clause**, main **51aa078ee4fe1ad803bc83ca7b372e7ab62120f3**: 9 commits posteriores al pin 7009584dadc20cf20c20a6062f357dd572ba6885; #13809 movió constante de CSL el 29/10, otros commits de address filter y Thread Direct; no se integra código.
- [makerspet/oomwoo](https://github.com/makerspet/oomwoo): Apache-2.0, main **1c2bd43abcf74288afcf2d8b64514cc325f9b905**; no se toca PR #79 ni repos de autores. PR #9 VALDO es la única destino de esta rama W.

Documentos maestros del 28/10, D22, C/W, LEEME_PRIMERO y WPT_DATOS_V01 consultados, reglas W y otras automatizaciones revisadas; no se editan sus archivos/locks. Licencia propia VALDO **pendiente de selección**, no se incluye material GPL ni código de terceros.

## BOM/abastecimiento
[BOM W-IND-18](BOM_W_IND_18.csv): no incorpora hardware ni cambia componentes. Diotronic sólo fuente auxiliar para pasivos equivalentes, sin referencias/precio IVA/MOQ/stock local acreditado; dispositivos de seguridad requieren datasheet y distribuidor con trazabilidad. **0 € gastados, 0 hardware energizado.**

## Siguiente puerta
Resolver las 3 infracciones ERC reales SIN PWR_FLAG ficticios, registrar biblioteca original VALDO y sus 6 advertencias; sólo después diseñar supervisores autónomos FOD, temperatura, protección inversa y cortes normalmente apagados, con esquema KiCad + netlist/DRC. ERC limpio no aprobará hardware.
