import machine

class MPU6050:
    """A lightweight, memory-efficient MicroPython driver for the MPU-6050 accelerometer/gyroscope."""
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Waking up the MPU-6050 as it starts in sleep mode by default (PWR_MGMT_1 register 0x6B set to 0)
        try:
            self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        except Exception as e:
            raise RuntimeError(f"Failed to wake up MPU-6050 at {hex(addr)}: {e}")

    def read_raw_data(self):
        """Reads 14 bytes of raw sensor data starting from ACCEL_XOUT_H (0x3B)."""
        return self.i2c.readfrom_mem(self.addr, 0x3B, 14)

    def get_values(self):
        """Reads the sensor registers and returns scaled acceleration, gyroscope, and temperature.
        
        Units:
        - accel: g (gravitational force, default scale +/- 2g, sensitivity 16384 LSB/g)
        - gyro: deg/s (degrees per second, default scale +/- 250 deg/s, sensitivity 131 LSB/deg/s)
        - temp: °C (degrees Celsius)
        """
        raw = self.read_raw_data()
        
        # Unpack 7 signed 16-bit big-endian integers
        vals = []
        for i in range(7):
            val = (raw[i*2] << 8) | raw[i*2 + 1]
            if val & 0x8000:
                val -= 65536
            vals.append(val)
            
        # Scaling calculations
        ax = vals[0] / 16384.0
        ay = vals[1] / 16384.0
        az = vals[2] / 16384.0
        
        # Temp formula per register map specification: (raw_temp / 340.0) + 36.53
        temp = (vals[3] / 340.0) + 36.53
        
        gx = vals[4] / 131.0
        gy = vals[5] / 131.0
        gz = vals[6] / 131.0
        
        return {
            'accel': {'x': round(ax, 3), 'y': round(ay, 3), 'z': round(az, 3)},
            'gyro': {'x': round(gx, 2), 'y': round(gy, 2), 'z': round(gz, 2)},
            'temp': round(temp, 1)
        }
