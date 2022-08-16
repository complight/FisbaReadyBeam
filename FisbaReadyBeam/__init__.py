import serial
import time
import struct
from crc import CrcCalculator, Crc16


class FisbaReadyBeam():
    """
    A class to control Fisba's ReadyBeam lasers.
    """
    device_errors = {
        1:  'Command not available',
        2:  'Device is busy',
        3:  'General communication error',
        4:  'Format error',
        5:  'Parameter not available',
        6:  'Parameter is read-only',
        7:  'Value is out of range',
        8:  'Instance is not available',
        9:  'Parameter general error. Device internal failure on this parameter'
    }
    device_status = {
        0:  'Init',
        1:  'Ready',
        2:  'Run',
        3:  'Error',
        4:  'Bootloader',
        5:  'Pending Reset'
    }

    def __init__(
                 self,
                 port='/dev/ttyUSB0',
                 baud=57600,
                 timeout=1,
                 address=0,
                 debug=0
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
        self.debug = debug
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
        self.get_device_status()
        command = self.construct_command(7000, value=1) # Enable digital control
        self.send_command(command)


    def close(self):
        """
        Internal function close the communication with the module.
        """
        command = self.construct_command(7000, value=0) # Disable digital control
        self.send_command(command)
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
                         Size of the read in bytes.
        
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
                            Command as string.

        Returns
        -------
        response_frame    : str
                            Response frame as string.
        """
        self.laser.reset_output_buffer()
        self.laser.reset_input_buffer()
        # Fill placeholder with sequence number
        self.sequence += 1
        command = command.replace('----', '{:04X}'.format(self.sequence))
        # Calculate checksum
        crc_calculator = CrcCalculator(Crc16.CCITT)
        checksum = crc_calculator.calculate_checksum(command.encode())
        command += '{:04X}'.format(checksum)
        command += '\r'
        # Send command and receive answer
        self.laser.write(command.encode())
        self.laser.flush()
        cr = "\r".encode()
        response_frame = b''
        response_byte = self.read(size=1)
        while response_byte != cr:
            response_frame += response_byte
            response_byte = self.read(size=1)
        response_frame = response_frame[1:] # Trim the hash caracter (#)
        response_frame = response_frame.decode()
        if self.debug >= 2:
            print('Sent command: ', command)
            print('Response:     ', response_frame)
        if response_frame[6] == '+': # Detect errors and raise Exception
            error_nr = int(response_frame[7:9])
            error = 'Error signaled by device: {0}, {1}'.format(error_nr, self.device_errors[error_nr])
            raise Exception(error)
        return response_frame


    def construct_command(self, parameter_id, value=None, instance=1):
        """
        Function to construct a command.

        Parameters
        ----------
        parameter_id       : int
                             Parameter identification (e.g., 7000, 7006). For more, see MeCom protocol specifications 5117c and communication protocol RGB-1171.
        value              : int
                             Value as an integer or a floating number. When no value pass, command will only query but not set anything.
        instance           : int
                             Instance channels (red:1, green:2, blue:3).

        Returns
        -------
        command            : str
                             Command as string.
        """
        command = '#{:02X}'.format(self.address)
        command += '----' # Insert placeholder for sequence number
        if isinstance(value, type(None)):
            command += '?VR'
        elif not isinstance(value, type(None)):
            command += 'VS'
        command += '{:04X}'.format(parameter_id)
        command += '{:02X}'.format(instance)
        if not isinstance(value, type(None)):
            if isinstance(value, float):
                command += '{:08X}'.format(struct.unpack('<I', struct.pack('<f', value))[0])
            elif isinstance(value, int):
                command += '{:08X}'.format(1)
        
        return command

    
    def set_brightness(self, power=[10., 0., 10.]):
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
            command = self.construct_command(7006, value=value, instance=int(i+1))
            self.send_command(command)
            command = self.construct_command(7013, value=power[i] * 1., instance=int(i+1))
            self.send_command(command)
        if self.debug >= 1:
            print('Power set to: ', power)
        if self.debug >= 2:
            command = self.construct_command(7010)
            print('Check if any laser is on: ', self.send_command(command))
            

    def get_device_status(self):
        """
        Function to get device status.

        Returns
        -------
        status_nr    :  int
                        Integer representing the device status. See device_status dictionary within this class for more.
        """
        command = self.construct_command(104) # Read ID 104 "Device Status"
        response = self.send_command(command)
        status_nr = int(response[13])
        if self.debug >= 1:
            print('Status of device: ', self.device_status[status_nr])
        return status_nr
