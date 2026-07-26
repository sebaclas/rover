# Web-monitor Specification
## Requirements
### Requirement: Visualización de Telemetría (Sonar)
El sistema DEBE transmitir los datos de distancia detectados por el sensor ultrasónico HC-SR04 hacia la interfaz web en tiempo real utilizando WebSockets.

#### Scenario: Transmisión exitosa de distancia
- **WHEN** el sensor realiza una lectura de distancia válida
- **THEN** el sistema envía un mensaje JSON vía WebSocket con el valor en centímetros a todos los clientes conectados

### Requirement: Control Remoto del Rover
El sistema DEBE permitir el envío de comandos de movimiento (adelante, atrás, izquierda, derecha, detener) desde la interfaz web.

#### Scenario: Ejecución de comando de movimiento
- **WHEN** el usuario presiona un botón de dirección en la web o una tecla (WASD)
- **THEN** el rover activa los motores en la dirección correspondiente y lo refleja en el log de la web

### Requirement: Interfaz Web Responsiva
Se extiende la capacidad del dashboard para permitir el control granular de actuadores de percepción.

#### Scenario: Orientación de sonar manual
- **WHEN** el usuario ingresa un ángulo numérico en el dashboard y presiona "Girar"
- **THEN** la interfaz envía un mensaje de control de servo vía WebSocket
- **AND** el rover orienta el sensor ultrasónico al ángulo exacto solicitado (dentro del rango -90 a 90)

