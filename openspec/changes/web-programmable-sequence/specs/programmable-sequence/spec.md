## ADDED Requirements

### Requirement: Carga y Ejecución de Secuencia Programada
El sistema SHALL permitir la recepción, decodificación y ejecución secuencial asíncrona de una lista de hasta 5 comandos de navegación (Avanzar, Retroceder, Girar Izquierda, Girar Derecha, Pausa) enviados desde la interfaz Web, soportando control de velocidad global y por paso.

#### Scenario: Recepción y ejecución exitosa de programa con velocidades personalizadas
- **WHEN** se recibe un mensaje WebSocket con el comando `EXECUTE_PROGRAM` conteniendo pasos con valores de velocidad individual y velocidad global por defecto
- **THEN** el sistema ejecuta ordenadamente cada paso aplicando la velocidad configurada para dicho paso (o la velocidad global si no se especifica), notificando el avance vía telemetría

#### Scenario: Ejecución del comando de Pausa
- **WHEN** un paso de la secuencia indica la acción `PAUSE` con un valor en segundos
- **THEN** el sistema detiene la marcha de los motores y aguarda de forma asíncrona el tiempo especificado antes de continuar con el siguiente paso

### Requirement: Aborto Manual y Automático de la Secuencia
El sistema SHALL abortar inmediatamente la ejecución de la secuencia programada y detener los motores si se recibe un comando de interrupción desde la web o si un sensor de seguridad reporta un evento de parada.

#### Scenario: Aborto enviado por el usuario
- **WHEN** el usuario presiona el botón de abortar en la web durante la ejecución de un programa
- **THEN** el sistema detiene inmediatamente los motores, cancela la tarea asíncrona en curso y emite el estado de secuencia abortada

### Requirement: Calibración Empírica de Velocidad
El sistema SHALL permitir ajustar la constante de velocidad lineal (metros por segundo) utilizada para convertir distancias en metros a tiempo de encendido de motores a potencia nominal.

#### Scenario: Ajuste de constante de calibración
- **WHEN** se recibe una actualización del parámetro de velocidad calibrada en m/s desde la web
- **THEN** el sistema actualiza la constante global utilizada para los cálculos de tiempo de desplazamiento en futuros comandos
