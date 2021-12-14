import serial
import os


class SerialWrapper:
    def __init__(self, mac_address, port):
        self.mac_address = mac_address
        self.port = port
        os.system(f'sudo rfcomm bind rfcomm{self.port} {self.mac_address}')
        self.ser = serial.Serial(f'/dev/rfcomm{self.port}')

    def __del__(self):
        self.ser.close()
        os.system(f'sudo rfcomm unbind rfcomm{self.port} {self.mac_address}')

    def readline(self):
        output = None
        try:
            output = self.ser.readline().decode().strip()
        except:
            return None
        else:
            return output
