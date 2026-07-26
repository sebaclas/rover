## ADDED Requirements

### Requirement: Panel de Programación de Secuencia en la Web
El sistema SHALL proveer un panel de control en la interfaz Web para construir, enviar y monitorear secuencias de movimiento de hasta 5 pasos con selectores de velocidad por paso, deslizador de velocidad global, y botones de ejecución y aborto inmediato.

#### Scenario: Construcción e inicio de secuencia desde la Web
- **WHEN** el usuario configura los pasos de la secuencia, ajusta las velocidades global o individuales en la interfaz web y presiona "Ejecutar Secuencia"
- **THEN** la interfaz valida los datos, los envía vía WebSocket en formato JSON y actualiza el indicador visual mostrando el paso y la velocidad en ejecución

### Requirement: Panel de Calibración de Velocidad
El sistema SHALL permitir al usuario realizar una prueba empírica de avance de 5 segundos a potencia nominal y actualizar la constante de velocidad en metros por segundo.

#### Scenario: Ejecución de prueba de calibración
- **WHEN** el usuario presiona el botón de prueba de calibración en la interfaz web
- **THEN** el rover avanza durante 5 segundos exactos a la velocidad nominal para permitir la medición manual de distancia
