from distutils.core import setup

setup(
    name='MPUdriver',
    version='.1',
    packages=['smbus','rpi.GPIO'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)