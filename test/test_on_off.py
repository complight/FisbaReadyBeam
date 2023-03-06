import sys
import time
from FisbaReadyBeam import FisbaReadyBeam


def test():
    laser = FisbaReadyBeam(port='/dev/ttyUSB0')
    laser.set_brightness([5., 0., 0.])
    time.sleep(3.)
    laser.set_brightness([0., 5., 0.])
    time.sleep(3.)
    laser.set_brightness([0., 0., 5.])
    time.sleep(3.)
    laser.close()
    assert True == True


if __name__ == '__main__':
    sys.exit(test())
