# Tasks

- [x] Incorporar el archivo `pca9685.py` al sistema (puede requerir adaptación de la librería de I2C/PCA9685 para uPython).
- [x] En `/rover.py` inicializar `machine.I2C` en los pines 4 y 5.
- [x] Construir la instancia de `PCA9685` pasándole el bus I2C creado.
- [x] En `/rover.py`, implementar el control interno de `set_motores` comunicándose con el objeto `pca9685`.
- [x] En `/rover.py`, agregar un nuevo método `set_servo_angle` (e.g. `set_servo_angle(0)`) y la lógica de ciclo de trabajo en el `pca9685`.
- [x] Modificar `main.py` si es necesario para llamar a la inicialización correcta o exponer el control del servo en el monitor web.
