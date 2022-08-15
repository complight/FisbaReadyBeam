import serial
import time
from PyCRC.CRCCCITT import CRCCCITT


class FisbaReadyBeam():
    """
    A class to control Fisba's ReadyBeam lasers.
    """

    def __init__(
                 self,
                 port='/dev/ttyUSB0',
                 baud=57600,
                 timeout=1,
                 address=0,
                ):
        """
        Parameters
        ----------
        port           : str
                         Communication port.
        baud           : int
                         Communication baudrate.
        timeout        : float
                         Communication time out duration in seconds while sending and receiving.
        address        : int
                         Communication address.
        """
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.address = address
        self.sequence = 0
        self.open()


    def open(self):
        """
        Internal function to start the communication link with the module.
        """
        self.laser = serial.Serial(
                                   self.port,
                                   self.baud,
                                   timeout=self.timeout,
                                   write_timeout=self.timeout
                                  )
        self.laser.flushInput()
        self.laser.flushOutput()
        command = self.construct_command(2010)
        self.send_command(command)


    def close(self):
        """
        Internal function close the communication with the module.
        """
        self.laser.flushInput()
        self.laser.flushOutput()
        self.laser.close()
        del self.laser


    def read(self, size=1):
        """
        Internal function to read data.

        Parameters
        ----------
        size           : int
                         Size of the ready in bytes.
        
        Returns
        -------
        incoming_data  : str
                         Incoming data.
        """
        incoming_data = self.laser.read(size=size)
        if len(incoming_data) < size:
            raise Exception('Communication timed out.')
        else:
            return incoming_data


    def send_command(self, command):
        """
        Function to send command to the module.

        Parameters
        ----------
        command           : str
                            Command as an encoded string.

        Returns
        -------
        response_frame    : str
                            Response frame as an encoded string.
        """
        self.laser.reset_output_buffer()
        self.laser.reset_input_buffer()
        self.laser.write(command)
        self.laser.flush()
        cr = "\r".encode()
        response_frame = b''
        response_byte = self.read(size=1)
        while response_byte != cr:
            response_frame += response_byte
            response_byte = self.read(size=1)
        response_frame = response_frame[1:]
#        time.sleep(0.005)
#        print(command.decode())
#        print(response_frame.decode())
        return response_frame


    def construct_command(self, parameter_id, value=None, instance=1):
        """
        Function to construct a command.

        Parameters
        ----------
        parameter_id       : int
                             Parameter identification (e.g., 7000, 7006). For more, see MeCom protocol specifications 5117c.
        value              : int
                             Value as an integer or a floating number. When no value pass, command will only query but not set anything.
        instance           : int
                             Instance channels (red:1, green:2, blue:3).

        Returns
        -------
        command            : str
                             Command as an encoded string.
        """
        command = '#{:02X}'.format(self.address)
        self.sequence += 1
        command += '{:04X}'.format(self.sequence)
        if isinstance(value, type(None)):
            command += '?VR'
        elif not isinstance(value, type(None)):
            command += 'VS'
        command += '{:04X}'.format(parameter_id)
        command += '{:02X}'.format(instance)
        if not isinstance(value, type(None)):
            if isinstance(value, float):
                if value == 0:
                    converted_value = '00000000'
                else:
                    converted_value = '41F00000'
                command += converted_value
#                command += '{:08X}'.format(converted_value) 
            elif isinstance(value, int):
                command += '{:08X}'.format(1)
        checksum = CRCCCITT().calculate(input_data=command.encode())
        command += '{:04X}'.format(checksum)
        command += '\r'
        return command.encode()

    
    def set_laser(self, power=[10., 0., 10.]):
        """
        Function to set laser powers.

        Parameters
        ----------
        power          : list
                         Laser powers set in percentage using floating numbers. Maximum percentage is 100.5 percent.
        """
        if power[power!=0] > 0:
            val = 1
        else:
            val = 0
        for i in range(len(power)):
            if power[i] > 0:
                value = 1
            else:
                value = 0
            command = self.construct_command(7000, value=1, instance=int(i+1))
            self.send_command(command)
            command = self.construct_command(7006, value=value, instance=int(i+1))
            self.send_command(command)
            command = self.construct_command(7013, value=power[i], instance=int(i+1))
            self.send_command(command)
            command = self.construct_command(7010, instance=int(i+1))
            self.send_command(command)
