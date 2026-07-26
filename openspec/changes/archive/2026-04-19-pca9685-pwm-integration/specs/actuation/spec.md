## MODIFIED Requirements

### Requirement: Control de Tracción y Dirección
Se modifica la capa física del control; la implementación de las señales PWM DEBE transferirse al controlador PCA9685 en I2C, preservando el comportamiento externo.

#### Scenario: Comando de avance
- **WHEN** el método `set_motores` es llamado con valores positivos
- **THEN** el sistema envía registros I2C al PCA9685 estableciendo los PWM correctos en los pines definidos
- **AND** el rover avanza correspondientemente sin usar pines PWM del ESP32

## ADDED Requirements

### Requirement: Posicionamiento del Sistema de Percepción
El sistema DEBE permitir ajustar la orientación física del HC-SR04 mediante un servo.

#### Scenario: Giro paramétrico
- **WHEN** se solicita orientar el sonar a +45°
- **THEN** se transmite el cálculo de ciclo de trabajo al canal del PCA9685 designado para el servo, girando físicamente la montura
