# W-IND-37: rearme local que exige observar liberación tras PG (MODELO)

30/10/2026, VALDO sector W, robot NUEVO. Xiaomi OEM expresamente descartado. Solo simulación lógica; **NO FABRICAR, ENERGIZAR NI CARGAR LITIO**.

## Defecto de alto retorno detectado
El modelo digital de W36 no exige observar liberación de los pulsadores después de verificar el estado de PG. Su Rearm().step(True,True,True,True) puede devolver (True, True) en el primer paso incluso si los dos botones estaban pulsados desde el arranque. Este es un fallo de la **especificación digital**, no evidencia física de que el hardware KiCad W36 se comportará así. SN74LVC1G74 de TI tiene reloj por flanco y clear asíncrono; POR/temporización/rebotes requieren comprobación eléctrica.

## Contrato W37 propuesto y probado digitalmente
Arranque ambos EN OFF; PG de 3,3 V y 5 V correctos 3 muestras consecutivas; ambos pulsadores LIBERADOS 2 muestras después de PG; posterior pulsación estable 2 muestras por pulsador; permisos EN_A y EN_B simultáneos sólo al cumplir ambos. Pérdida de cualquier PG borra todo y exige nueva secuencia. Ninguna entrada RF rearmará cortes. Temporización 10 ms/muestra, 3/2/2 y ~70 ms mínimo son hipótesis, NO garantías ni solución de seguridad. Un Schmitt por sí solo no memoriza liberación y no es solución suficiente.

Archivos originales: w37_rearm_guard.py, test_w37.py, W37_EVIDENCE.json, matriz y BOM. Reproducción desde este directorio:
    python3 -m unittest -v test_w37.py
    python3 w37_rearm_guard.py --report W37_EVIDENCE.json

15 pruebas deterministas: incluyen comparación con fuente W36 sin modificar, botones altos en arranque, rebotes, pérdidas de cada PG y salida conjunta. Barrido 16^4=65.536 secuencias sintéticas de 4 muestras; no pruebas físicas ni exhaustividad de fallos largos. JSON indica hardware_tested=false y safe_to_energize=false. W36 KiCad aún NO implementa la secuencia.

## Matriz de decisiones y límites
MATRIZ_W_IND_37.csv distingue W36, RC/Schmitt insuficiente, contrato W37, prohibición rearme por radio, WPT sin FOD y carga dock fuera de ámbito. BOM_W_IND_37.csv separa TI, TME y Diotronic. SN74LVC1G17DBVR solo candidato para bordes; TME España catálogo ~0,15 €/ud IVA mínimo 1, stock web 12552 no reservado; **Diotronic Zaragoza precio/stock NO comprobado**, auxiliar para pasivos y pulsadores compatibles. Ninguna compra ni nuevo chip seleccionado.

Problemas separados: (1) dock y batería/BMS totalmente desconectados; (2) distribución WPT a un primer sensor hipotético 5 V, 0,4 W promedio y 1,5 W pico; no motores o bombas; (3) ESP-NOW o OpenThread únicamente datos con ACK de aplicación, CRC, secuencia, timeout, privacidad y recuperación por implementar. WISP5 sólo microsensores RFID intermitentes. Alternativa conector cableado reparable sigue vigente sin retorno económico WPT demostrado.

PENDIENTES CRÍTICOS: INA301 todavía no corta sobrecorriente, monitor desalimentado puede aparentar alarma sana, fuente 3,3 V no acreditada, eFuse no discrimina por sí mismo 300/400 mA, FOD, temperatura, offset, humedad, metales, EMI, secuenciación, POR, antirrebote, retornos comunes y DRC. No hay PCB ni medición. La comunicación no controla la parada crítica.

## Auditoría de derechos y fuentes HEAD y PR (30/10/2026)
Se leyeron previamente el maestro 00_DECISION_20261028_NO_TRASPLANTE_X20.md, el maestro 19-alternativas-abiertas-para-robot-independiente.md, D22, coordinación C/W, VALDO_OOMWOO/LEEME_PRIMERO.md y WPT_DATOS_V01.md. No se incorporó código ni CAD ajeno.
- Belbin GPL-3.0 master 7c7858c0dd7040801b6f191df1396115560218f0 = pin, PR#1 fusionada. https://github.com/mark-belbin/simple-wireless-power
- WISP5 HW BSD-2-Clause master 08332bc398aa3350d351ef2aaac163f8007cffda = pin, PR#1 fusionada. https://github.com/wisp/wisp5-hw
- WISP5 firmware BSD-2-Clause 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 vs pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b; diverge 68 ahead / 11 behind; PR#40 abierta. https://github.com/wisp/wisp5
- ESP-NOW Apache-2.0 master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pin, PR#153/151 revisadas. https://github.com/espressif/esp-now
- OpenThread BSD-3-Clause main e577777c308f6c87e5da3056239231a8fc147cb2, +14/0 del pin 7009584dadc20cf20c20a6062f357dd572ba6885; commits #13810 y #13812 y PR#13820 revisados. https://github.com/openthread/openthread
OOMWOO oficial main f01a1b295f462da5ab8d5f021a3f741cbd2b47df, firmware c63a21e14e7d950be7ac8195078b6f2211a1c8a4, PCB 342e80811609b2df3b8f24d5c857e076151e468a, CAD 038002ddc5586d711960545ecf76a038eec48656; PR#79 cleaning-jobs SIN TOCAR; otros propietarios, Codex y C no modificados. Automatizaciones paralelas relevantes sin ejecución activa. Referencia TI https://www.ti.com/product/SN74LVC1G74 ; https://www.ti.com/product/SN74LVC1G17 ; https://www.ti.com/product/TPS3840.

Siguiente hito no iniciado: secuencia física KiCad de liberación, supervisor del INA301 y corte autónomo ante sobrecorriente, validar ERC/netlist y transitorios; posteriormente FOD/térmica independientes TX, sin litio ni estación.
