# W-IND-20 — Biblioteca original KiCad autoreproducible (2026-10-29)

**Mejora publicable:** Se extraen sin alterar las definiciones originales de dos símbolos (TPS22918 y resistencia) del borrador KiCad W-IND-15 y se registran como biblioteca de proyecto `VALDO.kicad_sym` con tabla `sym-lib-table`. Se incorporan 13 pruebas de regresión digital para detectar diferencias de los símbolos, cambio de pines, footprint, alias y caché, y pasan a la CI existente. El objetivo es resolver por la vía correcta los **6 avisos de biblioteca ausente** que mostró ERC real en W-IND-17. Las otras **3 infracciones eléctricas** (VIN_5V sin conexión, dos entradas de alimentación sin fuente) siguen pendientes, sin PWR_FLAG falso ni supresión de reglas. Una reducción real de avisos solo podrá afirmarse tras nuevo ERC nativo KiCad 9.0.2 en CI.

**Reproducir:** `cd research/2026-10-28-independent-wpt-sensor-v01 && python3 -m unittest -v test_w_ind_20_symbol_library`. El workflow `.github/workflows/w-ind-17-kicad-erc.yml` ejecuta también ERC nativo con informes archivados y **bloqueo expreso ante cualquier infracción**. Esto no es certificación eléctrica.

**Matriz de decisión**

| Opción | Retorno | Riesgo | Decisión |
|---|---|---|---|
| Silenciar avisos / PWR_FLAG inventados | check verde engañoso | Ocultar errores | Rechazado |
| Biblioteca KiCad original + tabla local + tests | Reproducibilidad y avisos solucionables | Mantener coherencia del caché | Implementado |
| Completar fuente 5 V y retorno aislados documentados | Corregir circuito de verdad | Requiere evaluación eléctrica | Siguiente hito |

**Tres problemas separados:** carga dock desconectada y sin litio/BMS; módulo WPT hipotético 5 V/0,4 W medio y 1,5 W pico sin ensayos de bobinas; datos RF ESP-NOW u OpenThread sin integración, requerir ACK de aplicación, CRC, secuencias, timeout, privacidad y recuperación. WISP5 solo microconsumos RFID. Nada de WPT para motores/bombas ni radio para parada crítica. FOD, sobretemperatura, sobrecorriente, corrientes inversas, fallos comunes, offset, EMI y humedad siguen sin verificación física.

**Titularidad y HEAD comprobados el 29/10/2026 contra los pins de 19-alternativas:** mark-belbin/simple-wireless-power GPL-3.0 master `7c7858c0dd7040801b6f191df1396115560218f0` igual pin; wisp/wisp5-hw BSD-2-Clause master `08332bc398aa3350d351ef2aaac163f8007cffda` igual pin; wisp/wisp5 BSD-2-Clause rama **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` frente a pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` **divergencia +68/-11**, sin actualización automática. espressif/esp-now Apache-2.0 master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` igual pin, sin PR abiertas. openthread/openthread BSD-3-Clause main `51aa078ee4fe1ad803bc83ca7b372e7ab62120f3`, +9 desde pin `7009584dadc20cf20c20a6062f357dd572ba6885`, PR #13802/#13804/#13815 recientes. makerspet/oomwoo Apache-2.0 main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`, cambio solo star-history el 29/10; NO tocar #79 ni fuentes ajenas. Autores y licencias conservados: ningún CAD ni código de ellos copiado.

**Coordinación:** leídos en el PC decisión NO_TRASPLANTE 28/10, 19-alternativas, D22, acuerdo W/C, notas de colaboración Codex, LEEME_PRIMERO y WPT_DATOS_V01. Checkout local master con trabajos ajenos sin editar; toda entrega se publica exclusivamente en VALDO PR #9 ámbito W.

**BOM:** 0 unidades físicas nuevas, 0 € gastados. Diotronic auxiliar para pasivos cuando se verifique referencia, MOQ, IVA total y stock Zaragoza; TME, Mouser, DigiKey alternativas no cotizadas para este hito sin nuevos componentes. FOD/thermal/cortes no homologados; no fabricar, imprimir, comprar, conectar ni energizar nada.

**Próximo paso:** circuito KiCad con fuente aislada, pines y retorno reales, FOD y protección térmica/corte independiente, verificar ERC y simulación antes de cualquier ensayo resistivo con autorización.

**Corrección del intento inicial:** el primer ERC del commit 7075ef51 todavía reportó 9 infracciones (6 avisos de biblioteca), porque el contenedor arrancaba desde la raíz del repositorio y no cargaba la tabla local del directorio del esquema. Se corrige el directorio de trabajo del contenedor al propio directorio del esquema, manteniendo el reporte de prueba original como evidencia y el bloqueo de errores. Confirmar resultado de esta corrección exclusivamente con ERC real del commit posterior; no atribuir reducción sin medición del verificador.
