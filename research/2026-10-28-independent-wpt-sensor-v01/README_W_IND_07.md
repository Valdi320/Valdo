# W-IND-07 — Doble ventana térmica fail-closed para TX WPT (28/10/2026)

**Ámbito:** robot aspirador NUEVO, independiente de Xiaomi; módulo sensor experimental 0,4 W medios / 1,5 W pico **hipotéticos**. Solo diseño de seguridad de transmisor para banco SELV; sin PCB, componentes energizados, batería, BMS, estación o WPT físico. No se propone alimentación inductiva para motores/bombas.

## Mejora real de ingeniería (solo software)

La detección térmica mediante un único umbral NTC con la resistencia NTC conectada a masa puede pasar por alto una rotura del cable del sensor: el punto medio sube al rail, pareciendo frío. En lugar de permitir transmisión solo cuando `ratio>umbral_inferior`, el contrato W-IND-07 exige **dos umbrales ratiométricos independientes** por canal: `0,27 < V_NTC/VREF < 0,88`. Así, **un NTC abierto (1,0), cortocircuitado (0,0), ausente o inválido inhibe**; no basta con apagar ante sobretemperatura. Dos cadenas de medición y dos cortes normalmente OFF en serie se representan por separado en modelo de fallos; arrancan desarmados, se enclavan al fallo y solo una nueva **acción local de rearmado en flanco** permite pasar al estado hipotético ON. RF, GPIO, ESP-NOW y OpenThread NO participan en parada crítica.

**Advertencia:** es una arquitectura lógica, NO un esquema de conexiones o dispositivo aprobado. FOD metálico REAL, temporización de sensores, aislamiento, tolerancias de comparador, rotura mecánica, alimentación y efecto de sensor pegado quedan por medir. Una pareja de cortes puede no eliminar fallos comunes, y las dos piezas soldadas en ON siguen peligrosas.

## Números reproducibles: suposiciones, no límites certificados

Modelo `R_NTC(T)=R25 exp(B(1/T-1/T25))`, NTC=10 kΩ a 25 °C, B=3950 K, pull-up=10 kΩ, entradas/umbrales idealizados. Barrido de 8 esquinas con R25=9,5/10,5 kΩ, B=3850/4050 K, pull-up=9,9/10,1 kΩ, además de cuatro combinaciones de umbrales `inferior=0,26/0,28`, `superior=0,87/0,89`. **Estos errores hipotéticos no son valores máximos garantizados de una implementación concreta**. El componente comercial Eaton NRNE104F3950B1F muestra R25=10k/B=3950, tolerancias ±1% declaradas; su curva física completa y tiempos de montaje requieren verificación, no se sustituye por fórmula Beta sin validar.

| Temperatura NTC, no bobina | V_NTC/VREF en 8 esquinas sintéticas | Decisión en 32 esquinas de componentes/umbrales |
|---|---|---|
| -20 °C | 0,90328–0,92226 | Todas inhiben (frío extremo en este contrato) |
| -10 °C | 0,83973–0,86594 | Todas permiten *si el resto de entradas ideales son buenas* |
| 25 °C | 0,48469–0,51471 | Todas permiten condicionalmente |
| 45 °C | 0,28594–0,32019 | Todas permiten condicionalmente |
| 50 °C | 0,24747–0,28087 | Decisión mixta: NO se declara umbral garantizado |
| 55 °C | 0,21364–0,24570 | Todas inhiben en el modelo |
| 60 °C | 0,18417–0,21454 | Todas inhiben en el modelo |
| Cable NTC abierto/corto | 1,0 / 0,0 | Siempre inhiben en el modelo |

**No interpretar** «55 °C inhibe» como temperatura máxima real del cobre, plásticos o ferritas: retardos, distancias térmicas, tolerancias reales, referencia de tensión, componentes en fallo y condiciones ambientales NO se han ensayado. El umbral definitivo deberá salir de un presupuesto térmico y ensayo autorizado. Los sensores deben ser reemplazables sin flex móvil. NO diseñar soporte CAD: sector C.

## Matriz de decisiones

| Alternativa | Ventaja | Defecto decisivo | Estado |
|---|---|---|---|
| NTC con un solo comparador `ratio>0,27` | Menos piezas | Rotura de cable entrega `ratio≈1,0`, parece bueno | RECHAZADA como interlock único |
| Doble ventana NTC + dos canales de vigilancia + dos cortes serie | Detecta abierto/corto, puede soportar **un corte soldado** ante alta temperatura si el otro observa el fallo | No detecta **ambos NTC pegados a lectura normal**, dos cortes soldados, fallos comunes de rail/referencia ni FOD sin detector real | **Seleccionada SOLO para modelado/banco independiente**, no hardware aprobado |
| TX Qi integrado con FOD declarado | Firmware y electrónica preexistentes | FOD de un TX comercial no prueba corte externo independiente, offset ni seguridad en nuestro montaje | Candidato futuro tras revisión de datasheet/placa |
| Cables y conectores robustos desmontables | Barato, sin pérdidas WPT | Contactos de servicio | Fallback preferente cuando WPT no compense |

**Exclusiones:** bq500212A de TI figura como «Not recommended for new designs» pese a ofrecer FOD/entrada T_SENSE; no elegirlo para nueva placa. STWBC86JR de ST figura activo y hasta 5 W, pero necesitaría firmware, caracterización, FOD y supervisión de corte ajena al chip; no hay BOM aprobada ni compra. TPS259630 del W-IND-06 está en la **salida RX DC**, no resuelve vigilancia/corte del TX.

## Contrato para futuro KiCad (NO un circuito de montaje)

**Dominio A:** NTC-A a masa + pullup-A a referencia-A + ventana A (comparador bajo y alto) + latch de fallo A + interruptor serie TX-A que vuelve a **abierto** al perder alimentación del driver. **Dominio B** repetido independientemente: NTC-B, referencia-B, ventana B, latch B y interruptor serie TX-B. Ambos canales deben detectar térmica y cualquier FOD grave; detector FOD real **no seleccionado** y por defecto su entrada `None` impide activar ambos. También pasan por entradas físicas de protección de sobrecorriente, humedad/offset, supervisor local y fuente. Un reset físico momentáneo solo libera el enclavamiento con todas las condiciones correctas. Ningún telegrama remoto puede liberar fallos.

No se asume que dos comparadores compartiendo rail y referencia sean independientes ante fallo común: antes de KiCad se necesitarán análisis de modos comunes, diseños separados de alimentación y POR, salidas inactivas ante falta de tensión, polaridad y pull-down confirmados por hoja de datos, curvas NTC, corriente disponible, capacidad de corte DC, disipación, tiempos máximos y fuga de transistores. Las salidas lógica ideal de Python no gobiernan energía real. `TPS3430` y `TLV3211` son referencias de fabricante de watchdog/comparador, NO piezas elegidas ni circuitos de seguridad resueltos.

## Fallos inyectados y límites encontrados

- **PASS lógico:** NTC abierto/corto/ausente, FOD desconocido, fuente ausente, agua/offset/corriente/WD en fallo, alta temperatura percibida por cualquiera de dos canales, un solo corte atascado cerrado durante alta temperatura; fallo enclavado y rearme de flanco local.
- **FAIL conocido y documentado:** dos contactos soldados, o **dos NTC pegados simultáneamente a una tensión aparentemente normal** frente a calor real; sin detección FOD real, la seguridad física es NO demostrada. Además, un solo interruptor soldado y un fallo aislado del único sensor que gobierna el otro pueden quedar fuera del modelo.
- **Escala:** 43 pruebas unitarias deterministas NUEVAS, 8 esquinas de componentes × 4 de comparadores por punto de temperatura. Cero pruebas físicas, cero medida de temperatura/FOD, no extrapolar fiabilidad en años. La etiqueta `installation_approved` del simulador es siempre `False`.

## BOM del estudio y abastecimiento Diotronic

Ver `BOM_W_IND_07.csv`: cantidades reales para arquitectura propuesta (2 NTC, al menos 4 funciones comparadoras, 2 latches/2 cuts, supervisión FOD aparte), NO una compra autorizada. Eaton NRNE104F3950B1F €0,242 con IVA por unidad, listado DigiKey España el 28/10/2026, sin envío ni disponibilidad local confirmada. Diotronic vendería componentes pasivos a particulares según su página oficial, pero **no se ha comprobado** allí una referencia 10k B3950 idéntica, sus existencias, pedido mínimo ni el precio final de la BOM. Comparar Diotronic/TME/Mouser/DigiKey con especificaciones exactas antes de adquisición. No comprar nada.

## Reproducción / evidencia

```
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m py_compile tx_thermal_window.py test_tx_thermal_window.py
python3 -m unittest -v test_tx_thermal_window
python3 tx_thermal_window.py
```

Comprobados **43/43 PASS** en un sandbox Python local antes de enviar el commit. El CI en GitHub deberá repetirlos junto a los 147 anteriores, sin hardware. Código nuevo original, sin derivar ni copiar GPL de Mark Belbin, BSD WISP/OpenThread ni Apache-2.0 Espressif.

### Estado de fuentes externas verificado 28/10/2026 (separado de nuestra autoría)
- Mark Belbin `simple-wireless-power` GPL-3.0, `master` HEAD `7c7858c0dd7040801b6f191df1396115560218f0`: igual al pin; sin PR ni release abierto relevante.
- WISP5 hardware BSD-2, `master` HEAD `08332bc398aa3350d351ef2aaac163f8007cffda`: igual al pin; sin PR.
- WISP5 firmware BSD-2, **`640kHz`** HEAD `604eee2dffaeba3a270de61cf3dae887a33309c2`: diverge del pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` **68 delante/11 detrás**; PR #40 abierta, sin rebase rápido.
- Espressif `esp-now` Apache-2.0, `master` HEAD `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5`: igual al pin; release v1.0 2022.
- OpenThread BSD-3, `main` HEAD `3d645eb9106cb1d5c2ff11891e84dc14e52e293a`: 5 commits por delante del pin, ninguno detrás; release v2026.10.0 01/10/2026, PRs #13805/#13804/#13802/#13801/#13800 abiertas, no afectan a este monitor analógico.
- OOMWOO oficial `makerspet/oomwoo` HEAD `1c2bd43abcf74288afcf2d8b64514cc325f9b905`; firmware HEAD `575c49abcdc115233f4f3ee8fa512d2939ac3bc5`; PR upstream #79 en cleaning-jobs ajena. VALDO PR propia #9 es el único destino. Adaptación local referenciada por `VALDO_OOMWOO/LEEME_PRIMERO.md` y `adaptacion/contratos/WPT_DATOS_V01.md`; snapshots OOMWOO no tocados, rama master de VALDO local sucia por terceros, sin intervención.

### Referencias de proveedor/fabricante (observaciones, no ensayos)
- NTC Eaton 10 kΩ B3950: https://www.digikey.es/es/products/detail/eaton-electronics-division/NRNE104F3950B1F/16909098
- Comparador TI TLV3211 POR, uso no cualificado: https://www.ti.com/product/TLV3211
- Watchdog TI TPS3430 con posibilidad de deshabilitar, comprobar configuración: https://www.ti.com/product/TPS3430
- TI bq500212A no recomendado para nuevos diseños: https://www.ti.com/product/BQ500212A
- ST STWBC86JR producto activo: https://www.st.com/en/power-management/stwbc86jr.html
- Tienda auxiliar Diotronic: https://diotronic.com/

**Próximo bloqueo:** diseñar y validar en circuito eléctrico independiente de baja tensión los comparadores/driver/cortes normalmente OFF, y detector FOD TX con criterio falsos negativos/metal en ausencia de RX y coste total. Sin FOD, corte físico, termometría/EMI, no hay permiso de banco energizado ni carga de batería.
