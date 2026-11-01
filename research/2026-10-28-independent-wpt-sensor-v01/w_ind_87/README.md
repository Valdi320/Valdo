# W-IND-87 — puerta de cadencia y reserva para microsensor NFC (solo digital)

**01-11-2026; robot aspirador NUEVO, abierto, reparable e imprimible; no Xiaomi OEM.** Esta mejora añade una puerta de decisión sobre *frecuencia de lectura, energía de arranque y capacidad efectiva* al cribado de puntos de ST de W-IND-86; reutiliza su código y los 22 datos del fabricante sin copiarlos. Ningún hardware está elegido, comprado, probado ni autorizado.

## Resultado material reproducible

**Hipótesis, NO mediciones**: microsensor no crítico, base 0,1 mW, evento extra de 1 mJ por lectura+transmisión, arranque 5 mJ, eficiencia de conversión constante 80%, fugas omitidas, condensador de 1200 µF **efectivos** entre 3,3 y 3,0 V, requisito VIN mínimo hipotético 3,0 V salvo donde se indica 3,3 V. Los **puntos** de potencia ST AN4913 Rev.2 p.7 son medidas del autor con su propio lector y antena; no son mínimos garantizados. El evento de 1 mJ NO es un consumo medido de ESP-NOW, OpenThread ni ST25.

| Muestra del autor ST | RX del autor | Neto tras eficiencia y base (hipótesis) | Margen con 1 mJ/1 s | Periodo mínimo matemático | Decisión |
|---|---:|---:|---:|---:|---|
| 0,5 A/m, AM100 | 2,310 mW | 1,748 mW | +0,748 mW | 0,572 s | Condicional SOLO en cálculo |
| 0,5 A/m, AM10 | 0,360 mW | 0,188 mW | **−0,812 mW** | **5,319 s** | **Déficit sostenido** aunque crezca C |
| 0,5 A/m, AM10 cada 10 s | 0,360 mW | 0,188 mW | +0,088 mW | 5,319 s | Condicional SOLO en cálculo |
| 3 A/m, AM10, VIN mínimo 3,3 V | 4,069 mW | 3,1552 mW | +2,1552 mW | 0,317 s | **Rechazar por EH=3,13 V** |

**Hallazgo:** para **una sola** ráfaga extra de 1 mJ, entre 3,3→3,0 V, el mínimo calculado es **1058,2 µF efectivos**; 1200 µF almacenan solo **1,134 mJ** ideales. A 0,5 A/m AM10, recargar ese mJ precisa **≥5,319 s ideales**, y reunir 5 mJ para un supuesto arranque precisaría **≥26,596 s**. No se garantiza que un sistema real pueda almacenar la energía o transmitir: falta caracterizar tensión/corriente variable, regulador, temperatura, ESR/fuga, lector completo y campo con desalineación. **Un gran condensador no soluciona un déficit de potencia media.**

La potencia útil se modela como `eta*P_EH`; el neto de carga = potencia útil menos base y fuga; el evento promedio = `E_mJ/T_s`; almacenamiento ideal `E_mJ=C_efectiva_uF*(V_alta²-V_baja²)/2000`; tiempo de recarga ideal `E_evento_mJ/P_neta_mW` solo si P_neta>0. El modelo valida todos los supuestos numéricos, rechaza NaN/infinitos/campos ST no muestreados y no interpola ni extrapola. **`hardware_release=BLOCKED` siempre**, incluso donde el balance resulta positivo.

## Pruebas, fuente y reproducción

31 pruebas digitales adversariales originales, cálculo determinista y SHA256 de JSON versionado; flujo dedicado en CI publica el JSON como artefacto. Desde la raíz del repositorio:

```sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_87 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_87/w87_nfc_duty_gate.py > /tmp/w87.json
sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_87/expected.sha256
```

**Límites:** ensayos **matemáticos, no físicos**; ni se ha demostrado alimentación continua ni lectura/ACK de aplicación en la misma ventana RF, ni arranque, radio, tiempo de supervisor/corte, condensador real, FOD, humedad, metal pequeño, offsets XYZ/angulares, EMI o envejecimiento. El hash verifica solamente repetibilidad del modelo. Para el ensayo futuro: caracterizar curva de V/I del par lector+etiqueta por pose, consumo total del lector, fases reposo/TX/RX/ACK/reintentos, mínimo transitorio, FOD/temperatura/corte autónomo, coste puesto en Zaragoza. Solo banco independiente aislado y con autorización de seguridad; **sin baterías, BMS ni estación conectados**.

## Tres sistemas independientes

- **Dock/carga**: WPT con protecciones, FOD, temperatura, humedad y corte autónomo, evaluación propia de BMS/litio posterior. No extrapolar mW a motores/bombas.
- **Alimentación de módulos**: ST25DV04KC NFC harvesting exclusivamente candidato de microsensor **intermitente no crítico**. Cable desmontable, económico y sustituible es la referencia; no eliminarlo solo por cálculos.
- **Datos**: ESP-NOW (Apache-2.0) y OpenThread (BSD-3-Clause) son alternativas RF, NO fuentes eléctricas. Elegir una tras medición de energía, ACK **de aplicación**, CRC, secuencias/epoch, timeout, recuperación, autenticación y privacidad; no usar radio para parada crítica. El inventario ISO15693 con EH activo no garantiza entrega fiable de datos. WISP5 BSD-2-Clause solo para microsensores de muy baja energía.

**Datos del autor:** [ST AN4913 Rev.2 tablas 4 y 5 p.7](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7); [ST25DV04KC](https://www.st.com/resource/en/datasheet/st25dv04kc.pdf). Autorías, licencias, SHAs upstream, comparación y BOM con Diotronic: [BOM_DECISION.md](BOM_DECISION.md). Todo el código W87 es original. Sin cambios en OOMWOO, PR #79, checkout compartido, archivos de C, autores externos ni Xiaomi.
