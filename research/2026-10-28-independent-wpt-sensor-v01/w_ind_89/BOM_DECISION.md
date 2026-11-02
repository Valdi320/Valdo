# W-IND-89 — BOM, decisiones y autoría, 01/11/2026

**Solo cribado digital, importe total puesto en Zaragoza NO conocido, cero compras.** Diotronic es proveedor AUXILIAR; no alterar arquitectura por stock ni aprobar seguridad por precio.

## BOM comparativa exploratoria

| Ítem | Fuente Diotronic / alternativa; precio con IVA 21% y MOQ | Disponibilidad local/verificación y criterio |
|---|---|---|
| ST25DV04KC-IE8S3, SO8N (solo chip EH) | **Diotronic pendiente** / Farnell ES ref.3972494 **~1,12 €**, MOQ 1 (0,926 € sin IVA), portes no incluidos. https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494 | Catálogo visible, stock Zaragoza NO verificado. SO8N más reparable; falta lector, antena, regulación y FOD. |
| El MISMO SKU (contraste) | Diotronic pendiente / RS ref.248-7495 **5,83 € lote 5** IVA, MOQ 5. https://es.rs-online.com/web/p/modulos-rf/2487495 | Stock anunciado en otro centro, NO local; lote más caro que Farnell para solo uno. |
| Rubycon 16YXG1200MEFC10X23, 1200 µF NOMINALES, 16 V | Diotronic pendiente / Farnell ES ref.2346191 **~0,59 € IVA**, MOQ 1 (0,49 € sin IVA). https://es.farnell.com/rubycon/16yxg1200mefc10x23/conden-1200-f-16v-20/dp/2346191 | Existencias de catálogo visibles, tienda Zaragoza NO verificada. ±20%, ESR, fugas y C EFECTIVA bajo carga NO calificados; no elegido. |
| Lector ISO15693+antena y emisor | Diotronic solo si equivalente / TME, Mouser, DigiKey o fabricante: SKU y precio pendientes | **BLOQUEO** del coste completo y consumo del lector, no existen medidas en nuestro banco. |
| Regulador DC (lineal/buck o boost) | Diotronic pasivos / TME, Mouser, DigiKey y ficha del fabricante: SKU, precio, MOQ y stock pendientes | 0,20 V es hipótesis, NO dropout de chip alguno; exigir máximo por temperatura, carga, eficiencia, arranque y trazabilidad. |
| Corte local, supervisor térmico y FOD | Diotronic solo con trazabilidad / distribuidores especializados: precio pendiente | Seguridad crítica sin tiempo máximo garantizado ni circuito ensayado; NO aprobación. |
| Cable desmontable (baseline de vida útil) | Diotronic / TME, Mouser, DigiKey: sin dimensiones, cotización, MOQ, IVA/porte final | Ningún supuesto ahorro global demostrado. |

TME, Mouser y DigiKey no aportan aquí **cotización verificada exacta de este SKU y condiciones de entrega**; constan como alternativa por confirmar, no se inventa coste. Diotronic Zaragoza: Av. Valencia 5; https://diotronic.com/contactenos ; tienda no consultada por teléfono, stock local NO afirmado. No confundir precio de catálogo con stock local. Costes totales incluyen lector, antena, PCBA, sujeción C, envío, impuestos, medición, reparación y tiempo. Sin compras.

## Matriz de decisión funcional

| Opción | Limitación crítica | Dictamen |
|---|---|---|
| Cable sustituible y fijado | C aporta ruta, longitud/vida/coste todavía sin medir | BASELINE, mantener |
| Potencia inductiva simple no regulada | precarga, offset, FOD/temperatura/EMI/corte ausentes | BLOQUEADA |
| WPT regulada con FOD térmico y desconexión local independiente | sin regulador cualificado ni pruebas propias, dock/BMS separados | CANDIDATO NO APROBADO |
| Captación ST25DV04KC con lineal/buck | 0/22 muestras ST cumplen conjunción de 3 restricciones **bajo escenario de 0,20 V**, no sentencia sobre hardware | NO SELECCIONAR aún |
| Elevador DC-DC | puede resolver tensión pero no se conoce rendimiento/arranque/curva | DATOS REQUERIDOS |
| WISP5 | ecosistema RFID, potencia mínima, lector específico | SECUNDARIO |
| ESP-NOW frente OpenThread | solo datos; ACK aplicación, CRC, secuencia, timeout y privacidad por verificar | DECISIÓN ABIERTA |
| Motores, bombas, estación de carga litio | potencias y seguridad no medidas | FUERA DEL PILOTO; NO energizar |

## Revisión exacta de cuatro proyectos externos (5 repos, propietarios y licencias)

Contraste HEAD contra SHAs registrados en 19-alternativas, GitHub 01/11/2026; se inspeccionaron PRs de autores y no se copiaron ni modificaron sus fuentes:

| Proyecto del autor y licencia | Rama HEAD actual y comparación con SHA 28/10 | PR/changelog reciente comprobado |
|---|---|---|
| https://github.com/mark-belbin/simple-wireless-power GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 = registrado, 0/0 | PR #1 TX board v1.1 integrada 2021 |
| https://github.com/wisp/wisp5-hw BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda = registrado, 0/0 | PR #1 integrada 2015 |
| https://github.com/wisp/wisp5 BSD-2-Clause | **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2, **divergencia +68/−11** de d978a6978ad23ccd6c44dd55430973b04a3d4a9b | PR #40 abierta histórica; NO ordenar ramas por nombre |
| https://github.com/espressif/esp-now Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = registrado, 0/0 | PR #151 y #153 cerradas 2026 sin incorporación |
| https://github.com/openthread/openthread BSD-3-Clause | main c6872259f4194fb76c7d333bda209343e8c88e71, **+21/−0** de 7009584dadc20cf20c20a6062f357dd572ba6885 | PR #13800 integrada 31/10; #13814/#13826 abiertas 01/11 |

Makerspet OOMWOO oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, último cambio 29/10 ornamental. Valdo master 8a6030bda52a159493a42dc4bed245e722b876e8. PR #9 es **propia W**; PR #79 cleaning-jobs ajena y NO tocada. El checkout local de Codex está sucio y NO se editó; 10 clones OOMWOO originales y adaptación ROS2 siguen intactos. Automatización OOMWOO pausada, no solapamiento conocido. Las licencias de terceros no se sustituyen ni cambian por las de Valdo. Evidencia matemática no certifica FOD/EMI/agua, hardware, radio o seguridad.
