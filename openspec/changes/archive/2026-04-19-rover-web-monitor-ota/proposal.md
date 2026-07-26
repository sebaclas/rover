## Why

El rover actualmente solo puede ser monitoreado vía cable USB/Serial, lo cual limita las pruebas de navegación autónoma. Además, cada cambio de código requiere conexión física. Esta propuesta busca implementar un monitor web en tiempo real para telemetría y control remoto, junto con un sistema de actualización inalámbrica (OTA) para agilizar el desarrollo.

## What Changes

- **Telemetría en tiempo real**: Visualización de datos del sonar vía WebSockets.
- **Control remoto**: Interfaz web con botones y soporte de teclado (WASD) para mover el rover.
- **Actualización OTA**: Capacidad de descargar nuevas versiones de software desde un servidor remoto/GitHub.
- **Refactorización de Hardware**: Separación de la lógica de sensores y actuadores en un módulo dedicado (`rover.py`).
- **Servidor Web Asíncrono**: Integración de `Microdot` para manejar peticiones web y WebSockets sin bloquear la ejecución del rover.

## Capabilities

### New Capabilities
- `web-monitor`: Interfaz web para visualización de telemetría y envío de comandos de movimiento.
- `ota-update`: Sistema de actualización de archivos .py vía WiFi para mantenimiento sin cables.

### Modified Capabilities
- Ninguna (el proyecto está en fase inicial y no hay especificaciones previas que cambiar).

## Impact

- **Código**: Reescritura completa de `main.py` para soportar el bucle asíncrono (`uasyncio`).
- **Nuevos Archivos**: `rover.py` (abstracción de hardware), `web_monitor.py` (servidor), `ota.py` (actualización).
- **Dependencias**: Incorporación de la librería `Microdot` (flash externa o local).
- **Hardware**: El rover debe estar conectado a la red local definida en `secrets.py`.
