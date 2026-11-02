# W-IND-97 — impedir rearmado local con sesión repetida o reloj atrasado (01-11-2026)

**Objeto:** robot aspirador NUEVO, abierto y reparable; área propia W, PR #9. Ninguna reutilización OEM Xiaomi ni edición de OOMWOO, PR #79, repositorios de autores o fuentes de otros compañeros. Código y pruebas propios, Python 3.10+, stdlib, solo software experimental.

## Defecto real y reparación

En el HEAD anterior `30524b6982329b620ed206720d691f71a5e8efd4`, `ModuleReceiver.commission_local(session, now_ms)` validaba tipos/rangos pero aceptaba la **misma sesión o una inferior** y una **marca de tiempo anterior** a la ya observada. Al rearmar se borraban `last_seq`, `last_ms` y el fallo enclavado; una trama antigua de esa sesión podía parecer nueva. Un reloj atrasado podía volver a abrir la ventana aparente de telemetría. Son condiciones de fallo del **código experimental**, no vulnerabilidades constatadas en un robot físico.

**Arreglo localizado antes de toda mutación:** rechazar con `ValueError` cualquier sesión `<= self.session` y cualquier `now_ms < self.last_clock_ms` cuando esos valores previos existan. Se conserva un nuevo comisionado legítimo con sesión estrictamente superior, reloj igual o creciente y recuperación local después de una avería. No cambian 22 bytes por trama, CRC-16/CCITT-FALSE, ACK aplicativo, secuencias, tres envíos máximos, reintento a 60 ms, caducidad a 240 ms ni frescura nominal a 250 ms. Un valor `authenticated_transport=True` sigue siendo exclusivamente un **stub de prueba**, nunca autenticación criptográfica.

**Límite crítico:** reiniciar un proceso/MCU elimina la memoria del receptor. El bloqueo de épocas entre reinicios exige usar el `PowerFencedTelemetry` ya existente con un almacén monotónico **realmente duradero** y autenticación del enlace/provisión externa; su ejemplo SQLite es solo de host. Este parche no valida persistencia en flash/FRAM, ni protege ante rollback físico del reloj, EEPROM, identidad o compromisos criptográficos. No gobierna potencia, FOD, motores, baterías o paro crítico.

## Pruebas digitales reproducibles

Desde `research/2026-10-28-independent-wpt-sensor-v01/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_w_link test_power_restart_gate
```

Diez métodos `TestW97RecommissionBoundary` nuevos incorporados a `test_w_link.py`. Escenarios: sesión repetida sin datos, tras fallo y con ACK pendiente; época inferior; retroceso de reloj previo y posterior a datos; rearmado legítimo con época mayor; igualdad de reloj; agotamiento de contador; memoria no duradera entre objetos. **Antes** de la corrección, 8 de 10 pruebas adversariales fallaron realmente en PC; **después**, **87/87** pruebas de `test_w_link` y `test_power_restart_gate` superadas en el PC (10 nuevas + 77 de esas dos suites). Ver `EVIDENCIA.json`. La CI del repositorio ejecuta la suite general completa y debe comprobarse por separado tras el push; no confundir pruebas locales con GitHub PASS. Clase: `SOFTWARE_SINTETICO`. Sin radios, prototipos, medidas propias, corte independiente, FOD, EMI ni temperatura.

## Decisión de ingeniería por subsistema

| Problema | Decisión actual | Puerta mensurable y pendiente |
| --- | --- | --- |
| Datos locales y recuperación | **Adoptar** comprobación monotónica local como defensa adicional | Port al MCU, cifrado y autenticación reales, APP ACK, CRC, secuencia, temporizadores, pérdidas, recuperación tras arranque y desgaste de NVM |
| Radio ESP-NOW | Candidato económico para enlace local simple; no fuente de energía | Verificar APP ACK, cifrado de pares, privacidad, pérdidas y latencia en la placa real; ACK MAC no basta |
| Radio OpenThread | Alternativa, **no** instalar simultáneamente por defecto | Comparar pila, memoria, energía en reposo, AES/commissioning, malla e interoperabilidad solo si lo requiere el producto |
| Distribución a primer módulo | **Cable sustituible** como referencia; WPT regulado solo candidato | Objetivo inicial de estudio **hipotético 0,3 W de carga**, medir potencia de entrada, arranque, rendimiento, offset XY/ángulo, pérdidas, FOD, calor, EMI y corte autónomo normalmente OFF antes de retirar cable |
| WPT lazo abierto sencillo | No integrar | No acredita regulación, FOD, térmica, fallo único o desconexión independiente |
| Dock inductivo de carga | BLOQUEADO como subsistema distinto | Banco resistivo aislado y proceso formal de seguridad; sin conectar litio, BMS ni estación real |
| WISP5/NFC pasivo | Solo microsensores de demanda realmente mínima | Balance completo del lector/receptor y tensión disponible antes de justificarlo; no alimentar motores ni bombas con supuestos |
| Motores, turbina y bombas | No introducir WPT por defecto | Caracterizar consumo/picos y pérdidas, luego decidir |

**Protecciones pendientes:** FOD real, termometría independiente, desalineación, humedad, EMI, dos cortes con riesgo de fallo común y latencia de desconexión. Los protocolos RF jamás determinan un paro de motor/colisión/borde ni desbloquean cargadores; el circuito debe partir normalmente OFF.

## Revisión de fuentes ajenas (HEAD frente a 28-10-2026)

| Autor/repositorio, licencia | HEAD rama verificada 01-11-2026 | SHA registrada | Evaluación |
| --- | --- | --- | --- |
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master `7c7858c0dd7040801b6f191df1396115560218f0` | igual | Experimento inductivo abierto del autor, no protección regulada; no importar fuentes GPL sin análisis |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master `08332bc398aa3350d351ef2aaac163f8007cffda` | igual | Plataforma RFID de consumo minúsculo, no uso para 0,3 W sin medir |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | rama **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` | `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` | Divergencia **+68/−11 commits**, PR #40 abierta; no inferir versión por edad o nombre de rama |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | igual | No confundir confirmación MAC con APP ACK |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main `c6872259f4194fb76c7d333bda209343e8c88e71` | `7009584dadc20cf20c20a6062f357dd572ba6885` | +21 commits, incluyendo #13800 MLE Link Accept; ninguna ventaja energética supuesta |
| [makerspet/oomwoo](https://github.com/makerspet/oomwoo), Apache-2.0 | main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` | comparación oficial actual | Solo referencia: OOMWOO firmware Nov 1 J1 sin I2C, PCB Nov 1 esquema; no tocar upstream |

No se ha copiado código, esquemas ni CAD de estos creadores. Fuente rectora: `19-alternativas-abiertas-para-robot-independiente.md` y contrato `WPT_DATOS_V01.md`. Ver matriz y BOM CSV del hito.

## Coste, abastecimiento, autorización y siguiente paso

**Coste incremental de hardware de esta corrección = 0 €**; ni tiempo de ingeniería ni precio de producción se valoran aquí. Diotronic solo proveedor **auxiliar**, sin referencias/MOQ/precio final IVA/stock de Zaragoza comprobados para futura cesta; TME, Mouser, DigiKey o fabricante según trazabilidad. No equiparar catálogo con inventario. No existe elección ni compra de componentes. El esquema KiCad W18 mantiene tres errores ERC previos; no aprobado para montaje/energía.

Siguiente trabajo de mayor retorno, **solo previa autorización y protocolo de seguridad**, es caracterizar en banco aislado con carga ficticia el consumo del lector, la salida del receptor, estabilidad, calor y fallos de comunicaciones, sin baterías, BMS, estación, motores ni material OEM.
