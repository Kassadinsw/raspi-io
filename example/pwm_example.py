#!/usr/bin/env python3.5

from raspi_io import SoftPWM, GPIO


if __name__ == '__main__':
    address = ('192.168.1.166', 9876)
    pwm20 = SoftPWM(address, GPIO.BCM, 20, 500)
    pwm21 = SoftPWM(address, GPIO.BCM, 21, 1000)

    pwm21.start(100)
    pwm21.start(50)
    pwm21.start(10)

    pwm20.start(10)
    pwm20.start(50)
    pwm20.start(100)

    pwm20.stop()
    pwm21.stop()
