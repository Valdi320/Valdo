# W-IND-16 — Auditor geométrico del esquema KiCad (29/10/2026)

## Mejora concreta
W-IND-15 sólo contaba cadenas de etiquetas y comparaba un JSON, sin recalcular los extremos reales de los pines KiCad. Mover U2, dejando sus etiquetas en su sitio, podía pasar inadvertido. Este hito añade un lector original de S-expressions que calcula posiciones, números, nombres y tipos de pines, valores, huella y orientación de los DOS TPS22918 y cuatro resistores; coteja las conexiones contra el contrato. Se niega a aceptar nuevas pistas, cables, buses, etiquetas globales y esquemas jerárquicos sin revisar su topología real. Incluye **24 pruebas nuevas** con mutaciones adversarias. Es un control de integridad geométrica estática, NO KiCad ERC, simulación SPICE, aislamiento de seguridad ni autorización para alimentar circuitos.

Reproducción: python3 sch_graph_audit.py y python3 -m unittest -v test_w_ind_16_schematic_reality. GitHub Actions ejecuta ambas órdenes junto a la suite W previa. Resultado de fixture sintético independiente: 24/24 PASS antes de publicar; la CI sobre el esquema real es el criterio de publicación.

## Matriz de decisión
| Opción | Retorno y límite | Estado |
|---|---|---|
| Conteo textual W-IND-15 | No detecta pin desplazado sin etiqueta | Insuficiente |
| Este auditor S-expr | Bloquea desplazamiento, rotación, cambio de pin/valor y by-pass nuevo | Elegido como control digital |
| KiCad CLI/ERC + netlist | Verificación eléctrica auténtica | Pendiente, no ejecutada |
| SPICE + FOD térmico y doble corte físico | Seguridad de banco | Pendiente, no construida |

## BOM
[BOM W-IND-16](BOM_W_IND_16.csv): ningún componente eléctrico nuevo y ninguna compra. Mantener los candidatos de W-IND-15 sin aprobación. Diotronic es proveedor auxiliar sin stock local, IVA final, MOQ y comparación TME/Mouser/DigiKey concluyentes. No usar el resultado para fabricar PCB.

## Revisión de fuentes, titulares y licencias (HEAD comprobados el 29/10/2026)
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0, master 7c7858c: igual al pin.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause, master 08332bc: igual al pin.
- [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause, default 640kHz 604eee2: diverge **68 delante / 11 detrás** del pin d978a69. Sin adoptar modificaciones.
- [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0, master c3b5f9b: igual al pin; PR recientes de compatibilidad IDF 5.5 no integradas aquí.
- [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause, main 51aa078: 9 commits posteriores al pin 7009584; [v2026.10.0](https://github.com/openthread/openthread/releases/tag/v2026.10.0) como referencia.
- [OOMWOO oficial](https://github.com/makerspet/oomwoo), main 1c2bd43: no modificado. VALDO PR #9 es W; no se toca PR #79 cleaning-jobs ni repos externos.

Revisados decisión NO-Xiaomi, contrato C/W, D22 y contrato WPT_DATOS_V01; el checkout local master original tiene cambios de compañeros no tocados. No se copia fuente ni CAD de autores ajenos.

## Límites y siguiente puerta
**Cero medidas propias de WPT/radio, FOD, temperatura, EMI, desalineación, eficiencia o vida útil.** Los controles EN_A y EN_B siguen sin supervisores físicos independientes, no hay protección demostrada de backfeed o sobrecorriente. La carga de dock y batería/BMS continúa separada y desconectada; RF ESP-NOW/OpenThread es sólo datos, y WISP se reserva para microsensores.

Próximo paso: ejecutar KiCad CLI/ERC en un entorno aislado y documentar errores reales; diseñar protección autónoma FOD/térmica/retorno antes de un banco resistivo autorizado. Sin compras, energía, impresión, soldadura ni cambios de firmware.