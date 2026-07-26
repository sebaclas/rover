## Context

The current rover codebase integrates I2S audio using a MAX98357A amplifier and WAV file playback. This is resource-intensive and overly complex for the current needs. We want to replace it with a simple GPIO buzzer that provides simple sound feedback (a startup completion sound and a distance-based obstacle warning).

## Goals / Non-Goals

**Goals:**
- Free up GPIO pins 17 and 18, and reuse GPIO 16 to drive the buzzer.
- Strip all I2S, WAV parsing, and volume control/scaling logic from `rover.py`.
- Add a new `beep(freq, duration_ms)` async function in `Rover` utilizing `machine.PWM` to generate simple beeps.
- Delete WAV audio files (`welcome.wav`, `alert.wav`, `obstacle.wav`).
- Implement a startup beep at the end of the initialization flow in `main.py`.
- Implement a distance-based alert sound in the sensor telemetry loop (`web_monitor.py`) when the measured distance is 5 cm or less.
- Clean up Web Monitor API endpoints (`/play`, `/volume`) and UI elements in `index.html`.

**Non-Goals:**
- Playing music, melodies, or polyphonic files.
- Keeping complex volume adjustment algorithms (buzzers typically only support simple frequency-based loudness, which is fixed at 50% PWM duty cycle).

## Decisions

- **GPIO Pin Choice**: GPIO 16 is chosen for the buzzer, since it was previously used for I2S LRC and is already exposed. GPIO 17 and 18 are completely freed.
- **Passive Buzzer Control via PWM**: We use `machine.PWM` with a 50% duty cycle (e.g., duty value 32768 in MicroPython) for driving the buzzer at specified frequencies (e.g., 2000Hz for high-pitch list-ok beep, and 800Hz/1000Hz for warning alerts).
- **Asynchronous non-blocking Beeps**: The `beep` method will be `async` and use `asyncio.sleep_ms` to avoid blocking other tasks like telemetry streaming or HTTP handlers.
- **Buzzer State Guard**: A boolean flag `buzzer_busy` will prevent concurrent beeps from colliding or overlapping, ensuring tones play sequentially.

## Risks / Trade-offs

- **[Risk] High-frequency distance telemetry could trigger too many warning beeps**
  → *Mitigation*: We will introduce a cooldown or a state check so that the 5 cm obstacle alarm only beeps once every few seconds, rather than beep constantly on every telemetry iteration (every 200ms).
- **[Risk] Web page breaks due to missing routes/WebSockets**
  → *Mitigation*: We will completely clean up the frontend UI elements and WebSocket listeners to prevent JS errors when trying to trigger WAV files.
