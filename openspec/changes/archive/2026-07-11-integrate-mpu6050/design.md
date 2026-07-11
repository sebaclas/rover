## Context

El ESP32-S3 del rover tiene inicializado un bus I2C global (usando `GPIO 4` para SDA y `GPIO 5` para SCL). Actualmente, este bus es compartido por el driver PWM PCA9685 y la pantalla OLED SSD1306. Agregaremos el acelerómetro/giroscopio MPU-6050 a este mismo bus en su dirección predeterminada (`0x68`). Los datos recopilados por el sensor se enviarán a través del servidor Microdot WebSocket al dashboard para su visualización.

## Goals / Non-Goals

**Goals:**
- Implementar o incorporar un driver minimalista y eficiente en MicroPython para el MPU-6050.
- Inicializar el MPU-6050 de forma segura en `rover.py` compartiendo el bus `self.i2c` existente.
- Leer datos de aceleración de 3 ejes, velocidad angular de 3 ejes y temperatura interna.
- Transmitir estos datos periódicamente en formato JSON en el handler del WebSocket en `web_monitor.py`.
- Diseñar y actualizar la interfaz de usuario en `index.html` para mostrar los datos de telemetría de forma premium (mediante barras indicadoras, giros o animaciones sutiles).

**Non-Goals:**
- Utilizar los datos del sensor para control de bucle cerrado (como auto-balanceo o corrección de rumbo de motores) en esta etapa.
- Almacenar históricos de telemetría localmente en la memoria flash del ESP32.
- Utilizar bibliotecas 3D pesadas (como Three.js) en el navegador; usaremos transformaciones CSS 3D nativas o elementos Canvas livianos para renderizar la inclinación/orientación física de manera fluida.

## Decisions

- **Driver Integrado**: Crearemos un archivo `mpu6050.py` con una clase minimalista de MicroPython que realice lecturas de memoria directas (`readfrom_mem`) de los registros del MPU-6050 (`0x3B` al `0x48`) para minimizar el uso de memoria RAM y almacenamiento.
- **Tasa de Refresco Ajustada**: La telemetría se consultará y enviará a una frecuencia de 5Hz a 10Hz (intervalo de 100ms - 200ms) dentro del bucle del WebSocket. Esto proporciona una respuesta visual fluida en el navegador sin sobrecargar la CPU del ESP32.
- **Manejo de Errores en I2C**: Las lecturas del sensor se encapsularán en bloques `try/except`. Si el sensor experimenta ruido eléctrico o desconexión temporal debido a los motores, la aplicación omitirá la lectura actual en lugar de detenerse o entrar en pánico.

## Risks / Trade-offs

- **Ruido Eléctrico en I2C**: Los motores de corriente continua pueden introducir ruido en el bus I2C y provocar fallos en las lecturas del MPU-6050.
  - *Mitigación*: Las lecturas fallidas se ignoran silenciosamente o devuelven valores por defecto. Si el error persiste durante múltiples lecturas consecutivas, se marca el sensor como no disponible sin afectar la estabilidad del sistema.
- **Sobrecarga de WebSocket**: Enviar telemetría de alta frecuencia puede aumentar la latencia del control de dirección del rover.
  - *Mitigación*: Empaquetar la telemetría del sonar y la del MPU-6050 en un único mensaje WebSocket periódico (e.g. cada 200ms) y priorizar los comandos entrantes del usuario.
