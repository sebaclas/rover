# buzzer-feedback Specification

## Purpose
TBD - created by archiving change simplify-audio-buzzer. Update Purpose after archive.
## Requirements
### Requirement: Inicialización de Buzzer en GPIO 16
El sistema MUST configurar un pin GPIO (GPIO 16) como salida para poder controlar el buzzer.

#### Scenario: Configuración de hardware
- **WHEN** se instancia la clase Rover
- **THEN** el sistema configura el pin GPIO 16 para control del buzzer utilizando PWM

### Requirement: Pitido de Inicialización
El sistema MUST emitir un pitido de confirmación una vez que el rover termine su secuencia de arranque.

#### Scenario: Alerta de sistema listo
- **WHEN** la secuencia de inicio en main.py finaliza con éxito
- **THEN** el rover hace sonar el buzzer con un pitido corto para notificar al usuario que está listo

### Requirement: Alerta por Distancia Crítica
El sistema MUST emitir un tono de alerta de proximidad cuando la lectura del sensor ultrasónico detecte que un obstáculo se encuentra a 5 centímetros de distancia.

#### Scenario: Detección de obstáculo muy cercano
- **WHEN** el sensor ultrasónico detecta un obstáculo a una distancia menor o igual a 5 centímetros (y mayor a 0)
- **THEN** el buzzer emite un patrón de tono de alerta

