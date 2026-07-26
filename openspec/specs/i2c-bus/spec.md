# I2C Bus Specification

## Overview
El sistema DEBE proveer un bus I2C global, accesible para múltiples periféricos concurrentes. Dado que el ESP32-S3 posee flexibilidad en el ruteo de sus pines, se estandariza el uso del bus principal en pines fijos para no interferir con las operaciones o la flash.

## Requirements

### Requirement: Inicialización del bus central
El sistema DEBE inicializar un bus maestro I2C que quede a disposición para todos los dispositivos que compartan direcciones no conflictivas (por ejemplo, el driver PWM PCA9685).

#### Scenario: Configuración de pines correcta
- **WHEN** la aplicación principal (o Rover initialization) se inicia
- **THEN** se configura un bus I2C usando GPIO 4 para la trama de datos (SDA) y GPIO 5 para el reloj (SCL)
- **AND** el reloj opera a una velocidad típica de Fast Mode (aprox. 400kHz)

## Impacted Components
- `rover.py`: Centraliza su `self.i2c` para propagarlo a controladores de más bajo nivel.
- Todo periférico (`pca9685`, IMUs en el futuro, expansores de I/O) consumirá esta referencia.
