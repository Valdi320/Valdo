# W-IND-56 — Cribado AB–BA–BA–AB: detectar un transitorio oculto con dos medidores

**30 octubre 2026. Robot aspirador NUEVO independiente. Experimento DIGITAL original de VALDO, únicamente ámbito W; prohibido energizar, comprar, modificar Xiaomi/OOMWOO, BMS o dock.**

## Defecto real y mejora

W-IND-55 usaba AB–BA–AB; sus extremos de orientación AB no ven un transitorio exclusivo de la lectura central BA. W-IND-56 añade la segunda lectura BA antes de recuperar AB: **AB0, BA1, BA2, AB3**, todavía solo **dos intercambios** de posición. Una perturbación aislada de BA1 o BA2 produce una inconsistencia matemáticamente detectable, bajo las hipótesis detalladas. Los dos INA219 son instrumentos REUTILIZABLES del banco, no dos sensores extra del robot.

Con ganancias multiplicativas fijas gA y gB, ratios R0=(gB/gA)*eta0, R1=(gA/gB)*eta1, R2=(gA/gB)*eta2, R3=(gB/gA)*eta3. La eficiencia media geométrica estimada es (R0 R1 R2 R3)^(1/4). Si la eficiencia real tiene una deriva LOG-LINEAL y los centros de cada pasada están equiespaciados, rho=(R2/R1)^3/(R3/R0) debe valer 1. El programa calcula un INTERVALO conservador de rho a partir de errores absolutos supuestos; también evalúa deriva entre extremos AB. No confundir esta inferencia condicional con medición física, calibración, FOD, EMI ni seguridad.

### Umbrales del cribado (HIPÓTESIS, no límites certificados)

- Residuos centrales máximos incluyendo incertidumbre: 3 %; deriva AB entre extremos: 2 %.
- Asimetría temporal de intervalos centrales: 5 %; temperatura 1 °C, distancia entre bobinas 0,1 mm, offset 0,1 mm, carga resistiva 0,5 %.
- Exige orden exacto AB-BA-BA-AB, dos instrumentos A/B, IDs y trazas distintos, fixture compartido, intervalos temporales sin solape, potencias físicamente coherentes y flags de metrología booleanos.
- BENCH_MEASURED con flags autodeclarados podría ser candidato **solo a revisión metrológica externa**: jamás aprobación eléctrica. El origen se recibe como dato, no se autentica.
- Ceguera residual: transitorio idéntico en BA1+BA2; cambios de ganancia/offset, deriva no log-lineal o correlacionada, desalineación no observada, error de reloj común, datos inventados. No reemplaza referencia trazable.

### Evidencia reproducible — SIN HARDWARE

Ejemplo sintético: Pin real supuesto 1000 mW, Pout supuesto 800 mW, ganancias ficticias A=1,1 y B=0,9. Ratios aparentes AB=65,4545 % y BA=97,7778 %. ABBA devuelve **80,0000 %** y rho=1. Con incertidumbre **ficticia ±0,1 mW por canal/pasada**, intervalo condicionado **79,98182–80,01818 %**; residual peor caso **0,18097 %**. Ninguno de esos números es rendimiento observado del sistema. Una alteración BA1 de Pout 880 a 770 mW activa bloqueo aunque AB0 y AB3 permanezcan idénticos; W55 no podía detectarla con sus extremos. 21 tests con inyecciones adversarias.

```sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_56 -p test_w56.py -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_56/w56_abba_gate.py --demo --out W56_SYNTHETIC_NOT_HARDWARE.json
```

No hay adquisición I²C, fuente conectada, patrón físico, temperatura, offsets o EMI medidos; **ningún circuito autorizado para energizar**. ERC histórico W-IND-18 sigue bloqueante. Una eventual repetición física exigiría fuente aislada, apagada antes de mover los medidores y autorización de seguridad previa; no se ordena hacerla.

## Separación arquitectónica obligatoria

| Problema | Estado W56 y decisión provisional | Puertas de seguridad |
|---|---|---|
| Potencia para sensor 5 V, media ficticia 80 mA, pico ficticio 300 mA | Cable corto reemplazable por defecto. WPT simple: solo hipótesis de banco; WPT regulada no seleccionada | Eficiencia real, carga/desalineación, metal FOD, humedad, temperaturas, EMI, fallo/corte local autónomo normalmente OFF y coste puesto en Zaragoza |
| Dock inductivo y carga | Investigación separada y pospuesta. Batería/BMS/dock DESCONECTADOS | Control independiente, química/cargador certificados, FOD, corte térmico, seguridad de litio; no trasladar hipótesis 0,4 W a potencias altas |
| Comunicación | ESP-NOW candidato inicial, OpenThread/802.15.4 alternativa; WISP solo microsensores RFID | ACK de aplicación, CRC, contador/epoch, timeout, identidad, privacidad, reingreso y cifrado; RF nunca sustituye parada crítica |
| Motores y bombas | NO WPT por defecto | Potencia continua/picos, pérdidas y térmica sin demostrar |

## Investigación de autores, licencias y revisiones

Releídas la decisión del 28/10, alternativas, D22 y contrato C/W locales, VALDO_OOMWOO/LEEME_PRIMERO y WPT_DATOS_V01. Contraste fresco de commits HEAD y últimas PR del autor, a 30/10/2026, frente a PIN del documento 19:

| Proyecto externo | Licencia; rama; PIN → HEAD contrastado | PR/changelog del creador y conclusión |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) | GPL-3.0; master; 7c7858c0 → 7c7858c0 | [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1) fusionada en 2021; prototipo del autor NO es circuito WPT seguro para VALDO |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) | BSD-2-Clause; master; 08332bc3 → 08332bc3 | [PR #1](https://github.com/wisp/wisp5-hw/pull/1) 2015; RFID requiere lector, no potencia continua a 80 mA |
| [wisp/wisp5](https://github.com/wisp/wisp5) | BSD-2-Clause; **640kHz**, no suponer master; d978a697 → 604eee2d | Comparación GitHub **DIVERGED +68/-11**, no fast-forward; CCS11 2022, [PR #38](https://github.com/wisp/wisp5/pull/38) actualizada 2024; no copiar |
| [espressif/esp-now](https://github.com/espressif/esp-now) | Apache-2.0; master; c3b5f9be → c3b5f9be | [PR #153](https://github.com/espressif/esp-now/pull/153) cerrada sin fusionar en 2026; ACK radio ≠ ACK aplicación |
| [openthread/openthread](https://github.com/openthread/openthread) | BSD-3-Clause; main; 7009584d → e577777c | **+14/-0** commits; cambios CLI/radio/GN; [PR #13819](https://github.com/openthread/openthread/pull/13819) abierta; alternativa, no integración |
| [makerspet/oomwoo](https://github.com/makerspet/oomwoo) | Apache-2.0; main f01a1b29 | Cambios gráficos sin integrar WPT; [PR #79 cleaning-jobs](https://github.com/makerspet/oomwoo/pull/79) no tocar |
| VALDO | Propio ámbito W PR #9 | W55 c7b03af5; checkout local Codex con cambios ajenos: NO editar |

La especificación y algoritmo ABBA son originales; **no se copió código, esquemas ni CAD** de repositorios externos. Los autores mantienen íntegramente autoría y licencias.

## BOM, proveedores y reparabilidad

Consultar BOM_W_IND_56.csv y MATRIZ_W_IND_56.csv. Coste electrónico incremental **0 € por robot**, 0 tercer medidor, **una pasada de tiempo extra en banco**; dos reposicionamientos igual que W55. Los dos INA219 Satkit MCU-219 se anuncian a [3,63 €/ud con IVA](https://satkit.com/sensor-de-corriente-ina219-i2c-mcu-219), 7,26 € la pareja solo catálogo, stock web "limitado", sin stock en tienda Zaragoza ni coste final envío verificados, calibración o patrón excluidos. Diotronic exclusivamente proveedor auxiliar para pasivos, conectores y prototipado; no existe SKU/stock local demostrado, comprobar MOQ, datasheet, IVA y portes antes de comprar. Comparar con TME, Mouser, DigiKey y fabricante en futura compra; FOD/corte/termistor de seguridad requieren trazabilidad.

**Estado:** ensayo digital sintético. FOD, temperatura, EMI, corte independiente, estabilidad de ganancia, I²C y calibración física pendientes. No se declara retorno económico total demostrado ni pieza apta para robot.

**Siguiente paso:** contrato de captura I²C + trazabilidad independiente, o banco físico *solo tras procedimiento y autorización*. Mantener cable reemplazable como patrón de coste.
