# W-IND-33 — contrato de POR y rearme local, todavía SIN conectar

**29 octubre 2026 · VALDO W propio · robot NUEVO independiente · NO ENERGIZAR.**

## Mejora verificable
El circuito W32 ya dibuja dos TI TPS259470LRPWR con bloqueo inverso, pero sólo tiene entradas externas PERMIT A/B; INA301 es monitor, no una desconexión. Un error sería alimentar directamente los EN desde la salida RESET de un supervisor: al recuperarse VDD se activarían automáticamente después del retardo, sin rearme local. W33 añade **la especificación de pines reales y una simulación reproducible** de dos supervisores **TI TPS3839K50DBZR**, dos biestables **TI SN74LVC1G74DCUR** y un pulsador SOLO LOCAL. CLR_N es activa-baja; Q no puede subir tras una caída de alimentación sin un nuevo flanco local en CLK. Los dos Q se asignan a EN A/B, con pulldowns separados.

Los diodos Schottky candidatos se orientan **ánodo a CLR_N y cátodo a ALERT_N** para que la alarma de drenador abierto del INA301 descargue ambos CLR sin cortocircuitar entre sí las salidas push-pull RESET de los supervisores. Cada RESET_N requiere 10k serie, cada CLR 100k a masa, cada EN 10k a masa, cada CLK 100k a masa. **No hay circuito KiCad W33 integrado ni PCB, transistor, SPICE, prueba física o señal de parada homologados**: `INTERFACE` es un contrato simbólico pendiente de ERC/netlist físico. FOD, temperatura, monitor VS, contacto abierto y fallo común no resueltos.

### Resultados reproducibles
Desde `research/2026-10-28-independent-wpt-sensor-v01/w_ind_33`:

```bash
python3 -m unittest -v test_w33_positive_permit.py
python3 w33_positive_permit.py
```

- **20 pruebas digitales**: pinout TI DCU8 (CLK1/D2/Q_N3/GND4/Q5/CLR6/PRE7/VCC8), supervisor SOT23 (GND1/RESET2/VDD3), polaridad diodos, rearme local, pérdida de tensión, radio ignorada y estados fallidos.
- Enumeración de **64 configuraciones ideales**, de las cuales **9 permiten energización insegura simulada** (incluido biestable soldado a alto + su supervisor fallado). Estas *no* son 9 mediciones reales ni una tasa de fiabilidad. Con una única avería simple del modelo no se infiere certificación.
- **Aritmética nominal**, 5V, 10k serie y 100k caída: CLR alta ideal **4,545V** frente a VIH=3,5V @5V. Corriente de hundimiento INA301 máxima *ideal* 4×5V/10k = **2mA** (dos ramas CLR más pullup W33 y W32) vs ensayo TI @3mA, VOL≤0,3V. Falta acotar Vf/IR de BAT54, fugas, tolerancias, desacoplo y fallos del INA301. NO se califica CLR baja. El TPS3839K50 tiene umbral nominal **4,38V** y reset de **120–350ms** según ficha; estado garantizado sólo para VDD>0,6V. El diseño NO está autorizado para alimentarse.

### Separación y decisión
**Módulos WPT** de bajo consumo: este estudio se centra solo en permisos de un receptor 5V hipotético de 80mA medios, 300mA pico y fallo 400mA. **Dock de carga**, litio y BMS quedan desconectados y fuera; no extrapolar umbrales RX al TX. **ESP-NOW/OpenThread son datos RF, nunca alimentación ni parada/rearme**; conservan ACK aplicación, CRC, secuencia, timeout, privacidad y recuperación local. WISP5 sólo microsensores intermitentes. Mantener la alternativa de cable modular protegido para comparar coste/eficiencia y reparación; ningún motor/bomba se pasa por defecto a WPT.

### Autores, licencias y HEAD verificados el 29/10/2026
Comparación frente a `19-alternativas-abiertas-para-robot-independiente.md`, más PRs de creadores:
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 master **7c7858c0** idéntico al pin; [PR #1](https://github.com/mark-belbin/simple-wireless-power/pull/1).
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2 master **08332bc3** idéntico; [PR #1](https://github.com/wisp/wisp5-hw/pull/1).
- [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2 rama **640kHz 604eee2d**, **divergente +68/−11** vs pin d978a697; [PR #40](https://github.com/wisp/wisp5/pull/40), no fast-forward.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2 master **c3b5f9be** idéntico; [PR #153](https://github.com/espressif/esp-now/pull/153).
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3 main **e577777c**, +14/0 vs pin 7009584d; [PR #13820](https://github.com/openthread/openthread/pull/13820) y cambio BUILD #13812.

OOMWOO main **f01a1b295f46** cambia chart, sin trabajo W nuevo; VALDO rama W anterior **4f7e5945**, C/otras automatizaciones preservadas. Ninguna línea GPL/BSD/Apache copiada. Fuentes de especificación de fabricantes: [TPS3839](https://www.ti.com/lit/ds/symlink/tps3839.pdf), [SN74LVC1G74](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf), [INA301](https://www.ti.com/lit/ds/symlink/ina301.pdf), [TPS25947](https://www.ti.com/product/TPS25947).

**BOM:** véase CSV. Tienda Diotronic Zaragoza es *auxiliar*, sin stock/precio/MOQ exactos confirmados. RS España ofrece el SN74LVC1G74DCUR **solo paquete 25 por 23,10€ con IVA** según ficha consultada, no implica precio para 2; ver https://es.rs-online.com/web/p/circuitos-integrados-de-biestables/2297041 . Precios finales del conjunto, TME/Mouser/DigiKey y todas las piezas críticas pendientes; ninguna compra.

**Siguiente paso:** convertir este contrato en esquema KiCad **integrado en la misma PCB W32**, con ERC/netlist, protecciones de INA301 sin alimentación, FOD y termometría autónoma, sin energizar ni tocar ningún equipo. Un conector ALERT_N abierto sería **inseguro**, por eso no está aprobado como arnés.
