## MODIFIED Requirements

### Requirement: Interfaz Web Responsiva
Se extiende la capacidad del dashboard para permitir el control granular de actuadores de percepción.

#### Scenario: Orientación de sonar manual
- **WHEN** el usuario ingresa un ángulo numérico en el dashboard y presiona "Girar"
- **THEN** la interfaz envía un mensaje de control de servo vía WebSocket
- **AND** el rover orienta el sensor ultrasónico al ángulo exacto solicitado (dentro del rango -90 a 90)
