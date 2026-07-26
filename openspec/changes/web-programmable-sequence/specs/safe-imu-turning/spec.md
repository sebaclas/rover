## MODIFIED Requirements

### Requirement: Escaneo Preventivo del Sonar (Look-Before-Turn)
El sistema SHALL posicionar el servo del sonar hacia el extremo del giro solicitado (ej. +85° o -85°) antes de arrancar los motores de tracción, evaluar si el espacio está libre y regresar el servo al centro antes de iniciar la rotación física del chasis.

#### Scenario: Trayectoria de giro obstruida
- **WHEN** el sonar detecta una distancia menor o igual a 15 cm en el ángulo de pre-giro
- **THEN** el sistema regresa el servo al centro, avanza el rover 30 cm hacia adelante monitoreando obstáculos frontales, y vuelve a realizar el escaneo de pre-giro en la misma dirección hasta encontrar la trayectoria libre

#### Scenario: Trayectoria de giro libre
- **WHEN** el sonar detecta una distancia superior a 15 cm en el ángulo de pre-giro
- **THEN** el sistema regresa el servo al centro, espera a que se estabilice física y mecánicamente, y arranca los motores para girar el rover
