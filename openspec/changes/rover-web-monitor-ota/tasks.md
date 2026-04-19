## 1. Preparación y Dependencias

- [x] 1.1 Descargar `microdot.py` y `microdot_websocket.py` para subir a la placa
- [x] 1.2 Crear archivo `version.json` local con `{"version": "0.1.0"}`

## 2. Abstracción de Hardware

- [x] 2.1 Crear `rover.py` con la clase `Rover` que gestione el Sonar (HC-SR04)
- [x] 2.2 Implementar métodos `medir_distancia()` y `set_motores()` en `rover.py`

## 3. Interfaz de Usuario y Servidor

- [x] 3.1 Crear `index.html` con el Dashboard (Gauge de sonar y botones de control)
- [x] 3.2 Crear `web_monitor.py` para servir el HTML y manejar WebSockets de telemetría
- [x] 3.3 Implementar rutas de control en `web_monitor.py` para recibir comandos

## 4. Sistema de Actualización (OTA)

- [x] 4.1 Crear `ota.py` con lógica para descargar archivos desde GitHub/URL
- [x] 4.2 Integrar botón de "Update" en la interfaz web que dispare la lógica de `ota.py`

## 5. Integración Final

- [x] 5.1 Re-escribir `main.py` usando `uasyncio` para coordinar el Rover y el Web Server
- [x] 5.2 Realizar pruebas de integración: acceso web, control de motores y lectura de sonar simultánea
