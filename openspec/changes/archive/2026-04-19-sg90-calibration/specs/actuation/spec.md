## MODIFIED Requirements
### Requirement: Posicionamiento del Sistema de Percepción
El sistema DEBE permitir ajustar la orientación física del HC-SR04 mediante un servo, específicamente un SG90, de manera que logre un grado real de movimiento por cada grado numérico de consigna introducido.

#### Scenario: Giro de 180° calibrado
- **WHEN** el comando cambia de `-90°` a `+90°`
- **THEN** la señal de PWM viaja a través del rango de pulso de `0.5 ms` a `2.5 ms` (correspondiente a SG90/rango extendido)
- **AND** el cabezal del sonar realiza físicamente un barrido de semicírculo completo.
