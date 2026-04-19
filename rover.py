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
        # --- SIMULACION PARA PRUEBAS ---
        import math
        # Generar una distancia que fluctúa entre 10 y 190 cm usando el tiempo
        sim_dist = 100 + 90 * math.sin(time.ticks_ms() / 1000)
        return round(sim_dist, 2)
        
        # Codigo real (comentado momentaneamente para la simulacion)
        # self.trigger.value(0)
        # ...

    def set_motores(self, izquierda, derecha):
        """
        Placeholder para control de motores via PCA9685.
        izquierda/derecha: -100 a 100
        """
        # TODO: Implementar I2C y PCA9685
        pass
