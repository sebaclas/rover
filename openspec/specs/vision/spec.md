# Vision

## Overview
The "Eyes" of the Rover. This is handled by a dedicated ESP32-CAM unit to ensure that image processing and streaming do not interfere with the real-time navigation and motor control tasks on the main MCU.

## Requirements

### Functional Requirements
- **Real-time Streaming**: Provide a low-latency JPEG stream accessible via WiFi.
- **Capture Control**: Ability to take snapshots on demand.
- **Resolution Management**: Support scaling from QQVGA (low bandwidth) to UXGA (high resolution).
- **MCU Communication**: A communication channel (WiFi or UART) to synchronize vision events with navigation logic (e.g., "object detected by camera").

### Technical Constraints
- **Hardware**: ESP32-CAM (AI-Thinker or similar) with OV2640 sensor.
- **Power**: Dedicated 5V/3.3V supply (can be power-hungry during transmission).
- **Firmware**: Independent firmware (Arduino or ESP-IDF recommended for vision tasks).

## Integration Points
- **WiFi Network**: Shared with the main ESP32-S3.
- **UART (Optional)**: For hard-wired synchronization between S3 and CAM.

## Definition of Done
- A video stream is accessible via a browser on the same network.
- Frame rate is sufficient for remote navigation (at least 5-10 FPS at CIF resolution).
- Image quality allows for human-driven navigation.
