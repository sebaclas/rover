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
        self.active_turn_task = None
        
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
            
            # 3. Medir el ancho de pulso en ECHO (timeout acotado a 15000us ~ 2.5 metros)
            duration = machine.time_pulse_us(self.echo, 1, 15000)
            
            if duration < 0:
                return -1 # Timeout o error de lectura
            
            # 4. Calcular distancia en cm: (tiempo_us * velocidad_sonido_cm_us) / 2
            distancia = (duration * 0.0343) / 2
            
            # El sensor tiene un rango útil de 2cm a 250cm
            if 2.0 <= distancia <= 250.0:
                return round(distancia, 2)
            else:
                return -1 # Fuera de rango
        except Exception:
            return -1

    def _controlar_motor(self, in1_ch, in2_ch, speed, brake=True):
        if not self.pca_ready:
            return
        
        # Convierte speed (-100 a 100) a duty cycle (0 a 4095)
        duty = int(min(max(abs(speed) / 100.0, 0.0), 1.0) * 4095)
        
        if speed > 0:
            self.pca.duty(in1_ch, duty)
            self.pca.duty(in2_ch, 0)
        elif speed < 0:
            self.pca.duty(in1_ch, 0)
            self.pca.duty(in2_ch, duty)
        else:
            if brake:
                self.pca.duty(in1_ch, 4095)
                self.pca.duty(in2_ch, 4095)
            else:
                self.pca.duty(in1_ch, 0)
                self.pca.duty(in2_ch, 0)

    def set_motores(self, izquierda, derecha, brake=True):
        """
        Control de motores DC utilizando puente H DRV8833 en PCA9685.
        Canales:
          - Motor Izquierdo: Canal 0 (IN1), Canal 1 (IN2)
          - Motor Derecho: Canal 2 (IN3), Canal 3 (IN4)
        izquierda/derecha: velocidad de -100 a 100
        """
        self._controlar_motor(0, 1, izquierda, brake)
        self._controlar_motor(2, 3, derecha, brake)

    def set_servo_angle(self, angle):
        """
        Gira el servo del HC-SR04 al ángulo especificado (-85 a 85 grados).
        """
        if not self.pca_ready:
            return
            
        # Limitar ángulo de seguridad para evitar tope mecánico de SG90
        angle = max(-85, min(85, angle))
        
        # Para 50Hz (20ms periodo), 12-bits = 4096 pasos.
        # Rango acotado para prevenir stall de corriente
        duty_center = 307
        duty_range = 175
        
        duty = int(duty_center + (angle / 90.0) * duty_range)
        try:
            self.pca.duty(4, duty) # Usamos el Canal 4 para el servo
        except Exception as e:
            print("Error I2C en set_servo_angle:", e)

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

    async def tomar_offset_gyro_z(self):
        """Toma una media rápida (10 muestras en 50ms) para calcular el offset de Gyro Z estando estático."""
        if not self.mpu_ready or self.mpu is None:
            return 0.0
        
        suma = 0.0
        muestras_validas = 0
        for _ in range(10):
            imu_data = self.leer_imu()
            if imu_data and 'gyro' in imu_data:
                suma += imu_data['gyro']['z']
                muestras_validas += 1
            await asyncio.sleep_ms(5)
            
        if muestras_validas > 0:
            offset = suma / muestras_validas
            # Si el offset es anormalmente alto, descartamos por seguridad
            if abs(offset) > 15.0:
                print(f"Advertencia: Offset Gyro Z anormal ({offset:.2f} deg/s). Descartado.")
                return 0.0
            return offset
        return 0.0

    async def retroceder_distancia_segura(self):
        """Retrocede el rover aproximadamente 10cm de forma temporizada y segura."""
        print("Retrocediendo por seguridad...")
        self.set_motores(-40, -40)
        await asyncio.sleep_ms(600)  # ~10cm estimado por tiempo a 40%
        self.set_motores(0, 0, brake=True)
        await asyncio.sleep_ms(200)  # Estabilización

    async def girar_grados(self, target_angle):
        """
        Ejecuta un giro controlado por giroscopio de N grados (positivo Izq, negativo Der).
        Antes de girar, escanea la dirección con el servo del sonar.
        Monitorea el sonar de frente durante el giro para paradas de emergencia.
        """
        print(f"Iniciando secuencia de giro: {target_angle} grados")
        
        # 1. Escaneo preventivo del sonar (Look-Before-Turn)
        # Apuntar el servo: +85° si es giro a la izquierda, -85° si es a la derecha
        servo_angle = 85 if target_angle > 0 else -85
        self.set_servo_angle(servo_angle)
        await asyncio.sleep_ms(300) # Esperar a que el servo se posicione
        
        dist = self.medir_distancia()
        print(f"Distancia leída por pre-escaneo en {servo_angle}°: {dist} cm")
        
        if 0 < dist <= 15.0:
            print("Trayectoria de giro obstruida! Iniciando evasión...")
            self.set_servo_angle(0) # Centrar servo
            await asyncio.sleep_ms(200)
            await self.beep(duration_ms=200)
            await self.retroceder_distancia_segura()
            print("Reintentando giro completo...")
            return await self.girar_grados(target_angle)
            
        # Trayectoria libre, centramos el servo para monitorear el frente durante el giro
        self.set_servo_angle(0)
        await asyncio.sleep_ms(200)
        
        # 2. Calibración rápida en estático
        offset_z = await self.tomar_offset_gyro_z()
        print(f"Offset Z de guiñada establecido en: {offset_z:.2f} deg/s")
        
        # 3. Arrancar motores
        # Giro a la izquierda: motor izquierdo atrás, motor derecho adelante
        # Giro a la derecha: motor izquierdo adelante, motor derecho atrás
        if target_angle > 0:
            self.set_motores(-60, 60)
        else:
            self.set_motores(60, -60)
            
        angulo_acumulado = 0.0
        last_time = time.ticks_us()
        
        try:
            # 4. Lazo de Integración del Giroscopio a 50Hz (20ms)
            while abs(angulo_acumulado) < abs(target_angle):
                await asyncio.sleep_ms(20)
                
                # Monitoreo frontal del sonar (Parada de emergencia si algo se cruza en el barrido)
                dist_front = self.medir_distancia()
                if 0 < dist_front <= 10.0:
                    print(f"Obstáculo frontal detectado durante rotación ({dist_front} cm). Abortando!")
                    self.set_motores(0, 0, brake=True)
                    await self.beep(duration_ms=300)
                    await self.retroceder_distancia_segura()
                    print("Reintentando giro completo...")
                    return await self.girar_grados(target_angle)
                
                # Integración temporal del ángulo
                now = time.ticks_us()
                dt = time.ticks_diff(now, last_time) / 1000000.0
                last_time = now
                
                imu_data = self.leer_imu()
                if imu_data and 'gyro' in imu_data:
                    gz_corregido = imu_data['gyro']['z'] - offset_z
                    angulo_acumulado += gz_corregido * dt
                    
        finally:
            # Asegurar parada de motores
            self.set_motores(0, 0, brake=True)
            
        print(f"Giro completado con éxito. Ángulo final integrado: {angulo_acumulado:.2f}°")
        await self.beep(duration_ms=100)
