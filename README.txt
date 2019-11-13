MPUdriver.

This is a MPU6050 connected to a raspberry pi.

Raspi Setup:

Install I2cdetect
Enable i2c in the /boot/config.txt.
Use i2cdetect to confirm x68 is correctly shown.

Python setup:

import MPUdriver as mpu
mpu = mpu()  #=> lol.
mpu()        #=>