MPUdriver.

This is a MPU6050 connected to a raspberry pi.

Raspi Setup:

Install I2cdetect
Enable i2c in the /boot/config.txt.
Use i2cdetect to confirm x68 is correctly shown.

Python setup:
sudo pip install MPUdriver

or clone this repo:
git clone https://github.com/Ruckusist/MPU6050driver
cd MPU6050driver
sudo pip install .
sudo python examples/test.py

Useage:
from MPUdriver import MPUDriver as mpu
mpu = mpu()
# print(mpu())
mpu.self_test()