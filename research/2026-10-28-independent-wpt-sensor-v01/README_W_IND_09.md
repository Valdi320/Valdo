# W-IND-09 — Criba de interruptores por variante, NO circuito aprobado (28/10/2026)

**Alcance:** robot aspirador NUEVO abierto, reparable e imprimible; piloto RX de sensor independiente **5 V, 0,4 W media/1,5 W pico hipotéticos**, límite nominal de 0,4 A. Cero trasplante Xiaomi; batería/BMS/estación/motores desconectados. Especificación W, sin tocar C, OOMWOO #79 ni autores externos.

## Hallazgo crítico de ficha original TI

[Tabla 5 del datasheet SLVSFJ2B](https://www.ti.com/document-viewer/TPS22950/datasheet/GUID-99272A5F-1586-473D-90BB-1F1AF0AA3545) distingue referencias que **NO** comparten seguridad:

| Variante | ILIM ajustable (típico) | Sobrecarga | Bloqueo inverso | Decisión para 5 V/0,4 A |
|---|---|---|---|---|
| **TPS22950** | **0,05–3,5 A** | reintento automático, SIN enclavamiento | Sí, condicionado | candidato RX **parcial**, enclavamiento externo obligatorio |
| **TPS22950L** | **0,5–3,5 A** | enclavamiento | **NO** | RECHAZADO para 0,4 A + RCB |
| **TPS22950C** | **0,5–3,5 A** | reintento | Sí, condicionado | RECHAZADO para 0,4 A |
| **TPS22918** anterior | sin ILIM | sin latch de sobrecarga | no declarado | solo interruptor; no sustituto de eFuse |

El [datasheet del TPS22950](https://www.ti.com/document-viewer/TPS22950/datasheet/GUID-EF07D84A-1858-4088-8805-B473C225581A) indica umbral inverso **~0,9 A típico** al estar habilitado y un tiempo antes de desconectar; con ON=0 bloquea corriente inversa. El [TPS22950 auto-retry](https://www.ti.com/document-viewer/TPS22950/datasheet/GUID-00D38A6A-7FB4-46B0-8B86-15E27417E6E2) puede reintentar y ciclar térmicamente; el [TPS22950L](https://www.ti.com/document-viewer/TPS22950/datasheet/GUID-74F39065-36D0-49BC-92D0-6FB7DA84BFA3) no aporta RCB. **Nunca inferir características del apellido de familia.** Tolerancias peores y transitorios sin cualificar.

## Evidencia y decisión

Código original `tx_variant_screen.py` con **21 pruebas deterministas** `test_tx_variant_screen.py` (Python 3.10+, sin dependencias externas). Reproducir en esta carpeta:

```bash
python3 -m py_compile tx_variant_screen.py test_tx_variant_screen.py
python3 -m unittest -v test_tx_variant_screen
python3 tx_variant_screen.py
```

**Resultado local: 21/21 PASS.** Todas las variantes generan bloqueo de selección; ninguna produce aprobación física. No hay un controlador de dos cortes, FOD, térmica, EMI, offset, fuente/POR, reverse-current medido ni seguridad certificada. TPS22950 QOD típicamente 150 Ω: si un pasante se quedara **hipotéticamente** corto y QOD condujera en OFF a 5 V, I=5/150≈**33,3 mA**, P=25/150≈**166,7 mW**. **Esto es una hipótesis de fallo de topología**, no una avería observada ni energía medida. RON típico 34 mΩ (5 V) a 0,4 A da I²R≈**5,44 mW** por IC, no pérdidas totales. No comparar con límites térmicos sin más datos.

**Coste:** referencia exacta **TPS22950CDDCR** en [Mouser España](https://www.mouser.es/es/c/semiconductors/power-management-ics/power-switch-ics-power-distribution/?m=Texas+Instruments&series=TPS22950) anuncia 0,748 €/unidad; suponiendo precio antes de IVA 21%, cálculo 0,90508 € con IVA **sin envío** (fiscalidad de oferta pendiente). El **TPS22950CQDDCRQ1** en [DigiKey España](https://www.digikey.es/en/products/detail/texas-instruments/TPS22950CQDDCRQ1/17394990) anuncia 0,968 € con IVA; es **variante C**, NO sustituto de 0,4 A. **Diotronic:** SKU, stock local, cantidad mínima y precio final NO verificados. Comprar cero. **TPS259630** de W-IND-06 continúa como candidato distinto; no se afirma reemplazo. Ver BOM_W_IND_09.csv.

### Matriz de arquitectura (tres problemas distintos)

- **Dock carga:** no seleccionar con esta tabla de 5,5 V; litio/BMS/no conectar hasta seguridad y autorización.
- **Potencia sensor WPT RX:** estudiar TPS22950 como protección **auxiliar**, no como único corte; medir fuente, salida, transitorios y FOD en banco aislado autorizado.
- **Datos RF:** ESP-NOW u OpenThread con ACK/CRC/epoch, nunca parada crítica; WISP5 solo para microsensores demostrados. No se confunde radio con alimentación.

### Lectura upstream/propiedad del 28/10/2026

GitHub API rama HEAD + comparación con SHAs de `19-alternativas-abiertas-para-robot-independiente.md` y PR/releases: Mark Belbin/simple-wireless-power GPL-3.0 master `7c7858c0dd7040801b6f191df1396115560218f0` igual; WISP/wisp5-hw BSD-2 master `08332bc398aa3350d351ef2aaac163f8007cffda` igual; WISP/wisp5 BSD-2 **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` vs pin d978a697..., **divergió +68/-11**, PR #40 abierta; Espressif/esp-now Apache-2 master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` igual, release v1.0 (2022); OpenThread BSD-3 main `3d645eb9106cb1d5c2ff11891e84dc14e52e293a` **+5/-0**, release v2026.10.0 y PR recientes, sin adaptar código. No se copiaron fuentes externas. OOMWOO oficial `makerspet/oomwoo` main `1c2bd43abcf74288afcf2d8b64514cc325f9b905`; no se toca la PR #79. VALDO PR #9 HEAD previo `f7fa9758b3238e7019fbb4a7196cddb2483c84c2`. Consultados maestros decisión/no OEM, D22, coordinación W/C, `VALDO_OOMWOO/LEEME_PRIMERO.md` y contrato WPT; master local sucio ajeno intacto. Apoyo Codex A01–A05 local ajeno no incorporado.

**Siguiente hito:** esquema real de doble corte normalmente OFF, validación POR/EN, realimentación inversa, QOD y FOD/termometría independientes, con ERC/SPICE y verificaciones de peor caso antes de autorizar siquiera banco resistivo. **Cero hardware, cero baterías, cero compras.**
