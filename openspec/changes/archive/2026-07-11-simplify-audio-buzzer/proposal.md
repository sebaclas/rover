## Why

The current ESP32 rover's audio system uses an I2S DAC (MAX98357A), volume scaling algorithms, and WAV file playback. This setup is overly complex, consumes significant code space and RAM, and requires managing multiple WAV files on the flash storage. Simplifying the audio subsystem to a single GPIO buzzer will streamline the code, reduce resource usage, and still provide crucial audio feedback for status and alerts.

## What Changes

- **Buzzer Hardware Integration**: Configure a single GPIO (GPIO 16) to drive a buzzer, replacing the I2S DAC pins (GPIO 16, 17, 18).
- **Clean Audio/WAV Code**: Remove all I2S, WAV header parsing, volume scaling, and WAV playback code from `rover.py`.
- **Remove WAV Files**: Delete the WAV audio files (`welcome.wav`, `alert.wav`, `obstacle.wav`) from the filesystem.
- **Buzzer Beep Implementation**: Add a new asynchronous `beep` function to the `Rover` class using PWM to control frequency and duration.
- **Initialization Beep**: Sound a distinctive beep when the rover finishes its initialization (at the end of `main.py`).
- **Sonar Distance Alert**: Trigger a warning beep pattern when the ultrasonic sensor detects an obstacle at 5 cm or closer.
- **Clean UI & Web Server**: Remove wav playback and volume controls from `index.html` and `web_monitor.py`.

## Capabilities

### New Capabilities
- `buzzer-feedback`: Provision of simple audio tones/beeps via a GPIO-connected buzzer for initialization success and distance-based collision alerts.

### Modified Capabilities

## Impact

- **Affected Files**:
  - `rover.py`: Substantial code simplification (removal of I2S, volume scaling, WAV parsing). Addition of buzzer beep logic.
  - `main.py`: Replace WAV playback with a buzzer beep.
  - `web_monitor.py`: Remove `/play` and `/volume` HTTP routes and WebSocket handlers for WAV playback and volume control. Integrate the 5 cm distance alert check into the telemetry loop.
  - `index.html`: Remove UI elements for WAV player and volume control.
  - Files to delete: `welcome.wav`, `alert.wav`, `obstacle.wav`.
- **API Changes**: Remove HTTP routes `/play` and `/volume`. Remove `play` and `volume` keys from WebSocket messages.
- **Resource Usage**: Reduced flash storage (removal of WAV files) and reduced heap memory usage.
