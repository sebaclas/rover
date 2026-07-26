## Why

El rover necesita controlar múltiples actuadores (como los motores de tracción y el servo del sensor ultrasónico). El ESP32-S3 tiene capacidades PWM integradas, pero usar un controlador I2C PCA9685 de 16 canales descarga al microcontrolador de esta tarea, ofreciendo mayor precisión y escalabilidad a futuro además de ahorrar pines GPIO valiosos. Además, requerimos inicializar el bus I2C usando pines seguros (GPIO 4 para SDA y GPIO 5 para SCL) que no interfieran con el arranque o los sensores existentes.

## What Changes

* Integración de bus I2C usando GPIO 4 (SDA) y GPIO 5 (SCL).
* Configuración de la abstracción de hardware para comunicarse con el módulo PCA9685 (dirección base 0x40).
* Reemplazo de los métodos de control de tracción a través de I2C en lugar de pines directos.
* Creación e incorporación de la lógica de posicionamiento del servo, asociada al sensor HC-SR04, usando el mismo bus.

## Capabilities

### New Capabilities
- `i2c-bus`: Manejo global del bus I2C para dispositivos y periféricos compartidos.

### Modified Capabilities
- `actuation`: Se modifican los requisitos de tracción y posicionamiento (ahora dependerán de la interfaz I2C a través del PCA9685 en vez de pines PWM nativos del ESP32).

## Impact

* **Hardware**: Se deben realizar conexiones I2C desde la shield base hacia el controlador PCA9685.
* **Firmware**: Se requiere integrar una librería para PCA9685 en MicroPython y actualizar `rover.py` o módulo equivalente para que los motores envíen señales por I2C.
* **Software**: No debería impactar en `web_monitor.py` ya que `rover.set_motores` abstraerá la complejidad por debajo, respetando la misma interfaz.
