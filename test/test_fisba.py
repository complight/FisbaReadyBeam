import sys
import time
from FisbaReadyBeam import FisbaReadyBeam


def test():
    laser = FisbaReadyBeam(port='/dev/ttyUSB0')
    laser.set_laser([50., 50., 10.])
    time.sleep(5.)
    laser.set_laser([0, 0, 0])
    laser.close()
    assert True == True


if __name__ == '__main__':
    sys.exit(test())
