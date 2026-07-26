# safe-imu-turning Specification

## Purpose
TBD - created by archiving change safe-imu-turning. Update Purpose after archive.
## Requirements
### Requirement: Integración del Driver DRV8833 en PCA9685
El sistema SHALL mapear el puente H DRV8833 utilizando dos canales PWM independientes del PCA9685 para el motor izquierdo (IN1, IN2) y dos canales para el motor derecho (IN3, IN4). El sistema SHALL permitir definir la velocidad y sentido mediante modulación de ancho de pulso en un canal mientras el canal opuesto permanece en 0 (LOW), y SHALL soportar freno activo configurando ambos canales del motor en HIGH (4095).

#### Scenario: Control de velocidad hacia adelante
- **WHEN** se solicita mover el motor izquierdo hacia adelante con velocidad de 80%
- **THEN** el sistema configura el canal IN1 del motor izquierdo con un duty cycle de 3276 y el canal IN2 en 0

#### Scenario: Freno activo de motores
- **WHEN** se solicita detener el rover aplicando el freno activo
- **THEN** el sistema configura los canales IN1, IN2, IN3 e IN4 del PCA9685 a un valor fijo de 4095

### Requirement: Lazo de Giro Preciso por IMU
El sistema SHALL calibrar dinámicamente el sesgo (offset) estático del giroscopio en el eje Z inmediatamente antes de encender los motores, y SHALL integrar la velocidad angular corregida a una tasa de muestreo mínima de 50Hz (cada 20ms) hasta alcanzar el ángulo de giro solicitado.

#### Scenario: Giro preciso completado
- **WHEN** la integración del ángulo corregido del giroscopio alcanza o supera en valor absoluto el objetivo solicitado
- **THEN** el sistema interrumpe el lazo de integración y detiene los motores aplicando freno activo

### Requirement: Escaneo Preventivo del Sonar (Look-Before-Turn)
El sistema SHALL posicionar el servo del sonar hacia el extremo del giro solicitado (ej. +90° o -90°) antes de arrancar los motores de tracción, evaluar si el espacio está libre y regresar el servo al centro antes de iniciar la rotación física del chasis.

#### Scenario: Trayectoria de giro obstruida
- **WHEN** el sonar detecta una distancia menor o igual a 15 cm en el ángulo de pre-giro
- **THEN** el sistema detiene la maniobra de giro, regresa el servo al centro, retrocede el rover una distancia fija por tiempo equivalente a 10 cm y reinicia la secuencia de giro completa

#### Scenario: Trayectoria de giro libre
- **WHEN** el sonar detecta una distancia superior a 15 cm en el ángulo de pre-giro
- **THEN** el sistema regresa el servo al centro, espera a que se estabilice física y mecánicamente, y arranca los motores para girar el rover

### Requirement: Detección y Evasión Activa de Obstáculos Durante el Giro
El sistema SHALL monitorear activamente la distancia frontal utilizando el sonar (con el servo centrado a 0°) durante la rotación física de las ruedas para prevenir colisiones laterales debidas al barrido físico del rover.

#### Scenario: Detección de obstáculo a mitad del giro
- **WHEN** el rover está girando físicamente y el sonar frontal registra una distancia menor o igual a 10 cm
- **THEN** el sistema detiene inmediatamente los motores, retrocede 10 cm por tiempo y reintenta el giro completo desde el inicio del escaneo preventivo

