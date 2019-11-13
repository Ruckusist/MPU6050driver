from distutils.core import setup
import setuptools

import os

setup(
    name='MPUdriver',
    author="Ruckusist",
    author_email="eric.alphagriffin@gmail.com",
    url="https://github.com/Ruckusist/MPU6050driver",
    version='0.1.2',
    # packages=['MPUdriver', 'smbus', 'rpi.GPIO'],
    packages=setuptools.find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)