# PCA9685 PWM Integration Design

## Overview
This feature integrates the PCA9685 16-channel PWM controller over I2C. The goal is to offload actuation (traction and servo positioning) from the ESP32-S3's native PWM channels.

## Architecture

1.  **I2C Initialization**:
    *   A single I2C bus will be created at startup in `main.py` or within `Rover.__init__`, configuring `SDA = Pin(4)` and `SCL = Pin(5)`.
2.  **PCA9685 Driver**:
    *   A new file, `pca9685.py`, will be added implementing the standard I2C register interface for this chip (or reusing an existing MicroPython driver like `machine.I2C` standard combined with `pca9685` library).
3.  **Actuation via Rover Class**:
    *   The `Rover` class in `rover.py` will initialize the PCA9685 module using the common I2C bus.
    *   `set_motores` will be refactored to send duty cycle commands to the specific PCA9685 channels assigned to traction (e.g., Channels 0..3).
    *   A new method `set_servo_angle` will be added to control the ultrasonic sensor rotation on a specific PWM channel (e.g., Channel 4).

## Data Model / State Changes

*   **No local state storage**: Actuation control remains stateless, sending commands directly to the PCA9685 registers over I2C.

## API Changes

*   `Rover.__init__()`: Internally initializes I2C and PCA9685.
*   `Rover.set_motores(izq, der)`: Maintains current signature but updates the internal implementation to use I2C.
*   `Rover.set_servo_angle(angle)`: **[NEW]** Controls the servo direction from -90° to 90°.

## System Requirements & Scaling

*   **Latency**: The I2C bus will operate at 400kHz (Fast Mode), keeping latency negligible.
*   **Safety**: If an invalid angle or duty cycle is provided, it should be clamped to valid hardware limits.
