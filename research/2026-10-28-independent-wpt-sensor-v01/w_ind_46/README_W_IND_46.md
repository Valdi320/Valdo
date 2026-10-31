# W-IND-46 — Sustituir el HEALTH de 5 V con P-MOS por diagnóstico local OUTB/3,3 V

30 octubre 2026. **Propuesta original, digital y NO APTA para hardware, carga ni seguridad.** Robot aspirador NUEVO abierto, reparable e imprimible; se respeta la cancelación definitiva del trasplante Xiaomi X20 Pro. Sector W exclusivo, sin cambios OOMWOO/PR #79, CAD C, clones de autores ni trabajo Codex. No se realizó ningún ensayo físico.

## Mejora real y de alto retorno

W44 proponía generar HEALTH positivo a **5 V** con TPS3700 (OUTB abierto), P-MOS BSS84, resistencia de puerta 22 kΩ y pulldown de 47 kΩ. W45 propuso cambiar a 4,7 kΩ tras un estrés de fuga hipotético, no caracterizado a 5 V. Como el receptor/GPIO todavía NO está seleccionado y podría aceptar solo 3,3 V, **mantener una línea lógica de 5 V requiere justificar compatibilidad o adaptación**. Suponer que un GPIO tolera 5 V sería peligroso.

**Alternativa W46:** salida de diagnóstico **local al receptor** HEALTH_N conectada directamente a OUTB del TI TPS3700, con una sola resistencia R5=10 kΩ a los **3,3 V locales**, nunca a los 5 V del supervisor. Se eliminan BSS84, 22 kΩ de puerta y 47 kΩ/4,7 kΩ de pulldown, sustituidos por R5; de 10 a **8 componentes conceptuales** y de 6 a **5 redes**, comparado con W44. Esta simplificación es comprobable por contrato de pines en código, **NO por ERC** (aún no existe esquema KiCad W46). No se ha demostrado reducción física de costes, temperatura o averías.

Con salida y alimentación válidas, OUTB hunde LOW cuando INB− supera umbral; HEALTH_N sería LOW favorable, HIGH anómalo. Un hilo HEALTH_N abierto tendería a HIGH solo mientras el pullup local esté alimentado. El modelo calcula para 3,3 V y 10 kΩ **0,330 mA y 1,089 mW ideales** al hundir LOW; con tolerancia 1 % supuesta 1,100 mW, no una medida de dispositivo. Frente a 5 V y el candidato W45 de 4,7 kΩ (5,373 mW teóricos) esto sugiere menores pérdidas en ese resistor, no una mejora comprobada del módulo.

## Contrato de conexión W46 (propuesta, no PCB ni cableado)

Componentes: J1 declaración de 5 V supervisor; J2 declaración de 3,3 V local; J3 salida HEALTH_N local; U1 TPS3700DDCR; R1 63,4 kΩ y R2 10 kΩ del divisor condicionado de W43; R5 10 kΩ de pullup a J2-3V3; C1 100 nF. Las cinco redes son: 5V_SUPERVISOR_ONLY, GND_LOCAL, 3V3_LOCAL, INB_MONITOR y HEALTH_N_LOCAL_DIAGNOSTIC. Pines U1: 1 OUTA NC, 2 GND, 3 INA+ NC, 4 INB−, 5 VDD, 6 OUTB. J3 es una unión **en la misma placa local**, NO un cable a través del acoplamiento inductivo. Fuente primaria: https://www.ti.com/product/TPS3700 (salidas open drain; VDD mínimo 1,8 V en condiciones especificadas).

Código original reproducible: W46/w46_diagnostic_model.py verifica 8 componentes, 5 redes, 20 pines sin duplicados (incluidos 2 NC), calcula 8 estados lógicos hipotéticos, y 16 pruebas focales que deben superar la CI. Ejecución: desde la carpeta w_ind_46, lanzar 'python3 -m unittest -v test_w46' y 'python3 w46_diagnostic_model.py --out W46_SYNTHETIC.json'. Todo resultado expone hardware_approved=false y native_kicad_erc=false. Workflow propio genera artefacto W46-SYNTHETIC-LOCAL-OD-NOT-HARDWARE.

## Fallos que NO resuelve

- Pérdida de 3,3 V receptor: desaparece el pullup y no existe HIGH garantizado; no confundir indicación con **desconexión física**. Supervisión UVLO, cortes autónomos normalmente OFF, comparador independente, W37 rearme local y FOD/térmica siguen pendientes.
- TPS3700 bajo rango de VDD/POR o OUTB pegada a LOW: la señal podría quedar indeterminada o falsamente saludable. El corto HEALTH_N a masa tiene el mismo riesgo; un corto a alto no genera salud, pero sigue siendo fallo eléctrico. No se validó backfeed, rampas, retardos, VIH/VIL, VOL, fugas, EMI ni encapsulado.
- No existe GPIO receptor elegido ni pruebas de resistencia/temperatura. No conectar HEALTH_N a EN, batería, motor, estación, cargador ni a un enlace RF. Este diagnóstico tampoco *es* una comunicación inalámbrica: no atraviesa el espacio.

Separación sistémica: **dock** de carga de litio/BMS completamente diferido; **WPT distribuido** solo candidato hipotético sensor de 5 V, 0,4 W medio/1,5 W pico, sin par bobinas ni eficiencia/offset/metal/temperatura/EMI/humedad medidos; **datos** ESP-NOW (Apache-2.0) frente a OpenThread (BSD-3), ambos requieren ACK de aplicación, CRC, secuencia y sesión, timeout, cifrado/autenticación de transporte, privacidad, reenganche y alimentación propia, nunca paro crítico por radio. WISP5 exclusivamente sensores RFID de energía ínfima. No introducir WPT en motores ni bombas sin medida. Alternativa arnés retenido aún vigente y puede ser más barata, mantener comparativa.

## Matriz, BOM, fuentes, autorías y revisión upstream

MATRIZ_W_IND_46.csv y BOM_W_IND_46.csv separan selección provisional, precio web y disponibilidad real. Diotronic Zaragoza es **solo auxiliar** y no tiene stock, SKU, IVA final ni MOQ confirmados. Panasonic ERJ6ENF1002V 10k 0805 1% 125mW es mero candidato: Farnell España muestra 0,036 EUR sin IVA por unidad en cantidad 10, equivalencia aritmética 0,04356 EUR con 21% IVA por unidad, **sin transporte**, precios vigentes por verificar antes de comprar (https://es.farnell.com/panasonic/erj6enf1002v/res-10k-1-0-125w-0805-pel-c-gruesa/dp/2303654). Componentes críticos con trazabilidad TI/onsemi y distribuidores especializados.

Se leyeron maestros 00, 19, D22, coordinación C/W, contrato y LEEME_PRIMERO de VALDO_OOMWOO; la única automatización W activa es la de este ámbito. Autores y SHAs comprobados frente al documento maestro 19, sin copiar ninguna fuente externa:
- mark-belbin/simple-wireless-power GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0 = pin, PR #1 antigua fusionada.
- wisp/wisp5-hw BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda = pin, PR #1 antigua.
- wisp/wisp5 BSD-2-Clause, **640kHz** HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2, diverge **+68/-11** del pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; PR #40 abierta.
- espressif/esp-now Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin; PR #153/#151 cerradas sin fusionar.
- openthread/openthread BSD-3-Clause, main e577777c308f6c87e5da3056239231a8fc147cb2 **+14/-0** vs pin 7009584dadc20cf20c20a6062f357dd572ba6885; PR #13822/#13819 abiertas 30/10.
- OOMWOO makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, PR #79 cleaning-jobs abierta ajena. No modificaciones upstream, originales ni trabajo C/Codex.

**Próxima comprobación de alto valor:** definir el receptor real, VIH/VIL y comportamiento con dominios parcialmente sin alimentación; **luego** representar W46 en KiCad si la interfaz es viable. Seguir a protecciones independientes FOD, térmica y paro sin radio, banco aislado solo después de autorización; sin batería/BMS/dock.
