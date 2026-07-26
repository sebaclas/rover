## Context

The Rover is an ESP32-S3 MicroPython rover with PCA9685 motor drivers, an ultrasonic sensor (Trig/Echo), an MPU-6050 IMU, and a Microdot Web Server with WebSockets.
Currently, navigation commands are sent step-by-step from manual controls or single 90° turns.
This design introduces:
1. Web-based multi-step sequence programming (up to 5 steps, with Forward, Backward, Turn Left, Turn Right, and Pause) with both global speed control and individual per-step speed override.
2. Dynamic speed control using a deceleration ramp (50 cm down to 10 cm sonar distance) to smoothly approach obstacles from step target speed down to 30% PWM, aborting when distance <= 10 cm.
3. Speed calibration constant configuration to convert meters into execution time based on nominal speed.
4. Turn obstruction evasion update: Advance 30 cm forward and re-scan the turn direction until clear, rather than reversing.

## Goals / Non-Goals

**Goals:**
- Allow users to build, send, execute, and monitor 5-step movement sequences via WebSockets.
- Support global speed setting (default 80%, range 30-100%) and optional per-step speed override in the program sequence builder.
- Implement smooth forward deceleration starting at 50 cm down to 10 cm (scaling from step target speed down to 30% PWM), followed by stopping and aborting if obstacle is within 10 cm.
- Update turn obstruction handling: move forward 30 cm and retry scanning when the turn angle path is blocked (<= 15 cm).
- Provide web UI for empirical speed calibration (meters/sec at nominal PWM) and storing the setting in memory.
- Provide a `PAUSE` command in seconds.

**Non-Goals:**
- Wheel encoder hardware integration (speed estimation remains open-loop timed using the empirical calibration constant).
- Complex path planning or SLAM algorithms (simple sequential execution with safety aborts).

## Decisions

### Decision 1: Sequence Execution Engine & Per-Step/Global Speed Control (`Rover.ejecutar_secuencia`)
- Implement an `async` task `ejecutar_secuencia(steps, calibration_speed, global_speed_pct)` on `Rover`.
- Step payload format: `{"action": "FORWARD", "val": 2.0, "speed": 90}`. If `speed` is not specified for a step, fallback to `global_speed_pct` (default 80%).
- Each step evaluates the action type:
  - `FORWARD`: Run motors with dynamic sonar monitoring loop at 50Hz (20ms).
    - `dist > 50 cm`: Speed = step target speed (`target_speed`).
    - `10 cm < dist <= 50 cm`: Speed scales linearly from `target_speed` down to 30% PWM (`speed = 30 + (target_speed - 30) * ((dist - 10) / (50 - 10))`).
    - `dist <= 10 cm`: Stop motors (`brake=True`), play beep, abort sequence.
  - `BACKWARD`: Run motors reverse at `target_speed` PWM for estimated time based on distance.
  - `TURN_LEFT` / `TURN_RIGHT`: Gyro-assisted turn at turning speed. If look-before-turn scan detects obstacle <= 15 cm, advance forward 30 cm (monitored for obstacles), center servo, and re-run look-before-turn until clear.
  - `PAUSE`: `await asyncio.sleep(value_seconds)`.

*Alternative considered*: Blocking thread per step. Rejected because MicroPython requires `uasyncio` cooperative multitasking to maintain active WebSocket telemetry and web server responsiveness.

### Decision 2: WebSocket Protocol Expansion
- Expand `telemetry` WebSocket message handling in `web_monitor.py`:
  - `{"command": "EXECUTE_PROGRAM", "steps": [{"action":"FORWARD","val":2.0,"speed":90},...], "global_speed": 80, "speed_m_s": 0.35}`
  - `{"command": "ABORT_PROGRAM"}`
  - `{"command": "SET_CALIBRATION", "speed_m_s": 0.35}`
  - `{"command": "SET_GLOBAL_SPEED", "global_speed": 80}`
- Send execution state updates in telemetry broadcasts:
  - `{"program_status": {"running": true, "current_step": 2, "total_steps": 4, "action": "FORWARD", "speed": 90, "message": "Ejecutando paso 2/4 (90% Vel)..."}}`

### Decision 3: Web UI Component Architecture
- Add a "Programador de Rutina" card in `index.html`.
- Global speed slider (30% to 100%, default 80%).
- Allow adding up to 5 step rows. Row fields: Action selector (`Avanzar`, `Retroceder`, `Girar Izq 90°`, `Girar Der 90°`, `Pausa`), Value input (Meters, Degrees, or Seconds), and optional Speed selector (% PWM, default: Auto/Global).
- Add "▶ Ejecutar Secuencia" and "⏹ Abortar" buttons.
- Add "Velocidad Calibrada (m/s)" input field and a "Prueba de Calibración (5s a 80%)" button to run the rover for 5s while measuring actual distance for the user to calculate exact speed.

## Risks / Trade-offs

- **[Wheel Slippage & Open-Loop Drift at variable speeds]** → Time estimation scales linearly with speed (`time = (dist / speed_m_s) * (80 / target_speed)`).
  *Mitigation*: The user can tune `speed_m_s` and speed % per step for different floor surfaces.
- **[Obstacle detection during 30 cm turn retry]** → Advancing 30 cm to clear a turn obstruction might hit an obstacle in front.
  *Mitigation*: Front sonar obstacle detection remains active during the 30 cm advance; if something is within 10 cm, the rover stops and aborts immediately.

## Migration Plan

1. Update `rover.py` with `avanzar_distancia_suave`, updated `girar_grados`, and `ejecutar_secuencia` accepting step and global speeds.
2. Update `web_monitor.py` WebSocket handler for sequence control messages and state feedback.
3. Update `index.html` with sequence builder UI, per-step and global speed controls, calibration inputs, and progress indicators.
4. Verify on hardware/browser.
