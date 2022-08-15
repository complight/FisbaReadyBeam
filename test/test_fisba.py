import sys
import time
from FisbaReadyBeam import FisbaReadyBeam


def test():
    laser = FisbaReadyBeam(port='/dev/ttyUSB0')
    for i in range(30):
        laser.set_brightness([0., 0., i * 1.])
    time.sleep(1.)
    for i in range(30):
        laser.set_brightness([0., i * 1., 0.])
    time.sleep(1.)
    for i in range(30):
        laser.set_brightness([i * 1., 0., 0.])
    time.sleep(1.)
    laser.set_brightness([0, 0, 0])
    laser.close()
    assert True == True


if __name__ == '__main__':
    sys.exit(test())
