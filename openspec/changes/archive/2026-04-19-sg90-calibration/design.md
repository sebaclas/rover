# SG90 Calibration Design

## Overview
Reemplazar los coeficientes matemáticos de la ecuación de ciclo de trabajo en `rover.py` para abrazar un rango "extendido" de señal PWM típico de los micro-servos.

## Architecture

### Matemáticas del SG90 en el PCA9685
- **Frecuencia Base:** `50 Hz` (El periodo de la onda PWM es de `20 ms`).
- **Resolución PCA9685:** `12 bits` (lo que da `4096` ciclos o pasos contables por periodo).
- **Fórmula de Duración a Cuentas:** `(duración_ms / 20.0 ms) * 4096 = Cuentas`

**Cálculo Extendido:**
1. `-90° (0.5 ms)` -> `(0.5 / 20) * 4096` = `102` cuentas.
2. `0° (1.5 ms)` -> `(1.5 / 20) * 4096` = `307` cuentas.
3. `+90° (2.5 ms)` -> `(2.5 / 20) * 4096` = `512` cuentas.

*Esto se traduce a un `duty_center` de 307 y un `duty_range` de `(512 - 307) = 205` cuentas.*

### Cambios a aplicar en rover.py
Se modificará `set_servo_angle` para reflejar el `duty_range = 205` y re-comentar la documentación interna.
