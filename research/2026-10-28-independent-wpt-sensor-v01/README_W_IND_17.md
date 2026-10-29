# W-IND-17 — KiCad ERC auténtico en CI (29/10/2026)

## Avance material
W-IND-15 y W-IND-16 comprueban contratos geométricos, NO reglas eléctricas nativas. Aquí añadimos un flujo automático propio que ejecuta kicad-cli sch erc de **KiCad oficial 9.0.2** en contenedor efímero de GitHub Actions y conserva el JSON original, el código real de salida, versión de herramienta, hash SHA-256 de esquema y una atestación inequívocamente **NO_APTO_PARA_FABRICAR**. Este resultado no se presenta como si el ERC hubiese corrido antes de terminar GitHub Actions. El nuevo clasificador tiene 12 pruebas deterministas de resultados y fallos deliberados.

## Reproducción y evidencia
Desde este directorio, ejecutar python3 -m unittest -v test_w_ind_17_erc_gate. Para ERC real usar el flujo .github/workflows/w-ind-17-kicad-erc.yml con kicad/kicad:9.0.2, ejecutando:
- kicad-cli sch erc --format json --severity-all --exit-code-violations --output erc.json W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch
- RC 0 = sin infracciones reportadas; RC 5 = infracciones; cualquier otro código = ERROR de herramienta (no ERC aprobado). La discrepancia entre RC y JSON es error.
- descargar artefactos erc.json y attestation.json de esa ejecución. Si se detectan infracciones, este CI publica evidencia del bloqueo (no maquilla un ERC incorrecto); si ERC es cero, el circuito sigue sin certificación.

## Hallazgo y matriz de decisión
El [fabricante TI](https://www.ti.com/product/TPS22918) publica TPS22918DBVR, SOT-23-6, 1–5.5 V, 2 A máx. y **Current limit type: None**. Los dos interruptores del esquema en serie NO equivalen a limitación de corriente, FOD, desconexión térmica independiente o protección inversa. Además, faltan fuente externa definida, condensadores de bypass, drivers EN_A/EN_B independientes y una carga TX específica. Las etiquetas y pruebas estáticas no prueban que esos bloques existan.

| Ruta | Aporta | Decisión |
| --- | --- | --- |
| W-IND-16 geométrico | Conexiones y pines no desplazados | Mantener |
| ERC nativo con versión y JSON inmutables | Identifica violaciones KiCad reales | **Implementado** |
| Asumir hardware seguro con ERC sin errores | Riesgo oculto de FOD/OC/reversa | Prohibido |
| Instalar/probar batería, dock o bobinas activas | No hay permiso ni seguridad | Bloqueado |

## Propietarios, licencias y cambios recientes contrastados el 29/10/2026
- [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0, master HEAD 7c7858c: igual al SHA registrado.
- [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause master 08332bc: igual; [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause rama por defecto **640kHz** HEAD 604eee2, divergencia respecto a d978a69 **68 commits delante y 11 detrás**. No fast-forward ni adopción.
- [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 master c3b5f9b: igual; datos RF no llevan potencia y necesitan ACK aplicación, CRC, secuencia, tiempo, privacidad.
- [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause main 51aa078: 9 commits posteriores a pin 7009584; no integrados. WISP sólo para microsensores.
- [KiCad CLI oficial](https://docs.kicad.org/9.0/en/cli/cli.html) y [contenedor oficial](https://hub.docker.com/r/kicad/kicad). Se utiliza herramienta, no se copia su código GPL en nuestro repositorio.

Leídas decisión NO_TRASPLANTE, 19-alternativas, D22, coordinación C/W, LEEME y contrato WPT_DATOS_V01. Se conserva el checkout master local con cambios de compañeros sin tocarlo. No se modifica OOMWOO, PR #79, geometría de C ni hardware OEM. PR #9 es propia y W.

## BOM y límite
[BOM_W_IND_17.csv](BOM_W_IND_17.csv): no añade ninguna pieza física; proveedor auxiliar Diotronic sin referencias/IVA final/stock/MOQ confirmados, TME/Mouser/DigiKey siguen alternativas; NO seleccionar seguridad crítica sin ficha y trazabilidad. Primera transferencia de sensores hipotética 5 V/0.4 W media/1.5 W pico, sin consumo real medido. Dock de carga y batería/BMS independientes, desconectados. No se ha alimentado ninguna bobina ni montado placa.

**Siguiente puerta:** interpretar el ERC real, corregir fuentes de alimentación y supervisores concretos; añadir FOD, temperatura, sobrecorriente, bloqueo inverso y circuitos de apagado verdaderamente independientes antes de valorar siquiera un banco resistivo autorizado.

## Resultado real del primer intento y corrección W-IND-17
El primer workflow del commit 5c46f498 ejecutó realmente KiCad 9.0.2, que informó **9 violaciones** del borrador W-IND-15: 1 etiqueta colgante (VIN_5V), 2 entradas de alimentación no excitadas y 6 advertencias porque no hay tabla local de la biblioteca VALDO. El primer clasificador marcó CI fallo porque esperaba erróneamente `violations` en la raíz; el informe real KiCad 9 utiliza `sheets[].violations`. Esta corrección reconoce esa estructura y suma por hoja, exige esquema oficial `erc.v1.json` y rechazo ante datos mal formados. Se corrige HOME/XDG temporal del contenedor que ocasionó errores de permiso de usuario no privilegiado. **Ni estas correcciones ni un ERC limpio declaran seguridad o validez eléctrica.**

Informe del primer intento: https://github.com/Valdi320/Valdo/actions/runs/40824199506 ; artefacto bruto https://github.com/Valdi320/Valdo/actions/runs/40824199506/artifacts/12875409308. El CI final posterior debe validarse aparte.
