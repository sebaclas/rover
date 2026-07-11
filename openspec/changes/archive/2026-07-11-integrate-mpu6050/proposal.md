## Why

El rover necesita medir su aceleración lineal y velocidad angular para conocer su estado de movimiento físico. El MPU-6050 es un sensor IMU (Acelerómetro + Giroscopio) de bajo costo conectado por I2C que permite capturar estos datos físicos y enviarlos en tiempo real a la interfaz web para propósitos de monitoreo, telemetría y diagnósticos, sin interferir con la lógica de actuación de motores del rover en esta etapa.

## What Changes

- **Integración de Driver MPU-6050**: Incorporar un módulo de software liviano para MicroPython que se comunique con el MPU-6050 a través de I2C.
- **Inicialización del Sensor**: Inicializar el sensor en el bus I2C global en la dirección predeterminada `0x68` (usando pines SDA: GPIO 4, SCL: GPIO 5).
- **Lectura de Sensores**: Lectura periódica de aceleración en 3 ejes (x, y, z), giroscopio en 3 ejes (x, y, z) y temperatura interna del sensor.
- **Telemetría WebSocket**: Envío de los datos estructurados en formato JSON a través del WebSocket de telemetría existente.
- **Visualización en Dashboard**: Actualizar la interfaz de usuario web (`index.html`) para mostrar dinámicamente las lecturas numéricas y gráficas de aceleración y rotación.

## Capabilities

### New Capabilities
- `mpu6050-telemetry`: Lectura de aceleración en 3 ejes, velocidad angular en 3 ejes y temperatura del sensor MPU-6050, y transmisión periódica de estos datos a través del WebSocket para su visualización gráfica en el dashboard web.

### Modified Capabilities
<!-- Dejamos vacío ya que no altera los requerimientos funcionales del sonar ni del control de motores. -->

## Impact

- `rover.py`: Adición de soporte para inicializar el MPU-6050 compartiendo el bus I2C y provisión de métodos no bloqueantes para recuperar las lecturas.
- `web_monitor.py`: Adición del envío de datos del acelerómetro y giroscopio en el bucle principal del WebSocket.
- `index.html`: Adición de componentes visuales en la interfaz gráfica para renderizar la telemetría del acelerómetro (e.g. orientación, inclinación o valores numéricos y barras de estado).
- `mpu6050.py`: Creación de un driver ligero para el sensor MPU-6050.
