# W-IND-86 — especificación de interfaces, NO circuito fabricable

**1. Dock de carga independiente** -> módulo WPT regulado con FOD, monitor térmico y corte autónomo; batería/BMS desconectados, ningún ensayo autorizado. No extrapolar potencia NFC en mW a dock.

**2. Módulo sensor opcional de potencia baja** -> lector NFC 13,56 MHz y antena (SIN SELECCIONAR) -> ST25DV04KC EH V_EH sin regular -> monitor normalmente OFF + convertidor + buffer (SIN SELECCIONAR) -> microsensor no crítico. Campo H, offset, humedad, temperatura, energía TX/RX, compatibilidad RF y precio pendientes. Cable desmontable sigue referencia.

**3. Datos** -> inventario ISO15693 de prueba ST no es ACK de aplicación ni comunicación garantizada. Independientemente, ESP-NOW/OpenThread necesitarían payload con CRC, HMAC o AEAD cuando corresponda, secuencias, desafío de arranque, ACK app, timeout y recuperación. Nunca parar motores/bomba por paquete RF: función crítica usa interruptor/corte local eléctrico.

Gates medibles antes de fabricar: H y 6DoF reales, lecturas P_TX/P_RX con incertidumbre y pérdidas de reposo, corriente radio wake/TX/RX/ACK, V_EH mínimo durante pérdida de campo, protección sobrevoltaje y undervoltaje, FOD metal pequeño, calor, EMI, humedad, corte independiente, tiempos de rearme, coste completo a Zaragoza y mantenimiento. Aprobación de banco aislado y sin litio por separado. **hardware_release=BLOCKED**.
