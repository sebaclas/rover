## Why

El rover actualmente cuenta con telemetría del sensor MPU-6050 y control de servo, pero carece de un sistema de control en lazo cerrado para realizar maniobras autónomas precisas. Esta propuesta introduce giros controlados por giroscopio (e.g., giros exactos de 90 grados) integrados con una capa de seguridad activa basada en el sonar ("Look-Before-Turn"), asegurando que el rover no colisione al iniciar o realizar una rotación.

## What Changes

*   **Giro Preciso con Gyro Z**: Implementación de un lazo de integración para controlar giros precisos usando el eje Z del giroscopio del MPU-6050.
*   **Look-Before-Turn (Sonar)**: Rotación previa del servo del sonar en la dirección elegida para inspeccionar la trayectoria antes de mover las ruedas.
*   **Prioridad Absoluta del Sonar**: Monitoreo constante durante el giro físico del rover; si se detecta un obstáculo (< 10cm), se detiene la maniobra.
*   **Evasión Activa**: Ante obstrucciones previas o durante el giro, el rover realiza un retroceso de seguridad (~10cm basado en tiempo) y reintenta el giro.
*   **Driver DRV8833**: Configuración y mapeo del puente H DRV8833 utilizando un esquema de 2 canales PWM por motor desde el PCA9685.

## Capabilities

### New Capabilities

- `safe-imu-turning`: Control de movimiento y giros precisos en lazo cerrado por IMU con escaneo preventivo por sonar y evasión activa de obstáculos.

### Modified Capabilities

*Ninguna. La telemetría del MPU-6050 existente no sufre alteraciones en sus requisitos de visualización.*

## Impact

*   `rover.py`: Se implementará la lógica del driver DRV8833 (2 canales por motor), el lazo de integración del giroscopio con calibración rápida "Zero-Rate" y el flujo asíncrono de verificación del sonar y evasión.
*   `web_monitor.py`: Adición de soporte para comandos de giros específicos (ej. girar 90° a la izquierda/derecha) a través del WebSocket.
*   `index.html`: (Opcional/Seguimiento) Botones o controles en el dashboard para disparar giros precisos.
