# W-IND-26 — INA301A1 LIMIT: valor calculado y corrección de ficha (29/10/2026)

**Hito original W-only; publicado para auditoría DIGITAL, NO diseño eléctrico fabricable, NO autorización de alimentación.** Robot aspirador NUEVO, independiente del Xiaomi. Se conservan todos los hitos históricos sin tocarlos.

## Cambio material frente a W-IND-25

Una revisión de la ficha TI INA301 SBOS713A Rev. A detectó una atribución incorrecta: W-IND-25 empleaba **35 µV** de offset máximo para INA301**A1**, pero en la tabla TI p. 5 ese máximo corresponde a **A3**; el A1 especifica **±125 µV**. Corregimos este dato en un **modelo nuevo** sin modificar ni borrar el anterior, y sustituimos el umbral hipotético 0,700 V por la ecuación auténtica de LIMIT de TI (p. 16): `V_LIMIT = I_LIMIT × R_LIMIT`, `I_TRIP,nom=V_LIMIT/(G×R_SHUNT)`.

Candidato inspeccionable: Vishay **CRCW06038K66FKEA**, 8,66 kΩ ±1 %, ±100 ppm/°C, 0603, 0,125 W, catálogo técnico y trazabilidad pendientes de compra. TI da `I_LIMIT` 79,2–80,8 µA sobre –40...125 °C (p. 6), nominal 80 µA, ganancia A1 20 V/V y offset A1 ±125 µV (p. 5), offset comparador A1 hasta 3,5 mV (p. 6, **sin cota térmica garantizada por este modelo**). Resultado nominal matemático: 0,6928 V y **346,4 mA** para shunt 0,100 Ω HIPOTÉTICO.

### Envolvente sintética, sin validación física

Se evalúan esquinas de ganancia (±0,1 % más ±10 ppm/°C×100 °C), offset de entrada A1 (±125 µV más ±0,5 µV/°C×100 °C), `R_LIMIT` ±1 % más ±100 ppm/°C×100 °C, `I_LIMIT` 79,2–80,8 µA, un **shunt todavía no seleccionado** (±1 % más ±200 ppm/°C×100 °C, SOLO hipótesis) y 3,5 mV de offset del comparador más **10 mV EXTRA HIPOTÉTICOS** para incertidumbre no caracterizada. No se convierten 10 mV en garantía frente a EMC, transitorios o deriva desconocida.

En esta caja de supuestos, 300 mA máximos normales y 400 mA mínimos de fallo se distinguen estáticamente: margen sin falso disparo **35,91156 mV**, margen de detección **43,73244 mV**. Garantías **SOLO dentro del modelo**: por debajo de **317,398 mA** no dispara y por encima de **377,412 mA** dispara; entre ambos no hay conclusión. No se han modelado rebotes, filtrado, slew, duraciones de corriente ni dependencia térmica efectiva.

Este hito **NO demuestra protección real**. La salida ALERT del INA301 es drenador abierto y puede quedar inoperante cuando su alimentación desaparece; el bloqueo reverso del eFuse tampoco demuestra desconexión autónoma ni continuidad tras fallo. Se requieren corte normalmente OFF, enclavamiento independiente, power-good local, FOD, termometría, medidas térmicas, offset/EMI, RC/tiempo real, ERC/netlist, pruebas ante soldadura de MOSFET y fallo común. Los 1 µs de alerta del fabricante no son tiempo demostrado de corte. Ningún paquete inalámbrico autoriza parada crítica.

## Ensayo repetible, clasificación y resultado

```bash
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_26
python3 -m unittest -v test_limit_resistor_envelope
python3 limit_resistor_envelope.py > result.json
```

Fuente reproducible: `limit_resistor_envelope.py`, `test_limit_resistor_envelope.py`, CI `.github/workflows/w-ind-26-limit.yml`, `BOM_W_IND_26.csv`, `MATRIZ_W_IND_26.csv`. Clasificación: **dato fabricante** (TI corriente LIMIT/gain/offset, Vishay tolerancia/TCR), **hipótesis** (shunt 0,1 Ω + TCR, 300/400mA, 100°C excursion, extra error 10mV), **simulación aritmética propia** (esquinas, márgenes), **medición propia = 0**. Ninguna seguridad física ni certificación ni integración probada.

## Revisiones y autoría (29 octubre 2026)

Antes de crear este hito, revisados: decisión de arquitectura 28/10, alternativas y pins de 28/10, D22, coordinación C/W, LEEME_PRIMERO y WPT_DATOS_V01; no editar proyecto OEM ni C, Codex, clones OOMWOO o PR #79 cleaning-jobs.

| Referencia externa / licencia del autor | Rama HEAD contrastada contra SHA fijado en 19-alternativas | Resultado, sin importar código |
| --- | --- | --- |
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | idéntico; PR #1 TX Board v1.1, referencia no integrada |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | idéntico; PR #1 hardware, NO sensores continuos WPT |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause | default **640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2 | **diverge 68 adelante/11 detrás** de d978a6978ad23ccd6c44dd55430973b04a3d4a9b; no actualizar a ciegas |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | idéntico; PR #153 sobre wakeup; datos solamente |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause | main 51aa078ee4fe1ad803bc83ca7b372e7ab62120f3 | 9 commits por encima de 7009584dadc20cf20c20a6062f357dd572ba6885, radio/CI; datos alternativa |

OOMWOO oficial `makerspet/oomwoo` revisión main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, sin efecto en LIMIT; VALDO propia PR #9 separada de OOMWOO #79. Fuentes de creador consultadas, sin copias de software o CAD externo. La decisión de ESP-NOW frente a OpenThread no afecta `R_LIMIT`.

**Bibliografía primaria:** TI [INA301 SBOS713A](https://www.ti.com/lit/ds/symlink/ina301.pdf) pp. 5, 6, 16; [Vishay CRCW06038K66FKEA características](https://www.digikey.fr/en/products/detail/vishay-dale/CRCW06038K66FKEA/1174775); [DigiKey INA301A1](https://www.digikey.es/es/products/detail/texas-instruments/INA301A1IDGKR/6571979); [Diotronic Zaragoza](https://diotronic.com/) proveedor auxiliar.

## Decisión / siguiente gate

**Conservar 8,66 kΩ solo como candidatura para KiCad**, nunca permiso de energización. Elegir y documentar shunt Kelvin real (TCR, pulsos, potencia, huella, sourcing), validar el error efectivo de comparador sobre temperatura y arrancar normalmente OFF. Después diseñar y verificar físicamente por separado el corte ante pérdida de energía, FOD y temperatura. El dock, baterías, BMS, motores y bombas no se prueban, ni se añaden por defecto WPT. No comprar, imprimir, soldar ni instalar servicios.
