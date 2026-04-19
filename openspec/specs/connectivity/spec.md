# Connectivity

## Overview
The Rover must have robust network connectivity to allow remote control, telemetry monitoring, and video streaming. This capability handles WiFi connection management and eventually Bluetooth/BLE interactions.

## Requirements

### Functional Requirements
- **Automatic Connection**: The rover must automatically attempt to connect to a pre-configured WiFi network upon startup.
- **Connection Persistence**: The system must detect disconnections and attempt to reconnect automatically.
- **Static IP Support**: The network manager must allow configuring a static IP address to ensure a predictable endpoint for the control dashboard.
- **Connectivity Status**: Provide visual or programmatic feedback of the current connection status.
- **Internet Verification**: Capability to verify if the connection has actual internet access (e.g., via HTTP ping).

### Technical Constraints
- **Hardware**: ESP32-S3 (Xtensa LX7 dual-core).
- **Runtime**: MicroPython.
- **Protocol**: WiFi 802.11 b/g/n.

## Current Implementation
- `wifi_manager.py`: Handles WiFi connection, retries, and static IP configuration.
- `secrets.py`: Stores SSID, passwords, and static IP configuration (excluded from version control).

## Definition of Done
- Network connection is established within 30 seconds of boot.
- Disconnections are handled gracefully without requiring a hard reset.
- Connection parameters are easily configurable via `secrets.py`.
