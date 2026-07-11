import machine
import time
import neopixel
import pca9685
import ssd1306
import uasyncio as asyncio
import array

class Rover:
    def __init__(self):
        # Configuracion de pines segun especificaciones
        self.pixel = neopixel.NeoPixel(machine.Pin(48), 1)
        
        # Estado del módulo de audio (Buzzer)
        self.buzzer_busy = False
        self.last_warning_beep = 0
        
        # Inicialización del bus I2C, PCA9685 y SSD1306
        self.pca_ready = False
        self.oled_ready = False
        
        try:
            self.i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
            
            # PCA9685
            self.pca = pca9685.PCA9685(self.i2c, 0x40)
            self.pca.freq(50) # Frecuencia típica para control de servos y PWM motores
            self.pca_ready = True
            self.set_servo_angle(0) # Centrar servo al arrancar
            print("PCA9685 inicializado en I2C.")
        except Exception as e:
            print("Error inicializando PCA9685:", e)

        try:
            # SSD1306 OLED (128x64)
            self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=0x3C)
            self.oled.fill(0)
            self.oled.show()
            self.oled_ready = True
            print("SSD1306 OLED inicializado en I2C (0x3C).")
        except Exception as e:
            print("Error inicializando SSD1306 OLED:", e)

        # MPU-6050 Accelerometer/Gyroscope
        self.mpu_ready = False
        self.mpu = None
        if hasattr(self, 'i2c'):
            try:
                import mpu6050
                self.mpu = mpu6050.MPU6050(self.i2c, addr=0x68)
                self.mpu_ready = True
                print("MPU-6050 inicializado en I2C (0x68).")
            except Exception as e:
                print("Error inicializando MPU-6050:", e)

        # Estado inicial del LED (apagado)
        self.set_led(0, 0, 0)
        
        # Inicialización del sensor ultrasónico (Trig/Echo GPIO)
        self.trig = machine.Pin(9, machine.Pin.OUT)
        self.echo = machine.Pin(10, machine.Pin.IN)
        self.trig.off()
        
    def set_led(self, r, g, b):
        """Controla el NeoPixel integrado (RGB)."""
        self.pixel[0] = (r, g, b)
        self.pixel.write()

    def medir_distancia(self):
        """Mide la distancia usando el sensor ultrasónico en modo GPIO (Trig/Echo)."""
        try:
            # 1. Asegurar TRIG en bajo
            self.trig.off()
            time.sleep_us(2)
            # 2. Enviar pulso de disparo de 10us
            self.trig.on()
            time.sleep_us(10)
            self.trig.off()
            
            # 3. Medir el ancho de pulso en ECHO (timeout de 30000us ~ 5 metros)
            duration = machine.time_pulse_us(self.echo, 1, 30000)
            
            if duration < 0:
                return -1 # Timeout o error de lectura
            
            # 4. Calcular distancia en cm: (tiempo_us * velocidad_sonido_cm_us) / 2
            distancia = (duration * 0.0343) / 2
            
            # El sensor tiene un rango útil de 2cm a 400cm
            if 2.0 <= distancia <= 400.0:
                return round(distancia, 2)
            else:
                return -1 # Fuera de rango
        except Exception:
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
        # Servo SG90 (Rango Extendido):
        # El límite teórico es ~102 a ~512, pero usamos un rango ligeramente menor (195)
        # para evitar el tope físico mecánico que ocasiona vibración en los extremos.
        duty_center = 307
        duty_range = 195
        
        duty = int(duty_center + (angle / 90.0) * duty_range)
        self.pca.duty(4, duty) # Usamos el Canal 4 para el servo

    async def beep(self, freq=None, duration_ms=100):
        """Genera un pitido asíncrono y no bloqueante en el buzzer activo (GPIO 16).
        El parámetro freq se conserva por compatibilidad de firma pero se ignora.
        """
        if self.buzzer_busy:
            return
        self.buzzer_busy = True
        try:
            buzzer = machine.Pin(16, machine.Pin.OUT)
            buzzer.on()
            await asyncio.sleep_ms(duration_ms)
            buzzer.off()
        except Exception as e:
            print("Error en buzzer:", e)
        finally:
            self.buzzer_busy = False

    def leer_imu(self):
        """Lee los valores de telemetría del MPU-6050. Devuelve None si no está listo o falla."""
        if not self.mpu_ready or self.mpu is None:
            return None
        try:
            return self.mpu.get_values()
        except Exception as e:
            print("Error al leer MPU-6050:", e)
            return None
