## 1. Implementación del Driver de Motores (DRV8833)

- [x] 1.1 Modificar `rover.py` para reescribir `set_motores(izquierda, derecha)` utilizando la lógica del DRV8833 con 2 canales del PCA9685 por motor: Canales 0 y 1 para el motor izquierdo, Canales 2 y 3 para el motor derecho.
- [x] 1.2 Implementar soporte de freno activo (escribiendo duty cycle 4095 en todos los canales involucrados) en `rover.py` para detención inmediata y precisa.

## 2. Lógica de Giro Controlado por IMU y Seguridad Activa

- [x] 2.1 Crear la función asíncrona `tomar_offset_gyro_z()` en `rover.py` para promediar lecturas estáticas rápidas (50ms) y establecer el sesgo del giroscopio justo antes del giro.
- [x] 2.2 Implementar la función asíncrona `retroceder_distancia_segura()` en `rover.py` para retroceder unos ~10cm por tiempo controlado a velocidad reducida.
- [x] 2.3 Implementar la función principal asíncrona `girar_grados(target_angle)` en `rover.py` que controle toda la secuencia: apuntar el servo del sonar a la trayectoria, escanear distancias, retornar el servo, calibrar offset, iniciar rotación integrando el giroscopio a 50Hz, y abortar/retroceder/reintentar de manera recurrente ante obstáculos detectados.

## 3. Integración en Web Server y Dashboard

- [x] 3.1 Actualizar el manejador de WebSocket en `web_monitor.py` para reconocer comandos de giros precisos (ej. `TURN_LEFT_90` y `TURN_RIGHT_90`) y disparar la rutina `girar_grados`.
- [x] 3.2 Añadir botones e indicaciones visuales correspondientes en `index.html` para permitir disparar y monitorear el estado del giro controlado desde la interfaz web.

## 4. Pruebas y Validación

- [x] 4.1 Crear un script de pruebas unitarias o de REPL en `.scratch/` para verificar el correcto funcionamiento de las tracciones y el comportamiento del lazo de integración y de evasión del sonar.
