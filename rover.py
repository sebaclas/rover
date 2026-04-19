import machine
import time
import neopixel
import pca9685

class Rover:
    def __init__(self):
        # Configuracion de pines segun especificaciones
        self.trigger = machine.Pin(9, machine.Pin.OUT)
        self.echo = machine.Pin(10, machine.Pin.IN)
        self.pixel = neopixel.NeoPixel(machine.Pin(48), 1)
        
        # Inicialización del bus I2C y PCA9685
        try:
            self.i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
            self.pca = pca9685.PCA9685(self.i2c, 0x40)
            self.pca.freq(50) # Frecuencia típica para control de servos y PWM motores
            self.pca_ready = True
            self.set_servo_angle(0) # Centrar servo al arrancar
            print("PCA9685 inicializado en I2C.")
        except Exception as e:
            print("Error inicializando PCA9685:", e)
            self.pca_ready = False

        # Estado inicial del LED (apagado)
        self.set_led(0, 0, 0)
        
    def set_led(self, r, g, b):
        """Controla el NeoPixel integrado (RGB)."""
        self.pixel[0] = (r, g, b)
        self.pixel.write()

    def medir_distancia(self):
        """Mide la distancia usando el HC-SR04 y devuelve cm."""
        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        
        try:
            # Timeout de 30ms (~5 metros)
            pulse_time = machine.time_pulse_us(self.echo, 1, 30000)
            if pulse_time > 0:
                distancia = (pulse_time * 0.0343) / 2
                return round(distancia, 2)
            else:
                return -1 # Fuera de rango o sin lectura
        except OSError:
            return -1

    def set_motores(self, izquierda, derecha):
        """
        Placeholder para control de motores via PCA9685.
        izquierda/derecha: -100 a 100
        """
        if not self.pca_ready:
            return

        def map_speed(speed):
            # Convierte 0-100% a PWM 0-4095
            return int(min(max(abs(speed) / 100.0, 0.0), 1.0) * 4095)
        
        # Canal 0: Motor Izquierdo, Canal 1: Motor Derecho
        # NOTA: Esto se adaptará cuando se defina si hay IN1/IN2/ENA por motor.
        self.pca.duty(0, map_speed(izquierda))
        self.pca.duty(1, map_speed(derecha))

    def set_servo_angle(self, angle):
        """
        Gira el servo del HC-SR04 al ángulo especificado (-90 a 90 grados).
        """
        if not self.pca_ready:
            return
            
        # Limitar ángulo de seguridad
        angle = max(-90, min(90, angle))
        
        # Para 50Hz (20ms periodo), 12-bits = 4096 pasos.
        # ~1ms (205) = -90 grados, ~1.5ms (307) = 0 grados, ~2ms (410) = 90 grados
        duty_center = 307
        duty_range = 102
        
        duty = int(duty_center + (angle / 90.0) * duty_range)
        self.pca.duty(4, duty) # Usamos el Canal 4 para el servo
