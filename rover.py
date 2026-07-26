import machine
import time
import neopixel
import pca9685
import ssd1306
import uasyncio as asyncio
import array
import gc
import mpu6050

class Rover:
    def __init__(self):
        # Configuracion de pines segun especificaciones
        self.pixel = neopixel.NeoPixel(machine.Pin(48), 1)
        
        # Estado del módulo de audio (Buzzer) y tareas
        self.buzzer_busy = False
        self.last_warning_beep = 0
        self.active_turn_task = None
        self.active_sequence_task = None
        
        # Parámetros de velocidad y estado de secuencias
        self.speed_m_s = 0.35
        self.global_speed_pct = 80
        self.sequence_status = {
            "running": False,
            "step": 0,
            "total": 0,
            "action": "",
            "message": "Inactivo"
        }
        
        # Inicialización del bus I2C, PCA9685 y SSD1306
        self.pca_ready = False
        self.oled_ready = False
        
        try:
            self.i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
            
            # PCA9685
            self.pca = pca9685.PCA9685(self.i2c, 0x40)
            self.pca.freq(50) # Frecuencia típica para control de servos y PWM motores
            self.pca_ready = True
            self.current_servo_angle = 0
            self.set_servo_angle_direct(0) # Centrar servo al arrancar
            self.apagar_servo()
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

        # Recolectar basura acumulada durante la inicialización de drivers
        gc.collect()
        print(f"Rover inicializado. RAM libre: {gc.mem_free()} bytes")

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
        Nota: El motor izquierdo tiene polaridad invertida en cableado respecto al derecho.
        """
        self._controlar_motor(0, 1, izquierda, brake)
        self._controlar_motor(2, 3, derecha, brake)

    def apagar_servo(self):
        """Desactiva el pulso PWM del servo para liberar corriente y evitar calentamiento/stall."""
        if self.pca_ready:
            try:
                self.pca.duty(4, 0)
            except Exception:
                pass

    def set_servo_angle_direct(self, angle):
        """Establece el ángulo del servo directamente (-85 a 85 grados)."""
        if not self.pca_ready:
            return
        angle = max(-85, min(85, angle))
        duty_center = 307
        duty_range = 145 # Rango seguro acotado (~0.8ms a ~2.2ms)
        duty = int(duty_center + (angle / 90.0) * duty_range)
        try:
            self.pca.duty(4, duty)
            self.current_servo_angle = angle
        except Exception as e:
            print("Error I2C en set_servo_angle:", e)

    def set_servo_angle(self, angle):
        """Compatibilidad síncrona."""
        self.set_servo_angle_direct(angle)

    async def set_servo_angle_smooth(self, target_angle):
        """Mueve el servo gradualmente en pasos para evitar picos de corriente (stall/brownout)."""
        if not self.pca_ready:
            return
            
        target_angle = max(-85, min(85, target_angle))
        start_angle = getattr(self, 'current_servo_angle', 0)
        
        if start_angle == target_angle:
            self.set_servo_angle_direct(target_angle)
            await asyncio.sleep_ms(100)
            self.apagar_servo()
            return

        step = 5 if target_angle > start_angle else -5
        curr = start_angle
        
        if step > 0:
            while curr < target_angle:
                curr = min(curr + step, target_angle)
                self.set_servo_angle_direct(curr)
                await asyncio.sleep_ms(15)
        else:
            while curr > target_angle:
                curr = max(curr + step, target_angle)
                self.set_servo_angle_direct(curr)
                await asyncio.sleep_ms(15)
                
        await asyncio.sleep_ms(150)
        self.apagar_servo()

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
        self.set_motores(40, -40) # Reversa segura considerando polaridad
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
        
        # 1. Escaneo preventivo suave del sonar (Look-Before-Turn)
        servo_angle = 85 if target_angle > 0 else -85
        await self.set_servo_angle_smooth(servo_angle)
        
        # Sensar durante 3 segundos en la dirección del giro para detectar obstáculos
        dist_min = -1
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:
            dist_lectura = self.medir_distancia()
            if dist_lectura > 0:
                if dist_min == -1 or dist_lectura < dist_min:
                    dist_min = dist_lectura
            await asyncio.sleep_ms(100)
            
        dist = dist_min
        print(f"Distancia mínima leída en pre-escaneo de 3s en {servo_angle}°: {dist} cm")
        
        if 0 < dist <= 15.0:
            print("Trayectoria de giro obstruida! Avanzando 30cm para despejar...")
            await self.set_servo_angle_smooth(0) # Centrar servo
            await self.beep(duration_ms=200)
            clear = await self.avanzar_distancia_suave(0.30, target_speed=50)
            if not clear:
                print("Obstáculo frontal detectado al avanzar. Abortando giro.")
                return False
            print("Re-evaluando trayectoria de giro...")
            return await self.girar_grados(target_angle)
            
        # Trayectoria libre, centramos el servo para monitorear el frente durante el giro
        await self.set_servo_angle_smooth(0)
        
        # 2. Calibración rápida en estático
        offset_z = await self.tomar_offset_gyro_z()
        print(f"Offset Z de guiñada establecido en: {offset_z:.2f} deg/s")
        
        # 3. Arrancar motores según giro diferencial y polaridad física
        # Giro a la izquierda: motor izquierdo atr/der ad -> (50, 50)
        # Giro a la derecha: motor izquierdo ad/der atr -> (-50, -50)
        if target_angle > 0:
            self.set_motores(50, 50)
        else:
            self.set_motores(-50, -50)
            
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
        return True

    async def avanzar_distancia_suave(self, distancia_m, target_speed=None):
        """Avanza la distancia indicada en metros utilizando una rampa de desaceleración suave al detectar obstáculos (50cm a 10cm)."""
        if target_speed is None:
            target_speed = self.global_speed_pct
        target_speed = max(30, min(100, target_speed))
        
        duracion_ms = int(((distancia_m / self.speed_m_s) * (80.0 / target_speed)) * 1000)
        print(f"Avanzando {distancia_m}m a {target_speed}% Vel (Tiempo est: {duracion_ms}ms)")
        
        start_time = time.ticks_ms()
        try:
            while time.ticks_diff(time.ticks_ms(), start_time) < duracion_ms:
                dist = self.medir_distancia()
                
                if 0 < dist <= 10.0:
                    print(f"¡Obstáculo crítico detectado a {dist}cm! Deteniendo avance.")
                    self.set_motores(0, 0, brake=True)
                    await self.beep(duration_ms=300)
                    return False # Abortado por obstáculo
                    
                if 10.0 < dist <= 50.0:
                    # Rampa de desaceleración proporcional entre 50cm y 10cm
                    factor = (dist - 10.0) / 40.0
                    current_speed = int(30 + (target_speed - 30) * factor)
                else:
                    current_speed = target_speed
                    
                self.set_motores(-current_speed, current_speed)
                await asyncio.sleep_ms(20)
        finally:
            self.set_motores(0, 0, brake=True)
            
        return True

    async def retroceder_distancia(self, distancia_m, target_speed=None):
        """Retrocede la distancia indicada en metros a la velocidad configurada."""
        if target_speed is None:
            target_speed = self.global_speed_pct
        target_speed = max(30, min(100, target_speed))
        
        duracion_ms = int(((distancia_m / self.speed_m_s) * (80.0 / target_speed)) * 1000)
        print(f"Retrocediendo {distancia_m}m a {target_speed}% Vel (Tiempo est: {duracion_ms}ms)")
        
        self.set_motores(target_speed, -target_speed)
        await asyncio.sleep_ms(duracion_ms)
        self.set_motores(0, 0, brake=True)
        return True

    async def ejecutar_calibracion_5s(self, power_pct=80):
        """Avanza durante 5.0s continuos a power_pct para permitir la medición empírica de velocidad."""
        print(f"Iniciando prueba de calibración de velocidad (5s a {power_pct}%)...")
        start_time = time.ticks_ms()
        try:
            while time.ticks_diff(time.ticks_ms(), start_time) < 5000:
                dist = self.medir_distancia()
                if 0 < dist <= 10.0:
                    print(f"Obstáculo detectado a {dist}cm durante prueba de calibración.")
                    self.set_motores(0, 0, brake=True)
                    await self.beep(duration_ms=300)
                    return False
                self.set_motores(-power_pct, power_pct)
                await asyncio.sleep_ms(20)
        finally:
            self.set_motores(0, 0, brake=True)
        await self.beep(duration_ms=200)
        return True

    async def ejecutar_secuencia(self, steps, calibration_speed=None, global_speed=None):
        """Ejecuta una secuencia programada de hasta N pasos asíncronos."""
        if calibration_speed and calibration_speed > 0:
            self.speed_m_s = calibration_speed
        if global_speed and global_speed > 0:
            self.global_speed_pct = global_speed
            
        total_steps = len(steps)
        self.sequence_status = {
            "running": True,
            "step": 0,
            "total": total_steps,
            "action": "START",
            "message": f"Iniciando secuencia ({total_steps} pasos)..."
        }
        print(f"Ejecutando secuencia: {steps}")
        
        try:
            for i, step in enumerate(steps):
                step_num = i + 1
                action = step.get('action', '')
                val = float(step.get('val', 0))
                speed = step.get('speed', None)
                if speed is None or speed == "" or speed == "auto":
                    speed = self.global_speed_pct
                else:
                    speed = int(speed)
                    
                self.sequence_status = {
                    "running": True,
                    "step": step_num,
                    "total": total_steps,
                    "action": action,
                    "message": f"Paso {step_num}/{total_steps}: {action} ({val}) [{speed}% Vel]"
                }
                print(f"Paso {step_num}/{total_steps}: {action} {val} (Vel: {speed}%)")
                
                success = True
                if action == 'FORWARD':
                    success = await self.avanzar_distancia_suave(val, target_speed=speed)
                elif action == 'BACKWARD':
                    success = await self.retroceder_distancia(val, target_speed=speed)
                elif action == 'TURN_LEFT':
                    success = await self.girar_grados(90)
                elif action == 'TURN_RIGHT':
                    success = await self.girar_grados(-90)
                elif action == 'PAUSE':
                    await asyncio.sleep(val)
                else:
                    print(f"Acción no reconocida en paso {step_num}: {action}")
                    
                if success is False:
                    print(f"Paso {step_num} abortado por obstáculo o falla.")
                    self.sequence_status = {
                        "running": False,
                        "step": step_num,
                        "total": total_steps,
                        "action": action,
                        "message": f"⚠️ ABORTADO en paso {step_num} ({action})"
                    }
                    return False
                    
                await asyncio.sleep_ms(200) # Pausa mecánica entre pasos
                
            self.sequence_status = {
                "running": False,
                "step": total_steps,
                "total": total_steps,
                "action": "DONE",
                "message": "🏁 Secuencia completada con éxito!"
            }
            await self.beep(duration_ms=100)
            await asyncio.sleep_ms(100)
            await self.beep(duration_ms=100)
            return True
        except asyncio.CancelledError:
            print("Secuencia cancelada por el usuario.")
            self.set_motores(0, 0, brake=True)
            self.sequence_status = {
                "running": False,
                "step": 0,
                "total": total_steps,
                "action": "CANCELLED",
                "message": "⏹ Secuencia cancelada por el usuario"
            }
            return False
        except Exception as e:
            print(f"Error ejecutando secuencia: {e}")
            self.set_motores(0, 0, brake=True)
            self.sequence_status = {
                "running": False,
                "step": 0,
                "total": total_steps,
                "action": "ERROR",
                "message": f"Error: {e}"
            }
            return False
        finally:
            self.set_motores(0, 0, brake=True)

    async def abortar_secuencia(self):
        """Detiene cualquier secuencia o giro en ejecución inmediatamente."""
        if self.active_sequence_task and not self.active_sequence_task.done():
            print("Cancelando tarea de secuencia activa...")
            self.active_sequence_task.cancel()
            self.active_sequence_task = None
        if self.active_turn_task and not self.active_turn_task.done():
            self.active_turn_task.cancel()
            self.active_turn_task = None
        self.set_motores(0, 0, brake=True)
        self.sequence_status = {
            "running": False,
            "step": 0,
            "total": 0,
            "action": "ABORTED",
            "message": "⏹ Secuencia abortada"
        }
        await self.beep(duration_ms=200)
