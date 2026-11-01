# W-IND-92 — Reconciliación de energía con un condensador de reserva (01/11/2026)

**Ámbito W: robot aspirador NUEVO, abierto, local, reparable e imprimible; ninguna pieza/firmware/batería/estación OEM Xiaomi.** Solo modelo digital original en Python estándar. No hay ensayos ni compra física. La PR propia #9 sigue en borrador. No se toca OOMWOO ni #79.

## Mejora material

W84 mide energías integradas TX/RX, pero un ciclo breve con una reserva capacitiva puede mostrar energía de carga superior a la energía de entrada al transmisor, o lo contrario al cargar la reserva. La advertencia anterior de W84 sobre energía almacenada se convierte aquí en un **libro de energía con intervalos**: evita clasificar automáticamente una aparente eficiencia >100 % como transferencia imposible o, en el extremo opuesto, aceptar un resultado ignorando la carga del buffer.

Modelo ideal SOLO cuando el condensador caracterizado está **en el MISMO raíl del consumo RX medido**, los canales comparten ventana temporal y no existen otras fuentes/almacenamientos sin contabilizar:

    E_fuente_raíl = E_carga + ΔE_C
    ΔE_C = 0.5 × C_efectiva × (V_fin² − V_inicio²)

Se propagan tolerancias declaradas de capacitancia, dos tensiones y ambas energías mediante extremos de intervalos, sin convertirlas en desviaciones estadísticas. El cociente (E_carga+ΔE_C)/E_TX es exclusivamente un **cociente energético condicional entre el raíl y la entrada TX**, NO eficiencia de las bobinas, reguladores o del dispositivo ST. La fórmula de condensador ideal está documentada por [Gamry](https://www.gamry.com/application-notes/battery-research/testing-electrochemical-capacitors-cyclic-voltammetry-leakage-current/); capacidad real, ESR y fugas tienen que caracterizarse.

### Evidencia de cálculo: datos INVENTADOS, nunca medidos

| Concepto | Valor simulado |
|---|---:|
| Entrada al transmisor TX en la ventana | 100 ± 2 µJ |
| Energía consumida por carga RX | 120 ± 2 µJ |
| Cociente ingenuo E_carga/E_TX | 120 % |
| Reserva | C = 1000 µF ±5 %, V_inicial = 3,200 V, V_final = 3,190 V, ±1 mV cada lectura |
| Variación energética estimada del condensador | −40,257 a −24,282 µJ |
| Energía condicional que habría tenido que llegar al raíl | 77,743 a 97,718 µJ |
| Cociente corregido, bajo supuestos ideales | **76,219–99,712 %**, no eficiencia RF validada |

La carga pudo consumir parte de una reserva previamente almacenada: esto *explica matemáticamente* el 120 % aparente. Otros casos ensayados: condensador que se carga, ventana sin TX (no hay prueba de WPT), almacenamiento ausente, instrumento con error excesivo, energía inconsistente y estados ambiguos. Se obliga a reportar incertidumbre.

**Importante:** la salida principal es consistencia con el modelo; no verifica que haya una única fuente, ni que ST25DV64KC alimente el sensor. W91 demuestra por el esquema ST que una NUCLEO USB puede contaminar la demostración. Por tanto el campo hardware_release es siempre BLOCKED, aunque el manifiesto se etiquete bench_measured: los metadatos y SHA256 no autentican por sí mismos una medición, ni este programa comprueba aislamiento eléctrico.

## Reproducción

    python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_92 -p 'test_*.py' -v
    python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_92/w92_storage_ledger.py > /tmp/w92.json
    sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_92/expected.sha256

25 pruebas unitarias digitales nuevas, incluida inyección adversarial y determinismo. Los datos demo y las tolerancias son hipótesis. La CI W88-92 ejecuta 74 regresiones W88–91 y estas 25 pruebas, compara el SHA256 y publica JSON.

Para análisis posterior de una ventana REAL de W84, primero revisar su CSV, hashes, instrumentación y avisos; introducir sus energías TX/RX y errores calibrados junto con lecturas de condensador simultáneas usando la opción --case de W92. **El programa NO importa ni transforma automáticamente W84 en un certificado**, y ningún dato etiquetado bench_measured se acepta sin revisión independiente de montaje, instrumentación y procedencia.

## Criterio que desbloquearía el siguiente estudio, NO la integración

Medir con fuente aislada en banco expresamente autorizado y carga artificial, sin batería/BMS ni estación real: entrada completa de lector, potencia en V_EH y raíl del sensor, reserva en ambos extremos de una ventana completa, tiempos de radio ACK/reintentos, arranque en frío, pérdidas, offset y ruido. Descartar USB/3V3 e I2C/GPO como fuentes auxiliares (W91) y registrar ESR, fugas, temperatura y transitorios entre muestras. Exigir FOD, humedad, EMI y corte eléctrico independiente normalmente OFF antes de cualquier energización. Sin autorización, NO realizar pruebas.

La carga desde el dock requiere calificación de potencia y seguridad separada; la potencia distribuida a módulos puede optar por cable desmontable de bajo coste; ESP-NOW/OpenThread son DATOS exclusivamente con ACK de aplicación, CRC, secuencia, timeout, cifrado y recuperación. WISP solo referencia de microsensores; motores/bombas no se proponen con WPT. Ninguna orden/parada crítica dependerá de radio.

Fuentes, estados HEAD/licencias/owners, matriz y BOM Diotronic: [BOM_DECISION.md](BOM_DECISION.md). Todo código W92 es original; no se copió código/CAD externo.
