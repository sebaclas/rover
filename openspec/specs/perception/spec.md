# Perception (Obstacle Detection)

## Overview
The Rover uses a "Scanning Sonar" system to perceive its surroundings. This consists of an ultrasonic sensor mounted on a servo motor to perform angular sweeps and detect obstacles without moving the entire chassis.

## Requirements

### Functional Requirements
- **Distance Measurement**: Measure distance to objects in front of the sensor with a range of 2 cm to 400 cm.
- **Scanning Sweep**: Rotate the sensor within a range of at least ±90° relative to the front axis to build a local map of obstacles.
- **Obstacle Alert**: Threshold-based detection to trigger navigation interventions.

### Technical Constraints
- **Hardware**: HC-SR04 Ultrasonic Sensor + Standard Servo.
- **Pins (ESP32-S3)**:
    - `GPIO 9`: TRIG (Output)
    - `GPIO 10`: ECHO (Input) - *Requires level shifter or voltage divider (3.3V logic).*
- **Servo Control**: Must be controlled via the PCA9685 PWM controller (I2C) to preserve ESP32 GPIOs and ensure smooth movement.

## Integration Points
- **I2C Bus**: Connects to PCA9685 for servo movement.
- **GPIO**: Direct pulse-width measurement for the HC-SR04.

## Definition of Done
- Sensor returns accurate distance readings (±10% error margin).
- Servo can position the sensor at specific angles (0°, 45°, 90°, etc.) reliably.
- Scanning logic can detect an obstacle and report its distance and relative angle.
