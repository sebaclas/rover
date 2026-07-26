## Context

El rover cuenta con una placa ESP32-S3, un driver de servos/motores PCA9685 y un sensor MPU-6050. Se planea incorporar un puente H DRV8833 para controlar dos motores DC de tracción trasera. Para habilitar giros autónomos controlados por giroscopio manteniendo la seguridad ante colisiones, se diseñará un módulo de control asíncrono que integre el sonar HC-SR04 y el MPU-6050.

## Goals / Non-Goals

**Goals:**
*   Implementar el driver de control de velocidad para el puente H DRV8833 utilizando 2 canales PWM independientes del PCA9685 por motor.
*   Diseñar un flujo asíncrono (`uasyncio`) de giro controlado por giroscopio (eje Z) con tolerancia a offsets ("Zero-Rate Calibration" al vuelo).
*   Integrar escaneo preventivo por sonar apuntando el servo hacia la trayectoria del giro antes de iniciar el movimiento.
*   Establecer un lazo de monitoreo constante del sonar durante el giro físico del chasis y una lógica de evasión por retroceso temporizado.

**Non-Goals:**
*   Control en lazo cerrado para distancias lineales (no se dispone de encoders en rueda).
*   Control proporcional de velocidad durante el giro (se usará control por umbral simple On/Off inicial).

## Decisions

### 1. Control de Motores (DRV8833 a PCA9685)
Se mapearán las entradas del DRV8833 a los canales 0, 1 (Motor Izquierdo) y 2, 3 (Motor Derecho) del PCA9685.
*   **Avanzar Izquierda**: Canal 0 = PWM, Canal 1 = 0
*   **Retroceder Izquierda**: Canal 0 = 0, Canal 1 = PWM
*   **Frenar Izquierda**: Canal 0 = 4095, Canal 1 = 4095 (Freno activo rápido para detención precisa)
*   *Alternativas*: Controlar la dirección por GPIOs directos del ESP32. Se descarta para simplificar el cableado físico y preservar pines GPIO del microcontrolador.

### 2. Calibración del Giroscopio
Antes de encender los motores para un giro, se tomará una ráfaga de 10 lecturas rápidas del giroscopio (50ms totales) para calcular el offset instantáneo de la guiñada (eje Z). Este offset se restará dinámicamente durante el lazo de integración del giro.
*   *Alternativas*: Guardar offsets en archivos flash. Se descarta debido a que los offsets cambian con la temperatura de funcionamiento y el envejecimiento del sensor.

### 3. Concurrencia y Prioridad del Sonar
El lazo de control del giro correrá a 50Hz (muestreo cada 20ms) usando `await asyncio.sleep_ms(20)`. Esto permitirá que la tarea de telemetría y el sonar sigan funcionando en paralelo.
*   El sonar frontal (con el servo centrado a 0°) medirá distancias de forma continua. Si en cualquier momento del giro físico la distancia leída es $\le 10\text{ cm}$, se aborta la tarea de rotación, se frena el rover y se ejecuta la evasión.

## Risks / Trade-offs

*   **[Riesgo] Deriva de integración si la tasa de muestreo fluctúa**
    *   *Mitigación*: Se calculará la diferencia de tiempo real (`dt` usando `time.ticks_us()`) entre iteraciones en lugar de asumir un intervalo de tiempo fijo de 20ms.
*   **[Riesgo] Imprecisión en el retroceso por falta de encoders**
    *   *Mitigación*: La distancia de evasión (10cm) se aproximará con un retroceso a velocidad controlada (ej. 40%) por un tiempo fijo experimental (ej. 600ms), calibrado empíricamente.
*   **[Riesgo] El rover arranca el giro sobre una superficie con vibración intensa**
    *   *Mitigación*: La calibración rápida se limitará a descartar sesgos moderados. Si el offset de Z excede los $\pm 15^\circ/\text{s}$, se registrará una advertencia y se utilizará un offset de seguridad de 0.
