## Why
El rango físico de giro de 180° del servo que mueve el sensor ultrasónico (modelo SG90) requiere un ancho de pulso PWM de 0.5 ms a 2.5 ms ("rango extendido"). La implementación actual utiliza un pulso estándar de 1.0 ms a 2.0 ms, que solo resulta en un giro efectivo de ~90° en total (de -45° a +45°). Se necesita ajustar esta calibración matemática. Además, las especificaciones actuales no mencionaban el modelo de hardware, por lo que es vital documentar que la cinemática está basada en el SG90.

## What Changes
* **Documentación (Specs)**: Se especificará formalmente la dependencia del hardware al modelo Servo SG90.
* **Controlador (Backend)**: Se actualizará el cálculo en la función `set_servo_angle` de `rover.py` para mapear el intervalo de ángulos [-90, 90] a un rango de pulsos de [0.5 ms, 2.5 ms] equivalente a [102, 512] unidades lógicas del registro de 12 bits para una señal a 50Hz.

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- `actuation`: Calibración de rango PWM extendido.

## Impact
* **rover.py**: Ajuste estricto en la matemática de `set_servo_angle`.
* **Rover_Especificaciones_v0.1.md**: Adición del componente SG90 a la lista de actuadores.
