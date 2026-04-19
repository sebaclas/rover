import machine
import time
import neopixel

class Rover:
    def __init__(self):
        # Configuracion de pines segun especificaciones
        self.trigger = machine.Pin(9, machine.Pin.OUT)
        self.echo = machine.Pin(10, machine.Pin.IN)
        self.pixel = neopixel.NeoPixel(machine.Pin(48), 1)
        
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
        # TODO: Implementar I2C y PCA9685
        pass
