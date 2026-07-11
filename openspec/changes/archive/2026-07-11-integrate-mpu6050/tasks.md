## 1. Driver MPU-6050

- [x] 1.1 Crear e implementar el archivo driver `mpu6050.py` en MicroPython
- [x] 1.2 Probar de manera aislada que el sensor es detectable en el bus I2C (dirección 0x68) y responde correctamente a las lecturas de los registros utilizando un script de prueba

## 2. Integración en el Rover y Telemetría

- [x] 2.1 Modificar `rover.py` para inicializar la instancia de MPU-6050 usando el bus I2C global, agregando control de errores para evitar fallos si el sensor no está conectado
- [x] 2.2 Modificar `web_monitor.py` para leer los valores de aceleración, giroscopio y temperatura, e incluirlos en el mensaje JSON periódico del WebSocket

## 3. Visualización en Interfaz Web

- [x] 3.1 Modificar `index.html` para añadir un panel visual dedicado a la telemetría del MPU-6050
- [x] 3.2 Implementar en `index.html` lógica de javascript para recibir, procesar y representar gráficamente las lecturas en tiempo real (acelerómetro y giroscopio) de forma fluida
- [x] 3.3 Rediseñar la tarjeta visual de IMU en `index.html` para que sea vertical, con ejes X (positivo adelante/arriba) e Y (positivo a la derecha) e inclinación 3D coherente
