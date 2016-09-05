#CreazyLeapController

This project is a weekend hobby project. The goal of the project is to control the nano-scale quadcopter named
[Crazyflie 2.0](https://www.bitcraze.io/crazyflie-2/) with a gesture based [leap motion controller](https://www.leapmotion.com/).

The main control strategy used in the project is to utilise human palm's orientation and vertical position to control the movement of the
quadcopter, more precisely, the yaw, row and pitch value of the palm is fed directly to the quadcopter through a long range  USB dongle. The
height of the plam relative to the leap motion device is scaled up and used as the thrust value of the quadcopter.

##Libraries used:
1. Python [Crazyflie open source library](https://github.com/bitcraze/crazyflie-lib-python) (cflib)
2. Official [Leap Motion python library](https://developer.leapmotion.com/v2). Note that, as the time this project was developed, the official leap library only supports python 2.7,
custom build is needed in order to make it compatible with python 3.x. More detailed information is available on Leap Motion's official website.