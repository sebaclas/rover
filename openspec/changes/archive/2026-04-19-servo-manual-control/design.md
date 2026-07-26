# Servo Manual Control Design

## Overview
Esta mejora permite al usuario enviar ángulos específicos al servo del sonar mediante la interfaz web.

## Architecture

### Frontend (index.html)
1. **Interfaz**: Se agregará una sección en la tarjeta de "Estado del Sistema" o una nueva tarjeta de "Percepción" que contenga:
   - Un `input type="number"` con rango de -90 a 90.
   - Un botón de "Girar".
2. **Lógica JS**: Una nueva función `sendServoAngle()` capturará el valor del input y enviará un JSON al WebSocket: `ws.send(JSON.stringify({servo: angle}))`.

### Backend (web_monitor.py)
1. **Manejador de WebSocket**: Se actualizará el loop `handle_websocket` para buscar la clave `servo` en el JSON recibido.
2. **Acción**: Si existe la clave `servo`, se llamará a `rover.set_servo_angle(int(data['servo']))`.

## Safety & Limits
* El firmware en `rover.py` ya limita el ángulo a [-90, 90], pero agregaremos validación en el HTML (`min` y `max`) para mejorar la experiencia de usuario.
