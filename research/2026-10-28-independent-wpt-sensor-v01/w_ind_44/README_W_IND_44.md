# W-IND-44 — KiCad independiente del enlace TPS3700 OUTB → P-MOS → HEALTH (solo diagnóstico)

**30/10/2026, sector propio W; robot aspirador NUEVO, abierto y separado totalmente de Xiaomi.**
Entrega digital original: generador de esquema editable KiCad 9, librería de símbolos con numeración de pines, modelo de integridad de redes, tests adversariales y comprobación ERC/XML nativa automatizada. **NO es un diseño apto para fabricar, energizar o conectar a los dos interruptores de corte.** Cero ensayos físicos, baterías, BMS, motores, dock o radio conectados.

## Mejora material sobre W-IND-43

El modelo W43 solo representaba OUTB y P-MOS idealmente; **no existía un esquema eléctrico KiCad cuyo pinout y redes pudieran examinarse**. W44 implementa un circuito experimental autónomo de **10 componentes / 6 redes nombradas / 25 pines contabilizados (23 conectados + 2 NC)**:

- J1: 5 V **declarados**, no fuente real, compartidos por VDD del TPS3700, la SOURCE del P-MOS y su R3 de pull-up 22 kΩ.
- J2: 3,3 V **declarados** del rail a vigilar; R1=63,4 kΩ/R2=10 kΩ excitan INB− (pin 4).
- U1: TI TPS3700DDCR, encapsulado **DDC-6**. Pines 1 OUTA (NC), 2 GND, 3 INA+ (NC), 4 INB−, 5 VDD, 6 OUTB. OUTB es **open drain**, hunde a LOW al superar el umbral.
- Q1: onsemi BSS84LT1G **candidato provisional** en SOT-23; pin 1 GATE, 2 SOURCE a +5 V, 3 DRAIN a HEALTH. R3 une GATE y SOURCE y evita asumir que OUTB pueda emitir un HIGH; es necesario comprobar la huella, orientación de diodo de cuerpo, RDS(on), VGS y fugas reales.
- J3: HEALTH_DIAGNOSTIC, **NO** conexión de seguridad/EN. R4=47 kΩ a GND reside conceptualmente en el receptor, de forma que un cable HEALTH abierto tiende a LOW en el modelo resistivo. El esquema no define aún un nivel VIH/VIL válido para la lógica receptora.
- C1: desacoplo provisional 100 nF del supervisor. No es análisis de impedancia de PCB, temperatura, EMI ni tiempo de respuesta.

La hoja W44 es **independiente**, no se modifica ningún archivo de W32/W36/W38/W39/W43, clones de autores, OOMWOO, CAD/locks de C o documentación maestra. El generador reutiliza el renderer original de **nuestro** W32 solo EN MEMORIA. Se preservan los derechos y fuentes externas.

### La ganancia y su límite exactos

Ganancia verificable: el contrato textual previo se convierte en conectividad KiCad trazable por número de terminal y un verificador rechaza intercambio SOURCE/DRAIN, desaparición del pulldown o etiquetas incompatibles. Esto evita soldar una supuesta solución cuyo pinout no estuviera auditado y permite revisar su viabilidad **antes** de pasar al circuito de doble corte.

**No hay mejora demostrada de seguridad del robot**: ERC correcto no verifica polaridad real del transistor, umbrales bajo POR, corriente de fuga, backfeeding, retardos, soldaduras o calentamiento. En concreto W43 ya reprodujo autorización potencialmente insegura con TPS3700 por debajo de POR, puerta a GND, HEALTH en cortocircuito a +5 V y alimentación parcial. W44 no oculta ni resuelve esos peligros; antes de unir HEALTH a un eFuse hay que introducir supervisión física de dominio independiente, entradas normalmente apagadas, rearme local W37, alarma autónoma, FOD y térmica.

## Reproducir: pruebas y evidencia

En research/2026-10-28-independent-wpt-sensor-v01/w_ind_44, dentro de la rama propia W:

    python3 generate_w44.py
    python3 generate_w44.py --verify
    python3 -m unittest -v test_w44

El runner GitHub Actions, usando imagen versionada kicad/kicad:9.0.2, ejecuta además:

    kicad-cli sch erc --format json --severity-all --exit-code-violations -o native_out/w44_erc.json W44_TPS3700_OUTB_PMOS_DIAGNOSTIC_NOT_SAFETY.kicad_sch
    kicad-cli sch export netlist --format kicadxml -o native_out/w44_native.xml W44_TPS3700_OUTB_PMOS_DIAGNOSTIC_NOT_SAFETY.kicad_sch
    python3 netlist_gate_w44.py native_out/w44_native.xml --out native_out/w44_gate.json

El verificador compara **conjuntos exactos de redes, terminales, componentes y no-conectados**, sin conceder aprobación analógica. Si falla ERC, generación, componentes o netlist, CI queda roja y bloquea la progresión. El paquete generado incluye esquema, librería, tabla, netlist, ERC JSON, auditoría y referencia a fallos W43 (1.536 combinaciones idealizadas, no medidas físicas independientes).

**Fuentes técnicas primarias:** [TI TPS3700 y función OUTB](https://www.ti.com/product/TPS3700/part-details/TPS3700DDCR), [características/TPS3700](https://www.ti.com/document-viewer/TPS3700/datasheet/electrical-characteristics-slvsci76498), [BSS84 onsemi, hoja de fabricante](https://www.onsemi.com/pdf/datasheet/bss84lt1-d.pdf), [evaluación previa W43](../w_ind_43/README_W_IND_43.md). La hoja de onsemi y sus cotas de patilla requieren comprobación documental completa antes de asignar footprint. No se ha obtenido un modelo SPICE OEM validado.

## Matriz de decisión y BOM

MATRIZ_W_IND_44.csv y BOM_W_IND_44.csv separan ficha de fabricante, dato estimado, incertidumbre, coste IVA y disponibilidad verificada/pendiente. Una ficha de BSS84 distinta de BSS84LT1G **no acredita precio ni compatibilidad** del SKU elegido. Diotronic es proveedor auxiliar: no se ha verificado stock de Zaragoza, MOQ local, precio final con IVA ni sustitutos críticos trazables. No comprar nada.

**Separación obligatoria:** (A) dock de carga/batería/BMS fuera de este hito, sin OEM; (B) WPT distribuido del primer microsensor ficticio 5 V, ~0,4 W promedio / 1,5 W pico, solo banco resistivo futuro tras permiso; este circuito solo prueba una línea de señal y **no entrega energía inductiva**; (C) ESP-NOW/OpenThread transportan datos con ACK aplicación, CRC, secuencia, timeout, privacidad y recuperación propios: ninguno alimenta el módulo ni da parada crítica. WISP5 es referencia RFID para microsensores de potencia ínfima.

## Propietarios, revisión upstream y trabajo paralelo

Revisadas las decisiones locales 00/19 de 28/10, D22, acuerdo W/C, VALDO_OOMWOO/LEEME_PRIMERO y contrato WPT_DATOS_V01; la automatización inalámbrica W es la única habilitada de las relacionadas. La PR propia es VALDO #9, distinta de la PR #79 cleaning-jobs del mantenedor OOMWOO. No alterar repositorios de creadores ni otras ramas locales con trabajo pendiente.

- mark-belbin/simple-wireless-power, GPL-3.0, master HEAD 7c7858c0dd7040801b6f191df1396115560218f0 = pin 19. Es prueba publicada del **autor**, no nuestro circuito ni base CAD copiada.
- wisp/wisp5-hw, BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda = pin 19.
- wisp/wisp5, BSD-2-Clause, **rama por defecto 640kHz** 604eee2dffaeba3a270de61cf3dae887a33309c2; respecto al pin 19 d978a6978ad23ccd6c44dd55430973b04a3d4a9b ramas **divergentes** (+68/−11). No inferir recencia por orden de ramas ni mezclar firmware experimental.
- espressif/esp-now, Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin 19. No usar código ajeno en W44.
- openthread/openthread, BSD-3-Clause, main e577777c308f6c87e5da3056239231a8fc147cb2, +14/−0 frente al pin 19. No copiar sus implementaciones.
- makerspet/oomwoo main f01a1b295f462da5ab8d5f021a3f741cbd2b47df; no se toca. VALDO PR #9 pertenece a Valdi320, su HEAD se consulta justo antes de crear el nuevo commit. Se mantienen avisos de licencias de los autores.

## Puertas de seguridad pendientes

1. Acreditar alimentación y POR independientes desde ambos lados de un corte; eliminar posibles falsos HEALTH por pérdida selectiva del VDD del comparador, cable corto a positivo o puerta atascada.
2. Comprobar la función analógica OUTB↔BSS84 con modelo de fabricante, valores extremos de fuga, VGS, RDS(on), curvas temperatura y tiempos; definir lado de interfaz, VIH/VIL y backfeed con 3V3 parcial.
3. Integrar con **doble corte normalmente apagado y rearme manual W37 en hardware**; verificar KiCad completo, SPICE/transitorios, FOD, temperatura, EMI, humedad, offset y seguridad de carga antes de cualquier prueba energizada.
4. Comparar coste total WPT frente a arnés retenido reparable, especialmente si no se elimina por completo un cable o contacto.

**Estado:** propuesta digital y prueba de conectividad; NO FABRICAR, NO ENERGIZAR, sin batería/BMS/estación, sin ensayos ni aprobación de hardware.
