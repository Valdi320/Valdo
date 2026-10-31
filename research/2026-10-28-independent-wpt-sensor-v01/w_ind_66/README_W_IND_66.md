# W-IND-66 — Borrado cruzado de los dos enclavamientos de potencia TX

**31/10/2026. Entrega propia del sector W, robot independiente NUEVO. Todo es software de simulación; cero ensayos eléctricos.**

### Fallo verdadero y corrección ejecutable
En el código W-IND-07, con ambos canales ya armados, si **solo A** señalaba alta temperatura y **su corte A estaba soldado cerrado**, se desarmaba A pero **B seguía ON** y el modelo mostraba TX energizado. El caso simétrico B también fallaba. Las 43 pruebas anteriores ponían **ambos sensores** calientes al ensayar un corte soldado y ocultaban esta vulnerabilidad.

**Autoría del descubrimiento:** Codex A01, relevo \`RELEVO_CODEX_W_A01_PARADA_CRUZADA_20261028.md\` de 28/10, commit de su rama local \`319784de6549a3a99eae59a93d166043175ce25f\`. El cambio y nuevas pruebas de esta PR se elaboran en nuestra fuente W tras revisar el hallazgo, **sin importar ni sobrescribir** el parche, clon o ficheros del compañero.

**Corrección:** un fallo de **cualquier** cadena A/B borra **ambos** latches; lo mismo ocurre si falta alimentación o petición local. Rearmar exige un **nuevo flanco local** y **ambos monitores sanos**. No hay camino para rearmar por radio ni aceptación de paquetes. El modelo ahora solicita abrir el otro corte si un lado falló y su interruptor quedó soldado.

### Prueba adversarial y límites
- **Antes:** A caliente / B normal / corte A soldado ⇒ \`energized=True\` (FALLO).
- **Después:** misma entrada ⇒ \`energized=False\` porque B ordena OFF. El caso B simétrico también se bloquea.
- Tras recuperación aparente, ambos siguen desarmados hasta un reset físico en flanco, con los dos sensores correctos.
- **Peligros no resueltos:** ambos cortes soldados ⇒ ON incluso con alarma; ambos sensores atascados en valores sanos ⇒ alarma no detectada; referencias/rails/firmware comunes, FOD, retardos, calor y cortocircuitos no verificados. **NO** existe aún cableado/circuito cruzado ni segundo corte autónomo comprobado. El resultado NO autoriza construir ni energizar.

### Reproducción
Desde \`research/2026-10-28-independent-wpt-sensor-v01\`:
\`\`\`bash
python3 -m unittest -v test_tx_thermal_window
python3 -m unittest discover -s w_ind_66 -p 'test_w66.py' -v
python3 -m w_ind_66.w66_demo > W66_CROSS_TRIP_SYNTHETIC.json
\`\`\`
Las pruebas nuevas incluyen 10 clases de fallo por cada canal, 18 combinaciones de fallo unilateral con cortes en estados normal/soldado/abierto, reset mantenido, rearmado, alimentación y petición local. La CI comprueba el código real del repositorio y archiva evidencia JSON **SYNTHETIC_BOOLEAN_MODEL_ONLY**. No atribuir PASS a la CI hasta verificar el resultado de GitHub.

### Tres subsistemas independientes
**Dock:** potencia/carga y BMS/litio bloqueados, sin estaciones/baterías reales; faltan doble corte autónomo, FOD, termometría, offset, metal, humedad y EMI. **Potencia a módulos:** piloto de sensor 5 V / 0,4 W medio y 1,5 W pico es SOLO HIPÓTESIS, no consumo medido; WPT sencillo frente a regulado y cable desmontable siguen sin validación real. NO WPT para motores/bombas sin consumos y pérdidas. **Datos:** ESP-NOW unicast CCMP y OpenThread se comparan en W65; ACK aplicativo, CRC, secuencias, timeout, privacidad y recuperación NO sustituyen una desconexión eléctrica independiente. WISP solo para microsensores RFID de potencia mínima.

### Matriz de decisiones
| Solución | Ventaja | Defecto / criterio | Estado |
|---|---|---|---|
| Dos latches W07 sin cruce | Menos lógica | Un corte soldado + alarma solo en ese canal deja TX ON | **RECHAZADA** |
| Borrado cruzado de latches W66 | Evita el fallo **en el modelo** sin electrónica añadida | No demuestra cableado de corte autónomo | **IMPLEMENTADO EN PYTHON** |
| Dos etapas independientes físicamente, normalmente OFF | Podría limitar fallo simple de corte | Exige esquema/ELC, selección de piezas, FOD real, pruebas | **PENDIENTE** |
| Parada crítica por RF | Ninguna garantía ante radio perdida | Inaceptable | **PROHIBIDA** |
| Cable reforzado desmontable | Sin pérdidas ni riesgo WPT | Sigue habiendo conexión en mantenimiento | **FALLBACK** |

### Auditoría de fuentes externas y propietarios — 31/10/2026
| Proyecto ajeno (licencia declarada) | SHA pin 28/10 ⇒ HEAD oficial y revisión |
|---|---|
| mark-belbin/simple-wireless-power (GPL-3.0) | \`7c7858c0\` ⇒ master \`7c7858c0\`; 0 nuevos, PR #1 fusionada 2021; potencia/eficiencia del autor NO nuestra |
| wisp/wisp5-hw (BSD-2-Clause) | \`08332bc3\` ⇒ master \`08332bc3\`; 0 nuevos, PR #1 histórica |
| wisp/wisp5 (BSD-2-Clause) | \`d978a697\` ⇒ **640kHz \`604eee2d\`**, 68 commits delante/11 detrás (DIVERGENTE), PR #40 abierta; NO fast-forward |
| espressif/esp-now (Apache-2.0) | \`c3b5f9be\` ⇒ master \`c3b5f9be\`; 0 nuevos, PR #151/#153 y compatibilidad IDF v6 consultadas |
| openthread/openthread (BSD-3-Clause) | \`7009584d\` ⇒ main \`b6d0f06d\` (+18/0); #13790/#13823 sobre radio/SPINEL/build, v2026.10.0 |
| OOMWOO oficial makerspet/oomwoo | main \`f01a1b29\` ; PR #79 cleaning-jobs sigue ajena |
| OOMWOO firmware oficial makerspet/oomwoo-firmware | main \`ce05f266\` (pinout/especificación 31/10), sin alterar |

Fuentes de sus respectivos autores: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo ; https://github.com/makerspet/oomwoo-firmware. Referencias técnicas: https://www.ti.com/product/TLV3211 ; https://www.ti.com/product/TPS3430 .

Documentación maestra del 28/10, D22, acuerdo W/C y VALDO_OOMWOO verificados antes de editar. No se modifica su contenido, los clones upstream, PR #79, CAD de C ni el checkout local sucio. Código externo GPL/BSD/Apache **NO copiado**; se acredita hallazgo del compañero.

### BOM, coste y Diotronic
Ver \`BOM_W_IND_66.csv\`: esta corrección **añade 0 € en hardware**, no implica que dos cortes físicos sean gratis. Para futura placa requieren trazabilidad dos NTC, cuatro funciones de comparador, dos latches y dos interruptores serie normalmente OFF, detección FOD/humedad/offset independiente. Referencia histórica NTC Eaton NRNE104F3950B1F 0,242 €/ud IVA el 28/10 según estudio W07, **precio actual no corroborado**. Stock, cantidades mínimas, IVA y portes de Diotronic Zaragoza **no confirmados**; TME, Mouser, DigiKey y fabricantes siguen alternativas por documentación técnica.

### Siguiente puerta
El ERC KiCad W18 sigue bloqueado por **3 errores y 6 advertencias**, y NO existe circuito real de cruce o corte independiente. Diseñar/validar hardware con FOD, temperatura y fallo único antes de preparar procedimiento físico, cuya ejecución exige autorización expresa. **Sin compras, impresiones, soldaduras, energización ni cambios de firmware/batería/estación.**
