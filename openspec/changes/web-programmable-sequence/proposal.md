## Why

The Rover currently supports manual real-time driving commands and single 90-degree gyro-assisted turns. To enable autonomous navigation experiments, users need to program multi-step movement routines (e.g., advance X meters, turn, pause, advance, turn) directly from the Web interface. Additionally, forward movement requires adaptive slowdown when approaching obstacles and refined turning logic so the Rover advances past obstacle obstructions rather than reversing indefinitely.

## What Changes

- **Web Control Interface**: Add a programmable sequence builder (up to 5 steps, supporting Forward, Backward, Turn Left, Turn Right, and Pause commands).
- **Global & Per-Step Speed Control**: Allow configuring speed globally (e.g. 30% to 100% PWM) and overriding target speed individually for each movement step in the sequence.
- **Speed Calibration Constant**: Add a web-configurable speed calibration parameter (meters/sec at nominal PWM) with empirical calibration support (run 5s at nominal PWM).
- **Smooth Obstacle Approach**: Implement a deceleration speed ramp during forward movement starting at 50 cm down to 10 cm. The speed scales down from the step's nominal target speed to 30% PWM at 10 cm. Stop and abort sequence if an obstacle is within 10 cm.
- **Turn Obstacle Handling**: Update gyro turn routine so if a side obstacle is detected during look-before-turn, the Rover advances 30 cm forward and re-checks the turn path instead of reversing.
- **Async Execution Engine & Abort**: MicroPython execution loop for queued commands with real-time status reporting and instant stop/abort capabilities from web or sonar events.

## Capabilities

### New Capabilities
- `programmable-sequence`: Program, execute, monitor, and abort multi-step movement and pause routines with per-step and global speed controls.
- `smooth-obstacle-approach`: Dynamic motor speed deceleration between 50 cm and 10 cm sonar distance with 10 cm emergency stop.

### Modified Capabilities
- `safe-imu-turning`: Update turn obstruction behavior to advance 30 cm and re-scan instead of performing reverse evasion.
- `web-monitor`: Expose sequence builder, global and per-step speed controls, calibration controls, and execution status via Web UI and WebSocket messages.

## Impact

- `rover.py`: Add sequence execution engine, step/global speed parameter handling, distance estimation based on speed calibration constant, smooth speed ramp logic, and turn re-scan forward movement.
- `web_monitor.py`: Handle new WebSocket messages (`EXECUTE_PROGRAM`, `ABORT_PROGRAM`, `SET_CALIBRATION`, `SET_GLOBAL_SPEED`).
- `index.html`: UI for sequence builder with per-step speed controls, global speed slider, execution progress feedback, stop/abort button, and speed calibration input.
