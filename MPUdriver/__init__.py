import smbus
import time
import RPi.GPIO as gpio


class MPUDriver(object):
    PWR_M          = 0x6B
    DIV            = 0x19
    CONFIG         = 0x1A
    GYRO_CONFIG    = 0x1B
    INT_EN         = 0x38
    ACCEL_X        = 0x3B
    ACCEL_Y        = 0x3D
    ACCEL_Z        = 0x3F
    GYRO_X         = 0x43
    GYRO_Y         = 0x45
    GYRO_Z         = 0x47
    TEMP           = 0x41
    Device_Address = 0x68
    AxCal = 0
    AyCal = 0
    AzCal = 0
    GxCal = 0
    GyCal = 0
    GzCal = 0
    RS = 18
    EN = 23
    D4 = 24
    D5 = 25
    D6 = 8
    D7 = 7

    def __init__(self):
        self.bus = smbus.SMBus(1)  
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.RS, gpio.OUT)
        gpio.setup(self.EN, gpio.OUT)
        gpio.setup(self.D4, gpio.OUT)
        gpio.setup(self.D5, gpio.OUT)
        gpio.setup(self.D6, gpio.OUT)
        gpio.setup(self.D7, gpio.OUT)
        self.context = {
            "tempC": 0,
            "tempF": 0,
            "Ax": 0,
            "Ay": 0,
            "Az": 0,
            "AxCal": 0,
            "AyCal": 0,
            "AzCal": 0,
            "Gx": 0,
            "Gy": 0,
            "Gz": 0,
            "GxCal": 0,
            "GyCal": 0,
            "GzCal": 0,
        }
        self.setup()
 
    def begin(self):
        self.cmd(0x33)
        self.cmd(0x32)
        self.cmd(0x06)
        self.cmd(0x0C) 
        self.cmd(0x28) 
        self.cmd(0x01) 
        time.sleep(0.0005)
        
    def setup(self):
        self.begin()
        self.InitMPU()
        self.calibrate()
 
    def cmd(self, ch): 
        gpio.output(self.RS, 0)
        gpio.output(self.D4, 0)
        gpio.output(self.D5, 0)
        gpio.output(self.D6, 0)
        gpio.output(self.D7, 0)
        if ch&0x10==0x10: gpio.output(self.D4, 1)
        if ch&0x20==0x20: gpio.output(self.D5, 1)
        if ch&0x40==0x40: gpio.output(self.D6, 1)
        if ch&0x80==0x80: gpio.output(self.D7, 1)
        gpio.output(self.EN, 1)
        time.sleep(0.005)
        gpio.output(self.EN, 0)

        # Low bits
        gpio.output(self.D4, 0)
        gpio.output(self.D5, 0)
        gpio.output(self.D6, 0)
        gpio.output(self.D7, 0)
        if ch&0x01==0x01: gpio.output(self.D4, 1)
        if ch&0x02==0x02: gpio.output(self.D5, 1)
        if ch&0x04==0x04: gpio.output(self.D6, 1)
        if ch&0x08==0x08: gpio.output(self.D7, 1)
        gpio.output(self.EN, 1)
        time.sleep(0.005)
        gpio.output(self.EN, 0)
    
    def write(self, ch): 
        gpio.output(self.RS, 1)
        gpio.output(self.D4, 0)
        gpio.output(self.D5, 0)
        gpio.output(self.D6, 0)
        gpio.output(self.D7, 0)
        if ch&0x10==0x10: gpio.output(self.D4, 1)
        if ch&0x20==0x20: gpio.output(self.D5, 1)
        if ch&0x40==0x40: gpio.output(self.D6, 1)
        if ch&0x80==0x80: gpio.output(self.D7, 1)
        gpio.output(self.EN, 1)
        time.sleep(0.005)
        gpio.output(self.EN, 0)
        # Low bits
        gpio.output(self.D4, 0)
        gpio.output(self.D5, 0)
        gpio.output(self.D6, 0)
        gpio.output(self.D7, 0)
        if ch&0x01==0x01: gpio.output(self.D4, 1)
        if ch&0x02==0x02: gpio.output(self.D5, 1)
        if ch&0x04==0x04: gpio.output(self.D6, 1)
        if ch&0x08==0x08: gpio.output(self.D7, 1)
        gpio.output(self.EN, 1)
        time.sleep(0.005)
        gpio.output(self.EN, 0)

    def clear(self):
        self.cmd(0x01)
   
    def InitMPU(self):
        self.bus.write_byte_data(self.Device_Address, self.DIV, 7)
        self.bus.write_byte_data(self.Device_Address, self.PWR_M, 1)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.Device_Address, self.INT_EN, 1)
        time.sleep(1)
 
    def readMPU(self, addr):
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)
        value = ((high << 8) | low)
        if(value > 32768):
            value = value - 65536
        return value

    def accel(self):
        x = self.readMPU(self.ACCEL_X)
        y = self.readMPU(self.ACCEL_Y)
        z = self.readMPU(self.ACCEL_Z)
        
        self.context["Ax"] = (x/16384.0-self.AxCal) 
        self.context["Ay"] = (y/16384.0-self.AyCal) 
        self.context["Az"] = (z/16384.0-self.AzCal)

    def gyro(self):
        x = self.readMPU(self.GYRO_X)
        y = self.readMPU(self.GYRO_Y)
        z = self.readMPU(self.GYRO_Z)
        self.context["Gx"] = x/131.0 - self.GxCal
        self.context["Gy"] = y/131.0 - self.GyCal
        self.context["Gz"] = z/131.0 - self.GzCal
 
    def temp(self):
        tempRow = self.readMPU(self.TEMP)
        tempC = (tempRow / 340.0) + 36.53
        # tempC = "%.2f" % tempC
        self.context["tempC"] = tempC
        self.context["tempF"] = tempC * (9/5) + 32
 
    def calibrate(self):
        self.clear()
        x = 0
        y = 0
        z = 0
        for _ in range(50):
            x = x + self.readMPU(self.ACCEL_X)
            y = y + self.readMPU(self.ACCEL_Y)
            z = z + self.readMPU(self.ACCEL_Z)
        x= x/50
        y= y/50
        z= z/50
        self.AxCal = x / 16384.0
        self.AyCal = y / 16384.0
        self.AzCal = z / 16384.0
        
        self.context["AxCal"] = self.AxCal
        self.context["AyCal"] = self.AyCal
        self.context["AzCal"] = self.AzCal
        ####################################
        x = 0
        y = 0
        z = 0
        for _ in range(50):
            x = x + self.readMPU(self.GYRO_X)
            y = y + self.readMPU(self.GYRO_Y)
            z = z + self.readMPU(self.GYRO_Z)
        x= x/50
        y= y/50
        z= z/50
        self.GxCal = x / 131.0
        self.GyCal = y / 131.0
        self.GzCal = z / 131.0
        
        self.context["GxCal"] = self.GxCal
        self.context["GyCal"] = self.GyCal
        self.context["GzCal"] = self.GzCal
        
    def self_test(self):
        print("Starting MPU6050 - RazPy Driver Test.")
        self.setup()
        self.temp(); self.clear()
        self.accel(); self.clear()
        self.gyro(); self.clear()
        for k, v in self.context.items():
            print(f"| {k}: {v:.2f}")
        print('That worked! -> Ruckusist.com <-')

    def __call__(self):
        self.temp(); self.clear()
        self.accel(); self.clear()
        self.gyro(); self.clear()
        return self.context


if __name__ == "__main__":
    mpu = MPUDriver()
    mpu.self_test()