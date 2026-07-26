## 1. Core Hardware Logic (`rover.py`)

- [x] 1.1 Implement dynamic obstacle deceleration ramp (`avanzar_distancia_suave`) with speed scaling from 80% at 50 cm down to 30% at 10 cm, and emergency stop/abort at <= 10 cm
- [x] 1.2 Update look-before-turn scan logic in `girar_grados` so detected turn obstructions cause the rover to advance 30 cm forward (with sonar front safety) and retry the turn scan
- [x] 1.3 Implement `ejecutar_secuencia(steps, calibration_speed)` asynchronous task loop with support for `FORWARD`, `BACKWARD`, `TURN_LEFT`, `TURN_RIGHT`, and `PAUSE`
- [x] 1.4 Add empirical calibration run method (5 seconds at 80% PWM)

## 2. Server Communication & Telemetry (`web_monitor.py`)

- [x] 2.1 Handle `EXECUTE_PROGRAM`, `ABORT_PROGRAM`, and `SET_CALIBRATION` WebSocket messages
- [x] 2.2 Add sequence execution progress state (`program_status`) to real-time WebSocket telemetry JSON payload

## 3. Web UI Controls (`index.html`)

- [x] 3.1 Build "Programador de Rutina" card with up to 5 programmable step rows (action selector and value input)
- [x] 3.2 Implement "▶ Ejecutar Secuencia" and "⏹ Abortar" buttons with live execution status display
- [x] 3.3 Add Speed Calibration UI field and 5s test run button

## 4. Verification & Testing

- [x] 4.1 Validate sequence execution, pause steps, smooth approach deceleration, turn re-scans, and manual/automatic aborts
