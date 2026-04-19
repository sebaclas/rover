# Actuation (Motion Control)

## Overview
Handles the physical movement of the Rover and its sub-systems (servos, motors) using specialized PWM controllers to offload timing-critical tasks from the main CPU.

## Requirements

### Functional Requirements
- **Multi-channel PWM**: Control at least 16 channels of PWM with 12-bit resolution.
- **Motion Primitives**: Provide high-level commands like `move_forward()`, `rotate_left()`, `stop()`.
- **Speed Control**: Variable speed control for traction motors.
- **Servo Positioning**: Precise angular control for non-continuous servos.

### Technical Constraints
- **Hardware**: PCA9685 16-Channel I2C PWM Controller.
- **Communication**: I2C Bus (Pins TBD, usually standard I2C pins for ESP32-S3).
- **Default I2C Address**: `0x40`.
- **Operating Voltage**: 3.3V for logic, external power for high-current actuators (servos/motors).

## Integration Points
- **ESP32-S3 I2C**: Master controller.
- **Power System**: Must provide sufficient current for multiple servos/motors simultaneously.

## Definition of Done
- PCA9685 is successfully initialized and addressable via I2C.
- Individual PWM channels can be set to specific duty cycles.
- Basic movement commands result in expected physical action (when hardware is connected).
