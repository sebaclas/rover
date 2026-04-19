import ustruct
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        # Despertar y reset
        self.i2c.writeto_mem(self.address, 0x00, b'\x30')
        time.sleep_ms(1)
        # MODE2: Salida en Totem pole (necesario para drivers y servos)
        self.i2c.writeto_mem(self.address, 0x01, b'\x04')
        # MODE1: Auto-incremento activado, AllCall habilitado
        self.i2c.writeto_mem(self.address, 0x00, b'\xa1')
        time.sleep_ms(1)
        # Apagar todos los canales inicializados
        for i in range(16):
            self.duty(i, 0)

    def freq(self, freq=None):
        if freq is None:
            prescale = self.i2c.readfrom_mem(self.address, 0xfe, 1)[0]
            if prescale == 0:
                prescale = 3 # Evitar division por cero, por default es bajo
            return int(25000000.0 / 4096.0 / prescale)
        
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        self.i2c.writeto_mem(self.address, 0x00, bytes([(old_mode & 0x7F) | 0x10])) # sleep mode
        self.i2c.writeto_mem(self.address, 0xfe, bytes([prescale])) # escribir prescale
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode])) # reactivar
        time.sleep_ms(1)
        self.i2c.writeto_mem(self.address, 0x00, bytes([old_mode | 0x80])) # reiniciar logic

    def pwm(self, index, on=None, off=None):
        """Ajusta o lee los registros brutos ON y OFF de 12 bits"""
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index, data)

    def duty(self, index, value=None):
        """Ajusta o lee el ciclo de trabajo de 0 a 4095"""
        if value is None:
            pwm_val = self.pwm(index)
            if pwm_val == (0, 4096):
                return 0 # Totalmente apagado (apagado se enciende en on=0, delay=4096)
            elif pwm_val == (4096, 0):
                return 4095 # Totalmente encendido
            return pwm_val[1]
            
        if not 0 <= value <= 4095:
            raise ValueError("Rango fuera de limites (0-4095)")
        
        if value == 0:
            self.pwm(index, 0, 4096) # Bit 4 on (OFF register)
        elif value == 4095:
            self.pwm(index, 4096, 0) # Bit 4 on (ON register)
        else:
            self.pwm(index, 0, value)
