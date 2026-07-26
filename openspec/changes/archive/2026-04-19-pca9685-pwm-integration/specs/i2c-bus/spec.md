## ADDED Requirements

### Requirement: Inicialización I2C
El sistema DEBE proveer un bus I2C global, accesible para múltiples periféricos, utilizando los pines definidos en la especificación de hardware.

#### Scenario: Configuración de pines correcta
- **WHEN** el sistema se inicializa
- **THEN** se configura un bus I2C usando GPIO 4 para SDA y GPIO 5 para SCL
- **AND** opera a una velocidad compatible con el PCA9685 (ej: 400kHz)
