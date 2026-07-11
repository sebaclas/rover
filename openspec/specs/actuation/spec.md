# Actuation (Motion Control)

## Overview
Handles the physical movement of the Rover and its sub-systems (servos, motors) using specialized PWM controllers to offload timing-critical tasks from the main CPU.

## Requirements

### Functional Requirements
- **Multi-channel PWM**: Control at least 16 channels of PWM with 12-bit resolution.
- **Motion Primitives**: Provide high-level commands like `move_forward()`, `rotate_left()`, `stop()`.
- **Speed Control**: Variable speed control for traction motors.
- **Servo Positioning**: Precise angular control for non-continuous servos.

### Technical Constraints
- **Hardware**: PCA9685 16-Channel I2C PWM Controller.
- **Communication**: I2C Bus (Pins TBD, usually standard I2C pins for ESP32-S3).
- **Default I2C Address**: `0x40`.
- **Operating Voltage**: 3.3V for logic, external power for high-current actuators (servos/motors).

## Integration Points
- **ESP32-S3 I2C**: Master controller.
- **Power System**: Must provide sufficient current for multiple servos/motors simultaneously.

## Definition of Done
- PCA9685 is successfully initialized and addressable via I2C.
- Individual PWM channels can be set to specific duty cycles.
- Basic movement commands result in expected physical action (when hardware is connected).

### Requirement: Control de Tracción y Dirección (Actualizado)
Se modifica la capa física del control; la implementación de las señales PWM DEBE realizarse a través del controlador PCA9685 por I2C, preservando el comportamiento externo de la interfaz.

#### Scenario: Comando de avance
- **WHEN** el método `set_motores` es llamado con valores positivos
- **THEN** el sistema envía registros I2C al PCA9685 estableciendo los ciclos de trabajo correctos
- **AND** el rover avanza correspondientemente sin usar pines PWM nativos del ESP32

### Requirement: Posicionamiento del Sistema de Percepción
El sistema DEBE permitir ajustar la orientación física del HC-SR04 mediante un servo, específicamente un SG90, de manera que logre un grado real de movimiento por cada grado numérico de consigna introducido.

#### Scenario: Giro de 180° calibrado
- **WHEN** el comando cambia de `-90°` a `+90°`
- **THEN** la señal de PWM viaja a través del rango de pulso de `0.5 ms` a `2.5 ms` (correspondiente a SG90/rango extendido)
- **AND** el cabezal del sonar realiza físicamente un barrido de semicírculo completo.
