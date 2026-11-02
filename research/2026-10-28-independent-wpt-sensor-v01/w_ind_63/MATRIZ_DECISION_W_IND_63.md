# W-IND-63 · matriz decisional y puertas

| Criterio | SQLite + ancla real externa | SQLite sin ancla | Solo RAM W62 | Resultado |
|---|---|---|---|---|
| Reapertura de proceso / fichero | Debería conservar token; probado con test fake-anchor | Conserva token mientras disco no se borre | No lo conserva tras proceso | Implementado digitalmente |
| Restauración de snapshot antiguo | Detectable con CAS fiable + digest anclado | **No detectable de forma segura** | No detectada | Test simulado con ancla RAM; sin prueba física |
| Corte entre CAS y commit | Se bloquea, sin recuperación automática; exige estudio NVM | Posible replay si base retrocede | No protegida | Fallo inyectado digital, no corte real |
| Disponibilidad / coste | Incógnita hasta escoger ancla, validar vida ciclos y temperatura | Más barata pero inaceptable para garantía antirollback | Solo tests | No seleccionar hardware aún |
| Reparación local | Necesita servicio y política de migración de credenciales, sin rearme remoto automático | Fácil pero inseguro ante ataques | No apto | Pendiente diseño de servicio |
| FOD/temperatura/EMI/corte eléctrico | No los controla: parar localmente y por hardware | Tampoco | Tampoco | Gate físico bloqueado |
| Privacidad RF | Sin cifrado; HMAC autentica pero no oculta el dato | Igual | Igual | No declarar privacidad demostrada |
| Elección de datos | ESP-NOW sencillo para enlace punto-punto candidato / OpenThread para red; ambos necesitan ACK aplicación y reloj | Igual | Igual | No elegida; compare head autor y licencia |
| Dock de carga | **Incompatible** con justificar carga segura solo por software | Igual | Igual | Dock y batería desconectados |

**Decisión:** conservar implementación como experimento reproducible, **no cualificar** ni ofrecer desplegado hasta elegir ancla de verdad y practicar pruebas de brownout con procedimiento autorizado. El flujo de seguridad no depende de ACK ni radio. WISP queda fuera salvo microsensores.
