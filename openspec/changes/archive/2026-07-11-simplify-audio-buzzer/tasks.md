## 1. Clean Audio/WAV Code and Files

- [x] 1.1 Remove WAV audio files (`welcome.wav`, `alert.wav`, `obstacle.wav`) from the workspace
- [x] 1.2 Remove I2S setup, volume scaling, WAV parsing, and play_wav_async code from `rover.py`

## 2. Implement Buzzer Logic and Integration

- [x] 2.1 Implement `beep` method and buzzer hardware configuration (GPIO 16) in `rover.py`
- [x] 2.2 Add startup beep notification at the end of the initialization sequence in `main.py`
- [x] 2.3 Implement the 5 cm obstacle distance warning sound in the telemetry loop in `web_monitor.py`

## 3. Clean UI and Web Server

- [x] 3.1 Remove `/play` and `/volume` routes and WebSocket WAV command handlers in `web_monitor.py`
- [x] 3.2 Clean up index.html UI elements for audio player and volume control
