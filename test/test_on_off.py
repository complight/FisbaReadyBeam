import sys
import time
from FisbaReadyBeam import FisbaReadyBeam


def test():
    laser = FisbaReadyBeam(port='/dev/ttyUSB0')
    laser.set_brightness([10., 0., 0.])
    time.sleep(1.)
    laser.set_brightness([0., 10., 0.])
    time.sleep(1.)
    laser.set_brightness([0., 0., 10.])
    time.sleep(1.)
    laser.close()
    assert True == True


if __name__ == '__main__':
    sys.exit(test())
