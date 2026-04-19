## ADDED Requirements

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
El sistema DEBE servir una página HTML única que contenga el dashboard de control y telemetría, accesible vía la dirección IP del ESP32.

#### Scenario: Acceso al Dashboard
- **WHEN** el usuario navega a la IP del rover en un navegador web
- **THEN** el sistema sirve el archivo HTML con los controles y el visor de sonar activos
