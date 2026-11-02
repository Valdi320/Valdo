# W-IND-50 — INA219: evitar eficiencias falsas por lecturas viejas sin añadir hardware
**30/10/2026. Solo ámbito W del robot NUEVO abierto, económico y reparable. Sin Xiaomi OEM, C/Codex, OOMWOO, PR #79, compras, pruebas físicas ni batería.** Código y modelos originales, sin copiar repositorios externos.

## Mejora material
W48 integra las energías TX/RX; W49 muestra que medir tensión y corriente mediante INA219 requiere dos conversiones ADC (8.51 ms por ADC con promedio 16; 17.02 ms por pareja). W50 añade una puerta verificable **previa** al cálculo de eficiencia que decodifica registros brutos (shunt 10 µV/LSB; bus 4 mV/LSB), exige modo *single-shot shunt+bus*, evidencia declarada de **CNVR=0 después de disparar**, CNVR=1 al leer, OVF=0 y lectura de POWER para limpiar CNVR; rechaza tiempos imposibles, muestras viejas, dos relojes distintos, sesiones mezcladas, duplicados, secuencias perdidas, inversión de corriente y aparente eficiencia >100%. El rechazo es atómico, sin consumir los números de secuencia. **No es un controlador I2C físico**: los booleanos de lectura y el clock_id son metadatos que en el futuro deberá demostrar un adaptador real; no se pueden inventar como evidencia.

Se evita añadir monitores costosos a cada sensor. Una única pareja de INA219 candidata de banco podrá reutilizarse si supera la validación metrológica. La corrección de ubicación del shunt TX incorpora la pérdida I²R antes de calcular el rendimiento.

### Ejemplo sintético (NO medida física)
Hipótesis: 5 V, shunt TX/RX 100 mΩ, corriente 80 mA, promedio 16, reloj común supuesto. TX bus 5.000V, caída shunt 8mV, potencia de fuente (5.000+0.008) × 0.08 = **0.40064 W**. RX bus 4.000V, carga 4.000 × 0.08 = **0.32000 W**. Rendimiento aparente = **79.872%** frente a 80% sin corregir el shunt TX, diferencia de 0.128 puntos porcentuales. No calibrado: no inferir incertidumbre ni eficiencia verdadera. Seis fallos inyectados digitalmente son rechazados (CNVR no limpiado, CNVR no listo, OVF, dato caduco, reloj distinto, eficiencia imposible). 42 tests unitarios cubren fallos, decodificación y secuencia.

## Reproducción
```sh
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_50
python3 -m unittest -v test_w50
python3 w50_ina219_freshness.py --demo --out W50_SYNTHETIC_NOT_HARDWARE.json
```
Suite Python local antes de publicar **42/42 PASS**; la CI W50 independiente realiza la misma prueba y archiva JSON etiquetado SYNTHETIC-NOT-HARDWARE. Distinguir la CI específica del **bloqueo histórico ERC W-IND-18**, sin declarar PR completa segura.

## Costes, decisiones y mantenimiento
**Coste adicional por W50 = 0 €** (solo software y validaciones digitales). Referencia W49 sin nueva compra: chips INA219BIDCNR a **2.15380 €/unidad IVA** (pareja de chips desnudos **4.30760 €**, DigiKey España, 30/10/2026), necesitan shunt, PCB, montaje, calibración, portes; pareja de placas INA219 100mΩ Berrybase **7.40 € precio histórico W49**, no se confirma hoy coste puesto en Zaragoza. **Diotronic solo auxiliar**, sin SKU equivalente, existencias físicas, MOQ ni precio entregado verificados; contrastar TME/Mouser/DigiKey antes de elegir. No comprar. Véanse BOM_W_IND_50.csv y MATRIZ_W_IND_50.csv.

Mantener **cable sustituible** como referencia económica y no poner WPT por defecto en cada sensor; permitir un piloto sensor no crítico solo después de comprobar protección autónoma. Tres problemas separados: (1) dock inductivo+cargador/BMS (no aprobado ni conectado), (2) distribución WPT de baja potencia frente a cable, (3) **datos** RF con ESP-NOW candidato y OpenThread alternativa, ACK de aplicación/CRC/secuencia/timeout/privacidad/recuperación, nunca la radio como corte crítico. WISP5 solo microsensores RFID; no WPT automático para bombas/motores.

## Auditoría de autores y SHAs (GitHub 30/10/2026)
Comparación de revisión PIN registrada en el maestro 19 con HEAD de rama y commits/PR de los creadores:
| Repositorio, licencia, rama | PIN 28/10 | HEAD 30/10 | Comparación y novedad |
|---|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 master | 7c7858c0dd70 | 7c7858c0dd70 | idéntico; README de gap; PR #1, no se copió GPL |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause master | 08332bc398aa | 08332bc398aa | idéntico, ajuste de resonancia; PR #1 |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause **640kHz** | d978a6978ad2 | 604eee2dffae | **divergido +68/-11**, CCS11, PR #40, NO fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 master | c3b5f9be245f | c3b5f9be245f | idéntico, compatibilidad IDF v6; PR #153 |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause main | 7009584dadc2 | e577777c308f | **+14/-0**, radio/CLI/CI y PR recientes |

OOMWOO oficial makerspet/oomwoo main f01a1b295f46: cambio solo de gráfico; PR #79 pertenece al módulo cleaning-jobs ajeno. VALDO PR propia #9 HEAD anterior b6a2ecbc3841 (W49). Adaptación VALDO_OOMWOO, worktrees locales C/Codex con cambios ajenos y fuentes upstream **no modificados**. Se revisó que la única automatización activa era este frente W.

## Límites de seguridad y siguiente puerta
W50 **NO** verifica driver I2C, reloj sincronizado, resistencia shunt real, calibración, error de ganancia/offset, potencia no estacionaria ni pérdidas bajo ruido EMI. INA219 no sustituye osciloscopio ni circuitos autónomos. Faltan cutoff normalmente apagado e independiente, FOD metálico, temperatura, humedad, desplazamiento de bobinas, EMI y potencia real; W-IND-18 ERC histórico continúa FAIL. **hardware_approved=false, lithium_dock_approved=false, pruebas físicas=0**; ninguna estación, BMS, batería, motor o bobina energizados. Siguiente hito: interfaz de reloj/DRDY y calibración real del banco de baja tensión, cuando exista autorización de ensayo seguro; primero documentación y protocolo, no compra.

**Fuentes:** [TI INA219 Rev.G](https://www.ti.com/product/INA219), [DigiKey INA219BIDCNR](https://www.digikey.es/es/products/detail/texas-instruments/INA219BIDCNR/2596849), [W49 maestro](https://github.com/Valdi320/Valdo/blob/b6a2ecbc384117f8ad7055f6651927cd274f1295/research/2026-10-28-independent-wpt-sensor-v01/w_ind_49/README_W_IND_49.md), [WPR #9](https://github.com/Valdi320/Valdo/pull/9).
