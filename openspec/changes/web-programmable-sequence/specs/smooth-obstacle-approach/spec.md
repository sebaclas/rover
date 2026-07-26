## ADDED Requirements

### Requirement: Desaceleración Proporcional por Aproximación a Obstáculos
El sistema SHALL monitorear la distancia frontal provista por el sensor ultrasónico durante los desplazamientos hacia adelante y reducir gradualmente la velocidad del motor cuando la distancia sea menor o igual a 50 cm.

#### Scenario: Rampa de desaceleración activa
- **WHEN** el rover avanza y el sonar detecta un obstáculo a una distancia entre 10 cm y 50 cm
- **THEN** el sistema ajusta la potencia PWM de los motores de forma proporcional a la distancia, desacelerando suavemente desde 80% (en 50 cm) hasta 30% (en 10 cm)

### Requirement: Parada de Emergencia y Aborto a 10 cm
El sistema SHALL detener inmediatamente la marcha aplicando freno activo e interrumpiendo cualquier secuencia programada cuando la distancia detectada por el sonar sea menor o igual a 10 cm.

#### Scenario: Obstáculo detectado a 10 cm o menos
- **WHEN** la distancia medida por el sonar cae a 10 cm o menos mientras el rover avanza
- **THEN** el sistema detiene los motores aplicando freno activo, emite un pitido de advertencia y aborta la secuencia de movimiento
