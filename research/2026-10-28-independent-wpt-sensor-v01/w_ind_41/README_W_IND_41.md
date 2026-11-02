# W-IND-41: supervisión del 3,3 V desde el dominio de 5 V y robustez del divisor

30/10/2026 · VALDO sector W · ROBOT NUEVO · SOFTWARE ANALÍTICO SOLAMENTE · NO ENERGIZAR

## Mejora contrastable

W40 detectó un punto único de fallo: los dos INA301 de W39 comparten tanto el shunt como los 3,3 V. En vez de añadir otro INA al mismo rail, se evalúa TI TPS3700DDCR alimentado desde RX5_SOURCE **antes** de los cortes y supervisando 3,3 V mediante INA+, sin conectar nada físicamente. TI especifica VDD de 1,8 a 18 V, umbral nominal de 400 mV con precisión del 1 % y OUTA drenador abierto que se activa en subtensión; histéresis típica de 5,5 mV (no garantizada). Fuente: https://www.ti.com/product/TPS3700 .

Dos divisores de idéntica proporción nominal no ofrecen la misma resistencia frente a corrientes parásitas. Se comparan 62k/10k y 620k/100k (resistencias 1 %, referencia ±1 %) con una perturbación de entrada FICTICIA de ±1 µA, **NO especificación del TPS3700**. Requisitos de la prueba, también hipotéticos: 3,3 V ±5 % normal; tensión defectuosa ≤2,70 V.

| Opción | disparo nominal | extremos con ±1µA sintético | margen hasta 3,135 V | decisión en el modelo |
| --- | ---: | ---: | ---: | --- |
| 62k + 10k | 2,880 V | 2,741–3,022 V | +0,113 V | PASS |
| 620k + 100k | 2,880 V | 2,189–3,586 V | −0,451 V | FAIL |
| 68k + 10k | 3,120 V | 2,968–3,275 V | −0,140 V | FAIL |

La opción 62k/10k demanda 0,151 mW frente a 0,015 mW del divisor 620k/100k (calculados a 3,3 V). Incremento: 0,136 mW o 0,00327 Wh/día si funcionara 24 h; **no medido**. La histéresis, fuga de entrada real, impedancias, tolerancias de temperatura, EMI y tiempos de los cortes no están incluidos. Por tanto PASS = **solo modelo matemático**, NO circuito validado.

## Contrato eléctrico candidato, aún SIN esquema KiCad

1. TPS3700 VDD desde RX5_SOURCE_PRE_CUT (dominio de 5 V distinto al regulador de 3V3); GND por estudiar, INA+ desde divisor 62k serie / 10k a tierra; salida OUTA drenador abierto, **NO permiso alto por sí misma**.
2. OUTA bajo puede solicitar apertura, pero abierto o bloqueado en alta impedancia todavía permitiría potencia. Antes de usarlo exigir cable de salud, pull-down de EN, pull-up a rail cualificado, antibackfeed, rearme W37 y trazado independiente a los dos TPS259470L. Los casos negativos están codificados. INB-/OUTB fuera de este hito, no conectar sin verificar ficha.
3. La lógica considera idealmente supervisor autónomo de 5 V (rango hipotético 4,5–5,5 V): todavía NO conectado, ni verificada protección ante arranque 5V/3V3 parcial. La alimentación desde otro rail **no acredita por sí sola independencia funcional**.
4. El shunt común continúa siendo un punto débil. No atribuir una reducción física de cutsets a este modelo, ni conectar bobina, estación, litio, BMS, bombas ni motores.

## Evidencia reproducible

Python 3.11, solo biblioteca estándar:
- python3 -m unittest -v test_w41
- python3 w41_independent_pg.py --out W41_EVIDENCE.json

19 pruebas digitales PASS en cálculo local. El JSON diferencia medición, hipótesis y fallo descubierto; sin pruebas de hardware. Dos escenarios negativos siguen **inseguros**: OUTA desconectada o atascada en alta impedancia mientras 3,3 V cae. Se mantiene safe_to_energize=false. El workflow W41 publica evidencia independiente cuando GitHub Actions termine.

## BOM y abastecimiento

Ver BOM_W_IND_41.csv, con Diotronic como auxiliar, NO exclusivo. DigiKey España muestra TPS3700DDCR a 2,21 EUR sin IVA / 2,6741 EUR con IVA por unidad y existencias web en una instantánea de catálogo consultada el 30/10: https://www.digikey.es/es/products/detail/texas-instruments/TPS3700DDCR/3137548 . No significa stock actual ni stock en Zaragoza, portes excluidos. Diotronic anuncia 62k 5 % axial ref 6235025 por 0,02 EUR IVA en su catálogo (https://diotronic.com/964-resistencias-de-carbono-1-4w-5), **NO compatible** con 1 % SMD requerido. TME/Mouser/componentes equivalentes pendientes de confirmar: sin precios inventados. No hay compras ni PCB.

## Fuente/autorías y cambios HEAD (30/10/2026)

Leídos antes de modificar: documentos maestros locales 00_DECISION_20261028_NO_TRASPLANTE_X20.md, 19-alternativas-abiertas-para-robot-independiente.md, D22, acuerdo W/C, VALDO_OOMWOO/LEEME_PRIMERO.md y WPT_DATOS_V01.md. Revisión API GitHub frente a SHAs del maestro 19:

| Propietario/licencia | HEAD de rama | variación / PR |
| --- | --- | --- |
| mark-belbin/simple-wireless-power GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | igual; PR #1 fusionada, no copiar CAD GPL |
| wisp/wisp5-hw BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | igual; PR #1 histórica |
| wisp/wisp5 BSD-2-Clause | 640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2 | diverge 68 ahead / 11 behind del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; PR #40 abierta |
| espressif/esp-now Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | igual; PR #153 cerrada sin merge |
| openthread/openthread BSD-3-Clause | main e577777c308f6c87e5da3056239231a8fc147cb2 | +14 del pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13822 abierta |

OOMWOO makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, sin editar; PR upstream #79 cleaning-jobs fuera del sector W. VALDO PR #9 pertenece al usuario. Local VALDO contiene trabajo ajeno sin integrar y NO se ha editado. Automatizaciones relevantes OOMWOO y mecánicas se encuentran pausadas. No se importaron fuentes externas.

Sistemas separados: dock de carga SIN conectar baterías/BMS; alimentación WPT experimental de un **sensor hipotético** 5 V, 0,4 W medio y 1,5 W pico (sin motor ni bomba); RF ESP-NOW u OpenThread únicamente telemetría con ACK aplicación, CRC, secuencia, timeout, privacidad y recuperación por verificar, sin parada crítica remota. WISP solo microsensores RFID intermitentes.

**Siguiente hito:** en KiCad, desarrollar interlock de corriente/rail con TPS3700, doble corte por defecto OFF y diagnóstico de cable OUTA abierto; validar ERC/netlist y luego transitorios, FOD, temperatura, offset, EMI y en último término ensayo aislado solo con autorización. Hito presente NO autoriza energizar.
