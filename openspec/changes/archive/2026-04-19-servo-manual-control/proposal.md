## Why

El usuario necesita tener control directo sobre la orientación del sensor ultrasónico (HC-SR04) para realizar exploraciones manuales sin mover el rover completo. Actualmente, el ángulo está fijo (centrado) en el arranque o mediante pruebas de código, pero no es accesible desde la interfaz web.

## What Changes

* **Dashboard (UI)**: Se agregará un nuevo control en la interfaz web (un selector numérico o slider y un botón) para definir el ángulo del servo.
* **Comunicación (Protocolo)**: Se implementará un nuevo tipo de comando en el WebSocket (`{"servo": <grados>}`) para transmitir la posición deseada.
* **Controlador (Backend)**: Se actualizará el manejador de mensajes en `web_monitor.py` para invocar el método `rover.set_servo_angle()` basado en las instrucciones recibidas por el usuario.

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- `web-monitor`: Se extienden los requisitos para incluir el control manual de periféricos (servos) desde el dashboard.

## Impact

* **index.html**: Modificación de la estructura y el script de comunicación.
* **web_monitor.py**: Actualización de la lógica del manejador de WebSockets.
* **rover.py**: Ninguno (el método `set_servo_angle` ya existe).
